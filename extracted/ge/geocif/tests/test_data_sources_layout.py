"""Regression test for the agmet 'Data Sources' caption layout (0.4.919).

The body block is bottom-anchored and grows upward, and its line count varies
per run (the CHIRPS-GEFS forecast line and the FLDAS line appear
conditionally). A constant header y therefore collided with the top body line
once the USA figures reached 6 source lines. data_sources_header_y derives the
header position from the line count so the gap is constant for any body size.
"""
import pytest

from geocif.agmet.plot import (
    DATA_SOURCES_BODY_Y,
    DATA_SOURCES_LINESPACING,
    data_sources_header_y,
)

FIG_H_IN = 25.0  # agmet figures are 5000x2500 px
FS = 10.0


def _body_top(n_lines, fig_h=FIG_H_IN, fs=FS):
    line_h = (fs * DATA_SOURCES_LINESPACING) / (fig_h * 72.0)
    return DATA_SOURCES_BODY_Y + n_lines * line_h


@pytest.mark.parametrize("n_lines", [3, 4, 5, 6, 7, 9])
def test_header_never_overlaps_body(n_lines):
    y = data_sources_header_y(n_lines, FIG_H_IN, FS)
    assert y > _body_top(n_lines), f"header overlaps body at {n_lines} lines"


def test_gap_is_constant_across_line_counts():
    gaps = [
        data_sources_header_y(n, FIG_H_IN, FS) - _body_top(n)
        for n in (4, 5, 6, 7)
    ]
    assert max(gaps) - min(gaps) < 1e-12


def test_header_rises_with_more_lines():
    ys = [data_sources_header_y(n, FIG_H_IN, FS) for n in (4, 5, 6)]
    assert ys[0] < ys[1] < ys[2]


def test_scales_with_figure_height():
    # a shorter figure => each line is a larger fraction => header sits higher
    tall = data_sources_header_y(6, 25.0, FS)
    short = data_sources_header_y(6, 12.5, FS)
    assert short > tall


def test_header_above_body_anchor():
    assert data_sources_header_y(1, FIG_H_IN, FS) > DATA_SOURCES_BODY_Y
