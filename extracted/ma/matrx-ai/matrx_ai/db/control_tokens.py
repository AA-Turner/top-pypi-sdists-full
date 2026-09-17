"""CONTROL TOKENS AT THE PERSISTENCE SEAM — the durable row is cleaned too.

The streaming emitter strips a DECLARED machine line (``WRAP_RATING: 4``) out of
the visible text and re-emits it as a structured ``control_token`` event
(``matrx_connect/emitters/control_tokens.py``). That owns the WIRE. The durable
``cx_message`` row is written from the provider's ``UnifiedResponse``, not from
the emitter — so until this module existed, a person saw clean text while the
stored assistant message still carried the line, and every consumer that later
reads the conversation (a rebuild sent back to the provider, a transcript, an
export) got the raw token back. The vision-interview room repaired its own rows;
every other mandate did not.

🚨 **One registry, every seam.** The emitter cleans the stream; this cleans the
row at all three write paths — the executor's mid-loop checkpoint,
``persist_completed_request``, and the native ConversationRunner's
``append_turn`` — all from ``CONTROL_TOKEN_REGISTRY``. Never a second matcher,
never a regex in a writer.

Two rules that make this safe for the consumers that WANT their tokens:

1. Only the ASSISTANT text a model wrote is cleaned. A user's own message is
   never touched, whatever it happens to contain.
2. The value is never lost — it lands on the row as structured message metadata
   under ``control_tokens``, the same ``name`` / ``value`` / ``declared_by``
   shape the stream event carries. Consumers that parse their own tokens (the
   masterworks bench harness, rag_kinds' ``USED:`` citations) read the RAW
   ``UnifiedResponse`` in their own process, or this metadata — never the
   cleaned text. That is why ``filter_enabled=False`` does not exempt a token
   here: it declares "leave it in the STREAM for a machine-only transcript",
   and a stored row is not that transcript.
"""

from __future__ import annotations

from typing import Any

from matrx_connect.emitters.control_tokens import (
    ControlTokenHit,
    ControlTokenRegistry,
    strip_control_tokens,
)

#: Where the stripped values live on ``cx_message.metadata``.
CONTROL_TOKEN_METADATA_KEY = "control_tokens"

__all__ = [
    "CONTROL_TOKEN_METADATA_KEY",
    "clean_assistant_content",
    "control_token_metadata",
    "merge_control_token_metadata",
]


def clean_assistant_content(
    content: Any,
    *,
    registry: ControlTokenRegistry | None = None,
) -> tuple[Any, tuple[ControlTokenHit, ...]]:
    """Storage content blocks with every declared control line removed.

    Returns ``(content, hits)``. ``content`` is returned UNCHANGED (same object)
    when nothing matched, so the overwhelmingly common turn pays one scan and no
    allocation. A text block whose whole body WAS the control line is dropped:
    an empty text block is rejected by providers when the conversation is rebuilt
    and sent back, so leaving one behind would trade a visible leak for a 400.
    """
    if not isinstance(content, list) or not content:
        return content, ()

    hits: list[ControlTokenHit] = []
    cleaned: list[Any] = []
    changed = False
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "text":
            cleaned.append(block)
            continue
        text = block.get("text")
        if not isinstance(text, str) or not text:
            cleaned.append(block)
            continue
        filtered = strip_control_tokens(text, registry=registry)
        if not filtered.found:
            cleaned.append(block)
            continue
        changed = True
        hits.extend(filtered.hits)
        if not filtered.text.strip():
            # The block held nothing but the machine line — drop it whole.
            continue
        new_block = dict(block)
        new_block["text"] = filtered.text
        cleaned.append(new_block)

    if not changed:
        return content, ()
    return cleaned, tuple(hits)


def control_token_metadata(hits: tuple[ControlTokenHit, ...]) -> list[dict[str, str]]:
    """The stream event's shape, as it is stored: name / value / declared_by."""
    return [
        {"name": hit.name, "value": hit.value, "declared_by": hit.declared_by}
        for hit in hits
    ]


def merge_control_token_metadata(
    metadata: dict[str, Any] | None,
    hits: tuple[ControlTokenHit, ...],
) -> dict[str, Any] | None:
    """Add ``hits`` to a message's metadata under ``control_tokens``.

    Idempotent by ``(name, value)``: the mid-loop flush and the end-of-loop
    persist can both run against the same row without recording a value twice.
    """
    if not hits:
        return metadata
    merged: dict[str, Any] = dict(metadata) if isinstance(metadata, dict) else {}
    existing = merged.get(CONTROL_TOKEN_METADATA_KEY)
    rows: list[dict[str, str]] = [r for r in existing if isinstance(r, dict)] if isinstance(existing, list) else []
    seen = {(str(r.get("name")), str(r.get("value"))) for r in rows}
    for row in control_token_metadata(hits):
        key = (row["name"], row["value"])
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)
    merged[CONTROL_TOKEN_METADATA_KEY] = rows
    return merged
