"""Experiments and runs from a folder import: the model names folders, code builds them.

The classifier SELECTS, through `probe-backfill-plan`: `experiment --under <dir>`
files a directory into a new experiment, `run --under <dir>` makes one folder a
run and `run --each-under <dir>` makes each folder under a directory one run.
Every selection is checked against the walk when it is made. Everything after
that is this module's, and none of it passes through a model:

    the plan        which experiments and runs, per project   (`resolve`)
    a run's record  name, times, config, metrics, status       (`read_run`)
    the records     created after approval, once              (`build`)
    the files       filed at their run or experiment          (`file_delivered`)

A run's record is READ, never written by a model (Richard 2026-10-25: "the llm
cant be trusted to be reliable if it has to regurgitate"). It is created
UNNAMED (its folder is kept in `metadata.backfill`), its start and end are the
oldest and newest file mtime, its config the top-level scalars of config-like
files, its metrics the top-level numbers of known result files (each also a
one-point series, `metric_points`), its status an explicit field. Nothing is
computed, averaged or guessed: a value that is not in a file does not exist, and a run with no
explicit status ends `untracked` (the API's "nothing is known about how it
ended") rather than claiming success.

IDEMPOTENT. A run's identity is `(import source, relative folder)`: the source
id is the folder import's own (`Coverage.source_id`, one per folder and
destination), sent as the run's `external_id` under source `backfill`, which the
server keeps unique. A re-import finds the run it made (a 409 naming it) and
creates nothing; the local record (coverage meta `structure`) skips even the
request when the run's record has not changed.

FILES ARE UPLOADED ONCE, at their project, by the delivery path that already
proves every byte with a receipt; then they are MOVED (same artifact id, no
bytes) to their run or experiment. A folder imported before experiments and
runs existed is organized the same way: its files already have receipts, so they
are moved and never sent again.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from probe._compat import StrEnum, tomllib

#: `runs.source` for every run an import creates. The provenance word.
RUN_SOURCE = "backfill"
#: `metadata.backfill.schema` on those runs.
RUN_SCHEMA = "1"
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

#: Per run, so one result file with a thousand fields cannot become a
#: thousand-key summary. Kept in sorted key order; the count dropped is recorded.
MAX_METRICS = 200
MAX_CONFIG = 200
#: Files larger than this are not parsed (a result table is not a result file).
MAX_PARSE_BYTES = 5 * 1024 * 1024
MAX_CONFIG_TEXT = 1_000
#: Provenance kept on the run: which files the values were read from.
MAX_SOURCES = 50
#: Lines of the plan screen given to experiments and runs.
SHOWN = 12
#: Moves in flight at once while filing files into their runs.
FILE_WORKERS = 4
#: The server's mark on a create it answered with an earlier run (0268).
REPLAY_HEADER = "Idempotent-Replay"


class Level(StrEnum):
    RUN = "run"
    EXPERIMENT = "experiment"
    #: Back at the project: a file a re-plan no longer places in a run or an
    #: experiment it was filed in (`Coverage.plan_placements`).
    PROJECT = "project"


class Ended(StrEnum):
    """The terminal statuses a read run can end in (the API's `RunStatus`)."""

    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    #: Nothing in the folder says how it ended. Never `completed`.
    UNKNOWN = "untracked"


# -- which files say what ------------------------------------------------------

_RESULT_JSON = re.compile(
    r"\A(reward|outcome|.*result.*|metrics.*|summary.*|eval.*)\.json\Z", re.I)
_LONE_NUMBER = re.compile(r"\A(reward|score)\.txt\Z", re.I)
_CONFIG = re.compile(
    r"\A(.*\.toml|config.*\.(json|ya?ml)|args.*\.json|h?params.*\.(json|ya?ml|toml))\Z", re.I)
#: Explicit status fields, in the order they are read.
STATUS_FIELDS = ("status", "outcome", "success", "passed", "exit_code")
_DONE = {"completed", "complete", "success", "succeeded", "successful", "passed", "pass",
         "ok", "done", "finished"}
_FAILED = {"failed", "failure", "fail", "error", "errored", "crashed", "timeout", "timed_out"}
_CANCELED = {"canceled", "cancelled", "aborted", "killed", "interrupted"}


def is_result_file(name: str) -> bool:
    return bool(_RESULT_JSON.match(name) or _LONE_NUMBER.match(name))


def is_config_file(name: str) -> bool:
    return bool(_CONFIG.match(name))


_MANIFEST = re.compile(r"\A.*manifest.*\.json\Z", re.I)
_LOG = re.compile(r"\A.*\.log\Z", re.I)


def run_candidates(paths) -> list[str]:
    """Folders that look like one run's output: a config or manifest AND a
    result file or a log, directly inside. A hint shown to the classifier,
    which keeps or drops each; code never makes a run from it. The import's
    root is never one (the whole folder is not a run by shape alone)."""
    seen: dict[str, set[str]] = {}
    for rel in paths:
        directory, _, name = rel.rpartition("/")
        if not directory:
            continue
        if is_config_file(name) or _MANIFEST.match(name):
            seen.setdefault(directory, set()).add("config")
        if is_result_file(name) or _LOG.match(name):
            seen.setdefault(directory, set()).add("output")
    return sorted(folder for folder, kinds in seen.items() if len(kinds) == 2)


@dataclass
class RunRecord:
    """Everything a run is created with, read from its folder."""

    name: str
    started_at: str | None
    ended_at: str | None
    status: Ended
    config: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    #: `metadata.backfill`: where it came from and which files said what.
    provenance: dict = field(default_factory=dict)
    #: metric key -> the ISO mtime of the file its value was read from: the
    #: point's `wall_clock` (`metric_points`). Not in the digest.
    clocks: dict = field(default_factory=dict)

    def digest(self) -> str:
        return hashlib.sha256(json.dumps(
            [self.name, self.started_at, self.ended_at, self.status.value,
             self.config, self.metrics, self.provenance],
            sort_keys=True, default=str).encode()).hexdigest()


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _number(value) -> float | int | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _scalar(value):
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return value if (not isinstance(value, float) or math.isfinite(value)) else None
    if isinstance(value, str):
        return value[:MAX_CONFIG_TEXT]
    return _SKIP


_SKIP = object()


def _read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_PARSE_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _json_object(path: Path) -> dict | None:
    text = _read_text(path)
    if text is None:
        return None
    try:
        data = json.loads(text)
    except (ValueError, RecursionError):
        return None
    return data if isinstance(data, dict) else None


def _lone_number(path: Path) -> float | int | None:
    text = _read_text(path)
    if text is None:
        return None
    token = text.strip()
    if not token or len(token.split()) != 1:
        return None
    try:
        value = int(token)
    except ValueError:
        try:
            value = float(token)
        except ValueError:
            return None
    return _number(value)


_YAML_KEY = re.compile(r"\A([A-Za-z_][\w.-]*)\s*:\s*(.*?)\s*\Z")


def _yaml_top(text: str) -> dict:
    """Top-level `key: scalar` lines of a YAML file, and nothing else.

    No YAML library ships with the CLI, and the rule only wants top-level
    scalars, which are one line each. A nested block, a list, an anchor or a
    multi-line string is skipped rather than half-read.
    """
    out: dict = {}
    for line in text.splitlines():
        if not line or line[0] in " \t#-" or line.startswith("---"):
            continue
        match = _YAML_KEY.match(line)
        if not match:
            continue
        key, raw = match.groups()
        if raw[:1] in ("\"", "'"):
            # A quoted value ends at its closing quote; a ` #` inside it is text.
            close = raw.find(raw[0], 1)
            rest = raw[close + 1:].strip() if close > 0 else "?"
            if not rest or rest.startswith("#"):
                out[key] = raw[1:close]
            continue
        raw = re.split(r"(?:^|\s)#", raw, maxsplit=1)[0].strip()
        if not raw or raw[0] in "[{|>&*!":
            continue
        lowered = raw.lower()
        if lowered in ("true", "false"):
            out[key] = lowered == "true"
        elif lowered in ("null", "~"):
            out[key] = None
        else:
            try:
                out[key] = int(raw)
            except ValueError:
                try:
                    value = float(raw)
                    out[key] = value if math.isfinite(value) else raw
                except ValueError:
                    out[key] = raw
    return out


def _config_values(path: Path) -> dict | None:
    name = path.name.lower()
    text = _read_text(path)
    if text is None:
        return None
    if name.endswith(".toml"):
        try:
            data = tomllib.loads(text)
        except (tomllib.TOMLDecodeError, ValueError, RecursionError):
            return None
    elif name.endswith(".json"):
        try:
            data = json.loads(text)
        except (ValueError, RecursionError):
            return None
        if not isinstance(data, dict):
            return None
    else:
        data = _yaml_top(text)
    out = {}
    for key, value in data.items():
        scalar = _scalar(value)
        if scalar is not _SKIP:
            out[str(key)] = scalar
    return out


def _status_of(values: list) -> Ended | None:
    """One explicit field's verdict, or None when it says nothing usable."""
    found: set[Ended] = set()
    for field_name, value in values:
        verdict = None
        if field_name in ("success", "passed"):
            if isinstance(value, bool):
                verdict = Ended.COMPLETED if value else Ended.FAILED
        elif field_name == "exit_code":
            if isinstance(value, int) and not isinstance(value, bool):
                verdict = Ended.COMPLETED if value == 0 else Ended.FAILED
        elif isinstance(value, str):
            word = value.strip().lower()
            verdict = (Ended.COMPLETED if word in _DONE else Ended.FAILED if word in _FAILED
                       else Ended.CANCELED if word in _CANCELED else None)
        if verdict is not None:
            found.add(verdict)
    # Two fields that disagree say nothing certain: no status is claimed.
    return found.pop() if len(found) == 1 else None


def _keyed(entries: list[tuple[str, str, str, object]]) -> dict:
    """`(directory, file, field, value)` -> `{key: value}`, keys traceable.

    `field` at the run's top level, `<dir>/field` below it. Two files that
    would give one key both get their file's name instead, so no number
    silently replaces another.
    """
    by_key: dict[str, list] = {}
    for directory, filename, name, value in entries:
        key = f"{directory}/{name}" if directory else name
        by_key.setdefault(key, []).append((directory, filename, name, value))
    out: dict = {}
    for key, rows in by_key.items():
        if len(rows) == 1:
            out[key] = rows[0][3]
            continue
        for directory, filename, name, value in rows:
            qualified = f"{directory}/{filename}" if directory else filename
            out[qualified if filename.rsplit(".", 1)[0] == name else f"{qualified}:{name}"] = value
    return out


def read_run(root: Path, under: str, files: list[str], *, times: bool = True) -> RunRecord:
    """A run's record from the files of its folder (paths relative to `root`).

    `files` are the files the import holds for the run (left-out ones are not
    among them). Times are their mtimes; config and metrics are read from the
    file kinds named in the module docs, at any depth, keyed by where they sit.
    The status is read only from files directly in the run's folder: a trial's
    outcome three levels down is that trial's, not the run's. With `times`
    False (the folder was copied, so every mtime is the copy's) no time is
    claimed.
    """
    mtimes: list[float] = []
    metric_rows: list = []
    config_rows: list = []
    status_fields: list = []
    sources = {"metrics": [], "config": [], "status": []}
    prefix = under + "/" if under else ""
    for rel in sorted(files):
        path = root / rel
        try:
            mtimes.append(path.stat().st_mtime)
        except OSError:
            continue
        inner = rel[len(prefix):] if rel.startswith(prefix) else rel
        directory, _, filename = inner.rpartition("/")
        if _LONE_NUMBER.match(filename):
            value = _lone_number(path)
            if value is not None:
                metric_rows.append((directory, filename, filename.rsplit(".", 1)[0],
                                    (value, mtimes[-1])))
                sources["metrics"].append(rel)
        elif _RESULT_JSON.match(filename):
            data = _json_object(path)
            if data is not None:
                found = False
                for key, value in data.items():
                    number = _number(value)
                    if number is not None and str(key) not in ("exit_code",):
                        metric_rows.append((directory, filename, str(key), (number, mtimes[-1])))
                        found = True
                if not directory:
                    picked = [(f, data[f]) for f in STATUS_FIELDS if f in data]
                    if picked:
                        status_fields.extend(picked)
                        sources["status"].append(rel)
                if found:
                    sources["metrics"].append(rel)
        if _CONFIG.match(filename):
            values = _config_values(path)
            if values:
                for key, value in values.items():
                    config_rows.append((directory, filename, key, value))
                sources["config"].append(rel)
    timed = _keyed(metric_rows)
    config = _keyed(config_rows)
    dropped = {}
    if len(timed) > MAX_METRICS:
        dropped["metrics"] = len(timed) - MAX_METRICS
        timed = dict(sorted(timed.items())[:MAX_METRICS])
    metrics = {key: value for key, (value, _) in timed.items()}
    clocks = {key: _iso(stamp) for key, (_, stamp) in timed.items()}
    if len(config) > MAX_CONFIG:
        dropped["config"] = len(config) - MAX_CONFIG
        config = dict(sorted(config.items())[:MAX_CONFIG])
    status = _status_of(status_fields) or Ended.UNKNOWN
    provenance = {
        "schema": RUN_SCHEMA,
        "relative_path": under,
        "files": len(files),
        # Unknown when every file of the import was written inside one window,
        # as a copy leaves them (`Evidence.mtime_uninformative`): a copy's time
        # is not the run's.
        "times": "file mtimes" if times else "unknown: every file has one copy-like mtime",
        "read_from": {k: v[:MAX_SOURCES] for k, v in sources.items() if v},
    }
    if dropped:
        provenance["dropped"] = dropped
    return RunRecord(
        name=(under.rsplit("/", 1)[-1] or "run")[:200],
        started_at=_iso(min(mtimes)) if mtimes and times else None,
        ended_at=_iso(max(mtimes)) if mtimes and times else None,
        status=status, config=config, metrics=metrics, provenance=provenance, clocks=clocks,
    )


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
    from .backfill_projects import plan_entry

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


def external_id(source_id: str, folder: str) -> str:
    """A run's identity: this import source and the run's relative folder."""
    digest = hashlib.sha256(f"{source_id}\0{folder}".encode()).hexdigest()[:40]
    return f"backfill:{digest}"


def _creation_key(external: str, target: str, body: dict) -> str:
    """Deterministic, so a lost response is replayed into the same run."""
    return hashlib.sha256(json.dumps([external, target, body], sort_keys=True).encode()
                          ).hexdigest()[:48]


@dataclass
class Built:
    experiments_created: int = 0
    runs_created: int = 0
    runs_existing: int = 0
    runs_updated: int = 0
    runs_zero_metrics: int = 0
    metric_points: int = 0
    metric_points_failed: int = 0
    #: Result values that changed while their file kept its time: the server
    #: keeps the first value at a (key, wall_clock), so the chart shows the old
    #: one (the run summary has the new). Reported, never retried.
    metric_points_stale: int = 0
    failed: int = 0
    problems: list[str] = field(default_factory=list)
    chart_problems: list[str] = field(default_factory=list)

    def stats(self) -> dict:
        return {"experiments_created": self.experiments_created,
                "runs_created": self.runs_created, "runs_existing": self.runs_existing,
                "runs_updated": self.runs_updated, "runs_zero_metrics": self.runs_zero_metrics,
                "metric_points": self.metric_points,
                "metric_points_failed": self.metric_points_failed,
                "metric_points_stale": self.metric_points_stale,
                "structure_failed": self.failed}


def _create_experiment(client, spec: dict, project_id: str, save) -> str:
    """Create the experiment; adopt an existing one only if THIS import made it.

    A taken slug that is not ours (slugs are one namespace with projects, and
    a person may have an experiment of that name) gets a numbered slug: the
    review promised a new experiment. A slug this import already tried -- its
    create landed but the answer was lost -- is adopted.
    """
    from ..sdk import agent_session, errors

    slug = spec["slug"]
    tried = set(spec.get("attempts") or [])
    foreign = set(spec.get("foreign") or [])
    for attempt in range(5):
        suffix = "" if attempt == 0 else f"-{attempt + 1}"
        candidate = slug[:63 - len(suffix)] + suffix
        if candidate in foreign:
            continue
        ours = candidate in tried
        if not ours:
            # Recorded BEFORE the create: a create that lands while its answer
            # is lost is ours to adopt on the next pass.
            tried.add(candidate)
            spec["attempts"] = sorted(tried)
            save()
        try:
            row = client.create_experiment(
                candidate, spec.get("name") or slug, question=spec["question"],
                project_id=project_id, authored_by=agent_session.AUTHORSHIP_AGENT,
            )
            return str(row["id"])
        except errors.ConflictError as exc:
            holder = exc.existing or {}
            if (ours and holder.get("kind") == "experiment" and holder.get("id")
                    and str(holder.get("parent_project_id")) == project_id):
                return str(holder["id"])
            # Someone else's: never adopted, never tried again.
            tried.discard(candidate)
            foreign.add(candidate)
            spec["attempts"], spec["foreign"] = sorted(tried), sorted(foreign)
            save()
    raise ValueError(f"no free slug for experiment {slug!r}")


def _converge(client, run_id: str, record: RunRecord, *, fresh: bool,
              experiment_id: str | None = None, project_id: str | None = None) -> bool:
    """Make the stored run say what its folder says. Returns True if it wrote.

    A run just created gets its end in one PATCH. An existing one is read
    first and only what differs is sent, so a re-import of an unchanged run
    writes nothing; the name is never touched (a person may have renamed it).
    An existing run the plan now files elsewhere (into an experiment, or out of
    one) is moved there, with the same PATCH.
    """
    want: dict = {"status": record.status.value}
    if record.ended_at:
        want["ended_at"] = record.ended_at
    if record.metrics:
        want["summary_metrics"] = record.metrics
    if not fresh:
        current = client.transport.get(f"/v1/runs/{run_id}")
        if current.get("status") == want["status"]:
            want.pop("status")
        if "ended_at" in want and current.get("ended_at") and _same_time(
                current["ended_at"], want["ended_at"]):
            want.pop("ended_at")
        if "summary_metrics" in want and (current.get("summary_metrics") or {}) == record.metrics:
            want.pop("summary_metrics")
        stored = current.get("config") or {}
        changed = {k: v for k, v in record.config.items() if stored.get(k) != v}
        if changed:
            want["config_merge"] = changed
        if experiment_id is not None and str(current.get("experiment_id")) != experiment_id:
            want["experiment_id"] = experiment_id
        elif experiment_id is None and project_id is not None and (
                current.get("experiment_id") or str(current.get("project_id")) != project_id):
            want["project_id"] = project_id
    if not want:
        return False
    client.transport.patch(f"/v1/runs/{run_id}", want)
    return True


def _same_time(a: str, b: str) -> bool:
    try:
        return abs(datetime.fromisoformat(a.replace("Z", "+00:00")).timestamp()
                   - datetime.fromisoformat(b.replace("Z", "+00:00")).timestamp()) < 0.001
    except ValueError:
        return a == b


def _create_run(client, *, source_id: str, folder: str, target_id: str,
                record: RunRecord) -> tuple[str, bool]:
    """The run for `folder`, created now or found. Returns (id, created)."""
    from ..sdk import errors

    external = external_id(source_id, folder)
    # NO NAME. A name sent on create is a claimed one (`name_customized`), and
    # that lock is monotonic: nothing could ever rename a run called after its
    # folder (1,008 of Tokenless's 1,032 were hex attempt ids, 2026-10-26). The
    # folder stays in `metadata.backfill.relative_path`; the run is titled like
    # any unnamed run until the import's record pass names it.
    body = {
        "source": RUN_SOURCE,
        "external_id": external,
        "config": record.config,
        "metadata": {"backfill": {**record.provenance, "source_id": source_id}},
        # Delivered after the fact: nothing beats for it, its start is the
        # folder's, and the create can be replayed under its key.
        "offline": True,
        "heartbeat": False,
    }
    if record.started_at:
        body["started_at"] = record.started_at
    body["creation_key"] = _creation_key(external, target_id, body)
    try:
        resp = client.transport.request("POST", f"/v1/projects/{target_id}/runs",
                                        json_body=body, idempotent=True)
        # The same request again (a lost answer, a wiped local record) is
        # answered with the run it made, marked as a replay: found, not new.
        return str(resp.json()["id"]), resp.headers.get(REPLAY_HEADER, "").lower() != "true"
    except errors.ConflictError as exc:
        # A different request for the same folder (its files changed since):
        # the server names the run this import already made.
        if exc.existing_id:
            return str(exc.existing_id), False
        raise


def metric_points(record: RunRecord) -> list[dict]:
    """The run's result numbers as one-point series, beside its summary.

    `track-work`: "one headline number -> one-point metric plus the run
    summary"; the summary alone draws no chart (0 of Tokenless's 1,032 imported
    runs had one, 2026-10-26). UNSTEPPED, stamped with the mtime of the file the
    value came from: the server keeps the first point per (key, wall_clock), so
    sending a run's points again stores nothing, and a result file that changed
    adds its new value at its new time instead of being dropped as a repeat of
    step 0. A `__`-prefixed key is the server's own (chart settings), never a
    result.
    """
    return [{"key": key, "value": float(value), "wall_clock": record.clocks[key]}
            for key, value in sorted(record.metrics.items())
            if key in record.clocks and not key.startswith("__")]


def _chart(client, run_id: str, record: RunRecord, sent: dict | None, built: Built,
           under: str) -> dict | None:
    """Send the run's `metric_points` that it does not hold yet.

    `sent` is what this import charted for the run before (key -> [value,
    wall_clock]), None for a run charted never: one an older CLI made, whose
    folder has not changed since, still gets its chart once. Returns what the
    run now holds, or `sent` unchanged when the send was refused (so the next
    pass tries again). A value whose file kept its time is not stored again by
    the server (first write wins at a (key, wall_clock)): counted stale.
    """
    points = metric_points(record)
    want = {p["key"]: [p["value"], p["wall_clock"]] for p in points}
    if want == sent:
        return sent
    previous = sent or {}
    todo = [p for p in points if previous.get(p["key"]) != want[p["key"]]]
    stale = sum(1 for p in todo
                if p["key"] in previous and previous[p["key"]][1] == p["wall_clock"])
    if todo:
        try:
            answer = client.transport.post(f"/v1/runs/{run_id}/metrics", {"points": todo})
        except Exception as exc:  # noqa: BLE001 - the summary holds them; reported
            built.metric_points_failed += 1
            built.chart_problems.append(f"run {under}: {str(exc)[:300]}")
            return sent
        inserted = (answer or {}).get("inserted") if isinstance(answer, dict) else None
        built.metric_points += len(todo) if inserted is None else int(inserted)
        built.metric_points_stale += stale
    return want


#: How many records `build` creates between saves of its local record.
SAVE_EVERY = 25


def build(client, coverage, folder: Path, *, report=None) -> Built:
    """Create the approved experiments and runs that do not exist yet; place files.

    Runs on every import after approval and on every resume, so a create that
    failed (the network, a plan's run cap) is tried again, and a re-import adds
    only what is new. A run is read from, and holds, only the files a plan
    approved for it (`remember`). The work is `build_plan`'s; this is the local
    record around it.
    """
    saved = coverage.meta(META_KEY) or {}
    experiments: dict = dict(saved.get("experiments") or {})
    runs: dict = dict(saved.get("runs") or {})
    if not experiments and not runs:
        return Built()
    unsaved = 0

    def save(force: bool = False) -> None:
        nonlocal unsaved
        unsaved += 1
        if force or unsaved >= SAVE_EVERY:
            coverage.put_meta(META_KEY, {"experiments": experiments, "runs": runs})
            unsaved = 0

    try:
        built, targets = build_plan(client, folder, source_id=coverage.source_id,
                                    experiments=experiments, runs=runs,
                                    placements=coverage.planned_placements(), save=save)
    finally:
        coverage.put_meta(META_KEY, {"experiments": experiments, "runs": runs})
    coverage.resolve_placements(targets)
    if report is not None:
        if built.experiments_created or built.runs_created:
            report.add(f"Created {built.experiments_created:,} experiment(s) and "
                       f"{built.runs_created:,} run(s) from the folder"
                       + (f" ({built.runs_zero_metrics:,} run(s) had no result file to read "
                          "metrics from)" if built.runs_zero_metrics else "") + ".")
        if built.problems:
            report.add(f"{built.failed:,} experiment(s)/run(s) could not be created; their files "
                       "stay at their projects and re-running tries again:",
                       *[f"  {p}" for p in built.problems[:5]])
        if built.chart_problems:
            report.add(f"{built.metric_points_failed:,} run(s) have their numbers but no chart "
                       "yet; re-running sends them again:",
                       *[f"  {p}" for p in built.chart_problems[:3]])
        if built.metric_points_stale:
            report.add(f"{built.metric_points_stale:,} result value(s) changed while their file kept "
                       "its time; the chart keeps the first value (the run's summary has the new one).")
    return built


def build_plan(client, folder: Path, *, source_id: str, experiments: dict, runs: dict,
               placements: list[dict], save=None) -> tuple[Built, dict[str, str]]:
    """Create a plan's experiments and runs that do not exist yet. Data in, no store.

    `experiments` and `runs` are the saved specs by folder (`remember`'s shape),
    updated IN PLACE with what was made (ids, digests); `placements` are the
    planned rows (`path`, `level`, `folder`, `present`, `exclusion`,
    `project_id`, `project_slug`, as `Coverage.planned_placements` gives them);
    `source_id` is the import source whose runs these are (their `external_id`,
    so a plan built again, here or elsewhere, finds the runs it made). `save()`
    is called after each record and `save(force=True)` before a create whose
    answer could be lost. Returns what it did and path -> the id of the run or
    experiment that file now belongs to.
    """
    save = save or (lambda force=False: None)
    built = Built()
    project_of_slug: dict[str, str] = {}
    by_folder: dict[tuple[str, str], list[dict]] = {}
    for row in placements:
        if row["project_id"] and row["project_slug"]:
            project_of_slug.setdefault(row["project_slug"], row["project_id"])
        if row["present"] and not row["exclusion"] and row["project_id"]:
            by_folder.setdefault((row["level"], row["folder"]), []).append(row)

    def fail(what: str, why) -> None:
        built.failed += 1
        built.problems.append(f"{what}: {str(why)[:300]}")

    targets: dict[str, str] = {}
    for under, spec in sorted(experiments.items()):
        project_id = spec.get("project_id") or project_of_slug.get(spec.get("project"))
        if spec.get("id") or project_id is None:
            continue
        try:
            spec["id"] = _create_experiment(client, spec, project_id, lambda: save(force=True))
            spec["project_id"] = project_id
            built.experiments_created += 1
            save()
        except Exception as exc:  # noqa: BLE001 - reported; the files still deliver
            fail(f"experiment {spec.get('slug')}", exc)

    for under, spec in sorted(runs.items()):
        found = by_folder.get((Level.RUN.value, under)) or []
        if not found:
            continue  # none of its approved files is here any more
        project_ids = {row["project_id"] for row in found}
        if len(project_ids) != 1:
            fail(f"run {under}", f"its files are in {len(project_ids)} projects; they stay there")
            continue
        project_id = project_ids.pop()
        experiment = experiments.get(spec["experiment"]) if spec.get("experiment") is not None else None
        if experiment is not None and not experiment.get("id"):
            continue  # its experiment failed above; the next pass retries both
        if experiment is not None and experiment.get("project_id") != project_id:
            experiment = None
        target_id = experiment["id"] if experiment is not None else project_id
        try:
            record = read_run(folder, under, [row["path"] for row in found],
                              times=spec.get("times", True))
            digest = hashlib.sha256((record.digest() + target_id).encode()).hexdigest()
            if not (spec.get("id") and spec.get("target_id") == target_id
                    and spec.get("digest") == digest):
                run_id, created = (spec["id"], False) if (
                    spec.get("id") and spec.get("target_id") == target_id
                ) else _create_run(client, source_id=source_id, folder=under,
                                   target_id=target_id, record=record)
                wrote = _converge(client, run_id, record, fresh=created,
                                  experiment_id=experiment["id"] if experiment is not None else None,
                                  project_id=project_id)
                if created:
                    built.runs_created += 1
                    built.runs_zero_metrics += int(not record.metrics)
                else:
                    built.runs_existing += 1
                    built.runs_updated += int(wrote)
                spec.update(id=run_id, target_id=target_id, digest=digest, project_id=project_id)
                save()
            charted = _chart(client, spec["id"], record, spec.get("points"), built, under)
            if charted != spec.get("points"):
                spec["points"] = charted
                save()
        except Exception as exc:  # noqa: BLE001 - reported; the files still deliver
            fail(f"run {under}", exc)
            continue
        targets.update({row["path"]: spec["id"] for row in found})

    for under, spec in experiments.items():
        if not spec.get("id"):
            continue
        for row in by_folder.get((Level.EXPERIMENT.value, under)) or []:
            if row["project_id"] == spec.get("project_id"):
                targets[row["path"]] = spec["id"]
    return built, targets


#: A move the server refused for good: the artifact or its target is gone (404),
#: a file identical to it is already there (409), or the move is not one the
#: server allows from where the file now is -- a person filed it elsewhere (422).
FINAL_MOVE_STATUSES = (404, 409, 422)


def file_delivered(coverage, client, *, report=None) -> dict:
    """Move every delivered file not yet at its run or experiment there.

    The artifact keeps its id and its bytes; only where it is filed changes. A
    file whose upload has not landed waits for the next pass; a changed file's
    new upload (a new artifact) is filed again. A move the server refuses for
    good is recorded and not retried.
    """
    pending = coverage.unfiled()
    if not pending:
        return {"files_filed": 0, "files_filing_failed": 0}
    filed, failed = file_moves(client, pending)
    for path, artifact_id, target_id in filed:
        coverage.filed(path, target_id, artifact_id)
    for path, artifact_id, error, final in failed:
        if final:
            coverage.filing_refused(path, artifact_id, error)
        else:
            # It may have moved part of the way (up to its project, then the
            # step down failed): where it sits is unknown, so the next pass
            # sends its move again whatever it was last filed as.
            coverage.filing_unknown(path)
    if report is not None:
        if filed:
            report.add(f"{len(filed):,} file(s) filed into their runs and experiments "
                       "(no bytes re-sent).")
        if failed:
            report.add(f"{len(failed):,} file(s) could not be filed into their run or experiment; "
                       "they stay at their project (a refused move is not retried):",
                       *[f"  {path}: {error}" for path, _, error, _ in failed[:3]])
    return {"files_filed": len(filed), "files_filing_failed": len(failed)}


def _landed(row: dict | None, level: str, target_id: str) -> bool:
    """Did a move's answer put the artifact at (level, target)? Both storage
    shapes: an experiment's file reads `project_id = E` until R6, or
    `experiment_id = E` beside its project."""
    if not isinstance(row, dict):
        return True  # an answer without a body: nothing says otherwise
    if level == Level.RUN.value:
        return str(row.get("run_id")) == str(target_id)
    if level == Level.EXPERIMENT.value:
        return row.get("run_id") is None and target_id in (
            str(row.get("experiment_id")), str(row.get("project_id")))
    return (row.get("run_id") is None and not row.get("experiment_id")
            and str(row.get("project_id") or target_id) == str(target_id))


def file_moves(client, moves) -> tuple[list[tuple[str, str, str]], list[tuple[str, str, str, bool]]]:
    """Move artifacts to their run, experiment or project. Data in, no store.

    `moves` are `(path, artifact id, level, target id)`. Returns the moves made,
    `(path, artifact id, target id)`, and the ones refused,
    `(path, artifact id, error, final)`: `final` when the server refused for
    good (`FINAL_MOVE_STATUSES`), so the caller does not offer it again.

    The server moves a file only along its own chain: up to an ancestor, or
    down into its own subtree; run to run is refused (422). A file a re-plan
    takes from one run (or experiment) to another goes up to its project
    first, then down to its target. A move counts only where the server's
    answer says the file landed.
    """
    from ..sdk import errors

    def move(item):
        path, artifact_id, level, target_id = item
        try:
            try:
                row = client.move_artifact(artifact_id, level=level, target_id=target_id)
            except errors.RosError as exc:
                if exc.status != 422 or level == Level.PROJECT.value:
                    raise
                # Not in the target's subtree: up to the project, then down.
                client.move_artifact(artifact_id, level=Level.PROJECT.value)
                row = client.move_artifact(artifact_id, level=level, target_id=target_id)
            if not _landed(row, level, target_id):
                # The server put it somewhere else (a person moved its run,
                # say): asking again would land it there again.
                return item, f"the server filed it elsewhere ({level} {target_id} asked)", True
            return item, None, False
        except Exception as exc:  # noqa: BLE001 - recorded per file
            final = isinstance(exc, errors.RosError) and exc.status in FINAL_MOVE_STATUSES
            return item, str(exc)[:300], final

    filed: list[tuple[str, str, str]] = []
    failed: list[tuple[str, str, str, bool]] = []
    with ThreadPoolExecutor(max_workers=FILE_WORKERS) as pool:
        for (path, artifact_id, _, target_id), error, final in pool.map(move, list(moves)):
            if error is None:
                filed.append((path, artifact_id, target_id))
            else:
                failed.append((path, artifact_id, error, final))
    return filed, failed


def restructure_candidates(coverage, *, version: int = STRUCTURE_VERSION) -> dict[str, str]:
    """Files imported before this folder's plan named experiments and runs.

    path -> project slug, for delivered (or referenced) files with a project.
    Empty once a plan has been made, or declined, under `version` or later.
    """
    if reviewed_version(coverage.meta(REVIEWED_KEY)) >= version:
        return {}
    report = coverage.report()
    done = set(report["delivered"]) | set(report["references"])
    return {row["path"]: row["project_slug"] for row in coverage.rows()
            if row["path"] in done and row["project_id"] and row["project_slug"]}


__all__ = [
    "STRUCTURE_VERSION", "Built", "Ended", "Level", "RUN_SOURCE", "Resolved", "RunRecord",
    "build", "build_plan", "counts_line", "decline", "describe", "external_id",
    "file_delivered", "file_moves", "merge_planned",
    "is_config_file", "is_result_file", "metric_points", "plan_json", "read_run", "remember",
    "resolve", "restructure_candidates", "reviewed_version", "run_candidates",
]
