import functools
import json
from typing import Any, Literal, TypeVar, get_args, override

from pydantic import BaseModel, Field, ValidationError
from pydantic_core.core_schema import ErrorType

from mistralai.vibe.harness.app_server.session import TextContentBlock
from mistralai.vibe.harness.runtime.capabilities import (
    PostLlmCallHookAccept,
    PostLlmCallHookReject,
    PostLlmCallHookRetry,
    PreAgentTurnHookContinue,
    PreLlmCallHookContinue,
)
from mistralai.vibe_agents.sdk.authoring.contracts import Hook, HookCallbackContext
from mistralai.vibe_agents.sdk.authoring.hooks import PostLlmCall, PreAgentTurn, PreLlmCall

__all__ = ["StructuredOutputHook"]

# Pydantic's own error types, except the two that wrap an error raised by a validator.
_SCHEMA_ERROR_TYPES = frozenset(get_args(ErrorType)) - {"value_error", "assertion_error"}

# The longest part of the last answer that the turn's error repeats.
_LAST_ANSWER_LIMIT = 1000


class _TurnCount(BaseModel):
    """The model calls and corrections of one turn."""

    turn_id: str
    model_calls: int = 0
    retries: int = 0


class StructuredOutputHook[T: BaseModel](Hook):
    """Validate the final answer of each turn with a Pydantic model, and ask the model to correct it.

    Name the model in brackets, as in ``StructuredOutputHook[City](max_retries=2)``, or subclass
    ``StructuredOutputHook[City]`` and set new defaults for its fields.

    The hook asks for a correction only while ``max_retries`` allows it and the turn has an
    iteration left under the agent's ``max_iterations``. At that limit it accepts the last answer,
    or, when ``on_limit`` is ``"reject"``, raises ``ValueError``, which fails the turn. Set
    ``schema_in_prompt`` to ``False`` to leave the JSON Schema out of the user message, for example
    when ``output_type`` already gives it to the model; corrections still include it. Set
    ``enabled`` to ``False`` to let answers through unchecked. ``turn`` holds the count of the
    current turn; the Session saves it with the other fields.

    The Hook counts each model call before it is made, so a call that a guardrail or an earlier
    Hook retries still counts toward ``max_iterations``.
    """

    max_retries: int = Field(default=2, ge=0)
    on_limit: Literal["accept", "reject"] = "accept"
    schema_in_prompt: bool = True
    enabled: bool = True
    turn: _TurnCount | None = None

    @override
    def model_post_init(self, context: Any, /) -> None:
        super().model_post_init(context)
        type(self)._output_type()

    @classmethod
    def _output_type(cls) -> type[BaseModel]:
        # Follow each type parameter to the argument it was given, so ``MyHook[Config]`` with
        # ``class MyHook[C](StructuredOutputHook[City])`` still validates against ``City``.
        bound: dict[object, object] = {}
        for base in cls.__mro__:
            metadata = getattr(base, "__pydantic_generic_metadata__", None)
            if metadata is None or metadata["origin"] is None:
                continue
            origin = metadata["origin"]
            args = [bound.get(arg, arg) if isinstance(arg, TypeVar) else arg for arg in metadata["args"]]
            if origin is StructuredOutputHook:
                [output] = args
                if isinstance(output, type) and issubclass(output, BaseModel):
                    return output
                break
            bound.update(zip(origin.__pydantic_generic_metadata__["parameters"], args, strict=False))
        raise TypeError(
            f"{cls.__qualname__} has no output model: name it in brackets, as in StructuredOutputHook[YourModel]"
        )

    @override
    async def pre_agent_turn(
        self,
        ctx: HookCallbackContext,
        request: PreAgentTurn,
    ) -> PreAgentTurnHookContinue:
        if not self.enabled or not self.schema_in_prompt:
            return PreAgentTurnHookContinue(user_content=request.user_content)
        instruction = (
            "Return the final answer as one JSON object that matches the JSON Schema below. "
            "Do not wrap the JSON in Markdown.\n\n"
            f"JSON Schema:\n{_schema_text(type(self)._output_type())}"
        )
        return PreAgentTurnHookContinue(user_content=[*request.user_content, TextContentBlock(text=instruction)])

    @override
    async def pre_llm_call(self, ctx: HookCallbackContext, invocation: PreLlmCall) -> PreLlmCallHookContinue:
        # Counted here, where every model call passes, so a call whose answer a guardrail or an
        # earlier Hook retries, and that post_llm_call never sees, still counts.
        if self.enabled:
            self._turn_count(invocation.turn_id).model_calls += 1
        return PreLlmCallHookContinue()

    @override
    async def post_llm_call(
        self,
        ctx: HookCallbackContext,
        invocation: PostLlmCall,
    ) -> PostLlmCallHookAccept | PostLlmCallHookRetry | PostLlmCallHookReject:
        if not self.enabled:
            return PostLlmCallHookAccept()
        # pre_llm_call of the same model call has counted it.
        count = self._turn_count(invocation.turn_id)
        if invocation.tool_calls:
            return PostLlmCallHookAccept()

        output_type = type(self)._output_type()
        text = invocation.text
        try:
            output_type.model_validate_json(text)
        except ValidationError as error:
            # The Harness fails the turn when a retry would need more model calls than max_iterations.
            max_iterations = ctx._max_iterations
            if count.retries < self.max_retries and (max_iterations is None or count.model_calls < max_iterations):
                count.retries += 1
                feedback = (
                    f"Your previous answer {_failed_check(text, error)}. Return only a corrected JSON object.\n\n"
                    f"Validation error:\n{error}\n\n"
                    f"JSON Schema:\n{_schema_text(output_type)}\n\n"
                    f"Previous answer:\n{text}"
                )
                return PostLlmCallHookRetry(feedback=[TextContentBlock(text=feedback)])
            if self.on_limit == "reject":
                # The Harness fails the turn with this message, and every client sees it.
                corrections = f"{count.retries} correction{'' if count.retries == 1 else 's'}"
                last_answer = text if len(text) <= _LAST_ANSWER_LIMIT else f"{text[:_LAST_ANSWER_LIMIT]}..."
                raise ValueError(
                    f"The final answer {_failed_check(text, error)} after {corrections}. "
                    f"Output model: {output_type.__name__}.\n\n"
                    f"Validation error:\n{error}\n\n"
                    f"Last answer:\n{last_answer}"
                ) from error
        return PostLlmCallHookAccept()

    def _turn_count(self, turn_id: str) -> _TurnCount:
        if self.turn is None or self.turn.turn_id != turn_id:
            self.turn = _TurnCount(turn_id=turn_id)
        return self.turn


@functools.lru_cache(maxsize=32)
def _schema_text(model: type[BaseModel]) -> str:
    return json.dumps(model.model_json_schema(), indent=2)


def _failed_check(text: str, error: ValidationError) -> str:
    if any(detail["type"] == "json_invalid" and not detail["loc"] for detail in error.errors()):
        return "is not valid JSON"
    if any(detail["type"] in _SCHEMA_ERROR_TYPES for detail in error.errors()):
        return "does not match the required JSON Schema"
    return "does not pass a validator of the output model"
