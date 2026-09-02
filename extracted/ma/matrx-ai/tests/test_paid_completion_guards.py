from __future__ import annotations

import asyncio
import time
from typing import Any

import pytest

from matrx_ai.config import TokenUsage, UnifiedResponse
from matrx_ai.providers.base_media import BaseMediaGeneration, GeneratedAsset
from matrx_ai.providers.errors import get_billed_usage, get_completed_response
from matrx_ai.tools.agent_tool import register_agent_as_tool
from matrx_ai.tools.executor import _await_must_complete
from matrx_ai.tools.models import ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.streaming import ToolStreamManager


def _success_result() -> ToolResult:
    now = time.time()
    return ToolResult(
        success=True,
        output={"status": "finished"},
        started_at=now,
        completed_at=now,
        tool_name="paid_child",
        call_id="call-paid",
    )


async def test_must_complete_timeout_is_soft_and_returns_real_result() -> None:
    finished = asyncio.Event()

    async def paid_child() -> ToolResult:
        await asyncio.sleep(0.04)
        finished.set()
        return _success_result()

    result, cancellation = await _await_must_complete(
        paid_child(),
        timeout_seconds=0.01,
        stream=ToolStreamManager(None, "call-paid", "paid_child"),
        tool_name="paid_child",
    )

    assert finished.is_set()
    assert result.success is True
    assert cancellation is None


async def test_must_complete_defers_parent_cancellation_until_child_finishes() -> None:
    started = asyncio.Event()
    finished = asyncio.Event()

    async def paid_child() -> ToolResult:
        started.set()
        await asyncio.sleep(0.04)
        finished.set()
        return _success_result()

    waiter = asyncio.create_task(
        _await_must_complete(
            paid_child(),
            timeout_seconds=10,
            stream=ToolStreamManager(None, "call-paid", "paid_child"),
            tool_name="paid_child",
        )
    )
    await started.wait()
    waiter.cancel()

    result, cancellation = await waiter

    assert finished.is_set()
    assert result.success is True
    assert isinstance(cancellation, asyncio.CancelledError)


def test_registry_reads_must_complete_from_tool_annotations() -> None:
    definition = ToolRegistry._row_to_definition(
        {
            "id": "tool-paid",
            "name": "paid_child",
            "description": "Runs paid work",
            "parameters": {},
            "annotations": [{"must_complete": True}],
            "source_kind": "native",
        }
    )

    assert definition.must_complete is True


async def test_projected_agent_tools_are_must_complete() -> None:
    definition = await register_agent_as_tool(
        prompt_id="agent-paid",
        tool_name="paid_agent",
        description="Runs a paid child agent",
    )

    assert definition.must_complete is True


def test_every_agent_tool_is_must_complete_by_construction() -> None:
    definition = ToolDefinition(
        name="paid_agent",
        description="Runs a paid child agent",
        parameters={},
        tool_type=ToolType.AGENT,
    )

    assert definition.must_complete is True


class _PaidMediaStub(BaseMediaGeneration):
    provider = "test-provider"
    modality = "image"

    def _build_kwargs(self, unified_config: Any, profile: Any) -> dict[str, Any]:
        return {}

    def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        return None

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        return []

    def _classify_error(self, exc: Exception) -> Any:
        return None

    def _telemetry_url(self, unified_config: Any, kwargs: dict[str, Any]) -> str:
        return ""


async def test_post_provider_persist_failure_is_not_retryable() -> None:
    """After the paid provider call returns, local failures must not retry."""
    from matrx_ai.providers.base_media import _non_retryable_after_paid_call
    from matrx_ai.providers.errors import RetryableError

    false_rate_limit = RetryableError(
        error_type="rate_limit",
        message="banner with 2026-08-04 10:31:17.542904+00",
        status_code=429,
        is_retryable=True,
        retry_after=10.0,
        user_message="Rate limited",
    )
    result = _non_retryable_after_paid_call(
        false_rate_limit,
        RuntimeError("persist failed"),
        provider="replicate",
        modality="video",
    )
    assert result.is_retryable is False
    assert result.error_type == "post_provider_failure"
    assert result.details["suppressed_retry"] is True


async def test_media_funnel_finishes_and_attaches_usage_before_cancelling() -> None:
    started = asyncio.Event()
    finished = asyncio.Event()
    usage = TokenUsage(
        input_tokens=10,
        output_tokens=20,
        matrx_model_name="paid-image",
        api="test-provider",
    )

    async def paid_media() -> UnifiedResponse:
        started.set()
        await asyncio.sleep(0.04)
        finished.set()
        return UnifiedResponse(messages=[], usage=usage)

    task = asyncio.create_task(_PaidMediaStub()._await_paid_completion(paid_media()))
    await started.wait()
    task.cancel()

    with pytest.raises(asyncio.CancelledError) as captured:
        await task

    assert finished.is_set()
    assert get_billed_usage(captured.value) is usage
    assert get_completed_response(captured.value).usage is usage
