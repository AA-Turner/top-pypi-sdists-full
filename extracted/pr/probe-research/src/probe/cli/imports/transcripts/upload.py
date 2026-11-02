"""upload one session's frozen prefix through the shared durable journal, and prove reviewed bytes already landed."""

from __future__ import annotations
import hashlib
import json
import os
import sqlite3
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from ....foundation.tls.tls import ssl_context
from ....tap_core import capture_gate as tap_gate
from ....tap_core.session_identity import validate_identity
from ....tap_core.session_journal import (
    DELETED_STATE, RECEIPTED_PROTOCOLS, DeliveryPending, Journal, ProtocolRestarted,
    ReconciliationRequired, SessionDeleted, Wire, prefix_hash)
from ....tap_core.transcript import MAX_BATCH_BYTES

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
#: Times one session's batch 0 may restart on the other protocol in one run
#: (`ProtocolRestarted`: protocol 3 refused -> 2, protocol 2 retired -> 3). One
#: each way covers a settings rollout; more means the server's answers flip
#: back and forth, and the session waits for a later run instead of looping.
MAX_PROTOCOL_RESTARTS = 2


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
    #: The session file was deleted from this machine (`_removed_from_machine`)
    #: while this call read it. The caller decides whether that is a skip.
    source_removed: bool = False


def _removed_from_machine(exc: BaseException, path: Path) -> bool:
    """`exc` failed because the session file at `path` was deleted, and nothing else.

    Claude Code deletes transcripts nobody has opened for `cleanupPeriodDays`
    (30 by default), silently, after any session starts, so a file a census
    found can be gone by upload time. It is a removal only when the error names
    this file, the file is still absent, and the folder that held it still
    exists: the sweep deletes session files, not the project folder around
    them. A folder that is gone too (an unmounted drive, a moved config
    directory, even one recreated empty since) or an absence that cannot be
    proved (a permission error) stays a failure, so it still stops the import
    and reaches its owner.
    """
    if not isinstance(exc, FileNotFoundError) or exc.filename is None:
        return False
    if os.fspath(exc.filename) != os.fspath(path):
        return False
    try:
        path.lstat()
    except FileNotFoundError:
        pass
    except OSError:
        return False
    else:
        return False
    try:
        return path.parent.is_dir()
    except OSError:
        return False


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
        # Coverage is cursors and hashes, whichever protocol the stream uses.
        remote.get("protocol_version") not in RECEIPTED_PROTOCOLS or remote.get("state") != "ready"
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
        is_rechecked = False
        expected_history = None
        restarts = 0
        while True:
            stage = "reading transcript"
            # The switch was decided above (`_switched_off`: a session's own
            # `off`); the journal's gate still skips what its gap file covers.
            with tap_gate.switch_decided():
                body = journal.stage(
                    transcript.session_id, cwd=transcript.cwd or "", historical_only=True,
                    require_no_pending=expected_history is not None, expected_history=expected_history,
                    # Protocol 3 packs toward 2 MiB: a smaller budget must still
                    # fit a batch, as protocol 2's 1 MiB fits the 1 MB minimum.
                    packing_cap=budget_bytes,
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
            except ProtocolRestarted as exc:
                # Batch 0 was refused on its protocol (3 not enabled, or 2
                # retired) and dropped; the same range is staged again on the
                # other protocol now, not on a later run. Bounded: a server
                # whose answers flip back and forth leaves the session for a
                # later run instead of looping -- and says so, not the
                # restart's "sent again" this run will not do.
                restarts += 1
                if restarts > MAX_PROTOCOL_RESTARTS:
                    raise DeliveryPending(
                        f"protocol restarted {restarts} times this run: {exc}",
                        retryable=True,
                        safe_message=(
                            "the server refused this new session on both protocols; "
                            "it is left for the next import"
                        ),
                    ) from exc
                continue
            except ReconciliationRequired as exc:
                if exc.status_code != 409 or is_rechecked:
                    raise
                is_rechecked = True
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
        result.source_removed = _removed_from_machine(exc, (coverage_source or transcript).path)
    finally:
        if own_journal and journal is not None:
            journal.close()
    return result
from probe.cli.imports.transcripts.discovery import Transcript  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.ledger import SessionRecord  # noqa: E402 -- pieces need each other; the front door loads this one first
