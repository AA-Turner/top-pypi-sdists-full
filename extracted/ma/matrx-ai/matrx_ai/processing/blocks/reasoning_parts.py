"""Inline reasoning becomes its own thinking part — the one lift for every text the stream wrote.

The providers stream a model's thought INLINE on the text channel (``<reasoning>…</reasoning>`` at the
front of the chunks; ``providers/reasoning.py``), so the emitter's turn text carries the tag. A finished
turn never saves that text: the provider builds its response from the native reasoning field, so the row
holds a separate ``thinking`` part and a clean ``text`` part. Every turn saved FROM the streamed text — a
stopped partial, a provider that failed mid-stream (often iteration 1 thinking before a tool call), an
interrupt, a late Stop's cut — must be saved in that same shape. Before this, those rows kept the tag in
one text part (AND-V 05r F6: 2,119 stopped rows and 21 others in four days), and every reader that was
not a renderer (copy, export, search, history read by agents) got the thought as answer text.

The regions are found by the server's ONE splitter (:func:`split_blocks_v1`): a ``reasoning`` block —
``<think>`` / ``<thinking>`` / ``<reasoning>`` opening a line, closed or still open — becomes a
:class:`ThinkingContent` with the region's body; everything else stays text, byte for byte, apart from
the line breaks that only separated it from a region.
"""

from __future__ import annotations

from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.processing.blocks.blocks_v1 import split_blocks_v1
from matrx_ai.processing.blocks.tag_detection_buffer import TagDetectionBuffer


def inline_reasoning_parts(text: str) -> list[TextContent | ThinkingContent]:
    """The parts a streamed ``text`` is saved as: each reasoning region its own thinking part, in order.

    Text with no region comes back as one text part, unchanged. Whitespace-only text yields no parts."""
    if not text.strip():
        return []
    blocks = split_blocks_v1(text)
    if not any(b.type == "reasoning" for b in blocks):
        return [TextContent(text=text)]
    raw = text.encode("utf-8")
    segments: list[tuple[bool, str]] = []  # (is_thought, text), in order
    for block in blocks:
        if block.type == "reasoning":
            body_start = int(block.fields.get("body_start", block.start))
            body_end = int(block.fields.get("body_end", block.end))
            segments.append((True, raw[body_start:body_end].decode("utf-8", errors="replace").strip()))
        elif segments and not segments[-1][0]:
            segments[-1] = (False, segments[-1][1] + raw[block.start : block.end].decode("utf-8", errors="replace"))
        else:
            segments.append((False, raw[block.start : block.end].decode("utf-8", errors="replace")))
    parts: list[TextContent | ThinkingContent] = []
    for index, (is_thought, value) in enumerate(segments):
        if is_thought:
            if value:
                parts.append(ThinkingContent(text=value))
            continue
        # Only the line breaks that separated this text from a region go; the rest stays as streamed.
        if index > 0:
            value = value.lstrip("\n")
        if index < len(segments) - 1:
            value = value.rstrip("\n")
        if value.strip():
            parts.append(TextContent(text=value))
    return parts


def inline_reply_text(text: str) -> str:
    """The words a PERSON is told from a streamed ``text``: every reasoning region removed.

    Every reader that hands the streamed text to a person or a caller as the reply (an SMS, a spoken
    voice line, the first words before a tool, a scheduled run's summary) reads it through this, never
    the raw chunks: the providers stream the model's thought inline on the text channel."""
    return "\n\n".join(p.text for p in inline_reasoning_parts(text) if isinstance(p, TextContent))


class InlineReplyStream:
    """:func:`inline_reply_text` for a door that forwards text AS it streams (voice).

    ``feed(chunk)`` returns only the newly visible reply text: an open reasoning region is held back
    until it closes, and a tail that may still become a reasoning opener (``<reaso``) waits a chunk."""

    __slots__ = ("_raw", "_sent", "_tags")

    def __init__(self) -> None:
        self._raw = ""
        self._sent = ""
        self._tags = TagDetectionBuffer()

    def feed(self, chunk: str) -> str:
        self._raw += chunk
        if self._tags.should_suppress(self._raw):
            return ""
        return self._advance(self._visible())

    def flush(self) -> str:
        return self._advance(self._visible())

    def _visible(self) -> str:
        # No tag anywhere: nothing to split (the per-token path of a plain reply stays linear).
        return self._raw if "<" not in self._raw else inline_reply_text(self._raw)

    def _advance(self, visible: str) -> str:
        if not visible.startswith(self._sent):
            return ""  # only separator whitespace moved; the next words carry it
        new = visible[len(self._sent) :]
        self._sent = visible
        return new


__all__ = ["InlineReplyStream", "inline_reasoning_parts", "inline_reply_text"]
