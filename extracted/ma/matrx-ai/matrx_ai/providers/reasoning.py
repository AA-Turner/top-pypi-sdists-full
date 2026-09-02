"""Shared reasoning helpers for provider adapters.

OpenAI-compatible vendors have settled on more than one field name for
reasoning text.  Adapters must turn either shape into a ``ThinkingContent``
block in the final ``UnifiedResponse``; emitting the text to the live stream
alone is not durable and loses it during conversation persistence.
"""

from __future__ import annotations

from typing import Any


def openai_compatible_reasoning_text(payload: Any) -> str | None:
    """Return provider reasoning text from a chat-completions delta/message.

    ``reasoning_content`` is used by Moonshot and Together.  Groq reasoning
    models use ``reasoning`` on some OpenAI-compatible responses.  Ignore
    non-text values so a vendor extension cannot become accidental user text.
    """
    for field_name in ("reasoning_content", "reasoning"):
        value = (
            payload.get(field_name)
            if isinstance(payload, dict)
            else getattr(payload, field_name, None)
        )
        if isinstance(value, str) and value:
            return value
    return None


async def emit_complete_reasoning_block(emitter: Any, reasoning: str) -> None:
    """Emit a balanced, already-complete reasoning block for non-streaming calls."""
    if not reasoning:
        return
    await emitter.send_reasoning_state("started")
    await emitter.send_chunk("<reasoning>")
    await emitter.send_chunk(reasoning)
    await emitter.send_chunk("\n</reasoning>\n")
    await emitter.send_reasoning_state("stopped")
