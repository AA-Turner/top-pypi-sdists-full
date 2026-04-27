from __future__ import annotations

import asyncio
import logging

import pytest

from anteroom.services.debug_diagnostics import DebugDiagnosticsCollector
from anteroom.services.diagnostic_context import (
    clear_diagnostic_context,
    current_fields,
    log_debug,
    redact_value,
    reset_diagnostic_context,
    set_diagnostic_context,
    shape_metadata,
)
from anteroom.tools import ToolRegistry


def test_context_sets_and_resets_fields() -> None:
    token = set_diagnostic_context(
        interface="cli",
        conversation_id="conv-1",
        turn_id="turn-1",
        request_id="req-1",
    )
    try:
        assert current_fields(phase="turn") == {
            "interface": "cli",
            "conversation_id": "conv-1",
            "turn_id": "turn-1",
            "request_id": "req-1",
            "phase": "turn",
        }
    finally:
        reset_diagnostic_context(token)

    assert current_fields() == {}


@pytest.mark.asyncio
async def test_contextvars_are_task_local() -> None:
    async def worker(turn_id: str) -> str:
        token = set_diagnostic_context(turn_id=turn_id)
        try:
            await asyncio.sleep(0)
            return str(current_fields()["turn_id"])
        finally:
            reset_diagnostic_context(token)

    clear_token = clear_diagnostic_context()
    try:
        assert await asyncio.gather(worker("turn-a"), worker("turn-b")) == ["turn-a", "turn-b"]
        assert current_fields() == {}
    finally:
        reset_diagnostic_context(clear_token)


def test_redaction_and_shape_metadata_omit_values() -> None:
    assert redact_value("api_key=sk-secretsecretsecret") == "[redacted]"
    assert redact_value("value", key="password") == "[redacted]"
    shape = shape_metadata({"prompt": "raw text", "token": "secret", "count": 1})
    assert shape == {"type": "object", "keys": ["count", "prompt", "token"], "key_count": 3}
    assert "raw text" not in str(shape)
    assert "secret" not in str(shape)


def test_log_debug_is_lazy_when_debug_disabled() -> None:
    logger = logging.getLogger("anteroom.tests.diagnostic_context.lazy")
    logger.setLevel(logging.INFO)
    called = False

    def expensive() -> dict[str, object]:
        nonlocal called
        called = True
        return {"type": "object"}

    try:
        emitted = log_debug(logger, "test.lazy", lifecycle="start", payload_shape=expensive)
        assert emitted is False
        assert called is False
    finally:
        logger.setLevel(logging.NOTSET)


def test_log_debug_emits_correlation_fields(caplog: pytest.LogCaptureFixture) -> None:
    logger = logging.getLogger("anteroom.tests.diagnostic_context.emit")
    token = set_diagnostic_context(interface="web", conversation_id="conv-1", turn_id="turn-1")
    try:
        with caplog.at_level(logging.DEBUG, logger=logger.name):
            emitted = log_debug(logger, "chat.request.start", lifecycle="start", phase="accept")
    finally:
        reset_diagnostic_context(token)

    assert emitted is True
    record = caplog.records[0]
    assert record.turn_id == "turn-1"
    assert record.conversation_id == "conv-1"
    assert record.lifecycle == "start"
    assert "chat.request.start" in record.getMessage()


def test_debug_diagnostics_summary_includes_correlation() -> None:
    collector = DebugDiagnosticsCollector(
        provider="openai",
        model="gpt-test",
        turn_id="turn-1",
        request_id="req-1",
        interface="cli",
        conversation_id="conv-1",
    )

    summary = collector.finish("completed")

    assert summary["correlation"] == {
        "turn_id": "turn-1",
        "request_id": "req-1",
        "interface": "cli",
        "conversation_id": "conv-1",
    }


@pytest.mark.asyncio
async def test_tool_registry_debug_logs_shapes_not_raw_values(caplog: pytest.LogCaptureFixture) -> None:
    registry = ToolRegistry()

    async def handler(**_: object) -> dict[str, object]:
        return {"stdout": "super secret output", "exit_code": 0}

    registry.register("sample", handler, {"name": "sample", "description": "", "parameters": {}})
    token = set_diagnostic_context(turn_id="turn-tool")
    try:
        with caplog.at_level(logging.DEBUG, logger="anteroom.tools"):
            result = await registry.call_tool("sample", {"prompt": "raw prompt text", "password": "secret"})
    finally:
        reset_diagnostic_context(token)

    assert result["exit_code"] == 0
    messages = "\n".join(record.getMessage() for record in caplog.records)
    assert "tool.dispatch.start" in messages
    assert "tool.dispatch.success" in messages
    assert "raw prompt text" not in messages
    assert "super secret output" not in messages
    assert any(getattr(record, "turn_id", None) == "turn-tool" for record in caplog.records)
