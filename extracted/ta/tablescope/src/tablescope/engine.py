from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from math import floor, isfinite, isnan
from typing import Any, Literal, cast

import narwhals as nw
import polars as pl

SortDirection = Literal["asc", "desc"]
FilterOperator = Literal[
    "contains",
    "starts_with",
    "ends_with",
    "eq",
    "neq",
    "gt",
    "gte",
    "lt",
    "lte",
    "between",
]
Frame = nw.DataFrame[Any] | nw.LazyFrame[Any]

# Per-cell serialization budget, in bytes of the JSON-ready value. A single
# cell can hold a large blob/array (e.g. a covariance matrix), and a page of
# such cells will OOM the browser before it renders. Values larger than this
# are replaced with a truncation marker (see _jsonify_scalar); the full value
# is still reachable on demand via fetch_cell.
DEFAULT_MAX_CELL_BYTES = 8192

# Marker key identifying a truncated-cell sentinel. The frontend recognizes
# this and renders a compact placeholder instead of stringifying the payload.
TRUNCATED_KEY = "__tablescope_truncated__"


@dataclass(frozen=True)
class SortSpec:
    column: str
    direction: SortDirection = "asc"

    @property
    def descending(self) -> bool:
        return self.direction == "desc"


@dataclass(frozen=True)
class FilterSpec:
    column: str
    operator: FilterOperator
    value: Any
    value_to: Any | None = None


def _is_number(value: Any) -> bool:
    # bool is an int subclass but never a meaningful bin edge; exclude it.
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class TableEngine:
    """Narwhals-backed query engine for the tablescope widget."""

    def __init__(
        self,
        source: Any,
        *,
        page_size: int = 100,
        frequency_limit: int = 25,
        max_cell_bytes: int = DEFAULT_MAX_CELL_BYTES,
    ) -> None:
        normalized = nw.from_native(source, eager_only=False)
        if not isinstance(normalized, (nw.DataFrame, nw.LazyFrame)):
            msg = (
                "tablescope expected an object that narwhals can treat as a "
                f"dataframe or lazy frame, got {type(source)!r}."
            )
            raise TypeError(msg)

        self._frame: Frame = normalized
        # The frame as supplied, before any derived columns. Edits and removals
        # replay the derived-column list against this base, so a derived column
        # can reference an earlier derived column and still be rebuilt cleanly.
        self._base_frame: Frame = normalized
        self._derived: list[tuple[str, str]] = []
        self._page_size = max(1, page_size)
        self._frequency_limit = max(1, frequency_limit)
        # 0 (or negative) disables truncation entirely.
        self._max_cell_bytes = max_cell_bytes if max_cell_bytes > 0 else None
        self._total_rows_cache: int | None = None
        self._filtered_count_cache: dict[Any, int] = {}

        self._refresh_schema()
        self._supports_random_access = self._can_paginate_frame(normalized)

    @property
    def page_size(self) -> int:
        return self._page_size

    @property
    def supports_random_access(self) -> bool:
        return self._supports_random_access

    @property
    def columns(self) -> list[str]:
        return list(self._columns)

    @property
    def total_rows(self) -> int:
        if self._total_rows_cache is None:
            result = self._materialize(
                self._as_lazy(self._frame).select(nw.len().alias("__total_rows__"))
            )
            row = self._rows_from_frame(result)[0]
            self._total_rows_cache = int(row["__total_rows__"])
        return self._total_rows_cache

    def initial_payload(self) -> dict[str, Any]:
        # Rows are intentionally not included: this payload is synced as
        # widget state, so embedding the first page would duplicate it in
        # every notebook snapshot. The frontend fetches page 0 over the
        # message channel instead.
        return {
            "columns": [self._column_payload(name) for name in self._columns],
            "page_size": self._page_size,
            "total_rows": self.total_rows,
            "supports_random_access": self._supports_random_access,
        }

    def fetch_rows(
        self,
        *,
        offset: int,
        limit: int | None = None,
        sort: list[SortSpec] | None = None,
        filters: list[FilterSpec] | None = None,
    ) -> dict[str, Any]:
        filter_specs = filters or []
        filtered = self._apply_filters(self._frame, filter_specs)
        total_rows = self._filtered_total_rows(filtered, filter_specs)
        bounded_offset = max(0, min(offset, max(0, total_rows - 1)))
        effective_limit = max(1, limit or self._page_size)
        bounded_limit = min(effective_limit, max(1, total_rows - bounded_offset))
        sort_specs = sort or []

        transformed = self._apply_sort(filtered, sort_specs)
        page = self._page_frame(transformed, offset=bounded_offset, limit=bounded_limit)
        rows = self._rows_from_frame(self._materialize(page), truncate=True)

        for index, row in enumerate(rows):
            row["__tablescope_row_number__"] = bounded_offset + index

        return {
            "offset": bounded_offset,
            "limit": bounded_limit,
            "total_rows": total_rows,
            "sort": [
                {"column": spec.column, "direction": spec.direction}
                for spec in sort_specs
            ],
            "filters": [
                {
                    "column": spec.column,
                    "operator": spec.operator,
                    "value": spec.value,
                    "value_to": spec.value_to,
                }
                for spec in filter_specs
            ],
            "rows": rows,
        }

    def fetch_cell(
        self,
        *,
        offset: int,
        column: str,
        sort: list[SortSpec] | None = None,
        filters: list[FilterSpec] | None = None,
    ) -> dict[str, Any]:
        """Return one cell's full, untruncated value.

        Backs the frontend's "load full value" affordance for a cell that was
        truncated in the page payload. The sort/filter context must match the
        page the user is viewing so `offset` addresses the same row.
        """
        if column not in self._columns:
            raise KeyError(f"Unknown column {column!r}.")

        filter_specs = filters or []
        filtered = self._apply_filters(self._frame, filter_specs)
        total_rows = self._filtered_total_rows(filtered, filter_specs)
        bounded_offset = max(0, min(offset, max(0, total_rows - 1)))

        transformed = self._apply_sort(filtered, sort or [])
        page = self._page_frame(transformed, offset=bounded_offset, limit=1)
        materialized = self._materialize(page).select(column)
        rows = self._rows_from_frame(materialized)  # untruncated
        value = rows[0][column] if rows else None
        return {"offset": bounded_offset, "column": column, "value": value}

    def jump_to_fraction(
        self,
        fraction: float,
        *,
        limit: int | None = None,
        sort: list[SortSpec] | None = None,
        filters: list[FilterSpec] | None = None,
    ) -> dict[str, Any]:
        """Fetch the page at a fractional position through the dataset.

        Public API for programmatic use; the bundled frontend reaches
        arbitrary offsets directly through fetch_rows.
        """
        filter_specs = filters or []
        total_rows = self._filtered_total_rows(
            self._apply_filters(self._frame, filter_specs), filter_specs
        )
        effective_limit = limit or self._page_size
        if total_rows <= effective_limit:
            offset = 0
        else:
            max_offset = total_rows - effective_limit
            clamped_fraction = min(1.0, max(0.0, fraction))
            offset = floor(max_offset * clamped_fraction)
        return self.fetch_rows(
            offset=offset,
            limit=effective_limit,
            sort=sort,
            filters=filter_specs,
        )

    @property
    def derived_columns(self) -> list[dict[str, str]]:
        """The derived columns, in application order, with their expressions."""
        return [{"name": name, "expr": expr} for name, expr in self._derived]

    def add_column(self, name: str, expr_string: str) -> dict[str, Any]:
        """Derive a new column from an evaluated narwhals expression.

        ``expr_string`` is evaluated with ``nw`` in scope, so callers write
        narwhals expressions such as ``nw.col("foo") + 1``. This is an
        intentional eval of user-supplied code: tablescope runs locally on the
        caller's own hardware, so the trust boundary is the same as a notebook
        cell. ``__builtins__`` is still stripped to block the most obvious
        footguns (``__import__``, ``open``) without pretending to be a sandbox.
        """
        name = name.strip()
        if not name:
            raise ValueError("Column name must not be empty.")
        if name in self._schema:
            raise ValueError(f"Column {name!r} already exists.")

        self._set_derived([*self._derived, (name, expr_string)])
        return self._column_payload(name)

    def update_column(self, name: str, expr_string: str) -> dict[str, Any]:
        """Replace the expression of an existing derived column."""
        index = self._derived_index(name)
        next_derived = list(self._derived)
        next_derived[index] = (name, expr_string)
        self._set_derived(next_derived)
        return self._column_payload(name)

    def remove_column(self, name: str) -> dict[str, Any]:
        """Drop a derived column, rebuilding from the base frame.

        Raises if a later derived column still references this one (the replay
        fails), leaving the engine on its current good state.
        """
        index = self._derived_index(name)
        next_derived = [item for i, item in enumerate(self._derived) if i != index]
        try:
            self._set_derived(next_derived)
        except ValueError as exc:
            # The most likely cause is a later derived column referencing this
            # one; the replay then can't resolve the dropped name.
            raise ValueError(
                f"Could not remove {name!r}: another derived column may "
                f"depend on it."
            ) from exc
        return {"removed": name}

    def _derived_index(self, name: str) -> int:
        for index, (existing, _expr) in enumerate(self._derived):
            if existing == name:
                return index
        raise ValueError(f"Column {name!r} is not a derived column.")

    def _set_derived(self, derived: list[tuple[str, str]]) -> None:
        """Replay ``derived`` against the base frame, committing only on success.

        Building a candidate frame and resolving its schema before assigning to
        ``self._frame`` means a bad expression (e.g. a typo'd column reference,
        which only fails when a lazy schema is resolved) leaves the engine on
        the previous good frame rather than poisoning every later query.
        """
        # Compile expressions first (their own error message), then build and
        # resolve the candidate frame (a separate message). These stay separate
        # try blocks because some backends raise ValueError subclasses from the
        # build phase, so a shared handler can't tell the phases apart by type.
        compiled: list[tuple[str, Any]] = [
            (name, self._compile_expr(expr_string)) for name, expr_string in derived
        ]
        try:
            candidate = self._base_frame
            for name, expr in compiled:
                candidate = self._with_derived_column(candidate, name, expr)
            schema = self._frame_schema(candidate)
        except Exception as exc:
            raise ValueError(f"Could not apply expression: {exc}") from exc

        self._frame = candidate
        self._derived = derived
        self._schema = schema
        self._columns = list(schema)
        # Row count is unchanged, but the filtered-count cache is keyed on
        # filter specs built against the old schema; invalidate it so a filter
        # that references a changed column can't read a stale count.
        self._filtered_count_cache.clear()

    def _compile_expr(self, expr_string: str) -> Any:
        if not expr_string.strip():
            raise ValueError("Expression must not be empty.")
        # Wrap in parens so newlines act as implicit line continuations: a user
        # can split a method chain across lines (e.g. `pl.col("a")\n.cum_sum()`)
        # and it still parses as a single expression.
        wrapped = f"({expr_string})"
        try:
            evaluated = eval(wrapped, self._expr_namespace())  # noqa: S307
        except Exception as exc:  # surface eval errors as a clean message
            raise ValueError(f"Could not evaluate expression: {exc}") from exc
        # A narwhals/polars expression carries .alias; a bare Python scalar
        # (e.g. the expression "1") is wrapped in a literal so it broadcasts.
        return evaluated if hasattr(evaluated, "alias") else nw.lit(evaluated)

    def _expr_namespace(self) -> dict[str, Any]:
        """Names available to a derived-column expression string.

        ``nw`` is narwhals. ``pl`` aliases to narwhals too, *unless* the source
        is a real polars frame — then ``pl`` is genuine polars, so the full
        polars expression API is available. Because narwhals is a deliberate
        subset of the polars API, aliasing ``pl`` -> ``nw`` on other backends
        works for the overlapping surface. The bare ``col``/``lit``/``when``
        shortcuts save users from typing the namespace at all.
        """
        namespace_module = pl if self._base_frame.implementation.is_polars() else nw
        return {
            "nw": nw,
            "pl": namespace_module,
            "col": namespace_module.col,
            "lit": namespace_module.lit,
            "when": namespace_module.when,
            "__builtins__": {},
        }

    def _with_derived_column(self, frame: Frame, name: str, expr: Any) -> Frame:
        """Attach a derived column, handling native-polars and narwhals exprs.

        A polars-backed frame may carry a genuine polars expression (from ``pl``
        in the namespace), which narwhals' ``with_columns`` rejects. For that
        case we drop to the native polars frame, apply there, and re-wrap.
        Narwhals expressions take the normal path and work on any backend.
        """
        if isinstance(expr, (pl.Expr, pl.Series)):
            native = frame.to_native()
            native = native.with_columns(expr.alias(name))
            rewrapped = nw.from_native(native, eager_only=False)
            if not isinstance(rewrapped, (nw.DataFrame, nw.LazyFrame)):
                msg = f"Unexpected frame type after derivation: {type(rewrapped)!r}."
                raise TypeError(msg)
            return rewrapped
        return frame.with_columns(expr.alias(name))

    def _refresh_schema(self) -> None:
        self._schema = self._frame_schema(self._frame)
        self._columns = list(self._schema)

    def _frame_schema(self, frame: Frame) -> dict[str, Any]:
        schema = (
            frame.collect_schema()
            if isinstance(frame, nw.LazyFrame)
            else frame.schema
        )
        return dict(schema.items())

    def describe_column(
        self,
        column: str,
        *,
        filters: list[FilterSpec] | None = None,
    ) -> dict[str, Any]:
        self._require_column(column)
        dtype = self._schema[column]
        filtered = self._apply_filters(self._frame, filters or [])
        exprs: list[Any] = [
            nw.len().alias("row_count"),
            nw.col(column).count().alias("non_null_count"),
            nw.col(column).null_count().alias("null_count"),
        ]

        if not dtype.is_nested():
            # min/max aren't defined for list/struct columns, and a distinct
            # count over nested values isn't meaningful, so all three share the
            # nested guard rather than computing partial stats.
            exprs.extend(
                [
                    nw.col(column).n_unique().alias("distinct_count"),
                    nw.col(column).min().alias("min"),
                    nw.col(column).max().alias("max"),
                ]
            )

        if dtype.is_numeric():
            exprs.extend(
                [
                    nw.col(column).mean().alias("mean"),
                    nw.col(column).median().alias("median"),
                    nw.col(column).std(ddof=1).alias("std"),
                    nw.col(column).sum().alias("sum"),
                ]
            )

        frame = self._materialize(self._as_lazy(filtered).select(*exprs))
        values = self._rows_from_frame(frame)[0]
        return {
            "column": column,
            "dtype": str(dtype),
            "is_numeric": dtype.is_numeric(),
            "is_temporal": dtype.is_temporal(),
            "stats": values,
        }

    def value_counts(
        self,
        column: str,
        *,
        limit: int | None = None,
        filters: list[FilterSpec] | None = None,
    ) -> dict[str, Any]:
        self._require_column(column)
        dtype = self._schema[column]
        if dtype.is_nested():
            raise TypeError(f"Column {column!r} is nested and cannot be grouped.")

        top_n = max(1, limit or self._frequency_limit)
        lazy = (
            self._as_lazy(self._apply_filters(self._frame, filters or []))
            .group_by(column)
            .agg(nw.len().alias("count"))
            .sort(["count", column], descending=[True, False])
            .head(top_n)
        )
        frame = self._materialize(lazy)
        return {
            "column": column,
            "limit": top_n,
            "values": self._rows_from_frame(frame),
        }

    def histogram(
        self,
        column: str,
        *,
        bin_count: int = 20,
        filters: list[FilterSpec] | None = None,
    ) -> dict[str, Any]:
        """Bin a numeric or temporal column's values into ``bin_count`` buckets.

        Uses narwhals' ``Series.hist``, which reports each bin's right edge
        (``breakpoint``) and ``count``. We pair consecutive edges so each bin
        carries an explicit ``left``/``right`` span, letting the frontend draw a
        true vertical histogram (bars positioned along the value axis) rather
        than ambiguous single-edge bars.

        Binning is pushed down to the backend, never materialized locally: a
        full column on a cloud table can be billions of rows. We fetch only the
        column's min/max (one row), compute fixed-width bin edges from that, and
        push a ``group_by`` on the floored bin index so the backend returns just
        ``bin_count`` counts. Temporal columns are binned on their epoch-
        millisecond value via ``dt.timestamp("ms")`` *inside the lazy frame*
        (so the backend, e.g. Spark, performs it; neither a local Arrow cast
        nor a backend ``CAST(date AS bigint)`` is portable), and each edge is
        mapped back to the dtype for a ``left_label``/``right_label``. Honors
        the active filters like the other profile queries.
        """
        self._require_column(column)
        dtype = self._schema[column]
        is_temporal = dtype.is_temporal()
        if not dtype.is_numeric() and not is_temporal:
            raise TypeError(
                f"Column {column!r} is not numeric or temporal and has no histogram."
            )

        bins = max(1, bin_count)
        filtered = self._apply_filters(self._frame, filters or [])
        lazy = self._as_lazy(filtered)

        # Numeric value to bin on. For temporal columns we bin on the offset
        # from the minimum, as an integer: (col - lit(min)).cast(Int64). The
        # subtraction yields a Duration whose integer cast is portable across
        # backends (Spark rejects a direct CAST(date AS bigint), and a local
        # Arrow date32->int64 cast is also unsupported). min()/max() and the
        # offset's max work on every backend; we read them in one aggregation
        # so the binning units come straight from the backend, never guessed.
        if is_temporal:
            # Fetch the native min/max first; the offset expression references
            # the min as a literal, and both anchor the edge labels. min()/max()
            # over a date column are portable. Read raw (not jsonified) values
            # so they stay as date/datetime objects for the literal and label
            # arithmetic — _rows_from_frame would stringify them.
            native = self._materialize(
                lazy.select(
                    nw.col(column).min().alias("min"),
                    nw.col(column).max().alias("max"),
                )
            ).rows(named=True)[0]
            low_native = native["min"]
            high_native = native["max"]
            value_expr = (nw.col(column) - nw.lit(low_native)).cast(nw.Int64)
        else:
            low_native = None
            high_native = None
            value_expr = nw.col(column)

        bounds = self._rows_from_frame(
            self._materialize(
                lazy.select(
                    value_expr.min().alias("min"),
                    value_expr.max().alias("max"),
                    value_expr.count().alias("non_null"),
                )
            )
        )[0]
        # Bin geometry runs on the numeric value_expr: 0..offset for temporal
        # (it starts at the min), the raw min..max otherwise.
        low: Any = 0 if is_temporal else bounds["min"]
        high: Any = bounds["max"]
        non_null = bounds["non_null"]

        # Degenerate cases: nothing to bin, or a single value (zero span). One
        # bin covering [low, high] keeps the frontend's geometry well-defined.
        if not non_null or low is None or high is None or float(high) <= float(low):
            edge = float(low) if low is not None else 0.0
            bin_specs = [
                {"left": edge, "right": edge + 1.0, "count": int(non_null or 0)}
            ]
            if is_temporal:
                self._attach_temporal_edge_labels(bin_specs, low_native, high_native)
            return {
                "column": column,
                "bin_count": 1,
                "is_temporal": is_temporal,
                "bins": bin_specs,
            }

        span = float(high) - float(low)
        width = span / bins
        # Bin index = floor((value - low) / width), clamped so the max value
        # (which would land at index == bins) folds into the last bin. The whole
        # group_by is pushed to the backend, which returns only `bins` rows.
        bin_index = (
            ((value_expr.cast(nw.Float64) - float(low)) / width)
            .floor()
            .cast(nw.Int64)
            .clip(0, bins - 1)
            .alias("bin")
        )
        counts_frame = self._materialize(
            lazy.filter(~nw.col(column).is_null())
            .select(bin_index)
            .group_by("bin")
            .agg(nw.len().alias("count"))
        )
        counts = {
            int(row["bin"]): int(row["count"])
            for row in self._rows_from_frame(counts_frame)
        }

        bin_specs = []
        for index in range(bins):
            left = float(low) + index * width
            right = float(low) + (index + 1) * width
            bin_specs.append(
                {"left": left, "right": right, "count": counts.get(index, 0)}
            )

        if is_temporal:
            self._attach_temporal_edge_labels(bin_specs, low_native, high_native)

        return {
            "column": column,
            "bin_count": bins,
            "is_temporal": is_temporal,
            "bins": bin_specs,
        }

    def _attach_temporal_edge_labels(
        self, bin_specs: list[dict[str, Any]], low_native: Any, high_native: Any
    ) -> None:
        """Map each numeric bin edge back to a temporal value for ISO labels.

        Edges are integer offsets from the minimum (``low``..``high`` over the
        offset axis); the numeric ``left``/``right`` stay for bar geometry. We
        translate each edge to a native temporal value by linear interpolation
        between ``low_native`` and ``high_native`` — fraction of the offset span
        — which is independent of the backend's duration unit (days vs. micros).
        """
        if low_native is None or high_native is None:
            return
        edges = [spec["left"] for spec in bin_specs] + [bin_specs[-1]["right"]]
        max_offset = float(edges[-1]) if _is_number(edges[-1]) else 0.0
        span = high_native - low_native  # a timedelta

        def label_for(offset: Any) -> Any:
            if not _is_number(offset) or max_offset <= 0:
                return self._jsonify_scalar(low_native)
            fraction = float(offset) / max_offset
            value = low_native + span * fraction
            return self._jsonify_scalar(value)

        labels = [label_for(edge) for edge in edges]
        for index, spec in enumerate(bin_specs):
            spec["left_label"] = labels[index]
            spec["right_label"] = labels[index + 1]

    def _column_payload(self, name: str) -> dict[str, Any]:
        dtype = self._schema[name]
        derived_expr = next(
            (expr for derived_name, expr in self._derived if derived_name == name),
            None,
        )
        return {
            "name": name,
            "dtype": str(dtype),
            "is_numeric": dtype.is_numeric(),
            "is_temporal": dtype.is_temporal(),
            "is_nested": dtype.is_nested(),
            "is_derived": derived_expr is not None,
            "expr": derived_expr,
        }

    def _require_column(self, column: str) -> None:
        if column not in self._schema:
            raise KeyError(f"Unknown column {column!r}.")

    def _apply_filters(self, frame: Frame, filters: list[FilterSpec]) -> Frame:
        result = frame
        for spec in filters:
            self._require_column(spec.column)
            result = result.filter(self._filter_expr(spec))
        return result

    def _apply_sort(self, frame: Frame, sort_specs: list[SortSpec]) -> Frame:
        if not sort_specs:
            return frame

        for spec in sort_specs:
            self._require_column(spec.column)

        by = [spec.column for spec in sort_specs]
        descending = [spec.descending for spec in sort_specs]
        if len(by) == 1:
            return frame.sort(by[0], descending=descending[0], nulls_last=True)
        return frame.sort(by, descending=descending, nulls_last=True)

    def _filtered_total_rows(self, frame: Frame, filters: list[FilterSpec]) -> int:
        """Count rows in a filtered frame, caching per filter combination.

        Without this, every page fetch under an active filter re-counts the
        entire filtered dataset, making scrolling O(dataset) per page on lazy
        backends.
        """
        if not filters:
            return self.total_rows

        key: Any
        try:
            key = tuple(filters)
            hash(key)
        except TypeError:
            # Unhashable filter values (e.g. lists) skip the cache.
            key = None

        if key is not None and key in self._filtered_count_cache:
            return self._filtered_count_cache[key]

        total = self._frame_total_rows(frame)
        if key is not None:
            self._filtered_count_cache[key] = total
        return total

    def _frame_total_rows(self, frame: Frame) -> int:
        if frame is self._frame:
            return self.total_rows

        result = self._materialize(
            self._as_lazy(frame).select(nw.len().alias("__total_rows__"))
        )
        row = self._rows_from_frame(result)[0]
        return int(row["__total_rows__"])

    def _filter_expr(self, spec: FilterSpec) -> Any:
        dtype = self._schema[spec.column]
        expr = nw.col(spec.column)

        if spec.operator in {"contains", "starts_with", "ends_with"}:
            value = str(spec.value)
            if spec.operator == "contains":
                return expr.str.contains(value, literal=True)
            if spec.operator == "starts_with":
                return expr.str.starts_with(value)
            return expr.str.ends_with(value)

        value = self._coerce_filter_value(spec.column, spec.value)
        literal = nw.lit(value)

        if spec.operator == "eq":
            return expr == literal
        if spec.operator == "neq":
            return expr != literal
        if spec.operator == "gt":
            return expr > literal
        if spec.operator == "gte":
            return expr >= literal
        if spec.operator == "lt":
            return expr < literal
        if spec.operator == "lte":
            return expr <= literal
        if spec.operator == "between":
            if spec.value_to is None:
                raise ValueError(
                    f"Filter {spec.column!r} with operator 'between' requires value_to."
                )
            upper = nw.lit(self._coerce_filter_value(spec.column, spec.value_to))
            return (expr >= literal) & (expr <= upper)

        raise ValueError(f"Unsupported filter operator {spec.operator!r} for {dtype}.")

    def _coerce_filter_value(self, column: str, value: Any) -> Any:
        dtype = self._schema[column]
        if dtype == nw.Boolean:
            if isinstance(value, bool):
                return value
            text = str(value).strip().lower()
            if text in {"true", "t", "yes", "1"}:
                return True
            if text in {"false", "f", "no", "0"}:
                return False
            raise ValueError(
                f"Filter for {column!r} requires a boolean value (true/false)."
            )

        if dtype.is_numeric():
            text = str(value).strip()
            if text == "":
                raise ValueError(f"Filter for {column!r} requires a numeric value.")
            if dtype.is_integer() or dtype.is_signed_integer() or dtype.is_unsigned_integer():
                return int(text)
            return float(text)

        if dtype.is_temporal():
            text = str(value).strip()
            if text == "":
                raise ValueError(f"Filter for {column!r} requires a temporal value.")
            dtype_name = str(dtype).lower()
            if dtype_name == "date":
                return date.fromisoformat(text)
            # datetime-local inputs may omit seconds (e.g. "2023-10-10T13:01").
            if "T" in text and text.count(":") == 1:
                text += ":00"
            return datetime.fromisoformat(text)

        return value

    def _page_frame(self, frame: Frame, *, offset: int, limit: int) -> Frame:
        if isinstance(frame, nw.DataFrame):
            # Slice before any conversion; converting the whole frame to
            # Arrow first costs a full-table copy per page fetch.
            return cast(Frame, frame[offset : offset + limit])

        native = frame.to_native()
        paged_native = self._slice_native(native, offset=offset, limit=limit)
        paged_frame = nw.from_native(paged_native, eager_only=False)
        if not isinstance(paged_frame, (nw.DataFrame, nw.LazyFrame)):
            msg = f"Unexpected paged frame type {type(paged_frame)!r}."
            raise TypeError(msg)
        return paged_frame

    def _slice_native(self, native: Any, *, offset: int, limit: int) -> Any:
        if hasattr(native, "slice"):
            try:
                return native.slice(offset, limit)
            except TypeError:
                try:
                    return native.slice(offset=offset, length=limit)
                except TypeError:
                    pass

        if hasattr(native, "limit"):
            try:
                return native.limit(limit, offset=offset)
            except TypeError:
                try:
                    return native.limit(limit, offset)
                except TypeError:
                    pass

        # Spark (incl. Spark Connect / databricks-connect) has no offset on
        # limit, but exposes a separate `offset(n)` operator that composes:
        # df.offset(o).limit(n). offset() is a no-op at 0, so this also covers
        # backends where only `limit` takes a bare count.
        if hasattr(native, "offset") and hasattr(native, "limit"):
            try:
                return native.offset(offset).limit(limit)
            except TypeError:
                pass

        # `native` already carries the applied filters and sort; falling back
        # to self._frame here would silently discard them.
        if offset == 0 and hasattr(native, "head"):
            return native.head(limit)

        msg = (
            "This backend does not expose a native paginated slice API. "
            "tablescope can render the first page, but random-access jumps are "
            "not supported for this source yet."
        )
        raise NotImplementedError(msg)

    def _can_paginate_frame(self, frame: Frame) -> bool:
        if isinstance(frame, nw.DataFrame):
            return True
        native = frame.to_native()
        return hasattr(native, "slice") or hasattr(native, "limit")

    def _as_lazy(self, frame: Frame) -> nw.LazyFrame[Any]:
        if isinstance(frame, nw.LazyFrame):
            return frame
        return frame.lazy()

    def _materialize(self, frame: Frame) -> nw.DataFrame[Any]:
        if isinstance(frame, nw.DataFrame):
            return frame
        return frame.collect()

    def _rows_from_frame(
        self, frame: nw.DataFrame[Any], *, truncate: bool = False
    ) -> list[dict[str, Any]]:
        rows = frame.rows(named=True)
        return [self._jsonify_mapping(row, truncate=truncate) for row in rows]

    def _jsonify_mapping(
        self, value: dict[str, Any], *, truncate: bool = False
    ) -> dict[str, Any]:
        return {
            key: self._jsonify_cell(item, truncate=truncate)
            for key, item in value.items()
        }

    def _jsonify_cell(self, value: Any, *, truncate: bool) -> Any:
        # A cell's converted value is what actually ships to the browser; cap
        # it here, after conversion, so the budget reflects the on-the-wire
        # size (bytes become hex, so a blob doubles before this check).
        jsonified = self._jsonify_scalar(value)
        if not truncate or self._max_cell_bytes is None:
            return jsonified
        if self._cell_size(jsonified) <= self._max_cell_bytes:
            return jsonified
        return self._truncation_marker(value, jsonified)

    def _jsonify_scalar(self, value: Any) -> Any:
        # Non-finite floats serialize to the literals NaN/Infinity, which are
        # not valid JSON and break JSON.parse in the browser.
        if isinstance(value, float) and not isfinite(value):
            if isnan(value):
                return "NaN"
            return "Infinity" if value > 0 else "-Infinity"
        if isinstance(value, (datetime, date, time)):
            return value.isoformat()
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, bytes):
            return value.hex()
        if isinstance(value, dict):
            return {key: self._jsonify_scalar(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._jsonify_scalar(item) for item in value]
        return value

    def _cell_size(self, jsonified: Any) -> int:
        # Strings dominate the large-cell cases (hex blobs, long text), so size
        # them directly and skip the json.dumps cost. Collections need their
        # full serialized footprint, including nesting, to be judged fairly.
        if isinstance(jsonified, str):
            return len(jsonified)
        if isinstance(jsonified, (dict, list)):
            return len(json.dumps(jsonified, default=str))
        return 0

    def _truncation_marker(self, original: Any, jsonified: Any) -> dict[str, Any]:
        """Compact stand-in for an oversized cell value.

        Carries enough to render a useful placeholder (a short preview and the
        original magnitude) without shipping the whole payload. The full value
        is fetched on demand via fetch_cell.
        """
        budget = self._max_cell_bytes or 0
        preview_chars = min(256, budget)
        if isinstance(original, bytes):
            kind = "bytes"
            size = len(original)
            preview = original[: preview_chars // 2].hex()
        elif isinstance(jsonified, str):
            kind = "str"
            size = len(jsonified)
            preview = jsonified[:preview_chars]
        elif isinstance(jsonified, list):
            kind = "list"
            size = len(jsonified)
            preview = None
        elif isinstance(jsonified, dict):
            kind = "dict"
            size = len(jsonified)
            preview = None
        else:
            kind = "value"
            size = self._cell_size(jsonified)
            preview = str(jsonified)[:preview_chars]
        return {
            TRUNCATED_KEY: True,
            "kind": kind,
            "size": size,
            "preview": preview,
        }
