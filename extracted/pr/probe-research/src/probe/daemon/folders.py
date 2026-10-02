"""The session's working folders, and the folder check before each bite (D8, S5).

Working folders: where the session started, folders the agent `cd`'d into or
wrote in, and folders of paths it named -- anywhere (a `/data/ckpts`, a
`/mnt/nvme/proj`, a `/workspace` too), but never `$HOME` itself (every session
on a shared box starts there), a folder above it, a shared root (`/`, `/tmp`,
`/mnt`...), anything in a system tree (`/etc`, `/usr`, `/var`, `/proc`, `/lib*`
...; under `$HOME` or the session's own folder excepted) or a hidden folder; the
most recent MAX_WORKING_FOLDERS. The folder check compares each file's size and
modification time with the last look and queues a FILE_CHANGE event for what is
new or changed; for a changed text file it keeps the last-seen copy (up to
MAX_TEXT_STORED per session) so the model gets a diff. A credential-shaped name
(the shell classifier's rule) is reported without its content. Only regular
files are looked at: a symlink (which could point at anything, a secret
included) or a FIFO is skipped, and a file is opened without following one. The
first look is a baseline: files that were there before the daemon started are
not "new". The walk runs off the event loop (`check_async`); the store is
touched only on it.
"""

from __future__ import annotations

import asyncio
import codecs
import difflib
import os
import re
import shlex
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from probe.daemon.events import Event, Kind
from probe.daemon.store import UNRECORDED_BITE, Store, scrub, state_dir

MAX_FILES_PER_FOLDER = 3000
MAX_FILES_PER_CHECK = 10_000
MAX_WORKING_FOLDERS = 8
MAX_DEPTH = 6
MAX_TEXT_KEPT = 256 * 1024
#: Last-seen text copies kept per session, in all.
MAX_TEXT_STORED = 64 * 1024 * 1024
MAX_DIFF_CHARS = 4000
#: Never a working folder itself, nor the root of a session's own tree.
_SYSTEM_DIRS = frozenset(Path(p) for p in (
    "/", "/bin", "/boot", "/dev", "/etc", "/home", "/lib", "/lib64", "/media", "/mnt", "/nix", "/opt", "/proc",
    "/root", "/run", "/sbin", "/snap", "/srv", "/sys", "/tmp", "/usr", "/var", "/Applications", "/Library",
    "/System", "/Users", "/Volumes", "/private", "/private/etc", "/private/tmp", "/private/var",
))
#: Nothing inside these is a working folder (unless under `$HOME` or the
#: session's own folder), and neither is anything in a top-level `/lib*`.
_SYSTEM_TREES = tuple(Path(p) for p in (
    "/bin", "/boot", "/dev", "/etc", "/nix", "/proc", "/root", "/run", "/sbin", "/snap", "/sys", "/usr", "/var",
    "/Applications", "/Library", "/System", "/private/etc", "/private/var",
))
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
             ".tox", "dist", "build", ".cache", "wandb", ".ipynb_checkpoints", "site-packages"}
_CD_RE = re.compile(r"(?:^|&&|\|\||;|\(|\n)\s*cd\s+(\"[^\"]+\"|'[^']+'|[^\s;&|)]+)")
_WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "write", "edit", "apply_patch"}


def _state_base() -> Path:
    return state_dir().parent


def note_dirs() -> list[Path]:
    """Where the daemon may write files: Probe's own note checkouts and the team note."""
    base = _state_base()
    return [base / "notes", base / "team-note"]


def protected_paths() -> list[Path]:
    """Never read by the daemon's shell, whatever the classifier's general rules say."""
    cfg = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    out = [Path(cfg) / "probe", _state_base() / "daemon", _state_base() / "approvals"]
    if os.environ.get("PROBE_CONFIG_PATH"):
        out.append(Path(os.environ["PROBE_CONFIG_PATH"]))
    return out


def _broad(path: Path, home: Path) -> bool:
    """`$HOME`, a folder above it, or a system folder (all resolved)."""
    return path == home or path in home.parents or path in _SYSTEM_DIRS


def _system_tree(path: Path) -> bool:
    """Inside a system tree (`/etc`, `/usr`, `/var`, `/proc`, `/lib*`...)?"""
    parts = path.parts
    if len(parts) >= 2 and parts[0] == "/" and parts[1].startswith("lib"):
        return True
    return any(path == tree or tree in path.parents for tree in _SYSTEM_TREES)


def _ok_folder(path: Path, home: Path, cwd: Path | None = None) -> bool:
    """A folder the daemon may treat as the session's: not hidden, never `$HOME`
    itself, a folder above it or a shared root. Under `$HOME` or the session's
    own folder `cwd`, hidden is judged below them; anywhere else (a data disk, a
    `/workspace`) it must also be outside every system tree."""
    try:
        resolved = path.resolve()
        home_r = home.resolve()
        cwd_r = cwd.resolve() if cwd is not None else None
    except OSError:
        return False
    if not resolved.is_dir() or _broad(resolved, home_r):
        return False
    roots = [home_r]
    if cwd_r is not None and not _broad(cwd_r, home_r):
        roots.append(cwd_r)
    for root in roots:
        try:
            rel = resolved.relative_to(root)
        except ValueError:
            continue
        return not any(part.startswith(".") for part in rel.parts)
    if _system_tree(resolved):
        return False
    return not any(part.startswith(".") for part in resolved.parts[1:])


_REDIRECTS = {">", ">>", ">|", "&>", "&>>", "1>", "2>", "1>>", "2>>"}


def written_paths(command: str) -> list[str]:
    """Paths a shell command WRITES (R5: shlex tokens, never first-word heads):
    redirect targets, `tee FILE`, `sed -i ... FILE`, and the destination of `cp`
    and `mv`. `cat > design.md` writes design.md; `cat design.md` writes nothing."""
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>()")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []
    out: list[str] = []
    segment: list[str] = []

    def flush() -> None:
        words = [w for w in segment if w]
        while words and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0]):
            words = words[1:]
        if not words:
            return
        head = words[0].rsplit("/", 1)[-1]
        args = [w for w in words[1:] if not w.startswith("-")]
        if head == "tee":
            out.extend(args)
        elif head == "sed" and any(w == "-i" or w.startswith("-i") or w == "--in-place" for w in words[1:]):
            out.extend(args[1:] if args else [])
        elif head in ("cp", "mv", "install", "rsync") and len(args) >= 2:
            out.append(args[-1])

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in _REDIRECTS or (tok.endswith(">") and tok.rstrip(">").isdigit()):
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("&"):
                out.append(tokens[i + 1])
            i += 2
            continue
        if tok in (";", "&&", "||", "|", "&", "(", ")", "\n"):
            flush()
            segment = []
        else:
            segment.append(tok)
        i += 1
    flush()
    return [p for p in out if p and p != "/dev/null"]


def working_folders(store: Store, cwd: Path, home: Path) -> list[Path]:
    """Recomputed from the store's commands and file writes (the session's folder
    first, then the most recent); cached as a fact. Once per bite."""
    found: list[Path] = []
    if _ok_folder(cwd, home, cwd):
        found.append(cwd.resolve())
    # The writer's view: a folder only `read only (daemon)` touched is not one of its.
    rows = store.db.execute("SELECT command, tool, tool_input, cwd FROM events WHERE kind = 'tool_call' "
                            f"AND (bite IS NULL OR bite != {UNRECORDED_BITE}) ORDER BY seq DESC LIMIT 2000")
    for row in rows:
        base = Path(row["cwd"]) if row["cwd"] else cwd
        for match in _CD_RE.findall(row["command"] or ""):
            target = Path(os.path.expanduser(match.strip("'\"")))
            target = target if target.is_absolute() else base / target
            if _ok_folder(target, home, cwd) and target.resolve() not in found:
                found.append(target.resolve())
            base = target if target.is_dir() else base
        for written in written_paths(row["command"] or ""):
            folder = Path(os.path.expanduser(written)).parent
            folder = folder if folder.is_absolute() else base / folder
            if _ok_folder(folder, home, cwd) and folder.resolve() not in found:
                found.append(folder.resolve())
        if row["tool"] in _WRITE_TOOLS and row["tool_input"]:
            try:
                import json

                data = json.loads(row["tool_input"])
            except ValueError:
                data = {}
            path = data.get("file_path") or data.get("path")
            if isinstance(path, str):
                folder = Path(os.path.expanduser(path)).parent
                folder = folder if folder.is_absolute() else base / folder
                if _ok_folder(folder, home, cwd) and folder.resolve() not in found:
                    found.append(folder.resolve())
    # A folder inside another adds nothing to the check.
    kept = [f for f in found if not any(f != g and g in f.parents for g in found)][:MAX_WORKING_FOLDERS]
    store.set_fact("working_folders", [str(f) for f in kept])
    return kept or ([cwd.resolve()] if cwd.is_dir() else [])


def _walk(folder: Path):
    count = 0
    base_depth = len(folder.parts)
    for root, dirs, files in os.walk(folder):
        depth = len(Path(root).parts) - base_depth
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".") and depth < MAX_DEPTH]
        for name in files:
            if name.startswith("."):
                continue
            count += 1
            if count > MAX_FILES_PER_FOLDER:
                return
            yield Path(root) / name


def _read_regular(path: Path, limit: int) -> bytes | None:
    """A regular file's bytes, at most `limit` of them, opened WITHOUT following a
    symlink (and never blocking on a FIFO swapped in since the walk looked)."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        return None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > limit:
            return None
        chunks = []
        left = limit
        while left > 0:
            chunk = os.read(fd, min(left, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            left -= len(chunk)
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(fd)


def _text_of(data: bytes) -> str | None:
    """`data` as text, or None when its head looks binary (a NUL, not UTF-8)."""
    head = data[:4096]
    if b"\0" in head:
        return None
    try:
        codecs.getincrementaldecoder("utf-8")().decode(head, final=len(data) <= 4096)
    except UnicodeDecodeError:
        return None
    return data.decode("utf-8", errors="replace")


@dataclass
class Seen:
    """One new or changed file, as the walk found it."""

    path: str
    size: int
    mtime: float
    text: str | None  # scrubbed; None for binary, too large, over budget, or secret
    secret: bool


def scan(workdirs: list[Path], known: dict[str, tuple[int, float]], *, is_secret: Callable[[str], bool],
         text_room: int) -> list[Seen]:
    """The files in `workdirs` that are new or changed since `known`. Touches only
    the file system (never the store), so it runs in a thread."""
    out: list[Seen] = []
    files = 0
    for folder in workdirs:
        for path in _walk(folder):
            files += 1
            if files > MAX_FILES_PER_CHECK:
                return out
            try:
                st = path.lstat()
            except OSError:
                continue
            if not stat.S_ISREG(st.st_mode):
                continue  # a symlink (to anything, a secret included), a FIFO, a socket, a device
            key = str(path)
            last = known.get(key)
            if last is not None and last[0] == st.st_size and abs(last[1] - st.st_mtime) < 1e-6:
                continue
            secret = is_secret(key)
            text = None
            if not secret and st.st_size <= min(text_room, MAX_TEXT_KEPT):
                data = _read_regular(path, min(text_room, MAX_TEXT_KEPT))
                raw = _text_of(data) if data is not None else None
                if raw is not None:
                    text = scrub(raw)
                    text_room -= len(text)
            out.append(Seen(key, st.st_size, st.st_mtime, text, secret))
    return out


def _prepare(store: Store, cwd: Path, home: Path, workdirs: list[Path] | None):
    from probe.daemon import shell

    folders = workdirs if workdirs is not None else working_folders(store, cwd, home)
    folders = [f for f in folders if _ok_folder(f, home, cwd)]
    checker = shell._Checker(workdirs=[], home=home, cwd=cwd, protected=protected_paths(), write_dirs=[])
    room = max(0, MAX_TEXT_STORED - store.stored_text_bytes())
    return folders, store.file_snapshot(), checker._secret, room


def _apply(store: Store, seen: list[Seen], *, emit: bool) -> int:
    events: list[Event] = []
    with store.tx():
        for s in seen:
            row = store.file_row(s.path)
            if emit:
                if s.secret:
                    what = (f"{'new' if row is None else 'changed'} file {s.path} ({s.size:,} bytes): a "
                            "credential-shaped name, so its content is not read")
                elif row is None:
                    what = f"new file {s.path} ({s.size:,} bytes)"
                    if s.text:
                        what += "\n" + s.text[:1500]
                else:
                    what = f"changed {s.path} ({row['size']:,} -> {s.size:,} bytes)"
                    if s.text is not None and row["text"] is not None:
                        diff = "\n".join(difflib.unified_diff(row["text"].splitlines(), s.text.splitlines(),
                                                              lineterm="", n=1))
                        what += "\n" + diff[:MAX_DIFF_CHARS]
                events.append(Event(kind=Kind.FILE_CHANGE, stream="folders", offset=store.next_offset(), text=what))
            store.set_file(s.path, s.size, s.mtime, s.text)
        if events:
            store.add(events)
    return len(events)


def check(store: Store, cwd: Path, home: Path, *, emit: bool = True, workdirs: list[Path] | None = None) -> int:
    folders, known, is_secret, room = _prepare(store, cwd, home, workdirs)
    return _apply(store, scan(folders, known, is_secret=is_secret, text_room=room), emit=emit)


async def check_async(store: Store, cwd: Path, home: Path, *, emit: bool = True,
                      workdirs: list[Path] | None = None) -> int:
    """`check`, with the walk in a thread: a big folder never stalls the loop."""
    folders, known, is_secret, room = _prepare(store, cwd, home, workdirs)
    seen = await asyncio.to_thread(scan, folders, known, is_secret=is_secret, text_room=room)
    return _apply(store, seen, emit=emit)


async def baseline(store: Store, cwd: Path, home: Path) -> None:
    if store.fact("folders_baselined"):
        return
    await check_async(store, cwd, home, emit=False)
    store.set_fact("folders_baselined", True)
