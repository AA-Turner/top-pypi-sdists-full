"""Probe's traces in each coding agent's own config, found and removed (clean-uninstall plan U-T1, U-T7).

`probe uninstall` removes Probe from EVERY agent that carries any trace of it,
whether or not the agent's binary is on PATH (a laptop that uninstalled
Claude Code before Probe still has Probe's plugin records, rules block and
skills under `~/.claude`). Each agent is a registry row (`probe.harness`);
what differs between them is the record its plugins live in:

    hook-plugin agents with a marketplace CLI (Claude Code, Codex): the agent's
        own `plugin uninstall` / `plugin remove` and `plugin marketplace remove`
        when its binary runs; then, whatever is left (no binary, or a CLI that
        left a record), file edits that remove ONLY Probe's entries: Claude
        Code's install ledger, known marketplaces, `enabledPlugins`, marketplace
        clone and plugin cache; Codex's `[plugins."...@research-os-agent"]`,
        `[marketplaces.research-os-agent]`, `[hooks.state."probe-research..."]`
        and `[mcp_servers.probe-research]` tables, its clone and its cache
    Kimi Code: its plugin list (`kimi_config`, a file edit either way)
    pi: its settings.json package entry and pi's git clone of the mirror

and, for every agent: the rules + team-note block in its global instruction
file, Probe's skill copies, the status-line segment (the command it wrapped
put back) with Probe's renderer and `.probe-backup`, and the reasoning-summary
setting Probe turned on. Nothing here creates a file: a missing folder is a
trace that is not there. Capture's tap state folders and the credentials go
with the state (`uninstall.py`), after the server was told.

Codex's own trust records of Probe's hooks (`$CODEX_HOME/.hook-trust/<id>`,
one per approved hooks.json) go too: exactly the ones Probe's approval made, as
it recorded them (`codex_hooks.trust_records`), while unchanged. And once every
agent is done, `remove_hollow` takes what Probe's install left that now holds
nothing: an agent's empty `skills/`, Claude Code's plugin ledger and known
marketplaces when no other plugin or marketplace is left, a settings.json or
config.toml of empty structures only, and the empty folders around them
(`.kimi-code/plugins`, `.kimi-code` itself).

`traces()` is what U-T1 records in the plan (`agent_edits`) and what a rerun
finds left; `remove()` is U-T7. Both never raise.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
from pathlib import Path

from probe.cli import plugin_cli

#: Plugins of Probe's that an earlier release installed under another name.
RETIRED_PLUGINS = ("prbe-cc-tap-plugin", "prbe-codex-tap-plugin")
BACKUP_SUFFIX = ".probe-backup"


def _names():
    from probe.cli import capabilities

    return (capabilities.TRACKING_PLUGIN_NAME, capabilities.DAEMON_PLUGIN_NAME, capabilities.TAP_PLUGIN_NAME)


def _marketplace() -> str:
    from probe.cli import capabilities

    return capabilities.MARKETPLACE


def probe_plugin_id(plugin_id: object) -> bool:
    """Is `<plugin>@<marketplace>` one of Probe's (current or retired)?"""
    if not isinstance(plugin_id, str):
        return False
    name, _, marketplace = plugin_id.partition("@")
    return (name in _names() and marketplace == _marketplace()) or name in RETIRED_PLUGINS


def _harnesses():
    from probe.harness import get_registry

    return [h for h in get_registry().all() if h.installable or h.captured]


def _exists(path: Path) -> bool:
    return os.path.lexists(path)


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _write_json(path: Path, data: object) -> None:
    from probe.sdk.durable import write_text_atomic

    target = Path(os.path.realpath(path))  # a dotfile manager's symlink is written through
    write_text_atomic(target, json.dumps(data, indent=2) + "\n", keep_mode=True)


# -- Claude Code ---------------------------------------------------------------------


def _claude_dirs() -> dict:
    from probe.cli.capabilities import claude_plugin_ledger

    ledger = claude_plugin_ledger()
    plugins = ledger.parent
    from probe.cli import statusline

    return {
        "ledger": ledger,
        "known": plugins / "known_marketplaces.json",
        "clone": plugins / "marketplaces" / _marketplace(),
        "cache": plugins / "cache" / _marketplace(),
        "settings": statusline.settings_path(),
    }


def _claude_ledger_ids(ledger: Path) -> list[str]:
    data = _read_json(ledger)
    table = data.get("plugins") if isinstance(data, dict) else None
    return [key for key in table if probe_plugin_id(key)] if isinstance(table, dict) else []


def _claude_retired_installs(ledger: Path) -> list[Path]:
    """Where the ledger says a retired Probe plugin's copy is (its own cache)."""
    data = _read_json(ledger)
    table = data.get("plugins") if isinstance(data, dict) else None
    found = []
    for key, entries in (table or {}).items() if isinstance(table, dict) else []:
        if not (isinstance(key, str) and key.partition("@")[0] in RETIRED_PLUGINS and isinstance(entries, list)):
            continue
        for entry in entries:
            path = entry.get("installPath") if isinstance(entry, dict) else None
            if isinstance(path, str) and "/plugins/cache/" in path.replace(os.sep, "/"):
                found.append(Path(path))
    return found


def _claude_enabled(settings: Path) -> list[str]:
    data = _read_json(settings)
    table = data.get("enabledPlugins") if isinstance(data, dict) else None
    return [key for key in table if probe_plugin_id(key)] if isinstance(table, dict) else []


def _claude_traces(found: dict) -> None:
    dirs = _claude_dirs()
    ids = sorted(set(_claude_ledger_ids(dirs["ledger"])) | set(_claude_enabled(dirs["settings"])))
    if ids:
        found["plugins"] = ids
    known = _read_json(dirs["known"])
    marketplace = [str(p) for p in (dirs["clone"], dirs["cache"]) if _exists(p)]
    if isinstance(known, dict) and _marketplace() in known:
        marketplace.append(str(dirs["known"]))
    if marketplace:
        found["marketplace"] = marketplace


def _claude_remove(lines: list[str]) -> None:
    dirs = _claude_dirs()
    ledger = dirs["ledger"]
    retired = _claude_retired_installs(ledger)
    data = _read_json(ledger)
    if isinstance(data, dict) and isinstance(data.get("plugins"), dict):
        kept = {k: v for k, v in data["plugins"].items() if not probe_plugin_id(k)}
        if len(kept) != len(data["plugins"]):
            data["plugins"] = kept
            _write_json(ledger, data)
    known = _read_json(dirs["known"])
    if isinstance(known, dict) and _marketplace() in known:
        known.pop(_marketplace())
        _write_json(dirs["known"], known)
    settings = _read_json(dirs["settings"])
    changed = False
    if isinstance(settings, dict) and isinstance(settings.get("enabledPlugins"), dict):
        kept = {k: v for k, v in settings["enabledPlugins"].items() if not probe_plugin_id(k)}
        if len(kept) != len(settings["enabledPlugins"]):
            if kept:
                settings["enabledPlugins"] = kept
            else:
                settings.pop("enabledPlugins")
            changed = True
    if isinstance(settings, dict) and isinstance(settings.get("extraKnownMarketplaces"), dict) \
            and _marketplace() in settings["extraKnownMarketplaces"]:
        settings["extraKnownMarketplaces"].pop(_marketplace())
        if not settings["extraKnownMarketplaces"]:
            settings.pop("extraKnownMarketplaces")
        changed = True
    if changed:
        _write_json(dirs["settings"], settings)
    for folder in (dirs["clone"], dirs["cache"], *retired):
        _rmtree(folder, lines)


# -- Codex ---------------------------------------------------------------------------


def _toml_key_path(line: str) -> list[str] | None:
    """`[a."b c".d]` -> ["a", "b c", "d"]; None for anything that is not a
    plain table header (an array of tables, a value line)."""
    text = line.strip()
    if not text.startswith("[") or text.startswith("[["):
        return None
    close = _closing_bracket(text)
    if close is None:
        return None
    inner, rest = text[1:close], text[close + 1 :].strip()
    if rest and not rest.startswith("#"):
        return None
    parts, current, quote, index = [], "", None, 0
    while index < len(inner):
        char = inner[index]
        if quote:
            if char == "\\" and quote == '"' and index + 1 < len(inner):
                current += inner[index + 1]
                index += 2
                continue
            if char == quote:
                quote = None
            else:
                current += char
        elif char in "\"'":
            quote = char
        elif char == ".":
            parts.append(current.strip())
            current = ""
        else:
            current += char
        index += 1
    if quote:
        return None
    parts.append(current.strip())
    return parts if all(parts) else None


def _closing_bracket(text: str) -> int | None:
    quote = None
    for index, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == "]" and index:
            return index
    return None


def codex_probe_table(keys: list[str]) -> bool:
    """Is this config.toml table (or a sub-table of one) Probe's?"""
    from probe.cli.capabilities import CODEX_MCP_NAME
    from probe.cli.codex_hooks import PROBE_PLUGINS

    if len(keys) >= 2 and keys[0] == "plugins" and probe_plugin_id(keys[1]):
        return True
    if len(keys) >= 2 and keys[0] == "marketplaces" and keys[1] == _marketplace():
        return True
    if len(keys) >= 2 and keys[0] == "mcp_servers" and keys[1] == CODEX_MCP_NAME:
        return True
    if len(keys) >= 3 and keys[:2] == ["hooks", "state"]:
        head = keys[2].split("@", 1)[0].split(":", 1)[0]
        return head in PROBE_PLUGINS or f"@{_marketplace()}" in keys[2]
    return False


def codex_probe_spans(text: str) -> list[tuple[int, int, list[str]]]:
    """(start, end, key path) of every Probe table in a config.toml's lines."""
    lines = text.splitlines(keepends=True)
    # Every header bounds the table before it; an array of tables (`[[x]]`)
    # bounds one too, and is never Probe's.
    headers: list[tuple[int, list[str] | None]] = []
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("[["):
            headers.append((index, None))
        elif stripped.startswith("["):
            keys = _toml_key_path(line)
            if keys is not None:
                headers.append((index, keys))
    spans = []
    for position, (start, keys) in enumerate(headers):
        end = headers[position + 1][0] if position + 1 < len(headers) else len(lines)
        if keys is not None and codex_probe_table(keys):
            spans.append((start, end, keys))
    return spans


def _codex_dirs() -> dict:
    from probe.cli import codex_config

    home = codex_config.codex_home()
    return {
        "config": codex_config.config_path(),
        "clone": home / ".tmp" / "marketplaces" / _marketplace(),
        "cache": home / "plugins" / "cache" / _marketplace(),
    }


def _codex_trust_dir() -> Path:
    from probe.cli import codex_config

    return codex_config.codex_home() / ".hook-trust"


def codex_trust_records() -> list[Path]:
    """Codex's trust records (`.hook-trust/<id>`) that Probe's own hook
    approval made, as it recorded them (`codex_hooks.trust_records`), each
    only while its content is still what was recorded. An approval from
    before that record existed left none: those records are left alone."""
    import hashlib

    from probe.cli import codex_hooks

    found = []
    for raw, digest in sorted(codex_hooks.trust_records().items()):
        path = Path(raw)
        if path.parent.name != codex_hooks.TRUST_DIRNAME or path.is_symlink() or not path.is_file():
            continue
        with contextlib.suppress(OSError):
            with path.open("rb") as handle:
                if hashlib.sha256(handle.read(1 << 20)).hexdigest() == digest:
                    found.append(path)
    return found


def _codex_remove_trust(lines: list[str]) -> None:
    """The trust records Probe's approval made (`codex_trust_records`)."""
    records = codex_trust_records()
    for record in records:
        try:
            record.unlink()
        except OSError as exc:
            lines.append(f"! could not remove Codex's trust record of Probe's hooks {record}: {exc}")
    if records:
        lines.append(f"Removed Codex's trust records of Probe's hooks ({len(records)}).")
        for folder in {record.parent for record in records}:
            with contextlib.suppress(OSError):
                folder.rmdir()  # only when nothing else is in it


def _codex_traces(found: dict) -> None:
    dirs = _codex_dirs()
    try:
        text = dirs["config"].read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        text = ""
    kinds = {"plugins": "plugins", "marketplaces": "marketplace", "mcp_servers": "mcp", "hooks": "hook_approvals"}
    for _start, _end, keys in codex_probe_spans(text):
        name = kinds.get(keys[0], keys[0])
        # A plugin by its `<plugin>@<marketplace>` id (what `codex plugin remove` takes).
        label = keys[1] if name == "plugins" else ".".join(keys)
        found.setdefault(name, [])
        if label not in found[name]:
            found[name].append(label)
    folders = [str(p) for p in (dirs["clone"], dirs["cache"]) if _exists(p)]
    if folders:
        found.setdefault("marketplace", []).extend(folders)
    trust = [str(p) for p in codex_trust_records()]
    if trust:
        found["hook_trust"] = trust


def _codex_remove(lines: list[str]) -> None:
    from probe._compat import tomllib
    from probe.sdk.durable import write_text_atomic

    dirs = _codex_dirs()
    _codex_remove_trust(lines)
    target = Path(os.path.realpath(dirs["config"]))
    try:
        original = target.read_bytes().decode("utf-8")
    except FileNotFoundError:
        original = ""
    except (OSError, UnicodeDecodeError) as exc:
        lines.append(f"! could not read {dirs['config']} ({exc}); remove Probe's tables from it by hand.")
        original = ""
    spans = codex_probe_spans(original)
    if spans:
        try:
            tomllib.loads(original)
        except tomllib.TOMLDecodeError as exc:
            lines.append(f"! left {dirs['config']} alone: it is not valid TOML ({exc}); remove Probe's tables by hand.")
            spans = []
    if spans:
        kept = original.splitlines(keepends=True)
        for start, end, _keys in sorted(spans, reverse=True):
            del kept[start:end]
        updated = "".join(kept)
        try:
            tomllib.loads(updated)
        except tomllib.TOMLDecodeError as exc:
            lines.append(f"! left {dirs['config']} alone: removing Probe's tables would break it ({exc}).")
        else:
            write_text_atomic(target, updated, mode=0o600, keep_mode=True)
            lines.append(f"Removed Probe's entries from {dirs['config']}.")
    for folder in (dirs["clone"], dirs["cache"]):
        _rmtree(folder, lines)


# -- Kimi Code -------------------------------------------------------------------------


def _kimi_traces(found: dict) -> None:
    from probe.cli import kimi_config

    data = _read_json(kimi_config.installed_path())
    plugins = data.get("plugins") if isinstance(data, dict) else None
    ids = sorted({p.get("id") for p in plugins or [] if isinstance(p, dict) and p.get("id") in kimi_config.PLUGIN_IDS})
    if ids:
        found["plugins"] = ids
    copies = []
    with contextlib.suppress(OSError):
        copies = [str(p) for p in kimi_config.managed_root().iterdir()
                  if p.name.split("@", 1)[0] in kimi_config.PLUGIN_IDS]
    lock = kimi_config.managed_root().parent / ".probe-installed.lock"
    if _exists(lock):
        copies.append(str(lock))
    if copies:
        found["plugin_copies"] = copies


def _kimi_remove(lines: list[str]) -> None:
    from probe.cli import kimi_config

    plugins_dir = kimi_config.managed_root().parent
    if not plugins_dir.is_dir():
        return  # never `kimi_config._locked`'s mkdir on an agent with no plugins
    for plugin_id in kimi_config.PLUGIN_IDS:
        result = kimi_config.uninstall_plugin(plugin_id)
        if not result.ok:
            lines.append(f"! {result.detail}")
    with contextlib.suppress(OSError):
        (plugins_dir / ".probe-installed.lock").unlink()


# -- pi --------------------------------------------------------------------------------


def _pi_id() -> str:
    from probe.cli import pi_config

    return pi_config.HARNESS_ID


def _pi_clone() -> Path:
    from probe.cli import pi_config

    host, repo = pi_config._MIRROR_IDENTITY  # noqa: SLF001 - the identity pi's clone is filed under
    return pi_config.pi_agent_dir() / "git" / host / Path(*repo.split("/"))


def _pi_legacy_link() -> Path:
    from probe.cli import pi_config

    return pi_config.pi_agent_dir() / Path(*pi_config._LEGACY_EXTENSION_RELATIVE)  # noqa: SLF001


def _pi_traces(found: dict) -> None:
    from probe.cli import pi_config

    try:
        if pi_config.package_entry_installed():
            found["plugins"] = [pi_config.PACKAGE_NAME]
    except Exception:  # noqa: BLE001 - an unreadable settings file is no trace we can remove
        pass
    folders = [str(p) for p in (_pi_clone(), _pi_legacy_link()) if _exists(p)]
    if folders:
        found["plugin_copies"] = folders


def _pi_remove(lines: list[str]) -> None:
    from probe.cli import pi_config

    try:
        if pi_config.package_entry_installed():
            removal = pi_config.remove_package_entry()
            if not removal.ok:
                lines.append(f"! pi: could not remove Probe's package entry: {removal.detail}")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"! pi: could not read its settings ({exc}); remove Probe's package entry by hand.")
    clone = _pi_clone()
    _rmtree(clone, lines)
    # The folders pi made only for this clone, up to (not including) its `git/`.
    for parent in list(clone.parents)[: len(Path(*pi_config._MIRROR_IDENTITY[1].split("/")).parts)]:  # noqa: SLF001
        with contextlib.suppress(OSError):
            parent.rmdir()
    legacy = _pi_legacy_link()
    if legacy.is_symlink():
        with contextlib.suppress(OSError):
            legacy.unlink()


# -- every agent -----------------------------------------------------------------------


def _rmtree(path: Path, lines: list[str]) -> None:
    if not _exists(path):
        return
    try:
        if path.is_symlink() or not path.is_dir():
            path.unlink()
        else:
            shutil.rmtree(path)
    except OSError as exc:
        lines.append(f"! could not remove {path}: {exc}")
        return
    _prune(path)


def _prune(path: Path) -> None:
    """The empty folders a removed path leaves (`plugins/marketplaces/`
    around Probe's clone), up to the agent's own home folder."""
    from probe.cli.uninstall import prune_empty_parents

    homes = [h.home_dir() for h in _harnesses() if h.home_dir() is not None]
    stop = next((home for home in homes if home in path.parents), None)
    if stop is not None:
        prune_empty_parents(path, stop)


def _rules_path(harness) -> Path | None:
    from probe.cli import agent_rules

    try:
        return agent_rules.memory_path(harness.id)
    except Exception:  # noqa: BLE001 - a row with no instruction file
        return None


def _statusline_files(harness) -> list[Path]:
    """The slot file's `.probe-backup` and Probe's renderer folder."""
    from probe.cli import statusline
    from probe.harness import registry as reg

    if harness.statusline == reg.STATUSLINE_CLAUDE_SETTINGS:
        slot, renderer = statusline.settings_path(), statusline.install_dir()
    elif harness.statusline == reg.STATUSLINE_KIMI_TUI_TOML:
        slot, renderer = statusline.kimi_tui_path(), statusline.kimi_install_dir()
    else:
        return []
    return [slot.with_name(slot.name + BACKUP_SUFFIX), renderer]


def _skills(harness) -> tuple[Path | None, list[str]]:
    from probe import root_skills_core as core
    from probe.cli import root_skills

    root = root_skills.skills_root(harness.id)
    if root is None or not root.is_dir():
        return root, []
    found = [str(p) for p in sorted(root.iterdir()) if p.is_dir() and core.is_ours(p)]
    if _exists(root / ".probe-sync.lock"):
        found.append(str(root / ".probe-sync.lock"))
    return root, found


def _tap_dirs(harness) -> list[Path]:
    capture = harness.capture
    if capture is None:
        return []
    override = (os.environ.get(capture.plugin_dir_env) or "").strip()
    folders = [Path(override)] if override else []
    folders.append(Path.home() / capture.plugin_dir)
    if capture.legacy_plugin_dir:
        folders.append(Path.home() / capture.legacy_plugin_dir)
    return list(dict.fromkeys(folders))


def tap_dirs() -> list[Path]:
    """Every agent's capture tap state folder that exists (current, override
    and legacy): `.token`, `.config`, `state.db`, `logs/`, `.disabled`."""
    return [p for h in _harnesses() for p in _tap_dirs(h) if _exists(p)]


def traces(harness) -> dict:
    """{trace: [what, ...]} of Probe in one agent's config; {} when none."""
    from probe.cli import agent_rules, reasoning_summaries, statusline

    found: dict = {}
    agent = harness.id
    with contextlib.suppress(Exception):
        if agent == plugin_cli.CLAUDE:
            _claude_traces(found)
        elif agent == plugin_cli.CODEX:
            _codex_traces(found)
        elif agent == plugin_cli.KIMI:
            _kimi_traces(found)
        elif agent == _pi_id():
            _pi_traces(found)
    path = _rules_path(harness)
    if path is not None and (agent_rules.has_block(path, agent_rules.POINTER_BLOCK)
                             or agent_rules.has_block(path, agent_rules.NOTE_BLOCK)):
        found["rules"] = [str(path)]
    with contextlib.suppress(Exception):
        _root, skills = _skills(harness)
        if skills:
            found["skills"] = skills
    with contextlib.suppress(Exception):
        shown = []
        if harness.statusline and statusline.installed_for(agent):
            shown.append(str(statusline.slot_path(agent)))
        shown += [str(p) for p in _statusline_files(harness) if _exists(p)]
        if shown:
            found["statusline"] = shown
    with contextlib.suppress(Exception):
        if agent in reasoning_summaries.SOURCES and agent in reasoning_summaries._claims():  # noqa: SLF001
            found["reasoning_summaries"] = [agent]
    taps = [str(p) for p in _tap_dirs(harness) if _exists(p)]
    if taps:
        found["capture"] = taps
    return found


def all_traces() -> dict:
    """{agent id: traces} for every agent with any trace of Probe."""
    out = {}
    for harness in _harnesses():
        found = traces(harness)
        if found:
            out[harness.id] = found
    return out


def remove(harness) -> list[str]:
    """Take Probe out of one agent's config (U-T7). Lines; `! ` for what was left."""
    from probe.cli import agent_rules, reasoning_summaries, statusline
    from probe.cli.capabilities import agent_target

    lines: list[str] = []
    agent = harness.id
    files = _statusline_files(harness)
    # Before anything below writes the slot file (the reasoning undo backs it
    # up first): no backup means Probe made that file itself.
    backup_before = files[0].exists() if files else False
    with agent_target(agent):
        if agent == plugin_cli.CODEX:
            # First, while Codex's own `plugin remove` has not run yet: the
            # trust records Probe's approval made, as it recorded them.
            with contextlib.suppress(Exception):
                _codex_remove_trust(lines)
        if agent in (plugin_cli.CLAUDE, plugin_cli.CODEX) and plugin_cli.available(agent):
            # The agent's own CLI first: it knows its records best.
            for plugin_id in traces(harness).get("plugins", []):
                if "@" not in plugin_id:
                    continue
                done = plugin_cli.uninstall(agent, plugin_id)
                if not done.ok and "not found" not in (done.detail or "").lower():
                    lines.append(f"  ({plugin_cli.binary_name(agent)} could not remove {plugin_id}: {done.detail};"
                                 " removing its record instead)")
            if traces(harness).get("marketplace"):
                with contextlib.suppress(Exception):
                    plugin_cli.run(agent, ["plugin", "marketplace", "remove", _marketplace()],
                                   timeout=60.0)
        try:
            if agent == plugin_cli.CLAUDE:
                _claude_remove(lines)
            elif agent == plugin_cli.CODEX:
                _codex_remove(lines)
            elif agent == plugin_cli.KIMI:
                _kimi_remove(lines)
            elif agent == _pi_id():
                _pi_remove(lines)
        except Exception as exc:  # noqa: BLE001 - one agent's record never stops the rest
            lines.append(f"! could not remove Probe's plugins from {harness.label}: {exc}")
        path = _rules_path(harness)
        if path is not None and path.exists():
            try:
                if agent_rules.remove_all(path):
                    lines.append(f"Removed the Probe block from {path}.")
                    # Probe's block was all it held: a file empty BEFORE Probe
                    # (no block taken out of it here) is the person's, and stays.
                    with contextlib.suppress(OSError):
                        if path.is_file() and not path.read_text(encoding="utf-8").strip():
                            path.unlink()
            except agent_rules.DamagedBlock as exc:
                lines.append(f"! left {path} alone: {exc}; delete the probe-research block by hand.")
            except (OSError, UnicodeDecodeError) as exc:
                lines.append(f"! could not update {path}: {exc}")
        with contextlib.suppress(Exception):
            root, skills = _skills(harness)
            if skills:
                from probe.cli import root_skills

                lines.extend(root_skills.remove(agent))
                if root is not None:
                    with contextlib.suppress(OSError):
                        (root / ".probe-sync.lock").unlink()
        if agent in reasoning_summaries.SOURCES:
            lines.extend(reasoning_summaries.undo_for_agent(agent))
        restored = True
        if harness.statusline:
            slot = statusline.slot_path(agent)
            try:
                result = statusline.uninstall_for(agent)
                if result.get("removed"):
                    lines.append("Status line: back to the command you had before." if result.get("restored")
                                 else "Status line: removed.")
            except (OSError, ValueError) as exc:
                restored = False
                lines.append(f"! left the status line in {slot} ({exc}); remove Probe's command by hand.")
            # A settings file Probe itself made (no backup was ever taken of it)
            # and that holds nothing now is Probe's to remove.
            with contextlib.suppress(OSError, ValueError):
                if restored and not backup_before and slot.is_file() \
                        and slot.read_text(encoding="utf-8").strip() in ("", "{}"):
                    slot.unlink()
        # The `.probe-backup` and the renderer go only once the status line no
        # longer needs them: a slot left as it was still runs the renderer, and
        # the backup is the person's way back.
        if restored:
            for path in files:
                _rmtree(path, lines)
    left = {k: v for k, v in traces(harness).items() if k != "capture"}
    if left:
        lines.append(f"! {harness.label}: still has Probe's {', '.join(sorted(left))}: "
                     f"{'; '.join(str(x) for v in left.values() for x in v[:2])}")
    return lines


# -- what Probe's install left that now holds nothing ---------------------------------


#: Keys Claude Code's plugin machinery writes into settings.json: a file left
#: holding only these, empty, is the trace of a plugin install and nothing else.
_CLAUDE_PLUGIN_SETTINGS = frozenset({"enabledPlugins", "extraKnownMarketplaces"})


#: The tables Probe's entries live under in Codex's config.toml: left with no
#: key of their own (and `hooks` with nothing but an empty `state`), they are
#: the trace of Probe's install and nothing else.
_CODEX_PROBE_TABLES = frozenset({"plugins", "marketplaces", "mcp_servers", "hooks"})


def _empty(value: object) -> bool:
    """An empty table or list. A key in it, whosever it is, is content."""
    return isinstance(value, (dict, list)) and not value


def _linked(path: Path, home: Path) -> bool:
    """Is `path`, or a folder between it and the agent's `home` (that one
    included), a link: a dotfile manager's file, a symlinked `~/.claude`?
    Such a file is the person's setup, never removed here."""
    stops = {home, Path.home()}
    for part in (path, *path.parents):
        if part.is_symlink():
            return True
        if part in stops:
            return False
    return False


def _claude_home() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude"))


def _unlink(path: Path, lines: list[str], why: str) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        return
    except OSError as exc:
        lines.append(f"! could not remove {path}: {exc}")
        return
    lines.append(f"Removed {path} ({why}).")


def _rmdir_empty(*folders: Path) -> None:
    """Each folder, in order, only while it is empty (never through a link)."""
    for folder in folders:
        if folder.is_symlink():
            return
        try:
            folder.rmdir()
        except OSError:
            return


def _claude_hollow(lines: list[str]) -> None:
    dirs = _claude_dirs()
    home = _claude_home()
    ledger_path, known_path = dirs["ledger"], dirs["known"]
    plugins = ledger_path.parent
    ledger, known = _read_json(ledger_path), _read_json(known_path)
    ledger_hollow = not _exists(ledger_path) or (
        isinstance(ledger, dict) and set(ledger) <= {"version", "plugins"} and _empty(ledger.get("plugins", {})))
    known_hollow = not _exists(known_path) or (isinstance(known, dict) and not known)
    others = []
    with contextlib.suppress(OSError):
        others = [entry.name for entry in (plugins / "marketplaces").iterdir() if entry.name != _marketplace()]
    # The ledger goes only when no other plugin AND no other marketplace is
    # left: in known_marketplaces.json, or as a clone under `marketplaces/`.
    if ledger_hollow and known_hollow and not others:
        for path in (ledger_path, known_path):
            if _exists(path) and not _linked(path, home):
                _unlink(path, lines, "no plugin or marketplace is left in it")
    _rmdir_empty(plugins / "marketplaces")
    _rmdir_empty(plugins / "cache")
    _rmdir_empty(plugins)
    settings = home / "settings.json"  # not `settings_path()`, which follows a link
    data = _read_json(settings)
    if isinstance(data, dict) and set(data) <= _CLAUDE_PLUGIN_SETTINGS and all(_empty(v) for v in data.values()) \
            and not _linked(settings, home):
        _unlink(settings, lines, "it held only empty plugin settings" if data else "nothing is left in it")


def _codex_hollow(lines: list[str]) -> None:
    from probe._compat import tomllib
    from probe.cli import codex_config

    config = _codex_dirs()["config"]
    if not config.is_file() or _linked(config, codex_config.codex_home()):
        return
    try:
        text = config.read_text(encoding="utf-8")
        data = tomllib.loads(text)
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return
    hollow = all(
        key in _CODEX_PROBE_TABLES and isinstance(value, dict)
        and (all(sub == "state" and _empty(inner) for sub, inner in value.items()) if key == "hooks" else not value)
        for key, value in data.items())
    # Empty, or bare table headers: a comment or a key is the person's, and stays.
    if hollow and all(line.strip().startswith("[") for line in text.splitlines() if line.strip()):
        _unlink(config, lines, "nothing is left in it")


def _kimi_hollow() -> None:
    from probe.cli import kimi_config

    home = kimi_config.kimi_home()
    _rmdir_empty(home / "plugins", home)


def remove_hollow() -> list[str]:
    """After every agent is done (U-T7): what Probe's install made that now
    holds nothing (see the module docstring). Never a file with anything of
    the person's in it. Lines; never raises."""
    lines: list[str] = []
    from probe.cli import root_skills

    for harness in _harnesses():
        with contextlib.suppress(Exception):
            root = root_skills.skills_root(harness.id)
            if root is not None:
                _rmdir_empty(root)
    for step in (_claude_hollow, _codex_hollow):
        try:
            step(lines)
        except Exception as exc:  # noqa: BLE001 - one agent's leftovers never stop the rest
            lines.append(f"! could not tidy {step.__name__}: {exc}")
    with contextlib.suppress(Exception):
        _kimi_hollow()
    return lines


__all__ = ["RETIRED_PLUGINS", "all_traces", "codex_probe_spans", "codex_trust_records", "probe_plugin_id", "remove",
           "remove_hollow", "tap_dirs", "traces"]
