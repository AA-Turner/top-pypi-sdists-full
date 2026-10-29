"""After an update lands: what open sessions read moves to the installed copy now (plan C9).

An update replaces the CLI and the plugins, and every open session is to go on
with no restart (the owner's rule, 2026-10-24). The hooks follow by
themselves (`dispatch.hand_over`); three things they read did not, until a
session started or ended:

    the status-line renderer   a copy of the plugin's `statusline.py` (and
                               the marker reader beside it) in Claude Code's
                               config folder, which only a SessionStart
                               refreshed: from the INSTALLED plugin copy only,
                               the one Claude Code's install ledger names
                               (an older copy's SessionStart rolled it back:
                               surface audit #7)
    the managed block          the CLI's block in CLAUDE.md / AGENTS.md, which
                               `probe agent-rules refresh` and `probe notes
                               sync` (reconcile) rewrite: run by the service's
                               note sync (`notesync.py`) for each context
    the recorders' tap         `recorders.RecorderHost.follow_installed`

and one the status line itself reads from Claude Code's settings: an install
made before `refreshInterval` (`ensure_refresh_interval`) is given it, so
Claude Code redraws an idle session's line when its marker changes.

The service runs these at the end of an update cycle that installed something
(the CLI unchanged: this service is current), else the next service, the new
code, runs them once it has resumed its recorders (`Updater.take_followup`).

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import threading
from pathlib import Path

from .protocol import CONTEXT_ENV

#: What a status-line install keeps in its folder, refreshed here
#: (`probe.cli.statusline.RENDERER_FILES`; the hook's own twin is
#: `hooks/statusline_refresh.py RENDERER_FILES`. tests/test_service_followup.py
#: holds the three equal).
RENDERER_FILES = ("statusline.py", "_session_marker.py")
#: The status-line install's folder name under Claude Code's config folder.
RENDERER_DIRNAME = "probe-research-statusline"
#: The Probe plugins that carry the renderer (the daemon profile's lean one too).
PLUGINS = ("probe-research", "probe-research-daemon")
LEDGER_MAX_BYTES = 1 << 20


def claude_dir(env: dict) -> Path:
    """Claude Code's config folder for a context: `CLAUDE_CONFIG_DIR`, else `~/.claude`."""
    configured = (env.get("CLAUDE_CONFIG_DIR") or "").strip()
    if configured:
        return Path(os.path.expanduser(configured))
    return Path(env.get("HOME") or os.path.expanduser("~")) / ".claude"


def ledger_path(env: dict) -> Path:
    """Claude Code's install ledger, where Claude Code keeps it (as the hooks'
    `dispatch._ledger` reads it): `$CLAUDE_CODE_PLUGIN_CACHE_DIR` when that
    moves it, else `<config folder>/plugins/`."""
    moved = (env.get("CLAUDE_CODE_PLUGIN_CACHE_DIR") or "").strip()
    if moved:
        return Path(os.path.expanduser(moved)) / "installed_plugins.json"
    return claude_dir(env) / "plugins" / "installed_plugins.json"


def read_ledger(env: dict) -> dict | None:
    """The ledger's `plugins` object, or None (absent, too big, not its shape)."""
    path = ledger_path(env)
    try:
        if path.stat().st_size > LEDGER_MAX_BYTES:
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    plugins = data.get("plugins") if isinstance(data, dict) else None
    return plugins if isinstance(plugins, dict) else None


def installed_paths(entries: object) -> set[Path] | None:
    """The install folders (resolved) a ledger key's entries name, or None for
    anything but a non-empty list of entries that each name one."""
    if not isinstance(entries, list) or not entries:
        return None
    try:
        return {Path(e["installPath"]).resolve() for e in entries}
    except (KeyError, TypeError, AttributeError, ValueError, OSError):
        return None


def _version_key(name: str) -> tuple:
    parts = name.split(".")
    return tuple(int(p) for p in parts) if all(p.isdigit() for p in parts) else ()


def renderer_copy(entries: object) -> Path | None:
    """Which of a ledger key's install folders every session's renderer comes
    from: its user-scope one (a project's own install serves that project
    only), else the newest version folder; the newest of several either way.
    None for anything but a non-empty list of entries that each name one.
    The hook's twin is `hooks/statusline_refresh.py renderer_copy`
    (tests/test_service_followup.py holds the two to one answer)."""
    if not isinstance(entries, list) or not entries:
        return None
    try:
        listed = [(e.get("scope"), Path(e["installPath"]).resolve()) for e in entries]
    except (KeyError, TypeError, AttributeError, ValueError, OSError):
        return None
    candidates = {p for scope, p in listed if scope == "user"} or {p for _, p in listed}
    return max(sorted(candidates), key=lambda root: _version_key(root.name))


def installed_renderer_root(env: dict) -> Path | None:
    """The Probe plugin copy Claude Code has installed for this context, which
    carries the renderer (`renderer_copy` of its key: a user-scope and a
    project-scope install of one plugin left nobody refreshing it); the newest
    when both Probe plugins are installed. None when the ledger names none."""
    plugins = read_ledger(env)
    if plugins is None:
        return None
    found: list[Path] = []
    for key, entries in plugins.items():
        if not isinstance(key, str) or key.split("@", 1)[0] not in PLUGINS:
            continue
        root = renderer_copy(entries)
        if root is None:
            continue
        if all((root / "hooks" / name).is_file() for name in RENDERER_FILES):
            found.append(root)
    if not found:
        return None
    return max(found, key=lambda root: _version_key(root.name))


def sync_renderer(env: dict) -> list[str]:
    """Refresh the status-line renderer copy of this context's Claude Code from
    the installed plugin copy (`installed_renderer_root`). Only where a status
    line was installed (its folder exists: never installing one nobody asked
    for), content-compared, each file replaced in one rename. The files it
    changed; never raises."""
    target = claude_dir(env) / RENDERER_DIRNAME
    try:
        if not target.is_dir():
            return []
        root = installed_renderer_root(env)
    except OSError:
        return []
    if root is None:
        return []
    changed = []
    for name in RENDERER_FILES:
        src, dst = root / "hooks" / name, target / name
        tmp = dst.with_name(f"{dst.name}.{os.getpid()}.tmp")
        try:
            new = src.read_bytes()
            try:
                if dst.read_bytes() == new:
                    continue
            except OSError:
                pass
            tmp.write_bytes(new)
            shutil.copymode(src, tmp)
            os.replace(tmp, dst)
            changed.append(name)
        except OSError:
            try:
                tmp.unlink()
            except OSError:
                pass
            continue
    return changed


#: `probe.cli.statusline.REFRESH_INTERVAL_S`, `.MARKER` and the line its chain
#: opens a predecessor's block with (`_OPEN`): that module explains them;
#: tests/test_service_followup.py holds them equal.
REFRESH_INTERVAL_S = 10
STATUSLINE_MARKER = "# probe-research statusline"
CHAIN_OPEN = 'printf \'%s\' "$_probe_sl_input" | {'
SETTINGS_MAX_BYTES = 1 << 22
#: Under the service's folder: one empty file per settings file decided on
#: (`ensure_refresh_interval`), so an interval a person removed stays removed.
REFRESH_INTERVAL_DIRNAME = "refresh-interval"


def settings_path(env: dict) -> Path:
    """Claude Code's user settings for a context, a symlink followed to its
    target (as `probe.cli.statusline.settings_path`: a dotfiles link stays one)."""
    path = claude_dir(env) / "settings.json"
    try:
        return path.resolve() if path.is_symlink() else path
    except (OSError, RuntimeError):
        return path


def _read_settings(path: Path) -> str:
    """The settings file's text: a regular file, read without blocking and at
    most SETTINGS_MAX_BYTES (a link to a FIFO or a device never holds the
    service). Raises OSError or ValueError."""
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > SETTINGS_MAX_BYTES:
            raise ValueError("not a settings file")
        data = os.read(fd, SETTINGS_MAX_BYTES + 1)
    finally:
        os.close(fd)
    if len(data) > SETTINGS_MAX_BYTES:
        raise ValueError("not a settings file")
    return data.decode("utf-8")


def ensure_refresh_interval(env: dict, *, seen_dir: Path) -> bool:
    """Give the Probe status line of this context's Claude Code its
    `refreshInterval` when its install predates it, ONCE per settings file
    (`seen_dir` remembers it: an interval a person removed is not put back).
    Only a `statusLine` slot carrying Probe's segment alone (over another
    status line the interval would re-run that one unasked) and no interval
    of its own; never a file that is not a JSON object. The pre-edit file is
    copied once (`.probe-backup`, as the installer's); written in one rename,
    flushed to disk with its folder, with the file's mode, and only when the
    file is still what was read. True when it wrote; never raises."""
    path = settings_path(env)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.probe-tmp")
    try:
        decided = seen_dir / hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:32]
        if decided.exists():
            return False
        text = _read_settings(path)
        data = json.loads(text)
        slot = data.get("statusLine") if isinstance(data, dict) else None
        command = slot.get("command") if isinstance(slot, dict) else None
        if not isinstance(command, str) or STATUSLINE_MARKER not in command:
            return False  # no Probe status line here (yet): `install` writes it
        seen_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        if "refreshInterval" in slot or CHAIN_OPEN in command.splitlines():
            decided.touch()
            return False
        slot["refreshInterval"] = REFRESH_INTERVAL_S
        backup = path.with_name(path.name + ".probe-backup")
        if not backup.exists():
            shutil.copy2(path, backup)
        mode = stat.S_IMODE(os.stat(path).st_mode)
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, mode)
        if _read_settings(path) != text:
            os.unlink(tmp)
            return False
        os.replace(tmp, path)
        folder = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(folder)
        finally:
            os.close(folder)
        decided.touch()
        return True
    except Exception:  # noqa: BLE001 -- never raises (a deeply nested file: RecursionError)
        try:
            tmp.unlink()
        except OSError:
            pass
        return False


#: Contexts one follow-up syncs the note in (`notesync.MAX_JOBS` is 8: the
#: hooks keep the rest).
MAX_CONTEXTS = 4
#: What a context names here: never the endpoint (the CLI config's, as
#: `Service._context` allows only one it already names) nor one session's
#: own switch.
_NOT_CONTEXT = frozenset({"PROBE_BASE_URL", "PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING"})


def _proxy_userinfo(name: str, value: str) -> bool:
    return name.upper().endswith("_PROXY") and "@" in value.split("://", 1)[-1].split("/", 1)[0]


def contexts(envs: list) -> list[dict]:
    """The contexts to follow an update in: the service's own (`{}`), and each
    distinct one the recorded sessions run in (their `CONTEXT_ENV` variables:
    where their agent and Probe keep their files, how they reach the network;
    never a proxy URL carrying a password). At most MAX_CONTEXTS."""
    seen: list[dict] = [{}]
    for env in envs:
        if len(seen) >= MAX_CONTEXTS:
            break
        if not isinstance(env, dict):
            continue
        context = {
            name: value for name, value in env.items()
            if name in CONTEXT_ENV and name not in _NOT_CONTEXT and isinstance(value, str) and value
            and "\0" not in value and len(value) <= 4096 and not _proxy_userinfo(name, value)
        }
        if context and context not in seen:
            seen.append(context)
    return seen
