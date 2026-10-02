"""A partial image never reaches the stream as one oversized data event.

Break named (census 2026-10-01): the OpenAI gpt-image streaming path forwarded
each provider partial as a ``media_block`` carrying the FULL-resolution PNG in
base64 (1-3 MB). Every data event is also one operation-stream journal frame,
whose per-frame bound may be set as low as 64 KiB; one such frame degrades the
journal and breaks rejoin — the class ``split_audio_frames`` closed for audio.

A slice of a PNG is not an image, so the honest framing is a PREVIEW: the
partial is downscaled to fit ``MEDIA_FRAME_MAX_BYTES`` (the final image still
arrives by URL).

SUT: ``OpenAIImageGeneration._emit_partial_image`` (+ ``fit_image_preview``).
Double: the emitter (records what reaches the wire).

Forcing: a 1024 px partial leaves as ONE event under the journal floor that
decodes to a real image of the same aspect, at most 640 px; a partial already
under budget leaves byte-identical as PNG; an undecodable oversized partial is
skipped, never sent.
"""

from __future__ import annotations

import asyncio
import base64
import io
import random
from typing import Any

import pytest
from PIL import Image

from matrx_ai.providers.media_frames import MEDIA_FRAME_MAX_BYTES
from matrx_ai.providers.openai.openai_image_api import OpenAIImageGeneration

_JOURNAL_MIN_QUEUED_BYTES = 65536


class _Wire:
    def __init__(self) -> None:
        self.frames: list[Any] = []

    async def send_data(self, payload: Any) -> None:
        self.frames.append(payload)


def _render(width: int, height: int, seed: int) -> str:
    """A noisy render — the worst case for compression, so the biggest partial."""
    rng = random.Random(seed)
    img = Image.new("RGB", (width, height))
    img.putdata([(rng.randrange(256), rng.randrange(256), (x * 3) % 256) for x in range(width * height)])
    out = io.BytesIO()
    img.save(out, format="PNG")
    return base64.b64encode(out.getvalue()).decode("ascii")


@pytest.mark.parametrize(
    ("width", "height", "expect_mime", "expect_unchanged"),
    [(1024, 1536, "image/jpeg", False), (48, 32, "image/png", True)],
    ids=["full-res-portrait-partial", "already-small-partial"],
)
def test_partial_leaves_as_one_bounded_preview(width: int, height: int, expect_mime: str, expect_unchanged: bool) -> None:
    original = _render(width, height, seed=width)
    wire = _Wire()
    sent = asyncio.run(OpenAIImageGeneration._emit_partial_image(wire, original, 2))

    assert sent is True
    assert len(wire.frames) == 1
    frame = wire.frames[0]
    assert len(frame.model_dump_json().encode()) < _JOURNAL_MIN_QUEUED_BYTES
    block = frame.block
    assert block.status == "streaming" and block.progress == 0.5
    assert block.mime_type == expect_mime
    raw = base64.b64decode(block.base64)
    assert len(raw) <= MEDIA_FRAME_MAX_BYTES
    assert (block.base64 == original) is expect_unchanged
    with Image.open(io.BytesIO(raw)) as preview:
        if expect_unchanged:
            assert preview.size == (width, height)
        else:
            assert max(preview.size) <= 640
        # Same picture, same shape: aspect ratio survives the downscale.
        assert abs(preview.size[0] / preview.size[1] - width / height) < 0.02


def test_an_oversized_partial_that_is_not_an_image_is_skipped_never_sent() -> None:
    junk = base64.b64encode(bytes(range(256)) * 400).decode("ascii")  # 100 KB, not an image
    wire = _Wire()
    sent = asyncio.run(OpenAIImageGeneration._emit_partial_image(wire, junk, 1))
    assert sent is False
    assert wire.frames == []
