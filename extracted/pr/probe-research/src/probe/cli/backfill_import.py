"""Folder orchestration: authenticated scope, reviewed bytes, verified receipts."""

from __future__ import annotations

from dataclasses import asdict
from contextlib import contextmanager, nullcontext
import hashlib
import json
import os
from pathlib import Path
import shlex
import time
import uuid

from ..sdk.durable import file_lock, fsync_directory, write_text_atomic
from . import backfill_delivery as delivery
from . import backfill_evidence as evidence
from . import backfill_github as github
from . import backfill_legacy as legacy
from ..sdk import agent_session
from . import backfill_plan as plans
from . import backfill_wandb as wandb
from . import backfill_ledger as ledger_mod
from .backfill_coverage import Coverage, CoverageError, Scope
from .backfill_ledger import Ledger, Unit, UnitKind, UnitState


class _Stopped(CoverageError):
    """An expected workflow stop with a closed telemetry outcome."""

    def __init__(self, outcome, *lines, **stats):
        super().__init__("\n".join(lines))
        self.outcome, self.lines, self.stats = outcome, list(lines), stats


class _BackToImport(KeyboardInterrupt):
    """A pre-delivery form returned to the folder import choices."""


BACKGROUND_SCHEMA = "probe.folder-import-job/1"
AUTO_BACKGROUND_SCHEMA = "probe.folder-auto-import-job/1"


def enqueue_auto_import(
    *, client_factory, folder, agent, auto_approve, project=None, concurrency=None,
    source_id=None, import_changed=False, import_unverified=False, retry_dead=False,
    wandb_approval=None,
):
    """Persist an explicit folder-scoped automatic approval before any scan."""
    from . import import_jobs
    from . import backfill_run as runner

    if auto_approve is not True:
        raise CoverageError("Automatic folder imports require explicit approval.")
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise CoverageError("The selected folder is unavailable.")
    info = folder.stat()
    with client_factory() as client:
        if wandb_approval is not None:
            wandb_approval = wandb.validate_automatic_approval(client, wandb_approval)
            approved_project = wandb_approval["project_id"]
            if project and Scope.resolve(client, project).project_id != approved_project:
                raise CoverageError("The selected project differs from the approved W&B destination.")
            project = f"id:{approved_project}"
        scope = Scope.resolve(client, project)
        if wandb_approval is not None and scope.workspace_id != wandb_approval["workspace_id"]:
            raise CoverageError("The approved W&B project moved to another workspace.")
        user_id = client.me().get("user_id")
        if not user_id:
            raise CoverageError("Cannot verify the account for this folder import.")
        store = Coverage.for_folder(folder, scope, source_id=source_id)
        intent = {
            "schema": AUTO_BACKGROUND_SCHEMA, "auto_approve": True,
            "folder": str(folder), "folder_identity": [info.st_dev, info.st_ino],
            "agent": agent.value, "scope": asdict(scope), "user_id": user_id,
            "source_id": store.source_id, "directory": str(store.directory),
            "concurrency": concurrency or runner.unit_concurrency(),
            "context": (client.journal.context or {}).get("name"),
            "spool_dir": str(client.journal.dir),
            "import_changed": bool(import_changed), "import_unverified": bool(import_unverified),
            "retry_dead": bool(retry_dead),
            **({"wandb_approval": wandb_approval} if wandb_approval is not None else {}),
        }
    # Close the admission client before registering a job: a cleanup failure
    # must not lose the identity of a worker that was already started.
    # The admission lock covers lookup + enqueue, keeping active work shared.
    with file_lock(store.directory / "auto-import.lock"):
        for job in import_jobs.list_jobs():
            previous = dict(job.get("payload") or {})
            previous.pop("request_id", None)
            if (job.get("kind") == import_jobs.Kind.FOLDER and previous == intent
                    and job["state"] in {import_jobs.State.QUEUED, import_jobs.State.RUNNING,
                                         import_jobs.State.INTERRUPTED}):
                return import_jobs.resume(job["id"]) if job["state"] == import_jobs.State.INTERRUPTED else job
        return import_jobs.enqueue(
            kind=import_jobs.Kind.FOLDER,
            payload={**intent, "request_id": uuid.uuid4().hex},
            label=f"Folder · {folder.name}",
        )


def _enqueue_reviewed_import(payload, *, label):
    """Deduplicate unfinished approvals, but allow another import after success.

    The request identity belongs to this run; delivery identities stay in
    Coverage. A fresh request therefore rechecks the reviewed files and their
    receipts without uploading already delivered bytes again.
    """
    from . import import_jobs

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


def _auto_checkpoint(payload):
    try:
        request_id = uuid.UUID(payload["request_id"]).hex
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        raise CoverageError("The automatic folder import has an invalid request identity.") from exc
    path = Path(payload["directory"]) / "auto-imports" / f"{request_id}.json"
    identity = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return path, identity


def _read_auto_checkpoint(path, identity):
    try:
        saved = json.loads(path.read_text())
        if (saved["intent"] != identity or not isinstance(saved["delivery"], dict)
                or saved["delivery"].get("schema") != BACKGROUND_SCHEMA
                or saved["sha256"] != hashlib.sha256(
                    json.dumps(saved["delivery"], sort_keys=True).encode()
                ).hexdigest()):
            raise ValueError("mismatched approval")
        return saved["delivery"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise CoverageError("The saved automatic import plan could not be verified; its files were retained.") from exc


def _verify_auto_folder(payload):
    folder = Path(payload["folder"])
    if not folder.is_absolute() or not folder.is_dir() or folder.resolve() != folder:
        raise CoverageError("The approved folder is unavailable. Restore it before resuming.")
    info = folder.stat()
    if [info.st_dev, info.st_ino] != payload.get("folder_identity"):
        raise CoverageError("The selected folder was replaced. Start a new import for the replacement folder.")
    return folder


def _run_auto_import(payload, *, progress):
    """Prepare once, durably pin the resulting approval, then deliver in this job."""
    from . import backfill as bf, import_jobs, telemetry

    if payload.get("auto_approve") is not True:
        raise CoverageError("This folder job has no explicit automatic approval.")
    folder = _verify_auto_folder(payload)
    checkpoint, identity = _auto_checkpoint(payload)
    scope = Scope(**payload["scope"])
    stats = {}
    history_lines = []
    try:
        progress("Resuming the saved import plan" if checkpoint.exists() else "Scanning the selected folder",
                 phase="importing" if checkpoint.exists() else "scanning")
        with _background_client(payload) as client:
            if (Scope.resolve(client, f"id:{scope.project_id}" if scope.project_id else None,
                              workspace_id=scope.workspace_id) != scope
                    or client.me().get("user_id") != payload["user_id"]):
                raise CoverageError("The current account or destination differs from this automatic import.")
            if payload.get("wandb_approval") is not None:
                approval = wandb.validate_automatic_approval(client, payload["wandb_approval"])
                if (approval["project_id"] != scope.project_id
                        or approval["workspace_id"] != scope.workspace_id):
                    raise CoverageError("The automatic folder and W&B destinations do not match.")
            store = Coverage(Path(payload["directory"]), scope, payload["source_id"])
            with store.writer() as coverage:
                coverage.validate_destinations(client)
                prior_digest = import_jobs.prepared_approval_digest()
                if prior_digest is not None and not checkpoint.exists():
                    raise CoverageError("The prepared import plan is missing. Restore it or start a new import.")
                if checkpoint.exists():
                    prepared = _read_auto_checkpoint(checkpoint, identity)
                else:
                    lines, stats, complete = _run(
                        client, coverage, folder, agent=bf.Agent(payload["agent"]),
                        interactive=False, yes=True, concurrency=payload["concurrency"],
                        import_changed=payload["import_changed"],
                        import_unverified=payload["import_unverified"],
                        retry_dead=bool(payload.get("retry_dead")),
                        tel=telemetry.null_context(), stats=stats, background=True,
                        progress=progress, auto_approve=True,
                    )
                    prepared = stats.get("_background_payload")
                    if prepared is None:
                        if complete:
                            if payload.get("wandb_approval") is not None:
                                progress("Starting approved W&B history", phase="importing")
                                history = wandb.admit_automatic_history(client, coverage, payload["wandb_approval"])
                                lines.append(f"W&B history {history['external_id']}: {history['receipt']['state']}.")
                            return lines
                        raise CoverageError(
                            "Folder preparation needs attention. "
                            + " ".join(str(line) for line in lines[-3:])[:600]
                        )
                    _verify_auto_folder(payload)
                    checkpoint.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                    fsync_directory(checkpoint.parent.parent)
                    write_text_atomic(checkpoint, json.dumps({
                        "intent": identity, "delivery": prepared,
                        "sha256": hashlib.sha256(json.dumps(prepared, sort_keys=True).encode()).hexdigest(),
                    }, sort_keys=True), mode=0o600)
                digest = hashlib.sha256(json.dumps(prepared, sort_keys=True).encode()).hexdigest()
                if prior_digest is not None and prior_digest != digest:
                    raise CoverageError("The prepared import plan changed. Start a new import to approve another plan.")
                import_jobs.remember_prepared_approval(digest)
                if payload.get("wandb_approval") is not None:
                    progress("Starting approved W&B history", phase="importing")
                    history = wandb.admit_automatic_history(client, coverage, payload["wandb_approval"])
                    history_lines.append(f"W&B history {history['external_id']}: {history['receipt']['state']}.")
        # The approval is durable before ANY file delivery starts. Replays use
        # only this snapshot, so later/new bytes need another import decision.
        _verify_auto_folder(payload)
        return [*history_lines, *run_background_job(prepared, progress=progress)]
    except Exception as exc:
        if not stats.get("failed_units") and import_jobs.is_retryable_error(exc):
            raise import_jobs.RetryableJobError(
                "The folder connection is unavailable. Completed reads and uploads are saved."
            ) from None
        if isinstance(exc, (CoverageError, import_jobs.JobError)):
            raise
        raise CoverageError(
            f"Automatic folder import paused ({type(exc).__name__}). Saved progress is retained."
        ) from None
    finally:
        bf.stop_all()


def _approval_snapshot(coverage):
    return {
        row["path"]: {"hash": row["approved_hash"], "project_id": row["project_id"],
                      "exclusion": row["exclusion"]}
        for row in coverage.rows()
        if row["approved_hash"] and row["project_id"]
    }


def _unit_snapshot(ledger):
    return {
        key: {"project": record.unit.project, "paths": list(record.unit.paths),
              "kind": record.unit.kind.value}
        for key, record in ledger.read().units.items()
    }


def _background_payload(coverage, client, folder, agent, concurrency, records, census):
    """Immutable reviewed scope and local checkpoint addresses, never credentials."""
    return {
        "schema": BACKGROUND_SCHEMA,
        "folder": str(folder),
        "agent": agent.value,
        "concurrency": concurrency,
        "scope": asdict(coverage.scope),
        "user_id": client.me().get("user_id"),
        "source_id": coverage.source_id,
        "directory": str(coverage.directory),
        "context": (client.journal.context or {}).get("name"),
        "spool_dir": str(client.journal.dir),
        "approved": _approval_snapshot(coverage),
        "targets": [
            row["path"] for row in coverage.rows()
            if row["approved_hash"] and row["project_id"] and row["present"]
            and row["approved_hash"] == row["observed_hash"] and not row["observation_error"]
        ],
        "units": coverage.meta("approved_units", {}),
        "unit_plan": _unit_snapshot(Ledger(coverage.directory / "units.jsonl")),
        "reviewed_sources": coverage.meta("reviewed_sources", {}),
        "records": [
            {"path": str(Path(record.path).relative_to(folder)), "size": record.size,
             "mtime": record.mtime, "tier": record.tier.value}
            for record in records
        ],
        "census": asdict(census),
    }


def _background_client(payload):
    from ..sdk.client import Client
    from ..sdk.config import resolve

    # Resolve credentials afresh from the saved context. Pin the reviewed
    # workspace, while retaining backend/tenant checks before any state write.
    settings = resolve(
        context=payload.get("context"), base_url=payload["scope"]["backend"],
        workspace=payload["scope"]["workspace_id"],
    )
    return Client(
        settings=settings, spool_dir=payload["spool_dir"], attribution="backfill",
        async_writes=False, auto_drain=False,
    )


def run_background_job(payload, *, progress):
    """Resume only the reviewed file versions captured by a queued folder job."""
    from . import backfill as bf
    from . import backfill_run as runner
    from .import_jobs import RetryableJobError, is_retryable_error

    if payload.get("schema") == AUTO_BACKGROUND_SCHEMA:
        return _run_auto_import(payload, progress=progress)
    if payload.get("schema") != BACKGROUND_SCHEMA:
        raise CoverageError("This folder job has an unsupported saved format.")
    folder = Path(payload["folder"])
    scope = Scope(**payload["scope"])
    if not folder.is_absolute() or not folder.is_dir() or folder.resolve() != folder:
        raise CoverageError("The approved source folder is unavailable. Restore it before resuming.")
    directory = Path(payload["directory"])
    if not (directory / "coverage.sqlite3").is_file():
        raise CoverageError("The approved folder checkpoint is unavailable; review the import again.")
    stats = {}
    try:
        progress("Verifying the approved folder and destination", phase="importing")
        with _background_client(payload) as client:
            actual = Scope.resolve(
                client, f"id:{scope.project_id}" if scope.project_id else None,
                workspace_id=scope.workspace_id,
            )
            if actual != scope or client.me().get("user_id") != payload["user_id"]:
                raise CoverageError("The current account or destination differs from this approved job.")
            store = Coverage(directory, scope, payload["source_id"])
            with store.writer() as coverage:
                ledger = Ledger(directory / "units.jsonl")
                coverage.validate_destinations(client)
                if (
                    _approval_snapshot(coverage) != payload["approved"]
                    or coverage.meta("approved_units", {}) != payload["units"]
                    or _unit_snapshot(ledger) != payload["unit_plan"]
                    or coverage.meta("approved_request")
                ):
                    raise CoverageError("The saved file approvals changed. Review this import again.")
                records = [
                    evidence.FileEvidence(
                        path=str(folder / item["path"]), size=item["size"], mtime=item["mtime"],
                        tier=evidence.Tier(item["tier"]),
                    )
                    for item in payload["records"]
                ]
                paths = [item["path"] for item in payload["records"]]
                coverage.observe(
                    folder, paths,
                    progress=_census_progress(progress, "Verifying approved file contents", phase="importing"),
                )
                coverage.reconcile(client)
                targets = set(payload["targets"])
                progress(
                    "Approved file receipts verified",
                    completion_completed=len(targets & _completed_paths(coverage)),
                    completion_total=len(targets),
                )
                git = github.GitEvidenceBundle([
                    github.GitEvidence(**item)
                    for items in payload["reviewed_sources"].values() for item in items
                ])
                report = runner.Report()
                lines, _, _ = _deliver_approved(
                    client, coverage, folder, agent=bf.Agent(payload["agent"]),
                    interactive=False, yes=False, concurrency=payload["concurrency"],
                    records=records, paths=paths, census=bf.Census(**payload["census"]),
                    ledger=ledger, work_dir=directory / "manifests",
                    git=git, report=report, stats=stats, selected=set(),
                    previously_complete=coverage.meta("last_verified_complete", False),
                    progress=progress,
                    retry_network=True,
                    completion_targets=targets,
                )
                delivered = _completed_paths(coverage)
                remaining = targets - delivered
                progress(
                    "Folder import complete" if not remaining else "Approved files need attention",
                    completed=len(targets & delivered), total=len(targets),
                    completion_completed=len(targets & delivered), completion_total=len(targets),
                )
                if remaining:
                    dead = remaining & set(coverage.report()["dead"])
                    if dead:
                        retry = [
                            "probe", "--base-url", scope.backend, "backfill", str(folder),
                            "--retry-dead", "--source-id", payload["source_id"], "--no-transcripts",
                        ]
                        if scope.project_id:
                            retry.extend(["--project", f"id:{scope.project_id}"])
                        raise CoverageError(
                            f"{len(remaining)} approved file(s) remain unfinished; "
                            f"{len(dead)} failed repeatedly and reached the agent attempt limit. "
                            "Resume can finish saved uploads, but will not retry those agent units. "
                            "In this import's account and workspace, review a new plan with: "
                            f"`{shlex.join(retry)}`. Per-file report: {coverage.write_report()}"
                        )
                    raise CoverageError(
                        f"{len(remaining)} approved file(s) remain unfinished. "
                        "Saved progress is retained; resume from Existing imports. "
                        "Changed files require another review."
                    )
                return lines
    except CoverageError:
        raise
    except Exception as exc:
        if not stats.get("failed_units") and is_retryable_error(exc):
            raise RetryableJobError(
                "The folder connection is unavailable. Approved files and completed uploads are saved."
            ) from None
        # Transport exceptions can contain request details or credentials.
        # Keep the durable job error useful without copying those details.
        raise CoverageError(
            f"Folder import paused ({type(exc).__name__}). "
            "Saved progress is retained; resume from Existing imports."
        ) from None
    finally:
        bf.stop_all()


def _completed_paths(coverage):
    known = coverage.report()
    return set(known["delivered"] + known["references"] + known["excluded"])


@contextmanager
def _phase(stats: dict, name: str):
    """Record how long one phase of an import took, in seconds.

    Every wall-clock figure anyone has quoted for this importer has been an
    estimate derived from its constants. These are the measurement: which phase
    a real drive actually spends its hours in decides which knob is worth
    turning, and nobody could tell before.
    """
    started = time.monotonic()
    try:
        yield
    finally:
        elapsed = round(time.monotonic() - started, 2)
        stats[f"seconds_{name}"] = round(stats.get(f"seconds_{name}", 0.0) + elapsed, 2)


class _TransientFlush(RuntimeError):
    """A drain that failed for a reason worth waiting out."""


#: Flush attempts before a foreground import stops waiting for the connection.
#: With the shared 2s->5min backoff the waits are 2+4+8+16+32+64 = just over two
#: minutes, which covers a laptop moving between networks. Longer than that
#: belongs to a background job, which has a supervisor; a foreground process
#: that sits for an hour is one nobody can tell from a hang.
FLUSH_ATTEMPTS = 7

#: Set to 1 to stop waiting at all. A known-offline machine wants that, and so
#: does a test suite pointed at an unroutable host -- otherwise every drain in
#: it is a genuine transient failure and every flush costs the full backoff.
FLUSH_ATTEMPTS_ENV = "PROBE_FLUSH_ATTEMPTS"


def flush_attempts() -> int:
    raw = os.environ.get(FLUSH_ATTEMPTS_ENV)
    if raw:
        try:
            return max(1, min(int(raw), 12))
        except ValueError:
            pass
    return FLUSH_ATTEMPTS


def _flush_uploads(client, *, retry_network: bool, report=None, progress=None,
                   on_delivered=None) -> None:
    """Drain the outbox, waiting out a dropped connection rather than failing.

    The outbox worker has had patient backoff since it was written. The import
    never used it: a Wi-Fi blip during the upload raised straight through
    `execute`, and a multi-hour run ended with "Backfill could not finish" even
    though every byte was already staged and resumable. Nothing was lost, but
    nothing continued either, and a person had to be there to re-run it.

    A background job keeps deferring to its own supervisor -- that worker owns
    the schedule and can wait far longer than a foreground process should. This
    only changes what happens when there is no supervisor.
    """
    from ..sdk import durable
    from .import_jobs import RetryableJobError, is_retryable_error

    attempts = flush_attempts()

    if retry_network:
        def on_error(exc):
            if is_retryable_error(exc):
                raise RetryableJobError(
                    "The upload connection is unavailable. Completed uploads are saved."
                ) from None

        client.flush(on_error=on_error, on_delivered=on_delivered)
        return

    def attempt():
        """Drain once. Returns the report, or None when it could not run at all.

        `Client.flush` returns a DELIVERED COUNT and never raises on a network
        failure -- the drain classifies transport errors itself, parks the
        operation and returns -- so an exception-shaped retry around it waits
        for something that cannot happen. The drain's own report is the signal,
        and `stopped_transient` is the precise half of it: work merely left
        QUEUED is the normal state of an import with no drainer attached, and
        sleeping through the backoff for that would add two minutes to every
        ordinary partial run.
        """
        from ..sdk.journal import drain

        try:
            return drain(client.journal, client_factory=client._outbox_client_factory(),
                         on_delivered=on_delivered)
        except Exception as exc:
            if not is_retryable_error(exc):
                raise
            return None

    def waiting(attempt_number, outcome):
        if attempt_number >= attempts or (outcome is not None
                                                and not outcome.stopped_transient):
            return
        message = "The upload connection is unavailable; waiting to retry. Completed uploads are saved."
        if progress:
            progress(message)
        elif report is not None:
            report.add(message)

    def settled(outcome) -> bool:
        """Anything but a transient stop. A parked queue is what we wait out."""
        return outcome is not None and not outcome.stopped_transient

    result = durable.retry(attempt, attempts=attempts, accept=settled, on_retry=waiting)
    if not settled(result) and report is not None:
        remaining = result.remaining if result is not None else len(client.journal.pending())
        report.add(
            f"{remaining:,} upload(s) are still queued after waiting for the connection. "
            "Re-running resumes them; nothing needs to be reviewed again."
        )


def _run_units(folder, jobs, *, progress=None, on_complete=None, **kwargs):
    """Report durable unit completion while the existing bounded runner works.

    `on_complete` is forwarded untouched. It runs on the CALLING thread, not on
    this module's monitor thread and not in a worker -- the monitor only reads
    the ledger, which is a file, while `on_complete` writes to SQLite.
    """
    from threading import Event, Thread
    from . import backfill_run as runner

    kwargs["on_complete"] = on_complete
    if progress is None:
        return runner.run_units(folder, jobs, **kwargs)
    stopped = Event()
    file_counts = {unit.unit_id: unit.files for unit in jobs}

    def update():
        state = kwargs["ledger"].read()
        completed = sum(
            file_counts.get(record.unit.unit_id, 0)
            for record in state.units.values() if record.state is UnitState.DONE
        )
        progress("Reading reviewed files", completed=completed, total=sum(file_counts.values()))

    def monitor():
        while not stopped.wait(1):
            update()

    update()
    thread = Thread(target=monitor, daemon=True)
    thread.start()
    try:
        return runner.run_units(folder, jobs, **kwargs)
    finally:
        stopped.set()
        thread.join()
        update()


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
    background=False,
    back_to_selection=False,
    wandb_source=None,
    offer_wandb=True,
):
    from . import backfill_run as runner
    from . import telemetry as tm

    tel = telemetry or tm.null_context()
    start = started_at or time.monotonic()
    stats = {}
    recovery_lines = []
    outcome = tm.BackfillOutcome.CREDENTIALS_FAILED
    started = False
    registered_job = None
    try:
        with client_factory() as client:
            scope = Scope.resolve(client, project)
            outcome = tm.BackfillOutcome.PARTIAL
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
                started = True
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
                    tel=tel,
                    stats=stats,
                    background=background,
                    back_to_selection=back_to_selection,
                    wandb_source=wandb_source, offer_wandb=offer_wandb,
                )
                outcome = stats.pop("_outcome", None) or (
                    tm.BackfillOutcome.SUCCESS if complete else tm.BackfillOutcome.PARTIAL
                )
                deferred = stats.pop("_background_payload", None)
                if deferred is None:
                    return [*recovery_lines, *lines]
            # The worker may start immediately. Release the coverage writer
            # before dispatch so it can resume this exact approved source.
            from . import backfill, import_jobs_ui
            from .import_job_messages import enqueue_report

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
        from . import tui

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
        if not started:
            tel.emit(tm.EVENT_BACKFILL_STARTED, backfill_agent=agent.value, resumed=False)
        if summary_state is not None:
            summary_state["emitted"] = True
        tel.emit(
            tm.EVENT_BACKFILL_SUMMARY,
            outcome=outcome,
            duration_seconds=int(time.monotonic() - start),
            **{key: value for key, value in stats.items() if not key.startswith("_")},
        )


def _choose_source(candidates, *, interactive, yes):
    """Offer same-scope recovery hints without adopting a fingerprint match."""
    from . import tui

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


def _existing(client, workspace_id):
    """Bounded suggestion list. Missing names are resolved exactly before writes."""
    names = []
    cursor = None
    seen = set()
    for _ in range(10):
        page = client.list_projects(
            workspace_id=workspace_id, limit=200, **({"cursor": cursor} if cursor else {})
        )
        rows = page if isinstance(page, list) else page.items
        names.extend(row["slug"] for row in rows if row.get("slug"))
        cursor = getattr(page, "next_cursor", None)
        if not cursor or cursor in seen:
            break
        seen.add(cursor)
    return names


def _review(
    folder, records, *, agent, work_dir, existing, fixed_project, census, interactive, yes, git,
    tel, stats, classification_identity=None, background=False, progress=None, auto_approve=False,
):
    """The existing classification conversation, limited to the selected delta."""
    from . import backfill_run as runner
    from . import tui
    from . import telemetry as tm

    estimate = plans.estimate(records)
    tui.page([
        f"Sampling {len(records):,} selected files for classification.",
        *([f"Roughly {estimate.describe()}."] if estimate.describe() else []),
        "",
        "First, your agent reads the files to prepare an import plan.",
        ("Your automatic approval applies to this folder's plan. Delivery follows in the background."
         if auto_approve else "You'll review and approve it before importing."),
    ])
    ev = evidence.enrich(folder, records)
    context_options = {"background": background}
    if progress is not None:
        context_options.update(progress=progress, auto_approve=auto_approve)
    with (runner.classification_context(classification_identity, **context_options)
          if classification_identity else nullcontext()):
        plan, detail, session = runner.classify(
            folder, ev, agent=agent, existing=existing, work_dir=work_dir
        )
    if plan is None:
        raise _Stopped(
            tm.BackfillOutcome.NO_PLAN,
            "The classification did not produce a usable plan.",
            detail[-512:],
            "Re-running is safe; no files were queued from this classification.",
        )
    note = ""
    revisions = 0
    initial = True
    while True:
        assigned, discrepancy = plans.resolve(ev, plan)
        if fixed_project:
            assigned = dict.fromkeys(assigned, fixed_project)
        if initial:
            tel.emit(
                tm.EVENT_BACKFILL_PLAN_READY,
                projects_count=len(set(assigned.values())), trustworthy=discrepancy.trustworthy,
            )
            initial = False
        if not discrepancy.trustworthy:
            raise _Stopped(
                tm.BackfillOutcome.UNTRUSTED_CLASSIFICATION,
                "Classification cannot be trusted: " + "; ".join(discrepancy.describe())
            )
        body = runner.describe_plan(
            ev, plan, assigned, discrepancy
        )
        if git.evidence:
            body += [
                "",
                "GitHub context and Code sources for these files:",
                *[
                    f"  {item.repo} at {item.ref}, path {item.path_prefix or '/'} ({item.state})"
                    for item in git.evidence
                ],
                "Matching accessible repositories will appear in their reviewed projects' Code tabs.",
            ]
        if not interactive or yes:
            stats["revision_count"] = revisions
            return plan, assigned, ev, body
        decision = tui.review(
            "Review the import plan",
            ["Reading is complete. Approve this plan to start importing"
             + (" in the background." if background else "."),
             "", *runner.incomplete_lines(census), *body, *([note] if note else [])],
            [("Import files", "import"), ("Change the plan", "revise"),
             ("Cancel import", "cancel")],
        )
        if decision == "import":
            stats["revision_count"] = revisions
            return plan, assigned, ev, body
        if decision is tui.BACK or decision == "cancel":
            raise _BackToImport
        if decision != "revise":
            raise KeyboardInterrupt
        feedback = tui.text(
            "Change the import plan",
            ["Describe what to move, split, or rename. You'll review the revised plan before importing.",
             "Escape returns to the plan."],
            "What should change?",
        )
        if feedback is None:
            raise KeyboardInterrupt
        if feedback is tui.BACK or not feedback.strip():
            continue
        feedback = feedback.strip()
        revision_identity = hashlib.sha256(json.dumps(
            [classification_identity, asdict(plan), feedback], sort_keys=True,
        ).encode()).hexdigest() if classification_identity else None
        with (runner.classification_context(revision_identity, background=background)
              if revision_identity else nullcontext()):
            if evidence.needs_chunking(ev):
                revised, detail = runner.classify_chunked(
                    folder, ev, agent=agent, existing=existing, work_dir=work_dir, feedback=feedback
                )
            else:
                revised, detail, session = runner.revise(
                    folder, ev, feedback, agent=agent, session_id=session, work_dir=work_dir
                )
        if revised is None:
            note = f"Could not revise: {detail[-512:] or 'the agent failed'}. The plan is unchanged."
            continue
        _, revised_disc = plans.resolve(ev, revised)
        if not revised_disc.trustworthy:
            note = (
                "The revised plan was discarded: " + "; ".join(revised_disc.describe())
                + ". The plan is unchanged."
            )
            continue
        plan, note = revised, ""
        revisions += 1


def _finish_approved_request(coverage, client, ledger) -> list[str]:
    """Resume project resolution from the saved reviewed proposal, without a model."""
    from ..sdk import errors
    from . import telemetry as tm

    request = coverage.meta("approved_request")
    if not request:
        return []
    rows = {row["path"]: row for row in coverage.rows()}
    drift = [
        path
        for path, digest in request["hashes"].items()
        if path not in rows or rows[path]["observed_hash"] != digest or not rows[path]["present"]
    ]
    if drift:
        raise CoverageError(
            f"{len(drift)} reviewed files changed before project resolution; review this delta again."
        )
    destinations = {}
    specs = {spec["slug"]: spec for spec in request["projects"]}
    for slug in sorted(set(request["assigned"].values())):
        try:
            project = client.resolve_project(slug, strict=True)
            if project is None:
                spec = specs.get(slug, {})
                try:
                    project = client.create_project(
                        slug,
                        spec.get("name") or slug,
                        kind="general",
                        # The spec file may carry a name a person wrote, but the
                        # `or slug` fallback means this cannot tell which -- and
                        # composing a name out of a file is what `authorship.py`
                        # calls a template. Pinned `agent` so an import from a
                        # bare terminal leaves it enhanceable instead of locking
                        # a slug; guessing `human` here is the unrecoverable
                        # direction.
                        authored_by=agent_session.AUTHORSHIP_AGENT,
                        description=spec.get("description") or None,
                        workspace_id=coverage.scope.workspace_id,
                    )
                except errors.ConflictError:
                    project = client.resolve_project(slug, strict=True)
                    if project is None:
                        raise
        except Exception as exc:
            raise _Stopped(
                tm.BackfillOutcome.PROJECT_CREATE_FAILED,
                f"Could not create every project: {slug}: {exc}",
                "The reviewed plan is saved. Re-running retries project resolution without reclassifying.",
                projects_failed=1,
            ) from exc
        destinations[slug] = project
    coverage.approve(
        {path: destinations[slug] for path, slug in request["assigned"].items()},
        changed=request["import_changed"],
    )
    approved_git = github.GitEvidenceBundle(
        [github.GitEvidence(**item) for item in request.get("git", [])]
    )
    _save_reviewed_sources(
        coverage,
        approved_git,
        request["folder"],
        {path: str(destinations[slug]["id"]) for path, slug in request["assigned"].items()},
    )
    units = [
        Unit(item["unit_id"], item["project"], tuple(item["paths"]), UnitKind(item["kind"]))
        for item in request["units"]
    ]
    bindings = coverage.meta("approved_units", {})
    for unit in units:
        bindings[unit.unit_id] = {
            "project_id": str(destinations[unit.project]["id"]),
            "hashes": {path: request["hashes"][path] for path in unit.paths},
        }
    coverage.put_meta("approved_units", bindings)
    known = ledger.read().units
    additional = [unit for unit in units if unit.unit_id not in known]
    if additional:
        ledger.record_plan(additional, sorted(destinations), append=True)
        ledger.record_approval()
    coverage.put_meta("approved_request", None)
    return list(destinations)


def _source_choice(item):
    return (
        item.repo.lower(),
        item.ref,
        item.path_prefix,
        item.start_sha,
        item.start_at,
        item.source_id,
    )


def _save_reviewed_sources(coverage, git, folder, assignments):
    reviewed = coverage.meta("reviewed_sources", {})
    for project_id in sorted(set(assignments.values())):
        subset = git.for_paths(
            [path for path, target in assignments.items() if target == project_id],
            folder=Path(folder),
        )
        subset.evidence.extend(
            item for item in git.evidence if item.project_id == project_id and not item.local_folder
        )
        previous = [github.GitEvidence(**item) for item in reviewed.get(project_id, [])]
        by_choice = {_source_choice(item): item for item in previous + subset.evidence}
        reviewed[project_id] = [asdict(item) for item in by_choice.values()]
    coverage.put_meta("reviewed_sources", reviewed)


def _census_progress(progress, label: str, *, phase="scanning"):
    """Report census work without treating file verification as delivery.

    The census is the longest silent stretch of a first import -- it reads
    every byte under the folder -- and it was reporting once, before it began.
    A bar that does not move for twenty minutes is indistinguishable from a
    hang, which is the one thing a long-running import must never look like.

    Reused files are named because they are the difference a repeat import
    actually feels: "1,154 of 1,154 · 1,154 already verified" says the pass is
    confirming rather than re-reading.
    Post-approval checks stay in the importing phase so they cannot reset
    verified upload completion or leave a finished job labeled as scanning.
    """
    if progress is None:
        return None

    def report(*, completed: int, total: int, reused: int) -> None:
        detail = f" · {reused:,} already verified" if reused else ""
        progress(f"{label} {completed:,} of {total:,}{detail}",
                 phase=phase, completed=completed, total=total,
                 stage=None, stage_completed=None, stage_total=None)

    return report


def _run(
    client,
    coverage,
    folder,
    *,
    agent,
    interactive,
    yes,
    concurrency,
    import_changed,
    import_unverified,
    tel,
    stats,
    retry_dead=False,
    background=False,
    progress=None,
    auto_approve=False,
    back_to_selection=False,
    wandb_source=None,
    offer_wandb=True,
):
    from . import backfill_run as runner
    from . import telemetry as tm
    from . import tui

    if wandb_source is not None and (not interactive or yes or auto_approve):
        raise CoverageError("Selected W&B history needs foreground review before file import.")
    report = runner.Report()
    stats["_report"] = report.lines
    degraded = runner.bf.degraded_note(agent)
    if degraded:
        report.add(degraded)
    # This marker only categorizes telemetry AFTER the fresh census and
    # receipt join succeed; it never authorizes a no-op or avoids rehashing.
    previously_complete = coverage.meta("last_verified_complete", False)
    with _phase(stats, "walk"):
        census, records, warn, _, _ = runner._index(folder, report)
    stats.update(files=census.files, bytes=census.bytes)
    tel.emit(
        tm.EVENT_BACKFILL_SCANNED,
        files=census.files, bytes=census.bytes,
        linked_dirs=len(census.linked_dirs), unreadable_dirs=len(census.unreadable_dirs),
    )
    if warn.root_unreadable:
        stats["_outcome"] = tm.BackfillOutcome.UNREADABLE_ROOT
        return report.lines + [f"{folder} could not be read; coverage was not advanced."], stats, False
    if not records:
        if not census.incomplete:
            # An actually empty folder is still a new observation: retain old
            # remote identities while marking their local paths absent.
            coverage.observe(folder, [])
            coverage.write_report()
        coverage.put_meta("last_verified_complete", False)
        stats["_outcome"] = (
            tm.BackfillOutcome.PARTIAL if census.incomplete else tm.BackfillOutcome.EMPTY_FOLDER
        )
        return [*report.lines, f"{folder}: no files to import."], stats, not census.incomplete
    report.add(f"{census.files:,} files found on disk in {folder}.")
    paths = [str(Path(record.path).relative_to(folder)) for record in records]
    tui.page(["Verifying current file contents against delivery receipts."])
    if progress is not None:
        progress("Verifying selected file contents", phase="scanning")
    with _phase(stats, "census"):
        coverage.observe(folder, paths,
                         progress=_census_progress(progress, "Verifying file contents"))
    stats.update(**{f"census_{key}": value
                    for key, value in (coverage.meta("last_census") or {}).items()
                    if key in ("hashed", "reused")})
    classification_identity = hashlib.sha256(json.dumps({
        "scope": asdict(coverage.scope), "source_id": coverage.source_id,
        "files": sorted((row["path"], row["observed_hash"])
                        for row in coverage.rows() if row["present"]),
    }, sort_keys=True).encode()).hexdigest()
    coverage.reconcile(client)
    blocked = legacy.reconcile(coverage, client, folder)
    if blocked:
        report.add(
            f"{len(blocked):,} legacy file(s) need reconciliation; old counts were not adopted."
        )
        write_text_atomic(
            coverage.directory / "legacy-reconciliation.json", json.dumps(blocked, indent=2)
        )
        report.add(f"Review: {coverage.directory / 'legacy-reconciliation.json'}")
    ledger = Ledger(coverage.directory / "units.jsonl")
    ledger.open_import(folder, files=census.files, bytes_=census.bytes)
    work_dir = coverage.directory / "manifests"
    work_dir.mkdir(exist_ok=True, mode=0o700)

    # A pending reviewed plan is independent of an old unit's upload recovery.
    if coverage.meta("approved_request") and import_changed:
        saved = coverage.meta("approved_request")
        current = {row["path"]: row for row in coverage.rows()}
        if any(
            current.get(path, {}).get("observed_hash") != digest
            for path, digest in saved["hashes"].items()
        ):
            coverage.put_meta("superseded_request", saved)
            coverage.put_meta("approved_request", None)
    if coverage.meta("approved_request"):
        report.add("Resuming the saved reviewed plan and its project resolution.")
    report.projects.extend(_finish_approved_request(coverage, client, ledger))
    project_ids = sorted({row["project_id"] for row in coverage.rows() if row["project_id"]})
    if coverage.scope.project_id and coverage.scope.project_id not in project_ids:
        project_ids.append(coverage.scope.project_id)
    git = github.collect_evidence(client, folder, records=records, project_ids=project_ids)
    write_text_atomic(work_dir / "github-context.txt", git.prompt_text)
    runner._git_note.cache_clear()
    report.add(*[f"GitHub context: {issue}" for issue in git.issues[:5]])
    if retry_dead:
        # Explicit retry requests a fresh review even if the last failed
        # attempt was saved immediately before retirement was interrupted.
        for record in ledger.read().exhausted():
            ledger.retire_unit(
                record.unit.unit_id,
                reason=f"{record.unit.unit_id}: {record.error or 'the unit did not finish'}",
            )
        _reconcile_dead_units(coverage, ledger)
        revived = coverage.clear_dead()
        if revived:
            report.add(
                f"{revived:,} file(s) that failed every attempt will be reviewed for import again."
            )
    known = coverage.report()
    new = set(known["new"]) - set(blocked)
    if import_unverified:
        report.add(
            "Previously unverified legacy paths will be reviewed for import; new artifact identities may be created."
        )
        new.update(blocked)
    changed = set(known["changed"])
    if changed and interactive and not yes and not import_changed:
        answer = tui.review(
            "Review changed files",
            [
                f"{len(changed)} files changed since their approved versions.",
                "Importing them may create new artifact identities alongside older versions.",
                *sorted(changed)[:10],
            ],
            [("Leave changed files pending", False), ("Review changed files for import", True)],
        )
        if answer is tui.BACK:
            raise _BackToImport
        if answer is None:
            raise KeyboardInterrupt
        import_changed = answer is True
    selected = new | (changed if import_changed else set())
    if selected:
        selected_records = [record for record, path in zip(records, paths) if path in selected]
        fixed = (
            client.get_project(coverage.scope.project_id)["slug"]
            if coverage.scope.project_id
            else None
        )
        plan, assigned, ev, body = _review(
            folder,
            selected_records,
            agent=agent,
            work_dir=work_dir,
            existing=_existing(client, coverage.scope.workspace_id),
            fixed_project=fixed,
            census=census,
            interactive=interactive,
            yes=yes,
            git=git,
            tel=tel,
            stats=stats,
            classification_identity=classification_identity,
            background=background,
            progress=progress,
            auto_approve=auto_approve,
        )
        # The review includes Code sources before attachment occurs.
        report.add(*body)
        units = plans.pack(ev, assigned) + plans.pack_tails(ev, assigned)
        hashes = {
            row["path"]: row["observed_hash"] for row in coverage.rows() if row["path"] in assigned
        }
        coverage.put_meta(
            "approved_request",
            {
                "assigned": assigned,
                "hashes": hashes,
                "projects": [asdict(spec) for spec in plan.projects],
                "units": [asdict(unit) for unit in units],
                "import_changed": import_changed,
                "git": [asdict(item) for item in git.evidence],
                "folder": str(folder),
            },
        )
        tel.emit(
            tm.EVENT_BACKFILL_APPROVED,
            revision_count=stats.get("revision_count", 0), units_total=len(units),
        )
        report.projects.extend(_finish_approved_request(coverage, client, ledger))

    # Persisted assignments, including resumed and receipt-only paths, are the
    # only inputs to attachment. They are never sent to transcript import.
    assigned_rows = coverage.rows()
    reviewed = coverage.meta("reviewed_sources", {})
    if (
        not selected
        and not reviewed
        and git.evidence
        and any(row["project_id"] for row in assigned_rows)
    ):
        proposal = [
            "Code sources proposed for the saved file assignments:",
            *[
                f"  {item.repo} at {item.ref}, path {item.path_prefix or '/'} ({item.state})"
                for item in git.evidence
            ],
        ]
        approved = yes
        if interactive and not yes:
            answer = tui.review(
                "Review Code sources", proposal,
                [("Attach these Code sources", True), ("Leave attachment pending", False)],
            )
            if answer is tui.BACK:
                raise _BackToImport
            if answer is None:
                raise KeyboardInterrupt
            approved = answer is True
        if approved:
            _save_reviewed_sources(
                coverage,
                git,
                folder,
                {row["path"]: row["project_id"] for row in assigned_rows if row["project_id"]},
            )
            reviewed = coverage.meta("reviewed_sources", {})
        else:
            report.add(*proposal, "Code-source attachment is pending review.")
    for project_id in sorted({row["project_id"] for row in assigned_rows if row["project_id"]}):
        scoped = git.for_paths(
            [row["path"] for row in assigned_rows if row["project_id"] == project_id], folder=folder
        )
        scoped.evidence.extend(
            item for item in git.evidence if item.project_id == project_id and not item.local_folder
        )
        allowed = {
            _source_choice(github.GitEvidence(**item)) for item in reviewed.get(project_id, [])
        }
        scoped.evidence = [item for item in scoped.evidence if _source_choice(item) in allowed]
        try:
            attachment_results = github.attach_reviewed_sources(client, project_id, scoped)
        except Exception as exc:
            report.add(
                f"Code-source attachment pending ({type(exc).__name__}); file delivery continues."
            )
            continue
        for result in attachment_results:
            if result["state"] not in {"attached", "reused"}:
                report.add(f"Code source {result['repo']}: {result['state']}; attachment pending.")

    while True:
        wandb_lines = wandb.run(
            client, coverage, interactive=interactive, yes=yes,
            offer=offer_wandb or wandb_source is not None,
            wandb_source=wandb_source,
            **({"back_to_selection": True} if back_to_selection else {}),
        )
        if wandb_lines is tui.BACK:
            raise _BackToImport
        if wandb_source is None or getattr(wandb_lines, "source_resolved", False):
            break
        answer = tui.review(
            "W&B import could not start",
            [line.removesuffix(" File delivery continues.") for line in wandb_lines]
            or ["The W&B destination needs review."],
            [("Retry W&B", "retry"), ("Continue with files", tui.SKIP), ("Back", tui.BACK)],
        )
        if answer is None:
            raise KeyboardInterrupt
        if answer is tui.BACK:
            raise _BackToImport
        if answer is tui.SKIP:
            break
    report.add(*wandb_lines)

    return _deliver_approved(
        client, coverage, folder, agent=agent, interactive=interactive, yes=yes,
        concurrency=concurrency, records=records, paths=paths, census=census,
        ledger=ledger, work_dir=work_dir, git=git, report=report, stats=stats,
        selected=selected, previously_complete=previously_complete,
        background=background,
    )


def _reconcile_dead_units(coverage, ledger, *, current=None):
    """Repair an interruption between ledger retirement and the file markers."""
    saved = ledger.read().units
    dead = [record for record in saved.values() if record.state is UnitState.DEAD]
    if not dead:
        return []
    if current is None:
        current = {row["path"]: row for row in coverage.rows()}
    bindings = coverage.meta("approved_units", {})
    # Appended plans supersede earlier bindings for the same approved bytes.
    # An explicit retry keeps its historical DEAD unit in the ledger, but that
    # unit must never mark the newly reviewed replacement's files dead again.
    owners = {}
    for unit_id in saved:
        binding = bindings.get(unit_id, {})
        for path, digest in binding.get("hashes", {}).items():
            row = current.get(path, {})
            if row.get("project_id") == binding.get("project_id") and row.get("approved_hash") == digest:
                owners[path] = unit_id
    repaired = []
    for record in dead:
        paths = [path for path in record.unit.paths if owners.get(path) == record.unit.unit_id]
        if paths:
            repaired.extend(coverage.mark_dead(
                paths, record.error or f"{record.unit.unit_id}: agent attempt limit reached",
            ))
    return repaired


def _deliver_approved(
    client, coverage, folder, *, agent, interactive, yes, concurrency, records, paths,
    census, ledger, work_dir, git, report, stats, selected, previously_complete, progress=None,
    background=False,
    retry_network=False,
    completion_targets=None,
):
    """Execute saved file assignments; this half contains no plan or source picker."""
    from threading import Lock

    from . import backfill_run as runner
    from . import telemetry as tm

    current = {row["path"]: row for row in coverage.rows()}
    retired = _reconcile_dead_units(coverage, ledger, current=current)
    bindings = coverage.meta("approved_units", {})
    saved_units = ledger.read().units
    bound_paths = {
        path
        for unit_id, binding in bindings.items()
        if unit_id in saved_units
        for path, digest in binding["hashes"].items()
        if path in current
        and current[path]["project_id"] == binding["project_id"]
        and current[path]["approved_hash"] == digest
    }
    # Pre-binding scoped state can contain an approved destination but no proof
    # of the bytes an old model manifest described. Regenerate only those units;
    # never reuse an unbound manifest or repeat project classification.
    unbound = {
        row["path"]: row["project_slug"]
        for row in current.values()
        if row["path"] not in bound_paths
        and row["approved_hash"]
        and not row["manifest"]
        and row["present"]
        and row["approved_hash"] == row["observed_hash"]
    }
    unsampled = evidence.Evidence(
        root=str(folder),
        files=[record for record, path in zip(records, paths) if path in unbound],
        clusters=[],
        sampled_files=0,
        sampled_bytes=0,
    )
    replacements = plans.pack(unsampled, unbound) + plans.pack_tails(unsampled, unbound)
    for unit in replacements:
        bindings[unit.unit_id] = {
            "project_id": current[unit.paths[0]]["project_id"],
            "hashes": {path: current[path]["approved_hash"] for path in unit.paths},
        }
    if replacements:
        coverage.put_meta("approved_units", bindings)
        ledger.record_plan(
            replacements, sorted({unit.project for unit in replacements}), append=True
        )
        ledger.record_approval()
    if background:
        stats["_background_payload"] = _background_payload(
            coverage, client, folder, agent, concurrency, records, census
        )
        return report.lines, stats, False
    targets = set(completion_targets or ())
    if progress and completion_targets is None:
        targets = {
            row["path"] for row in current.values()
            if row["approved_hash"] and row["project_id"] and row["present"]
            and row["approved_hash"] == row["observed_hash"] and not row["observation_error"]
        }
    completed_paths = targets & _completed_paths(coverage) if progress else set()
    connection_failure = None
    progress_lock = Lock()

    def report_progress(message, **fields):
        # Unit monitoring runs on a helper thread. Read SQLite only on this
        # delivery thread; preparation reports reuse the verified receipt set.
        if progress:
            # Keep sampling and publication ordered together. Otherwise a
            # delayed monitor callback can overwrite a newer receipt count or
            # clear an outage reported by the delivery thread.
            with progress_lock:
                if connection_failure is not None:
                    fields["waiting_for_connection"] = True
                progress(
                    message, **fields,
                    completion_completed=len(completed_paths), completion_total=len(targets),
                )

    correlations = {}

    def track_deliveries(paths=None):
        if not progress:
            return
        rows = coverage.rows() if paths is None else coverage.rows_for(paths).values()
        correlations.update({
            row["correlation"]: row["path"] for row in rows
            if row["path"] in targets and row["correlation"] and row["present"]
            and row["approved_hash"] == row["observed_hash"] and not row["observation_error"]
        })

    def on_delivered(correlation):
        path = correlations.get(correlation)
        if path is None:
            return  # A shared outbox can also contain unrelated writes.
        coverage.accept_receipt(correlation, client.delivery_state(correlation))
        completed_paths.add(path)
        report_progress(
            "Uploading reviewed files", completed=len(completed_paths), total=len(targets),
        )

    jobs, sessions = [], {}
    claimed_paths = set()
    for record in ledger.read().units.values():
        if record.state is UnitState.DEAD:
            # Retiring a unit has to take it out of THIS loop, not just
            # out of `outstanding()`. Without it a retired unit is
            # re-planned on the next run, fails, is retired again, and
            # the import reports itself complete while quietly re-running
            # the same broken work forever.
            continue
        binding = bindings.get(record.unit.unit_id, {})
        pending = tuple(
            path
            for path in record.unit.paths
            if path in current
            and path not in claimed_paths
            and current[path]["project_id"] == binding.get("project_id")
            and current[path]["approved_hash"] == binding.get("hashes", {}).get(path)
            and current[path]["present"]
            and not current[path]["manifest"]
            and current[path]["approved_hash"] == current[path]["observed_hash"]
        )
        if not pending:
            continue
        manifest = work_dir / f"{record.unit.unit_id}.jsonl"
        if manifest.exists():
            recovery = runner.UnitOutcome(
                Unit(record.unit.unit_id, record.unit.project, pending, record.unit.kind),
                ok=False,
                manifest=manifest,
            )
            touched, _ = delivery.ingest_manifests(coverage, folder, [recovery])
            # Just this unit's rows. Re-reading the whole file table here made
            # a resume O(units x files): 500 units over a 200,000-file drive
            # built a hundred million dict entries to look at four hundred.
            current.update(coverage.rows_for(touched or pending))
            pending = tuple(path for path in pending if not current[path]["manifest"])
        if record.exhausted:
            # A crash or a failed flush can leave the last failed attempt
            # unretired. Recover any manifest above, but never spend another
            # agent attempt before the explicit --retry-dead review path.
            reason = f"{record.unit.unit_id}: {record.error or 'the unit did not finish'}"
            ledger.retire_unit(record.unit.unit_id, reason=reason)
            retired.extend(coverage.mark_dead(record.unit.paths, reason))
            continue
        if pending:
            claimed_paths.update(pending)
            jobs.append(Unit(record.unit.unit_id, record.unit.project, pending, record.unit.kind))
            if record.session_id:
                sessions[record.unit.unit_id] = record.session_id
    if jobs and not selected:
        report.add(f"Resuming {len(jobs)} unit(s) from their saved file assignments.")

    problems: list[str] = []
    delivered_units = 0

    def deliver_finished_unit(outcome) -> None:
        """Queue one unit's files the moment its manifest exists.

        ON THE MAIN THREAD. `run_units` hands outcomes back here as they
        complete rather than calling this from the worker, because the coverage
        connection is a plain `sqlite3.connect` -- `check_same_thread` is left
        at its default on purpose -- and a helper thread writing to it raises.

        Doing it here instead of after the last unit is the whole point: the
        drain has nothing to do until the final agent finishes, so on a real
        drive the upload used to be appended to the import rather than hidden
        inside it.
        """
        nonlocal delivered_units, connection_failure
        touched, errors = delivery.ingest_manifests(coverage, folder, [outcome])
        problems.extend(errors)
        if not touched:
            return
        _, failures = delivery.enqueue(coverage, client, folder, paths=touched)
        delivered_units += 1
        for failure in failures:
            problems.append(f"{outcome.unit.unit_id}: {failure}")
            if progress:
                report_progress(f"Unit {outcome.unit.unit_id}: {failure}")
        if retry_network and connection_failure is None:
            from .import_jobs import is_retryable_error

            # Background clients deliberately have no detached drainer. Drain
            # this finished unit here while the remaining agent futures keep
            # reading. Receipt callbacks stay on this SQLite-owning thread.
            track_deliveries(touched)
            completed_paths.update(targets & coverage.delivered_paths(touched))
            try:
                _flush_uploads(
                    client, retry_network=True, report=report, progress=progress,
                    on_delivered=on_delivered if progress else None,
                )
            except Exception as exc:
                if not is_retryable_error(exc):
                    raise
                # Let in-flight reads save their manifests before the supervisor
                # retries. Raising out of on_complete would leave those futures
                # racing the next attempt over the same unit checkpoints.
                with progress_lock:
                    connection_failure = exc
                if progress:
                    report_progress(
                        "Upload connection unavailable; continuing approved local reads."
                    )

    with _phase(stats, "units"):
        outcomes = _run_units(
            folder,
            jobs,
            agent=agent,
            ledger=ledger,
            work_dir=work_dir,
            concurrency=concurrency,
            sessions=sessions,
            sizes={path: row["size"] for path, row in current.items()},
            progress=report_progress if progress else None,
            on_complete=deliver_finished_unit,
        )
    stats.update(
        units_total=len(jobs), units_done=sum(outcome.ok for outcome in outcomes),
        failed_units=sum(not outcome.ok for outcome in outcomes),
    )
    if stats["failed_units"]:
        report.add(f"{stats['failed_units']} unit(s) did not finish. Re-running resumes saved work.")

    # Retire before delivery can raise or wait for the connection. A resume
    # retains valid manifests and receipts without resetting the attempt cap.
    for record in ledger.read().exhausted():
        reason = f"{record.unit.unit_id}: {record.error or 'the unit did not finish'}"
        ledger.retire_unit(record.unit.unit_id, reason=reason)
        retired.extend(coverage.mark_dead(record.unit.paths, reason))

    # Anything the per-unit pass could not take -- a unit whose manifest was
    # already on disk from a previous run, a row that lost a race with staging
    # pressure -- plus a sweep for the whole folder, so a partial per-unit pass
    # can never be the last word.
    if progress:
        report_progress("Uploading reviewed files", completed=0, total=len(current))
    with _phase(stats, "deliver"):
        _, errors = delivery.enqueue(coverage, client, folder)
        problems.extend(errors)
        coverage.reconcile(client)
    # Counted from the store, not summed across calls. Delivery now runs once
    # per unit and then sweeps, so an op the unit pass queued is offered to the
    # sweep again -- resuming it is a harmless nudge, but adding both returns
    # would report more files handed to the outbox than the folder holds.
    enqueued = len(coverage.report()["queued"])

    # BEFORE the flush. A background job whose flush hits a transient network
    # error raises RetryableJobError out of this function to be re-queued, and
    # anything added to the report after that point is never reached -- so real
    # manifest and enqueue problems would be replaced, run after run, by a
    # silent whole-import retry.
    report.add(*problems[:5])
    if len(problems) > 5:
        report.add(f"... and {len(problems) - 5:,} more; see the per-file report.")

    if progress:
        completed_paths = targets & _completed_paths(coverage)
        report_progress("Uploading reviewed files", completed=0, total=len(current))
        track_deliveries()

    if connection_failure is not None:
        raise connection_failure
    with _phase(stats, "flush"):
        _flush_uploads(client, retry_network=retry_network, report=report,
                       progress=progress, on_delivered=on_delivered if progress else None)
        coverage.reconcile(client)

    # A failed agent can still leave valid manifest rows. Only the files
    # without receipts after draining remain given up on.
    retired_count = len(set(retired) & set(coverage.report()["dead"])) if retired else 0
    if retired_count:
        report.add(
            f"{retired_count:,} file(s) in {len(ledger.read().dead()):,} unit(s) failed "
            f"{ledger_mod.MAX_UNIT_ATTEMPTS} attempts and were not imported. "
            "Re-run with `--retry-dead` to plan them again."
        )

    # Live per-file upload progress, from main: one exact receipt validation
    # per file after its durable commit, rather than re-scanning every pending
    # receipt (which would make delivery O(N^2)).
    # Rewalk as well as rehash: a file added during a long resumed import is an
    # unreviewed delta in THIS result, even if every original path has a receipt.
    final_warn = evidence.WalkWarnings()
    with _phase(stats, "rewalk"):
        final_records = list(evidence.walk(folder, final_warn))
        final_paths = [str(Path(record.path).relative_to(folder)) for record in final_records]
        coverage.observe(
            folder, final_paths,
            progress=_census_progress(report_progress if progress else None,
                                      "Re-checking file contents", phase="importing"),
        )
        coverage.reconcile(client)
    for key, value in (coverage.meta("last_census") or {}).items():
        if key in ("hashed", "reused"):
            stats[f"census_{key}"] = stats.get(f"census_{key}", 0) + value
    try:
        client.compact_delivery_receipts(max_records=256, max_seconds=0.25)
    except Exception as exc:
        report.add(
            f"Receipt maintenance deferred ({type(exc).__name__}); delivery identities are retained."
        )
    incomplete = bool(
        census.linked_dirs
        or census.unreadable_dirs
        or final_warn.linked
        or final_warn.unreadable
        or final_warn.root_unreadable
        or any(not outcome.ok for outcome in outcomes)
    )
    report.add(*delivery.lines(coverage, incomplete_walk=incomplete))
    report.add(*wandb.run(client, coverage))
    known = coverage.report()
    pending = any(known[key] for key in ("new", "changed", "queued", "unresolved"))
    # `dead` is deliberately NOT pending: those files will not be picked up by
    # re-running, so counting them would leave the import reporting "partial,
    # re-run" forever about work it has already given up on. They are reported
    # in their own line, and `--retry-dead` is what brings them back.
    complete = not pending and not incomplete and not known.partial
    coverage.put_meta("last_verified_complete", complete)
    if complete and known["delivered"]:
        from .backfill_reconstruction import complete_reconstruction

        report.add(
            *complete_reconstruction(
                client, folder, coverage, git, agent=agent, interactive=interactive, yes=yes
            )
        )
    final_count = len(final_records)
    stats.update(
        files=final_count,
        enqueued=enqueued,
        coverage_pct=round(100 * len(known["delivered"]) / final_count, 1) if final_count else None,
    )
    if complete and previously_complete and not selected and not jobs and not enqueued:
        stats["_outcome"] = tm.BackfillOutcome.ALREADY_IMPORTED
        report.add("The current file versions were already imported; their receipts were verified again.")
    return (
        report.lines,
        stats,
        complete,
    )
