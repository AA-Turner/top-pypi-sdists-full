"""metric reads: server-side grouping, coordinates, one raw export page, and multi-run series under a budget."""

from __future__ import annotations
import hashlib
import math
import uuid
from itertools import islice
from typing import Any
from ....sdk import errors
from ....foundation.token_budget.token_budget import MIN_TOKENS as _MIN_TOKEN_BUDGET
from ....foundation.token_budget.token_budget import MAX_TOKENS as _MAX_TOKEN_BUDGET
from ....foundation.token_budget.token_budget import Budget, serialize
from ....shared.reads.search_contract import (
    EnvelopeState,
    MissingMarker)
from ...delivery.delivery import omit_defaults
from ...delivery.context import current_delivery, source_changed
from probe.mcp.tools.shaping.cursors import _delivery_cursor_stand_in
from probe.mcp.tools.shaping.shaping import _budget_cost

# Row bounds for the coordinate reads. Grouped cells are aggregates (one per step
# bucket x group), so a few hundred already draws a chart; export points are raw
# and unbounded, so the tool serves ONE keyset page and hands the cursor back.
# Both are clamps, not defaults an agent can override past.
_GROUPED_ROWS_MAX = 2_000
_GROUPED_ROWS_DEFAULT = 500
_EXPORT_PAGE_MAX = 1_000
_EXPORT_PAGE_DEFAULT = 200


#: Headroom on a refused series' `min_token_budget`, before rounding up to the
#: next hundred: room for the re-read to come back a little longer.
_SERIES_BUDGET_HEADROOM = 1.1
#: Tokens reserved past the heaviest stand-in (see `_STAND_IN_IDENTITIES`).
_CURSOR_TOKEN_SLACK = 8


class MetricsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    # -- coordinate reads (below-run coordinates, 0059-0062) -----------------

    def metrics_grouped(
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
        """One bounded server-side reduction. ``max_rows`` clamps to the tool's
        row bound — grouped cells are aggregates, so the clamp cuts pathology,
        not typical reads — and a cut read reports partial with the resume step
        in ``next_cursor``."""
        bound = min(max_rows or _GROUPED_ROWS_DEFAULT, _GROUPED_ROWS_MAX)
        payload = self.source.run_metrics_grouped(
            run_id,
            key,
            kind=kind,
            agg=agg,
            by=by,
            where=where,
            step_bucket=step_bucket,
            step_from=step_from,
            step_to=step_to,
            max_rows=bound,
        )
        missing = [MissingMarker.ROWS_BEYOND_PAGE_BOUND] if payload.get("truncated") else []
        next_step = payload.get("next_step")
        return self._envelope(
            {"run_id": run_id, **payload},
            state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
            missing=missing,
            next_cursor=str(next_step) if missing and next_step is not None else None,
        )

    def run_coordinates(self, run_id: str) -> dict:
        """The coordinate catalog is bounded by the series cap's cardinality
        arithmetic (no pagination on the route), so this is one complete read."""
        return self._envelope(
            {"run_id": run_id, "coordinates": self.source.run_coordinates(run_id)}
        )

    def metrics_export(
        self,
        run_id: str,
        *,
        key: str | None = None,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        after_id: int | None = None,
        limit: int | None = None,
    ) -> dict:
        """ONE keyset page of the lossless export. The SDK generator would follow
        the walk to the last point; a tool response cannot, so the page is sliced
        off it here and the cursor handed back as ``next_cursor`` (pass it back
        as ``after_id``)."""
        bound = max(1, min(limit or _EXPORT_PAGE_DEFAULT, _EXPORT_PAGE_MAX))
        filters = {
            name: value
            for name, value in {
                "key": key,
                "kind": kind,
                "step_from": step_from,
                "step_to": step_to,
                "after_id": after_id,
            }.items()
            if value is not None
        }
        walk = self.source.export_points(run_id, limit=bound, **filters)
        # Lookahead past the page bound, so "more points exist" is a fact rather
        # than an inference from a full page (the _bounded contract).
        points = list(islice(walk, bound + 1))
        more = len(points) > bound
        points = points[:bound]
        return self._envelope(
            {"run_id": run_id, "filters": filters or None, "points": points},
            state=EnvelopeState.PARTIAL if more else EnvelopeState.COMPLETE,
            missing=[MissingMarker.ROWS_BEYOND_PAGE_BOUND] if more else [],
            next_cursor=str(points[-1]["id"]) if more else None,
        )

    #: Points per series a `series` read asks the backend for when the caller
    #: names no `max_points`. The backend's own default is EVERY point, and one
    #: 10k-step series is ~100k tokens: no response can carry it. 100 is the
    #: chart path's min-max downsample (endpoints and extremes kept), and the
    #: response says the number it used.
    _SERIES_DEFAULT_MAX_POINTS = 100

    #: How many per-series read failures one response lists; the count is exact.
    _SERIES_ERRORS_LISTED = 20

    #: The provenance of an exact local read. A series whose provenance differs
    #: (a provider's sample, a bucket-smoothed curve) carries it on its row.
    _EXACT_PROVENANCE = {"source": "probe", "coverage": "complete", "exactness": "exact"}

    #: What the API stamps on EVERY local series of a read that named
    #: `max_points` (`provider_reads.local_read_provenance`), whether or not the
    #: downsample dropped a point. Kept on a row only when the row can have been
    #: cut -- see `_series_row`.
    _LOCAL_DISPLAY_SAMPLE = {"source": "probe", "coverage": "sampled", "exactness": "sampled"}

    #: `delivery_context` snapshot source for a series read's identity hash.
    _SERIES_SNAPSHOT = "series"

    @staticmethod
    def _series_run_id(value: Any) -> str:
        """A run UUID from `<uuid>` or `run:<uuid>` (browse's `uuid` field).
        The series route types `run_ids` as UUIDs, so a slug is refused here in
        words that say how to get the id, not relayed as a body 422."""
        text = str(value)
        ident = text[len("run:") :] if text.startswith("run:") else text
        try:
            return str(uuid.UUID(ident))
        except ValueError:
            raise errors.ValidationError(
                f"mode=series takes run UUIDs, not {text!r}: a slug resolves with "
                f'entity(refs=["run:<slug>"]), whose card carries the id',
                status=422,
            ) from None

    @classmethod
    def _plain_display_sample(cls, series: dict) -> bool:
        provenance = series.get("read_provenance")
        return isinstance(provenance, dict) and all(
            provenance.get(key) == value for key, value in cls._LOCAL_DISPLAY_SAMPLE.items()
        )

    @staticmethod
    def _catalog_identity(series: dict) -> tuple:
        return (
            str(series.get("run_id")),
            series.get("kind"),
            series.get("key"),
            serialize(series.get("dimensions") or {}),
        )

    def _logged_counts(self, raw: list[dict], keys: list[str]) -> dict[tuple, int]:
        """How many points each LOCALLY-sampled series has logged in all, from
        the catalog (`POST /v1/series/latest`: one call, no point scan) -- what
        tells a series the downsample cut from one it returned whole.

        Only for the runs that carry the API's blanket "sampled" stamp; a
        provider's receipt is its own and is never second-guessed (asking would
        also cost a provider read). Empty on any failure, which keeps every
        stamp: unsure reads as "may be sampled", never as "exact"."""
        runs = sorted({str(s.get("run_id")) for s in raw if self._plain_display_sample(s)})
        if not runs:
            return {}
        try:
            answer = self.source.latest_scalars(runs, keys=keys) or {}
        except errors.RosError:
            return {}
        return {
            self._catalog_identity(row): row["point_count"]
            for row in answer.get("scalars") or []
            if isinstance(row, dict)
            and isinstance(row.get("point_count"), int)
            and not isinstance(row.get("point_count"), bool)
        }

    @classmethod
    def _series_row(
        cls, series: dict, fields: list[str], max_points: int, logged: int | None = None
    ) -> dict:
        """One series, its points as positional arrays in `point_fields` order.

        Positional because a point object repeats its three key names on every
        point -- most of a long series' tokens -- and the legend rides once on
        the response instead."""

        def cell(point: dict, field: str) -> Any:
            value = point.get(field)
            # Strict JSON: a non-finite float would fail the whole response.
            if isinstance(value, float) and not math.isfinite(value):
                return None
            return value

        points = [
            [cell(point, field) for field in fields]
            for point in series.get("points") or []
            if isinstance(point, dict)
        ]
        row: dict[str, Any] = {
            "run_id": str(series.get("run_id")),
            "key": series.get("key"),
            "kind": series.get("kind"),
        }
        if series.get("dimensions"):
            row["dimensions"] = series["dimensions"]
        if series.get("x_axis") not in (None, "step"):
            row["x_axis"] = series["x_axis"]
        provenance = series.get("read_provenance")
        if isinstance(provenance, dict):
            if cls._plain_display_sample(series) and logged is not None and logged <= max_points:
                # The API stamps every local series of a `max_points` read as
                # sampled, so on its own the stamp says only that a bound was
                # sent. The downsample only runs on more points than the bound,
                # and a series that has LOGGED no more than that -- in all, so
                # in any step window too -- came back whole. Its returned count
                # cannot say this: a cut series often comes back a point or two
                # short of the bound (an endpoint is also a bucket's extreme),
                # and a flat one far shorter.
                provenance = None
            if provenance is not None and any(
                provenance.get(key, default) != default
                for key, default in cls._EXACT_PROVENANCE.items()
            ):
                row["read_provenance"] = {
                    key: value
                    for key, value in provenance.items()
                    if value is not None and key != "fetched_at"
                }
        row["point_count"] = len(points)
        row["points"] = points
        return row

    @staticmethod
    def _series_identity(series: dict) -> list:
        """What makes a series row THE SAME row on a re-read: never its points,
        which a still-logging run keeps adding to."""
        return [
            str(series.get("run_id")),
            series.get("kind"),
            series.get("key"),
            serialize(series.get("dimensions") or {}),
            str(series.get("x_axis") or ""),
        ]

    def _check_series_identity(self, raw: list[dict]) -> None:
        """Refuse to continue a series read whose LIST of series changed.

        Each page re-runs the query (the route takes no cursor) and the cursor
        is an index into its rows. If a series appears or vanishes between two
        pages -- a W&B read that fails on page 2, or recovers -- the same index
        names a different series and one is skipped or repeated with nothing
        saying so. The first page's identity hash rides the delivery cursor;
        every later page must match it or say "restart".

        KNOWN COST, accepted: every page re-reads every series (provider reads
        included), because the cursorless route offers nothing narrower."""
        digest = hashlib.sha256(
            serialize([self._series_identity(series) for series in raw]).encode("utf-8")
        ).hexdigest()
        context = current_delivery()
        if context is None:
            return
        if context.snapshot is None:
            context.snapshot = {"source": self._SERIES_SNAPSHOT, "end": 0, "sha256": digest}
            return
        if context.snapshot.get("source") != self._SERIES_SNAPSHOT:
            raise source_changed("document identity changed")
        if context.snapshot.get("sha256") != digest:
            raise source_changed(
                "the series this read returns changed since its first page (a series "
                "appeared or vanished -- a provider read can fail or recover between "
                "calls)"
            )

    def metrics_series(
        self,
        run_ids: list[str],
        keys: list[str],
        *,
        step_from: int | None = None,
        step_to: int | None = None,
        smoothing: str | None = None,
        max_points: int | None = None,
        offset: int = 0,
        token_budget: int = 2000,
    ) -> dict:
        """Several runs x several keys in one read (`POST /v1/series/query`).

        One ROW per series (run x key x dimensions). The read is one backend
        call; the response carries as many WHOLE series as `token_budget`
        holds, measured with the real tokenizer, and `next_cursor` is the
        index of the next series (pass it back as the cursor argument).

        A series is never split across responses. One that does not fit even
        alone is REFUSED with the budget that would carry it (or the
        `max_points` that would fit the largest budget): a series re-read for
        its second half on a still-logging run is a different series, so a
        multi-response series could not be put back together.
        """
        ids = [self._series_run_id(run) for run in run_ids]
        bound = self._SERIES_DEFAULT_MAX_POINTS if max_points is None else int(max_points)
        body: dict[str, Any] = {"keys": list(keys), "max_points": bound}
        if step_from is not None:
            body["step_from"] = step_from
        if step_to is not None:
            body["step_to"] = step_to
        if smoothing is not None:
            body["smoothing"] = str(smoothing)
        result = self.source.query_series(ids, **body) or {}
        raw = [series for series in result.get("series") or [] if isinstance(series, dict)]
        self._check_series_identity(raw)
        # The timestamp column is decided by the series' AXIS, not only by
        # whether a point lacks a step: a step window drops every stepless point,
        # and a wall-clock series must still say when its points were logged.
        timed = any(series.get("x_axis") == "wall_clock" for series in raw) or any(
            isinstance(point, dict) and point.get("step_index") is None
            for series in raw
            for point in series.get("points") or []
        )
        fields = ["step_index", "value"]
        if timed:
            fields.append("wall_clock")
        if smoothing is not None:
            fields.append("smoothed")
        logged = self._logged_counts(raw, list(keys))
        rows = [
            self._series_row(series, fields, bound, logged.get(self._catalog_identity(series)))
            for series in raw
        ]
        failures = [error for error in result.get("errors") or [] if isinstance(error, dict)]
        if offset > len(rows):
            raise errors.ValidationError(
                "this cursor is past the end of the series read; repeat it without cursor",
                status=422,
            )
        source_missing: list[str] = []
        if result.get("truncated"):
            # The backend's raw-point safety ceiling: points past it were never
            # read, so a line may end early. Narrow the keys or the step window.
            source_missing.append(MissingMarker.METRIC_POINTS_BEYOND_BACKEND_LIMIT)
        if failures:
            source_missing.append(MissingMarker.SERIES_READ_ERRORS)

        def build(count: int, next_cursor: str | None, extra: dict | None = None) -> dict:
            data: dict[str, Any] = {
                "max_points": bound,
                "point_fields": fields,
                "series_total": len(rows),
                "series": rows[offset : offset + count],
                **(extra or {}),
            }
            if failures and offset == 0:
                data["errors"] = failures[: self._SERIES_ERRORS_LISTED]
                if len(failures) > self._SERIES_ERRORS_LISTED:
                    data["errors_total"] = len(failures)
            missing = list(source_missing)
            if offset + count < len(rows):
                missing.append(
                    MissingMarker.TRUNCATED_BY_TOKEN_BUDGET
                    if count
                    else MissingMarker.FIRST_RESULT_EXCEEDS_BUDGET
                )
            return omit_defaults(
                {
                    "data": data,
                    "completeness": {
                        "state": EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
                        "missing": missing,
                    },
                    "next_cursor": next_cursor,
                }
            )

        remaining = len(rows) - offset
        budget = Budget(max(_MIN_TOKEN_BUDGET, min(int(token_budget), _MAX_TOKEN_BUDGET)))
        # Measured with a STAND-IN for the delivery cursor that will replace the
        # native one: delivery wraps `next_cursor` in a bound, compressed token of
        # about this size, and a fit computed without it overflows by exactly
        # that much.
        stand_in = _delivery_cursor_stand_in()
        low, high, kept = 1, remaining, 0
        while low <= high:
            mid = (low + high) // 2
            cursor = stand_in if mid < remaining else None
            if budget.fits(build(mid, cursor), reserve=_CURSOR_TOKEN_SLACK if cursor else 0):
                kept, low = mid, mid + 1
            else:
                high = mid - 1
        if remaining and not kept:
            # Not even the next series fits. Say what would, rather than cut it.
            needed = _budget_cost(build(1, stand_in if remaining > 1 else None)) + (
                _CURSOR_TOKEN_SLACK if remaining > 1 else 0
            )
            extra: dict[str, Any] = {"next_series_tokens": needed}
            # WITH HEADROOM, as `_budget_for` names its number: the retry
            # re-reads the series, and on a still-logging run with noisy values
            # it comes back a little longer -- a hint of exactly `needed` was
            # refused again on retry in 7 of 12 seeds, 1-12 tokens short.
            hint = -(-int(needed * _SERIES_BUDGET_HEADROOM) // 100) * 100
            if hint <= _MAX_TOKEN_BUDGET:
                extra["min_token_budget"] = hint
                extra["retry"] = (
                    "repeat this call (same cursor) with token_budget >= min_token_budget"
                )
            else:
                points = rows[offset].get("point_count") or 0
                extra["fits_max_points"] = max(
                    2, int(points * _MAX_TOKEN_BUDGET / (needed * _SERIES_BUDGET_HEADROOM))
                )
                if needed <= _MAX_TOKEN_BUDGET:
                    # It fits the largest budget today, with too little room to
                    # promise a re-read will.
                    extra["min_token_budget"] = _MAX_TOKEN_BUDGET
                extra["retry"] = (
                    "this series is at the largest token_budget's edge or past it: repeat "
                    "the read with max_points <= fits_max_points"
                )
            shaped = build(0, None, extra)
            return self._envelope(
                shaped["data"],
                state=EnvelopeState.PARTIAL,
                missing=(shaped.get("completeness") or {}).get("missing", []),
            )
        next_cursor = str(offset + kept) if offset + kept < len(rows) else None
        shaped = build(kept, next_cursor)
        return self._envelope(
            shaped["data"],
            state=(shaped.get("completeness") or {}).get("state", EnvelopeState.COMPLETE),
            missing=(shaped.get("completeness") or {}).get("missing", []),
            next_cursor=next_cursor,
        )
