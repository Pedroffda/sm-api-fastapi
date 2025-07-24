import json
import redis.asyncio as redis
from typing import Optional, Any
from src.config.settings import Settings

# Constantes
REDIS_NOT_CONNECTED_MSG = "⚠️  Redis não conectado"

class RedisService:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Conecta ao Redis"""
        try:
            self.redis_client = redis.Redis.from_url(
                Settings.REDIS_URL,
                encoding="utf-8", 
                decode_responses=True
            )
            # Testa a conexão
            print(self.redis_client)
            await self.redis_client.ping()
            print("✅ Conexão com Redis estabelecida com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar com Redis: {e}")
            self.redis_client = None
    
    async def disconnect(self):
        """Desconecta do Redis"""
        if self.redis_client:
            await self.redis_client.aclose()
            print("🔌 Conexão com Redis fechada")
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        Define um valor no Redis
        
        Args:
            key: Chave
            value: Valor (será serializado como JSON se não for string)
            expire: Tempo de expiração em segundos
        """
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return False
        
        try:
            # Serializa o valor se não for string
            if not isinstance(value, str):
                value = json.dumps(value)
            
            result = await self.redis_client.set(key, value, ex=expire)
            return result
        except Exception as e:
            print(f"❌ Erro ao definir valor no Redis: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Recupera um valor do Redis
        
        Args:
            key: Chave
            
        Returns:
            Valor deserializado ou None se não encontrado
        """
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value is None:
                return None
            
            # Tenta deserializar como JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # Se não for JSON, retorna como string
                return value
        except Exception as e:
            print(f"❌ Erro ao recuperar valor do Redis: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """Remove uma chave do Redis"""
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return False
        
        try:
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"❌ Erro ao deletar chave do Redis: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Verifica se uma chave existe no Redis"""
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return False
        
        try:
            result = await self.redis_client.exists(key)
            return result > 0
        except Exception as e:
            print(f"❌ Erro ao verificar existência da chave no Redis: {e}")
            return False
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Define expiração para uma chave"""
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return False
        
        try:
            result = await self.redis_client.expire(key, seconds)
            return result
        except Exception as e:
            print(f"❌ Erro ao definir expiração no Redis: {e}")
            return False
    
    async def ttl(self, key: str) -> int:
        """Retorna o TTL de uma chave (-1 se não tem expiração, -2 se não existe)"""
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return -2
        
        try:
            return await self.redis_client.ttl(key)
        except Exception as e:
            print(f"❌ Erro ao obter TTL do Redis: {e}")
            return -2
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Incrementa um contador no Redis"""
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return None
        
        try:
            if amount == 1:
                return await self.redis_client.incr(key)
            else:
                return await self.redis_client.incrby(key, amount)
        except Exception as e:
            print(f"❌ Erro ao incrementar no Redis: {e}")
            return None
    
    async def get_all_keys(self, pattern: str = "*") -> list:
        """Retorna todas as chaves que correspondem ao padrão"""
        if not self.redis_client:
            print(REDIS_NOT_CONNECTED_MSG)
            return []
        
        try:
            return await self.redis_client.keys(pattern)
        except Exception as e:
            print(f"❌ Erro ao buscar chaves no Redis: {e}")
            return []

# Instância global do serviço Redis
redis_service = RedisService()
