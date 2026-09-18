"""Start and stop Selkies with the human-control lifecycle."""

from __future__ import annotations

import os
import json
import signal
import socket
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SelkiesSupervisor:
    executable: str = "/opt/selkies-gstreamer/selkies-gstreamer-run"
    # The container joins the private application network; the authenticated
    # app proxy is the only browser-facing route to this listener.
    address: str = "0.0.0.0"
    port: int = 8080
    rtc_config_path: str = "/tmp/rtc.json"
    _process: subprocess.Popen[bytes] | None = field(default=None, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)
    startup_timeout_seconds: float = 8.0

    @property
    def running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self) -> None:
        with self._lock:
            if self.running:
                return
            process = subprocess.Popen(
                [
                    self.executable,
                    f"--addr={self.address}",
                    f"--port={self.port}",
                    "--enable_https=false",
                    "--enable_basic_auth=false",
                    "--encoder=x264enc",
                    "--enable_resize=false",
                    "--enable_clipboard=false",
                    f"--rtc_config_json={self.rtc_config_path}",
                ],
                stdin=subprocess.DEVNULL,
                # The packaged launcher is a shell wrapper whose foreground
                # Python child owns the signalling listener.  A signal sent
                # only to the wrapper leaves that child alive on :8080, so the
                # next takeover collides with the orphan.  One private process
                # group makes the stream lifecycle atomic.
                start_new_session=True,
            )
            self._process = process
            try:
                self._wait_until_listening(process)
            except RuntimeError:
                self._process = None
                self._terminate_process(process)
                raise

    def configure_rtc(self, rtc_config: Any) -> None:
        """Refresh Selkies' watched config file without replacing its inode.

        Selkies 1.6.2 watches the existing path by close events; rename-based
        atomic writes are therefore invisible to its monitor.
        """
        encoded = json.dumps(
            rtc_config.model_dump(mode="json") if hasattr(rtc_config, "model_dump") else rtc_config,
            separators=(",", ":"),
        ).encode()
        with self._lock:
            path = Path(self.rtc_config_path)
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "wb", closefd=True) as handle:
                os.fchmod(handle.fileno(), 0o600)
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())

    def clear_rtc(self) -> None:
        with self._lock:
            try:
                os.unlink(self.rtc_config_path)
            except FileNotFoundError:
                pass

    def stop(self) -> None:
        with self._lock:
            process = self._process
            self._process = None
            if process is None or process.poll() is not None:
                return
            self._terminate_process(process)

    def _wait_until_listening(self, process: subprocess.Popen[bytes]) -> None:
        """Do not advertise human control before Selkies accepts stream traffic."""
        deadline = time.monotonic() + self.startup_timeout_seconds
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError("Selkies failed during startup")
            try:
                with socket.create_connection(("127.0.0.1", self.port), timeout=0.2):
                    return
            except OSError:
                time.sleep(0.05)
        raise RuntimeError("Selkies did not become ready during startup")

    @staticmethod
    def _terminate_process(process: subprocess.Popen[bytes]) -> None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            # The whole group is already gone — a launcher that died during
            # startup was reaped by poll(). Nothing is left to stop, and raising
            # here would mask the real startup failure the caller must see.
            return
        try:
            process.wait(timeout=0.75)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=0.25)
