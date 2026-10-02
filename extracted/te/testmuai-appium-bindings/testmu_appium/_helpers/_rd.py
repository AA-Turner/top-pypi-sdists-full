"""rd-details.env access — device-session sidecar config on the runner.

The LambdaTest device manager writes rd-details.env into the temp dir of the
machine driving the session; it carries HOST_IP and PROXY_API_PORT for the
per-session proxy sidecar. Env vars win over the file (same precedence
network_query has always used)."""

import os
import tempfile
from pathlib import Path


def rd_details() -> dict[str, str]:
    """Read the device-host details file without logging its contents."""
    path = Path(tempfile.gettempdir()) / "rd-details.env"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    result: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def proxy_host_port() -> tuple[str, str]:
    """(HOST_IP, PROXY_API_PORT) with env-first precedence; empty strings when absent."""
    details = rd_details()
    host = os.getenv("HOST_IP", "").strip() or details.get("HOST_IP", "")
    port = os.getenv("PROXY_API_PORT", "").strip() or details.get("PROXY_API_PORT", "")
    return host, port
