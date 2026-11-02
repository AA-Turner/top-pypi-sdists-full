"""the reviewed plan's structure: resolve it against the final file map, describe it, remember or decline it."""

from __future__ import annotations
from dataclasses import dataclass, field

from probe.foundation.compat.compat import StrEnum
#: The coverage meta key holding the planned and created structure.
META_KEY = "structure"
#: Set once a folder's plan has been made by a CLI that names experiments and
#: runs: the `STRUCTURE_VERSION` it was made under. A source without it holds
#: files imported before, which the next import organizes (and never
#: re-uploads).
REVIEWED_KEY = "structure_reviewed"
#: The rules a folder's experiments and runs were planned under. Bumping it
#: re-plans every imported folder ONCE on its next import: its files are
#: classified again and moved, never uploaded again. 1 = the first rules
#: (#3488, 2026-10-26); a store that saved `True` or "declined" was made under
#: them.
STRUCTURE_VERSION = 1
#: Lines of the plan screen given to experiments and runs.
SHOWN = 12


class Level(StrEnum):
    RUN = "run"
    EXPERIMENT = "experiment"
    #: Back at the project: a file a re-plan no longer places in a run or an
    #: experiment it was filed in (`Coverage.plan_placements`).
    PROJECT = "project"


# -- the plan ------------------------------------------------------------------


def _ancestors(path: str):
    """Every folder above `path`, deepest first, ending with the root ("")."""
    parts = path.split("/")[:-1]
    for n in range(len(parts), 0, -1):
        yield "/".join(parts[:n])
    yield ""


@dataclass
class Resolved:
    """The plan's experiments and runs, checked against the final file map."""

    #: experiment folder -> {slug, project, name, question, under}
    experiments: dict[str, dict] = field(default_factory=dict)
    #: run folder -> {under, project, experiment (folder or None), name}
    runs: dict[str, dict] = field(default_factory=dict)
    #: path -> (Level, folder)
    targets: dict[str, tuple[Level, str]] = field(default_factory=dict)
    #: Declared but not kept: their files no longer sit in one project.
    dropped_runs: int = 0
    dropped_experiments: int = 0

    def per_project(self) -> dict[str, dict[str, int]]:
        out: dict[str, dict[str, int]] = {}
        for spec in self.experiments.values():
            out.setdefault(spec["project"], {"experiments": 0, "runs": 0})["experiments"] += 1
        for spec in self.runs.values():
            out.setdefault(spec["project"], {"experiments": 0, "runs": 0})["runs"] += 1
        return out

    def files_in(self) -> dict[tuple[Level, str], int]:
        counts: dict[tuple[Level, str], int] = {}
        for target in self.targets.values():
            counts[target] = counts.get(target, 0) + 1
        return counts

    def planned(self, *, times: bool = True) -> dict:
        """What the approval saves: specs, and each file's placement by folder.

        `times` is False for a folder that was copied (every file carries the
        copy's mtime, `Evidence.mtime_uninformative`): its runs get no times.
        """
        return {"experiments": self.experiments, "runs": self.runs, "times": times,
                "targets": {path: [level.value, folder]
                            for path, (level, folder) in self.targets.items()}}


def resolve(plan, assigned: dict[str, str], *, fixed_project: str | None = None) -> Resolved:
    """Keep the experiments and runs whose files sit in one project; place files.

    Selections were checked when they were made, but a later assignment can
    move a run's files to another project. Such a run is DROPPED, never split
    or guessed at: its files stay at their projects. A file goes to the deepest
    run folder above it, else the deepest experiment folder of its project.
    """
    out = Resolved()
    experiments_by_dir: dict[str, dict] = {}
    slug_dir: dict[str, str] = {}
    for slug, spec in (plan.experiments or {}).items():
        under = spec.get("under", "")
        experiments_by_dir[under] = {**spec, "slug": slug,
                                     "project": fixed_project or spec.get("project")}
        slug_dir[slug] = under
    run_dirs = set(plan.runs or {})
    run_files: dict[str, list[str]] = {d: [] for d in run_dirs}
    exp_files: dict[str, int] = {d: 0 for d in experiments_by_dir}
    for path, project in assigned.items():
        for folder in _ancestors(path):
            if folder in run_dirs:
                run_files[folder].append(path)
                break
        for folder in _ancestors(path):
            spec = experiments_by_dir.get(folder)
            if spec is not None and spec["project"] == project:
                exp_files[folder] += 1
                break
    for folder in sorted(run_dirs):
        members = run_files[folder]
        projects = {assigned[p] for p in members}
        if len(projects) != 1:
            out.dropped_runs += 1
            continue
        project = projects.pop()
        declared = (plan.runs[folder] or {}).get("experiment")
        experiment = slug_dir.get(declared) if declared else None
        if experiment is not None and experiments_by_dir[experiment]["project"] != project:
            experiment = None
        if experiment is None:
            experiment = next((d for d in _ancestors(folder + "/x")
                               if d in experiments_by_dir
                               and experiments_by_dir[d]["project"] == project), None)
        out.runs[folder] = {"under": folder, "project": project, "experiment": experiment,
                            "name": folder.rsplit("/", 1)[-1] or "run"}
    used = {spec["experiment"] for spec in out.runs.values() if spec["experiment"] is not None}
    for folder, spec in experiments_by_dir.items():
        if exp_files[folder] or folder in used:
            out.experiments[folder] = spec
        else:
            out.dropped_experiments += 1
    for path, project in assigned.items():
        target = None
        for folder in _ancestors(path):
            if folder in out.runs:
                target = (Level.RUN, folder)
                break
        if target is None:
            for folder in _ancestors(path):
                spec = out.experiments.get(folder)
                if spec is not None and spec["project"] == project:
                    target = (Level.EXPERIMENT, folder)
                    break
        if target is not None:
            out.targets[path] = target
    return out


def counts_line(projects: int, resolved: Resolved) -> str:
    """`3 projects · 12 experiments · 87 runs`."""
    def n(count: int, noun: str) -> str:
        return f"{count:,} {noun}{'s' if count != 1 else ''}"
    return " · ".join([n(projects, "project"), n(len(resolved.experiments), "experiment"),
                       n(len(resolved.runs), "run")])


def describe(resolved: Resolved, *, fixed: int = 0) -> list[str]:
    """The review screen's experiments-and-runs section."""
    if not resolved.experiments and not resolved.runs:
        return []
    files = resolved.files_in()
    lines = ["", "Experiments and runs (each run's times, config, metrics and status "
                 "are read from its files after you approve):"]
    runs_of: dict[str | None, list[str]] = {}
    for folder, spec in sorted(resolved.runs.items()):
        runs_of.setdefault(spec["experiment"], []).append(folder)
    for folder, spec in sorted(resolved.experiments.items())[:SHOWN]:
        count = len(runs_of.get(folder, []))
        other = files.get((Level.EXPERIMENT, folder), 0)
        lines.append(f"  {spec['slug']}  ({spec['project']} · {folder or '.'}/ · "
                     f"{count:,} run{'s' if count != 1 else ''} · "
                     f"{other:,} other file{'s' if other != 1 else ''})")
        lines.append(f"      {spec.get('question', '')[:160]}")
    if len(resolved.experiments) > SHOWN:
        lines.append(f"  ... and {len(resolved.experiments) - SHOWN:,} more experiments")
    shown = sorted(resolved.runs)[:SHOWN]
    for folder in shown:
        spec = resolved.runs[folder]
        where = resolved.experiments[spec["experiment"]]["slug"] if spec["experiment"] is not None \
            else spec["project"]
        count = files.get((Level.RUN, folder), 0)
        lines.append(f"  run {folder}  ->  {where}  ({count:,} file{'s' if count != 1 else ''})")
    if len(resolved.runs) > SHOWN:
        lines.append(f"  ... and {len(resolved.runs) - SHOWN:,} more runs")
    if resolved.dropped_runs or resolved.dropped_experiments:
        lines.append(f"  Not kept: {resolved.dropped_runs:,} run(s) and "
                     f"{resolved.dropped_experiments:,} experiment(s) whose files are no "
                     "longer in one project; their files stay at their projects.")
    if fixed:
        lines.append(f"  {fixed:,} of these files were imported before: they are moved into "
                     "their run or experiment, never uploaded again.")
    return lines


def plan_json(assigned: dict[str, str], resolved: Resolved, *, left_out: int = 0,
              fixed: int = 0, skipped: dict | None = None, projects=None) -> dict:
    """The approval's plan for a program: counts first, then each record.

    `skipped` is what the walk left out by rule (`backfill.Census.skipped_json`:
    hidden folders and worktree copies, with file counts), the same fields as
    the desktop's job record; added under `skipped` when given.

    `projects` is the plan's `ProjectSpec`s: each project then says whether it
    already `existing` and why (`backfill_projects.plan_entry`): its `origin`,
    `name`, `project_id`, `reason`, what it already holds (`existing_runs`,
    `existing_files`) and `possibly_same_as` for a new slug close to an
    existing one."""
    from .projects import plan_entry

    per_project = resolved.per_project()
    files_per: dict[str, int] = {}
    for project in assigned.values():
        files_per[project] = files_per.get(project, 0) + 1
    files = resolved.files_in()
    runs_of: dict[str | None, int] = {}
    for spec in resolved.runs.values():
        runs_of[spec["experiment"]] = runs_of.get(spec["experiment"], 0) + 1
    specs = {spec.slug: spec for spec in projects or ()}
    origins = {slug: plan_entry(specs.get(slug)) for slug in files_per} if projects is not None else {}
    existing = sum(1 for entry in origins.values() if entry["existing"])
    return {
        "schema": "probe.backfill.plan/1",
        "totals": {"files": len(assigned), "projects": len(files_per),
                   "experiments": len(resolved.experiments), "runs": len(resolved.runs),
                   "left_out": left_out, "already_imported": fixed,
                   **({"projects_new": len(files_per) - existing, "projects_existing": existing}
                      if projects is not None else {})},
        "projects": [
            {"slug": slug, "files": count,
             "experiments": per_project.get(slug, {}).get("experiments", 0),
             "runs": per_project.get(slug, {}).get("runs", 0), **origins.get(slug, {})}
            for slug, count in sorted(files_per.items())
        ],
        "experiments": [
            {"slug": spec["slug"], "name": spec.get("name") or spec["slug"],
             "question": spec.get("question", ""), "project": spec["project"],
             "folder": folder, "runs": runs_of.get(folder, 0),
             "files": files.get((Level.EXPERIMENT, folder), 0)}
            for folder, spec in sorted(resolved.experiments.items())
        ],
        "runs": [
            {"name": spec["name"], "folder": folder, "project": spec["project"],
             "experiment": (resolved.experiments[spec["experiment"]]["slug"]
                            if spec["experiment"] is not None else None),
             "files": files.get((Level.RUN, folder), 0)}
            for folder, spec in sorted(resolved.runs.items())
        ],
        **({"skipped": skipped} if skipped is not None else {}),
    }


# -- after approval: build, then file ------------------------------------------


def remember(coverage, planned: dict | None, paths) -> None:
    """Save an approved plan's experiments, runs and file placements.

    The specs merge by FOLDER into what earlier imports planned, so a re-import
    that names the same run again changes nothing and one that names a new run
    adds it. The placements are the plan's own, per file: `build` reads a run
    from its approved files only and moves only those, so a file nobody
    approved for a run (one imported before and left as it was, say) is never
    read into it or moved. `paths` are every file this plan decided; one it
    placed nowhere loses an older placement.
    """
    planned = planned or {}
    coverage.put_meta(META_KEY, merge_planned(coverage.meta(META_KEY), planned))
    targets = planned.get("targets") or {}
    coverage.plan_placements(
        {path: (str(level), str(folder)) for path, (level, folder) in targets.items()},
        cleared=[path for path in paths if path not in targets],
    )
    coverage.put_meta(REVIEWED_KEY, STRUCTURE_VERSION)


def merge_planned(saved: dict | None, planned: dict) -> dict:
    """`Resolved.planned()` (JSON) merged by FOLDER into the specs saved before.

    Returns `{"experiments": ..., "runs": ...}`, `build_plan`'s input: what a
    folder was made into before (its id, digest, slug attempts) is kept, so a
    plan made again over the same folders makes nothing twice.
    """
    saved = saved or {}
    experiments = dict(saved.get("experiments") or {})
    runs = dict(saved.get("runs") or {})
    for folder, spec in (planned.get("experiments") or {}).items():
        old = experiments.get(folder) or {}
        experiments[folder] = {**spec, **{k: old[k] for k in ("id", "project_id", "attempts",
                                                              "foreign") if k in old}}
    for folder, spec in (planned.get("runs") or {}).items():
        old = runs.get(folder) or {}
        runs[folder] = {**spec, "times": bool(planned.get("times", True)),
                        **{k: old[k] for k in ("id", "target_id", "digest", "project_id", "points")
                           if k in old}}
    return {"experiments": experiments, "runs": runs}


def reviewed_version(value) -> int:
    """The `STRUCTURE_VERSION` a stored `REVIEWED_KEY` value was made under."""
    if value is True or value == "declined":
        return 1
    if isinstance(value, dict):
        value = value.get("version")
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def decline(coverage) -> None:
    """A person chose to leave this folder's imported files as they are: not
    asked again until the structure rules change."""
    coverage.put_meta(REVIEWED_KEY, {"version": STRUCTURE_VERSION, "declined": True})
