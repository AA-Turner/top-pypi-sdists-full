"""Bridge between execution record state and completion types.

Converts TaskState history into CompletionRequest messages (for the LLM),
and converts streaming CompletionChunk responses back into TaskState mutations
(for the reducer/dispatch loop).

The flow:
  reducer → completion effect → build_completion_request_from_state()
  → CompletionModel.complete() → stream_to_mutations() → patches → reducer
"""

import json
import uuid
from collections.abc import AsyncIterator, Callable
from typing import Any, Literal

from mistralai.vibe.sdk.execution_record.patching.produce import produce
from mistralai.vibe.sdk.execution_record.projections.completion_request import (
    build_completion_request_from_state as _build_completion_request_from_state,
)
from mistralai.vibe.sdk.execution_record.projections.completion_request import (
    tool_call_provider_id as _tool_call_provider_id,
)
from mistralai.vibe.sdk.execution_record.state import (
    CompletedOutput,
    JsonValue,
    MessageEntry,
    MessageEntryPayload,
    TaskCallEntry,
    TaskCallEntryPayload,
    TaskState,
    TextContentBlock,
    ThinkingContentBlock,
)
from mistralai.vibe.sdk.providers.completion.types import (
    CompletionChunk,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

# Type alias for produce() output
_MutationResult = tuple[TaskState, list[Any], list[TaskCallEntry] | None, TokenUsage | None]
_PROVIDER_ID_PREFIX = "llm:"
build_completion_request_from_state = _build_completion_request_from_state
tool_call_provider_id = _tool_call_provider_id

__all__ = [
    "build_completion_request_from_state",
    "encode_tool_call_id",
    "stream_states",
    "tool_call_provider_id",
]


def encode_tool_call_id(provider_id: str | None) -> str:
    """Encode a provider-local tool-call id into the protocol id field."""
    sdk_id = uuid.uuid4().hex
    if not provider_id:
        return sdk_id
    provider_blob = json.dumps(provider_id)
    return f"{_PROVIDER_ID_PREFIX}{provider_blob}:{sdk_id}"


def _make_delta_recipe(
    *,
    thinking_delta: str | None,
    content_delta: str | None,
    thinking_index: int | None,
    message_index: int | None,
) -> Callable[[Any], None]:
    def apply_delta_recipe(draft: Any) -> None:
        _apply_assistant_delta(
            draft,
            delta=thinking_delta,
            entry_index=thinking_index,
            channel="thinking",
            block_type="thinking",
        )
        _apply_assistant_delta(
            draft,
            delta=content_delta,
            entry_index=message_index,
            channel="message",
            block_type="text",
        )

    return apply_delta_recipe


def _apply_assistant_delta(
    draft: Any,
    *,
    delta: str | None,
    entry_index: int | None,
    channel: Literal["thinking", "message"],
    block_type: str,
) -> None:
    if not delta:
        return

    content_block = (
        ThinkingContentBlock(thinking=delta)
        if block_type == "thinking"
        else TextContentBlock(text=delta)
    )

    if entry_index is None:
        draft.history.append(
            MessageEntry(
                payload=MessageEntryPayload(
                    role="assistant",
                    content=[content_block],
                    channel=channel,
                ),
                generation_status="generating",
            ),
        )
        return

    content = draft.history[entry_index].payload.content
    if content and content[-1].type == block_type:
        setattr(content[-1], block_type, getattr(content[-1], block_type) + delta)
    else:
        content.append(content_block)


# ---------------------------------------------------------------------------
# stream_to_mutations — streaming LLM bridge
# ---------------------------------------------------------------------------


async def stream_to_mutations(
    state: TaskState,
    chunks: AsyncIterator[CompletionChunk],
) -> AsyncIterator[_MutationResult]:
    """Yields ``(new_state, patches, tool_calls, usage)`` for each meaningful chunk.

    Uses produce() for recording — AppendOp emitted for content growth.

    Manages the lifecycle of a single LLM turn:
    1. Thinking deltas stream into an assistant entry with channel="thinking"
    2. Text deltas stream into an assistant entry with channel="message"
    3. Tool call deltas accumulate id/name/arguments across chunks
    4. Finalization marks any streamed entries complete and surfaces tool calls

    Args:
        state: Current TaskState before this LLM turn.
        chunks: Async iterator of CompletionChunk from the LLM backend.

    Yields:
        ``(new_state, patches, tool_calls, usage)`` tuples — one per meaningful
        chunk (text delta, finalization, or a trailing usage-only chunk). Tool
        call deltas are accumulated silently and surfaced only on the finalization
        yield; ``usage`` carries the latest reported token usage seen so far.
    """
    current_state = state
    tool_call_accumulators: dict[int, dict[str, str]] = {}
    thinking_entry_index: int | None = None
    message_entry_index: int | None = None
    latest_usage: TokenUsage | None = None

    async for chunk in chunks:
        if chunk.usage is not None:
            latest_usage = chunk.usage

        if chunk.thinking_delta or chunk.content_delta:
            history_len = len(current_state.history)
            creates_thinking_entry = bool(chunk.thinking_delta) and thinking_entry_index is None
            creates_message_entry = bool(chunk.content_delta) and message_entry_index is None

            new_state, patches = produce(
                current_state,
                _make_delta_recipe(
                    thinking_delta=chunk.thinking_delta,
                    content_delta=chunk.content_delta,
                    thinking_index=thinking_entry_index,
                    message_index=message_entry_index,
                ),
            )
            if creates_thinking_entry:
                thinking_entry_index = history_len
                history_len += 1
            if creates_message_entry:
                message_entry_index = history_len

            current_state = new_state
            yield (new_state, patches, None, latest_usage)

        # Handle tool call deltas (accumulate, no yield)
        if chunk.tool_call_deltas:
            for tc_delta in chunk.tool_call_deltas:
                acc = tool_call_accumulators.setdefault(
                    tc_delta.index, {"id": "", "name": "", "arguments": ""}
                )
                if tc_delta.id:
                    acc["id"] = tc_delta.id
                if tc_delta.function_name:
                    acc["name"] = tc_delta.function_name
                if tc_delta.arguments_delta:
                    acc["arguments"] += tc_delta.arguments_delta

        # Handle finalization
        if chunk.finish_reason:
            # Build tool calls list
            tool_calls_list: list[TaskCallEntry] = []
            if tool_call_accumulators:
                for _idx, acc in sorted(tool_call_accumulators.items()):
                    parsed_args: JsonValue
                    try:
                        parsed_args = json.loads(acc["arguments"]) if acc["arguments"] else {}
                    except json.JSONDecodeError:
                        parsed_args = {"raw_arguments": acc["arguments"]}
                    tc = TaskCallEntry(
                        payload=TaskCallEntryPayload(
                            id=encode_tool_call_id(acc["id"]),
                            name=acc["name"],
                            input=parsed_args,
                        ),
                    )
                    tool_calls_list.append(tc)

            tcs = tool_calls_list

            def finalize_recipe(
                draft: Any,
                *,
                _tcs: list[TaskCallEntry] = tcs,
                _thinking_index: int | None = thinking_entry_index,
                _message_index: int | None = message_entry_index,
            ) -> None:
                needs_empty_message_entry = _message_index is None and (
                    _thinking_index is None or bool(_tcs)
                )
                if needs_empty_message_entry:
                    draft.history.append(
                        MessageEntry(
                            payload=MessageEntryPayload(
                                role="assistant",
                                content=[],
                            ),
                            generation_status="complete",
                        )
                    )

                if _thinking_index is not None:
                    draft.history[_thinking_index].generation_status = "complete"
                if _message_index is not None:
                    draft.history[_message_index].generation_status = "complete"

                if not _tcs:
                    # No tool calls: task completes with the response text
                    content = (
                        "".join(
                            block.text
                            for block in draft.history[_message_index].payload.content
                            if isinstance(block, TextContentBlock)
                        )
                        if _message_index is not None
                        else ""
                    )
                    draft.output = CompletedOutput(value={"response": content})

            new_state, patches = produce(current_state, finalize_recipe)
            current_state = new_state
            yield (new_state, patches, tcs, latest_usage)
            continue

        # Usage only chunk e.g. trailing usage that providers emit after finish_reason.
        if chunk.usage is not None and not (chunk.thinking_delta or chunk.content_delta):
            yield (current_state, [], None, latest_usage)


# ---------------------------------------------------------------------------
# stream_states — state-only iterator (no patch computation)
# ---------------------------------------------------------------------------


async def stream_states(
    state: TaskState,
    chunks: AsyncIterator[CompletionChunk],
) -> AsyncIterator[tuple[TaskState, list[TaskCallEntry] | None, TokenUsage | None]]:
    """Yield ``(TaskState, tool_calls, usage)`` while discarding low-level patches.

    Wraps stream_to_mutations but discards the patch output, avoiding
    redundant diff computation when the caller only needs the state (e.g.,
    the workflow execution path where patches are handled by the Workflows
    API task() CM instead of the local in-process queue).

    Args:
        state: Current TaskState before this LLM turn.
        chunks: Async iterator of CompletionChunk from the LLM backend.

    Yields:
        ``(TaskState, tool_calls, usage)`` after each meaningful chunk is
        applied.
    """
    async for new_state, _, tool_calls, usage in stream_to_mutations(state, chunks):
        yield (new_state, tool_calls, usage)
