"""The daemon profile's lean plugin, `probe-research-daemon` (daemon reads, T7).

In the daemon profile the coding agent gets ONLY the blurb and the team note
(its instruction file), the `instrument-code` skill, the reads hooks (messages +
the Stop wake), the daemon's approval questions and the guard. Claude Code lists
every skill of an installed plugin and loads its MCP at connect, so what must
not reach the agent must not be in the plugin at all -- these tests hold the
plugin's CONTENTS to that, and its hooks to being the full plugin's own files.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "plugins" / "probe-research"
LEAN = ROOT / "plugins" / "probe-research-daemon"
PROFILE_EXPORT = "export PROBE_PLUGIN_PROFILE=daemon; "


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _hooks(plugin: Path) -> dict:
    return _json(plugin / "hooks" / "hooks.json")["hooks"]


def _commands(hooks: dict):
    for event, entries in hooks.items():
        for entry in entries:
            for hook in entry["hooks"]:
                yield event, entry.get("matcher"), hook


def _scripts(command: str) -> set[str]:
    return set(re.findall(r"hooks/([A-Za-z_.-]+\.(?:py|sh))", command))


def _makefile_list() -> list[str]:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^DAEMON_PLUGIN_HOOKS := (.*?)(?<!\\)$", text, re.MULTILINE | re.DOTALL)
    assert match, "Makefile has no DAEMON_PLUGIN_HOOKS"
    return match.group(1).replace("\\\n", " ").split()


# ---------------------------------------------------------------------------
# What is in it, and what is not.
# ---------------------------------------------------------------------------


def test_the_skills_are_instrument_code_and_the_switch_and_instrument_code_is_the_canonical_copy():
    skills = {path.parent.name for path in (LEAN / "skills").glob("*/SKILL.md")}
    # `probe` is the on / read / off switch (Richard 2026-09-29), hand-kept here.
    assert skills == {"instrument-code", "probe"}, "no track-work (or any other skill): Claude Code lists it to the agent"
    canonical = ROOT / "skills" / "instrument-code"
    shipped = LEAN / "skills" / "instrument-code"
    names = sorted(p.relative_to(canonical) for p in canonical.rglob("*") if p.is_file())
    assert names == sorted(p.relative_to(shipped) for p in shipped.rglob("*") if p.is_file())
    for rel in names:
        assert (canonical / rel).read_bytes() == (shipped / rel).read_bytes(), f"{rel} drifted: make sync-daemon-plugin"


def test_no_mcp_no_commands_no_setup():
    assert not (LEAN / ".mcp.json").exists()
    assert not (LEAN / "bin").exists(), "bin/probe-mcp-headers belongs to the MCP"
    assert not (LEAN / "commands").exists(), "the setup command is not installed in the daemon profile"
    for manifest in (LEAN / ".claude-plugin" / "plugin.json", LEAN / ".codex-plugin" / "plugin.json"):
        body = _json(manifest)
        assert "mcpServers" not in body and "commands" not in body
        assert body["name"] == "probe-research-daemon"


def test_the_manifests():
    claude = _json(LEAN / ".claude-plugin" / "plugin.json")
    assert claude["hooks"] == "./hooks/claude-reads.json", "the Stop wake (asyncRewake) lives only there"
    assert (LEAN / "hooks" / "claude-reads.json").is_file()
    codex = _json(LEAN / ".codex-plugin" / "plugin.json")
    assert codex["skills"] == "./skills/"
    assert "hooks" not in codex, "Codex discovers hooks/hooks.json itself; declaring it runs every hook twice"
    full = _json(FULL / ".claude-plugin" / "plugin.json")
    assert claude["version"] == codex["version"] == full["version"]


def test_hook_files_are_byte_identical_copies_of_the_full_plugins():
    listed = _makefile_list()
    shipped = sorted(p.name for p in (LEAN / "hooks").iterdir() if p.is_file() and p.name != "hooks.json")
    assert shipped == sorted(listed), "hooks/ holds exactly the files `make sync-daemon-plugin` copies"
    assert "note_audit.py" not in listed, "the team-note audit reminder needs Probe reads: not wired"
    for name in listed:
        lean, full = LEAN / "hooks" / name, FULL / "hooks" / name
        assert lean.read_bytes() == full.read_bytes(), f"hooks/{name} drifted: make sync-daemon-plugin"
        assert (lean.stat().st_mode & 0o111) == (full.stat().st_mode & 0o111), f"hooks/{name} lost its exec bit"


# ---------------------------------------------------------------------------
# hooks.json: the full plugin's wrappers, minus what the daemon profile drops.
# ---------------------------------------------------------------------------


def test_every_hook_is_a_full_plugin_wrapper_and_names_a_shipped_file():
    full_commands = {hook["command"] for _e, _m, hook in _commands(_hooks(FULL))}
    for event, _matcher, hook in _commands(_hooks(LEAN)):
        command = hook["command"]
        reused = command.replace(PROFILE_EXPORT, "", 1)
        assert reused in full_commands, f"{event}: not one of the full plugin's wrappers"
        for script in _scripts(command):
            assert (LEAN / "hooks" / script).is_file(), f"{event} runs hooks/{script}, which is not shipped"


def test_the_guard_and_session_start_run_in_the_daemon_profile():
    seen = set()
    for event, matcher, hook in _commands(_hooks(LEAN)):
        scripts = _scripts(hook["command"])
        profiled = hook["command"].startswith("/bin/bash -c '" + PROFILE_EXPORT)
        if scripts & {"tracking_guard.py", "session-start.sh"}:
            assert profiled, f"{event} {matcher}: {scripts} must run with PROBE_PLUGIN_PROFILE=daemon"
            seen.add((event, matcher, *sorted(scripts)))
        else:
            assert not profiled, f"{event}: only the guard and session start need the profile"
    assert seen == {
        ("SessionStart", None, "session-start.sh"),
        ("PreCompact", None, "session-start.sh"),
        ("PreToolUse", "^Bash$|probe[-_]research", "tracking_guard.py"),
        ("PreToolUse", "^(Write|Edit|MultiEdit|NotebookEdit)$", "tracking_guard.py"),
        # The switch: a typed `/probe on|read|off` and the Skill tool (Richard 2026-09-29).
        ("UserPromptSubmit", None, "tracking_guard.py"),
        ("PostToolUse", "^(Bash|Skill|SlashCommand)$|probe[-_]research", "tracking_guard.py"),
    }, "the guard: the refusal before a call, and the on / read / off switch"


def test_what_the_daemon_profile_keeps_and_drops():
    by_event: dict[str, set[str]] = {}
    for event, _matcher, hook in _commands(_hooks(LEAN)):
        by_event.setdefault(event, set()).update(_scripts(hook["command"]))
    assert by_event == {
        "UserPromptSubmit": {"tracking_guard.py", "statusline_refresh.py", "approvals_hook.py", "reads_hook.py"},
        "SessionStart": {"session-start.sh", "statusline_refresh.py", "approvals_hook.py"},
        "PreCompact": {"session-start.sh"},
        "PreToolUse": {"tracking_guard.py", "approvals_hook.py"},
        "PostToolUse": {"telemetry.py", "tracking_guard.py", "statusline_refresh.py", "approvals_hook.py",
                        "reads_hook.py"},
        "SessionEnd": {"telemetry.py", "team-note-sync.sh"},
        "Stop": {"statusline_notify.py", "team-note-sync.sh"},
    }


def test_marketplaces_list_it():
    claude = {p["name"]: p for p in _json(ROOT / ".claude-plugin" / "marketplace.json")["plugins"]}
    assert claude["probe-research-daemon"]["source"] == "./plugins/probe-research-daemon"
    codex = {p["name"]: p for p in _json(ROOT / ".agents" / "plugins" / "marketplace.json")["plugins"]}
    assert codex["probe-research-daemon"]["source"] == {"source": "local", "path": "./plugins/probe-research-daemon"}


# ---------------------------------------------------------------------------
# version_check in the daemon profile: nothing for the agent.
# ---------------------------------------------------------------------------


def _load_version_check(plugin: Path):
    path = plugin / "hooks" / "version_check.py"
    spec = importlib.util.spec_from_file_location("_daemon_profile_version_check", path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(path.parent))
    module._team_note_cli_too_old = lambda _binary: None
    return module


def _emitted(capsys, call) -> dict:
    with pytest.raises(SystemExit):
        call()
    return json.loads(capsys.readouterr().out)


@pytest.fixture
def hook(monkeypatch):
    module = _load_version_check(LEAN)
    spawned: list[str] = []
    monkeypatch.setattr(module, "_spawn_session_maintenance", lambda: spawned.append("x") or None)
    monkeypatch.setattr(module, "_spawn_autoupdate", lambda _bin: None)
    monkeypatch.setattr(module, "_outbox_dead_letters", lambda: 0)
    monkeypatch.setattr(module, "_render_failures", lambda: [])
    monkeypatch.setattr(module, "_parked_copies", lambda: [])
    monkeypatch.delenv(module.HOOK_EVENT_ENV, raising=False)
    monkeypatch.setenv(module.SESSION_SOURCE_ENV, module.COMPACT_SOURCE)
    monkeypatch.setenv(module.SESSION_ID_ENV, "11111111-2222-3333-4444-555555555555")
    module.spawned = spawned
    return module


def test_the_update_nudge_reaches_the_researcher_only(hook, monkeypatch, capsys):
    monkeypatch.setenv(hook.PROFILE_ENV, hook.PROFILE_DAEMON)
    monkeypatch.setattr(
        hook.version_policy, "read_cache", lambda *a, **k: ({"cli": {"latest": "9.0.0", "min": "0.0.1"}}, 2**31, True)
    )
    monkeypatch.setattr(hook, "_local_cli", lambda _bin: "1.0.0")
    monkeypatch.setattr(hook, "_local_plugin", lambda _json: None)
    monkeypatch.setattr(hook, "_local_tap", lambda: None)
    out = _emitted(capsys, hook.main)
    assert "hookSpecificOutput" not in out, "no additionalContext: not the update line, not the compact line"
    assert "update available" in out["systemMessage"]
    assert hook.spawned, "the maintenance (agent-rules refresh + notes sync) still runs"


def test_stuck_writes_go_to_the_researcher(hook, monkeypatch, capsys):
    monkeypatch.setenv(hook.PROFILE_ENV, hook.PROFILE_DAEMON)
    monkeypatch.setattr(hook, "_outbox_dead_letters", lambda: 3)
    out = _emitted(capsys, lambda: hook._final({"continue": True}))
    assert "hookSpecificOutput" not in out
    assert out["systemMessage"] == "Probe: 3 writes stuck in the outbox. Run `probe doctor`."


def test_the_agent_profile_is_unchanged(hook, monkeypatch, capsys):
    monkeypatch.delenv(hook.PROFILE_ENV, raising=False)
    out = _emitted(capsys, lambda: hook._final({"continue": True}))
    assert "reconcile Probe" in out["hookSpecificOutput"]["additionalContext"]


def test_a_daemon_profile_session_that_starts_on_starts_in_daemon(hook, monkeypatch):
    from probe.sdk import session_marker

    sid = "22222222-3333-4444-5555-666666666666"
    monkeypatch.setenv(hook.SESSION_ID_ENV, sid)
    monkeypatch.setenv(hook.PROFILE_ENV, hook.PROFILE_DAEMON)
    session_marker.write_default_state(session_marker.STATE_FULL)
    hook._seed_tracking_signal()
    assert session_marker.session_state(sid) == session_marker.STATE_DAEMON
    other = "33333333-4444-5555-6666-777777777777"
    monkeypatch.setenv(hook.SESSION_ID_ENV, other)
    session_marker.write_default_state(session_marker.STATE_READ_ONLY)
    hook._seed_tracking_signal()
    assert session_marker.session_state(other) == session_marker.STATE_READ_ONLY, "off stays off"


def test_the_lean_plugins_reads_commands_are_the_full_plugins():
    """The delivery fast path is one command in both plugins (the lean hooks.json
    is hand-kept, not synced): a fix to one must reach the other."""
    import json as _json

    root = Path(__file__).resolve().parents[1] / "plugins"

    def reads(name, event):
        hooks = _json.loads((root / name / "hooks" / "hooks.json").read_text())["hooks"]
        return [h["command"] for g in hooks.get(event, []) for h in g["hooks"] if "reads_hook.py" in h["command"]]

    for event in ("UserPromptSubmit", "PostToolUse"):
        assert reads("probe-research-daemon", event) == reads("probe-research", event), event
