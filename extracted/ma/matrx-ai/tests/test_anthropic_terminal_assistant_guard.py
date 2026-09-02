import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import MessageSanitizationError
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile


def _profile():
    return make_profile(model_name="claude-sonnet", wire_format="anthropic_chat")


def test_anthropic_refuses_terminal_assistant_prefill_before_provider_io() -> None:
    config = UnifiedConfig(
        model="claude-sonnet",
        messages=MessageList(
            _messages=[
                UnifiedMessage(role="user", content=[TextContent(text="Question")]),
                UnifiedMessage(role="assistant", content=[TextContent(text="Prefill")]),
            ]
        ),
    )

    with pytest.raises(MessageSanitizationError, match="must end with a user/tool turn"):
        AnthropicTranslator().to_anthropic(config, _profile())


def test_anthropic_accepts_terminal_user_turn() -> None:
    config = UnifiedConfig(
        model="claude-sonnet",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="Question")])]
        ),
    )

    request = AnthropicTranslator().to_anthropic(config, _profile())

    assert request["messages"][-1]["role"] == "user"
