import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from src.services.nft_service import NFTService
from src.services.redis_service import redis_service
from src.services.reputation_service import reputation_service
from src.schemas.models import DelegateAccessRequest, MintNFTRequest

async def latency_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    response.headers["X-API-Latency"] = str(latency)
    return response

app = FastAPI()
# app.add_middleware(latency_middleware)
app.middleware("http")(latency_middleware) 

nft_service = NFTService()

@app.on_event("startup")
async def startup_event():
    """Conecta ao Redis quando a aplicação inicia"""
    await redis_service.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Desconecta do Redis quando a aplicação termina"""
    await redis_service.disconnect()

def measure_chain_latency(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        kwargs["chain_latency"] = time.time() - start  # Adiciona ao contexto
        return result
    return wrapper

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erro interno: {str(exc)}"},
    )

@app.post("/mint-nft")
async def mint_nft(request: MintNFTRequest):
    tx_hash = nft_service.mint_nft(
        request.recipient,
        request.token_uri
    )
    return {"tx_hash": tx_hash}

@app.get("/access/{token_id}/{user}")
async def check_access(token_id: int, user: str):
    # 1. Verifica se o usuário está banido
    if await reputation_service.is_banned(user):
        ttl = await reputation_service.get_ban_ttl(user)
        raise HTTPException(
            status_code=429, 
            detail=f"Too Many Requests. You are temporarily blocked. Try again in {ttl} seconds."
        )

    # 2. Consulta o Smart Contract
    has_access = nft_service.check_access(token_id, user)

    # 3. Atualiza a reputação
    if has_access:
        await reputation_service.update_reputation_on_success(user)
    else:
        await reputation_service.update_reputation_on_failure(user)

    if not has_access:
        raise HTTPException(status_code=403, detail="Access denied by Smart Contract.")

    return {"has_access": has_access}

@app.get("/access-details/{token_id}")
async def get_access_details(token_id: int):
    return nft_service.get_access_details(token_id)

@app.post("/delegate-access")
async def delegate_access(request: DelegateAccessRequest):
    tx_hash = nft_service.delegate_access(
        request.token_id,
        request.delegatee,
        request.duration
    )
    return {"tx_hash": tx_hash}

@app.post("/revoke-access/{token_id}")
async def revoke_access(token_id: int):
    tx_hash = nft_service.revoke_access(token_id)
    return {"tx_hash": tx_hash}

# ====== REDIS ENDPOINTS DE EXEMPLO ======

@app.get("/redis/status")
async def redis_status():
    """Verifica o status da conexão com Redis"""
    if redis_service.redis_client:
        try:
            await redis_service.redis_client.ping()
            return {"status": "connected", "message": "Redis está conectado e funcionando"}
        except Exception as e:
            return {"status": "error", "message": f"Erro na conexão: {e}"}
    else:
        return {"status": "disconnected", "message": "Redis não está conectado"}

@app.post("/redis/cache/{key}")
async def set_cache(key: str, value: str, expire: int = None):
    """Define um valor no cache Redis"""
    success = await redis_service.set(key, value, expire)
    if success:
        return {"message": f"Valor armazenado com chave '{key}'", "expire": expire}
    else:
        return {"error": "Falha ao armazenar valor"}

@app.get("/redis/cache/{key}")
async def get_cache(key: str):
    """Recupera um valor do cache Redis"""
    value = await redis_service.get(key)
    if value is not None:
        ttl = await redis_service.ttl(key)
        return {"key": key, "value": value, "ttl": ttl}
    else:
        raise HTTPException(status_code=404, detail="Chave não encontrada")

@app.delete("/redis/cache/{key}")
async def delete_cache(key: str):
    """Remove uma chave do cache Redis"""
    success = await redis_service.delete(key)
    if success:
        return {"message": f"Chave '{key}' removida com sucesso"}
    else:
        return {"message": f"Chave '{key}' não encontrada"}

@app.get("/redis/keys")
async def list_keys(pattern: str = "*"):
    """Lista todas as chaves no Redis que correspondem ao padrão"""
    keys = await redis_service.get_all_keys(pattern)
    return {"pattern": pattern, "keys": keys, "count": len(keys)}

@app.post("/redis/counter/{name}")
async def increment_counter(name: str, amount: int = 1):
    """Incrementa um contador no Redis"""
    result = await redis_service.increment(f"counter:{name}", amount)
    if result is not None:
        return {"counter": name, "value": result, "incremented_by": amount}
    else:
        return {"error": "Falha ao incrementar contador"}

@app.get("/redis/counter/{name}")
async def get_counter(name: str):
    """Obtém o valor atual de um contador"""
    value = await redis_service.get(f"counter:{name}")
    if value is not None:
        return {"counter": name, "value": int(value)}
    else:
        return {"counter": name, "value": 0}

# Exemplo de cache para os detalhes de acesso do NFT
@app.get("/access-details-cached/{token_id}")
async def get_access_details_cached(token_id: int, cache_time: int = 300):
    """
    Obtém detalhes de acesso com cache Redis
    cache_time: tempo de cache em segundos (padrão: 5 minutos)
    """
    cache_key = f"access_details:{token_id}"
    
    # Tenta buscar no cache primeiro
    cached_data = await redis_service.get(cache_key)
    if cached_data is not None:
        return {
            "data": cached_data,
            "from_cache": True,
            "ttl": await redis_service.ttl(cache_key)
        }
    
    # Se não estiver no cache, busca os dados e armazena
    try:
        access_details = nft_service.get_access_details(token_id)
        await redis_service.set(cache_key, access_details, cache_time)
        
        return {
            "data": access_details,
            "from_cache": False,
            "cached_for": cache_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar detalhes: {e}")

@app.get("/reputation/{wallet_address}")
async def get_reputation(wallet_address: str):
    """Retorna os dados de reputação de um endereço."""
    reputation_data = await reputation_service.get_reputation_data(wallet_address)
    is_banned = await reputation_service.is_banned(wallet_address)
    ban_ttl = await reputation_service.get_ban_ttl(wallet_address) if is_banned else 0
    
    return {
        "wallet_address": wallet_address,
        "is_banned": is_banned,
        "ban_ttl_seconds": ban_ttl,
        "reputation_data": reputation_data
    }