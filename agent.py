import psutil
import socket
import requests
import platform
import argparse
import time
import shutil


def collect_system_info():
    """Collect system-level info"""
    hostname         = socket.gethostname()
    os_name          = platform.system()
    os_version       = platform.version()
    cpu              = platform.processor()
    cpu_count        = psutil.cpu_count(logical=False)  
    cpu_threads      = psutil.cpu_count(logical=True) 
    cpu_usage        = psutil.cpu_percent(interval=1)
    memory           = psutil.virtual_memory()
    memory_total     = round(memory.total / (1024**3), 2)      
    memory_used      = round(memory.used / (1024**3), 2)        
    memory_available = round(memory.available / (1024**3), 2)
    disk             = shutil.disk_usage("/")
    disk_total       = round(disk.total / (1024**3), 2)
    disk_used        = round(disk.used / (1024**3), 2)
    disk_free        = round(disk.free / (1024**3), 2)

    return {
        "hostname": hostname,
        "os": os_name,
        "os_version": os_version,
        "cpu": cpu,
        "cpu_count": cpu_count,
        "cpu_threads": cpu_threads,
        "cpu_usage": cpu_usage,
        "memory_total": memory_total,
        "memory_used": memory_used,
        "memory_available": memory_available,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_free": disk_free,
    }


def build_process_tree():
    """Build process tree with children (recursive)"""
    processes = {}
    children_map = {}
    for proc in psutil.process_iter(attrs=["pid", "ppid", "name", "cpu_percent", "memory_info"]):
        try:
            info = {
                "ppid": proc.info["ppid"],
                "name": proc.info["name"],
                "cpu": proc.info["cpu_percent"],
                "memory": round(proc.info["memory_info"].rss / (1024**2), 2),
                "children": [],
            }
            processes[proc.info["pid"]] = info
            children_map.setdefault(proc.info["ppid"], []).append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    for pid, proc in processes.items():
        if pid in children_map:
            proc["children"].extend(children_map[pid])
    root_procs = [p for p in processes.values() if p["ppid"] not in processes]
    return root_procs


def main(endpoint):
    while True:
        system_info = collect_system_info()
        processes = build_process_tree()
        payload = system_info
        payload["processes"] = processes
        try:
            res = requests.post(endpoint, json=payload)
            if res.status_code == 201:
                print(f"[OK] Sent data to {endpoint}")
            else:
                print(f"[ERR] {res.status_code} {res.text}")
        except Exception as e:
            print("Error sending:", e)
        time.sleep(5)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True, help="Django API endpoint")
    args = parser.parse_args()
    main(args.endpoint)
