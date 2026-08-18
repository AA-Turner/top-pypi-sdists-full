"""Telemetry emitted at the completion request boundary."""

from mistralai.vibe.sdk.agent.telemetry_events import EVENT_CONTEXT_KEYS, REQUEST_SENT_EVENT
from mistralai.vibe.sdk.observability import (
    RequestMetadata,
    attributes_from_context,
)
from mistralai.vibe.sdk.observability import datalake as datalake_telemetry
from mistralai.vibe.sdk.providers.completion.messages import Message
from mistralai.vibe.sdk.providers.completion.types import CompletionRequest


async def emit_completion_request_sent(
    *,
    model: str,
    request: CompletionRequest,
) -> None:
    metadata = RequestMetadata(**(request.metadata or {}))
    context = attributes_from_context(*EVENT_CONTEXT_KEYS[REQUEST_SENT_EVENT])
    ambient_correlation_id = context.get("correlation_id")
    correlation_id: str | None = (
        ambient_correlation_id
        if isinstance(ambient_correlation_id, str)
        else metadata.correlation_id
    )
    properties = metadata.model_dump(exclude_none=True) | {
        **context,
        "model": model,
        "nb_context_chars": sum(len(message.content or "") for message in request.messages),
        "nb_context_messages": len(request.messages),
        "nb_prompt_chars": _latest_user_prompt_chars(request.messages),
    }
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
