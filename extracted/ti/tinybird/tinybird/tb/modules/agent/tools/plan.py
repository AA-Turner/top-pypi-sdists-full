import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext, show_confirmation, show_input


def plan(ctx: RunContext[TinybirdAgentContext], plan: str) -> str:
    """Given a plan, ask the user for confirmation to implement it

    Args:
        plan (str): The plan to implement. Required.

    Returns:
        str: If the plan was implemented or not.
    """
    ctx.deps.thinking_animation.stop()
    plan = plan.strip()
    click.echo(plan)
    confirmation = show_confirmation(
        title="Do you want to continue with the plan?", skip_confirmation=ctx.deps.dangerously_skip_permissions
    )

    if confirmation == "review":
        feedback = show_input(ctx.deps.workspace_name)
        ctx.deps.thinking_animation.start()
        return f"User did not confirm the proposed plan and gave the following feedback: {feedback}"

    ctx.deps.thinking_animation.start()
    return "User confirmed the plan. Implementing..."
