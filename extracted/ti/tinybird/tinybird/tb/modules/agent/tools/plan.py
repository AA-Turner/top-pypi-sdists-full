from typing import Literal

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    TinybirdAgentContext,
    show_input,
    show_options,
)

PlanConfirmationResult = Literal["yes", "review", "yes_and_auto_implement"]


def show_plan_confirmation(skip_confirmation: bool = False) -> PlanConfirmationResult:
    if skip_confirmation:
        return "yes"

    title = "Do you want to continue with the plan?"
    while True:
        result = show_options(
            options=[
                "Yes, continue",
                "Yes, continue and implement all",
                "No, tell Tinybird Code what to do",
                "Cancel",
            ],
            title=title,
        )

        if result is None:  # Cancelled
            raise AgentRunCancelled(f"User cancelled the operation: {title}")

        if result.startswith("Yes, continue and implement all"):
            return "yes_and_auto_implement"
        if result.startswith("Yes"):
            return "yes"
        elif result.startswith("No"):
            return "review"

        raise AgentRunCancelled(f"User cancelled the operation: {title}")


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
    confirmation = show_plan_confirmation(skip_confirmation=ctx.deps.dangerously_skip_permissions)

    if confirmation == "review":
        feedback = show_input(ctx.deps.workspace_name)
        ctx.deps.thinking_animation.start()
        ctx.deps.cancel_plan()
        return f"User did not confirm the proposed plan and gave the following feedback: {feedback}"

    ctx.deps.thinking_animation.start()

    if confirmation == "yes_and_auto_implement":
        plan_id = ctx.deps.start_plan(plan=plan)
        return f"User confirmed the plan {plan_id}. Implementing..."
    else:
        return "User confirmed the plan. Implementing..."


def complete_plan(ctx: RunContext[TinybirdAgentContext]) -> str:
    """Given an ongoing plan, complete it

    Args:
        ctx (RunContext[TinybirdAgentContext]): The context of the agent.

    Returns:
        str: The result of the plan.
    """

    plan_id = ctx.deps.cancel_plan()
    return f"Plan {plan_id} completed"
