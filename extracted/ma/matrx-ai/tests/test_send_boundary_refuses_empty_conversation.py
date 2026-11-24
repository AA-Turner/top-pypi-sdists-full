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


def test_the_refusal_carries_everything_the_executor_failure_path_reads() -> None:
    """The executor reads is_retryable / details / retry_schedule off ``exc.error_info``.

    The refusal once carried a lookalike without them, so the executor turned this plain
    refusal into ``AttributeError: ... has no attribute 'is_retryable'`` (found by the Model
    view capture, 2026-10-11). It must be the same envelope every other classified error uses.
    """
    from matrx_ai.providers.errors import RetryableError

    info = EmptyConversationError(step="conversation c1").error_info
    assert isinstance(info, RetryableError)
    assert info.is_retryable is False
    assert info.status_code == 422
    assert info.user_message == "There is nothing to send yet. Type a message and try again."


def test_an_empty_conversation_is_a_caller_refusal_never_a_provider_issue() -> None:
    """The caller sent nothing to answer: a CALLER REFUSAL, final and never filed as the provider's.

    Live 2026-11-06..13 (issue class ``anthropic.empty_conversation``, 5 events, every one a
    ``POST /ai/manual`` answered 422): the refusal was not marked, so the executor's terminal path
    filed it through ``capture_issue`` as Anthropic's own failure and fed it to the provider-outage
    alarm, although no provider was ever called. The executor skips ``capture_issue`` exactly when
    the exception says ``is_caller_refusal``; a code-only consumer (a retry loop, a workflow step)
    asks the registry.
    """
    from matrx_ai.providers.caller_refusal import caller_refusal_codes, is_caller_refusal

    exc = EmptyConversationError(step="conversation 00000000-0000-4000-8000-000000000000")
    assert is_caller_refusal(exc)
    assert exc.error_info.is_retryable is False
    assert "empty_conversation" in caller_refusal_codes()
    assert is_caller_refusal({"code": "empty_conversation"})
