"""Exclusive branch. Input {"text": "hello", "flagged": true} returns "review: hello"."""

from pydantic import BaseModel

from dreadnode.workflows import Ctx, StartEvent, StopEvent, Workflow, WorkflowEvent


class Input(BaseModel):
    text: str
    flagged: bool = False


class NeedsReview(WorkflowEvent):
    text: str


class Accepted(WorkflowEvent):
    text: str


workflow = Workflow(name="route-text", input=Input)


@workflow.step
async def route(ctx: Ctx, ev: StartEvent[Input]) -> NeedsReview | Accepted:
    """Return exactly one event; the other path is recorded as skipped."""
    if ev.input.flagged:
        return NeedsReview(text=ev.input.text)
    return Accepted(text=ev.input.text)


@workflow.step
async def review(ctx: Ctx, ev: NeedsReview) -> StopEvent[str]:
    """This example labels the result; it does not request a human approval gate."""
    return StopEvent(result=f"review: {ev.text}")


@workflow.step
async def accept(ctx: Ctx, ev: Accepted) -> StopEvent[str]:
    """Every branch has its own terminal result."""
    return StopEvent(result=f"accepted: {ev.text}")
