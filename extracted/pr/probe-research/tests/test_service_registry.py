"""The service's session registry: owners, generations, heartbeats, persistence.

Real processes stand in for agents (plan X3): an owner is `{pid, start_time}`,
its exit is seen by the kernel (pidfd / kqueue), a recycled pid reads as dead,
a higher generation replaces and a lower one is refused, a heartbeat-only owner
lapses after its TTL, and a restarted service restores what it knew.
"""

from __future__ import annotations

import contextlib
import os
import sys
import time

import pytest

from probe.service import client, paths, procid
from probe.service.protocol import ErrorCode, Method, Mode
from probe.service.registry import Outcome, Registry
from tests.service_harness import (  # noqa: F401 -- service_home is a fixture
    kill_agent,
    service_home,
    spawn_agent,
    wait_for,
)

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")


def _register(sh, sid, *, owner, generation=1, mode=Mode.INLINE, harness="test"):
    return sh.call(
        Method.SESSION_REGISTER,
        {"sid": sid, "harness": harness, "mode": mode, "owner": owner, "generation": generation},
    )


def _sessions(sh) -> dict:
    return {s["sid"]: s for s in sh.call(Method.SESSION_LIST)["sessions"]}


def test_an_owner_exit_ends_its_session_at_once(service_home):
    service_home.start()
    watcher = service_home.connect()
    watcher.call(Method.EVENTS_SUBSCRIBE, {"topics": ["session.started", "session.ended"]})
    agent, owner = spawn_agent()
    try:
        assert _register(service_home, "s-exit", owner=owner) == {"alive": True}
        started = watcher.next_event(3.0)
        assert started["topic"] == "session.started" and started["sid"] == "s-exit" and started["alive"]
        assert _sessions(service_home)["s-exit"]["alive"] is True
        killed = time.monotonic()
        kill_agent(agent)
        ended = watcher.next_event(3.0)
        took = time.monotonic() - killed
    finally:
        kill_agent(agent)
        watcher.close()
    assert ended == {"topic": "session.ended", "sid": "s-exit", "generation": 1, "reason": "owner_exit"}
    assert took < 1.0, f"owner exit seen after {took:.2f}s"
    assert "s-exit" not in _sessions(service_home)
    assert service_home.call(Method.STATUS)["sessions"] == 0


def test_a_recycled_pid_is_a_dead_owner(service_home):
    """The pid runs, but it is not the process that registered: mismatched start time."""
    service_home.start()
    agent, owner = spawn_agent()
    try:
        recycled = {"pid": owner["pid"], "start_time": owner["start_time"] + "0"}
        assert _register(service_home, "s-recycled", owner=recycled) == {"alive": False}
        assert "s-recycled" not in _sessions(service_home)
        gone = {"pid": 2**22 + 12345, "start_time": "1"}
        assert _register(service_home, "s-gone", owner=gone) == {"alive": False}
    finally:
        kill_agent(agent)


def test_generations_lower_refused_higher_replaces(service_home):
    service_home.start()
    first, owner1 = spawn_agent()
    second, owner2 = spawn_agent()
    try:
        assert _register(service_home, "s-gen", owner=owner1, generation=5) == {"alive": True}
        with pytest.raises(client.ServiceError) as refused:
            _register(service_home, "s-gen", owner=owner2, generation=3)
        assert refused.value.code == ErrorCode.REFUSED
        assert refused.value.data["reason"] == "stale_generation"
        assert _register(service_home, "s-gen", owner=owner2, generation=7) == {"alive": True}
        listed = _sessions(service_home)["s-gen"]
        assert listed["generation"] == 7 and listed["owner"] == owner2
        # The REPLACED owner's exit ends nothing: it was generation 5's.
        kill_agent(first)
        time.sleep(0.5)
        assert _sessions(service_home)["s-gen"]["alive"] is True
        # The same generation refreshes (a heartbeat), never replaces.
        assert _register(service_home, "s-gen", owner=owner2, generation=7, mode=Mode.DAEMON) == {"alive": True}
        assert _sessions(service_home)["s-gen"]["mode"] == Mode.DAEMON
        kill_agent(second)
        assert wait_for(lambda: "s-gen" not in _sessions(service_home), 3.0)
    finally:
        kill_agent(first)
        kill_agent(second)


def test_session_end_is_a_hint_for_its_generation_only(service_home):
    service_home.start()
    agent, owner = spawn_agent()
    try:
        _register(service_home, "s-end", owner=owner, generation=4)
        with pytest.raises(client.ServiceError) as refused:
            service_home.call(Method.SESSION_END, {"sid": "s-end", "generation": 3})
        assert refused.value.code == ErrorCode.REFUSED
        assert service_home.call(Method.SESSION_END, {"sid": "s-end", "generation": 4}) == {}
        assert "s-end" not in _sessions(service_home)
        # Idempotent, and a late heartbeat of the ended generation cannot revive it.
        assert service_home.call(Method.SESSION_END, {"sid": "s-end", "generation": 4}) == {}
        with pytest.raises(client.ServiceError):
            _register(service_home, "s-end", owner=owner, generation=4)
        assert service_home.call(Method.SESSION_END, {"sid": "never-registered", "generation": 1}) == {}
    finally:
        kill_agent(agent)


def test_a_heartbeat_only_owner_lapses_after_its_ttl(service_home, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_TTL_S", "0.6")
    service_home.start()
    watcher = service_home.connect()
    watcher.call(Method.EVENTS_SUBSCRIBE, {"topics": ["session.ended"]})
    assert _register(service_home, "s-beat", owner=None) == {"alive": True}
    time.sleep(0.35)
    assert _register(service_home, "s-beat", owner=None) == {"alive": True}  # refreshed
    time.sleep(0.35)
    assert _sessions(service_home)["s-beat"]["alive"] is True  # 0.7 s in, 0.35 s since the beat
    ended = watcher.next_event(2.0)
    watcher.close()
    assert ended == {"topic": "session.ended", "sid": "s-beat", "generation": 1, "reason": "expired"}
    assert "s-beat" not in _sessions(service_home)


def test_mode_off_never_counts_as_alive(service_home, monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.3")
    status = service_home.start()
    agent, owner = spawn_agent()
    try:
        assert _register(service_home, "s-off", owner=owner, mode=Mode.OFF) == {"alive": False}
        assert _register(service_home, "s-off-beat", owner=None, mode=Mode.OFF) == {"alive": False}
        # Registered and listed, but nothing holds the service: it idles out.
        assert service_home.wait_exit(status["pid"], 3.0)
    finally:
        kill_agent(agent)


def test_the_registry_survives_a_restart(service_home):
    status = service_home.start()
    agent, owner = spawn_agent()
    try:
        _register(service_home, "s-kept", owner=owner, generation=9)
        _register(service_home, "s-beat", owner=None, generation=2)
        dead, dead_owner = spawn_agent()
        _register(service_home, "s-dies", owner=dead_owner)
        stored = service_home.registry_file()
        assert {s["sid"] for s in stored["sessions"]} == {"s-kept", "s-beat", "s-dies"}
        service_home.call(Method.STOP)
        assert service_home.wait_exit(status["pid"], 3.0)
        kill_agent(dead)  # exits while no service watches
        restarted = service_home.start()
        assert restarted["pid"] != status["pid"]
        listed = _sessions(service_home)
        assert set(listed) == {"s-kept", "s-beat"}
        assert listed["s-kept"]["alive"] and listed["s-kept"]["generation"] == 9
        assert restarted["sessions"] == 2
        # Restored owners are watched again.
        kill_agent(agent)
        assert wait_for(lambda: "s-kept" not in _sessions(service_home), 3.0)
    finally:
        kill_agent(agent)


def test_the_registry_file_is_private(service_home):
    service_home.start()
    _register(service_home, "s-1", owner=None)
    assert paths.registry_path().stat().st_mode & 0o777 == 0o600


# -- the registry alone (no process), for the rules the timers hide ----------


def test_registry_rules_with_a_fake_clock(tmp_path):
    now = [1000.0]
    alive = {(101, "a"): True, (102, "b"): True}
    reg = Registry(
        tmp_path / "sessions.json",
        ttl=10.0,
        clock=lambda: now[0],
        owner_alive=lambda pid, start: alive.get((pid, start), False),
    )
    assert reg.register("s", "h", Mode.INLINE, {"pid": 101, "start_time": "a"}, 1).outcome == Outcome.NEW
    assert reg.register("s", "h", Mode.INLINE, {"pid": 101, "start_time": "a"}, 1).outcome == Outcome.REFRESHED
    replaced = reg.register("s", "h", Mode.INLINE, {"pid": 102, "start_time": "b"}, 2)
    assert replaced.outcome == Outcome.REPLACED and replaced.previous.generation == 1
    assert reg.drop("s", 1) is None  # the replaced generation's exit ends nothing
    assert reg.register("x", "h", Mode.INLINE, {"pid": 103, "start_time": "c"}, 1).outcome == Outcome.DEAD
    assert reg.register("hb", "h", Mode.DAEMON, None, 1).outcome == Outcome.NEW
    assert reg.alive_count() == 2
    now[0] += 10.0
    assert [s.sid for s in reg.expired()] == ["hb"]
    assert reg.alive_count() == 1
    assert reg.next_expiry() == 1010.0


def test_procid_matches_a_real_process():
    pid = os.getpid()
    start = procid.start_time(pid)
    assert start
    assert procid.alive(pid, start) is True
    assert procid.alive(pid, start + "1") is False
    assert procid.alive(2**22 + 4321, start) is False


_TAP_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugins", "probe-research-tap")
_TAP_LINK = """
import json, os, sys, time
sys.path.insert(0, sys.argv[1])
from tap import service_link
owner = json.loads(sys.argv[3])
link = service_link.ServiceLink(sys.argv[2], harness="test", owner_fn=lambda: owner,
                                heartbeat_s=0.3, retry_s=0.05, undecided_wait_s=0)
link.start()
sys.stdout.write("started\\n"); sys.stdout.flush()
sys.stdin.readline()
link.stop()
"""


def test_the_tap_link_registers_and_ends_against_the_real_service(service_home, monkeypatch):
    """The tap's vendored client against the real server: the contract both ends read."""
    import json
    import subprocess

    monkeypatch.delenv("XDG_STATE_HOME", raising=False)  # the switch's file, under this HOME
    service_home.start()
    agent, owner = spawn_agent()
    state = paths.home() / ".local" / "state" / "probe" / "sessions"
    state.mkdir(parents=True, exist_ok=True)
    (state / "s-tap.state").write_text("daemon")
    link = subprocess.Popen(
        [sys.executable, "-I", "-c", _TAP_LINK, _TAP_ROOT, "s-tap", json.dumps(owner)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
        env={**os.environ, "PROBE_TAP_SOURCE": "claude_code"},  # harness-literal-ok: the tap's default source
    )
    try:
        assert link.stdout.readline().strip() == "started"
        assert wait_for(lambda: "s-tap" in _sessions(service_home), 3.0)
        listed = _sessions(service_home)["s-tap"]
        assert listed["mode"] == Mode.DAEMON and listed["owner"] == owner and listed["alive"]
        link.stdin.write("\n")
        link.stdin.flush()
        assert link.wait(5) == 0
        assert "s-tap" not in _sessions(service_home)  # session.end on the way out
    finally:
        link.kill()
        kill_agent(agent)


_LAPSING_LINK = """
import sys
sys.path.insert(0, sys.argv[1])
from tap import service_link
link = service_link.ServiceLink(sys.argv[2], harness="test", owner_fn=lambda: None,
                                heartbeat_s=float(sys.argv[3]), retry_s=0.05, undecided_wait_s=0)
link.start()
sys.stdout.write("started\\n"); sys.stdout.flush()
sys.stdin.readline()
link.stop()
"""


def test_a_tap_link_whose_heartbeat_lapsed_registers_again(service_home, monkeypatch):
    """The service ended the link's OWN generation (a heartbeat-only owner past
    its TTL: a laptop that slept, a stalled tap). That is no newer registrant:
    the link must come back under a new generation, never step back for good."""
    import json
    import subprocess

    monkeypatch.setenv("PROBE_SERVICE_TTL_S", "0.5")
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    service_home.start()
    watcher = service_home.connect()
    watcher.call(Method.EVENTS_SUBSCRIBE, {"topics": ["session.ended"]})
    state = paths.home() / ".local" / "state" / "probe" / "sessions"
    state.mkdir(parents=True, exist_ok=True)
    (state / "s-lapse.state").write_text("full")
    link = subprocess.Popen(
        # Beats every 1.2 s against a 0.5 s TTL: every beat finds its generation ended.
        [sys.executable, "-I", "-c", _LAPSING_LINK, _TAP_ROOT, "s-lapse", "1.2"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
        env={**os.environ, "PROBE_TAP_SOURCE": "claude_code"},  # harness-literal-ok: the tap's default source
    )
    try:
        assert link.stdout.readline().strip() == "started"
        assert wait_for(lambda: "s-lapse" in _sessions(service_home), 3.0)
        first = _sessions(service_home)["s-lapse"]["generation"]
        ended = watcher.next_event(3.0)
        assert ended and ended["reason"] == "expired" and ended["generation"] == first, ended
        again = wait_for(lambda: _sessions(service_home).get("s-lapse"), 4.0)
        assert again, f"the link never registered again after its heartbeat lapsed:\n{json.dumps(_sessions(service_home))}"
        assert again["generation"] > first and again["alive"]
    finally:
        watcher.close()
        link.stdin.write("\n")
        link.stdin.flush()
        with contextlib.suppress(Exception):
            link.wait(5)
        link.kill()
