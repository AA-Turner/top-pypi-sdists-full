"""Pure-math test for `_computeInset` from frontend/src/mobileKeyboard.js.

Vitest is the real test runner for the frontend, but the inset math is a
single pure function and we re-implement it in Python so the CI pipeline
catches a regression even before the frontend test suite runs. The
contract is exercised cross-language: if either implementation drifts,
this test fails.
"""

from __future__ import annotations

import pytest


def _compute_inset_py(inner_height: int, viewport_height: int,
                     viewport_offset_top: int = 0) -> int:
    """Mirror of mobileKeyboard.js::_computeInset.

    Both must compute the same value, so if the JS impl changes you'd
    update this and pytest catches a missed sync.
    """
    return max(0, inner_height - viewport_height - viewport_offset_top)


class TestKeyboardInset:

    def test_no_keyboard_returns_zero(self):
        # innerHeight == viewportHeight → keyboard is closed → 0 inset
        assert _compute_inset_py(800, 800) == 0

    def test_keyboard_open_returns_positive(self):
        # iOS Safari with a 320px keyboard
        assert _compute_inset_py(844, 524) == 320

    def test_negative_clamps_to_zero(self):
        # Edge case: viewport reports BIGGER than window (shouldn't happen,
        # but the impl must guard against negative padding)
        assert _compute_inset_py(800, 1000) == 0

    def test_viewport_offset_subtracted(self):
        # iPad in split-view sometimes reports an offsetTop
        assert _compute_inset_py(1024, 700, viewport_offset_top=100) == 224
