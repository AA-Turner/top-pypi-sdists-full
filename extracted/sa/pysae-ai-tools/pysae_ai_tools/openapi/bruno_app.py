"""Integrate a generated Bruno collection with the locally installed Bruno app.

Bruno keeps its state under an Electron ``userData`` directory (``bruno``):
per-platform, ``~/.config/bruno`` (Linux), ``~/Library/Application Support/bruno``
(macOS) or ``%APPDATA%/bruno`` (Windows). Three files matter here:

- ``ui-state-snapshot.json`` — records ``activeWorkspacePath`` (the workspace the
  sidebar currently shows).
- ``<workspace>/workspace.yml`` — the OpenCollection workspace manifest whose
  ``collections:`` list is the source of truth for what Bruno mounts. A
  collection only appears once it is declared there.
- ``preferences.json`` — holds ``preferences.request.oauth2.useSystemBrowser``.

Bruno watches ``workspace.yml`` (chokidar) and reloads the sidebar live, so
registering a collection while Bruno is running takes effect without a restart.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml

# Bruno's OAuth2 redirect when the system browser is used: the IdP redirects to
# this custom scheme and the OS routes it back into the app (deep link), instead
# of the built-in browser intercepting a localhost callback.
SYSTEM_BROWSER_CALLBACK_URL = "bruno://app/oauth2/callback"


def bruno_config_dir() -> Path | None:
    """Return Bruno's Electron userData directory, or None if it does not exist."""
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    elif os.name == "nt":
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME")
        base = Path(xdg) if xdg else Path.home() / ".config"
    config_dir = base / "bruno"
    return config_dir if config_dir.is_dir() else None


def _read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file written by an external tool, tolerant of odd encodings."""
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    return data if isinstance(data, dict) else {}


def active_workspace_path(config_dir: Path) -> Path | None:
    """Resolve the active Bruno workspace directory.

    Prefers ``ui-state-snapshot.json``'s ``activeWorkspacePath``, falls back to
    the configured default workspace, then to the built-in ``default-workspace``.
    """
    snapshot = config_dir / "ui-state-snapshot.json"
    if snapshot.is_file():
        try:
            active = _read_json(snapshot).get("activeWorkspacePath")
        except (ValueError, OSError):
            active = None
        if isinstance(active, str) and (Path(active) / "workspace.yml").is_file():
            return Path(active)

    prefs = config_dir / "preferences.json"
    if prefs.is_file():
        try:
            general = _read_json(prefs).get("preferences", {}).get("general", {})
            default = general.get("defaultWorkspacePath") if isinstance(general, dict) else None
        except (ValueError, OSError, AttributeError):
            default = None
        if isinstance(default, str) and (Path(default) / "workspace.yml").is_file():
            return Path(default)

    fallback = config_dir / "default-workspace"
    return fallback if (fallback / "workspace.yml").is_file() else None


def _quote_yaml_value(value: str) -> str:
    """Match Bruno's ``quoteYamlValue``: always double-quoted, backslash/quote escaped."""
    if value == "":
        return '""'
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _render_workspace_yaml(config: dict[str, Any]) -> str:
    """Serialise a workspace config the way Bruno's ``generateYamlContent`` does."""
    info = config.get("info")
    if not isinstance(info, dict):
        info = {}
    name = info.get("name") or config.get("name") or "Untitled Workspace"
    wtype = info.get("type") or config.get("type") or "workspace"

    lines = [
        f"opencollection: {config.get('opencollection') or '1.0.0'}",
        "info:",
        f"  name: {_quote_yaml_value(str(name))}",
        f"  type: {wtype}",
        "",
        "collections:",
    ]
    for collection in config.get("collections") or []:
        if not isinstance(collection, dict) or not collection.get("name") or not collection.get("path"):
            continue
        lines.append(f"  - name: {_quote_yaml_value(str(collection['name']))}")
        lines.append(f"    path: {_quote_yaml_value(str(collection['path']))}")
        if collection.get("remote"):
            lines.append(f"    remote: {_quote_yaml_value(str(collection['remote']))}")
    lines.append("")

    lines.append("specs:")
    for spec in config.get("specs") or []:
        if not isinstance(spec, dict) or not spec.get("name") or not spec.get("path"):
            continue
        lines.append(f"  - name: {_quote_yaml_value(str(spec['name']))}")
        lines.append(f"    path: {_quote_yaml_value(str(spec['path']))}")
    lines.append("")

    docs = config.get("docs") or ""
    lines.append(f"docs: {_quote_yaml_value(str(docs))}" if docs else "docs: ''")
    lines.append("")
    return "\n".join(lines)


def register_collection_in_workspace(workspace_path: Path, name: str, collection_dir: Path) -> bool:
    """Add a collection to a workspace's ``workspace.yml``. Returns True if newly added.

    Idempotent: an entry with the same resolved path is left untouched.
    """
    workspace_file = workspace_path / "workspace.yml"
    if not workspace_file.is_file():
        raise FileNotFoundError(f"Not a Bruno workspace (no workspace.yml): {workspace_path}")

    loaded = yaml.safe_load(workspace_file.read_text(encoding="utf-8", errors="replace"))
    config: dict[str, Any] = loaded if isinstance(loaded, dict) else {}
    collections = config.get("collections")
    if not isinstance(collections, list):
        collections = []
        config["collections"] = collections

    target = os.path.normpath(str(collection_dir.resolve())).replace("\\", "/")
    for entry in collections:
        if isinstance(entry, dict) and entry.get("path"):
            existing = os.path.normpath(str(entry["path"])).replace("\\", "/")
            if existing == target:
                return False

    collections.append({"name": name, "path": str(collection_dir.resolve())})
    workspace_file.write_text(_render_workspace_yaml(config), encoding="utf-8")
    return True


def set_system_browser(config_dir: Path, enabled: bool) -> bool:
    """Toggle ``preferences.request.oauth2.useSystemBrowser``. Returns True if changed."""
    prefs_file = config_dir / "preferences.json"
    if not prefs_file.is_file():
        return False

    data = _read_json(prefs_file)
    preferences = data.setdefault("preferences", {})
    request = preferences.setdefault("request", {})
    oauth2 = request.setdefault("oauth2", {})
    if oauth2.get("useSystemBrowser") == enabled:
        return False

    oauth2["useSystemBrowser"] = enabled
    prefs_file.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n", encoding="utf-8")
    return True
