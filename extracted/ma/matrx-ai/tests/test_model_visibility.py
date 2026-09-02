"""Regression guard for the "hidden from agent" invariant.

A cx_message with is_visible_to_model=False (a failed turn, or a system-
compacted message) must NEVER reach the provider. Enforced at two independent
layers:
  1. rebuild_conversation_messages — primary filter at DB-load time (excludes
     the row before it ever becomes a UnifiedMessage). Covered by DB-backed
     tests elsewhere; here we pin the unit pieces it composes.
  2. UnifiedMessage carries is_visible_to_model, and MessageList.sanitize drops
     such messages at the provider-payload boundary — the last-line backstop
     for ANY path that bypasses rebuild.

NOTE: compaction sets is_visible_to_model=False but leaves status='active', so
filtering MUST key off is_visible_to_model, not status.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config.message_config import (
    MessageList,
    MessageSanitizationError,
    UnifiedMessage,
)
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent


def test_from_cx_message_carries_visibility_false() -> None:
    row = SimpleNamespace(
        role="assistant", content=[], id="a1", created_at=None,
        status="failed", metadata={}, position=1, is_visible_to_model=False,
    )
    um = UnifiedMessage.from_cx_message(row)
    assert um.is_visible_to_model is False


def test_from_cx_message_carries_visibility_compacted_active() -> None:
    # Compaction: is_visible_to_model=False while status stays 'active'.
    row = SimpleNamespace(
        role="assistant", content=[], id="c1", created_at=None,
        status="active", metadata={}, position=2, is_visible_to_model=False,
    )
    um = UnifiedMessage.from_cx_message(row)
    assert um.is_visible_to_model is False  # keyed off the flag, NOT status


def test_from_cx_message_defaults_visible_when_absent() -> None:
    row = SimpleNamespace(
        role="user", content=[], id="u0", created_at=None,
        status="active", metadata={}, position=0,
    )  # no is_visible_to_model attribute at all
    um = UnifiedMessage.from_cx_message(row)
    assert um.is_visible_to_model is True


def test_sanitize_drops_hidden_from_provider_payload() -> None:
    visible = UnifiedMessage(
        role="user", content=[TextContent(text="hi")], id="u", is_visible_to_model=True,
    )
    hidden = UnifiedMessage(
        role="assistant", content=[TextContent(text="this turn failed")],
        id="a", status="failed", is_visible_to_model=False,
    )
    ml = MessageList([visible, hidden])
    ml.sanitize()
    ids = [m.id for m in ml]
    assert "u" in ids
    assert "a" not in ids  # hidden message never reaches the provider


def test_sanitize_keeps_visible_with_content() -> None:
    visible = UnifiedMessage(
        role="assistant", content=[TextContent(text="real answer")], id="ok",
        status="active", is_visible_to_model=True,
    )
    ml = MessageList([visible])
    ml.sanitize()
    assert [m.id for m in ml] == ["ok"]


# --- tool_use / tool_result coherence (the dangling-tool_use 400 guard) ---

def test_sanitize_drops_orphan_tool_use_keeps_text() -> None:
    # Assistant called a tool that never returned a result (delegated timeout).
    # The orphan tool_use must be stripped, the assistant's text kept.
    asst = UnifiedMessage(
        role="assistant",
        content=[TextContent(text="let me check"), ToolCallContent(id="toolu_1", name="storage")],
        id="a",
    )
    ml = MessageList([asst])
    ml.sanitize()
    msgs = list(ml)
    assert len(msgs) == 1
    assert any(isinstance(c, TextContent) for c in msgs[0].content)
    assert not any(isinstance(c, ToolCallContent) for c in msgs[0].content)


def test_sanitize_keeps_paired_tool_use_and_result() -> None:
    asst = UnifiedMessage(role="assistant", content=[ToolCallContent(id="toolu_1", name="storage")], id="a")
    tool = UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="toolu_1", name="storage")], id="t")
    ml = MessageList([asst, tool])
    ml.sanitize()
    msgs = list(ml)
    assert len(msgs) == 2
    assert any(isinstance(c, ToolCallContent) for c in msgs[0].content)
    assert any(isinstance(c, ToolResultContent) for c in msgs[1].content)


def test_sanitize_drops_orphan_tool_use_only_message() -> None:
    # Assistant message whose ONLY content is a dangling tool_use → dropped.
    asst = UnifiedMessage(role="assistant", content=[ToolCallContent(id="toolu_1", name="storage")], id="a")
    ml = MessageList([asst])
    with pytest.raises(MessageSanitizationError, match="emptying_pass=tool_pairing"):
        ml.sanitize()


def test_sanitize_drops_orphan_tool_result() -> None:
    tool = UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="toolu_x")], id="t")
    ml = MessageList([tool])
    with pytest.raises(MessageSanitizationError, match="emptying_pass=tool_pairing"):
        ml.sanitize()


def test_sanitize_names_visibility_when_all_messages_are_hidden() -> None:
    hidden = UnifiedMessage(
        role="assistant",
        content=[TextContent(text="failed output")],
        id="hidden",
        is_visible_to_model=False,
    )
    ml = MessageList([hidden])

    with pytest.raises(MessageSanitizationError, match="emptying_pass=visibility"):
        ml.sanitize()


def test_sanitize_names_empty_scrub_for_whitespace_only_input() -> None:
    empty = UnifiedMessage(
        role="user",
        content=[TextContent(text="  \n")],
        id="empty-user",
    )
    ml = MessageList([empty])

    with pytest.raises(MessageSanitizationError, match="emptying_pass=empty_scrub"):
        ml.sanitize()


def test_sanitize_allows_an_initially_empty_message_list() -> None:
    ml = MessageList([])

    ml.sanitize()

    assert list(ml) == []


# --- single-result-per-tool_use (the duplicate-tool_result 400 guard) ---

def _tool_results_for(ml: MessageList, rid: str) -> list[ToolResultContent]:
    out: list[ToolResultContent] = []
    for m in ml:
        for c in m.content:
            if isinstance(c, ToolResultContent) and (c.tool_use_id or c.call_id) == rid:
                out.append(c)
    return out


def test_sanitize_dedupes_duplicate_tool_result_keeps_content_bearing() -> None:
    # Reproduces the incident: a server tool whose completion write was lost
    # left an orphaned cx_tool_call row that the watchdog swept, so the rebuild
    # emitted TWO tool_results for the same tool_use — an empty inline stub and
    # a content-bearing (watchdog) one. Anthropic 400s the WHOLE request on this
    # ("each tool_use must have a single result"). sanitize must collapse to one,
    # keeping the informative block.
    asst = UnifiedMessage(role="assistant", content=[ToolCallContent(id="toolu_016", name="agent_call")], id="a")
    empty = UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="toolu_016", name="agent_call")], id="t1")
    informative = UnifiedMessage(
        role="tool",
        content=[ToolResultContent(
            tool_use_id="toolu_016", name="agent_call", is_error=True,
            content=[{"type": "text", "text": "watchdog_timeout"}],
        )],
        id="t2",
    )
    ml = MessageList([asst, empty, informative])
    ml.sanitize()
    kept = _tool_results_for(ml, "toolu_016")
    assert len(kept) == 1  # exactly one result survives — no provider 400
    assert kept[0].content  # the content-bearing block was the one kept


def test_sanitize_dedupes_duplicate_tool_result_when_both_empty() -> None:
    asst = UnifiedMessage(role="assistant", content=[ToolCallContent(id="toolu_016", name="agent_call")], id="a")
    dup1 = UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="toolu_016", name="agent_call")], id="t1")
    dup2 = UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="toolu_016", name="agent_call")], id="t2")
    ml = MessageList([asst, dup1, dup2])
    ml.sanitize()
    assert len(_tool_results_for(ml, "toolu_016")) == 1  # still collapses to one
