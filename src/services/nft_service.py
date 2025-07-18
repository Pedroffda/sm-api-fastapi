from src.contracts.iot_access_nft import IoTAccessNFT
from src.config.settings import settings
from fastapi import HTTPException

class NFTService:
    def __init__(self):
        self.contract = IoTAccessNFT()

    def get_access_details(self, token_id: int):
        delegatee, expires_at = self.contract.get_access_details(token_id)
        if delegatee is None:
            raise HTTPException(status_code=404, detail="Token não encontrado")
        return {
            "delegatee": delegatee,
            "expires_at": expires_at,
            "is_active": expires_at > self.contract.w3.eth.get_block('latest').timestamp
        }

    def check_access(self, token_id: int, user: str):
        try:
            return self.contract.has_access(token_id, user)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delegate_access(self, token_id: int, delegatee: str, duration: int):
        return self.contract.delegate_access(
            token_id,
            delegatee,
            duration,
            settings.PRIVATE_KEY
        )

    def revoke_access(self, token_id: int):
        return self.contract.revoke_access(token_id, settings.PRIVATE_KEY)