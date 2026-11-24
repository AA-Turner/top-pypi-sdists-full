"""Gemini 2.5 refuses a per-picture ``mediaResolution`` (CGU-10 IMG7, measured 2026-11-11: 400 INVALID_ARGUMENT
on every level, while Gemini 3 accepts LOW / MEDIUM / HIGH / ULTRA_HIGH). A picture carrying one, sent to
a 2.x model, failed the whole call. The translator now removes it there (announced) and keeps it on 3+.
Proven red by removing ``_drop_part_resolution_before_gemini_3``'s call."""

from __future__ import annotations

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.media_config import ImageContent
from matrx_ai.providers.google.translator import _drop_part_resolution_before_gemini_3


@pytest.fixture(autouse=True)
def _text_making_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    """The catalog the server loads says these Gemini make text (CGU-10 IMG10: with NO catalog, a
    per-picture resolution is never sent — unknown is not "supported")."""
    from matrx_ai.catalog.manager import AiCatalogManager

    catalog = AiCatalogManager()
    catalog.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={}, aliases=[],
        models=[
            {"id": f"id-{n}", "name": n, "capabilities": {"input": ["text", "image"], "output": ["text"]}}
            for n in ("gemini-2.5-flash", "gemini-2.0-flash", "gemini-3-flash", "gemini-3.8-flash",
                      "gemini-2.5-pro", "gemini-3-pro")
        ],
    )
    monkeypatch.setattr("matrx_ai.catalog.manager.ai_catalog_manager", catalog)


def test_an_uncatalogued_gemini_3_gets_no_per_picture_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("matrx_ai.processing.vision.vision_classes._catalog", lambda: None)
    contents = _contents()
    _drop_part_resolution_before_gemini_3(contents, "gemini-3-flash")
    assert "mediaResolution" not in contents[0]["parts"][1]


def _contents() -> list[dict]:
    return [{"role": "user", "parts": [{"text": "x"}, {"inlineData": {"data": "AA"}, "mediaResolution": {"level": "MEDIA_RESOLUTION_LOW"}}]}]


@pytest.mark.parametrize(("model", "kept"), [("gemini-2.5-flash", False), ("gemini-2.0-flash", False),
                                             ("gemini-3-flash", True), ("gemini-3.8-flash", True), ("models/gemini-2.5-pro", False)])
def test_only_gemini_3_and_later_keep_a_per_picture_resolution(model: str, kept: bool) -> None:
    contents = _contents()
    _drop_part_resolution_before_gemini_3(contents, model)
    assert ("mediaResolution" in contents[0]["parts"][1]) is kept
    assert contents[0]["parts"][1]["inlineData"] == {"data": "AA"}  # the picture itself always goes


@pytest.mark.parametrize(("model", "kept"), [("gemini-2.5-flash", False), ("gemini-3-pro", True)])
def test_the_translator_applies_it(model: str, kept: bool) -> None:
    from matrx_ai.providers.google.translator import GoogleTranslator
    from matrx_ai.testing.profile_factory import make_profile

    picture = ImageContent(base64_data="AAAA", mime_type="image/jpeg", media_resolution="MEDIA_RESOLUTION_LOW")
    config = UnifiedConfig(
        model=model,
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="x"), picture])]),
    )
    wire = GoogleTranslator().to_google(
        config,
        make_profile(model_name=model, wire_format="google_genai",
                     capabilities={"input": ["text", "image"], "output": ["text"], "features": [], "interaction": "turn"}),
    )
    parts = [part for content in wire["contents"] for part in content["parts"]]
    pictures = [part for part in parts if "inlineData" in part or "inline_data" in part]
    assert pictures, f"the picture never reached the wire: {parts}"
    assert any("mediaResolution" in part for part in pictures) is kept
