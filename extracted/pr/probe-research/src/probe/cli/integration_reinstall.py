"""Explicit repair of selected, existing integrations; never a settings reset.

Runs under the wizard lock, before configure's defaults/auth/bootstrap. A bounded
private intent survives a failed remove/install so retry still repairs a plugin
whose registration disappeared. Paths come from the harness, never that journal.
"""

from __future__ import annotations

import json
import hashlib
import os
import shutil
import tempfile
from pathlib import Path

from probe.cli import capabilities, claude_cli, codex_config, pi_config, plugin_cli
from probe.core import events
from probe.harness import get_registry
from probe.sdk import session_marker
from probe.sdk.durable import write_text_atomic

_LIMIT = 8192
_SOURCES = ("claude_code", "codex", "pi")


class RepairError(ValueError):
    pass


def _read_json(path: Path, *, missing: dict | None = None) -> dict:
    try:
        if path.stat().st_size > _LIMIT:
            raise RepairError("repair metadata is too large")
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if missing is not None:
            return missing
        raise RepairError("integration metadata is missing") from None
    if not isinstance(value, dict):
        raise RepairError("integration metadata is not an object")
    return value


def _journal(source: str) -> Path:
    return session_marker.sessions_dir().parent / "integration-reinstall" / f"{source}.json"


def _settings_path(source: str) -> Path:
    if source == "codex":
        return codex_config.config_path()
    return get_registry().get(source).home_dir() / "settings.json"


def _flags(source: str, names: list[str]) -> dict:
    path = _settings_path(source)
    if source == "codex":
        import tomlkit

        data = tomlkit.parse(path.read_text(encoding="utf-8")) if path.exists() else {}
        table = data.get("plugins", {})
        result = {}
        for name in names:
            entry = table.get(f"{name}@{capabilities.MARKETPLACE}", {})
            if set(entry) - {"enabled"} or ("enabled" in entry and type(entry["enabled"]) is not bool):
                raise RepairError("custom plugin options need repair in the coding agent; left unchanged")
            result[name] = entry.get("enabled")
        return result
    data = _read_settings_json(path)
    table = data.get("enabledPlugins", {})
    if not isinstance(table, dict):
        raise RepairError("plugin enable settings are unreadable")
    result = {name: table.get(f"{name}@{capabilities.MARKETPLACE}") for name in names}
    if any(value is not None and type(value) is not bool for value in result.values()):
        raise RepairError("plugin enable settings are unreadable")
    return result


def _read_settings_json(path: Path) -> dict:
    # Settings may legitimately exceed the small repair journal's bound.
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    if not isinstance(data, dict):
        raise RepairError("agent settings are unreadable")
    return data


def _restore_flags(source: str, flags: dict) -> None:
    path = _settings_path(source)
    if source == "codex":
        import tomlkit

        data = tomlkit.parse(path.read_text(encoding="utf-8"))
        for name, flag in flags.items():
            table = data.get("plugins", {}).get(f"{name}@{capabilities.MARKETPLACE}")
            if table is not None:
                if table.get("enabled") is False:
                    flag = False  # an explicit off during repair wins
                if flag is None:
                    table.pop("enabled", None)
                else:
                    table["enabled"] = flag
        text = tomlkit.dumps(data)
    else:
        data = _read_settings_json(path)
        table = data.get("enabledPlugins", {})
        if not isinstance(table, dict):
            raise RepairError("plugin enable settings changed during repair")
        for name, flag in flags.items():
            key = f"{name}@{capabilities.MARKETPLACE}"
            if table.get(key) is False:
                flag = False
            if flag is None:
                table.pop(key, None)
            else:
                table[key] = flag
        data["enabledPlugins"] = table
        text = json.dumps(data, indent=2) + "\n"
    write_text_atomic(path, text, mode=0o600)


def _cache(source: str, name: str) -> Path:
    home = get_registry().get(source).home_dir()
    base = home / "plugins" / "cache"
    path = base / capabilities.MARKETPLACE / name
    if (any(part.is_symlink() for part in (path, path.parent, base))
            or not base.resolve().is_relative_to(home.resolve())
            or not path.parent.resolve().is_relative_to(base.resolve())):
        raise RepairError("plugin cache resolves outside its managed directory; left unchanged")
    if path.exists() and not path.is_dir():
        raise RepairError("plugin cache is not a directory; left unchanged")
    return path


def _check(result: claude_cli.Result) -> None:
    if not result.ok:
        raise RepairError(result.detail or "the coding agent refused the repair")


def _registered(source: str) -> set[str]:
    if not plugin_cli.available(source):
        raise RepairError(f"`{plugin_cli.binary_name(source)}` not found on PATH")
    # Preserve marketplace identity: PluginState.names intentionally drops it.
    return set(capabilities.LOCAL_PLUGIN_RECORDS[source]())


def _validate_registrations(source: str, names: list[str]) -> None:
    if source != "claude_code":
        _flags(source, names)  # reject unknown/custom Codex plugin options
        return
    ledger = _read_settings_json(capabilities.claude_plugin_ledger())
    plugins = ledger.get("plugins")
    if not isinstance(plugins, dict):
        raise RepairError("Claude Code's plugin registration is unreadable")
    for name in names:
        entries = plugins.get(f"{name}@{capabilities.MARKETPLACE}", [])
        if not isinstance(entries, list):
            raise RepairError("Claude Code's plugin registration is unreadable")
        cache = _cache(source, name)
        for entry in entries:
            if not isinstance(entry, dict) or entry.get("scope") != "user":
                raise RepairError("project/local plugin installs need repair in Claude Code; left unchanged")
            installed = entry.get("installPath")
            if not isinstance(installed, str):
                raise RepairError("plugin install path is unreadable; left unchanged")
            path = Path(installed)
            if not path.is_absolute() or path.is_symlink() or path.resolve().parent != cache.resolve():
                raise RepairError("plugin registration points outside its managed cache; left unchanged")


def _physical(source: str, name: str) -> bool:
    root = _cache(source, name)
    manifest = ".codex-plugin" if source == "codex" else ".claude-plugin"
    for path in root.glob(f"*/{manifest}/plugin.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("name") == name and (path.parent.parent / "hooks" / "hooks.json").is_file():
                return True
        except (OSError, ValueError, AttributeError):
            continue
    return False


def _hook_repair(source: str) -> None:
    profile = session_marker.recorder(source)
    tracking = capabilities.tracking_plugin_name(source)
    allowed = {tracking, capabilities.capture_plugin_name(source)}
    path = _journal(source)
    if path.exists():
        intent = _read_json(path)
        if (set(intent) != {"v", "source", "profile", "home", "names", "flags", "phase"} or intent.get("v") != 1
                or intent.get("source") != source or intent.get("profile") != profile
                or intent.get("home") != str(get_registry().get(source).home_dir().resolve())
                or not isinstance(intent.get("names"), list) or not intent["names"]
                or any(name not in allowed for name in intent["names"])
                or not isinstance(intent.get("flags"), dict)
                or set(intent["flags"]) != set(intent["names"])
                or intent.get("phase") not in ("ready", "applying")
                or any(value is not None and type(value) is not bool for value in intent["flags"].values())):
            raise RepairError("saved repair no longer matches this agent/profile; left unchanged")
    else:
        installed = _registered(source)
        names = sorted(name for name in allowed if f"{name}@{capabilities.MARKETPLACE}" in installed)
        if not names:
            raise RepairError("no installed stock integration to repair; custom marketplaces were left unchanged")
        intent = {"v": 1, "source": source, "profile": profile, "names": names,
                  "home": str(get_registry().get(source).home_dir().resolve()),
                  "flags": _flags(source, names), "phase": "ready"}
        for name in names:
            cache = _cache(source, name)
            if cache.with_name(f".{name}.probe-reinstall-backup").exists():
                raise RepairError("an unrecognized plugin repair backup exists; left unchanged")
    _validate_registrations(source, intent["names"])
    if intent["phase"] == "applying":
        # A killed installer may have default-enabled a previously disabled
        # plugin. Recover off before a refresh can fail or wait on the network.
        off = {name: False for name, value in intent["flags"].items() if value is False}
        if off:
            _restore_flags(source, off)
    # Never remove a working copy after a failed/offline marketplace refresh.
    _check(plugin_cli.refresh_marketplace(source, capabilities.MARKETPLACE))
    _validate_registrations(source, intent["names"])
    current_flags = _flags(source, intent["names"])
    for name, value in current_flags.items():
        if value is False or (value is not None and intent["phase"] == "ready"):
            intent["flags"][name] = value
    # `applying` survives a process kill before flag restoration. A true flag
    # there may be the installer's default, so it never overrides saved off.
    intent["phase"] = "applying"
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    write_text_atomic(path, json.dumps(intent) + "\n", mode=0o600)
    backups = []
    try:
        for name in intent["names"]:
            cache = _cache(source, name)
            backup = cache.with_name(f".{name}.probe-reinstall-backup")
            if backup.is_symlink() or (backup.exists() and not backup.is_dir()):
                raise RepairError("repair backup is a symlink; left unchanged")
            if cache.exists():
                if backup.exists():
                    shutil.rmtree(cache)
                else:
                    os.replace(cache, backup)
            backups.append((cache, backup))
            _validate_registrations(source, [name])
            current = _registered(source)
            plugin_id = f"{name}@{capabilities.MARKETPLACE}"
            if plugin_id in current:
                _check(plugin_cli.uninstall(source, plugin_id))
            _check(plugin_cli.install(source, plugin_id))
            _restore_flags(source, {name: intent["flags"][name]})
            if not _physical(source, name):
                raise RepairError(f"{name}: installed files could not be verified")
        installed = _registered(source)
        if not all(f"{name}@{capabilities.MARKETPLACE}" in installed for name in intent["names"]):
            raise RepairError("reinstalled plugins could not be verified")
    except BaseException:
        for cache, backup in backups:
            if backup.exists():
                if cache.exists():
                    shutil.rmtree(cache)
                os.replace(backup, cache)
        raise
    finally:
        _restore_flags(source, intent["flags"])
        restored = _flags(source, intent["names"])
        for name, value in restored.items():
            if value is not None:
                intent["flags"][name] = value
        intent["phase"] = "ready"
        write_text_atomic(path, json.dumps(intent) + "\n", mode=0o600)
    for _cache_path, backup in backups:
        if backup.exists():
            shutil.rmtree(backup)
    path.unlink()


def _pi_repair() -> None:
    active = os.environ
    settings = pi_config.settings_path(active)
    before = settings.read_bytes()
    data = pi_config._load_settings(settings)
    index = pi_config._our_entry_index(data, root=pi_config.local_package_root(active),
                                     agent_dir=pi_config.pi_agent_dir(active))
    if index is None:
        raise RepairError("no installed pi integration to repair")
    source = pi_config._entry_source(data["packages"][index]) or ""
    if pi_config._git_repo_identity(source) != pi_config._MIRROR_IDENTITY:
        raise RepairError("pi uses a local/custom package; repair it at that source, which was left unchanged")
    root = pi_config.pi_agent_dir(active) / "git" / "github.com" / pi_config.MIRROR_REPO
    base = pi_config.pi_agent_dir(active) / "git"
    if (any(part.is_symlink() for part in (root, root.parent, root.parent.parent, base))
            or not root.parent.resolve().is_relative_to(base.resolve())):
        raise RepairError("pi package resolves outside its managed clone; left unchanged")
    if root.exists() and not root.is_dir():
        raise RepairError("pi package cache is not a directory; left unchanged")
    binary = shutil.which("pi")
    if not binary:
        raise RepairError("pi is not on PATH")
    backup = root.with_name(root.name + ".probe-reinstall-backup")
    intent = {"v": 1, "source": "pi", "profile": session_marker.recorder("pi"), "package_source": source,
              "home": str(pi_config.pi_agent_dir(active).resolve()),
              "entry_digest": hashlib.sha256(json.dumps(data["packages"][index], sort_keys=True).encode()).hexdigest()}
    journal = _journal("pi")
    if journal.exists():
        if (_read_json(journal) != intent or backup.is_symlink()
                or (backup.exists() and not backup.is_dir())):
            raise RepairError("saved pi repair no longer matches its package/profile; left unchanged")
        if backup.exists():
            if root.exists():
                shutil.rmtree(root)
            os.replace(backup, root)
    elif backup.exists() or backup.is_symlink():
        raise RepairError("an unrecognized pi repair backup exists; left unchanged")
    journal.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    write_text_atomic(journal, json.dumps(intent) + "\n", mode=0o600)
    if root.exists():
        os.replace(root, backup)
    try:
        # pi's updateGit calls installGit when the managed clone is absent;
        # unlike `pi install`, it never normalizes/replaces the settings entry.
        # pi update matches both user and cwd's project package entries. An
        # empty temporary cwd prevents repair from updating another project.
        with tempfile.TemporaryDirectory(prefix="pi-reinstall-", dir=journal.parent) as neutral:
            child_env = {**active, "PI_CODING_AGENT_DIR": str(pi_config.pi_agent_dir(active).resolve())}
            _check(pi_config.update_package(child_env, cwd=Path(neutral)))
        package = root / "plugins" / pi_config.PACKAGE_NAME
        if not (package / "index.ts").is_file() or not (package / "package.json").is_file():
            raise RepairError("pi integration files could not be verified")
        if settings.read_bytes() != before:
            raise RepairError("pi changed package settings during repair")
    except BaseException:
        if root.exists():
            shutil.rmtree(root)
        if backup.exists():
            os.replace(backup, root)
        journal.unlink(missing_ok=True)
        raise
    if backup.exists():
        shutil.rmtree(backup)
    journal.unlink()


def run(sources: tuple[str, ...] | list[str]) -> bool:
    from probe.cli import telemetry

    from probe.sdk.config import resolve

    tel = telemetry.TelemetryContext.start(via=telemetry.Via.WIZARD, interactive=False,
                                          base_url=resolve().base_url)
    events.begin_result("configure", sources)
    all_ok = True
    for source in sources:
        tel.emit(telemetry.EVENT_INTEGRATION_REINSTALL_STARTED, operation="reinstall", agent_source=source)
        events.step(events.Step.REINSTALL_INTEGRATION, events.Status.STARTED, "Reinstalling Probe integration", agent=source)
        try:
            if source not in _SOURCES:
                raise RepairError("this agent does not support integration repair")
            if source == "pi":
                _pi_repair()
            else:
                _hook_repair(source)
        except Exception as exc:  # noqa: BLE001 - report a failed repair, never a complete installation
            all_ok = False
            message = str(exc)
            events.step(events.Step.REINSTALL_INTEGRATION, events.Status.FAILED, message, agent=source)
            events.agent_result(source, requested={"reinstall": True}, actual=None, ok=False, message=message)
            tel.emit(telemetry.EVENT_INTEGRATION_REINSTALL_COMPLETED, operation="reinstall",
                     agent_source=source, outcome=telemetry.ConfigureOutcome.FAILED)
        else:
            events.step(events.Step.REINSTALL_INTEGRATION, events.Status.DONE, "Probe integration reinstalled", agent=source)
            events.agent_result(source, requested={"reinstall": True}, actual={"reinstalled": True}, ok=True)
            tel.emit(telemetry.EVENT_INTEGRATION_REINSTALL_COMPLETED, operation="reinstall",
                     agent_source=source, outcome=telemetry.ConfigureOutcome.SUCCESS)
    return all_ok
