"""the reviewed import as a background job: its immutable payload, and resuming only the reviewed file versions."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import shlex
from probe.cli.imports.folder import evidence as evidence
from ..sources import github as github
from ..coverage.coverage import Coverage, CoverageError
from ..coverage.scope import Scope
from ..coverage.observe import skipped_folders
from ..upload.ledger import Ledger


BACKGROUND_SCHEMA = "probe.folder-import-job/1"


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
    from .....sdk.client.client import Client
    from .....sdk.settings.settings import resolve

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


def run_background_job(payload, *, progress, meter=None):
    """Resume only the reviewed file versions captured by a queued folder job.

    `meter` is the worker attempt's (`import_jobs.run_worker`), so its
    `import_job.finished` carries what this job's agents cost and under which
    settings, read here once per attempt (`import_agent_settings.resolve`)."""
    from ... import folder as bf
    from .... import backfill_run as runner
    from ... import agent_settings as import_agent_settings, jobs as import_jobs
    from ...jobs.errors import RetryableJobError, UnitRetryJobError, is_retryable_error

    if payload.get("schema") == AUTO_BACKGROUND_SCHEMA:
        return _run_auto_import(payload, progress=progress, meter=meter)
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
            agents = import_agent_settings.resolve(client, bf.Agent(payload["agent"]), meter=meter)
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
                census = bf.Census(**payload["census"])
                coverage.observe(
                    folder, paths,
                    progress=_census_progress(progress, "Verifying approved file contents", phase="importing"),
                    skipped=skipped_folders(census, root_name=Path(folder).resolve().name),
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
                # The reviewed plan said what was skipped; this job's own report
                # and record say it again, because they are what the desktop reads.
                report.add(*runner.skipped_lines(census))
                try:
                    import_jobs.remember_skipped(census.skipped_json())
                except (import_jobs.JobError, OSError):
                    pass
                lines, _, _ = _deliver_approved(
                    client, coverage, folder, agent=bf.Agent(payload["agent"]),
                    interactive=False, yes=False, concurrency=payload["concurrency"],
                    records=records, paths=paths, census=census,
                    ledger=ledger, work_dir=directory / "manifests",
                    git=git, report=report, stats=stats, selected=set(),
                    previously_complete=coverage.meta("last_verified_complete", False),
                    progress=progress,
                    retry_network=True,
                    completion_targets=targets,
                    agents=agents,
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
                    # Only batches that ran THIS pass and failed with tries left:
                    # a failed batch whose files changed since approval is not
                    # run again, so it would never reach its attempt limit.
                    retry = stats.get("_retry_units") or []
                    if retry:
                        # An agent that stopped mid-batch is retried by the job
                        # itself, up to the batch's attempt limit, instead of
                        # leaving the import for someone to resume by hand.
                        raise UnitRetryJobError(
                            f"{len(retry)} import batch(es) stopped before finishing; "
                            "retrying them with their saved progress."
                        )
                    raise CoverageError(
                        f"{len(remaining)} approved file(s) remain unfinished. "
                        "Saved progress is retained; resume from Existing imports. "
                        "Changed files require another review."
                    )
                return lines
    except (CoverageError, UnitRetryJobError):
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
from probe.cli.imports.folder.flow.auto_import import AUTO_BACKGROUND_SCHEMA, _run_auto_import  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.flow.deliver import _deliver_approved  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.flow.flow import _census_progress  # noqa: E402 -- pieces need each other; the front door loads this one first
