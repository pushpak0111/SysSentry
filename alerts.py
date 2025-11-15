import psutil
import time
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/alert"

CPU_THRESHOLD = 85
MEM_THRESHOLD = 80
DISK_THRESHOLD = 85

def check_alerts():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    alerts = []

    if cpu > CPU_THRESHOLD:
        alerts.append("High CPU Usage")
    if mem > MEM_THRESHOLD:
        alerts.append("High Memory Usage")
    if disk > DISK_THRESHOLD:
        alerts.append("High Disk Usage")

    for a in alerts:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "alert": a
        }
        try:
            requests.post(API_URL, json=payload, timeout=1)
            print("⚠️ Alert Sent:", a)
        except Exception as e:
            print("❌ Failed to send alert:", e)

if __name__ == "__main__":
    print("🚨 Alert Engine Started...")
    while True:
        check_alerts()
