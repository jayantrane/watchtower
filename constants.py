import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="tokens.env", override=True, verbose=True)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DEVICE_IP = os.getenv("DEVICE_IP")
LOG_FILE_DIR = os.getenv("LOG_FILE_DIR")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))  
ALERT_FREQUENCY = int(os.getenv("ALERT_FREQUENCY", 1))  
ALERT_TIME_WINDOW = int(os.getenv("ALERT_TIME_WINDOW", 2)) 
