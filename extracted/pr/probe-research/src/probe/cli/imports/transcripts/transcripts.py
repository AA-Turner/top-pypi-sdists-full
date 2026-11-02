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
import sqlite3
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from ....foundation.tls.tls import ssl_context
from ....tap_core.session_journal import (
    DELETED_STATE, DeliveryPending, Journal, ReconciliationRequired, SessionDeleted, Wire)


def _upload_started(remote: dict, journal: Journal, session_id: str) -> bool:
    """Part of this session already reached the server, or is staged to.

    A removed file is nothing-to-do only when nothing was sent: a partial
    stream on the server, or a batch the journal still holds, stays a failure
    rather than a skip that would hide an upload left half done.
    """
    stream = remote.get("stream")
    if isinstance(stream, dict) and stream.get("finalized") is not True:
        return True
    # One read of the journal, so a writer cannot stage a batch between the two.
    with journal.transaction():
        pending = journal.pending(session_id)
        state = journal.get(session_id)
    if pending is not None:
        return True
    return bool(state) and state.get("last_seq", -1) >= 0 and not state.get("historical_complete")


# --- project mapping ---------------------------------------------------------


def _human_bytes(count: int) -> str:
    size = float(count)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}GB"


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
    #: Session files deleted from this machine between the census and the
    #: upload, with nothing of them sent. A skip, never a failure.
    skipped_removed: int = 0
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
        if self.skipped_removed:
            out.append(
                f"{self.skipped_removed} removed from this machine before upload (nothing sent)"
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
    ``on_completion`` counts every session the lane has accounted for (see
    `accounted_ids`), not only finalizations. ``on_stage`` retains its
    processed-session semantics.
    """
    outcome = LaneOutcome(
        found=census.sessions,
        skipped_live=census.captured_live,
        skipped_in_probe=census.already_in_probe,
    )
    posters = poster if isinstance(poster, dict) else dict.fromkeys(INGEST_PATH, poster)
    remaining = budget_bytes
    #: Sessions this lane has ACCOUNTED FOR -- finalized here, found already
    #: held by the server, deleted at the team's request, or removed from this
    #: machine with nothing sent. All belong in the progress denominator: a bar that
    #: can never reach its total on a machine with pre-protocol-2 history reads
    #: as an import that never finished, which is the opposite of the truth.
    #: The report lines below keep them apart in words.
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
        is_processed = True
        is_already_finalized = False
        failure = None
        #: Replaces the finally block's "Session processed" when a session was
        #: counted without being uploaded. One `on_stage` per session is the
        #: contract the progress estimator and the job record both assume.
        note = None
        #: The session file on disk. `transcript` is rebound to the reviewed
        #: copy below, so this is what tells a removed source apart.
        source_path = transcript.path
        remote = None
        result = None
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
            is_already_finalized = result.already_finalized
            outcome.bytes_sent += result.bytes_sent
            if remaining is not None:
                remaining = max(0, remaining - result.bytes_sent)
            if not result.ok:
                raise DeliveryPending(result.error or "upload pending", retryable=result.retryable)
            if result.error == "budget":
                outcome.deferred += len(census.candidates) - index
                is_processed = False
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
            # The session file was deleted after the census found it -- usually
            # by Claude Code's own `cleanupPeriodDays` sweep (see
            # `_removed_from_machine`), which can land between review and
            # upload. With nothing of it sent, that is a skip, like
            # `skipped_legacy`: no resume can bring the file back, so counting
            # it as a failure only failed the job and mailed "Resume to retry"
            # every time. A receipt that matches the approved size and hash
            # finalizes without the file and never reaches here; one that runs
            # past them needs the file for its proof, so it lands here too, and
            # the server's longer copy stands untouched.
            is_removed = remote is not None and (
                _removed_from_machine(exc, source_path)
                or (result is not None and result.source_removed)
            )
            if is_removed:
                opened = None
                try:
                    if journal is None:
                        journal = opened = Journal(wire.base_url, remote["customer_id"], transcript.agent)
                    # Fresh receipts: `upload_session` read its own after ours,
                    # and an upload may have started in between.
                    is_removed = not _upload_started(
                        wire.receipts(transcript.session_id), journal, transcript.session_id,
                    )
                except Exception:
                    # Anything that stops the check (an unreadable or newer
                    # journal, no answer from the server) leaves it unproved:
                    # the ordinary failure below, never an error that ends the
                    # whole import. A journal opened only for this check is
                    # closed here, so the cleanup below does not read it again.
                    is_removed = False
                    if opened is not None:
                        with contextlib.suppress(Exception):
                            opened.close()
                        journal = None
            if is_removed:
                outcome.skipped_removed += 1
                note = "Removed from this machine before upload; nothing sent"
                accounted_ids.add((transcript.agent, transcript.session_id))
                if on_completion:
                    on_completion(len(accounted_ids), census.sessions, sorted(accounted_ids))
            else:
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
                    if not is_already_finalized:
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
                    index + int(is_processed), census.sessions, transcript,
                    f"Session failed — {failure}" if failure else (
                        note or ("Session processed" if is_processed else "Byte budget reached")
                    ),
                )
    return outcome
from probe.cli.imports.transcripts.background import _approved_transcript  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.discovery import Census, Transcript  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.ledger import SessionRecord, TranscriptLedger  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.roots import INGEST_PATH  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.upload import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    Poster,
    UploadResult,
    _failure_message,
    _finalized_coverage,
    _record_finalized_coverage,
    _removed_from_machine,
    upload_session,
)
