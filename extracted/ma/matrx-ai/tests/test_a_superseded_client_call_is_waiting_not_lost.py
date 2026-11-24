"""A client-run call the person talked past is waiting, not lost (system_error e50a8a75, 2026-11-19).

A client-run (delegated) call was open in a held stream (an approval or plan card; ``probe_step`` in aidream
``scripts/prove_held_stream_live.py``) and the person sent a new message instead of answering. aidream
``release_holds_for_new_message`` released the hold (RESUME-AND-RECOVERY section 1b rule P9) and the call stayed
``delegated``. The new message is appended AFTER the rebuild, so the call was the last thing in history; the rebuild
left it bare, and the sanitizer wrote "TOOL NEVER ANSWERED" to the model and filed ``orphan_tool_use_repaired``.

The release now marks the call ``superseded_by_person``; a marked call reads "STILL WAITING FOR THE APP" and files
nothing. A call unanswered WITHOUT the mark is a truly lost call and still files.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db._registry import configure_db

configure_db(models={"CxMessage": SimpleNamespace, "CxToolCall": SimpleNamespace, "CxMedia": SimpleNamespace})

from matrx_ai.config import message_config  # noqa: E402
from matrx_ai.config.enums import Role  # noqa: E402
from matrx_ai.config.message_config import MessageList, UnifiedMessage  # noqa: E402
from matrx_ai.config.tools_config import ToolResultContent  # noqa: E402
from matrx_ai.config.unified_content import TextContent  # noqa: E402
from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages  # noqa: E402
from matrx_ai.tools.logger import SUPERSEDED_BY_PERSON_KEY  # noqa: E402

ASSISTANT = "22222222-2222-2222-2222-222222222222"


def _history() -> list[SimpleNamespace]:
    return [
        SimpleNamespace(
            id="u1", role="user", position=0, content=[{"type": "text", "text": "Check the page for me."}],
            created_at=None, status="active", metadata={}, deleted_at=None, is_visible_to_model=True,
        ),
        SimpleNamespace(
            id=ASSISTANT, role="assistant", position=1,
            content=[{"type": "tool_call", "call_id": "toolu_probe", "name": "probe_step", "arguments": {}}],
            created_at=None, status="active", metadata={}, deleted_at=None, is_visible_to_model=True,
        ),
    ]


def _row(metadata: dict[str, Any]) -> SimpleNamespace:
    return SimpleNamespace(
        id="row-0", call_id="toolu_probe", message_id=ASSISTANT, tool_name="probe_step", output="",
        is_error=False, status="delegated", output_chars=0, output_preview=None, error_type=None,
        error_message=None, deleted_at=None, metadata=metadata,
    )


async def _next_turn(row: SimpleNamespace, monkeypatch: Any) -> tuple[list[ToolResultContent], list[Any]]:
    """Rebuild history, append the person's new message, run the strict sanitizer as a send does."""
    reported: list[Any] = []
    monkeypatch.setattr(message_config, "report_orphan_tool_uses_repaired", lambda **kw: reported.append(kw))
    rebuilt = await rebuild_conversation_messages(_history(), [row], [])
    messages = MessageList(
        [*rebuilt, UnifiedMessage(role=Role.USER, content=[TextContent(text="Never mind, what time is it?")])]
    )
    messages.sanitize()
    results = [c for m in messages for c in m.content if isinstance(c, ToolResultContent)]
    return results, reported


@pytest.mark.asyncio
async def test_a_call_superseded_by_the_person_reads_still_waiting_and_files_nothing(monkeypatch: Any) -> None:
    results, reported = await _next_turn(_row({SUPERSEDED_BY_PERSON_KEY: {"at": "2026-11-19T00:00:00+00:00"}}), monkeypatch)
    [result] = results
    assert result.tool_use_id == "toolu_probe"
    assert "STILL WAITING FOR THE APP [probe_step]" in str(result.content)
    assert "NEVER ANSWERED" not in str(result.content)
    assert not result.is_error
    assert reported == [], "a call the person talked past is not a lost call: no orphan row"


@pytest.mark.asyncio
async def test_an_unmarked_lost_call_still_files(monkeypatch: Any) -> None:
    results, reported = await _next_turn(_row({}), monkeypatch)
    [result] = results
    assert "TOOL NEVER ANSWERED [probe_step]" in str(result.content)
    assert result.is_error
    assert len(reported) == 1, "a truly lost client call still files orphan_tool_use_repaired"
