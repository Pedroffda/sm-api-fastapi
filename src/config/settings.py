from decouple import config

class Settings:
    ALCHEMY_API_KEY = config("ALCHEMY_API_KEY")
    CONTRACT_ADDRESS = config("CONTRACT_ADDRESS")
    MY_ADDRESS = config("MY_ADDRESS")
    PRIVATE_KEY = config("PRIVATE_KEY")  # Armazenar com segurança!
    NETWORK_URL = f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    # NETWORK_URL = f"https://arb-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    # NETWORK_URL = f"https://opt-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    
    # Redis settings
    REDIS_HOST = config("REDIS_HOST", default="localhost")
    REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
    REDIS_DB = config("REDIS_DB", default=0, cast=int)
    REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
    REDIS_URL = config("REDIS_URL", default=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

    # Reputation System Settings
    REPUTATION_INITIAL_SCORE = config("REPUTATION_INITIAL_SCORE", default=100, cast=int)
    REPUTATION_SCORE_INCREMENT = config("REPUTATION_SCORE_INCREMENT", default=5, cast=int)
    REPUTATION_SCORE_DECREMENT = config("REPUTATION_SCORE_DECREMENT", default=10, cast=int)
    REPUTATION_MAX_FAILED_STREAK = config("REPUTATION_MAX_FAILED_STREAK", default=3, cast=int)
    REPUTATION_BAN_THRESHOLD_SCORE = config("REPUTATION_BAN_THRESHOLD_SCORE", default=50, cast=int)
    REPUTATION_BAN_DURATION_SECONDS = config("REPUTATION_BAN_DURATION_SECONDS", default=300, cast=int) # 5 minutos
    
print("Settings loaded successfully.")
print("Contract Address:", Settings.CONTRACT_ADDRESS)
print("My Address:", Settings.MY_ADDRESS)
print("Network URL:", Settings.NETWORK_URL)

settings = Settings()