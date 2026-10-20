"""A current-but-corrupt integration must be replaced without resetting Probe.

The fake coding-agent binary is a real child process: installing an already
registered version deliberately does nothing, as Claude does. This distinguishes
repair from an ordinary update/configure that merely reports the same version.
"""

from __future__ import annotations

import importlib
import json
import os
import shutil
import sys

import pytest
from typer.testing import CliRunner

import probe.core
from probe.cli import integration_reinstall as repair
from probe.core import actions, requests
from probe.core.requests import Agent, ConfigureRequest, RequestError
from probe.sdk import session_marker

main = importlib.import_module("probe.cli.main")
PROFILE = "probe-research-daemon"
MARKET = "research-os-agent"

STUB = r'''
import json, os, sys
from pathlib import Path
home = Path(os.environ["CLAUDE_CONFIG_DIR"])
args = sys.argv[1:]
with (home / "calls.jsonl").open("a") as f:
    f.write(json.dumps(args) + "\n")
if args[:3] == ["plugin", "marketplace", "update"]:
    print("refresh failed" if os.environ.get("FAIL_REFRESH") else "refreshed")
    sys.exit(1 if os.environ.get("FAIL_REFRESH") else 0)
ledger = home / "plugins" / "installed_plugins.json"
data = json.loads(ledger.read_text())
settings = home / "settings.json"
cfg = json.loads(settings.read_text())
plugin = args[2]
name = plugin.split("@")[0]
if args[1] == "uninstall":
    data["plugins"].pop(plugin, None)
    cfg["enabledPlugins"].pop(plugin, None)
elif args[1] == "install":
    if os.environ.get("FAIL_INSTALL") == name:
        print("install failed")
        sys.exit(1)
    if plugin in data["plugins"]:
        print("already installed")
        sys.exit(0)
    root = home / "plugins" / "cache" / "research-os-agent" / name / "1.0.0"
    (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (root / "hooks").mkdir(exist_ok=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name":name,"version":"1.0.0"}))
    (root / "hooks" / "hooks.json").write_text("{}")
    (root / "code.py").write_text("healthy")
    data["plugins"][plugin] = [{"scope":"user","version":"1.0.0","installPath":str(root)}]
    cfg["enabledPlugins"][plugin] = True
else:
    raise SystemExit(2)
ledger.write_text(json.dumps(data))
settings.write_text(json.dumps(cfg))
'''


@pytest.fixture
def device(tmp_path, monkeypatch):
    for key in ("PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING", "PROBE_CONFIG_PATH", "PROBE_PI_PACKAGE_ROOT",
                "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PI_SESSION_ID", "PROBE_INSTALLED_PLUGINS_JSON"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    home = tmp_path / "claude"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home))
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    binary = bin_dir / "claude"
    binary.write_text(f"#!{sys.executable}\n" + STUB)
    binary.chmod(0o755)
    monkeypatch.setenv("PATH", str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
    monkeypatch.setattr(repair.plugin_cli, "available", lambda source: shutil.which(repair.plugin_cli.binary_name(source)) is not None)
    ledger = {"version": 2, "plugins": {}}
    for name in (PROFILE, "probe-research-tap", "unrelated-plugin"):
        root = home / "plugins" / "cache" / MARKET / name / "1.0.0"
        (root / "hooks").mkdir(parents=True)
        (root / ".claude-plugin").mkdir()
        (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": name}))
        (root / "hooks" / "hooks.json").write_text("{}")
        (root / "code.py").write_text("corrupt")
        ledger["plugins"][f"{name}@{MARKET}"] = [{"scope": "user", "version": "1.0.0", "installPath": str(root)}]
    (home / "plugins" / "installed_plugins.json").write_text(json.dumps(ledger))
    (home / "settings.json").write_text(json.dumps({"enabledPlugins": {
        f"{PROFILE}@{MARKET}": False, f"probe-research-tap@{MARKET}": False,
        f"unrelated-plugin@{MARKET}": True}, "userChoice": "kept"}))
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    session_marker.write_default_state(session_marker.STATE_OFF)
    return home


def _code(home, name):
    return home / "plugins" / "cache" / MARKET / name / "1.0.0" / "code.py"


def test_core_reinstalls_current_corrupt_files_and_preserves_off_defaults_credentials_and_other_plugins(device, tmp_path):
    config = session_marker.config_path().read_bytes()
    disabled = tmp_path / "state" / "tap" / ".disabled"
    disabled.parent.mkdir(parents=True)
    disabled.write_text("capture stays off")
    events = []
    code = probe.core.configure(ConfigureRequest(agents=(Agent.CLAUDE,), reinstall=True), events.append)
    assert code == 0 and events[-1]["complete"] is True
    assert _code(device, PROFILE).read_text() == "healthy"
    assert _code(device, "probe-research-tap").read_text() == "healthy"
    assert _code(device, "unrelated-plugin").read_text() == "corrupt"
    assert session_marker.config_path().read_bytes() == config
    assert disabled.read_text() == "capture stays off"
    settings = json.loads((device / "settings.json").read_text())
    assert settings["enabledPlugins"][f"{PROFILE}@{MARKET}"] is False
    assert settings["enabledPlugins"][f"probe-research-tap@{MARKET}"] is False
    assert settings["userChoice"] == "kept"
    assert not repair._journal("claude_code").exists()
    assert all(event["event"] != "device_prompt" for event in events)


def test_failed_install_is_incomplete_and_retry_repairs_a_now_missing_registration(device, monkeypatch):
    monkeypatch.setenv("FAIL_INSTALL", PROFILE)
    events = []
    assert probe.core.configure(ConfigureRequest(agents=(Agent.CLAUDE,), reinstall=True), events.append) == 1
    assert events[-1]["complete"] is False
    assert _code(device, PROFILE).read_text() == "corrupt", "working cache is recovered"
    intent = repair._journal("claude_code")
    assert intent.exists() and intent.stat().st_mode & 0o777 == 0o600
    assert f"{PROFILE}@{MARKET}" not in json.loads((device / "plugins" / "installed_plugins.json").read_text())["plugins"]
    monkeypatch.delenv("FAIL_INSTALL")
    events = []
    assert probe.core.configure(ConfigureRequest(agents=(Agent.CLAUDE,), reinstall=True), events.append) == 0
    assert events[-1]["complete"] is True and _code(device, PROFILE).read_text() == "healthy"


def test_failed_refresh_cannot_remove_any_installed_plugin(device, monkeypatch):
    before = (device / "plugins" / "installed_plugins.json").read_bytes()
    monkeypatch.setenv("FAIL_REFRESH", "1")
    events = []
    assert probe.core.configure(ConfigureRequest(agents=(Agent.CLAUDE,), reinstall=True), events.append) == 1
    assert events[-1]["complete"] is False
    assert (device / "plugins" / "installed_plugins.json").read_bytes() == before
    assert _code(device, PROFILE).read_text() == "corrupt"


def test_cli_flag_and_core_request_produce_the_same_repair_steps(device):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--agent", "claude", "--reinstall", "--yes", "--json"])
    assert result.exit_code == 0, result.output
    wire = [json.loads(line) for line in result.stdout.splitlines()]
    assert wire[-1]["complete"] is True
    assert wire[-2]["agents"][0]["requested"] == {"reinstall": True}
    assert actions.wizard_flags(requests.ActionName.CONFIGURE, ConfigureRequest((Agent.CLAUDE,), reinstall=True))["reinstall"] is True


@pytest.mark.parametrize("value", [None, "true", 1, [], {}])
def test_reinstall_is_a_strict_boolean(value):
    with pytest.raises(RequestError):
        requests.parse("configure", {"agents": ["claude"], "reinstall": value})
    with pytest.raises(RequestError):
        ConfigureRequest((Agent.CLAUDE,), reinstall=value)


def test_reinstall_cannot_reset_settings_or_redeem_an_onboarding_code(device):
    with pytest.raises(RequestError):
        requests.parse("configure", {"agents": ["claude"], "reinstall": True, "capture": False})
    result = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--agent", "claude", "--reinstall", "ABCDE12345", "--json"])
    assert result.exit_code == 2
    assert _code(device, PROFILE).read_text() == "corrupt"


def test_codex_repairs_only_the_current_profile_and_preserves_disabled_plugins(device, tmp_path, monkeypatch):
    import tomlkit
    from probe.cli import claude_cli, codex_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    home = codex_config.codex_home()
    home.mkdir()
    (home / "config.toml").write_text(f'''user_choice = "kept"
[plugins."{PROFILE}@{MARKET}"]
enabled = false
[plugins."probe-research-tap@{MARKET}"]
enabled = false
[plugins."probe-research@{MARKET}"]
enabled = true
''')
    for name in (PROFILE, "probe-research-tap", "probe-research"):
        root = home / "plugins/cache" / MARKET / name / "1.0.0"
        (root / ".codex-plugin").mkdir(parents=True)
        (root / ".codex-plugin/plugin.json").write_text(json.dumps({"name": name}))
        (root / "hooks").mkdir()
        (root / "hooks/hooks.json").write_text("{}")
        (root / "code.py").write_text("corrupt")
    calls = []

    def command(source, args, *, timeout):
        calls.append(args)
        if args[:2] == ["plugin", "marketplace"]:
            return claude_cli.Result(ok=True)
        name = args[2].split("@")[0]
        data = tomlkit.parse((home / "config.toml").read_text())
        if args[1] == "remove":
            data["plugins"].pop(args[2])
        else:
            root = home / "plugins/cache" / MARKET / name / "1.0.0"
            (root / ".codex-plugin").mkdir(parents=True)
            (root / ".codex-plugin/plugin.json").write_text(json.dumps({"name": name}))
            (root / "hooks").mkdir()
            (root / "hooks/hooks.json").write_text("{}")
            (root / "code.py").write_text("healthy")
            data["plugins"][args[2]] = {"enabled": True}
        (home / "config.toml").write_text(tomlkit.dumps(data))
        return claude_cli.Result(ok=True)

    monkeypatch.setattr(repair.plugin_cli, "run", command)
    monkeypatch.setattr(repair.plugin_cli, "available", lambda source: True)
    before = session_marker.config_path().read_bytes()
    assert repair.run(["codex"])
    data = tomlkit.parse((home / "config.toml").read_text())
    assert data["plugins"][f"{PROFILE}@{MARKET}"]["enabled"] is False
    assert data["plugins"][f"probe-research-tap@{MARKET}"]["enabled"] is False
    assert (home / "plugins/cache" / MARKET / "probe-research/1.0.0/code.py").read_text() == "corrupt"
    assert not any("probe-research@" in " ".join(call) for call in calls)
    assert session_marker.config_path().read_bytes() == before


def test_reinstall_refuses_an_escaping_cache_before_removing_anything(device, tmp_path):
    cache = device / "plugins/cache" / MARKET / PROFILE
    outside = tmp_path / "user-fork"
    cache.rename(outside)
    cache.symlink_to(outside, target_is_directory=True)
    assert not repair.run(["claude_code"])
    assert (outside / "1.0.0/code.py").read_text() == "corrupt"
    assert not (device / "calls.jsonl").exists()


def test_large_real_claude_ledger_does_not_inherit_the_private_journal_limit(device):
    path = device / "plugins/installed_plugins.json"
    data = json.loads(path.read_text())
    data["unrelatedMetadata"] = "x" * 20000
    path.write_text(json.dumps(data))
    assert repair.run(["claude_code"])


@pytest.mark.parametrize("fails", [False, True])
@pytest.mark.parametrize("relative", [False, True])
def test_pi_reclones_physical_package_without_changing_tracking_off_or_profile(device, tmp_path, monkeypatch, fails, relative):
    from probe.cli import pi_config

    home = tmp_path / "pi-agent"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PI_CODING_AGENT_DIR", "pi-agent" if relative else str(home))
    home.mkdir()
    entry = {"source": pi_config.MIRROR_GIT_SOURCE, "probeTracking": False,
             "skills": [], "extensions": ["index.ts"], "probeAgentSkills": ["user-filter"]}
    settings = home / "settings.json"
    settings.write_text(json.dumps({"packages": [entry], "userChoice": "kept"}))
    before = settings.read_bytes()
    root = home / "git/github.com/prbe-ai/research-os-agent"
    package = root / "plugins/probe-research-pi"
    package.mkdir(parents=True)
    (package / "index.ts").write_text("corrupt")
    binary = tmp_path / "bin/pi"
    binary.write_text(f'''#!{sys.executable}
import os,sys
from pathlib import Path
if os.environ.get("FAIL_PI_REPAIR"): raise SystemExit(1)
root=Path(os.environ["PI_CODING_AGENT_DIR"])/"git/github.com/prbe-ai/research-os-agent/plugins/probe-research-pi"
root.mkdir(parents=True)
(root/"index.ts").write_text("healthy")
(root/"package.json").write_text('{{"name":"probe-research-pi"}}')
(Path(os.environ["PI_CODING_AGENT_DIR"])/"repair-cwd").write_text(str(Path.cwd()))
''')
    binary.chmod(0o755)
    if fails:
        monkeypatch.setenv("FAIL_PI_REPAIR", "1")
    assert repair.run(["pi"]) is not fails
    assert settings.read_bytes() == before
    assert (package / "index.ts").read_text() == ("corrupt" if fails else "healthy")
    if not fails:
        assert (home / "repair-cwd").read_text() != str(tmp_path)


def test_pi_local_fork_is_preserved_and_refused(device, tmp_path, monkeypatch):
    from probe.cli import pi_config

    home = tmp_path / "pi-agent"
    home.mkdir()
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(home))
    fork = tmp_path / "custom-pi"
    fork.mkdir()
    (fork / "package.json").write_text(json.dumps({"name": pi_config.PACKAGE_NAME}))
    (home / "settings.json").write_text(json.dumps({"packages": [{"source": str(fork), "probeTracking": False}]}))
    before = (home / "settings.json").read_bytes()
    assert not repair.run(["pi"])
    assert (home / "settings.json").read_bytes() == before
    assert fork.exists()


@pytest.mark.parametrize("scope,external", [("project", False), ("user", True)])
def test_claude_non_owned_registration_is_refused_even_on_retry(device, tmp_path, scope, external):
    path = device / "plugins/installed_plugins.json"
    data = json.loads(path.read_text())
    entry = data["plugins"][f"{PROFILE}@{MARKET}"][0]
    entry["scope"] = scope
    if external:
        entry["installPath"] = str(tmp_path / "user-fork")
    path.write_text(json.dumps(data))
    journal = repair._journal("claude_code")
    journal.parent.mkdir(parents=True)
    journal.write_text(json.dumps({"v": 1, "source": "claude_code", "profile": "daemon",
                                  "home": str(device.resolve()),
                                  "names": [PROFILE], "flags": {PROFILE: False}, "phase": "ready"}))
    assert not repair.run(["claude_code"])
    assert not (device / "calls.jsonl").exists()


def test_fork_marketplace_does_not_become_a_second_stock_install(device):
    path = device / "plugins/installed_plugins.json"
    data = json.loads(path.read_text())
    data["plugins"] = {key.replace(f"@{MARKET}", "@my-fork"): value for key, value in data["plugins"].items()}
    path.write_text(json.dumps(data))
    assert not repair.run(["claude_code"])
    assert not (device / "calls.jsonl").exists()


def test_user_disabling_between_failure_and_retry_wins(device, monkeypatch):
    settings = device / "settings.json"
    data = json.loads(settings.read_text())
    data["enabledPlugins"][f"{PROFILE}@{MARKET}"] = True
    settings.write_text(json.dumps(data))
    monkeypatch.setenv("FAIL_INSTALL", PROFILE)
    assert not repair.run(["claude_code"])
    data = json.loads(settings.read_text())
    data["enabledPlugins"][f"{PROFILE}@{MARKET}"] = False
    settings.write_text(json.dumps(data))
    monkeypatch.delenv("FAIL_INSTALL")
    assert repair.run(["claude_code"])
    assert json.loads(settings.read_text())["enabledPlugins"][f"{PROFILE}@{MARKET}"] is False


def test_interrupted_default_enable_is_recovered_before_network_retry(device, monkeypatch):
    journal = repair._journal("claude_code")
    journal.parent.mkdir(parents=True)
    journal.write_text(json.dumps({"v": 1, "source": "claude_code", "profile": "daemon",
                                  "home": str(device.resolve()),
                                  "names": [PROFILE], "flags": {PROFILE: False}, "phase": "applying"}))
    settings = device / "settings.json"
    data = json.loads(settings.read_text())
    data["enabledPlugins"][f"{PROFILE}@{MARKET}"] = True
    settings.write_text(json.dumps(data))
    monkeypatch.setenv("FAIL_REFRESH", "1")
    assert not repair.run(["claude_code"])
    assert json.loads(settings.read_text())["enabledPlugins"][f"{PROFILE}@{MARKET}"] is False


def test_backup_cleanup_failure_keeps_retry_intent(device, monkeypatch):
    original = shutil.rmtree
    failed = False

    def remove(path, *args, **kwargs):
        nonlocal failed
        if "probe-reinstall-backup" in str(path) and not failed:
            failed = True
            raise OSError("cleanup interrupted")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(repair.shutil, "rmtree", remove)
    assert not repair.run(["claude_code"])
    assert repair._journal("claude_code").exists()
    assert repair.run(["claude_code"])
    assert not repair._journal("claude_code").exists()


def test_repair_telemetry_never_counts_as_install_configure_completion(device, monkeypatch):
    from probe.cli import telemetry

    seen = []
    monkeypatch.setattr(telemetry.TelemetryContext, "start", lambda **kwargs: type("Telemetry", (), {
        "emit": lambda self, event, **props: seen.append((event, props))})())
    assert repair.run(["claude_code"])
    assert [event for event, props in seen] == [telemetry.EVENT_INTEGRATION_REINSTALL_STARTED,
                                                telemetry.EVENT_INTEGRATION_REINSTALL_COMPLETED]
    assert seen[-1][1]["outcome"] == telemetry.ConfigureOutcome.SUCCESS
    assert all(props["operation"] == "reinstall" for event, props in seen)


def test_failed_repair_cannot_follow_a_switch_to_another_agent_home(device, tmp_path, monkeypatch):
    monkeypatch.setenv("FAIL_INSTALL", PROFILE)
    assert not repair.run(["claude_code"])
    other = tmp_path / "another-claude"
    other.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(other))
    monkeypatch.delenv("FAIL_INSTALL")
    assert not repair.run(["claude_code"])
    assert list(other.iterdir()) == []
