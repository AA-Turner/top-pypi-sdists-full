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
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from probe.cli.imports.folder.structure.resolution import Level, META_KEY
from probe.cli.imports.folder.structure.run_records import RunRecord, read_run
from probe.sdk.routes import WriteOp, path_for

#: `runs.source` for every run an import creates. The provenance word.
RUN_SOURCE = "backfill"
#: The server's mark on a create it answered with an earlier run (0268).
REPLAY_HEADER = "Idempotent-Replay"


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
    from .....sdk import agent_session, errors

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
    client.transport.patch(path_for(WriteOp.RUN_PATCH, run_id), want)
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
    from .....sdk import errors

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
        response = client.transport.request("POST", f"/v1/projects/{target_id}/runs",
                                        json_body=body, idempotent=True)
        # The same request again (a lost answer, a wiped local record) is
        # answered with the run it made, marked as a replay: found, not new.
        return str(response.json()["id"]), response.headers.get(REPLAY_HEADER, "").lower() != "true"
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
            answer = client.transport.post(path_for(WriteOp.METRICS, run_id), {"points": todo})
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
