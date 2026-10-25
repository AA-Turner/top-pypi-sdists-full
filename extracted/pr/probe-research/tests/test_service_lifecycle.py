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


@pytest.mark.realtime
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


_UNCLEAN = "ended without stopping"


def _run_record() -> dict:
    return json.loads((paths.service_dir() / "service.run").read_text())


def test_the_next_service_names_a_killed_one_and_never_a_stopped_one(service_home):
    """Crash-report plan B2: a service that left no stop record on this boot
    (SIGKILL, an OOM kill) is a `service_crash` at the next start; a stop on
    purpose (SIGTERM, `service.stop`, idle) writes its record and is none."""
    first = service_home.start()
    assert _run_record()["pid"] == first["pid"] and _run_record()["boot"]
    os.kill(first["pid"], signal.SIGTERM)
    assert service_home.wait_exit(first["pid"], 5.0)
    second = service_home.start()
    assert _UNCLEAN not in service_home.log()
    assert _run_record()["pid"] == second["pid"]
    os.kill(second["pid"], signal.SIGKILL)
    assert service_home.wait_exit(second["pid"], 5.0)
    third = service_home.start()
    assert service_home.log().count(f"{_UNCLEAN} (unclean_exit)") == 1
    service_home.call(Method.STOP)
    assert service_home.wait_exit(third["pid"], 5.0)
    # What the next start compares with (a fourth start here would meet
    # `ensure`'s back-off: three a minute).
    stop = json.loads((paths.service_dir() / "last-stop.json").read_text())
    assert stop["pid"] == third["pid"] == _run_record()["pid"] and stop["start"] == _run_record()["start"]


def test_ensure_backs_off_after_three_starts_a_minute(service_home):
    for _ in range(3):
        status = service_home.start()
        os.kill(status["pid"], signal.SIGKILL)
        assert service_home.wait_exit(status["pid"], 3.0)
    assert client.ensure() == client.Ensured.BACKOFF
    assert service_home.status() is None


def test_a_restart_on_purpose_is_no_start_to_back_off_from(service_home):
    """An update's restart and the tap restart right after it (a session asks
    for a newer tap) are no crash loop: the next start is never refused, or
    every hook meanwhile finds no service (5 h live run, R2)."""
    for _ in range(2):
        status = service_home.start()
        os.kill(status["pid"], signal.SIGKILL)
        assert service_home.wait_exit(status["pid"], 3.0)
    third = service_home.start()
    client.forget_start(third["pid"])  # what a service stopping for an update or a newer tap does
    assert len(json.loads(paths.starts_path().read_text())["starts"]) == 2
    service_home.call(Method.STOP)
    assert service_home.wait_exit(third["pid"], 3.0)
    assert client.ensure() == client.Ensured.SPAWNED
    os.kill(wait_for(service_home.status, 5.0)["pid"], signal.SIGKILL)


def test_idle_exits_and_manual_stops_are_no_starts_to_back_off_from(service_home, monkeypatch):
    """`ensure`'s back-off (three starts a minute) is for a service that dies.
    One that stopped on purpose -- idle, or `probe service stop` -- counted
    too, so a session starting right after two quick idle exits and a stop
    found no service for most of a minute (live test I, 2026-10-24)."""
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.2")
    for _ in range(2):
        status = service_home.start()
        assert service_home.wait_exit(status["pid"], 5.0), service_home.log()
    assert service_home.log().count("stopping (idle)") == 2
    third = service_home.start()
    service_home.call(Method.STOP)
    assert service_home.wait_exit(third["pid"], 5.0)
    starts = json.loads(paths.starts_path().read_text())["starts"]
    assert starts == [], starts
    assert client.ensure() == client.Ensured.SPAWNED
    assert wait_for(service_home.status, 5.0)


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


@pytest.mark.realtime
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


def _venv(tmp_path, cfg: str, scripts: tuple = ("python.exe",), home_files: tuple = ("python.exe",)):
    home = tmp_path / "base"
    home.mkdir()
    for name in home_files:
        (home / name).write_text("")
    venv = tmp_path / "venv"
    (venv / "Scripts").mkdir(parents=True)
    for name in scripts:
        (venv / "Scripts" / name).write_text("")
    (venv / "pyvenv.cfg").write_text(cfg.format(home=home), encoding="utf-8")
    return home, venv


def test_the_base_interpreter_keeps_the_venvs_own_build(tmp_path):
    """A free-threaded venv's launcher runs home's python3.13t.exe, not the
    regular python.exe beside it: the service must start that same build, or
    the venv's native packages (built for the other ABI) fail to import."""
    home, venv = _venv(tmp_path, "home = {home}\nversion_info = 3.13.1\n",
                       scripts=("python.exe", "python3.13t.exe"), home_files=("python.exe", "python3.13t.exe"))
    launcher = str(venv / "Scripts" / "python.exe")
    argv, env = client._without_venv_launcher([launcher, "-I"], {})
    assert argv == [str(home / "python3.13t.exe"), "-I"]
    assert env == {"__PYVENV_LAUNCHER__": launcher}


def test_the_base_interpreter_is_the_one_pyvenv_cfg_names(tmp_path):
    home, venv = _venv(tmp_path, "home = {home}\nexecutable = {home}/python3.13t.exe\n",
                       home_files=("python.exe", "python3.13t.exe"))
    argv, _ = client._without_venv_launcher([str(venv / "Scripts" / "python.exe")], {})
    assert argv == [str(home / "python3.13t.exe")]


def test_a_free_threaded_venv_without_its_interpreter_keeps_the_launcher(tmp_path):
    _, venv = _venv(tmp_path, "home = {home}\nversion_info = 3.13.1+freethreaded\n")
    launcher = [str(venv / "Scripts" / "python.exe"), "-I"]
    assert client._without_venv_launcher(launcher, {}) == (launcher, {})


def test_a_regular_venv_starts_homes_python(tmp_path):
    home, venv = _venv(tmp_path, "home = {home}\nversion_info = 3.12.7\n")
    argv, _ = client._without_venv_launcher([str(venv / "Scripts" / "python.exe")], {})
    assert argv == [str(home / "python.exe")]
