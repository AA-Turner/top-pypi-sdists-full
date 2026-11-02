"""Command registry mapping chart names to their classes, data models, and schemas.

The registry is the single source of truth for both CLI and MCP. It defines
command names, descriptions, chart-specific parameters, and JSON input schemas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ParamInfo:
    """Describes a chart-specific parameter."""

    name: str
    type: str  # "string", "number", "integer", "boolean"
    description: str
    default: Any = None
    enum: list[str] | None = None


@dataclass(frozen=True)
class DataFieldInfo:
    """Describes a field in the input data model."""

    name: str
    type: str  # "string", "number", "boolean", "array", "object"
    description: str
    required: bool = True
    default: Any = None


@dataclass(frozen=True)
class CommandInfo:
    """Complete descriptor for a chart command."""

    name: str
    description: str
    chart_module: str  # e.g., "textcharts.bar_chart"
    chart_class: str  # e.g., "BarChart" — module-level class name
    data_param_name: str  # Constructor param name for data: "data", "points", "series", "stats", "matrix"
    data_fields: list[DataFieldInfo] = field(default_factory=list)
    input_is_list: bool = True  # True if data is a list of items, False if single object
    chart_params: list[ParamInfo] = field(default_factory=list)
    extra_data_params: list[str] = field(default_factory=list)  # Extra constructor params from input (e.g., row_labels)


def _build_registry() -> dict[str, CommandInfo]:
    """Build the command registry. Called once at import time."""
    return {
        "bar": CommandInfo(
            name="bar",
            description="Horizontal bar chart for comparing values across categories",
            chart_module="textcharts.bar_chart",
            chart_class="BarChart",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("label", "string", "Category label"),
                DataFieldInfo("value", "number", "Numeric value"),
                DataFieldInfo("group", "string", "Optional grouping key", required=False),
                DataFieldInfo("error", "number", "Optional error margin", required=False),
                DataFieldInfo("is_best", "boolean", "Mark as best performer", required=False, default=False),
                DataFieldInfo("is_worst", "boolean", "Mark as worst performer", required=False, default=False),
            ],
            chart_params=[
                ParamInfo("metric_label", "string", "Label for the value axis", "Value"),
                ParamInfo("sort_by", "string", "Sort order", "value", enum=["value", "label", "none"]),
            ],
        ),
        "histogram": CommandInfo(
            name="histogram",
            description="Vertical bar chart for frequency distribution or categorical comparison",
            chart_module="textcharts.histogram",
            chart_class="Histogram",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("label", "string", "Category or item label"),
                DataFieldInfo("value", "number", "Numeric value"),
                DataFieldInfo("platform", "string", "Optional platform name", required=False),
                DataFieldInfo("error", "number", "Optional error margin", required=False),
                DataFieldInfo("is_best", "boolean", "Mark as best performer", required=False, default=False),
                DataFieldInfo("is_worst", "boolean", "Mark as worst performer", required=False, default=False),
            ],
            chart_params=[
                ParamInfo("y_label", "string", "Label for the Y axis", "Value"),
                ParamInfo("sort_by", "string", "Sort order", "label", enum=["label", "value"]),
                ParamInfo("max_per_chart", "integer", "Max bars before splitting", 25),
                ParamInfo("show_mean_line", "boolean", "Show mean reference line", True),
            ],
        ),
        "heatmap": CommandInfo(
            name="heatmap",
            description="Matrix heatmap with color intensity showing value magnitude",
            chart_module="textcharts.heatmap",
            chart_class="Heatmap",
            data_param_name="matrix",
            input_is_list=False,
            data_fields=[
                DataFieldInfo("matrix", "array", "2D array of numeric values (rows x cols); null for missing"),
                DataFieldInfo("row_labels", "array", "Labels for each row"),
                DataFieldInfo("col_labels", "array", "Labels for each column"),
            ],
            extra_data_params=["row_labels", "col_labels"],
            chart_params=[
                ParamInfo("value_label", "string", "Unit label for values", ""),
                ParamInfo("x_label", "string", "Label for column axis", "Columns"),
                ParamInfo("show_values", "boolean", "Display numeric values in cells", True),
                ParamInfo("color_scheme", "string", "Color scheme", "diverging", enum=["diverging", "sequential"]),
            ],
        ),
        "boxplot": CommandInfo(
            name="boxplot",
            description="Box plot showing distribution with quartiles, whiskers, and outliers",
            chart_module="textcharts.box_plot",
            chart_class="BoxPlot",
            data_param_name="series",
            data_fields=[
                DataFieldInfo("name", "string", "Series name"),
                DataFieldInfo("values", "array", "Array of numeric values"),
            ],
            chart_params=[
                ParamInfo("y_label", "string", "Label for the value axis", "Value"),
                ParamInfo("show_stats", "boolean", "Show statistical summary", True),
                ParamInfo("show_mean", "boolean", "Show mean marker", True),
            ],
        ),
        "line": CommandInfo(
            name="line",
            description="Line chart for time series or trend visualization",
            chart_module="textcharts.line_chart",
            chart_class="LineChart",
            data_param_name="points",
            data_fields=[
                DataFieldInfo("series", "string", "Series name for grouping"),
                DataFieldInfo("x", "number", "X-axis value (numeric or string)"),
                DataFieldInfo("y", "number", "Y-axis value"),
                DataFieldInfo("label", "string", "Optional point label", required=False),
            ],
            chart_params=[
                ParamInfo("x_label", "string", "Label for X axis", "X"),
                ParamInfo("y_label", "string", "Label for Y axis", "Y"),
                ParamInfo("show_trend", "boolean", "Show trend line", False),
            ],
        ),
        "scatter": CommandInfo(
            name="scatter",
            description="Scatter plot for visualizing X/Y relationships with optional Pareto frontier",
            chart_module="textcharts.scatter_plot",
            chart_class="ScatterPlot",
            data_param_name="points",
            data_fields=[
                DataFieldInfo("name", "string", "Point label"),
                DataFieldInfo("x", "number", "X-axis value"),
                DataFieldInfo("y", "number", "Y-axis value"),
                DataFieldInfo("is_pareto", "boolean", "Mark as Pareto-optimal", required=False, default=False),
            ],
            chart_params=[
                ParamInfo("x_label", "string", "Label for X axis", "X"),
                ParamInfo("y_label", "string", "Label for Y axis", "Y"),
                ParamInfo("show_pareto", "boolean", "Show Pareto frontier", True),
            ],
        ),
        "comparison": CommandInfo(
            name="comparison",
            description="Side-by-side paired bar chart comparing baseline vs. comparison values",
            chart_module="textcharts.comparison_bar",
            chart_class="ComparisonBar",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("label", "string", "Item label"),
                DataFieldInfo("baseline_value", "number", "Baseline measurement"),
                DataFieldInfo("comparison_value", "number", "Comparison measurement"),
                DataFieldInfo(
                    "baseline_name", "string", "Name for baseline series", required=False, default="Baseline"
                ),
                DataFieldInfo(
                    "comparison_name", "string", "Name for comparison series", required=False, default="Comparison"
                ),
            ],
            chart_params=[
                ParamInfo("metric_label", "string", "Label for the value axis", "Value"),
            ],
        ),
        "diverging": CommandInfo(
            name="diverging",
            description="Centered diverging bar chart showing positive/negative change as percentage change",
            chart_module="textcharts.diverging_bar",
            chart_class="DivergingBar",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("label", "string", "Item label"),
                DataFieldInfo("pct_change", "number", "Percentage change (negative=improvement, positive=regression)"),
            ],
            chart_params=[
                ParamInfo("clip_pct", "number", "Outlier clipping threshold percentage", 200.0),
                ParamInfo("lower_is_better", "boolean", "Treat negative change as improvement", True),
            ],
        ),
        "summary": CommandInfo(
            name="summary",
            description="Bordered summary box with aggregate statistics and environment info",
            chart_module="textcharts.summary_box",
            chart_class="SummaryBox",
            data_param_name="stats",
            input_is_list=False,
            data_fields=[
                DataFieldInfo("title", "string", "Summary box title", required=False, default="Summary"),
                DataFieldInfo(
                    "primary_value", "number", "Primary aggregate value (e.g. geometric mean)", required=False
                ),
                DataFieldInfo("secondary_value", "number", "Secondary aggregate value (e.g. median)", required=False),
                DataFieldInfo("total_value", "number", "Total aggregate value", required=False),
                DataFieldInfo("primary_baseline", "number", "Baseline primary value", required=False),
                DataFieldInfo("primary_comparison", "number", "Comparison primary value", required=False),
                DataFieldInfo("total_baseline", "number", "Baseline total value", required=False),
                DataFieldInfo("total_comparison", "number", "Comparison total value", required=False),
                DataFieldInfo("baseline_name", "string", "Baseline label", required=False, default="Baseline"),
                DataFieldInfo("comparison_name", "string", "Comparison label", required=False, default="Comparison"),
                DataFieldInfo("num_items", "integer", "Number of items", required=False, default=0),
                DataFieldInfo("num_improved", "integer", "Count of improved items", required=False, default=0),
                DataFieldInfo("num_stable", "integer", "Count of stable items", required=False, default=0),
                DataFieldInfo("num_regressed", "integer", "Count of regressed items", required=False, default=0),
                DataFieldInfo("best_items", "array", "List of [name, value] pairs for best items", required=False),
                DataFieldInfo(
                    "worst_items", "array", "List of [name, value] pairs for worst items", required=False
                ),
                DataFieldInfo("environment", "object", "Environment info dict (OS, Python, etc.)", required=False),
                DataFieldInfo("platform_config", "object", "Platform config dict", required=False),
                DataFieldInfo(
                    "metric_label", "string",
                    "Unit label for values (e.g. ms, ops)",
                    required=False, default="ms",
                ),
                DataFieldInfo("primary_label", "string", "Label for primary metric", required=False, default="Primary"),
                DataFieldInfo(
                    "secondary_label", "string", "Label for secondary metric",
                    required=False, default="Secondary",
                ),
                DataFieldInfo("total_label", "string", "Label for total metric", required=False, default="Total"),
                DataFieldInfo("count_label", "string", "Label for item count", required=False, default="Items"),
            ],
        ),
        "percentile": CommandInfo(
            name="percentile",
            description="Layered percentile bands showing P50/P90/P95/P99 distribution",
            chart_module="textcharts.percentile_ladder",
            chart_class="PercentileLadder",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("name", "string", "Series name"),
                DataFieldInfo("p50", "number", "50th percentile value"),
                DataFieldInfo("p90", "number", "90th percentile value"),
                DataFieldInfo("p95", "number", "95th percentile value"),
                DataFieldInfo("p99", "number", "99th percentile value"),
            ],
            chart_params=[
                ParamInfo("metric_label", "string", "Unit label for values", ""),
            ],
        ),
        "speedup": CommandInfo(
            name="speedup",
            description="Log-scale normalized speedup chart relative to a baseline",
            chart_module="textcharts.normalized_speedup",
            chart_class="NormalizedSpeedup",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("name", "string", "Platform or variant name"),
                DataFieldInfo("ratio", "number", "Speedup ratio (2.0 = 2x faster, 0.5 = 2x slower)"),
                DataFieldInfo("is_baseline", "boolean", "Mark as baseline (ratio=1.0)", required=False, default=False),
            ],
            chart_params=[
                ParamInfo("baseline_name", "string", "Name of the baseline for labeling", None),
            ],
        ),
        "stacked": CommandInfo(
            name="stacked",
            description="Stacked horizontal bar chart showing phase or component breakdown",
            chart_module="textcharts.stacked_bar",
            chart_class="StackedBar",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("label", "string", "Bar label"),
                DataFieldInfo(
                    "segments",
                    "array",
                    "List of {phase_name, value, color?} segments",
                ),
                DataFieldInfo("total", "number", "Override total (auto-computed if omitted)", required=False),
            ],
            chart_params=[
                ParamInfo("metric_label", "string", "Unit label for values", ""),
            ],
        ),
        "sparkline": CommandInfo(
            name="sparkline",
            description="Compact table with inline sparkline mini-charts for multi-metric comparison",
            chart_module="textcharts.sparkline_table",
            chart_class="SparklineTable",
            data_param_name="data",
            input_is_list=False,
            data_fields=[
                DataFieldInfo("rows", "array", "List of row names"),
                DataFieldInfo(
                    "columns",
                    "array",
                    "List of {name, values: {row: number}, higher_is_better?} column definitions",
                ),
            ],
        ),
        "cdf": CommandInfo(
            name="cdf",
            description="Cumulative distribution function chart for comparing value distributions",
            chart_module="textcharts.cdf_chart",
            chart_class="CDFChart",
            data_param_name="data",
            data_fields=[
                DataFieldInfo("name", "string", "Series name"),
                DataFieldInfo("values", "array", "Array of numeric values"),
            ],
            chart_params=[
                ParamInfo("x_label", "string", "Label for X axis", "Value"),
                ParamInfo("y_label", "string", "Label for Y axis", "Cumulative Share"),
                ParamInfo("height", "integer", "Plot height in rows", 15),
            ],
        ),
        "rank": CommandInfo(
            name="rank",
            description="Competitive ranking table with win counts across items",
            chart_module="textcharts.rank_table",
            chart_class="RankTable",
            data_param_name="data",
            input_is_list=False,
            data_fields=[
                DataFieldInfo("items", "array", "List of item names"),
                DataFieldInfo("groups", "array", "List of group names"),
                DataFieldInfo("values", "object", "Mapping of 'group,item' keys to numeric values"),
            ],
        ),
    }


REGISTRY: dict[str, CommandInfo] = _build_registry()

COMMON_OPTIONS: list[ParamInfo] = [
    ParamInfo("width", "integer", "Chart width in characters (auto-detect if omitted)"),
    ParamInfo("height", "integer", "Chart height in rows (auto-detect if omitted)"),
    ParamInfo("use_color", "boolean", "Enable ANSI color output", True),
    ParamInfo("use_unicode", "boolean", "Enable Unicode box-drawing characters", True),
    ParamInfo("theme", "string", "Color theme", "light", enum=["light", "dark"]),
    ParamInfo("show_legend", "boolean", "Show chart legend", True),
    ParamInfo("show_values", "boolean", "Show numeric values on chart", True),
    ParamInfo("outlier_cap", "number", "Fixed scale cap for outliers (auto P95-based if omitted, 0 disables)"),
]


def get_command(name: str) -> CommandInfo:
    """Get a command descriptor by name. Raises KeyError if not found."""
    try:
        return REGISTRY[name]
    except KeyError:
        available = ", ".join(sorted(REGISTRY))
        raise KeyError(f"Unknown command {name!r}. Available commands: {available}") from None


def list_commands() -> list[tuple[str, str]]:
    """Return list of (name, description) for all registered commands, sorted by name."""
    return [(cmd.name, cmd.description) for cmd in sorted(REGISTRY.values(), key=lambda c: c.name)]


def describe_command(name: str) -> dict[str, Any]:
    """Return full description of a command including parameters and input schema."""
    cmd = get_command(name)
    return {
        "name": cmd.name,
        "description": cmd.description,
        "data_format": "list of objects" if cmd.input_is_list else "single object",
        "data_fields": [
            {
                "name": f.name,
                "type": f.type,
                "description": f.description,
                "required": f.required,
                **({"default": f.default} if f.default is not None else {}),
            }
            for f in cmd.data_fields
        ],
        "chart_params": [
            {
                "name": p.name,
                "type": p.type,
                "description": p.description,
                **({"default": p.default} if p.default is not None else {}),
                **({"enum": p.enum} if p.enum else {}),
            }
            for p in cmd.chart_params
        ],
        "common_options": [
            {
                "name": p.name,
                "type": p.type,
                "description": p.description,
                **({"default": p.default} if p.default is not None else {}),
                **({"enum": p.enum} if p.enum else {}),
            }
            for p in COMMON_OPTIONS
        ],
    }


def get_input_schema(name: str) -> dict[str, Any]:
    """Return JSON-Schema-like dict describing the input data format for a command."""
    cmd = get_command(name)

    if cmd.input_is_list:
        item_properties: dict[str, Any] = {}
        required_fields = []
        for f in cmd.data_fields:
            prop: dict[str, Any] = {"type": f.type, "description": f.description}
            if f.default is not None:
                prop["default"] = f.default
            item_properties[f.name] = prop
            if f.required:
                required_fields.append(f.name)

        data_schema: dict[str, Any] = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": item_properties,
                "required": required_fields,
            },
        }
    else:
        obj_properties: dict[str, Any] = {}
        required_fields = []
        for f in cmd.data_fields:
            prop = {"type": f.type, "description": f.description}
            if f.default is not None:
                prop["default"] = f.default
            obj_properties[f.name] = prop
            if f.required:
                required_fields.append(f.name)

        data_schema = {
            "type": "object",
            "properties": obj_properties,
            "required": required_fields,
        }

    # Build full tool schema with data + title + chart params + common options
    properties: dict[str, Any] = {"data": data_schema}
    properties["title"] = {"type": "string", "description": "Chart title"}

    for p in cmd.chart_params:
        prop = {"type": p.type, "description": p.description}
        if p.default is not None:
            prop["default"] = p.default
        if p.enum:
            prop["enum"] = p.enum
        properties[p.name] = prop

    for p in COMMON_OPTIONS:
        prop = {"type": p.type, "description": p.description}
        if p.default is not None:
            prop["default"] = p.default
        if p.enum:
            prop["enum"] = p.enum
        properties[p.name] = prop

    return {
        "type": "object",
        "properties": properties,
        "required": ["data"],
    }
