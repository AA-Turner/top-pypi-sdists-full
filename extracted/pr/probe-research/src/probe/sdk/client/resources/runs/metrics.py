"""MetricsResource (client.metrics, typed reads) and RunMetricsMixin, Client's methods: per-run
metrics, grouped and wide reads merged page by page, export, coordinates
(twin: app/runs/metrics)."""

from __future__ import annotations
import builtins
from collections.abc import Iterator
from ...resource import Resource
import json
from typing import Any
from .....generated.models import (
    CoordinateOut,
    ExportPoint,
    GroupedSeriesResult,
    LatestScalarsWithSettings,
    MetricPointOut,
    MetricSeriesOut,
    MetricViewData,
    MetricViewOut,
    SeriesQueryResult,
    SourceReadContractEnum,
    WideSeriesResult,
)
from ....reads import nonfinite


#: A run mirrored from another tool (a W&B live-sync run, say) keeps its metric
#: POINTS at the source; Probe stores a passport, not a copy. The provider read
#: paths therefore refuse a caller that has not declared which coverage contract
#: it understands, because a silent fallback would hand back a truncated or
#: re-sampled series as though it were the whole run. Every read below is
#: written against coverage-v1, so every read below says so. Omitting it is how
#: the MCP metric views came to report a mirrored run as having no metrics at
#: all while the same data returned fine over HTTP.
SOURCE_READ_CONTRACT = SourceReadContractEnum.coverage_v1.value

#: Iteration cap for the step-paged reads (metrics grouped/wide). The loop already
#: stops when the server reports the read exhausted; the cap only exists so a server
#: that keeps answering ``truncated`` with a non-advancing ``next_step`` cannot spin
#: a notebook forever. Hitting it returns honestly: ``truncated`` stays True and
#: ``next_step`` says where to resume.
_MAX_STEPPED_PAGES = 100


def _series_key(column: dict) -> tuple:
    """A wide-read column's series identity: (key, kind, canonical dimensions)."""
    return (
        column.get("key"),
        column.get("kind"),
        json.dumps(column.get("dimensions") or {}, sort_keys=True),
    )


def _merge_wide_page(merged: dict, page: dict) -> None:
    """Append one page of a wide read onto the merged result, in place.

    Columns are per-window: a series with no point inside a page's step range is
    absent from that page's ``columns``, so later pages can be wider (or narrower)
    than the first. Positions therefore cannot be trusted across pages — values are
    realigned by series identity, and a column new to the merge back-fills ``None``
    into the rows already collected, exactly as the server would have emitted had
    the whole range fit in one page."""
    if page.get("columns") == merged["columns"]:
        merged["rows"].extend(page.get("rows") or [])
        return
    positions = {_series_key(column): i for i, column in enumerate(merged["columns"])}
    for column in page.get("columns") or []:
        if _series_key(column) not in positions:
            positions[_series_key(column)] = len(merged["columns"])
            merged["columns"].append(column)
            for row in merged["rows"]:
                row["values"].append(None)
    width = len(merged["columns"])
    page_keys = [_series_key(column) for column in page.get("columns") or []]
    for row in page.get("rows") or []:
        values: list = [None] * width
        for series, value in zip(page_keys, row.get("values") or []):
            values[positions[series]] = value
        merged["rows"].append({**row, "values": values})


class RunMetricsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def run_metrics(
        self,
        run_id: str,
        *,
        key: str | None = None,
        kind: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Raw metric points for a run. :meth:`run_series` is the summarized view;
        :meth:`query_series` is the multi-run comparison. A logged NaN / +inf /
        -inf comes back as that float (see :mod:`probe.sdk.reads.nonfinite`)."""
        params = {
            k: v for k, v in {"key": key, "kind": kind, "limit": limit}.items() if v is not None
        }
        rows = self.transport.get(f"/v1/runs/{run_id}/metrics", params=params or None)
        return [nonfinite.to_float(row) for row in rows]

    def delete_series(
        self,
        run_id: str,
        *,
        key: str,
        kind: str = "model",
        dimensions: dict | None = None,
    ) -> None:
        """Delete a DERIVED series and its points — the counterpart to pushing one.

        Derived only: a logged series is the run's captured record, cannot be
        recomputed, and has no undo, so the server refuses it with a 409.

        Identity is (kind, key, dimensions), the same triple a write uses.
        `dimensions` pins ONE variant; omitting it addresses the dimension-less
        series, not every variant of the key."""
        params = {"kind": kind, "key": key}
        if dimensions is not None:
            params["dimensions"] = json.dumps(dimensions)
        self.transport.request("DELETE", f"/v1/runs/{run_id}/series", params=params)

    def run_series(self, run_id: str) -> list[dict]:
        """Per-series summary for a run (key/kind/dimensions + first/last/min/max)."""
        return self.transport.get(
            f"/v1/runs/{run_id}/series",
            params={"source_read_contract": SOURCE_READ_CONTRACT},
        )

    def get_series_digests(self, run_id: str, keys: list[str], *, kind: str = "model") -> dict:
        """Each named series' point count, stats and order-free digest, as Probe stores them: what a copy's parity
        check compares (`connectors/wandb_history.py` has the rule). `{run_id, kind, series: [...]}`."""
        return self.transport.get(f"/v1/runs/{run_id}/series/digest", params={"keys": list(keys), "kind": kind})

    # -- coordinate reads (below-run coordinates, research-os 0059-0062) -----
    def get_metrics_grouped(
        self,
        run_id: str,
        key: str,
        *,
        kind: str | None = None,
        agg: str | None = None,
        by: list[str] | None = None,
        where: dict[str, Any] | None = None,
        step_bucket: int | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        max_rows: int | None = None,
    ) -> dict:
        """Server-side reduce/group over one metric's stepped points (0059).

        ``by`` names coordinate axes to split on (sent comma-joined; one cell per
        combination of axis values); ``where`` is a coord filter dict (sent
        JSON-encoded, matched by type-faithful containment). ``agg`` is one of
        mean|sum|min|max|count — OPTIONAL since server 0062: omitted resolves to
        the key's DECLARED reduce fn (see :meth:`Run.log`'s ``agg``), else mean;
        conflicting declarations are a 422. An unknown ``by``/``where`` axis or a
        kind-ambiguous key is a 422, never a silent empty reduction.

        Paging is followed here: a truncated page's ``next_step`` is fed back as
        ``step_from`` until the reduction is exhausted, so one call answers the
        whole range. ``max_rows`` bounds the TOTAL cells returned — when it cuts
        the read short (or ``_MAX_STEPPED_PAGES`` does), the result says so:
        ``truncated`` is True and ``next_step`` is where to resume."""
        merged: dict | None = None
        remaining = max_rows
        for _ in range(_MAX_STEPPED_PAGES):
            params = {
                param: value
                for param, value in {
                    "key": key,
                    "kind": kind,
                    "agg": agg,
                    "by": ",".join(by) if by else None,
                    "where": json.dumps(where) if where is not None else None,
                    "step_bucket": step_bucket,
                    "step_from": step_from,
                    "step_to": step_to,
                    "max_rows": remaining,
                }.items()
                if value is not None
            }
            page = self.transport.get(f"/v1/runs/{run_id}/metrics/grouped", params=params)
            if merged is None:
                merged = page
            else:
                merged["groups"].extend(page.get("groups") or [])
                merged["truncated"] = page.get("truncated", False)
                merged["next_step"] = page.get("next_step")
            if remaining is not None:
                remaining -= len(page.get("groups") or ())
                if remaining <= 0:
                    break
            if not page.get("truncated") or page.get("next_step") is None:
                break
            step_from = page["next_step"]
        return merged

    def get_metrics_wide(
        self,
        run_id: str,
        *,
        key: list[str] | None = None,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        max_rows: int | None = None,
    ) -> dict:
        """Step x metric table for a run — the DataFrame pivot, aligned by step.

        Same paging treatment as :meth:`get_metrics_grouped`: ``next_step`` is
        followed until the table is exhausted (rows realigned by series identity,
        since a page's columns cover only its own step window), ``max_rows``
        bounds the TOTAL step rows, and a short read reports ``truncated`` +
        ``next_step``. ``key`` narrows to those metric keys (repeated query
        param, matching the route's array parameter)."""
        merged: dict | None = None
        remaining = max_rows
        for _ in range(_MAX_STEPPED_PAGES):
            params = {
                param: value
                for param, value in {
                    "key": key or None,
                    "kind": kind,
                    "step_from": step_from,
                    "step_to": step_to,
                    "max_rows": remaining,
                    "source_read_contract": SOURCE_READ_CONTRACT,
                }.items()
                if value is not None
            }
            page = self.transport.get(f"/v1/runs/{run_id}/metrics/wide", params=params or None)
            if merged is None:
                merged = page
            else:
                _merge_wide_page(merged, page)
                merged["truncated"] = page.get("truncated", False)
                merged["next_step"] = page.get("next_step")
            if remaining is not None:
                remaining -= len(page.get("rows") or ())
                if remaining <= 0:
                    break
            if not page.get("truncated") or page.get("next_step") is None:
                break
            step_from = page["next_step"]
        return merged

    def export_metric_points(
        self,
        run_id: str,
        *,
        key: str | None = None,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        after_id: int | None = None,
        limit: int | None = None,
    ):
        """Lossless raw-point export: every point exactly once, labels included,
        no downsampling. A GENERATOR — the ``after_id`` keyset paging is followed
        transparently, so callers just iterate; ``limit`` is the page size of the
        walk, not a total bound. Pass ``after_id`` to resume a previous walk from
        its last point id. A logged NaN / +inf / -inf comes back as that float
        (see :mod:`probe.sdk.reads.nonfinite`)."""
        while True:
            params = {
                param: value
                for param, value in {
                    "key": key,
                    "kind": kind,
                    "step_from": step_from,
                    "step_to": step_to,
                    "after_id": after_id,
                    "limit": limit,
                }.items()
                if value is not None
            }
            page = self.transport.get(f"/v1/runs/{run_id}/metrics/export", params=params or None)
            for point in page.get("points") or ():
                yield nonfinite.to_float(point)
            next_after_id = page.get("next_after_id")
            # None means the last currently visible page. The monotonic check is
            # the loop's own guard: a cursor that fails to advance would replay
            # the same page forever, and an infinite generator that yields
            # duplicates is worse than stopping at the point already delivered.
            if next_after_id is None or (after_id is not None and next_after_id <= after_id):
                return
            after_id = next_after_id

    def list_run_coordinates(self, run_id: str) -> list[dict]:
        """The run's coordinate catalog (0060): every non-empty coordinate any
        fact has landed on, with which fact tables have it — enumeration for
        split/overlay pickers without scanning points/spans/artifacts. Bounded by
        the series cap's cardinality arithmetic, so no pagination."""
        return self.transport.get(f"/v1/runs/{run_id}/coordinates")


class MetricsResource(Resource):
    """`client.metrics`: typed metric reads. A non-finite point keeps the value the flat
    read restores from its marker (NaN, inf)."""

    __slots__ = ()

    def list(
        self, run_id: str, *, key: str | None = None, kind: str | None = None,
        limit: int | None = None,
    ) -> builtins.list[MetricPointOut]:
        """`Client.run_metrics` as `MetricPointOut`s."""
        return self._to_models(
            MetricPointOut,
            self._client.run_metrics(run_id, key=key, kind=kind, limit=limit),
        )

    def list_series(self, run_id: str) -> builtins.list[MetricSeriesOut]:
        """`Client.run_series` as `MetricSeriesOut`s."""
        return self._to_models(MetricSeriesOut, self._client.run_series(run_id))

    def get_grouped(
        self, run_id: str, key: str, *, kind: str | None = None, agg: str | None = None,
        by: builtins.list[str] | None = None, where: dict[str, Any] | None = None,
        step_bucket: int | None = None, step_from: int | None = None, step_to: int | None = None,
        max_rows: int | None = None,
    ) -> GroupedSeriesResult:
        """`Client.get_metrics_grouped` as a `GroupedSeriesResult`."""
        return self._to_model(
            GroupedSeriesResult,
            self._client.get_metrics_grouped(
                run_id, key, kind=kind, agg=agg, by=by, where=where, step_bucket=step_bucket,
                step_from=step_from, step_to=step_to, max_rows=max_rows,
            ),
        )

    def get_wide(
        self, run_id: str, *, key: builtins.list[str] | None = None, kind: str | None = None,
        step_from: int | None = None, step_to: int | None = None, max_rows: int | None = None,
    ) -> WideSeriesResult:
        """`Client.get_metrics_wide` as a `WideSeriesResult`."""
        return self._to_model(
            WideSeriesResult,
            self._client.get_metrics_wide(
                run_id, key=key, kind=kind, step_from=step_from, step_to=step_to, max_rows=max_rows,
            ),
        )

    def export_points(
        self, run_id: str, *, key: str | None = None, kind: str | None = None,
        step_from: int | None = None, step_to: int | None = None, after_id: int | None = None,
        limit: int | None = None,
    ) -> Iterator[ExportPoint]:
        """`Client.export_metric_points` as `ExportPoint`s, read page by page as it reads them."""
        for point in self._client.export_metric_points(
            run_id, key=key, kind=kind, step_from=step_from, step_to=step_to, after_id=after_id,
            limit=limit,
        ):
            yield ExportPoint.model_validate(point)

    def list_coordinates(self, run_id: str) -> builtins.list[CoordinateOut]:
        """`Client.list_run_coordinates` as `CoordinateOut`s."""
        return self._to_models(CoordinateOut, self._client.list_run_coordinates(run_id))

    def list_views(self, run_id: str) -> builtins.list[MetricViewOut]:
        """`Client.list_views` as `MetricViewOut`s."""
        return self._to_models(MetricViewOut, self._client.list_views(run_id))

    def get_view_data(
        self, run_id: str, view_id: str, *, step_from: int | None = None,
        step_to: int | None = None, max_points: int | None = None,
    ) -> MetricViewData:
        """`Client.view_data` as a `MetricViewData`."""
        return self._to_model(
            MetricViewData,
            self._client.view_data(
                run_id, view_id, step_from=step_from, step_to=step_to, max_points=max_points,
            ),
        )

    def query_series(self, run_ids: builtins.list[str], **kw) -> SeriesQueryResult:
        """`Client.query_series` as a `SeriesQueryResult`."""
        return self._to_model(SeriesQueryResult, self._client.query_series(run_ids, **kw))

    def get_latest(
        self, run_ids: builtins.list[str], *, keys: builtins.list[str] | None = None,
        kind: str | None = None,
    ) -> LatestScalarsWithSettings:
        """`Client.latest_scalars` as a `LatestScalarsWithSettings`."""
        return self._to_model(
            LatestScalarsWithSettings,
            self._client.latest_scalars(run_ids, keys=keys, kind=kind),
        )
