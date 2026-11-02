"""what is already imported: the server's ingest state and this machine's append-only transcript ledger."""

from __future__ import annotations
import json
import os
from dataclasses import dataclass
from probe.foundation.compat.compat import StrEnum
from pathlib import Path

from ....foundation.durable.durable import file_lock, fsync_directory, now_iso
from probe.cli.imports.transcripts.roots import CLAUDE

SCHEMA = "probe.backfill.transcripts/1"


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
    from ....sdk import errors

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
        from ..folder.upload.ledger import default_dir

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
from probe.cli.imports.transcripts.discovery import Census, Transcript  # noqa: E402 -- pieces need each other; the front door loads this one first
