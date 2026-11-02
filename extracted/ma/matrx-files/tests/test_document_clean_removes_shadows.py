"""document_clean flattens a shadowed page photo: paper goes white, ink stays dark."""

from __future__ import annotations

import io

import numpy as np
import pytest
from PIL import Image, ImageDraw

from matrx_files.specific_handlers.image_ops import dispatch_op

pytest.importorskip("cv2")


def _shadowed_page() -> tuple[bytes, np.ndarray]:
    w, h = 800, 600
    page = Image.new("L", (w, h), 235)
    draw = ImageDraw.Draw(page)
    for row in range(8):
        y = 60 + row * 60
        draw.rectangle([60, y, 740, y + 6], fill=30)  # "text lines"
    ink = np.array(page) < 100
    # A hard diagonal shadow darkening the left half to ~40% brightness.
    xs = np.linspace(0.4, 1.0, w)[None, :].repeat(h, axis=0)
    shaded = (np.array(page, dtype=np.float32) * xs).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(shaded, "L").convert("RGB").save(buf, format="PNG")
    return buf.getvalue(), ink


@pytest.mark.parametrize("mode", ["gray", "color", "bw"])
def test_document_clean_flattens_shadow(mode: str) -> None:
    data, ink = _shadowed_page()
    before = np.array(Image.open(io.BytesIO(data)).convert("L"))
    assert before[~ink].min() < 110  # the shadow is real

    result = dispatch_op("document_clean", data, mask_bytes=None, params_dict={"mode": mode})
    out = np.array(result.image.convert("L"))

    paper = out[~ink]
    assert np.percentile(paper, 2) > 225, "shadowed paper must come out white"
    assert out[ink].mean() < 80, "ink must stay dark"
