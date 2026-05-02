"""Event generators — scaled up from simulate_compromise.py to produce 16K events per batch."""

import random
import time
from datetime import datetime, timezone


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Normal telemetry generators ──────────────────────────────────────────────

def gen_system(n: int) -> list[dict]:
    events = []
    for _ in range(n):
        events.append({
            "timestamp": _ts(), "kind": "system", "source_type": "agent",
            "data": {
                "hostname": "DEMO-WORKSTATION", "os": "Windows", "os_release": "11",
                "cpu_percent": round(random.uniform(2, 45), 1),
                "ram_percent": round(random.uniform(30, 75), 1),
                "uptime_secs": int(time.time()) % 200000 + random.randint(0, 300),
            },
        })
    return events


def gen_network(n: int) -> list[dict]:
    events = []
    for _ in range(n):
        events.append({
            "timestamp": _ts(), "kind": "network", "source_type": "agent",
            "data": {"summary": [{"established": random.randint(30, 120), "listening": random.randint(8, 30)}]},
        })
    return events


def gen_processes(n: int) -> list[dict]:
    procs = [
        ("svchost.exe", 800, "SYSTEM"), ("explorer.exe", 4200, "admin"),
        ("chrome.exe", 12400, "admin"), ("MsMpEng.exe", 3100, "SYSTEM"),
        ("RuntimeBroker.exe", 5600, "admin"), ("SearchHost.exe", 7800, "SYSTEM"),
        ("dwm.exe", 900, "DWM-1"), ("lsass.exe", 680, "SYSTEM"),
        ("csrss.exe", 540, "SYSTEM"), ("services.exe", 620, "SYSTEM"),
        ("spoolsv.exe", 2200, "SYSTEM"), ("taskhostw.exe", 6100, "admin"),
        ("conhost.exe", 8800, "admin"), ("dllhost.exe", 9200, "admin"),
        ("WmiPrvSE.exe", 3400, "SYSTEM"), ("audiodg.exe", 4600, "LOCAL SERVICE"),
    ]
    events = []
    for _ in range(n):
        name, base_pid, user = random.choice(procs)
        events.append({
            "timestamp": _ts(), "kind": "process_list", "source_type": "agent",
            "data": {
                "name": name, "pid": base_pid + random.randint(0, 5000),
                "user": user, "cpu_percent": round(random.uniform(0, 15), 1),
                "memory_mb": round(random.uniform(5, 800), 1),
            },
        })
    return events


def gen_disk(n: int) -> list[dict]:
    events = []
    for _ in range(n):
        events.append({
            "timestamp": _ts(), "kind": "disk_usage", "source_type": "agent",
            "data": {"count": 2, "volumes": [
                {"mount": "C:\\", "percent": round(random.uniform(50, 75), 1), "total_bytes": 500_000_000_000},
                {"mount": "D:\\", "percent": round(random.uniform(25, 55), 1), "total_bytes": 1_000_000_000_000},
            ]},
        })
    return events


def gen_services(n: int) -> list[dict]:
    svc_pool = [
        ("Winmgmt", "Windows Management Instrumentation"), ("Dhcp", "DHCP Client"),
        ("Dnscache", "DNS Client"), ("W32Time", "Windows Time"),
        ("EventLog", "Windows Event Log"), ("Schedule", "Task Scheduler"),
        ("Spooler", "Print Spooler"), ("BITS", "Background Intelligent Transfer"),
        ("Themes", "Themes"), ("LanmanServer", "Server"),
        ("WSearch", "Windows Search"), ("wuauserv", "Windows Update"),
    ]
    events = []
    for _ in range(n):
        svc_name, display = random.choice(svc_pool)
        events.append({
            "timestamp": _ts(), "kind": "services", "source_type": "agent",
            "data": {"services": [{"service_name": svc_name, "display_name": display, "status": "RUNNING"}]},
        })
    return events


def gen_ports(n: int) -> list[dict]:
    port_pool = [
        (135, "TCP", "LISTENING"), (445, "TCP", "LISTENING"),
        (3389, "TCP", "LISTENING"), (5040, "TCP", "LISTENING"),
        (49664, "TCP", "LISTENING"), (49665, "TCP", "LISTENING"),
    ]
    events = []
    for _ in range(n):
        port, proto, state = random.choice(port_pool)
        events.append({
            "timestamp": _ts(), "kind": "open_ports", "source_type": "agent",
            "data": {"count": len(port_pool), "ports": [
                {"port": port, "proto": proto, "state": state, "pid": random.randint(500, 10000)},
            ]},
        })
    return events


def gen_event_log(n: int) -> list[dict]:
    normal_logs = [
        (4624, "Security", "Information", "An account was successfully logged on. Logon Type: 2"),
        (7036, "System", "Information", "The Windows Time service entered the running state."),
        (10016, "System", "Warning", "The application-specific permission settings do not grant Local Activation permission."),
        (1, "Application", "Information", "Windows Error Reporting: Fault bucket, type 0"),
        (4672, "Security", "Information", "Special privileges assigned to new logon."),
    ]
    events = []
    for _ in range(n):
        eid, log_name, level, msg = random.choice(normal_logs)
        events.append({
            "timestamp": _ts(), "kind": "event_log", "source_type": "agent",
            "data": {"entries": [{
                "event_id": eid, "log_name": log_name, "source": "Microsoft-Windows-Security-Auditing",
                "level": level, "event_time": _ts(), "message": msg,
            }]},
        })
    return events


# ── Compromise event generators ──────────────────────────────────────────────

_C2_DOMAINS = [
    "update-service.dynamic-dns.net", "cdn-assets.cloud-sync.io",
    "telemetry.app-analytics.net", "api.secure-update-check.com",
    "health.system-monitor-pro.net", "sync.cloud-backup-service.net",
]

_C2_IPS = [
    "185.141.62.77", "91.215.85.142", "185.234.216.33",
    "91.108.44.19", "185.56.83.200", "91.219.237.44",
]


def gen_compromise_initial_access(n: int) -> list[dict]:
    events = []
    for _ in range(n):
        events.append({
            "timestamp": _ts(), "kind": "event_log", "source_type": "agent",
            "data": {"entries": [{
                "event_id": 4688, "log_name": "Security",
                "source": "Microsoft-Windows-Security-Auditing", "level": "Information",
                "event_time": _ts(),
                "message": f"New process created: chrome.exe --load-extension=nmmhkkegccagdldgiimedpiccmgmieda --silent-install (PID {random.randint(10000, 65000)})",
            }]},
        })
        events.append({
            "timestamp": _ts(), "kind": "event_log", "source_type": "agent",
            "data": {"entries": [{
                "event_id": 1033, "log_name": "Application",
                "source": "Chrome-Extensions", "level": "Warning",
                "event_time": _ts(),
                "message": "Extension nmmhkkegccagdldgiimedpiccmgmieda granted permissions: tabs, webRequest, webRequestBlocking, cookies, storage, <all_urls>",
            }]},
        })
    return events


def gen_compromise_c2(n: int) -> list[dict]:
    events = []
    for _ in range(n):
        domain = random.choice(_C2_DOMAINS)
        ip = random.choice(_C2_IPS)
        events.append({
            "timestamp": _ts(), "kind": "dns_cache", "source_type": "agent",
            "data": {"count": 2, "entries": [
                {"name": domain, "address": ip, "type": "1"},
                {"name": random.choice(_C2_DOMAINS), "address": f"185.{random.randint(100,255)}.{random.randint(0,255)}.{random.randint(1,254)}", "type": "1"},
            ]},
        })
        events.append({
            "timestamp": _ts(), "kind": "open_ports", "source_type": "agent",
            "data": {"count": 10, "ports": [
                {"port": 4443, "proto": "TCP", "state": "LISTENING", "pid": random.randint(60000, 65000), "address": "0.0.0.0"},
                {"port": 8443, "proto": "TCP", "state": "ESTABLISHED", "pid": random.randint(60000, 65000), "address": ip},
            ]},
        })
        events.append({
            "timestamp": _ts(), "kind": "scheduled_tasks", "source_type": "agent",
            "data": {"count": 5, "tasks": [
                {"task_name": "\\ChromeUpdateCheck", "status": "Running", "next_run": "Every 15 minutes"},
                {"task_name": "\\SystemHealthMonitor", "status": "Running", "next_run": "Every 5 minutes"},
            ]},
        })
    return events


def gen_compromise_credential(n: int) -> list[dict]:
    events = []
    for _ in range(n):
        pid = random.randint(60000, 65000)
        events.append({
            "timestamp": _ts(), "kind": "event_log", "source_type": "agent",
            "data": {"entries": [
                {
                    "event_id": 4648, "log_name": "Security",
                    "source": "Microsoft-Windows-Security-Auditing", "level": "Information",
                    "event_time": _ts(),
                    "message": f"A logon was attempted using explicit credentials. Subject: chrome.exe (PID {pid}). Target: lsass.exe. Logon Type: 9 (NewCredentials)",
                },
                {
                    "event_id": 4625, "log_name": "Security",
                    "source": "Microsoft-Windows-Security-Auditing", "level": "Warning",
                    "event_time": _ts(),
                    "message": f"An account failed to log on. Logon Type: 3 (Network). Source: {random.choice(_C2_IPS)}. Status: 0xC000006D. Failure count: {random.randint(10, 200)}",
                },
            ]},
        })
        events.append({
            "timestamp": _ts(), "kind": "startup_programs", "source_type": "agent",
            "data": {"count": 4, "programs": [
                {"hive": "HKCU", "name": "ChromeHelper", "value": "C:\\Users\\admin\\AppData\\Local\\Temp\\svchost_helper.exe --silent"},
                {"hive": "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "name": "SystemHealthCheck",
                 "value": "powershell.exe -WindowStyle Hidden -EncodedCommand SQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0AA=="},
            ]},
        })
    return events


def gen_compromise_exfil(n: int) -> list[dict]:
    events = []
    for _ in range(n):
        events.append({
            "timestamp": _ts(), "kind": "event_log", "source_type": "agent",
            "data": {"entries": [{
                "event_id": 4663, "log_name": "Security",
                "source": "Microsoft-Windows-Security-Auditing", "level": "Information",
                "event_time": _ts(),
                "message": f"An attempt was made to access object: C:\\Users\\admin\\AppData\\Local\\Temp\\~cache_export_{random.randint(1,99):02d}.dat ({random.randint(100, 900)} MB staged for exfiltration)",
            }]},
        })
        events.append({
            "timestamp": _ts(), "kind": "network_bytes", "source_type": "agent",
            "data": {"adapters": [{
                "adapter_name": "Total",
                "bytes_received": random.randint(500_000, 5_000_000),
                "bytes_sent": random.randint(50_000_000, 500_000_000),
            }]},
        })
        events.append({
            "timestamp": _ts(), "kind": "dns_cache", "source_type": "agent",
            "data": {"count": 3, "entries": [
                {"name": random.choice(_C2_DOMAINS), "address": random.choice(_C2_IPS), "type": "1"},
            ]},
        })
    return events


# ── Batch builder ────────────────────────────────────────────────────────────

# 22 batches. Each batch = 16K events.
# Phase timeline:
#   Batches  1-6  (min 0-6):   Normal telemetry
#   Batches  7-9  (min 6-9):   Initial access (normal + chrome extension attack)
#   Batches 10-13 (min 9-13):  C2 + persistence
#   Batches 14-17 (min 13-17): Credential access + lateral movement
#   Batches 18-22 (min 17-22): Data exfiltration

BATCH_SIZE = 10_000

PHASES = [
    # (batch_range_start, batch_range_end, phase_name, generator_mix)
    # 32 batches x 10K = 320K events
    (1,  8,  "NORMAL",           [(gen_system, 0.15), (gen_network, 0.15), (gen_processes, 0.25), (gen_disk, 0.10), (gen_services, 0.10), (gen_ports, 0.10), (gen_event_log, 0.15)]),
    (9,  13, "INITIAL ACCESS",   [(gen_system, 0.10), (gen_network, 0.10), (gen_processes, 0.20), (gen_event_log, 0.20), (gen_compromise_initial_access, 0.25), (gen_services, 0.05), (gen_ports, 0.10)]),
    (14, 19, "C2 + PERSISTENCE", [(gen_system, 0.08), (gen_processes, 0.15), (gen_event_log, 0.12), (gen_compromise_initial_access, 0.10), (gen_compromise_c2, 0.35), (gen_ports, 0.10), (gen_network, 0.10)]),
    (20, 25, "CREDENTIAL ACCESS", [(gen_system, 0.05), (gen_processes, 0.10), (gen_compromise_c2, 0.20), (gen_compromise_credential, 0.40), (gen_event_log, 0.10), (gen_network, 0.10), (gen_ports, 0.05)]),
    (26, 32, "EXFILTRATION",     [(gen_system, 0.05), (gen_compromise_c2, 0.10), (gen_compromise_credential, 0.15), (gen_compromise_exfil, 0.50), (gen_network, 0.10), (gen_processes, 0.10)]),
]


def get_phase(batch_num: int) -> tuple[str, list]:
    for start, end, name, mix in PHASES:
        if start <= batch_num <= end:
            return name, mix
    return "EXFILTRATION", PHASES[-1][3]


def generate_batch(batch_num: int) -> tuple[str, list[dict]]:
    """Generate one batch of ~16K events for the given batch number (1-22)."""
    phase_name, mix = get_phase(batch_num)
    events = []
    for gen_fn, fraction in mix:
        count = int(BATCH_SIZE * fraction)
        events.extend(gen_fn(count))
    # Top up or trim to exactly BATCH_SIZE
    while len(events) < BATCH_SIZE:
        events.append(gen_system(1)[0])
    events = events[:BATCH_SIZE]
    return phase_name, events
