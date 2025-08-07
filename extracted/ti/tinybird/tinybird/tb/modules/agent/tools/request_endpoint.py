from typing import Optional

import click
import humanfriendly
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext, limit_result_output, show_env_options
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_pretty_table
from tinybird.tb.modules.feedback_manager import FeedbackManager


def request_endpoint(
    ctx: RunContext[TinybirdAgentContext],
    endpoint_name: str,
    params: Optional[dict[str, str]] = None,
    cloud_or_local: Optional[str] = None,
    explanation_why_not_know_about_last_environment: Optional[str] = None,
):
    """Request an endpoint:

    Args:
        endpoint_name (str): The name of the endpoint to request. Required.
        params (dict): The parameters to pass to the endpoint. Optional.
        cloud_or_local (str): Whether to request the endpoint on cloud or local. Use the last environment used in previous queries or endpoint requests. If you don't have any information about the last environment, use None. Options: cloud, local. Optional.
        explanation_why_not_know_about_last_environment (str): Why you don't know about the last environment used in previous queries or endpoint requests. Required.

    Returns:
        str: The result of the query.
    """
    try:
        # Handle cloud parameter - ask user if uncertain and not in dangerous skip mode
        if cloud_or_local is None:
            if ctx.deps.dangerously_skip_permissions:
                # Default to local when in dangerous skip mode
                cloud_or_local = "local"
            else:
                # Ask the user to choose execution mode
                cloud = show_env_options(ctx)
                if cloud is None:
                    return "Endpoint request cancelled by user."
                cloud_or_local = "cloud" if cloud else "local"
        ctx.deps.thinking_animation.stop()
        with_params = f" with params {params}" if params else ""
        click.echo(
            FeedbackManager.highlight(
                message=f"» Calling endpoint {endpoint_name} in {cloud_or_local} environment{with_params}"
            )
        )

        request_endpoint = (
            ctx.deps.request_endpoint_cloud if cloud_or_local == "cloud" else ctx.deps.request_endpoint_local
        )
        result = request_endpoint(endpoint_name=endpoint_name, params=params)

        # Apply output limiting using the utility function
        result, truncated_columns = limit_result_output(result)

        stats = result["statistics"]
        seconds = stats["elapsed"]
        rows_read = humanfriendly.format_number(stats["rows_read"])
        bytes_read = humanfriendly.format_size(stats["bytes_read"])

        click.echo(FeedbackManager.success_print_pipe(pipe=endpoint_name))
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

        if not result["data"]:
            click.echo(FeedbackManager.info_no_rows())
        else:
            echo_safe_humanfriendly_tables_format_pretty_table(
                data=[d.values() for d in result["data"]], column_names=result["data"][0].keys()
            )
            click.echo("Showing first 10 results\n")

        # Prepare return message with truncation info
        truncation_info = ""
        if truncated_columns:
            truncated_list = ", ".join(sorted(truncated_columns))
            truncation_info = (
                f" Note: The following columns had values truncated due to length > 200 characters: {truncated_list}."
            )

        ctx.deps.thinking_animation.start()
        return f"Result for endpoint {endpoint_name} with params {params} in {cloud_or_local} environment: {result}. Do not show result is already shown in the console.{truncation_info}"
    except Exception as e:
        error = str(e)
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=error))
        ctx.deps.thinking_animation.start()
        not_found_errors = ["not found", "does not exist"]
        if any(not_found_error in error.lower() for not_found_error in not_found_errors) and cloud:
            return f"Error executing query: {error}. Please run the query against Tinybird local instead of cloud."
        else:
            return f"Error executing query: {error}. Please try again."
