"""judge a model response: did it answer, did the token limit cut it, did this call end the run or lose a write."""

from __future__ import annotations
import re
from typing import Any
from pydantic_ai import RunContext
from pydantic_ai.exceptions import UnexpectedModelBehavior
from probe.daemon.agent import tools
#: Pydantic AI's own words (`_agent_graph`, pinned 2.51.0) for a response the token
#: limit cut off before any of it was an answer, or in the middle of a tool call
#: (`IncompleteToolCall`). gpt-6.1-sol spent the provider's 16,384-token default
#: thinking (strand-ai, 2026-10-09..12: 126 such calls, one request sent 14 times).
_NO_ANSWER = re.compile(r"Model token limit \(.*?\) exceeded (before any response was generated|while "
                        r"generating a tool call)")
#: What the daemon says when that happened.
ANSWERED_NOTHING = "the model thought until its token limit and answered nothing"


#: pydantic-ai's own message when a tool asked for one retry more than its budget.
_TOOL_RETRIES = re.compile(r"Tool '[^']*' exceeded max retries count of \d+")


def tool_retries_spent(exc: BaseException) -> bool:
    """Did a tool run out of retries (the library's own message, caused by the
    tool's `ModelRetry`)? Not the model's own answer failing: an output that
    keeps failing its validation says "Exceeded maximum output retries"."""
    from pydantic_ai import ModelRetry

    return (isinstance(exc, UnexpectedModelBehavior) and isinstance(exc.__cause__, ModelRetry)
            and bool(_TOOL_RETRIES.match(exc.message or "")))


def answered_nothing(exc: BaseException) -> bool:
    """Did the model spend its whole token limit before answering anything? The
    same request does the same again, so it is never retried as it was. Only the
    library's own message counts: never a body a model's words could fill."""
    return isinstance(exc, UnexpectedModelBehavior) and bool(_NO_ANSWER.match(exc.message or ""))


def answered(response: Any) -> bool:
    """Did a model response come back with an answer? Only one the token limit cut
    off (`finish_reason` "length") can be none: when it holds no words and no
    complete tool call -- a call cut off mid arguments is no answer, the way
    Pydantic AI's own `IncompleteToolCall` check reads it. Any other response is
    one, a turn that only thought included (its retry is the model's next round)."""
    from pydantic_ai.messages import TextPart, ToolCallPart

    if response.finish_reason != "length":
        return True
    for part in response.parts:
        if isinstance(part, TextPart) and part.content.strip():
            return True
        if isinstance(part, ToolCallPart):
            try:
                part.args_as_dict(raise_if_invalid=True)
            except Exception:  # noqa: BLE001 -- arguments cut off mid way
                continue
            return True
    return False


def ends_run(ctx: RunContext) -> bool:
    """Whether the response this tool call came in also calls `final_result`:
    under pydantic-ai's default 'graceful' end strategy the run ends once the
    tools before it ran, and the model never reads their answers."""
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    last = ctx.messages[-1] if ctx.messages else None
    return isinstance(last, ModelResponse) and any(
        isinstance(p, ToolCallPart) and p.tool_name == FINAL_RESULT for p in last.parts)


def lost_write_retry(ctx: RunContext[tools.Deps], lost_before: int, output: str) -> None:
    """Raise `ModelRetry` (which suppresses the run's end) when this call lost a
    write (`Deps.lost_writes` grew) in a response that also ends the run. Not on
    the tool's last attempt: past it the call answers an error instead
    (`RetriesSpentAreRefusals`), and the worker's open-failures list still shows
    the write to the next one."""
    from pydantic_ai import ModelRetry

    if ctx.deps.lost_writes > lost_before and not ctx.last_attempt and ends_run(ctx):
        raise ModelRetry(WRITE_LOST.format(output=output))
from probe.daemon.agent.agent import FINAL_RESULT, WRITE_LOST  # noqa: E402 -- pieces need each other; the front door loads this one first
