"""Tests for ``[ML] exclude_cids`` / ``exclude_cid_categories``.

Motivation: the usa_admin1 soybean 2025 fold selected ENSO teleconnection
scalars (``ONI_curr_MAM Oct 1-Oct 31`` at gOMP position 9) among its 53
features. ENSO indices are ONE VALUE PER HARVEST YEAR broadcast to every
region (cid/definitions.py:315), so they carry no within-year spatial signal
and can act as a year-identity proxy. These flags allow excluding them -- or
any CID family -- without touching ``use_cids``.

The filter runs on the FINISHED feature_names list, for the same reason
``filter_feature_names_cci`` does: with ``correlation_plots = False`` the
fallback assigns all CID columns directly and bypasses candidate-level hooks.
"""

import pytest

from geocif.ml.stages import (
    cid_category_map,
    filter_feature_names_exclude_cids,
    resolve_excluded_cids,
)

NAMES = [
    "ONI_curr_MAM Oct 1-Oct 31",
    "ONI_prev_JJA Oct 1-Oct 31",
    "MEI_curr_DJ Sep 1-Sep 30",
    "MEAN_CCI Sep 1-Sep 30",
    "MAX_CCIGE Aug 1-Jun 30",
    "AUC_NDVI Oct 1-Apr 30",
    "STD_ESI4WK Sep 1-Jun 30",
    "KDD Oct 1-Aug 31",
    "vDTR Jun 1-Jun 30",
    # engineered / structural columns must always survive
    "Region",
    "Region_ID",
    "Harvest Year",
    "t -3 Yield (tn per ha)",
    "lat",
    "lon",
]
STRUCTURAL = ["Region", "Region_ID", "Harvest Year",
              "t -3 Yield (tn per ha)", "lat", "lon"]


# ------------------------------------------------------------ category map
def test_category_map_knows_enso():
    m = cid_category_map()
    assert m.get("ONI_curr_MAM") == "ENSO"
    assert m.get("ONI_prev_JJA") == "ENSO"
    assert any(k.startswith("MEI_") for k in m)


def test_category_map_covers_other_families():
    m = cid_category_map()
    assert m.get("KDD") == "Heat"
    assert m.get("HD17") == "Cold"
    assert m.get("CDD") == "Drought"


# ------------------------------------------------------------ resolution
def test_resolve_category_expands_to_bases():
    drop, unmatched = resolve_excluded_cids(None, ["ENSO"])
    assert unmatched == []
    assert "ONI_curr_MAM" in drop and "ONI_prev_JJA" in drop
    # ENSO has 5 prev + 4 curr ONI and 5 prev + 4 curr MEI = 18
    assert len(drop) >= 10
    assert "KDD" not in drop and "MEAN_CCI" not in drop


@pytest.mark.parametrize("cat", ["ENSO", "enso", "  EnSo  "])
def test_resolve_category_case_insensitive(cat):
    drop, unmatched = resolve_excluded_cids(None, [cat])
    assert unmatched == []
    assert "ONI_curr_MAM" in drop


def test_resolve_explicit_cids_union_with_category():
    drop, _ = resolve_excluded_cids(["KDD"], ["ENSO"])
    assert "KDD" in drop and "ONI_curr_MAM" in drop


def test_resolve_reports_unmatched_category():
    """A typo must be reported, not silently excluded nothing."""
    drop, unmatched = resolve_excluded_cids(None, ["ENSOO"])
    assert unmatched == ["ENSOO"]
    assert not drop


def test_resolve_empty_is_empty():
    assert resolve_excluded_cids(None, None) == (set(), [])
    assert resolve_excluded_cids([], []) == (set(), [])


# ------------------------------------------------------------ filtering
def test_enso_names_dropped_others_kept():
    drop, _ = resolve_excluded_cids(None, ["ENSO"])
    out = filter_feature_names_exclude_cids(NAMES, drop)
    assert not [f for f in out if f.startswith(("ONI_", "MEI_"))]
    for keep in ("MEAN_CCI Sep 1-Sep 30", "AUC_NDVI Oct 1-Apr 30",
                 "KDD Oct 1-Aug 31", "vDTR Jun 1-Jun 30"):
        assert keep in out


def test_structural_columns_never_dropped():
    for cat in ("ENSO", "Heat", "Cold", "VI", "CCI", "Drought"):
        drop, _ = resolve_excluded_cids(None, [cat])
        out = filter_feature_names_exclude_cids(NAMES, drop)
        for s in STRUCTURAL:
            assert s in out, f"{s} dropped by category {cat}"


def test_explicit_single_cid_only_that_one():
    out = filter_feature_names_exclude_cids(NAMES, {"ONI_curr_MAM"})
    assert "ONI_curr_MAM Oct 1-Oct 31" not in out
    assert "ONI_prev_JJA Oct 1-Oct 31" in out
    assert len(out) == len(NAMES) - 1


def test_underscored_bases_matched_exactly_not_by_prefix():
    """MEAN_CCI must not drag MAX_CCIGE with it -- these are distinct bases."""
    out = filter_feature_names_exclude_cids(NAMES, {"MEAN_CCI"})
    assert "MEAN_CCI Sep 1-Sep 30" not in out
    assert "MAX_CCIGE Aug 1-Jun 30" in out


def test_empty_drop_set_is_noop():
    assert filter_feature_names_exclude_cids(NAMES, set()) == NAMES
    assert filter_feature_names_exclude_cids(NAMES, None) == NAMES


def test_unknown_base_removes_nothing():
    assert filter_feature_names_exclude_cids(NAMES, {"NOT_A_CID"}) == NAMES


def test_returns_new_list_not_mutating_input():
    original = list(NAMES)
    filter_feature_names_exclude_cids(NAMES, {"ONI_curr_MAM"})
    assert NAMES == original
