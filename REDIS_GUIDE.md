# Redis Configuration Guide

Este guia explica como usar o Redis no projeto FastAPI para cache, rate limiting e outras funcionalidades.

## 📋 Pré-requisitos

### Instalando o Redis

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Docker:**
```bash
docker run --name redis-server -p 6379:6379 -d redis:alpine
```

### Verificando se o Redis está funcionando

```bash
redis-cli ping
# Deve retornar: PONG
```

## 🔧 Configuração

### 1. Variáveis de Ambiente

Adicione ao seu arquivo `.env`:

```env
# Redis Configuration (opcional - valores padrão serão usados se não definidos)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
# REDIS_PASSWORD=sua_senha_aqui  # se o Redis tiver autenticação
# REDIS_URL=redis://localhost:6379/0  # URL completa (opcional)
```

### 2. Dependências Python

As dependências já foram adicionadas ao `requirements.txt`:
- `redis==5.0.8`
- `aioredis==2.0.1`

Para instalar:
```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

### 1. Testando o Redis

Execute o exemplo para testar todas as funcionalidades:

```bash
python example/redis_example.py
```

### 2. Usando na API

O Redis está integrado automaticamente à API. Quando você iniciar o servidor FastAPI, ele se conectará automaticamente ao Redis:

```bash
uvicorn main:app --reload
```

### 3. Endpoints de Exemplo

#### Status do Redis
```http
GET /redis/status
```

#### Armazenar dados no cache
```http
POST /redis/cache/minha_chave
Content-Type: application/json

{
  "value": "meu valor",
  "expire": 300
}
```

#### Recuperar dados do cache
```http
GET /redis/cache/minha_chave
```

#### Cache de detalhes de NFT
```http
GET /access-details-cached/123?cache_time=600
```

#### Contador simples
```http
POST /redis/counter/page_views
```

## 📊 Casos de Uso

### 1. Cache de Dados NFT

```python
from src.services.redis_service import redis_service

async def get_nft_details_cached(token_id: int):
    cache_key = f"nft:{token_id}"
    
    # Tenta buscar no cache
    cached_data = await redis_service.get(cache_key)
    if cached_data:
        return cached_data
    
    # Se não estiver no cache, busca dos dados reais
    nft_data = nft_service.get_access_details(token_id)
    
    # Armazena no cache por 5 minutos
    await redis_service.set(cache_key, nft_data, expire=300)
    
    return nft_data
```

### 2. Rate Limiting

```python
async def check_rate_limit(user_ip: str, max_requests: int = 100, window: int = 3600):
    key = f"rate_limit:{user_ip}"
    
    current_count = await redis_service.get(key)
    
    if current_count is None:
        # Primeira requisição
        await redis_service.set(key, 1, expire=window)
        return True
    
    if int(current_count) >= max_requests:
        return False  # Limite excedido
    
    await redis_service.increment(key)
    return True
```

### 3. Estatísticas e Contadores

```python
async def track_nft_access(token_id: int):
    # Contador global de acessos
    total_accesses = await redis_service.increment("total_nft_accesses")
    
    # Contador específico do NFT
    nft_accesses = await redis_service.increment(f"nft_accesses:{token_id}")
    
    # Contador diário
    today = datetime.now().strftime("%Y-%m-%d")
    daily_accesses = await redis_service.increment(f"daily_accesses:{today}")
    
    return {
        "total": total_accesses,
        "nft_specific": nft_accesses,
        "today": daily_accesses
    }
```

### 4. Sessões de Usuário

```python
async def store_user_session(user_id: str, session_data: dict, expire_hours: int = 24):
    session_key = f"session:{user_id}"
    expire_seconds = expire_hours * 3600
    
    await redis_service.set(session_key, session_data, expire=expire_seconds)

async def get_user_session(user_id: str):
    session_key = f"session:{user_id}"
    return await redis_service.get(session_key)
```

## 🛠️ Funcionalidades Disponíveis

O `RedisService` oferece os seguintes métodos:

- `connect()` - Conecta ao Redis
- `disconnect()` - Desconecta do Redis
- `set(key, value, expire=None)` - Define um valor
- `get(key)` - Recupera um valor
- `delete(key)` - Remove uma chave
- `exists(key)` - Verifica se existe
- `expire(key, seconds)` - Define expiração
- `ttl(key)` - Tempo restante até expiração
- `increment(key, amount=1)` - Incrementa contador
- `get_all_keys(pattern="*")` - Lista chaves

## 🔍 Monitoramento

### Comandos úteis do Redis CLI

```bash
# Conectar ao Redis
redis-cli

# Ver todas as chaves
KEYS *

# Ver informações de uma chave
TYPE chave
TTL chave
GET chave

# Estatísticas do servidor
INFO

# Monitor comandos em tempo real
MONITOR

# Limpar todas as chaves (CUIDADO!)
FLUSHALL
```

### Logs e Debug

O serviço Redis inclui logs automáticos:
- ✅ Conexão estabelecida
- ❌ Erros de conexão
- ⚠️ Avisos quando não conectado

## 🔒 Segurança

### Produção

Para ambiente de produção, considere:

1. **Autenticação:**
   ```env
   REDIS_PASSWORD=sua_senha_muito_segura
   ```

2. **SSL/TLS:**
   ```env
   REDIS_URL=rediss://username:password@host:port/db
   ```

3. **Configuração de rede:**
   - Bind apenas para IPs necessários
   - Use firewall para restringir acesso
   - Configure `protected-mode` no Redis

### Exemplo de configuração segura

```env
REDIS_HOST=redis-cluster.exemplo.com
REDIS_PORT=6380
REDIS_PASSWORD=sua_senha_super_segura
REDIS_DB=1
REDIS_URL=rediss://user:sua_senha_super_segura@redis-cluster.exemplo.com:6380/1
```

## 🚨 Troubleshooting

### Redis não conecta
1. Verifique se o Redis está rodando: `systemctl status redis`
2. Teste a conexão: `redis-cli ping`
3. Verifique as configurações no `.env`

### Erro de importação do aioredis
```bash
pip install aioredis==2.0.1
```

### Performance
- Use TTL apropriado para evitar acúmulo de dados
- Monitor o uso de memória: `redis-cli info memory`
- Configure `maxmemory` no Redis se necessário

## 📚 Recursos Adicionais

- [Documentação do Redis](https://redis.io/documentation)
- [aioredis Documentation](https://aioredis.readthedocs.io/)
- [Redis Best Practices](https://redis.io/docs/manual/clients-guide/)
