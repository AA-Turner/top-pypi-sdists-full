"""A mandate-held (live-Holder) thread keeps the tools added during the conversation.

The Holder supplies the structural half every turn, but a tool a surface, compute target,
attached context or opened bundle added during THIS conversation belongs to the conversation
(TOOL-SOURCES.md, stickiness). RED before 2026-10-03 twice over: persistence dropped
``dynamic_tools`` from a live row (``HOLDER_OWNED_CONFIG_KEYS``), and the responder branch of the
resolver never read the row's toolset at all.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents import resolver as module
from matrx_ai.agents.live_structure import stamp_live_structure
from matrx_ai.config import UnifiedConfig

CONVERSATION = "33333333-3333-4333-8333-333333333333"
HOLDER = "44444444-4444-4444-8444-444444444444"
STICKY = ["bundle:list_data-and-documents", "workbook"]
SOURCES = {"bundle:list_data-and-documents": "surface", "workbook": "bundle"}


def test_persistence_keeps_the_conversations_sticky_toolset_on_a_live_row() -> None:
    row = stamp_live_structure(
        {"tools": ["staff_roster"], "dynamic_tools": STICKY, "dynamic_tool_sources": SOURCES},
        mandate_key="personal_staff.chief_of_staff",
    )
    assert "tools" not in row, "the Holder's belt must not be frozen onto the row"
    assert row.get("dynamic_tools") == STICKY, f"the conversation's sticky tools were dropped: {row}"
    assert row.get("dynamic_tool_sources") == SOURCES


@pytest.mark.asyncio
async def test_a_holder_turn_carries_the_conversations_sticky_toolset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    holder_config = UnifiedConfig(model="claude-sonnet-5", messages=[], tools=["staff_roster"])

    class _Holder:
        config = holder_config

    async def from_agent(agent_id: str, **_kwargs: object) -> _Holder:
        return _Holder()

    async def persisted(_conversation_id: str) -> list:
        return []

    async def sticky(conversation_id: str) -> tuple[list[str], dict[str, str]]:
        assert conversation_id == CONVERSATION
        return list(STICKY), dict(SOURCES)

    async def prepare_for_send(_config: UnifiedConfig, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(module.Agent, "from_agent", from_agent)
    monkeypatch.setattr(module, "_load_persisted_messages", persisted)
    monkeypatch.setattr(module, "_load_sticky_toolset", sticky)
    monkeypatch.setattr("matrx_ai.config.send_boundary.prepare_for_send", prepare_for_send)

    config = await module.ConversationResolver.from_conversation_id(
        CONVERSATION,
        user_input="And the spreadsheet?",
        responder_agent_id=HOLDER,
        responder_mandate_key="personal_staff.chief_of_staff",
    )
    assert config.dynamic_tools[: len(STICKY)] == STICKY, config.dynamic_tools
    assert config.dynamic_tool_sources["workbook"] == "bundle"
    assert holder_config.dynamic_tools in ([], None), "the Holder's own config was mutated"
