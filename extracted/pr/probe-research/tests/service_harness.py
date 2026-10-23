"""A real Probe service in a throwaway HOME, for the `test_service_*` files.

The service's socket path is fixed under `$HOME` (API v1, X2), so every test
gets its own short HOME under /tmp: short, because a UNIX socket path stops at
~100 bytes and pytest's own tmp paths (macOS's especially) pass that, which
would move the socket to the shared /tmp fallback. `runtime.json` names THIS
interpreter, so `ensure()` spawns the code under test (the package is installed
editable; the service runs `-I`, so PYTHONPATH is not what finds it).

Real processes only: `ensure` spawns `python -m probe.service` detached, and
teardown stops it (service.stop, then SIGKILL) so no test leaves one behind.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

from probe.service import client, paths, procid
from probe.service.protocol import Client, Method


def wait_for(predicate, timeout: float, interval: float = 0.02):
    deadline = time.monotonic() + timeout
    while True:
        value = predicate()
        if value:
            return value
        if time.monotonic() >= deadline:
            return value
        time.sleep(interval)


def _is_fake_core(pid: int) -> bool:
    """Is `pid` still a FakeCore child (never a process that reused its pid)?"""
    try:
        argv = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
    except OSError:
        try:
            argv = subprocess.run(["ps", "-o", "args=", "-p", str(pid)], capture_output=True, timeout=5).stdout.split()
        except (OSError, subprocess.SubprocessError):
            return False
    return b"probe.core.run" in argv and any(a.endswith(b"fake-python") for a in argv)


def pid_running(pid: int) -> bool:
    """Alive and not a zombie (a service we never waited on reads as exited)."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return procid.start_time(pid) is not None


class ServiceHome:
    def __init__(self, home: Path) -> None:
        self.home = home
        self.pids: set[int] = set()

    # -- paths ---------------------------------------------------------------
    @property
    def service_dir(self) -> Path:
        return paths.service_dir()

    @property
    def socket(self) -> Path:
        return paths.socket_path()

    # -- talking -------------------------------------------------------------
    def connect(self, *, hello: bool = True, keepalive: bool = False, who: str = Client.CLI) -> client.Connection:
        conn = client.Connection.open(2.0)
        if hello:
            conn.hello(who, "test", keepalive=keepalive)
        return conn

    def call(self, method: str, params: dict | None = None) -> object:
        return client.call(method, params, client=Client.CLI, client_version="test")

    def status(self) -> dict | None:
        try:
            answer = self.call(Method.STATUS)
        except OSError:
            return None
        self.pids.add(answer["pid"])
        return answer

    def start(self, timeout: float = 5.0) -> dict:
        """ensure() and wait until the service answers; its status."""
        outcome = client.ensure()
        status = wait_for(self.status, timeout)
        if not status and outcome == client.Ensured.RUNNING and not self.service_processes():
            # What answered was a service on its way out (its idle exit): the
            # next ensure starts one.
            outcome = client.ensure()
            status = wait_for(self.status, timeout)
        assert status, (
            f"no service answered within {timeout}s (ensure: {outcome}; service processes: "
            f"{self.service_processes()}; starts: {self._starts()}); log:\n{self.log()}"
        )
        return status

    def _starts(self) -> str:
        try:
            return paths.starts_path().read_text(encoding="utf-8")
        except OSError:
            return "(none)"

    def wait_exit(self, pid: int, timeout: float) -> bool:
        return wait_for(lambda: not pid_running(pid), timeout)

    def log(self) -> str:
        try:
            return paths.log_path().read_text(encoding="utf-8")
        except OSError:
            return "(no service.log)"

    def registry_file(self) -> dict:
        return json.loads(paths.registry_path().read_text(encoding="utf-8"))

    def service_processes(self) -> list[int]:
        """Live `-m probe.service` processes whose HOME is this one (Linux /proc)."""
        found = []
        proc = Path("/proc")
        if not proc.is_dir():
            return sorted(p for p in self.pids if pid_running(p))
        for entry in proc.iterdir():
            if not entry.name.isdigit():
                continue
            try:
                argv = (entry / "cmdline").read_bytes().split(b"\0")
                env = (entry / "environ").read_bytes().split(b"\0")
            except OSError:
                continue
            if b"probe.service" in argv and b"-m" in argv and f"HOME={self.home}".encode() in env:
                if pid_running(int(entry.name)):
                    found.append(int(entry.name))
        return sorted(found)

    def teardown(self) -> None:
        with contextlib.suppress(Exception):
            status = self.status()
            if status:
                self.call(Method.STOP)
                self.wait_exit(status["pid"], 3.0)
        for pid in set(self.pids) | set(self.service_processes()) | set(self.fake_children()):
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)

    def fake_children(self) -> list[int]:
        """`probe.core.run` stand-ins (`service_fakes.FakeCore`) still running:
        a test that failed before opening its gate leaves one waiting."""
        try:
            lines = (self.home / "fake-core.log").read_text(encoding="utf-8").splitlines()
        except OSError:
            return []
        pids = []
        for line in lines:
            with contextlib.suppress(ValueError, KeyError, TypeError):
                pids.append(int(json.loads(line)["pid"]))
        return [pid for pid in pids if pid_running(pid) and _is_fake_core(pid)]


@pytest.fixture
def service_home(monkeypatch: pytest.MonkeyPatch):
    home = Path(tempfile.mkdtemp(prefix="ps-", dir="/tmp"))
    monkeypatch.setenv("HOME", str(home))
    # Fast lifecycle by default; a test that measures the real defaults unsets these.
    monkeypatch.setenv("PROBE_SERVICE_DISCOVERY_S", "0")
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "30")
    paths.private_dir(paths.service_dir())
    client.write_runtime(sys.executable, "test")
    sh = ServiceHome(home)
    try:
        yield sh
    finally:
        sh.teardown()
        shutil.rmtree(home, ignore_errors=True)


def spawn_agent() -> tuple[subprocess.Popen, dict]:
    """A real process standing in for an agent, and its {pid, start_time} owner."""
    proc = subprocess.Popen(["sleep", "120"])
    owner = wait_for(lambda: client.owner_of(proc.pid), 2.0)
    assert owner, "could not read the stand-in agent's start time"
    return proc, owner


def kill_agent(proc: subprocess.Popen) -> None:
    with contextlib.suppress(OSError):
        proc.kill()
    with contextlib.suppress(Exception):
        proc.wait(timeout=5)
