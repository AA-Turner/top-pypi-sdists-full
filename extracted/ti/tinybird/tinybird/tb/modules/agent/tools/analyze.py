import json
from urllib.parse import urlparse

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    TinybirdAgentContext,
    copy_fixture_to_project_folder_if_needed,
)
from tinybird.tb.modules.feedback_manager import FeedbackManager


def analyze_file(ctx: RunContext[TinybirdAgentContext], fixture_pathname: str):
    """Analyze a fixture data file present in the project folder or outside by copying it to the project folder before analyzing

    Args:
        fixture_pathname (str): a path or an external url to a fixture file. Required.

    Returns:
        str: The content of the fixture data file.
    """
    try:
        ctx.deps.thinking_animation.stop()
        fixture_path_or_error = copy_fixture_to_project_folder_if_needed(ctx, fixture_pathname)

        if isinstance(fixture_path_or_error, str):
            ctx.deps.thinking_animation.start()
            return fixture_path_or_error

        fixture_path = fixture_path_or_error

        click.echo(FeedbackManager.highlight(message=f"» Analyzing {fixture_path.name}..."))

        if not fixture_path.exists():
            click.echo(FeedbackManager.error(message=f"No fixture data found for {fixture_pathname}."))
            ctx.deps.thinking_animation.start()
            return f"No fixture data found for {fixture_pathname}. Please check the path of the fixture and try again."

        fixture_extension = fixture_path.suffix.lstrip(".")
        response = ctx.deps.analyze_fixture(fixture_path=str(fixture_path), format=fixture_extension)
        click.echo(FeedbackManager.success(message="✓ Done!\n"))
        ctx.deps.thinking_animation.start()
        # limit content to first 10 rows
        data = response["preview"]["data"][:10]
        columns = response["analysis"]["columns"]

        return f"#Result of analysis of {fixture_path.name}:\n##Columns:\n{json.dumps(columns)}\n##Data sample:\n{json.dumps(data)}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=f"Error analyzing {fixture_pathname}: {e}"))
        ctx.deps.thinking_animation.start()
        return f"Error analyzing {fixture_pathname}: {e}"


def analyze_url(ctx: RunContext[TinybirdAgentContext], fixture_url: str):
    """Analyze a fixture file present in an external url

    Args:
        fixture_url (str): an external url to a fixture file. Required.

    Returns:
        str: The analysis with the columns and the first 10 rows of the fixture data file.
    """
    try:
        ctx.deps.thinking_animation.stop()
        is_url = urlparse(fixture_url).scheme in ("http", "https")
        click.echo(FeedbackManager.highlight(message=f"» Analyzing {fixture_url}..."))
        if not is_url:
            click.echo(FeedbackManager.error(message=f"{fixture_url} is not a valid url."))
            ctx.deps.thinking_animation.start()
            return f"{fixture_url} is not a valid url. Please check the url and try again."

        fixture_extension = fixture_url.split(".")[-1]

        response = ctx.deps.analyze_fixture(fixture_path=fixture_url, format=fixture_extension)
        click.echo(FeedbackManager.success(message="✓ Done!\n"))
        ctx.deps.thinking_animation.start()
        # limit content to first 10 rows
        data = response["preview"]["data"][:10]
        columns = response["analysis"]["columns"]

        return f"#Result of analysis of URL {fixture_url}:\n##Columns:\n{json.dumps(columns)}\n##Data sample:\n{json.dumps(data)}"
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=f"Error analyzing {fixture_url}: {e}"))
        ctx.deps.thinking_animation.start()
        return f"Error analyzing {fixture_url}: {e}"
