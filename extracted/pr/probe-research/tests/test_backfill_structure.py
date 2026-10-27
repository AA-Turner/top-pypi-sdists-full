"""Experiments and runs from a folder import: the model names folders, code builds them.

Real files and real parsing throughout. The model's judgement is faked through
the REAL `probe-backfill-plan` launcher (`backfill_plan_agent.tool`), and the
server is faked only at the HTTP boundary (`FakeAPI` stands in for the
transport's post/get/patch); the walk, the census, the coverage store, the
outbox and its receipts are the real ones (`test_backfill_scoped_orchestration`'s
harness). `tests/integration/test_backfill_structure_e2e.py` runs `build` and
`file_delivered` against a real server.
"""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

import pytest

from backfill_plan_agent import tool

from probe.cli import backfill as bf
from probe.cli import backfill_plan as plans
from probe.cli import backfill_plan_tool as t
from probe.cli import backfill_run as runner
from probe.cli import backfill_structure as structure
from probe.cli import telemetry, tui
from probe.sdk import errors

from test_backfill_scoped_orchestration import make_harness

REAL_CLASSIFY = runner.classify

#: 2026-09-01 12:00 UTC and later, so every mtime in a run folder is known.
T0 = 1_788_264_000


def _write(root: Path, rel: str, text: str, mtime: int) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    os.utime(path, (mtime, mtime))


def customer_tree(root: Path) -> None:
    """Shaped like team tokenless's `runs/<name>/` folders of eval output."""
    _write(root, "runs/a/reward.json", json.dumps({"reward": 0.75}), T0)
    _write(root, "runs/a/trial.log", "started\nfinished\n", T0 + 60)
    _write(root, "runs/b/reward.txt", "1\n", T0 + 100)
    _write(root, "runs/c/bench-runner-result.json",
           json.dumps({"accuracy": 0.5, "n_tasks": 10, "status": "completed",
                       "label": "kept as text, not a metric", "flag": True}), T0 + 200)
    _write(root, "runs/c/config.toml",
           'lr = 0.001\nmodel = "glm-flash"\nseed = 7\n[agent]\nturns = 30\n', T0 + 190)
    _write(root, "runs/c/run.log", "step 1\nstep 2\n", T0 + 250)
    _write(root, "runs/c/events.jsonl", '{"event": "start"}\n{"event": "stop"}\n', T0 + 240)
    _write(root, "runs/d/notes.md", "# nothing parseable here\n", T0 + 300)
    _write(root, "README.md", "# evals\n", T0 + 400)


# -- reading a run ---------------------------------------------------------------


def test_a_run_is_read_from_its_files_and_nothing_else(tmp_path):
    customer_tree(tmp_path)
    files = ["runs/c/bench-runner-result.json", "runs/c/config.toml", "runs/c/run.log",
             "runs/c/events.jsonl"]
    record = structure.read_run(tmp_path, "runs/c", files)
    assert record.name == "c"
    assert record.metrics == {"accuracy": 0.5, "n_tasks": 10}
    # Top-level scalars only: the [agent] table is not a config value.
    assert record.config == {"lr": 0.001, "model": "glm-flash", "seed": 7}
    assert record.status is structure.Ended.COMPLETED
    assert record.started_at == "2026-09-01T12:03:10+00:00"
    assert record.ended_at == "2026-09-01T12:04:10+00:00"
    assert record.provenance["read_from"] == {
        "metrics": ["runs/c/bench-runner-result.json"],
        "config": ["runs/c/config.toml"],
        "status": ["runs/c/bench-runner-result.json"],
    }


def test_a_lone_number_file_is_a_metric_and_no_status_is_claimed(tmp_path):
    customer_tree(tmp_path)
    record = structure.read_run(tmp_path, "runs/b", ["runs/b/reward.txt"])
    assert record.metrics == {"reward": 1}
    assert record.status is structure.Ended.UNKNOWN
    assert record.status.value == "untracked"


def test_a_folder_with_nothing_parseable_is_a_run_with_no_metrics(tmp_path):
    customer_tree(tmp_path)
    record = structure.read_run(tmp_path, "runs/d", ["runs/d/notes.md"])
    assert record.metrics == {} and record.config == {}
    assert record.status is structure.Ended.UNKNOWN
    assert record.started_at == record.ended_at == "2026-09-01T12:05:00+00:00"


@pytest.mark.parametrize("payload, expected", [
    ({"success": False}, "failed"),
    ({"passed": True}, "completed"),
    ({"exit_code": 0}, "completed"),
    ({"exit_code": 2}, "failed"),
    ({"outcome": "cancelled"}, "canceled"),
    ({"outcome": "weird"}, "untracked"),
    # Two fields that disagree claim nothing.
    ({"success": True, "exit_code": 1}, "untracked"),
])
def test_status_comes_only_from_an_explicit_field(tmp_path, payload, expected):
    _write(tmp_path, "r/outcome.json", json.dumps(payload), T0)
    assert structure.read_run(tmp_path, "r", ["r/outcome.json"]).status.value == expected


def test_nested_result_files_keep_their_place_and_never_merge(tmp_path):
    """Trials three levels down: each number keyed by where it sits, none averaged,
    and a trial's outcome is not the run's."""
    _write(tmp_path, "r/trials/01-x/verifier/reward.txt", "1", T0)
    _write(tmp_path, "r/trials/02-y/verifier/reward.txt", "0", T0 + 1)
    _write(tmp_path, "r/trials/02-y/result.json", json.dumps({"status": "failed", "steps": 4}), T0 + 2)
    _write(tmp_path, "r/reward.json", json.dumps({"reward": 0.5}), T0 + 3)
    _write(tmp_path, "r/reward.txt", "0.25", T0 + 4)
    files = ["r/trials/01-x/verifier/reward.txt", "r/trials/02-y/verifier/reward.txt",
             "r/trials/02-y/result.json", "r/reward.json", "r/reward.txt"]
    record = structure.read_run(tmp_path, "r", files)
    assert record.metrics == {
        "trials/01-x/verifier/reward": 1,
        "trials/02-y/verifier/reward": 0,
        "trials/02-y/steps": 4,
        # Two root files both say "reward": both kept, each under its file.
        "reward.json": 0.5,
        "reward.txt": 0.25,
    }
    assert record.status is structure.Ended.UNKNOWN


def test_yaml_config_reads_top_level_scalars_only(tmp_path):
    _write(tmp_path, "r/config.yaml",
           "lr: 3e-4\nname: 'base'\nuse_amp: true\nlayers:\n  - 1\nopt:\n  beta: 0.9\n", T0)
    record = structure.read_run(tmp_path, "r", ["r/config.yaml"])
    assert record.config == {"lr": 3e-4, "name": "base", "use_amp": True}


# -- selecting through the plan tool -----------------------------------------------


def _ref(files, projects=("evals",), **extra):
    return t.Reference(root="/data", mode=t.Mode.CLASSIFY, files=tuple(files),
                       projects=tuple(projects), **extra)


FILES = ["runs/a/reward.json", "runs/a/trial.log", "runs/b/reward.txt",
         "runs/c/bench-runner-result.json", "runs/c/config.toml", "runs/d/notes.md", "README.md"]


def test_each_under_makes_one_run_per_folder_in_one_call():
    ref = _ref(FILES)
    state = t.initial_state(ref)
    t.apply(ref, state, {"op": "assign", "project": "evals", "rest": True})
    msg = t.apply(ref, state, {"op": "run", "each_under": "runs"})
    assert msg == "4 runs (runs)"
    assert sorted(state.runs) == ["runs/a", "runs/b", "runs/c", "runs/d"]


def test_a_missing_directory_is_refused_with_the_nearest_real_one():
    ref = _ref(FILES)
    state = t.initial_state(ref)
    t.apply(ref, state, {"op": "assign", "project": "evals", "rest": True})
    with pytest.raises(t.Refused, match="nearest: runs"):
        t.apply(ref, state, {"op": "run", "each_under": "rnus"})
    with pytest.raises(t.Refused, match="nearest: runs/a"):
        t.apply(ref, state, {"op": "run", "under": "runs/aa"})
    # ... and the model can retry: the corrected call is accepted.
    assert t.apply(ref, state, {"op": "run", "under": "runs/a"}) == "1 run (runs/a)"


def test_an_unassigned_directory_is_refused_until_its_files_are_assigned():
    ref = _ref(FILES)
    state = t.initial_state(ref)
    with pytest.raises(t.Refused, match="undecided; assign them first"):
        t.apply(ref, state, {"op": "experiment", "slug": "calib", "project": "evals",
                             "question": "Does calibration hold?", "under": "runs"})
    with pytest.raises(t.Refused, match="cannot be runs yet"):
        t.apply(ref, state, {"op": "run", "each_under": "runs"})
    t.apply(ref, state, {"op": "assign", "project": "evals", "under": "runs"})
    t.apply(ref, state, {"op": "experiment", "slug": "calib", "project": "evals",
                         "question": "Does calibration hold?", "under": "runs"})
    assert t.apply(ref, state, {"op": "run", "each_under": "runs", "experiment": "calib"}) \
        == "4 runs in experiment calib (runs)"


def test_a_run_holds_one_project_and_runs_do_not_nest():
    ref = _ref(FILES, projects=("evals", "other"))
    state = t.initial_state(ref)
    t.apply(ref, state, {"op": "assign", "project": "evals", "under": "runs"})
    t.apply(ref, state, {"op": "assign", "project": "other", "file": "runs/a/trial.log"})
    with pytest.raises(t.Refused, match=r"runs/a \(files in evals, other\)"):
        t.apply(ref, state, {"op": "run", "under": "runs/a"})
    t.apply(ref, state, {"op": "run", "under": "runs/b"})
    t.apply(ref, state, {"op": "assign", "project": "evals", "file": "runs/a/trial.log"})
    with pytest.raises(t.Refused, match="overlaps run runs/b"):
        t.apply(ref, state, {"op": "run", "under": "runs"})
    with pytest.raises(t.Refused, match="is a file"):
        t.apply(ref, state, {"op": "run", "under": "runs/b/reward.txt"})
    with pytest.raises(t.Refused, match="is not an experiment here"):
        t.apply(ref, state, {"op": "run", "under": "runs/c", "experiment": "nope"})


def test_already_imported_files_keep_their_project():
    ref = _ref(FILES, fixed=("runs/a/reward.json",),
               seed={"runs/a/reward.json": {"kind": "assigned", "project": "old"}},
               projects=("evals", "old"))
    state = t.initial_state(ref)
    msg = t.apply(ref, state, {"op": "assign", "project": "evals", "under": "runs/a"})
    assert msg.endswith("1 already imported stay in their project")
    assert state.decided["runs/a/reward.json"].project == "old"


def test_the_log_replays_structure_through_the_same_checks():
    ref = _ref(FILES)
    lines = [json.dumps(op) for op in (
        {"op": "assign", "project": "evals", "rest": True},
        {"op": "run", "each_under": "runs"},
        {"op": "run", "each_under": "nowhere"},  # written by hand: refused on replay
    )]
    state = t.replay(ref, lines)
    assert sorted(state.runs) == ["runs/a", "runs/b", "runs/c", "runs/d"]
    assert state.invalid == 1


# -- the plan the person approves -----------------------------------------------------


def _plan(experiments=None, runs=None, assigned=None):
    plan = plans.Plan(projects=[plans.ProjectSpec("evals")], assignments=[])
    plan.experiments = experiments or {}
    plan.runs = runs or {}
    return plan, assigned or {f: "evals" for f in FILES}


def test_the_plan_counts_experiments_and_runs_per_project():
    plan, assigned = _plan(
        experiments={"calib": {"slug": "calib", "project": "evals", "name": "Calibration",
                               "question": "Does it hold?", "under": "runs"}},
        runs={d: {"under": d, "experiment": "calib", "project": "evals"}
              for d in ("runs/a", "runs/b", "runs/c", "runs/d")},
    )
    resolved = structure.resolve(plan, assigned)
    assert structure.counts_line(1, resolved) == "1 project · 1 experiment · 4 runs"
    assert resolved.per_project() == {"evals": {"experiments": 1, "runs": 4}}
    assert resolved.targets["runs/c/config.toml"] == (structure.Level.RUN, "runs/c")
    assert "README.md" not in resolved.targets
    as_json = structure.plan_json(assigned, resolved)
    assert as_json["totals"] == {"files": 7, "projects": 1, "experiments": 1, "runs": 4,
                                 "left_out": 0, "already_imported": 0}
    assert as_json["projects"] == [{"slug": "evals", "files": 7, "experiments": 1, "runs": 4}]
    assert [r["folder"] for r in as_json["runs"]] == ["runs/a", "runs/b", "runs/c", "runs/d"]
    assert {r["experiment"] for r in as_json["runs"]} == {"calib"}


def test_a_run_whose_files_were_moved_apart_is_dropped_not_split():
    assigned = {f: "evals" for f in FILES} | {"runs/a/trial.log": "other"}
    plan, _ = _plan(runs={"runs/a": {"under": "runs/a"}, "runs/b": {"under": "runs/b"}})
    resolved = structure.resolve(plan, assigned)
    assert sorted(resolved.runs) == ["runs/b"] and resolved.dropped_runs == 1
    assert "runs/a/reward.json" not in resolved.targets


# -- after approval: the import, end to end (fakes only at HTTP) ------------------------


class _Response:
    def __init__(self, body: dict, headers: dict | None = None):
        self.body, self.headers = body, headers or {}

    def json(self):
        return self.body


class FakeAPI:
    """The server, at the transport: experiments, runs, and artifact moves."""

    def __init__(self, transport):
        self.transport = transport
        self.real = {name: getattr(transport, name) for name in ("post", "get", "patch")}
        self.experiments: dict[str, dict] = {}
        self.runs: dict[str, dict] = {}
        self.moves: list[tuple[str, str, str]] = []
        self.writes: list[tuple[str, str]] = []

    def install(self, monkeypatch):
        for name in ("post", "get", "patch", "request"):
            monkeypatch.setattr(self.transport, name, getattr(self, name))
        self.real["request"] = type(self.transport).request.__get__(self.transport)

    def request(self, method, path, *, json_body=None, **kwargs):
        if method == "POST" and path.endswith("/runs") and path.startswith("/v1/projects/"):
            # 0268: the same creation key answers with the run it made.
            for row in self.runs.values():
                if row.get("creation_key") == json_body.get("creation_key"):
                    self.writes.append(("POST", path))
                    return _Response(dict(row), {"Idempotent-Replay": "true"})
            return _Response(self.post(path, json_body))
        return self.real["request"](method, path, json_body=json_body, **kwargs)

    def post(self, path, json_body=None, **kwargs):
        parts = path.strip("/").split("/")
        if parts[:2] == ["v1", "projects"] and parts[3:] == ["experiments"]:
            self.writes.append(("POST", path))
            for row in self.experiments.values():
                if row["slug"] == json_body["slug"]:
                    raise errors.ConflictError("taken", detail={"existing": {
                        "id": row["id"], "kind": "experiment", "parent_project_id": row["project_id"]}})
            row = {"id": str(uuid.uuid4()), "project_id": parts[2], **json_body}
            self.experiments[row["id"]] = row
            return dict(row)
        if parts[:2] == ["v1", "projects"] and parts[3:] == ["runs"]:
            self.writes.append(("POST", path))
            for row in self.runs.values():
                if (row["source"], row["external_id"]) == (json_body["source"], json_body["external_id"]):
                    raise errors.ConflictError("exists", detail={"existing_id": row["id"]})
            row = {"id": str(uuid.uuid4()), "target": parts[2], "status": "running",
                   "ended_at": None, "summary_metrics": {}, **json_body}
            self.runs[row["id"]] = row
            return dict(row)
        if parts[:2] == ["v1", "artifacts"] and parts[3:] == ["move"]:
            self.writes.append(("POST", path))
            self.moves.append((parts[2], json_body["level"], json_body["target_id"]))
            return {"id": parts[2]}
        return self.real["post"](path, json_body, **kwargs)

    def get(self, path, **kwargs):
        parts = path.strip("/").split("/")
        if parts[:2] == ["v1", "runs"] and len(parts) == 3:
            row = dict(self.runs[parts[2]])
            experiment = self.experiments.get(row["target"])
            row["experiment_id"] = experiment["id"] if experiment else None
            row["project_id"] = experiment["project_id"] if experiment else row["target"]
            return row
        return self.real["get"](path, **kwargs)

    def patch(self, path, json_body):
        parts = path.strip("/").split("/")
        if parts[:2] == ["v1", "runs"] and len(parts) == 3:
            self.writes.append(("PATCH", path))
            row = self.runs[parts[2]]
            for key in ("status", "ended_at", "summary_metrics"):
                if key in json_body:
                    row[key] = json_body[key]
            for key in ("experiment_id", "project_id"):
                if key in json_body:
                    row["target"] = json_body[key]
            row["config"] = {**row.get("config", {}), **json_body.get("config_merge", {})}
            return dict(row)
        return self.real["patch"](path, json_body)

    def by_name(self) -> dict[str, dict]:
        return {row["name"]: row for row in self.runs.values()}


def _classifier(structure_ops=True, seen=None):
    """A model that files the folder through the real tool: one project, and
    (when asked) one experiment over `runs/` with each folder a run."""

    def launch(folder, prompt, **kwargs):
        if "Decide which project each file" not in prompt:
            return True, ""  # an upload unit: notes are optional
        if seen is not None:
            seen.append(prompt)
        tool(kwargs, "project", "evals", "--name", "Evals", "--description", "Eval runs.")
        tool(kwargs, "assign", "evals", "--rest")
        if structure_ops:
            code, out = tool(kwargs, "experiment", "--slug", "calib", "--project", "evals",
                             "--name", "Calibration", "--question",
                             "Does the model stay calibrated?", "--under", "runs")
            assert code == 0, out
            code, out = tool(kwargs, "run", "--each-under", "runs", "--experiment", "calib")
            assert code == 0, out
        return True, ""

    return launch


@pytest.fixture
def harness(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_FLUSH_ATTEMPTS", "1")
    h = make_harness(tmp_path, monkeypatch)
    for path in list(h.folder.iterdir()):
        path.unlink()
    customer_tree(h.folder)
    monkeypatch.setattr(runner, "classify", REAL_CLASSIFY)
    api = FakeAPI(h.client.transport)
    api.install(monkeypatch)
    h.api = api
    return h


def test_the_import_creates_experiments_and_runs_after_approval_and_files_each_upload_once(
    harness, monkeypatch,
):
    h = harness
    monkeypatch.setattr(bf, "launch_agent", _classifier())
    shown: list[list[str]] = []

    def review(title, lines, choices):
        if title == "Review the import plan":
            # NOTHING exists before the person approves.
            assert not h.api.runs and not h.api.experiments
            shown.append(list(lines))
        return choices[0][1]

    monkeypatch.setattr(tui, "review", review)
    h.run(interactive=True, yes=False)
    screen = "\n".join(shown[0])
    assert "1 project · 1 experiment · 4 runs" in screen
    assert "evals" in screen and "· 1 experiment · 4 runs" in screen
    plan_file = next(line.split(": ", 1)[1] for line in shown[0] if line.startswith("Plan as JSON"))
    as_json = json.loads(Path(plan_file).read_text())
    assert as_json["totals"]["experiments"] == 1 and as_json["totals"]["runs"] == 4

    # Created after approval, every value read from the files.
    (experiment,) = h.api.experiments.values()
    assert (experiment["slug"], experiment["question"]) == ("calib", "Does the model stay calibrated?")
    runs = h.api.by_name()
    assert sorted(runs) == ["a", "b", "c", "d"]
    assert {row["target"] for row in runs.values()} == {experiment["id"]}
    assert runs["a"]["summary_metrics"] == {"reward": 0.75}
    assert runs["b"]["summary_metrics"] == {"reward": 1}
    assert runs["c"]["summary_metrics"] == {"accuracy": 0.5, "n_tasks": 10}
    assert runs["d"]["summary_metrics"] == {}
    assert runs["c"]["config"] == {"lr": 0.001, "model": "glm-flash", "seed": 7}
    assert runs["c"]["status"] == "completed"
    assert {runs[n]["status"] for n in "abd"} == {"untracked"}
    assert runs["a"]["started_at"] == "2026-09-01T12:00:00+00:00"
    assert runs["a"]["ended_at"] == "2026-09-01T12:01:00+00:00"
    assert runs["c"]["started_at"] == "2026-09-01T12:03:10+00:00"
    assert runs["c"]["ended_at"] == "2026-09-01T12:04:10+00:00"
    assert {row["source"] for row in runs.values()} == {"backfill"}
    assert runs["a"]["metadata"]["backfill"]["relative_path"] == "runs/a"
    summary = [data for event, data in h.events if event == telemetry.EVENT_BACKFILL_SUMMARY][-1]
    assert summary["runs_created"] == 4 and summary["runs_zero_metrics"] == 1
    assert summary["experiments_created"] == 1
    approved = [data for event, data in h.events if event == telemetry.EVENT_BACKFILL_APPROVED][-1]
    assert (approved["experiments_approved"], approved["runs_approved"]) == (1, 4)
    ready = [data for event, data in h.events if event == telemetry.EVENT_BACKFILL_PLAN_READY][-1]
    assert (ready["experiments_proposed"], ready["runs_proposed"]) == (1, 4)

    # Uploaded once, at the project; then each file moved to its run.
    assert h.drain().delivered == 9
    h.run()
    uploads = len(h.remote.calls)
    assert uploads == 9
    by_run = {row["id"]: name for name, row in runs.items()}
    moved = {}
    with h.coverage().writer() as coverage:
        receipts = {row["path"]: row for row in coverage.rows()}
        artifact_of = {}
        for path, row in receipts.items():
            found = coverage.conn.execute(
                "SELECT receipt FROM versions WHERE correlation=?", (row["correlation"],)).fetchone()
            artifact_of[json.loads(found[0])["artifact_id"]] = path
    for artifact, level, target in h.api.moves:
        moved[artifact_of[artifact]] = (level, by_run.get(target, target))
    assert moved == {
        "runs/a/reward.json": ("run", "a"), "runs/a/trial.log": ("run", "a"),
        "runs/b/reward.txt": ("run", "b"),
        "runs/c/bench-runner-result.json": ("run", "c"), "runs/c/config.toml": ("run", "c"),
        "runs/c/run.log": ("run", "c"), "runs/c/events.jsonl": ("run", "c"),
        "runs/d/notes.md": ("run", "d"),
    }  # README.md stays at the project

    # Applying again creates nothing, writes nothing, uploads nothing.
    before = list(h.api.writes)
    h.run()
    assert h.api.writes == before and len(h.remote.calls) == uploads


def test_a_lost_create_response_finds_its_run_instead_of_making_another(harness, monkeypatch):
    """The local record is gone (another machine, a wiped state dir): the run's
    identity is its folder in this import, so the server's 409 names it."""
    h = harness
    monkeypatch.setattr(bf, "launch_agent", _classifier())
    h.run()
    first = dict(h.api.runs)
    with h.coverage().writer() as coverage:
        saved = coverage.meta(structure.META_KEY)
        for spec in saved["runs"].values():
            spec.pop("id"), spec.pop("digest"), spec.pop("target_id")
        coverage.put_meta(structure.META_KEY, saved)
    h.run()
    assert h.api.runs.keys() == first.keys()
    summary = [data for event, data in h.events if event == telemetry.EVENT_BACKFILL_SUMMARY][-1]
    assert (summary["runs_created"], summary["runs_existing"], summary["runs_updated"]) == (0, 4, 0)


def test_a_reimport_organizes_files_uploaded_before_without_uploading_them_again(
    harness, monkeypatch,
):
    h = harness
    # Imported by a CLI that could not make runs: files land at the project.
    monkeypatch.setattr(bf, "launch_agent", _classifier(structure_ops=False))
    h.run()
    assert h.drain().delivered == 9
    h.run()
    with h.coverage().writer() as coverage:
        coverage.put_meta(structure.REVIEWED_KEY, None)  # as a pre-feature store reads
    uploads = len(h.remote.calls)
    assert not h.api.runs

    prompts: list[str] = []
    monkeypatch.setattr(bf, "launch_agent", _classifier(seen=prompts))
    h.run()
    assert "9 of these files were imported before" in prompts[-1]
    assert sorted(h.api.by_name()) == ["a", "b", "c", "d"]
    assert len(h.api.moves) == 8
    assert len(h.remote.calls) == uploads, "a re-import must never upload a file again"
    with h.coverage().writer() as coverage:
        assert not coverage.unfiled()
    # And the next import asks nothing again.
    h.run()
    assert len(prompts) == 1


def test_a_failed_organize_pass_neither_fails_the_import_nor_settles_it(harness, monkeypatch):
    """An agent that dies before naming anything over files imported before
    leaves them as they were, says so, and the next import asks again."""
    h = harness
    monkeypatch.setattr(bf, "launch_agent", _classifier(structure_ops=False))
    h.run()
    assert h.drain().delivered == 9
    h.run()
    with h.coverage().writer() as coverage:
        coverage.put_meta(structure.REVIEWED_KEY, None)
    monkeypatch.setattr(bf, "launch_agent", lambda folder, prompt, **kw: (False, "agent crashed"))
    lines = h.run()
    assert any("could not be organized into experiments and runs" in line for line in lines)
    assert not h.api.runs and not h.api.moves
    with h.coverage().writer() as coverage:
        assert not coverage.meta(structure.REVIEWED_KEY)
    prompts: list[str] = []
    monkeypatch.setattr(bf, "launch_agent", _classifier(seen=prompts))
    h.run()
    assert prompts and sorted(h.api.by_name()) == ["a", "b", "c", "d"]


def _artifact_paths(h) -> dict[str, str]:
    """artifact id -> path, from the import's own receipts."""
    out = {}
    with h.coverage().writer() as coverage:
        for row in coverage.rows():
            found = coverage.conn.execute(
                "SELECT receipt FROM versions WHERE correlation=?", (row["correlation"],)).fetchone()
            if found and found[0]:
                out[json.loads(found[0])["artifact_id"]] = row["path"]
    return out


def test_a_changed_file_is_filed_again_and_its_run_reads_the_new_value(harness, monkeypatch):
    h = harness
    monkeypatch.setattr(bf, "launch_agent", _classifier())
    h.run()
    h.drain()
    h.run()
    first_moves = len(h.api.moves)
    (h.folder / "runs/a/reward.json").write_text(json.dumps({"reward": 0.9}))
    h.run(import_changed=True)
    assert h.drain().delivered == 1
    h.run()
    new = h.api.moves[first_moves:]
    paths = _artifact_paths(h)
    assert [paths[artifact] for artifact, _, _ in new] == ["runs/a/reward.json"]
    assert h.api.by_name()["a"]["summary_metrics"] == {"reward": 0.9}


def test_files_left_as_they_were_never_join_a_run_named_later(harness, monkeypatch):
    """Declining to organize old uploads keeps them out of every later run: a
    run is read from, and holds, only the files a plan approved for it."""
    h = harness
    monkeypatch.setattr(bf, "launch_agent", _classifier(structure_ops=False))
    h.run()
    h.drain()
    h.run()
    with h.coverage().writer() as coverage:
        coverage.put_meta(structure.REVIEWED_KEY, None)

    def review(title, lines, choices):
        return False if title == "Organize imported files" else choices[0][1]

    monkeypatch.setattr(tui, "review", review)
    _write(h.folder, "runs/a/extra/reward.txt", "2\n", T0 + 500)
    _write(h.folder, "runs/e/reward.txt", "3\n", T0 + 600)
    monkeypatch.setattr(bf, "launch_agent", _classifier())
    h.run(interactive=True, yes=False)
    h.drain()
    h.run()
    runs = h.api.by_name()
    # The classifier saw only the two new files: run a holds the new one only,
    # run e its own; the eight older files stay where they were.
    assert sorted(runs) == ["a", "e"]
    assert runs["a"]["summary_metrics"] == {"extra/reward": 2}
    paths = _artifact_paths(h)
    assert sorted(paths[artifact] for artifact, _, _ in h.api.moves) == [
        "runs/a/extra/reward.txt", "runs/e/reward.txt"]


def test_copied_folders_claim_no_times(tmp_path):
    customer_tree(tmp_path)
    record = structure.read_run(tmp_path, "runs/a", ["runs/a/reward.json", "runs/a/trial.log"],
                                times=False)
    assert record.started_at is None and record.ended_at is None
    assert record.provenance["times"].startswith("unknown")
    assert record.metrics == {"reward": 0.75}


def test_two_slices_choosing_one_slug_for_different_folders_make_two_experiments():
    def pass_of(experiments, runs):
        ref = _ref(FILES)
        state = t.initial_state(ref)
        state.experiments, state.runs = experiments, runs
        return runner.ToolPass(ref, state, runner.SessionOutcome.COMPLETE)

    first = pass_of({"base": {"slug": "base", "project": "evals", "under": "runs/a"}},
                    {"runs/a": {"under": "runs/a", "experiment": "base"}})
    second = pass_of({"base": {"slug": "base", "project": "evals", "under": "runs/b"}},
                     {"runs/b": {"under": "runs/b", "experiment": "base"}})
    plan = runner._plan_from_passes([first, second], [])
    assert {slug: spec["under"] for slug, spec in plan.experiments.items()} == {
        "base": "runs/a", "base-2": "runs/b"}
    assert plan.runs["runs/b"]["experiment"] == "base-2"
    assert plan.runs["runs/a"]["experiment"] == "base"


def test_a_move_the_server_refuses_for_good_is_not_retried(harness, monkeypatch):
    h = harness
    monkeypatch.setattr(bf, "launch_agent", _classifier())
    h.run()
    h.drain()
    calls = []

    def refuse(artifact_id, *, level, target_id=None):
        calls.append(artifact_id)
        raise errors.RosError("lateral move refused", status=422)

    monkeypatch.setattr(h.client, "move_artifact", refuse)
    lines = h.run()
    assert len(calls) == 8 and any("could not be filed" in line for line in lines)
    h.run()
    assert len(calls) == 8, "a refused move must not be sent again"


def test_a_pathological_result_file_costs_its_values_not_the_import(tmp_path):
    _write(tmp_path, "r/result.json", "[" * 100_000 + "]" * 100_000, T0)
    _write(tmp_path, "r/config.yaml", 'name: "exp #3"\nlr: 1e-3 # tuned\n', T0)
    record = structure.read_run(tmp_path, "r", ["r/result.json", "r/config.yaml"])
    assert record.metrics == {}
    assert record.config == {"name": "exp #3", "lr": 1e-3}


def test_a_long_colliding_slug_still_gets_a_distinct_number():
    slug = "x" * 63

    def pass_of(under):
        ref = _ref(FILES)
        state = t.initial_state(ref)
        state.experiments = {slug: {"slug": slug, "project": "evals", "under": under}}
        return runner.ToolPass(ref, state, runner.SessionOutcome.COMPLETE)

    plan = runner._plan_from_passes([pass_of("runs/a"), pass_of("runs/b"), pass_of("runs/c")], [])
    assert sorted(len(s) for s in plan.experiments) == [63, 63, 63]
    assert len(plan.experiments) == 3


def test_someone_elses_experiment_with_the_slug_is_never_adopted():
    holder = {"id": "theirs", "kind": "experiment", "parent_project_id": "p1"}

    class Client:
        made: list[str] = []

        def create_experiment(self, slug, name, **kw):
            if slug == "calib":
                raise errors.ConflictError("taken", detail={"existing": holder})
            self.made.append(slug)
            return {"id": "ours"}

    spec = {"slug": "calib", "question": "q?"}
    assert structure._create_experiment(Client(), spec, "p1", lambda: None) == "ours"
    assert Client.made == ["calib-2"] and spec["foreign"] == ["calib"]
    # A later pass (the answer to `calib-2` lost, say) still never takes `calib`.
    assert structure._create_experiment(Client(), spec, "p1", lambda: None) == "ours"
    assert Client.made == ["calib-2", "calib-2"]


def test_a_yaml_block_header_with_a_comment_is_not_a_value(tmp_path):
    _write(tmp_path, "r/config.yml", "optimizer:  # settings\n  lr: 1\nseed: 3 # fixed\n", T0)
    assert structure.read_run(tmp_path, "r", ["r/config.yml"]).config == {"seed": 3}
