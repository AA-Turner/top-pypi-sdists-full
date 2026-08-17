"""Regression tests for agmet logo scaling (0.4.917).

fig.figimage draws at NATIVE pixel size. acres.png (3089x973) therefore
rendered wider than the whole figure and covered the title, while the older
harvest.png (221x235) / geoglam.png (466x143) pair always fit. load_scaled_logo
downsizes into a display box, preserving aspect ratio and never upscaling — so
the pre-existing logos must come through byte-identical in shape.
"""
import numpy as np
import pytest
from PIL import Image

from geocif.agmet.plot import LOGO_MAX_PX, load_scaled_logo


def _png(tmp_path, name, size):
    p = tmp_path / name
    Image.new("RGBA", size, (10, 20, 30, 255)).save(p)
    return p


def test_default_box_is_500x240():
    # 240 not 200: harvest.png is 235px tall and must not be shrunk
    assert LOGO_MAX_PX == (500, 240)


def test_oversized_logo_scaled_into_box(tmp_path):
    # acres.png real dimensions
    arr = load_scaled_logo(_png(tmp_path, "acres.png", (3089, 973)))
    h, w = arr.shape[:2]
    assert w <= 500 and h <= 240
    # width is the binding constraint here; aspect ratio preserved
    assert w == 500
    assert h == round(973 * (500 / 3089))


def test_small_logos_untouched(tmp_path):
    # harvest.png and geoglam.png real dimensions — must NOT be upscaled
    for name, size in [("harvest.png", (221, 235)), ("geoglam.png", (466, 143))]:
        arr = load_scaled_logo(_png(tmp_path, name, size))
        assert arr.shape[:2] == (size[1], size[0]), name


def test_height_bound_can_bind(tmp_path):
    # tall-and-narrow: height caps first
    arr = load_scaled_logo(_png(tmp_path, "tall.png", (300, 900)))
    h, w = arr.shape[:2]
    assert h == 240
    assert w == round(300 * (240 / 900))


def test_custom_box_respected(tmp_path):
    arr = load_scaled_logo(_png(tmp_path, "acres.png", (3089, 973)), 250, 100)
    h, w = arr.shape[:2]
    assert w <= 250 and h <= 100


def test_returns_ndarray_for_figimage(tmp_path):
    arr = load_scaled_logo(_png(tmp_path, "acres.png", (3089, 973)))
    assert isinstance(arr, np.ndarray)
    assert arr.ndim == 3 and arr.shape[2] == 4
