"""Test an agent without a real model: a scripted model answers each model call in order."""

import json
from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass
from typing import Self

from pydantic import JsonValue

from mistralai.vibe.harness.core.protocol import TextContentBlock
from mistralai.vibe.harness.runtime.completion.models import (
    CompletionError,
    CompletionFailure,
    CompletionRequest,
    CompletionStreamItem,
    CompletionUsage,
    ModelAssistantContentDelta,
    ModelCompletionFinished,
    ModelToolCallArgumentsDelta,
    ModelToolCallStartedDelta,
)


@dataclass(frozen=True, slots=True)
class ToolCallStep:
    """One model call that asks to run a tool."""

    name: str
    arguments: dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class ReplyStep:
    """One model call that answers with text."""

    text: str


type _Step = ToolCallStep | ReplyStep


def call(name: str, /, **arguments: JsonValue) -> ToolCallStep:
    """Script a model call that asks for the tool ``name``, the name the model sees, with ``arguments``."""
    return ToolCallStep(name=name, arguments=arguments)


def reply(text: str) -> ReplyStep:
    """Script a model call that answers with ``text``."""
    return ReplyStep(text=text)


class ScriptedModel:
    """Answer each model call with the next step of the script, in order."""

    def __init__(self, steps: Sequence[_Step]) -> None:
        self._steps = tuple(steps)
        self._used = 0

    def __deepcopy__(self, memo: dict[int, object]) -> Self:
        # Every copy of an overridden Agent plays the same script.
        memo[id(self)] = self
        return self

    async def complete(self, request: CompletionRequest) -> AsyncIterator[CompletionStreamItem]:
        """Stream the next step of the script, whatever the request."""
        del request
        index = self._used
        if index >= len(self._steps):
            raise CompletionError(
                CompletionFailure(
                    kind="provider",
                    retryable=False,
                    message=(
                        f"ScriptedModel has no step for model call {index + 1}; "
                        f"the script has {len(self._steps)} step(s)"
                    ),
                )
            )
        self._used += 1
        match self._steps[index]:
            case ToolCallStep(name=name, arguments=arguments):
                call_id = f"call_{index}"
                yield ModelToolCallStartedDelta(call_id=call_id, name=name)
                yield ModelToolCallArgumentsDelta(call_id=call_id, json=json.dumps(arguments))
                yield ModelCompletionFinished(finish_reason="tool_call", usage=CompletionUsage())
            case ReplyStep(text=text):
                yield ModelAssistantContentDelta(content=[TextContentBlock(text=text)])
                yield ModelCompletionFinished(finish_reason="stop", usage=CompletionUsage())

    def assert_consumed(self) -> None:
        """Fail if a step of the script was never used."""
        left = len(self._steps) - self._used
        if left:
            raise AssertionError(
                f"ScriptedModel used {self._used} of {len(self._steps)} step(s); {left} were never used"
            )


__all__ = ["ScriptedModel", "call", "reply"]
