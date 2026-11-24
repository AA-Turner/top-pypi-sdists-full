"""A text layer's word boxes keep a tenth of a pixel (A9 review MINOR-1: full float precision made every
stored layer ~2x larger, copied on every page row of every version). Break caught: the rounding dropped,
or rounding to whole pixels (moves a word's edge by up to half a pixel)."""

from __future__ import annotations

import json

import pytest

from matrx_files.specific_handlers.pdf.ops.text_layer import LayerPage, LayerWord


@pytest.mark.parametrize(
    ("box", "stored"),
    [
        ((100.04999, 140.2500001, 612.3333333, 219.96), [100.0, 140.3, 612.3, 220.0]),
        ((0.0, 0.0, 9.87654321, 1.0500001), [0.0, 0.0, 9.9, 1.1]),
    ],
)
def test_a_word_box_is_stored_to_a_tenth_of_a_pixel(box, stored) -> None:
    page = LayerPage(width_px=1240, height_px=1754, words=[LayerWord(text="Invoice", box=box)])
    dumped = json.loads(json.dumps(page.model_dump(mode="json", exclude_defaults=True)))
    assert dumped["words"] == [{"text": "Invoice", "box": stored}]
