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


def reasoning_opener(content_so_far: str) -> str:
    """The ``<reasoning>`` opener, on its own line.

    Reasoning can arrive AFTER answer text has streamed (gpt-oss interleaves it).
    Sent bare, the opener lands mid-sentence and the one block splitter keeps a
    same-line ``prose <reasoning>…</reasoning>`` span as literal text (its inline
    rule), so the fence printed in the answer (feedback 9f22a41d). The splitter
    fences a region whose opener starts a line, so an opener after text that did
    not end a line gets a newline first.
    """
    if content_so_far and not content_so_far.endswith("\n"):
        return "\n<reasoning>"
    return "<reasoning>"


async def emit_settled_content(emitter: Any, response: Any) -> None:
    """Push a settled (non-streaming) response's text and thought to the live stream.

    The ONE funnel every non-streaming adapter uses. It tracks the answer text
    already sent so a thought that follows answer text gets its opener on its
    own line (``reasoning_opener``) — the same wire rule the streaming paths
    keep. Tool calls are announced by the shared tool loop, never here.

    NEVER raises (cancellation aside): a failing emitter is a display loss, not a lost response.
    """
    from matrx_ai.config.unified_content import TextContent, ThinkingContent

    sent = ""
    try:
        for message in getattr(response, "messages", None) or []:
            for content in getattr(message, "content", None) or []:
                if isinstance(content, ThinkingContent):
                    await emit_complete_reasoning_block(emitter, content.text, content_so_far=sent)
                    if content.text:
                        sent += "\n"
                elif isinstance(content, TextContent) and content.text:
                    await emitter.send_chunk(content.text)
                    sent += content.text
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001 - the live display copy; the response already holds the text
        logger.exception(
            "could not stream the settled response text — it remains on the response "
            "and persists normally; only the live display is lost",
        )


async def emit_complete_reasoning_block(emitter: Any, reasoning: str, *, content_so_far: str) -> None:
    """Emit a balanced, already-complete reasoning block for non-streaming calls.

    ``content_so_far`` is the answer text already sent this turn; the opener
    comes from ``reasoning_opener`` so it always starts a line.

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
        await emitter.send_chunk(reasoning_opener(content_so_far))
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
