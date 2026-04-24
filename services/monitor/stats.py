#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import socket
import time
import os
import docker

app = Flask(__name__)
CORS(app)

def cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return round(int(f.read()) / 1000, 1)
    except:
        return None

def check_port(port, host="127.0.0.1"):
    try:
        s = socket.create_connection((host, port), timeout=1)
        s.close()
        return True
    except:
        return False

def check_proc(name):
    try:
        for d in os.listdir('/proc'):
            if d.isdigit():
                try:
                    with open(f'/proc/{d}/comm') as f:
                        if name in f.read().strip():
                            return True
                except:
                    pass
        return False
    except:
        return False

def docker_containers():
    try:
        c = docker.from_env()
        return {
            container.name: container.status == "running"
            for container in c.containers.list(all=True)
            if container.name != "pi-monitor"
        }
    except:
        return {}

def service_status():
    services = {
        "nginx": check_port(80, "192.168.10.57"),
        "cloudflared": check_proc("cloudflared"),
    }
    services.update(docker_containers())
    return services

def uptime():
    seconds = int(time.time() - psutil.boot_time())
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

@app.route("/api/stats")
def stats():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    return jsonify({
        "cpu": {
            "percent": cpu,
            "count": psutil.cpu_count(),
            "freq": round(psutil.cpu_freq().current) if psutil.cpu_freq() else None,
        },
        "ram": {
            "percent": ram.percent,
            "used_gb": round(ram.used / 1e9, 2),
            "total_gb": round(ram.total / 1e9, 2),
        },
        "disk": {
            "percent": disk.percent,
            "used_gb": round(disk.used / 1e9, 1),
            "total_gb": round(disk.total / 1e9, 1),
        },
        "temp": cpu_temp(),
        "uptime": uptime(),
        "net": {
            "sent_mb": round(net.bytes_sent / 1e6, 1),
            "recv_mb": round(net.bytes_recv / 1e6, 1),
        },
        "services": service_status(),
        "timestamp": int(time.time()),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
