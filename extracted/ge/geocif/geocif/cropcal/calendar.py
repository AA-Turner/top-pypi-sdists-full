# -*- coding: utf-8 -*-
"""GEOGLAM Crop Monitor calendar: workbook -> four transition days per region.

Each row of a crop sheet is one calendar region and 24 fortnightly growth-stage
codes, ``jan_1 ... dec_15``. This module turns that row into the four days the
validation compares against:

``plant`` -> ``midgreenup`` -> ``midgreendown`` -> ``harvest``

where **midgreenup is the end of stage 1** and **midgreendown is the end of
stage 2**.

Stage codes
-----------
``GlobalCM_2026-09-11.xlsx`` uses ``-1, 0, 1, 2, 3, 4``, where ``-1`` means the
crop is not grown in that region and **both ``0`` and ``4`` are out of season**.
Codes ``1``, ``2`` and ``3`` are the three growth stages of the older
``AMISCM``/``EWCM`` workbooks, so those are folded onto the legacy ``0/1/2/3``
alphabet up front (:func:`to_legacy_codes`) and every branch below is the
original's, unchanged. That keeps this reader valid for both workbook
generations, which the reference comparison in the test suite relies on.

Two day-of-year conventions
---------------------------
The original converts a fortnight index to a day with a flat ``index * 15``,
which makes the GEOGLAM year 360 days long and drifts up to five days late by
December. geocif already has a true month-half conversion in
:mod:`geocif.aquacrop.calendar`. Both are produced: :class:`StageDates` carries
bin indices, and :func:`to_days` renders them under either convention. The
legacy one exists so published thresholds stay comparable; the calendar one is
the default for new work.
"""
from __future__ import annotations

import datetime as _dt
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd

from geocif.aquacrop.calendar import BIMONTH_COLS, _bin_to_doy
from geocif.cropcal import naming

logger = logging.getLogger(__name__)

N_BINS = 24

#: Raw workbook codes.
CODE_NOT_GROWN = -1
CODE_OFF_SEASON = 0
CODE_STAGE_1 = 1
CODE_STAGE_2 = 2
CODE_STAGE_3 = 3
CODE_POST_HARVEST = 4

#: Days per fortnight bin under the original's flat convention.
LEGACY_DAYS_PER_BIN = 15

#: Reference year for the true-calendar convention. Non-leap, so December 15
#: through 31 is the longest bin at 17 days and the year ends on day 365,
#: matching the 365-day period used by :mod:`geocif.cropcal.circular`.
REFERENCE_YEAR = 2001

#: Column aliases across workbook generations: GlobalCM (new) and AMISCM/EWCM.
_KEY_COLS = ("Key", "Admin2")
_NAME_COLS = ("Name", "admin")
_COUNTRY_COLS = ("Country", "Country2")


class CalendarError(ValueError):
    """A calendar row that cannot be turned into four transition days."""


# --------------------------------------------------------------------------
# Codes
# --------------------------------------------------------------------------
def to_legacy_codes(flags: Iterable[float]) -> np.ndarray:
    """Fold the six-value workbook alphabet onto the legacy ``0/1/2/3``.

    ``4`` (post-harvest) becomes ``0`` (out of season) per the project ruling;
    ``-1`` is preserved so :func:`is_not_grown` can still tell "crop absent"
    from "off season"; NaN becomes ``0``, matching the original's treatment of
    blank cells.
    """
    arr = np.asarray(list(flags), dtype=float)
    arr = np.where(np.isnan(arr), float(CODE_OFF_SEASON), arr)
    arr = np.where(arr == CODE_POST_HARVEST, float(CODE_OFF_SEASON), arr)
    return arr.astype(int)


def is_not_grown(flags: np.ndarray) -> bool:
    """Is this the all-``-1`` sentinel meaning the crop is absent here?"""
    return bool(np.all(np.asarray(flags) == CODE_NOT_GROWN))


def _first(arr: np.ndarray, value: int) -> Optional[int]:
    hits = np.flatnonzero(arr == value)
    return int(hits[0]) if hits.size else None


def _last(arr: np.ndarray, value: int) -> Optional[int]:
    hits = np.flatnonzero(arr == value)
    return int(hits[-1]) if hits.size else None


def _count_blocks(arr: np.ndarray, value: int) -> int:
    """Number of contiguous runs of ``value``, treating the array as circular."""
    mask = (arr == value).astype(int)
    if mask.sum() in (0, mask.size):
        return int(mask.sum() > 0)
    return int(sum(1 for i in np.flatnonzero(mask) if mask[(i - 1) % mask.size] == 0))


# --------------------------------------------------------------------------
# 24 codes -> four bins
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class StageDates:
    """The four transitions, as fortnight bin indices plus stage lengths.

    ``plant_bin`` is read at the *start* of its bin; the other three are read at
    the *end* of theirs. Rendering to days is :func:`to_days`.

    Indices are stored **unwrapped**: two branches can legitimately produce
    ``-1`` (the bin before ``jan_1``) or ``24`` (the bin after ``dec_15``), and
    the legacy renderer depends on that. ``-1`` renders to day 0 and ``24`` to
    day 360, exactly as the original computed them. Only the calendar renderer
    takes them modulo 24.
    """

    plant_bin: int
    midgreenup_bin: int
    midgreendown_bin: int
    harvest_bin: int
    len_stage1_bins: int
    len_stage2_bins: int
    len_stage3_bins: int
    wraps_year: bool
    #: No off-season bin at all. The parser then defines planting as "the bin
    #: after harvest" (see :func:`stage_bins`), so the planting and harvest
    #: days of such a row are an artefact of the parser, not a calendar
    #: assertion. Carried so the model evaluation can exclude them.
    wall_to_wall: bool = False


def stage_bins(codes: np.ndarray) -> StageDates:
    """Locate the four transitions in a 24-bin legacy-code row.

    The four branches are the original's
    (``util_cal.get_geoglam_calendar_info``), discriminated on whether the
    stage-2 block touches ``jan_1``, ``dec_15``, both, or neither. Positions are
    plain 0..23 indices here because the row has already been reduced to its 24
    code columns; the original compared against the column positions of
    ``jan_1``/``dec_15`` inside a wider merged frame, which is the same thing.

    Raises:
        CalendarError: when a required stage is missing or the row is the
            all-``-1`` sentinel.
    """
    codes = np.asarray(codes, dtype=int)
    if codes.size != N_BINS:
        raise CalendarError(f"expected {N_BINS} stage codes, got {codes.size}")
    if is_not_grown(codes):
        raise CalendarError("crop not grown in this region (all -1)")

    first_col, last_col = 0, N_BINS - 1

    first_1, last_1 = _first(codes, CODE_STAGE_1), _last(codes, CODE_STAGE_1)
    first_2, last_2 = _first(codes, CODE_STAGE_2), _last(codes, CODE_STAGE_2)
    first_3, last_3 = _first(codes, CODE_STAGE_3), _last(codes, CODE_STAGE_3)
    first_0, last_0 = _first(codes, CODE_OFF_SEASON), _last(codes, CODE_OFF_SEASON)

    missing = [n for n, v in (("1", first_1), ("2", first_2), ("3", first_3)) if v is None]
    if missing:
        raise CalendarError(f"row has no stage {'/'.join(missing)} bins")

    if first_2 == first_col and last_2 == last_col:
        # Stage 2 spans both ends: the season wraps and stage 2 is split.
        #   2 2 2 3 3 3 0 0 1 1 1 2 2
        midgreenup_bin = last_1
        midgreendown_bin = first_3 - 1
        plant_bin = first_1
        harvest_bin = last_3
    elif last_2 == last_col:
        #   3 3 3 1 1 1 1 2 2 2 2 2
        midgreenup_bin = last_1
        midgreendown_bin = first_3 - 1
        plant_bin = first_1
        harvest_bin = last_3
    elif first_2 == first_col:
        #   2 2 2 3 3 3 0 0 0 1 1 1
        midgreenup_bin = last_1
        midgreendown_bin = last_2
        plant_bin = first_1
        harvest_bin = last_3
    else:
        # Season contained within the year.
        #   0 0 1 1 1 2 2 2 2 3 3 0 0
        midgreenup_bin = first_2 - 1
        midgreendown_bin = last_2
        if first_0 is None:
            # No off-season bins at all: the row is wall-to-wall season.
            plant_bin = last_3 + 1
            harvest_bin = last_3
        elif first_3 == first_col and last_3 == last_col:
            #   3 3 0 0 0 1 1 1 2 2 2 3 3
            plant_bin = last_0 + 1
            harvest_bin = first_0 - 1
        else:
            plant_bin = first_1
            harvest_bin = last_3

    bins = StageDates(
        plant_bin=int(plant_bin),
        midgreenup_bin=int(midgreenup_bin),
        midgreendown_bin=int(midgreendown_bin),
        harvest_bin=int(harvest_bin),
        len_stage1_bins=int(np.count_nonzero(codes == CODE_STAGE_1)),
        len_stage2_bins=int(np.count_nonzero(codes == CODE_STAGE_2)),
        len_stage3_bins=int(np.count_nonzero(codes == CODE_STAGE_3)),
        wraps_year=bool(codes[first_col] in (CODE_STAGE_1, CODE_STAGE_2, CODE_STAGE_3)
                        and codes[last_col] in (CODE_STAGE_1, CODE_STAGE_2, CODE_STAGE_3)),
        wall_to_wall=bool(first_0 is None),
    )
    return bins


def split_stage_blocks(codes: np.ndarray) -> dict[int, int]:
    """How many separate runs each stage forms. Any value > 1 is malformed.

    One Spring Wheat row in ``GlobalCM_2026-09-11.xlsx`` has a split block; the
    caller records it as a skip reason rather than silently taking the first
    and last occurrence across the gap.
    """
    codes = np.asarray(codes, dtype=int)
    return {stage: _count_blocks(codes, stage) for stage in (1, 2, 3)}


# --------------------------------------------------------------------------
# Bins -> days
# --------------------------------------------------------------------------
def to_days(bins: StageDates, *, convention: str = "calendar") -> dict[str, int]:
    """Render :class:`StageDates` as days of year.

    Args:
        bins: output of :func:`stage_bins`.
        convention: ``"calendar"`` uses real month halves via
            :func:`geocif.aquacrop.calendar._bin_to_doy` (a 365-day year);
            ``"legacy"`` reproduces the original's flat ``index * 15``
            (a 360-day year).

    Returns:
        ``{plant, midgreenup, midgreendown, harvest, len_stage1..3}`` in days.
    """
    if convention == "legacy":
        return {
            "plant": bins.plant_bin * LEGACY_DAYS_PER_BIN,
            "midgreenup": (bins.midgreenup_bin + 1) * LEGACY_DAYS_PER_BIN,
            "midgreendown": (bins.midgreendown_bin + 1) * LEGACY_DAYS_PER_BIN,
            "harvest": (bins.harvest_bin + 1) * LEGACY_DAYS_PER_BIN,
            "len_stage1": bins.len_stage1_bins * LEGACY_DAYS_PER_BIN,
            "len_stage2": bins.len_stage2_bins * LEGACY_DAYS_PER_BIN,
            "len_stage3": bins.len_stage3_bins * LEGACY_DAYS_PER_BIN,
        }
    if convention != "calendar":
        raise ValueError(f"unknown convention {convention!r}")

    year = REFERENCE_YEAR
    return {
        "plant": _bin_to_doy(bins.plant_bin % N_BINS, year, edge="start"),
        "midgreenup": _bin_to_doy(bins.midgreenup_bin % N_BINS, year, edge="end"),
        "midgreendown": _bin_to_doy(bins.midgreendown_bin % N_BINS, year, edge="end"),
        "harvest": _bin_to_doy(bins.harvest_bin % N_BINS, year, edge="end"),
        "len_stage1": _bin_days(bins.len_stage1_bins),
        "len_stage2": _bin_days(bins.len_stage2_bins),
        "len_stage3": _bin_days(bins.len_stage3_bins),
    }


def _bin_days(n_bins: int) -> int:
    """Mean real length of ``n_bins`` fortnights (365 / 24 ~= 15.2 days)."""
    return int(round(n_bins * 365.0 / N_BINS))


# --------------------------------------------------------------------------
# Workbook I/O
# --------------------------------------------------------------------------
def _resolve_column(columns, candidates, what: str) -> str:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    raise CalendarError(
        f"no {what} column: looked for {candidates}, have {list(columns)[:8]}"
    )


def read_sheet(path: Path | str, sheet: str) -> pd.DataFrame:
    """One crop sheet as ``key, country, region, code_0 .. code_23``.

    Works on both workbook generations. ``key`` is alias-resolved and cleaned,
    so it joins directly against the region shapefile's ``Key``.
    """
    raw = pd.read_excel(path, sheet_name=sheet)
    key_col = _resolve_column(raw.columns, _KEY_COLS, "join-key")
    name_col = _resolve_column(raw.columns, _NAME_COLS, "region-name")
    country_col = _resolve_column(raw.columns, _COUNTRY_COLS, "country")
    missing = [c for c in BIMONTH_COLS if c not in raw.columns]
    if missing:
        raise CalendarError(f"sheet {sheet!r} missing half-month columns: {missing[:5]}")

    out = pd.DataFrame(
        {
            "country": raw[country_col].map(naming.resolve_country),
            "region": [
                naming.resolve_region(c, n)
                for c, n in zip(raw[country_col], raw[name_col])
            ],
        }
    )
    out["key"] = [
        naming.resolve_key(c, n) for c, n in zip(raw[country_col], raw[name_col])
    ]
    out["country_slug"] = out["country"].map(naming.country_slug)
    # The workbook's own key column is kept only to assert it agrees with the
    # rebuilt one; see tests/test_cropcal_calendar.py.
    out["key_raw"] = raw[key_col].map(naming.clean_text)
    codes = raw[BIMONTH_COLS].to_numpy(dtype=float)
    for i in range(N_BINS):
        out[f"code_{i}"] = codes[:, i]

    # Blank country/region cells (the shipped EWCM workbook has a few, and the
    # 2025-11 region file carried an "N/A N/A" row) produce an empty key, which
    # would join to nothing and then be reported as a missing region rather than
    # as a defective source row. Drop them here and say so.
    blank = out["key"].str.strip().eq("") | out["country"].str.strip().eq("")
    if blank.any():
        logger.warning(
            f"sheet {sheet!r}: dropping {int(blank.sum())} row(s) with a blank "
            f"country or region name"
        )
        out = out.loc[~blank].reset_index(drop=True)
    return out


def read_workbook(path: Path | str) -> dict[naming.CropSeason, pd.DataFrame]:
    """Every crop sheet of a calendar workbook, keyed by ``(crop, season)``."""
    path = Path(path)
    with pd.ExcelFile(path) as book:
        sheets = list(book.sheet_names)
    out: dict[naming.CropSeason, pd.DataFrame] = {}
    for sheet in sheets:
        crop_season = naming.parse_sheet_name(sheet)
        out[crop_season] = read_sheet(path, sheet)
    logger.info(f"calendar {path.name}: {len(out)} crop-season sheet(s)")
    return out


def code_columns(frame: pd.DataFrame) -> list[str]:
    """The 24 stage-code column names produced by :func:`read_sheet`."""
    return [f"code_{i}" for i in range(N_BINS)]


def row_stage_days(
    row: pd.Series, *, convention: str = "calendar"
) -> tuple[Optional[dict[str, int]], Optional[StageDates], Optional[str]]:
    """``(days, bins, skip_reason)`` for one row of a :func:`read_sheet` frame.

    Never raises: a malformed row comes back as ``(None, None, reason)`` so the
    caller can record it and carry on. Split stage blocks are rejected here,
    because the first/last-occurrence logic in :func:`stage_bins` would
    otherwise silently span the gap.
    """
    raw = row[[f"code_{i}" for i in range(N_BINS)]].to_numpy(dtype=float)
    if is_not_grown(raw):
        return None, None, "crop not grown"
    if np.any(raw == CODE_NOT_GROWN):
        return None, None, "partial -1 sentinel (crop grown in only part of the year)"

    codes = to_legacy_codes(raw)
    blocks = split_stage_blocks(codes)
    split = [str(stage) for stage, count in blocks.items() if count > 1]
    if split:
        return None, None, f"stage {'/'.join(split)} block is not contiguous"

    try:
        bins = stage_bins(codes)
    except CalendarError as exc:
        return None, None, str(exc)
    return to_days(bins, convention=convention), bins, None
