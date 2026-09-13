"""Shared reasoning helpers for provider adapters.

OpenAI-compatible vendors have settled on more than one field name for
reasoning text.  Adapters must turn either shape into a ``ThinkingContent``
block in the final ``UnifiedResponse``; emitting the text to the live stream
alone is not durable and loses it during conversation persistence.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)


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
    """Emit a balanced, already-complete reasoning block for non-streaming calls.

    NEVER raises. The provider call already succeeded and its reasoning is
    durable on the ``UnifiedResponse``; this is the live-display copy. A failing
    emitter here used to abort the adapter mid-response at all four call sites
    (together / xai / groq / generic OpenAI), which is the operation-stream
    journal class: a display sink failing the work it merely narrates.
    """
    if not reasoning:
        return
    try:
        await emitter.send_reasoning_state("started")
        await emitter.send_chunk("<reasoning>")
        await emitter.send_chunk(reasoning)
        await emitter.send_chunk("\n</reasoning>\n")
        await emitter.send_reasoning_state("stopped")
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001 - reasoning is already on the response
        logger.exception(
            "could not stream the reasoning block (%d chars) — it remains on the "
            "response and persists normally; only the live display is lost",
            len(reasoning),
        )
