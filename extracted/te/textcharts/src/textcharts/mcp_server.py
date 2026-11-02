"""MCP server exposing textcharts as tools.

Thin wrapper around the shared command layer. Each chart type becomes an MCP
tool with the same command name, parameters, and behavior as the CLI.

Usage:
    pip install textcharts[mcp]
    textcharts-mcp              # starts stdio MCP server

MCP config:
    {"mcpServers": {"textcharts": {"command": "textcharts-mcp"}}}
"""

from __future__ import annotations

import json
import sys
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP

    _HAS_MCP = True
except ImportError:
    _HAS_MCP = False

from textcharts.commands import execute_command, list_commands
from textcharts.commands.parsers import ParseError
from textcharts.commands.registry import REGISTRY, describe_command


def _build_tool_description(name: str) -> str:
    """Build a rich tool description from the command registry."""
    desc = describe_command(name)
    lines = [desc["description"], ""]
    lines.append(f"Input: {desc['data_format']}")
    lines.append("")
    lines.append("Data fields:")
    for field in desc["data_fields"]:
        req = "required" if field["required"] else "optional"
        default = f", default: {field['default']}" if "default" in field else ""
        lines.append(f"  - {field['name']} ({field['type']}, {req}{default}): {field['description']}")

    if desc["chart_params"]:
        lines.append("")
        lines.append("Chart parameters (pass via 'chart_params' dict):")
        for param in desc["chart_params"]:
            default = f", default: {param['default']}" if "default" in param else ""
            enum = f", options: {param['enum']}" if "enum" in param else ""
            lines.append(f"  - {param['name']} ({param['type']}{default}{enum}): {param['description']}")

    return "\n".join(lines)


def _create_chart_handler(chart_name: str):
    """Create an async handler function for a chart tool."""
    cmd_info = REGISTRY[chart_name]
    chart_param_names = [p.name for p in cmd_info.chart_params]

    async def handler(
        data: list[dict[str, Any]] | dict[str, Any],
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        width: int | None = None,
        height: int | None = None,
        use_color: bool = True,
        use_unicode: bool = True,
        theme: str = "light",
        show_legend: bool = True,
        show_values: bool = True,
        outlier_cap: float | None = None,
        chart_params: dict[str, Any] | None = None,
    ) -> str:
        """Render a chart from data.

        Args:
            data: Chart data (list of objects or single object depending on chart type).
            title: Optional chart title.
            subtitle: Optional subtitle line displayed below the title.
            subject: Domain noun phrase prepended to default title
                (e.g. "Query Latency" produces "Query Latency Histogram").
            width: Chart width in characters.
            height: Chart height in rows.
            use_color: Enable ANSI color output.
            use_unicode: Enable Unicode box-drawing characters.
            theme: Color theme ("light" or "dark").
            show_legend: Show chart legend.
            show_values: Show numeric values on chart.
            outlier_cap: Fixed scale cap for outliers (auto P95-based if omitted, 0 disables).
            chart_params: Chart-specific parameters (see tool description for available params).
        """
        options: dict[str, Any] = {
            "use_color": use_color,
            "use_unicode": use_unicode,
            "theme": theme,
            "show_legend": show_legend,
            "show_values": show_values,
        }
        if width is not None:
            options["width"] = width
        if height is not None:
            options["height"] = height
        if outlier_cap is not None:
            options["outlier_cap"] = outlier_cap

        # Extract chart-specific params
        chart_kwargs: dict[str, Any] = {}
        if chart_params:
            valid_names = set(chart_param_names)
            chart_kwargs = {k: v for k, v in chart_params.items() if k in valid_names}

        try:
            return execute_command(
                chart_name, data, title=title, subtitle=subtitle,
                subject=subject, options=options, **chart_kwargs,
            )
        except (ParseError, KeyError, ValueError, TypeError) as e:
            return f"Error: {e}"

    # Set function metadata for FastMCP schema generation
    handler.__name__ = f"textcharts_{chart_name}"
    handler.__qualname__ = f"textcharts_{chart_name}"

    return handler


def create_server() -> Any:
    """Create and configure the MCP server with all chart tools.

    Returns the FastMCP server instance. Separated from main() for testability.
    """
    if not _HAS_MCP:
        raise ImportError(
            "The 'mcp' package is required for the MCP server. "
            "Install it with: pip install textcharts[mcp]"
        )

    server = FastMCP(
        name="textcharts",
        instructions=(
            "Terminal chart visualization server. Use the textcharts_list tool to discover "
            "available chart types, then call the appropriate textcharts_<type> tool with your data."
        ),
    )

    # Register a tool for each chart type
    for name in sorted(REGISTRY):
        handler = _create_chart_handler(name)
        server.add_tool(
            handler,
            name=f"textcharts_{name}",
            description=_build_tool_description(name),
        )

    # Meta-tool: list available chart types
    @server.tool(name="textcharts_list", description="List all available textcharts chart types with descriptions")
    async def tool_list() -> str:
        commands = list_commands()
        lines = [f"Available chart types ({len(commands)}):"]
        for cmd_name, desc in commands:
            lines.append(f"  textcharts_{cmd_name}: {desc}")
        lines.append("")
        lines.append("Call any tool above with your data. Use textcharts_describe for detailed usage info.")
        return "\n".join(lines)

    # Meta-tool: describe a chart type
    @server.tool(
        name="textcharts_describe",
        description="Get detailed usage information for a specific chart type including data format and parameters",
    )
    async def tool_describe(chart_type: str) -> str:
        """Describe a chart type's parameters and input format.

        Args:
            chart_type: Chart type name (e.g., "bar", "heatmap", "line").
        """
        # Strip prefix if user passes "textcharts_bar" instead of "bar"
        if chart_type.startswith("textcharts_"):
            chart_type = chart_type[len("textcharts_"):]

        try:
            desc = describe_command(chart_type)
        except KeyError:
            available = ", ".join(name for name, _ in list_commands())
            return f"Unknown chart type: {chart_type!r}. Available: {available}"

        return json.dumps(desc, indent=2)

    return server


def main() -> None:
    """Entry point for the textcharts-mcp console script."""
    if not _HAS_MCP:
        print(
            "Error: The 'mcp' package is required for the MCP server.\n"
            "Install it with: pip install textcharts[mcp]",
            file=sys.stderr,
        )
        sys.exit(1)

    server = create_server()
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
