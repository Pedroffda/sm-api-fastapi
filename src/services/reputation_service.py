import time
from src.services.redis_service import redis_service
from src.config.settings import settings

class ReputationService:
    """
    Serviço para gerenciar a reputação de endereços de carteira.
    """

    async def is_banned(self, wallet_address: str) -> bool:
        """Verifica se um endereço está na lista de bloqueio."""
        ban_key = f"ban:{wallet_address}"
        return await redis_service.exists(ban_key)

    async def get_reputation_data(self, wallet_address: str) -> dict:
        """Recupera os dados de reputação de um endereço."""
        reputation_key = f"reputation:{wallet_address}"
        data = await redis_service.get(reputation_key)
        
        if data is None:
            # Retorna dados padrão se não existir
            return {
                "score": settings.REPUTATION_INITIAL_SCORE,
                "failed_attempts_streak": 0,
                "last_successful_attempt_ts": None,
                "last_failed_attempt_ts": None,
                "total_requests": 0,
                "total_failures": 0,
            }
        return data

    async def update_reputation_on_success(self, wallet_address: str):
        """Atualiza a reputação após uma tentativa bem-sucedida."""
        reputation_key = f"reputation:{wallet_address}"
        data = await self.get_reputation_data(wallet_address)

        data["score"] += settings.REPUTATION_SCORE_INCREMENT
        data["failed_attempts_streak"] = 0
        data["last_successful_attempt_ts"] = int(time.time())
        data["total_requests"] += 1

        await redis_service.set(reputation_key, data)

    async def update_reputation_on_failure(self, wallet_address: str):
        """Atualiza a reputação após uma tentativa falha."""
        reputation_key = f"reputation:{wallet_address}"
        data = await self.get_reputation_data(wallet_address)

        data["score"] -= settings.REPUTATION_SCORE_DECREMENT
        data["failed_attempts_streak"] += 1
        data["last_failed_attempt_ts"] = int(time.time())
        data["total_requests"] += 1
        data["total_failures"] += 1

        # Verifica se o endereço deve ser banido
        if (data["score"] < settings.REPUTATION_BAN_THRESHOLD_SCORE or
            data["failed_attempts_streak"] >= settings.REPUTATION_MAX_FAILED_STREAK):
            
            ban_key = f"ban:{wallet_address}"
            await redis_service.set(ban_key, "banned", expire=settings.REPUTATION_BAN_DURATION_SECONDS)
            print(f"🚫 Endereço {wallet_address} banido por {settings.REPUTATION_BAN_DURATION_SECONDS} segundos.")

        await redis_service.set(reputation_key, data)

    async def get_ban_ttl(self, wallet_address: str) -> int:
        """Retorna o tempo restante do banimento em segundos."""
        ban_key = f"ban:{wallet_address}"
        return await redis_service.ttl(ban_key)

# Instância global do serviço de reputação
reputation_service = ReputationService()
