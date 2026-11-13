"""Routes: the API routes the SDK writes to, in both directions. `path_for` builds a run write's
path from its WriteOp; `classify` reads any path back. The only place a route's shape lives."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ...foundation.compat.compat import StrEnum


class WriteOp(StrEnum):
    """What a write is, as far as delivery cares."""

    METRICS = "metrics"  # POST /v1/runs/{run}/metrics: points, merged into one POST by the drain
    STEPS = "steps"  # POST /v1/runs/{run}/steps: one step record; many go as one /steps/batch
    SPANS = "spans"  # POST /v1/runs/{run}/spans: NULs in span text are escaped, not refused
    SAMPLES = "samples"  # POST /v1/runs/{run}/samples/batch: RL samples, seals, plans; many ops go as one
    SAMPLE_POINTS = "sample_points"  # POST /v1/runs/{run}/samples/points: per-sample metrics; never merged with SAMPLES
    RUN_PATCH = "run_patch"  # PATCH /v1/runs/{run}: the run's row; a terminal status closes it
    WRITER_RELEASE = "writer_release"  # POST /v1/runs/{run}/writers/{session}/release: closes a `leases` run
    INGEST_RUNS = "ingest_runs"  # /ingest/v1/runs: a batch of runs with their spans
    INGEST = "ingest"  # any other /ingest route: sent with the ingest token
    OTHER = "other"


#: The run writes a writer may build with `path_for`: their path is the run id and nothing else.
BUILDABLE = frozenset({WriteOp.METRICS, WriteOp.STEPS, WriteOp.SPANS, WriteOp.SAMPLES, WriteOp.SAMPLE_POINTS,
                       WriteOp.RUN_PATCH})
_SUFFIX = {
    WriteOp.METRICS: "/metrics",
    WriteOp.STEPS: "/steps",
    WriteOp.SPANS: "/spans",
    WriteOp.SAMPLES: "/samples/batch",
    WriteOp.SAMPLE_POINTS: "/samples/points",
    WriteOp.RUN_PATCH: "",
}
_RUN_POSTS = {"metrics": WriteOp.METRICS, "steps": WriteOp.STEPS, "spans": WriteOp.SPANS}


@dataclass(frozen=True)
class Route:
    """A path read back. ``run``: the run segment as written (an id, a `local:` key, a slug).
    ``exact``: the path is the route's own shape, with no query, fragment or trailing slash;
    the drain merges and batches only exact paths, as it always has."""

    op: WriteOp
    run: str | None = None
    exact: bool = True


def classify(method: str, path: str | None) -> Route:
    """What ``method path`` writes. One rule for every reader: the query, the fragment and one
    trailing slash do not change what a write is (``exact`` says whether there were any)."""
    raw = path if isinstance(path, str) else ""  # a corrupt op's path reads as no route, never a crash
    bare = raw.split("?", 1)[0].split("#", 1)[0]
    trimmed = bare[:-1] if len(bare) > 1 and bare.endswith("/") else bare
    exact = trimmed == raw
    verb = (method or "").upper()
    if trimmed.startswith("/ingest"):
        return Route(WriteOp.INGEST_RUNS if trimmed == "/ingest/v1/runs" else WriteOp.INGEST, None, exact)
    parts = trimmed.split("/")
    if len(parts) >= 4 and parts[:3] == ["", "v1", "runs"] and parts[3]:
        run, tail = parts[3], parts[4:]
        if not tail:
            op = WriteOp.RUN_PATCH if verb == "PATCH" else WriteOp.OTHER
        elif verb == "POST" and len(tail) == 1 and tail[0] in _RUN_POSTS:
            op = _RUN_POSTS[tail[0]]
        elif verb == "POST" and tail == ["samples", "batch"]:
            op = WriteOp.SAMPLES
        elif verb == "POST" and tail == ["samples", "points"]:
            op = WriteOp.SAMPLE_POINTS
        elif verb == "POST" and len(tail) == 3 and tail[0] == "writers" and tail[1] and tail[2] == "release":
            op = WriteOp.WRITER_RELEASE
        else:
            op = WriteOp.OTHER
        return Route(op, run, exact)
    return Route(WriteOp.OTHER, None, exact)


def path_for(op: WriteOp, run: str) -> str:
    """The path of a run write (one of `BUILDABLE`)."""
    if op not in BUILDABLE:
        raise ValueError(f"{op} is not built from a run id alone")
    return f"/v1/runs/{run}{_SUFFIX[op]}"


def batch_path(op: WriteOp, path: str) -> str:
    """Where many ``op`` writes go as one request, from one of their (already bound) paths: a
    `local:` run key is rewritten in the path, never in `run_ref`, so the path is the address."""
    route = classify("POST", path)
    if op is not WriteOp.STEPS or route.op is not op or not route.exact:
        raise ValueError(f"no batch route for {op} at {path!r}")
    return f"/v1/runs/{route.run}/steps/batch"


# -- the two readers that shape an op file's bytes ----------------------------------------------
# Older drainers share the outbox, so these keep their exact old shapes (review of #3826): a NUL
# escaped here is a span batch an older worker would have refused, and vice versa.
def is_metrics_post(method: str, path: str) -> bool:
    """A metrics POST whose unstorable points are dropped before queueing: a query is ignored,
    a fragment is not."""
    return classify(method, path).op is WriteOp.METRICS and "#" not in path.split("?", 1)[0]


def is_span_batch(method: str, path: str) -> bool:
    """A POST whose span text may carry escaped NULs: a run's spans or an ingest batch of runs,
    with no query or fragment."""
    spans = classify(method, path).op in (WriteOp.SPANS, WriteOp.INGEST_RUNS)
    return (method or "").upper() == "POST" and spans and "?" not in path and "#" not in path


# -- the run a path addresses -------------------------------------------------------------------
_RUN_PATH = re.compile(r"^/v1/runs/([^/]+)(?:/|$)")


def run_ref_of(path: str) -> str | None:
    """The run a v1 path addresses, as written (a query stays on the segment): the lane and
    barrier key stamped on every op, so it keeps the shape older releases stamped."""
    match = _RUN_PATH.match(path)
    return match.group(1) if match else None


# -- tokens ---------------------------------------------------------------------------------
def is_ingest(path: str | None) -> bool:
    """Whether a request goes out with the INGEST token."""
    return bool(path) and str(path).startswith("/ingest")


def is_public(path: str) -> bool:
    """Whether a request is a public read that carries no credential."""
    return path.startswith("/public/")


# -- experiment children ------------------------------------------------------------------------
#: The project segment of an experiment child path queued before its project is known:
#: `/v1/projects/~/experiments/{E}/...`. The drain asks where the experiment is filed. `~`
#: cannot be a project slug or id, so an older drainer sends it to a 404 and dead-letters it.
UNPLACED_PROJECT = "~"
_UUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
_PLACED_EXPERIMENT_PATH = re.compile(rf"/v1/projects/{_UUID}/experiments/({_UUID})((?:/[^?#]*)?)")
_UNPLACED_EXPERIMENT_PATH = re.compile(r"/v1/projects/~/experiments/([^/?#]+)((?:/[^?#]*)?)")


def unplaced_experiment_path(path: str) -> str:
    """``path`` with an experiment child route's project replaced by `UNPLACED_PROJECT`; any
    other path unchanged."""
    match = _PLACED_EXPERIMENT_PATH.fullmatch(path or "")
    if match is None:
        return path
    return f"/v1/projects/{UNPLACED_PROJECT}/experiments/{match.group(1)}{match.group(2)}"


def unplaced_experiment(path: str | None) -> tuple[str, str] | None:
    """(experiment, rest of the path) of a queued unplaced experiment child write, else None."""
    match = _UNPLACED_EXPERIMENT_PATH.fullmatch(path or "")
    return (match.group(1), match.group(2)) if match else None
