from web3 import Web3
from src.config.settings import settings

class GasService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.NETWORK_URL))

    def estimate_gas_for_mint(self, recipient: str, token_uri: str) -> int:
        tx = {
            "to": settings.CONTRACT_ADDRESS,
            "data": self._encode_mint_data(recipient, token_uri),
            "from": settings.MY_ADDRESS,
        }
        return self.w3.eth.estimate_gas(tx)

    def _encode_mint_data(self, recipient: str, token_uri: str) -> str:
        # Implementar ABI encoding (usar web3.py ou eth_abi)
        pass