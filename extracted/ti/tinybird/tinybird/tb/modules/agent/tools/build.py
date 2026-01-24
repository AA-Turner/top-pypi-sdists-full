import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.exceptions import CLIBuildException
from tinybird.tb.modules.feedback_manager import FeedbackManager


def build(ctx: RunContext[TinybirdAgentContext]) -> str:
    """Build the project"""
    try:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message="» Building project..."))
        ctx.deps.build_project(test=False, silent=False, load_fixtures=False)
        ctx.deps.thinking_animation.start()
        return "Project built successfully"
    except CLIBuildException as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error building project: {e}"
