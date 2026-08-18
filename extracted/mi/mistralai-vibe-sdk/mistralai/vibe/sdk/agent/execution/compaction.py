"""Reusable conversation compaction helper.

Owns the compaction primitives: deciding what history is compactable, inserting the
running ``agent.compaction`` entry (``begin_compaction``), and running the summary
call to finalize it as completed/failed (``run_compaction``).
"""

from typing import Any, Literal

from pydantic import BaseModel

from mistralai.vibe.sdk.agent.execution.completion_request_telemetry import (
    emit_completion_request_sent,
)
from mistralai.vibe.sdk.execution_record.snapshots import make_snapshot_entry
from mistralai.vibe.sdk.execution_record.state import (
    MessageEntry,
    MessageEntryPayload,
    StateEntry,
    TaskState,
    content_blocks,
    content_text,
)
from mistralai.vibe.sdk.observability import RequestMetadata, observability_context
from mistralai.vibe.sdk.providers.completion.bridge import (
    build_completion_request_from_state,
    stream_states,
)
from mistralai.vibe.sdk.providers.completion.errors import (
    CompletionContextTooLargeError,
    is_context_too_large_error,
)
from mistralai.vibe.sdk.providers.completion.port import CompletionModel
from mistralai.vibe.sdk.providers.completion.tokens import (
    estimate_context_tokens,
    latest_compaction_sentinel_index,
)
from mistralai.vibe.sdk.providers.completion.types import (
    AGENT_COMPACTION_SENTINEL_TYPE,
    COMPACTION_ANNOTATION,
    COMPLETION_REQUEST_KIND_COMPACTION,
    AgentCompactionSentinelContent,
    CompactionAnnotation,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage

__all__ = [
    "COMPACTION_STREAM_NAME",
    "DEFAULT_COMPACTION_PROMPT",
    "compact_conversation",
]

COMPACTION_STREAM_NAME = "compaction"

DEFAULT_COMPACTION_PROMPT = """\
Create a comprehensive summary of our entire conversation that will serve
as complete context for continuing this work. Structure your summary to capture both the narrative
flow and technical details necessary for seamless continuation.

Your summary must include these sections in order:

## 1. User's Primary Goals and Intent
Capture ALL explicit requests and objectives stated by the user throughout the conversation,
preserving their exact priorities and constraints.

## 2. Conversation Timeline and Progress
Chronologically document the key phases of our work:
- Initial requests and how they were addressed
- Major decisions made and their rationale
- Problems encountered and solutions applied
- Current state of the work

## 3. Technical Context and Decisions
- Technologies, frameworks, and tools being used
- Architectural patterns and design decisions made
- Key technical constraints or requirements identified
- Important code patterns or conventions established

## 4. Files and Code Changes
For each file created, modified, or examined:
- Full file path/name
- Purpose and importance of the file
- Specific changes made (with key code snippets where critical)
- Current state of the file

## 5. Active Work and Last Actions
CRITICAL: Detail EXACTLY what was being worked on in the most recent exchanges:
- The specific task or problem being addressed
- Last completed action
- Any partial work or mid-implementation state
- Include relevant code snippets from the most recent work

## 6. Unresolved Issues and Pending Tasks
- Any errors or issues still requiring attention
- Tasks explicitly requested but not yet started
- Decisions waiting for user input

## 7. Immediate Next Step
State the SPECIFIC next action to take based on:
- The user's most recent request
- The current state of implementation
- Any ongoing work that was interrupted

Important: Be precise with technical details, file names, and code. The next agent reading this
should be able to continue exactly where we left off without asking clarifying questions.
Include enough detail that no context is lost, but remain focused on actionable information.

Respond with ONLY the summary text following this structure - no additional commentary or
meta-discussion."""


class CompactionResult(BaseModel):
    """Outcome of a compaction summary call."""

    summary: str
    usage: TokenUsage | None = None


async def compact_conversation(
    completion: CompletionModel,
    state: TaskState,
    prompt: str | None = None,
    *,
    request_metadata: dict[str, Any] | None = None,
) -> CompactionResult:
    """Return a compact summary of the history plus the summary call's usage."""
    prompt_text = (prompt or "").strip() or DEFAULT_COMPACTION_PROMPT
    prompt_entry = MessageEntry(
        payload=MessageEntryPayload(
            role="user",
            content=content_blocks(prompt_text),
        )
    )
    request_state = state.model_copy(update={"history": [*state.history, prompt_entry]})
    if request_metadata is None:
        # Direct calls build from ambient context; effects pass serialized request metadata.
        with observability_context(call_type="secondary_call", message_id=state.id):
            request_metadata = RequestMetadata.build_from_context()
    request = build_completion_request_from_state(
        request_state,
        {},
        metadata=request_metadata,
        request_kind=COMPLETION_REQUEST_KIND_COMPACTION,
    )
    await emit_completion_request_sent(model=completion.model, request=request)
    current_state = request_state
    latest_usage: TokenUsage | None = None

    async for new_state, _tool_calls, usage in stream_states(
        request_state, completion.complete(request)
    ):
        current_state = new_state
        if usage is not None:
            latest_usage = usage

    summary = ""
    for entry in reversed(current_state.history):
        if isinstance(entry, MessageEntry) and entry.payload.role == "assistant":
            summary = content_text(entry.payload.content)
            break

    return CompactionResult(summary=summary, usage=latest_usage)


def _latest_user_message_index(state: TaskState) -> int | None:
    for index in range(len(state.history) - 1, -1, -1):
        entry = state.history[index]
        if isinstance(entry, MessageEntry) and entry.payload.role == "user":
            return index
    return None


def has_compactable_history(state: TaskState) -> bool:
    """True when there is non-system history before the latest user message."""
    suffix_start_index = _latest_user_message_index(state)
    if suffix_start_index is None:
        return False

    for index in range(suffix_start_index):
        entry = state.history[index]
        if not (isinstance(entry, MessageEntry) and entry.payload.role == "system"):
            return True
    return False


def make_compaction_entry(
    status: Literal["running", "completed", "failed"],
    *,
    threshold: int,
    old_context_tokens: int,
    summary: str = "",
    error: str | None = None,
    new_context_tokens: int | None = None,
    result: CompactionResult | None = None,
) -> StateEntry:
    """Build an ``agent.compaction`` entry for one lifecycle beat (running/completed/failed)."""
    usage = result.usage if result is not None else None
    annotation = CompactionAnnotation(
        status=status,
        threshold=threshold,
        old_context_tokens=old_context_tokens,
        new_context_tokens=new_context_tokens,
        summary_length=len(summary) if result is not None else None,
        input_tokens=usage.input_tokens if usage is not None else None,
        output_tokens=usage.output_tokens if usage is not None else None,
        error=error,
    )

    return make_snapshot_entry(
        AGENT_COMPACTION_SENTINEL_TYPE,
        AgentCompactionSentinelContent(summary=summary).model_dump(),
        generation_status="generating" if status == "running" else "complete",
        annotations={COMPACTION_ANNOTATION: annotation.model_dump(exclude_none=True)},
    )


class CompactionOutcome(BaseModel):
    """Result of the compaction summary call."""

    entry: StateEntry
    error: str | None = None


async def run_compaction(
    completion: CompletionModel,
    state: TaskState,
    *,
    tools: dict[str, Any],
    threshold: int,
    compaction_prompt: str | None,
    provider: str,
    model: str,
    request_metadata: dict[str, Any] | None = None,
) -> CompactionOutcome:
    """Summarize the conversation and return the finalized outcome (completed/failed)."""
    anchor = latest_compaction_sentinel_index(state)
    head, tail = state.history[:anchor], state.history[anchor + 1 :]
    original = state.model_copy(update={"history": [*head, *tail]})
    old_context_tokens = estimate_context_tokens(original, tools)

    def state_with(sentinel: StateEntry) -> TaskState:
        return state.model_copy(update={"history": [*head, sentinel, *tail]})

    try:
        result = await compact_conversation(
            completion,
            original,
            compaction_prompt,
            request_metadata=request_metadata,
        )
    except Exception as exc:
        if not (isinstance(exc, CompletionContextTooLargeError) or is_context_too_large_error(exc)):
            raise
        error = f"{provider} compaction request exceeded the context limit for model {model}"
        failed = make_compaction_entry(
            "failed",
            threshold=threshold,
            old_context_tokens=old_context_tokens,
            error=error,
        )
        return CompactionOutcome(entry=failed, error=error)

    # Estimate the post-compaction context using an entry without its own token count.
    new_context_tokens = estimate_context_tokens(
        state_with(
            make_compaction_entry(
                "completed",
                threshold=threshold,
                old_context_tokens=old_context_tokens,
                summary=result.summary,
                result=result,
            )
        ),
        tools,
        prefer_reported_usage=False,
    )
    completed = make_compaction_entry(
        "completed",
        threshold=threshold,
        old_context_tokens=old_context_tokens,
        summary=result.summary,
        new_context_tokens=new_context_tokens,
        result=result,
    )
    return CompactionOutcome(entry=completed)
