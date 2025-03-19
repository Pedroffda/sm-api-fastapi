from web3 import Web3
from decouple import config
from contract_abi import abi 

ALCHEMY_API_KEY = config('ALCHEMY_API_KEY')

w3 = Web3(Web3.HTTPProvider(f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"))

CONTRACT_ADDRESS = config('CONTRACT_ADDRESS')

contract_instance = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

doc_hash= "0000xx"

try:
    result = contract_instance.functions.getDocument(doc_hash).call()
    print(result)

except Exception as e:
    print(f"Erro ao chamar a função: {e}")

my_address = config('MY_ADDRESS')
private_key = config('PRIVATE_KEY')

# Parâmetros para adicionar o documento
user_id = "user_123"
doc_hash = "0xabc123"

nonce = w3.eth.get_transaction_count(my_address)

transaction = contract_instance.functions.addDocument(user_id, doc_hash).build_transaction({
    'from': my_address,
    'gas': 200000,  # Ajuste conforme necessário
    'gasPrice': w3.to_wei('30', 'gwei'),
    'nonce': nonce
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# Enviar a transação para a rede
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# Aguardar a confirmação da transação
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Transação enviada! Hash: {tx_hash.hex()}")
print(f"Status da transação: {tx_receipt.status}")  # 1 = Sucesso, 0 = Falha