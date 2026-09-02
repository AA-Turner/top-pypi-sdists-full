from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.persistence.postgres_text import sanitize_postgres_text


def test_recursive_sanitizer_is_copy_on_write_and_covers_json_keys() -> None:
    original = {
        "content": [{"type": "text", "text": "before\x00after"}],
        "meta\x00key": ("clean", "bad\x00value"),
    }
    result = sanitize_postgres_text(original)
    assert result.replacements == 3
    assert result.value == {
        "content": [{"type": "text", "text": "before\ufffdafter"}],
        "meta\ufffdkey": ("clean", "bad\ufffdvalue"),
    }
    assert original["content"][0]["text"] == "before\x00after"
    assert set(result.paths) == {
        "payload.content[0].text",
        "payload.<key>",
        "payload.meta\ufffdkey[1]",
    }


@pytest.mark.asyncio
async def test_queue_helper_sanitizes_message_before_coordinator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.persistence import queue_helpers

    queued: list[dict[str, object]] = []
    captures: list[dict[str, object]] = []

    class FakeCoordinator:
        _late_boundary_captured = False

        def queue(self, table: str, payload: dict[str, object], **kwargs: object) -> str:
            queued.append({"table": table, "payload": payload, "kwargs": kwargs})
            return "op-1"

    async def fake_capture_error(exc: BaseException, **kwargs: object) -> None:
        captures.append({"exc": exc, **kwargs})

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: FakeCoordinator())
    monkeypatch.setattr(queue_helpers, "get_current_lane", lambda: None)
    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(request_id="r-1", user_id="u-1", conversation_id="c-1"),
    )
    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        fake_capture_error,
    )
    op_id = queue_helpers.queue_message_create(
        id="m-1",
        conversation_id="c-1",
        content=[{"type": "text", "text": "hello\x00world"}],
    )
    await asyncio.sleep(0)
    assert op_id == "op-1"
    assert queued[0]["payload"]["content"][0]["text"] == "hello\ufffdworld"
    assert captures[0]["kind"] == "persistence_payload_sanitized"


@pytest.mark.asyncio
async def test_coordinator_backstop_sanitizes_direct_queue(
    monkeypatch: pytest.MonkeyPatch,
    capture_sink: tuple[list[dict[str, object]], list[dict[str, object]]],
) -> None:
    from matrx_ai.persistence import coordinator as coordinator_module

    class FakeSession:
        ops_count = 0

        def defer_insert(self, model: object, payload: dict[str, object], **kwargs: object) -> str:
            assert payload["content"][0]["text"] == "hello\ufffdworld"
            return "op-direct"

    monkeypatch.setattr(coordinator_module, "get_model", lambda table: object())
    coord = object.__new__(coordinator_module.Coordinator)
    coord._session = FakeSession()
    coord._phase = coordinator_module.CoordinatorPhase.OPEN
    coord._dropped_ops_count = 0
    coord._request_id = "r-2"
    coord._user_id = "u-2"
    coord._conversation_id = "c-2"
    coord._database = "matrx"
    op_id = coord.queue(
        "chat.message",
        {"id": "m-2", "content": [{"type": "text", "text": "hello\x00world"}]},
    )
    await asyncio.sleep(0)
    assert op_id == "op-direct"
    assert capture_sink[1][0]["kwargs"]["kind"] == "persistence_payload_sanitized"
    assert capture_sink[1][0]["kwargs"]["context"]["layer"] == "coordinator_backstop"


def test_tool_metadata_sanitizes_explicit_output_and_preview_before_snapshot() -> None:
    from matrx_ai.tools.logger import ToolExecutionLogger
    from matrx_ai.tools.models import ToolResult

    result = ToolResult(
        success=True,
        output={"stdout": "first\x00second"},
        output_chars=12,
        output_preview={"stdout": "first\x00second"},
    )

    ToolExecutionLogger().prepare_metadata(result)

    assert result.output == {"stdout": "first\ufffdsecond"}
    assert result.output_preview == {"stdout": "first\ufffdsecond"}
    assert result.output_chars == 12


@pytest.mark.asyncio
async def test_tool_completion_event_sanitizes_its_persisted_result_copy() -> None:
    from matrx_ai.tools.models import ToolResult
    from matrx_ai.tools.streaming import ToolStreamManager

    stream = ToolStreamManager(None, call_id="call-1", tool_name="shell_execute")
    await stream.completed(
        result=ToolResult(success=True, output={"stdout": "first\x00second"})
    )

    events = stream.get_events_for_persistence()
    assert events[0]["data"]["result"]["stdout"] == "first\ufffdsecond"
