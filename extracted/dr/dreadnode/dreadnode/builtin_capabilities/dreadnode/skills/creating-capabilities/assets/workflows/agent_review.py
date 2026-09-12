"""Typed agent output. Requires the capability's reviewer agent and a configured model."""

from pydantic import BaseModel

from dreadnode.workflows import Ctx, StartEvent, StopEvent, Workflow, WorkflowEvent


class Input(BaseModel):
    text: str


class Reviewed(WorkflowEvent):
    summary: str
    approved: bool


workflow = Workflow(name="review-text", input=Input)


@workflow.step(timeout_sec=120)
async def review(ctx: Ctx, ev: StartEvent[Input]) -> Reviewed:
    """The literal name must match a declared capability agent."""
    result = await ctx.agent(
        "reviewer",
        f"Review this text for clarity: {ev.input.text!r}. "
        'Return only JSON with a string "summary" and a boolean "approved".',
        max_steps=3,
    )
    return result.parse(Reviewed)


@workflow.step
async def finish(ctx: Ctx, ev: Reviewed) -> StopEvent[Reviewed]:
    """Preserve structured data in the result instead of parsing prose downstream."""
    return StopEvent(result=ev)
