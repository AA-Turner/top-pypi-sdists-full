"""the review conversation over the selected delta, and finishing an approved request from its saved proposal."""

from __future__ import annotations

from dataclasses import asdict
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path

from .....foundation.durable.durable import write_text_atomic
from probe.cli.imports.folder import evidence as evidence
from ..sources import github as github
from .....sdk import agent_session
from ..classify import plan as plans
from ..structure import projects as projects_mod
from .. import structure as structure
from ..coverage.coverage import CoverageError
from ..upload.ledger import Unit, UnitKind


def _review(
    folder, records, *, agent, work_dir, known, fixed_project, census, interactive, yes, git,
    tel, stats, classification_identity=None, background=False, progress=None, auto_approve=False,
    agents=None, imported=None, plan_file=None,
):
    """The existing classification conversation, limited to the selected delta.

    `imported` (path -> project slug) are files delivered before this folder's
    plans named experiments and runs: classified again so they can be
    organized, never re-assigned or re-uploaded. `plan_file` receives the plan
    as JSON (`backfill_structure.plan_json`) each time it is shown.

    `known` is the workspace's projects (`backfill_projects.load`). Every plan
    is settled against it before it is shown: new projects by default, this
    folder's own ones reused, and one the classifier chose to reuse marked
    EXISTING -- or, when nobody reviews this plan, given a new project."""
    from .... import backfill_run as runner
    from ....wizard import terminal as tui
    from probe import analytics as tm

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
            folder, ev, agent=agent, existing=known.others, work_dir=work_dir, agents=agents,
            fixed=imported or None, own=list(known.own.values()),
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
    attended = interactive and not yes

    def settle(plan):
        if fixed_project:
            # Pointed at one project: every file goes there, whatever was named.
            own = known.own.get(fixed_project)
            if own is not None:
                plan.projects = [own]
            return projects_mod.Settled()
        settled = projects_mod.settle(plan, known, attended=attended, folder=Path(folder))
        projects_mod.fill_counts(plan, known)
        return settled

    while True:
        settled = settle(plan)
        left_out: dict[str, str] = {}
        assigned, discrepancy = plans.resolve(ev, plan, left_out=left_out)
        if fixed_project:
            assigned = dict.fromkeys(assigned, fixed_project)
        resolved = structure.resolve(plan, assigned, fixed_project=fixed_project)
        if plan_file is not None:
            write_text_atomic(plan_file, json.dumps(structure.plan_json(
                assigned, resolved, left_out=len(left_out),
                fixed=sum(1 for path in (imported or {}) if path in assigned),
                skipped=census.skipped_json(), projects=plan.projects), indent=2))
        if initial:
            # The plan is built from validated selections, so `trustworthy` is
            # an invariant on OUR code; a false one is reported here and the
            # plan goes on with `resolve`'s map, never refused whole (a 52-minute
            # classification was thrown away over two typos on 2026-10-25).
            stats.update(plan.stats)
            stats["unclassified_files"] = len(plan.excluded)
            # Metadata only: how many projects are new, reused by code's rule,
            # or reused because the classifier chose them (and how many such
            # choices became new projects because nobody reviews this plan).
            project_counts = {**projects_mod.counts(plan, assigned),
                              "projects_reuse_declined": settled.declined}
            stats.update(project_counts)
            tel.emit(
                tm.EVENT_BACKFILL_PLAN_READY,
                projects_count=len(set(assigned.values())), trustworthy=discrepancy.trustworthy,
                left_out_files=len(left_out), experiments_proposed=len(resolved.experiments),
                runs_proposed=len(resolved.runs), already_imported_files=len(imported or {}),
                **project_counts, **plan.stats,
            )
            initial = False
        stats.update(experiments_proposed=len(resolved.experiments),
                     runs_proposed=len(resolved.runs))
        body = runner.describe_plan(
            ev, plan, assigned, discrepancy, left_out=left_out, structure=resolved
        )
        if settled.notes:
            body += ["", *settled.notes]
        if plan_file is not None:
            body += ["", f"Plan as JSON: {plan_file}"]
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
             "", *runner.incomplete_lines(census), *runner.skipped_lines(census), *body,
             *([note] if note else [])],
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
            revised, detail, session = runner.revise(
                folder, ev, feedback, agent=agent, session_id=session, work_dir=work_dir,
                plan=plan, existing=known.others, agents=agents, own=list(known.own.values()),
            )
        if revised is None:
            note = f"Could not revise: {detail[-512:] or 'the agent failed'}. The plan is unchanged."
            continue
        plan, note = revised, ""
        revisions += 1


def _finish_approved_request(coverage, client, ledger) -> list[str]:
    """Resume project resolution from the saved reviewed proposal, without a model."""
    from probe import analytics as tm

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
    # Before project resolution, which needs no left-out file: a create that
    # fails must not keep them `new`. One whose bytes moved since the review is
    # skipped and stays `new`, so the next run reviews what it is now.
    hashes_out = request.get("left_out_hashes") or {}
    coverage.exclude(
        {path: why for path, why in (request.get("left_out") or {}).items()
         if path in rows and rows[path]["present"]
         and rows[path]["observed_hash"] == hashes_out.get(path)},
        changed=request["import_changed"],
    )
    destinations = {}
    specs = {spec["slug"]: spec for spec in request["projects"]}
    # What this request created, saved before anything else happens, so a
    # resumed run finds its own new project instead of making another.
    created = request.setdefault("created", {})
    for slug in sorted(set(request["assigned"].values())):
        try:
            project = projects_mod.destination(
                client, slug, specs.get(slug, {}),
                workspace_id=coverage.scope.workspace_id, created=created,
                remember=lambda: coverage.put_meta("approved_request", request),
                # The spec file may carry a name a person wrote, but the `or
                # slug` fallback means this cannot tell which -- and composing
                # a name out of a file is what `authorship.py` calls a
                # template. Pinned `agent` so an import from a bare terminal
                # leaves it enhanceable instead of locking a slug; guessing
                # `human` here is the unrecoverable direction.
                authored_by=agent_session.AUTHORSHIP_AGENT,
            )
        except projects_mod.ExistingGone as exc:
            # Nothing was filed into it. The approval named a project that no
            # longer exists, so it cannot be completed: set aside, and the next
            # run reviews these files again instead of failing here for good.
            coverage.put_meta("superseded_request", request)
            coverage.put_meta("approved_request", None)
            raise _Stopped(
                tm.BackfillOutcome.PROJECT_CREATE_FAILED,
                f"The existing project {exc.slug} was deleted after the plan was approved; "
                "nothing was imported into it.",
                "Re-running reviews these files again.",
                projects_failed=1,
            ) from exc
        except Exception as exc:
            raise _Stopped(
                tm.BackfillOutcome.PROJECT_CREATE_FAILED,
                f"Could not create every project: {slug}: {exc}",
                "The reviewed plan is saved. Re-running retries project resolution without reclassifying.",
                projects_failed=1,
            ) from exc
        destinations[slug] = project
    # A new project whose slug someone took after the review got the next
    # free one: the saved experiments and runs follow it.
    projects_mod.retarget_structure(request.get("structure"), {
        slug: project["slug"] for slug, project in destinations.items()
        if project.get("slug") and project["slug"] != slug})
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
    # Before the request is cleared, so a crash here re-runs it. The records
    # themselves are created by `structure.build`, which every later pass
    # retries until they exist.
    if request.get("structure") is not None:  # absent from an older CLI's saved request
        structure.remember(coverage, request["structure"],
                           [*request["assigned"], *(request.get("imported") or [])])
    coverage.put_meta("approved_request", None)
    return [project.get("slug") or slug for slug, project in destinations.items()]


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
from probe.cli.imports.folder.flow.flow import _BackToImport, _Stopped  # noqa: E402 -- pieces need each other; the front door loads this one first
