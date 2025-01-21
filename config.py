import os
from pathlib import Path

# Telegram Bot Token
BOT_TOKEN = '8008634632:AAGcAf45-1KhsJtHSL8FOOGQUlf00UOEtCs'


MAIN_CHANNEL = -1001829128097  
TARGET_CHANNELS = [
    -1001688162930, -1002141782346, -1001742421592, 
    -1002111068954, -1002421121693, -1002498151570, 
    -1001936938972, -1002441332024
]

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Paths
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'bot.log'

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True) 