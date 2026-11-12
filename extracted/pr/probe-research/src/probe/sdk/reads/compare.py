"""Reading several runs back for comparison.

The ``wandb.Api()`` job: runs in a group, aligned on step, to see which config
won. A shaping layer over :meth:`~probe.sdk.client.client.Client.query_series`
(``POST /v1/series/query``, many run ids in one round trip), reached as
``client.compare(...)``. Deliberately NOT a second client: one REST transport
needs no separate read object.

No pandas dependency: :meth:`Comparison.to_pandas` builds a DataFrame when pandas
is installed, and the plain structures plot directly:

    aligned = client.compare(experiment_id=exp).aligned("loss")
    for label, values in aligned.values.items():
        plt.plot(aligned.steps, values, label=label)
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Any

#: Server cap per series query (SeriesQueryRequest.run_ids); more runs are batched, not truncated.
_RUN_IDS_PER_QUERY = 50


@dataclass
class Aligned:
    """One metric key across several runs, on a shared step axis.

    ``values`` maps a run label to a list matching :attr:`steps` positionally, with
    ``None`` where that run has no point: runs of unequal length are the normal
    case, and dropping holes would truncate every series to the shortest."""

    key: str
    kind: str
    steps: list[int]
    values: dict[str, list[float | None]]

    @property
    def labels(self) -> list[str]:
        return list(self.values)

    def rows(self):
        """``(step, {label: value})`` per step, for writing out or tabulating."""
        for index, step in enumerate(self.steps):
            yield step, {label: col[index] for label, col in self.values.items()}

    def to_pandas(self):
        """A DataFrame indexed by step, one column per run. Requires pandas."""
        pandas = _pandas()
        return pandas.DataFrame(self.values, index=pandas.Index(self.steps, name="step"))


@dataclass
class Comparison:
    """Several runs and their series, fetched together.

    ``runs`` is in the order asked for; ``series`` is the raw ``SeriesResult`` list (lossless)."""

    runs: list[dict]
    series: list[dict] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.runs)

    @property
    def keys(self) -> list[str]:
        """Metric keys present, in first-seen order."""
        seen = {}
        for row in self.series:
            seen.setdefault(row["key"], None)
        return list(seen)

    def label(self, run_id: str) -> str:
        """A readable, UNIQUE column name for a run.

        Prefers the server's petname ``slug``; it is nullable, so the fallback is
        ``name``, which is NOT unique (generated names are second-resolution, so a
        sweep launching runs in one second repeats them). Shared columns would
        silently merge two runs into one curve, so a collision gets a short-id suffix."""
        chosen = None
        for row in self.runs:
            if str(row.get("id")) == str(run_id):
                chosen = row.get("slug") or row.get("name")
                break
        if not chosen:
            return str(run_id)[:8]
        clashes = [
            row
            for row in self.runs
            if (row.get("slug") or row.get("name")) == chosen
        ]
        if len(clashes) > 1:
            return f"{chosen} ({str(run_id)[:8]})"
        return chosen

    def aligned(self, key: str, *, kind: str = "model") -> Aligned:
        """One metric across every run, on the union of their step axes."""
        matching = [
            row for row in self.series if row["key"] == key and row.get("kind", "model") == kind
        ]
        if not matching:
            available = ", ".join(self.keys) or "none"
            raise KeyError(f"no series {key!r} (kind={kind!r}) in this comparison. Have: {available}")

        by_run: dict[str, dict[int, float]] = {}
        steps: set[int] = set()
        for row in matching:
            label = self.label(row["run_id"])
            points = by_run.setdefault(label, {})
            for point in row.get("points") or []:
                step = point.get("step_index")
                if step is None:
                    # Wall-clock point: no position on a step-aligned table; inventing one would mix unrelated points.
                    continue
                points[step] = point["value"]
                steps.add(step)

        ordered = sorted(steps)
        return Aligned(
            key=key,
            kind=kind,
            steps=ordered,
            values={
                label: [points.get(step) for step in ordered] for label, points in by_run.items()
            },
        )

    def to_pandas(self, key: str, *, kind: str = "model"):
        return self.aligned(key, kind=kind).to_pandas()


def _pandas():
    try:
        import pandas
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on the env
        raise ModuleNotFoundError(
            "to_pandas() needs pandas, which probe does not depend on. "
            "`pip install pandas`, or use .steps / .values directly — they plot as-is."
        ) from exc
    return pandas


def compare(
    client,
    *,
    run_ids: list[str] | None = None,
    keys: list[str] | None = None,
    kind: str = "model",
    step_from: int | None = None,
    step_to: int | None = None,
    max_points: int | None = None,
    **filters: Any,
) -> Comparison:
    """Fetch several runs and their series together. See :meth:`Client.compare`."""
    if run_ids is None:
        # Every page: GET /v1/runs answers 50 a page by default, so one page would compare a part.
        runs = list(client.iter_runs(**filters))
    else:
        runs = [client.get_run(run_id) for run_id in run_ids]
    if not runs:
        return Comparison(runs=[], series=[])

    ids = [str(row["id"]) for row in runs]
    body: dict[str, Any] = {}
    if keys is not None:
        body["series"] = [{"key": key, "kind": kind} for key in keys]
    if step_from is not None:
        body["step_from"] = step_from
    if step_to is not None:
        body["step_to"] = step_to
    if max_points is not None:
        body["max_points"] = max_points

    series: list[dict] = []
    # Batched, not truncated: dropping runs 51+ would read as "these are all of them".
    for start in range(0, len(ids), _RUN_IDS_PER_QUERY):
        chunk = ids[start : start + _RUN_IDS_PER_QUERY]
        result = client.query_series(chunk, **body)
        series.extend(result.get("series") or [])
    if len(ids) > _RUN_IDS_PER_QUERY:
        warnings.warn(
            f"comparing {len(ids)} runs took {-(-len(ids) // _RUN_IDS_PER_QUERY)} series "
            "queries; narrow with keys= or step_from/step_to if this is slow.",
            stacklevel=3,
        )
    return Comparison(runs=runs, series=series)
