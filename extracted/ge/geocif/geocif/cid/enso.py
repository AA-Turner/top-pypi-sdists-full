"""
Fetch and parse ENSO indices for use as scalar-per-year features.

Two operational (~1-month-lag) sources are pulled:
  - ONI  (Oceanic Nino Index, 3-mo running Nino 3.4 SST anomaly) from CPC
  - MEI v2 (Multivariate ENSO Index) from NOAA PSL

Both are ASCII text, no auth. Files are cached under
``params.dir_intermed / "enso" /`` and re-downloaded only if older than
``max_age_days`` (default 7). ``get_enso_frame`` returns a wide DataFrame
indexed on ``year`` with one column per (index, 3-mo-window) tuple, ready
to be broadcast onto the merged EO CSV.

Windows chosen to bracket a Southern-Hemisphere summer safra maize season
(planting Nov-Y-1, harvest Feb-Jun Y):
  - prev-year: JJA, ASO, SON, OND, NDJ  (pre-planting / El-Nino onset)
  - curr-year: DJF, JFM, FMA, MAM        (early growth through grain fill)

Neither source covers only Brazil -- these are global scalars, so the
same value is broadcast to every region of every country in year Y.
"""
from __future__ import annotations

import io
import logging
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
MEI_URL = "https://psl.noaa.gov/enso/mei/data/meiv2.data"

# CPC ONI 3-mo season codes centered on middle month, in calendar order.
ONI_SEASONS = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ",
               "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]

# PSL MEI v2 bimonthly (2-mo) season codes, in calendar order.
MEI_SEASONS = ["DJ", "JF", "FM", "MA", "AM", "MJ",
               "JJ", "JA", "AS", "SO", "ON", "ND"]

# Windows kept as features. Prev-year covers pre-planting to El-Nino onset;
# curr-year covers early growth through grain fill for Southern Hemisphere
# summer crops. Trimmed intentionally -- all 12 seasons are highly
# autocorrelated, we don't need them all.
ONI_WINDOWS_PREV = ["JJA", "ASO", "SON", "OND", "NDJ"]
ONI_WINDOWS_CURR = ["DJF", "JFM", "FMA", "MAM"]
MEI_WINDOWS_PREV = ["JJ", "AS", "SO", "ON", "ND"]
MEI_WINDOWS_CURR = ["DJ", "JF", "FM", "MA"]

_ONI_MISSING = -99.9   # CPC ONI missing sentinel
_MEI_MISSING = -999.0  # PSL MEI missing sentinel


def _cache_path(dir_cache: Path, url: str) -> Path:
    return dir_cache / url.rsplit("/", 1)[-1]


def _download(url: str, dest: Path, max_age_days: int = 7) -> Path:
    """Download ``url`` to ``dest`` if missing or older than ``max_age_days``.

    Writes atomically via a temp file + rename so concurrent workers in a
    parallel run can't observe a partially-written file. Without this, a
    reader forked from another worker mid-write would read fewer bytes than
    were downloaded and parse zero rows (ValueError seen 2026-07-08 in the
    first cluster run).
    """
    import os
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        age_days = (
            datetime.now(timezone.utc).timestamp() - dest.stat().st_mtime
        ) / 86400.0
        if age_days < max_age_days:
            return dest
    logger.info(f"Downloading {url} -> {dest}")
    with urllib.request.urlopen(url, timeout=60) as resp:
        data = resp.read()
    tmp = dest.with_suffix(dest.suffix + f".tmp.{os.getpid()}")
    tmp.write_bytes(data)
    os.replace(tmp, dest)  # atomic on POSIX + Windows
    return dest


def parse_oni(text: str) -> pd.DataFrame:
    """Parse CPC ONI ascii: header 'SEAS YR TOTAL ANOM' + whitespace rows.

    Returns a wide DataFrame indexed on ``year`` with one column per season
    (e.g. ``oni_djf``, ``oni_jfm``, ...). Missing values -> NaN.
    """
    rows = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) != 4:
            continue
        seas, yr, total, anom = parts
        if seas == "SEAS":
            continue
        try:
            rows.append((int(yr), seas.upper(), float(anom)))
        except ValueError:
            continue
    if not rows:
        raise ValueError("parse_oni: no rows parsed -- CPC file format changed?")

    df = pd.DataFrame(rows, columns=["year", "seas", "value"])
    df.loc[df["value"] == _ONI_MISSING, "value"] = np.nan
    wide = df.pivot(index="year", columns="seas", values="value")
    wide.columns = [f"oni_{s.lower()}" for s in wide.columns]
    # Ensure all 12 season columns present even if the file trails off mid-year
    for s in ONI_SEASONS:
        col = f"oni_{s.lower()}"
        if col not in wide.columns:
            wide[col] = np.nan
    return wide.sort_index()


def parse_mei(text: str) -> pd.DataFrame:
    """Parse NOAA PSL MEI v2: two header lines (year range + season labels),
    then whitespace rows of ``year v1 v2 ... v12``.

    Returns a wide DataFrame indexed on ``year`` with one column per bimonthly
    season (e.g. ``mei_dj``, ``mei_jf``, ...). Missing values -> NaN.
    """
    year_rows = []
    for line in text.splitlines():
        parts = line.split()
        # Data rows are exactly 13 whitespace tokens: year + 12 season values.
        # PSL's leading/trailing metadata lines have 2 tokens (year range) or
        # words, so this shape filter is a clean discriminator.
        if len(parts) != 13:
            continue
        try:
            yr = int(parts[0])
            vals = [float(v) for v in parts[1:]]
        except ValueError:
            continue
        year_rows.append((yr, vals))
    if not year_rows:
        raise ValueError(
            f"parse_mei: no rows parsed from {len(text)}-byte input "
            f"(first 200 chars: {text[:200]!r}) -- PSL file format changed "
            "or partial download?"
        )

    years = [r[0] for r in year_rows]
    data = np.array([r[1] for r in year_rows], dtype=float)
    data[data == _MEI_MISSING] = np.nan
    wide = pd.DataFrame(
        data,
        index=pd.Index(years, name="year"),
        columns=[f"mei_{s.lower()}" for s in MEI_SEASONS],
    )
    return wide.sort_index()


def fetch_oni(dir_cache: Path, max_age_days: int = 7) -> pd.DataFrame:
    """Fetch (with caching) and parse CPC ONI. See ``parse_oni``."""
    path = _download(ONI_URL, _cache_path(dir_cache, ONI_URL), max_age_days)
    return parse_oni(path.read_text())


def fetch_mei(dir_cache: Path, max_age_days: int = 7) -> pd.DataFrame:
    """Fetch (with caching) and parse NOAA PSL MEI v2. See ``parse_mei``."""
    path = _download(MEI_URL, _cache_path(dir_cache, MEI_URL), max_age_days)
    return parse_mei(path.read_text())


def get_enso_frame(
    dir_cache: Path,
    years: Iterable[int] | None = None,
    max_age_days: int = 7,
) -> pd.DataFrame:
    """Assemble prev-year + curr-year ENSO features keyed on harvest ``year``.

    For each harvest year Y, emits:
      - ONI_prev_{JJA,ASO,SON,OND,NDJ}  from season means centered in year Y-1
      - ONI_curr_{DJF,JFM,FMA,MAM}      from season means centered in year Y
      - MEI_prev_{JJ,AS,SO,ON,ND}       from bimonthlies centered in year Y-1
      - MEI_curr_{DJ,JF,FM,MA}          from bimonthlies centered in year Y

    Returns a DataFrame indexed on ``year`` with one column per feature.
    Rows are NaN where the raw index has missing values (e.g. the current
    year has not yet reached MAM at forecast time).
    """
    oni_wide = fetch_oni(dir_cache, max_age_days)
    mei_wide = fetch_mei(dir_cache, max_age_days)

    out_index = pd.Index(sorted(years), name="year") if years is not None \
        else oni_wide.index.union(mei_wide.index).rename("year")

    out = pd.DataFrame(index=out_index)

    # ONI: current year = same year; prev year = year - 1
    for s in ONI_WINDOWS_CURR:
        col = f"oni_{s.lower()}"
        out[f"ONI_curr_{s}"] = out.index.map(oni_wide[col]) if col in oni_wide else np.nan
    for s in ONI_WINDOWS_PREV:
        col = f"oni_{s.lower()}"
        if col in oni_wide:
            out[f"ONI_prev_{s}"] = (out.index - 1).map(oni_wide[col])
        else:
            out[f"ONI_prev_{s}"] = np.nan

    # MEI: same pattern.
    for s in MEI_WINDOWS_CURR:
        col = f"mei_{s.lower()}"
        out[f"MEI_curr_{s}"] = out.index.map(mei_wide[col]) if col in mei_wide else np.nan
    for s in MEI_WINDOWS_PREV:
        col = f"mei_{s.lower()}"
        if col in mei_wide:
            out[f"MEI_prev_{s}"] = (out.index - 1).map(mei_wide[col])
        else:
            out[f"MEI_prev_{s}"] = np.nan

    return out
