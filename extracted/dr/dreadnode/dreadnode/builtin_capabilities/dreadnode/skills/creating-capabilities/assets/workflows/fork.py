"""Fixed fork and typed join. Input {"text": "one two"} returns {"words": 2, "characters": 7}."""

from pydantic import BaseModel

from dreadnode.workflows import Collect, Ctx, StartEvent, StopEvent, Workflow, WorkflowEvent


class Input(BaseModel):
    text: str


class ForWords(WorkflowEvent):
    text: str


class ForCharacters(WorkflowEvent):
    text: str


class WordCount(WorkflowEvent):
    count: int


class CharacterCount(WorkflowEvent):
    count: int


workflow = Workflow(name="text-metrics", input=Input)


@workflow.step
async def split(ctx: Ctx, ev: StartEvent[Input]) -> tuple[ForWords, ForCharacters]:
    """A tuple runs both paths; a union would choose one."""
    return ForWords(text=ev.input.text), ForCharacters(text=ev.input.text)


@workflow.step
async def words(ctx: Ctx, ev: ForWords) -> WordCount:
    return WordCount(count=len(ev.text.split()))


@workflow.step
async def characters(ctx: Ctx, ev: ForCharacters) -> CharacterCount:
    return CharacterCount(count=len(ev.text))


@workflow.step(min_success="all")
async def finish(ctx: Ctx, ev: Collect[WordCount, CharacterCount]) -> StopEvent[dict[str, int]]:
    """Retrieve one successful event of each type after both paths settle."""
    return StopEvent(
        result={"words": ev.get(WordCount).count, "characters": ev.get(CharacterCount).count}
    )
