"""The Probe service's lifecycle, with real processes in a throwaway HOME.

One service per user no matter how many sessions start it at once; it exits a
grace period after the last live session (or keep-alive client) is gone, never
during its discovery window; a crash is repaired by the next `ensure`; a
second instance leaves at once. Plan T3, API v1 "Lifecycle".
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time

import pytest

from probe.service import client, paths
from probe.service.protocol import Method, Mode
from tests.service_harness import (  # noqa: F401 -- service_home is a fixture
    kill_agent,
    pid_running,
    service_home,
    spawn_agent,
    wait_for,
)

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

_ENSURE = "from probe.service import client; print(client.ensure())"


def test_twenty_concurrent_ensures_start_exactly_one_service(service_home):
    procs = [
        subprocess.Popen([sys.executable, "-c", _ENSURE], stdout=subprocess.PIPE, text=True) for _ in range(20)
    ]
    outcomes = [p.communicate(timeout=30)[0].strip() for p in procs]
    assert all(p.returncode == 0 for p in procs)
    assert outcomes.count(client.Ensured.SPAWNED) <= 1, outcomes
    status = wait_for(service_home.status, 5.0)
    assert status, service_home.log()
    # Every spawn ensure made is recorded; a duplicate instance would also have
    # to get past service.lock, so count the live processes too.
    starts = json.loads(paths.starts_path().read_text())["starts"]
    assert len(starts) == 1, starts
    time.sleep(0.3)
    live = service_home.service_processes()
    assert live == [status["pid"]], (live, status)


def test_ensure_finds_the_running_service_and_spawns_nothing(service_home):
    first = service_home.start()
    assert client.ensure() == client.Ensured.RUNNING
    assert service_home.status()["pid"] == first["pid"]


def test_idle_exit_follows_the_last_session_within_the_grace(service_home, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "1")
    status = service_home.start()
    agent, owner = spawn_agent()
    try:
        assert service_home.call(
            Method.SESSION_REGISTER,
            {"sid": "s-1", "harness": "test", "mode": Mode.INLINE, "owner": owner, "generation": 1},
        ) == {"alive": True}
        time.sleep(1.5)  # past the grace: the live session holds it
        assert pid_running(status["pid"])
        ended = time.monotonic()
        kill_agent(agent)
        assert service_home.wait_exit(status["pid"], 5.0)
        took = time.monotonic() - ended
    finally:
        kill_agent(agent)
    assert took <= 1.0 + 0.5, f"exited {took:.2f}s after the last session (grace 1s)"
    assert not service_home.socket.exists()
    assert "stopping (idle)" in service_home.log()


def test_discovery_window_blocks_idle_exit(service_home, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_DISCOVERY_S", "1.5")
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.2")
    started = time.monotonic()
    status = service_home.start()
    assert status["state"] == "discovering"
    assert status["discovering_until"] is not None
    time.sleep(1.0)
    assert pid_running(status["pid"]), "exited inside its discovery window"
    assert service_home.wait_exit(status["pid"], 5.0)
    assert time.monotonic() - started >= 1.5


def test_a_keepalive_connection_holds_the_service(service_home, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.3")
    status = service_home.start()
    app = service_home.connect(keepalive=True, who="app")
    try:
        time.sleep(1.2)
        assert pid_running(status["pid"]), "a keep-alive client did not hold the service"
        assert service_home.call(Method.STATUS)["app_clients"] == 1
        closed = time.monotonic()
    finally:
        app.close()
    assert service_home.wait_exit(status["pid"], 3.0)
    assert time.monotonic() - closed <= 0.3 + 0.5


def test_a_plain_connection_does_not_hold_it(service_home, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.3")
    status = service_home.start()
    with service_home.connect():
        assert service_home.wait_exit(status["pid"], 3.0)


def test_a_crashed_service_is_respawned_by_the_next_ensure(service_home):
    first = service_home.start()
    os.kill(first["pid"], signal.SIGKILL)
    assert service_home.wait_exit(first["pid"], 3.0)
    # The dead service left its socket file behind: ensure must see through it.
    assert client.ensure() == client.Ensured.SPAWNED
    second = wait_for(service_home.status, 5.0)
    assert second and second["pid"] != first["pid"]


def test_ensure_backs_off_after_three_starts_a_minute(service_home):
    for _ in range(3):
        status = service_home.start()
        os.kill(status["pid"], signal.SIGKILL)
        assert service_home.wait_exit(status["pid"], 3.0)
    assert client.ensure() == client.Ensured.BACKOFF
    assert service_home.status() is None


def test_a_second_instance_exits_zero_at_once(service_home):
    first = service_home.start()
    started = time.monotonic()
    second = subprocess.run([sys.executable, "-m", "probe.service"], timeout=10, capture_output=True)
    assert second.returncode == 0
    assert time.monotonic() - started < 3.0
    assert service_home.status()["pid"] == first["pid"]


def test_service_stop_stops_it_and_says_so_to_subscribers(service_home):
    status = service_home.start()
    watcher = service_home.connect()
    watcher.call(Method.EVENTS_SUBSCRIBE, {"topics": ["service.stopping"]})
    assert service_home.call(Method.STOP) == {"stopping": True}
    event = watcher.next_event(3.0)
    watcher.close()
    assert event == {"topic": "service.stopping", "reason": "stop"}
    assert service_home.wait_exit(status["pid"], 3.0)
    assert not service_home.socket.exists()


def test_the_service_starts_with_a_clean_environment(service_home, monkeypatch):
    """Plan X2: never the first launcher's token, endpoint or PYTHONPATH."""
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_secret")
    monkeypatch.setenv("PROBE_BASE_URL", "https://example.invalid")
    status = service_home.start()
    environ = f"/proc/{status['pid']}/environ"
    if not os.path.exists(environ):
        pytest.skip("no /proc to read the service's environment from")
    env = dict(
        item.split(b"=", 1) for item in open(environ, "rb").read().split(b"\0") if b"=" in item
    )
    assert b"PROBE_TOKEN" not in env and b"PROBE_BASE_URL" not in env and b"PYTHONPATH" not in env
    assert env[b"HOME"] == str(service_home.home).encode()


def test_socket_ready_within_300ms_of_the_spawn(service_home):
    """Plan "Super lightweight": socket ready <= 150 ms warm; 300 ms on CI. Best of 3."""
    best = None
    for _ in range(3):
        started = time.monotonic()
        assert client.ensure() in (client.Ensured.SPAWNED, client.Ensured.RUNNING)
        assert wait_for(lambda: client.connect(0.2), 5.0)
        took = time.monotonic() - started
        best = took if best is None else min(best, took)
        status = service_home.status()
        service_home.call(Method.STOP)
        service_home.wait_exit(status["pid"], 3.0)
        paths.starts_path().unlink()  # not a crash loop: three deliberate starts
    assert best < 0.3, f"socket ready after {best * 1000:.0f} ms"
