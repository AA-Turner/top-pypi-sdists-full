"""A Gemini image model that answers in TEXT keeps the reply (feedback be97b536).

Live 2026-10-04 (system_error f9fb9972, ca2e1e6e): gemini-3.1-flash-image asked "17*23"
answered in text, produced no image, and the run failed "google image generation returned
no assets" -> "processing the result failed"; the paid reply was thrown away.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config import TokenUsage, UnifiedResponse


def _raw(*parts: SimpleNamespace) -> SimpleNamespace:
    return SimpleNamespace(candidates=[SimpleNamespace(content=SimpleNamespace(parts=list(parts)))])


def test_native_gemini_text_parts_are_the_reply_and_thoughts_are_not() -> None:
    from matrx_ai.providers.google.google_image_api import GoogleImageGeneration

    gen = GoogleImageGeneration()
    raw = _raw(
        SimpleNamespace(text="thinking about arithmetic", thought=True, inline_data=None),
        SimpleNamespace(text="17 × 23 = 391.", thought=False, inline_data=None),
    )
    assert gen._extract_assets(raw) == []
    assert gen._extract_text_reply(raw) == "17 × 23 = 391."


@pytest.mark.asyncio
async def test_text_only_response_returns_the_text_with_usage() -> None:
    from matrx_ai.providers.google.google_image_api import GoogleImageGeneration

    gen = GoogleImageGeneration()
    sent: list[str] = []

    class _Emitter:
        async def send_chunk(self, text: str) -> None:
            sent.append(text)

    usage = TokenUsage(input_tokens=12, output_tokens=8, matrx_model_name="gemini-3.1-flash-image", provider_model_name="gemini-3.1-flash-image", api="google")
    gen._build_usage = lambda *args, **kwargs: usage  # type: ignore[method-assign]
    profile = SimpleNamespace(offering_id=None, model_name="gemini-3.1-flash-image")
    response = await gen._text_only_response(
        SimpleNamespace(model="gemini-3.1-flash-image"), {}, _raw(), profile, "17 × 23 = 391.", _Emitter()
    )
    assert isinstance(response, UnifiedResponse)
    assert response.messages[0].content[0].text == "17 × 23 = 391."
    assert response.usage is usage
    assert sent == ["17 × 23 = 391."]
