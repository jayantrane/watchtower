from argparse import ArgumentParser
from enum import Enum
from logging import info, warning
import random
from sqlite3.dbapi2 import Timestamp
from constants import ALERT_FREQUENCY, ALERT_TIME_WINDOW, CHAT_ID, LOG_FILE_DIR, TELEGRAM_BOT_TOKEN, DEVICE_IP, CHECK_INTERVAL
import time
import os
import re
from datetime import datetime, timedelta
from queue import LifoQueue
import requests

class Stack:
    def __init__(self):
        self.items = LifoQueue()

    def push(self, item):
        self.items.put(item)

    def pop(self):
        return self.items.get() if not self.items.empty() else None

    def peek(self):
        if self.items.empty():
            return None
        return self.items.queue[-1]  # Direct access to underlying deque

    def is_empty(self):
        return self.items.empty()
    

# Regex to extract the timestamp portion (e.g., "Nov 15 21:06:44")
pattern = r'([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})'

def extract_timestamp(log_line):
    match = re.search(pattern, log_line)
    if match:
        timestamp_str = match.group(1)

        # Construct datetime object; assume current year since log doesn't include year
        current_year = datetime.now().year

        # Parse using datetime
        dt = datetime.strptime(f"{current_year} {timestamp_str}", "%Y %b %d %H:%M:%S")
        return dt
    else:
        warning("No timestamp found.")
        return None

def send_message_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        warning(f"Failed to send message: {response.text}")

def _sliding_window(file_path):
    start_time = None
    last_time  = None
    count      = 0
    with open(file_path, "r") as f:
        for line in f:
            if DEVICE_IP in line:
                current_time = extract_timestamp(line)
                if start_time is None:
                    start_time = last_time = current_time

                if current_time > (last_time + timedelta(seconds=CHECK_INTERVAL)):
                    count = count + (last_time - start_time).total_seconds() // 60
                    start_time = last_time = current_time
                
                last_time = current_time

    last_window_time = 0
    if start_time is not None and last_time is not None:
        last_window_time =  (last_time - start_time).total_seconds() // 60
        count = count + last_window_time

    return count, last_window_time

def parse_args():
    parser = ArgumentParser(description="Device Online Time Checker")
    parser.add_argument(
        "--eod", action="store_true", help="Check until end of day"
    )

    parser.add_argument(
        "--periodic_alert", action="store_true", help="Enable periodic alerts"
    )

    parser.add_argument(
        "--file_name", type=str, help="Log file name", default="pihole.log"
    )
    return parser.parse_args()

def main():
    opts = parse_args()
    file_path = os.path.join(LOG_FILE_DIR, opts.file_name)
    if opts.eod:
        count = _sliding_window(file_path)
        print(f"Device {DEVICE_IP} was online for {count} minutes in the log period.")
        #count = _stack_solution(LOG_FILE_PATH)

    if opts.periodic_alert:
        while True:
            _, last_window_time = _sliding_window(file_path)
            print(f"Last window time: {last_window_time} minutes")
            if (last_window_time >= ALERT_TIME_WINDOW):
                message = f"Alert: You have been watching TV for {last_window_time} minutes! \n" \
                          f"Be mindful, you have goals to achieve! 📺🚀"

                send_message_to_telegram(message)
                print(f"Sent alert: {message}")

            time.sleep(ALERT_FREQUENCY * 60)

if __name__ == "__main__":
    main()