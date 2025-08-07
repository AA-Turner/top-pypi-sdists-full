import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import humanfriendly
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext, show_env_options
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_pretty_table
from tinybird.tb.modules.feedback_manager import FeedbackManager

forbidden_commands = [
    "currentDatabase()",
    "create table",
    "insert into",
    "create database",
    "show tables",
    "show datasources",
    "truncate table",
    "delete from",
    "system.tables",
    "system.datasources",
    "information_schema.tables",
]

forbidden_commands_start_with = [
    "describe",
]


def execute_query(
    ctx: RunContext[TinybirdAgentContext],
    query: str,
    task: str,
    cloud_or_local: Optional[str] = None,
    script: Optional[str] = None,
    export_format: Optional[str] = None,
    explanation_why_not_know_about_last_environment: Optional[str] = None,
):
    """Execute a query and return the result as a table, chart or exported file.

    Args:
        query (str): The query to execute. Required.
        task (str): The purpose of the query. Required.
        cloud_or_local (str): Whether to execute the query on cloud or local. Use the last environment used in previous queries or endpoint requests. If you don't have any information about the last environment, use None. Options: cloud, local.
        script (str): Python script using plotext to render the query results as a chart. The script will have access to 'data' (list of dicts), 'meta' (list of column info dicts), 'terminal_width' and 'terminal_height' variables. Always use plt.theme("clear") for transparent background and plt.plot_size(terminal_width, terminal_height) for proper sizing. For bar charts, use the simple versions: plt.simple_bar(), plt.simple_multiple_bar(), and plt.simple_stacked_bar(). Optional.
        export_format (str): The format to export the query results to. Options: csv, json, ndjson. Optional.
        explanation_why_not_know_about_last_environment (str): Why you don't know about the last environment used in previous queries or endpoint requests. Required.

    Returns:
        str: The result of the query.
    """
    try:
        for forbidden_command in forbidden_commands:
            if forbidden_command in query.lower():
                return f"Error executing query: {forbidden_command} is not allowed."

        for forbidden_command in forbidden_commands_start_with:
            if query.lower().startswith(forbidden_command):
                return f"Error executing query: {forbidden_command} is not allowed."

        # Handle cloud_or_local parameter - ask user if uncertain and not in dangerous skip mode
        if cloud_or_local is None:
            if ctx.deps.dangerously_skip_permissions:
                # Default to local when in dangerous skip mode
                cloud_or_local = "local"
            else:
                # Ask the user to choose execution mode

                cloud = show_env_options(ctx)
                if cloud is None:
                    return "Query execution cancelled by user."
                cloud_or_local = "cloud" if cloud else "local"

        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Executing query to {cloud_or_local}:\n{query}\n"))
        is_templating = query.strip().startswith("%")
        query_format = "JSON"
        if export_format == "csv":
            query_format = "CSVWithNames"
        elif export_format == "ndjson":
            query_format = "JSONEachRow"
        elif export_format == "json":
            query_format = "JSON"

        if is_templating:
            query = query.strip()
            query = f"%\nSELECT * FROM ({query}) FORMAT {query_format}"
        else:
            query = f"SELECT * FROM ({query}) FORMAT {query_format}"

        execute_query = ctx.deps.execute_query_cloud if cloud_or_local == "cloud" else ctx.deps.execute_query_local
        result = execute_query(query=query)
        if export_format:
            file_extension = f".{export_format}"
            filename = f"export_{export_format}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if not filename.endswith(file_extension):
                filename = f"{filename}{file_extension}"

            file_path = Path(ctx.deps.folder) / filename

            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write raw ClickHouse formatted data directly to file
            with open(file_path, "w", encoding="utf-8") as f:
                if export_format == "json":
                    content = json.dumps(result)
                else:
                    content = str(result)
                f.write(content)
            ctx.deps.thinking_animation.start()
            return f"Successfully exported data to {file_path} ({export_format.upper()} format)"

        stats = result["statistics"]
        seconds = stats["elapsed"]
        rows_read = humanfriendly.format_number(stats["rows_read"])
        bytes_read = humanfriendly.format_size(stats["bytes_read"])

        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))
        click.echo()

        if not result["data"]:
            click.echo(FeedbackManager.info_no_rows())
        else:
            if script:
                try:
                    # Execute the LLM-generated plotext script
                    chart_output = _execute_plotext_script(script, result["data"], result["meta"])
                    click.echo(chart_output)
                except Exception as script_error:
                    click.echo(
                        FeedbackManager.error(message=f"There was an error rendering the chart.\n{script_error}")
                    )
                    ctx.deps.thinking_animation.start()
                    return f"After executing the query: {query}, there was an error rendering the chart: {script_error}. Fix the script and render the chart again."
            else:
                echo_safe_humanfriendly_tables_format_pretty_table(
                    data=[d.values() for d in result["data"]], column_names=result["data"][0].keys()
                )
                click.echo("Showing first 10 results\n")

        ctx.deps.thinking_animation.start()
        display_format = "chart" if script else "table"
        return f"Result for task '{task}' in {cloud_or_local} environment: {result}. The user is being shown the result as a {display_format} in the console, so do not render that again."
    except Exception as e:
        error = str(e)
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=error))
        ctx.deps.thinking_animation.start()
        if "not found" in error.lower() and cloud:
            return f"Error executing query: {error}. Please run the query against Tinybird local instead of cloud."
        else:
            return f"Error executing query: {error}. Please try again."


def _execute_plotext_script(script: str, data: List[Dict[str, Any]], meta: List[Dict[str, str]]) -> str:
    """Execute a plotext script with the provided data using exec().

    Args:
        script: Python script using plotext
        data: Query result data
        meta: Query result metadata

    Returns:
        Chart output as string
    """
    import io
    from contextlib import redirect_stdout

    try:
        # Capture stdout
        output = io.StringIO()

        # Prepare globals with data and required imports
        script_globals = {
            "data": data,
            "meta": meta,
            "__builtins__": __builtins__,
        }

        # Import required modules into the script namespace
        exec("import plotext as plt", script_globals)
        exec("import json", script_globals)
        exec("from datetime import datetime", script_globals)
        exec("import re", script_globals)
        exec("import os", script_globals)

        # Clear any previous plot data to prevent chart reuse
        exec("plt.clear_data()", script_globals)

        # Get terminal dimensions and make them available
        try:
            terminal_size = os.get_terminal_size()
            terminal_width = terminal_size.columns
            terminal_height = max(20, terminal_size.lines // 3)  # Use 1/3 of terminal height, min 20
        except:
            terminal_width = 80
            terminal_height = 20

        script_globals["terminal_width"] = terminal_width
        script_globals["terminal_height"] = terminal_height

        # Execute the user script with stdout capture
        with redirect_stdout(output):
            exec(script, script_globals)

        # Clean up after rendering to prevent state leakage
        exec("plt.clear_data()", script_globals)
        exec("plt.clear_figure()", script_globals)

        return output.getvalue()

    except Exception as e:
        raise Exception(f"Script execution error: {str(e)}")
