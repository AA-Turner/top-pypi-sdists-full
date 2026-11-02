"""pi's TranscriptLocator: its session roots and the header that marks a pi session file."""

from __future__ import annotations
import json
import os
from pathlib import Path


#: Mirrors tap/pi_discovery.py's SESSION_ROOTS_ENV exactly -- reimplemented
#: rather than imported (separate distributions, see tap_core/__init__.py).
#: pi is NOT given a row in `_ROOT_ENV`/`_ROOT_PARENT_INDEX`/`_ROOT_NAME`
#: above: those three assume a single relocatable directory with a fixed name
#: at a fixed depth, which is true for Claude Code and Codex because they own
#: their session layout -- and false for pi, whose `SessionManager` is a
#: published library an embedder points wherever it likes (see
#: pi_discovery.py's module docstring for the "fork moves the whole tree"
#: case). So pi gets its own ladder-free root resolution below instead of a
#: slot in the shared one.
_PI_SESSION_ROOTS_ENV = "PROBE_PI_SESSION_ROOTS"


def pi_root() -> Path:
    """Where `SessionManager.create(cwd)` writes when nothing overrides it.

    Not the only place a pi session can live -- see `pi_session_roots` -- just
    the one canonical path callers that want a single answer (tests, status
    output) can ask for, the same role `claude_root`/`codex_root` play for
    their agents.
    """
    return Path.home() / ".pi" / "agent" / "sessions"


def pi_session_roots() -> list[Path]:
    """Every configured pi session root, or just the upstream default.

    `PROBE_PI_SESSION_ROOTS` is os.pathsep-separated, same convention as PATH
    and the same env var tap/pi_discovery.py reads -- a machine that relocated
    its pi roots for the live tap relocated them for this importer too.
    """
    raw = (os.environ.get(_PI_SESSION_ROOTS_ENV) or "").strip()
    if not raw:
        return [pi_root()]
    return [Path(p).expanduser() for p in raw.split(os.pathsep) if p.strip()]


def _is_pi_session_file(path: Path) -> bool:
    """True when `path`'s first line is a pi session header.

    Mirrors tap/pi_discovery.py's `is_pi_session_file` (reimplemented, not
    imported -- separate distributions, see tap_core/__init__.py). Claude Code
    and Codex each write to one fixed, named directory this module already
    trusts (`_ROOT_NAME`), so every `.jsonl` under their roots is presumed
    theirs. pi has no such guarantee -- an embedder's configured
    `PROBE_PI_SESSION_ROOTS` entry can be a directory shared with unrelated
    `.jsonl` files -- so pi transcripts are found by shape instead.
    """
    try:
        with path.open("rb") as handle:
            head = handle.read(8192)
    except OSError:
        return False
    if not head:
        return False
    newline = head.find(b"\n")
    if newline == -1:
        return False
    try:
        first = json.loads(head[:newline])
    except (ValueError, UnicodeDecodeError, RecursionError):
        return False
    return isinstance(first, dict) and first.get("type") == "session"
