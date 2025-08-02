from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext, show_confirmation, show_input
from tinybird.tb.modules.exceptions import CLIDeploymentException


def deploy_check(ctx: RunContext[TinybirdAgentContext]) -> str:
    """Check that project can be deployed"""
    try:
        ctx.deps.thinking_animation.stop()
        confirmation = show_confirmation(
            title="Check that project can be deployed?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm deployment check and gave the following feedback: {feedback}"

        ctx.deps.deploy_check_project()
        ctx.deps.thinking_animation.start()
        return "Project can be deployed"
    except CLIDeploymentException as e:
        ctx.deps.thinking_animation.start()
        return f"Project cannot be deployed: {e}"
