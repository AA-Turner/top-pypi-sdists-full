import click

from tinybird.tb.modules.agent import run_agent
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.exceptions import CLIMockException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project


@cli.command()
@click.argument("datasource", type=str)
@click.option("--rows", type=int, default=10, help="Number of events to send")
@click.option(
    "--prompt",
    type=str,
    default="",
    help="Extra context to use for data generation",
)
@click.option(
    "--format",
    "format_",
    type=click.Choice(["ndjson", "csv"], case_sensitive=False),
    default="ndjson",
    help="Format of the fixture to create",
)
@click.pass_context
def mock(ctx: click.Context, datasource: str, rows: int, prompt: str, format_: str) -> None:
    """Generate sample data for a data source."""

    try:
        project: Project = ctx.ensure_object(dict)["project"]
        ctx_config = ctx.ensure_object(dict)["config"]
        prompt = f"""Generate mock data for the following datasource: {datasource} with {rows} rows and {format_} format. Extra context: {prompt}"""
        env = ctx.ensure_object(dict)["env"]
        if env == "cloud":
            prompt += "Append the fixture data to the datasource in Tinybird Cloud."

        run_agent(ctx_config, project, True, prompt=prompt, feature="tb_mock")

    except Exception as e:
        raise CLIMockException(FeedbackManager.error(message=str(e)))
