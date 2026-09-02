from types import SimpleNamespace

import pytest

from matrx_ai.tools.executor import (
    CONTEXT_PATCH_NO_MATCH_KIND,
    TOOL_ARGUMENT_VALIDATION_FAILED_KIND,
    _capture_context_patch_no_match,
    _capture_tool_argument_validation_failed,
    _is_expected_domain_failure,
)


def test_expected_domain_failures_exclude_context_create_denial_from_error_logs() -> None:
    assert _is_expected_domain_failure(
        tool_name="context", error_type="context_create_disabled"
    )
    assert _is_expected_domain_failure(
        tool_name="context", error_type="context_not_attached"
    )
    assert _is_expected_domain_failure(tool_name="context_patch", error_type="patch_no_match")
    assert _is_expected_domain_failure(
        tool_name="code_execute_python", error_type="python_error"
    )
    # The refusal list is not a blanket pass for the tool: an OPERATIONAL
    # failure on `context` still has to reach the repair queue. (Bare
    # "validation" moved into the tool-agnostic refusal set on 2026-08-27 —
    # see tools/FEATURE.md — so the contract is pinned here with an
    # operational error type instead.)
    assert not _is_expected_domain_failure(tool_name="context", error_type="execution")


@pytest.mark.asyncio
async def test_context_patch_no_match_creates_structured_incident(monkeypatch) -> None:
    captured: list[tuple[BaseException, dict[str, object]]] = []

    async def fake_capture_error(exc: BaseException, **kwargs: object) -> None:
        captured.append((exc, kwargs))

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture_error)
    ctx = SimpleNamespace(
        request_id="req-1", user_id="user-1", conversation_id="conv-1", call_id="call-1"
    )

    await _capture_context_patch_no_match(ctx=ctx)

    assert len(captured) == 1
    _exc, incident = captured[0]
    assert incident["kind"] == CONTEXT_PATCH_NO_MATCH_KIND
    assert incident["route"] == "tool_executor.context_patch"
    assert incident["error_type"] == "PatchNoMatch"
    assert incident["context"] == {
        "tool_name": "context_patch",
        "call_id": "call-1",
        "retryable": True,
    }
    assert "payload" not in incident
    assert "old_str" not in repr(incident)


@pytest.mark.asyncio
async def test_invalid_tool_arguments_create_safe_structured_incident(monkeypatch) -> None:
    captured: list[tuple[BaseException, dict[str, object]]] = []

    async def fake_capture_error(exc: BaseException, **kwargs: object) -> None:
        captured.append((exc, kwargs))

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture_error)
    ctx = SimpleNamespace(
        request_id="req-1", user_id="user-1", conversation_id="conv-1", call_id="call-1"
    )

    await _capture_tool_argument_validation_failed(ctx=ctx, tool_name="memory")

    assert len(captured) == 1
    _exc, incident = captured[0]
    assert incident["kind"] == TOOL_ARGUMENT_VALIDATION_FAILED_KIND
    assert incident["route"] == "tool_executor.argument_validation"
    assert incident["error_type"] == "ToolArgumentValidationError"
    assert incident["context"] == {"tool_name": "memory", "call_id": "call-1"}
    assert "payload" not in incident
    assert "limit" not in repr(incident)
