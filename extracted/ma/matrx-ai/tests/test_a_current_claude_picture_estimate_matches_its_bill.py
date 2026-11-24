"""A CURRENT CLAUDE'S PICTURE ESTIMATE IS WITHIN 2% OF ITS BILL (CGU-10 AND-V IMG17, finding N2).

AND-IMG17 #3 proved the Claude picture estimate within 2% on claude-sonnet-4-6, a DEPRECATED offering. On the
current Claudes the estimate is outside the bar. Live, server 5c3c107, test run 70f3eb6c, a 3000x2250 picture
replayed on later turns (picture chat minus a text-only twin, equal replies): claude-sonnet-5-5 and
claude-haiku-5-5 each billed 2,430 for the picture with its label; the estimate (picture 2,459 + label) is 2,517,
+3.6% (over, never under). claude-opus-4-6 (standard tier) was +1.6%, inside the bar.

Fixed (AND-IMG18): Claude counts 28 px patches + 3 and its tokenizer counts the label 75 (``count_tokens``:
2,355 + 75 = 2,430, the bill to the token). The sizing is each model row's ``capabilities.image_sizing`` in the
catalog; the name's tier answers only when no catalog does. Both paths are checked here.
"""

from __future__ import annotations

import base64
import io

import pytest

from matrx_ai.config.context_preflight import media_label_tokens
from matrx_ai.config.media_config import ImageContent
from matrx_ai.processing.vision.image_tokens import image_content_tokens

FILE_ID = "ea1e35af-4521-475d-bf7e-dde5bcf71b4a"
BILLED = 2_430  # picture + its label, claude-sonnet-5-5 and claude-haiku-5-5 alike (live, run 70f3eb6c)


def _png() -> str:
    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (3000, 2250), (40, 90, 160)).save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


@pytest.mark.parametrize("model", ["claude-sonnet-5-5", "claude-haiku-5-5"])
def test_a_current_claude_picture_is_estimated_within_two_percent(model: str) -> None:
    item = ImageContent(base64_data=_png(), mime_type="image/png", file_id=FILE_ID,
                        metadata={"file_name": f"{FILE_ID}.png"})
    est = image_content_tokens(item, model=model, wire_format="anthropic_chat") + media_label_tokens(
        item, "user", model=model, wire_format="anthropic_chat")
    assert BILLED <= est <= BILLED * 1.02, est


HIRES_ROW = {"long_edge": 2576, "max_patches": 4784, "patch_px": 28, "overhead": 3, "label_scale": 1.35}
STANDARD_ROW = {"long_edge": 1568, "max_patches": 1568, "patch_px": 28, "overhead": 4, "label_scale": 1.15}

# count_tokens, 2026-11-12, picture tokens over a text-only twin (every current Claude alike per tier).
MEASURED_HIRES = {(1568, 1176): 2_355, (1568, 1568): 3_139, (1092, 1092): 1_524, (2576, 1456): 4_787,
                  (1000, 1000): 1_299, (3000, 2250): 4_743, (500, 300): 201}
MEASURED_STANDARD = {(1568, 1176): 1_568, (1568, 1568): 1_525, (1092, 1092): 1_525, (2576, 1456): 1_564,
                     (1000, 1000): 1_300, (3000, 2250): 1_568, (500, 300): 202}


class _Catalog:
    """A catalog whose rows say how each model counts a picture — and that names the model differently from
    the name rule, so a pass proves the catalog was read."""

    def __init__(self, rows: dict[str, dict]) -> None:
        self._rows = rows

    def model_image_sizing(self, model: str | None):
        return self._rows.get(model or "")


@pytest.mark.parametrize(("row", "measured"), [(HIRES_ROW, MEASURED_HIRES), (STANDARD_ROW, MEASURED_STANDARD)])
def test_claude_counts_patches_exactly_as_count_tokens_does(monkeypatch, row, measured) -> None:
    from matrx_ai.processing.vision import vision_classes
    from matrx_ai.processing.vision.image_tokens import claude_image_sizing, claude_picture_tokens

    monkeypatch.setattr(vision_classes, "_catalog", lambda: _Catalog({"claude-from-the-catalog": row}))
    sizing = claude_image_sizing("claude-from-the-catalog")
    for (w, h), billed in measured.items():
        assert claude_picture_tokens(w, h, sizing) == billed, (w, h)


def test_the_catalog_row_decides_the_tier_not_the_name(monkeypatch) -> None:
    from matrx_ai.processing.vision import vision_classes
    from matrx_ai.processing.vision.image_tokens import claude_image_sizing

    monkeypatch.setattr(vision_classes, "_catalog", lambda: _Catalog({"claude-sonnet-5-5": STANDARD_ROW}))
    assert claude_image_sizing("claude-sonnet-5-5").max_patches == 1568  # the name alone says high-resolution


def test_the_sizing_fact_is_canonical_vocabulary() -> None:
    from matrx_ai.providers.capability_vocabulary import normalize_capabilities

    base = {"input": ["image", "text"], "output": ["text"], "features": [], "interaction": "turn"}
    assert normalize_capabilities({**base, "image_sizing": HIRES_ROW}).ok
    bad = normalize_capabilities({**base, "image_sizing": {"long_edge": "2576", "tiles": 4}})
    assert not bad.ok, bad.rejections
