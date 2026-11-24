"""Turning streaming on for a long answer is the provider doing its job — never a warning in the person's chat.

Live 2026-10-19: a woken agent turn (non-streaming, max_tokens 32,000) printed "Your token limit (32,000) exceeds
the maximum allowed without streaming…" in yellow on every model call. The override stays logged and captured for
operators; the chat stays clean.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

from matrx_ai.providers.anthropic import anthropic_api


def test_the_auto_streaming_override_sends_nothing_to_the_chat() -> None:
    source = stable_source(anthropic_api)
    start = source.index("anthropic_requires_streaming(str(config_data")
    override = source[start : source.index("stream_requested = True", start)]
    assert "send_warning" not in override, "the auto-streaming override must not warn the person"
    assert "Streaming was enabled automatically" not in source
