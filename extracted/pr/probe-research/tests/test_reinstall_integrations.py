"""Installed means usable, and one tap per agent (plan clean-uninstall-reinstall R-T5).

R6: a plugin record that read installed while unusable (its files gone,
disabled, a project-scope install) made configure say "Nothing to change".
R9: the retired `prbe-cc-tap-plugin` never removed (double capture), both
profile plugins together, the Codex `/hooks` approval line only on a fresh
capture install, pi's `extensions: []` never repaired, a Kimi record whose
files are gone. Every agent's folder is the test's own (conftest, and the
variables below); the agents' CLIs are never run.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import capabilities, claude_cli, integration_repair, plugin_cli

M = capabilities.MARKETPLACE


@pytest.fixture
def homes(tmp_path, monkeypatch):
    claude = tmp_path / "claude"
    codex = tmp_path / "codex"
    for name, value in {"CLAUDE_CONFIG_DIR": claude, "CODEX_HOME": codex, "PI_CODING_AGENT_DIR": tmp_path / "pi",
                        "KIMI_CODE_HOME": tmp_path / "kimi"}.items():
        monkeypatch.setenv(name, str(value))
    monkeypatch.delenv("PROBE_INSTALLED_PLUGINS_JSON", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_PLUGIN_CACHE_DIR", raising=False)
    removed: list[tuple[str, str]] = []
    monkeypatch.setattr(plugin_cli, "uninstall",
                        lambda source, plugin_id: removed.append((source, plugin_id)) or claude_cli.Result(ok=True))
    return claude, codex, removed


def _claude_ledger(claude: Path, plugins: dict, *, enabled: dict | None = None) -> None:
    (claude / "plugins").mkdir(parents=True, exist_ok=True)
    (claude / "plugins" / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": plugins}))
    (claude / "settings.json").write_text(json.dumps({"enabledPlugins": enabled or {}}))


def _entry(claude: Path, name: str, *, scope: str = "user", files: bool = True) -> list[dict]:
    path = claude / "plugins" / "cache" / M / name / "1.0.0"
    if files:
        path.mkdir(parents=True, exist_ok=True)
    return [{"scope": scope, "installPath": str(path), "version": "1.0.0"}]


def test_a_claude_plugin_whose_files_are_gone_is_not_installed(homes):
    claude, _codex, _removed = homes
    _claude_ledger(claude, {f"probe-research@{M}": _entry(claude, "probe-research", files=False)})
    assert integration_repair.unusable_plugins(plugin_cli.CLAUDE) == {"probe-research": "its files are gone"}


def test_a_disabled_or_project_scope_claude_plugin_is_not_installed(homes):
    claude, _codex, _removed = homes
    _claude_ledger(
        claude,
        {f"probe-research@{M}": _entry(claude, "probe-research"),
         f"probe-research-tap@{M}": _entry(claude, "probe-research-tap", scope="project")},
        enabled={f"probe-research@{M}": False},
    )
    found = integration_repair.unusable_plugins(plugin_cli.CLAUDE)
    assert found["probe-research"] == "disabled in Claude Code"
    assert "user scope" in found["probe-research-tap"]


def test_a_usable_plugin_is_left_alone(homes):
    claude, _codex, removed = homes
    _claude_ledger(claude, {f"probe-research@{M}": _entry(claude, "probe-research")},
                   enabled={f"probe-research@{M}": True})
    assert integration_repair.unusable_plugins(plugin_cli.CLAUDE) == {}
    done = integration_repair.repair(plugin_cli.CLAUDE)
    assert not done.lines and not done.problems and removed == []


def test_the_retired_tap_and_the_other_recorders_plugin_are_removed(homes):
    claude, _codex, removed = homes
    _claude_ledger(claude, {
        "prbe-cc-tap-plugin@prbe-ai": _entry(claude, "prbe-cc-tap-plugin"),
        f"probe-research@{M}": _entry(claude, "probe-research"),
        f"probe-research-daemon@{M}": _entry(claude, "probe-research-daemon"),
        f"probe-research-tap@{M}": _entry(claude, "probe-research-tap"),
    })
    done = integration_repair.repair(plugin_cli.CLAUDE)
    assert removed == [(plugin_cli.CLAUDE, "prbe-cc-tap-plugin@prbe-ai"),
                       (plugin_cli.CLAUDE, f"probe-research-daemon@{M}")], "the agent records: the daemon's goes"
    assert not done.problems and len(done.lines) == 2


def test_a_disabled_plugin_is_turned_back_on_and_one_whose_files_are_gone_reinstalled(homes, monkeypatch):
    claude, _codex, _removed = homes
    _claude_ledger(claude, {f"probe-research@{M}": _entry(claude, "probe-research"),
                            f"probe-research-tap@{M}": _entry(claude, "probe-research-tap", files=False)},
                   enabled={f"probe-research@{M}": False})
    from probe.cli import integration_reinstall

    reinstalled = []

    def hook_repair(source):
        reinstalled.append(source)
        (claude / "plugins" / "cache" / M / "probe-research-tap" / "1.0.0").mkdir(parents=True)

    monkeypatch.setattr(integration_reinstall, "_hook_repair", hook_repair)
    done = integration_repair.repair(plugin_cli.CLAUDE)
    settings = json.loads((claude / "settings.json").read_text())
    assert settings["enabledPlugins"][f"probe-research@{M}"] is True
    assert reinstalled == [plugin_cli.CLAUDE] and not done.problems
    assert integration_repair.unusable_plugins(plugin_cli.CLAUDE) == {}


def _codex(codex: Path, plugins: dict, copies: dict) -> None:
    codex.mkdir(parents=True, exist_ok=True)
    lines = []
    for plugin_id, enabled in plugins.items():
        lines += [f'[plugins."{plugin_id}"]', f"enabled = {str(enabled).lower()}", ""]
    (codex / "config.toml").write_text("\n".join(lines))
    for name, hooks in copies.items():
        root = codex / "plugins" / "cache" / M / name / "1.0.0"
        (root / ".codex-plugin").mkdir(parents=True, exist_ok=True)
        (root / ".codex-plugin" / "plugin.json").write_text(json.dumps({"name": name}))
        (root / "hooks").mkdir(exist_ok=True)
        (root / "hooks" / "hooks.json").write_text(hooks)


def test_codex_says_the_hooks_line_whenever_probes_hook_entries_changed(homes, monkeypatch):
    """Codex trusts each hook by its hash: changed entries run only once a person
    approves them again, and the line was said only on a fresh capture install."""
    _claude, codex, _removed = homes
    _codex(codex, {f"probe-research@{M}": True, f"probe-research-tap@{M}": True},
           {"probe-research": "{}", "probe-research-tap": '{"v": 1}'})
    from probe.cli import integration_reinstall

    def hook_repair(source):  # the stock reinstall writes a new copy of the hooks
        (codex / "plugins" / "cache" / M / "probe-research-tap" / "1.0.0" / "hooks" / "hooks.json").write_text(
            '{"v": 2}')

    monkeypatch.setattr(integration_reinstall, "_hook_repair", hook_repair)
    assert integration_repair.repair(plugin_cli.CODEX).hooks_changed is False, "nothing changed: no line"
    import shutil

    tap = codex / "plugins" / "cache" / M / "probe-research-tap"
    shutil.rmtree(tap / "1.0.0" / ".codex-plugin")  # its files gone: the reinstall writes new hooks
    done = integration_repair.repair(plugin_cli.CODEX)
    assert done.hooks_changed and integration_repair.CODEX_HOOKS_LINE in done.lines


def test_pi_with_its_extension_filtered_out_is_repaired(homes, tmp_path):
    from probe.cli import pi_config

    settings = pi_config.settings_path()
    settings.parent.mkdir(parents=True, exist_ok=True)
    source = "git:github.com/prbe-ai/research-os-agent"
    settings.write_text(json.dumps({"packages": [{"source": source, "extensions": []}]}))
    assert integration_repair.unusable_plugins("pi")
    done = integration_repair.repair("pi")
    assert not done.problems, done.problems
    assert json.loads(settings.read_text())["packages"] == [source]
    assert integration_repair.unusable_plugins("pi") == {}


def test_a_kimi_record_whose_files_are_gone_is_put_back(homes, monkeypatch):
    from probe.cli import kimi_config

    root = kimi_config.managed_root() / "probe-research@1.0.0"
    doc = {"version": kimi_config.INSTALLED_VERSION, "plugins": [
        {"id": "probe-research", "root": str(root), "source": "local-path", "enabled": True}]}
    kimi_config.installed_path().parent.mkdir(parents=True, exist_ok=True)
    kimi_config.installed_path().write_text(json.dumps(doc))
    assert integration_repair.unusable_plugins(plugin_cli.KIMI) == {"probe-research": "its files are gone"}
    put_back = []

    def install_plugin(plugin_id):
        put_back.append(plugin_id)
        (root / kimi_config.MANIFEST).parent.mkdir(parents=True)
        (root / kimi_config.MANIFEST).write_text("{}")
        return claude_cli.Result(ok=True)

    monkeypatch.setattr(kimi_config, "install_plugin", install_plugin)
    done = integration_repair.repair(plugin_cli.KIMI)
    assert put_back == ["probe-research"] and not done.problems


def test_configure_does_not_call_an_unusable_plugin_installed(homes, monkeypatch):
    """The wizard's verdict (`doctor.collect`): installed means usable, so the
    plan reinstalls instead of "Nothing to change"."""
    from probe.cli import doctor

    claude, _codex, _removed = homes
    _claude_ledger(claude, {f"probe-research@{M}": _entry(claude, "probe-research", files=False)})
    monkeypatch.setenv("PROBE_AGENT", plugin_cli.CLAUDE)
    caps = doctor.collect(local=True, plugins=capabilities.PluginState(
        names=frozenset({"probe-research"}), verified=True))
    assert caps.tracking_plugin_installed is False
