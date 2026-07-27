"""Item #6 — Sticky model warmth daemon."""

from __future__ import annotations

import socket
from dataclasses import dataclass
from pathlib import Path

__all__ = ["socket_path", "DaemonStatus", "daemon_status"]


def socket_path() -> Path:
    return Path.home() / ".sage" / "warmth.sock"


@dataclass
class DaemonStatus:
    running: bool
    stale: bool = False
    detail: str = ""


def daemon_status() -> DaemonStatus:
    p = socket_path()
    if not p.exists():
        return DaemonStatus(running=False, detail="no socket")
    # Try to connect
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(str(p))
        s.close()
        return DaemonStatus(running=True, detail="responsive")
    except (socket.error, OSError):
        return DaemonStatus(running=False, stale=True,
                            detail="socket exists but no server")
