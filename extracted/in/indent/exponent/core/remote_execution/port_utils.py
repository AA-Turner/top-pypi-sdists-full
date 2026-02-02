import time

import psutil

from exponent.core.remote_execution.types import PortInfo


def get_port_usage() -> list[PortInfo] | None:
    """
    Get information about all listening ports on the system.

    Returns:
        List of PortInfo objects containing process name, port, protocol, pid, and uptime.
        Returns None if there's a permission error.
        Returns empty list if no listening ports are found.
    """
    try:
        connections = psutil.net_connections(kind="tcp")
    except (psutil.AccessDenied, PermissionError):
        # If we don't have permission to see connections, return None
        return None
    except Exception:
        # For any other unexpected errors, return None
        return None

    port_info_list: list[PortInfo] = []
    seen_ports: set[int] = set()
    current_time = time.time()

    for conn in connections:
        # Only include TCP ports in LISTEN state
        if conn.status != "LISTEN":
            continue

        # Skip if no local address (shouldn't happen for LISTEN, but be safe)
        if not conn.laddr:
            continue

        port = conn.laddr.port

        # Skip duplicate ports (IPv4/IPv6 bindings)
        if port in seen_ports:
            continue
        seen_ports.add(port)

        pid = conn.pid

        # Try to get process information
        process_name = "unknown"
        uptime_seconds = None

        if pid:
            try:
                process = psutil.Process(pid)
                process_name = process.name()

                # Calculate uptime
                create_time = process.create_time()
                uptime_seconds = current_time - create_time
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process disappeared or we don't have permission
                pass
            except Exception:
                # Any other unexpected error, just skip process info
                pass

        port_info = PortInfo(
            process_name=process_name,
            port=port,
            protocol="TCP",
            pid=pid,
            uptime_seconds=uptime_seconds,
        )
        port_info_list.append(port_info)

        # Limit to 50 ports to avoid bloating the heartbeat payload
        if len(port_info_list) >= 50:
            break

    return port_info_list
