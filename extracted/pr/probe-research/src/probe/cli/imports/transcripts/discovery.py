"""walk the transcript trees: one Transcript per session file (id, cwd), bucketed into a Census, tap-tracked ones noted."""

from __future__ import annotations
import json
import os
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from ....tap_core.session_identity import check_identity, compatible_copy
from ....tap_core.session_journal import ReconciliationRequired
from probe.cli.imports.transcripts.roots import CLAUDE, CODEX, KIMI, PI, _tap_offsets, transcript_roots


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
    if agent == KIMI:
        # sessions/<workdir>/session_<uuid>/agents/main/wire.jsonl
        if path.name != "wire.jsonl" or path.parent.name != "main":
            return None
        canonical = _kimi().canonical_session_id(path.parent.parent.parent.name)
        return canonical if _CLAUDE_SESSION_STEM_RE.fullmatch(canonical) else None
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
    if agent == KIMI:
        # Kimi keeps the session's folder in its own state.json, beside the wire.
        try:
            state = json.loads((path.parent.parent.parent / "state.json").read_text(encoding="utf-8"))
        except (OSError, ValueError, RecursionError):
            return None
        found = state.get("cwd") if isinstance(state, dict) else None
        return found if isinstance(found, str) and found else None
    try:
        with path.open("rb") as handle:
            for index, raw in enumerate(handle):
                if index >= max_lines:
                    return None
                try:
                    event = json.loads(raw)
                except (ValueError, UnicodeDecodeError, RecursionError):
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


def _walk(root: Path, agent: str) -> Iterator[Path]:
    if not root.exists():
        return
    if agent == KIMI:
        # Main wires only: helper agents' wires sit beside them.
        yield from sorted(root.glob(_kimi().transcript_pattern()))
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
    #: Sessions whose Probe switch reads `off`, or that have a stretch written
    #: while it was (their gap file, `probe.service.sessions.capture_gate`): Probe off
    #: means the session is not captured, and an import never backfills one.
    switched_off: int = 0
    #: Sessions Probe's own folder import ran (their working directory is
    #: inside the import's state): its classifier and upload agents, never the
    #: researcher's work. 45 of them were imported as one researcher's history
    #: on 2026-10-25.
    import_agents: int = 0
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
    from ..folder.upload.ledger import is_import_agent_cwd

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
                check_identity(path, agent, session_id)
            except ReconciliationRequired:
                census.identity_unverified += 1
                continue
            except OSError:
                census.unreadable += 1
                continue
            if session_id in tracked:
                census.captured_live += 1
                continue
            if _switched_off(session_id):
                census.switched_off += 1
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
            cwd = read_cwd(path, agent)
            if is_import_agent_cwd(cwd):
                census.import_agents += 1
                continue
            by_session[key] = Transcript(
                path=path,
                session_id=session_id,
                agent=agent,
                cwd=cwd,
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


def _switched_off(session_id: str) -> bool:
    """Was Probe switched off for this session itself (its own `.state` says
    `off`), or for a stretch of it (its gap file holds a gap, or does not
    read)? Such a session is never imported: not the stretch, and not the rest
    either, since an import cannot tell where the stretch was. A machine
    default of `off`, or PROBE_SESSION_STATE in this shell, skips nothing: it
    says nothing about a session written before it was set."""
    try:
        from probe.service.sessions import capture_gate

        sessions = capture_gate.sessions_dir_for(os.environ)
        if capture_gate.read_gap_file(sessions, session_id):
            return True
        return capture_gate.explicitly_off(session_id, sessions)
    except Exception:  # noqa: BLE001 -- the switch decides nothing it cannot be read for
        return False


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
from probe.shared.harness.harnesses.claude_code.transcripts import _CLAUDE_SESSION_STEM_RE, history_sessions  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.kimi_code.transcripts import _kimi  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.transcripts import _is_pi_session_file  # noqa: E402 -- pieces need each other; the front door loads this one first
