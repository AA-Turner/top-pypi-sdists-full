"""An empty conversation is refused at the send boundary, never sent (feedback 577420ef).

Live 2026-10-01..03: the notes page-guidance agent (system-prompt only) ran with an
empty user turn, and conversation crash recovery resumed a conversation with nothing
in it; both reached Anthropic, which answered 400 "messages: at least one message is
required" after a round-trip. The send boundary now refuses first, with a typed,
classified error the stream layer surfaces.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.send_boundary import (
    STAGE_LOOP,
    EmptyConversationError,
    prepare_for_send,
)
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.context_trim import TrimPolicy


def _config(messages: list) -> UnifiedConfig:
    return UnifiedConfig(model="claude-sonnet-4-6", messages=messages, system_instruction="You help with notes.")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "messages",
    [
        [],
        [{"role": "user", "content": []}],
        [{"role": "user", "content": [{"type": "text", "text": "   "}]}],
    ],
    ids=["no-messages", "empty-user-turn", "whitespace-user-turn"],
)
async def test_nothing_to_send_is_refused_before_the_provider(messages: list) -> None:
    with pytest.raises(EmptyConversationError) as caught:
        await prepare_for_send(_config(messages), stage=STAGE_LOOP, policy=TrimPolicy())
    assert caught.value.error_info.error_type == "empty_conversation"
    assert caught.value.error_info.user_message


@pytest.mark.asyncio
async def test_a_real_user_turn_is_sent() -> None:
    prep = await prepare_for_send(
        _config([{"role": "user", "content": [{"type": "text", "text": "Summarize this note."}]}]),
        stage=STAGE_LOOP,
        policy=TrimPolicy(),
    )
    assert "empty_conversation_check" in prep.steps
