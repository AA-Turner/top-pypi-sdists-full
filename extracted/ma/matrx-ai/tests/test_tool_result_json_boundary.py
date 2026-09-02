from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.streaming import ToolStreamManager


def _output() -> dict[str, object]:
    return {
        "created_at": datetime(2026, 7, 25, 12, 30, tzinfo=UTC),
        "id": UUID("c9894a96-4f73-45df-bf90-f7138c51f926"),
        "cost": Decimal("1.25"),
    }


def test_tool_result_content_normalizes_json_native_values() -> None:
    result = ToolResult(
        success=True,
        output=_output(),
        tool_name="sql",
        call_id="call-1",
    )

    content = json.loads(result.to_tool_result_content()["content"])

    assert content == {
        "created_at": "2026-07-25T12:30:00Z",
        "id": "c9894a96-4f73-45df-bf90-f7138c51f926",
        "cost": "1.25",
    }


@pytest.mark.asyncio
async def test_completed_stream_normalizes_json_native_values() -> None:
    result = ToolResult(
        success=True,
        output={"rows": [_output()]},
        tool_name="sql",
        call_id="call-2",
    )
    stream = ToolStreamManager(None, "call-2", "sql")

    await stream.completed(result=result)

    assert stream.get_events_for_persistence()[0]["data"]["result"]["rows"][0] == {
        "created_at": "2026-07-25T12:30:00Z",
        "id": "c9894a96-4f73-45df-bf90-f7138c51f926",
        "cost": "1.25",
    }


class _Logger:
    def __init__(self) -> None:
        self.errors: list[tuple[str, ToolResult, list[dict[str, object]]]] = []

    def prepare_metadata(self, result: ToolResult) -> None:
        result.output_chars = 0

    def row_id_for_call(self, ctx: ToolContext) -> str:
        return "running-row-id"

    async def log_error(
        self,
        row_id: str,
        result: ToolResult,
        events: list[dict[str, object]],
        *,
        coordinator: object,
    ) -> None:
        self.errors.append((row_id, result, events))


@pytest.mark.asyncio
async def test_batch_terminalizes_started_row_after_unhandled_exception(monkeypatch) -> None:
    from matrx_ai.tools.executor import ToolExecutor

    logger = _Logger()
    executor = ToolExecutor(registry=object(), execution_logger=logger)

    async def explode(*args: object, **kwargs: object) -> object:
        raise RuntimeError("completion boundary exploded")

    async def persist(coro: object, **kwargs: object) -> None:
        await coro

    monkeypatch.setattr(executor, "execute", explode)
    monkeypatch.setattr(executor, "_persist_tool_outcome", persist)

    content, results = await executor.execute_batch(
        [{"name": "sql", "arguments": {}, "call_id": "call-3"}],
        ToolContext(call_id="parent"),
    )

    assert content[0]["is_error"] is True
    assert results[0].error == ToolError(
        error_type="unhandled",
        message="completion boundary exploded",
        traceback=results[0].error.traceback,
    )
    assert "RuntimeError: completion boundary exploded" in (results[0].error.traceback or "")
    assert logger.errors[0][0] == "running-row-id"
    assert logger.errors[0][1].success is False
