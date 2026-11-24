"""A CLAUDE PICTURE ESTIMATE MATCHES WHAT CLAUDE BILLS (AND-V IMG16 F3).

Live (server 53de963, 2026-11-12, run 876e061d): a 3000x2250 photo on claude-sonnet-4-6 billed 1,626 input
tokens over its text-only twin (picture + its label); the estimate was 2,459 (+51%). The estimator fits the
picture to the class's 1,568 long edge and counts w*h/750 (1568x1176 -> 2,459), but Claude scales any picture
over ~1.15 megapixels (~1,600 tokens) down again before it counts it. The same gap means the Sonnet class
sends ~1.6x the pixels Claude uses. GPT (3,733 billed / 3,687 est.) and Gemini (1,144 / 1,120) are within 2%.

Fixed (AND-IMG17 #3): the Anthropic estimate fits to the model's documented pixel budget
(``claude_pixel_budget``) — ~1.2 MP for the earlier tier, ~3.75 MP for the high-resolution tier.
"""

from __future__ import annotations

import base64
import io

from PIL import Image

from matrx_ai.config.media_config import ImageContent
from matrx_ai.processing.vision.image_tokens import image_content_tokens

BILLED_PICTURE_AND_LABEL = 1_626  # live, claude-sonnet-4-6, 3000x2250


def _jpeg(width: int, height: int) -> str:
    buf = io.BytesIO()
    Image.new("RGB", (width, height), (40, 90, 160)).save(buf, "JPEG")
    return base64.b64encode(buf.getvalue()).decode()


def test_a_large_picture_on_sonnet_is_estimated_within_two_percent_and_never_under() -> None:
    est = image_content_tokens(
        ImageContent(base64_data=_jpeg(3000, 2250), mime_type="image/jpeg"), model="claude-sonnet-4-6", wire_format="anthropic"
    )
    # the label rides in the bill too (~40 tokens): the picture alone is at most the bill
    assert BILLED_PICTURE_AND_LABEL * 0.95 <= est <= BILLED_PICTURE_AND_LABEL * 1.02, est


def test_a_high_resolution_claude_still_counts_the_whole_picture() -> None:
    """The high-resolution tier (Opus 4.7+, Sonnet 5+, Haiku 5+) is NOT capped at ~1,600: Claude's own
    ``count_tokens`` for a 1568² picture is 3,139 (56 x 56 patches + 3; AND-IMG18 N2 — the old 3,279 was w*h/750)."""
    est = image_content_tokens(
        ImageContent(base64_data=_jpeg(1568, 1568), mime_type="image/jpeg"), model="claude-haiku-5-5", wire_format="anthropic"
    )
    assert est == 3_139, est


def test_an_unknown_claude_counts_on_the_safe_side() -> None:
    from matrx_ai.processing.vision.image_tokens import claude_pixel_budget

    assert claude_pixel_budget("claude-sonnet-4-6")[1] == 1_568 * 28 * 28
    assert claude_pixel_budget("claude-opus-4-6")[1] == 1_568 * 28 * 28
    assert claude_pixel_budget("claude-opus-4-7")[1] == 4_784 * 28 * 28
    assert claude_pixel_budget("claude-something-new")[1] == 4_784 * 28 * 28


def test_a_numbered_gemini_3_counts_what_google_counts() -> None:
    """Live AND-IMG17: gemini-3.8-flash billed 1,136 for a 3000x2250 picture and its label; the published 1,120
    budget + label estimated 1,172 (+3.2%). A numbered Gemini 3.x counts 1,089 at HIGH (countTokens on every
    live 3.x row); Gemini 4 (1,120) and an un-numbered ``*-latest`` keep the published budget."""
    from matrx_ai.config.context_preflight import media_label_tokens

    fid = "9beeddf7-1a09-43da-aac0-00cd14257f6a"
    picture = ImageContent(base64_data=_jpeg(3000, 2250), mime_type="image/jpeg", file_id=fid,
                           metadata={"file_name": f"{fid}.png"})
    est = image_content_tokens(picture, model="gemini-3.8-flash", wire_format="google_chat") + media_label_tokens(
        picture, "user", model="gemini-3.8-flash", wire_format="google_chat"
    )
    # AND-IMG18 (live, run f67bd337): billed 1,118 = countTokens' 1,064 for the 4:3 picture + 54 for its label.
    # (The older bills, 1,136-1,148, carried a longer storage-name label the server no longer sends.)
    for billed in (1_118,):
        assert billed <= est <= billed * 1.02, (est, billed)
    assert image_content_tokens(picture, model="gemini-4-argon", wire_format="google_chat") == 1_120
    assert image_content_tokens(picture, model="gemini-flash-latest", wire_format="google_chat") == 1_120


def test_a_numbered_gemini_3_counts_the_budget_as_a_grid_of_the_pictures_shape() -> None:
    """countTokens on gemini-3.8-flash at HIGH, 2026-11-12 (AND-IMG18): every shape exact."""
    from matrx_ai.processing.vision.image_tokens import gemini3_grid_tokens

    measured = {(1536, 1536): 1089, (1536, 1152): 1064, (1920, 1080): 1100, (1536, 768): 1081, (1000, 100): 1050,
                (3000, 1000): 1083, (1000, 1500): 1080, (1280, 1024): 1073, (1100, 1000): 1085, (1300, 1000): 1102,
                (2500, 1000): 1092, (4000, 1000): 1056, (1000, 700): 1120, (1000, 800): 1073, (400, 400): 1089}
    for (w, h), counted in measured.items():
        assert gemini3_grid_tokens(w, h, 1120) == counted, (w, h)
