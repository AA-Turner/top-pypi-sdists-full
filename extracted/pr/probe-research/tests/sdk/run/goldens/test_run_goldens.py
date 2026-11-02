"""Goldens for the run's write path: opening a run (`Client.run` -> `_run_impl`, the conflict
policy), `Run.log` (flattening, point shapes) and the close (`finish`, `set_status`). Each scenario
records every request the fake API saw, the warnings, and what the call returned or raised."""

from __future__ import annotations

import ast
import functools
import re
import warnings

import pytest

from tests.conftest import make_client
from pathlib import Path

from tests.sdk.delivery.goldens import recorder
from tests.sdk.delivery.goldens.recorder import HttpScript, Normaliser, describe_error

RECORDED = Path(__file__).with_name("recorded")


class RunNormaliser(Normaliser):
    """Also masks the fake API's random run slugs (`run-<hex8>`)."""

    def text(self, value: str) -> str:
        return re.sub(r"\brun-[0-9a-f]{8}\b", "run-<slug>", super().text(value))


def check(name: str, record: dict) -> None:
    recorder.check(name, record, root=RECORDED)


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)


class World:
    def __init__(self, app, tmp_path, monkeypatch, *, async_writes: bool = False):
        self.app = app
        self.norm = RunNormaliser(tmp_path)
        self.http = HttpScript(app.handler, self.norm)
        monkeypatch.setattr(app, "handler", self.http)
        self.client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=async_writes)
        self.client.create_project("lab", kind="general")  # client.run never creates a project
        self.http.log.clear()
        self.steps: list = []

    def call(self, label: str, fn) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                value = fn()
                out = {"value": self.norm.value(_shape(value))}
            except Exception as exc:  # noqa: BLE001 -- the error is the golden
                out = {"error": describe_error(exc, self.norm)}
        out["warnings"] = [f"{_where(w)}: {self.norm.text(str(w.message))}" for w in caught]
        self.steps.append([label, out])

    def open(self, **kw):
        kw.setdefault("heartbeat", False)
        kw.setdefault("snapshot", False)
        return self.client.run(**kw)

    def record(self) -> dict:
        self.client.close()
        return {"steps": self.steps, "requests": self.http.log}


def _where(w) -> str:
    """The file and enclosing function a warning names: proves its stacklevel reaches the same frame."""
    return f"{Path(w.filename).name}:{_enclosing_function(w.filename, w.lineno)}"


@functools.lru_cache(maxsize=None)
def _functions(filename: str) -> tuple:
    try:
        tree = ast.parse(Path(filename).read_text())
    except (OSError, SyntaxError, ValueError):
        return ()
    return tuple((n.lineno, n.end_lineno, n.name) for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))


def _enclosing_function(filename: str, lineno: int) -> str:
    spans = [(start, end, name) for start, end, name in _functions(filename) if start <= lineno <= end]
    return max(spans)[2] if spans else "<module>"


def _shape(value):
    if value is None or isinstance(value, (str, int, float, bool, dict, list)):
        return value
    fields = {k: getattr(value, k, None) for k in ("id", "name", "status", "external_id", "experiment_id", "project_id")}
    return {"<object>": type(value).__name__, **fields}


@pytest.fixture
def world(app, tmp_path, monkeypatch):
    return World(app, tmp_path, monkeypatch)


# -- opening a run ---------------------------------------------------------------------------
def scenario_open_in_a_new_project(w: World):
    w.call("open", lambda: w.open(project="lab", name="r1"))


def scenario_open_with_question_creates_the_experiment(w: World):
    w.call("open", lambda: w.open(project="lab", experiment="exp", question="does it learn?", name="r1"))


def scenario_external_id_auto_resumes(w: World):
    w.call("first", lambda: w.open(project="lab", name="job", external_id="job-1"))
    w.call("again", lambda: w.open(project="lab", name="job", external_id="job-1"))


def scenario_external_id_error_policy(w: World):
    w.call("first", lambda: w.open(project="lab", name="job", external_id="job-2"))
    w.call("again", lambda: w.open(project="lab", name="job", external_id="job-2", on_conflict="error"))


def scenario_external_id_supersede(w: World):
    w.call("first", lambda: w.open(project="lab", name="job", external_id="job-3"))
    w.call("again", lambda: w.open(project="lab", name="job", external_id="job-3", on_conflict="supersede"))


def scenario_external_id_new(w: World):
    w.call("first", lambda: w.open(project="lab", name="job", external_id="job-4"))
    w.call("again", lambda: w.open(project="lab", name="job", external_id="job-4", on_conflict="new"))


def scenario_unknown_conflict_policy(w: World):
    w.call("open", lambda: w.open(project="lab", name="job", external_id="job-5", on_conflict="sideways"))


def scenario_create_refused_then_retried(w: World):
    w.http.answer("POST", r"/runs$", 503, times=1)
    w.call("open", lambda: w.open(project="lab", name="r1"))


def scenario_create_refused_for_good(w: World):
    w.http.answer("POST", r"/runs$", (422, {"detail": "bad run"}), times=5)
    w.call("open", lambda: w.open(project="lab", name="r1"))


def scenario_open_with_config_tags_and_parent(w: World):
    def go():
        parent = w.open(project="lab", name="parent")
        return w.open(project="lab", name="child", config={"lr": 0.1, "nested": {"a": 1}}, tags=["x", "y"],
                      parent_run_id=parent.id)
    w.call("open", go)


# -- Run.log ---------------------------------------------------------------------------------
def scenario_log_flattens_nested_metrics(w: World):
    run = w.open(project="lab", name="r")
    w.call("log", lambda: run.log({"loss": 1.5, "acc": {"top1": 0.5, "top5": {"strict": 0.9}}, "lr": 1e-3}, step=1))
    w.call("log2", lambda: run.log({"acc/top1": 0.6, "acc": {"top5": {"strict": 0.95}}}, step=2))


def scenario_log_value_kinds(w: World):
    run = w.open(project="lab", name="r")
    w.call("log", lambda: run.log({"int": 3, "bool": True, "nan": float("nan"), "inf": float("inf"),
                                   "none": None, "text": "hello", "list": [1, 2], "tuple": (1.0,)}, step=1))


def scenario_log_auto_steps_and_commit(w: World):
    run = w.open(project="lab", name="r")
    w.call("a", lambda: run.log({"loss": 1.0}))
    w.call("b", lambda: run.log({"loss": 0.9}))
    w.call("c", lambda: run.log({"acc": 0.1}, commit=False))
    w.call("d", lambda: run.log({"loss": 0.8}))


def scenario_log_dimensions_labels_kind(w: World):
    run = w.open(project="lab", name="r")
    w.call("dims", lambda: run.log({"loss": 1.0}, step=1, dimensions={"split": "val", "shard": 2}, labels={"note": "x"}))
    w.call("kind", lambda: run.log({"gpu": 50.0}, step=1, kind="system", agg="mean"))


def scenario_log_bad_keys(w: World):
    run = w.open(project="lab", name="r")
    w.call("empty", lambda: run.log({"": 1.0}, step=1))
    w.call("long", lambda: run.log({"k" * 600: 1.0}, step=1))
    w.call("not_a_dict", lambda: run.log([1, 2], step=1))
    w.call("huge_step", lambda: run.log({"loss": 1.0}, step=2**70))


def scenario_log_strict_refused(w: World):
    run = w.open(project="lab", name="r")
    w.http.answer("POST", r"/metrics$", (422, {"detail": "refused"}), times=3)
    w.call("strict", lambda: run.log({"loss": 1.0}, step=1, strict=True))
    w.call("lenient", lambda: run.log({"loss": 2.0}, step=2))


# -- the close -------------------------------------------------------------------------------
def scenario_finish_completed(w: World):
    run = w.open(project="lab", name="r")
    w.call("log", lambda: run.log({"loss": 1.0}, step=1))
    w.call("finish", lambda: run.finish())
    w.call("finish_again", lambda: run.finish())


def scenario_finish_failed_with_summary(w: World):
    run = w.open(project="lab", name="r")
    w.call("finish", lambda: run.finish("failed", summary_metrics={"best": 0.9}))


def scenario_finish_status_write_refused(w: World):
    run = w.open(project="lab", name="r")
    w.http.answer("PATCH", r"/runs/[^/]+$", 503, times=20)
    w.http.answer("POST", r"/finish$", 503, times=20)
    w.call("finish", lambda: run.finish(flush_timeout=1))


def scenario_finish_strict_refused(w: World):
    run = w.open(project="lab", name="r")
    w.http.answer("PATCH", r"/runs/[^/]+$", (422, {"detail": "no"}), times=20)
    w.http.answer("POST", r"/finish$", (422, {"detail": "no"}), times=20)
    w.call("finish", lambda: run.finish(strict=True))


def scenario_set_status_variants(w: World):
    run = w.open(project="lab", name="r")
    w.call("running", lambda: run.set_status("running"))
    w.call("crashed_sync", lambda: run.set_status("crashed", sync=True))
    w.call("only_if_running", lambda: run.set_status("failed", only_if_running=True))


def scenario_unknown_status(w: World):
    run = w.open(project="lab", name="r")
    w.call("finish", lambda: run.finish("sideways"))


# -- the close's branches, over a scripted drain result (deterministic, no retry timing) ------
def _drain_result(monkeypatch, run, *, pending=0, dead=0, delivered=0, auth_blocked=False):
    result = ([{"op": n} for n in range(pending)], [{"dead": n} for n in range(dead)], delivered, auth_blocked)
    monkeypatch.setattr(type(run), "_drain_until", lambda self, deadline, *, strict: result)


def _uploads_running(w: World, monkeypatch, run, *, why, recorded=0, settle_raises=False):
    def settle_for_close(client, uploading, deadline, *, why):
        w.steps.append(["settle_for_close", {"uploading": uploading, "why": why}])
        if settle_raises:
            raise RuntimeError("settle failed")
        return recorded

    monkeypatch.setattr(type(run), "_multipart_still_uploading", lambda self: ["model.bin"])
    monkeypatch.setattr("probe.sdk.artifact.storage_handlers.multipart.settle_reason", lambda client: why)
    monkeypatch.setattr("probe.sdk.artifact.storage_handlers.multipart.settle_for_close", settle_for_close)


def close_scenario_deferred_after_timeout(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _drain_result(monkeypatch, run, pending=2, delivered=3)
    w.call("finish", lambda: run.finish(flush_timeout=7))


def close_scenario_deferred_auth_refused(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _drain_result(monkeypatch, run, pending=1, auth_blocked=True)
    w.call("finish", lambda: run.finish())


def close_scenario_strict_dead_lettered(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _drain_result(monkeypatch, run, pending=1, dead=2)
    w.call("finish", lambda: run.finish(strict=True))


def close_scenario_strict_undelivered(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _drain_result(monkeypatch, run, pending=3)
    w.call("finish", lambda: run.finish(strict=True, flush_timeout=9))


def close_scenario_strict_auth_refused(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _drain_result(monkeypatch, run, pending=1, auth_blocked=True)
    w.call("finish", lambda: run.finish(strict=True))


def close_scenario_dead_letters_counted(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _drain_result(monkeypatch, run, dead=2, delivered=1)
    w.call("finish", lambda: run.finish())


def close_scenario_uploads_left_to_worker(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _uploads_running(w, monkeypatch, run, why=None)
    w.call("finish", lambda: run.finish())


def close_scenario_uploads_recorded_as_references(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _uploads_running(w, monkeypatch, run, why="no worker will carry them", recorded=2)
    w.call("finish", lambda: run.finish())


def close_scenario_uploads_settle_fails(w: World, monkeypatch):
    run = w.open(project="lab", name="r")
    _uploads_running(w, monkeypatch, run, why="no worker will carry them", settle_raises=True)
    w.call("finish", lambda: run.finish())


# -- which scope each way of opening a run passes on (a scripted retry-lineage check) -------
def open_scenario_retry_parent_asked_on_every_path(w: World, monkeypatch):
    def ask(self, run_kw, **scope):
        w.steps.append(["retry_parent?", w.norm.value({"scope": scope, "run_kw": sorted(run_kw)})])

    monkeypatch.setattr(type(w.client), "_maybe_attach_retry_parent", ask)
    # No home: refused before the retry check asks anything (every run has a project).
    w.call("no_home", lambda: w.open(name="f"))
    w.call("project_direct", lambda: w.open(project="lab", name="p", config={"a": 1}))
    w.call("experiment", lambda: w.open(project="lab", experiment="exp", question="q?", name="e"))


def open_scenario_experiment_from_another_project(w: World, monkeypatch):
    first = w.open(project="other", experiment="elsewhere", question="does it?", name="r0")
    w.call("by_id", lambda: w.open(project="lab", experiment=first.experiment_id, name="r1"))
    w.call("by_slug", lambda: w.open(project="lab", experiment="elsewhere", name="r2"))


SCENARIOS = {name[len("scenario_"):]: fn for name, fn in sorted(globals().items()) if name.startswith("scenario_")}
CLOSE_SCENARIOS = {
    name[len("close_scenario_"):]: fn for name, fn in sorted(globals().items()) if name.startswith("close_scenario_")
}


OPEN_SCENARIOS = {
    name[len("open_scenario_"):]: fn for name, fn in sorted(globals().items()) if name.startswith("open_scenario_")
}


@pytest.mark.parametrize("name", sorted(OPEN_SCENARIOS))
def test_open_golden(name, world, monkeypatch):
    OPEN_SCENARIOS[name](world, monkeypatch)
    check(f"open/{name}", world.record())


@pytest.mark.parametrize("name", sorted(CLOSE_SCENARIOS))
def test_close_golden(name, world, monkeypatch):
    CLOSE_SCENARIOS[name](world, monkeypatch)
    check(f"close/{name}", world.record())


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_run_golden(name, world):
    SCENARIOS[name](world)
    check(f"run/{name}", world.record())


def test_async_finish_drains_first(app, tmp_path, monkeypatch):
    w = World(app, tmp_path, monkeypatch, async_writes=True)
    run = w.open(project="lab", name="r")
    w.call("log", lambda: run.log({"loss": 1.0}, step=1))
    w.call("finish", lambda: run.finish(flush_timeout=30))
    check("run/async_finish_drains_first", w.record())
