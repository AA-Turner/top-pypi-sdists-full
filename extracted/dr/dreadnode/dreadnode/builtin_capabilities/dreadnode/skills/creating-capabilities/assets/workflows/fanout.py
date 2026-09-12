"""Bounded fan-out and join. Input {"texts": ["one two", "three"]} returns 3."""

from pydantic import BaseModel, Field

from dreadnode.workflows import Collect, Ctx, StartEvent, StopEvent, Workflow, WorkflowEvent


class Input(BaseModel):
    texts: list[str] = Field(max_length=25)


class TextTask(WorkflowEvent):
    text: str


class Counted(WorkflowEvent):
    words: int


workflow = Workflow(name="count-texts", input=Input)


@workflow.step(materialization_cap=25)
async def plan(ctx: Ctx, ev: StartEvent[Input]) -> list[TextTask]:
    """The producer bounds how many instances can be created."""
    return [TextTask(text=text) for text in ev.input.texts]


@workflow.step(max_concurrency=3, timeout_sec=30)
async def count(ctx: Ctx, ev: TextTask) -> Counted:
    """The consumer bounds simultaneous instances; errors become node failures."""
    if not ev.text.strip():
        raise ValueError("text must contain at least one word")
    return Counted(words=len(ev.text.split()))


@workflow.step(min_success="all")
async def finish(ctx: Ctx, ev: Collect[Counted]) -> StopEvent[int]:
    """Require every count to succeed; an empty input list returns zero."""
    return StopEvent(result=sum(item.words for item in ev.ok))
