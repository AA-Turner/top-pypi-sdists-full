"""The prompt estimate counts every picture by its provider's own rule (CGU-10 AND-V IMG5 #2/#10).

Live 2026-11-11 (chat 8e205257…, Claude turn): the fit check estimated 2,356 input tokens and the
provider counted 10,671 — the three pictures in the history were measured by their storage form
with the bytes stripped, a few dozen characters each. A long chat with pictures could pass the
estimate and be refused by the provider.

Forcing: the real ``estimate_prompt_tokens`` over a real picture-bearing history; only the
catalog's wire-format lookup is replaced. Before the fix every picture case is within a few dozen
tokens of the text-only estimate.
"""

from __future__ import annotations

import base64
import io

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
    context_preflight,
)
from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.media_config import DocumentContent, ImageContent
from matrx_ai.processing.vision.image_tokens import PAGE_TEXT_TOKENS, image_tokens, page_tokens
from matrx_ai.processing.vision.vision_classes import VISION_API_CLASSES


def _png(width: int, height: int) -> str:
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (width, height), (255, 0, 0)).save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def _history(*pictures: ImageContent) -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", content=[TextContent(text="Edit the centre."), *pictures]),
        UnifiedMessage(role="assistant", content=[TextContent(text="Done.")]),
        UnifiedMessage(role="user", content=[TextContent(text="Describe it.")]),
    ]


def _estimate(model: str, history: list[UnifiedMessage]) -> int:
    return estimate_prompt_tokens(UnifiedConfig(model=model, messages=MessageList(_messages=history)))


@pytest.fixture(autouse=True)
def _wire(monkeypatch):
    routes = {
        "claude-haiku-5-5": "anthropic_chat",
        "gpt-5.4-nano": "openai_chat",
        "gpt-4o": "openai_chat",
        "gpt-5.5": "openai_chat",
        "gemini-2.5-flash": "google_chat",
        "deepseek-chat": "openai_chat",
    }
    monkeypatch.setattr(context_preflight, "_wire_format", lambda _config, model: routes.get(model))
    sees = {"deepseek-chat": False}
    monkeypatch.setattr(context_preflight, "_reads_images", lambda _config, model: sees.get(model))


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        # Anthropic: fit to 1,568, then 28 px patches + 3 — count_tokens for 1568² on haiku-5-5 is 3,139
        # (AND-IMG18 N2; w*h/750 said 3,279).
        ("claude-haiku-5-5", 3 * 3139),
        # OpenAI GPT-5.4 (IMG7 #1, measured): 32-px patches at the class's edge (original, 2,048, now
        # SENT explicitly): 64*64 = 4,096 patches, x1.2 (float32) = 4,916 — the provider's own count.
        ("gpt-5.4-nano", 3 * 4_916),
        # OpenAI legacy tiles: 2,048 -> 768 short side -> 2x2 tiles -> 170*4 + 85.
        ("gpt-4o", 3 * 765),
        # Gemini 2.5: a flat 258 a picture (CGU-10 IMG8, countTokens + a billed 1,536² call: 258;
        # the 768-tile rule said 1,032).
        ("gemini-2.5-flash", 3 * 258),
    ],
)
def test_three_large_pictures_are_counted_by_the_providers_rule(model: str, expected: int) -> None:
    text_only = _estimate(model, _history())
    pictures = [ImageContent(base64_data=_PNG_2048, mime_type="image/png") for _ in range(3)]
    with_pictures = _estimate(model, _history(*pictures))
    # Each picture rides behind its own ``<attachment/>`` label, counted too (CGU-10 AND-IMG12 #2).
    labels = sum(
        context_preflight.media_label_tokens(p, "user", model=model, wire_format=context_preflight._wire_format(None, model))
        for p in pictures
    )
    assert labels > 0
    assert with_pictures - text_only >= expected + labels
    assert with_pictures - text_only < expected + labels + 200  # the stripped storage form only adds a little


def test_a_stored_size_is_used_without_decoding() -> None:
    picture = ImageContent(url="https://cdn.example/x.png", width=1000, height=500, mime_type="image/png")
    assert _estimate("claude-haiku-5-5", _history(picture)) - _estimate("claude-haiku-5-5", _history()) >= 667


def test_a_picture_of_unknown_size_counts_as_the_largest_its_class_sends() -> None:
    picture = ImageContent(url="https://cdn.example/x.png", mime_type="image/png")
    grew = _estimate("claude-haiku-5-5", _history(picture)) - _estimate("claude-haiku-5-5", _history())
    assert grew >= 3139  # 1568², the largest the Claude class sends (count_tokens, AND-IMG18 N2)


def test_a_picture_hidden_from_the_model_counts_nothing() -> None:
    history = _history(ImageContent(base64_data=_PNG_2048, mime_type="image/png"))
    history[0].is_visible_to_model = False
    assert _estimate("claude-haiku-5-5", history) < 200
    # The estimator's OWN exclusion (plant N7): a turn hidden after the config was built (the
    # constructor's sanitize already drops one hidden before) is still not counted.
    config = UnifiedConfig(
        model="claude-haiku-5-5",
        messages=MessageList(_messages=_history(ImageContent(base64_data=_PNG_2048, mime_type="image/png"))),
    )
    config.messages[0].is_visible_to_model = False
    assert estimate_prompt_tokens(config) < 200


def test_the_rules() -> None:
    assert image_tokens(200, 200, VISION_API_CLASSES["openai_low"]) == 85  # gpt-4o-style tiles at low
    assert image_tokens(300, 300, VISION_API_CLASSES["gemini25_default"]) == 258
    assert image_tokens(4000, 3000, VISION_API_CLASSES["gemini3_high"]) == 1120
    assert image_tokens(4000, 3000, VISION_API_CLASSES["gemini3_low"]) == 280
    # 27 x 36 patches of 28 px + 3 (an unnamed Claude counts high-resolution — AND-IMG18 N2).
    assert image_tokens(750, 1000, VISION_API_CLASSES["anthropic_sonnet_default"]) == 975


# ── CGU-10 IMG6 #3: GPT-5 counts 32-px patches, not the gpt-4o tiles ───────────────────────────────


@pytest.mark.parametrize(
    ("model", "cls", "size", "expected"),
    [
        # IMG7 #1: the provider's OWN counts (tests/test_openai_picture_counts_match_the_provider.py).
        ("gpt-5.5", "openai_original", (2048, 2048), 4916),  # 4,096 patches x1.2
        ("gpt-5.5", "openai_original", (3024, 4032), 3687),  # fit to 2,048: 1,536 x 2,048 = 3,072 x1.2
        ("gpt-5.5", "openai_original", (8000, 1500), 922),  # 2,048 x 384 = 768 x1.2
        ("gpt-5.5", "openai_original", (64, 64), 5),
        ("gpt-5.5", "openai_original", (None, None), 4916),  # unknown: the largest the class sends
        ("gpt-5.2", "openai_high", (2048, 2048), 4916),  # gpt-5.2 ignores detail: no 2,500 cap
        ("gpt-5-mini", "openai_high", (1000, 1000), 1229),  # 32 x 32 patches x1.2
        ("gpt-5-nano", "openai_high", (1000, 1000), 1536),  # x1.5
        ("gpt-5-nano", "openai_low", (1000, 1000), 384),  # its class sends 512²; nano ignores low
        ("gpt-4o", "openai_high", (2048, 2048), 765),  # legacy keeps tiles
        ("o3", "openai_high", (2048, 2048), 675),  # o3 tiles: 75 + 150 per tile
    ],
)
def test_openai_counts_by_model_family(model: str, cls: str, size: tuple, expected: int) -> None:
    assert image_tokens(*size, VISION_API_CLASSES[cls], model) == expected


def test_the_patch_cap_holds_for_any_shape() -> None:
    for w, h in [(4000, 3000), (5000, 37), (2047, 2049), (1999, 1999), (33, 9000)]:
        assert image_tokens(w, h, VISION_API_CLASSES["openai_high"], "gpt-5") <= 1536


# ── CGU-10 IMG6 #4: a PDF's pages count ─────────────────────────────────────────────────────────


def _pdf(pages: int) -> str:
    body = b"%PDF-1.4\n1 0 obj << /Type /Pages /Count " + str(pages).encode() + b" >> endobj\n"
    body += b"".join(str(n + 2).encode() + b" 0 obj << /Type /Page /Parent 1 0 R >> endobj\n" for n in range(pages))
    return base64.b64encode(body + b"%%EOF").decode()


@pytest.mark.parametrize(
    ("model", "per_page"),
    # A letter page picture at 1,212 x 1,568: 44 x 56 patches + 3 (AND-IMG18 N2). count_tokens for a blank
    # letter PDF page is ~1,550, so the page estimate stays over (the safe side).
    [("claude-haiku-5-5", PAGE_TEXT_TOKENS + 2467), ("gemini-2.5-flash", 258)],
)
def test_a_hundred_page_pdf_counts_every_page(model: str, per_page: int) -> None:
    by_count = DocumentContent(url="https://cdn.example/x.pdf", mime_type="application/pdf", page_count=100)
    by_bytes = DocumentContent(base64_data=_pdf(100), mime_type="application/pdf")
    text_only = _estimate(model, _history())
    for document in (by_count, by_bytes):
        grew = _estimate(model, _history(document)) - text_only
        assert 100 * per_page <= grew < 100 * per_page + 200, grew  # was 49 in all


def test_a_pdf_of_unknown_length_counts_one_page() -> None:
    document = DocumentContent(url="https://cdn.example/x.pdf", mime_type="application/pdf")
    grew = _estimate("claude-haiku-5-5", _history(document)) - _estimate("claude-haiku-5-5", _history())
    assert grew >= PAGE_TEXT_TOKENS + 2467


# ── CGU-10 IMG6 #5: a model that cannot see is not charged for pictures ───────────────────────────


def test_a_text_only_model_is_not_charged_for_pictures_it_never_receives() -> None:
    pictures = [ImageContent(url=f"https://cdn.example/{n}.png", mime_type="image/png") for n in range(40)]
    grew = _estimate("deepseek-chat", _history(*pictures)) - _estimate("deepseek-chat", _history())
    assert grew < 40 * 60  # the stripped storage form only (was 30,600)
    # The same pictures on a model that sees: counted.
    assert _estimate("gpt-4o", _history(*pictures)) - _estimate("gpt-4o", _history()) >= 40 * 765


# ── CGU-10 IMG7 #3: a text-only model's PDF rides the wire as its extracted text ──────────────────


def test_a_text_only_model_counts_a_pdf_as_its_extracted_text() -> None:
    """Plant N15 survived IMG7: nothing decided. The media fallback EXTRACTS a PDF's text for a model that
    reads no images (a one-line attachment is for pictures only), so 100 pages are 100 pages of text —
    not the 47 tokens the estimate said, and not page pictures the model never gets."""
    document = DocumentContent(url="https://cdn.example/x.pdf", mime_type="application/pdf", page_count=10)
    grew = _estimate("deepseek-chat", _history(document)) - _estimate("deepseek-chat", _history())
    assert 10 * PAGE_TEXT_TOKENS <= grew < 10 * PAGE_TEXT_TOKENS + 200, grew
    # A picture next to it still costs nothing on that model.
    picture = ImageContent(url="https://cdn.example/p.png", mime_type="image/png")
    assert _estimate("deepseek-chat", _history(picture)) - _estimate("deepseek-chat", _history()) < 60


def test_a_long_text_only_pdf_counts_no_more_text_than_the_fallback_extracts() -> None:
    """CGU-10 IMG8 #7: the media fallback cuts a PDF's extracted text at 100,000 characters, so a
    100-page PDF puts at most ~34,500 tokens on a text-only model's wire — the estimate said 150,000
    and refused a fit the provider would have taken. Red when the cut is ignored."""
    from matrx_ai.config.context_trim import estimate_budget_tokens
    from matrx_ai.processing.media_fallback.resolvers import MAX_EXTRACTED_DOCUMENT_CHARS

    ceiling = estimate_budget_tokens(MAX_EXTRACTED_DOCUMENT_CHARS, "prose")
    document = DocumentContent(url="https://cdn.example/x.pdf", mime_type="application/pdf", page_count=100)
    grew = _estimate("deepseek-chat", _history(document)) - _estimate("deepseek-chat", _history())
    assert ceiling <= grew < ceiling + 200, grew
    assert grew < 100 * PAGE_TEXT_TOKENS


# ── CGU-10 IMG7 #4: Gemini's per-picture resolution is what is counted ──────────────────────────


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        # A numbered Gemini 3.x counts what countTokens counts (AND-IMG17); Gemini 4 / ``*-latest`` the published.
        (None, 1089),  # the class's (HIGH)
        ("MEDIA_RESOLUTION_LOW", 256),
        ("media_resolution_medium", 529),
        ("HIGH", 1089),
        ("MEDIA_RESOLUTION_ULTRA_HIGH", 2209),
    ],
)
def test_a_gemini_3_picture_counts_its_own_media_resolution(level: str | None, expected: int) -> None:
    from matrx_ai.processing.vision.image_tokens import image_content_tokens

    # A square picture: the budget's grid is 16², 23², 33², 47² (countTokens; AND-IMG18 — any shape, any size).
    picture = ImageContent(url="https://cdn.example/p.png", mime_type="image/png", media_resolution=level,
                           width=1000, height=1000)
    assert image_content_tokens(picture, model="gemini-3-flash", wire_format="google_chat") == expected
    # A picture of unknown size counts the published budget: no shape counts more.
    unknown = ImageContent(url="https://cdn.example/p.png", mime_type="image/png", media_resolution=level)
    assert image_content_tokens(unknown, model="gemini-3-flash", wire_format="google_chat") >= expected


def test_gemini_25_ignores_a_per_picture_resolution() -> None:
    """Gemini 2.5 refuses ``mediaResolution`` on a part (400, measured 2026-11-11): never a cheaper count."""
    from matrx_ai.processing.vision.image_tokens import image_content_tokens

    low = ImageContent(url="https://cdn.example/p.png", mime_type="image/png", media_resolution="MEDIA_RESOLUTION_LOW")
    assert image_content_tokens(low, model="gemini-2.5-flash", wire_format="google_chat") == 258


def test_a_gemini_3_pdf_page_counts_560() -> None:
    """Survivor N9 (IMG7): Gemini 3's default PDF media resolution is 560 a page, not 2.5's 258."""
    assert page_tokens(VISION_API_CLASSES["gemini3_high"], "gemini-3-flash") == 560
    assert page_tokens(VISION_API_CLASSES["gemini25_default"], "gemini-2.5-flash") == 258


# ── F9 guards ──────────────────────────────────────────────────────────────────────────────────


def test_two_pictures_of_one_length_and_header_never_share_a_size() -> None:
    """A JPEG's size sits past any short prefix: the cache key covers the whole payload (plant N8)."""
    from matrx_ai.processing.vision.image_tokens import _payload_key

    head = "/9j/4AAQSkZJRgABAQ" + "A" * 120
    assert _payload_key(head + "BBBB") != _payload_key(head + "CCCC")
    assert _payload_key(head + "BBBB") == _payload_key(head + "BBBB")


_PNG_2048 = _png(2048, 2048)
