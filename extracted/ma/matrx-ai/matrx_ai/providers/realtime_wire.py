"""Raw realtime wires to a provider, for MEASURING the wire itself.

The voice latency bench (``scripts/voice_latency_bench.py``) times first reply
audio over each vendor's own realtime WebSocket. The funnel's catalog, retries
and cost ledger would sit inside the very number being measured, so the bench
speaks the provider protocol itself — but it never names a provider host. It
asks this module, the provider layer, to open the wire (no-exemptions ruling,
2026-10-19: the bench's host list became this seam). Same shape as the token
broker's ``open_broker_stream``: the caller names the operation, the endpoint
stays in the funnel.

Every call spends real provider money (cents). Nothing in the app calls this.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, Literal

import httpx

from matrx_ai.providers.keys import resolve_api_key

RealtimeVendor = Literal["xai", "openai", "gemini"]

_XAI_REALTIME = "wss://api.x.ai/v1/realtime"
_OPENAI_REALTIME = "wss://api.openai.com/v1/realtime"
_GEMINI_LIVE = (
    "wss://generativelanguage.googleapis.com/ws/"
    "google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent"
)
_OPENAI_SPEECH = "https://api.openai.com/v1/audio/speech"


@asynccontextmanager
async def open_realtime_wire(vendor: RealtimeVendor, model: str) -> AsyncIterator[Any]:
    """A connected realtime WebSocket to ``vendor`` for ``model``; closed on exit.

    xAI and OpenAI take the model on the URL and the key as a bearer header;
    Gemini Live takes the key on the URL and the model in the caller's setup frame.
    """
    import websockets  # noqa: PLC0415 — a measuring tool; the app never opens this

    if vendor == "xai":
        url = f"{_XAI_REALTIME}?model={model}"
        headers = {"Authorization": f"Bearer {resolve_api_key('XAI_API_KEY', required=True)}"}
    elif vendor == "openai":
        url = f"{_OPENAI_REALTIME}?model={model}"
        headers = {"Authorization": f"Bearer {resolve_api_key('OPENAI_API_KEY', required=True)}"}
    else:
        url = f"{_GEMINI_LIVE}?key={resolve_api_key('GEMINI_API_KEY', 'GOOGLE_API_KEY', required=True)}"
        headers = {}
    async with websockets.connect(url, additional_headers=headers or None, max_size=None) as ws:
        yield ws


def synthesize_speech_pcm(
    text: str, *, model: str = "gpt-4o-mini-tts", voice: str = "alloy"
) -> bytes:
    """``text`` spoken as 24 kHz mono PCM16 (OpenAI speech), for a bench fixture."""
    response = httpx.post(
        _OPENAI_SPEECH,
        headers={"Authorization": f"Bearer {resolve_api_key('OPENAI_API_KEY', required=True)}"},
        json={"model": model, "voice": voice, "input": text, "response_format": "pcm"},
        timeout=60,
    )
    response.raise_for_status()
    return response.content
