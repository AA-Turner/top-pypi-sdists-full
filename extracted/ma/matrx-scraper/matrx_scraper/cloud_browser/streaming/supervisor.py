"""Start and stop Selkies with the human-control lifecycle."""

from __future__ import annotations

import os
import signal
import socket
import subprocess
import threading
import time
from dataclasses import dataclass, field


@dataclass
class SelkiesSupervisor:
    executable: str = "/opt/selkies-gstreamer/selkies-gstreamer-run"
    # The container joins the private application network; the authenticated
    # app proxy is the only browser-facing route to this listener.
    address: str = "0.0.0.0"
    port: int = 8080
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
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=0.75)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=0.25)
