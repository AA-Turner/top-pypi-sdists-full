"""Turning streaming on for a long answer is the provider doing its job — never a warning in the person's chat.

Live 2026-10-19: a woken agent turn (non-streaming, max_tokens 32,000) printed "Your token limit (32,000) exceeds
the maximum allowed without streaming…" in yellow on every model call. The override stays logged and captured for
operators; the chat stays clean.
"""

from __future__ import annotations

import inspect

from matrx_ai.providers.anthropic import anthropic_api


def test_the_auto_streaming_override_sends_nothing_to_the_chat() -> None:
    source = inspect.getsource(anthropic_api)
    block = source[source.index("_ANTHROPIC_NONSTREAMING_MAX_TOKENS:\n"):] if "_ANTHROPIC_NONSTREAMING_MAX_TOKENS:\n" in source else source
    override = block[: block.index("capture_issue(") + 400]
    assert "send_warning" not in override, "the auto-streaming override must not warn the person"
    assert "Streaming was enabled automatically" not in source
