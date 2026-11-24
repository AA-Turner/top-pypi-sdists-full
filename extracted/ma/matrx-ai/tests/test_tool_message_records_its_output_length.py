"""A persisted tool-result message records the length of the output it holds.

Live voice (2026-11-05): the saved tool-result message said ``output_chars: 0`` while its
``chat.tool_call`` row held the real output. The message is built from the STORAGE dict, which
does not carry ``output_chars`` (only the executor's logger stamp does, on typed turns), so any
result without that stamp recorded 0. The same 0 sat on typed chats' tool messages.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config.tools_config import ToolResultContent
from matrx_ai.db import persistence


@pytest.mark.asyncio
async def test_a_tool_result_without_a_logger_stamp_records_its_real_length(monkeypatch):
    async def _backfill(*a, **k):
        return None

    import matrx_ai.tools.handle_tool_calls as htc

    monkeypatch.setattr(
        htc, "get_executor", lambda: SimpleNamespace(execution_logger=SimpleNamespace(backfill_message_id=_backfill))
    )
    result = ToolResultContent(
        tool_use_id="call_1", call_id="call_1", name="list_agents",
        content=[{"type": "text", "text": "x" * 40}],
    )
    # Exactly what persistence receives: the storage dict, not the object.
    msg = {"role": "tool", "content": [result.to_storage_dict()]}

    blocks = await persistence._backfill_tool_message(msg, "m1", "c1")

    assert blocks[0]["output_chars"] == 40
