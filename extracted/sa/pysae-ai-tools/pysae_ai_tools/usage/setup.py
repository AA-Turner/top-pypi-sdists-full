"""Manage the Claude usage status line and migrate away the legacy usage hooks.

The two usage hooks — ``PreToolUse`` → ``pysae-ai-tools usage hook`` and ``UserPromptSubmit`` →
``pysae-ai-tools usage prompt-hook`` — now ship with the Pysae plugin (``hooks/hooks.json``), so
they are no longer written into ``~/.claude/settings.json``. This module keeps ownership of the
``statusLine`` feed (which the hooks read for plan-window data — the plugin does not manage status
lines) and, as a migration, strips any legacy usage hook a previous version left behind so it does
not fire twice next to the plugin's copy.

Usage:
    pysae-ai-tools usage setup status
    pysae-ai-tools usage setup install
    pysae-ai-tools usage setup uninstall
"""

import json
import os
import platform
import shlex
from pathlib import Path
from typing import Annotated

import typer


def _settings_path() -> Path:
    """Return the Claude Code settings.json path for the current platform."""
    if platform.system() == "Windows":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "Claude" / "settings.json"
    return Path.home() / ".claude" / "settings.json"


SETTINGS_PATH = _settings_path()

# (settings.json event, matcher | None, canonical command). UserPromptSubmit has no matcher.
_HOOKS: tuple[tuple[str, str | None, str], ...] = (
    ("PreToolUse", "*", "pysae-ai-tools usage hook"),
    ("UserPromptSubmit", None, "pysae-ai-tools usage prompt-hook"),
)

# Claude Code status line command (single `statusLine` key, unlike the list-valued hooks).
# Doubles as the usage feed: it writes the plan windows it receives into the shared cache.
STATUSLINE_COMMAND = "pysae-ai-tools usage statusline"

app = typer.Typer(help="Manage the Claude usage hooks (PreToolUse + UserPromptSubmit) in Claude Code settings.")


def _read_settings() -> dict[str, object]:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
    except (json.JSONDecodeError, OSError):
        return {}


def _write_settings(cfg: dict[str, object]) -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _event_list(cfg: dict[str, object], event: str) -> list[object]:
    hooks = cfg.get("hooks", {})
    if not isinstance(hooks, dict):
        return []
    groups = hooks.get(event, [])
    return groups if isinstance(groups, list) else []


def _entries(cfg: dict[str, object], event: str, command: str) -> list[dict[str, object]]:
    """The ``{type, command, …}`` dicts registering ``command`` under ``event``."""
    return [
        h
        for group in _event_list(cfg, event)
        if isinstance(group, dict)
        for h in group.get("hooks", [])
        if isinstance(h, dict) and command in str(h.get("command", ""))
    ]


def _find(cfg: dict[str, object], event: str, command: str) -> bool:
    return bool(_entries(cfg, event, command))


def _remove_hook(cfg: dict[str, object], event: str, command: str) -> None:
    hooks = cfg.get("hooks")
    if not isinstance(hooks, dict):
        return
    groups = hooks.get(event)
    if isinstance(groups, list):
        kept = [
            g
            for g in groups
            if not (isinstance(g, dict) and any(command in str(h.get("command", "")) for h in g.get("hooks", [])))
        ]
        if kept:
            hooks[event] = kept
        else:
            hooks.pop(event, None)
    if not hooks:
        cfg.pop("hooks", None)


def _statusline_command(cfg: dict[str, object]) -> str | None:
    sl = cfg.get("statusLine")
    if isinstance(sl, dict):
        cmd = sl.get("command")
        return cmd if isinstance(cmd, str) else None
    return None


def _statusline_state(cfg: dict[str, object]) -> str:
    """``"ours"`` (our command — direct or wrapping another), ``"foreign"`` (a user's own status
    line) or ``"absent"``."""
    cmd = _statusline_command(cfg)
    if cmd is None:
        return "absent"
    if cmd == STATUSLINE_COMMAND or cmd.startswith(STATUSLINE_COMMAND + " "):
        return "ours"
    return "foreign"


def _wrapped_command(cfg: dict[str, object]) -> str | None:
    """When our status line wraps another (``… --exec <cmd>``), return the original ``<cmd>``.

    The wrapped command is stored shell-quoted as a single word (see ``install``), so it is
    unquoted here — a round-trip that restores the byte-exact original. Falls back to the raw
    tail for a hand-edited value that isn't a single quoted word."""
    cmd = _statusline_command(cfg)
    prefix = STATUSLINE_COMMAND + " --exec "
    if cmd is None or not cmd.startswith(prefix):
        return None
    rest = cmd[len(prefix) :].strip()
    if not rest:
        return None
    try:
        parts = shlex.split(rest)
    except ValueError:
        return rest
    return parts[0] if len(parts) == 1 else rest


@app.command()
def status(as_json: Annotated[bool, typer.Option("--json", help="Sortie JSON structurée")] = False) -> None:
    """Vérifie l'état de la status line usage (et les hooks legacy résiduels)."""
    cfg = _read_settings()
    states = {event: _find(cfg, event, command) for event, _matcher, command in _HOOKS}
    sl_state = _statusline_state(cfg)
    # "configured" gates reinstall on the status line alone — the hooks now ship with the plugin.
    # False unless the status line is ours (direct or wrapping), so a fresh, absent, or still-
    # foreign status line is picked up / wrapped on the next install. ``hooks`` reports only
    # residual legacy entries (migrated away on install), never gating ``configured``.
    configured = sl_state == "ours"
    if as_json:
        print(json.dumps({"configured": configured, "hooks": states, "statusline": sl_state}))
        return
    for event, present in states.items():
        if present:
            print(f"HOOK ({event}): LEGACY (migrated on install)")
    print(f"STATUSLINE: {sl_state.upper()}")


@app.command()
def install() -> None:
    """Installe la status line usage dans ~/.claude/settings.json et migre les hooks legacy.

    Si aucune status line n'existe, la nôtre est posée. Si une status line personnalisée existe,
    elle n'est pas écrasée mais **enveloppée** (`… --exec <commande existante>`) : le feed d'usage
    est alimenté et l'affichage reste délégué à la status line d'origine. Les hooks usage (désormais
    fournis par le plugin) sont retirés de settings.json s'ils y traînent encore.
    """
    cfg = _read_settings()
    migrated = []
    for event, _matcher, command in _HOOKS:
        if _find(cfg, event, command):
            _remove_hook(cfg, event, command)
            migrated.append(event)

    sl_state = _statusline_state(cfg)
    sl_note = "STATUSLINE: ALREADY CONFIGURED"
    if sl_state == "absent":
        cfg["statusLine"] = {"type": "command", "command": STATUSLINE_COMMAND, "padding": 0}
        sl_note = "STATUSLINE: INSTALLED"
    elif sl_state == "foreign":
        existing = cfg.get("statusLine")
        wrapped = _statusline_command(cfg)
        if isinstance(existing, dict) and wrapped is not None:
            # Quote the original as one shell word so it survives the outer shell re-parsing the
            # wrapped line at render time (paths with spaces, metacharacters stay intact).
            existing["command"] = f"{STATUSLINE_COMMAND} --exec {shlex.quote(wrapped)}"
            sl_note = f"STATUSLINE: WRAPPED (existing: {wrapped})"

    if migrated or sl_state in ("absent", "foreign"):
        _write_settings(cfg)

    if migrated:
        print(f"HOOK: MIGRATED TO PLUGIN ({', '.join(migrated)})")
    else:
        print("HOOK: ALREADY MIGRATED")
    print(sl_note)


@app.command()
def uninstall() -> None:
    """Désinstalle les hooks usage (et notre status line) de ~/.claude/settings.json.

    Une status line que nous avons enveloppée est restaurée à sa commande d'origine ; une status
    line que nous avons posée nous-mêmes est retirée.
    """
    cfg = _read_settings()
    hooks_present = any(_find(cfg, event, command) for event, _matcher, command in _HOOKS)
    sl_ours = _statusline_state(cfg) == "ours"
    if not hooks_present and not sl_ours:
        print("HOOK: NOT CONFIGURED")
        return
    for event, _matcher, command in _HOOKS:
        _remove_hook(cfg, event, command)
    sl_note = None
    if sl_ours:
        wrapped = _wrapped_command(cfg)
        sl = cfg.get("statusLine")
        if wrapped is not None and isinstance(sl, dict):
            sl["command"] = wrapped
            sl_note = f"STATUSLINE: UNWRAPPED (restored: {wrapped})"
        else:
            cfg.pop("statusLine", None)
            sl_note = "STATUSLINE: REMOVED"
    _write_settings(cfg)
    print("HOOK: REMOVED")
    if sl_note:
        print(sl_note)
