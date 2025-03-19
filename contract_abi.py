abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "user_id", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "doc_hash", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "name": "DocumentAdded",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "user_id", "type": "string"},
            {"internalType": "string", "name": "doc_hash", "type": "string"},
        ],
        "name": "addDocument",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "", "type": "string"},
        ],
        "name": "documents",
        "outputs": [
            {"internalType": "string", "name": "user_id", "type": "string"},
            {"internalType": "string", "name": "doc_hash", "type": "string"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "doc_hash", "type": "string"},
        ],
        "name": "getDocument",
        "outputs": [
            {"internalType": "string", "name": "user_id", "type": "string"},
            {"internalType": "string", "name": "doc_hash", "type": "string"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]
