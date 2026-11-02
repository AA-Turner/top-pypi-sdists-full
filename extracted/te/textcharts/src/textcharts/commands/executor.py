"""Command executor: dispatch command name + data + options to chart rendering.

This is the single entry point that both CLI and MCP call.
"""

from __future__ import annotations

import importlib
from typing import Any

from textcharts.commands.parsers import ParseError, parse_input
from textcharts.commands.registry import get_command


def execute_command(
    command: str,
    data: Any,
    title: str | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    options: dict[str, Any] | None = None,
    **kwargs: Any,
) -> str:
    """Execute a chart command and return the rendered string.

    Args:
        command: Chart command name (e.g., "bar", "heatmap").
        data: Raw input data (list of dicts or single dict, depending on chart type).
        title: Optional chart title.
        subtitle: Optional subtitle line displayed below the title.
        subject: Domain noun phrase prepended to default title (e.g. "Query Latency").
        options: Common chart options dict (width, height, use_color, use_unicode, theme, etc.).
        **kwargs: Chart-specific parameters (e.g., sort_by, metric_label).

    Returns:
        Rendered chart as a string.

    Raises:
        KeyError: If command name is unknown.
        ParseError: If input data is invalid.
        ValueError: If chart-specific parameters are invalid.
    """
    cmd_info = get_command(command)

    # Parse input data into chart-ready form
    parsed_data = parse_input(command, data)

    # Build ChartOptions from options dict
    chart_options = _build_chart_options(options)

    # Build constructor kwargs
    ctor_kwargs: dict[str, Any] = {}

    # Set data parameter — heatmap returns a dict of kwargs, others return data directly
    if command == "heatmap":
        if not isinstance(parsed_data, dict):
            raise ParseError("heatmap parser must return a dict")
        ctor_kwargs.update(parsed_data)
    else:
        ctor_kwargs[cmd_info.data_param_name] = parsed_data

    if title is not None:
        # SummaryBox has title inside the SummaryStats dataclass, not as a constructor param
        if command == "summary":
            parsed_data.title = title
        else:
            ctor_kwargs["title"] = title

    if subtitle is not None:
        ctor_kwargs["subtitle"] = subtitle

    if subject is not None:
        ctor_kwargs["subject"] = subject

    if chart_options is not None:
        ctor_kwargs["options"] = chart_options

    # Apply chart-specific parameters from kwargs
    valid_param_names = {p.name for p in cmd_info.chart_params}
    for key, value in kwargs.items():
        if key in valid_param_names:
            ctor_kwargs[key] = value

    # Import and instantiate the chart class
    module = importlib.import_module(cmd_info.chart_module)
    chart_cls = getattr(module, cmd_info.chart_class)
    chart = chart_cls(**ctor_kwargs)

    return chart.render()


def _build_chart_options(options: dict[str, Any] | None) -> Any | None:
    """Convert an options dict to a ChartOptions instance."""
    if not options:
        return None

    from textcharts.base import ChartOptions

    opt_kwargs: dict[str, Any] = {}
    field_map = {
        "width": "width",
        "height": "height",
        "use_color": "use_color",
        "use_unicode": "use_unicode",
        "theme": "theme",
        "show_legend": "show_legend",
        "show_values": "show_values",
        "outlier_cap": "outlier_cap",
    }
    for key, attr in field_map.items():
        if key in options and options[key] is not None:
            opt_kwargs[attr] = options[key]

    if not opt_kwargs:
        return None

    return ChartOptions(**opt_kwargs)
