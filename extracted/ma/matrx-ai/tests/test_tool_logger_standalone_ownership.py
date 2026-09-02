from __future__ import annotations

from contextlib import asynccontextmanager
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.tools import logger as logger_module
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType


@pytest.mark.asyncio
async def test_out_of_request_started_insert_uses_standalone_coordinator(monkeypatch) -> None:
    queued: list[dict] = []
    reasons: list[str] = []

    @asynccontextmanager
    async def fake_standalone_coordinator(*, reason: str, **_kwargs):
        reasons.append(reason)
        yield object()

    async def fake_ensure(**_kwargs) -> None:
        return None

    monkeypatch.setattr(
        "matrx_ai.persistence.standalone_coordinator", fake_standalone_coordinator
    )
    monkeypatch.setattr(logger_module, "_ensure_tool_call_parents", fake_ensure)
    monkeypatch.setattr(logger_module, "_should_persist_tool_call", lambda: True)
    monkeypatch.setattr(logger_module, "_get_coordinator", lambda: None)
    monkeypatch.setattr(
        logger_module, "_queue_tool_call_create", lambda **data: queued.append(data)
    )
    monkeypatch.setattr(logger_module, "_cx_tool_call_supports_as_called", lambda: False)
    monkeypatch.setattr(logger_module, "stamp_row_owner", lambda data, _uid: data)
    monkeypatch.setattr(logger_module, "try_get_tracker", lambda: None)

    app_ctx = SimpleNamespace(
        user_id=str(uuid4()),
        conversation_id=str(uuid4()),
        request_id=str(uuid4()),
        store=True,
        metadata={},
        emitter=None,
    )
    monkeypatch.setattr(
        "matrx_ai.context.app_context.get_app_context", lambda: app_ctx
    )
    monkeypatch.setattr(
        "matrx_ai.context.app_context.try_get_app_context", lambda: app_ctx
    )

    tool_def = ToolDefinition(
        name="probe",
        description="forcing probe",
        parameters={"type": "object", "properties": {}},
        tool_type=ToolType.LOCAL,
    )
    ctx = ToolContext(call_id=f"call_{uuid4().hex[:12]}", tool_name="probe")

    row_id = await logger_module.ToolExecutionLogger().log_started(ctx, tool_def, {})

    assert row_id
    assert reasons == ["tool_ledger_insert_started"]
    assert len(queued) == 1


@pytest.mark.asyncio
async def test_out_of_request_update_uses_standalone_coordinator(monkeypatch) -> None:
    queued: list[tuple] = []
    reasons: list[str] = []

    class FakeCoordinator:
        def queue(self, *args, **kwargs) -> None:
            queued.append((args, kwargs))

    @asynccontextmanager
    async def fake_standalone_coordinator(*, reason: str, **_kwargs):
        reasons.append(reason)
        yield FakeCoordinator()

    monkeypatch.setattr(
        "matrx_ai.persistence.standalone_coordinator", fake_standalone_coordinator
    )
    monkeypatch.setattr(logger_module, "_get_coordinator", lambda: None)
    monkeypatch.setattr(logger_module, "get_conversation_store", None, raising=False)

    await logger_module.ToolExecutionLogger()._update_row(
        "tool-row-1", {"status": "completed"}
    )

    assert reasons == ["tool_ledger_update"]
    assert queued == [
        (
            ("chat.tool_call", {"id": "tool-row-1", "status": "completed"}),
            {"op_type": "update", "primary_key": ("id", "tool-row-1")},
        )
    ]


@pytest.mark.asyncio
async def test_out_of_request_update_failure_is_structured(monkeypatch) -> None:
    captured: list[tuple[BaseException, str, dict]] = []

    @asynccontextmanager
    async def failing_standalone_coordinator(*, reason: str, **_kwargs):
        assert reason == "tool_ledger_update"
        raise RuntimeError("forced standalone finalize failure")
        yield

    async def fake_capture(exc: BaseException, operation: str, **payload) -> None:
        captured.append((exc, operation, payload))

    monkeypatch.setattr(
        "matrx_ai.persistence.standalone_coordinator", failing_standalone_coordinator
    )
    monkeypatch.setattr(logger_module, "_get_coordinator", lambda: None)
    monkeypatch.setattr(logger_module, "_capture_tool_ledger_failure", fake_capture)

    await logger_module.ToolExecutionLogger()._update_row(
        "tool-row-2", {"status": "error", "error_type": "forced"}
    )

    assert len(captured) == 1
    exc, operation, payload = captured[0]
    assert isinstance(exc, RuntimeError)
    assert operation == "update_tool_call"
    assert payload == {
        "row_id": "tool-row-2",
        "data_keys": ["error_type", "status"],
    }
