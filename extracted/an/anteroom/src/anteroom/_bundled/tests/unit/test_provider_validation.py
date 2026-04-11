"""Tests for provider pre-flight validation rules."""

from __future__ import annotations

import pytest

from anteroom.services.provider_validation import (
    ProviderRequestError,
    _is_anthropic_or_bedrock_route,
    validate_first_message_user,
    validate_not_bedrock_tools_without_confirmation,
)

# ---------------------------------------------------------------------------
# ProviderRequestError
# ---------------------------------------------------------------------------


class TestProviderRequestError:
    def test_to_error_event_shape(self) -> None:
        exc = ProviderRequestError(
            rule_name="test_rule",
            provider="test_provider",
            model="test_model",
            message="something went wrong",
        )
        event = exc.to_error_event()
        assert event["event"] == "error"
        assert event["data"]["message"] == "something went wrong"
        assert event["data"]["code"] == "request_invalid"
        assert event["data"]["retryable"] is False
        assert event["data"]["provider"] == "test_provider"
        assert event["data"]["model"] == "test_model"

    def test_str_returns_message(self) -> None:
        exc = ProviderRequestError(rule_name="r", provider="p", model="m", message="hello")
        assert str(exc) == "hello"

    def test_attributes(self) -> None:
        exc = ProviderRequestError(
            rule_name="my_rule", provider="anthropic", model="claude-sonnet-4-20250514", message="msg"
        )
        assert exc.rule_name == "my_rule"
        assert exc.provider == "anthropic"
        assert exc.model == "claude-sonnet-4-20250514"


# ---------------------------------------------------------------------------
# validate_first_message_user
# ---------------------------------------------------------------------------


class TestValidateFirstMessageUser:
    def test_passes_with_user_first(self) -> None:
        msgs = [{"role": "user", "content": "Hi"}]
        validate_first_message_user(msgs, allow_leading_system=True, provider="p", model="m")

    def test_passes_with_system_then_user(self) -> None:
        msgs = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hi"},
        ]
        validate_first_message_user(msgs, allow_leading_system=True, provider="p", model="m")

    def test_passes_with_multiple_system_then_user(self) -> None:
        msgs = [
            {"role": "system", "content": "Part 1"},
            {"role": "system", "content": "Part 2"},
            {"role": "user", "content": "Hi"},
        ]
        validate_first_message_user(msgs, allow_leading_system=True, provider="p", model="m")

    def test_fails_when_first_non_system_is_assistant(self) -> None:
        msgs = [
            {"role": "system", "content": "sys"},
            {"role": "assistant", "content": "oops"},
        ]
        with pytest.raises(ProviderRequestError) as exc_info:
            validate_first_message_user(msgs, allow_leading_system=True, provider="anthropic", model="claude")
        assert exc_info.value.rule_name == "first_message_must_be_user"
        assert "role='assistant'" in exc_info.value.message
        assert "index 1" in exc_info.value.message

    def test_fails_when_assistant_first_no_system(self) -> None:
        msgs = [{"role": "assistant", "content": "oops"}]
        with pytest.raises(ProviderRequestError) as exc_info:
            validate_first_message_user(msgs, allow_leading_system=True, provider="p", model="m")
        assert "index 0" in exc_info.value.message

    def test_fails_on_empty_messages(self) -> None:
        with pytest.raises(ProviderRequestError) as exc_info:
            validate_first_message_user([], allow_leading_system=True, provider="p", model="m")
        assert "empty or system-only" in exc_info.value.message

    def test_fails_on_system_only_messages(self) -> None:
        msgs = [{"role": "system", "content": "sys"}]
        with pytest.raises(ProviderRequestError) as exc_info:
            validate_first_message_user(msgs, allow_leading_system=True, provider="p", model="m")
        assert "empty or system-only" in exc_info.value.message

    def test_allow_leading_system_false_rejects_system(self) -> None:
        """When allow_leading_system=False (Anthropic converted list),
        a system message at index 0 is treated as a violation."""
        msgs = [{"role": "system", "content": "sys"}, {"role": "user", "content": "hi"}]
        with pytest.raises(ProviderRequestError) as exc_info:
            validate_first_message_user(msgs, allow_leading_system=False, provider="anthropic", model="claude")
        assert "role='system'" in exc_info.value.message

    def test_tool_role_first_fails(self) -> None:
        msgs = [
            {"role": "system", "content": "sys"},
            {"role": "tool", "content": "result", "tool_call_id": "abc"},
        ]
        with pytest.raises(ProviderRequestError):
            validate_first_message_user(msgs, allow_leading_system=True, provider="p", model="m")


# ---------------------------------------------------------------------------
# validate_not_bedrock_tools_without_confirmation
# ---------------------------------------------------------------------------


class TestValidateNotBedrockTools:
    def test_passes_when_no_tools(self) -> None:
        validate_not_bedrock_tools_without_confirmation(
            "bedrock/anthropic.claude-v2", None, confirmed=False, provider="litellm"
        )

    def test_passes_when_tools_empty_list(self) -> None:
        validate_not_bedrock_tools_without_confirmation(
            "bedrock/anthropic.claude-v2", [], confirmed=False, provider="litellm"
        )

    def test_passes_when_not_bedrock_prefix(self) -> None:
        validate_not_bedrock_tools_without_confirmation(
            "openai/gpt-4o",
            [{"type": "function", "function": {"name": "test"}}],
            confirmed=False,
            provider="litellm",
        )

    def test_passes_when_confirmed_true(self) -> None:
        validate_not_bedrock_tools_without_confirmation(
            "bedrock/anthropic.claude-v2",
            [{"type": "function", "function": {"name": "test"}}],
            confirmed=True,
            provider="litellm",
        )

    def test_fails_for_bedrock_slash_prefix_with_tools(self) -> None:
        with pytest.raises(ProviderRequestError) as exc_info:
            validate_not_bedrock_tools_without_confirmation(
                "bedrock/anthropic.claude-v2",
                [{"type": "function", "function": {"name": "test"}}],
                confirmed=False,
                provider="litellm",
            )
        assert exc_info.value.rule_name == "bedrock_tool_route"
        assert "litellm_bedrock_tools_confirmed" in exc_info.value.message

    def test_fails_for_bedrock_dot_prefix(self) -> None:
        with pytest.raises(ProviderRequestError):
            validate_not_bedrock_tools_without_confirmation(
                "bedrock.anthropic.claude-v2",
                [{"type": "function", "function": {"name": "test"}}],
                confirmed=False,
                provider="litellm",
            )

    def test_fails_for_amazon_bedrock_prefix(self) -> None:
        with pytest.raises(ProviderRequestError):
            validate_not_bedrock_tools_without_confirmation(
                "amazon/bedrock/anthropic.claude-v2",
                [{"type": "function", "function": {"name": "test"}}],
                confirmed=False,
                provider="litellm",
            )

    def test_case_insensitive(self) -> None:
        with pytest.raises(ProviderRequestError):
            validate_not_bedrock_tools_without_confirmation(
                "Bedrock/anthropic.claude-v2",
                [{"type": "function", "function": {"name": "test"}}],
                confirmed=False,
                provider="litellm",
            )


# ---------------------------------------------------------------------------
# _is_anthropic_or_bedrock_route
# ---------------------------------------------------------------------------


class TestIsAnthropicOrBedrockRoute:
    def test_anthropic_slash(self) -> None:
        assert _is_anthropic_or_bedrock_route("anthropic/claude-sonnet-4-20250514") is True

    def test_anthropic_dot(self) -> None:
        assert _is_anthropic_or_bedrock_route("anthropic.claude-v2") is True

    def test_bedrock_slash(self) -> None:
        assert _is_anthropic_or_bedrock_route("bedrock/anthropic.claude-v2") is True

    def test_openai_not_matched(self) -> None:
        assert _is_anthropic_or_bedrock_route("openai/gpt-4o") is False

    def test_plain_model_not_matched(self) -> None:
        assert _is_anthropic_or_bedrock_route("gpt-4o") is False

    def test_case_insensitive(self) -> None:
        assert _is_anthropic_or_bedrock_route("Anthropic/claude-sonnet-4-20250514") is True
