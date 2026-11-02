"""Input parsers: convert dicts/JSON to chart dataclass instances.

Each parser takes raw data (list of dicts or a single dict) and returns the
appropriate dataclass instances ready for chart constructors.
"""

from __future__ import annotations

from typing import Any, Sequence


class ParseError(Exception):
    """Raised when input data cannot be parsed into chart data models."""


def _require_keys(d: dict, keys: Sequence[str], context: str) -> None:
    """Raise ParseError if any required keys are missing from dict."""
    missing = [k for k in keys if k not in d]
    if missing:
        raise ParseError(f"{context}: missing required fields: {', '.join(missing)}")


def _coerce_float(value: Any, field_name: str, context: str) -> float:
    """Coerce a value to float with a clear error message."""
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ParseError(f"{context}: field {field_name!r} must be numeric, got {type(value).__name__}") from None


def _coerce_int(value: Any, field_name: str, context: str) -> int:
    """Coerce a value to int with a clear error message."""
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ParseError(f"{context}: field {field_name!r} must be integer, got {type(value).__name__}") from None


def _require_list(data: Any, context: str) -> list[dict]:
    """Validate that data is a non-empty list of dicts."""
    if not isinstance(data, list):
        raise ParseError(f"{context}: expected a list of objects, got {type(data).__name__}")
    if not data:
        raise ParseError(f"{context}: data list must not be empty")
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ParseError(f"{context}: item {i} must be an object, got {type(item).__name__}")
    return data


def _require_dict(data: Any, context: str) -> dict:
    """Validate that data is a dict."""
    if not isinstance(data, dict):
        raise ParseError(f"{context}: expected an object, got {type(data).__name__}")
    return data


def parse_bar(data: Any) -> list:
    """Parse bar chart data: list of {label, value, group?, error?, is_best?, is_worst?}."""
    from textcharts.bar_chart import BarData

    items = _require_list(data, "bar")
    result = []
    for i, d in enumerate(items):
        ctx = f"bar[{i}]"
        _require_keys(d, ["label", "value"], ctx)
        result.append(BarData(
            label=str(d["label"]),
            value=_coerce_float(d["value"], "value", ctx),
            group=str(d["group"]) if d.get("group") is not None else None,
            error=_coerce_float(d["error"], "error", ctx) if d.get("error") is not None else None,
            is_best=bool(d.get("is_best", False)),
            is_worst=bool(d.get("is_worst", False)),
        ))
    return result


def parse_histogram(data: Any) -> list:
    """Parse histogram data: list of {label, value, platform?, error?, is_best?, is_worst?}."""
    from textcharts.histogram import HistogramBar

    items = _require_list(data, "histogram")
    result = []
    for i, d in enumerate(items):
        ctx = f"histogram[{i}]"
        _require_keys(d, ["label", "value"], ctx)
        result.append(HistogramBar(
            label=str(d["label"]),
            value=_coerce_float(d["value"], "value", ctx),
            platform=str(d["platform"]) if d.get("platform") is not None else None,
            error=_coerce_float(d["error"], "error", ctx) if d.get("error") is not None else None,
            is_best=bool(d.get("is_best", False)),
            is_worst=bool(d.get("is_worst", False)),
        ))
    return result


def parse_heatmap(data: Any) -> dict[str, Any]:
    """Parse heatmap data: {matrix, row_labels, col_labels}.

    Returns a dict of constructor kwargs (matrix, row_labels, col_labels)
    since Heatmap doesn't use a single data model.
    """
    d = _require_dict(data, "heatmap")
    _require_keys(d, ["matrix", "row_labels", "col_labels"], "heatmap")

    matrix = d["matrix"]
    if not isinstance(matrix, list):
        raise ParseError("heatmap: 'matrix' must be a 2D array")
    row_labels = list(d["row_labels"])
    col_labels = list(d["col_labels"])

    if len(matrix) != len(row_labels):
        raise ParseError(
            f"heatmap: matrix has {len(matrix)} rows but row_labels has {len(row_labels)} entries"
        )

    parsed_matrix = []
    for i, row in enumerate(matrix):
        if not isinstance(row, list):
            raise ParseError(f"heatmap: matrix[{i}] must be an array")
        if len(row) != len(col_labels):
            raise ParseError(
                f"heatmap: matrix[{i}] has {len(row)} columns but col_labels has {len(col_labels)} entries"
            )
        parsed_matrix.append([float(v) if v is not None else None for v in row])

    return {"matrix": parsed_matrix, "row_labels": row_labels, "col_labels": col_labels}


def parse_boxplot(data: Any) -> list:
    """Parse box plot data: list of {name, values}."""
    from textcharts.box_plot import BoxPlotSeries

    items = _require_list(data, "boxplot")
    result = []
    for i, d in enumerate(items):
        ctx = f"boxplot[{i}]"
        _require_keys(d, ["name", "values"], ctx)
        values = d["values"]
        if not isinstance(values, list):
            raise ParseError(f"{ctx}: 'values' must be an array of numbers")
        result.append(BoxPlotSeries(
            name=str(d["name"]),
            values=[_coerce_float(v, f"values[{j}]", ctx) for j, v in enumerate(values)],
        ))
    return result


def parse_line(data: Any) -> list:
    """Parse line chart data: list of {series, x, y, label?}."""
    from textcharts.line_chart import LinePoint

    items = _require_list(data, "line")
    result = []
    for i, d in enumerate(items):
        ctx = f"line[{i}]"
        _require_keys(d, ["series", "x", "y"], ctx)
        x = d["x"]
        if isinstance(x, str):
            x_val: float | str = x
        else:
            x_val = _coerce_float(x, "x", ctx)
        result.append(LinePoint(
            series=str(d["series"]),
            x=x_val,
            y=_coerce_float(d["y"], "y", ctx),
            label=str(d["label"]) if d.get("label") is not None else None,
        ))
    return result


def parse_scatter(data: Any) -> list:
    """Parse scatter plot data: list of {name, x, y, is_pareto?}."""
    from textcharts.scatter_plot import ScatterPoint

    items = _require_list(data, "scatter")
    result = []
    for i, d in enumerate(items):
        ctx = f"scatter[{i}]"
        _require_keys(d, ["name", "x", "y"], ctx)
        result.append(ScatterPoint(
            name=str(d["name"]),
            x=_coerce_float(d["x"], "x", ctx),
            y=_coerce_float(d["y"], "y", ctx),
            is_pareto=bool(d.get("is_pareto", False)),
        ))
    return result


def parse_comparison(data: Any) -> list:
    """Parse comparison bar data: list of {label, baseline_value, comparison_value, ...}."""
    from textcharts.comparison_bar import ComparisonBarData

    items = _require_list(data, "comparison")
    result = []
    for i, d in enumerate(items):
        ctx = f"comparison[{i}]"
        _require_keys(d, ["label", "baseline_value", "comparison_value"], ctx)
        result.append(ComparisonBarData(
            label=str(d["label"]),
            baseline_value=_coerce_float(d["baseline_value"], "baseline_value", ctx),
            comparison_value=_coerce_float(d["comparison_value"], "comparison_value", ctx),
            baseline_name=str(d.get("baseline_name", "Baseline")),
            comparison_name=str(d.get("comparison_name", "Comparison")),
        ))
    return result


def parse_diverging(data: Any) -> list:
    """Parse diverging bar data: list of {label, pct_change}."""
    from textcharts.diverging_bar import DivergingBarData

    items = _require_list(data, "diverging")
    result = []
    for i, d in enumerate(items):
        ctx = f"diverging[{i}]"
        _require_keys(d, ["label", "pct_change"], ctx)
        result.append(DivergingBarData(
            label=str(d["label"]),
            pct_change=_coerce_float(d["pct_change"], "pct_change", ctx),
        ))
    return result


def parse_summary(data: Any) -> Any:
    """Parse summary box data: single object with stats fields."""
    from textcharts.summary_box import SummaryStats

    d = _require_dict(data, "summary")
    kwargs: dict[str, Any] = {}
    if "title" in d:
        kwargs["title"] = str(d["title"])

    float_fields = [
        "primary_value", "secondary_value", "total_value",
        "primary_baseline", "primary_comparison",
        "total_baseline", "total_comparison",
    ]
    for field_name in float_fields:
        if field_name in d and d[field_name] is not None:
            kwargs[field_name] = _coerce_float(d[field_name], field_name, "summary")

    int_fields = ["num_items", "num_improved", "num_stable", "num_regressed"]
    for field_name in int_fields:
        if field_name in d:
            kwargs[field_name] = _coerce_int(d[field_name], field_name, "summary")

    str_fields = [
        "baseline_name", "comparison_name", "metric_label",
        "primary_label", "secondary_label", "total_label", "count_label",
    ]
    for field_name in str_fields:
        if field_name in d:
            kwargs[field_name] = str(d[field_name])

    if "best_items" in d and d["best_items"] is not None:
        kwargs["best_items"] = [(str(q[0]), float(q[1])) for q in d["best_items"]]
    if "worst_items" in d and d["worst_items"] is not None:
        kwargs["worst_items"] = [(str(q[0]), float(q[1])) for q in d["worst_items"]]

    if "environment" in d and d["environment"] is not None:
        kwargs["environment"] = {str(k): str(v) for k, v in d["environment"].items()}
    if "platform_config" in d and d["platform_config"] is not None:
        kwargs["platform_config"] = {str(k): str(v) for k, v in d["platform_config"].items()}

    return SummaryStats(**kwargs)


def parse_percentile(data: Any) -> list:
    """Parse percentile ladder data: list of {name, p50, p90, p95, p99}."""
    from textcharts.percentile_ladder import PercentileData

    items = _require_list(data, "percentile")
    result = []
    for i, d in enumerate(items):
        ctx = f"percentile[{i}]"
        _require_keys(d, ["name", "p50", "p90", "p95", "p99"], ctx)
        result.append(PercentileData(
            name=str(d["name"]),
            p50=_coerce_float(d["p50"], "p50", ctx),
            p90=_coerce_float(d["p90"], "p90", ctx),
            p95=_coerce_float(d["p95"], "p95", ctx),
            p99=_coerce_float(d["p99"], "p99", ctx),
        ))
    return result


def parse_speedup(data: Any) -> list:
    """Parse normalized speedup data: list of {name, ratio, is_baseline?}."""
    from textcharts.normalized_speedup import SpeedupData

    items = _require_list(data, "speedup")
    result = []
    for i, d in enumerate(items):
        ctx = f"speedup[{i}]"
        _require_keys(d, ["name", "ratio"], ctx)
        result.append(SpeedupData(
            name=str(d["name"]),
            ratio=_coerce_float(d["ratio"], "ratio", ctx),
            is_baseline=bool(d.get("is_baseline", False)),
        ))
    return result


def parse_stacked(data: Any) -> list:
    """Parse stacked bar data: list of {label, segments: [{phase_name, value, color?}], total?}."""
    from textcharts.stacked_bar import StackedBarData, StackedBarSegment

    items = _require_list(data, "stacked")
    result = []
    for i, d in enumerate(items):
        ctx = f"stacked[{i}]"
        _require_keys(d, ["label", "segments"], ctx)
        segments_raw = d["segments"]
        if not isinstance(segments_raw, list):
            raise ParseError(f"{ctx}: 'segments' must be an array")
        segments = []
        for j, seg in enumerate(segments_raw):
            seg_ctx = f"{ctx}.segments[{j}]"
            if not isinstance(seg, dict):
                raise ParseError(f"{seg_ctx}: must be an object")
            _require_keys(seg, ["phase_name", "value"], seg_ctx)
            segments.append(StackedBarSegment(
                phase_name=str(seg["phase_name"]),
                value=_coerce_float(seg["value"], "value", seg_ctx),
                color=str(seg["color"]) if seg.get("color") is not None else None,
            ))
        result.append(StackedBarData(
            label=str(d["label"]),
            segments=segments,
            total=_coerce_float(d["total"], "total", ctx) if d.get("total") is not None else None,
        ))
    return result


def parse_sparkline(data: Any) -> Any:
    """Parse sparkline table data: {rows, columns: [{name, values, higher_is_better?}]}."""
    from textcharts.sparkline_table import SparklineColumn, SparklineTableData

    d = _require_dict(data, "sparkline")
    _require_keys(d, ["rows", "columns"], "sparkline")

    rows = [str(r) for r in d["rows"]]
    columns_raw = d["columns"]
    if not isinstance(columns_raw, list):
        raise ParseError("sparkline: 'columns' must be an array")

    columns = []
    for i, col in enumerate(columns_raw):
        ctx = f"sparkline.columns[{i}]"
        if not isinstance(col, dict):
            raise ParseError(f"{ctx}: must be an object")
        _require_keys(col, ["name", "values"], ctx)
        values = col["values"]
        if not isinstance(values, dict):
            raise ParseError(f"{ctx}: 'values' must be an object mapping row names to numbers")
        columns.append(SparklineColumn(
            name=str(col["name"]),
            values={str(k): _coerce_float(v, f"values.{k}", ctx) for k, v in values.items()},
            higher_is_better=bool(col.get("higher_is_better", False)),
        ))

    return SparklineTableData(rows=rows, columns=columns)


def parse_cdf(data: Any) -> list:
    """Parse CDF chart data: list of {name, values}."""
    from textcharts.cdf_chart import CDFSeriesData

    items = _require_list(data, "cdf")
    result = []
    for i, d in enumerate(items):
        ctx = f"cdf[{i}]"
        _require_keys(d, ["name", "values"], ctx)
        values = d["values"]
        if not isinstance(values, list):
            raise ParseError(f"{ctx}: 'values' must be an array of numbers")
        result.append(CDFSeriesData(
            name=str(d["name"]),
            values=[_coerce_float(v, f"values[{j}]", ctx) for j, v in enumerate(values)],
        ))
    return result


def parse_rank(data: Any) -> Any:
    """Parse rank table data: {items, groups, values}.

    Values is a dict with "group,item" string keys mapping to float values.
    """
    from textcharts.rank_table import RankTableData

    d = _require_dict(data, "rank")
    _require_keys(d, ["items", "groups", "values"], "rank")

    items = [str(item) for item in d["items"]]
    groups = [str(g) for g in d["groups"]]
    values_raw = d["values"]
    if not isinstance(values_raw, dict):
        raise ParseError("rank: 'values' must be an object mapping 'group,item' keys to numbers")

    values: dict[tuple[str, str], float] = {}
    for key, value in values_raw.items():
        parts = str(key).split(",", 1)
        if len(parts) != 2:
            raise ParseError(f"rank: values key {key!r} must be 'group,item' format")
        values[(parts[0].strip(), parts[1].strip())] = _coerce_float(value, f"values[{key}]", "rank")

    return RankTableData(items=items, groups=groups, values=values)


# Parser dispatch table: command name -> parser function
PARSERS: dict[str, Any] = {
    "bar": parse_bar,
    "histogram": parse_histogram,
    "heatmap": parse_heatmap,
    "boxplot": parse_boxplot,
    "line": parse_line,
    "scatter": parse_scatter,
    "comparison": parse_comparison,
    "diverging": parse_diverging,
    "summary": parse_summary,
    "percentile": parse_percentile,
    "speedup": parse_speedup,
    "stacked": parse_stacked,
    "sparkline": parse_sparkline,
    "cdf": parse_cdf,
    "rank": parse_rank,
}


def parse_input(command: str, data: Any) -> Any:
    """Parse input data for a command, returning chart-ready dataclass instance(s).

    For most commands, returns a list of dataclass instances.
    For heatmap, returns a dict of constructor kwargs.
    For summary/sparkline/rank, returns a single dataclass instance.
    """
    parser = PARSERS.get(command)
    if parser is None:
        available = ", ".join(sorted(PARSERS))
        raise ParseError(f"No parser for command {command!r}. Available: {available}")
    return parser(data)
