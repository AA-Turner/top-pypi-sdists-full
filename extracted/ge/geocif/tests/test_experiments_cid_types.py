"""cid_ablation with use_cids = ['all'] runs every CID type a project can have,
and each CID keeps one colour across the bar chart and the by-year lines."""

import pytest

ex = pytest.importorskip("geocif.experiments")


def test_all_cid_types_include_etref():
    # dict_etref was missing from the 'all' lists, so a poppy all-types
    # ablation silently ran without ETREF.
    assert "ETREF" in ex._all_cid_types()
    assert any(k.endswith("ETREF") for k in ex._all_cid_indices())


def test_cid_colours_are_fixed_per_name_and_distinct():
    names = ["VI", "Heat", "All CIDs", "Rain", "ETREF"]
    colours = ex._cid_colors(names)
    assert "All CIDs" not in colours  # drawn in black
    assert colours == ex._cid_colors(list(reversed(names)))  # order-free
    assert len(set(colours.values())) == len(colours)
    assert len(set(ex._FIXED_PALETTE[:13])) == 13  # 13 CID types, 13 hues
