"""Filesystem artifacts written by Runlayer hook installation."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping


def _environment_value(
    environment: Mapping[str, str],
    name: str,
    *,
    system: str,
) -> str | None:
    value = environment.get(name)
    if value is not None or system != "Windows":
        return value
    name_key = name.casefold()
    return next(
        (item for key, item in environment.items() if key.casefold() == name_key),
        None,
    )


def _override_root(
    environment: Mapping[str, str],
    name: str,
    *,
    home: Path,
    system: str,
) -> Path | None:
    value = _environment_value(environment, name, system=system)
    if not value:
        return None
    if value == "~":
        path = home
    elif value.startswith("~/") or value.startswith("~\\"):
        path = home / value[2:]
    else:
        path = Path(value)
    return path if path.is_absolute() else None


def runlayer_written_hook_artifact_paths(
    *,
    home: Path,
    system: str,
    environment: Mapping[str, str],
) -> frozenset[Path]:
    """Return user-path artifacts a Runlayer hook install can create or edit."""
    codex_roots = {home / ".codex"}
    copilot_roots = {home / ".copilot"}
    grok_roots = {home / ".grok"}
    copilot_override = _override_root(
        environment,
        "COPILOT_HOME",
        home=home,
        system=system,
    )
    if copilot_override is not None:
        copilot_roots.add(copilot_override)
    grok_override = _override_root(
        environment,
        "GROK_HOME",
        home=home,
        system=system,
    )
    if grok_override is not None:
        grok_roots.add(grok_override)

    if system == "Windows":
        devin_appdata = _environment_value(environment, "APPDATA", system=system)
        devin_root = (
            Path(devin_appdata) if devin_appdata else home / "AppData" / "Roaming"
        ) / "devin"
    else:
        devin_root = home / ".config" / "devin"

    if system == "Darwin":
        vscode_settings = (
            home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
        )
    elif system == "Windows":
        appdata = _environment_value(environment, "APPDATA", system=system)
        vscode_root = Path(appdata) if appdata else home / "AppData" / "Roaming"
        vscode_settings = vscode_root / "Code" / "User" / "settings.json"
    else:
        vscode_settings = home / ".config" / "Code" / "User" / "settings.json"

    artifacts = {
        home / ".cursor" / "hooks.json",
        home / ".hermes" / "config.yaml",
        home / ".copilot" / "hooks" / "runlayer.json",
        home / ".codeium" / "windsurf" / "hooks.json",
        devin_root / "config.json",
        vscode_settings,
    }
    for root in codex_roots:
        artifacts.add(root / "hooks.json")
        artifacts.add(root / "config.toml")
        if system == "Windows":
            artifacts.add(root / "managed_config.toml")
    for root in copilot_roots:
        artifacts.add(root / "settings.json")
    for root in grok_roots:
        artifacts.add(root / "hooks" / "runlayer.json")
    return frozenset(artifacts)


__all__ = ["runlayer_written_hook_artifact_paths"]
