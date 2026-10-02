"""Static release gates for the Codex plugin surfaces."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from probe.cli import plugin_cli


ROOT = Path(__file__).resolve().parents[1]


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _base_version(value: str) -> str:
    return value.split("+", 1)[0]


def test_tracking_plugin_uses_native_oauth_mcp() -> None:
    manifest = _json(ROOT / "plugins/probe-research/.codex-plugin/plugin.json")
    server = manifest["mcpServers"]["probe-research"]
    assert server == {
        "url": "https://mcp.research.prbe.ai/mcp",
        "auth": "oauth",
        "required": False,
    }
    assert manifest["skills"] == "./skills/"
    hooks = _json(ROOT / "plugins/probe-research/hooks/hooks.json")["hooks"]
    command = hooks["SessionStart"][0]["hooks"][0]["command"]
    assert "PROBE_AGENT=codex" in command
    assert "PLUGIN_ROOT" in command


def test_repo_marketplace_exposes_tracking_and_capture() -> None:
    marketplace = _json(ROOT / ".agents/plugins/marketplace.json")
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert set(entries) == {"probe-research", "probe-research-daemon", "probe-research-tap"}
    for entry in entries.values():
        assert entry["source"]["source"] == "local"
        assert entry["policy"]["installation"] == "AVAILABLE"
        assert entry["policy"]["authentication"] in {"ON_INSTALL", "ON_USE"}
        assert entry["category"]


def test_capture_plugin_has_codex_manifest_and_hooks() -> None:
    root = ROOT / "plugins/probe-research-tap"
    manifest = _json(root / ".codex-plugin/plugin.json")
    hooks = _json(root / "hooks/hooks.json")["hooks"]
    assert manifest["name"] == "probe-research-tap"
    # One hooks.json backs BOTH manifests -- neither declares hooks, both
    # plugin systems auto-discover this file -- so anything added for Claude
    # Code is also what Codex is handed. UserPromptSubmit is the respawn hook
    # (hooks/ensure-daemon.sh), which needs no Codex-specific code: it exits 0
    # without spawning when the payload carries no `session_id`. Stop is the
    # daemon's turn-end signal (hooks/turn-end.sh): silent, and a no-op outside
    # the `daemon` state or without a transcript path. Codex runs it once the
    # researcher approves the new entry (Codex trusts hooks entry by entry).
    assert set(hooks) == {"SessionStart", "UserPromptSubmit", "SessionEnd", "Stop"}
    assert "ensure-daemon.sh" in hooks["UserPromptSubmit"][0]["hooks"][0]["command"]
    assert "turn-end.sh" in hooks["Stop"][0]["hooks"][0]["command"]


def test_both_plugins_are_single_source_dual_target_packages() -> None:
    for name in ("probe-research", "probe-research-daemon", "probe-research-tap"):
        root = ROOT / "plugins" / name
        claude_manifest = _json(root / ".claude-plugin/plugin.json")
        codex_manifest = _json(root / ".codex-plugin/plugin.json")
        assert claude_manifest["name"] == codex_manifest["name"] == name
        assert _base_version(claude_manifest["version"]) == _base_version(codex_manifest["version"])


def test_tracking_skills_are_one_shared_tree() -> None:
    """Both agents read the SAME skills/ directory in this plugin."""
    root = ROOT / "plugins/probe-research"
    assert {path.parent.name for path in (root / "skills").glob("*/SKILL.md")} == {
        "probe",
        "track-work",
        "visualize-progress",
        "instrument-code",
        "audit-team-note",
        "edit-notes",
        "notes-audit",
    }
    assert not (ROOT / "plugins/prbe-codex-tap-plugin").exists()


def test_plugin_cli_contains_the_only_agent_verb_translation(monkeypatch) -> None:
    calls: list[tuple[str, list[str]]] = []

    def fake_run(source: str, args: list[str], *, timeout: float):
        calls.append((source, args))
        return plugin_cli.claude_cli.Result(ok=True)

    monkeypatch.setattr(plugin_cli, "run", fake_run)
    plugin_cli.refresh_marketplace(plugin_cli.CLAUDE, "research-os-agent")
    plugin_cli.refresh_marketplace(plugin_cli.CODEX, "research-os-agent")
    plugin_cli.install(plugin_cli.CLAUDE, "probe-research@research-os-agent")
    plugin_cli.install(plugin_cli.CODEX, "probe-research@research-os-agent")

    assert calls == [
        ("claude_code", ["plugin", "marketplace", "update", "research-os-agent"]),
        ("codex", ["plugin", "marketplace", "upgrade", "research-os-agent"]),
        ("claude_code", ["plugin", "install", "probe-research@research-os-agent"]),
        ("codex", ["plugin", "add", "probe-research@research-os-agent"]),
    ]


def test_codex_plugin_cli_closes_stdin(monkeypatch) -> None:
    observed: dict = {}

    def fake_subprocess_run(command, **kwargs):
        observed.update(kwargs)
        return subprocess.CompletedProcess(command, 0, stdout="{}", stderr="")

    monkeypatch.setattr(plugin_cli.shutil, "which", lambda _name: "/usr/bin/codex")
    monkeypatch.setattr(plugin_cli.subprocess, "run", fake_subprocess_run)

    result = plugin_cli.run("codex", ["plugin", "list", "--json"], timeout=1)

    assert result.ok is True
    assert observed["stdin"] is subprocess.DEVNULL


def test_codex_mcp_auth_status_selects_the_named_server(monkeypatch) -> None:
    payload = json.dumps(
        [
            {"name": "PRBE", "auth_status": "o_auth"},
            {"name": "probe-research", "auth_status": "not_logged_in"},
        ]
    )
    monkeypatch.setattr(
        plugin_cli,
        "run",
        lambda *_args, **_kwargs: plugin_cli.claude_cli.Result(ok=True, detail=payload),
    )
    assert plugin_cli.codex_mcp_auth_status("probe-research") == "not_logged_in"


def test_shared_hooks_json_carries_no_harness_specific_keys() -> None:
    """ONE hooks.json is read by BOTH harnesses, so a key only one of them knows
    is a warning printed at every session start of the other.

    `additionalContextLimit` was such a key: Codex honours it, Claude Code has
    never had it, and once Claude Code started validating hook config it began
    announcing `unknown key "additionalContextLimit" ... ignored` on every
    startup. Splitting the file is not the escape hatch -- Codex SUPPLEMENTS
    manifest-declared hooks on top of its default discovery of
    `hooks/hooks.json` rather than replacing it ("loading hooks from both ...;
    prefer a single representation for this layer"), so a second file runs every
    hook twice.

    The shape below is what both harnesses agree on. Anything outside it belongs
    in the hook's own code, where it can read which harness it is running under.
    """
    shared = {"matcher", "hooks"}
    # `statusMessage` stays: it is in Claude Code's own hooks example AND in
    # Codex's hook config, which is exactly the bar a key has to clear here.
    per_hook = {"type", "command", "timeout", "statusMessage"}
    for name in ("probe-research", "probe-research-daemon", "probe-research-tap"):
        hooks = _json(ROOT / "plugins" / name / "hooks/hooks.json")["hooks"]
        for event, entries in hooks.items():
            for entry in entries:
                extra = set(entry) - shared
                assert not extra, f"{name} {event}: harness-specific key(s) {sorted(extra)}"
                for hook in entry["hooks"]:
                    extra = set(hook) - per_hook
                    assert not extra, f"{name} {event}: harness-specific key(s) {sorted(extra)}"
