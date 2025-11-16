# 🚀 SysSentry – Smart System Health Monitoring & Real-Time Alerting System

SysSentry is a real-time system monitoring platform that collects, analyzes, and visualizes system performance metrics such as CPU, Memory, and Disk usage. It provides live dashboards, automatic alerting, diagnostic recommendations, and simple deployment using Docker, AWS, and CI/CD.

---
## Dashboard Images 

<img width="1911" height="910" alt="image" src="https://github.com/user-attachments/assets/f15800ce-f819-4ad8-a416-3d3a45dc0c51" />

<img width="1919" height="881" alt="image" src="https://github.com/user-attachments/assets/982a6018-5cd4-4a32-abee-f991371c5eab" />

<img width="1917" height="890" alt="image" src="https://github.com/user-attachments/assets/6d190db1-af7d-4ead-a6f4-90c21c03a4c1" />

## 🔥 Key Features

### 🧠 1. FastAPI Backend
- Receives metrics from monitor.py
- Provides REST APIs for metrics, alerts, and diagnostics
- Lightweight & high-performance

### 📊 2. Real-Time Static Dashboard
- Pure HTML + CSS + JavaScript
- Smooth animated charts
- Auto-refreshes metrics without reloading

### 🖥 3. System Monitor (monitor.py)
- Collects CPU, Memory, Disk I/O
- Sends metrics to backend every second
- Works on Windows, Linux, and macOS

### 🚨 4. Alerts + Diagnostics
- Alerts triggered on threshold breaches
- diagnostics.py suggests automatic fixes (e.g., kill heavy processes, clear memory cache)

### 🐳 5. Docker + Docker Compose
- Complete containerization
- One-command deployment:
docker compose up -d --build

### ☁️ 6. AWS Deployment
- Runs flawlessly on EC2
- Dockerized services for easy scaling

### 🔄 7. CI/CD Pipeline (GitHub Actions)
- Auto deploys to EC2 on every push
- Pull latest code, rebuilds Docker, restarts services


## 📁 Project Structure

```
SysSentry/
├── api/                     # FastAPI backend
│   ├── app.py
│   ├── requirements.txt
│
├── dashboard/               # Static dashboard UI
│   ├── index.html
│   └── static/
│       └── dashboard.png    # Dashboard preview image
│
├── monitor/                 # Client-side monitoring agent
│   ├── monitor.py
│   └── requirements.txt
│
├── diagnostics/
│   └── diagnostics.py
│
├── alerts/
│   └── alerts.py
│
├── Dockerfile
├── docker-compose.yml
│
└── .github/
    └── workflows/
        └── deploy.yml       # CI/CD pipeline
```


## ⚙️ Architecture Overview

[monitor.py] → metrics → [FastAPI Backend] → stores/analyzes → [Dashboard] ← fetch every 1–2 sec
↑
[alerts.py]
↓
[diagnostics.py]
---

# 🛠 Installation

## 1️⃣ Clone the repo
git clone https://github.com/pushpak0111/SysSentry-Smart-System-Health-Monitoring-and-Alerting-System

cd SysSentry
---

## 2️⃣ Run using Docker (recommended)
docker compose up -d --build
Backend → http://localhost:8000  
Dashboard → http://localhost:8080

---

## 3️⃣ Run manually (optional)

### Backend:
cd api
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000

### Dashboard:
Open:

### Monitor:
cd monitor
pip install -r requirements.txt
python monitor.py
---

# ☁️ Deployment on AWS EC2

### Install Docker:
sudo apt update
sudo apt install docker.io docker-compose -y

### Pull repository:
git clone https://github.com/pushpak0111/SysSentry-Smart-System-Health-Monitoring-and-Alerting-System

cd SysSentry

### Run:
docker compose up -d --build
---

# 🔄 CI/CD Pipeline (GitHub Actions)

Your deploy workflow is stored at:
.github/workflows/deploy.yml


Pipeline actions:
- Connect to EC2 via SSH  
- Pull the latest code  
- Rebuild Docker containers  
- Restart services  

### Required GitHub Secrets
| Secret | Description |
|--------|-------------|
| `EC2_PUBLIC_IP` | Your server's public IP |
| `EC2_SSH_KEY` | Private SSH key for EC2 |

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /ingest | Receive CPU/RAM/Disk metrics |
| GET | /metrics/latest | Latest metrics |
| GET | /alerts | List active alerts |
| GET | /diagnostics | Suggested fixes |

Swagger Docs → `/docs`

---

# 🎨 Dashboard Features
- Modern UI
- Real-time charts
- No JS frameworks required
- Auto updates every second

---

# 📈 Future Enhancements
- WebSocket streaming
- Multi-node monitoring
- Login/auth system
- ML-based anomaly detection
- Historical time-series graphs

---

# ❤️ Contributing
Pull requests are welcome.  
Create issues for bugs or new features.

---

# 📜 License
MIT License

---

# ⭐ Support
If you find this project helpful, please ⭐ star the repository!
