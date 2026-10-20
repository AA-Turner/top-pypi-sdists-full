"""A system run made inside someone's conversation is saved as a hidden system process.

The labeler names a chat by running inside it as a system run; the run mints its own
conversation linked to the chat. The fork stamped it ``subagent``, so ~2,100 labeler runs
showed up nested under the chats they named (2026-10-18). A helper an agent DELEGATES to
is still a ``subagent``; a root system run keeps its derived type.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.agents.conversation_type import (
    HIDDEN_CONVERSATION_TYPES,
    INTERNAL_CONVERSATION_TYPES,
    ConversationType,
)
from matrx_ai.db.conversation_gate import _resolve_conversation_type

PARENT = "6b7d1d36-6d0b-4c6e-9a5e-2f4c8f0d1a11"


def _ctx(**fields: object) -> SimpleNamespace:
    base: dict[str, object] = {
        "metadata": {},
        "conversation_type": "subagent",
        "is_internal_agent": True,
        "source_feature": "mandate:conversation.label_chat",
        "parent_conversation_id": PARENT,
        "system_run": False,
    }
    base.update(fields)
    return SimpleNamespace(**base)


def test_a_system_run_inside_a_chat_is_a_system_process() -> None:
    assert _resolve_conversation_type(_ctx(system_run=True)) == "system_process"
    # The parent may arrive as the write site's argument instead of on the context.
    ctx = _ctx(system_run=True, parent_conversation_id=None)
    assert _resolve_conversation_type(ctx, PARENT) == "system_process"


def test_a_delegated_helper_stays_a_visible_subagent() -> None:
    assert _resolve_conversation_type(_ctx(system_run=False)) == "subagent"


def test_a_root_system_run_keeps_its_own_type() -> None:
    ctx = _ctx(system_run=True, parent_conversation_id=None, conversation_type="scheduled")
    assert _resolve_conversation_type(ctx) == "scheduled"


def test_a_system_process_is_hidden_and_internal() -> None:
    assert ConversationType.SYSTEM_PROCESS.value in HIDDEN_CONVERSATION_TYPES
    assert ConversationType.MANDATE_CANDIDATE.value in HIDDEN_CONVERSATION_TYPES
    # Internal: it is never itself labeled or ingested (no labeler labeling the labeler).
    assert ConversationType.SYSTEM_PROCESS.value in INTERNAL_CONVERSATION_TYPES
