"""Claiming a share of Claude Code's status line without evicting anyone.

`statusLine` is ONE global slot in `~/.claude/settings.json`:

    "statusLine": {"type": "command", "command": "..."}

There is no plugin manifest field for it -- a plugin manifest may declare
commands, skills, agents, hooks, themes, workflows, outputStyles and
mcpServers, and that is the whole list. So a plugin that wants to render there
has to edit the user's settings, and the only decent way to do that is to CHAIN:
keep whatever was already configured and append our segment to it.

That is not a hypothetical courtesy. The slot is popular -- imsg-device's
installer wrap-chains into it, plenty of people have a hand-rolled PS1-alike
there -- and silently replacing someone's status line to advertise ourselves
would be the rudest possible install step.

THE PART THAT IS EASY TO GET WRONG: STDIN.
------------------------------------------
Claude Code pipes the status-line payload to ONE process. Chain two commands
with `a; b` and whichever reads first drains the pipe -- most status lines do
`input=$(cat)`, so the second command reliably gets nothing. Our renderer needs
`session_id` out of that payload, and a naive chain would leave it permanently
blank while looking like it worked.

So the chain this module writes reads stdin ONCE and feeds a copy to each side:

    _probe_sl_input=$(cat)
    printf '%s' "$_probe_sl_input" | {
    <whatever was already there>
    }
    printf '%s' "$_probe_sl_input" | <ours> # probe-research statusline

`printf '%s'`, never `echo`: a payload beginning with `-n`, or containing a
backslash, is mangled by echo on some shells. Both sides therefore see the
identical bytes Claude Code sent, and neither can starve the other.

The NEWLINES and the brace group are load-bearing too, for a second trap — see
`_HEADER` below.

IDEMPOTENT AND REVERSIBLE. Re-running replaces our own segment rather than
stacking copies (the marker comment is how we find it), `uninstall` restores the
predecessor exactly, and the pre-edit file is backed up once.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
from pathlib import Path

from ..sdk import session_marker

#: How our segment is recognised on a later run. A comment, so it is inert to
#: the shell and visible to a human reading their own settings file.
MARKER = "# probe-research statusline"

#: Shell variable the tee'd chain parks the payload in. Prefixed because it
#: lands in the same shell as somebody else's status-line script, and a bare
#: `input` would collide with theirs.
VAR = "_probe_sl_input"

#: The renderer is COPIED here and the settings file points at this path.
#:
#: Not at the plugin, because the plugin's installed directory is version-pinned
#: -- `~/.claude/plugins/cache/<marketplace>/probe-research/0.23.0/` -- so a path
#: baked into settings.json breaks on the next plugin release, and it breaks
#: SILENTLY: a status-line command that cannot be executed just renders nothing.
#: A stable directory we own has no such cliff, and the copies are stdlib-only
#: single files, so an out-of-date copy still runs correctly against the same
#: marker format. `sync` refreshes them when the plugin updates.
INSTALL_DIRNAME = "probe-research-statusline"

#: What `sync`/`install` copy out of the plugin's hooks directory. The renderer
#: loads `_session_marker` by explicit sibling path, so the two travel together.
#: `_telemetry_core` is deliberately NOT among them: it imports urllib.request,
#: which is ~23ms of interpreter startup on a path that renders constantly, so
#: `session_marker.configured()` answers the only question it was needed for.
RENDERER_FILES = ("statusline.py", "_session_marker.py")


def claude_dir() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude"))


def install_dir() -> Path:
    return claude_dir() / INSTALL_DIRNAME


def python_bin() -> str:
    """An ABSOLUTE, LONG-LIVED python3, resolved once at install time.

    Absolute, because a dock-launched Claude Code sources no shell profile and
    runs the status-line command with a minimal PATH on which a bare `python3`
    may not resolve -- the same trap `hooks/session-start.sh` documents for the
    `probe` binary.

    NOT the active virtualenv, which is the trap this function exists for.
    `probe` is typically invoked from inside a project venv (or a `uv tool`
    environment), so a plain `which` resolves to an interpreter that is deleted
    the moment that venv is. The path is then baked into settings.json forever
    and the status line silently renders nothing. The renderer is stdlib-only
    precisely so it can run under whatever python the machine will still have
    next month, so prefer that one.
    """
    stripped = [
        entry
        for entry in os.environ.get("PATH", "").split(os.pathsep)
        if entry
        and not any(
            _within(entry, os.environ.get(var))
            for var in ("VIRTUAL_ENV", "CONDA_PREFIX", "UV_PROJECT_ENVIRONMENT")
        )
    ]
    found = shutil.which("python3", path=os.pathsep.join(stripped)) if stripped else None
    if found:
        return found
    if os.access("/usr/bin/python3", os.X_OK):
        return "/usr/bin/python3"
    return shutil.which("python3") or "python3"


def _within(entry: str, root: str | None) -> bool:
    if not root:
        return False
    try:
        return os.path.commonpath(
            [os.path.abspath(entry), os.path.abspath(root)]
        ) == os.path.abspath(root)
    except ValueError:  # different drives on Windows
        return False


def discover_plugin_root() -> Path | None:
    """Where the probe-research plugin's files are, or None.

    Three places, in the order that keeps a developer's checkout from being
    shadowed by an installed release:

    1. ``PROBE_PLUGIN_ROOT`` -- explicit beats inference, and it is what the
       hooks already export when they call in.
    2. This checkout, when running from source (``…/agent/plugins/probe-research``).
    3. The installed plugin. Both layouts are searched: the version-pinned
       ``plugins/cache/<marketplace>/probe-research/<version>/`` and the
       marketplace clone. Highest version wins -- string sort would put 0.9 above
       0.23, so the key is the numeric tuple.
    """
    explicit = os.environ.get("PROBE_PLUGIN_ROOT")
    if explicit and (Path(explicit) / "hooks" / "statusline.py").is_file():
        return Path(explicit)

    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "plugins" / "probe-research"
        if (candidate / "hooks" / "statusline.py").is_file():
            return candidate

    def _version_key(path: Path) -> tuple:
        parts = []
        for chunk in path.parent.name.split("."):
            parts.append(int(chunk) if chunk.isdigit() else -1)
        return tuple(parts)

    root = claude_dir() / "plugins"
    # The daemon profile's lean plugin carries the same renderer, and is the
    # only Probe plugin a machine on that profile has.
    for name in ("probe-research", "probe-research-daemon"):
        cached = sorted(root.glob(f"cache/*/{name}/*/hooks/statusline.py"), key=_version_key)
        if cached:
            return cached[-1].parent.parent
        for clone in sorted(root.glob(f"marketplaces/*/plugins/{name}/hooks/statusline.py")):
            return clone.parent.parent
    return None


def sync(plugin_root: Path | str) -> list[str]:
    """Refresh the installed renderer copies from the plugin. Returns what changed.

    Content-compared rather than timestamped: a plugin update rewrites mtimes on
    files whose bytes are identical, and copying on every session start would
    churn the directory for nothing.
    """
    source = Path(plugin_root) / "hooks"
    target = install_dir()
    changed: list[str] = []
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError:
        return changed
    for name in RENDERER_FILES:
        src = source / name
        dst = target / name
        try:
            if not src.is_file():
                continue
            if dst.is_file() and dst.read_bytes() == src.read_bytes():
                continue
            shutil.copy2(src, dst)
            changed.append(name)
        except OSError:
            continue
    return changed


def settings_path() -> Path:
    """The user-level settings file, following a symlink to its target.

    Claude Code's own status-line instructions call this out: people symlink
    `~/.claude/settings.json` into a dotfiles repo, and writing the link
    replaces it with a regular file, quietly detaching them from their repo.
    """
    path = Path(os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude")) / "settings.json"
    try:
        return path.resolve() if path.is_symlink() else path
    except (OSError, RuntimeError):  # 3.10 raises RuntimeError for a symlink loop
        return path


def renderer_command(python: str | None = None) -> str:
    """The shell command that prints our segment."""
    script = install_dir() / "statusline.py"
    return f"{_quote(python or python_bin())} {_quote(str(script))} {MARKER}"


def _quote(value: str) -> str:
    """Single-quote for /bin/sh. Paths carry spaces; `~` must not be expanded
    by us when the user typed a literal one."""
    return "'" + value.replace("'", "'\\''") + "'"


#: Lines the composed chain is built from. NEWLINE-SEPARATED, NOT `a; b`, and
#: that is a correctness fix rather than a formatting preference.
#:
#: Status-line commands routinely END IN A SHELL COMMENT -- imsg-device's
#: installer appends `# imsg-device statusline` as its idempotency marker, and
#: this module appends one of its own for the same reason. A comment runs to
#: end of LINE, so `<theirs> # their-marker; <ours>` comments OUR SEGMENT OUT
#: entirely. It fails silently and looks exactly like a renderer bug.
#:
#: A newline terminates a comment. So does putting the predecessor inside a
#: brace group opened and closed on its own lines, which additionally lets a
#: multi-line predecessor be fed by one pipe and keeps a failure on either side
#: from taking the other down.
_HEADER = f"{VAR}=$(cat)"
_PIPE = f"printf '%s' \"${VAR}\" | "
_OPEN = _PIPE + "{"
_CLOSE = "}"


def split_existing(command: str) -> str:
    """Whatever was in the slot BEFORE us, given the current command string.

    Handles the three shapes a repeat install can find: a slot we have never
    touched (return it whole), a chain we wrote (return the predecessor we
    wrapped, so a re-install re-wraps rather than nests), and a chain we wrote
    around nothing (return empty).
    """
    if MARKER not in command:
        return command.strip()
    lines = command.splitlines()
    try:
        start = lines.index(_OPEN)
        end = lines.index(_CLOSE, start + 1)
    except ValueError:
        return ""
    return "\n".join(lines[start + 1 : end]).strip()


def chain(previous: str, ours: str) -> str:
    """Compose the final command. Both sides get the payload; see `_HEADER`."""
    lines = [_HEADER]
    if previous:
        lines.append(_OPEN)
        lines.append(previous)
        lines.append(_CLOSE)
    lines.append(_PIPE + ours)
    return "\n".join(lines)


def _load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _save(path: Path, settings: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    # The replace must not loosen the file: a `settings.json` kept 0600 because
    # its `env` holds tokens would otherwise come back as the umask's 0664.
    try:
        os.chmod(tmp, stat.S_IMODE(path.stat().st_mode))
    except FileNotFoundError:
        pass
    os.replace(tmp, path)


def _backup(path: Path) -> Path | None:
    """Copy the pre-edit file once. Never overwritten: the FIRST backup is the
    one taken before we ever touched this file, and that is the state a person
    reaching for it wants -- a later one would only capture our own edit."""
    if not path.is_file():
        return None
    backup = path.with_name(path.name + ".probe-backup")
    if backup.exists():
        return backup
    try:
        shutil.copy2(path, backup)
    except OSError:
        return None
    return backup


def install(plugin_root: Path | str, *, python: str | None = None) -> dict:
    """Add (or refresh) our segment in the status-line slot."""
    copied = sync(plugin_root)
    path = settings_path()
    settings = _load(path)
    slot = settings.get("statusLine")
    current = slot.get("command") if isinstance(slot, dict) else None
    previous = split_existing(current) if isinstance(current, str) else ""

    backup = _backup(path)
    ours = renderer_command(python)
    settings["statusLine"] = {"type": "command", "command": chain(previous, ours)}
    _save(path, settings)
    return {
        "settings": str(path),
        "backup": str(backup) if backup else None,
        "renderer": str(install_dir() / "statusline.py"),
        "copied": copied,
        "chained_after": previous or None,
        "command": settings["statusLine"]["command"],
    }


def uninstall() -> dict:
    """Remove our segment, restoring exactly what we wrapped.

    Removing the key entirely when we wrapped nothing is deliberate: an empty
    `statusLine` command is not the same as no status line, and leaving one
    behind would make an uninstall visible forever as a blank row.
    """
    path = settings_path()
    settings = _load(path)
    slot = settings.get("statusLine")
    current = slot.get("command") if isinstance(slot, dict) else None
    if not isinstance(current, str) or MARKER not in current:
        return {"settings": str(path), "removed": False, "restored": None}

    previous = split_existing(current)
    if previous:
        settings["statusLine"] = {"type": "command", "command": previous}
    else:
        settings.pop("statusLine", None)
    _save(path, settings)
    return {"settings": str(path), "removed": True, "restored": previous or None}


def status() -> dict:
    """Whether the slot currently carries our segment, and what else is in it."""
    path = settings_path()
    slot = _load(path).get("statusLine")
    current = slot.get("command") if isinstance(slot, dict) else None
    if not isinstance(current, str):
        return {"settings": str(path), "installed": False, "command": None, "chained_after": None}
    return {
        "settings": str(path),
        "installed": MARKER in current,
        "command": current,
        "chained_after": (split_existing(current) or None) if MARKER in current else None,
    }


# ---------------------------------------------------------------------------
# The Codex half: a notice on change, because there is nothing to render into
# ---------------------------------------------------------------------------


def enable_notice() -> Path:
    """Turn on the on-change notice. Returns the flag path.

    Codex HAS a status line, but it is a picker over built-in items, so a
    computed segment has nowhere to go. The same information is delivered as a
    message when it changes instead — see hooks/statusline_notify.py.
    """
    path = session_marker.notify_flag_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("enabled by the Probe wizard\n", encoding="utf-8")
    return path


def disable_notice() -> bool:
    """Turn it off. True when it had been on."""
    path = session_marker.notify_flag_path()
    try:
        path.unlink()
        return True
    except OSError:
        return False


def notice_enabled() -> bool:
    return session_marker.notify_enabled()
