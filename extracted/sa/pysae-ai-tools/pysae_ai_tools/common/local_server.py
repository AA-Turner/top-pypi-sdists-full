"""Shared lifecycle for the local FastAPI dashboards.

Both the activity tracker (`tracker/server.py`) and the issue-audit report
(`glab/issue_audit/server.py`) run a short-lived uvicorn server on localhost,
reuse an already-running instance across invocations, and shut themselves down
after an idle timeout. `LocalServer` carries that machinery once so a fix
(zombie PID, occupied port, timeout) only has to be made in one place.

Each server keeps its own FastAPI routes and configuration (spawned module,
health endpoint, accepted statuses, idle timeout, PID file path) and delegates
port selection, PID bookkeeping, liveness probing, background spawn, keepalive
and the auto-shutdown timer to an instance of this class.
"""

import os
import signal
import socket
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class LocalServer:
    def __init__(
        self,
        *,
        app: Any,
        module: str,
        pid_file: Path,
        health_path: str,
        healthy_statuses: set[int],
        shutdown_timeout: int,
        keepalive_path: str = "/api/keepalive",
    ) -> None:
        self.app = app
        self.module = module
        self.pid_file = pid_file
        self.health_path = health_path
        self.healthy_statuses = healthy_statuses
        self.shutdown_timeout = shutdown_timeout
        self.keepalive_path = keepalive_path
        self._shutdown_timer: threading.Timer | None = None

    def schedule_shutdown(self) -> None:
        if self._shutdown_timer is not None:
            self._shutdown_timer.cancel()
        self._shutdown_timer = threading.Timer(self.shutdown_timeout, lambda: os.kill(os.getpid(), signal.SIGTERM))
        self._shutdown_timer.daemon = True
        self._shutdown_timer.start()

    @staticmethod
    def find_free_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            port: int = s.getsockname()[1]
            return port

    def save_pid_file(self, port: int) -> None:
        self.pid_file.write_text(f"{os.getpid()}:{port}", encoding="utf-8")

    def read_pid_file(self) -> tuple[int, int] | None:
        try:
            text = self.pid_file.read_text(encoding="utf-8").strip()
            pid_str, port_str = text.split(":")
            return int(pid_str), int(port_str)
        except (FileNotFoundError, ValueError):
            return None

    def is_alive(self, port: int) -> bool:
        try:
            resp = urllib.request.urlopen(f"http://127.0.0.1:{port}{self.health_path}", timeout=2)
            return resp.status in self.healthy_statuses
        except (urllib.error.URLError, OSError):
            return False

    def _keepalive(self, port: int) -> None:
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}{self.keepalive_path}", method="POST")
            urllib.request.urlopen(req, timeout=2)
        except (urllib.error.URLError, OSError):
            pass

    def _spawn_background(self, port: int) -> None:
        subprocess.Popen(
            [sys.executable, "-m", self.module, "--port", str(port)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    def ensure(self, port: int = 0) -> tuple[int, bool]:
        """Ensure a server is running. Returns (port, is_new)."""
        saved = self.read_pid_file()
        if saved:
            _, saved_port = saved
            if self.is_alive(saved_port):
                self._keepalive(saved_port)
                return saved_port, False
        actual_port = port if port else self.find_free_port()
        self._spawn_background(actual_port)
        return actual_port, True

    def run(self, port: int) -> None:
        import uvicorn

        self.save_pid_file(port)
        self.schedule_shutdown()
        uvicorn.run(self.app, host="127.0.0.1", port=port, log_level="warning")
