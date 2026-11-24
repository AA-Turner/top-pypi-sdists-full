"""The person's own words, echoed on their message's reservation frame.

A turn's rows are committed when the turn settles. A page that reloads
mid-answer rejoins the live NDJSON journal from frame one, and until now the
user ``record_reserved`` frame carried only ``role`` + ``position`` — so the
rejoined transcript knew a user row existed but not what it said, and showed
an empty bubble until the answer finished and the conversation was re-read.

The reservation already holds the pristine ``user_content`` (what the person
authored: their text and attachment references, never the machine template
and never inline bytes — ``TextContent.to_storage_dict`` /
``validate_message_content``). Echoing it on the frame lets every rejoining
client render the real message immediately, from server truth.

Bounded: inline bytes are stripped again here (defense in depth), and an
oversized echo is omitted rather than bloating the replay journal — the client
then shows no row until the turn's own re-read lands, never an empty box.

HONEST ABOUT A FILE STILL MOVING (CGU-10 AND-IMG15 #1). A person's attachment
gets its file id before its bytes reach storage, and the upload runs beside the
provider call — so the echo can name a file that does not exist yet. Such a part
carries ``metadata.attachment_pending`` (a client draws a placeholder, never a
fetch), an attachment whose store already failed is echoed as the marked
stand-in, and :func:`echo_settled_uploads` re-sends the frame (same record id)
as each upload lands or fails: the part then names the stored file, or becomes
the stand-in.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

#: Serialized-size ceiling for the echoed content (bytes of JSON).
MAX_USER_TURN_ECHO_BYTES = 64_000

_INLINE_BYTE_KEYS = frozenset({"base64_data", "base64"})


def _without_inline_bytes(block: Any) -> Any:
    if not isinstance(block, dict):
        return block
    return {k: v for k, v in block.items() if k not in _INLINE_BYTE_KEYS}


#: ``metadata`` key on an echoed media part whose file is still being stored.
PENDING_ATTACHMENT_KEY = "attachment_pending"


def _honest(block: Any) -> Any:
    """The block as a rejoining client may draw it NOW: a part whose upload runs is marked pending,
    a part whose store failed is the marked stand-in, everything else as it is."""
    from matrx_ai.persistence.sealed import (
        person_media_upload_failed,
        person_media_upload_in_flight,
        unavailable_attachment_part,
        upload_failure_type,
    )

    block = _without_inline_bytes(block)
    if not isinstance(block, dict) or block.get("type") != "media":
        return block
    file_id = block.get("file_id")
    if person_media_upload_failed(file_id):
        return unavailable_attachment_part(block, upload_failure_type(file_id))
    if person_media_upload_in_flight(file_id):
        meta = dict(block.get("metadata") or {})
        meta[PENDING_ATTACHMENT_KEY] = {"reason": "uploading"}
        return {**block, "metadata": meta}
    return block


def pending_upload_ids(pristine_user_content: list[Any] | None) -> list[str]:
    """The file ids in the echoed content whose upload is still running, in order, once each."""
    from matrx_ai.persistence.sealed import person_media_upload_in_flight

    seen: list[str] = []
    for block in pristine_user_content or []:
        if isinstance(block, dict) and block.get("type") == "media":
            file_id = str(block.get("file_id") or "")
            if file_id and person_media_upload_in_flight(file_id) and file_id not in seen:
                seen.append(file_id)
    return seen


async def echo_settled_uploads(
    emitter: Any,
    *,
    record_id: str,
    parent_refs: dict[str, str] | None,
    metadata: dict[str, Any],
    pristine_user_content: list[Any],
    file_ids: list[str],
) -> int:
    """Re-send the user row's reservation frame each time one of ``file_ids`` finishes storing (or
    fails): the echo then names the stored file, or the stand-in. Never raises. Returns frames sent."""
    from matrx_connect.context.events import RecordReservedPayload

    from matrx_ai.persistence.sealed import person_media_upload_task

    tasks = [t for t in (person_media_upload_task(f) for f in file_ids) if t is not None]
    sent = 0
    for done in asyncio.as_completed([asyncio.shield(t) for t in tasks]):
        try:
            await done
        except BaseException:  # noqa: BLE001 — the upload captured its own failure; the echo says it
            pass
        await asyncio.sleep(0)  # let the upload's own bookkeeping (``finally``) land first
        echo = user_turn_echo(pristine_user_content)
        if not echo:
            continue
        try:
            await emitter.send_record_reserved(
                RecordReservedPayload(
                    db_project="matrx",
                    table="message",
                    record_id=record_id,
                    parent_refs=parent_refs or {},
                    metadata={**metadata, **echo},
                )
            )
            sent += 1
        except Exception as exc:  # noqa: BLE001 — the stream may be gone; the turn's re-read stands
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                exc,
                kind="user_turn_echo_failed",
                route="user_turn_echo/settled_upload",
                error_type=type(exc).__name__,
                payload={"record_id": record_id},
            )
    return sent


def user_turn_echo(pristine_user_content: list[Any] | None) -> dict[str, Any]:
    """Metadata keys to merge into the user message's reservation frame.

    Returns ``{"user_content": [...]}`` when the authored content is known and
    small enough to journal, else ``{}`` (the frame stays as it was).
    """
    if not pristine_user_content:
        return {}
    blocks = [_honest(b) for b in pristine_user_content]
    try:
        size = len(json.dumps(blocks, default=str).encode("utf-8"))
    except (TypeError, ValueError):
        return {}
    if size > MAX_USER_TURN_ECHO_BYTES:
        return {}
    return {"user_content": blocks}
