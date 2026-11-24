from __future__ import annotations

import pytest

from matrx_ai.config.message_config import (
    MessageList,
    MessageSanitizationError,
    UnifiedMessage,
)
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent


def _agent_definition() -> dict[str, object]:
    return {
        "model": "test-model",
        "messages": [
            {
                "role": "system",
                "content": [{"type": "text", "text": "Operate autonomously."}],
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": ""}],
            },
        ],
    }


def test_config_hydration_allows_empty_runtime_input_placeholder() -> None:
    config = UnifiedConfig.from_dict(_agent_definition())

    assert config.resolved_system_instruction is not None
    assert "Operate autonomously." in config.resolved_system_instruction
    assert list(config.messages) == []


def test_runtime_input_resolves_deferred_empty_placeholder() -> None:
    config = UnifiedConfig.from_dict(_agent_definition())

    config.append_or_extend_user_input("Run the requested system test.")
    config.messages.sanitize()

    assert len(config.messages) == 1
    content = config.messages[0].content
    assert len(content) == 1
    assert isinstance(content[0], TextContent)
    assert content[0].text == "Run the requested system test."


def test_provider_bound_sanitize_rejects_unfilled_placeholder() -> None:
    config = UnifiedConfig.from_dict(_agent_definition())

    with pytest.raises(MessageSanitizationError, match="emptying_pass=empty_scrub"):
        config.messages.sanitize()


def test_deferred_failure_survives_repeated_hydration_sanitization() -> None:
    config = UnifiedConfig.from_dict(_agent_definition())

    config.messages.sanitize(allow_empty=True)

    with pytest.raises(MessageSanitizationError, match="emptying_pass=empty_scrub"):
        config.messages.sanitize()


def test_message_list_strict_mode_remains_the_default() -> None:
    messages = MessageList([{"role": "user", "content": [{"type": "text", "text": ""}]}])

    with pytest.raises(MessageSanitizationError, match="emptying_pass=empty_scrub"):
        messages.sanitize()


def test_hydration_defers_visibility_collapse_but_strict_mode_rejects_it() -> None:
    messages = MessageList(
        [
            UnifiedMessage(
                role="assistant",
                content=[TextContent(text="failed output")],
                is_visible_to_model=False,
            )
        ]
    )

    messages.sanitize(allow_empty=True)

    with pytest.raises(MessageSanitizationError, match="emptying_pass=model_visibility"):
        messages.sanitize()


def _capture_sanitize_warnings(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    import matrx_ai.config.message_config as message_config

    seen: list[str] = []
    real = message_config.vcprint

    def _spy(data=None, *args, **kwargs):
        if isinstance(data, str) and data.startswith("[MessageList.sanitize]"):
            seen.append(data)
        return real(data, *args, **kwargs)

    monkeypatch.setattr(message_config, "vcprint", _spy)
    return seen


def test_hydrating_the_authored_blank_placeholder_logs_no_warning(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """2026-11-17: every export/preview of an agent with the stored blank user turn wrote two
    false WARNINGs to app_log ("Dropped message…", "Deferred empty-conversation…"). The blank
    placeholder is the documented legitimate case: quiet at hydration, still refused strictly."""
    seen = _capture_sanitize_warnings(monkeypatch)

    config = UnifiedConfig.from_dict(_agent_definition())
    config.messages.sanitize(allow_empty=True)

    assert seen == []
    with pytest.raises(MessageSanitizationError, match="emptying_pass=empty_scrub"):
        config.messages.sanitize()


def test_hydration_still_warns_when_real_content_is_dropped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _capture_sanitize_warnings(monkeypatch)
    messages = MessageList(
        [
            UnifiedMessage(
                role="assistant",
                content=[TextContent(text="failed output")],
                is_visible_to_model=False,
            )
        ]
    )

    messages.sanitize(allow_empty=True)

    assert any("Deferred empty-conversation failure" in line for line in seen)
