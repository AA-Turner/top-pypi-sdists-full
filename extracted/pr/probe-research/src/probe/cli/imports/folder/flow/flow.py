"""Folder orchestration: authenticated scope, reviewed bytes, verified receipts."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from .....foundation.durable.durable import write_text_atomic
from probe.cli.imports.folder import evidence as evidence
from ..sources import github as github
from ..upload import legacy as legacy
from ..classify import plan as plans
from ..structure import projects as projects_mod
from .. import structure as structure
from ..sources import wandb as wandb
from ..coverage.coverage import CoverageError
from ..coverage.observe import skipped_folders
from ..upload.ledger import Ledger, UnitState


class _Stopped(CoverageError):
    """An expected workflow stop with a closed telemetry outcome."""

    def __init__(self, outcome, *lines, **stats):
        super().__init__("\n".join(lines))
        self.outcome, self.lines, self.stats = outcome, list(lines), stats


class _BackToImport(KeyboardInterrupt):
    """A pre-delivery form returned to the folder import choices."""


def _skip_counts(census) -> dict[str, int]:
    """`backfill.scanned`'s skip counts. Numbers only: folder names are paths."""
    return {
        "skipped_hidden_dirs": len(census.skipped_hidden),
        "skipped_hidden_files": census.skipped_hidden_files,
        "skipped_worktrees": len(census.skipped_worktrees),
        "skipped_worktree_files": census.skipped_worktree_files,
    }


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
    review_excluded=False,
    background=False,
    progress=None,
    auto_approve=False,
    back_to_selection=False,
    wandb_source=None,
    offer_wandb=True,
    agents=None,
    include_hidden=(),
):
    from .... import backfill_run as runner
    from ... import jobs as import_jobs
    from probe import analytics as tm
    from ....wizard import terminal as tui

    if wandb_source is not None and (not interactive or yes or auto_approve):
        raise CoverageError("Selected W&B history needs foreground review before file import.")
    report = runner.Report()
    stats["_report"] = report.lines
    degraded = runner.bf.degraded_note(agent, agents.flags() if agents is not None else ())
    if degraded:
        report.add(degraded)
    if agents is not None:
        report.add(*agents.notes)
    # This marker only categorizes telemetry AFTER the fresh census and
    # receipt join succeed; it never authorizes a no-op or avoids rehashing.
    previously_complete = coverage.meta("last_verified_complete", False)
    report.add(*runner.refused_includes(include_hidden))
    with _phase(stats, "walk"):
        census, records, warn, _, _ = runner._index(folder, report, include_hidden=include_hidden)
    stats.update(files=census.files, bytes=census.bytes)
    tel.emit(
        tm.EVENT_BACKFILL_SCANNED,
        files=census.files, bytes=census.bytes,
        linked_dirs=len(census.linked_dirs), unreadable_dirs=len(census.unreadable_dirs),
        **_skip_counts(census),
    )
    # The desktop's view of a background import: a no-op in a foreground run,
    # and never a reason for the import to stop.
    try:
        import_jobs.remember_skipped(census.skipped_json())
    except (import_jobs.JobError, OSError):
        pass
    if warn.root_unreadable:
        stats["_outcome"] = tm.BackfillOutcome.UNREADABLE_ROOT
        return report.lines + [f"{folder} could not be read; coverage was not advanced."], stats, False
    if not records:
        if not census.incomplete:
            # An actually empty folder is still a new observation: retain old
            # remote identities while marking their local paths absent.
            coverage.observe(folder, [], skipped=skipped_folders(
                census, root_name=Path(folder).resolve().name))
            coverage.write_report()
            known = coverage.report()
            stats.update(absent_files=len(known["vanished"]),
                         absent_skipped_files=len(coverage.skipped_rules(on_disk=False)),
                         skipped_by_rule_files=len(known["skipped"]))
        coverage.put_meta("last_verified_complete", False)
        stats["_outcome"] = (
            tm.BackfillOutcome.PARTIAL if census.incomplete else tm.BackfillOutcome.EMPTY_FOLDER
        )
        return [*report.lines, f"{folder}: no files to import."], stats, not census.incomplete
    skipped = census.skipped_hidden_files + census.skipped_worktree_files
    report.add(f"{census.files:,} files found on disk in {folder}"
               + (f", and {skipped:,} more skipped (listed above)." if skipped else "."))
    paths = [str(Path(record.path).relative_to(folder)) for record in records]
    tui.page(["Verifying current file contents against delivery receipts."])
    if progress is not None:
        progress("Verifying selected file contents", phase="scanning")
    with _phase(stats, "census"):
        coverage.observe(folder, paths,
                         progress=_census_progress(progress, "Verifying file contents"),
                         skipped=skipped_folders(census, root_name=Path(folder).resolve().name))
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
    if review_excluded:
        reopened = coverage.clear_exclusions()
        if reopened:
            report.add(f"{reopened:,} file(s) left out as not research will be classified again.")
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
    # Files delivered before this folder's plans named experiments and runs are
    # organized once: classified with the rest, kept in their project, moved
    # (never re-uploaded) into the runs and experiments the plan names.
    imported = structure.restructure_candidates(coverage)
    imported = {path: slug for path, slug in imported.items() if path not in selected}
    if imported and interactive and not yes:
        answer = tui.review(
            "Organize imported files",
            [f"{len(imported):,} files were imported before experiments and runs could be.",
             "Your agent reads them again to name their experiments and runs; you review the "
             "plan first. They stay in their projects and are not uploaded again."],
            [("Organize them into experiments and runs", True), ("Leave them as they are", False)],
        )
        if answer is tui.BACK:
            raise _BackToImport
        if answer is None:
            raise KeyboardInterrupt
        if answer is not True:
            structure.decline(coverage)
            imported = {}
    reviewed_plan = None
    if selected or imported:
        selected_records = [record for record, path in zip(records, paths)
                            if path in selected or path in imported]
        fixed = (
            client.get_project(coverage.scope.project_id)["slug"]
            if coverage.scope.project_id
            else None
        )
        try:
            reviewed_plan = _review(
                folder,
                selected_records,
                agent=agent,
                work_dir=work_dir,
                known=projects_mod.load(client, coverage, folder),
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
                agents=agents,
                imported=imported,
                plan_file=coverage.directory / "plan.json",
            )
        except _Stopped as exc:
            # Organizing files imported before is a bonus on a re-import with
            # nothing new: its classification failing must not fail the import.
            if selected or exc.outcome != tm.BackfillOutcome.NO_PLAN:
                raise
            report.add("The imported files could not be organized into experiments and runs "
                       "this time; re-running tries again.", *exc.lines[1:2])
            reviewed_plan = None
    if reviewed_plan is not None:
        plan, assigned, ev, body = reviewed_plan
        # The review includes Code sources before attachment occurs.
        report.add(*body)
        resolved = structure.resolve(plan, assigned, fixed_project=fixed)
        # Imported files are organized, never re-approved or re-uploaded.
        assigned = {path: slug for path, slug in assigned.items() if path not in imported}
        units = plans.pack(ev, assigned) + plans.pack_tails(ev, assigned)
        # Settled as `excluded` rather than left `new` (re-classified every run).
        # Hashed SEPARATELY: an edit to product code before project resolution
        # must not block the research files' drift check below.
        left_out: dict[str, str] = {}
        plans.resolve(ev, plan, left_out=left_out)
        observed = {row["path"]: row["observed_hash"] for row in coverage.rows()}
        hashes = {path: observed[path] for path in assigned if path in observed}
        coverage.put_meta(
            "approved_request",
            {
                "assigned": assigned,
                "left_out": left_out,
                "left_out_hashes": {path: observed[path] for path in left_out if path in observed},
                "hashes": hashes,
                "projects": [asdict(spec) for spec in plan.projects],
                "units": [asdict(unit) for unit in units],
                "import_changed": import_changed,
                "git": [asdict(item) for item in git.evidence],
                "folder": str(folder),
                # Copy-like mtimes are judged over the WHOLE folder's walk: this
                # plan's files alone (one new run, say) are often one burst.
                "structure": resolved.planned(times=not evidence.Evidence(
                    root=str(folder), files=records, clusters=[], sampled_files=0,
                    sampled_bytes=0).mtime_uninformative),
                # Files imported before that this plan organizes (never re-approved).
                "imported": sorted(imported),
            },
        )
        stats.update(experiments_approved=len(resolved.experiments),
                     runs_approved=len(resolved.runs))
        tel.emit(
            tm.EVENT_BACKFILL_APPROVED,
            revision_count=stats.get("revision_count", 0), units_total=len(units),
            experiments_approved=len(resolved.experiments), runs_approved=len(resolved.runs),
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
        background=background, agents=agents,
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
from probe.cli.imports.folder.flow.deliver import _deliver_approved, _phase  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.flow.review import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _finish_approved_request,
    _review,
    _save_reviewed_sources,
    _source_choice,
)
