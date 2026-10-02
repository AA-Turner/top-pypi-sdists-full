"""`session_capture_state` — is a daemon live for this session, and if not, why."""

from __future__ import annotations

import contextlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

from probe.cli import capture_state


SID = "01a06383-6f4e-751a-b94c-bcefef19938c"


@pytest.fixture
def tap_dir(tmp_path, monkeypatch):
    d = tmp_path / "tap-state"
    d.mkdir()
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(d))
    monkeypatch.setenv("PROBE_AGENT", "pi")
    # The pid file lives in /tmp by contract (it is the one fact three
    # processes share, and `tap.config.pid_file` hardcodes it), so it is the
    # one piece of state `tmp_path` does NOT isolate. Clear it on both sides:
    # a leftover from the previous RUN of this file would otherwise decide
    # the "no pid file" case.
    pf = capture_state.pid_file(SID, "pi")
    with contextlib.suppress(OSError):
        pf.unlink()
    yield d
    with contextlib.suppress(OSError):
        pf.unlink()


def test_no_pid_file_reads_not_started(tap_dir):
    state = capture_state.session_capture_state(SID, source="pi")
    assert state.running is False
    assert state.reason == "not started"


def test_live_tap_pid_reads_running(tap_dir, monkeypatch):
    capture_state.pid_file(SID, "pi").write_text(str(os.getpid()), encoding="utf-8")
    monkeypatch.setattr(capture_state, "_looks_like_the_uploader", lambda pid: True)
    state = capture_state.session_capture_state(SID, source="pi")
    assert state.running is True
    assert state.pid == os.getpid()
    assert state.reason == "running"


def test_dead_pid_reads_not_started(tap_dir):
    capture_state.pid_file(SID, "pi").write_text("999999999", encoding="utf-8")
    state = capture_state.session_capture_state(SID, source="pi")
    assert state.running is False
    assert state.reason == "not started"


def test_killswitch_is_named_before_the_pid_file_is_read(tap_dir):
    (tap_dir / ".disabled").write_text("", encoding="utf-8")
    state = capture_state.session_capture_state(SID, source="pi")
    assert state.reason == "killswitch"


def test_a_halted_daemon_says_halted(tap_dir, monkeypatch):
    monkeypatch.setattr(capture_state, "_halted", lambda source: True)
    state = capture_state.session_capture_state(SID, source="pi")
    assert state.reason == "halted"


def test_every_reason_is_in_the_closed_vocabulary():
    assert capture_state.REASONS == (
        "running",
        "not started",
        "not installed",
        "not paired",
        "killswitch",
        "disabled path",
        "no session file",
        "interpreter too old",
        "halted",
    )


class _Spawned(list):
    def __call__(self, argv, env):
        self.append((argv, env))
        return 0


@pytest.fixture
def healable(tap_dir, tmp_path, monkeypatch):
    """Everything `ensure_capture` needs, so each test breaks exactly one thing."""
    (tap_dir / ".token").write_text("probe_ing_test", encoding="utf-8")
    transcript = tmp_path / "session.jsonl"
    transcript.write_text('{"type":"session"}\n', encoding="utf-8")
    monkeypatch.setenv("PI_SESSION_FILE", str(transcript))
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setattr(capture_state, "_tracking_is_on", lambda sid, cwd: True)
    monkeypatch.setattr(capture_state, "_capture_installed", lambda cwd: True)
    monkeypatch.setattr(capture_state, "_tap_runtime", lambda: ("/usr/bin/python3", None))
    return tmp_path


def test_heals_when_tracking_is_on_and_no_daemon_runs(healable, monkeypatch):
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    result = capture_state.ensure_capture(SID, cwd=healable, source="pi")
    assert result.started is True
    assert len(spawned) == 1
    argv, _env = spawned[0]
    assert argv[:4] == ["/usr/bin/python3", "-m", "tap", "start"]


def test_does_not_heal_under_claude_code(healable, monkeypatch):
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    result = capture_state.ensure_capture(SID, cwd=healable, source="claude_code")
    assert result.started is False
    assert result.reason == "not applicable"
    assert spawned == []


def test_does_not_heal_when_tracking_is_off(healable, monkeypatch):
    monkeypatch.setattr(capture_state, "_tracking_is_on", lambda sid, cwd: False)
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    assert capture_state.ensure_capture(SID, cwd=healable, source="pi").started is False
    assert spawned == []


def test_does_not_heal_when_capture_was_never_installed(healable, monkeypatch):
    monkeypatch.setattr(capture_state, "_capture_installed", lambda cwd: False)
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    result = capture_state.ensure_capture(SID, cwd=healable, source="pi")
    assert result.started is False
    assert result.reason == "not installed"
    assert spawned == []


def test_does_not_heal_an_ephemeral_session(healable, monkeypatch):
    monkeypatch.setenv("PI_SESSION_FILE", "")
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    result = capture_state.ensure_capture(SID, cwd=healable, source="pi")
    assert result.reason == "no session file"
    assert spawned == []


def test_a_fresh_heal_marker_blocks_a_second_attempt(healable, monkeypatch):
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    capture_state.ensure_capture(SID, cwd=healable, source="pi")
    capture_state.ensure_capture(SID, cwd=healable, source="pi")
    assert len(spawned) == 1


def test_an_expired_heal_marker_allows_another_attempt(healable, monkeypatch):
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    capture_state.ensure_capture(SID, cwd=healable, source="pi")
    marker = capture_state.heal_marker(SID, "pi")
    old = os.stat(marker).st_mtime - capture_state.HEAL_RETRY_SECONDS - 1
    os.utime(marker, (old, old))
    capture_state.ensure_capture(SID, cwd=healable, source="pi")
    assert len(spawned) == 2


def test_a_running_daemon_is_left_alone(healable, monkeypatch):
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(True, 123, "running"),
    )
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)
    assert capture_state.ensure_capture(SID, cwd=healable, source="pi").started is False
    assert spawned == []


# -- found by the live matrix, 2026-09-11 ------------------------------------


def test_an_absent_tap_state_dir_stops_the_heal_instead_of_recreating_it(
    healable, monkeypatch, tmp_path
):
    """`not installed` is a fact about the machine, not a failed daemon.

    The heal used to press on and then create the tap's state directory as a
    side effect of stamping its retry marker -- and that directory's absence
    is exactly what `session_capture_state` reads to answer `not installed`.
    So the heal erased the evidence for its own diagnosis, and a machine with
    no tap reported a crashed daemon that never existed.
    """
    gone = tmp_path / "no-tap-here"
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(gone))
    spawned = _Spawned()
    monkeypatch.setattr(capture_state, "_run", spawned)

    result = capture_state.ensure_capture(SID, cwd=healable, source="pi")

    assert result.started is False
    assert result.reason == "not installed"
    assert spawned == []
    assert not gone.exists(), "the heal conjured the tap state directory it was diagnosing"


@pytest.mark.parametrize("module", ["capture_state", "capture"])
def test_a_live_uploader_is_recognised_in_a_narrow_terminal(monkeypatch, module):
    """The real wrapper's command line carries ~550 characters of script before
    its first `tap`, and `ps` cuts at `$COLUMNS` unless told `-ww`. Without it,
    a caller with `COLUMNS` set read a live daemon as `not started`
    (2026-09-28). A real process, not a fake: the bug was in what `ps`
    prints."""
    from probe.cli import capture

    target = {"capture_state": capture_state, "capture": capture}[module]
    proc = _sleeper("x" * 600, "tap")
    try:
        monkeypatch.setenv("COLUMNS", "80")
        cut = subprocess.run(
            ["/bin/ps", "-p", str(proc.pid), "-o", "command="], capture_output=True, text=True
        ).stdout
        assert "tap" not in cut, "precondition: without -ww the line must be cut before `tap`"
        assert target._looks_like_the_uploader(proc.pid) is True
    finally:
        proc.kill()
        proc.wait()


def test_a_long_unrelated_command_line_is_not_the_uploader_it_would_signal(monkeypatch):
    """`-ww` hands `capture`'s SIGTERM gate the whole line, so its whole-word
    rule now sees every argument: a near-miss must still read as not ours."""
    from probe.cli import capture

    proc = _sleeper("x" * 600, "tapestry")
    try:
        monkeypatch.setenv("COLUMNS", "80")
        assert capture._looks_like_the_uploader(proc.pid) is False
    finally:
        proc.kill()
        proc.wait()


def test_every_uploader_identity_check_asks_ps_for_the_whole_line():
    """Four hand-kept copies (see `capture_state._looks_like_the_uploader`), one
    of them TypeScript that no Python test reaches: each must pass `-ww`."""
    agent = Path(__file__).resolve().parents[1]
    copies = [
        agent / "src/probe/cli/capture.py",
        agent / "src/probe/cli/capture_state.py",
        agent / "plugins/probe-research-tap/tap/start.py",
        agent / "plugins/probe-research-pi/src/daemon.ts",
    ]
    for path in copies:
        src = path.read_text(encoding="utf-8")
        calls = src.count('"command="')
        assert calls >= 1, f"{path}: no `ps` identity call found"
        assert src.count('"-ww", "-p"') == calls, f"{path}: a `ps` identity call without -ww"


def _sleeper(*args: str) -> subprocess.Popen:
    # argv[0] is fixed, not the interpreter path, so nothing but `args` can put
    # `tap` into what `ps` prints (a venv under `.../probe-research-tap/` would).
    return subprocess.Popen(
        ["sleeper", "-c", "import time; time.sleep(30)", *args], executable=sys.executable
    )
