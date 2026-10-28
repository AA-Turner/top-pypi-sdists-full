"""Probe's traces in every coding agent, found and removed with or without the agent's binary (U-T1, U-T7).

Every test runs in the suite's isolated HOME with the agent homes moved into
it. `claude` and `codex` are the suite's loud stubs (exit 97) unless a test
takes them off PATH: the file edits must do the whole job either way, and
remove ONLY Probe's entries.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from probe.cli import uninstall_agents
from probe.harness import get_registry


@pytest.fixture
def homes(tmp_path, monkeypatch):
    home = Path(os.environ["HOME"])
    monkeypatch.setenv("CODEX_HOME", str(home / ".codex"))
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(home / ".pi" / "agent"))
    monkeypatch.setenv("KIMI_CODE_HOME", str(home / ".kimi-code"))
    return home


def _agent(agent_id: str):
    return get_registry().get(agent_id)


def _no_binaries(monkeypatch):
    monkeypatch.setenv("PATH", "/usr/bin:/bin")


CODEX_CONFIG = """model = "gpt-5"

[plugins."probe-research@research-os-agent"]
enabled = true

[plugins."other@else"]
enabled = true

[marketplaces.research-os-agent]
source = "github"

[mcp_servers.probe-research]
url = "https://mcp.research.prbe.ai/mcp"

[mcp_servers.probe-research.http_headers]
Authorization = "Bearer x"

[mcp_servers.other]
url = "https://other"

[hooks.state."probe-research-tap@research-os-agent:hooks/hooks.json:Stop:0"]
trusted = "a"

[hooks.state."someone-else@x:hooks.json:Stop:0"]
trusted = "b"

[[profiles.list]]
name = "p"
"""


def test_codex_tables_are_found_by_key_and_only_probes_go(homes, monkeypatch):
    from probe._compat import tomllib

    _no_binaries(monkeypatch)
    config = homes / ".codex" / "config.toml"
    config.parent.mkdir(parents=True)
    config.write_text(CODEX_CONFIG)
    found = uninstall_agents.traces(_agent("codex"))
    assert found["plugins"] == ["probe-research@research-os-agent"]
    assert found["mcp"] and found["hook_approvals"] and found["marketplace"]
    uninstall_agents.remove(_agent("codex"))
    left = tomllib.loads(config.read_text())
    assert left["model"] == "gpt-5"
    assert set(left["plugins"]) == {"other@else"}
    assert set(left["mcp_servers"]) == {"other"}
    assert set(left["hooks"]["state"]) == {"someone-else@x:hooks.json:Stop:0"}
    assert "marketplaces" not in left and left["profiles"]["list"][0]["name"] == "p"
    assert uninstall_agents.traces(_agent("codex")) == {}


def test_claude_records_go_by_file_edit_when_claude_is_not_installed(homes, monkeypatch):
    _no_binaries(monkeypatch)
    plugins = homes / ".claude" / "plugins"
    (plugins / "marketplaces" / "research-os-agent").mkdir(parents=True)
    (plugins / "cache" / "research-os-agent" / "probe-research").mkdir(parents=True)
    (plugins / "cache" / "else" / "other").mkdir(parents=True)
    retired = plugins / "cache" / "prbe-ai" / "prbe-cc-tap-plugin" / "0.1"
    retired.mkdir(parents=True)
    (plugins / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {
        "probe-research-daemon@research-os-agent": [{"installPath": "x"}],
        "prbe-cc-tap-plugin@prbe-ai": [{"installPath": str(retired)}],
        "other@else": [{"installPath": "y"}],
    }}))
    (plugins / "known_marketplaces.json").write_text(json.dumps({"research-os-agent": {}, "else": {}}))
    found = uninstall_agents.traces(_agent("claude_code"))
    assert set(found["plugins"]) == {"probe-research-daemon@research-os-agent", "prbe-cc-tap-plugin@prbe-ai"}
    uninstall_agents.remove(_agent("claude_code"))
    ledger = json.loads((plugins / "installed_plugins.json").read_text())
    assert set(ledger["plugins"]) == {"other@else"}
    assert set(json.loads((plugins / "known_marketplaces.json").read_text())) == {"else"}
    assert not (plugins / "marketplaces").exists() and not (plugins / "cache" / "research-os-agent").exists()
    assert not retired.exists() and (plugins / "cache" / "else" / "other").is_dir()
    assert uninstall_agents.traces(_agent("claude_code")) == {}


def test_kimi_records_and_copies_go_and_nothing_is_made_for_an_agent_without_them(homes):
    from probe.cli import kimi_config

    uninstall_agents.remove(_agent("kimi_code"))
    assert not (homes / ".kimi-code").exists()  # no plugins folder, no lock file made
    managed = kimi_config.managed_root()
    (managed / "probe-research@1.0").mkdir(parents=True)
    (managed / "someone-else").mkdir()
    kimi_config.installed_path().write_text(json.dumps({"version": 1, "plugins": [
        {"id": "probe-research", "root": str(managed / "probe-research@1.0")},
        {"id": "someone-else", "root": str(managed / "someone-else")},
    ]}))
    assert uninstall_agents.traces(_agent("kimi_code"))["plugins"] == ["probe-research"]
    uninstall_agents.remove(_agent("kimi_code"))
    records = json.loads(kimi_config.installed_path().read_text())["plugins"]
    assert [p["id"] for p in records] == ["someone-else"]
    assert not (managed / "probe-research@1.0").exists() and (managed / "someone-else").is_dir()
    assert not (managed.parent / ".probe-installed.lock").exists()


def test_pi_entry_and_its_clone_go(homes, monkeypatch):
    from probe.cli import pi_config

    _no_binaries(monkeypatch)
    agent_dir = homes / ".pi" / "agent"
    clone = agent_dir / "git" / "github.com" / "prbe-ai" / "research-os-agent"
    clone.mkdir(parents=True)
    (agent_dir / "git" / "github.com" / "someone" / "pkg").mkdir(parents=True)
    pi_config.settings_path().write_text(json.dumps(
        {"theme": "dark", "packages": [pi_config.MIRROR_GIT_SOURCE, "npm:other"]}))
    found = uninstall_agents.traces(_agent("pi"))
    assert found["plugins"] and found["plugin_copies"]
    uninstall_agents.remove(_agent("pi"))
    settings = json.loads(pi_config.settings_path().read_text())
    assert settings["packages"] == ["npm:other"] and settings["theme"] == "dark"
    assert not clone.exists() and not (agent_dir / "git" / "github.com" / "prbe-ai").exists()
    assert (agent_dir / "git" / "github.com" / "someone" / "pkg").is_dir()


def test_rules_skills_and_status_line_go_and_what_they_wrapped_comes_back(homes):
    from probe.cli import agent_rules, statusline

    claude = homes / ".claude"
    (claude / "skills" / "mine").mkdir(parents=True)
    (claude / "skills" / "probe").mkdir()
    (claude / "skills" / "probe" / ".probe-installed").write_text("probe-research\n")
    (claude / "CLAUDE.md").write_text("# mine\n")
    agent_rules.install(claude / "CLAUDE.md")
    (claude / "settings.json").write_text(json.dumps({"statusLine": {"type": "command", "command": "mine"}}))
    (claude / "settings.json.probe-backup").write_text("{}")
    command = statusline.chain("mine", statusline.renderer_command("/usr/bin/python3"))
    (claude / "settings.json").write_text(json.dumps({"statusLine": {"type": "command", "command": command}}))
    found = uninstall_agents.traces(_agent("claude_code"))
    assert {"rules", "skills", "statusline"} <= set(found)
    uninstall_agents.remove(_agent("claude_code"))
    assert (claude / "CLAUDE.md").read_text() == "# mine\n"
    assert json.loads((claude / "settings.json").read_text())["statusLine"]["command"] == "mine"
    assert not (claude / "settings.json.probe-backup").exists()
    assert not (claude / "skills" / "probe").exists() and (claude / "skills" / "mine").is_dir()


def test_a_rules_file_goes_only_when_probes_block_was_all_it_held(homes):
    from probe.cli import agent_rules

    claude = homes / ".claude"
    claude.mkdir()
    (claude / "CLAUDE.md").write_text("")  # the person's, empty before Probe
    uninstall_agents.remove(_agent("claude_code"))
    assert (claude / "CLAUDE.md").exists()
    agent_rules.install(claude / "CLAUDE.md")
    uninstall_agents.remove(_agent("claude_code"))
    assert not (claude / "CLAUDE.md").exists()  # only Probe's block was in it


def test_a_status_line_that_cannot_be_restored_keeps_its_backup_and_renderer(homes, monkeypatch):
    from probe.cli import statusline

    claude = homes / ".claude"
    (claude / statusline.INSTALL_DIRNAME).mkdir(parents=True)
    command = statusline.chain("mine", statusline.renderer_command("/usr/bin/python3"))
    (claude / "settings.json").write_text(json.dumps({"statusLine": {"type": "command", "command": command}}))
    (claude / "settings.json.probe-backup").write_text('{"statusLine": {"command": "mine"}}')

    def refuse(source):
        raise ValueError("an unusual layout")

    monkeypatch.setattr(statusline, "uninstall_for", refuse)
    lines = uninstall_agents.remove(_agent("claude_code"))
    assert any("left the status line" in line for line in lines)
    assert (claude / "settings.json.probe-backup").exists()
    assert (claude / statusline.INSTALL_DIRNAME).is_dir()
    assert "statusline" in uninstall_agents.traces(_agent("claude_code"))


def test_a_settings_file_probe_made_alone_goes_with_it(homes):
    from probe.cli import statusline

    claude = homes / ".claude"
    claude.mkdir()
    command = statusline.renderer_command("/usr/bin/python3")
    (claude / "settings.json").write_text(json.dumps({"statusLine": {"type": "command", "command": command}}))
    uninstall_agents.remove(_agent("claude_code"))
    assert not (claude / "settings.json").exists()


def test_turning_capture_off_for_removal_makes_no_tap_folder(homes, monkeypatch):
    from probe.cli import capture
    from probe.cli.capabilities import agent_target, tap_plugin_dir

    with agent_target("codex"):
        assert capture._set_killswitch(create=False) is True
        capture._append_stop_log({"ts": 0})
        assert not tap_plugin_dir().exists()
        tap_plugin_dir().mkdir(parents=True)
        assert capture._set_killswitch(create=False) is True
        assert (tap_plugin_dir() / ".disabled").exists()
