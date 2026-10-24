#!/usr/bin/env python3
"""A stand-in for Claude Code's `claude plugin ...` commands (live-run harness only).

The live run (`live_run.py`) has no real Claude Code: no API key exists in this
repo's CI secrets. What the Probe updater needs from `claude` is its PLUGIN
MANAGER, and that is small and file-based, so this script plays it against a
local marketplace folder instead of a git repo:

    claude --version
    claude plugin marketplace add <dir>        copy <dir> to plugins/marketplaces/<name>/
    claude plugin marketplace update <name>    copy it again from where it was added
                                               (Claude Code: `git pull`)
    claude plugin install <plugin>@<market>    copy the marketplace's plugin folder to
    claude plugin update <plugin>@<market>     plugins/cache/<market>/<plugin>/<version>/
                                               and record it in installed_plugins.json
    claude plugin list [--json]

The layout is Claude Code's own: `$CLAUDE_CONFIG_DIR` (else `~/.claude`) /
plugins/{installed_plugins.json, known_marketplaces.json, marketplaces/, cache/},
`settings.json` `enabledPlugins`. Older version folders are kept, as Claude Code
keeps them for sessions that still run them.

Everything is derived from HOME, never from a harness variable: the Probe
service runs its update child with a clean environment (`ENV_ALLOWLIST`), and
that child is what calls this. Every call is appended to
`~/.live-run/claude-standin.jsonl` for the report.

Stdlib only.
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

VERSION_LINE = "2.1.140 (Claude Code; live-run stand-in)"
LEDGER_VERSION = 2


def _home() -> Path:
    return Path(os.environ.get("HOME") or os.path.expanduser("~"))


def config_dir() -> Path:
    raw = (os.environ.get("CLAUDE_CONFIG_DIR") or "").strip()
    return Path(os.path.expanduser(raw)) if raw else _home() / ".claude"


def plugins_dir() -> Path:
    return config_dir() / "plugins"


def ledger_path() -> Path:
    return plugins_dir() / "installed_plugins.json"


def known_path() -> Path:
    return plugins_dir() / "known_marketplaces.json"


def settings_path() -> Path:
    return config_dir() / "settings.json"


def log_path() -> Path:
    return _home() / ".live-run" / "claude-standin.jsonl"


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def _log(argv: list[str], code: int, note: str, started: float) -> None:
    with contextlib.suppress(OSError):
        log_path().parent.mkdir(parents=True, exist_ok=True)
        with log_path().open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "t": time.time(),
                        "argv": argv,
                        "exit": code,
                        "note": note,
                        "duration_s": round(time.time() - started, 3),
                        "ppid": os.getppid(),
                    }
                )
                + "\n"
            )


def _copytree(src: Path, dst: Path) -> None:
    """Copy a folder into place in one rename, so nobody sees half of it."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    staging = dst.with_name(f".{dst.name}.staging-{os.getpid()}")
    if staging.exists():
        shutil.rmtree(staging)
    shutil.copytree(src, staging, symlinks=True, ignore=shutil.ignore_patterns("__pycache__"))
    if dst.exists():
        shutil.rmtree(dst)
    os.replace(staging, dst)


def _marketplace_manifest(root: Path) -> dict:
    return _read_json(root / ".claude-plugin" / "marketplace.json", {})


def _plugin_version(folder: Path) -> str | None:
    data = _read_json(folder / ".claude-plugin" / "plugin.json", {})
    value = data.get("version") if isinstance(data, dict) else None
    return value if isinstance(value, str) and value else None


# -- marketplaces -------------------------------------------------------------


def marketplace_add(source: str) -> tuple[int, str]:
    src = Path(source).expanduser().resolve()
    manifest = _marketplace_manifest(src)
    name = manifest.get("name") if isinstance(manifest, dict) else None
    if not name:
        return 1, f"no .claude-plugin/marketplace.json with a name in {src}"
    location = plugins_dir() / "marketplaces" / name
    _copytree(src, location)
    known = _read_json(known_path(), {})
    known[name] = {
        "source": {"source": "directory", "path": str(src)},
        "installLocation": str(location),
        "lastUpdated": _now(),
    }
    _write_json(known_path(), known)
    return 0, f"Successfully added marketplace: {name}"


def marketplace_update(name: str) -> tuple[int, str]:
    known = _read_json(known_path(), {})
    entry = known.get(name)
    if not isinstance(entry, dict):
        return 1, f"Marketplace '{name}' not found"
    src = Path(entry["source"]["path"])
    location = Path(entry["installLocation"])
    if not (src / ".claude-plugin" / "marketplace.json").is_file():
        return 1, f"Marketplace source {src} is not readable"
    _copytree(src, location)
    entry["lastUpdated"] = _now()
    _write_json(known_path(), known)
    return 0, f"Successfully updated marketplace: {name}"


# -- plugins --------------------------------------------------------------------


def _split(plugin_id: str) -> tuple[str, str] | None:
    name, _, market = plugin_id.partition("@")
    return (name, market) if name and market else None


def _source_folder(name: str, market: str) -> Path | None:
    known = _read_json(known_path(), {})
    entry = known.get(market)
    if not isinstance(entry, dict):
        return None
    location = Path(entry["installLocation"])
    for plugin in _marketplace_manifest(location).get("plugins") or []:
        if isinstance(plugin, dict) and plugin.get("name") == name and isinstance(plugin.get("source"), str):
            return (location / plugin["source"]).resolve()
    return None


def _install(plugin_id: str, *, update: bool) -> tuple[int, str]:
    parts = _split(plugin_id)
    if parts is None:
        return 1, f"Plugin id must be <plugin>@<marketplace>, got {plugin_id!r}"
    name, market = parts
    source = _source_folder(name, market)
    if source is None or not source.is_dir():
        return 1, f'Plugin "{name}" not found in marketplace "{market}"'
    version = _plugin_version(source) or "unknown"
    ledger = _read_json(ledger_path(), {"version": LEDGER_VERSION, "plugins": {}})
    ledger.setdefault("version", LEDGER_VERSION)
    plugins = ledger.setdefault("plugins", {})
    entries = plugins.get(plugin_id) or []
    current = entries[0] if entries and isinstance(entries[0], dict) else None
    if update and current is None:
        return 1, f'Plugin "{name}" is not installed'
    if current is not None and current.get("version") == version and Path(current.get("installPath", "")).is_dir():
        return 0, f"✔ {name} is already at the latest version ({version})."
    target = plugins_dir() / "cache" / market / name / version
    _copytree(source, target)
    stamp = _now()
    record = {
        "scope": "user",
        "installPath": str(target),
        "version": version,
        "installedAt": (current or {}).get("installedAt", stamp),
        "lastUpdated": stamp,
        "gitCommitSha": "live-run",
    }
    plugins[plugin_id] = [record]
    _write_json(ledger_path(), ledger)
    settings = _read_json(settings_path(), {})
    settings.setdefault("enabledPlugins", {})[plugin_id] = True
    _write_json(settings_path(), settings)
    if current is None:
        return 0, f"✔ Successfully installed plugin: {name}@{market} (scope: user)"
    return 0, (
        f"✔ Plugin \"{name}\" updated from {current.get('version')} to {version} for scope user. "
        "Restart to apply changes."
    )


def plugin_list(as_json: bool) -> tuple[int, str]:
    ledger = _read_json(ledger_path(), {"plugins": {}})
    rows = []
    for plugin_id, entries in (ledger.get("plugins") or {}).items():
        for entry in entries or []:
            rows.append({"id": plugin_id, "version": entry.get("version"), "scope": entry.get("scope"),
                         "enabled": True, "installPath": entry.get("installPath")})
    if as_json:
        return 0, json.dumps(rows)
    return 0, "\n".join(f"{r['id']} {r['version']}" for r in rows) or "No plugins installed"


def main(argv: list[str]) -> int:
    started = time.time()
    code, out = 1, ""
    try:
        if argv[:1] in (["--version"], ["-v"]):
            code, out = 0, VERSION_LINE
        elif argv[:3] == ["plugin", "marketplace", "add"] and len(argv) >= 4:
            code, out = marketplace_add(argv[3])
        elif argv[:3] == ["plugin", "marketplace", "update"] and len(argv) >= 4:
            code, out = marketplace_update(argv[3])
        elif argv[:2] == ["plugin", "install"] and len(argv) >= 3:
            code, out = _install(argv[2], update=False)
        elif argv[:2] == ["plugin", "update"] and len(argv) >= 3:
            code, out = _install(argv[2], update=True)
        elif argv[:2] == ["plugin", "list"]:
            code, out = plugin_list("--json" in argv)
        else:
            code, out = 1, f"live-run stand-in: `claude {' '.join(argv)}` is not supported"
    except Exception as exc:  # noqa: BLE001 -- reported like a CLI error
        code, out = 1, f"live-run stand-in failed: {type(exc).__name__}: {exc}"
    stream = sys.stdout if code == 0 else sys.stderr
    if out:
        print(out, file=stream)
    _log(argv, code, out[:300], started)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
