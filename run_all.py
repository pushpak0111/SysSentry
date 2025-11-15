import subprocess
import time

print("🚀 Starting SysSentry System...\n")

api = subprocess.Popen(["uvicorn", "api.app:app", "--reload", "--port", "8000"])
time.sleep(2)

monitor = subprocess.Popen(["python", "monitor.py"])
alerts = subprocess.Popen(["python", "alerts.py"])

print("✔ Dashboard Running → http://127.0.0.1:8000/static/index.html\n")

try:
    api.wait()
    monitor.wait()
    alerts.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down SysSentry...")
    api.terminate()
    monitor.terminate()
    alerts.terminate()
    print("✔ Shutdown complete.")
