"""
calendar.py — derive planting/harvest dates per calendar_region from the
existing geocif calendar Excel (EWCM_*.xlsx / AMISCM_*.xlsx).

The calendar Excel uses dekadal flags in columns jan_1, jan_2, jan_3,
feb_1, ..., dec_3, with values:
    1 = season start (planting window)
    2 = mid-season
    3 = season end (harvest window)
    4 = off-season

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


# Dekad columns in the calendar Excel, in chronological order.
_MONTHS = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec",
]
DEKAD_COLS: list[str] = [f"{m}_{d}" for m in _MONTHS for d in (1, 2, 3)]
# 36 dekads. Dekad k (1..36) covers days-of-year roughly (k-1)*10+1 .. k*10
# (with the third dekad of each month absorbing the remaining days).

# Flag semantics in the dekad columns
FLAG_START = 1
FLAG_MID = 2
FLAG_END = 3
FLAG_OFF = 4


def _dekad_to_doy(dekad_idx: int, year: int, *, edge: str = "start") -> int:
    """Convert dekad index (0..35) to a day-of-year.

    ``edge='start'`` → first day of the dekad.
    ``edge='end'``   → last day of the dekad.

    Dekads 1 and 2 of a month are always days 1-10 / 11-20. Dekad 3 covers
    day 21 through the last day of the month, so its length is 8-11 days.
    """
    month = dekad_idx // 3 + 1  # 1..12
    within = dekad_idx % 3      # 0, 1, 2

    if within == 0:
        day = 1 if edge == "start" else 10
    elif within == 1:
        day = 11 if edge == "start" else 20
    else:
        if edge == "start":
            day = 21
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
    """Find contiguous in-season blocks in a 36-dekad flag vector.

    A block is a maximal run of dekads with flag in {1, 2, 3}. Returns
    a list of (start_dekad_idx, end_dekad_idx) tuples, sorted by the dekad
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
    n = 36
    s, e = block
    block_indices = [k % n for k in range(s, e + 1)]

    # Planting: first FLAG_START in the block
    plant_dekad = next(
        (k for k in block_indices if flags[k] == FLAG_START),
        block_indices[0],
    )
    # Harvest: last FLAG_END in the block
    harvest_dekad = next(
        (k for k in reversed(block_indices) if flags[k] == FLAG_END),
        block_indices[-1],
    )

    plant_doy = _dekad_to_doy(plant_dekad, year, edge="start")
    plant_date = _dt.date(year, 1, 1) + _dt.timedelta(days=plant_doy - 1)

    # Did the block wrap past Dec? If harvest_dekad < plant_dekad (after
    # mod), harvest is in the next calendar year.
    if harvest_dekad < plant_dekad:
        harvest_year = year + 1
    else:
        harvest_year = year
    harvest_doy = _dekad_to_doy(harvest_dekad, harvest_year, edge="end")
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

    # Country filter: convention column is 'country2' (geomerge uses this).
    country_col = "country2" if "country2" in df.columns else "country"
    df_country = df[df[country_col].str.lower() == country.lower()].copy()
    if df_country.empty:
        raise ValueError(
            f"No calendar rows for country='{country}' crop='{crop}' "
            f"in {path}."
        )

    # Verify required dekad columns are present
    missing = [c for c in DEKAD_COLS if c not in df_country.columns]
    if missing:
        raise ValueError(
            f"Calendar {path} missing dekad columns: {missing[:5]}..."
        )

    out_rows = []
    for _, row in df_country.iterrows():
        region = row.get("calendar_region", row.get(country_col))
        flags = row[DEKAD_COLS].to_numpy(dtype=float)
        # Replace NaN with FLAG_OFF (4) so non-in-season treatment matches
        # the geomerge convention.
        flags = np.where(np.isnan(flags), FLAG_OFF, flags).astype(int)

        blocks = _find_season_blocks(flags)
        if not blocks:
            logger.warning(
                "No in-season block for %s/%s/%s region=%s — skipping",
                country, crop, season, region,
            )
            continue

        # Pick the block matching the requested season number.
        # season=1 → blocks[0] (primary), season=2 → blocks[1] (secondary).
        block_idx = season - 1
        if block_idx >= len(blocks):
            logger.warning(
                "Region %s has only %d season(s), requested season=%d — skipping",
                region, len(blocks), season,
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
