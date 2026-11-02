from __future__ import annotations

import pytest

from matrx_connect.context.events import (
    EventType,
    PAYLOAD_REGISTRY,
    ProviderRetryPayload,
    build_event,
)
from matrx_connect.request_controls import RequestControlRegistry


def test_provider_retry_payload_is_registered_and_serializable() -> None:
    assert PAYLOAD_REGISTRY[EventType.PROVIDER_RETRY] is ProviderRetryPayload

    event = build_event(
        EventType.PROVIDER_RETRY,
        ProviderRetryPayload(
            state="scheduled",
            provider="anthropic",
            error_type="provider_overloaded",
            message="Anthropic is temporarily overloaded (529)",
            user_message="Anthropic is busy. We are waiting and retrying automatically.",
            status_code=529,
            model="claude-sonnet",
            request_id="request-1",
            iteration=1,
            failed_attempt=1,
            next_attempt=2,
            max_retries=5,
            retry_delay=2.0,
            retry_at=1002.0,
            discard_partial_output=True,
            schedule=[2.0, 5.0, 10.0, 30.0, 60.0],
            actions={
                "cancel": "/ai/cancel/request-1",
                "retry_now": "/ai/retry-now/request-1",
            },
        ),
    )

    assert event.event == EventType.PROVIDER_RETRY
    assert event.data["retry_delay"] == 2.0
    assert event.data["discard_partial_output"] is True
    assert event.data["actions"]["retry_now"] == "/ai/retry-now/request-1"


@pytest.mark.asyncio
async def test_request_control_retry_now_is_one_shot() -> None:
    registry = RequestControlRegistry(ttl_seconds=60)
    await registry.retry_now("request-1")

    assert await registry.consume_retry_now("request-1") is True
    assert await registry.consume_retry_now("request-1") is False

    await registry.cancel("request-1")
    assert registry.is_cancelled("request-1") is True
