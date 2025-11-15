import psutil
import time
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/ingest"

prev_disk = psutil.disk_io_counters()
prev_time = time.time()


def get_disk_stats():
    """Return Read IOPS, Write IOPS, and MB/s throughput."""
    global prev_disk, prev_time

    now = time.time()
    new_disk = psutil.disk_io_counters()

    time_diff = now - prev_time
    if time_diff == 0:
        time_diff = 1

    # IOPS
    read_iops = (new_disk.read_count - prev_disk.read_count) / time_diff
    write_iops = (new_disk.write_count - prev_disk.write_count) / time_diff

    # MB/s
    read_mb = (new_disk.read_bytes - prev_disk.read_bytes) / (1024 * 1024) / time_diff
    write_mb = (new_disk.write_bytes - prev_disk.write_bytes) / (1024 * 1024) / time_diff

    # Update state
    prev_disk = new_disk
    prev_time = now

    return round(read_iops, 1), round(write_iops, 1), round(read_mb + write_mb, 2)


def log_metrics():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk_activity = psutil.disk_usage("C:\\").percent  # storage usage %

    read_iops, write_iops, throughput = get_disk_stats()

    payload = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": cpu,
        "memory_percent": mem,
        "disk_percent": disk_activity,       # Storage %
        "read_iops": read_iops,
        "write_iops": write_iops,
        "throughput": throughput
    }

    try:
        requests.post(API_URL, json=payload, timeout=1)
        print(
            f"📡 Sent → CPU {cpu}% | MEM {mem}% | DISK {disk_activity}% "
            f"| R-IOPS {read_iops} | W-IOPS {write_iops} | MB/s {throughput}"
        )
    except Exception as e:
        print("❌ Failed to send:", e)


if __name__ == "__main__":
    print("🚀 SysSentry Monitor Started...")
    while True:
        log_metrics()
