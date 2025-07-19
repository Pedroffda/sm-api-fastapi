import json
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from src.config.settings import settings

class IoTAccessNFT:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.NETWORK_URL))
        with open("src/contracts/abis/IoTAccessNFT.json") as f:
            abi = json.load(f)
        
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
        self.contract = self.w3.eth.contract(
            address=settings.CONTRACT_ADDRESS,
            abi=abi
        )

    def mint_nft(self, recipient: str, token_uri: str, private_key: str):
        """Cria um novo NFT para o destinatário especificado"""
        start = time.time()
        # Converte para checksum address
        checksum_address = self.w3.to_checksum_address(recipient)
        nonce = self.w3.eth.get_transaction_count(settings.MY_ADDRESS)
        tx = self.contract.functions.mintNFT(
            checksum_address,
            token_uri
        ).build_transaction({
            "from": settings.MY_ADDRESS,
            "nonce": nonce
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        latency = time.time() - start
        print(f"Latência da transação de mint: {latency:.2f} segundos")
        return tx_hash.hex()

    def get_access_details(self, token_id: int) -> tuple:
        """Retorna (delegatee, expiresAt) para um token"""
        try:
            return self.contract.functions.accessControl(token_id).call()
        except Exception as e:
            print(f"Erro ao acessar accessControl: {e}")
            return (None, 0)

    def has_access(self, token_id: int, user: str) -> bool:
        """Verifica se um usuário tem acesso ao token"""
        try:
            return self.contract.functions.hasAccess(token_id, user).call()
        except Exception as e:
            print(f"Erro ao verificar acesso: {e}")
            return False

    def delegate_access(self, token_id: int, delegatee: str, duration: int, private_key: str):
        """Delega acesso temporário"""
        start = time.time()
        # Converte para checksum address
        checksum_address = self.w3.to_checksum_address(delegatee)
        nonce = self.w3.eth.get_transaction_count(settings.MY_ADDRESS)
        tx = self.contract.functions.delegateAccess(
            token_id,
            checksum_address,
            duration
        ).build_transaction({
            "from": settings.MY_ADDRESS,
            "nonce": nonce
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        latency = time.time() - start
        print(f"Latência da transação: {latency:.2f} segundos")
        return tx_hash.hex()

    def revoke_access(self, token_id: int, private_key: str):
        """Revoga acesso delegado"""
        nonce = self.w3.eth.get_transaction_count(settings.MY_ADDRESS)
        tx = self.contract.functions.revokeAccess(token_id).build_transaction({
            "from": settings.MY_ADDRESS,
            "nonce": nonce
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()