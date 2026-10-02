"""Downscaling a partial-image preview never runs on the event loop.

Break named (2026-10-01 review): ``_emit_partial_image`` called
``fit_image_preview`` — a PIL decode of a 1-3 MB PNG plus up to a dozen JPEG
re-encodes — directly on the event loop, so every streamed partial froze every
other stream, heartbeat and request in the process for the length of the
resize. The work belongs in a worker thread (``asyncio.to_thread``).

SUT: ``OpenAIImageGeneration._emit_partial_image``. Doubles: the preview
fitter (records the thread it ran on and returns a fixed preview) and the
emitter (records what was sent).
"""

from __future__ import annotations

import threading
from typing import Any

from matrx_ai.providers import media_frames
from matrx_ai.providers.openai.openai_image_api import OpenAIImageGeneration


class _Emitter:
    def __init__(self) -> None:
        self.sent: list[Any] = []

    async def send_data(self, payload: Any) -> None:
        self.sent.append(payload)


async def test_the_preview_is_fitted_in_a_worker_thread(monkeypatch) -> None:
    ran_on: list[int] = []

    def _fit(b64: str, *, mime_type: str = "image/png", **_kw: Any) -> tuple[str, str]:
        ran_on.append(threading.get_ident())
        return "cHJldmlldw==", "image/jpeg"

    monkeypatch.setattr(media_frames, "fit_image_preview", _fit)
    emitter = _Emitter()

    sent = await OpenAIImageGeneration._emit_partial_image(emitter, "iVBORw0KGgo=", 2)

    assert sent is True
    assert ran_on and ran_on[0] != threading.get_ident(), "the resize ran on the event loop"
    block = emitter.sent[0].block
    dumped = block.model_dump() if hasattr(block, "model_dump") else block
    assert "cHJldmlldw==" in str(dumped)  # the fitted preview, not the raw partial
