"""Unit tests for CLI feedback command handling."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.cli.feedback_cli import handle_feedback_command


def _config() -> Any:
    return SimpleNamespace(feedback=SimpleNamespace(max_history_messages=1))


@pytest.mark.asyncio
async def test_handle_feedback_command_passes_runtime_context() -> None:
    with patch("anteroom.services.feedback.submit_feedback", new_callable=AsyncMock) as mock_submit:
        mock_submit.return_value = {"status": "sent", "reporter": "test"}

        msg = await handle_feedback_command(
            "bug",
            True,
            _config(),
            object(),
            conversation_id="conv-1",
            project_path="/work/project",
            conversation_messages=[{"role": "user", "content": "old"}, {"role": "assistant", "content": "new"}],
            active_space={"id": "space-1", "name": "Main"},
            tool_registry=object(),
            mcp_manager=object(),
            turn_diagnostics={"stop_reason": "completed"},
        )

    assert msg == "Feedback submitted via reporter 'test'."
    kwargs = mock_submit.call_args.kwargs
    assert kwargs["interface"] == "cli"
    assert kwargs["space_id"] == "space-1"
    assert kwargs["project_path"] == "/work/project"
    assert kwargs["conversation_messages"] == [{"role": "assistant", "content": "new"}]
    assert kwargs["turn_diagnostics"] == {"stop_reason": "completed"}


@pytest.mark.asyncio
async def test_handle_feedback_command_preserves_explicit_empty_history() -> None:
    with patch("anteroom.services.feedback.submit_feedback", new_callable=AsyncMock) as mock_submit:
        mock_submit.return_value = {"status": "saved_locally", "path": "/tmp/feedback.json"}

        msg = await handle_feedback_command(
            "bug",
            True,
            _config(),
            object(),
            conversation_messages=[],
        )

    assert msg == "No reporter configured. Bundle saved to: /tmp/feedback.json"
    assert mock_submit.call_args.kwargs["conversation_messages"] == []
