"""Two steps, no model or API. Input {"text": " hello "} returns "HELLO"."""

from pydantic import BaseModel

from dreadnode.workflows import Ctx, StartEvent, StopEvent, Workflow, WorkflowEvent


class Input(BaseModel):
    text: str


class Cleaned(WorkflowEvent):
    text: str


workflow = Workflow(name="normalize", input=Input)


@workflow.step
async def clean(ctx: Ctx, ev: StartEvent[Input]) -> Cleaned:
    """Pass data to the next step through a typed event."""
    return Cleaned(text=ev.input.text.strip())


@workflow.step
async def finish(ctx: Ctx, ev: Cleaned) -> StopEvent[str]:
    """Return the run's result."""
    return StopEvent(result=ev.text.upper())
