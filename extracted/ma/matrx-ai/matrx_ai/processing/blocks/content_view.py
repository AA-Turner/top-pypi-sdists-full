"""``content_from_text`` — an agent's final text as a LIST OF KIND INSTANCES.

The agent output contract (plan of record
``common-docs/systems/content-ir-system/KINDS_EVERYWHERE_PLAN.md`` §6, designed
with Arman 2026-08-20): a message's content is ALWAYS a list of typed
instances, one element in the simple case — Anthropic's own content-block
model, applied to our kinds. This module produces that list from a COMPLETE
final text, reusing the exact detection pipeline chat already runs
(``process_complete_to_blocks``) — never a second parser.

Mapping, per complete block, in document order:

1. **Envelope-stamped block** (``metadata.__ir`` — the detector recognized a
   registered kind and VALIDATED the value): the envelope's value, guaranteed
   to carry ``__kind``.
2. **Text block**: a ``markdown`` instance ``{"__kind": "markdown", "text": …}``.
3. **JSON code fence whose body already carries ``__kind``**: the body as-is —
   a self-described instance. It is NOT validated here (this mapper is sync
   and pure); the kind gates downstream (node settlement, ingestion, render
   trust) hold the line, exactly as they do for any self-described payload.
4. **Everything else** (unstamped XML, plain code, images, tables): folded
   back into the surrounding markdown — ZERO data loss, nothing invented. A
   block that could not be named stays prose rather than gaining a fake name.

Consecutive markdown segments merge, so pure prose yields exactly ONE
element — the 99% case pays nothing.
"""

from __future__ import annotations

import json
from typing import Any

from matrx_ai.processing.blocks.envelope import IR_ENVELOPE_KEY
from matrx_ai.processing.blocks.stream_processor import process_complete_to_blocks

__all__ = ["content_from_text", "MARKDOWN_KIND"]

MARKDOWN_KIND = "markdown"


def _markdown_instance(text: str) -> dict[str, Any]:
    return {"__kind": MARKDOWN_KIND, "text": text}


def _envelope_value(block: dict[str, Any]) -> dict[str, Any] | None:
    """The validated kind instance from a stamped envelope, if one is present.

    🚨 THE KIND LIVES ON ``root``, not at the top level. The envelope this
    reads is built by ``envelope_for_block`` → ``_assemble`` and its shape is
    ``{v, engine, fingerprint, root: {kind, kindState, value, …}}``. This
    reader looked for ``envelope["kind"]``, which is ALWAYS absent — so it
    returned None for every stamped block that ever existed, and the §6
    content channel could not name a single validated kind. Every agent
    answer containing a recognized quiz / flashcard set / presentation was
    folded into markdown prose and reached the reader as a wall of raw JSON
    (Arman's run a268ba41, 2026-08-22; reproduced against the live producer).

    The top level is still accepted as a fallback so a producer that stamps
    it there is not broken by this fix — but ``root`` is the contract.
    """
    metadata = block.get("metadata")
    if not isinstance(metadata, dict):
        return None
    envelope = metadata.get(IR_ENVELOPE_KEY)
    if not isinstance(envelope, dict):
        return None
    root = envelope.get("root")
    kind = (root.get("kind") if isinstance(root, dict) else None) or envelope.get("kind")
    value = root.get("value") if isinstance(root, dict) else None
    if not isinstance(kind, str) or not kind or not isinstance(value, dict):
        return None
    # Round-1 F11 (mirror of round-2 W1): the VALIDATED envelope's kind wins
    # over whatever inner marker the unvalidated payload carries — one
    # region, one designated renderer.
    if value.get("__kind") != kind:
        value = {**value, "__kind": kind}
    return value


def _self_described_json(block: dict[str, Any]) -> dict[str, Any] | None:
    """A JSON fence whose body carries its own ``__kind`` discriminator."""
    data = block.get("data")
    language = (data or {}).get("language") if isinstance(data, dict) else None
    if block.get("type") != "code" or language != "json":
        return None
    body = (data or {}).get("code") or block.get("content") or ""
    try:
        parsed = json.loads(body)
    except (TypeError, ValueError):
        return None
    if isinstance(parsed, dict) and isinstance(parsed.get("__kind"), str) and parsed["__kind"]:
        return parsed
    return None


def _is_json_document(raw: str) -> bool:
    """True when this body is a JSON object/array, so folding it must fence."""
    stripped = raw.strip()
    if not stripped or stripped[0] not in "{[":
        return False
    try:
        json.loads(stripped)
    except (TypeError, ValueError):
        return False
    return True


def content_from_text(text: str) -> list[dict[str, Any]]:
    """Parse a COMPLETE final text into the ordered kind-instance list."""
    if not text or not text.strip():
        return []

    instances: list[dict[str, Any]] = []
    prose: list[str] = []

    def flush_prose() -> None:
        joined = "\n".join(segment for segment in prose if segment.strip())
        prose.clear()
        if joined.strip():
            instances.append(_markdown_instance(joined))

    for block in process_complete_to_blocks(text):
        stamped = _envelope_value(block)
        if stamped is not None:
            flush_prose()
            instances.append(stamped)
            continue
        described = _self_described_json(block)
        if described is not None:
            flush_prose()
            instances.append(described)
            continue
        if block.get("type") == "text":
            prose.append(str(block.get("content") or ""))
            continue
        # Unnamed structure (plain code, unstamped XML, tables, media
        # references): keep its SOURCE inside the prose stream — zero data
        # loss, no fake identity. It re-fences, because the detector stripped
        # the markers on the way in.
        #
        # 🚨 The re-fence covers ANY block whose body is a JSON document, not
        # just `type == "code"`. A recognized structured block that could not
        # be NAMED — a cold catalog, an unregistered kind, a schema that did
        # not validate — arrives here as e.g. `type: "quiz"`, and folding its
        # body in bare dumped a wall of naked JSON into the middle of the
        # reader's prose (measured on run a268ba41, 2026-08-22). Fenced, the
        # worst case is a collapsed code block instead of soup.
        raw = block.get("content")
        if isinstance(raw, str) and raw.strip():
            data = block.get("data")
            language = (data or {}).get("language") if isinstance(data, dict) else None
            if block.get("type") == "code":
                prose.append(f"```{language or ''}\n{raw}\n```")
            elif _is_json_document(raw):
                prose.append(f"```{language or 'json'}\n{raw}\n```")
            else:
                prose.append(raw)
    flush_prose()
    return instances
