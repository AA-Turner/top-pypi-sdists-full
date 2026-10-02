"""The tracking-off branch of the plugin's context-boundary injection.

`probe session untrack` writes a durable marker, but before this branch the
only thing carrying "do not record" across a compaction was skill text the
summarizer may drop -- and version_check.py then injected a reconcile-Probe
nudge into the rebuilt context without consulting the marker. The skill
promises "no more tracking nudges"; the plugin broke the promise at the exact
moment the model was most suggestible.

The properties pinned here:

  1. Compact + marker  -> the off contract, and NOT the reconcile nudge.
  2. Compact + no marker -> the reconcile nudge, unchanged (regression guard).
  3. Resume + marker   -> the off contract (same marker, same rebuilt context).
  4. Resume + no marker -> nothing. A normally-tracking resume needs no nudge;
     injecting one would be new nagging, not a fix.
  5. Every doubt (no id, invalid id, precompact) degrades to today's
     behaviour, never to honouring a declaration nobody made.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "probe-research"

SESSION_ID = "11111111-2222-3333-4444-555555555555"


def _load_hook():
    """Load version_check.py the way session-start.sh does.

    The hook's own directory must be on sys.path -- that is what makes its
    sibling imports (`version_policy`, `_session_marker`) resolve, because the
    system python3 it ships to has no probe package.
    """
    path = PLUGIN / "hooks" / "version_check.py"
    spec = importlib.util.spec_from_file_location("_tracking_off_hook_under_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    hooks_dir = str(path.parent)
    added = hooks_dir not in sys.path
    if added:
        sys.path.insert(0, hooks_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(hooks_dir)
    # Same reason as the sibling nudge test: these two probe the MACHINE (the
    # installed CLI's version, a real state directory) and would make every
    # assertion here depend on the laptop running the suite.
    module._team_note_cli_too_old = lambda _binary: None
    return module


@pytest.fixture
def hook(tmp_path, monkeypatch):
    """The hook with isolated state and a session id, tracking ON by default."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")
    monkeypatch.delenv("PROBE_HOOK_EVENT", raising=False)
    monkeypatch.delenv("PROBE_SESSION_SOURCE", raising=False)
    monkeypatch.setenv("PROBE_SESSION_ID", SESSION_ID)
    return _load_hook()


def _untrack(hook):
    assert hook._session_marker.set_tracking(SESSION_ID, False)


# ---------------------------------------------------------------------------
# The four branches.
# ---------------------------------------------------------------------------


def test_compact_with_marker_restates_the_contract(hook, monkeypatch):
    """Property 1. The one change this feature exists for: an untracked
    session's compaction gets the off contract, not an order to do Probe work."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    _untrack(hook)

    ctx = hook._start_context()
    assert ctx == hook.TRACKING_OFF_CONTEXT
    assert ctx != hook.COMPACT_CONTEXT


def test_compact_without_marker_keeps_the_nudge(hook, monkeypatch):
    """Property 2. The regression guard: a tracking session compacts exactly
    as before."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")

    assert hook._start_context() == hook.COMPACT_CONTEXT


def test_resume_with_marker_restates_the_contract(hook, monkeypatch):
    """Property 3. A resume rebuilds context from the same transcript the
    summarizer already ate; the marker outlives both."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "resume")
    _untrack(hook)

    assert hook._start_context() == hook.TRACKING_OFF_CONTEXT


def test_resume_without_marker_says_nothing(hook, monkeypatch):
    """Property 4. No new nagging: resume was silent before and stays silent
    for a session that is tracking normally."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "resume")

    assert hook._start_context() is None


# ---------------------------------------------------------------------------
# The machine default is a declaration too.
# ---------------------------------------------------------------------------


def _default_off(tmp_path):
    """Set the machine default to `off` in the config FILE (its documented
    home), leaving no per-session marker."""
    cfg = tmp_path / "config" / "probe"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "config.json").write_text(
        json.dumps({"version": 2, "defaults": {"session_tracking": "off"}}),
        encoding="utf-8",
    )


def _folder_default(folder: Path, value: str = "off") -> None:
    cfg = folder / ".probe"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "config.json").write_text(
        json.dumps({"defaults": {"session_tracking": value}}), encoding="utf-8"
    )


def test_a_fresh_start_gets_the_contract_when_off(hook, monkeypatch, tmp_path):
    """The channel that was empty. A fresh start carried nothing about
    tracking, so the model's only information was the global instruction
    telling it to register the work -- and it did."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "startup")
    _default_off(tmp_path)

    assert hook._start_context() == hook.TRACKING_OFF_CONTEXT


def test_a_fresh_start_stays_silent_when_tracking(hook, monkeypatch):
    """No new nagging: a tracking session starts as quietly as it always did."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "startup")

    assert hook._start_context() is None


def test_session_start_seeds_the_signal_from_the_default(hook, tmp_path):
    """One setting, one file, present from the session's first moment -- so no
    reader has to invent what an absent file means."""
    _default_off(tmp_path)
    assert hook._session_marker.tracking_signal(SESSION_ID) is None

    hook._seed_tracking_signal()

    assert hook._session_marker.tracking_signal(SESSION_ID) == "off"


def test_session_start_seeds_the_signal_from_the_initial_folder(hook, monkeypatch, tmp_path):
    repo = tmp_path / "research repo"
    cwd = repo / "src"
    cwd.mkdir(parents=True)
    _folder_default(repo)
    monkeypatch.setenv("PROBE_SESSION_CWD", str(cwd))

    hook._seed_tracking_signal()

    assert hook._session_marker.tracking_signal(SESSION_ID) == "off"


def test_the_seed_never_overrides_a_decision(hook, tmp_path):
    """A researcher who turned tracking ON on a default-off machine keeps it
    through every resume and compaction the seed runs on."""
    _default_off(tmp_path)
    assert hook._session_marker.set_tracking(SESSION_ID, True)

    hook._seed_tracking_signal()

    assert hook._session_marker.tracking_signal(SESSION_ID) == "on"


def test_the_seed_bypasses_folder_resolution_after_a_decision(hook, monkeypatch):
    assert hook._session_marker.set_tracking(SESSION_ID, False)
    monkeypatch.setattr(
        hook._session_marker,
        "resolve_tracking_default",
        lambda *_args, **_kwargs: pytest.fail(
            "an existing signal must bypass folder resolution"
        ),
    )

    hook._seed_tracking_signal()

    assert hook._session_marker.tracking_signal(SESSION_ID) == "off"


@pytest.mark.parametrize("source", ["resume", "compact"])
def test_folder_seed_never_overrides_a_decision_at_context_boundaries(
    hook, monkeypatch, tmp_path, source
):
    repo = tmp_path / "research"
    repo.mkdir()
    _folder_default(repo)
    monkeypatch.setenv("PROBE_SESSION_CWD", str(repo))
    monkeypatch.setenv("PROBE_SESSION_SOURCE", source)
    assert hook._session_marker.set_tracking(SESSION_ID, True)

    hook._seed_tracking_signal()

    assert hook._session_marker.tracking_signal(SESSION_ID) == "on"


def test_a_default_off_machine_gets_the_contract_with_no_marker(hook, monkeypatch, tmp_path):
    """The hole this closes. A default-off machine WAS treated as tracking here
    because only an explicit marker counted, so a compaction told the model to
    reconcile Probe on a box whose whole posture is `do not record`."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    _default_off(tmp_path)

    assert hook._start_context() == hook.TRACKING_OFF_CONTEXT


# ---------------------------------------------------------------------------
# Doubt degrades to today's behaviour.
# ---------------------------------------------------------------------------


def test_the_off_contract_stays_one_sentence(hook):
    """Length is a feature here, not tidiness. This string is injected at EVERY
    session start, so it is the most-repeated text the plugin owns and the only
    one a researcher re-reads all day.

    TWO sentences since 2026-09-17: the state, and ONE mention of `/probe on`
    that replaced "ask the user" -- the behaviour eval showed that phrasing
    turning into an agent reaching for the switch itself, or asking on every
    refusal. Drift back toward the four-sentence version -- naming which of two
    origins set the state, or repeating how to flip it -- is the regression."""
    import re as _re

    text = hook.TRACKING_OFF_CONTEXT
    assert len(_re.findall(r"[.!?](?:\s|$)", text)) <= 2, "two sentences at most"
    assert text.endswith(".")
    assert len(text.split()) <= 45
    assert "never as a running reminder" in text


def test_every_start_carries_the_contract_when_off(hook, monkeypatch):
    """Inverted deliberately. This pinned startup, clear and an unknown source
    staying SILENT with the marker set, because the feature was scoped to
    context BOUNDARIES -- the places a declaration gets lost.

    That scoping was the leak. A fresh start is exactly where an agent picks up
    a global instruction to register its work in Probe, and it was the one
    start that said nothing back. The contract describes the session's STATE,
    not which boundary it crossed, so every start carries it."""
    _untrack(hook)
    for source in ("startup", "clear", ""):
        monkeypatch.setenv("PROBE_SESSION_SOURCE", source)
        assert hook._start_context() == hook.TRACKING_OFF_CONTEXT


def test_precompact_stays_silent_even_with_marker(hook, monkeypatch):
    """PreCompact has no context channel; the marker changes nothing there."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    monkeypatch.setenv("PROBE_HOOK_EVENT", "precompact")
    _untrack(hook)

    assert hook._start_context() is None


def test_missing_session_id_reads_as_tracking_on(hook, monkeypatch):
    """No id (an old session-start.sh, a codex path) -> the nudge, exactly as
    today. Uncertain must not silently honour a declaration nobody made."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    monkeypatch.delenv("PROBE_SESSION_ID", raising=False)
    _untrack(hook)

    assert hook._start_context() == hook.COMPACT_CONTEXT


def test_invalid_session_id_reads_as_tracking_on(hook, monkeypatch):
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    monkeypatch.setenv("PROBE_SESSION_ID", "../../../etc/passwd")

    assert hook._start_context() == hook.COMPACT_CONTEXT


# ---------------------------------------------------------------------------
# The contract line reaches the payload.
# ---------------------------------------------------------------------------


def test_final_carries_the_contract_into_additional_context(hook, monkeypatch):
    """_final is where every main() exit converges; the contract must land on
    the additionalContext channel there, whatever the version check said."""
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")
    _untrack(hook)
    captured = {}

    def _emit(obj):
        captured.update(obj)
        raise SystemExit(0)

    monkeypatch.setattr(hook, "_emit", _emit)
    with pytest.raises(SystemExit):
        hook._final({"continue": True})

    hso = captured["hookSpecificOutput"]
    assert hso["hookEventName"] == "SessionStart"
    assert hso["additionalContext"] == hook.TRACKING_OFF_CONTEXT
    assert json.dumps(captured)  # the payload stays serializable


def test_wiring_registers_no_new_events(hook):
    """Change 1 rides the existing SessionStart registration; hooks.json must
    still route session-start.sh there (the guard's wiring is asserted in
    test_tracking_guard.py)."""
    wiring = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())
    session_start = json.dumps(wiring["hooks"]["SessionStart"])
    assert "session-start.sh" in session_start


def test_session_start_carries_hostile_cwd_as_data(tmp_path):
    """The shell wrapper must preserve path bytes without evaluating them.

    A NUL-delimited parse is intentional here: whitespace delimiters corrupt a
    newline or tab, and sourcing/eval would execute the command substitutions.
    """
    fake_plugin = tmp_path / "plugin"
    hooks = fake_plugin / "hooks"
    hooks.mkdir(parents=True)
    (hooks / "telemetry.py").write_text("", encoding="utf-8")
    (hooks / "version_check.py").write_text(
        "import json, os\n"
        "print(json.dumps({k: os.environ.get(k) for k in "
        "('PROBE_SESSION_SOURCE', 'PROBE_SESSION_ID', 'PROBE_SESSION_CWD')}))\n",
        encoding="utf-8",
    )
    cwd = str(tmp_path / "repo with spaces\tand-newline\n'\"$(`touch PWNED`) `${IFS}`")
    payload = {"source": "startup", "session_id": SESSION_ID, "cwd": cwd}
    env = os.environ.copy()
    env.update(
        {
            "PLUGIN_ROOT": str(fake_plugin),
            "HOME": str(tmp_path / "home"),
            "PATH": os.environ.get("PATH", ""),
        }
    )

    result = subprocess.run(
        ["bash", str(PLUGIN / "hooks" / "session-start.sh")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
        cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "PROBE_SESSION_SOURCE": "startup",
        "PROBE_SESSION_ID": SESSION_ID,
        "PROBE_SESSION_CWD": cwd,
    }
    assert not (tmp_path / "PWNED").exists()
