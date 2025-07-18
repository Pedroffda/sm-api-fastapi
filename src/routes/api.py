import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from src.services.nft_service import NFTService
from src.schemas.models import DelegateAccessRequest

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

@app.get("/access/{token_id}/{user}")
async def check_access(token_id: int, user: str):
    return {"has_access": nft_service.check_access(token_id, user)}

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