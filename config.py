import os
from pathlib import Path

# Telegram Bot Token
BOT_TOKEN = '7548650434:AAFg7UwyLQp9MjxVSiNOfjjKt0glrHBCUxo'


MAIN_CHANNEL = -1002062360459  
TARGET_CHANNELS = [
    -1001889023251, -1001961620089
]

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Paths
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'bot.log'

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True) 