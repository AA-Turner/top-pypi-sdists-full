"""
calendar.py — derive planting/harvest dates per calendar_region from the
existing geocif calendar Excel (EWCM_*.xlsx / AMISCM_*.xlsx).

The calendar Excel uses bi-monthly flags in columns
``jan_1, jan_15, feb_1, feb_15, ..., dec_1, dec_15`` (24 columns, two
periods per month: ``<mon>_1`` covers days 1-14, ``<mon>_15`` covers
days 15-end-of-month). Flag values:
    1 = season start (planting window)
    2 = mid-season
    3 = season end (harvest window)
    4 = off-season

Older variants of this loader (pre-0.4.661) assumed 36 dekad columns
(``<mon>_{1,2,3}``); the actual EWCM/AMISCM files have been bi-monthly
the whole time. See git history for the dekad→bi-monthly migration.

We expose:
    load_calendar(parser, country, crop, season)
        → DataFrame with [calendar_region, planting_date, harvest_date,
          growing_days] rows (one per calendar_region in the country).

    planting_doy(row) / harvest_doy(row)
        Helpers returning Python date objects for a given simulation year.

Convention note: the *first* dekad flagged 1 within a contiguous in-season
block is the planting window start; the *last* dekad flagged 3 in the same
block is the harvest. If multiple disjoint blocks exist (multi-season),
the season number (1 = primary, 2 = secondary) picks the block — matching
the geomerge.read_calendar / utils.get_cal_list convention.
"""

from __future__ import annotations

import datetime as _dt
import logging
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# Bi-monthly columns in the calendar Excel, in chronological order.
_MONTHS = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec",
]
BIMONTH_COLS: list[str] = [f"{m}_{d}" for m in _MONTHS for d in (1, 15)]
# 24 bins. Bin k (0..23) maps to (month=k//2+1, half=k%2): half 0 covers
# days 1-14 of the month, half 1 covers days 15..last-day-of-month.

# Flag semantics in the dekad columns
FLAG_START = 1
FLAG_MID = 2
FLAG_END = 3
FLAG_OFF = 4


def _bin_to_doy(bin_idx: int, year: int, *, edge: str = "start") -> int:
    """Convert bi-monthly bin index (0..23) to a day-of-year.

    Bin layout: ``<month>_1`` covers days 1-14, ``<month>_15`` covers
    day 15 through the last day of the month.

    ``edge='start'`` → first day of the bin.
    ``edge='end'``   → last day of the bin.
    """
    month = bin_idx // 2 + 1   # 1..12
    within = bin_idx % 2       # 0 or 1

    if within == 0:
        day = 1 if edge == "start" else 14
    else:
        if edge == "start":
            day = 15
        else:
            # Last day of the month
            if month == 12:
                next_month = _dt.date(year + 1, 1, 1)
            else:
                next_month = _dt.date(year, month + 1, 1)
            day = (next_month - _dt.timedelta(days=1)).day

    return _dt.date(year, month, day).timetuple().tm_yday


def _resolve_calendar_path(parser, country: str) -> Path:
    """Resolve the calendar Excel path for a country.

    Reads ``dir_crop_calendars`` from [PATHS] and ``calendar_file`` from
    the per-country section in countries.txt.
    """
    dir_calendars = Path(parser.get("PATHS", "dir_crop_calendars"))
    fname = parser.get(country, "calendar_file")
    return dir_calendars / fname


def _find_season_blocks(flags: np.ndarray) -> list[tuple[int, int]]:
    """Find contiguous in-season blocks in a 24-bin flag vector.

    A block is a maximal run of dekads with flag in {1, 2, 3}. Returns
    a list of (start_bin_idx, end_bin_idx) tuples, sorted by the bin
    that contains the FLAG_START sentinel (so block ordering matches the
    biological season order, not calendar position — important for seasons
    wrapping the year boundary).
    """
    in_season = (flags >= FLAG_START) & (flags <= FLAG_END)
    blocks: list[tuple[int, int]] = []
    i = 0
    n = len(flags)
    while i < n:
        if in_season[i]:
            j = i
            while j < n and in_season[j]:
                j += 1
            blocks.append((i, j - 1))
            i = j
        else:
            i += 1

    # Handle wraparound: if first and last dekads are both in-season,
    # merge them into a single block crossing the year boundary.
    if len(blocks) >= 2 and blocks[0][0] == 0 and blocks[-1][1] == n - 1:
        first = blocks.pop(0)
        last = blocks.pop(-1)
        # Represent the wrap with end_idx >= n (so caller can mod-36 it).
        blocks.insert(0, (last[0], first[1] + n))

    # Sort blocks by FLAG_START position (the planting dekad), not by the
    # block's calendar position. Two blocks within one year: primary
    # season is typically the longer / earlier one — leave it to geocif
    # convention (seasons = [1, 2] where 1 is primary).
    def _start_dekad(block):
        s, e = block
        for k in range(s, e + 1):
            if flags[k % n] == FLAG_START:
                return k
        return s
    blocks.sort(key=_start_dekad)
    return blocks


def _block_to_dates(
    block: tuple[int, int], flags: np.ndarray, year: int,
) -> tuple[_dt.date, _dt.date, int]:
    """Convert a (start_idx, end_idx) season block to planting/harvest dates.

    Planting = first day of the first FLAG_START dekad within the block.
    Harvest  = last day of the last FLAG_END dekad within the block.

    Returns ``(planting_date, harvest_date, growing_days)``.
    """
    n = 24
    s, e = block
    block_indices = [k % n for k in range(s, e + 1)]

    # Planting: first FLAG_START in the block
    plant_bin = next(
        (k for k in block_indices if flags[k] == FLAG_START),
        block_indices[0],
    )
    # Harvest: last FLAG_END in the block
    harvest_bin = next(
        (k for k in reversed(block_indices) if flags[k] == FLAG_END),
        block_indices[-1],
    )

    plant_doy = _bin_to_doy(plant_bin, year, edge="start")
    plant_date = _dt.date(year, 1, 1) + _dt.timedelta(days=plant_doy - 1)

    # Did the block wrap past Dec? If harvest_bin < plant_bin (after mod),
    # harvest is in the next calendar year.
    if harvest_bin < plant_bin:
        harvest_year = year + 1
    else:
        harvest_year = year
    harvest_doy = _bin_to_doy(harvest_bin, harvest_year, edge="end")
    harvest_date = _dt.date(harvest_year, 1, 1) + _dt.timedelta(days=harvest_doy - 1)

    growing_days = (harvest_date - plant_date).days
    return plant_date, harvest_date, growing_days


def load_calendar(
    parser,
    country: str,
    crop: str,
    season: int,
    year: int,
) -> pd.DataFrame:
    """Load planting/harvest dates per calendar_region for one
    (country, crop, season, year) combination.

    Args:
        parser: ConfigParser instance with sections from
            geobase.txt + countries.txt + crops.txt + aquacrop.txt.
        country: Lowercase country name (e.g. 'malawi').
        crop: Canonical crop name (e.g. 'maize').
        season: Season number — 1 (primary) or 2 (secondary).
        year: Simulation year (planting year).

    Returns:
        DataFrame with columns:
            calendar_region : str
            planting_date   : datetime.date
            harvest_date    : datetime.date
            growing_days    : int
            sim_start_str   : str  (YYYY/MM/DD — AquaCropModel.sim_start_time)
            sim_end_str     : str  (YYYY/MM/DD — AquaCropModel.sim_end_time)

    Raises:
        FileNotFoundError: if the calendar Excel doesn't exist.
        ValueError: if no in-season block is found for the requested season.
    """
    path = _resolve_calendar_path(parser, country)
    if not path.is_file():
        raise FileNotFoundError(
            f"Calendar Excel not found for {country}: {path}. "
            f"Set [{country}] calendar_file in countries.txt."
        )

    # Crop sheet name. Mirrors geoprepare.BaseGeo.get_calendar_sheet_name:
    # wheat is single-season so sheet name is just the crop; everything else
    # uses "<crop>_<season>" (e.g. maize_1 for Gu, maize_2 for Deyr).
    # Multi-season countries (Kenya, Somalia) require the season suffix.
    if crop in ("winter_wheat", "spring_wheat"):
        sheet_name = crop
    else:
        sheet_name = f"{crop}_{season}"
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
    except (ValueError, KeyError) as exc:
        # ValueError on bad sheet name in pandas/openpyxl
        raise ValueError(
            f"Calendar sheet '{sheet_name}' not found in {path}. "
            f"Expected '<crop>_<season>' (e.g. 'maize_1') or '<crop>' for wheat."
        ) from exc

    # Match the canonical column name geoprepare's BaseGeo.read_statistics
    # uses (base.py:188-190). EWCM sheets call this column 'admin'; AMISCM
    # variants may call it 'calendar_region' already. Without this rename,
    # the per-row region label below falls back to country_col → every log
    # line reads 'region=Somalia' instead of the actual admin name.
    if "admin" in df.columns and "calendar_region" not in df.columns:
        df = df.rename(columns={"admin": "calendar_region"})

    # Country filter: convention column is 'country2' (geomerge uses this).
    country_col = "country2" if "country2" in df.columns else "country"
    df_country = df[df[country_col].str.lower() == country.lower()].copy()
    if df_country.empty:
        raise ValueError(
            f"No calendar rows for country='{country}' crop='{crop}' "
            f"in {path}."
        )

    # Verify required bi-monthly columns are present
    missing = [c for c in BIMONTH_COLS if c not in df_country.columns]
    if missing:
        raise ValueError(
            f"Calendar {path} missing bi-monthly columns: {missing[:5]}..."
        )

    out_rows = []
    n_no_data = 0
    for _, row in df_country.iterrows():
        region = row.get("calendar_region", row.get(country_col))
        flags_raw = row[BIMONTH_COLS].to_numpy(dtype=float)
        # Replace NaN with FLAG_OFF (4) so non-in-season treatment matches
        # the geomerge convention.
        flags = np.where(np.isnan(flags_raw), FLAG_OFF, flags_raw).astype(int)

        # All-(-1) rows are geomerge's "no calendar data for this admin"
        # sentinel (e.g. somalia maize Central/Coastal/Northeast/Togdheer
        # — crop doesn't grow in this region/season). Silent skip at debug;
        # accumulate a count for one summary line per call.
        if np.all(flags == -1):
            n_no_data += 1
            logger.debug(
                f"No calendar data for {country}/{crop}/{season} "
                f"region={region} (all -1 sentinel) — skipping"
            )
            continue

        blocks = _find_season_blocks(flags)
        if not blocks:
            logger.warning(
                f"No in-season block for {country}/{crop}/{season} "
                f"region={region} (flags present but none in {{1,2,3}}) — skipping"
            )
            continue

        # Pick the block matching the requested season number.
        # season=1 → blocks[0] (primary), season=2 → blocks[1] (secondary).
        block_idx = season - 1
        if block_idx >= len(blocks):
            logger.warning(
                f"Region {region} has only {len(blocks)} season(s), "
                f"requested season={season} — skipping"
            )
            continue

        plant_dt, harvest_dt, gdays = _block_to_dates(blocks[block_idx], flags, year)

        out_rows.append({
            "calendar_region": region,
            "planting_date": plant_dt,
            "harvest_date": harvest_dt,
            "growing_days": gdays,
            "sim_start_str": plant_dt.strftime("%Y/%m/%d"),
            "sim_end_str": (harvest_dt + _dt.timedelta(days=14)).strftime("%Y/%m/%d"),
            # +14 day buffer so AquaCrop can finish maturity calc cleanly
        })

    if not out_rows:
        raise ValueError(
            f"No usable calendar blocks for {country}/{crop}/season={season}"
        )

    logger.info(
        f"Calendar {country}/{crop}/season={season}: "
        f"{len(out_rows)} region(s) loaded"
        + (f", {n_no_data} no-data region(s) skipped" if n_no_data else "")
    )
    return pd.DataFrame(out_rows)


def planting_dekad_range(planting_date: _dt.date, harvest_date: _dt.date) -> tuple[int, int]:
    """Convert planting/harvest dates to dekad indices (1..36) for Stage_ID.

    Returns ``(start_dekad, end_dekad)`` matching the geocif Stage_ID format
    (e.g. 8_32 means dekad 8 through dekad 32 in the calendar year).
    """
    def _doy_to_dekad(d: _dt.date) -> int:
        # Dekad k starts at (k-1)*10 + 1 (approximately). Use month-aware
        # mapping to handle dekad 3 of each month being 8-11 days.
        month = d.month
        day = d.day
        if day <= 10:
            within = 0
        elif day <= 20:
            within = 1
        else:
            within = 2
        return (month - 1) * 3 + within + 1

    return _doy_to_dekad(planting_date), _doy_to_dekad(harvest_date)
