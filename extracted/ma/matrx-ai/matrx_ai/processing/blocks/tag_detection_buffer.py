"""
Tag Detection Buffer — prevents text flicker when XML block tags arrive token-by-token.

When the LLM streams `<thinki`, we don't yet know if this becomes `<thinking>`
(a block tag) or `<thinkingly>` (plain text).  Without buffering, the
processor would emit a text block with `<thinki`, then replace it with a
thinking block once the full tag arrives — causing visible flicker in React.

This module detects potential partial XML tags at the tail of the stream buffer
and signals the processor to suppress emission until the tag resolves.

Resolution happens when:
  - The tag closes with `>` → check against known tags
  - A space or newline appears before `>` → not a block tag, resume emission
  - The stream ends or finalizes → emit as text

See streaming-constitution.md Part III — The Detection Buffer.
"""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.block_detector import ATTRIBUTE_XML_BLOCKS, XML_TAG_BLOCKS

_PARTIAL_TAG_RE = re.compile(r'<([a-zA-Z_]\w*)$')

_KNOWN_TAG_NAMES: set[str] = set()
_KNOWN_TAG_PROPER_PREFIXES: set[str] = set()


def _build_tag_sets() -> tuple[set[str], set[str]]:
    """Build two sets from known XML block tags.

    Returns:
        tag_names: Complete tag names (e.g. "thinking", "think", "reasoning")
        proper_prefixes: Substrings that are a prefix of some tag name but
            shorter than the full name.  For "thinking" this is
            {"t", "th", "thi", "thin", "think", "thinki", "thinkin"}.
            "thinking" itself is NOT in this set.

    Suppression logic uses both sets:
        - `<thinki` — "thinki" is a proper prefix → suppress (could become <thinking>)
        - `<think`  — "think" is a full tag name AND also a proper prefix of
          "thinking" → suppress (could become <thinking>)
        - `<thinking` — "thinking" is a full tag name, `>` hasn't arrived yet
          → suppress (wait for closing `>`)
        - `<thinking>` — has `>`, so the regex `<(\\w+)$` won't match → not suppressed
        - `<zebra` — neither a tag name nor a proper prefix → don't suppress
    """
    tag_names: set[str] = set()
    proper_prefixes: set[str] = set()
    for tags in XML_TAG_BLOCKS.values():
        for tag in tags:
            name = tag.strip('<>')
            tag_names.add(name)
            for length in range(1, len(name)):
                proper_prefixes.add(name[:length])
    # Also include attribute-bearing XML block names (e.g. "decision")
    for name in ATTRIBUTE_XML_BLOCKS:
        tag_names.add(name)
        for length in range(1, len(name)):
            proper_prefixes.add(name[:length])
    return tag_names, proper_prefixes


def _ensure_tag_sets() -> None:
    global _KNOWN_TAG_NAMES, _KNOWN_TAG_PROPER_PREFIXES
    if not _KNOWN_TAG_NAMES:
        _KNOWN_TAG_NAMES, _KNOWN_TAG_PROPER_PREFIXES = _build_tag_sets()


class TagDetectionBuffer:
    """Tracks whether the stream buffer tail looks like a partial XML block tag.

    Usage in StreamBlockProcessor:

        self._tag_buffer = TagDetectionBuffer()

        def process_token(self, token: str) -> list[RenderBlockEvent]:
            self._buffer += token
            if self._tag_buffer.should_suppress(self._buffer):
                return []
            return self._detect_and_emit()
    """

    def should_suppress(self, buffer: str) -> bool:
        """Return True if the buffer tail looks like a partial known XML tag.

        Checks the last 30 characters of the buffer for a pattern like
        ``<thinking`` (no closing ``>``) where the tag name could still
        become a known XML block tag with more characters.

        Cases:
        - ``<thinki``  → proper prefix of "thinking" → suppress
        - ``<think``   → exact tag name AND proper prefix of "thinking" → suppress
        - ``<thinking`` → exact tag name (``>`` not yet arrived) → suppress
        - ``<thinking>`` → complete (has ``>``, regex won't match) → don't suppress
        - ``<zebra``   → not a prefix of any known tag → don't suppress
        """
        tail = buffer[-30:] if len(buffer) > 30 else buffer
        match = _PARTIAL_TAG_RE.search(tail)
        if match is None:
            return False

        partial_name = match.group(1)
        _ensure_tag_sets()

        # Suppress if this is a proper prefix (could become a longer tag)
        # OR if it's an exact tag name (the `>` hasn't arrived yet — wait one
        # more character to let the detector see the complete `<tagname>` line).
        if partial_name in _KNOWN_TAG_PROPER_PREFIXES or partial_name in _KNOWN_TAG_NAMES:
            return True

        return False
