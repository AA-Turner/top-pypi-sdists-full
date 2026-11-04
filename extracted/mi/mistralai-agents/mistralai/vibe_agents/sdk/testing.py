"""Test an agent without a real model: a scripted model answers each model call in order."""

import json
import keyword
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

_RUN_TYPESCRIPT = "run_typescript"


def call(name: str, /, **arguments: JsonValue) -> ToolCallStep:
    """Script a model call that asks for the tool ``name``, the name the model sees, with ``arguments``.

    The model must be able to call ``name`` directly. A tool with the default ``model_access`` is
    called from ``run_typescript``: script it with :func:`run_typescript`.
    """
    return ToolCallStep(name=name, arguments=arguments)


def run_typescript(code: str) -> ToolCallStep:
    """Script a model call that runs ``code`` in ``run_typescript``.

    The program calls a tool as ``tools.<namespace>.<name>(...)``, as a real model would.
    """
    return ToolCallStep(name=_RUN_TYPESCRIPT, arguments={"code": code})


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
        """Stream the next step of the script.

        A tool call step fails the model call when the request does not offer its tool.
        """
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
        step = self._steps[index]
        if isinstance(step, ToolCallStep):
            _require_offered(step, index, request)
        self._used += 1
        match step:
            case ToolCallStep(name=name, arguments=arguments):
                # A tool call ID must be unique in the Session, also across a restore that
                # starts a new script, so it comes from the model call, not the step.
                call_id = f"call_{request.action_id}"
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


def _require_offered(step: ToolCallStep, index: int, request: CompletionRequest) -> None:
    """Fail the model call when the model cannot call the step's tool directly."""
    offered = sorted(tool.function.name for tool in request.tools)
    if step.name in offered:
        return
    message = (
        f"ScriptedModel step {index + 1} calls {step.name!r}, which the model cannot call directly; "
        f"its tool list has {', '.join(offered) or 'no tool'}."
    )
    namespace, _, name = step.name.rpartition(".")
    if namespace and name in offered:
        message += f" Script the step with the name in that list:\n{_call_line(name, step.arguments)}"
    elif _RUN_TYPESCRIPT in offered:
        code = f"return await tools.{namespace or 'client'}.{name}({json.dumps(step.arguments)});"
        message += (
            f" If {step.name!r} is a tool with the default model_access, the model calls it from "
            f"run_typescript; script the step as:\nagents.testing.run_typescript({code!r})"
        )
        if not namespace:
            message += "\nIf the tool has a namespace, write it in place of client."
    raise CompletionError(CompletionFailure(kind="provider", retryable=False, message=message))


def _call_line(name: str, arguments: dict[str, JsonValue]) -> str:
    """The ``agents.testing.call(...)`` line that scripts the tool ``name`` with ``arguments``."""
    if all(key.isidentifier() and not keyword.iskeyword(key) for key in arguments):
        listed = "".join(f", {key}={value!r}" for key, value in arguments.items())
    else:
        listed = f", **{arguments!r}"
    return f"agents.testing.call({name!r}{listed})"


__all__ = ["ScriptedModel", "call", "reply", "run_typescript"]
