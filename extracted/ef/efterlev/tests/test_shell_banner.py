"""Tests for the shell banner — verifies basic shape invariants."""

from __future__ import annotations

from efterlev.shell.banner import BANNER_LINES, render_banner


def test_banner_is_five_rows() -> None:
    """Banner is 5 rows (figlet standard font; v0.1.133 final form)."""
    assert len(BANNER_LINES) == 5


def test_banner_fits_in_80_columns() -> None:
    """No banner row should exceed 80 visible columns (Unicode chars count as 1)."""
    for row in BANNER_LINES:
        assert len(row) <= 80, f"row too wide ({len(row)}): {row!r}"


def test_banner_rows_are_consistent_width() -> None:
    """All rows are padded to the same width so terminal renderers don't shift baselines.

    The visible CONTENT can taper (e.g. V's pointed bottom), but the underlying
    string must be uniform-width so the layout module doesn't apply any
    per-row adjustment.
    """
    widths = {len(r) for r in BANNER_LINES}
    assert len(widths) == 1, f"inconsistent widths (rstrip trailing spaces?): {widths}"


def test_render_banner_returns_string_with_newlines() -> None:
    out = render_banner()
    assert isinstance(out, str)
    assert out.count("\n") == 4  # 5 rows = 4 newlines between them
