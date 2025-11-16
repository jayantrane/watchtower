from dotenv import load_dotenv
import os
from dotenv import find_dotenv

load_dotenv(dotenv_path="tokens.env", override=True, verbose=True)
TELEGRATM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DEVICE_IP = os.getenv("DEVICE_IP")
LOG_FILE_DIR = os.getenv("LOG_FILE_DIR", "data")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))  
ALERT_FREQUENCY = int(os.getenv("ALERT_FREQUENCY", 1))  
ALERT_TIME_WINDOW = int(os.getenv("ALERT_TIME_WINDOW", 2)) 
