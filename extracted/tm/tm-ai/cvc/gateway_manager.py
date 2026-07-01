"""
cvc.gateway_manager — Service lifecycle manager for the CVC Gateway.

Manages the lifecycle of all CVC subsystems (proxy, MCP server, agent sessions)
as child processes.  Tracks PIDs in ``.cvc/services.json``, polls health
endpoints, and provides start/stop/restart/pause/kill operations.

Platform-aware:
  - Windows: CREATE_NO_WINDOW + DETACHED_PROCESS, taskkill /PID
  - Unix:    start_new_session, SIGTERM/SIGSTOP/SIGCONT/SIGKILL
"""

from __future__ import annotations

import json
import logging
import os
import signal
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import sys
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.gateway")

# Service states
STATUS_RUNNING = "running"
STATUS_STOPPED = "stopped"
STATUS_STARTING = "starting"
STATUS_PAUSED = "paused"
STATUS_ERROR = "error"
STATUS_UNKNOWN = "unknown"


class ServiceRecord:
    """State for a single managed service."""

    __slots__ = ("name", "pid", "port", "status", "started_at", "transport")

    def __init__(
        self,
        name: str,
        *,
        pid: int | None = None,
        port: int | None = None,
        status: str = STATUS_STOPPED,
        started_at: float | None = None,
        transport: str | None = None,
    ) -> None:
        self.name = name
        self.pid = pid
        self.port = port
        self.status = status
        self.started_at = started_at
        self.transport = transport

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "pid": self.pid,
            "port": self.port,
            "status": self.status,
            "started_at": self.started_at,
            "transport": self.transport,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ServiceRecord:
        return cls(
            name=data["name"],
            pid=data.get("pid"),
            port=data.get("port"),
            status=data.get("status", STATUS_UNKNOWN),
            started_at=data.get("started_at"),
            transport=data.get("transport"),
        )

    @property
    def uptime_seconds(self) -> float:
        if self.started_at and self.status == STATUS_RUNNING:
            return time.time() - self.started_at
        return 0.0

    @property
    def uptime_display(self) -> str:
        secs = self.uptime_seconds
        if secs <= 0:
            return "-"
        if secs < 60:
            return f"{int(secs)}s"
        if secs < 3600:
            return f"{int(secs // 60)}m {int(secs % 60)}s"
        hrs = int(secs // 3600)
        mins = int((secs % 3600) // 60)
        return f"{hrs}h {mins}m"


def _pid_alive(pid: int) -> bool:
    """Check if a process with *pid* is still alive."""
    try:
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            SYNCHRONIZE = 0x00100000
            handle = kernel32.OpenProcess(SYNCHRONIZE, False, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
            return False
        else:
            os.kill(pid, 0)
            return True
    except (OSError, ProcessLookupError):
        return False


def _kill_pid(pid: int, *, force: bool = False) -> bool:
    """Kill a process by PID. Returns True if signal was sent."""
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F"] if force else ["taskkill", "/PID", str(pid)],
                capture_output=True,
                timeout=5,
                            **HIDDEN_KW,
            )
        else:
            os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)
        return True
    except Exception:
        logger.debug("Failed to kill PID %d", pid, exc_info=True)
        return False


def _pause_pid(pid: int) -> bool:
    """Pause (suspend) a process. Unix only — no-op on Windows."""
    if sys.platform == "win32":
        logger.warning("Pause is not supported on Windows")
        return False
    try:
        os.kill(pid, signal.SIGSTOP)
        return True
    except Exception:
        return False


def _resume_pid(pid: int) -> bool:
    """Resume a paused process. Unix only — no-op on Windows."""
    if sys.platform == "win32":
        logger.warning("Resume is not supported on Windows")
        return False
    try:
        os.kill(pid, signal.SIGCONT)
        return True
    except Exception:
        return False


def _check_health(host: str, port: int, path: str = "/health") -> bool:
    """HTTP health check using stdlib (avoids heavy httpx import). Returns True on 200."""
    try:
        import urllib.request
        req = urllib.request.Request(f"http://{host}:{port}{path}")
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def _port_open(host: str, port: int) -> bool:
    """Fast TCP connect check (no HTTP). Used for pre-launch detection."""
    import socket
    try:
        with socket.create_connection((host, port), timeout=0.15):
            return True
    except (OSError, ConnectionRefusedError):
        return False


class GatewayManager:
    """
    Manages the lifecycle of CVC subsystem processes.

    Services managed:
      - **proxy**  — FastAPI CVC Cognitive Proxy (port 19333)
      - **mcp**    — MCP stdio/SSE server (no port by default)
      - **agent**  — Interactive agent sessions (tracked, not managed)
      - **sdk**    — SDK availability (no separate process)

    State is persisted to ``.cvc/services.json`` so a gateway restart
    can detect previously-launched child processes.
    """

    def __init__(self, cvc_root: Path, *, host: str = "127.0.0.1") -> None:
        self.cvc_root = cvc_root
        self.host = host
        self._services: dict[str, ServiceRecord] = {}
        self._state_file = cvc_root / "services.json"
        self._procs: dict[str, subprocess.Popen] = {}

        # Initialise default service records
        for name in ("proxy", "mcp", "agent", "sdk"):
            self._services[name] = ServiceRecord(name)

        # Load persisted state (reconcile with live OS state)
        self._load_state()

    # -- State persistence -------------------------------------------------

    def _load_state(self) -> None:
        """Load services.json and reconcile with live process state."""
        if not self._state_file.exists():
            return
        try:
            data = json.loads(self._state_file.read_text(encoding="utf-8"))
            for svc_data in data.get("services", []):
                name = svc_data.get("name")
                if name not in self._services:
                    continue
                rec = ServiceRecord.from_dict(svc_data)
                # Check if the PID is still alive
                if rec.pid and _pid_alive(rec.pid):
                    rec.status = STATUS_RUNNING
                else:
                    rec.pid = None
                    rec.status = STATUS_STOPPED
                    rec.started_at = None
                self._services[name] = rec
        except Exception:
            logger.debug("Could not load services.json", exc_info=True)

    def _save_state(self) -> None:
        """Persist current service state to services.json."""
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        data = {"services": [s.to_dict() for s in self._services.values()]}
        self._state_file.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    # -- Service accessors -------------------------------------------------

    def get_service(self, name: str) -> ServiceRecord | None:
        return self._services.get(name)

    def all_services(self) -> dict[str, ServiceRecord]:
        return dict(self._services)

    def service_status(self) -> list[dict[str, Any]]:
        """Return all service states as dicts (for API responses)."""
        return [s.to_dict() for s in self._services.values()]

    # -- Proxy lifecycle ---------------------------------------------------

    def start_proxy(self, port: int = 19333) -> ServiceRecord:
        """Start the CVC Cognitive Proxy.

        DEPRECATED: The proxy is now integrated into the gateway itself.
        This method marks the proxy as 'running' for backward-compatible
        service status reporting, but does NOT spawn a separate process.
        """
        rec = self._services["proxy"]
        rec.status = STATUS_RUNNING
        rec.port = port
        rec.started_at = rec.started_at or time.time()
        self._save_state()
        return rec

    def launch_proxy(self, port: int = 19333) -> ServiceRecord:
        """Launch the proxy process.

        DEPRECATED: The proxy is now integrated into the gateway itself.
        Alias for start_proxy() for backward compatibility.
        """
        return self.start_proxy(port)

    def stop_proxy(self) -> ServiceRecord:
        """Stop the proxy process.

        DEPRECATED: The proxy is now integrated into the gateway.
        Marks the service as stopped for status reporting.
        """
        rec = self._services["proxy"]
        rec.pid = None
        rec.status = STATUS_STOPPED
        rec.started_at = None
        self._procs.pop("proxy", None)
        self._save_state()
        return rec

    def restart_proxy(self, port: int = 19333) -> ServiceRecord:
        """Restart the proxy (deprecated — no-op, proxy is in-process)."""
        return self.start_proxy(port)

    def pause_proxy(self) -> ServiceRecord:
        """Pause the proxy (deprecated — no-op, proxy is in-process)."""
        rec = self._services["proxy"]
        return rec

    def resume_proxy(self) -> ServiceRecord:
        """Resume the proxy (deprecated — no-op, proxy is in-process)."""
        rec = self._services["proxy"]
        return rec

    # -- MCP lifecycle (informational; MCP is usually stdio) ---------------

    def update_mcp_status(
        self,
        *,
        running: bool = False,
        transport: str = "stdio",
        pid: int | None = None,
    ) -> ServiceRecord:
        """Update MCP status (since MCP is often started externally by IDEs)."""
        rec = self._services["mcp"]
        rec.status = STATUS_RUNNING if running else STATUS_STOPPED
        rec.transport = transport
        rec.pid = pid
        if running and not rec.started_at:
            rec.started_at = time.time()
        elif not running:
            rec.started_at = None
        self._save_state()
        return rec

    # -- Agent session tracking (informational) ----------------------------

    def update_agent_status(self, *, active_sessions: int = 0) -> ServiceRecord:
        """Update agent status (agent is part of the CLI, not a daemon)."""
        rec = self._services["agent"]
        rec.status = STATUS_RUNNING if active_sessions > 0 else STATUS_STOPPED
        self._save_state()
        return rec

    # -- SDK status (availability check) -----------------------------------

    def update_sdk_status(self) -> ServiceRecord:
        """Check SDK availability by inspecting the agent registry."""
        rec = self._services["sdk"]
        agents_dir = self.cvc_root / "agents"
        agent_count = len(list(agents_dir.glob("*.json"))) if agents_dir.exists() else 0
        rec.status = STATUS_RUNNING if agent_count > 0 else STATUS_STOPPED
        self._save_state()
        return rec

    # -- Lifecycle for all services ----------------------------------------

    def start_all(self, *, proxy_port: int = 19333) -> dict[str, ServiceRecord]:
        """Start all manageable services."""
        self.start_proxy(proxy_port)
        self.update_sdk_status()
        return dict(self._services)

    def stop_all(self) -> dict[str, ServiceRecord]:
        """Stop all managed services."""
        self.stop_proxy()
        for name, rec in self._services.items():
            if rec.pid and name != "proxy":
                _kill_pid(rec.pid)
                rec.pid = None
                rec.status = STATUS_STOPPED
                rec.started_at = None
        self._save_state()
        return dict(self._services)

    # -- Health polling (for background tasks) -----------------------------

    def refresh_health(self) -> dict[str, ServiceRecord]:
        """
        Re-check the live status of all services.

        Called periodically by the gateway's background health loop.
        """
        # Proxy
        proxy = self._services["proxy"]
        if proxy.port and proxy.status in (STATUS_RUNNING, STATUS_PAUSED):
            if proxy.pid and not _pid_alive(proxy.pid):
                proxy.status = STATUS_STOPPED
                proxy.pid = None
                proxy.started_at = None
            elif proxy.status == STATUS_RUNNING and not _check_health("127.0.0.1", proxy.port):
                proxy.status = STATUS_ERROR

        # SDK
        self.update_sdk_status()

        self._save_state()
        return dict(self._services)
