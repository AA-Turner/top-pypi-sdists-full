"""BaseTranslator.build_request — the single validated entry for ALL providers.

Two guarantees:
1. ABC enforcement — a translator that forgets `_assemble_request` cannot be
   instantiated (TypeError). A new provider can't silently skip the chokepoint.
2. build_request runs the provider-agnostic critical validations
   (MessageList.sanitize → duplicate-tool_result dedup) BEFORE handing off to
   the provider's assembly — so the duplicate-tool_result 400 is now caught for
   EVERY provider, not just Anthropic, even on the replace()/deepcopy() config
   paths that bypass UnifiedConfig.__post_init__.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.cerebras.translator import CerebrasTranslator
from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
from matrx_ai.providers.groq.translator import GroqTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.providers.together.translator import TogetherTranslator
from matrx_ai.testing.profile_factory import make_profile


def test_missing_assemble_request_cannot_instantiate():
    """The 'spanking' — forget the contract hook and Python refuses to build it."""

    class _BadTranslator(BaseTranslator):
        pass  # no _assemble_request

    with pytest.raises(TypeError):
        _BadTranslator()


def test_every_real_translator_implements_the_hook():
    for cls in (
        AnthropicTranslator,
        OpenAITranslator,
        GroqTranslator,
        CerebrasTranslator,
        TogetherTranslator,
        GenericOpenAITranslator,
    ):
        t = cls()  # must not raise
        assert hasattr(t, "_assemble_request")
        assert hasattr(t, "build_request")


class _SpyTranslator(BaseTranslator):
    """Returns the (already-sanitized) config so we can inspect what assembly
    would have received — provider-agnostic, no payload-shape coupling."""

    def _assemble_request(self, config, api_class=""):
        return config


def _dup_config() -> UnifiedConfig:
    config = UnifiedConfig(
        model="m",
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="X", name="t", arguments={})],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="X", call_id="X", name="t", content="r")],
            ),
        ],
    )
    # __post_init__ already sanitized (one result). Now inject a duplicate AFTER
    # construction — the replace()/deepcopy() shape that skips __post_init__.
    config.messages._messages.append(
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="X", call_id="X", name="t", content="r")],
        )
    )
    return config


def test_build_request_dedups_before_assembly_provider_agnostic():
    config = _dup_config()
    # Sanity: the duplicate is really there pre-build.
    pre = [
        c
        for m in config.messages
        for c in m.content
        if isinstance(c, ToolResultContent) and (c.tool_use_id or c.call_id) == "X"
    ]
    assert len(pre) == 2

    sanitized = _SpyTranslator().build_request(config)

    post = [
        c
        for m in sanitized.messages
        for c in m.content
        if isinstance(c, ToolResultContent) and (c.tool_use_id or c.call_id) == "X"
    ]
    assert len(post) == 1, "build_request must dedup tool_result for ANY provider"


def _anthropic_tool_results(payload, tid):
    return [
        b
        for m in payload["messages"]
        for b in m["content"]
        if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") == tid
    ]


def test_build_request_strips_duplicate_for_anthropic_payload():
    payload = AnthropicTranslator().build_request(
        _dup_config(), make_profile(model_name="m", wire_format="anthropic_chat")
    )
    assert len(_anthropic_tool_results(payload, "X")) == 1


def test_build_request_matches_direct_assembly_for_simple_config():
    """For a no-tool config (sanitize is a no-op), build_request must produce the
    same payload as the provider's own builder — proof the delegation is faithful."""
    def _simple():
        return UnifiedConfig(
            model="claude-x",
            messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
        )

    openai_profile = make_profile(model_name="claude-x", wire_format="openai_chat")
    assert (
        OpenAITranslator().build_request(_simple(), openai_profile)
        == OpenAITranslator().to_openai(_simple(), openai_profile)
    )
    anthropic_profile = make_profile(model_name="claude-x", wire_format="anthropic_chat")
    assert (
        AnthropicTranslator().build_request(_simple(), anthropic_profile)
        == AnthropicTranslator().to_anthropic(_simple(), anthropic_profile)
    )
    together_profile = make_profile(model_name="claude-x", wire_format="together_chat")
    assert (
        TogetherTranslator().build_request(_simple(), together_profile)
        == TogetherTranslator().to_together(_simple(), together_profile)
    )
