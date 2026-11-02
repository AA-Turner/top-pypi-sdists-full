"""the automatic folder import: pin an explicit folder-scoped approval before any scan, then prepare and deliver."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import uuid

from .....foundation.durable.durable import file_lock, fsync_directory, write_text_atomic
from ..sources import wandb as wandb
from ..coverage.coverage import Coverage, CoverageError
from ..coverage.scope import Scope
AUTO_BACKGROUND_SCHEMA = "probe.folder-auto-import-job/1"


def enqueue_auto_import(
    *, client_factory, folder, agent, auto_approve, project=None, concurrency=None,
    source_id=None, import_changed=False, import_unverified=False, retry_dead=False,
    review_excluded=False, wandb_approval=None, request_id=None,
):
    """Persist an explicit folder-scoped automatic approval before any scan."""
    from ... import jobs as import_jobs
    from .... import backfill_run as runner

    if auto_approve is not True:
        raise CoverageError("Automatic folder imports require explicit approval.")
    if request_id is not None:
        try:
            request_id = uuid.UUID(request_id).hex
        except (ValueError, TypeError, AttributeError) as exc:
            raise CoverageError("The automatic import request identity is invalid.") from exc
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
            "review_excluded": bool(review_excluded),
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
            payload={**intent, "request_id": request_id or uuid.uuid4().hex},
            label=f"Folder · {folder.name}",
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


def _run_auto_import(payload, *, progress, meter=None):
    """Prepare once, durably pin the resulting approval, then deliver in this job."""
    from ... import folder as bf, agent_settings as import_agent_settings, jobs as import_jobs
    from probe import analytics as telemetry

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
            agents = import_agent_settings.resolve(client, bf.Agent(payload["agent"]), meter=meter)
            meter = agents.meter
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
                        review_excluded=bool(payload.get("review_excluded")),
                        tel=telemetry.null_context(), stats=stats, background=True,
                        progress=progress, auto_approve=True, agents=agents,
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
        return [*history_lines, *run_background_job(prepared, progress=progress, meter=meter)]
    except Exception as exc:
        if isinstance(exc, import_jobs.UnitRetryJobError):
            raise
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
from probe.cli.imports.folder.flow.background_job import BACKGROUND_SCHEMA, _background_client, run_background_job  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.flow.flow import _run  # noqa: E402 -- pieces need each other; the front door loads this one first
