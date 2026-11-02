"""`probe.sdk.routes` against the route checks it replaced (plan sdk-typed-write-ops, T1).

The ORACLE below is the eleven checks as they stood on main before the refactor, copied once and
frozen: every reader's question about a path is asked of both, over every shape we could think
of. They must agree, except where `INTENDED` names the shape and says why."""

from __future__ import annotations

import itertools
import re
import uuid

import pytest

from probe.sdk.routes import (
    BUILDABLE,
    UNPLACED_PROJECT,
    WriteOp,
    batch_path,
    classify,
    is_ingest,
    path_for,
    run_ref_of,
    unplaced_experiment,
    unplaced_experiment_path,
)

U = "0b6f2b0e-6f0e-4a4e-9d47-2f7a1c3e5d10"
E = "11111111-1111-4111-8111-111111111111"
P = "22222222-2222-4222-8222-222222222222"


# -- the checks as they were (main ca5d0b7700), frozen --------------------------------------------
def _is_uuid(ref: str) -> bool:
    try:
        uuid.UUID(ref)
    except (AttributeError, TypeError, ValueError):
        return False
    return True


_DRAIN_METRICS = re.compile(r"/v1/runs/([^/?#]+)/metrics")  # coalesce.py / upload_windows.py
_DRAIN_STEPS = re.compile(r"/v1/runs/([^/?#]+)/steps")  # coalesce.py
_TELEMETRY = re.compile(r"/v1/runs/([^/?#]+)/(metrics|steps)")  # window.py
_UNSTORABLE_METRICS = re.compile(r"/v1/runs/[^/?#]+/metrics/?")  # values/unstorable.py
_SPAN = re.compile(r"/v1/runs/[^/?#]+/spans/?")  # values/unstorable.py
_RUN_CLOSE = re.compile(r"/v1/runs/[^/]+")  # ops.py
_RUN_RELEASE = re.compile(r"/v1/runs/[^/]+/writers/[^/]+/release")  # ops.py


def old_answers(method: str, path: str) -> dict:
    """The drain's readers compared the op's own method to "POST" first; they still do."""
    post = method == "POST"
    m = _DRAIN_METRICS.fullmatch(path) if post else None
    s = _DRAIN_STEPS.fullmatch(path) if post else None
    t = _TELEMETRY.fullmatch(path) if post else None
    return {
        "merge_metrics": bool(m and _is_uuid(m.group(1))),
        "batch_steps": bool(s and _is_uuid(s.group(1))),
        "collectable": (t.group(2) if t and _is_uuid(t.group(1)) else None),
        "passes_uploads": m is not None,
        "drops_unstorable": method.upper() == "POST" and bool(_UNSTORABLE_METRICS.fullmatch(path.split("?", 1)[0])),
        "escapes_spans": method.upper() == "POST"
        and (_SPAN.fullmatch(path) is not None or path in ("/ingest/v1/runs", "/ingest/v1/runs/")),
        "close_shape": (method == "PATCH" and bool(_RUN_CLOSE.fullmatch(path)))
        or (method == "POST" and bool(_RUN_RELEASE.fullmatch(path))),
        "ingest": path.startswith("/ingest"),
    }


def new_answers(method: str, path: str) -> dict:
    """Each reader's answer, asked of the READER itself on an op carrying this method and path
    (review of #3826: the table must catch a reader that asks classify the wrong question)."""
    from probe.sdk import errors
    from probe.sdk.delivery.ops.ops import _is_run_close
    from probe.sdk.delivery.outbox.drain import coalesce, upload_windows, window
    from probe.sdk.delivery.outbox.drain.credentials import op_credential
    from probe.sdk.values import unstorable

    def op(body):
        return {"kind": "http", "method": method, "path": path, "body": body}

    points = {"points": [{"key": "k", "value": 1.0, "step_index": 1}]}
    step = {"step_index": 1}
    try:
        _, escaped = unstorable.escape_nuls({"spans": [{"attributes": {"result": "a\x00b"}}]}, path=path, method=method)
    except errors.ValidationError:
        escaped = {}
    collectable = (
        "metrics" if window.is_collectable(op(points)) else "steps" if window.is_collectable(op(step)) else None
    )
    principal = {"principal": {"fingerprint": "personal", "ingest_fingerprint": "ingest"}}
    return {
        "merge_metrics": coalesce._merge_key(op(points)) is not None,
        "batch_steps": coalesce._step_key(op(step)) is not None,
        "collectable": collectable,
        "passes_uploads": upload_windows._passes_uploads(op(points)),
        "drops_unstorable": bool(unstorable.drop_unstorable_points(
            method, path, {"points": [{"key": "k", "step_index": 2**70}]})[1]),
        "escapes_spans": bool(escaped),
        "close_shape": _is_run_close(op({"status": "completed"})),
        "ingest": op_credential({**op({}), "context": principal})[1],
    }


# -- the shapes -------------------------------------------------------------------------------------
RUNS = [U, "r-1", "local:abc", "not a uuid"]
TAILS = [
    "", "/", "?force=1", "#x", "/metrics", "/metrics/", "/metrics?x=1", "/metrics#f", "/metrics/?x",
    "/metrics/extra", "/steps", "/steps/", "/steps?x", "/steps/batch", "/spans", "/spans/", "/spans?x",
    "/writers/s1/release", "/writers/s1/release/", "/writers/s1/release?x", "/writers//release",
    "/artifacts", "/finish", "/metrics#a?b", "/spans#a?b", "/spans/?x",
]
OTHER_PATHS = [
    "", "/", "/v1/runs", "/v1/runs/", "/v1/runs//metrics", "/ingest/v1/runs", "/ingest/v1/runs/",
    "/ingest/v1/runs?x", "/ingest/v1/other", "/ingestx", "/public/docs", "/v1/experiments/e-1/artifacts",
    f"/v1/projects/~/experiments/{E}/versions", f"/v1/projects/{P}/experiments/{E}", f"/v1/projects/{P}/experiments/{E}/notes",
    f"/v1/projects/~/experiments/{E}?x", "/v2/runs/x/metrics", "/v1/runs/?x", "/v1/runs/x?q/writers/s/release",
    "/ingest/v1/runs#f",
]
METHODS = ["POST", "PATCH", "GET", "PUT", "post", "patch"]
PATHS = [f"/v1/runs/{run}{tail}" for run, tail in itertools.product(RUNS, TAILS)] + OTHER_PATHS


def _intended(method: str, path: str, question: str, old, new) -> str | None:
    """Why the new answer differs on purpose, or None. Only the drain's close hold may differ,
    and only on shapes no SDK writer sends; every reader that shapes an op file's BYTES
    (unstorable points, NUL escaping, collect window, run_ref) answers exactly as before."""
    if question != "close_shape" or method not in ("PATCH", "POST"):
        return None
    bare = path.split("?", 1)[0].split("#", 1)[0]
    if new and not old and (bare.endswith("/") or "?" in path or "#" in path):
        return "wider: a trailing slash, query or fragment on a run PATCH or release holds the close too"
    if old and not new and "?" in path.split("/v1/runs/", 1)[-1].split("/", 1)[0]:
        return "narrower: a run segment holding a query (`/v1/runs/x?q/...`) is not a run"
    return None


CASES = [(m, p) for m in METHODS for p in PATHS]


@pytest.mark.parametrize("method,path", CASES)
def test_every_reader_gets_the_old_answer_or_a_named_reason(method, path):
    old, new = old_answers(method, path), new_answers(method, path)
    for question in old:
        if old[question] != new[question]:
            reason = _intended(method, path, question, old[question], new[question])
            assert reason is not None, (question, method, path, old[question], new[question])


def test_the_named_differences_are_all_reached():
    """An INTENDED reason no shape needs any more is dead text: drop it."""
    seen = set()
    for method, path in CASES:
        old, new = old_answers(method, path), new_answers(method, path)
        for question in old:
            if old[question] != new[question]:
                seen.add(_intended(method, path, question, old[question], new[question]))
    assert seen == {
        "wider: a trailing slash, query or fragment on a run PATCH or release holds the close too",
        "narrower: a run segment holding a query (`/v1/runs/x?q/...`) is not a run",
    }


@pytest.mark.parametrize("op", sorted(BUILDABLE))
def test_a_built_path_reads_back_as_its_own_write(op):
    method = "PATCH" if op is WriteOp.RUN_PATCH else "POST"
    route = classify(method, path_for(op, U))
    assert (route.op, route.run, route.exact) == (op, U, True)


def test_only_run_id_routes_are_built():
    for op in set(WriteOp) - BUILDABLE:
        with pytest.raises(ValueError):
            path_for(op, U)


def test_the_steps_batch_goes_to_the_bound_run_in_the_path():
    """An offline op keeps its `local:` key in run_ref; the drain binds the PATH to the server
    id first, so the batch is built from the path (plan finding 3)."""
    assert batch_path(WriteOp.STEPS, f"/v1/runs/{U}/steps") == f"/v1/runs/{U}/steps/batch"
    for op, path in ((WriteOp.METRICS, f"/v1/runs/{U}/metrics"), (WriteOp.STEPS, f"/v1/runs/{U}/metrics"),
                     (WriteOp.STEPS, f"/v1/runs/{U}/steps?x"), (WriteOp.STEPS, "/v1/projects/p")):
        with pytest.raises(ValueError):
            batch_path(op, path)


@pytest.mark.parametrize("body", [{"status": []}, {"status": ["completed"]}, {"status": {}}, [], "x", None])
def test_a_corrupt_run_patch_is_not_a_close_and_never_crashes_the_pass(body):
    """One hand-edited op used to raise out of `_is_run_close` and stop every drain pass on the
    machine (review of #3826, Codex; main raised too on a plain run path)."""
    from probe.sdk.delivery.ops.ops import _is_run_close

    for path in (f"/v1/runs/{U}", f"/v1/runs/{U}?source=/backfill"):
        assert _is_run_close({"kind": "http", "method": "PATCH", "path": path, "body": body}) is False


@pytest.mark.parametrize("path", [5, None, ["/v1/runs/x/metrics"], {"p": 1}])
def test_a_path_that_is_not_text_is_no_route(path):
    assert classify("POST", path).op is WriteOp.OTHER


def test_random_shapes_get_the_old_answer_or_a_named_reason():
    """A seeded fuzz over the characters that matter to the old checks: anything the table
    above missed, in either direction (review of #3826)."""
    import random

    pieces = ["/", "v1", "runs", U, "r", "local:k", "metrics", "steps", "spans", "writers", "release",
              "?", "#", "x=1", "", "ingest", "batch", "projects", "~", "experiments", E]
    rng = random.Random(3826)
    for _ in range(1500):
        path = "/" + "".join(rng.choice(pieces) + rng.choice(["/", "", "/", "?", "#"]) for _ in range(rng.randint(1, 6)))
        if rng.random() < 0.5:
            path = rng.choice([f"/v1/runs/{U}", "/v1/runs/r", "/ingest/v1/runs"]) + path
        method = rng.choice(["POST", "PATCH", "post"])
        old, new = old_answers(method, path), new_answers(method, path)
        for question in old:
            if old[question] != new[question]:
                assert _intended(method, path, question, old[question], new[question]), (question, method, path)


@pytest.mark.parametrize("path,ref", [
    ("/v1/runs/r-1/metrics", "r-1"), ("/v1/runs/r-1", "r-1"), ("/v1/runs/r-1?force=1", "r-1?force=1"),
    ("/v1/runs/local:k/steps", "local:k"), ("/v1/experiments/e-1/artifacts", None), ("/v1/runs/", None),
])
def test_the_run_ref_keeps_the_shape_older_releases_stamped(path, ref):
    assert run_ref_of(path) == ref


def test_experiment_children_are_placed_and_unplaced_as_before():
    assert unplaced_experiment_path(f"/v1/projects/{P}/experiments/{E}/versions") == f"/v1/projects/{UNPLACED_PROJECT}/experiments/{E}/versions"
    assert unplaced_experiment_path(f"/v1/projects/{P}/experiments/{E}") == f"/v1/projects/~/experiments/{E}"
    for kept in ("/v1/projects/slug/experiments/x/notes", f"/v1/runs/{U}", f"/v1/projects/{P}/experiments/{E}?x"):
        assert unplaced_experiment_path(kept) == kept
    assert unplaced_experiment(f"/v1/projects/~/experiments/{E}/versions") == (E, "/versions")
    assert unplaced_experiment(f"/v1/projects/~/experiments/{E}") == (E, "")
    assert unplaced_experiment(f"/v1/projects/{P}/experiments/{E}") is None


# -- writers name the write (plan T3) ---------------------------------------------------------------
_SRC = __import__("pathlib").Path(__file__).resolve().parents[3] / "src" / "probe"
_HAND_BUILT = re.compile(r"/v1/runs/\{[^}]*\}(/metrics|/steps|/spans)?")
_WRITE_CALLS = {"write": 1, "send": 1, "request": 1, "append_http": 1, "_write_to_run": 2, "post": 0, "patch": 0}


def _hand_built_write_paths() -> list[str]:
    import ast

    found = []
    for py in sorted(_SRC.rglob("*.py")):
        if "routes" in py.relative_to(_SRC).parts[:2]:
            continue
        for node in ast.walk(ast.parse(py.read_text())):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            index = _WRITE_CALLS.get(name)
            if index is None or len(node.args) <= index:
                continue
            method = node.args[index - 1] if index else None
            if method is not None and not (isinstance(method, ast.Constant) and method.value in ("POST", "PATCH")):
                continue
            path = node.args[index]
            text = ast.unparse(path)
            if isinstance(path, (ast.JoinedStr, ast.Constant)) and _HAND_BUILT.fullmatch(
                re.sub(r"\{[^}]*\}", "{}", text.strip("f'\""))
            ):
                found.append(f"{py.relative_to(_SRC)}:{node.lineno}  {text}")
    return found


def test_no_writer_builds_a_run_write_path_by_hand():
    """A run's metrics, steps, spans or row write is `path_for(WriteOp.X, run)`: the route
    table is the only place its shape lives, so a moved route moves everywhere at once."""
    assert _hand_built_write_paths() == []


@pytest.mark.parametrize("run", [U, "local:abc", "r-1"])
def test_a_built_path_is_the_string_writers_used_to_write(run):
    """Op files stay byte-identical (plan D1): `path_for` returns exactly the old f-strings."""
    assert path_for(WriteOp.METRICS, run) == f"/v1/runs/{run}/metrics"
    assert path_for(WriteOp.STEPS, run) == f"/v1/runs/{run}/steps"
    assert path_for(WriteOp.SPANS, run) == f"/v1/runs/{run}/spans"
    assert path_for(WriteOp.RUN_PATCH, run) == f"/v1/runs/{run}"
