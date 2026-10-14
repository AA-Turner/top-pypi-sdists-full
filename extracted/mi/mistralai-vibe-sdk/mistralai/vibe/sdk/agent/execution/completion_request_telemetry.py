"""Telemetry emitted at the completion request boundary."""

import uuid

from mistralai.vibe.sdk.agent.telemetry_events import EVENT_CONTEXT_KEYS, REQUEST_SENT_EVENT
from mistralai.vibe.sdk.observability import (
    RequestMetadata,
    attributes_from_context,
)
from mistralai.vibe.sdk.observability import datalake as datalake_telemetry
from mistralai.vibe.sdk.providers.completion.messages import Message
from mistralai.vibe.sdk.providers.completion.types import CompletionRequest, CompletionRequestKind

_COMPLETION_CORRELATION_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL,
    "mistralai.vibe.sdk.completion",
)


def completion_correlation_id(
    task_id: str, kind: CompletionRequestKind, history_length: int
) -> str:
    # Task history only grows, so its length orders the completions of one
    # task and is identical on replay and retry. The kind separates a
    # compaction from the agent call issued at the same history length.
    return str(
        uuid.uuid5(
            _COMPLETION_CORRELATION_NAMESPACE,
            f"{task_id}:{kind}:{history_length}",
        )
    )


async def emit_completion_request_sent(
    *,
    model: str,
    request: CompletionRequest,
) -> None:
    metadata = RequestMetadata(**(request.metadata or {}))
    context = attributes_from_context(*EVENT_CONTEXT_KEYS[REQUEST_SENT_EVENT])
    ambient_correlation_id = context.get("correlation_id")
    correlation_id = metadata.correlation_id
    if correlation_id is None and isinstance(ambient_correlation_id, str):
        correlation_id = ambient_correlation_id
    properties = metadata.model_dump(exclude_none=True) | {
        **context,
        "model": model,
        "nb_context_chars": sum(len(message.content or "") for message in request.messages),
        "nb_context_messages": len(request.messages),
        "nb_prompt_chars": _latest_user_prompt_chars(request.messages),
    }
    if correlation_id is not None:
        properties["correlation_id"] = correlation_id
    await datalake_telemetry.atrack(
        REQUEST_SENT_EVENT,
        properties=properties,
        correlation_id=correlation_id,
    )


def _latest_user_prompt_chars(messages: list[Message]) -> int:
    for message in reversed(messages):
        if message.role == "user":
            return len(message.content or "")
    return 0
