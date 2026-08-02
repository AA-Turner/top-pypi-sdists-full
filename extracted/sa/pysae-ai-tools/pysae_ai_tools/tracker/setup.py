"""Migrate away the legacy activity-tracker hooks in Claude Code settings.

The tracker hooks — ``PostToolUse`` → ``pysae-ai-tools tracker hook`` and ``Stop`` →
``pysae-ai-tools tracker stop-hook`` — now ship with the Pysae plugin (``hooks/hooks.json``), so
they are no longer written into ``~/.claude/settings.json``. This module strips any legacy entry a
previous version left behind (including the historical ``activity_tracker`` command name) so it
does not fire twice next to the plugin's copy.

Usage:
    pysae-ai-tools tracker setup status
    pysae-ai-tools tracker setup install
    pysae-ai-tools tracker setup uninstall [--delete-logs]
"""

import json
import os
import platform
import shutil
from pathlib import Path

import typer

from .hook import LOG_DIR


def _settings_path() -> Path:
    """Return the Claude Code settings.json path for the current platform."""
    if platform.system() == "Windows":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "Claude" / "settings.json"
    return Path.home() / ".claude" / "settings.json"


SETTINGS_PATH = _settings_path()

# (event, command substring). The marker is loose on purpose: ``tracker hook`` also matches the
# historical ``activity_tracker hook`` (and likewise for the stop hook), so both name variants are
# migrated. ``tracker hook`` never matches ``tracker stop-hook`` — they live in different events.
_LEGACY_HOOKS: tuple[tuple[str, str], ...] = (
    ("PostToolUse", "tracker hook"),
    ("Stop", "tracker stop-hook"),
)

app = typer.Typer()


def _read_settings() -> dict[str, object]:
    """Read ~/.claude/settings.json, returning empty dict if missing."""
    if not SETTINGS_PATH.exists():
        return {}
    try:
        return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
    except (json.JSONDecodeError, OSError):
        return {}


def _write_settings(cfg: dict[str, object]) -> None:
    """Write ~/.claude/settings.json with pretty formatting."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _find_marker(cfg: dict[str, object], event: str, marker: str) -> bool:
    """True when a hook command under ``event`` contains ``marker``."""
    hooks = cfg.get("hooks", {})
    if not isinstance(hooks, dict):
        return False
    groups = hooks.get(event, [])
    if not isinstance(groups, list):
        return False
    return any(
        any(marker in str(h.get("command", "")) for h in group.get("hooks", []))
        for group in groups
        if isinstance(group, dict)
    )


def _remove_marker(cfg: dict[str, object], event: str, marker: str) -> None:
    """Drop every group under ``event`` whose command contains ``marker``; prune empties."""
    hooks = cfg.get("hooks")
    if not isinstance(hooks, dict):
        return
    groups = hooks.get(event)
    if isinstance(groups, list):
        kept = [
            g
            for g in groups
            if not (isinstance(g, dict) and any(marker in str(h.get("command", "")) for h in g.get("hooks", [])))
        ]
        if kept:
            hooks[event] = kept
        else:
            hooks.pop(event, None)
    if not hooks:
        cfg.pop("hooks", None)


def _has_legacy(cfg: dict[str, object]) -> bool:
    return any(_find_marker(cfg, event, marker) for event, marker in _LEGACY_HOOKS)


@app.command()
def status() -> None:
    """Vérifie s'il reste des hooks tracker legacy dans ~/.claude/settings.json."""
    if _has_legacy(_read_settings()):
        print("HOOK: LEGACY (migrated on install)")
    else:
        print("HOOK: MIGRATED TO PLUGIN")


@app.command()
def install() -> None:
    """Migre les hooks tracker legacy de ~/.claude/settings.json (fournis désormais par le plugin)."""
    cfg = _read_settings()
    migrated = _has_legacy(cfg)
    if migrated:
        for event, marker in _LEGACY_HOOKS:
            _remove_marker(cfg, event, marker)
        _write_settings(cfg)

    # The hook handler writes here; keep the directory even though the hook now ships in the plugin.
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    print("HOOK: MIGRATED TO PLUGIN" if migrated else "HOOK: ALREADY MIGRATED")


@app.command()
def uninstall(
    delete_logs: bool = typer.Option(False, "--delete-logs", help="Supprimer aussi les fichiers de logs"),
) -> None:
    """Retire les hooks tracker legacy de ~/.claude/settings.json."""
    cfg = _read_settings()
    if _has_legacy(cfg):
        for event, marker in _LEGACY_HOOKS:
            _remove_marker(cfg, event, marker)
        _write_settings(cfg)
        print("HOOK: REMOVED")
    else:
        print("HOOK: NOT CONFIGURED")

    if delete_logs and LOG_DIR.exists():
        shutil.rmtree(LOG_DIR)
        print(f"LOGS: DELETED ({LOG_DIR})")
