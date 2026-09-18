"""The calendar half of the crop-calendar validator.

Two things are pinned here.

**Fidelity.** ``geocif.cropcal.calendar`` must reproduce the original
``GEOGLAM/Code/Code/CropCalendar/util_cal.py::get_geoglam_calendar_info``
exactly under the ``legacy`` day convention, on both workbook generations. The
original is re-implemented verbatim in :func:`reference_stage_days` below so the
comparison does not depend on the GEOGLAM repo being present. Measured when this
was written: 1546/1546 rows of ``GlobalCM_2026-09-11.xlsx``, 519/519 of
``AMISCM_2026-01-05.xlsx`` and 923/923 of ``EWCM_2026-01-05.xlsx`` agree, with
all four year-wrap branches exercised in each.

**Robustness.** A malformed row must come back as a recorded skip reason, never
an exception and never a silently wrong date -- ``GlobalCM_2026-09-11.xlsx``
ships two such rows.

The workbook-driven tests skip when the files are not on this machine, so the
table-driven ones still guard the branch logic in a bare checkout.
"""

from pathlib import Path

import numpy as np
import pytest

from geocif.cropcal import calendar as cal
from geocif.cropcal import naming

# --------------------------------------------------------------------------
# Workbooks, if present
# --------------------------------------------------------------------------
_WORKBOOKS = {
    "GlobalCM_2026-09-11": Path(r"C:/Users/ritvik/Downloads/GlobalCM_2026-09-11.xlsx"),
    "AMISCM_2026-01-05": Path(
        r"D:/Users/ritvik/projects/GEO/inputs/metadata/crop_calendars/AMISCM_2026-01-05.xlsx"
    ),
    "EWCM_2026-01-05": Path(
        r"D:/Users/ritvik/projects/GEO/inputs/metadata/crop_calendars/EWCM_2026-01-05.xlsx"
    ),
}


# --------------------------------------------------------------------------
# Verbatim re-implementation of the original, for the fidelity comparison
# --------------------------------------------------------------------------
def _pos(arr, val, occurrence="first"):
    """``util_cal.get_position_in_array``, including its bare-except -> NaN."""
    try:
        if occurrence == "first":
            return np.where(arr.squeeze() == val)[0][0]
        return np.where(arr.squeeze() == val)[0][-1]
    except Exception:  # noqa: BLE001 - reproducing the original's bare except
        return np.nan


def reference_stage_days(vals):
    """``util_cal.get_geoglam_calendar_info`` with ``col_jan=0``, ``col_dec=23``.

    Takes a 24-long float array of legacy ``0/1/2/3`` codes and returns the same
    keys :func:`geocif.cropcal.calendar.to_days` produces.
    """
    col_jan, col_dec = 0, 23
    mid_start = _pos(vals, 2.0, "first")
    mid_last = _pos(vals, 2.0, "last")
    no_season = _pos(vals, 0.0, "first")

    if mid_start == col_jan and mid_last == col_dec:
        green, down = _pos(vals, 1.0, "last"), _pos(vals, 3.0, "first")
        plant, harvest = _pos(vals, 1.0, "first"), _pos(vals, 3.0, "last")
    elif mid_last == col_dec:
        green, down = _pos(vals, 1.0, "last"), _pos(vals, 3.0, "first")
        plant, harvest = _pos(vals, 1.0, "first"), _pos(vals, 3.0, "last")
    elif mid_start == col_jan and mid_last < col_dec:
        green, down = _pos(vals, 1.0, "last"), _pos(vals, 2.0, "last") + 1
        plant, harvest = _pos(vals, 1.0, "first"), _pos(vals, 3.0, "last")
    else:
        green, down = _pos(vals, 2.0, "first") - 1, _pos(vals, 2.0, "last") + 1
        if np.isnan(no_season):
            plant, harvest = _pos(vals, 3.0, "last") + 1, _pos(vals, 3.0, "last")
        elif _pos(vals, 3.0, "first") == col_jan and _pos(vals, 3.0, "last") == col_dec:
            plant, harvest = _pos(vals, 0.0, "last") + 1, _pos(vals, 0.0, "first") - 1
        else:
            plant, harvest = _pos(vals, 1.0, "first"), _pos(vals, 3.0, "last")

    return {
        "plant": (plant - col_jan) * 15,
        "midgreenup": (green - col_jan + 1) * 15,
        "midgreendown": (down - col_jan) * 15,
        "harvest": (harvest - col_jan + 1) * 15,
        "len_stage1": np.count_nonzero(vals == 1.0) * 15,
        "len_stage2": np.count_nonzero(vals == 2.0) * 15,
        "len_stage3": np.count_nonzero(vals == 3.0) * 15,
    }


def _branch(codes):
    """Which of the four wrap branches a row takes, for coverage assertions."""
    first_2, last_2 = cal._first(codes, 2), cal._last(codes, 2)
    if first_2 == 0 and last_2 == 23:
        return "A_both_ends"
    if last_2 == 23:
        return "B_ends_dec"
    if first_2 == 0:
        return "C_starts_jan"
    return "D_contained"


# --------------------------------------------------------------------------
# Table-driven branch coverage (no workbook needed)
# --------------------------------------------------------------------------
def _codes(spec):
    """``"0011222330"``-style spec padded to 24 bins with trailing zeros."""
    arr = [int(c) for c in spec]
    assert len(arr) <= cal.N_BINS
    return np.array(arr + [0] * (cal.N_BINS - len(arr)), dtype=int)


# (label, 24 codes, expected branch)
_BRANCH_CASES = [
    # Season contained inside the year: 0 0 1 1 1 2 2 2 2 3 3 0 ...
    ("contained", _codes("001112222330"), "D_contained"),
    # Stage 2 runs to dec_15 and continues as stage 3 in January.
    ("ends_dec", _codes("333111111122222222222222"[:24]), "B_ends_dec"),
    # Stage 2 starts at jan_1 and the season closes before dec_15.
    ("starts_jan", _codes("222333000111000000000000"), "C_starts_jan"),
    # Stage 2 touches both ends: the block is split across the new year.
    ("both_ends", _codes("222333001110000000000022"), "A_both_ends"),
]


@pytest.mark.parametrize("label,codes,expected_branch", _BRANCH_CASES,
                         ids=[c[0] for c in _BRANCH_CASES])
def test_branch_matches_reference(label, codes, expected_branch):
    """Every wrap branch reproduces the original's legacy day numbers."""
    assert _branch(codes) == expected_branch
    bins = cal.stage_bins(codes)
    got = cal.to_days(bins, convention="legacy")
    want = reference_stage_days(codes.astype(float))
    assert got == want, f"{label}: {got} != {want}"


def test_post_harvest_code_is_out_of_season():
    """Code 4 folds onto 0, so 1/2/3 keep the original meaning.

    This is the project ruling for ``GlobalCM_2026-09-11.xlsx``: ``-1`` is
    "crop not grown", ``0`` and ``4`` are both out of season.
    """
    with_four = _codes("001112222334400000000000")
    with_zero = _codes("001112222330000000000000")
    assert np.array_equal(cal.to_legacy_codes(with_four), with_zero)
    assert cal.to_days(cal.stage_bins(cal.to_legacy_codes(with_four))) == cal.to_days(
        cal.stage_bins(with_zero)
    )


def test_not_grown_sentinel_is_not_off_season():
    """An all -1 row is "crop absent", which must not be read as day 0."""
    assert cal.is_not_grown(np.full(cal.N_BINS, -1))
    assert not cal.is_not_grown(_codes("001112222330"))
    with pytest.raises(cal.CalendarError):
        cal.stage_bins(np.full(cal.N_BINS, -1))


def test_split_stage_block_is_rejected():
    """A non-contiguous stage must skip, not span the gap.

    ``stage_bins`` works from first/last occurrence, so a split block would
    silently produce a season stretching across the hole. One Spring Wheat row
    in the shipped workbook is like this.
    """
    split = _codes("011011222330")
    assert cal.split_stage_blocks(split)[1] == 2
    row = _row_from_codes(split)
    days, bins, reason = cal.row_stage_days(row)
    assert days is None and bins is None
    assert "not contiguous" in reason


def test_partial_not_grown_sentinel_is_rejected():
    """A row mixing -1 with real stages is malformed, not a short season."""
    codes = _codes("001112222330").astype(float)
    codes[20] = -1
    row = _row_from_codes(codes)
    days, _bins, reason = cal.row_stage_days(row)
    assert days is None and "-1" in reason


def _row_from_codes(codes):
    import pandas as pd

    return pd.Series({f"code_{i}": float(v) for i, v in enumerate(codes)})


# --------------------------------------------------------------------------
# Day conventions
# --------------------------------------------------------------------------
def test_legacy_and_calendar_conventions_preserve_ordering():
    """Both conventions order the four transitions identically."""
    codes = _codes("001112222330")
    bins = cal.stage_bins(codes)
    legacy = cal.to_days(bins, convention="legacy")
    calendar = cal.to_days(bins, convention="calendar")
    for days in (legacy, calendar):
        assert days["plant"] < days["midgreenup"] < days["midgreendown"] <= days["harvest"]


def test_legacy_convention_drifts_early_through_the_year():
    """Legacy packs the year into 24x15 = 360 days, so it runs progressively
    early against the real calendar.

    The gap is not monotone -- a ``<month>_1`` bin ends on day 14, which can be
    *earlier* than the flat estimate in the first half of the year -- so the
    contract is a bounded divergence that is clearly positive by December, not
    ``calendar >= legacy`` everywhere.
    """
    from geocif.aquacrop.calendar import _bin_to_doy

    gaps = [
        _bin_to_doy(b, cal.REFERENCE_YEAR, edge="end") - (b + 1) * cal.LEGACY_DAYS_PER_BIN
        for b in range(cal.N_BINS)
    ]
    assert min(gaps) == -2 and max(gaps) == 5
    assert gaps[-1] == 5, "dec_15 should end on day 365 against a legacy 360"
    assert sum(gaps[:12]) < sum(gaps[12:]), "drift should accumulate through the year"


def test_unwrapped_bins_survive_to_the_legacy_renderer():
    """``plant_bin`` may legitimately be 24 and render to day 360, not day 0.

    A row with no off-season bins at all takes the "wall-to-wall season" branch,
    where the original computes ``plant = last_3 + 1``. Modding that to 0 early
    would move planting by a full year in the delta.
    """
    codes = _codes("111122222222222233333333")
    bins = cal.stage_bins(codes)
    assert bins.plant_bin == cal.N_BINS
    assert cal.to_days(bins, convention="legacy")["plant"] == 360
    assert reference_stage_days(codes.astype(float))["plant"] == 360


# --------------------------------------------------------------------------
# Whole-workbook fidelity
# --------------------------------------------------------------------------
@pytest.mark.parametrize("name", sorted(_WORKBOOKS))
def test_workbook_matches_reference(name):
    """Every scorable row of every shipped workbook matches the original."""
    path = _WORKBOOKS[name]
    if not path.is_file():
        pytest.skip(f"{name} not available on this machine")

    sheets = cal.read_workbook(path)
    branches, mismatches, skipped, scored = set(), [], 0, 0

    for crop_season, frame in sheets.items():
        if crop_season.crop == "rangelands":
            continue  # codes 0/1 only -- no growth stages to locate
        for _, row in frame.iterrows():
            raw = row[cal.code_columns(frame)].to_numpy(dtype=float)
            if cal.is_not_grown(raw):
                continue
            days, _bins, reason = cal.row_stage_days(row, convention="legacy")
            if reason is not None:
                skipped += 1
                continue
            scored += 1
            codes = cal.to_legacy_codes(raw)
            branches.add(_branch(codes))
            want = reference_stage_days(codes.astype(float))
            if days != want:
                mismatches.append((crop_season, row["key"], days, want))

    assert scored > 0, f"{name}: no rows scored"
    assert not mismatches, (
        f"{name}: {len(mismatches)} row(s) differ from the original, "
        f"first: {mismatches[0]}"
    )
    assert branches == {"A_both_ends", "B_ends_dec", "C_starts_jan", "D_contained"}, (
        f"{name}: only exercised {sorted(branches)}"
    )
    # A skip must always be a deliberate, explained one -- never the norm.
    assert skipped <= 0.02 * (scored + skipped), (
        f"{name}: {skipped} of {scored + skipped} rows skipped"
    )


def test_globalcm_defect_count_is_known():
    """The two known defective rows in the current workbook, pinned.

    If a future calendar drop changes this number, the audit report needs
    re-reading rather than the threshold moving.
    """
    path = _WORKBOOKS["GlobalCM_2026-09-11"]
    if not path.is_file():
        pytest.skip("GlobalCM_2026-09-11 not available on this machine")

    reasons = []
    for crop_season, frame in cal.read_workbook(path).items():
        if crop_season.crop == "rangelands":
            continue
        for _, row in frame.iterrows():
            raw = row[cal.code_columns(frame)].to_numpy(dtype=float)
            if cal.is_not_grown(raw):
                continue
            _days, _bins, reason = cal.row_stage_days(row)
            if reason is not None:
                reasons.append(reason)

    assert len(reasons) == 2, f"expected 2 defective rows, found {len(reasons)}: {reasons}"
    assert any("not contiguous" in r for r in reasons)
    assert any("-1" in r for r in reasons)


@pytest.mark.parametrize("name", sorted(_WORKBOOKS))
def test_rebuilt_key_agrees_with_the_workbook_column(name):
    """``"<Name> <Country>"`` reconstructs the workbook's own key column.

    Both files are joined on this string, so a drift between the stored key and
    the rebuilt one would silently drop regions.
    """
    path = _WORKBOOKS[name]
    if not path.is_file():
        pytest.skip(f"{name} not available on this machine")

    frame = next(iter(cal.read_workbook(path).values()))
    # Aliased rows are expected to differ -- that is the point of the alias.
    aliased = {naming.resolve_key(c, n) for c, n in
               [("East Timor\u00a0(Timor-Leste)", "East Timor\u00a0(Timor-Leste)"),
                ("Gaza & the West Bank", "Gaza & the West Bank")]}
    drift = frame.loc[
        (frame["key"] != frame["key_raw"]) & ~frame["key"].isin(aliased), ["key", "key_raw"]
    ]
    assert drift.empty, f"{name}: rebuilt key differs from stored key:\n{drift.head()}"
