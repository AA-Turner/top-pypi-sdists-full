"""turn_person_words: what the person typed in the running turn's message, never the platform parts on it."""

from __future__ import annotations

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
    turn_person_words,
)

BLOCK = '<turn_context source="platform">\nReference material for this turn.\n</turn_context>'


def _words(message: UnifiedMessage | None) -> str | None:
    state = ExecutionState()
    state.trigger_message = message
    token = set_execution_state(state)
    try:
        return turn_person_words()
    finally:
        clear_execution_state(token)


def test_her_words_without_the_platform_block() -> None:
    assert turn_person_words() is None  # outside a run
    assert _words(UnifiedMessage(role="user", content=[TextContent(text=BLOCK), TextContent(text="Yes, open it.")])) == "Yes, open it."
    assert _words(UnifiedMessage(role="user", content=[TextContent(text=BLOCK + "\n\nYes, open it.")])) == "Yes, open it."
    assert _words(UnifiedMessage(role="user", content=[TextContent(text=BLOCK)])) is None
    assert _words(UnifiedMessage(role="assistant", content=[TextContent(text="Yes")])) is None
    assert _words(UnifiedMessage(role="user", content=[TextContent(text="Yes")], position=4)) is None  # stored already
    assert _words(None) is None
