"""One service per MACHINE, also on a home folder many machines share (plan D8).

The service's folder, socket and locks are keyed by a hash of the OS's own
machine id; `runtime.json` and `app-update.json` stay in the shared folder
above. The desktop app (prbe-ai/desktop `src-tauri/src/service.rs`) computes
the same key: the vectors below are pinned there too. Clients from before the
key connect to the shared folder's socket, which the service serves while it
holds that folder's lock.
"""

from __future__ import annotations

import fcntl
import hashlib
import os
import socket
import sys
import time
from pathlib import Path

import pytest

from probe.service import client, paths
from probe.service.protocol import Client, Method, Mode
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

#: (machine id as the OS gives it, the folder name). Pinned in the desktop app's tests.
VECTORS = [
    ("0123456789abcdef0123456789abcdef", "26ebed430e5e1d10"),  # Linux /etc/machine-id
    ("6F1A2B3C-4D5E-6F70-8192-A3B4C5D6E7F8", "db0d06d5c7c9750f"),  # macOS IOPlatformUUID
    ("devbox", "0c9da4fea3124f10"),  # a hostname: neither exists
]


@pytest.fixture
def fresh_key(monkeypatch):
    monkeypatch.setattr(paths, "_machine_key", None)
    yield
    paths._machine_key = None


@pytest.mark.parametrize(("machine", "key"), VECTORS)
def test_the_folder_is_a_hash_of_the_machine_id(fresh_key, monkeypatch, machine, key):
    monkeypatch.setattr(paths, "machine_id", lambda: machine)
    assert paths.machine_key() == key == hashlib.sha256(b"probe-service\0" + machine.encode()).hexdigest()[:16]
    assert paths.service_dir() == paths.root_dir() / key
    assert paths.root_dir() == Path.home() / ".local" / "state" / "probe" / "service"


@pytest.mark.skipif(sys.platform == "darwin", reason="Linux's machine-id files")
def test_linux_reads_its_machine_id_and_falls_back_to_the_hostname(tmp_path, fresh_key, monkeypatch):
    first = tmp_path / "machine-id"
    first.write_text("0123456789abcdef0123456789abcdef\n")
    monkeypatch.setattr(paths, "MACHINE_ID_FILES", (str(tmp_path / "missing"), str(first)))
    assert paths.machine_id() == "0123456789abcdef0123456789abcdef"
    monkeypatch.setattr(paths, "MACHINE_ID_FILES", (str(tmp_path / "missing"),))
    assert paths.machine_id() == socket.gethostname()


@pytest.mark.skipif(sys.platform != "darwin", reason="the Mac's hardware UUID")
def test_macos_reads_its_hardware_uuid():
    uuid = paths._darwin_uuid()
    assert uuid and len(uuid) == 36 and uuid == uuid.upper()


def test_two_machines_sharing_a_home_get_two_services(fresh_key, monkeypatch):
    monkeypatch.setattr(paths, "machine_id", lambda: "node-a")
    a = (paths.service_dir(), paths.socket_path(), paths.lock_path(), paths.registry_path(), paths.barrier_path())
    paths._machine_key = None
    monkeypatch.setattr(paths, "machine_id", lambda: "node-b")
    b = (paths.service_dir(), paths.socket_path(), paths.lock_path(), paths.registry_path(), paths.barrier_path())
    assert all(x != y for x, y in zip(a, b))
    # What describes the install, not the machine, stays shared.
    assert paths.runtime_path().parent == paths.app_update_path().parent == paths.root_dir()


def test_a_client_from_before_the_key_reaches_the_service(service_home):
    """An older tap or app connects to `root_dir()/service.sock`."""
    service_home.start()
    legacy = paths.legacy_socket_path()
    assert wait_for(legacy.exists, 5.0), service_home.log()
    agent, owner = spawn_agent()
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        sock.connect(str(legacy))
        conn = client.Connection(sock)
        conn.hello(Client.TAP, "0.9.24")
        conn.call(
            Method.SESSION_REGISTER,
            {"sid": "s-old", "harness": "claude_code", "mode": Mode.INLINE, "owner": owner, "generation": 1},
        )
        conn.close()
        with service_home.connect() as now:
            assert [s["sid"] for s in now.call(Method.SESSION_LIST)["sessions"]] == ["s-old"]
    finally:
        kill_agent(agent)


def test_the_old_door_opens_once_an_older_service_lets_go(service_home, monkeypatch):
    """A service from before the key still runs (it holds the shared folder's
    lock): the new one serves its own socket, and the old one's once it exits."""
    monkeypatch.setenv("PROBE_SERVICE_LEGACY_RETRY_S", "0.5")
    paths.private_dir(paths.root_dir())
    old = os.open(paths.legacy_lock_path(), os.O_RDWR | os.O_CREAT, 0o600)
    fcntl.flock(old, fcntl.LOCK_EX)
    try:
        service_home.start()
        time.sleep(1.0)
        assert not paths.legacy_socket_path().exists()
    finally:
        os.close(old)  # the older service exits
    assert wait_for(paths.legacy_socket_path().exists, 5.0), service_home.log()
    assert "also serving" in service_home.log()


def test_a_client_finds_a_service_from_before_the_key(service_home):
    """An older CLI (not updated yet) starts an older service, which listens on
    the shared folder's socket only: this client still reaches it."""
    import threading

    legacy = paths.legacy_socket_path()
    paths.private_dir(legacy.parent)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(str(legacy))
    server.listen(1)
    answered = []

    def serve():
        conn, _ = server.accept()
        answered.append(True)
        conn.close()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        conn = client.connect(1.0)
        assert conn is not None
        conn.close()
        thread.join(5)
        assert answered
    finally:
        server.close()
        legacy.unlink()
