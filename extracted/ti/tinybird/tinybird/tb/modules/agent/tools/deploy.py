import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext, show_confirmation, show_input
from tinybird.tb.modules.exceptions import CLIDeploymentException
from tinybird.tb.modules.feedback_manager import FeedbackManager


def deploy(ctx: RunContext[TinybirdAgentContext], allow_destructive_operations: bool = False) -> str:
    """Deploy the project

    Args:
        allow_destructive_operations (bool): Set to true if a datasource, pipe or connection file has been deleted locally.
                                           Optional. Default is False.

    Returns:
        str: The result of the deployment
    """
    try:
        ctx.deps.thinking_animation.stop()

        if allow_destructive_operations:
            click.echo(
                FeedbackManager.warning(message="Destructive operations flag is enabled due to a file deleted recently")
            )

        click.echo("")
        confirmation = show_confirmation(
            title="Deploy the project?",
            skip_confirmation=False,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm deployment and gave the following feedback: {feedback}"

        allow_destructive_operations_flag = " --allow-destructive-operations" if allow_destructive_operations else ""
        click.echo(
            FeedbackManager.highlight(
                message=f"» Running command: tb --cloud deploy{allow_destructive_operations_flag}"
            )
        )
        ctx.deps.deploy_project(allow_destructive_operations=allow_destructive_operations)
        click.echo(FeedbackManager.success(message="✓ Project deployed successfully"))
        ctx.deps.thinking_animation.start()
        return "Project deployed successfully"
    except CLIDeploymentException as e:
        ctx.deps.thinking_animation.start()
        return f"Error depoying project: {e}"
