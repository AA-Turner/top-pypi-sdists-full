"""The papers hook: a paper-type `WebSearch` in the daemon profile is held once,
with the command to run, until the agent has tried `probe paper find`.

The hook runs as shipped (the full plugin's file, its sibling `_session_marker`
copy), on the same state files the CLI writes; only `version_check`'s
`probe --version` probe is replaced, so no test spawns a CLI.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe.sdk import session_marker

AGENT = Path(__file__).resolve().parents[1]
FULL = AGENT / "plugins" / "probe-research" / "hooks"
LEAN = AGENT / "plugins" / "probe-research-daemon" / "hooks"
SID = "0199a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b"
WINDOW = session_marker.PAPER_FIND_WINDOW_S


def _load():
    spec = importlib.util.spec_from_file_location("_test_papers_hook", FULL / "papers_hook.py")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(FULL))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(FULL))
    return module


hook = _load()


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.setenv("PROBE_PLUGIN_PROFILE", "daemon")


@pytest.fixture
def cli(monkeypatch):
    """`version_check.paper_find_ready`, counted: the hook may ask it at most once."""
    calls: list[int] = []
    answer = {"ready": True}
    sys.path.insert(0, str(FULL))
    try:
        import version_check
    finally:
        sys.path.remove(str(FULL))

    def ready() -> bool:
        calls.append(1)
        return answer["ready"]

    monkeypatch.setattr(version_check, "paper_find_ready", ready)
    monkeypatch.setitem(sys.modules, "version_check", version_check)
    return answer, calls


def _search(query: str = "SFT data scaling small model distillation arXiv 2026", **extra) -> dict:
    return {
        "hook_event_name": "PreToolUse",
        "session_id": SID,
        "tool_name": "WebSearch",
        "tool_input": {"query": query},
        "cwd": "/tmp",
        **extra,
    }


def _touch(path: Path, age_s: float = 0.0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    when = time.time() - age_s
    os.utime(path, (when, when))


def test_a_paper_search_is_held_with_the_approved_text(cli):
    assert hook.hold_reason(_search(), time.time()) == session_marker.PAPER_SEARCH_HOLD
    assert session_marker.paper_hold_stamp_path(SID).exists(), "the hold is recorded before it is answered"


@pytest.mark.parametrize(
    "query,held",
    [
        ("LLM post-processing ASR transcripts inverse text normalization arXiv", True),
        ("Karan et al finetuning with sampling", True),
        ("recent papers on GRPO reward collapse", True),
        ("NeurIPS 2025 best paper", True),
        ("a survey paper on dictation formatting", True),
        ("survey table schema postgres", False),
        ("linux acl permissions", False),
        ("s3 bucket acl policy", False),
        ("literature on KL penalties in RLHF", True),
        ("openreview LIMA reviews", True),
        ("pytorch lightning ddp hang on exit", False),
        ("paperclip maximizer", False),
        ("how to vacuum a postgres table", False),
        ("", False),
    ],
)
def test_only_paper_type_queries_are_held(cli, query, held):
    assert (hook.hold_reason(_search(query), time.time()) is not None) is held


def test_the_agent_profile_is_never_held(cli, monkeypatch):
    monkeypatch.delenv("PROBE_PLUGIN_PROFILE")
    assert hook.hold_reason(_search(), time.time()) is None
    assert cli[1] == [], "no CLI probe outside the daemon profile"


@pytest.mark.parametrize("tool", ["WebFetch", "Bash", "FetchURL"])
def test_other_tools_are_never_held(cli, tool):
    payload = _search()
    payload["tool_name"] = tool
    payload["tool_input"] = {"url": "https://arxiv.org/abs/2610.02140", "command": "probe ask x"}
    assert hook.hold_reason(payload, time.time()) is None


def test_a_session_turned_off_is_never_held(cli):
    assert session_marker.set_session_state(SID, session_marker.STATE_OFF)
    assert hook.hold_reason(_search(), time.time()) is None


@pytest.mark.parametrize("state", [session_marker.STATE_DAEMON, session_marker.STATE_READ_ONLY])
def test_on_and_read_only_sessions_are_held(cli, state):
    assert session_marker.set_session_state(SID, state)
    assert hook.hold_reason(_search(), time.time()) is not None


def test_a_recent_paper_find_lets_the_web_through(cli):
    _touch(session_marker.paper_find_stamp_path(SID), age_s=WINDOW - 60)
    assert hook.hold_reason(_search(), time.time()) is None


def test_an_old_paper_find_does_not(cli):
    _touch(session_marker.paper_find_stamp_path(SID), age_s=WINDOW + 60)
    assert hook.hold_reason(_search(), time.time()) is not None


def test_one_hold_per_window_then_searches_run(cli):
    now = time.time()
    assert hook.hold_reason(_search(), now) is not None
    assert hook.hold_reason(_search("another arXiv query"), now + 5) is None
    assert hook.hold_reason(_search("a third arXiv query"), now + WINDOW + 5) is not None


def test_an_unwritable_hold_stamp_lets_the_search_run(cli, monkeypatch):
    def refuse(self, *a, **k):
        raise PermissionError("read-only state dir")

    monkeypatch.setattr(Path, "touch", refuse)
    assert hook.hold_reason(_search(), time.time()) is None, "no hold the hook could not bound"


def test_a_cli_without_the_command_is_never_held_and_asked_once(cli):
    answer, calls = cli
    answer["ready"] = False
    assert hook.hold_reason(_search(), time.time()) is None
    assert hook.hold_reason(_search("arXiv again"), time.time()) is None
    assert len(calls) == 1, "the answer is cached for the session"
    assert session_marker.paper_cli_cache_path(SID).read_text() == "0"


def test_a_cli_that_could_not_be_asked_is_asked_again(cli):
    """One slow or failed start must not switch the hook off for the session."""
    answer, calls = cli
    answer["ready"] = None
    assert hook.hold_reason(_search(), time.time()) is None
    assert not session_marker.paper_cli_cache_path(SID).exists()
    answer["ready"] = True
    assert hook.hold_reason(_search("arXiv again"), time.time()) is not None
    assert len(calls) == 2


@pytest.mark.parametrize("sid", ["../../escape", "/tmp/abs-session-id", "short", ""])
def test_a_session_id_that_is_not_a_file_name_writes_nothing(cli, tmp_path, sid):
    payload = _search()
    payload["session_id"] = sid
    assert hook.hold_reason(payload, time.time()) is None
    assert not list(tmp_path.rglob("*.papers*"))
    assert cli[1] == []


def test_a_machine_default_of_off_is_never_held(cli, monkeypatch):
    monkeypatch.setenv("PROBE_SESSION_STATE", session_marker.STATE_OFF)
    assert hook.hold_reason(_search(), time.time()) is None
    assert cli[1] == [], "off is decided before the CLI is asked"


def test_a_stored_default_of_off_is_never_held(cli):
    session_marker.write_default_state(session_marker.STATE_OFF)
    assert hook.hold_reason(_search(), time.time()) is None


def test_the_cli_answer_is_asked_only_after_the_cheap_checks(cli):
    hook.hold_reason(_search("pytorch ddp hang"), time.time())
    assert cli[1] == []


def test_main_writes_the_deny_shape_and_survives_garbage(cli, monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(_search())))
    hook.main()
    out = json.loads(capsys.readouterr().out)
    assert out == {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": session_marker.PAPER_SEARCH_HOLD,
        }
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO("not json"))
    hook.main()
    assert capsys.readouterr().out == ""


def test_an_exception_inside_lets_the_call_run(monkeypatch, capsys):
    def boom(*_a, **_k):
        raise RuntimeError("bug")

    monkeypatch.setattr(hook, "hold_reason", boom)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(_search())))
    hook.main()
    assert capsys.readouterr().out == ""


def _fake_cli(tmp_path: Path, kind: str) -> Path:
    """A `probe` that has `paper find` (`has-command`), an older one click answers
    `No such command` for (`older-cli`), or one that crashes (`crashes`, as a CLI
    mid-update does)."""
    fake = tmp_path / "bin" / "probe"
    fake.parent.mkdir(parents=True, exist_ok=True)
    answer = {
        "has-command": "exit 0",
        "older-cli": "echo \"Error: No such command 'find'.\" >&2; exit 2",
        "crashes": "echo \"ImportError: half-installed\" >&2; exit 1",
    }[kind]
    fake.write_text(f'#!/bin/sh\nif [ "$1 $2 $3" = "paper find --help" ]; then {answer}; fi\nexit 2\n')
    fake.chmod(0o755)
    return fake


@pytest.mark.parametrize(
    "cli_kind,held,cached",
    [("has-command", True, "1"), ("older-cli", False, "0"), ("crashes", False, None), ("no-cli", False, None)],
)
def test_the_shipped_lean_copy_holds_only_beside_a_cli_with_the_command(tmp_path, cli_kind, held, cached):
    """System python3 -S, the lean plugin's own folder, a real subprocess to a
    fake `probe`: the deny reaches stdout only when `probe paper find --help`
    succeeds, and a CLI that could not be asked is not remembered."""
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(tmp_path),
        "XDG_STATE_HOME": str(tmp_path / "state"),
        "PROBE_PLUGIN_PROFILE": "daemon",
    }
    if cli_kind != "no-cli":
        env["PROBE_BIN"] = str(_fake_cli(tmp_path, cli_kind))
    else:
        env["PROBE_BIN"] = str(tmp_path / "missing" / "probe")
    out = subprocess.run(
        ["/usr/bin/env", "python3", "-S", str(LEAN / "papers_hook.py")],
        input=json.dumps(_search()),
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    assert out.returncode == 0, out.stderr
    if held:
        assert json.loads(out.stdout)["hookSpecificOutput"]["permissionDecisionReason"] == session_marker.PAPER_SEARCH_HOLD
    else:
        assert out.stdout == ""
    cache = tmp_path / "state" / "probe" / "sessions" / f"{SID}.papers-cli"
    assert (cache.read_text() if cache.exists() else None) == cached
