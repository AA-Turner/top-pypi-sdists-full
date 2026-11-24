"""``quad_problem`` judges a crop quad against the picture it crops, small pictures included.

Breaks caught (A9 review MINOR-2): the full frame of a picture of 7 x 7 px or less refused as "holds no
page" (a fixed 64 px² floor); a 1 x 1 px picture told its quad "looks like 0-1 fractions".
"""

from __future__ import annotations

import pytest

from matrx_files.specific_handlers.pdf.images_to_pdf import quad_problem


def _frame(w: float, h: float) -> dict:
    return {"top_left": [0, 0], "top_right": [w, 0], "bottom_right": [w, h], "bottom_left": [0, h]}


@pytest.mark.parametrize(("w", "h"), [(7, 7), (5, 3), (2, 2), (8, 8), (60, 60), (1000, 5)])
def test_the_full_frame_of_any_picture_bigger_than_a_pixel_is_a_crop(w: float, h: float) -> None:
    assert quad_problem(_frame(w, h), w, h) is None


def test_a_single_pixel_picture_is_named_as_too_small_not_as_fractions() -> None:
    said = quad_problem(_frame(1, 1), 1, 1)
    assert said is not None and "single pixel" in said and "fractions" not in said


@pytest.mark.parametrize(
    ("quad", "w", "h", "says"),
    [
        ({"top_left": [10, 10], "top_right": [14, 10], "bottom_right": [14, 13], "bottom_left": [10, 13]},
         1240, 1754, "12 square pixels, so it holds no page"),
        (_frame(0.95, 0.97), 1240, 1754, "looks like 0-1 fractions"),
        (_frame(7, 7), None, None, None),  # the door, without the picture: a 7 x 7 frame may be the whole picture
    ],
)
def test_a_quad_too_small_for_its_picture_is_refused_in_words(quad: dict, w, h, says) -> None:
    said = quad_problem(quad, w, h)
    assert (said is None) if says is None else (said is not None and says in said)
