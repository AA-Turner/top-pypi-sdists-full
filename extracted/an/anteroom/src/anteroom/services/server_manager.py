"""Background web server process management.

Provides PID file lifecycle, process health probing, and cross-platform
start/stop for the Anteroom web UI server.
"""

from __future__ import annotations

import json
import logging
import os
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

IS_WINDOWS = sys.platform == "win32"

_MAX_LOG_BYTES = 10 * 1024 * 1024  # 10 MB

# Windows process creation flags
_CREATE_NEW_PROCESS_GROUP = 0x00000200
_CREATE_NO_WINDOW = 0x08000000
_PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
_PROCESS_TERMINATE = 0x0001


@dataclass(frozen=True)
class ServerStatus:
    """Snapshot of background server state."""

    pid: int | None
    port: int
    alive: bool
    responding: bool
    start_time: float | None
    log_path: Path


class ServerManager:
    """Manages a background Anteroom server process.

    Parameterized by *service_name* so multiple services (e.g. the web UI and
    the docs site) can coexist in the same ``data_dir`` with disjoint pid,
    log, and progress files.

    File layout:
      - PID: ``{data_dir}/anteroom-{service_name}-{port}.pid``
      - Log: ``{data_dir}/anteroom-{service_name}.log``
      - Progress: ``{data_dir}/anteroom-{service_name}-{port}.progress``

    ``bg_worker_flag`` is the hidden flag emitted into the subprocess argv
    by :meth:`start_background`; the CLI re-dispatches on it.
    """

    def __init__(
        self,
        data_dir: Path,
        host: str = "127.0.0.1",
        port: int = 8080,
        *,
        service_name: str = "web",
        bg_worker_flag: str = "--_bg-worker",
    ) -> None:
        self.data_dir = data_dir
        self.host = host
        self.port = port
        self.service_name = service_name
        self.bg_worker_flag = bg_worker_flag
        self.pid_path = data_dir / f"anteroom-{service_name}-{port}.pid"
        self.progress_path = data_dir / f"anteroom-{service_name}-{port}.progress"
        self.log_path = data_dir / f"anteroom-{service_name}.log"
        # Legacy PID path retained for a one-release fallback so web servers
        # running at upgrade time are not orphaned. Only honoured for the
        # default "web" service.
        self._legacy_pid_path: Path | None = data_dir / f"anteroom-{port}.pid" if service_name == "web" else None

    # ------------------------------------------------------------------
    # PID file operations
    # ------------------------------------------------------------------

    def read_pid_info(self) -> dict | None:
        """Read PID file and return parsed JSON, or None if missing/invalid.

        Falls back to the legacy ``anteroom-{port}.pid`` filename (pre-service-
        name layout) for the default ``web`` service only, to avoid orphaning
        servers that were started before the upgrade.
        """
        candidates: list[Path] = [self.pid_path]
        if self._legacy_pid_path is not None:
            candidates.append(self._legacy_pid_path)

        for path in candidates:
            if not path.exists():
                continue
            try:
                text = path.read_text().strip()
            except OSError:
                continue
            if not text:
                continue
            try:
                info = json.loads(text)
            except json.JSONDecodeError:
                continue
            if not isinstance(info, dict) or "pid" not in info:
                continue
            return info
        return None

    def read_pid(self) -> int | None:
        """Return the PID from the PID file, or None."""
        info = self.read_pid_info()
        if info is None:
            return None
        pid = info.get("pid")
        if not isinstance(pid, int) or pid <= 0:
            return None
        return pid

    def write_pid(self, pid: int) -> None:
        """Write PID info as JSON to the PID file."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        info = {
            "pid": pid,
            "port": self.port,
            "host": self.host,
            "start_time": time.time(),
        }
        self.pid_path.write_text(json.dumps(info) + "\n")

    def clear_pid(self) -> None:
        """Remove the PID file (and legacy fallback) if they exist."""
        try:
            self.pid_path.unlink(missing_ok=True)
        except OSError:
            pass
        if self._legacy_pid_path is not None:
            try:
                self._legacy_pid_path.unlink(missing_ok=True)
            except OSError:
                pass

    def clear_progress(self) -> None:
        """Remove the progress file if it exists."""
        try:
            self.progress_path.unlink(missing_ok=True)
        except OSError:
            pass

    # ------------------------------------------------------------------
    # Process / port health
    # ------------------------------------------------------------------

    @staticmethod
    def is_process_alive(pid: int) -> bool:
        """Check whether a process with the given PID is running."""
        if pid <= 0:
            return False
        if IS_WINDOWS:
            return _is_process_alive_windows(pid)
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        except OSError:
            return False

    @staticmethod
    def is_port_responding(host: str, port: int, timeout: float = 1.0) -> bool:
        """Check whether a TCP connection can be established."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    @classmethod
    def discover_pid_ports(cls, data_dir: Path, service_name: str) -> list[int]:
        """Discover all ports that have PID files for a given service.

        Scans ``data_dir`` for filenames matching
        ``anteroom-{service_name}-{port}.pid`` and returns the sorted list of
        port numbers. Non-integer segments are silently skipped. Returns ``[]``
        when the directory is missing, unreadable, or has no matching files.
        """
        prefix = f"anteroom-{service_name}-"
        suffix = ".pid"
        ports: list[int] = []
        try:
            entries = list(data_dir.iterdir())
        except OSError:
            return []
        for entry in entries:
            name = entry.name
            if not name.startswith(prefix) or not name.endswith(suffix):
                continue
            middle = name[len(prefix) : -len(suffix)]
            try:
                port = int(middle)
            except ValueError:
                continue
            if 1 <= port <= 65535:
                ports.append(port)
        ports.sort()
        return ports

    def get_status(self) -> ServerStatus:
        """Build a status snapshot from PID file + liveness probes.

        Host and port are preferred from the PID file (recorded at start) so
        ``stop``/``status`` callers do not need to re-supply ``--host``. Falls
        back to the instance attributes when the PID file omits those fields.
        """
        info = self.read_pid_info()
        pid = None
        start_time = None
        alive = False
        responding = False

        probe_host = self.host
        probe_port = self.port

        if info is not None:
            pid = info.get("pid")
            raw_time = info.get("start_time")
            if isinstance(raw_time, (int, float)) and raw_time > 0:
                start_time = float(raw_time)
            info_host = info.get("host")
            if isinstance(info_host, str) and info_host:
                probe_host = info_host
            info_port = info.get("port")
            if isinstance(info_port, int) and 1 <= info_port <= 65535:
                probe_port = info_port
            if isinstance(pid, int) and pid > 0:
                alive = self.is_process_alive(pid)
                if alive:
                    responding = self.is_port_responding(probe_host, probe_port)
            else:
                pid = None

        if not alive:
            responding = self.is_port_responding(probe_host, probe_port)

        return ServerStatus(
            pid=pid,
            port=probe_port,
            alive=alive,
            responding=responding,
            start_time=start_time,
            log_path=self.log_path,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start_background(
        self,
        *,
        debug: bool = False,
        extra_args: list[str] | None = None,
    ) -> int:
        """Launch the web server as a detached background process.

        Returns the child PID on success.
        Raises RuntimeError if the server is already running.
        """
        existing = self.read_pid()
        if existing is not None and self.is_process_alive(existing):
            raise RuntimeError(
                f"Server is already running (PID {existing}) on port {self.port}. "
                f"Use 'aroom stop' first, or 'aroom status' to check."
            )

        if existing is not None:
            self.clear_pid()

        self.clear_progress()
        self._rotate_log()

        self.data_dir.mkdir(parents=True, exist_ok=True)
        log_file = open(self.log_path, "a")  # noqa: SIM115

        cmd = [
            sys.executable,
            "-m",
            "anteroom",
            self.bg_worker_flag,
            "--port",
            str(self.port),
        ]
        if debug:
            cmd.append("--debug")
        if extra_args:
            cmd.extend(extra_args)

        kwargs: dict = {
            "stdout": log_file,
            "stderr": log_file,
            "stdin": subprocess.DEVNULL,
        }

        if IS_WINDOWS:
            kwargs["creationflags"] = _CREATE_NEW_PROCESS_GROUP | _CREATE_NO_WINDOW
        else:
            kwargs["start_new_session"] = True

        try:
            proc = subprocess.Popen(cmd, **kwargs)
        except Exception:
            log_file.close()
            raise
        log_file.close()

        try:
            self.write_pid(proc.pid)
        except Exception:
            proc.kill()
            raise
        return proc.pid

    def stop(self, timeout: float = 10.0) -> bool:
        """Stop the background server. Returns True if the process was stopped."""
        pid = self.read_pid()
        if pid is None:
            self.clear_pid()
            return False

        if not self.is_process_alive(pid):
            self.clear_pid()
            return False

        if IS_WINDOWS:
            stopped = _terminate_windows(pid, timeout)
        else:
            stopped = _terminate_unix(pid, timeout)

        self.clear_pid()
        self.clear_progress()
        return stopped

    # ------------------------------------------------------------------
    # Log rotation
    # ------------------------------------------------------------------

    def _rotate_log(self) -> None:
        """Truncate the log file if it exceeds the size cap."""
        try:
            if self.log_path.exists() and self.log_path.stat().st_size > _MAX_LOG_BYTES:
                self.log_path.write_text("")
        except OSError:
            pass


# ------------------------------------------------------------------
# Platform-specific helpers (module-level for easy patching)
# ------------------------------------------------------------------


def _is_process_alive_windows(pid: int) -> bool:
    """Check process liveness on Windows via kernel32."""
    try:
        import ctypes

        handle = ctypes.windll.kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, pid)  # type: ignore[attr-defined]
        if handle == 0:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)  # type: ignore[attr-defined]
        return True
    except (OSError, AttributeError):
        return False


def _terminate_unix(pid: int, timeout: float) -> bool:
    """Send SIGTERM, wait, then SIGKILL if needed."""
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return False
    except PermissionError:
        logger.warning("Permission denied sending SIGTERM to PID %d", pid)
        return False

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        except PermissionError:
            return True
        time.sleep(0.2)

    try:
        os.kill(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    return True


def _terminate_windows(pid: int, timeout: float) -> bool:
    """Terminate process on Windows."""
    try:
        import ctypes

        handle = ctypes.windll.kernel32.OpenProcess(_PROCESS_TERMINATE, False, pid)  # type: ignore[attr-defined]
        if handle == 0:
            return False
        ctypes.windll.kernel32.TerminateProcess(handle, 1)  # type: ignore[attr-defined]
        ctypes.windll.kernel32.CloseHandle(handle)  # type: ignore[attr-defined]
        return True
    except (OSError, AttributeError):
        return False
