"""Integrations that read installed are usable, and one of each per agent (plan clean-uninstall-reinstall R-T5).

"Installed" used to mean "the agent's record names it": a Claude Code ledger
entry whose cache was deleted, a plugin the person (or a crash) disabled, a
project-scope install, a Kimi record whose folder is gone, pi's package entry
with `extensions: []` -- all read as installed, so the wizard's configure said
"Nothing to change" over a Probe that did nothing (R6, R9). Now:

    unusable_plugins   what the record names but cannot work, and why (file
                       reads only: the wizard's `doctor.collect` asks it on
                       every pass, and a usable plugin is never reinstalled)
    leftovers          the retired `prbe-cc-tap-plugin` / `prbe-codex-tap-plugin`
                       (a second tap: double capture) and the other profile's
                       plugin next to this one's (`probe-research` with
                       `probe-research-daemon`)
    repair             removes the leftovers, re-enables a disabled plugin,
                       reinstalls one whose files are gone (the stock
                       reinstall, `integration_reinstall`), puts pi's
                       extension back and Kimi's files back -- and says the
                       Codex `/hooks` approval line whenever Probe's hook
                       entries changed (Codex trusts each by its hash)
"""

from __future__ import annotations

import contextlib
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from probe.cli import capabilities, plugin_cli

#: Retired plugins that capture beside today's tap (a second upload of every session).
RETIRED = {
    plugin_cli.CLAUDE: ("prbe-cc-tap-plugin",),
    plugin_cli.CODEX: ("prbe-codex-tap-plugin",),
}
PROFILE_NAMES = (capabilities.TRACKING_PLUGIN_NAME, capabilities.DAEMON_PLUGIN_NAME)
#: Codex trusts a hook by its hash: changed entries wait for a person's approval.
CODEX_HOOKS_LINE = "In the new Codex session: `/hooks` › approve the Probe hooks (until then they do not run)."


def _package_source() -> str | None:
    """The harness whose Probe is a package entry in its settings (pi's), from
    the registry rather than by name."""
    try:
        from probe.harness import FAMILY_EXTENSION, get_registry

        return next((h.id for h in get_registry().installable() if h.family == FAMILY_EXTENSION), None)
    except Exception:  # noqa: BLE001
        return None


@dataclass
class Repaired:
    source: str
    lines: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    hooks_changed: bool = False


def _probe_names(source: str) -> tuple[str, ...]:
    return (*PROFILE_NAMES, capabilities.capture_plugin_name(source))


def _claude_ledger() -> dict:
    try:
        raw = json.loads(capabilities.claude_plugin_ledger().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    plugins = raw.get("plugins") if isinstance(raw, dict) else None
    return plugins if isinstance(plugins, dict) else {}


def _claude_enabled() -> dict:
    from probe.harness import get_registry

    try:
        path = get_registry().get(plugin_cli.CLAUDE).home_dir() / "settings.json"
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError):
        return {}
    table = data.get("enabledPlugins") if isinstance(data, dict) else None
    return table if isinstance(table, dict) else {}


def _codex_tables() -> dict:
    from probe._compat import tomllib
    from probe.cli import codex_config

    try:
        parsed = tomllib.loads(codex_config.config_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    plugins = parsed.get("plugins") if isinstance(parsed, dict) else None
    return plugins if isinstance(plugins, dict) else {}


def _codex_cache(name: str) -> Path:
    from probe.cli import codex_config

    return codex_config.codex_home() / "plugins" / "cache" / capabilities.MARKETPLACE / name


def _claude_unusable(names: tuple[str, ...]) -> dict:
    ledger, enabled, found = _claude_ledger(), _claude_enabled(), {}
    for name in names:
        key = f"{name}@{capabilities.MARKETPLACE}"
        entries = [e for e in ledger.get(key) or [] if isinstance(e, dict)]
        if not entries:
            continue
        mine = [e for e in entries if e.get("scope") == "user"]
        if not mine:
            found[name] = "installed for a project only, not for you (user scope)"
            continue
        paths = [Path(e["installPath"]) for e in mine if isinstance(e.get("installPath"), str)]
        if paths and not any(path.is_dir() for path in paths):
            # (An entry naming no folder cannot be told: never "gone".)
            found[name] = "its files are gone"
        elif enabled.get(key) is False:
            found[name] = "disabled in Claude Code"
    return found


def _codex_unusable(names: tuple[str, ...]) -> dict:
    tables, found = _codex_tables(), {}
    # No plugin cache at all: a Codex that keeps none there cannot be told
    # about (only a cache without this plugin's copy is "gone").
    cached = _codex_cache("x").parent.parent.is_dir()
    for name in names:
        table = tables.get(f"{name}@{capabilities.MARKETPLACE}")
        if not isinstance(table, dict):
            continue
        cache = _codex_cache(name)
        if cached and not any(cache.glob("*/.codex-plugin/plugin.json")):
            found[name] = "its files are gone"
        elif table.get("enabled") is False:
            found[name] = "disabled in Codex"
    return found


def _kimi_unusable() -> dict:
    from probe.cli import kimi_config

    found = {}
    for plugin_id in kimi_config.PLUGIN_IDS:
        root = kimi_config._record_root(plugin_id)  # noqa: SLF001 -- the record's own reader
        if root is not None and not (root / kimi_config.MANIFEST).is_file():
            found[plugin_id] = "its files are gone"
    return found


def _pi_unusable() -> dict:
    from probe.cli import pi_config

    merged = pi_config.merged_package_entry()
    if merged.installed and merged.scope == "global" and merged.extension_filtered_out:
        return {capabilities.TAP_PLUGIN_NAME: "its settings entry filters out Probe's extension (`extensions: []`)"}
    return {}


def unusable_plugins(source: str) -> dict:
    """`{plugin name: why}` for Probe plugins the agent's record names that
    cannot work. File reads only; never raises (an unreadable record: {})."""
    try:
        if source == plugin_cli.CLAUDE:
            return _claude_unusable(_probe_names(source))
        if source == plugin_cli.CODEX:
            return _codex_unusable(_probe_names(source))
        if source == plugin_cli.KIMI:
            return _kimi_unusable()
        if source == _package_source():
            return _pi_unusable()
    except Exception:  # noqa: BLE001 -- a check, never a reason to fail the wizard
        return {}
    return {}


def leftovers(source: str) -> list[tuple[str, str]]:
    """`[(plugin id, why)]` to remove: retired taps, and the other profile's
    plugin beside this one's (one tracking plugin per agent)."""
    try:
        if source == plugin_cli.CLAUDE:
            ids = [key for key, entries in _claude_ledger().items() if isinstance(key, str) and entries]
        elif source == plugin_cli.CODEX:
            ids = [key for key in _codex_tables() if isinstance(key, str)]
        elif source == plugin_cli.KIMI:
            from probe.cli import kimi_config

            ids = [f"{pid}" for pid in kimi_config.PLUGIN_IDS if kimi_config._record_root(pid) is not None]  # noqa: SLF001
        else:
            return []
    except Exception:  # noqa: BLE001
        return []
    found: list[tuple[str, str]] = []
    for plugin_id in ids:
        name = plugin_id.split("@", 1)[0]
        if name in RETIRED.get(source, ()):
            found.append((plugin_id, "the retired capture plugin (it captured every session a second time)"))
    names = {plugin_id.split("@", 1)[0]: plugin_id for plugin_id in ids
             if plugin_id.split("@", 1)[-1] in (capabilities.MARKETPLACE, plugin_id)}
    if all(name in names for name in PROFILE_NAMES):
        keep = capabilities.tracking_plugin_name(source)
        drop = next(name for name in PROFILE_NAMES if name != keep)
        found.append((names[drop], f"the other recorder's plugin, beside {keep} (one per agent)"))
    return found


def codex_hooks_digest() -> str:
    """One digest of every Probe hook entry Codex runs (`hooks/hooks.json` of
    each Probe plugin copy in its cache): what its trust is keyed on."""
    from probe.cli import codex_config, codex_hooks

    digest = hashlib.sha256()
    cache = codex_config.codex_home() / "plugins" / "cache"
    for copy in codex_hooks.installed_copies():
        digest.update(copy.encode())
        with contextlib.suppress(OSError):
            digest.update((cache / copy / "hooks" / "hooks.json").read_bytes())
    return digest.hexdigest()


def _set_enabled(source: str, name: str) -> None:
    """Turn a Probe plugin back on in the agent's own settings (a person asked
    for Probe in this agent: the install or `probe repair`)."""
    from probe.sdk.durable import through_symlink, write_text_atomic

    key = f"{name}@{capabilities.MARKETPLACE}"
    if source == plugin_cli.CODEX:
        import tomlkit

        from probe.cli import codex_config

        original = codex_config.config_path()
        path = through_symlink(original)
        data = tomlkit.parse(path.read_text(encoding="utf-8"))
        table = data.get("plugins", {}).get(key)
        if table is None:
            return
        table["enabled"] = True
        write_text_atomic(path, tomlkit.dumps(data), mode=0o600, keep_mode=path != original)
        return
    from probe.harness import get_registry

    original = get_registry().get(source).home_dir() / "settings.json"
    path = through_symlink(original)
    data = json.loads(path.read_text(encoding="utf-8"))
    table = data.get("enabledPlugins")
    if not isinstance(table, dict):
        return
    table[key] = True
    write_text_atomic(path, json.dumps(data, indent=2) + "\n", mode=0o600, keep_mode=True)


def _repair_pi(out: Repaired) -> None:
    """Drop the `extensions` filter that keeps Probe's extension from loading
    on the global entry: the filter is pi's way to choose a package's parts,
    and an empty one chose none of Probe's (strand-ai)."""
    from probe.cli import pi_config

    path = pi_config.settings_path()
    data = pi_config._load_settings(path)  # noqa: SLF001 -- the one reader, refuses an unreadable file
    index = pi_config._our_entry_index(data, root=pi_config.local_package_root(),  # noqa: SLF001
                                       agent_dir=pi_config.pi_agent_dir())
    if index is None:
        return
    packages = list(data["packages"])
    entry = packages[index]
    if not isinstance(entry, dict) or pi_config._loads_our_extension(entry.get("extensions")):  # noqa: SLF001
        return
    updated = {k: v for k, v in entry.items() if k != "extensions"}
    packages[index] = updated["source"] if set(updated) == {"source"} else updated
    data["packages"] = packages
    pi_config._write_settings(path, data)  # noqa: SLF001
    out.lines.append(f"pi: Probe's extension loads again (removed `extensions: []` from {path})")


def repair(source: str, *, reinstall: bool = True, enable_disabled: bool = True) -> Repaired:
    """Make Probe's plugins in `source` usable and one per kind (see the
    module docstring). `reinstall`: reinstall a plugin whose files are gone
    (the network: the marketplace); off, it is only named. `enable_disabled`:
    turn a disabled Probe plugin back on (the install a person asked for);
    off (`probe repair`), it is only reported -- disabling it was theirs.
    Never raises."""
    out = Repaired(source)
    codex_before = codex_hooks_digest() if source == plugin_cli.CODEX else None
    try:
        for plugin_id, why in leftovers(source):
            result = plugin_cli.uninstall(source, plugin_id)
            if result.ok:
                out.lines.append(f"removed {plugin_id}: {why}")
            else:
                out.problems.append(f"could not remove {plugin_id} ({why}): {result.detail}"[:400])
        broken = unusable_plugins(source)
        if source == _package_source() and broken:
            _repair_pi(out)
            broken = unusable_plugins(source)
        elif source == plugin_cli.KIMI and broken:
            from probe.cli import kimi_config

            for plugin_id in list(broken):
                result = kimi_config.install_plugin(plugin_id)
                if result.ok:
                    out.lines.append(f"Kimi: put {plugin_id}'s files back")
            broken = unusable_plugins(source)
        elif source in (plugin_cli.CLAUDE, plugin_cli.CODEX):
            for name, why in list(broken.items()):
                if not why.startswith("disabled"):
                    continue
                if enable_disabled:
                    _set_enabled(source, name)
                    out.lines.append(f"turned {name} back on ({why})")
                else:
                    out.lines.append(f"{name} is disabled by you; `probe wizard` turns it back on")
            broken = {name: why for name, why in unusable_plugins(source).items()
                      if enable_disabled or not why.startswith("disabled")}
            gone = [name for name, why in broken.items() if why == "its files are gone"]
            if gone and reinstall:
                from probe.cli import integration_reinstall

                try:
                    integration_reinstall._hook_repair(source)  # noqa: SLF001 -- the stock reinstall, with its backups
                    out.lines.append(f"reinstalled {', '.join(gone)} (its files were gone)")
                except Exception as exc:  # noqa: BLE001
                    out.problems.append(f"could not reinstall {', '.join(gone)}: {exc}"[:400])
                broken = {name: why for name, why in unusable_plugins(source).items()
                          if enable_disabled or not why.startswith("disabled")}
        for name, why in broken.items():
            out.problems.append(f"{name} cannot work: {why}")
    except Exception as exc:  # noqa: BLE001 -- said, never a crash of the install
        out.problems.append(f"the integrations check failed: {type(exc).__name__}: {exc}"[:400])
    if codex_before is not None and codex_hooks_digest() != codex_before:
        out.hooks_changed = True
        out.lines.append(CODEX_HOOKS_LINE)
    return out
