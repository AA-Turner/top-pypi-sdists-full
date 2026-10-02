"""Standalone import of the coding-agent history this machine already holds.

Explicit consent covers the machine transcript census. Producer-native records
validate identity; matching copies reconcile by content. CLI and live tap share
an immutable pre-send journal with separate source/event cursors. Remote receipts
prove accepted coverage; legacy offsets cannot authorize replay. Imports never
create research entity links.

Upload and finalization are the whole lane. The local digest stage that used to
follow them -- render a view, launch the machine's own agent, POST the result --
was removed when the session-digest lane was retired server-side: there is no
POST /v1/sessions/{id}/digest to send one to, and nothing generates or stores
session digests any more.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import sqlite3
import time
from collections.abc import Callable, Iterable, Iterator
from dataclasses import asdict, dataclass, field, replace
from probe._compat import StrEnum
from pathlib import Path
from typing import NamedTuple

from ..sdk.durable import file_lock, fsync_directory, now_iso
from ..sdk.tls import ssl_context
from ..tap_core import codex_sanitize, pi_sanitize, sanitize
from ..tap_core.session_identity import compatible_copy, validate_identity
from ..tap_core.session_journal import (
    DELETED_STATE, DeliveryPending, Journal, ReconciliationRequired, SessionDeleted, Wire,
    prefix_hash,
)
from ..tap_core.transcript import (
    MAX_BATCH_BYTES,
)

CLAUDE = "claude_code"
CODEX = "codex"
PI = "pi"

#: The ingest route per agent. The gateway binds a paired device to ONE source
#: and answers 403 for the other, which the tap's classifier treats as a
#: permanent drop -- so posting a Codex rollout to the Claude Code door does not
#: fail loudly, it fails silently. The mapping is data, not a branch, to keep
#: that impossible. Mirrors tap/sources.py's per-source `webhook_path` --
#: reimplemented rather than imported, because the tap plugin and this CLI are
#: separate distributions (see tap_core/__init__.py's module docstring). A
#: source present in that registry but missing here is a live bug: `discover()`
#: happily finds and queues that agent's transcripts, and `upload_session`
#: KeyErrors on the very first one it tries to send -- see
#: test_ingest_path_and_sanitizer_cover_every_tap_capture_source.
INGEST_PATH = {
    CLAUDE: "/ingest/v1/sessions/claude-code",
    CODEX: "/ingest/v1/sessions/codex",
    PI: "/ingest/v1/sessions/pi",
}

#: Claude Code writes tool OUTPUT twice: once as a `tool_result` block inside
#: `message.content`, which the sanitizer compacts to a byte count, and once as
#: a top-level `toolUseResult` object, which it does not touch. That second copy
#: carries `originalFile` (whole file contents), `oldString`/`newString` (entire
#: edit bodies) and `stdout`/`stderr` (full command output). Measured over one
#: real 12.9MB session on the machine this was written against: present on 329
#: events and 54% of all sanitized bytes.
#:
#: THE IMPORT LANE DROPS IT, AND LIVE CAPTURE IS LEFT ALONE. The two are
#: different bargains. Someone who turns capture on is consenting to their
#: sessions being recorded from that moment, and the engine's extraction reads
#: that field. This lane ships history nobody consented to at the time, under a
#: screen that promises file contents and tool output do not leave -- so for
#: historical transcripts the promise wins. Changing the shared sanitizer would
#: change live capture for every existing user, which is a product decision and
#: not this feature's to make silently.
_HEAVY_TOP_LEVEL = ("toolUseResult",)


def _import_sanitizer(inner):
    """The canonical sanitizer, plus the drops an unconsented import needs."""

    def sanitize_for_import(event):
        result = inner(event)
        if isinstance(result, dict):
            for key in _HEAVY_TOP_LEVEL:
                result.pop(key, None)
        return result

    return sanitize_for_import


SANITIZER = {
    CLAUDE: _import_sanitizer(sanitize.sanitize_event),
    CODEX: _import_sanitizer(codex_sanitize.sanitize_event),
    PI: _import_sanitizer(pi_sanitize.sanitize_event),
}

#: How many bytes one line may be read into memory at a time. A transcript can
#: be tens of MB and `read_new` reads to EOF in one call, so the importer walks
#: it in windows instead of materialising the file.
READ_WINDOW_BYTES = 4 * 1024 * 1024

#: Wire-body target. The gateway hard-caps at 2MB and maps the 413 to a
#: permanent drop, so batches are built to half that -- the same budget the tap
#: uses, from the same constant.
BATCH_BYTES = MAX_BATCH_BYTES

#: Give up on one session after this many consecutive transport failures. The
#: session stays PARTIAL in the ledger and the next run resumes it; what this
#: prevents is one unreachable server turning a 500-session import into 500
#: identical stack traces.
MAX_RETRIES_PER_BATCH = 4

SCHEMA = "probe.backfill.transcripts/1"


# --- discovery ---------------------------------------------------------------


#: The explicit override per agent. Same names the tap uses, so a machine that
#: relocated one relocated both.
_ROOT_ENV = {
    CLAUDE: "PROBE_RESEARCH_TAP_PROJECTS_DIR",
    CODEX: "PRBE_CODEX_SESSIONS_DIR",
}

#: How far above a transcript its ROOT sits, as an index into `Path.parents`.
#: Claude Code files are `<root>/<cwd-slug>/<session>.jsonl`; Codex partitions
#: by date, `<root>/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl`. Derived rather than
#: assumed because these are the depths that make a LEARNED path (below) into a
#: root worth walking.
_ROOT_PARENT_INDEX = {CLAUDE: 1, CODEX: 3}


#: The directory name a root MUST have. Claude Code always writes
#: `<config>/projects`, Codex always `<CODEX_HOME>/sessions` -- both are fixed
#: by those tools, not by us -- so the name is a cheap, reliable check that a
#: derived root is a transcript tree rather than something a bad row pointed at.
_ROOT_NAME = {CLAUDE: "projects", CODEX: "sessions"}


def _env_path(name: str) -> Path | None:
    """An env var as a path, tilde expanded. None when unset or empty.

    `expanduser` because these are routinely set in a config file or quoted in
    a shell, where `~` arrives literally: without it the value becomes a
    RELATIVE path, `is_dir()` is false, and the honest "Looked in:" line would
    name a directory nothing ever searched.
    """
    raw = (os.environ.get(name) or "").strip()
    return Path(raw).expanduser() if raw else None


def claude_root() -> Path:
    """The default location. See `transcript_roots` for what is actually walked."""
    return _env_path(_ROOT_ENV[CLAUDE]) or Path.home() / ".claude" / "projects"


def codex_root() -> Path:
    """Codex's default. `CODEX_HOME` is Codex's OWN relocation knob, and this
    package already honours it in `codex_config` and `agent_rules` -- resolving
    it here too is what keeps the Codex half from having the silent-zero bug the
    Claude half just lost."""
    override = _env_path(_ROOT_ENV[CODEX])
    if override:
        return override
    home = _env_path("CODEX_HOME")
    return (home / "sessions") if home else Path.home() / ".codex" / "sessions"


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


def _tap_offsets(plugin_dir: Path) -> list[tuple[str, str]]:
    """`(path, session_id)` rows from the tap's cursor. One read, closed.

    Both things this module wants from the tap -- which sessions it already
    tracks, and where it has seen transcripts -- come from the same table, so
    they come from the same query. `closing` because `sqlite3.connect` as a
    context manager commits a TRANSACTION and leaves the handle to the garbage
    collector.
    """
    db = plugin_dir / "state.db"
    if not db.exists():
        return []
    try:
        with contextlib.closing(sqlite3.connect(f"file:{db}?mode=ro", uri=True)) as conn:
            return [
                (str(row[0]), str(row[1] or ""))
                for row in conn.execute("SELECT path, session_id FROM file_offsets")
                if row and row[0]
            ]
    except sqlite3.Error:
        return []


def learned_roots(agent: str, plugin_dir: Path) -> list[Path]:
    """Transcript roots the tap has actually OBSERVED on this machine.

    The strongest evidence available, and it costs one column of a query this
    module already makes. `file_offsets.path` holds absolute paths the tap was
    HANDED by the agent itself -- the SessionStart hook passes the real
    transcript path -- so these are ground truth no matter where the config
    directory lives, including layouts nothing here knows to guess.

    Bootstrapping limit, stated honestly: this only helps where capture has run
    at least once, and this importer exists for machines where it mostly has
    not. One row is enough to reveal a root, though, and where there are zero
    the ladder below still has `CLAUDE_CONFIG_DIR` and the default.
    """
    index = _ROOT_PARENT_INDEX[agent]
    roots: list[Path] = []
    for path, _session in _tap_offsets(plugin_dir):
        parents = Path(path).parents
        if len(parents) <= index:
            continue
        root = parents[index]
        # THE NAME CHECK IS NOT COSMETIC. The index assumes a layout, and the
        # tap does not enforce one -- it resolves a Codex rollout by rglob at
        # ANY depth, so a flat row makes `parents[3]` something like `/home`,
        # and a two-segment row makes `parents[1]` `/`. Handing either to
        # `_walk` would rglob a whole home directory and offer every `.jsonl`
        # under it as a transcript to upload. Both agents fix their own
        # directory name, so requiring it rejects every one of those without
        # rejecting any real tree.
        if root.name != _ROOT_NAME[agent]:
            continue
        if root not in roots and root.is_dir():
            roots.append(root)
    return roots


def transcript_roots(agent: str, plugin_dir: Path | None = None) -> list[Path]:
    """Every directory that might hold this agent's transcripts, best first.

    A LADDER rather than one guess, because the failure it replaces is silent:
    a machine whose config directory was relocated reported "no agent
    sessions found", which is a confident zero and indistinguishable from
    a machine that genuinely has none.

        explicit override  -- the caller said where; nothing else is consulted
        learned            -- where the tap has actually seen transcripts
        CLAUDE_CONFIG_DIR  -- the documented relocation knob (Claude Code only)
        the default        -- the guess, last

    Returns every distinct EXISTING directory, so a machine with more than one
    config dir is walked in full rather than only in its first.

    pi does not join the ladder above: it has no single relocatable directory
    to rank rungs against (see `pi_session_roots`'s docstring), so its roots
    come from `PROBE_PI_SESSION_ROOTS`/the upstream default directly, with the
    same "existing, else the first candidate" fallback the ladder ends on.
    """
    if agent == PI:
        candidates = pi_session_roots()
        existing = [root for root in candidates if root.is_dir()]
        return existing or candidates[:1]

    env = os.environ.get(_ROOT_ENV[agent])
    if env:
        # An explicit answer is an answer. Adding guesses beside it would walk
        # trees the caller deliberately excluded.
        return [Path(env)]

    roots: list[Path] = []
    if plugin_dir is not None:
        roots.extend(learned_roots(agent, plugin_dir))
    for candidate in (*_config_roots(agent), claude_root() if agent == CLAUDE else codex_root()):
        if candidate not in roots:
            roots.append(candidate)
    existing = [root for root in roots if root.is_dir()]
    # Nothing exists: hand back the FIRST candidate so the caller's "Looked in"
    # names something real rather than an empty list.
    return existing or roots[:1]


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
        except ValueError:
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


@dataclass(frozen=True)
class Transcript:
    """One session's log on disk."""

    path: Path
    session_id: str
    agent: str
    #: The working directory the session ran in, read from the transcript's own
    #: content. NEVER derived from the containing directory name: Claude Code
    #: encodes the cwd into that name by replacing every separator with a dash,
    #: which is not reversible -- `/home/a-b/c` and `/home/a/b/c` produce the
    #: same directory. An unreadable cwd stays None; it is source context only.
    cwd: str | None
    size: int
    mtime: float


#: Codex rollout filenames end with the session uuid: rollout-<ts>-<uuid>.jsonl.
#: pi's do too, with a different prefix: <ts>_<uuid>.jsonl. The SAME anchored
#: pattern the tap's reconciler uses for both, deliberately: this importer
#: ships the complement of what the tap tracks, and two different notions of
#: "the session id" would make that complement wrong at the edges. A loose
#: split would also mint an id from any dashed filename that happened to be
#: under the sessions directory.
_UUID_SUFFIX_RE = re.compile(
    r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$"
)


#: Claude Code names every session file with the bare session uuid. Case kept
#: loose (macOS filesystems preserve but do not enforce case).
_CLAUDE_SESSION_STEM_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def session_id_for(path: Path, agent: str) -> str | None:
    """The session id a transcript filename encodes, or None if it has none."""
    stem = path.stem
    if stem.startswith("agent-"):
        # Subagent sidechain: no session identity of its own, under any agent.
        # Checked before the branch so the rule cannot apply to some and not
        # others.
        return None
    if agent in (CODEX, PI):
        match = _UUID_SUFFIX_RE.search(stem)
        return match.group(1) if match else None
    # Claude Code session files are `<uuid>.jsonl`; anything else in the
    # directory is a foreign file, not a session. The Workflow tool drops a
    # `journal.jsonl` right beside real transcripts, and treating its stem as
    # a session id crashed the whole run one server round-trip later ("could
    # not check journal: malformed session id") — discovery is where a
    # non-session file must be rejected, quietly, like a sidechain.
    return stem if _CLAUDE_SESSION_STEM_RE.fullmatch(stem) else None


def read_cwd(path: Path, agent: str, *, max_lines: int = 200) -> str | None:
    """The cwd recorded inside a transcript.

    SCANS, rather than reading line one. Claude Code's first line is often a
    `queue-operation` carrying only `{type, sessionId, timestamp, content}`, and
    Codex writes its `session_meta` first but not always. Bounded so a huge
    transcript with no cwd at all costs a few KB, not a full read.
    """
    try:
        with path.open("rb") as handle:
            for index, raw in enumerate(handle):
                if index >= max_lines:
                    return None
                try:
                    event = json.loads(raw)
                except (ValueError, UnicodeDecodeError):
                    continue
                if not isinstance(event, dict):
                    continue
                if agent == CODEX:
                    payload = event.get("payload")
                    if isinstance(payload, dict):
                        found = payload.get("cwd")
                        if isinstance(found, str) and found:
                            return found
                    continue
                if agent == PI:
                    # pi's cwd lives only on the "session" header entry (see
                    # pi_sanitize.py's _translate_session_header) -- reading it
                    # from the raw event here, rather than de-slugging the
                    # containing directory name the way the encoded Claude Code
                    # dirname tempts, because a SessionManager embedder can
                    # point pi's roots anywhere and the directory name is not
                    # guaranteed to encode anything at all.
                    if event.get("type") != "session":
                        continue
                    found = event.get("cwd")
                    if isinstance(found, str) and found:
                        return found
                    continue
                found = event.get("cwd")
                if isinstance(found, str) and found:
                    return found
    except OSError:
        return None
    return None


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
    except (ValueError, UnicodeDecodeError):
        return False
    return isinstance(first, dict) and first.get("type") == "session"


def _walk(root: Path, agent: str) -> Iterator[Path]:
    if not root.exists():
        return
    candidates = sorted(root.rglob("*.jsonl"))
    if agent == PI:
        yield from (path for path in candidates if _is_pi_session_file(path))
        return
    yield from candidates


@dataclass
class Census:
    """The denominator, and every reason a transcript is not in it.

    Every count here is produced by walking the disk, never by a model, for the
    same reason the file importer's census is: silent partial coverage that
    reads as "done" is the failure this whole flow exists to make impossible.
    Each exclusion is counted separately because they mean opposite things --
    `captured_live` is healthy, `unreadable` is a problem, `already_in_probe`
    is the duplicate check working.
    """

    candidates: list[Transcript] = field(default_factory=list)
    #: Every session id seen on disk, before any exclusion.
    seen: int = 0
    sidechains: int = 0
    duplicates: int = 0
    captured_live: int = 0
    already_in_probe: int = 0
    unreadable: int = 0
    identity_unverified: int = 0
    identity_conflicts: int = 0
    #: Sessions Claude Code's prompt history records that left NO transcript
    #: file. Nothing to upload -- there is no content for them -- but counting
    #: them is what stops the walk's own total from reading as the whole
    #: population. See `history_sessions`.
    known_no_transcript: int = 0
    #: Every directory actually walked, so an empty result can say WHERE it
    #: looked instead of only that it found nothing.
    roots: list[Path] = field(default_factory=list)

    @property
    def bytes(self) -> int:
        return sum(t.size for t in self.candidates)

    @property
    def sessions(self) -> int:
        return len(self.candidates)


def discover(
    *,
    agents: Iterable[str] = (CLAUDE,),
    tracked: set[str] | None = None,
    plugin_dirs: dict[str, Path] | None = None,
) -> Census:
    """Walk the machine's transcript trees and bucket what is there.

    Deliberately does NOT ask the server anything: this is the deterministic
    half, and it has to be reproducible offline. `already_in_probe` is filled
    in later by `exclude_ingested`.

    `plugin_dirs` lets the roots be LEARNED from the tap's own cursor rather
    than guessed -- see `transcript_roots`. Omitted, discovery still works from
    the override and the default; it just cannot find a relocated tree.
    """
    tracked = tracked or set()
    plugin_dirs = plugin_dirs or {}
    census = Census()
    by_session: dict[str, Transcript] = {}
    conflicting: set[str] = set()
    #: Every id seen on disk INCLUDING the ones excluded below. The history
    #: cross-check asks "does a file exist", which tracked and duplicate
    #: sessions both answer yes to.
    on_disk: set[str] = set()

    for agent in agents:
        agent_roots = transcript_roots(agent, plugin_dirs.get(agent))
        census.roots.extend(r for r in agent_roots if r not in census.roots)
        for path in (p for root in agent_roots for p in _walk(root, agent)):
            session_id = session_id_for(path, agent)
            if session_id is None:
                census.sidechains += 1
                continue
            census.seen += 1
            on_disk.add(session_id)
            try:
                stat = path.stat()
                validate_identity(path, agent, session_id)
            except ReconciliationRequired:
                census.identity_unverified += 1
                continue
            except OSError:
                census.unreadable += 1
                continue
            if session_id in tracked:
                census.captured_live += 1
                continue
            key = f"{agent}:{session_id}"
            if key in conflicting:
                continue
            if key in by_session:
                census.duplicates += 1
                if not compatible_copy(path, by_session[key].path):
                    census.identity_conflicts += 1
                    conflicting.add(key)
                    del by_session[key]
                    continue
                if stat.st_size <= by_session[key].size:
                    continue
            by_session[key] = Transcript(
                path=path,
                session_id=session_id,
                agent=agent,
                cwd=read_cwd(path, agent),
                size=stat.st_size,
                mtime=stat.st_mtime,
            )

    # The second denominator. Only Claude Code keeps a prompt history; Codex
    # has no equivalent, so its population is whatever the walk found.
    if CLAUDE in agents:
        # BOUNDED BY THE OLDEST SURVIVING TRANSCRIPT, because history is never
        # pruned and transcripts are (Claude Code's `cleanupPeriodDays`, 30 by
        # default). Everything older than the oldest file we still have was
        # almost certainly DELETED rather than never written, and counting it
        # would put a number on the consent screen that grows for the life of
        # the machine while claiming something untrue about every entry in it.
        # With no transcripts at all there is no horizon to draw, so nothing is
        # claimed.
        horizon = min((t.mtime for t in by_session.values()), default=None)
        if horizon is not None:
            for root in transcript_roots(CLAUDE, plugin_dirs.get(CLAUDE)):
                for session_id, entry in history_sessions(root).items():
                    if session_id not in on_disk and entry.at >= horizon:
                        census.known_no_transcript += 1

    # Newest first: an interrupted import should have shipped the sessions
    # someone is most likely to be looking for.
    census.candidates = sorted(by_session.values(), key=lambda t: t.mtime, reverse=True)
    return census


def tap_tracked_sessions(plugin_dir: Path) -> set[str]:
    """Session ids the live capture plugin already has a cursor for.

    Read straight from the tap's SQLite, read-only, the same way
    `capabilities.capture_device_id` does -- the plugin's Python may not be
    runnable from here, and shelling out to it would make this importer depend
    on the plugin being healthy rather than merely present.

    An unreadable or absent database returns an EMPTY set, which is the safe
    direction: every session then looks untracked, and the server-side
    duplicate check is what actually prevents a re-upload.
    """
    return {session for _path, session in _tap_offsets(plugin_dir) if session}


# --- the server-side duplicate check ----------------------------------------


@dataclass(frozen=True)
class IngestState:
    known: bool
    #: A paired device uploaded this transcript, and nothing more. The route
    #: also answered `digested`/`digest_prompt_version` until the digest lane
    #: was retired; both are gone from the response, not merely unread here.
    ingested: bool


class ProbeUnavailable(RuntimeError):
    """The duplicate check could not be answered. Do NOT treat as "not there"."""


def _is_route_absent(exc: Exception) -> bool:
    """Whether a failed read means "this server has no such route".

    A 404 from a route that exists is impossible here: the endpoint answers
    200 with `known=false` for an id it has never seen, precisely so the
    importer's normal case is not an exception path. So a NotFoundError can
    only mean the deployment predates the route.
    """
    from ..sdk import errors

    return isinstance(exc, errors.NotFoundError | errors.UnroutableEndpointError)


def fetch_ingest_state(client, session_id: str) -> IngestState | None:
    """Ask the server what it already holds.

    Three outcomes, and collapsing any two of them is a bug:
      IngestState       the server answered.
      None              the ROUTE does not exist -- a self-host older than this
                        feature. Degraded but workable: fall back to local
                        knowledge and ship.
      ProbeUnavailable  the question could not be asked (timeout, 5xx, DNS).

    The third used to be folded into the second, which is the expensive
    mistake: a flaky link during the pre-flight pass would report every session
    as "not in Probe", and the importer would re-POST from batch_seq 0 over
    sessions the server already holds -- overwriting their stored blobs, since
    the engine keys on "<session>:<seq>" and takes the last write. A transient
    failure must stop the lane, never silently authorise a re-upload.
    """
    try:
        body = client.transport.get(f"/v1/sessions/{session_id}/ingest-state")
    except Exception as exc:
        if _is_route_absent(exc):
            return None
        raise ProbeUnavailable(f"could not check {session_id}: {exc}") from exc
    if not isinstance(body, dict):
        return None
    return IngestState(
        known=bool(body.get("known")),
        ingested=bool(body.get("ingested")),
    )


def exclude_ingested(census: Census, client, *, ledger: TranscriptLedger | None = None) -> Census:
    """Drop candidates the server already holds a transcript for.

    THE LEDGER TRUMPS THE PROBE for a session this importer itself started:
    a PARTIAL upload has already produced an activity row with a device id, so
    the server would answer `ingested` and the resume would be skipped forever,
    stranding the tail of the very session we were shipping.
    """
    resumable = ledger.resumable_sessions() if ledger else set()
    keep: list[Transcript] = []
    for transcript in census.candidates:
        if transcript.session_id in resumable:
            keep.append(transcript)
            continue
        # A ProbeUnavailable propagates on purpose: it means the duplicate
        # check is blind, and shipping blind overwrites stored batches.
        state = fetch_ingest_state(client, transcript.session_id)
        if state is not None and state.ingested:
            census.already_in_probe += 1
            continue
        keep.append(transcript)
    census.candidates = keep
    return census


# --- the ledger --------------------------------------------------------------


class SessionState(StrEnum):
    PENDING = "pending"
    PARTIAL = "partial"
    DONE = "done"
    FAILED = "failed"


@dataclass
class SessionRecord:
    session_id: str
    path: str = ""
    agent: str = CLAUDE
    state: SessionState = SessionState.PENDING
    #: The last batch sequence this importer successfully POSTed. The next one
    #: is +1, always -- a reused sequence overwrites a stored blob rather than
    #: being rejected, so this number may never go backwards.
    last_seq: int = -1
    #: How far into the file those batches got. Re-derived from the file rather
    #: than accumulated, because blank lines and \r stripping mean summed line
    #: lengths are not a file position.
    byte_end: int = 0
    #: How many lines have been shipped. Carried because `line_no` in the wire
    #: envelope orders events WITHIN the session document: a resumed upload that
    #: restarted the count at zero would file its second half on top of its
    #: first.
    line_no: int = 0
    finalized: bool = False
    anchored: bool = False
    error: str | None = None


class TranscriptLedger:
    """What this machine has already imported. Append-only, folded on read.

    Device-scoped, not folder-scoped: the thing it tracks is a machine's
    transcript history, which no folder owns. Same primitives and the same
    crash posture as the file importer's ledger -- one line per fact, fsynced
    under a lock, and a torn final line is skipped rather than fatal.
    """

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(".lock")

    @classmethod
    def for_device(cls, *, directory: Path | None = None) -> TranscriptLedger:
        from .backfill_ledger import default_dir

        base = directory or default_dir()
        return cls(base / "transcripts.jsonl")

    def _append(self, record: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        record.setdefault("schema", SCHEMA)
        record.setdefault("at", now_iso())
        line = json.dumps(record, ensure_ascii=False)
        with file_lock(self.lock_path):
            created = not self.path.exists()
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            if created:
                fsync_directory(self.path.parent)
                try:
                    os.chmod(self.path, 0o600)
                except OSError:
                    pass

    def record_census(self, census: Census) -> None:
        self._append(
            {
                "t": "census",
                "sessions": census.sessions,
                "bytes": census.bytes,
                "sidechains": census.sidechains,
                "captured_live": census.captured_live,
                "already_in_probe": census.already_in_probe,
            }
        )

    def record_session(self, record: SessionRecord) -> None:
        self._append(
            {
                "t": "session",
                "session_id": record.session_id,
                "path": record.path,
                "agent": record.agent,
                "state": record.state.value,
                "last_seq": record.last_seq,
                "byte_end": record.byte_end,
                "line_no": record.line_no,
                "finalized": record.finalized,
                "anchored": record.anchored,
                "error": record.error,
            }
        )

    def read(self) -> dict[str, SessionRecord]:
        """Fold the log. Unknown record kinds are ignored, not fatal.

        A newer importer may write facts this one does not understand; refusing
        the file would turn a forward-compatible addition into a re-upload of
        every session on the machine.
        """
        state: dict[str, SessionRecord] = {}
        if not self.path.exists():
            return state
        try:
            lines = self.path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return state
        for line in lines:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except ValueError:
                continue  # torn final line: skip, never fatal
            if record.get("t") != "session":
                continue
            session_id = record.get("session_id")
            if not session_id:
                continue
            try:
                session_state = SessionState(record.get("state", "pending"))
            except ValueError:
                session_state = SessionState.PENDING
            state[session_id] = SessionRecord(
                session_id=session_id,
                path=record.get("path", ""),
                agent=record.get("agent", CLAUDE),
                state=session_state,
                last_seq=int(record.get("last_seq", -1)),
                byte_end=int(record.get("byte_end", 0)),
                line_no=int(record.get("line_no", 0)),
                finalized=bool(record.get("finalized")),
                anchored=bool(record.get("anchored")),
                error=record.get("error"),
            )
        return state

    def resumable_sessions(self) -> set[str]:
        """Sessions this importer started and did not finish."""
        return {
            session_id
            for session_id, record in self.read().items()
            if record.state in (SessionState.PARTIAL, SessionState.FAILED)
        }

    def done_sessions(self) -> set[str]:
        return {
            session_id
            for session_id, record in self.read().items()
            if record.state is SessionState.DONE
        }


# --- upload ------------------------------------------------------------------


@dataclass
class Poster:
    """Paired destination configuration; delivery uses the shared protocol Wire."""

    base_url: str
    token: str
    timeout: float = 30.0


@dataclass
class UploadResult:
    session_id: str
    batches: int = 0
    bytes_sent: int = 0
    ok: bool = False
    error: str | None = None
    retryable: bool = False
    already_finalized: bool = False
    #: The server deleted this session at its team's request: final, nothing
    #: was or will be uploaded. Counted as a skip, never as a failure.
    deleted: bool = False


def _failure_message(exc: Exception) -> str:
    """Authored protocol prose is safe; OS/SQLite strings can contain paths."""
    if isinstance(exc, (DeliveryPending, ReconciliationRequired)):
        return exc.safe_message
    if isinstance(exc, sqlite3.Error):
        return f"local transcript journal failed ({getattr(exc, 'sqlite_errorname', type(exc).__name__)})"
    if isinstance(exc, OSError) and exc.errno is not None:
        return f"local transcript access failed ({type(exc).__name__}, errno {exc.errno})"
    return f"local transcript access failed ({type(exc).__name__})"


def _finalized_coverage(
    transcript: Transcript,
    remote: dict,
    *,
    approved: dict | None = None,
    expected_customer_id: str | None = None,
) -> dict | None:
    """Prove reviewed bytes already landed without changing the shared journal.

    Capture or another import can finish a longer prefix after this job was
    approved. Its cursor must not be validated against our shorter temporary
    copy, nor may this job deliver its pending tail. Equal boundaries are
    proved directly by the approved hash; larger boundaries require the
    original source to prove both prefixes belong to the accepted stream.
    """
    if expected_customer_id is not None and remote.get("customer_id") != expected_customer_id:
        raise ReconciliationRequired("capture credentials belong to a different team")
    if (remote.get("source"), remote.get("session_id")) != (
        transcript.agent, transcript.session_id,
    ) or not remote.get("customer_id"):
        raise ReconciliationRequired("refusing adoption across transcript destination identities")
    stream = remote.get("stream")
    if (
        remote.get("protocol_version") != 2 or remote.get("state") != "ready"
        or not isinstance(stream, dict) or stream.get("finalized") is not True
    ):
        return None
    end = int(approved["size"]) if approved is not None else transcript.path.stat().st_size
    remote_end = stream.get("source_byte_end")
    if not isinstance(remote_end, int) or remote_end < end:
        return None
    expected_hash = approved["sha256"] if approved is not None else prefix_hash(transcript.path, end)
    if remote_end == end:
        return stream if stream.get("prefix_sha256") == expected_hash else None
    # Both hashes come from one read of one descriptor. Separate reads could
    # prove the approved prefix from one version and the receipt from another.
    # Extra bytes are evidence only, never this import's upload source.
    digest = hashlib.sha256()
    approved_hash = digest.hexdigest() if end == 0 else None
    with transcript.path.open("rb") as handle:
        before = os.fstat(handle.fileno())
        offset = 0
        while offset < remote_end:
            boundary = end if offset < end else remote_end
            chunk = handle.read(min(1024 * 1024, boundary - offset))
            if not chunk:
                raise ReconciliationRequired("source truncated inside an acknowledged or pending range")
            digest.update(chunk)
            offset += len(chunk)
            if offset == end:
                approved_hash = digest.hexdigest()
        after = os.fstat(handle.fileno())
    if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
        after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns,
    ):
        raise ReconciliationRequired("source changed while checking accepted transcript coverage")
    if approved_hash == expected_hash and digest.hexdigest() == stream.get("prefix_sha256"):
        return stream
    return None


def _record_finalized_coverage(record: SessionRecord, stream: dict) -> None:
    record.byte_end = stream["source_byte_end"]
    record.line_no = stream["source_line_end"]
    record.last_seq = stream["last_seq"]
    record.finalized = True


def upload_session(
    transcript: Transcript,
    record: SessionRecord,
    poster: Poster,
    *,
    device_id: str,
    budget_bytes: int | None = None,
    sleep: Callable[[float], None] = time.sleep,
    journal: Journal | None = None,
    wire: Wire | None = None,
    coverage_source: Transcript | None = None,
    approved: dict | None = None,
) -> UploadResult:
    """Upload a frozen prefix through the shared pre-send durable journal.

    Legacy offsets never authorize replay. Remote coverage and the local source
    prefix must match before a reservation is made. ``coverage_source`` retains
    the original source for receipt proofs while ``transcript`` remains the
    shorter approved copy used for any actual upload.
    """
    result = UploadResult(session_id=transcript.session_id)
    own_journal = journal is None
    stage = "source validation"
    try:
        provenance = validate_identity(transcript.path, transcript.agent, transcript.session_id)
        requested_size = approved["size"] if approved is not None else transcript.path.stat().st_size
        requested_approval = approved if approved is not None else {
            "size": requested_size, "sha256": prefix_hash(transcript.path, requested_size),
        }
        wire = wire or Wire(
            poster.base_url, poster.token, transcript.agent, poster.timeout,
            context=ssl_context(),
        )
        stage = "receipt check"
        remote = wire.receipts(transcript.session_id)
        # Checks the answer's team, source and session before anything trusts it.
        covered = _finalized_coverage(
            coverage_source or transcript, remote, approved=requested_approval,
            expected_customer_id=journal.customer_id if journal is not None else None,
        )
        if remote.get("state") == DELETED_STATE:
            if journal is not None:
                journal.mark_deleted(transcript.session_id, transcript.path)
            result.ok = result.deleted = True
            return result
        if covered is not None:
            _record_finalized_coverage(record, covered)
            result.ok = True
            result.already_finalized = True
            return result
        stage = "snapshot"
        journal = journal or Journal(wire.base_url, remote["customer_id"], transcript.agent)
        journal.ensure(
            transcript.session_id,
            transcript.path,
            remote,
            historical=True,
            provenance=provenance,
            cwd=transcript.cwd,
        )
        rechecked = False
        expected_history = None
        while True:
            stage = "reading transcript"
            body = journal.stage(
                transcript.session_id, cwd=transcript.cwd or "", historical_only=True,
                require_no_pending=expected_history is not None, expected_history=expected_history,
            )
            if body is None:
                result.ok = True
                break
            if budget_bytes is not None and result.bytes_sent + len(body) > budget_bytes:
                result.ok, result.error = True, "budget"
                break
            stage = "finalization" if json.loads(body).get("finalize") else "upload"
            try:
                journal.deliver(transcript.session_id, wire, expected_body=body)
            except ReconciliationRequired as exc:
                if exc.status_code != 409 or rechecked:
                    raise
                rechecked = True
                # A compatible writer may have finalized after our receipt read.
                # Proof of the whole approved prefix needs no journal mutation.
                try:
                    remote = wire.receipts(transcript.session_id)
                    covered = _finalized_coverage(
                        coverage_source or transcript, remote, approved=requested_approval,
                        expected_customer_id=journal.customer_id,
                    )
                    if remote.get("state") == DELETED_STATE:
                        raise SessionDeleted(transcript.session_id)
                except SessionDeleted:
                    journal.mark_deleted(transcript.session_id, transcript.path)
                    raise
                except DeliveryPending as refresh_error:
                    if refresh_error.retryable:
                        stage = "receipt recheck"
                        raise
                    raise exc
                except (ReconciliationRequired, OSError, sqlite3.Error):
                    raise exc
                if covered is not None:
                    _record_finalized_coverage(record, covered)
                    result.ok = True
                    result.already_finalized = True
                    return result
                if stage != "finalization":
                    raise
                # A shorter accepted completion can unblock new approved data,
                # but only if the same no-data reservation is still pending.
                # Adoption and the replacement snapshot commit atomically.
                requested_history = (requested_approval["size"], requested_approval["sha256"])
                try:
                    journal.ensure(
                        transcript.session_id, transcript.path, remote, historical=True,
                        provenance=provenance, cwd=transcript.cwd, reconcile_body=body,
                        expected_history=requested_history,
                    )
                except (DeliveryPending, ReconciliationRequired, OSError, sqlite3.Error):
                    raise exc
                expected_history = requested_history
                continue
            result.batches += 1
            result.bytes_sent += len(body)
        state = journal.get(transcript.session_id)
        record.byte_end = state["source_byte_end"]
        record.line_no = state["source_line_end"]
        record.last_seq = state["last_seq"]
        record.finalized = bool(state.get("historical_complete"))
    except SessionDeleted:
        # Final. The journal (shared with the tap) has dropped anything pending
        # for it, so no capture path sends it again either.
        result.ok = result.deleted = True
        result.error = None
    except (DeliveryPending, ReconciliationRequired, OSError, sqlite3.Error) as exc:
        result.error = f"{stage}: {_failure_message(exc)}"
        result.retryable = isinstance(exc, DeliveryPending) and exc.retryable
    finally:
        if own_journal and journal is not None:
            journal.close()
    return result


# --- project mapping ---------------------------------------------------------


def _human_bytes(count: int) -> str:
    size = float(count)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}GB"


def _date_range(census: Census) -> str:
    if not census.candidates:
        return ""
    stamps = sorted(t.mtime for t in census.candidates)
    first = time.strftime("%Y-%m-%d", time.localtime(stamps[0]))
    last = time.strftime("%Y-%m-%d", time.localtime(stamps[-1]))
    return first if first == last else f"{first} to {last}"


def gate_lines(
    census: Census, assignments: dict[str, str], *, sources: Iterable[str] | None = None,
) -> list[str]:
    """What the reviewer sees before any session leaves the machine.

    THE CONSENT SURFACE. There is no server-side redaction gate any more (it was
    removed in 0.104.9.0 for quarantining whole sessions on false positives), so
    what this screen says is the only thing standing between a person and a
    surprise. It therefore names the true scope -- the whole machine, not the
    folder -- the byte total, the date range, and how many sessions are skipped
    and why.

    It no longer says anything about summaries: the digest lane was retired
    server-side, so this run writes none and promising them here would describe
    work that cannot happen.
    """
    from . import setup

    selected = tuple(sources) if sources is not None else tuple(
        dict.fromkeys(transcript.agent for transcript in census.candidates)
    )
    label = setup.agent_label(selected) if selected else "coding-agent"
    lines = [
        "Agent sessions on this machine",
        "",
        f"  {census.sessions} sessions · {_human_bytes(census.bytes)}"
        + (f" · {_date_range(census)}" if census.candidates else ""),
        "",
        f"  Your local {label} logs from the whole machine.",
        "  They are sanitized here before upload:",
        "  tool output, file contents and API metadata never leave.",
        "",
        "  Each imports on its own, with no project or experiment attached.",
    ]
    skipped = []
    if census.captured_live:
        skipped.append(f"{census.captured_live} already captured live")
    if census.already_in_probe:
        skipped.append(f"{census.already_in_probe} already in Probe")
    if census.sidechains:
        skipped.append(f"{census.sidechains} subagent sidechains")
    if skipped:
        lines += ["", "  Skipped: " + ", ".join(skipped)]
    if census.unreadable:
        lines += [f"  {census.unreadable} could not be read"]
    if census.identity_unverified or census.identity_conflicts:
        lines += [
            f"  {census.identity_unverified} identities unverified · "
            f"{census.identity_conflicts} conflicting copies need reconciliation"
        ]
    if census.known_no_transcript:
        # Not a failure and not uploadable -- there is no file. Shown because
        # the alternative is a total that reads as the whole population.
        lines += [
            f"  {census.known_no_transcript} more recent session(s) have no transcript "
            "on disk — nothing to import for those"
        ]
    return lines


# --- the lane ----------------------------------------------------------------


@dataclass
class LaneOutcome:
    """What the import did, in the terms the reconcile block prints."""

    found: int = 0
    uploaded: int = 0
    finalized: int = 0
    anchored: int = 0
    failed: int = 0
    deferred: int = 0
    skipped_live: int = 0
    skipped_in_probe: int = 0
    #: Sessions the server holds from a capture that predates protocol 2. See
    #: `import_transcripts` for why these are a skip and not a failure.
    skipped_legacy: int = 0
    #: Sessions the server deleted at their team's request. Never uploaded,
    #: never a failure: the engine refuses them for good.
    skipped_deleted: int = 0
    bytes_sent: int = 0
    pending_batches: int = 0
    pending_bytes: int = 0
    #: Delivery failures that can retry the same approval when connectivity returns.
    retryable_failures: int = 0
    errors: list[str] = field(default_factory=list)

    def lines(self) -> list[str]:
        """The deterministic half of the report: what landed, against what was
        counted. Every non-zero bucket prints, including the failures -- a
        session that fell over must never quietly leave the denominator."""
        out = [
            f"{self.found} sessions found · {self.uploaded} uploaded · "
            f"{self.finalized} finalized"
        ]
        if self.skipped_live or self.skipped_in_probe:
            out.append(
                f"{self.skipped_live} already captured live · "
                f"{self.skipped_in_probe} already in Probe"
            )
        if self.skipped_legacy:
            # Named separately from `skipped_in_probe`, and never folded into
            # it: those were proved absent from this import's work, these are
            # present with coverage nobody can verify. A reader deciding whether
            # their history is complete needs to be able to tell them apart.
            out.append(
                f"{self.skipped_legacy} already in Probe from an earlier capture "
                "(coverage not verifiable, nothing re-sent)"
            )
        if self.skipped_deleted:
            out.append(
                f"{self.skipped_deleted} deleted at your team's request (not uploaded)"
            )
        if self.deferred:
            out.append(
                f"{self.deferred} deferred (byte budget) — re-run to continue where this stopped"
            )
        if self.pending_batches:
            out.append(
                f"{self.pending_batches} pending batches ({_human_bytes(self.pending_bytes)}) retained for retry"
            )
        if self.failed:
            out.append(f"{self.failed} failed:")
            out.extend(f"  {message}" for message in self.errors[:5])
            if len(self.errors) > 5:
                out.append(f"  … and {len(self.errors) - 5} more")
        return out


def import_transcripts(
    census: Census,
    *,
    poster: Poster | dict[str, Poster],
    device_id: str | dict[str, str],
    ledger: TranscriptLedger,
    assignments: dict[str, str] | None = None,
    budget_bytes: int | None = None,
    scratch: Path | None = None,
    on_progress: Callable[[int, int, Transcript], None] | None = None,
    on_stage: Callable[[int, int, Transcript, str], None] | None = None,
    on_completion: Callable[[int, int, list[tuple[str, str]]], None] | None = None,
    approved_files: dict[str, dict] | None = None,
    expected_customer_id: str | None = None,
    stop_on_retryable: bool = False,
) -> LaneOutcome:
    """Standalone upload and finalization stages with independent retry.

    Two stages, not three: the local digest pass that ran after finalization
    was removed with the server-side digest lane, and with it the `client` this
    function only ever needed to POST a digest with. `scratch` is where a
    background import snapshots each reviewed prefix before uploading it; it is
    required with `approved_files` and unused otherwise.

    `assignments` is ignored for compatibility. Legacy pending anchor intent
    never creates entity links. The old ledger is read neither as coverage nor
    as a session completion claim; the v2 journal and receipts own those facts.
    ``on_completion`` counts only verified finalizations, including previously
    finalized receipts. ``on_stage`` retains its processed-session semantics.
    """
    outcome = LaneOutcome(
        found=census.sessions,
        skipped_live=census.captured_live,
        skipped_in_probe=census.already_in_probe,
    )
    posters = poster if isinstance(poster, dict) else dict.fromkeys(INGEST_PATH, poster)
    remaining = budget_bytes
    #: Sessions this lane has ACCOUNTED FOR -- finalized here, or found already
    #: held by the server. Both belong in the progress denominator: a bar that
    #: can never reach its total on a machine with pre-protocol-2 history reads
    #: as an import that never finished, which is the opposite of the truth.
    #: The report lines below keep the two apart in words.
    accounted_ids: set[tuple[str, str]] = set()
    if on_completion:
        on_completion(0, census.sessions, [])
    for index, transcript in enumerate(census.candidates):
        if on_progress:
            on_progress(index + 1, census.sessions, transcript)
        if on_stage:
            on_stage(index, census.sessions, transcript, "Checking upload status")
        agent_poster = posters.get(transcript.agent)
        if agent_poster is None:
            outcome.failed += 1
            error = f"{transcript.agent}/{transcript.session_id}: no paired device"
            outcome.errors.append(error)
            if on_stage:
                on_stage(index + 1, census.sessions, transcript, f"Session failed — {error}")
            continue
        journal = None
        #: The team a `deleted` receipts answer named (identity-checked).
        deleted_customer: str | None = None
        processed = True
        already_finalized = False
        failure = None
        #: Replaces the finally block's "Session processed" when a session was
        #: counted without being uploaded. One `on_stage` per session is the
        #: contract the progress estimator and the job record both assume.
        note = None
        stage = "reviewed snapshot"
        approved_snapshot = contextlib.ExitStack()
        try:
            approved = None
            if approved_files is not None:
                approved = approved_files.get(f"{transcript.agent}:{transcript.session_id}")
                if approved is None or scratch is None:
                    raise ReconciliationRequired("transcript was not in the approved inventory")
            wire = Wire(
                agent_poster.base_url, agent_poster.token, transcript.agent, agent_poster.timeout,
                context=ssl_context(),
            )
            stage = "receipt check"
            remote = wire.receipts(transcript.session_id)
            covered = _finalized_coverage(
                transcript, remote, approved=approved, expected_customer_id=expected_customer_id,
            )
            if remote.get("state") == DELETED_STATE:
                deleted_customer = remote["customer_id"]
                raise SessionDeleted(transcript.session_id)
            if covered is None and remote.get("state") == "legacy":
                # ALREADY THERE, and unreachable by this lane forever.
                #
                # `legacy` means the server holds this session from a
                # capture that predates protocol 2, so it can name no byte
                # cursor for it. `_finalized_coverage` therefore cannot prove
                # the prefix, and `Journal.ensure` refuses to replay onto an
                # unverified stream -- correctly: a blind replay overwrites
                # stored blobs, because the engine keys on "<session>:<seq>"
                # and takes the last write.
                #
                # Counting that refusal as a FAILURE was the bug. It is not
                # retryable, no `probe` command reconciles it, and the content
                # is not missing -- it is the pre-09-08 half of every machine's
                # history, which the census cannot recognise offline because the
                # local tap cursor only goes back as far as protocol 2. One
                # import reported 166 of these as failures and, because a single
                # non-retryable failure downgrades the whole lane, told its owner
                # to go fix something that was already done.
                outcome.skipped_legacy += 1
                note = "Already in Probe from an earlier capture"
                accounted_ids.add((transcript.agent, transcript.session_id))
                if on_completion:
                    on_completion(len(accounted_ids), census.sessions, sorted(accounted_ids))
                continue
            record = SessionRecord(
                session_id=transcript.session_id, path=str(transcript.path), agent=transcript.agent
            )
            if on_stage:
                on_stage(
                    index, census.sessions, transcript,
                    "Verifying completed session" if covered is not None else "Uploading session",
                )
            stage = "delivery"
            if covered is not None:
                _record_finalized_coverage(record, covered)
                result = UploadResult(session_id=transcript.session_id, ok=True, already_finalized=True)
            else:
                coverage_source = transcript
                if approved is not None:
                    stage = "reviewed snapshot"
                    transcript = approved_snapshot.enter_context(
                        _approved_transcript(transcript, approved, scratch)
                    )
                journal = Journal(wire.base_url, remote["customer_id"], transcript.agent)
                stage = "delivery"
                result = upload_session(
                    transcript,
                    record,
                    agent_poster,
                    device_id="",
                    journal=journal,
                    wire=wire,
                    budget_bytes=remaining,
                    coverage_source=coverage_source,
                    approved=approved,
                )
            if result.deleted:
                raise SessionDeleted(transcript.session_id)
            already_finalized = result.already_finalized
            outcome.bytes_sent += result.bytes_sent
            if remaining is not None:
                remaining = max(0, remaining - result.bytes_sent)
            if not result.ok:
                raise DeliveryPending(result.error or "upload pending", retryable=result.retryable)
            if result.error == "budget":
                outcome.deferred += len(census.candidates) - index
                processed = False
                break
            outcome.uploaded += 1
            if not record.finalized:
                raise DeliveryPending("finalization pending; transcript retained for retry")
            outcome.finalized += 1
            accounted_ids.add((transcript.agent, transcript.session_id))
            if on_completion:
                on_completion(len(accounted_ids), census.sessions, sorted(accounted_ids))
        except SessionDeleted:
            # Deleted at the team's request (receipts `state: "deleted"` or a
            # 410): a skip, like `skipped_legacy`, never a failure to fix.
            # Recorded in the journal the tap reads (idempotent), so capture
            # drops what it holds for the session too and never stages it again.
            customer = deleted_customer or expected_customer_id
            try:
                if journal is None and customer is not None:
                    journal = Journal(wire.base_url, customer, transcript.agent)
                if journal is not None:
                    journal.mark_deleted(transcript.session_id, transcript.path)
            except (OSError, sqlite3.Error):
                pass  # still a skip: the tap records it on its own next receipts read
            outcome.skipped_deleted += 1
            note = "Deleted at your team's request; not uploaded"
            accounted_ids.add((transcript.agent, transcript.session_id))
            if on_completion:
                on_completion(len(accounted_ids), census.sessions, sorted(accounted_ids))
        except (DeliveryPending, ReconciliationRequired, OSError, sqlite3.Error) as exc:
            outcome.failed += 1
            if isinstance(exc, DeliveryPending) and exc.retryable:
                outcome.retryable_failures += 1
            failure = f"{transcript.agent}/{transcript.session_id} — {stage}: {_failure_message(exc)}"
            outcome.errors.append(failure)
            if stop_on_retryable and isinstance(exc, DeliveryPending) and exc.retryable:
                break
        finally:
            cleanup_failure = None
            if journal is not None:
                try:
                    if not already_finalized:
                        pending = journal.pending(transcript.session_id)
                        if pending:
                            outcome.pending_batches += 1
                            outcome.pending_bytes += len(pending)
                        journal.release_snapshot(transcript.session_id)
                except (OSError, sqlite3.Error) as exc:
                    cleanup_failure = _failure_message(exc)
                finally:
                    try:
                        journal.close()
                    except (OSError, sqlite3.Error) as exc:
                        cleanup_failure = cleanup_failure or _failure_message(exc)
            try:
                approved_snapshot.close()
            except OSError as exc:
                cleanup_failure = cleanup_failure or _failure_message(exc)
            if cleanup_failure and failure is None:
                outcome.failed += 1
                failure = f"{transcript.agent}/{transcript.session_id} — cleanup: {cleanup_failure}"
                outcome.errors.append(failure)
            if on_stage:
                on_stage(
                    index + int(processed), census.sessions, transcript,
                    f"Session failed — {failure}" if failure else (
                        note or ("Session processed" if processed else "Byte budget reached")
                    ),
                )
    return outcome


# --- the CLI entry point -----------------------------------------------------


def saved_session_sources(
    sources: Iterable[str], *, plugin_dirs: dict[str, Path]
) -> tuple[str, ...]:
    """Sources with saved session files, independent of installed CLIs or pairing.

    Use the same roots and filename rules as discovery. An empty directory,
    prompt history without transcripts, or only subagent sidechains is not a
    saved history to offer. The full identity check and census run only after
    the source selection; deselected histories are excluded from that import.
    """
    return tuple(
        source for source in sources
        if any(
            session_id_for(path, source) is not None and path.is_file()
            for root in transcript_roots(source, plugin_dirs.get(source))
            for path in _walk(root, source)
        )
    )


def choose_sources(available: tuple[str, ...], *, selected: tuple[str, ...] | None = None):
    """Choose saved histories; every detected source starts selected."""
    import questionary

    from . import setup, tui

    title = "Import past coding sessions"
    body = tui.wrap("Saved sessions were found for these agents.")
    prompt = "Which ones should be imported?"
    message = tui.framed(title, body, prompt)
    instruction = "enter or space toggle · ↑↓ choose · → next · ctrl+s skip · esc back"
    tui.use_checkmarks()
    checked = set(available if selected is None else selected)
    rows = {
        source: questionary.Choice(
            title=setup._menu_row(
                setup.AGENT_LABELS[source], (), checked=source in checked, indent=tui.body_indent()
            ),
            value=source,
            checked=source in checked,
        )
        for source in available
    }
    # Each border needs its own separator. Roomier screens also keep a blank
    # line outside the border; the shared layout drops that extra air to fit.
    first_border = questionary.Separator(" ")
    choices: list = [questionary.Separator(" "), first_border]
    compact_choices: list = [first_border]
    for row in rows.values():
        if len(compact_choices) > 1:
            border = questionary.Separator(" ")
            choices.extend([questionary.Separator(" "), border])
            compact_choices.append(border)
        choices.append(row)
        compact_choices.append(row)
    footer = setup.nav_footer(skip_title="Skip sessions")
    choices.extend([questionary.Separator(" "), *footer])
    compact_choices.extend(footer)

    def make_question(options, hint):
        return questionary.checkbox(
            message, choices=options, instruction=hint, style=tui.style(),
            qmark=tui.qmark(), pointer=tui.pointer(),
            validate=lambda answer: any(value in rows for value in answer)
            or "Choose at least one coding-agent history.",
        )

    question = make_question(choices, instruction)
    own_boxes = tui.draw_own_boxes(question)

    def redraw(control):
        for source, row in rows.items():
            row.title = setup._menu_row(
                setup.AGENT_LABELS[source], (),
                checked=source in control.selected_options, indent=tui.body_indent(),
            )
        control.error_message = (
            None if any(value in rows for value in control.selected_options)
            else "Choose a history, or Skip sessions."
        )

    control = setup._wire_picker(
        question, redraw=redraw,
        can_submit=lambda control: any(value in rows for value in control.selected_options),
        on_leave=lambda control: [value for value in control.selected_options if value in rows],
    )
    if control is None:
        choices = setup.without_nav(choices)
        compact_choices = None
        for source, row in rows.items():
            row.title = setup.AGENT_LABELS[source]
        instruction = "space toggle · ↑↓ choose · enter continue · esc back"
        question = make_question(choices, instruction)
    elif not own_boxes:
        for source, row in rows.items():
            row.title = setup.AGENT_LABELS[source]
    tui.point_at(control, lambda value: value == setup.NAV_BAND)
    setup.dress_band(question, control)
    @question.application.key_bindings.add("c-s", eager=True)
    def skip(event):
        event.app.exit(result=tui.SKIP)

    tui.sectioned(
        question, title=title, lines=body, prompt=prompt, instruction=instruction,
        compact_choices=compact_choices,
    )
    picked = tui.ask(question, height=tui.content_height(message, choices))
    if picked is None or picked is tui.BACK or picked is tui.SKIP:
        return picked
    return tuple(source for source in available if source in picked) or tui.BACK


@contextlib.contextmanager
def _import_progress(total: int, *, enabled: bool):
    """Keep session counts and the active phase visible during long agent calls."""
    from . import setup, tui

    if not enabled or not tui.interactive():
        yield None
        return
    import threading

    board = tui.Board("Importing past coding sessions", ["", "", "", ""])
    board.open()
    stop = threading.Event()
    lock = threading.Lock()
    state = {"completed": 0, "phase": "Preparing import", "session": "", "started": time.monotonic()}

    def paint():
        with lock:
            completed = state["completed"]
            phase = state["phase"]
            session = state["session"]
            elapsed = int(time.monotonic() - state["started"])
        board.update(0, f"{tui.progress_bar(completed / max(1, total))}  {completed}/{total} processed")
        board.update(1, f"{phase} · {elapsed}s")
        board.update(2, session)
        board.update(3, "ctrl+c stop · re-run to resume")

    def update(completed: int, _total: int, transcript: Transcript, phase: str):
        with lock:
            state.update(
                completed=completed, phase=phase,
                session=f"{setup.AGENT_LABELS[transcript.agent]} · {transcript.session_id}",
                started=time.monotonic(),
            )
        paint()

    def heartbeat():
        while not stop.wait(1):
            paint()

    thread = threading.Thread(target=heartbeat, daemon=True)
    paint()
    thread.start()
    try:
        yield update
    finally:
        stop.set()
        thread.join(timeout=0.5)
        board.close()


def run_lane(**kwargs):
    """Run the past-sessions lane and report its verdict exactly once.

    The lane RETURNS EARLY from seven places, and every one of them renders as
    a short message the wizard prints and moves on from. That made the whole
    half of the import offer invisible: a machine where session capture was
    never paired and a person who read the review and said no are the same
    silence from the outside.

    The outcome is set explicitly at each of those returns rather than inferred
    from the prose, and the emit lives here so a new early return that forgets
    to name itself still reports SOMETHING rather than nothing.
    """
    import time as _time

    from . import telemetry as tm

    tel = tm.current()
    summary: dict = {}
    started = _time.monotonic()

    def report(outcome):
        try:
            tel.emit(
                tm.EVENT_TRANSCRIPTS_SUMMARY,
                outcome=str(outcome),
                duration_seconds=round(_time.monotonic() - started, 3),
                background=bool(kwargs.get("background")),
                interactive=bool(kwargs.get("interactive", True)),
                **{key: value for key, value in summary.items() if key != "outcome"},
            )
        except Exception:
            pass  # observability must never become observable

    try:
        result = _run_lane(summary=summary, **kwargs)
    except KeyboardInterrupt:
        report(tm.TranscriptsOutcome.ABORTED)
        raise
    except BaseException:
        report(tm.TranscriptsOutcome.ERROR)
        raise
    report(summary.get("outcome") or tm.TranscriptsOutcome.COMPLETED)
    return result


def _run_lane(
    *,
    summary: dict,
    client,
    assignments: dict[str, str] | None = None,
    include_codex: bool = True,
    include_pi: bool = True,
    interactive: bool = True,
    yes: bool = False,
    budget_bytes: int | None = None,
    sources: Iterable[str] | None = None,
    background: bool = False,
    back_to_selection: bool = False,
):
    """Discover, gate, and import this machine's transcripts. Returns report lines.

    With ``back_to_selection``, review Back reopens the source selection and
    the source selection returns ``tui.BACK``; Skip advances with a report.

    Returns EARLY, with an explanation, for every reason the lane cannot run --
    no capture credential, no sessions, a declined gate. None of them is an
    error: a machine with capture never paired simply has no way to upload, and
    saying so beats a stack trace.

    Uploads go through the capture credential's own Wire; `client` is for the
    per-session server check and for pinning the account a background import
    runs under. The local digest stage that also used it went with the
    server-side digest lane, and no scratch dir is taken any more.
    """
    from . import capabilities, setup, tui

    wanted = list(dict.fromkeys(sources)) if sources is not None else [
        CLAUDE, *([CODEX] if include_codex else []), *([PI] if include_pi else [])
    ]
    unknown = [source for source in wanted if source not in INGEST_PATH]
    if unknown:
        raise ValueError(f"Unknown coding-agent history source: {', '.join(unknown)}")
    if not wanted:
        summary["outcome"] = "no_sources"
        return ["No coding-agent histories selected; nothing was uploaded."]
    plugin_dirs = {source: capabilities.tap_plugin_dir(source) for source in wanted}
    if interactive and not yes:
        with tui.working("Looking for saved coding-agent sessions"):
            available = saved_session_sources(wanted, plugin_dirs=plugin_dirs)
        if not available:
            summary["outcome"] = "no_saved_sessions"
            return ["No saved coding-agent sessions were found on this machine."]
    previous_selection = None
    prepared = {}
    while True:
        if interactive and not yes:
            selected = (choose_sources(available, selected=previous_selection)
                        if previous_selection is not None else choose_sources(available))
            if selected is None:
                raise KeyboardInterrupt
            if selected is tui.BACK and back_to_selection:
                summary["outcome"] = "back"
                return tui.BACK
            if selected is tui.BACK or selected is tui.SKIP:
                summary["outcome"] = "skipped"
                summary["declined_at"] = "sources"
                return ["Skipped the agent sessions."]
            wanted = list(selected)
            previous_selection = tuple(selected)

        key = tuple(wanted)
        if key in prepared:
            posters, devices, unpaired, agents, census, ledger, assignments, approved_payload = prepared[key]
        else:
            # ONE CREDENTIAL PER AGENT, resolved BEFORE the walk. A device token is
            # bound to its source, so an agent with no pairing has no way to upload at
            # all -- and discovering its sessions only to fail every one of them would
            # report a fleet of errors for a machine that is simply not set up for it.
            posters: dict[str, Poster] = {}
            devices: dict[str, str] = {}
            unpaired: list[str] = []
            for source in wanted:
                resolved = capabilities.resolved_capture_credential(source)
                if resolved is None:
                    unpaired.append(source)
                    continue
                token, base_url = resolved
                posters[source] = Poster(base_url=base_url, token=token)
                devices[source] = capabilities.capture_device_id(source) or ""

            agents = [source for source in wanted if source in posters]
            if not agents:
                summary["outcome"] = "not_paired"
                summary["unpaired"] = len(unpaired)
                from probe.sdk.session_marker import WIZARD_HINT

                return [
                    "Session capture is not paired on this machine, so there is no "
                    "credential to upload sessions with.",
                    f"Pair it with the wizard's Install, then re-run ({WIZARD_HINT}).",
                ]

            with tui.working("Counting the selected coding-agent sessions"):
                census = discover(
                    agents=agents,
                    tracked=set(),
                    plugin_dirs={source: plugin_dirs[source] for source in agents},
                )
            if not census.candidates:
                # NAME THE DIRECTORIES. "None found" on a machine whose config dir was
                # relocated is a confident zero and indistinguishable from a machine
                # that genuinely has none -- which is the whole failure this census
                # exists to prevent.
                looked = ", ".join(str(root) for root in census.roots) or "no readable directory"
                found = (
                    f" {census.known_no_transcript} recent session(s) have no transcript on disk."
                    if census.known_no_transcript
                    else ""
                )
                summary["outcome"] = "no_candidates"
                summary["agents"] = len(agents)
                summary["identity_unverified"] = census.identity_unverified
                summary["identity_conflicts"] = census.identity_conflicts
                summary["known_no_transcript"] = census.known_no_transcript
                return [
                    "No verified agent sessions are available to import.",
                    f"Looked in: {looked}.{found}",
                    f"{census.identity_unverified} identities unverified; {census.identity_conflicts} conflicting copies.",
                ]

            ledger = TranscriptLedger.for_device()
            assignments = {}  # Historical transcripts are always standalone.
            approved_payload = None
            if background and interactive:
                with tui.working("Preparing selected sessions for background import"):
                    approved_payload = _background_payload(
                        census, client=client, posters=posters, devices=devices,
                        budget_bytes=budget_bytes, unpaired=unpaired,
                    )
            prepared[key] = (posters, devices, unpaired, agents, census, ledger, assignments, approved_payload)
        if interactive and not yes:
            lines = gate_lines(census, assignments, sources=agents)
            if unpaired:
                from probe.sdk.session_marker import WIZARD_HINT

                lines += [
                    "",
                    f"  {setup.agent_label(unpaired)} histories cannot be imported yet:",
                    f"  session capture is not paired. Pair it with the wizard's Install ({WIZARD_HINT}).",
                ]
            answer = tui.review(
                lines[0], lines[2:],
                [("Import these sessions", "import"), ("Skip agent sessions", "skip")],
            )
            if answer is None:
                raise KeyboardInterrupt
            if answer is tui.BACK and back_to_selection:
                continue
            if answer != "import":
                summary["outcome"] = "skipped"
                summary["declined_at"] = "review"
                summary["sessions"] = census.sessions
                summary["agents"] = len(agents)
                return ["Skipped the agent sessions."]

        break

    summary["sessions"] = census.sessions
    summary["candidates"] = len(census.candidates)
    summary["agents"] = len(agents)
    summary["unpaired"] = len(unpaired)
    if approved_payload is not None:
        from . import import_jobs, import_jobs_ui
        from .import_job_messages import enqueue_report

        job = import_jobs.enqueue(
            "transcripts", approved_payload,
            f"{census.sessions} sessions from {setup.agent_label(agents)}",
        )
        # Handed off, NOT finished. Whether it lands is `import_job.finished`,
        # which the detached worker emits under this same session id.
        summary["outcome"] = "enqueued"
        summary["job_state"] = str(job.get("state") or "")
        if not yes:
            job = import_jobs_ui.show_started_import(job)
        return enqueue_report(job, "Session import")

    summary["outcome"] = "completed"
    return _execute_census(
        census, client=client, posters=posters, devices=devices,
        ledger=ledger, interactive=interactive,
        budget_bytes=budget_bytes, unpaired=unpaired,
    )


def _background_identity(client) -> dict:
    """Nonsecret account identity pinned before the transcript review."""
    from urllib.parse import urlsplit, urlunsplit

    from ..sdk.config import current_context_name

    identity = client.me()
    url = urlsplit(client.settings.base_url)
    if (
        not identity.get("customer_id") or not identity.get("user_id")
        or not url.hostname or url.username or url.password
    ):
        raise ReconciliationRequired("Cannot verify the account for this background import.")
    return {
        "context": current_context_name(),
        "base_url": urlunsplit((url.scheme, url.netloc, url.path.rstrip("/"), "", "")),
        "customer_id": str(identity["customer_id"]),
        "user_id": str(identity["user_id"]),
        # Historical sessions are standalone: no workspace or project
        # anchor is created, so changing the current folder workspace cannot
        # change this job's destination.
    }


def _background_payload(
    census: Census, *, client, posters, devices, budget_bytes, unpaired,
) -> dict:
    identity = _background_identity(client)
    files = []
    for transcript in census.candidates:
        row = asdict(transcript)
        row["path"] = str(transcript.path.resolve())
        row["sha256"] = prefix_hash(transcript.path, transcript.size)
        files.append(row)
    return {
        "schema": 1,
        "account": identity,
        "files": files,
        "sources": {
            source: {"base_url": poster.base_url.rstrip("/"), "device_id": devices[source]}
            for source, poster in posters.items()
        },
        "budget_bytes": budget_bytes,
        "unpaired": list(unpaired),
    }


@contextlib.contextmanager
def _approved_transcript(transcript: Transcript, approved: dict, scratch: Path):
    """Import only the reviewed prefix, even when a producer appends afterwards.

    The worker keeps at most one temporary source copy. The existing session
    journal owns its durable upload snapshot and receipts. A copy left by an
    interrupted worker is verified and reused; changed source bytes require a
    fresh review rather than silently extending the approved history.
    """
    import tempfile

    directory = scratch / "approved"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = directory / f"{transcript.agent}-{transcript.session_id}.jsonl"
    size = int(approved["size"])
    if not target.exists() or target.stat().st_size != size or prefix_hash(target, size) != approved["sha256"]:
        fd, temporary = tempfile.mkstemp(dir=directory)
        temporary = Path(temporary)
        digest = hashlib.sha256()
        try:
            with os.fdopen(fd, "wb") as output, transcript.path.open("rb") as source:
                remaining = size
                while remaining:
                    chunk = source.read(min(1024 * 1024, remaining))
                    if not chunk:
                        raise ReconciliationRequired("A reviewed session was truncated; review it again.")
                    output.write(chunk)
                    digest.update(chunk)
                    remaining -= len(chunk)
                output.flush()
                os.fsync(output.fileno())
            if digest.hexdigest() != approved["sha256"]:
                raise ReconciliationRequired("A reviewed session changed; review it again.")
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    try:
        yield replace(transcript, path=target, size=size)
    finally:
        target.unlink(missing_ok=True)


def run_background_job(payload: dict, *, progress) -> list[str]:
    """Resume an approved file list without discovering any additional history."""
    from . import import_jobs

    try:
        return _run_background_job(payload, progress=progress)
    except import_jobs.JobError:
        raise
    except Exception as exc:
        if import_jobs.is_retryable_error(exc):
            raise import_jobs.RetryableJobError(
                "Session import is waiting for the connection to return."
            ) from exc
        raise


def _run_background_job(payload: dict, *, progress) -> list[str]:
    from ..sdk.client import Client
    from ..sdk.config import current_context_name, resolve
    from . import capabilities, import_jobs

    if payload.get("schema") != 1:
        raise import_jobs.JobError("This session import needs a new review.")
    account = payload["account"]
    if current_context_name() != account["context"]:
        raise import_jobs.JobError("Switch back to the saved account before resuming this import.")
    with Client(
        settings=resolve(context=account["context"]),
        async_writes=False, auto_drain=False, attribution="backfill",
    ) as client:
        if _background_identity(client) != account:
            raise import_jobs.JobError("The saved import account changed; nothing was uploaded.")
        posters = {}
        devices = {}
        for source, approved in payload["sources"].items():
            resolved = capabilities.resolved_capture_credential(source)
            device = capabilities.capture_device_id(source) or ""
            if (
                resolved is None or resolved[1].rstrip("/") != approved["base_url"]
                or device != approved["device_id"]
            ):
                raise import_jobs.JobError("A selected capture pairing changed; restore it before resuming.")
            posters[source] = Poster(base_url=resolved[1], token=resolved[0])
            devices[source] = device
        census = Census(candidates=[
            Transcript(
                path=Path(row["path"]), session_id=row["session_id"], agent=row["agent"],
                cwd=row["cwd"], size=row["size"], mtime=row["mtime"],
            )
            for row in payload["files"]
        ])
        approved_files = {
            f"{row['agent']}:{row['session_id']}": row for row in payload["files"]
        }
        if any(transcript.agent not in posters for transcript in census.candidates):
            raise import_jobs.JobError("A session is outside the approved source selection.")
        # A payload saved by an older CLI may still carry `agent` and
        # `digest_note`; both belonged to the local summary stage and are
        # ignored. The sessions it reviewed upload the same way.
        ledger = TranscriptLedger.for_device()
        fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:24]
        scratch = ledger.path.parent / "background-transcript-imports" / fingerprint
        progress(
            "Importing approved sessions", completed=0, total=census.sessions,
            completion_completed=0, completion_total=census.sessions, completion_ids=[],
        )
        return _execute_census(
            census, client=client, posters=posters, devices=devices,
            ledger=ledger, work_dir=scratch, budget_bytes=payload.get("budget_bytes"),
            unpaired=payload.get("unpaired", []),
            approved_files=approved_files, expected_customer_id=account["customer_id"],
            progress=progress,
        )


def _execute_census(
    census: Census, *, client, posters, devices, ledger,
    interactive: bool = False, work_dir: Path | None = None,
    budget_bytes: int | None = None,
    unpaired: Iterable[str] = (), approved_files: dict[str, dict] | None = None,
    expected_customer_id: str | None = None, progress=None,
) -> list[str]:
    """Upload one census. `work_dir` is only needed by a background import,
    which snapshots each reviewed prefix there before uploading it; the
    interactive lane writes nothing to disk but its ledger."""
    from . import tui

    if census.candidates:
        # ONE server read before anything uploads. The answer itself is no
        # longer used (it carried the digest prompt version); the call stays
        # because a server that cannot be reached must surface HERE, as
        # `ProbeUnavailable` -- retryable, nothing sent -- and not as the
        # first upload's failure.
        with tui.working("Preparing the session import"):
            fetch_ingest_state(client, census.candidates[0].session_id)
    scratch = work_dir
    try:
        if scratch is not None:
            scratch.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        # AFTER CONSENT: the gate has been accepted and nothing has uploaded.
        # An unhandled OSError here is a traceback where a sentence belongs.
        if progress is not None:
            from . import import_jobs

            raise import_jobs.JobError("Could not create the background import working directory.") from exc
        return [
            f"Could not create the working directory for this import ({scratch}): {exc}",
            "Nothing was uploaded. Free some space or fix the permissions, then re-run.",
        ]

    ledger.record_census(census)
    completion = {
        "completion_completed": 0, "completion_total": census.sessions, "completion_ids": [],
    }

    def on_completion(done, total, identities):
        completion.update(
            completion_completed=done, completion_total=total,
            completion_ids=[list(identity) for identity in identities],
        )

    with _import_progress(census.sessions, enabled=interactive) as on_stage:
        outcome = import_transcripts(
            census,
            on_stage=(
                lambda done, total, transcript, phase: progress(
                    phase, completed=done, total=total, source=transcript.agent,
                    session_id=transcript.session_id,
                    **completion,
                )
            ) if progress is not None else on_stage,
            on_completion=on_completion if progress is not None else None,
            approved_files=approved_files,
            expected_customer_id=expected_customer_id,
            stop_on_retryable=progress is not None,
            poster=posters,
            device_id=devices,
            ledger=ledger,
            assignments={},
            scratch=scratch,
            budget_bytes=budget_bytes,
        )
    lines = outcome.lines()
    if census.identity_unverified or census.identity_conflicts or census.unreadable:
        lines.append(
            f"{census.identity_unverified} identities unverified · "
            f"{census.identity_conflicts} conflicting copies · {census.unreadable} unreadable"
        )
    if unpaired:
        # Named, never silent: on a machine with both agents installed, a
        # missing pairing is the difference between importing half the history
        # and thinking you imported all of it.
        lines.append(
            f"{', '.join(unpaired)} sessions were not looked at — no paired "
            "device for that agent on this machine."
        )
    if progress is not None:
        incomplete = outcome.failed or outcome.pending_batches
        progress(
            "Session import paused" if incomplete else "Session import finished",
            completed=outcome.uploaded,
            total=outcome.found, uploaded=outcome.uploaded, failed=outcome.failed,
            skipped_legacy=outcome.skipped_legacy,
            **completion,
        )
        if incomplete:
            from . import import_jobs

            if any("reviewed session" in error for error in outcome.errors):
                raise import_jobs.JobError(
                    "A reviewed session changed. Start a new import to review it again."
                )
            if any("capture credentials belong to a different team" in error for error in outcome.errors):
                raise import_jobs.JobError(
                    "A capture pairing belongs to a different team. Restore the approved pairing to resume."
                )
            if outcome.retryable_failures and outcome.retryable_failures == outcome.failed:
                raise import_jobs.RetryableJobError(
                    f"Session delivery will retry. {outcome.errors[0]}"
                )
            detail = (
                f"First failure: {outcome.errors[0]}. " if outcome.errors else
                "Unacknowledged transcript batches are retained for retry. "
            )
            raise import_jobs.JobError(
                f"Session import is incomplete: {outcome.finalized}/{outcome.found} finalized, "
                f"{outcome.failed} failed. {detail}"
                "See the log for each failed session. Resume from Existing imports to retry."
            )
    return lines
