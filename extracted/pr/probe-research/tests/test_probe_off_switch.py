"""Whoever moves a session's switch tells the Probe service at once, so Probe
off means the session is not captured from that moment, and a move back on
captures from that moment (`probe.service.capture_gate`).

    the CLI     `probe session state|toggle|track|untrack`
                (`service_calls.capture_switched`): the service looks now; with
                the switch on again and the service gone idle while the session
                was off, it starts it. Never a start for a session switched off.
    the hook    a typed `/probe ...` (`tracking_guard._capture_switched`): the
                same, through the hook's own helper (`_service_call`), which
                itself never starts a service.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

from probe import cli
from probe.cli import service_calls
from probe.sdk import session_marker

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
SID = "abcdabcd-1111-4222-8333-444455556666"


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_HOOK_SERVICE", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)


# -- the CLI ---------------------------------------------------------------------------


class _Client:
    def __init__(self, monkeypatch, *, reachable: bool):
        from probe.service import client

        self.ensured: list = []
        self.calls: list = []
        monkeypatch.setattr(service_calls, "_reachable", lambda: reachable)
        monkeypatch.setattr(client, "ensure", lambda wait=0.0: self.ensured.append(wait) or client.Ensured.RUNNING)
        monkeypatch.setattr(client, "call_within", lambda method, params, **kw: self.calls.append((method, params))
                            or {"recording": True})


def _hold(sid: str) -> None:
    """What a service that held `sid` (off) saves when it goes idle."""
    from probe.service import paths

    folder = paths.service_dir()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "recorders.json").write_text(json.dumps({"v": 1, "sessions": [{"sid": sid}]}))


@pytest.mark.parametrize("word, off", [("off", True), ("on", False), ("read", False)])
def test_moving_the_switch_has_the_service_look_at_once(monkeypatch, capsys, word, off):
    seen = []
    monkeypatch.setattr(service_calls, "capture_switched", lambda sid, *, off: seen.append((sid, off)))
    session_marker.set_session_state(SID, session_marker.STATE_FULL if off else session_marker.STATE_OFF)
    assert cli.main(["session", "state", word, "--session", SID]) in (0, None)
    assert seen == [(SID, off)]


def test_a_toggle_and_track_and_untrack_tell_it_too(monkeypatch, capsys):
    seen = []
    monkeypatch.setattr(service_calls, "capture_switched", lambda sid, *, off: seen.append((sid, off)))
    session_marker.set_session_state(SID, session_marker.STATE_OFF)
    for args in (["session", "toggle"], ["session", "untrack"], ["session", "track"]):
        assert cli.main([*args, "--session", SID]) in (0, None)
    assert seen == [(SID, False), (SID, False), (SID, False)]


def test_the_service_looks_when_it_runs(monkeypatch):
    fake = _Client(monkeypatch, reachable=True)
    assert service_calls.capture_switched(SID, off=True) is True
    assert fake.calls == [("session.recording", {"sid": SID})] and fake.ensured == []


def test_a_session_switched_off_never_starts_the_service(monkeypatch):
    fake = _Client(monkeypatch, reachable=False)
    _hold(SID)
    assert service_calls.capture_switched(SID, off=True) is None
    assert fake.ensured == [] and fake.calls == []


def test_switched_on_the_service_that_held_it_while_off_starts_and_looks(monkeypatch):
    fake = _Client(monkeypatch, reachable=False)
    _hold(SID)
    assert service_calls.capture_switched(SID, off=False) is True
    assert fake.ensured == [service_calls.SWITCH_START_S]
    assert fake.calls == [("session.recording", {"sid": SID})]


def test_switched_on_a_session_the_service_never_held_starts_nothing(monkeypatch):
    fake = _Client(monkeypatch, reachable=False)
    _hold("someone-else-0000")
    assert service_calls.capture_switched(SID, off=False) is None
    assert fake.ensured == [] and fake.calls == []


# -- the hook ------------------------------------------------------------------------------


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    added = str(path.parent) not in sys.path
    if added:
        sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(str(path.parent))
    return module


@pytest.fixture
def guard():
    return _load(HOOKS / "tracking_guard.py", "_tracking_guard_off_switch")


@pytest.mark.parametrize("prompt, state", [("/probe off", "off"), ("/probe on", "full"), ("/probe read", "read-only")])
def test_a_typed_switch_has_the_service_look_at_once(guard, monkeypatch, capsys, prompt, state):
    seen = []
    monkeypatch.setattr(guard, "_capture_switched", seen.append)
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": SID, "prompt": prompt, "cwd": "/tmp"}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    assert session_marker.session_state(SID) == state
    assert seen == [SID]


class _Popen:
    started: list = []

    def __init__(self, argv, **kwargs):
        _Popen.started.append(argv)


@pytest.fixture
def no_service(monkeypatch, tmp_path):
    """No service answers; runtime.json names an interpreter (a CLI ran here)."""
    paths = _load(HOOKS / "_service_paths.py", "_service_paths_off_switch")
    runtime = Path(paths.runtime_path())
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(json.dumps({"python": sys.executable}))
    import subprocess

    _Popen.started = []
    monkeypatch.setattr(subprocess, "Popen", _Popen)
    return _Popen.started


def test_the_hook_starts_the_service_for_a_session_switched_back_on(guard, no_service):
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    guard._capture_switched(SID)
    assert no_service == [[sys.executable, "-I", "-m", "probe.service.client", "ensure"]]


def test_the_hook_never_starts_the_service_for_a_session_switched_off(guard, no_service):
    session_marker.set_session_state(SID, session_marker.STATE_OFF)
    guard._capture_switched(SID)
    assert no_service == []


def test_a_hook_told_not_to_ask_the_service_neither_asks_nor_starts_it(guard, no_service, monkeypatch):
    monkeypatch.setenv("PROBE_HOOK_SERVICE", "off")
    session_marker.set_session_state(SID, session_marker.STATE_FULL)
    guard._capture_switched(SID)
    assert no_service == []


def test_the_hooks_helper_itself_never_starts_a_service(no_service):
    helper = _load(HOOKS / "_service_call.py", "_service_call_off_switch")
    assert helper.capture_switched(SID) is False
    assert no_service == []
