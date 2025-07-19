from decouple import config

class Settings:
    ALCHEMY_API_KEY = config("ALCHEMY_API_KEY")
    CONTRACT_ADDRESS = config("CONTRACT_ADDRESS")
    MY_ADDRESS = config("MY_ADDRESS")
    PRIVATE_KEY = config("PRIVATE_KEY")  # Armazenar com segurança!
    NETWORK_URL = f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    # NETWORK_URL = f"https://arb-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    # NETWORK_URL = f"https://opt-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    
print("Settings loaded successfully.")
print("Contract Address:", Settings.CONTRACT_ADDRESS)
print("My Address:", Settings.MY_ADDRESS)
print("Network URL:", Settings.NETWORK_URL)

settings = Settings()