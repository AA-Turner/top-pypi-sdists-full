"""What `probe session status`, `probe doctor` and `probe status` say about a
session's capture must be what is true (service hardening plan, lane A).

    A1  a pid file whose wrapper is gone does not hide the Probe service's
        `.hosted` marker beside it
    A3  a session the service hosts reads running only while its recorder
        holds the session (`service.status` `recorders[].recording`); no answer
        from the service keeps the old reading
    A5  a live session in mode off is "(off)", not "(ended)"
    A7  the CLI finds the watcher files where the Windows hooks put them
    A8  the 401 halt is read from the tap's state db without importing the tap
"""

from __future__ import annotations

import contextlib
import hashlib
import os
import sqlite3
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

from probe.cli import capture_state, doctor, service_calls
from probe.cli.service_calls import Reach
from probe.service import procid
from probe.service.protocol import Method
from probe.service.registry import Registry
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401
from tests.test_service_recorders import _THREADENV, _params

SID = "5d3e1c2a-capture-truth-0000-000000000001"

posix = pytest.mark.skipif(os.name != "posix", reason="POSIX /tmp, ps and the service")
#: The service records a session only on Python 3.11+ (the tap's floor,
#: `recorders.MIN_PYTHON`); on 3.10 the session's own `tap watch` does.
hosting = pytest.mark.skipif(sys.version_info < (3, 11), reason="the service loads the tap on 3.11+ only")


@pytest.fixture
def sid(tap_dir):
    """This test's own session id: its watcher files are in the shared /tmp,
    where tests running beside it (`-n`) must not find them."""
    return tap_dir[1]


@pytest.fixture
def tap_dir(tmp_path, monkeypatch):
    d = tmp_path / "tap-state"
    d.mkdir()
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(d))
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    own = f"capture-truth-{uuid.uuid4()}"
    files = [capture_state.pid_file(own, "claude_code"), capture_state.hosted_file(own, "claude_code")]
    yield d, own
    for path in files:
        path.unlink(missing_ok=True)


@pytest.fixture
def stand_in_service():
    """A live process whose command line names `probe.service`, which is all
    `_hosted_pid` asks `ps` for."""
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)", "probe.service"])
    try:
        yield proc.pid
    finally:
        proc.kill()
        proc.wait()


def _dead_pid() -> int:
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


# -- A1: a stale pid file beside the service's marker ---------------------------------


@posix
def test_a_dead_wrappers_pid_file_does_not_hide_the_services_marker(sid, stand_in_service):
    """Audit #2: the wrapper gave up (or was killed), the session moved to the
    service, and `probe session status` said `not started` for a session the
    service recorded, because a pid file it could read decided alone."""
    capture_state.hosted_file(sid, "claude_code").write_text(str(stand_in_service))
    capture_state.pid_file(sid, "claude_code").write_text(str(_dead_pid()))
    state = capture_state.session_capture_state(sid, "claude_code")
    assert state == capture_state.CaptureState(True, stand_in_service, "running")


@posix
def test_a_reused_pid_that_is_not_the_uploader_does_not_hide_the_marker(sid, stand_in_service, monkeypatch):
    capture_state.hosted_file(sid, "claude_code").write_text(str(stand_in_service))
    capture_state.pid_file(sid, "claude_code").write_text(str(os.getpid()))
    monkeypatch.setattr(capture_state, "_looks_like_the_uploader", lambda pid: pid != os.getpid())
    state = capture_state.session_capture_state(sid, "claude_code")
    assert state == capture_state.CaptureState(True, stand_in_service, "running")


@posix
def test_a_live_uploader_still_answers_before_the_marker(sid, stand_in_service, monkeypatch):
    capture_state.hosted_file(sid, "claude_code").write_text(str(stand_in_service))
    capture_state.pid_file(sid, "claude_code").write_text(str(os.getpid()))
    monkeypatch.setattr(capture_state, "_looks_like_the_uploader", lambda pid: True)
    assert capture_state.session_capture_state(sid, "claude_code").pid == os.getpid()


@posix
def test_a_dead_pid_file_and_no_marker_still_reads_not_started(sid):
    capture_state.pid_file(sid, "claude_code").write_text(str(_dead_pid()))
    assert capture_state.session_capture_state(sid, "claude_code").reason == "not started"


# -- A3: the recorder's claim decides a hosted session ---------------------------------


#: What the service could answer about this session's recorder, and the reading.
RECORDER_CASES = [
    pytest.param(None, "running", id="no-answer"),  # the marker, as before
    pytest.param([], "not started", id="not-recorded"),  # it answered and records no such session
    pytest.param([{"sid": "THIS", "alive": True, "recording": True}], "running", id="claimed"),
    # A live recorder holding nothing: its server does not answer, a retry wait,
    # the session's own `tap watch` holds it. Not a start that failed.
    pytest.param([{"sid": "THIS", "alive": True, "recording": False}], "not recording", id="not-claimed"),
    pytest.param([{"sid": "THIS", "alive": False, "recording": None}], "not started", id="ended"),
    pytest.param([{"sid": "THIS", "alive": True, "recording": None}], "running", id="old-tap"),  # cannot say
    pytest.param([{"sid": "another-session", "alive": True, "recording": True}], "not started", id="another"),
]


def _answer(rows, sid):
    return None if rows is None else [{**row, "sid": sid if row["sid"] == "THIS" else row["sid"]} for row in rows]


@posix
@pytest.mark.parametrize(("rows", "reading"), RECORDER_CASES)
def test_a_hosted_session_reads_what_its_recorder_does(sid, stand_in_service, monkeypatch, rows, reading):
    capture_state.hosted_file(sid, "claude_code").write_text(str(stand_in_service))
    monkeypatch.setattr(service_calls, "recorders", lambda timeout=0.5: _answer(rows, sid), raising=False)
    state = capture_state.session_capture_state(sid, "claude_code")
    assert (state.running, state.reason) == (reading == "running", reading), state
    assert state.reason in capture_state.REASONS


@posix
@pytest.mark.parametrize(("rows", "reading"), RECORDER_CASES)
def test_the_status_line_reads_the_recorder_as_the_cli_does(sid, stand_in_service, monkeypatch, hook, rows, reading):
    """The refresh asks the service too (`_service_recorders`, through the
    vendored `_service_rpc`), so the segment and `probe session status` say
    the same word."""
    capture_state.hosted_file(sid, "claude_code").write_text(str(stand_in_service))
    monkeypatch.setattr(service_calls, "recorders", lambda timeout=0.5: _answer(rows, sid), raising=False)
    monkeypatch.setattr(hook, "_service_recorders", lambda: _answer(rows, sid), raising=False)
    # Which pid is the service is its own check (`_is_the_service`: /proc on
    # Linux, the service's lock file on macOS, where a stand-in has none).
    monkeypatch.setattr(hook, "_is_the_service", lambda pid: pid == stand_in_service)
    cli = capture_state.session_capture_state(sid, "claude_code")
    assert hook._capture_reading(sid, "claude_code") == {"running": cli.running, "reason": cli.reason} == {
        "running": reading == "running", "reason": reading}


@posix
def test_the_status_line_asks_the_service_through_its_vendored_client(sid, stand_in_service, monkeypatch, hook):
    """One `service.status` for every session a refresh process reads (its
    `fetch-all` refreshes many), and the marker alone when it cannot ask."""
    import types

    calls = []

    class Rpc:
        @classmethod
        def connect(cls, timeout=0.3):
            return cls()

        def call(self, method, params, *, timeout):
            calls.append((method, timeout))
            return {"recorders": [{"sid": sid, "alive": True, "recording": False}]}

        def close(self):
            pass

    real_load = hook._load
    monkeypatch.setattr(hook, "_load", lambda name: types.SimpleNamespace(Rpc=Rpc) if name == "_service_rpc"
                        else real_load(name))
    monkeypatch.setattr(hook, "_is_the_service", lambda pid: pid == stand_in_service)  # see above
    capture_state.hosted_file(sid, "claude_code").write_text(str(stand_in_service))
    for _ in range(3):
        assert hook._capture_reading(sid, "claude_code") == {"running": False, "reason": "not recording"}
    assert calls == [("service.status", hook._RECORDERS_TIMEOUT_S)]
    hook._recorders_cache.clear()
    monkeypatch.setattr(Rpc, "connect", classmethod(lambda cls, timeout=0.3: None))
    assert hook._capture_reading(sid, "claude_code") == {"running": True, "reason": "running"}


@posix
def test_the_service_is_asked_only_for_a_hosted_session(sid, monkeypatch):
    asked = []
    monkeypatch.setattr(service_calls, "recorders", lambda timeout=0.5: asked.append(1) or [], raising=False)
    assert capture_state.session_capture_state(sid, "claude_code").reason == "not started"
    assert asked == []


@pytest.fixture
def pi_hosted(tmp_path, monkeypatch, stand_in_service):
    """A pi session the Probe service hosts, whose recorder holds no claim
    (its server does not answer); everything the heal needs."""
    d = tmp_path / "pi-tap"
    d.mkdir()
    (d / ".token").write_text("probe_ing_test", encoding="utf-8")
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(d))
    monkeypatch.setenv("PROBE_AGENT", "pi")
    transcript = tmp_path / "session.jsonl"
    transcript.write_text('{"type":"session"}\n', encoding="utf-8")
    monkeypatch.setenv("PI_SESSION_FILE", str(transcript))
    monkeypatch.setattr(capture_state, "_tracking_is_on", lambda sid, cwd: True)
    monkeypatch.setattr(capture_state, "_capture_installed", lambda cwd: True)
    monkeypatch.setattr(capture_state, "_tap_runtime", lambda: ("/usr/bin/python3", None))
    sid = f"capture-truth-heal-{uuid.uuid4()}"
    marker = capture_state.hosted_file(sid, "pi")
    marker.write_text(str(stand_in_service))
    asked, ran = [], []
    monkeypatch.setattr(service_calls, "recorders",
                        lambda timeout=0.5: asked.append(1) or [{"sid": sid, "alive": True, "recording": False}],
                        raising=False)
    monkeypatch.setattr(capture_state, "_run", lambda argv, env: ran.append(argv) or 0)
    try:
        yield sid, asked, ran
    finally:
        marker.unlink(missing_ok=True)


@posix
def test_the_self_heal_leaves_a_hosted_session_to_the_service(pi_hosted, tmp_path, capsys):
    """pi heals before every `probe` command (`ensure_capture`). A recorder the
    service runs that holds no claim at this moment (its server does not
    answer) must not be read as no recorder: that ran `tap start` every 10
    minutes and printed "started transcript capture" each time, and asked the
    service on every command."""
    sid, asked, ran = pi_hosted
    result = capture_state.ensure_capture(sid, tmp_path, source="pi")
    assert (result.started, result.reason) == (False, "running")
    assert ran == [] and asked == []
    assert "started transcript capture" not in capsys.readouterr().err


@posix
def test_pi_session_status_says_not_recording_for_a_hosted_session_without_a_claim(pi_hosted, tmp_path):
    """`probe session status` / `session on` / the state block (`_capture_block`)
    heal first, and the heal (marker only) says `running`: copied over the
    service's answer, it printed {"running": false, "reason": "running"}."""
    import importlib

    sid, asked, ran = pi_hosted
    cli_main = importlib.import_module("probe.cli.main")
    block = cli_main._capture_block(sid, heal_cwd=str(tmp_path))  # noqa: SLF001
    assert block == {"running": False, "pid": None, "reason": "not recording"}
    assert ran == [] and len(asked) == 1
    assert cli_main._effective(True, block) == "tracked, not capturing session transcript"  # noqa: SLF001


_STUCK_TAP = '''
import threading
from dataclasses import dataclass, field
ENDED, PAUSED, STOPPED, FAILED = "ended", "paused", "stopped", "failed"


@dataclass
class Controls:
    stop: threading.Event = field(default_factory=threading.Event)
    pause: threading.Event = field(default_factory=threading.Event)
    workers: object = None
    claimed: object = None

    def claim(self, folder):
        self.claimed = folder

    def beat(self):
        pass


def record(session, controls):
    behaviour = session["env"].get("BEHAVIOUR")
    if behaviour == "claim":
        controls.claim(session["cwd"])
        while not controls.stop.wait(0.05) and not controls.pause.is_set():
            pass
        controls.claim(None)
        return (ENDED if controls.stop.is_set() else PAUSED), ""
    # What tap.main does for a `.disabled_paths` folder or no token: return at
    # once, holding nothing; or fail every pass.
    return (FAILED, "boom") if behaviour == "fail" else (STOPPED, "returned 0")
'''


def _stuck_tap(root: Path) -> Path:
    tap = root / "tap"
    tap.mkdir(parents=True)
    (tap / "__init__.py").write_text('__version__ = "0.10.16"\n')
    (tap / "main.py").write_text("")
    (tap / "hosted.py").write_text(_STUCK_TAP)
    (tap / "threadenv.py").write_text(_THREADENV)
    return root


@hosting
@posix
@pytest.mark.parametrize("behaviour", ["stopped", "fail", "claim"])
def test_a_real_service_whose_recorder_records_nothing_is_not_running(service_home, tmp_path, monkeypatch, behaviour):
    """Audit #3, against a real service: a recorder whose tap loop returned at
    once (or fails every pass) leaves a live service behind the session's
    marker, and both `probe session status` and `probe doctor` said it was
    recording. The service itself says it is not (`recording: false`)."""
    sid = f"capture-truth-{behaviour}-{os.getpid()}"
    tap_state = tmp_path / "tap-state"
    tap_state.mkdir()
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tap_state))
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    proc, owner = spawn_agent()
    marker = capture_state.hosted_file(sid, "claude_code")
    try:
        service_home.start()
        answer = service_home.call(
            Method.SESSION_RECORD, _params(sid, owner, _stuck_tap(tmp_path / "tap"), "0.10.16", tmp_path,
                                           BEHAVIOUR=behaviour),
        )
        assert answer["recording"] is True
        marker.write_text(str(answer["pid"]))  # what `tap record` does with that answer
        claimed = behaviour == "claim"

        def settled():
            status = service_home.call(Method.STATUS)
            row = next((r for r in status["recorders"] if r["sid"] == sid), None)
            return status if row is not None and row["recording"] is claimed else None

        status = wait_for(settled, 5.0)
        assert status, "the recorder never reached the expected claim"
        state = capture_state.session_capture_state(sid, "claude_code")
        assert (state.running, state.reason) == ((True, "running") if claimed else (False, "not recording")), state
        view = service_calls.view()
        rows = [r for r in doctor.service_rows(view) if sid[:12] in r and "Recorded by the service" in r]
        assert rows and ("recording" if claimed else "not recording") in rows[0], rows
        assert ("not recording" in rows[0]) is not claimed
    finally:
        kill_agent(proc)
        with contextlib.suppress(OSError):
            marker.unlink()


def test_the_view_keeps_whether_a_recorder_holds_its_session():
    status = {
        "service_version": "1", "pid": 1, "state": "running",
        "recorders": [
            {"sid": "held-elsewhere-session", "alive": True, "recording": False, "last": "", "failures": 0},
            {"sid": "recording-session-id", "alive": True, "recording": True, "last": "", "failures": 0},
            {"sid": "an-old-taps-session", "alive": True, "last": "", "failures": 0},
            {"sid": "a-finished-session", "alive": False, "recording": None, "last": "ended", "failures": 0},
        ],
    }
    view = service_calls._filled(status, {"sessions": []})  # noqa: SLF001
    assert [r["recording"] for r in view["recorders"]] == [False, True, None, None]
    text = "\n".join(doctor.service_rows(view))
    assert "held-elsewhe… not recording" in text
    assert "recording-se… recording" in text
    assert "an-old-taps-… recording" in text  # a tap that cannot say: its thread's life
    assert "a-finished-s… stopped, last ended" in text


def test_recorders_answers_none_without_a_service(tmp_path):
    assert service_calls.recorders() is None


@hosting
@posix
def test_recorders_reads_the_services_status(service_home, tmp_path, monkeypatch):
    proc, owner = spawn_agent()
    sid = f"capture-truth-rows-{os.getpid()}"
    try:
        service_home.start()
        service_home.call(
            Method.SESSION_RECORD,
            _params(sid, owner, _stuck_tap(tmp_path / "tap"), "0.10.16", tmp_path, BEHAVIOUR="claim"),
        )
        rows = wait_for(lambda: [r for r in service_calls.recorders() or [] if r["recording"]], 5.0)
        assert rows, "no recorder row"
        assert rows[0]["sid"] == sid
        assert rows[0]["harness"] == "claude_code"
        # The tap the service loaded, which the update report compares (A6).
        assert rows[0]["tap_version"] == "0.10.16"
        assert set(rows[0]) == set(service_calls.RECORDER_KEYS)
    finally:
        kill_agent(proc)


# -- A6: the update report and the tap the service loaded ------------------------------


@hosting
@posix
def test_the_update_report_sees_a_session_the_service_records_on_an_older_tap(service_home, tmp_path):
    """Audit #6, against a real service: it loaded tap 0.10.13 for a session,
    the tap on disk is 0.10.16 now, and no `tap watch` command line shows it."""
    from probe.cli import updater

    proc, owner = spawn_agent()
    sid = f"capture-truth-old-tap-{os.getpid()}"
    old = tmp_path / "tap-0.10.13"
    _stuck_tap(old)
    (old / "tap" / "__init__.py").write_text('__version__ = "0.10.13"\n')
    try:
        service_home.start()
        service_home.call(Method.SESSION_RECORD, _params(sid, owner, old, "0.10.13", tmp_path, BEHAVIOUR="claim"))
        assert wait_for(lambda: updater.hosted_taps("claude_code").get(sid) == "0.10.13", 5.0)
        assert updater.stale_tap_daemons("claude_code", "0.10.16") == ("0.10.13",)
        assert updater.stale_tap_daemons("claude_code", "0.10.13") == ()
        assert updater.stale_tap_daemons("codex", "0.10.16") == ()
    finally:
        kill_agent(proc)


# -- A5: a live session in mode off ---------------------------------------------------


def _me() -> dict:
    return {"pid": os.getpid(), "start_time": procid.start_time(os.getpid())}


@pytest.mark.skipif(procid.start_time(os.getpid()) is None, reason="no start time on this platform")
def test_doctor_and_status_show_a_live_off_session_as_off(tmp_path, monkeypatch):
    """Audit #5: `Session.alive` is False for every mode-off session by design
    (it holds nothing up), and doctor rendered that as "(ended)" while its
    agent ran. The service's own `agent_live` decides instead: its owner,
    watched until it exits. Nothing is asked here per session (no `ps`)."""
    reg = Registry(tmp_path / "sessions.json")
    reg.register("sid-off-live", "claude_code", "off", _me(), 1)
    reg.register("sid-inline-live", "claude_code", "inline", _me(), 1)
    reg.register("sid-off-gone", "claude_code", "off", _me(), 1)
    reg.sessions["sid-off-gone"].owner_live = False  # its exit seen, not yet dropped
    listing = reg.listing()
    assert [s["agent_live"] for s in listing] == [True, True, False]
    monkeypatch.setattr(procid, "alive", lambda *a: pytest.fail("the CLI asked a process itself"))
    view = service_calls._filled(  # noqa: SLF001
        {"service_version": "1", "pid": 1, "state": "running", "recorders": []}, {"sessions": listing}
    )
    assert [s["agent_live"] for s in view["sessions"]] == [True, True, False]
    text = "\n".join(doctor.service_rows(view))
    assert "sid-off-live claude_code off (off)" in text
    assert "sid-inline-l… claude_code inline\n" in text + "\n"
    assert "sid-off-gone claude_code off (ended)" in text
    assert "3 live sessions" not in service_calls.summary(view)
    assert "2 live sessions (1 off)" in service_calls.summary(view)


def test_a_heartbeat_only_off_session_is_live_inside_its_ttl(tmp_path):
    now = [1000.0]
    reg = Registry(tmp_path / "sessions.json", clock=lambda: now[0])
    reg.register("pi-off", "pi", "off", None, 1)
    assert reg.listing()[0]["agent_live"] is True
    now[0] += reg.ttl + 1
    assert reg.listing()[0]["agent_live"] is False


def test_an_older_service_that_does_not_say_reads_off():
    """A service from before `agent_live`: unknown, which the service would
    not list once the agent exited; never a `ps` per session to find out."""
    view = service_calls._filled(  # noqa: SLF001
        {"service_version": "1", "pid": 1, "state": "running"},
        {"sessions": [{"sid": "pi-off", "harness": "pi", "mode": "off", "alive": False,
                       "owner": {"pid": os.getpid(), "start_time": "1"}}]},
    )
    assert view["sessions"][0]["agent_live"] is None
    assert "pi-off pi off (off)" in "\n".join(doctor.service_rows(view))


def test_an_ended_session_in_another_mode_still_reads_ended():
    view = {"reach": Reach.ANSWERED, "state": "running", "version": "1", "pid": 1, "recorders": [],
            "sessions": [{"sid": "sid-inline", "harness": "claude_code", "mode": "inline", "alive": False,
                          "agent_live": False}]}
    assert "sid-inline claude_code inline (ended)" in "\n".join(doctor.service_rows(view))


# -- A7: Windows watcher folder ---------------------------------------------------------


def test_on_windows_the_cli_reads_the_folder_the_hooks_named(tmp_path, monkeypatch):
    """Audit #13: session-start.sh exports Git Bash's `/tmp` as
    PROBE_TAP_WATCHER_DIR, and the tap and the service's recorder use it; the
    CLI looked in the user's temp folder, which need not be it."""
    import tempfile
    import types

    given = str(tmp_path / "git-bash-tmp")
    # `os.name` on capture_state's own view only: pathlib keeps this platform's
    # paths (Python 3.10's refuses a WindowsPath off Windows).
    fake_os = types.SimpleNamespace(name="nt", environ=os.environ, path=os.path)
    with monkeypatch.context() as patch:
        patch.setattr(capture_state, "os", fake_os)
        patch.setenv("PROBE_TAP_WATCHER_DIR", given)
        found = capture_state._watcher_dir()  # noqa: SLF001
        patch.setenv("PROBE_TAP_WATCHER_DIR", "relative/not-a-folder")
        fallback = capture_state._watcher_dir()  # noqa: SLF001
    assert found == Path(given)
    assert fallback == Path(tempfile.gettempdir())


def _on_windows(monkeypatch, module):
    """`os.name` "nt" on `module`'s own view only (pathlib keeps this platform's)."""
    import types

    fake = types.SimpleNamespace(**{n: getattr(os, n) for n in dir(os) if not n.startswith("__")})
    fake.name = "nt"
    monkeypatch.setattr(module, "os", fake)


@pytest.mark.skipif(os.name != "posix", reason="drives session-start.sh under bash")
def test_on_windows_the_folder_session_start_records_reaches_the_cli_and_the_status_line(
    tmp_path, monkeypatch, hook
):
    """Audit #13, end to end: PROBE_TAP_WATCHER_DIR lives only in what
    session-start.sh starts; `probe session status` and the status line's
    refresh run from other shells. The hook records Git Bash's `/tmp` in the
    tap's state folder, and both read it from there."""
    state = tmp_path / "tap-state"
    state.mkdir()
    git_bash_tmp = tmp_path / "git-bash-tmp"  # what `cygpath -w /tmp` says
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "cygpath").write_text(f'#!/bin/sh\n[ "$1" = -w ] && [ "$2" = /tmp ] && echo "{git_bash_tmp}"\n')
    (bin_dir / "cygpath").chmod(0o755)
    hooks = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap" / "hooks"
    env = {**os.environ, "OSTYPE": "msys", "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
           "PROBE_RESEARCH_TAP_PLUGIN_DIR": str(state), "PROBE_TAP_HOSTED": "0"}
    env.pop("PROBE_TAP_WATCHER_DIR", None)
    env.pop("PROBE_TAP_SOURCE", None)
    done = subprocess.run(["bash", str(hooks / "session-start.sh")], input="{}", capture_output=True, text=True,
                          env=env, timeout=30, check=False)
    assert done.returncode == 0, done.stderr
    assert (state / capture_state.WATCHER_DIR_FILE).read_text() == str(git_bash_tmp)

    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(state))
    monkeypatch.delenv("PROBE_TAP_WATCHER_DIR", raising=False)
    _on_windows(monkeypatch, capture_state)
    _on_windows(monkeypatch, hook)
    assert capture_state.pid_file("s1", "claude_code") == git_bash_tmp / "probe-research-tap-watcher-s1.pid"
    assert hook._watcher_dir("claude_code") == str(git_bash_tmp)
    assert hook._WATCHER_DIR_FILE == capture_state.WATCHER_DIR_FILE


def test_the_recorded_folder_wins_over_the_variable_and_the_temp_folder(tmp_path, monkeypatch, hook):
    state = tmp_path / "tap-state"
    state.mkdir()
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(state))
    monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", str(tmp_path / "from-the-variable"))
    _on_windows(monkeypatch, capture_state)
    _on_windows(monkeypatch, hook)
    assert capture_state._watcher_dir("claude_code") == tmp_path / "from-the-variable"  # noqa: SLF001
    (state / capture_state.WATCHER_DIR_FILE).write_text(str(tmp_path / "recorded"))
    assert capture_state._watcher_dir("claude_code") == tmp_path / "recorded"  # noqa: SLF001
    assert hook._watcher_dir("claude_code") == str(tmp_path / "recorded")
    (state / capture_state.WATCHER_DIR_FILE).write_text("not/absolute")
    assert capture_state._watcher_dir("claude_code") == tmp_path / "from-the-variable"  # noqa: SLF001


def test_probe_capture_off_on_windows_looks_at_the_watchers_pid_files_without_a_uid(tmp_path, monkeypatch):
    """`probe capture off` (and the wizard's disable and uninstall) on Windows:
    `_pid_dir()` names the folder the hooks' pid files are really in (the
    watcher folder), and Windows has no `os.getuid`. The stop looks at them
    and goes on; before, the uid check crashed it after the killswitch was
    set, before the service was asked to finish its recorders."""
    from probe.cli import capture

    monkeypatch.delenv(capture.PID_DIR_ENV, raising=False)
    monkeypatch.setattr(capture_state, "_watcher_dir", lambda source=None: tmp_path)
    monkeypatch.delattr(os, "getuid")
    prefix = capture_state.watcher_prefix(capture.agent_source())
    (tmp_path / f"{prefix}-watcher-s-0123456789.pid").write_text("4242\n")
    monkeypatch.setattr(capture, "_looks_like_the_uploader", lambda pid: False)  # no /bin/ps on Windows
    assert capture._pid_dir() == str(tmp_path)
    stopped, warnings = capture._stop_daemon()
    assert stopped is True and warnings == []


def test_off_windows_the_variable_names_the_folder_too_else_it_is_tmp(tmp_path, monkeypatch, hook):
    """From tap 0.10.19 the tap reads PROBE_TAP_WATCHER_DIR on every OS (a test
    keeps its watcher files out of the shared /tmp with it): `probe` and the
    status line look where it writes. Unset, or not an absolute folder: /tmp."""
    assert capture_state.WATCHER_DIR_ENV == "PROBE_TAP_WATCHER_DIR"
    if os.name != "posix":
        pytest.skip("POSIX's default")
    monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", str(tmp_path))
    assert capture_state._watcher_dir() == tmp_path  # noqa: SLF001
    assert hook._watcher_dir("claude_code") == str(tmp_path)  # noqa: SLF001
    monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", "relative/not-a-folder")
    assert capture_state._watcher_dir() == Path("/tmp")  # noqa: SLF001
    assert hook._watcher_dir("claude_code") == "/tmp"  # noqa: SLF001
    monkeypatch.delenv("PROBE_TAP_WATCHER_DIR")
    assert capture_state._watcher_dir() == Path("/tmp")  # noqa: SLF001


# -- A7: the status line hook on Windows -------------------------------------------------

_REFRESH = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks" / "statusline_refresh.py"


@pytest.fixture
def hook():
    """`statusline_refresh.py` loaded the way its hook runner loads it."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("statusline_refresh_capture_truth", _REFRESH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def on_windows(hook, monkeypatch, tmp_path):
    """The hook as it runs on Windows: the watcher folder Git Bash's `/tmp`
    maps to (PROBE_TAP_WATCHER_DIR), the service's lock file, and no
    `os.kill` at all (signal 0 is CTRL_C_EVENT there). `os.name` is patched
    on the hook's own view only: `os.path` stays this platform's."""
    import types

    watcher = tmp_path / "git-bash-tmp"
    watcher.mkdir()
    state = tmp_path / "tap-state"
    state.mkdir()
    lock = tmp_path / "service.lock"
    killed = []
    fake_os = types.SimpleNamespace(**{name: getattr(os, name) for name in dir(os) if not name.startswith("__")})
    fake_os.name = "nt"
    fake_os.kill = lambda pid, sig: killed.append(pid)
    monkeypatch.setattr(hook, "os", fake_os)
    monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", str(watcher))
    monkeypatch.setattr(hook, "_tap_plugin_dir", lambda source, env=None: str(state))
    monkeypatch.setattr(hook, "_service_lock", lambda: str(lock))
    alive = {}
    monkeypatch.setattr(hook, "_alive_nt", lambda pid, start: alive.get((pid, start), False), raising=False)
    return types.SimpleNamespace(watcher=watcher, lock=lock, alive=alive, killed=killed)


def _windows_file(win, source: str, suffix: str) -> Path:
    return win.watcher / f"{capture_state.watcher_prefix(source)}-watcher-{SID}{suffix}"


@pytest.mark.parametrize("source", ["claude_code", "codex", "pi"])
def test_on_windows_the_marker_the_lock_names_reads_running(hook, on_windows, source):
    """It said `not started` for every Windows session: the hook never read
    there, and read only `/tmp` elsewhere."""
    _windows_file(on_windows, source, ".hosted").write_text("4321", encoding="utf-8")
    on_windows.lock.write_text("4321 133456789012345678\n", encoding="utf-8")
    on_windows.alive[(4321, "133456789012345678")] = True
    assert hook._capture_reading(SID, source) == {"running": True, "reason": "running"}
    assert on_windows.killed == []


@pytest.mark.parametrize(
    "case", ["lock-names-another-pid", "service-gone", "no-lock", "marker-in-the-temp-folder", "pid-1"]
)
def test_on_windows_a_marker_naming_no_live_service_reads_not_started(hook, on_windows, case, monkeypatch, tmp_path):
    marker = _windows_file(on_windows, "claude_code", ".hosted")
    pid = "1" if case == "pid-1" else "4321"
    marker.write_text(pid, encoding="utf-8")
    if case != "no-lock":
        lock_pid = "9999" if case == "lock-names-another-pid" else pid
        on_windows.lock.write_text(f"{lock_pid} 1334\n", encoding="utf-8")
    on_windows.alive[(int(pid), "1334")] = case != "service-gone"
    if case == "marker-in-the-temp-folder":
        # The folder the hooks named is not Python's temp folder.
        monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", str(tmp_path / "elsewhere"))
    assert hook._capture_reading(SID, "claude_code") == {"running": False, "reason": "not started"}
    assert on_windows.killed == []


def test_on_windows_a_pid_file_is_never_probed_with_os_kill(hook, on_windows):
    """A wrapper's pid file names a Git Bash pid, and `os.kill(pid, 0)` there
    sends CTRL_C_EVENT: only the service's marker can say running."""
    _windows_file(on_windows, "claude_code", ".pid").write_text(str(os.getpid()), encoding="utf-8")
    assert hook._capture_reading(SID, "claude_code") == {"running": False, "reason": "not started"}
    assert on_windows.killed == []


def test_the_windows_liveness_check_says_no_where_it_cannot_ask(hook):
    """Off Windows there is no kernel32: never a crash, never a yes."""
    if os.name != "nt":
        assert hook._alive_nt(os.getpid(), "0") is False


@pytest.mark.skipif(os.name != "nt", reason="kernel32")
def test_the_windows_liveness_check_is_procids(hook):
    """The hook's stdlib copy of `procid.alive`'s Windows branch: the same
    start time for the same process, and no for a process that is gone."""
    start = procid.start_time(os.getpid())
    assert start and hook._alive_nt(os.getpid(), start) is True
    assert hook._alive_nt(os.getpid(), start + "1") is False
    gone = subprocess.Popen([sys.executable, "-c", "pass"])
    gone.wait()
    assert hook._alive_nt(gone.pid, start) is False


# -- A8: the 401 halt, from the tap's state db ------------------------------------------


@pytest.fixture
def halted_db(tmp_path, monkeypatch):
    # The tap is not importable from most CLI installs (another test may have
    # put a copy on this worker's sys.path): blocked, as it is there.
    monkeypatch.setitem(sys.modules, "tap", None)
    d = tmp_path / "pi-tap"
    d.mkdir()
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(d))
    monkeypatch.setenv("PROBE_BASE_URL", "https://probe.invalid")
    (d / ".token").write_text("probe_ing_current", encoding="utf-8")
    db = sqlite3.connect(d / "state.db")
    db.execute("CREATE TABLE meta (k TEXT PRIMARY KEY, v TEXT NOT NULL)")
    db.commit()
    yield d, db
    db.close()


def _fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def test_the_tap_is_blocked_in_these_tests(halted_db):
    """The precondition of the next tests: as on most CLI installs."""
    with pytest.raises(ImportError):
        import tap  # noqa: F401


@pytest.mark.parametrize(
    ("rows", "halted"),
    [
        ({}, False),
        ({"last_401_at": "2026-10-24T03:00:00Z"}, True),  # an old tap stamped no fingerprint
        ({"last_401_at": "2026-10-24T03:00:00Z", "last_401_token_sha256": _fingerprint("probe_ing_current")}, True),
        ({"last_401_at": "2026-10-24T03:00:00Z", "last_401_token_sha256": _fingerprint("probe_ing_old")}, False),
        ({"last_401_at": ""}, False),
    ],
    ids=["no-latch", "no-fingerprint", "same-token", "re-paired", "cleared"],
)
def test_the_401_latch_is_read_without_the_tap(halted_db, rows, halted):
    d, db = halted_db
    db.executemany("INSERT INTO meta VALUES (?, ?)", rows.items())
    db.commit()
    assert capture_state._halted("pi") is halted  # noqa: SLF001
    assert (capture_state.session_capture_state(SID, "pi").reason == "halted") is halted


def test_no_credential_is_no_halt(halted_db):
    d, db = halted_db
    (d / ".token").unlink()
    db.execute("INSERT INTO meta VALUES ('last_401_at', 'x')")
    db.commit()
    assert capture_state._halted("pi") is False  # noqa: SLF001


def test_a_status_read_never_creates_the_db(tmp_path, monkeypatch):
    d = tmp_path / "pi-tap"
    d.mkdir()
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(d))
    assert capture_state._halted("pi") is False  # noqa: SLF001
    assert not (d / "state.db").exists()


def test_a_db_that_is_not_the_taps_is_no_halt(tmp_path, monkeypatch):
    d = tmp_path / "pi-tap"
    d.mkdir()
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(d))
    (d / ".token").write_text("t", encoding="utf-8")
    (d / "state.db").write_bytes(b"not a database at all")
    assert capture_state._halted("pi") is False  # noqa: SLF001


def test_a_db_locked_by_a_writer_is_answered_at_once(halted_db):
    d, db = halted_db
    db.execute("INSERT INTO meta VALUES ('last_401_at', 'x')")
    db.commit()
    db.execute("BEGIN EXCLUSIVE")
    try:
        started = time.monotonic()
        capture_state._halted("pi")  # noqa: SLF001
        assert time.monotonic() - started < 1.0
    finally:
        db.rollback()
