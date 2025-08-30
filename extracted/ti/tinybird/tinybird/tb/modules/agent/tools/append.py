import os
from typing import Optional

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    TinybirdAgentContext,
    copy_fixture_to_project_folder_if_needed,
    show_confirmation,
    show_env_options,
    show_input,
)
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_pretty_table
from tinybird.tb.modules.feedback_manager import FeedbackManager


def append_file(
    ctx: RunContext[TinybirdAgentContext], datasource_name: str, fixture_pathname: str, cloud: Optional[bool] = None
) -> str:
    """Append a fixture file to a datasource

    Args:
        datasource_name: Name of the datasource to append fixture to
        fixture_pathname: Path to the fixture file to append
        cloud: Whether to append the fixture to the cloud or local environment. If None (user didn't specify in a previous step), will ask user to clarify. Defaults to local (False) in dangerous skip permissions mode.

    Returns:
        str: Message indicating the success or failure of the appending
    """
    try:
        ctx.deps.thinking_animation.stop()
        fixture_path_or_error = copy_fixture_to_project_folder_if_needed(ctx, fixture_pathname)

        if isinstance(fixture_path_or_error, str):
            ctx.deps.thinking_animation.start()
            return fixture_path_or_error

        fixture_path = fixture_path_or_error
        fixture_pathname = os.path.relpath(fixture_path, ctx.deps.folder)

        # Handle cloud parameter - ask user if uncertain and not in dangerous skip mode
        if cloud is None:
            if ctx.deps.dangerously_skip_permissions:
                # Default to local when in dangerous skip mode
                cloud = False
            else:
                # Ask the user to choose execution mode
                cloud = show_env_options(ctx)
                if cloud is None:
                    ctx.deps.thinking_animation.start()
                    return "Append operation cancelled by user."

        cloud_or_local = "Cloud" if cloud else "Local"
        active_plan = ctx.deps.get_plan() is not None and not cloud
        ctx.deps.thinking_animation.stop()
        confirmation = show_confirmation(
            title=f"Append fixture {fixture_pathname} to datasource '{datasource_name}' in Tinybird {cloud_or_local}?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm appending {fixture_pathname} fixture in Tinybird {cloud_or_local} and gave the following feedback: {feedback}"

        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Appending {fixture_pathname} to {datasource_name}..."))
        if cloud:
            ctx.deps.append_data_cloud(datasource_name=datasource_name, path=fixture_pathname)
        else:
            ctx.deps.append_data_local(datasource_name=datasource_name, path=fixture_pathname)
        click.echo(FeedbackManager.success(message=f"✓ Data appended to {datasource_name}"))
        ctx.deps.thinking_animation.start()
        return f"Data appended to {datasource_name} in Tinybird {cloud_or_local}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        error_message = str(e)
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=error_message))
        error_message = handle_quarantine_error(ctx, error_message, datasource_name)
        ctx.deps.thinking_animation.start()
        return f"Error appending fixture {fixture_pathname} to {datasource_name} in Tinybird {cloud_or_local}: {error_message}"


def append_url(
    ctx: RunContext[TinybirdAgentContext], datasource_name: str, fixture_url: str, cloud: Optional[bool] = None
) -> str:
    """Append existing fixture to a datasource

    Args:
        datasource_name: Name of the datasource to append fixture to
        fixture_url: external url to the fixture file to append
        cloud: Whether to append the fixture to the cloud or local environment. If None (user didn't specify), will ask user to clarify. Defaults to local (False) in dangerous skip permissions mode.

    Returns:
        str: Message indicating the success or failure of the appending
    """
    try:
        ctx.deps.thinking_animation.stop()

        # Handle cloud parameter - ask user if uncertain and not in dangerous skip mode
        if cloud is None:
            if ctx.deps.dangerously_skip_permissions:
                # Default to local when in dangerous skip mode
                cloud = False
            else:
                # Ask the user to choose execution mode
                cloud = show_env_options(ctx)
                if cloud is None:
                    ctx.deps.thinking_animation.start()
                    return "Append operation cancelled by user."

        cloud_or_local = "Cloud" if cloud else "Local"
        active_plan = ctx.deps.get_plan() is not None and not cloud
        confirmation = show_confirmation(
            title=f"Append URL {fixture_url} to datasource '{datasource_name}' in Tinybird {cloud_or_local}?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm appending URL {fixture_url} in Tinybird {cloud_or_local} and gave the following feedback: {feedback}"

        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Appending {fixture_url} to {datasource_name}..."))
        if cloud:
            ctx.deps.append_data_cloud(datasource_name=datasource_name, path=fixture_url)
        else:
            ctx.deps.append_data_local(datasource_name=datasource_name, path=fixture_url)
        click.echo(FeedbackManager.success(message=f"✓ Data appended to {datasource_name}"))
        ctx.deps.thinking_animation.start()
        return f"Data appended to {datasource_name} in Tinybird {cloud_or_local}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        error_message = str(e)
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=error_message))
        error_message = handle_quarantine_error(ctx, error_message, datasource_name)
        ctx.deps.thinking_animation.start()
        return f"Error appending URL {fixture_url} to {datasource_name} in Tinybird {cloud_or_local}: {error_message}"


def handle_quarantine_error(
    ctx: RunContext[TinybirdAgentContext], error_message: str, datasource_name: str, cloud: Optional[bool] = None
) -> str:
    try:
        if "in quarantine" in error_message:
            # Default to local if cloud is None for error handling
            if cloud is None:
                cloud = False
            cloud_or_local = "Cloud" if cloud else "Local"
            click.echo(FeedbackManager.highlight(message=f"» Looking for errors in {datasource_name}_quarantine..."))
            query = f"select * from {datasource_name}_quarantine order by insertion_date desc limit 5 FORMAT JSON"
            result = ctx.deps.execute_query_cloud(query=query) if cloud else ctx.deps.execute_query_local(query=query)
            quarantine_data = result["data"] or []
            quarantine_meta = result["meta"] or []
            column_names = [c["name"] for c in quarantine_meta]
            echo_safe_humanfriendly_tables_format_pretty_table(
                data=[d.values() for d in quarantine_data], column_names=column_names
            )
            error_message = (
                error_message
                + f"\nThese are the first 5 rows of the quarantine table for datasource '{datasource_name}' in {cloud_or_local}:\n{quarantine_data}"
            )

    except Exception as quarantine_error:
        error_message = (
            error_message + f"\nError accessing to {datasource_name}_quarantine in {cloud_or_local}: {quarantine_error}"
        )

    return error_message
