"""Live media framing: no single media ``data`` event outgrows the journal.

Every live media event (``audio_stream_chunk``, a streaming ``media_block``) is
also one frame in the operation-stream journal — the store a reloaded page
rejoins from — whose per-frame bound is a runtime knob
(``operation_stream_queued_bytes``) that may be set as low as 64 KiB. One
oversized frame degrades the journal and breaks every rejoin for that run
(2026-10-01). ``MEDIA_FRAME_MAX_BYTES`` is the ONE raw-byte budget for a media
frame: 32 KiB raw is ~43 KiB base64, under the knob's floor with room for the
envelope.

Two shapes of media, two honest answers:

* **Audio is a stream** — consecutive pieces are meaningful, clients already
  append them by ``seq``. It is SPLIT: ``audio_stream.split_audio_frames``.
* **A partial image is a whole picture** — a slice of a PNG is not an image,
  and no client reassembles image slices on a chat stream. It exists to show
  a low-fidelity preview while the real image renders, so it is DOWNSCALED to
  a preview that fits the budget (``fit_image_preview``). The full-resolution
  image is never framed here: it is persisted and arrives as the final
  ``media_block`` by URL.

Guards: tests/test_audio_stream_chunk_framing.py,
tests/test_partial_image_preview_framing.py.
"""

from __future__ import annotations

import base64
import io
import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

#: Raw bytes in ONE live media frame (~43 KiB once base64-encoded).
MEDIA_FRAME_MAX_BYTES = 32 * 1024

#: Longest-side ladder tried for a preview, largest first, and the JPEG
#: qualities tried at each. A gpt-image partial is 1024-1536 px; 512 px at
#: q70 is typically 25-40 KiB.
_PREVIEW_SIDES = (640, 512, 384, 256, 192, 128)
_PREVIEW_QUALITIES = (72, 55)


def fit_image_preview(
    b64: str, *, mime_type: str = "image/png", max_bytes: int = MEDIA_FRAME_MAX_BYTES
) -> tuple[str, str] | None:
    """A base64 preview of ``b64`` whose raw size is at most ``max_bytes``.

    Returns ``(base64, mime_type)``: the input unchanged when it already fits,
    else a downscaled JPEG. Returns None when no preview fits or the bytes are
    not a decodable image — the caller skips that partial (a preview is
    optional; the final image still arrives) and says so.

    CPU-bound (PIL decode + re-encode ladder): an async caller runs it in a
    worker thread (``asyncio.to_thread``), never on the event loop.
    """
    try:
        raw = base64.b64decode(b64, validate=False)
    except (ValueError, TypeError):
        logger.warning("partial image preview: base64 did not decode — preview skipped")
        return None
    if len(raw) <= max_bytes:
        return b64, mime_type
    try:
        from PIL import Image

        with Image.open(io.BytesIO(raw)) as opened:
            source = opened.convert("RGB")
    except Exception:  # noqa: BLE001 — an undecodable partial is skipped, never fatal
        logger.warning(
            "partial image preview: %d-byte %s did not decode as an image — preview skipped",
            len(raw),
            mime_type,
            exc_info=True,
        )
        return None
    for side in _PREVIEW_SIDES:
        preview = source.copy()
        preview.thumbnail((side, side))
        for quality in _PREVIEW_QUALITIES:
            out = io.BytesIO()
            preview.save(out, format="JPEG", quality=quality, optimize=True)
            data = out.getvalue()
            if len(data) <= max_bytes:
                return base64.b64encode(data).decode("ascii"), "image/jpeg"
    logger.warning(
        "partial image preview: no %d px+ preview of a %d-byte image fits %d bytes — preview skipped",
        _PREVIEW_SIDES[-1],
        len(raw),
        max_bytes,
    )
    return None


#: Serialized bytes of ONE live media event whose payload is metadata, not
#: media (a final ``media_block``): under the journal's 64 KiB floor with room
#: for the envelope.
MEDIA_EVENT_MAX_BYTES = 48 * 1024


def fit_live_metadata(
    metadata: dict[str, Any],
    *,
    size_of: Callable[[dict[str, Any]], int],
    droppable: tuple[str, ...],
    max_bytes: int = MEDIA_EVENT_MAX_BYTES,
) -> dict[str, Any]:
    """The metadata a LIVE media event may carry: ``metadata`` shed of the
    ``droppable`` keys, in order, until ``size_of`` the event fits ``max_bytes``.

    The persisted record keeps everything — this trims only the live frame (a
    reload reads the full record). Shed keys are named on the event as
    ``live_omitted`` and logged; an event still oversized after every droppable
    key is logged as an error, never silently sent as if it fitted.
    """
    live = dict(metadata)
    omitted: list[str] = []
    for key in droppable:
        if size_of(live) <= max_bytes:
            break
        if key in live:
            live.pop(key)
            omitted.append(key)
            live["live_omitted"] = list(omitted)
    if omitted:
        logger.warning(
            "live media event: shed %s to fit the %d-byte journal frame; the persisted "
            "record keeps them",
            ", ".join(omitted),
            max_bytes,
        )
    size = size_of(live)
    if size > max_bytes:
        logger.error(
            "live media event is still %d bytes after shedding %s (limit %d) — it will "
            "degrade the stream journal; add the heavy key to `droppable`",
            size,
            omitted or "nothing",
            max_bytes,
        )
    return live


#: Metadata keys a live media block sheds first, heaviest first: the per-word
#: timeline, then the performed script. Both stay on the persisted part.
LIVE_DROPPABLE_METADATA = ("alignment", "speech_script")


def fitted_media_block(
    record: dict[str, Any],
    *,
    url_set: dict[str, Any] | None = None,
    kind_override: str | None = None,
) -> Any:
    """THE live ``media_block`` event for a persisted file record.

    Carries the record's metadata (so live and reload render alike) shed of
    :data:`LIVE_DROPPABLE_METADATA` only when the event would outgrow the
    journal frame (:func:`fit_live_metadata`). Every adapter emitting a final
    audio/image block for a stored file builds it here.
    """
    from matrx_connect.context.data_types import MediaBlockData
    from matrx_connect.context.media_block import cloud_file_to_media_block

    def _event(metadata: dict[str, Any]) -> MediaBlockData:
        return MediaBlockData(
            block=cloud_file_to_media_block(
                {**record, "metadata": metadata}, url_set=url_set, kind_override=kind_override
            )
        )

    live = fit_live_metadata(
        dict(record.get("metadata") or {}),
        size_of=lambda m: len(_event(m).model_dump_json().encode()),
        droppable=LIVE_DROPPABLE_METADATA,
    )
    return _event(live)


__all__ = [
    "LIVE_DROPPABLE_METADATA",
    "MEDIA_EVENT_MAX_BYTES",
    "MEDIA_FRAME_MAX_BYTES",
    "fit_image_preview",
    "fit_live_metadata",
    "fitted_media_block",
]
