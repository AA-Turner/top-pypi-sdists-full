"""Claude Code's TranscriptLocator: projects/ root and its relocations, and the prompt history that names each session's cwd."""

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import NamedTuple


def claude_root() -> Path:
    """The default location. See `transcript_roots` for what is actually walked."""
    return _env_path(_ROOT_ENV[CLAUDE]) or Path.home() / ".claude" / "projects"


def _config_roots(agent: str) -> list[Path]:
    """Roots implied by a relocation env var, as their OWN rung.

    Deliberately NOT folded into the default: someone who worked for months in
    `~/.claude` and then set `CLAUDE_CONFIG_DIR` has transcripts in BOTH, and
    replacing one with the other silently drops the older half -- the same
    confident-zero this ladder exists to remove, just moved.
    """
    if agent == CLAUDE:
        config = _env_path("CLAUDE_CONFIG_DIR")
        return [config / "projects"] if config else []
    home = _env_path("CODEX_HOME")
    return [home / "sessions"] if home else []


def history_path(root: Path) -> Path:
    """Claude Code's prompt history, which sits beside `projects/`."""
    return root.parent / "history.jsonl"


class HistoryEntry(NamedTuple):
    """One session Claude Code's prompt history remembers."""

    #: The REAL working directory, un-encoded. The directory name on disk is a
    #: lossy encoding of this; here it is recorded verbatim.
    cwd: str | None
    #: Epoch seconds of the last prompt typed in that session.
    at: float


def history_sessions(root: Path) -> dict[str, HistoryEntry]:
    """`session_id -> cwd` for every session that ever took a prompt.

    A SECOND, INDEPENDENT DENOMINATOR, and neither it nor the walk is a superset
    of the other. Measured on the machine this was written against: 201 sessions
    here, 179 transcripts on disk, 167 in both -- so the walk alone under-reports
    the population by about 16%, and reports its own count as if it were
    complete. That is the exact failure this module was built to prevent, so the
    difference is counted and shown rather than left invisible.

    It is NOT a source of transcripts: a session listed here with no file has no
    content to upload. It is a source of TRUTH ABOUT THE COUNT.

    (The 12 that go the other way -- a transcript with no history entry -- are
    headless `claude -p` runs, which never write interactive prompt history.)
    """
    sessions: dict[str, HistoryEntry] = {}
    path = history_path(root)
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return sessions
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except (ValueError, RecursionError):
            continue  # a torn line costs one entry, never the file
        if not isinstance(entry, dict):
            continue
        session_id = entry.get("sessionId")
        if not isinstance(session_id, str) or not session_id:
            continue
        stamp = entry.get("timestamp")
        at = float(stamp) / 1000 if isinstance(stamp, (int, float)) else 0.0
        previous = sessions.get(session_id)
        if previous is None:
            sessions[session_id] = HistoryEntry(entry.get("project"), at)
        elif at > previous.at:
            sessions[session_id] = HistoryEntry(previous.cwd or entry.get("project"), at)
    return sessions


#: Claude Code names every session file with the bare session uuid. Case kept
#: loose (macOS filesystems preserve but do not enforce case).
_CLAUDE_SESSION_STEM_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
from probe.cli.imports.transcripts.roots import CLAUDE, _ROOT_ENV  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.transcripts import _env_path  # noqa: E402 -- pieces need each other; the front door loads this one first
