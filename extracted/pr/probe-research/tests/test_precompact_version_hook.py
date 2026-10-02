"""The PreCompact half of the plugin's version hook.

SessionStart fires once per session, which is the wrong cadence for the person
this tool is for: researchers keep a handful of sessions alive for weeks, and
their Probe work goes through the hosted MCP, which runs nothing on their
machine. PreCompact fires when a long session compacts -- so it reaches exactly
the laptops SessionStart misses, and nobody else.

Two properties matter more than the branches:

  1. PreCompact APPLIES. If it stopped spawning the upgrade it would be a hook
     that costs a process and achieves nothing.
  2. PreCompact is SILENT. The nudge payload is SessionStart's output contract,
     and a message injected mid-compaction interrupts work the user did not
     start to repeat something they already saw.

Both are asserted directly. The wiring in hooks.json is asserted too: the hook
cannot fire at all if the event is not registered, and no test of the module
would notice.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "probe-research"


def _load_hook():
    """Load version_check.py the way session-start.sh does.

    The hook's own directory must be on sys.path -- that is the only thing that
    makes its `import version_policy` resolve, because the system python3 it runs
    under has no probe package. Loading by path alone does not add it, so without
    this the test exercises a configuration that never ships.
    """
    path = PLUGIN / "hooks" / "version_check.py"
    spec = importlib.util.spec_from_file_location("_precompact_hook_under_test", path)
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
    return module


@pytest.fixture
def hook(tmp_path, monkeypatch):
    """The hook with an isolated cache/state and no network."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")
    monkeypatch.delenv("PROBE_HOOK_EVENT", raising=False)
    return _load_hook()


def _stale_install(hook, monkeypatch, spawns: list):
    """An install that is enabled, opted in, and behind the manifest."""
    monkeypatch.setattr(
        hook.version_policy,
        "read_cache",
        lambda *a, **k: ({"cli": {"latest": "99.9.9", "min": "0.0.1"}}, 2**31, True),
    )
    monkeypatch.setattr(hook, "_local_cli", lambda _bin: "0.1.0")
    monkeypatch.setattr(hook, "_local_plugin", lambda _json: None)
    monkeypatch.setattr(hook, "_local_tap", lambda: None)
    monkeypatch.setattr(hook, "_spawn_autoupdate", lambda _bin: spawns.append("apply"))


def _run(hook) -> dict:
    """Run main() and capture the JSON it emits before exiting."""
    with pytest.raises(SystemExit):
        hook.main()
    return json.loads(_run.captured)


def _capture(hook, monkeypatch):
    def _emit(obj):
        _run.captured = json.dumps(obj)
        raise SystemExit(0)

    monkeypatch.setattr(hook, "_emit", _emit)


# ---------------------------------------------------------------------------
# The two properties.
# ---------------------------------------------------------------------------


def test_precompact_still_applies_the_upgrade(hook, monkeypatch):
    """Property 1. A PreCompact that does not spawn is a hook that costs a
    process and achieves nothing -- which is the whole point of wiring it up."""
    spawns: list[str] = []
    _stale_install(hook, monkeypatch, spawns)
    _capture(hook, monkeypatch)
    monkeypatch.setenv("PROBE_HOOK_EVENT", "precompact")

    _run(hook)
    assert spawns == ["apply"]


def test_precompact_says_nothing(hook, monkeypatch):
    """Property 2. No systemMessage, no additionalContext -- a nudge here would
    interrupt mid-compaction to repeat what SessionStart already said, using an
    output contract that belongs to a different event."""
    spawns: list[str] = []
    _stale_install(hook, monkeypatch, spawns)
    _capture(hook, monkeypatch)
    monkeypatch.setenv("PROBE_HOOK_EVENT", "precompact")

    out = _run(hook)
    assert out == {"continue": True}


def test_session_start_is_unchanged(hook, monkeypatch):
    """The regression guard on the other half. PROBE_HOOK_EVENT is exported only
    for PreCompact, so an unset value must keep the old behaviour exactly --
    including for an OLD hooks.json shipped alongside a new copy of this file."""
    spawns: list[str] = []
    _stale_install(hook, monkeypatch, spawns)
    _capture(hook, monkeypatch)

    out = _run(hook)
    assert spawns == ["apply"], "SessionStart must still apply"
    assert "99.9.9" in out["systemMessage"]
    assert out["hookSpecificOutput"]["hookEventName"] == "SessionStart"


def test_an_unknown_hook_event_reads_as_session_start(hook, monkeypatch):
    """Forward compatibility: a future hooks.json naming a fourth event must not
    silently turn the nudge off. Only the exact PreCompact value suppresses it."""
    spawns: list[str] = []
    _stale_install(hook, monkeypatch, spawns)
    _capture(hook, monkeypatch)
    monkeypatch.setenv("PROBE_HOOK_EVENT", "somethingelse")

    out = _run(hook)
    assert "systemMessage" in out


def test_a_current_install_is_silent_on_precompact_too(hook, monkeypatch):
    """The common case, and the one that must stay free: nothing to do, nothing
    spawned, nothing said."""
    spawns: list[str] = []
    monkeypatch.setattr(
        hook.version_policy,
        "read_cache",
        lambda *a, **k: ({"cli": {"latest": "0.1.0", "min": "0.0.1"}}, 2**31, True),
    )
    monkeypatch.setattr(hook, "_local_cli", lambda _bin: "0.1.0")
    monkeypatch.setattr(hook, "_local_plugin", lambda _json: None)
    monkeypatch.setattr(hook, "_local_tap", lambda: None)
    monkeypatch.setattr(hook, "_spawn_autoupdate", lambda _bin: spawns.append("apply"))
    _capture(hook, monkeypatch)
    monkeypatch.setenv("PROBE_HOOK_EVENT", "precompact")

    out = _run(hook)
    assert out == {"continue": True}
    assert spawns == []


# ---------------------------------------------------------------------------
# WIRING. The module can be perfect and never run.
# ---------------------------------------------------------------------------


def test_hooks_json_registers_precompact():
    """MUTANT: drop the PreCompact block from hooks.json -> red.

    Claude Code only runs what is registered, so every test above passes against
    a plugin where this hook never fires.
    """
    hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())
    assert "PreCompact" in hooks["hooks"], "PreCompact must be registered to fire at all"
    assert "SessionStart" in hooks["hooks"], "and it must not have replaced SessionStart"


def test_precompact_exports_the_event_marker():
    """MUTANT: drop `export PROBE_HOOK_EVENT=precompact` -> red.

    Without the marker the PreCompact run is indistinguishable from a session
    start, so it would emit SessionStart's payload on the wrong event and inject
    a nudge mid-compaction.
    """
    hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())
    command = hooks["hooks"]["PreCompact"][0]["hooks"][0]["command"]
    assert "PROBE_HOOK_EVENT=precompact" in command
    assert "session-start.sh" in command, "both events share one script"

    session = hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    assert "PROBE_HOOK_EVENT" not in session, (
        "SessionStart must NOT export the marker -- unset is what preserves its behaviour"
    )


# ---------------------------------------------------------------------------
# The team-note reconcile: the second thing PreCompact applies.
# ---------------------------------------------------------------------------


def _capture_maintenance(hook, monkeypatch) -> list[str]:
    """Record the shell command `_spawn_session_maintenance` would have run."""
    commands: list[str] = []

    class _FakePopen:
        def __init__(self, argv, **_kw):
            commands.append(argv[-1])

    monkeypatch.setattr(hook.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(hook, "_team_note_cli_too_old", lambda _binary: None)
    monkeypatch.setenv("PROBE_BIN", "probe")
    return commands


def test_precompact_reconciles_the_team_note(hook, monkeypatch):
    """A session alive for weeks pushes on every `Stop`, but may not reach
    `SessionEnd` for weeks and cannot re-run its start hook. Compaction is the
    only recurring occasion it offers, so the reconcile has to happen here."""
    commands = _capture_maintenance(hook, monkeypatch)
    _capture(hook, monkeypatch)
    monkeypatch.setattr(hook, "_tracking_off", lambda: False)
    monkeypatch.setenv("PROBE_HOOK_EVENT", "precompact")

    _run(hook)
    assert any("notes sync" in c for c in commands), commands


def test_the_reconcile_ignores_the_tracking_toggle(hook, monkeypatch):
    """REGRESSION. This used to send `--pull-only` when tracking was off, so an
    untracked session's edits sat unsent until some later session pushed them --
    while the instruction block told the agent the file "syncs on its own".

    It was half a gate anyway: the `Stop` hook has never consulted the toggle and
    pushes every turn. The toggle governs what Probe records ABOUT THE WORK; the
    team note is the lab's shared document, not a record of this session.
    """
    for tracking_off in (True, False):
        commands = _capture_maintenance(hook, monkeypatch)
        _capture(hook, monkeypatch)
        monkeypatch.setattr(hook, "_tracking_off", lambda v=tracking_off: v)
        monkeypatch.delenv("PROBE_HOOK_EVENT", raising=False)

        _run(hook)
        sync = [c for c in commands if "notes sync" in c]
        assert sync, f"tracking_off={tracking_off}: no sync spawned"
        assert "--pull-only" not in sync[0], f"tracking_off={tracking_off}: {sync[0]}"


def test_a_too_old_cli_still_blocks_the_spawn_on_precompact(hook, monkeypatch):
    """The version floor is the one thing that must still stop the spawn: a CLI
    without `notes sync` fails silently, which is what the floor exists to catch.
    Its MESSAGE is still discarded on PreCompact -- that is the silence rule."""
    commands: list[str] = []

    class _FakePopen:
        def __init__(self, argv, **_kw):
            commands.append(argv[-1])

    monkeypatch.setattr(hook.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(hook, "_team_note_cli_too_old", lambda _binary: "upgrade me")
    _capture(hook, monkeypatch)
    monkeypatch.setenv("PROBE_HOOK_EVENT", "precompact")

    out = _run(hook)
    assert commands == []
    assert out == {"continue": True}, "the floor's message must not leak into a compaction"
