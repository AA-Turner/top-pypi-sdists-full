"""The service's watch: what fails is reported once, with consent (crash-report plan B2, rev 5).

Unit half: a `Watch` with an injected clock and a stand-in report child --
the per-family windows (3 in 15 min, else the first), one child at a time and
its 60 s bound, consent (a session's own environment, its registrant's
`report_env`, every live session for a machine family, the login shell with
none live), nothing counted or sent while an update drains or discovers, the
once-per-version families, the rev 3 lease triggers on two scans, bounded
facts; `last_run` (a crash is no stop record on the same boot, or a recorded
crash; a reboot is not); each subsystem's hook (worker give-up and crash loop,
the hook queue, background children, `hooks.run`, the loop and threads, the
update streak); `report_env` in the registry; and the tap's copy of the
consent rule held equal to `report_policy`'s.

The real service, end to end, is `test_service_crash_reports.py`.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import os
import subprocess
import sys
import threading
import time
import types
from pathlib import Path

import pytest

from probe._shared import report_policy
from probe.service import background, hookqueue, paths, protocol, watch, workers
from probe.service.registry import Registry
from probe.service.watch import Family, Watch

# The watch runs wherever the service does, Windows included (R3).

SID = "11111111-2222-3333-4444-555555555555"
SID2 = "22222222-3333-4444-5555-666666666666"


#: The watch's POSIX-only rules, skipped on Windows with the reason each one has.
POSIX_LAST_RUN = pytest.mark.skipif(
    os.name == "nt", reason="Windows reports only a recorded crash (watch.WINDOWS: a logoff leaves no stop record "
    "and the uptime boot id survives it); test_on_windows_a_service_that_left_no_stop_record_is_no_crash pins that")
POSIX_WORKERS = pytest.mark.skipif(
    os.name == "nt", reason="the service supervises no daemon worker on Windows (WorkerHost.claim refuses there)")


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    # Windows: the home is USERPROFILE (the CLI config's folder) and the
    # service's files are under LOCALAPPDATA, not HOME (`paths.root_dir`).
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "AppData" / "Local"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "AppData" / "Roaming"))
    for name in ("XDG_CONFIG_HOME", "PROBE_CONFIG_PATH", "PROBE_TELEMETRY", "PROBE_DIAGNOSTICS", "PROBE_BASE_URL"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv(watch.REPORTS_ENV, "1")
    # Never the real service's records: one test's watch.json or last-crash.json
    # would be the next one's (and a person's service would read them).
    assert tmp_path in paths.service_dir().parents
    paths.private_dir(paths.service_dir())
    return tmp_path


class Session:
    """A registered session as the service hands it over (`registry.Session`'s shape)."""

    def __init__(self, sid: str, *, mode: str = "inline", state_dir: str | None = None, report_env=None,
                 owner: dict | None = None, heartbeat_at: float | None = None) -> None:
        self.sid, self.mode, self.state_dir, self.report_env = sid, mode, state_dir, report_env
        self.owner, self.owner_live = owner, True
        self.heartbeat_at = heartbeat_at if heartbeat_at is not None else 1_000_000.0


class Rig:
    """A Watch with an injected clock, sessions and report child. Built from
    the parameters its constructor takes, so a regression test runs against an
    older Watch too (and fails there for what it pins, not for a keyword)."""

    def __init__(self, **over) -> None:
        self.now = 1_000_000.0
        self.mono = 5_000.0
        self.calls: list = []
        self.lines: list = []
        self.sessions: list = []
        #: Registered sessions whose owner lives but whose mode is off (never "live").
        self.off_sessions: list = []
        self.hosted: dict = {}
        self.supervised: set = set()
        self.updating = False
        self.barrier = False
        #: The threads the blocking barrier check ran on.
        self.barrier_calls: list = []
        self.discovering = False
        self.login: dict | None = {}
        self.beats: list = []
        self.gate: asyncio.Event | None = None
        self.answer = (0, {"sent": True, "id": "r-1", "skipped": None, "path": None})

        async def run_report(params):
            self.calls.append(params)
            if self.gate is not None:
                await self.gate.wait()
            return self.answer

        async def login():
            return self.login

        params = dict(
            log=self.lines.append, loop_getter=lambda: None,
            quiet=lambda: self.updating or self._barrier_check(),  # an older Watch's one check
            updating=lambda: self.updating, barrier_up=self._barrier_check,
            discovering=lambda: self.discovering, sessions=lambda: list(self.sessions), voters=self._voters,
            hosted_env=lambda sid: self.hosted.get(sid), supervised=lambda sid: sid in self.supervised,
            recorders=lambda: list(self.beats),
            # The slower checks read nothing real unless a test hands them in:
            # never this machine's outbox, never a `/v1/me` with a saved key.
            outbox=lambda now: None, credentials=lambda **_: {},
            run_report=run_report, login=login, clock=lambda: self.now, monotonic=lambda: self.mono, scan_s=15.0,
        )
        accepted = inspect.signature(Watch).parameters
        params.update(over)
        self.watch = Watch(**{k: v for k, v in params.items() if k in accepted})

    def _barrier_check(self) -> bool:
        self.barrier_calls.append(threading.current_thread())
        return self.barrier

    def _voters(self) -> list:
        return [watch.Live(s.sid, hosted_env=self.hosted.get(s.sid), report_env=s.report_env)
                for s in self.sessions + self.off_sessions]

    def tick(self, seconds: float) -> None:
        """Time passes, awake: wall and monotonic alike."""
        self.now += seconds
        self.mono += seconds

    def waiting(self) -> int:
        """Incidents not yet sent (noted, or looked at and waiting for the slot)."""
        return len(getattr(self.watch, "_pending", {})) + len(getattr(self.watch, "_fresh", []))

    def note(self, *args, **kwargs) -> None:
        self.watch.note(*args, **kwargs)

    def send(self) -> None:
        asyncio.run(self._drain(self.watch._send_next()))

    def scan(self) -> None:
        asyncio.run(self._drain(self.watch._scan()))

    async def _drain(self, first) -> None:
        await first
        while self.watch._child is not None or self.watch._tasks:
            if self.watch._child is not None:
                await asyncio.gather(self.watch._child, return_exceptions=True)
            if self.watch._tasks:
                await asyncio.gather(*list(self.watch._tasks), return_exceptions=True)
            # A finished task leaves `_tasks` in its done callback, on a later
            # turn: gather (3.12) completes at once for done ones, without one.
            await asyncio.sleep(0)
        if self.watch._timer is not None:
            self.watch._timer.cancel()
            self.watch._timer = None

    def families(self) -> list:
        return [(c["family"], c["reason"], c["sid"]) for c in self.calls]


@pytest.fixture
def rig():
    return Rig()


# -- the windows ---------------------------------------------------------------


def test_three_recorder_failures_in_15_minutes_are_one_report_about_that_session(rig):
    rig.hosted[SID] = {"HOME": "/h", "PROBE_TEST": "x"}
    rig.sessions = [Session(SID)]
    for n in range(2):
        rig.note(Family.RECORDER, "failing", SID, {"failures": n + 1}, env=rig.hosted[SID])
    rig.send()
    assert rig.calls == [], "two are not yet a report"
    rig.note(Family.RECORDER, "failing", SID, {"failures": 3, "detail": "boom"}, env=rig.hosted[SID])
    rig.send()
    (call,) = rig.calls
    assert call["auto"] is True and call["family"] == "recorder" and call["reason"] == "failing" and call["sid"] == SID
    # Only the consent variables of its environment, never the rest of it.
    assert call["env"] == {}
    assert call["facts"]["count"] == 3 and call["facts"]["window_s"] == watch.WINDOW_S
    assert call["facts"]["events"][-1] == {"failures": 3, "detail": "boom"}
    assert any("report recorder (failing) (session" in line and "sent r-1" in line for line in rig.lines)
    for _ in range(6):  # it keeps failing: the next ones are inside the report's 6 h
        rig.note(Family.RECORDER, "failing", SID, {}, env=rig.hosted[SID])
    rig.send()
    assert len(rig.calls) == 1


def test_failures_spread_past_the_window_are_none(rig):
    for _ in range(4):
        rig.note(Family.HOOK, "did_not_finish", None, {"lane": "stop"})
        rig.mono += watch.WINDOW_S / 2 + 1
    rig.send()
    assert rig.calls == []


def test_a_family_without_a_threshold_reports_its_first_event(rig):
    rig.sessions = [Session("a", report_env=True)]
    rig.note(Family.BACKGROUND, "early_exit", None, {"code": 1})
    rig.send()
    assert rig.families() == [("background", "early_exit", None)]
    assert rig.calls[0]["facts"] == {"code": 1} and rig.calls[0]["env"] == {}


# -- consent -------------------------------------------------------------------


@pytest.mark.parametrize("off", [
    {"PROBE_TELEMETRY": "off"}, {"PROBE_DIAGNOSTICS": "0"}, {"PROBE_BASE_URL": "https://probe.example.com"},
])
def test_a_session_whose_environment_turns_reports_off_gets_none(rig, off):
    rig.sessions = [Session(SID)]
    for _ in range(3):
        rig.note(Family.RECORDER, "failing", SID, {}, env={"HOME": "/h", **off})
    rig.send()
    assert rig.calls == []
    assert any("not reported" in line for line in rig.lines)
    for _ in range(3):  # declined: not asked again for the report's window
        rig.note(Family.RECORDER, "failing", SID, {}, env={"HOME": "/h", **off})
    rig.send()
    assert rig.calls == [] and sum("not reported" in line for line in rig.lines) == 1


@pytest.mark.parametrize("said, sent", [(True, True), (False, False), (None, False)])
def test_a_registered_session_decides_by_its_report_env(rig, said, sent):
    """No environment of its own here (a `tap watch` session's lease): what its
    registrant said; an older registrant that said nothing is a no."""
    rig.sessions = [Session(SID, report_env=said)]
    rig.note(Family.WORKER, "lease_error", SID, {"source": "lease"})
    rig.send()
    assert bool(rig.calls) is sent
    if sent:
        assert rig.calls[0]["env"] == {}


def test_a_hosted_session_s_recorder_environment_decides_over_its_report_env(rig):
    rig.sessions = [Session(SID, report_env=True)]
    rig.hosted[SID] = {"PROBE_TELEMETRY": "off"}
    rig.note(Family.WORKER, "hung", SID, {})
    rig.send()
    assert rig.calls == []


def test_a_machine_family_is_sent_when_every_session_live_at_its_moment_allows_it(rig):
    rig.sessions = [Session("a"), Session("b", report_env=True)]
    rig.hosted["a"] = {"HOME": "/h"}
    rig.note(Family.SERVICE_CRASH, "unclean_exit", None, {"previous": {}})
    rig.send()
    assert rig.families() == [("service_crash", "unclean_exit", None)] and rig.calls[0]["env"] == {}


def test_a_no_from_a_session_live_when_it_happened_drops_it_even_after_that_session_ends(rig):
    """Review #1 (reproduced): it used to WAIT, and went out once the opted-out
    session ended and the login shell (which says nothing) decided."""
    rig.sessions = [Session("a")]
    rig.hosted["a"] = {"PROBE_TELEMETRY": "off"}
    for _ in range(3):
        rig.note(Family.HOOK_HOST, "timed_out", None, {"lane": "pre-tool"})
    rig.send()
    assert rig.calls == []
    rig.sessions.clear()  # it ends; the desktop app keeps the service up
    rig.hosted.clear()
    rig.send()
    rig.tick(3600)
    rig.send()
    assert rig.calls == [], "a no is a no"
    assert any("hook_host (timed_out) not reported: session a does not allow reports" in line for line in rig.lines)


def test_the_environment_it_happened_in_can_say_no_to_a_machine_family(rig):
    """A `hooks.run` event, a queued hook event, a background child each run
    with their caller's environment: its opt-out counts (review #1)."""
    rig.sessions = [Session("a", report_env=True)]
    for env in ({"HOME": "/h"}, {"PROBE_DIAGNOSTICS": "off"}, {"HOME": "/h"}):
        rig.note(Family.HOOK_HOST, "timed_out", None, {"lane": "pre-tool"}, env=env)
    rig.send()
    assert rig.calls == []
    rig.note(Family.BACKGROUND, "early_exit", None, {}, env={"PROBE_TELEMETRY": "on"})
    rig.send()
    assert rig.families() == [("background", "early_exit", None)]


def test_a_session_whose_probe_is_off_is_asked_too(rig):
    """Mode `off` is never "live" (it holds nothing), but its agent runs and
    its registrant said no: a machine report waits for nobody, it is dropped."""
    rig.sessions = [Session("a", report_env=True)]
    rig.off_sessions = [Session("o", mode="off", report_env=False)]
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    assert rig.calls == []


@pytest.mark.parametrize("login, sent", [({}, True), ({"PROBE_TELEMETRY": "false"}, False), (None, False)])
def test_with_no_live_session_the_login_environment_decides(rig, login, sent):
    rig.login = login
    rig.note(Family.UPDATE_FAILED, "failed_in_a_row", None, {"in_a_row": 3})
    rig.send()
    assert bool(rig.calls) is sent


def test_a_self_hosted_cli_config_says_no_to_a_machine_family(rig, home):
    from probe.sdk.config import save_context

    # The CLI's own writer: wherever it keeps the config on this OS, the watch reads it there.
    written = save_context({"base_url": "http://10.0.0.5:8000"})
    assert home in written.parents
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    assert rig.calls == []


def test_the_suite_s_switch_turns_the_watch_off(monkeypatch):
    monkeypatch.setenv(watch.REPORTS_ENV, "0")
    off = Rig()
    off.note(Family.BACKGROUND, "early_exit", None, {})
    off.send()
    assert off.calls == [] and off.waiting() == 0


# -- when nothing is sent ------------------------------------------------------


def test_nothing_counts_while_an_update_drains_and_nothing_is_sent_until_it_ends(rig):
    rig.sessions = [Session(SID, report_env=True)]
    rig.updating = True
    for _ in range(5):
        rig.note(Family.RECORDER, "failing", SID, {})
    rig.note(Family.WORKER, "crash_loop", SID, {})
    assert rig.waiting() == 0, "a hand-over's failures are its own"
    rig.note(Family.SERVICE_CRASH, "unclean_exit", None, {})  # not the update's doing: kept
    rig.send()
    assert rig.calls == []
    rig.updating = False
    rig.send()
    assert rig.families() == [("service_crash", "unclean_exit", None)]


def test_nothing_is_sent_while_discovering(rig):
    rig.discovering = True
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    assert rig.calls == []
    rig.discovering = False
    rig.send()
    assert len(rig.calls) == 1


def test_one_report_child_at_a_time(rig):
    async def go():
        rig.gate = asyncio.Event()
        rig.note(Family.BACKGROUND, "early_exit", None, {})
        rig.note(Family.TAP_LOAD, "import_failed", None, {"tap_version": "0.10.99"})
        await rig.watch._send_next()
        await asyncio.sleep(0.05)
        await rig.watch._send_next()  # a scan meanwhile: the slot is taken
        assert len(rig.calls) == 1
        rig.gate.set()
        await rig._drain(asyncio.sleep(0))
        assert [c["family"] for c in rig.calls] == ["background", "tap_load"]

    asyncio.run(go())


def test_a_scan_and_a_note_s_kick_asking_at_once_start_one_child(rig):
    """Both ask before either has taken the incident (the first awaits a thread)."""
    async def go():
        rig.note(Family.UPDATE_REJECTED, "switched_back", None, {"rejected_version": "9.9.9"})
        await asyncio.gather(rig.watch._send_next(), rig.watch._send_next())
        await rig._drain(asyncio.sleep(0))

    asyncio.run(go())
    assert len(rig.calls) == 1


def test_the_report_child_is_the_report_read_killed_at_60_s(monkeypatch):
    seen = {}

    async def run_read(action, request, *, env_extra=None, timeout):
        seen.update(action=action, request=request, timeout=timeout, env_extra=env_extra)
        return None, None

    from probe.service import children

    monkeypatch.setattr(children, "run_read", run_read)
    assert asyncio.run(watch._run_report({"family": "hook"})) == (None, None)
    assert seen == {"action": "report", "request": {"family": "hook"}, "timeout": 60.0, "env_extra": None}
    assert watch.outcome(None, None) == "killed after 60 s"
    assert watch.outcome(0, {"sent": False, "skipped": "deduped"}) == "not sent: deduped"
    assert watch.outcome(2, None) == "failed (exit 2)"


def test_a_child_that_cannot_start_is_logged_and_the_next_goes_on(rig):
    async def broken(params):
        rig.calls.append(params)
        raise OSError("no interpreter")

    rig.watch.run_report = broken
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    assert len(rig.calls) == 1 and any("could not start: no interpreter" in line for line in rig.lines)


# -- once per version ----------------------------------------------------------


def _guard(**record) -> None:
    (paths.service_dir() / "guard.json").write_text(json.dumps(record))


def test_a_rejected_release_is_reported_once_per_version(rig):
    rig.sessions = [Session("a", report_env=True)]
    _guard(at=rig.now - 60, ok=False, to="9.9.9", reason="the new service did not answer", rollback="done",
           active="1.0.0", answering="1.0.0", **{"from": "1.0.0"})
    rig.scan()
    rig.scan()
    assert rig.families() == [("update_rejected", "switched_back", None)]
    facts = rig.calls[0]["facts"]
    assert facts["rejected_version"] == "9.9.9" and facts["from"] == "1.0.0" and facts["rollback"] == "done"
    again = Rig()  # the next service: watch.json remembers the version
    again.sessions = [Session("a", report_env=True)]
    again.scan()
    assert again.calls == []
    _guard(at=again.now - 60, ok=False, to="9.9.10", reason="crashed", **{"from": "1.0.0"})
    again.scan()
    assert [c["facts"]["rejected_version"] for c in again.calls] == ["9.9.10"]


@pytest.mark.parametrize("record", [
    {"ok": True, "to": "9.9.9"}, {"ok": None, "state": "watching", "to": "9.9.9"},
    {"ok": False, "to": "9.9.9", "age": watch.GUARD_FRESH_S + 60},
])
def test_a_guard_record_that_is_no_new_rejection_is_none(rig, record):
    rig.sessions = [Session("a", report_env=True)]
    age = record.pop("age", 60)
    _guard(at=rig.now - age, **record)
    rig.scan()
    assert rig.calls == []


def test_a_tap_that_will_not_load_is_reported_once_per_version(rig):
    rig.sessions = [Session("a", report_env=True)]
    for _ in range(3):
        rig.note(Family.TAP_LOAD, "import_failed", None, {"tap_version": "0.10.99"}, once="tap_load:0.10.99")
        rig.send()
    assert len(rig.calls) == 1
    later = Rig()
    later.sessions = [Session("a", report_env=True)]
    later.note(Family.TAP_LOAD, "import_failed", None, {"tap_version": "0.10.99"}, once="tap_load:0.10.99")
    later.send()
    assert later.calls == []


# -- the rev 3 lease triggers (sessions the service does not supervise) --------


def _lease(state: Path, sid: str, **record) -> None:
    (state / "sessions").mkdir(parents=True, exist_ok=True)
    (state / "sessions" / f"{sid}.writer").write_text(json.dumps({"v": 1, "writer": "daemon", "pid": 1, **record}))


@pytest.mark.parametrize("reason", ["error", "gateway", "unauthorized"])
def test_a_lease_released_on_a_failure_two_scans_in_a_row_is_a_worker_report(rig, tmp_path, reason):
    state = tmp_path / "state" / "probe"
    rig.sessions = [Session(SID, mode="daemon", state_dir=str(state), report_env=True)]
    _lease(state, SID, expires_at=rig.now - 5, renewed_at=rig.now - 5, reason=reason)
    rig.scan()
    assert rig.calls == [], "one scan is not yet a report"
    rig.scan()
    assert rig.families() == [("worker", f"lease_{reason}", SID)]
    assert rig.calls[0]["facts"]["source"] == "lease"


@pytest.mark.parametrize("reason", ["stopped", "budget", "handover"])
def test_a_lease_released_on_purpose_is_none(rig, tmp_path, reason):
    state = tmp_path / "state" / "probe"
    rig.sessions = [Session(SID, mode="daemon", state_dir=str(state), report_env=True)]
    _lease(state, SID, expires_at=rig.now - 500, reason=reason)
    rig.scan()
    rig.scan()
    assert rig.calls == []


@pytest.mark.skipif(os.name == "nt", reason="the worker lock is an flock; Windows has no worker supervision")
def test_an_expired_lease_is_hung_while_the_worker_lock_is_held_else_not_running(rig, tmp_path):
    import fcntl

    state = tmp_path / "state" / "probe"
    rig.sessions = [Session(SID, mode="daemon", state_dir=str(state), report_env=True),
                    Session(SID2, mode="daemon", state_dir=str(state), report_env=True)]
    _lease(state, SID, expires_at=rig.now - watch.LEASE_GRACE_S - 30, reason=None)
    _lease(state, SID2, expires_at=rig.now - watch.LEASE_GRACE_S - 30, reason=None)
    (state / "daemon").mkdir(parents=True)
    lock = open(state / "daemon" / f"{workers.safe_sid(SID)}.lock", "w")  # noqa: SIM115
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    try:
        rig.scan()
        rig.scan()
    finally:
        lock.close()
    assert sorted(rig.families()) == [("worker", "hung", SID), ("worker", "not_running", SID2)]


def test_a_supervised_session_or_one_inline_is_left_to_the_supervisor(rig, tmp_path):
    state = tmp_path / "state" / "probe"
    rig.sessions = [Session(SID, mode="daemon", state_dir=str(state), report_env=True),
                    Session("s2", mode="inline", state_dir=str(state), report_env=True)]
    rig.supervised.add(SID)
    _lease(state, SID, expires_at=rig.now - 5, reason="error")
    _lease(state, "s2", expires_at=rig.now - 5, reason="error")
    rig.scan()
    rig.scan()
    assert rig.calls == []


def test_a_condition_that_changed_between_scans_is_not_yet_one(rig, tmp_path):
    state = tmp_path / "state" / "probe"
    rig.sessions = [Session(SID, mode="daemon", state_dir=str(state), report_env=True)]
    _lease(state, SID, expires_at=rig.now - 5, reason="gateway")
    rig.scan()
    _lease(state, SID, expires_at=rig.now + 200, renewed_at=rig.now, reason=None)  # it recovered
    rig.scan()
    _lease(state, SID, expires_at=rig.now - 5, reason="gateway")
    rig.scan()
    assert rig.calls == []


# -- facts ---------------------------------------------------------------------


def test_facts_are_bounded_to_the_contract_s_64_kib(rig):
    rig.sessions = [Session("a", report_env=True)]
    huge = {f"k{i}": "x" * 10_000 for i in range(100)}
    rig.note(Family.BACKGROUND, "early_exit", None, huge)
    rig.send()
    (call,) = rig.calls
    assert len(json.dumps(call["facts"])) <= watch.MAX_FACTS_BYTES
    assert all(len(v) <= watch.MAX_FACT_TEXT for v in call["facts"].values() if isinstance(v, str))


# -- the last run ----------------------------------------------------------------


@pytest.fixture
def boot(monkeypatch):
    value = {"id": "boot-a"}
    monkeypatch.setattr(watch, "boot_id", lambda: value["id"])
    return value


def _stop(pid: int, start: str) -> None:
    (paths.service_dir() / "last-stop.json").write_text(json.dumps(
        {"pid": pid, "start": start, "reason": "idle", "version": "1.0.0", "at": time.time()}))


def _run(pid: int, start: str, boot_value: str | None) -> None:
    (paths.service_dir() / watch.RUN_NAME).write_text(json.dumps(
        {"pid": pid, "start": start, "boot": boot_value, "version": "1.0.0", "at": time.time()}))


def test_a_first_start_is_no_crash_and_writes_its_own_record(boot):
    assert watch.last_run(None, "2.0.0") is None
    run = json.loads((paths.service_dir() / watch.RUN_NAME).read_text())
    assert run["pid"] == os.getpid() and run["boot"] == "boot-a" and run["version"] == "2.0.0"
    if os.name != "nt":  # Windows has no POSIX mode bits (every file reads 0o666): its folder is the user's own
        assert oct((paths.service_dir() / watch.RUN_NAME).stat().st_mode & 0o777) == "0o600"


@POSIX_LAST_RUN
def test_a_previous_service_with_no_stop_record_on_this_boot_crashed(boot):
    _run(4242, "777", "boot-a")
    _stop(4000, "1")  # an older one's stop
    found = watch.last_run((4242, "777"), "2.0.0")
    assert found["reason"] == "unclean_exit" and found["boot_known"] is True
    assert found["previous"]["version"] == "1.0.0" and found["last_stop"]["reason"] == "idle"


@POSIX_LAST_RUN
def test_a_previous_service_that_stopped_on_purpose_did_not(boot):
    _run(4242, "777", "boot-a")
    _stop(4242, "777")
    assert watch.last_run((4242, "777"), "2.0.0") is None


@POSIX_LAST_RUN
def test_the_same_pid_with_another_start_is_another_process(boot):
    _run(4242, "777", "boot-a")
    _stop(4242, "111")  # a container reuses its pids: an earlier run's stop
    assert watch.last_run((4242, "777"), "2.0.0")["reason"] == "unclean_exit"


@POSIX_LAST_RUN
def test_a_reboot_is_no_crash(boot):
    _run(4242, "777", "boot-a")
    boot["id"] = "boot-b"
    assert watch.last_run((4242, "777"), "2.0.0") is None


@POSIX_LAST_RUN
def test_an_unknown_boot_is_never_called_a_reboot(boot):
    _run(4242, "777", None)  # a service from before this record, or a platform that cannot say
    found = watch.last_run((4242, "777"), "2.0.0")
    assert found["reason"] == "unclean_exit" and found["boot_known"] is False


def test_a_recorded_crash_is_reported_with_its_traceback_once(boot, monkeypatch):
    from probe.service import procid

    # A context of its own: undoing the whole monkeypatch would undo the HOME
    # this file's fixture set, and the next write would land in the real one.
    with monkeypatch.context() as crashing:
        crashing.setattr(watch.os, "getpid", lambda: 4242)
        crashing.setattr(procid, "start_time", lambda pid: "777")
        watch.record_crash("RuntimeError('boom')", "Traceback (most recent call last):\n  ...\nRuntimeError: boom\n")
    assert str(paths.service_dir()).startswith(os.environ["HOME"])
    _run(4242, "777", "boot-a")
    _stop(4242, "777")  # a crash in the shutdown still left its stop record: the crash file wins
    found = watch.last_run((4242, "777"), "2.0.0")
    assert found["reason"] == "crashed" and "RuntimeError: boom" in found["traceback"]
    assert not (paths.service_dir() / watch.LAST_CRASH_NAME).exists()


def test_the_previous_holder_is_read_from_the_lock_file():
    paths.lock_path().write_text("4242 777\n")
    assert watch.previous_holder() == (4242, "777")
    paths.lock_path().write_text("")
    assert watch.previous_holder() is None


def test_boot_ids():
    assert watch.same_boot("a", "a") is True and watch.same_boot("a", "b") is False
    assert watch.same_boot(None, "a") is None
    assert watch.same_boot("boottime:1000", "boottime:1090") is True
    assert watch.same_boot("boottime:1000", "boottime:5000") is False
    if sys.platform.startswith("linux") or sys.platform == "darwin":
        assert watch.boot_id() == watch.boot_id() and watch.boot_id()


# -- each subsystem's hook ---------------------------------------------------------


class Notes:
    def __init__(self) -> None:
        self.calls: list = []

    def __call__(self, family, reason, sid=None, facts=None, **kwargs):
        self.calls.append({"family": family, "reason": reason, "sid": sid, "facts": facts, **kwargs})


def _supervisor(tmp_path, notes) -> workers.Supervisor:
    spec = workers.parse_spec({
        "sid": SID, "transcript": str(tmp_path / "t.jsonl"), "cwd": str(tmp_path), "source": "claude_code",
        "daemon_dir": str(tmp_path / "daemon"), "env": {"HOME": str(tmp_path), "PROBE_TELEMETRY": "off"},
        "switch": lambda: ("daemon", True),
    })
    return workers.Supervisor(spec, owner=None, incident=notes)


@POSIX_WORKERS
@pytest.mark.parametrize("code", [workers.EXIT_DO_NOT_RESPAWN, workers.EXIT_NO_COMMAND])
def test_a_worker_that_gives_up_is_a_worker_report_with_its_session_s_environment(tmp_path, code):
    notes = Notes()
    _supervisor(tmp_path, notes)._exited(code, 0.0)
    (call,) = notes.calls
    assert call["family"] == "worker" and call["reason"] == f"gave_up_exit_{code}" and call["sid"] == SID
    assert call["env"]["PROBE_TELEMETRY"] == "off", "its consent is its own"


@POSIX_WORKERS
def test_three_worker_crashes_in_a_row_are_a_report_and_respawning_is_unchanged(tmp_path):
    notes = Notes()
    sup = _supervisor(tmp_path, notes)
    for n in range(4):
        sup._exited(workers.EXIT_CRASHED, 0.0)
        assert sup.crashes == n + 1 and sup.gave_up_in is None
    assert [c["reason"] for c in notes.calls] == ["crash_loop", "crash_loop"]
    for code in (0, workers.EXIT_RESPAWN_LATER, workers.EXIT_RETRY_LIBS):
        sup._exited(code, 0.0)
    assert len(notes.calls) == 2


def test_a_queued_hook_event_that_did_not_finish_is_one_hook_event(monkeypatch, tmp_path):
    notes = Notes()
    queue = hookqueue.HookQueue(lambda m: None, folder=tmp_path, incident=notes)
    monkeypatch.setattr(hookqueue.hookhosts, "runnable", lambda request: None)
    monkeypatch.setattr(hookqueue, "declares_record_keeping", lambda root, lane: True)
    monkeypatch.setattr(hookqueue.hookhosts, "_via_host", lambda *a: None)
    answers = iter([
        {"exit_code": None, "timed_out": True, "via": "process"},
        {"exit_code": 2, "timed_out": False, "via": "process"},  # a Stop message delivered: no failure
        {"exit_code": 0, "timed_out": False, "via": "process"},
    ])
    monkeypatch.setattr(hookqueue.hookhosts, "_via_process", lambda *a: next(answers))
    item = {"id": "a" * 32, "plugin_root": str(tmp_path), "lane": "stop", "payload": "{}",
            "env": {"HOME": str(tmp_path), "PROBE_TELEMETRY": "off"}, "cwd": str(tmp_path), "at": time.time()}
    for _ in range(3):
        queue._run_one(item)
    assert [(c["family"], c["reason"]) for c in notes.calls] == [("hook", "did_not_finish")]
    assert notes.calls[0]["env"] == item["env"], "the event's own environment, for its consent (review #1)"


def test_a_background_child_that_fails_early_is_a_background_report():
    notes = Notes()
    host = background.BackgroundHost(log=lambda m: None, incident=notes)
    for code, key in ((1, "/outbox"), (0, "/outbox2")):
        child = background._Child(key, subprocess.Popen([sys.executable, "-c", f"import sys; sys.exit({code})"]))
        host._live[child.pid] = child
        host._wait(child)
    (call,) = notes.calls
    assert call["family"] == "background" and call["reason"] == "early_exit" and call["facts"]["code"] == 1


def test_a_background_child_s_report_carries_its_caller_s_opt_outs():
    """It ran with the SDK caller's environment: that one's opt-out counts (review #1)."""
    notes = Notes()
    host = background.BackgroundHost(log=lambda m: None, incident=notes)
    popen = subprocess.Popen([sys.executable, "-c", "import sys; sys.exit(1)"])
    child = background._Child("/outbox", popen, {"PROBE_TELEMETRY": "off", "PATH": "/usr/bin", "PROBE_X": "1"})
    host._live[child.pid] = child
    host._wait(child)
    (call,) = notes.calls
    assert call["env"] == {"PROBE_TELEMETRY": "off"}, "its consent variables, never the rest"


@pytest.fixture
def service(tmp_path):
    from probe.service.server import Service

    svc = Service(registry=Registry(tmp_path / "sessions.json"), discovery_s=0)
    notes = Notes()
    svc.watch.note = notes
    svc.watch_notes = notes  # never `svc.notes`: the service's team-note sync
    return svc


@pytest.mark.parametrize("answer, reason", [
    (None, "timed_out"),
    ({"exit_code": None, "timed_out": True, "via": "host"}, "timed_out"),
    ({"exit_code": None, "timed_out": False, "via": "host"}, "host_lost"),
    ({"exit_code": 2, "timed_out": False, "via": "host"}, None),
    ({"exit_code": 2, "timed_out": False, "via": "process"}, None),
    ({"exit_code": 1, "timed_out": False, "via": "process"}, None),
    ({"exit_code": None, "timed_out": False, "via": None}, None),
])
def test_hooks_run_counts_a_timeout_or_a_lost_host_never_an_exit_code(service, answer, reason):
    service._note_hook_run({"lane": "pre-tool", "timeout_s": 0.3}, answer)
    assert [c["reason"] for c in service.watch_notes.calls] == ([reason] if reason else [])


def test_the_loop_s_and_a_thread_s_unhandled_exceptions_are_logged_and_counted(service, monkeypatch):
    from probe.service import server

    lines: list = []
    monkeypatch.setattr(server, "log", lines.append)
    try:
        raise ValueError("boom")
    except ValueError as exc:
        error = exc
    service._loop_exception(None, {"message": "Exception in callback", "exception": error})
    args = types.SimpleNamespace(exc_type=KeyError, exc_value=KeyError("k"), exc_traceback=None,
                                 thread=threading.current_thread())
    server._thread_exception(service, args)
    server._thread_exception(service, types.SimpleNamespace(exc_type=SystemExit, exc_value=None, exc_traceback=None,
                                                             thread=None))
    assert [c["reason"] for c in service.watch_notes.calls] == ["loop_exception", "thread_exception"]
    assert "ValueError: boom" in service.watch_notes.calls[0]["facts"]["traceback"]
    assert lines[0] == "loop: Exception in callback" and any("ValueError: boom" in line for line in lines)


def test_a_handler_s_own_exception_is_logged_with_its_traceback_and_counted(service, monkeypatch):
    from probe.service import server

    lines: list = []
    monkeypatch.setattr(server, "log", lines.append)
    try:
        {}["missing"]
    except KeyError as exc:
        service._internal_error("status.get", exc)
    (call,) = service.watch_notes.calls
    assert call["family"] == "service_error" and call["reason"] == "request_error"
    assert lines[0] == "status.get failed: KeyError('missing')" and any("KeyError" in line for line in lines[1:])


@pytest.mark.parametrize("streak, reported", [(2, False), (3, True), (4, True)])
def test_three_failed_update_cycles_in_a_row_are_one_update_failed(service, streak, reported):
    service.updater.state["failed_in_a_row"] = streak
    service.updater.state["last_result"] = {"cycle_id": "c1", "ok": False, "steps": {}}
    service._note_update_cycles()
    assert bool(service.watch_notes.calls) is reported
    if reported:
        assert service.watch_notes.calls[0]["once"] == "update_failed:c1"


# -- report_env ------------------------------------------------------------------


def test_the_registry_keeps_report_env_across_a_restart(tmp_path):
    path = tmp_path / "sessions.json"
    reg = Registry(path)
    reg.register("a", "claude_code", "daemon", None, 1, None, True)
    reg.register("b", "pi", "inline", None, 1, None, False)
    reg.register("c", "codex", "inline", None, 1)
    reg.register("a", "claude_code", "daemon", None, 1, None, None)  # a register that says nothing keeps it
    again = Registry(path)
    again.load()
    assert {s.sid: s.report_env for s in again.sessions.values()} == {"a": True, "b": False, "c": None}


def test_session_register_takes_report_env_as_a_bool_only(service):
    for sid, value in (("a", True), ("b", "yes"), ("c", None)):
        params = {"sid": sid, "harness": "pi", "mode": "inline", "owner": None, "generation": 1}
        if value is not None:
            params[protocol.REPORT_ENV] = value
        service._register(None, params)
    assert {s: service.registry.sessions[s].report_env for s in "abc"} == {"a": True, "b": None, "c": None}


_GRID = [
    {}, {"PROBE_TELEMETRY": "off"}, {"PROBE_TELEMETRY": "OFF "}, {"PROBE_TELEMETRY": "on"},
    {"PROBE_DIAGNOSTICS": "disabled"}, {"PROBE_DIAGNOSTICS": "on", "PROBE_TELEMETRY": "0"},
    {"PROBE_BASE_URL": "https://api.research.prbe.ai"}, {"PROBE_BASE_URL": "https://prbe.ai/"},
    {"PROBE_BASE_URL": "http://api.research.prbe.ai"}, {"PROBE_BASE_URL": "https://evil-notprbe.ai"},
    {"PROBE_BASE_URL": "https://localhost:8443"}, {"PROBE_BASE_URL": ""},
]


@pytest.mark.parametrize("env", _GRID)
def test_the_registrants_consent_rule_is_report_policy_s(env):
    """The tap's copy (`protocol.report_consent`, synced into the tap) and the
    one the service and the report apply agree on every case."""
    assert protocol.report_consent(env) is report_policy.allowed(env)


# -- review fixes (PR #3327) ---------------------------------------------------------


def test_the_barrier_is_read_by_the_scan_never_on_the_thread_that_notes(rig):
    """Review #10: a note comes from a recorder's thread or the loop itself;
    the barrier's check reads files and may run `ps` (macOS)."""
    noted = threading.Thread(target=lambda: rig.note(Family.HOOK, "did_not_finish", None, {}))
    noted.start()
    noted.join()
    rig.note(Family.HOOK, "did_not_finish", None, {})
    assert rig.barrier_calls == []
    rig.scan()
    assert rig.barrier_calls and all(t is not threading.main_thread() for t in rig.barrier_calls)


def test_what_fails_once_the_scan_saw_the_barrier_is_not_counted(rig):
    rig.sessions = [Session(SID, report_env=True)]
    rig.barrier = True
    rig.scan()
    for _ in range(3):
        rig.note(Family.RECORDER, "failing", SID, {}, env={})
    rig.send()
    assert rig.calls == [] and rig.waiting() == 0


def test_a_lease_that_lapsed_while_the_machine_slept_is_no_hung_worker(rig, tmp_path):
    """Review #2: an hour asleep leaves every lease expired by the wall clock;
    the worker renews it once it runs again, which takes more than two scans."""
    state = tmp_path / "state" / "probe"
    rig.sessions = [Session(SID, mode="daemon", state_dir=str(state), report_env=True)]
    _lease(state, SID, expires_at=rig.now + 100, renewed_at=rig.now - 140, reason=None)
    rig.scan()
    rig.now += 3600  # asleep: the wall clock ran on, the monotonic one did not
    rig.mono += 15
    for _ in range(19):  # 285 s awake, a scan every 15 s
        rig.scan()
        rig.tick(15)
    assert rig.calls == []
    for _ in range(3):  # awake long enough for the worker to have renewed it: a lapse now is real
        rig.scan()
        rig.tick(15)
    assert rig.families() == [("worker", "not_running", SID)]


def test_on_windows_a_service_that_left_no_stop_record_is_no_crash(boot, monkeypatch):
    """Review #3: Windows has no SIGTERM handler, a logoff kills the service with
    no stop record, and the uptime-based boot id survives the logoff."""
    monkeypatch.setattr(watch, "WINDOWS", True, raising=False)
    _run(4242, "777", "boot-a")
    assert watch.last_run((4242, "777"), "2.0.0") is None
    with monkeypatch.context() as crashing:
        from probe.service import procid

        crashing.setattr(watch.os, "getpid", lambda: 4343)
        crashing.setattr(procid, "start_time", lambda pid: "888")
        watch.record_crash("RuntimeError('boom')", "RuntimeError: boom\n")
    _run(4343, "888", "boot-a")
    assert watch.last_run((4343, "888"), "2.0.0")["reason"] == "crashed", "a Python-level crash is still one"


@pytest.mark.parametrize("answer", [
    (0, {"sent": False, "id": None, "skipped": "offline", "path": None}),
    (0, {"sent": False, "id": None, "skipped": "server", "path": None}),
    (None, None),  # killed at 60 s
    (2, None),  # the read failed
])
def test_a_once_incident_is_kept_until_the_report_was_taken(rig, answer):
    """Review #4: only `sent`, `deduped` or `disabled:*` settle a once-ever
    report; anything else is tried again every 30 min, for 24 h."""
    rig.sessions = [Session("a", report_env=True)]
    rig.answer = answer
    rig.note(Family.TAP_LOAD, "import_failed", None, {"tap_version": "0.10.99"}, once="tap_load:0.10.99")
    rig.send()
    rig.tick(60)
    rig.send()
    assert len(rig.calls) == 1, "not again at once"
    restarted = Rig()  # meanwhile the next service still reports it
    restarted.sessions = [Session("a", report_env=True)]
    restarted.note(Family.TAP_LOAD, "import_failed", None, {"tap_version": "0.10.99"}, once="tap_load:0.10.99")
    restarted.send()
    assert len(restarted.calls) == 1
    rig.tick(30 * 60)
    rig.send()
    assert len(rig.calls) == 2, "tried again half an hour later"
    rig.answer = (0, {"sent": True, "id": "r-2", "skipped": None, "path": None})
    rig.tick(30 * 60)
    rig.send()
    rig.tick(30 * 60)
    rig.send()
    assert len(rig.calls) == 3, "settled"
    last = Rig()
    last.sessions = [Session("a", report_env=True)]
    last.note(Family.TAP_LOAD, "import_failed", None, {"tap_version": "0.10.99"}, once="tap_load:0.10.99")
    last.send()
    assert last.calls == []


def test_a_once_incident_is_tried_for_a_day_at_most(rig):
    rig.answer = (0, {"sent": False, "id": None, "skipped": "offline", "path": None})
    rig.note(Family.UPDATE_FAILED, "failed_in_a_row", None, {}, once="update_failed:c1")
    rig.send()
    rig.tick(25 * 3600)
    rig.send()
    rig.tick(30 * 60)
    rig.send()
    assert len(rig.calls) == 2 and rig.waiting() == 0


def test_the_keeper_s_report_child_opens_no_window_on_windows(monkeypatch):
    """Review #6: the keeper runs as pythonw (no console); a python.exe child
    without CREATE_NO_WINDOW opens a console window for up to 60 s."""
    from probe.service import children

    seen: dict = {}

    def run(argv, **kwargs):
        seen.update(argv=argv, **kwargs)
        return types.SimpleNamespace(returncode=0, stdout=b'{"sent": true, "id": "r-1"}')

    monkeypatch.setattr(watch.subprocess, "run", run)
    monkeypatch.setattr(children, "core_argv", lambda action: ["python.exe", "-I", "-m", "probe.core.run", action])
    monkeypatch.setattr(watch, "os", types.SimpleNamespace(name="nt", environ=os.environ, getpid=os.getpid))
    # Windows-only in `subprocess`: its value there, set here.
    monkeypatch.setattr(watch.subprocess, "CREATE_NO_WINDOW", 0x08000000, raising=False)
    assert watch.report_blocking({"family": "service_down"}) == (0, {"sent": True, "id": "r-1"})
    assert seen["creationflags"] == 0x08000000 and seen["timeout"] == watch.REPORT_TIMEOUT_S


def test_a_traceback_keeps_its_last_lines(rig):
    """Review #8: the exception itself is the traceback's LAST line."""
    text = "Traceback (most recent call last):\n" + "  frame\n" * 3000 + "ValueError: boom"
    facts = watch.bounded_facts({"traceback": text, "detail": "x" * 10_000})
    assert facts["traceback"].endswith("ValueError: boom") and len(facts["traceback"]) == watch.MAX_FACT_TEXT
    assert facts["detail"] == "x" * watch.MAX_FACT_TEXT


def test_old_counts_and_settled_reports_are_pruned_at_the_scan(rig):
    """Review #9: a key per session, forever, otherwise."""
    for n in range(50):
        rig.note(Family.RECORDER, "failing", f"s{n}", {}, env={})
    rig.watch._settled[("background", None)] = rig.now
    rig.tick(watch.DEDUPE_S + 1)
    rig.scan()
    assert rig.watch._seen == {} and rig.watch._settled == {}


def test_the_watch_shows_in_service_status(service, monkeypatch):
    """Review #11: what `probe doctor` and the debug log read."""
    status = service._status(None, {})
    assert set(status["watch"]) == {"enabled", "last_scan", "waiting", "reports"}
    assert status["watch"]["reports"] == []


def test_the_watch_s_status_names_its_last_five_reports(rig):
    rig.sessions = [Session("a", report_env=True)]
    for n in range(7):
        rig.note(Family.BACKGROUND, "early_exit", None, {"n": n})
        rig.send()
        rig.tick(watch.DEDUPE_S + 1)
    public = rig.watch.public()
    assert public["enabled"] is True and public["waiting"] == 0 and len(public["reports"]) == 5
    assert public["reports"][-1] == {"family": "background", "reason": "early_exit", "sid": None, "answer": "sent r-1",
                                     "at": rig.now - watch.DEDUPE_S - 1}


def test_a_hosted_recorder_whose_beat_stopped_while_its_agent_runs_is_stalled(rig):
    """Review #12 (plan rev 3, Codex #6): its thread is alive and not paused,
    its last beat more than 5 min old: nothing else would see it."""
    from probe.service import procid

    owner = {"pid": os.getpid(), "start_time": procid.start_time(os.getpid())}
    rig.sessions = [Session(SID)]
    rig.hosted[SID] = {"HOME": "/h"}
    rig.beats = [{"sid": SID, "beat_age_s": 200.0, "owner": owner}]
    rig.scan()
    rig.scan()
    assert rig.calls == []
    rig.beats = [{"sid": SID, "beat_age_s": 400.0, "owner": owner}]
    rig.scan()
    rig.scan()
    assert rig.families() == [("recorder", "stalled", SID)]
    assert rig.calls[0]["facts"]["beat_s"] == 400


def test_a_stalled_beat_of_an_agent_that_exited_is_none(rig):
    rig.sessions = [Session(SID)]
    rig.beats = [{"sid": SID, "beat_age_s": 400.0, "owner": {"pid": 999_999_999, "start_time": "1"}}]
    rig.scan()
    rig.scan()
    assert rig.calls == []


def test_a_tap_watch_session_whose_heartbeat_stopped_while_its_agent_runs_is_gone(rig):
    """A session the service does not record (its own `tap watch`): its link
    re-registers every 20 s; 90 s of silence while its agent runs is a recorder gone."""
    owner = {"pid": os.getpid(), "start_time": "x"}
    rig.sessions = [Session(SID, owner=owner, report_env=True, heartbeat_at=rig.now - 30),
                    Session("hosted", owner=owner, report_env=True, heartbeat_at=rig.now - 500),
                    Session("beats", owner=None, report_env=True, heartbeat_at=rig.now - 100)]
    rig.hosted["hosted"] = {"HOME": "/h"}  # recorded here: its beat says, not its link
    rig.scan()
    rig.scan()
    assert rig.calls == []
    rig.tick(100)
    rig.scan()
    rig.scan()
    assert rig.families() == [("recorder", "gone", SID)]


def test_a_hooks_run_event_s_report_carries_its_session_s_opt_outs(service):
    """pi sends the session's environment with each event (review #1)."""
    env = {"HOME": "/h", "PROBE_DIAGNOSTICS": "off"}
    service._note_hook_run({"lane": "pre-tool", "timeout_s": 0.3, "env": env}, None)
    (call,) = service.watch_notes.calls
    assert call["env"] == env


def test_a_repeating_exception_logs_its_traceback_three_times_in_15_minutes_then_a_line(service, monkeypatch):
    """Review #5: service.log rotates only at start; a handler failing on every
    request must not write ~20 lines each time."""
    from probe.service import server

    lines: list = []
    monkeypatch.setattr(server, "log", lines.append)

    def fail(method: str) -> None:
        try:
            {}["missing"]
        except KeyError as exc:
            service._internal_error(method, exc)

    for _ in range(5):
        fail("status.get")
    assert sum(line == "  Traceback (most recent call last):" for line in lines) == 3
    assert sum(line.startswith("status.get failed: KeyError") for line in lines) == 5, "one line each, always"
    fail("session.list")  # another site: its own three
    assert sum(line == "  Traceback (most recent call last):" for line in lines) == 4
    assert len(service.watch_notes.calls) == 6, "every one still counts for service_error"


def test_the_service_hands_the_watch_each_recorder_s_beat(service):
    """Review #12: the age of a hosted recorder's last beat, only for one inside
    `hosted.record` that beat in this run of it (a tap from before `beat`, or a
    thread not yet in its loop, says nothing)."""
    from probe.service.recorders import Recording

    done = threading.Event()
    thread = threading.Thread(target=done.wait)
    thread.start()
    try:
        controls = types.SimpleNamespace(stop=threading.Event(), pause=threading.Event(), beaten=time.monotonic() - 400)
        rec = Recording(SID, {"owner": {"pid": 1, "start_time": "s"}, "env": {}}, controls, thread)
        rec.in_record, rec.record_since = True, time.monotonic() - 500
        older = Recording("old", {"owner": None, "env": {}}, types.SimpleNamespace(
            stop=threading.Event(), pause=threading.Event()), thread)
        older.in_record, older.record_since = True, time.monotonic() - 500
        service.recorders.recordings = {SID: rec, "old": older}
        (beat,) = service._recorder_beats()
        assert beat["sid"] == SID and 399 < beat["beat_age_s"] < 410 and beat["owner"] == {"pid": 1, "start_time": "s"}
        rec.record_since = time.monotonic()  # a new run of it: the old beat says nothing
        assert service._recorder_beats() == []
        rec.record_since, rec.in_record = time.monotonic() - 500, False  # waiting to try again
        assert service._recorder_beats() == []
    finally:
        done.set()
        thread.join()


def test_the_service_hands_the_watch_the_receipts_of_live_sessions_asked_as_session_list_asks(service):
    """C1 reviews: the watch asked the shared receipt cache for its own
    sessions only, and each read replaced the cache, so `session.list` (the
    desktop app, `probe status`) lost every other session's receipts. It asks
    for every registered session, as `session.list` does, and keeps the live
    ones whose agent runs."""
    for sid in ("live", "dead-owner", "off"):
        service.registry.register(sid, "claude_code", "inline", None, 1)
    service.registry.sessions["dead-owner"].owner = {"pid": 1, "start_time": "s"}
    service.registry.sessions["dead-owner"].owner_live = False
    asked: list = []

    async def get(sids, roots, *, wait, claims=None):
        asked.append(sorted(sids))
        return {sid: {"pending_bytes": 1} for sid in sids}

    service.receipts.get = get
    found = asyncio.run(service._watch_receipts())
    assert asked == [sorted(service.registry.sessions)]
    assert set(found) == {"live", "off"}


def test_the_recorder_host_marks_each_run_of_hosted_record(monkeypatch):
    from probe.service import recorders

    seen: list = []
    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)

    class Hosted:
        ENDED, PAUSED, FAILED = "ended", "paused", "failed"

        @staticmethod
        def Controls():  # noqa: N802 -- the tap's class
            return types.SimpleNamespace(stop=threading.Event(), pause=threading.Event())

        @staticmethod
        def record(params, controls):
            (rec,) = host.recordings.values()
            seen.append((rec.in_record, rec.record_since <= time.monotonic()))
            return "ended", ""

    host.hosted = Hosted
    host._start({"sid": SID, "owner": None, "env": {}})
    host.recordings[SID].thread.join(5)
    assert seen == [(True, True)] and host.recordings[SID].in_record is False


# -- delta review of e7684f543 ---------------------------------------------------------


OFF = watch.Live("off", hosted_env={"PROBE_TELEMETRY": "off"})


class Loop:
    """A Watch on a running loop (its notes kick the loop, as in the service)."""

    def __init__(self, loop, *, login: dict | None = None, slow_login: float = 0.0, child_s: float = 0.0,
                 discovering: bool = False) -> None:
        self.voters: list = []
        self.sent: list = []
        self.lines: list = []
        self.discovering = discovering

        async def run_report(params):
            self.sent.append(params)
            await asyncio.sleep(child_s)
            return 0, {"sent": True, "id": "r-1"}

        async def login_env():
            await asyncio.sleep(slow_login)
            return login if login is not None else {}

        self.watch = Watch(log=self.lines.append, loop_getter=lambda: loop, voters=lambda: list(self.voters),
                           discovering=lambda: self.discovering, run_report=run_report, login=login_env,
                           scan_s=3600)

    def families(self) -> list:
        return [p["family"] for p in self.sent]


def test_an_incident_noted_while_a_report_runs_is_decided_by_the_sessions_of_its_moment():
    """Delta review #1 (leak2 s2): the slot was busy, so the incident waited to
    be looked at, and the opted-out session had ended by then."""
    async def go():
        w = Loop(asyncio.get_running_loop(), child_s=1.0)
        w.watch.note(Family.SERVICE_CRASH, "crashed")  # no session: the login shell allows; its child runs 1 s
        await asyncio.sleep(0.2)
        w.voters.append(OFF)  # an opted-out session starts...
        for _ in range(3):
            w.watch.note(Family.HOOK_HOST, "timed_out")  # ...fails meanwhile...
        await asyncio.sleep(0.2)
        w.voters.clear()  # ...and ends before the child is done
        await asyncio.sleep(1.5)
        return w

    w = asyncio.run(go())
    assert w.families() == ["service_crash"]
    assert any("hook_host (timed_out) not reported: session off does not allow reports" in line for line in w.lines)


def test_an_incident_noted_while_the_login_shell_is_asked_is_decided_by_the_sessions_of_its_moment():
    """Delta review #1 (leak2 s3): `_send_next` awaited a slow login shell."""
    async def go():
        w = Loop(asyncio.get_running_loop(), login={"PROBE_TELEMETRY": "off"}, slow_login=1.0)
        w.watch.note(Family.SERVICE_CRASH, "crashed")  # asks the (slow) login shell: declined
        await asyncio.sleep(0.2)
        w.voters.append(OFF)
        for _ in range(3):
            w.watch.note(Family.HOOK_HOST, "timed_out")
        await asyncio.sleep(0.2)
        w.voters.clear()
        await asyncio.sleep(1.2)
        w.watch._login_cache = (w.watch.monotonic(), {})  # the login shell itself allows now
        await w.watch._send_next()
        await asyncio.sleep(0.3)
        return w

    assert asyncio.run(go()).sent == []


def test_an_incident_noted_while_discovering_asks_the_sessions_of_its_moment_too():
    """Leak2 s6: an opted-out session restored at start that ends before the
    discovery window is over still says no."""
    async def go():
        w = Loop(asyncio.get_running_loop(), discovering=True)
        w.voters.append(OFF)
        for _ in range(3):
            w.watch.note(Family.HOOK_HOST, "timed_out")
        await asyncio.sleep(0.2)
        w.voters.clear()
        w.discovering = False
        await w.watch._send_next()
        await asyncio.sleep(0.3)
        return w

    assert asyncio.run(go()).sent == []


def test_a_session_still_coming_back_at_its_moment_is_asked_once_it_is_back():
    """...while one restored before its recorder resumed (consent not yet
    known) is decided by what it says once the discovery window is over."""
    async def go():
        w = Loop(asyncio.get_running_loop(), discovering=True)
        w.voters.append(watch.Live("hosted"))  # restored; its recorder not resumed yet
        for _ in range(3):
            w.watch.note(Family.HOOK_HOST, "timed_out")
        await asyncio.sleep(0.2)
        w.voters[:] = [watch.Live("hosted", hosted_env={"HOME": "/h"})]
        w.discovering = False
        await w.watch._send_next()
        await asyncio.sleep(0.3)
        return w

    assert asyncio.run(go()).families() == ["hook_host"]


def test_the_sessions_a_report_asks_are_a_required_argument():
    """Delta review #1: a default of "no sessions" would fail open."""
    with pytest.raises(TypeError):
        Watch(log=print, loop_getter=lambda: None)


def test_a_retry_whose_first_try_failed_is_not_settled_by_deduped(rig):
    """Delta review #2: the first child claimed the dedupe window and failed;
    a `deduped` answer to the retry is that claim, not a report."""
    rig.answer = (0, {"sent": False, "id": None, "skipped": "offline", "path": None})
    rig.note(Family.TAP_LOAD, "import_failed", None, {}, once="tap_load:0.10.99")
    rig.send()
    rig.answer = (0, {"sent": False, "id": None, "skipped": "deduped", "path": None})
    rig.tick(30 * 60)
    rig.send()
    rig.answer = (0, {"sent": True, "id": "r-2", "skipped": None, "path": None})
    rig.tick(30 * 60)
    rig.send()
    assert len(rig.calls) == 3, "tried again until it was sent"
    later = Rig()
    later.note(Family.TAP_LOAD, "import_failed", None, {}, once="tap_load:0.10.99")
    later.send()
    assert later.calls == []


def test_a_first_try_answered_deduped_is_settled(rig):
    """Another reporter (the keeper, the last service) sent it in this window."""
    rig.answer = (0, {"sent": False, "id": None, "skipped": "deduped", "path": None})
    rig.note(Family.TAP_LOAD, "import_failed", None, {}, once="tap_load:0.10.98")
    rig.send()
    rig.tick(30 * 60)
    rig.send()
    assert len(rig.calls) == 1 and rig.waiting() == 0


def test_a_retry_asks_the_sessions_of_its_own_moment_too(rig):
    """Delta review #4: consent 24 h old is not consent for now."""
    rig.sessions = [Session("a", report_env=True)]
    rig.answer = (0, {"sent": False, "id": None, "skipped": "offline", "path": None})
    rig.note(Family.TAP_LOAD, "import_failed", None, {}, once="tap_load:0.10.99")
    rig.send()
    rig.sessions.append(Session("b", report_env=False))  # a session that says no runs now
    rig.tick(30 * 60)
    rig.send()
    assert len(rig.calls) == 1 and rig.waiting() == 0
    assert any("not reported: session b does not allow reports" in line for line in rig.lines)


def test_start_reads_the_barrier_and_the_once_record_before_any_note(home):
    """Delta review #5: the first note after start must see a barrier that is
    up, and must not read watch.json under the lock on the loop."""
    (paths.service_dir() / watch.STATE_NAME).write_text(json.dumps({"v": 1, "once": ["tap_load:0.10.99"]}))

    async def go():
        loop = asyncio.get_running_loop()
        sent: list = []

        async def run_report(params):
            sent.append(params)
            return 0, {"sent": True, "id": "r-1"}

        w = Watch(log=print, loop_getter=lambda: loop, voters=list, barrier_up=lambda: True,
                  run_report=run_report, scan_s=3600)
        w.start()
        assert w._once == {"tap_load:0.10.99"}, "read at start"
        for _ in range(3):
            w.note(Family.RECORDER, "failing", SID, {}, env={})
        await asyncio.sleep(0.2)
        w.close()
        return sent, w

    sent, w = asyncio.run(go())
    assert sent == [] and w._seen == {}, "the barrier was up: nothing counted"


def test_stalled_and_gone_are_counted_apart_from_failing(rig):
    """Delta review #6: two earlier `failing` events are not a `stalled` report's."""
    from probe.service import procid

    owner = {"pid": os.getpid(), "start_time": procid.start_time(os.getpid())}
    rig.sessions = [Session(SID)]
    rig.hosted[SID] = {"HOME": "/h"}
    for _ in range(2):
        rig.note(Family.RECORDER, "failing", SID, {"detail": "boom"}, env={})
    rig.beats = [{"sid": SID, "beat_age_s": 400.0, "owner": owner}]
    rig.scan()
    rig.scan()
    (call,) = rig.calls
    assert call["reason"] == "stalled" and call["facts"] == {"beat_s": 400}


def test_a_session_id_the_report_read_would_refuse_goes_in_the_facts(rig):
    """The `report` read takes a UUID or nothing for `sid` (its parser refuses
    the rest, the whole report with it): any other id rides in the facts."""
    rig.hosted["s-1"] = {"HOME": "/h"}
    rig.sessions = [Session("s-1")]
    rig.note(Family.WORKER, "gave_up_exit_3", "s-1", {"last_exit": 3}, env={})
    rig.note(Family.WORKER, "gave_up_exit_3", SID, {"last_exit": 3}, env={})
    rig.send()
    rig.send()
    by_reason = {c["sid"]: c for c in rig.calls}
    assert set(by_reason) == {None, SID}
    assert by_reason[None]["facts"] == {"last_exit": 3, "session": "s-1"}
    assert by_reason[SID]["facts"] == {"last_exit": 3}


def test_no_window_flag_is_spelled_out_in_the_service_s_sources():
    """Delta review #7: `subprocess.CREATE_NO_WINDOW`, never a bare literal."""
    import re

    folder = Path(watch.__file__).parent
    found = [p.name for p in folder.glob("*.py") if re.search(r"0x0*8000000\b", p.read_text())]
    assert found == []


# -- the slower checks: the outbox, receipts, keys (silent-failure guards) -------


def _iso_ago(hours: float) -> str:
    from datetime import datetime, timedelta, timezone

    return (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()


def _queue(root: Path, **status) -> None:
    """A queue folder whose `status.json` says `status` (the drain's own record)."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "status.json").write_text(json.dumps(status))


def test_an_outbox_refused_for_an_hour_is_stuck_and_names_no_credential(tmp_path):
    """Bucket, 2026-10-22: writes queued under a credential the API refused
    wait for it forever. The report carries counts, never the fingerprint."""
    root = tmp_path / "outbox"
    _queue(root, pending=9061, held=9061, oldest_pending=_iso_ago(26), failed=0,
           refused_fingerprints={"738f7f8ed3fe16d6": _iso_ago(0.1)})
    reason, facts = watch.outbox_condition(time.time(), root)
    assert reason == "credential_refused"
    assert facts == {"pending": 9061, "oldest_pending_h": 26.0, "held": 9061, "refused_credentials": 1,
                     "dead_lettered": 0}
    assert "738f" not in json.dumps(facts)


@pytest.mark.parametrize(("status", "hours", "why"), [
    ({"pending": 5, "held": 5, "refused_fingerprints": {"f": "x"}}, 0.9, "not an hour old"),
    ({"pending": 0, "held": 0, "refused_fingerprints": {"f": "x"}}, 5, "nothing waits"),
    ({"pending": 5, "held": 5, "refused_fingerprints": {"f": "x"}, "paused": True}, 5, "someone paused it"),
    ({"pending": 5}, 5, "busy, not refused or held"),
    ({"pending": 5, "held": 0, "refused_fingerprints": {"f": "x"}}, 5, "a refusal remembered, nothing held"),
    ({"pending": 5, "held": 1, "close_held": 1}, 5, "a run close waiting on its data"),
])
def test_an_outbox_that_is_not_stuck_says_nothing(tmp_path, status, hours, why):
    _queue(tmp_path / "outbox", oldest_pending=_iso_ago(hours), **status)
    assert watch.outbox_condition(time.time(), tmp_path / "outbox") is None, why


def test_writes_held_in_a_credential_queue_under_an_empty_root_are_stuck(tmp_path):
    """Codex O3: `read_status` folded pending and refusals from the credential
    queues but not `held`, so a held queue under an empty root said nothing."""
    from probe.sdk.journal import CREDENTIAL_NAMESPACE

    root = tmp_path / "outbox"
    _queue(root, pending=0)
    _queue(root / CREDENTIAL_NAMESPACE / "0123456789abcdef", pending=40, held=40, held_at=_iso_ago(0),
           oldest_pending=_iso_ago(3))
    reason, facts = watch.outbox_condition(time.time(), root)
    assert (reason, facts["held"], facts["pending"]) == ("held", 40, 40)


def test_refused_writes_in_a_credential_queue_s_delivery_namespace_are_stuck(tmp_path):
    """Codex C1 #3: the delivery fold kept pending but dropped `held`, the
    refusal and the oldest write, so forty refused writes there said nothing."""
    from probe.sdk.journal import CREDENTIAL_NAMESPACE, DELIVERY_NAMESPACE

    root = tmp_path / "outbox"
    queue = root / CREDENTIAL_NAMESPACE / "0123456789abcdef"
    _queue(queue, pending=0)
    _queue(queue / DELIVERY_NAMESPACE, pending=40, held=40, oldest_pending=_iso_ago(3),
           refused_fingerprints={"0123456789abcdef": _iso_ago(0.1)})
    reason, facts = watch.outbox_condition(time.time(), root)
    assert (reason, facts["held"], facts["pending"], facts["oldest_pending_h"]) == ("credential_refused", 40, 40, 3.0)


def test_one_queue_s_old_backlog_never_makes_another_s_fresh_hold_stuck(tmp_path):
    """Codex C1 #6: the oldest write anywhere was paired with a hold anywhere,
    so a healthy queue draining a two-hour backlog plus a hold taken a
    minute ago in another queue read as an hour-old stall."""
    from probe.sdk.journal import CREDENTIAL_NAMESPACE

    root = tmp_path / "outbox"
    _queue(root, pending=500, oldest_pending=_iso_ago(2))
    _queue(root / CREDENTIAL_NAMESPACE / "0123456789abcdef", pending=3, held=3, oldest_pending=_iso_ago(0.02))
    assert watch.outbox_condition(time.time(), root) is None
    _queue(root / CREDENTIAL_NAMESPACE / "fedcba9876543210", pending=7, held=7, oldest_pending=_iso_ago(4))
    reason, facts = watch.outbox_condition(time.time(), root)
    assert (reason, facts["oldest_pending_h"]) == ("held", 4.0)


def test_a_session_waiting_an_hour_past_its_last_receipt_is_stalled():
    now = 1_000_000.0
    receipts = {
        "stalled": {"received_at": now - 2 * 3600, "pending_bytes": 1200, "pending_lines": 3},
        "batch": {"received_at": now - 2 * 3600, "pending_bytes": 0, "pending_batch": True},
        "uncounted": {"received_at": now - 2 * 3600, "pending_bytes": 1200, "pending_lines": None},
        "recent": {"received_at": now - 1800, "pending_bytes": 1200},
        "caught_up": {"received_at": now - 5 * 3600, "pending_bytes": 0},
        "partial_tail": {"received_at": now - 5 * 3600, "pending_bytes": 40, "pending_lines": 0},
        "finalized": {"received_at": now - 5 * 3600, "pending_bytes": 10, "finalized": True},
        "unread": None,
    }
    found = watch.capture_conditions(receipts, now)
    assert set(found) == {"stalled", "batch", "uncounted"}
    assert found["stalled"]["received_h"] == 2.0 and found["stalled"]["pending_bytes"] == 1200


def test_a_session_none_of_whose_batches_landed_is_stalled_once_its_cursor_sat_an_hour():
    """Codex C1 #4: a session whose FIRST batch keeps failing has no
    `received_at`, and was never reported. Its cursor not moving is."""
    still: dict = {}
    never = {"received_at": None, "received_bytes": 0, "pending_bytes": 900, "pending_lines": 4, "retrying": True}
    now = 1_000_000.0
    assert watch.capture_conditions({"s": never}, now, still) == {}
    assert watch.capture_conditions({"s": never}, now + 3599, still) == {}
    found = watch.capture_conditions({"s": never}, now + 3600, still)
    assert found["s"]["receipt"] == "unmoved" and found["s"]["received_h"] == 1.0
    moved = {**never, "received_bytes": 300}
    assert watch.capture_conditions({"s": moved}, now + 3700, still) == {}, "its cursor moved: an hour from now"
    assert watch.capture_conditions({}, now + 9000, still) == {} and still == {}, "a session gone is forgotten"


def _slow_rig(**over) -> Rig:
    calls = {"outbox": 0, "credentials": 0}
    asked: list = []

    def outbox(now):
        calls["outbox"] += 1
        return rig_state["outbox"]

    def credentials(*, due=lambda ident: True):
        calls["credentials"] += 1
        found = {kind: answer for kind, answer in rig_state["credentials"].items() if due(answer[0])}
        asked.append(sorted(found))
        return found

    async def receipts():
        return rig_state["receipts"]

    rig_state = {"outbox": None, "credentials": {}, "receipts": {}}
    rig = Rig(**{"outbox": outbox, "credentials": credentials, "receipts": receipts, **over})
    rig.state, rig.slow_calls, rig.asked = rig_state, calls, asked
    rig.sessions = [Session(SID, report_env=True)]
    return rig


def _awake(rig: Rig, seconds: float) -> None:
    """`seconds` of an awake service: a scan every 15 s (a longer gap reads as a sleep)."""
    for _ in range(int(seconds // 15)):
        rig.tick(15)
        rig.scan()


def test_a_stuck_outbox_on_two_checks_in_a_row_is_one_report_and_the_first_scan_checks():
    rig = _slow_rig()
    rig.state["outbox"] = ("credential_refused", {"pending": 5})
    rig.scan()
    assert rig.slow_calls["outbox"] == 1, "the first scan checks at once (a report 5 min in, not 10)"
    assert rig.calls == [], "one check is not yet one"
    _awake(rig, 30)
    assert rig.slow_calls["outbox"] == 1, "not again before SLOW_CHECK_S"
    _awake(rig, watch.SLOW_CHECK_S)
    assert rig.families() == [(Family.OUTBOX_STUCK, "credential_refused", None)]
    assert rig.calls[0]["facts"] == {"pending": 5}


def test_sessions_whose_capture_stalled_on_two_checks_are_one_report_for_the_machine():
    """An hour-long stall of the server's ingestion stalls every session at
    once: one report per machine, naming its sessions, not one per session
    (C1 adversarial #10: up to 16 reports a machine, retried for a day)."""
    rig = _slow_rig()
    rig.state["receipts"] = {f"s-{n}": {"received_at": rig.now - (2 + n) * 3600, "pending_bytes": 9}
                             for n in range(watch.CAPTURE_MAX_SESSIONS + 2)}
    rig.scan()
    _awake(rig, watch.SLOW_CHECK_S)
    assert rig.families() == [(Family.CAPTURE_STALLED, "waiting", None)]
    facts = rig.calls[0]["facts"]
    assert facts["count"] == watch.CAPTURE_MAX_SESSIONS + 2
    assert len(facts["sessions"]) == watch.CAPTURE_MAX_SESSIONS and "s-9" in facts["sessions"], "the oldest first"


def test_a_stall_that_cleared_while_its_report_waits_for_a_retry_is_dropped():
    """C1 adversarial #11: a stall noted during an outage was sent up to a
    day after it cleared."""
    rig = _slow_rig()
    rig.state["outbox"] = ("held", {"pending": 5})
    rig.answer = (0, {"sent": False, "id": None, "skipped": "offline", "path": None})
    rig.scan()
    _awake(rig, watch.SLOW_CHECK_S)
    assert len(rig.calls) == 1 and rig.waiting() == 1, "offline: waiting for its retry"
    rig.state["outbox"] = None
    _awake(rig, watch.SLOW_CHECK_S)
    assert rig.waiting() == 0 and any("cleared before it was reported" in line for line in rig.lines)
    _awake(rig, watch.RETRY_S)
    assert len(rig.calls) == 1


def test_a_read_that_did_not_answer_drops_no_waiting_report(monkeypatch):
    """C1 fix review: a timed-out outbox read (or a failed receipt read) read
    as "cleared" and dropped the report's retry, while the 6 h hold kept a new
    one from being noted."""
    monkeypatch.setattr(watch, "OUTBOX_TIMEOUT_S", 0.2)
    release = threading.Event()
    state = {"hang": False}

    def outbox(now):
        if state["hang"]:
            release.wait(10)
        return ("held", {"pending": 5})

    async def receipts():
        if state["hang"]:
            raise OSError("receipts unreadable")
        return {SID: {"received_at": rig.now - 2 * 3600, "pending_bytes": 9}}

    rig = _slow_rig(outbox=outbox, receipts=receipts)
    rig.answer = (0, {"sent": False, "id": None, "skipped": "offline", "path": None})
    try:
        rig.scan()
        _awake(rig, watch.SLOW_CHECK_S)
        assert rig.waiting() == 2, "both waiting for their retry"
        state["hang"] = True
        _awake(rig, watch.SLOW_CHECK_S)
        assert rig.waiting() == 2 and not any("cleared" in line for line in rig.lines)
    finally:
        release.set()


def test_a_key_check_stuck_past_its_deadline_holds_off_the_next(monkeypatch):
    """C1 fix review: the given-up check's thread kept running, and another
    started every 5 min: three timeouts, three live threads."""
    monkeypatch.setattr(watch, "CREDENTIAL_DEADLINE_S", 0.2)
    monkeypatch.setattr(watch, "CREDENTIAL_TIMEOUT_S", 0.1)
    release = threading.Event()
    asked: list = []

    def stuck(**_):
        asked.append(1)
        release.wait(10)
        return {}

    rig = _slow_rig(credentials=stuck)
    try:
        rig.scan()
        _awake(rig, 3 * watch.SLOW_CHECK_S)
        assert len(asked) == 1, "none while the last one's thread still runs"
        release.set()
        deadline = time.monotonic() + 5
        while rig.watch._credentials_busy and time.monotonic() < deadline:
            time.sleep(0.01)
        _awake(rig, watch.SLOW_CHECK_S)
        assert len(asked) == 1, "and an hour's wait after one was given up on"
        _awake(rig, watch.CREDENTIAL_RETRY_S)
        assert len(asked) >= 2, "then asked again (this fake holds no key: every check after)"
    finally:
        release.set()


def test_an_outbox_read_stuck_on_a_hung_mount_never_holds_the_scan(monkeypatch):
    """C1 security #8 / adversarial #18: the outbox read had no bound, and a
    hung home mount held every scan and the service's exit."""
    monkeypatch.setattr(watch, "OUTBOX_TIMEOUT_S", 0.2)
    release = threading.Event()
    reads: list = []

    def hung(now):
        reads.append(now)
        release.wait(10)

    rig = _slow_rig(outbox=hung)
    try:
        started = time.monotonic()
        rig.scan()
        assert time.monotonic() - started < 3
        assert any("reading the outbox did not finish in time" in line for line in rig.lines)
        _awake(rig, watch.SLOW_CHECK_S)
        assert len(reads) == 1, "none started while the last one is still stuck"
    finally:
        release.set()


def test_a_refused_key_is_reported_by_kind_once_and_each_answered_key_asked_again_a_day_later():
    rig = _slow_rig()
    rig.state["credentials"] = {"login": ("id-l", "ok"), "daemon_key": ("id-d", "refused"),
                                "mcp_key": ("id-m", "unknown")}
    rig.scan()
    assert rig.families() == [(Family.CREDENTIAL_REFUSED, "refused", None)]
    assert rig.calls[0]["facts"] == {"refused": ["daemon_key"], "unknown": ["mcp_key"]}
    _awake(rig, watch.CREDENTIAL_RETRY_S)
    assert [a for a in rig.asked if a] == [["daemon_key", "login", "mcp_key"], ["mcp_key"]], \
        "an answered key once a day (Codex C1 #5); one with no answer an hour later, not every 5 min"
    restarted = _slow_rig()  # a new service reads when each was answered (watch.json)
    restarted.state["credentials"] = rig.state["credentials"]
    restarted.now = rig.now
    restarted.scan()
    assert restarted.asked == [["mcp_key"]]
    rig.tick(watch.CREDENTIAL_CHECK_S - 2 * watch.SLOW_CHECK_S)
    rig.mono -= watch.CREDENTIAL_CHECK_S - 2 * watch.SLOW_CHECK_S  # a day later: the laptop slept, so the
    # check first waits out the wake grace, then asks
    _awake(rig, 2 * watch.SLOW_CHECK_S)
    assert rig.asked[-1] == ["daemon_key", "login", "mcp_key"]
    assert len(rig.calls) == 1, "the same refused key is reported once, not every day (C1 adversarial #14)"


def test_no_key_is_asked_when_its_report_could_not_be_sent():
    """C1 security #3: a person who turned reports off still got a daily
    request whose only use is a report."""
    rig = _slow_rig()
    rig.sessions = [Session(SID, report_env=False)]
    rig.state["credentials"] = {"login": ("id-l", "refused")}
    rig.scan()
    assert rig.slow_calls["credentials"] == 0 and rig.calls == []


def test_a_replaced_key_is_asked_at_the_next_check_whatever_the_others_answered():
    """Codex C1 #5: one machine-wide stamp let a key answered this morning
    hold back a login replaced at noon for a day."""
    rig = _slow_rig()
    rig.state["credentials"] = {"login": ("id-l", "ok"), "daemon_key": ("id-d", "ok")}
    rig.scan()
    rig.state["credentials"] = {"login": ("id-l2", "refused"), "daemon_key": ("id-d", "ok")}
    _awake(rig, watch.SLOW_CHECK_S)
    assert rig.asked[-1] == ["login"]
    assert rig.families() == [(Family.CREDENTIAL_REFUSED, "refused", None)]


def test_keys_that_could_not_be_asked_are_asked_again_an_hour_later():
    """C1 security #5: an unanswered key was asked every 5 min, forever, on a
    machine that can never get an answer (a proxy, a firewall)."""
    rig = _slow_rig()
    rig.state["credentials"] = {"login": ("id-l", "unknown")}  # offline
    rig.scan()
    _awake(rig, watch.CREDENTIAL_RETRY_S - watch.SLOW_CHECK_S)
    assert [a for a in rig.asked if a] == [["login"]]
    _awake(rig, 2 * watch.SLOW_CHECK_S)
    assert [a for a in rig.asked if a] == [["login"], ["login"]] and rig.calls == []


def test_a_slow_key_check_never_holds_the_scan(monkeypatch):
    """Codex C1 #2: the check was awaited inside the scan, and a server
    trickling its answer past the socket timeout held every later scan and
    report retry. It runs beside the scan, and is given up past its deadline."""
    monkeypatch.setattr(watch, "CREDENTIAL_DEADLINE_S", 0.2)
    monkeypatch.setattr(watch, "CREDENTIAL_TIMEOUT_S", 0.1)
    release = threading.Event()

    def stuck(**_):
        release.wait(10)
        return {}

    rig = _slow_rig(credentials=stuck)

    async def scan() -> None:
        await rig.watch._scan()
        task = rig.watch._credential_task
        assert task is not None and not task.done(), "the scan returned with the check still running"
        await asyncio.wait_for(task, 5)

    try:
        started = time.monotonic()
        asyncio.run(scan())
        assert time.monotonic() - started < 3
        assert any("did not finish in time" in line for line in rig.lines)
    finally:
        release.set()
        if rig.watch._timer is not None:
            rig.watch._timer.cancel()


@pytest.mark.parametrize("skipped", ["unauthorized", "too_large"])
def test_a_report_whose_claim_the_child_kept_is_not_tried_again(rig, skipped):
    """C1 reviews: refused for its credentials or too large, the child kept
    its claim of the window, so each retry only answered `deduped`: 48
    report processes a day per incident."""
    rig.sessions = [Session("a", report_env=True)]
    rig.answer = (0, {"sent": False, "id": None, "skipped": skipped, "path": None})
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    for _ in range(4):
        rig.tick(watch.RETRY_S)
        rig.send()
    assert len(rig.calls) == 1 and rig.waiting() == 0


def test_a_rate_limited_report_waits_longer_before_its_retry(rig):
    rig.sessions = [Session("a", report_env=True)]
    rig.answer = (0, {"sent": False, "id": None, "skipped": "rate_limited", "path": None})
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    rig.tick(watch.RETRY_S)
    rig.send()
    assert len(rig.calls) == 1, "not after RETRY_S"
    rig.tick(watch.RATE_LIMITED_RETRY_S - watch.RETRY_S)
    rig.send()
    assert len(rig.calls) == 2


def test_a_failed_send_of_a_recurring_family_is_tried_again_not_held_back_six_hours(rig):
    """Codex O4: the incident was settled before its child ran, and only
    once-ever incidents were retried, so a diagnostics 503 silenced a
    recurring family for DEDUPE_S. A taken report still holds it back."""
    rig.sessions = [Session("a", report_env=True)]
    rig.answer = (0, {"sent": False, "id": None, "skipped": "server", "path": None})
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    rig.tick(watch.RETRY_S)
    rig.answer = (0, {"sent": True, "id": "r-2", "skipped": None, "path": None})
    rig.send()
    assert len(rig.calls) == 2, "tried again RETRY_S later"
    rig.tick(60)
    rig.note(Family.BACKGROUND, "early_exit", None, {})
    rig.send()
    assert len(rig.calls) == 2, "a taken report holds its family back for DEDUPE_S"


class _Me:
    """A local `/v1/me` answering each bearer as told."""

    def __init__(self, answers: dict) -> None:
        import http.server

        test = self
        self.seen: list = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_args) -> None:
                pass

            def do_GET(self) -> None:  # noqa: N802 -- the stdlib's name
                token = self.headers.get("Authorization", "").split()[-1]
                test.seen.append((self.path, token))
                self.send_response(answers.get(token, 500))
                self.end_headers()
                self.wfile.write(b"{}")

            def do_POST(self) -> None:  # noqa: N802 -- `/v1/device-state`: the key in the body, no bearer
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                ((source, token),) = body["capture_tokens"].items()
                test.seen.append((self.path, token, self.headers.get("Authorization")))
                code = answers.get(token, 500)
                verdict = {200: "ok", 401: "rejected"}.get(code, "unknown")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"account_status": "signed_out", "capture": {source: verdict}}).encode())

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


def _verdicts(found: dict) -> dict:
    return {kind: verdict for kind, (_, verdict) in found.items()}


def test_each_key_is_asked_v1_me_once_401_refused_200_ok_else_unknown(home):
    from probe.sdk.config import save_context

    me = _Me({"login-1": 200, "daemon-1": 401, "mcp-1": 503})
    try:
        save_context({"base_url": me.url, "token": "login-1", "companion_token": "daemon-1",
                      "mcp_token": "mcp-1"})
        found = watch.credential_verdicts()
        assert _verdicts(found) == {"login": "ok", "daemon_key": "refused", "mcp_key": "unknown"}
        # The daemon key through the door that records no use of it (C1 security #2).
        assert me.seen == [("/v1/me", "login-1"), ("/v1/device-state", "daemon-1", None), ("/v1/me", "mcp-1")]
        ids = {ident for ident, _ in found.values()}
        assert len(ids) == 3 and not any(t in i for i in ids for t in ("login-1", "daemon-1", "mcp-1"))
        assert watch.credential_verdicts(due=lambda ident: ident != found["login"][0]).keys() == {
            "daemon_key", "mcp_key"}, "a key not due is not asked"
    finally:
        me.close()


def test_a_403_is_no_refusal_and_plain_http_elsewhere_carries_no_key(home):
    """C1 adversarial #14: a proxy's 403 read as a dead key. C1 security #4:
    a key never crosses a network in the clear for a check."""
    from probe.sdk.config import save_context

    me = _Me({"login-1": 403})
    try:
        save_context({"base_url": me.url, "token": "login-1"})
        assert _verdicts(watch.credential_verdicts()) == {"login": "unknown"}
        save_context({"base_url": "http://api.example.test", "token": "login-1"})
        assert watch.credential_verdicts() == {}
    finally:
        me.close()


def test_a_redirect_is_never_followed_with_the_key(home):
    """Codex C1 #1: urllib followed a redirect with the `Authorization`
    header, to another host or to plain HTTP."""
    import http.server

    from probe.sdk.config import save_context

    elsewhere = _Me({"login-1": 200})

    class Redirect(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_args) -> None:
            pass

        def do_GET(self) -> None:  # noqa: N802 -- the stdlib's name
            self.send_response(302)
            self.send_header("Location", elsewhere.url + "/v1/me")
            self.end_headers()

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Redirect)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        save_context({"base_url": f"http://127.0.0.1:{server.server_address[1]}", "token": "login-1"})
        assert _verdicts(watch.credential_verdicts()) == {"login": "unknown"}
        assert elsewhere.seen == [], "the key never left for the redirect's host"
    finally:
        server.shutdown()
        server.server_close()
        elsewhere.close()


def test_no_ask_starts_past_the_check_s_deadline(home):
    from probe.sdk.config import save_context

    save_context({"base_url": "https://api.example.test", "token": "a", "companion_token": "b",
                  "mcp_token": "c"})
    clock = iter([0.0, 1.0, watch.CREDENTIAL_DEADLINE_S + 1, watch.CREDENTIAL_DEADLINE_S + 2])
    asked: list = []

    def ask(base_url, token, timeout, door):
        asked.append((token, timeout))
        return "ok"

    found = watch.credential_verdicts(ask=ask, monotonic=lambda: next(clock))
    assert asked == [("a", watch.CREDENTIAL_TIMEOUT_S)]
    assert _verdicts(found) == {"login": "ok", "daemon_key": "unknown", "mcp_key": "unknown"}


def test_a_machine_with_no_key_asks_nothing(home):
    assert watch.credential_verdicts() == {}
