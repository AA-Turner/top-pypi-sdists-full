"""show the plan to the reviewer: grouped by directory, and the approval screen's body."""

from __future__ import annotations

from ... import folder as bf
from probe.cli.imports.folder import evidence as evidence_mod
from . import plan as plan_mod
from ..structure import projects as projects_mod


#: Rows in the revise prompt's view of the plan. The view is a map, not the
#: plan: `probe-backfill-plan show` reaches the rest.
PLAN_VIEW_LINES = 60


def plan_view(plan: plan_mod.Plan) -> str:
    """The plan as the reviewer saw it, grouped by directory, largest first."""
    where: dict[str, str] = {a.path: a.project for a in plan.assignments}
    where.update({row.path: "left out" for row in plan.left_out})
    groups: dict[tuple[str, str], int] = {}
    for path, project in where.items():
        parts = path.replace("\\", "/").split("/")
        key = "/".join(parts[:2]) + ("/" if len(parts) > 2 else "")
        groups[key, project] = groups.get((key, project), 0) + 1
    lines = [f"    {d}  ->  {p}  ({n:,} file{'s' if n != 1 else ''})"
             for (d, p), n in sorted(groups.items(), key=lambda kv: (-kv[1], kv[0]))]
    if len(lines) > PLAN_VIEW_LINES:
        lines = lines[:PLAN_VIEW_LINES] + [f"    ... and {len(lines) - PLAN_VIEW_LINES:,} more"]
    if plan.excluded:
        lines.append(f"    ({len(plan.excluded):,} files are not classified yet)")
    for slug, spec in sorted(plan.experiments.items())[:PLAN_VIEW_LINES // 6]:
        lines.append(f"    experiment {slug} ({spec.get('project')}): {spec.get('under') or '.'}/")
    if plan.runs:
        shown = sorted(plan.runs)[:PLAN_VIEW_LINES // 6]
        more = f" and {len(plan.runs) - len(shown):,} more" if len(plan.runs) > len(shown) else ""
        lines.append(f"    {len(plan.runs):,} run(s): {', '.join(shown)}{more}")
    return "\n".join(lines) or "    (empty)"


def _destination(path: str, assigned: dict[str, str], left_out_paths=frozenset()) -> str:
    """Where `path` is going, whether it names a FILE or a rollup DIRECTORY.

    `assigned` is keyed by the expanded per-file paths, so a bare lookup misses
    every rollup row and printed `(unplaced)` beside a directory the plan had in
    fact placed -- next to a header saying all 204 files were placed. The label
    was the only thing wrong, which is worse than a real gap: it sends a
    reviewer hunting for a problem that does not exist.
    """
    direct = assigned.get(path)
    if direct:
        return direct
    if path in left_out_paths:
        return "left out"
    prefix = path.rstrip("/") + "/"
    under = {project for p, project in assigned.items() if p.startswith(prefix)}
    if len(under) == 1:
        return f"{under.pop()}  (all {sum(1 for p in assigned if p.startswith(prefix)):,} files under it)"
    if under:
        return "split across " + ", ".join(sorted(under))
    if any(p.startswith(prefix) for p in left_out_paths):
        return "left out"
    return "(unplaced)"


def describe_plan(
    ev: evidence_mod.Evidence,
    plan: plan_mod.Plan,
    assigned: dict[str, str],
    disc: plan_mod.Discrepancy,
    census: bf.Census | None = None,
    left_out: dict[str, str] | None = None,
    structure=None,
) -> list[str]:
    """The approval screen's body: what will happen, and what is uncertain.

    Leads with the counts a reviewer approves -- `3 projects · 12 experiments ·
    87 runs` -- and each project's share of them. Nothing is created until the
    plan is approved; `structure` is `backfill_structure.resolve`'s view of it.

    Least-certain first. A reviewer reading top-down should meet the decisions
    worth arguing with before the ones that are obviously fine, because the
    whole value of the gate is catching the shared `data/` directory that got
    filed under one researcher.
    """
    from .. import structure as structure_mod

    per_project: dict[str, int] = {}
    for project in assigned.values():
        per_project[project] = per_project.get(project, 0) + 1
    if structure is None:
        structure = structure_mod.resolve(plan, assigned)
    counts = structure.per_project()

    specs = {spec.slug: spec for spec in plan.projects}
    reused = sum(1 for p in per_project if projects_mod.tag(specs.get(p)) != "new")
    lines = [structure_mod.counts_line(len(per_project), structure),
             f"{len(assigned):,} of {ev.total_files:,} files placed into "
             f"{len(per_project)} project(s)"
             + (f", {reused} of them EXISTING (files are added to them)" if reused else "")
             + ":", ""]
    for project in sorted(per_project, key=lambda p: (-per_project[p], p)):
        extra = counts.get(project)
        spec = specs.get(project)
        lines.append(f"  {project:<32} {per_project[project]:>7,} files"
                     + (f" · {extra['experiments']:,} experiment{'s' if extra['experiments'] != 1 else ''}"
                        f" · {extra['runs']:,} run{'s' if extra['runs'] != 1 else ''}" if extra else "")
                     + f" · {projects_mod.tag(spec)}")
        about = projects_mod.detail(spec)
        if about:
            lines.append(f"      {about}")
    lines += structure_mod.describe(
        structure, fixed=sum(1 for path in plan.fixed if path in assigned))

    if left_out:
        # By the classifier's own rows, largest first, so a reviewer sees each
        # decision once with its why -- and can say "keep apps/lab" if wrong.
        def under(path: str, row: str) -> bool:
            if row in ("", "."):
                return "/" not in path
            return path == row or path.startswith(row.rstrip("/") + "/")

        counts = {row.path: sum(1 for p in left_out if under(p, row.path))
                  for row in plan.left_out}
        lines += ["", f"{len(left_out):,} files left out as not research (nothing uploads):"]
        for row in sorted(plan.left_out, key=lambda r: (-counts[r.path], r.path))[:12]:
            lines.append(f"  {row.path}  ({counts[row.path]:,} files)"
                         + (f"  {row.why}" if row.why else ""))
        if len(plan.left_out) > 12:
            lines.append(f"  ... and {len(plan.left_out) - 12:,} more")

    if plan.stats.get("naming_fallback"):
        lines += ["", "The project names could not be decided, so everything was filed into one "
                      "project named for the folder. Change the plan to split it."]
    if plan.stats.get("unread_slices"):
        lines += ["", f"{plan.stats['unread_slices']} slice(s) could not be read for naming; "
                      "their files were still filed."]
    if plan.excluded:
        # Named, not folded into "missing": nobody decided these, and guessing a
        # failed session's files from their neighbours is a guess at scale.
        lines += ["", f"{len(plan.excluded):,} files not classified: their classifier session "
                      "failed. Nothing of theirs uploads; re-running the import classifies only them."]
        for path in plan.excluded[:5]:
            lines.append(f"  {path}")
        if len(plan.excluded) > 5:
            lines.append(f"  ... and {len(plan.excluded) - 5:,} more")

    # The agent's own low-confidence SELECTIONS (a directory it was unsure of
    # reads as one line, not as its 400 files); per-file low marks only when a
    # plan carries no selections, as older plans do.
    low = [a for a in plan.assignments if a.confidence != "high"]
    unsure = list(dict.fromkeys(plan.unsure or [a.path for a in low]))
    if unsure:
        lines += ["", "Least certain — check these first:"]
        for path in unsure[:12]:
            lines.append(f"  {path}  ->  {_destination(path, assigned, left_out or {})}")
        if len(unsure) > 12:
            lines.append(f"  ... and {len(unsure) - 12:,} more")

    notes = disc.describe()
    if notes:
        lines += ["", *notes]
    # The linked-directory warning used to be built HERE. It moved to `_index`,
    # which runs straight after the walk: this gate is only reached on the
    # classify path, so resume, already-imported, empty-folder and the stranded
    # recovery all exited without ever mentioning what the walk could not see.
    if plan.summary:
        lines += ["", plan.summary]
    return lines
