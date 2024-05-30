import os
import time
import logging
import cv2
import numpy as np
import requests

# Einrichten des Loggings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Discord Webhook URL (ersetzen Sie dies durch Ihre tatsächliche URL)
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/YOUR_WEBHOOK_URL'

def adb_command(command):
    result = os.system(command)
    if result != 0:
        logging.error(f"ADB command failed: {command}")
    return result

def capture_screenshot(filename="screenshot.png"):
    adb_command(f"adb exec-out screencap -p > {filename}")

def detect_wheat_ready(screenshot_path="screenshot.png"):
    capture_screenshot(screenshot_path)
    image = cv2.imread(screenshot_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_ratio = cv2.countNonZero(mask) / (image.size / 3)
    if yellow_ratio > 0.05:  # Beispielwert, anpassen nach Bedarf
        return True
    return False

def plant_wheat():
    logging.info("Planting wheat...")
    adb_command("adb shell input tap 500 500")
    time.sleep(2)
    adb_command("adb shell input tap 500 600")
    time.sleep(2)

def harvest_wheat():
    logging.info("Harvesting wheat...")
    adb_command("adb shell input swipe 400 400 600 600")
    time.sleep(2)

def sell_wheat():
    logging.info("Selling wheat...")
    adb_command("adb shell input tap 300 300")
    time.sleep(2)
    adb_command("adb shell input tap 300 400")
    time.sleep(2)

def feed_animals():
    logging.info("Feeding animals...")
    adb_command("adb shell input tap 400 400")
    time.sleep(2)
    adb_command("adb shell input tap 400 500")
    time.sleep(2)

def manage_inventory():
    logging.info("Managing inventory...")
    adb_command("adb shell input tap 200 200")
    time.sleep(2)

def send_discord_notification(message):
    data = {
        "content": message,
        "username": "Hay Day Bot"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        logging.error(f"Failed to send Discord notification: {response.text}")

def main():
    while True:
        try:
            if detect_wheat_ready():
                harvest_wheat()
                sell_wheat()
                send_discord_notification("Wheat harvested and sold successfully!")
            else:
                plant_wheat()
                send_discord_notification("Wheat planted!")
            feed_animals()
            manage_inventory()
            logging.info("Waiting for the next cycle...")
            time.sleep(300)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            send_discord_notification(f"An error occurred: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()