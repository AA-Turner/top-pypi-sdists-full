"""the approved session import as a background job: identity and payload, reviewed prefix only, execute the census."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
from collections.abc import Iterable
from dataclasses import asdict, replace
from pathlib import Path
from ....tap_core.session_journal import (
    ReconciliationRequired, prefix_hash)


def _background_identity(client) -> dict:
    """Nonsecret account identity pinned before the transcript review."""
    from urllib.parse import urlsplit, urlunsplit

    from ....sdk.settings.settings import current_context_name

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


#: Threads pinning the reviewed transcripts' bytes (`_background_payload`).
HASH_WORKERS = 4


def _background_payload(
    census: Census, *, client, posters, devices, budget_bytes, unpaired,
) -> dict:
    from concurrent.futures import ThreadPoolExecutor

    identity = _background_identity(client)
    # hashlib releases the GIL: a whole history (GBs) hashes ~3x faster on 4 threads.
    pool = ThreadPoolExecutor(max_workers=HASH_WORKERS)
    try:
        digests = pool.map(lambda t: prefix_hash(t.path, t.size), census.candidates)
        files = []
        for transcript, digest in zip(census.candidates, digests):
            row = asdict(transcript)
            row["path"] = str(transcript.path.resolve())
            row["sha256"] = digest
            files.append(row)
    except BaseException:
        # A failure or Ctrl-C surfaces now, not after every queued file is hashed.
        pool.shutdown(wait=False, cancel_futures=True)
        raise
    pool.shutdown()
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
    from .. import jobs as import_jobs

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
    from ....sdk.client.client import Client
    from ....sdk.settings.settings import current_context_name, resolve
    from ...wizard import state as capabilities
    from .. import jobs as import_jobs

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
    from ...wizard import terminal as tui

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
            from .. import jobs as import_jobs

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
            skipped_legacy=outcome.skipped_legacy, skipped_removed=outcome.skipped_removed,
            **completion,
        )
        if incomplete:
            from .. import jobs as import_jobs

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
from probe.cli.imports.transcripts.discovery import Census, Transcript  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.lane import _import_progress  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.ledger import TranscriptLedger, fetch_ingest_state  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.transcripts import import_transcripts  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.upload import Poster  # noqa: E402 -- pieces need each other; the front door loads this one first
