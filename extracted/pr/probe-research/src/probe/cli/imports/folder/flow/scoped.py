"""the scoped import's entry: offer same-scope recovery, dedupe an unfinished approval, run it."""

from __future__ import annotations
import json
from pathlib import Path
import time
import uuid

from .....foundation.durable.durable import file_lock
from ..coverage.coverage import Coverage, CoverageError
from ..coverage.scope import Scope


def _enqueue_reviewed_import(payload, *, label):
    """Deduplicate unfinished approvals, but allow another import after success.

    The request identity belongs to this run; delivery identities stay in
    Coverage. A fresh request therefore rechecks the reviewed files and their
    receipts without uploading already delivered bytes again.
    """
    from ... import jobs as import_jobs

    # Dataclass census fields can contain tuples; compare the persisted JSON
    # representation so repeated foreground approvals share their worker.
    payload = json.loads(json.dumps(payload, sort_keys=True, allow_nan=False))
    with file_lock(Path(payload["directory"]) / "reviewed-import.lock"):
        for job in import_jobs.list_jobs():
            previous = dict(job.get("payload") or {})
            previous.pop("request_id", None)
            if (job.get("kind") == import_jobs.Kind.FOLDER and previous == payload
                    and job["state"] not in {import_jobs.State.SUCCEEDED, import_jobs.State.CANCELED}):
                return (import_jobs.resume(job["id"])
                        if job["state"] == import_jobs.State.INTERRUPTED else job)
        return import_jobs.enqueue(
            kind=import_jobs.Kind.FOLDER,
            payload={**payload, "request_id": uuid.uuid4().hex},
            label=label,
        )


def execute(
    *,
    client_factory,
    folder,
    agent,
    project=None,
    interactive=True,
    yes=False,
    concurrency=None,
    telemetry=None,
    started_at=None,
    summary_state=None,
    lane_state=None,
    source_id=None,
    import_changed=False,
    import_unverified=False,
    retry_dead=False,
    review_excluded=False,
    background=False,
    back_to_selection=False,
    wandb_source=None,
    offer_wandb=True,
    include_hidden=(),
):
    from .... import backfill_run as runner
    from ... import agent_settings as import_agent_settings
    from probe import analytics as tm

    tel = telemetry or tm.null_context()
    start = started_at or time.monotonic()
    stats = {}
    recovery_lines = []
    outcome = tm.BackfillOutcome.CREDENTIALS_FAILED
    is_started = False
    registered_job = None
    agents = None
    try:
        with client_factory() as client:
            scope = Scope.resolve(client, project)
            outcome = tm.BackfillOutcome.PARTIAL
            # Once, before any agent: what this import's lanes run at, and the
            # meter `backfill.summary` reports them from.
            agents = import_agent_settings.resolve(client, agent)
            if not source_id:
                source_id, recovery_lines = _choose_source(
                    Coverage.recovery_candidates(folder, scope), interactive=interactive, yes=yes
                )
            store = Coverage.for_folder(folder, scope, source_id=source_id)
            with store.writer() as coverage:
                coverage.validate_destinations(client)
                tel.emit(
                    tm.EVENT_BACKFILL_STARTED,
                    backfill_agent=agent.value,
                    resumed=bool(coverage.rows()),
                )
                is_started = True
                lines, stats, complete = _run(
                    client,
                    coverage,
                    folder,
                    agent=agent,
                    interactive=interactive,
                    yes=yes,
                    concurrency=concurrency or runner.unit_concurrency(),
                    import_changed=import_changed,
                    import_unverified=import_unverified,
                    retry_dead=retry_dead,
                    review_excluded=review_excluded,
                    tel=tel,
                    stats=stats,
                    background=background,
                    back_to_selection=back_to_selection,
                    wandb_source=wandb_source, offer_wandb=offer_wandb,
                    agents=agents, include_hidden=include_hidden,
                )
                outcome = stats.pop("_outcome", None) or (
                    tm.BackfillOutcome.SUCCESS if complete else tm.BackfillOutcome.PARTIAL
                )
                if outcome in (tm.BackfillOutcome.SUCCESS, tm.BackfillOutcome.PARTIAL) and stats.get(
                    "unclassified_files"
                ):
                    # A failed classifier session left files for the next run,
                    # which by itself keeps coverage short of complete. Said
                    # apart from PARTIAL so analytics can tell a slice the model
                    # could not file from an upload that failed; units_failed
                    # still carries the second.
                    outcome = tm.BackfillOutcome.PARTIAL_CLASSIFICATION
                deferred = stats.pop("_background_payload", None)
                if deferred is None:
                    return [*recovery_lines, *lines]
            # The worker may start immediately. Release the coverage writer
            # before dispatch so it can resume this exact approved source.
            from ... import folder as backfill
            from ...jobs import ui as import_jobs_ui
            from ...jobs.messages import enqueue_report

            job = _enqueue_reviewed_import(
                deferred, label=f"Folder · {Path(folder).name}"
            )
            registered_job = job
            if interactive and not yes:
                job = import_jobs_ui.show_started_import(job)
            return backfill.StartedFolderImport(
                job, [*recovery_lines, *lines, *enqueue_report(job, "Folder import")],
            )
    except _BackToImport:
        from ....wizard import terminal as tui

        outcome = tm.BackfillOutcome.ABORTED
        if back_to_selection:
            return tui.BACK
        raise
    except KeyboardInterrupt:
        outcome = tm.BackfillOutcome.ABORTED
        raise
    except _Stopped as exc:
        if registered_job is not None:
            return backfill.StartedFolderImport.status_unavailable(registered_job, exc)
        outcome = exc.outcome
        stats.update(exc.stats)
        return [*recovery_lines, *stats.pop("_report", []), *exc.lines]
    except CoverageError as exc:
        if registered_job is not None:
            return backfill.StartedFolderImport.status_unavailable(registered_job, exc)
        return [*recovery_lines, *stats.pop("_report", []), f"Backfill needs attention: {exc}"]
    except Exception as exc:
        if registered_job is not None:
            return backfill.StartedFolderImport.status_unavailable(registered_job, exc)
        if outcome == tm.BackfillOutcome.CREDENTIALS_FAILED:
            from probe.sdk.session_marker import WIZARD_HINT

            return [
                f"Could not reach Probe: {exc}",
                f"Sign in again ({WIZARD_HINT}), then re-run; "
                "no file delivery was started.",
            ]
        return [
            *recovery_lines,
            *stats.pop("_report", []),
            f"Backfill could not finish: {exc}",
            "Saved plans, intentions and receipts are retained. Re-running resumes verified work.",
        ]
    finally:
        if not is_started:
            tel.emit(tm.EVENT_BACKFILL_STARTED, backfill_agent=agent.value, resumed=False)
        if summary_state is not None:
            summary_state["emitted"] = True
        tel.emit(
            tm.EVENT_BACKFILL_SUMMARY,
            outcome=outcome,
            duration_seconds=int(time.monotonic() - start),
            # One dict, so a stats key the meter also names can never become a
            # duplicate-keyword TypeError out of this `finally`.
            **{
                **{key: value for key, value in stats.items() if not key.startswith("_")},
                **(agents.meter.properties() if agents is not None else {}),
            },
        )


def _choose_source(candidates, *, interactive, yes):
    """Offer same-scope recovery hints without adopting a fingerprint match."""
    from ....wizard import terminal as tui

    if not candidates:
        return None, []
    lines = ["Possible earlier imports in this destination scope:"]
    for candidate in candidates:
        lines.append(f"  {candidate['source_id']}: {', '.join(candidate['paths'][:3])}")
    lines.append("Folder similarity is a recovery hint; it does not verify file delivery.")
    chosen = ""
    if interactive and not yes:
        chosen = tui.review(
            "Recover an earlier import?", lines,
            [
                ("Start a separate import", ""),
                *[(f"Recover {item['source_id']}", item["source_id"]) for item in candidates],
            ],
        )
        if chosen is tui.BACK:
            raise _BackToImport
        if chosen is None:
            raise KeyboardInterrupt
        if chosen and chosen not in {item["source_id"] for item in candidates}:
            raise CoverageError(
                "Choose a listed source ID, or rerun with --source-id and the saved ID."
            )
    if chosen:
        lines.append(
            f"Recovering selected source {chosen}; current bytes and receipts will be checked."
        )
    else:
        lines.append(
            "Starting a separate source. To recover an earlier import, rerun with --source-id ID."
        )
    return chosen or None, lines
from probe.cli.imports.folder.flow.flow import _BackToImport, _Stopped, _run  # noqa: E402 -- pieces need each other; the front door loads this one first
