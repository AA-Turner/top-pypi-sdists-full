"""FORCING GUARD — OpenAI's prompt_cache_key is the same on every turn of a conversation.

OpenAI routes a request to a prompt cache by the prefix hash plus
``prompt_cache_key``. The key was a hash of request id + conversation id, so
every turn of one conversation carried a DIFFERENT key and turn 2 was routed by
chance, away from the cache turn 1 wrote. The group that shares a prefix across
turns is the conversation. Red on origin/main, green after.
"""

from __future__ import annotations

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.send_boundary import _set_prompt_cache_key
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers import cache_guard
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.testing.profile_factory import make_profile

CONVERSATION = "081a351a-0264-4fe4-8d55-a12d4e8f9a11"


def _wire_key(request_id: str) -> str:
    config = UnifiedConfig(
        model="gpt-5-mini",
        system_instruction="stable system",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
    )
    _set_prompt_cache_key(config, CONVERSATION, request_id)  # the send boundary's step
    return OpenAITranslator().build_request(
        config, make_profile(model_name="gpt-5-mini", wire_format="openai_responses")
    )["prompt_cache_key"]


def test_two_turns_of_one_conversation_send_the_same_key() -> None:
    turn_one = _wire_key("request-turn-1")
    turn_two = _wire_key("request-turn-2")
    assert turn_one == turn_two, (
        "each turn carried a different prompt_cache_key, so OpenAI routed turn 2 "
        "away from the cache turn 1 wrote"
    )
    assert CONVERSATION not in turn_one
    assert len(turn_one) <= cache_guard.OPENAI_PROMPT_CACHE_KEY_MAX_CHARS


def test_two_conversations_get_different_keys() -> None:
    a = cache_guard.provider_prompt_cache_key("conversation-a", "r1")
    b = cache_guard.provider_prompt_cache_key("conversation-b", "r1")
    assert a and b and a != b


def test_a_call_with_no_conversation_still_gets_a_key_from_its_request() -> None:
    assert cache_guard.provider_prompt_cache_key(None, "r1") == cache_guard.provider_prompt_cache_key(None, "r1")
    assert cache_guard.provider_prompt_cache_key(None, "r1") != cache_guard.provider_prompt_cache_key(None, "r2")
    assert cache_guard.provider_prompt_cache_key(None, None) is None
