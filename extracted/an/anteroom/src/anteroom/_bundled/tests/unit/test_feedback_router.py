"""Unit tests for the feedback API router."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from anteroom.routers.feedback import FeedbackRequest, _public_feedback_result, submit_feedback_endpoint


def _request() -> Any:
    return SimpleNamespace(
        headers={"content-type": "application/json"},
        app=SimpleNamespace(
            state=SimpleNamespace(
                config=SimpleNamespace(),
                db=MagicMock(),
                tool_registry=None,
                mcp_manager=None,
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
