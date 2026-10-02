"""The post-compaction reconcile nudge (SessionStart, source="compact").

A compacted session keeps only what was written down, and Michael's workflow
(prompts compacted five times) is exactly where mid-session decisions died.
PreCompact cannot carry the recovery instruction -- it has no additionalContext
channel and no agent turn runs before the summarizer -- so the nudge rides the
NEXT SessionStart, the one Claude Code fires with source="compact".

Three properties matter:

  1. source=compact on a SessionStart adds the reconcile context, whatever
     main() was otherwise going to say (up-to-date, no manifest, update nudge).
  2. An update nudge already occupying additionalContext is appended to,
     never clobbered.
  3. PreCompact stays silent even if a source leaks into its environment --
     the event guard wins, per the module's SessionStart-channel contract.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "probe-research"




def _load_hook():
    """Load version_check.py the way session-start.sh does (see the sibling
    test_precompact_version_hook.py for why the hooks dir must be on sys.path)."""
    path = PLUGIN / "hooks" / "version_check.py"
    spec = importlib.util.spec_from_file_location("_compact_nudge_under_test", path)
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
    # Neutralize the two probes that read the MACHINE rather than the test.
    # `_team_note_cli_too_old` shells out to whichever `probe` is installed and
    # `_team_note_unsynced` stats a real state directory, so leaving them live
    # makes every assertion here depend on the laptop it runs on -- green in CI,
    # red locally, for reasons that have nothing to do with the nudge. A test
    # that wants either behaviour sets it back on the returned module.
    module._team_note_cli_too_old = lambda _binary: None
    module._team_note_unsynced = lambda: False
    return module


def _emitted(capsys, call) -> dict:
    with pytest.raises(SystemExit) as exc:
        call()
    assert exc.value.code == 0
    return json.loads(capsys.readouterr().out)


def _drive_main(hook, monkeypatch, capsys, *, latest: str, local: str) -> dict:
    """Run main() end-to-end with a fresh cache and no network (the pattern
    test_precompact_version_hook.py established)."""
    monkeypatch.setattr(
        hook.version_policy,
        "read_cache",
        lambda *a, **k: ({"cli": {"latest": latest, "min": "0.0.1"}}, 2**31, True),
    )
    monkeypatch.setattr(hook, "_local_cli", lambda _bin: local)
    monkeypatch.setattr(hook, "_local_plugin", lambda _json: None)
    monkeypatch.setattr(hook, "_local_tap", lambda: None)
    monkeypatch.setattr(hook, "_spawn_autoupdate", lambda _bin: None)
    return _emitted(capsys, hook.main)


def test_compact_start_adds_the_reconcile_context(monkeypatch, capsys) -> None:
    hook = _load_hook()
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, hook.COMPACT_SOURCE)

    out = _emitted(capsys, lambda: hook._final({"continue": True}))
    hso = out["hookSpecificOutput"]
    assert hso["hookEventName"] == "SessionStart"
    assert "reconcile Probe" in hso["additionalContext"]
    assert "track-work" in hso["additionalContext"]


def test_main_up_to_date_exit_still_carries_the_nudge(monkeypatch, capsys) -> None:
    """The common case: nothing to update, session compacted. This drives
    main() itself, so a merge-resolution that reverts a `_final(` back to
    `_emit(` on any exit path goes red here, not silently dead in production."""
    hook = _load_hook()
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, hook.COMPACT_SOURCE)

    out = _drive_main(hook, monkeypatch, capsys, latest="0.1.0", local="0.1.0")
    assert out.get("continue") is True
    assert "reconcile Probe" in out["hookSpecificOutput"]["additionalContext"]


def test_main_stale_install_appends_nudge_to_the_update_context(monkeypatch, capsys) -> None:
    hook = _load_hook()
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, hook.COMPACT_SOURCE)

    out = _drive_main(hook, monkeypatch, capsys, latest="99.9.9", local="0.1.0")
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert ctx.startswith("The Probe Research client is out of date")
    assert "reconcile Probe" in ctx
    assert "systemMessage" in out


def test_update_nudge_is_appended_to_not_clobbered(monkeypatch, capsys) -> None:
    hook = _load_hook()
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, hook.COMPACT_SOURCE)

    payload = {
        "systemMessage": "update available",
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "The Probe Research client is out of date.",
        },
    }
    out = _emitted(capsys, lambda: hook._final(payload))
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert ctx.startswith("The Probe Research client is out of date.")
    assert "reconcile Probe" in ctx
    assert out["systemMessage"] == "update available"


def test_precompact_event_stays_silent_even_with_a_compact_source(monkeypatch, capsys) -> None:
    hook = _load_hook()
    monkeypatch.setenv(hook.HOOK_EVENT_ENV, hook.PRECOMPACT)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, hook.COMPACT_SOURCE)

    out = _emitted(capsys, lambda: hook._final({"continue": True}))
    assert out == {"continue": True}


def test_ordinary_startup_is_untouched(monkeypatch, capsys) -> None:
    hook = _load_hook()
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, "startup")

    out = _emitted(capsys, lambda: hook._final({"continue": True}))
    assert out == {"continue": True}


def test_an_unset_source_is_untouched(monkeypatch, capsys) -> None:
    """Direct invocation without the shell wrapper: no env var at all."""
    hook = _load_hook()
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.delenv(hook.SESSION_SOURCE_ENV, raising=False)

    out = _emitted(capsys, lambda: hook._final({"continue": True}))
    assert out == {"continue": True}


def test_an_empty_source_is_untouched(monkeypatch, capsys) -> None:
    """The exact value session-start.sh exports on a PreCompact run and on an
    unparseable payload — its fail-open contract must read as 'no nudge'."""
    hook = _load_hook()
    monkeypatch.delenv(hook.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(hook.SESSION_SOURCE_ENV, "")

    out = _emitted(capsys, lambda: hook._final({"continue": True}))
    assert out == {"continue": True}


def test_session_start_sh_actually_sets_the_source() -> None:
    """version_check.py only READS the env var; only session-start.sh sets it.
    Deleting the parse block would leave every test green while the nudge is
    dead in production — the wiring itself must be pinned (same idiom as the
    hooks.json assertion in test_precompact_version_hook.py)."""
    sh = (PLUGIN / "hooks" / "session-start.sh").read_text(encoding="utf-8")
    assert "export PROBE_SESSION_SOURCE" in sh
    assert '.get("source")' in sh, "the parse must pull SessionStart stdin `source`"
    assert '"precompact"' in sh, "the parse must skip the PreCompact path"
