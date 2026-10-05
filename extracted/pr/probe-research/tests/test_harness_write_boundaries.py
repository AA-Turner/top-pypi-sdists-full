"""Where a wrong harness default did real damage, it is now a registry lookup,
and an unknown harness is refused by name.

Each test is a bug the harness audit (2026-10-02) found: a `"codex" if ...
else "claude_code"` (or the reverse) that quietly did one agent's work for
another. The registry rows decide now.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"


def _hook(name: str):
    spec = importlib.util.spec_from_file_location(f"_boundary_{name}", HOOKS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_pis_manual_steps_are_pis_not_claude_codes():
    """"Set it up manually" for pi printed `claude plugin marketplace add ...`."""
    from probe.cli import actions, pi_config

    text = actions.manual_steps(base_url="https://api.test", agent_source="pi")
    assert f"pi install {pi_config.MIRROR_GIT_SOURCE}" in text
    assert "claude plugin" not in text
    assert "codex plugin" not in text


def test_manual_steps_for_every_agent_name_each_ones_own_commands():
    from probe.cli import actions

    text = actions.manual_steps(base_url="https://api.test", agent_source=("claude_code", "codex", "pi"))
    assert "claude plugin install" in text
    assert "codex plugin add" in text
    assert "pi install git:" in text
    assert "codex mcp login probe-research" in text


def test_instruction_files_name_pis_file_too():
    from probe.cli import setup

    assert setup.instruction_files(("pi",)) == "AGENTS.md"
    assert setup.instruction_files(("claude_code", "codex", "pi")) == "CLAUDE.md + AGENTS.md"


def test_a_pi_run_never_writes_claude_codes_status_line(tmp_path, monkeypatch):
    """`apply_agent_rules` installed Claude Code's status line on every run."""
    from probe.cli import setup

    calls = []
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi"))
    monkeypatch.setattr(setup, "apply_statusline", lambda: calls.append(1) or ["status line"])
    setup.apply_agent_rules(True)
    assert calls == []

    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    setup.apply_agent_rules(True)
    assert calls == [1]


def test_the_plugin_cli_refuses_an_agent_with_no_marketplace():
    """`run` sent every non-Codex source to the `claude` binary."""
    from probe.cli import plugin_cli

    with pytest.raises(ValueError, match="pi"):
        plugin_cli.run("pi", ["plugin", "list"], timeout=1)
    with pytest.raises(ValueError):
        plugin_cli.install("cursor", "probe-research@research-os-agent")
    # Kimi Code has no plugin command at all: its installs go to kimi_config.
    with pytest.raises(ValueError, match="kimi_config"):
        plugin_cli.run("kimi_code", ["plugin", "list"], timeout=1)


def test_reasoning_settings_refuse_an_agent_without_one():
    """Every non-Claude source would have written Codex's config.toml."""
    from probe.cli import reasoning_summaries

    assert reasoning_summaries.SOURCES == ("claude_code", "codex")
    with pytest.raises(ValueError, match="pi"):
        reasoning_summaries.settings_path("pi")


def test_telemetry_reads_the_running_harnesss_tap_database(tmp_path, monkeypatch):
    """The team fallback read Claude Code's tap state.db under every harness."""
    import sqlite3

    pi_dir = tmp_path / "pi-tap"
    pi_dir.mkdir()
    conn = sqlite3.connect(pi_dir / "state.db")
    conn.execute("CREATE TABLE meta (k TEXT, v TEXT)")
    conn.execute("INSERT INTO meta VALUES ('customer_id', 'team-from-pi')")
    conn.commit()
    conn.close()
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(pi_dir))
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "claude-tap-empty"))

    assert _hook("telemetry")._tap_customer_id() == "team-from-pi"


def test_the_update_check_reads_the_running_harnesss_tap_version(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(HOOKS))  # version_check imports its siblings by name
    codex_dir = tmp_path / "codex-tap"
    codex_dir.mkdir()
    (codex_dir / ".installed_version").write_text("0.9.9\n")
    monkeypatch.setenv("PROBE_AGENT", "codex")
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(codex_dir))
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "claude-tap-empty"))

    assert _hook("version_check")._local_tap() == "0.9.9"


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({"PROBE_AGENT": "codex"}, "codex"),
        ({"PLUGIN_ROOT": "/x"}, "codex"),
        ({"CLAUDE_PLUGIN_ROOT": "/x", "PLUGIN_ROOT": "/y"}, "claude_code"),
        ({"CODEX_THREAD_ID": "t"}, "codex"),
        ({}, "claude_code"),
    ],
)
def test_the_hook_resolver_tells_the_harnesses_apart(env, expected):
    assert _hook("_hook_harness").current(env).id == expected


def test_the_hook_resolver_reads_a_session_id_for_any_harness():
    resolver = _hook("_hook_harness")
    assert resolver.session_id({"PROBE_AGENT": "pi", "PI_SESSION_ID": "s-pi"}) == "s-pi"
    assert resolver.session_id({"CODEX_THREAD_ID": "s-codex"}) == "s-codex"
    assert resolver.session_id({}) == ""


def test_the_daemon_plugin_ships_the_resolver_beside_its_hooks():
    daemon_hooks = AGENT / "plugins" / "probe-research-daemon" / "hooks"
    for name in ("_hook_harness.py", "_harness_registry.py", "harnesses.json"):
        assert (daemon_hooks / name).read_bytes() == (HOOKS / name).read_bytes(), name
    assert json.loads((daemon_hooks / "harnesses.json").read_text())["version"] == 1
