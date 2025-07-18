from pydantic import BaseModel, field_validator
from web3 import Web3

class DelegateAccessRequest(BaseModel):
    token_id: int
    delegatee: str
    duration: int  # Duração em segundos
    @field_validator('delegatee')
    def validate_address(cls, v):
        try:
            return Web3.to_checksum_address(v)
        except ValueError:
            raise ValueError("Endereço Ethereum inválido")