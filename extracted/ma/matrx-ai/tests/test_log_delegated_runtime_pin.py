"""log_delegated stamps the runtime-spine ROOT execution id onto the delegated
cx_tool_call row — the pin the conversation resume re-attaches by (migration 0164).

Two invariants:
1. The stamp reads `runtime_root_execution_id` (stamped once per request by the
   conversation open/resume), NEVER `runtime_execution_id` — that key is the CURRENT
   NESTING PARENT and is legitimately re-stamped mid-turn (a chat-launched workflow
   points it at the workflow execution), which would pin an id the resume can never
   match.
2. No context / no stamp → the column is simply absent (best-effort, ledger unharmed).
"""

from __future__ import annotations

import types
from datetime import UTC, datetime
from unittest.mock import patch

import pytest

from matrx_ai.tools.logger import ToolExecutionLogger

pytestmark = pytest.mark.asyncio


def _ctx(metadata):
    return types.SimpleNamespace(metadata=metadata)


async def _run_log_delegated(logger, captured):
    async def fake_update_row(row_id, data, *, coordinator=None):
        captured["row_id"] = row_id
        captured["data"] = data

    logger._update_row = fake_update_row  # instance-level override
    await logger.log_delegated("row-1", expires_at=datetime(2026, 7, 13, tzinfo=UTC))


async def test_stamp_uses_root_key_not_nesting_key():
    captured = {}
    logger = ToolExecutionLogger()
    ctx = _ctx(
        {
            "runtime_execution_id": "workflow-exec",  # re-stamped nesting parent — poison
            "runtime_root_execution_id": "conversation-root",
        }
    )
    with patch("matrx_ai.context.app_context.try_get_app_context", return_value=ctx):
        await _run_log_delegated(logger, captured)

    assert captured["row_id"] == "row-1"
    assert captured["data"]["status"] == "delegated"
    assert captured["data"]["runtime_execution_id"] == "conversation-root"


async def test_no_root_stamp_leaves_column_absent():
    captured = {}
    logger = ToolExecutionLogger()
    # Only the nesting key present (e.g. a v1 path that never opened the spine root):
    ctx = _ctx({"runtime_execution_id": "workflow-exec"})
    with patch("matrx_ai.context.app_context.try_get_app_context", return_value=ctx):
        await _run_log_delegated(logger, captured)

    assert "runtime_execution_id" not in captured["data"]


async def test_no_context_leaves_column_absent():
    captured = {}
    logger = ToolExecutionLogger()
    with patch("matrx_ai.context.app_context.try_get_app_context", return_value=None):
        await _run_log_delegated(logger, captured)

    assert "runtime_execution_id" not in captured["data"]
    assert captured["data"]["is_client_delegated"] is True
