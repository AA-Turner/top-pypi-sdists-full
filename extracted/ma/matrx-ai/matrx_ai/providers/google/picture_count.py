"""Google's own picture count for a Gemini (free ``countTokens``) — the provider call behind the
catalog walk in ``matrx_ai.processing.vision.gemini_picture_walk``.

Provider access lives in the provider layer (mandates STATE.md section 9): the walk decides what a row
SHOULD count; this module is the one place that asks Google what it DOES count. Opt-in only — the
live walks call it with ``MATRX_LIVE_GEMINI=1`` and ``GEMINI_API_KEY``.
"""

from __future__ import annotations

from typing import Any


def measure_picture_tokens(name: str, api_key: str) -> int:
    """Google's own count for one 1,536² JPEG on ``name`` (free ``countTokens``; picture minus text)."""
    import base64
    import io
    import json
    import urllib.request

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (1536, 1536), (120, 30, 200)).save(buf, "JPEG")
    data = base64.b64encode(buf.getvalue()).decode()

    def count(parts: list[dict[str, Any]]) -> int:
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{name}:countTokens",
            data=json.dumps({"contents": [{"role": "user", "parts": parts}]}).encode(),
            headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        )
        return int(json.load(urllib.request.urlopen(req, timeout=60))["totalTokens"])

    text = count([{"text": "hi"}])
    return count([{"text": "hi"}, {"inlineData": {"mimeType": "image/jpeg", "data": data}}]) - text


__all__ = ["measure_picture_tokens"]
