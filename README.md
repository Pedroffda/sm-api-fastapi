# **Interagindo com um Contrato Ethereum usando Web3**

Este projeto interage com um contrato inteligente na rede Polygon usando a biblioteca Web3.py. O código permite chamar funções de leitura e escrever dados no contrato, como obter informações sobre um documento e adicionar um novo documento.

## **Requisitos**

Antes de começar, certifique-se de ter os seguintes itens instalados:

- **Python 3.7+**
- **Web3.py**: Biblioteca para interagir com a blockchain Ethereum.
- **python-decouple**: Para gerenciar variáveis de ambiente de forma segura.
  
Instale as dependências necessárias:

```bash
pip install web3 python-decouple
```

## **Configuração**

1. **Obtenha uma chave de API da Alchemy**: 
   Crie uma conta no [Alchemy](https://www.alchemy.com/) e obtenha sua chave de API para conectar-se à rede Polygon.

2. **Variáveis de ambiente**:
   Crie um arquivo `.env` na raiz do seu projeto e adicione as seguintes variáveis:

   ```env
   ALCHEMY_API_KEY=your-alchemy-api-key
   CONTRACT_ADDRESS=your-contract-address
   MY_ADDRESS=your-wallet-address
   PRIVATE_KEY=your-wallet-private-key
   ```

   Substitua `your-alchemy-api-key`, `your-contract-address`, `your-wallet-address`, e `your-wallet-private-key` pelos valores reais.

## **Descrição do Código**

O código está dividido em duas principais funcionalidades:

1. **Leitura de Dados (Função `getDocument`)**:
   O código chama a função `getDocument` do contrato inteligente para obter informações sobre um documento a partir de seu `doc_hash`.

   **Exemplo de chamada**:

   ```python
   doc_hash = "0000xx"
   result = contract_instance.functions.getDocument(doc_hash).call()
   print(result)
   ```

2. **Escrita de Dados (Função `addDocument`)**:
   Você pode adicionar um novo documento ao contrato usando a função `addDocument`. O código envia uma transação para a rede Polygon para adicionar o documento.

   **Parâmetros para adicionar o documento**:
   
   - `user_id`: Identificador do usuário (por exemplo, "user_123").
   - `doc_hash`: Hash do documento (por exemplo, "0xabc123").

   **Exemplo de envio de transação**:

   ```python
   transaction = contract_instance.functions.addDocument(user_id, doc_hash).build_transaction({
       'from': my_address,
       'gas': 200000,
       'gasPrice': w3.to_wei('30', 'gwei'),
       'nonce': nonce
   })

   signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
   tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
   tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

   print(f"Transação enviada! Hash: {tx_hash.hex()}")
   print(f"Status da transação: {tx_receipt.status}")  # 1 = Sucesso, 0 = Falha
   ```

## **Como Rodar**

1. **Prepare seu ambiente**:
   Certifique-se de que as dependências estão instaladas e que o arquivo `.env` está configurado corretamente.

2. **Execute o script**:
   No terminal, execute o script Python que contém o código acima:

   ```bash
   python seu_script.py
   ```

   Isso irá:
   - Consultar os dados do documento com o `doc_hash` especificado.
   - Enviar uma transação para adicionar um novo documento ao contrato inteligente.

## **Segurança**

Certifique-se de não compartilhar sua chave privada (`PRIVATE_KEY`) com ninguém. Ela é essencial para assinar e enviar transações de forma segura.
