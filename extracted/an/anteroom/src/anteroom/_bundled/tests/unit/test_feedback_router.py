"""Unit tests for the feedback API router."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from anteroom.routers.feedback import (
    FeedbackRequest,
    _is_json_content_type,
    _public_feedback_result,
    submit_feedback_endpoint,
)


def _request() -> Any:
    return SimpleNamespace(
        headers={"content-type": "application/json"},
        app=SimpleNamespace(
            state=SimpleNamespace(
                config=SimpleNamespace(),
                db=MagicMock(),
                tool_registry=None,
                mcp_manager=None,
                feedback_turn_diagnostics={"conv-1": {"stop_reason": "completed"}},
            )
        ),
    )


def test_public_feedback_result_hides_local_path() -> None:
    result = _public_feedback_result(
        {
            "status": "saved_locally",
            "reporter": "local",
            "path": "/Users/troy/.anteroom/feedback-secret.json",
        }
    )

    assert result == {
        "status": "saved_locally",
        "reporter": "local",
        "message": "Feedback bundle saved locally on the server.",
    }
    assert "path" not in result


def test_public_feedback_result_hides_failure_details() -> None:
    result = _public_feedback_result(
        {
            "status": "failed",
            "reporter": "jira",
            "error": "Traceback with /Users/troy/.ssh/id_ed25519",
        }
    )

    assert result["status"] == "failed"
    assert result["reporter"] == "jira"
    assert "/Users/" not in result["error"]
    assert "Traceback" not in result["error"]


def test_json_content_type_requires_json_media_type() -> None:
    assert _is_json_content_type("application/json")
    assert _is_json_content_type("application/json; charset=utf-8")
    assert not _is_json_content_type("application/jsonp")
    assert not _is_json_content_type("text/plain")


@pytest.mark.asyncio
async def test_include_history_requires_existing_conversation() -> None:
    body = FeedbackRequest(description="bug", include_history=True, conversation_id="missing")

    with patch("anteroom.services.storage.get_conversation", return_value=None):
        with pytest.raises(HTTPException) as excinfo:
            await submit_feedback_endpoint(body, _request())

    assert excinfo.value.status_code == 404


@pytest.mark.asyncio
async def test_endpoint_returns_sanitized_service_result() -> None:
    body = FeedbackRequest(description="bug")

    with patch("anteroom.services.feedback.submit_feedback", new_callable=AsyncMock) as mock_submit:
        mock_submit.return_value = {
            "status": "saved_locally",
            "reporter": "local",
            "path": "/tmp/feedback.json",
        }
        result = await submit_feedback_endpoint(body, _request())

    assert result["status"] == "saved_locally"
    assert "path" not in result


@pytest.mark.asyncio
async def test_endpoint_passes_feedback_context_to_service() -> None:
    body = FeedbackRequest(description="bug", conversation_id="conv-1", space_id="space-1")
    req = _request()

    with (
        patch("anteroom.services.storage.get_conversation", return_value={"id": "conv-1", "space_id": "space-1"}),
        patch("anteroom.services.space_storage.get_space", return_value={"id": "space-1", "name": "Main"}),
        patch("anteroom.services.space_storage.get_space_local_dirs", return_value=["/work/project"]),
        patch("anteroom.services.feedback.submit_feedback", new_callable=AsyncMock) as mock_submit,
    ):
        mock_submit.return_value = {"status": "sent", "reporter": "test"}
        result = await submit_feedback_endpoint(body, req)

    assert result == {"status": "sent", "reporter": "test"}
    kwargs = mock_submit.call_args.kwargs
    assert kwargs["interface"] == "web"
    assert kwargs["space_id"] == "space-1"
    assert kwargs["project_path"] == "/work/project"
    assert kwargs["turn_diagnostics"] == {"stop_reason": "completed"}


@pytest.mark.asyncio
async def test_endpoint_rejects_space_mismatch_for_conversation() -> None:
    body = FeedbackRequest(description="bug", conversation_id="conv-1", space_id="space-2")

    with patch("anteroom.services.storage.get_conversation", return_value={"id": "conv-1", "space_id": "space-1"}):
        with pytest.raises(HTTPException) as excinfo:
            await submit_feedback_endpoint(body, _request())

    assert excinfo.value.status_code == 400


@pytest.mark.asyncio
async def test_endpoint_rejects_jsonp_content_type() -> None:
    body = FeedbackRequest(description="bug")
    req = _request()
    req.headers = {"content-type": "application/jsonp"}

    with pytest.raises(HTTPException) as excinfo:
        await submit_feedback_endpoint(body, req)

    assert excinfo.value.status_code == 415
