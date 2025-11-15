# api/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import traceback
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()


# =========================================================
# OPTIONAL SUPABASE CLIENT
# =========================================================
try:
    from supabase import create_client as create_supabase_client
except:
    create_supabase_client = None

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")

SUPABASE_AVAILABLE = (
    create_supabase_client is not None
    and SUPABASE_URL is not None
    and SUPABASE_KEY is not None
)

supabase = (
    create_supabase_client(SUPABASE_URL, SUPABASE_KEY)
    if SUPABASE_AVAILABLE
    else None
)

# =========================================================
# FASTAPI APP INIT
# =========================================================
app = FastAPI()

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# IN-MEMORY REAL-TIME STORE
# =========================================================
METRICS = []      # last 200 samples
ALERTS = []       # last 100 samples
MAX_METRICS = 200
MAX_ALERTS = 100

# =========================================================
# PAYLOAD MODELS
# =========================================================
class MetricPayload(BaseModel):
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    read_iops: float
    write_iops: float
    throughput: float

class AlertPayload(BaseModel):
    timestamp: str
    alert: str

# =========================================================
# INGEST FROM monitor.py
# =========================================================
@app.post("/ingest")
def ingest_metrics(payload: MetricPayload):
    try:
        data = payload.dict()
        METRICS.append(data)
        if len(METRICS) > MAX_METRICS:
            METRICS.pop(0)

        if SUPABASE_AVAILABLE:
            try:
                supabase.table("metrics").insert(data).execute()
            except:
                traceback.print_exc()

        return {"status": "ok"}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# INGEST ALERTS
# =========================================================
@app.post("/alert")
def ingest_alert(payload: AlertPayload):
    try:
        entry = payload.dict()
        ALERTS.append(entry)
        if len(ALERTS) > MAX_ALERTS:
            ALERTS.pop(0)

        if SUPABASE_AVAILABLE:
            try:
                supabase.table("alerts").insert(entry).execute()
            except:
                traceback.print_exc()

        return {"status": "ok"}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# REAL-TIME ENDPOINTS USED BY FRONTEND
# =========================================================

# Original (kept for compatibility)
@app.get("/metrics")
def api_metrics():
    return METRICS

# NEW (frontend expects this)
@app.get("/metrics/latest")
def latest_metric():
    if not METRICS:
        return {}
    return METRICS[-1]

# NEW (frontend expects this)
@app.get("/metrics/history")
def metrics_history(limit: int = 40):
    return METRICS[-limit:]

@app.get("/alerts")
def api_alerts():
    return ALERTS[::-1]

# =========================================================
# HISTORY (full)
# =========================================================
@app.get("/history")
def api_history(limit: int = 200):
    if SUPABASE_AVAILABLE:
        try:
            resp = (
                supabase
                .table("metrics")
                .select("*")
                .order("timestamp", desc=True)
                .limit(limit)
                .execute()
            )
            return resp.data
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Supabase read failed: " + str(e))

    return METRICS[-limit:]

# =========================================================
# AI INSIGHTS
# =========================================================
@app.get("/ai-insights")
def ai_insights():
    try:
        series = METRICS
        if not series:
            return {"message": "no data yet"}

        cpu_vals = [m["cpu_percent"] for m in series]
        mem_vals = [m["memory_percent"] for m in series]
        disk_vals = [m["disk_percent"] for m in series]
        times = list(range(len(cpu_vals)))

        def moving_avg(arr, n=5):
            n = min(n, len(arr))
            return sum(arr[-n:]) / n

        def slope(xs, ys):
            if len(xs) < 2:
                return 0.0
            n = len(xs)
            mx = sum(xs)/n
            my = sum(ys)/n
            num = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
            den = sum((xs[i]-mx)**2 for i in range(n))
            return 0 if den == 0 else num/den

        insights = {
            "latest": series[-1],
            "cpu": {
                "current": cpu_vals[-1],
                "ma_5": moving_avg(cpu_vals, 5),
                "trend_slope": slope(times, cpu_vals)
            },
            "memory": {
                "current": mem_vals[-1],
                "ma_5": moving_avg(mem_vals, 5),
                "trend_slope": slope(times, mem_vals)
            },
            "disk": {
                "current": disk_vals[-1],
                "ma_5": moving_avg(disk_vals, 5),
                "trend_slope": slope(times, disk_vals)
            },
            "recommendations": []
        }

        if insights["cpu"]["current"] > 85:
            insights["recommendations"].append("CPU extremely high — identify heavy processes.")
        if insights["memory"]["current"] > 85:
            insights["recommendations"].append("Memory very high — close unused apps.")
        if insights["disk"]["current"] > 90:
            insights["recommendations"].append("Disk almost full — consider cleanup.")

        if not insights["recommendations"]:
            insights["recommendations"] = ["System looks healthy."]

        return insights

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
