import subprocess

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import AgentRunCancelled, TinybirdAgentContext, show_confirmation, show_input
from tinybird.tb.modules.feedback_manager import FeedbackManager


def run_command(ctx: RunContext[TinybirdAgentContext], command: str):
    """Run a tinybird CLI command with the given arguments

    Args:
        command (str): The command to run. Required. Examples: `tb --local sql "select 1"`, `tb --cloud datasource ls`, `tb --help`
    """
    try:
        ctx.deps.thinking_animation.stop()
        force_confirmation = " deploy" in command.lower() or " truncate" in command.lower()
        confirmation = show_confirmation(
            title=f"Run command: {command}?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions and not force_confirmation,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the command and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message=f"» Running command: {command}"))
        command = command.replace("tb", "tb --no-version-warning")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        click.echo(result.stdout)
        ctx.deps.thinking_animation.start()
        return result.stdout
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Error running command: {e}"))
        ctx.deps.thinking_animation.start()
        return f"Error running command: {e}"
