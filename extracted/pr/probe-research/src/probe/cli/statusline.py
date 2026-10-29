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
import re
import shutil
import time
from pathlib import Path

from ..sdk import session_marker
from ..sdk.durable import write_text_atomic

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

#: How often Claude Code re-runs the status line on its own
#: (`statusLine.refreshInterval`, seconds; Claude Code 2.1.97, and the plugin
#: needs 2.1.195 already: `probe.mcp.server`). Without it the command runs only
#: on Claude Code's own events (a new message, a mode change), so an idle
#: session kept whatever it last drew -- "not started" for a session the Probe
#: service records -- however often its marker was refreshed (2026-10-27). One
#: render reads a local file (~20 ms). Written only where Probe's segment is
#: alone (it re-runs the whole slot: a chained status line would run every few
#: seconds unasked); a slot's own value is kept. The service gives an install
#: from before this one (`probe.service.followup`, which holds its own copy of
#: this number: tests/test_service_followup.py).
REFRESH_INTERVAL_S = 10

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


def discover_plugin_root(source: str | None = None) -> Path | None:
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

    from probe.harness import get_registry
    from probe.harness import registry as reg

    if source is not None and get_registry().get(source).statusline == reg.STATUSLINE_KIMI_TUI_TOML:
        # Kimi Code's own installed copy (the recorded root it loads).
        from probe.cli import kimi_config

        for plugin_id in ("probe-research", "probe-research-daemon"):
            root = kimi_config._record_root(plugin_id)
            if root is not None and (root / "hooks" / "statusline.py").is_file():
                return root
        return None

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


def sync(plugin_root: Path | str, *, target: Path | None = None) -> list[str]:
    """Refresh the installed renderer copies from the plugin. Returns what changed.

    Content-compared rather than timestamped: a plugin update rewrites mtimes on
    files whose bytes are identical, and copying on every session start would
    churn the directory for nothing.
    """
    source = Path(plugin_root) / "hooks"
    target = target if target is not None else install_dir()
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
    """For READING only: a missing, unreadable or broken file reads as empty."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _load_for_edit(path: Path) -> dict:
    """The settings to edit and write back; only a MISSING file reads as empty.

    A file that cannot be read or does not hold a JSON object is refused, never
    edited: reading it as `{}` and saving that back replaced the researcher's
    whole settings.json (env tokens, permission rules, hooks) with our one key.
    The `.probe-backup` did not save them -- it is taken once, so a second
    broken file had no copy at all. Raises OSError or ValueError, which every
    caller already reports.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except UnicodeDecodeError as exc:
        raise ValueError(f"left {path} alone: it is not UTF-8 text ({exc})") from exc
    if not text.strip():
        return {}  # Claude Code reads an empty settings.json as no settings, and so do we
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ValueError(f"left {path} alone: it is not valid JSON ({exc}); fix it and run this again") from exc
    if not isinstance(data, dict):
        raise ValueError(f"left {path} alone: it holds a JSON {type(data).__name__}, not an object")
    return data


def _save(path: Path, settings: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # The replace must not loosen the file: a `settings.json` kept 0600 because
    # its `env` holds tokens would otherwise come back as the umask's 0664.
    write_text_atomic(path, json.dumps(settings, indent=2) + "\n", keep_mode=True)


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
    path = settings_path()
    settings = _load_for_edit(path)  # before anything is copied: a refusal changes nothing
    copied = sync(plugin_root)
    slot = settings.get("statusLine")
    current = slot.get("command") if isinstance(slot, dict) else None
    previous = split_existing(current) if isinstance(current, str) else ""

    backup = _backup(path)
    ours = renderer_command(python)
    own = slot.get("refreshInterval") if isinstance(slot, dict) else None
    settings["statusLine"] = {"type": "command", "command": chain(previous, ours)}
    # Not over another status line: the interval re-runs the whole chain, so a
    # predecessor would run every few seconds in every idle session unasked.
    if own is not None or not previous:
        settings["statusLine"]["refreshInterval"] = own if own is not None else REFRESH_INTERVAL_S
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
        # Over another status line `install` writes none of its own: any is theirs.
        own = slot.get("refreshInterval")
        if own is not None:
            settings["statusLine"]["refreshInterval"] = own
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


# --- Kimi Code: `$KIMI_CODE_HOME/tui.toml` `[status_line] command` -----------
#
# Kimi runs that command through `sh -c` with a JSON snapshot on stdin
# (`model, cwd, gitBranch, ..., sessionId`) and `KIMI_CODE_STATUS_LINE=1` in
# its environment, and uses its FIRST stdout line as footer line 1, REPLACING
# Kimi's own; it re-runs at most once a second and kills it after 300 ms. So
# the renderer prints the whole line (`statusline.kimi_line`), and a
# researcher's own command is chained by handing its first line over in
# `PROBE_SL_PREFIX` rather than by printing two lines (only the first counts).

#: The chain parks the researcher's first line here. Prefixed like `VAR`.
KIMI_PREFIX_VAR = "_probe_sl_theirs"
_KIMI_OPEN = f"{KIMI_PREFIX_VAR}=$(" + _PIPE + "{"
_KIMI_CLOSE = "} 2>/dev/null | head -n 1)"


def kimi_tui_path() -> Path:
    from probe.cli import kimi_config

    return kimi_config.kimi_home() / "tui.toml"


def kimi_install_dir() -> Path:
    from probe.cli import kimi_config

    return kimi_config.kimi_home() / INSTALL_DIRNAME


def kimi_renderer_command(python: str | None = None) -> str:
    script = kimi_install_dir() / "statusline.py"
    return f"{_quote(python or python_bin())} {_quote(str(script))} {MARKER}"


def kimi_chain(previous: str, ours: str) -> str:
    """Kimi's command: ours alone, or theirs first with its first line handed
    to ours, both fed the same snapshot (see `_HEADER`)."""
    if not previous:
        return "\n".join([_HEADER, _PIPE + ours])
    return "\n".join([_HEADER, _KIMI_OPEN, previous, _KIMI_CLOSE,
                      f'{_PIPE}PROBE_SL_PREFIX="${KIMI_PREFIX_VAR}" {ours}'])


def kimi_split_existing(command: str) -> str:
    """What was in Kimi's slot before us (the `split_existing` contract)."""
    if MARKER not in command:
        return command.strip()
    lines = command.splitlines()
    try:
        start = lines.index(_KIMI_OPEN)
        end = lines.index(_KIMI_CLOSE, start + 1)
    except ValueError:
        return ""
    return "\n".join(lines[start + 1 : end]).strip()


def _toml_basic(value: str) -> str:
    """A TOML basic string, as Kimi's own `escapeTomlBasicString` writes it."""
    out = []
    for ch in value:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def _kimi_command(text: str) -> str | None:
    """The current `[status_line] command`. Raises ValueError on a file that is
    not TOML: it is the researcher's, and an unparseable one is left alone."""
    from probe._compat import tomllib

    try:
        doc = tomllib.loads(text) if text.strip() else {}
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"{kimi_tui_path()} is not valid TOML ({exc}); left as it is") from exc
    table = doc.get("status_line")
    command = table.get("command") if isinstance(table, dict) else None
    return command if isinstance(command, str) else None


#: A TOML table header (`[name]`, `[[name]]`), as opposed to an array value
#: line such as `  ["model"],` that also starts with a bracket.
_TOML_HEADER = re.compile(r"""^\s*\[\[?\s*[A-Za-z0-9_.\-"' ]+\s*\]\]?\s*(#.*)?$""")
_TOML_COMMAND = re.compile(r"^\s*command\s*=")
_MULTILINE_QUOTES = ('"' * 3, "'" * 3)


def _value_end(lines: list[str], start: int) -> int:
    """The last line of the value that begins on `lines[start]`: a multi-line
    string spans to its closing delimiter."""
    rest = lines[start].split("=", 1)[1].lstrip()
    for quote in _MULTILINE_QUOTES:
        if rest.startswith(quote):
            if rest.count(quote) >= 2:
                return start
            for i in range(start + 1, len(lines)):
                if quote in lines[i]:
                    return i
            return len(lines) - 1
    return start


def _with_kimi_command(text: str, command: str | None) -> str:
    """`text` with ONLY the `[status_line]` table's `command` set (or, for None,
    removed); every other byte kept. Callers re-parse the result
    (`_kimi_command`) before writing, so a shape this cannot edit is refused,
    never written."""
    lines = text.split("\n")
    header = next((i for i, line in enumerate(lines) if _TOML_HEADER.match(line)
                   and line.split("#", 1)[0].strip() == "[status_line]"), None)
    if header is None:
        if command is None:
            return text
        tail = "" if not text or text.endswith("\n") else "\n"
        return f"{text}{tail}\n[status_line]\ncommand = {_toml_basic(command)}\n"
    end = next((i for i in range(header + 1, len(lines)) if _TOML_HEADER.match(lines[i])), len(lines))
    existing = next((i for i in range(header + 1, end) if _TOML_COMMAND.match(lines[i])), None)
    new_line = None if command is None else f"command = {_toml_basic(command)}"
    if existing is not None:
        last = _value_end(lines, existing)
        lines[existing:last + 1] = [] if new_line is None else [new_line]
        end -= last + 1 - existing - (0 if new_line is None else 1)
    elif new_line is not None:
        lines.insert(header + 1, new_line)
    if new_line is None and not any(line.strip() for line in lines[header + 1:end]):
        # The table held only our command (install added it): take it out whole.
        start = header - 1 if header > 0 and not lines[header - 1].strip() else header
        del lines[start:header + 1]
    return "\n".join(lines)


def _save_text(path: Path, text: str) -> None:
    """Write `text` to `path`, THROUGH a symlink (a dotfiles-managed tui.toml
    stays a link to the researcher's file), keeping the file's mode."""
    target = path.resolve() if path.is_symlink() else path
    target.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomic(target, text, keep_mode=True)


def install_kimi(plugin_root: Path | str, *, python: str | None = None) -> dict:
    """Add (or refresh) our segment in Kimi Code's footer, chaining what was there."""
    path = kimi_tui_path()
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    current = _kimi_command(text)
    previous = kimi_split_existing(current) if current else ""
    command = kimi_chain(previous, kimi_renderer_command(python))
    updated = _with_kimi_command(text, command)
    if _kimi_command(updated) != command:  # never write a file Kimi would read differently
        raise ValueError(f"Probe could not place its status line in {path} (an unusual layout there); "
                         "the file was left as it is")
    # Only once the edit is known to land: a refusal leaves no renderer folder
    # behind (its presence turns the statusline_refresh hook on).
    copied = sync(plugin_root, target=kimi_install_dir())
    backup = _backup(path)
    _save_text(path, updated)
    mark_caught_up(_kimi_slot())
    return {
        "settings": str(path),
        "backup": str(backup) if backup else None,
        "renderer": str(kimi_install_dir() / "statusline.py"),
        "copied": copied,
        "chained_after": previous or None,
        "command": command,
    }


def uninstall_kimi() -> dict:
    """Remove our segment from Kimi's footer, restoring exactly what we wrapped."""
    path = kimi_tui_path()
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    try:
        current = _kimi_command(text)
    except ValueError:
        return {"settings": str(path), "removed": False, "restored": None}
    if not current or MARKER not in current:
        return {"settings": str(path), "removed": False, "restored": None}
    previous = kimi_split_existing(current)
    updated = _with_kimi_command(text, previous or None)
    if _kimi_command(updated) != (previous or None):  # the same guard as install
        raise ValueError(f"Probe could not take its status line out of {path} (an unusual layout there); "
                         "the file was left as it is")
    _save_text(path, updated)
    mark_caught_up(_kimi_slot())
    return {"settings": str(path), "removed": True, "restored": previous or None}


def kimi_installed() -> bool:
    try:
        path = kimi_tui_path()
        current = _kimi_command(path.read_text(encoding="utf-8")) if path.is_file() else None
    except (OSError, ValueError):
        return False
    return bool(current) and MARKER in current


def install_for(source: str, plugin_root: Path | str, *, python: str | None = None) -> dict:
    """Install into the status-line slot the registry names for `source`."""
    from probe.harness import get_registry
    from probe.harness import registry as reg

    slot = get_registry().get(source).statusline
    if slot == reg.STATUSLINE_KIMI_TUI_TOML:
        return install_kimi(plugin_root, python=python)
    if slot == reg.STATUSLINE_CLAUDE_SETTINGS:
        return install(plugin_root, python=python)
    raise ValueError(f"{source} has no status line Probe installs into")


def installed_for(source: str) -> bool:
    """`source`'s status-line slot carries Probe's segment."""
    from probe.harness import get_registry
    from probe.harness import registry as reg

    harness = get_registry().find(source)
    slot = harness.statusline if harness is not None else None
    if slot == reg.STATUSLINE_KIMI_TUI_TOML:
        return kimi_installed()
    if slot == reg.STATUSLINE_CLAUDE_SETTINGS:
        return bool(status().get("installed"))
    return False


def _kimi_slot() -> str:
    from probe.harness import registry as reg

    return reg.STATUSLINE_KIMI_TUI_TOML


def _later_slots() -> tuple[str, ...]:
    """Slots that shipped AFTER Probe's rules were already on machines (Kimi
    Code's footer, 0.214.0). The status line is written only by the rules step,
    which a machine whose rules are current never runs again, so those machines
    get one catch-up (`setup.catch_up_statusline`). Claude Code's slot has ridden
    with the rules since it shipped: a missing one there was removed on purpose."""
    from probe.harness import registry as reg

    return (reg.STATUSLINE_KIMI_TUI_TOML,)


def _catch_up_path(slot: str) -> Path:
    return session_marker.state_dir() / "statusline-catch-up" / slot


def _slot_of(source: str) -> "str | None":
    from probe.harness import get_registry

    harness = get_registry().find(source)
    return harness.statusline if harness is not None else None


def catch_up_owed(source: str) -> bool:
    """`source` has a later slot that has never been installed into or removed
    from on this machine (any install or uninstall of the slot marks it)."""
    slot = _slot_of(source)
    return slot in _later_slots() and not _catch_up_path(slot).exists()


def mark_caught_up(source_or_slot: str) -> None:
    """Never catch this slot up again: a later `probe statusline uninstall`
    stays. Takes an agent id or the slot name itself."""
    slot = _slot_of(source_or_slot) or source_or_slot
    path = _catch_up_path(slot)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + "\n", encoding="utf-8")
    except OSError:
        return


def uninstall_for(source: str) -> dict:
    from probe.harness import get_registry
    from probe.harness import registry as reg

    slot = get_registry().get(source).statusline
    if slot == reg.STATUSLINE_KIMI_TUI_TOML:
        return uninstall_kimi()
    if slot == reg.STATUSLINE_CLAUDE_SETTINGS:
        return uninstall()
    return {"settings": None, "removed": False, "restored": None}


def slot_path(source: str) -> Path:
    """The file holding `source`'s status-line slot."""
    from probe.harness import get_registry
    from probe.harness import registry as reg

    if get_registry().get(source).statusline == reg.STATUSLINE_KIMI_TUI_TOML:
        return kimi_tui_path()
    return settings_path()
