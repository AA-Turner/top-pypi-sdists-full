"""
Load the USDA NASS Census of Agriculture county irrigated-area share as a
per-region ANNUAL predictor.

The source CSV (``metadata/irrigation/nass_census_irrigated_share.csv``, built
by ``geoprepare.datasets.NASS_IRRIGATION``) has one row per (crop, county,
census year)::

    crop, state_alpha, state_fips_code, county_ansi, fips, county_name,
    year, irr_acres, all_acres, irr_share

``irr_share`` is irrigated harvested acres / all harvested acres, in [0, 1].

Why an annual (not static) predictor
------------------------------------
Irrigated share is not a fixed county property: farmers reallocate water in
response to allocation rules and declining well capacity, so the blend weight
behind a county-mean yield drifts. It is also not a monthly one — the census
reports it once per county-year. So it joins on ``(Region, Harvest Year)``,
which is a join key neither ``_add_static_eo_features`` (Region only) nor the
CCI path (Region, year, Month) provides.

Interpolation
-------------
The census runs every five years (2002, 2007, 2012, 2017, 2022). ``get_irrigation_frame``
expands that to every requested year by linear interpolation between census
points and a flat hold outside them — before the first census year and, more
importantly, after the last, since forecasts run past 2022. Holding flat is the
honest choice: we have no basis for extrapolating a trend in irrigated share,
and a linear extrapolation would drift without bound.

Contract
--------
Non-fatal throughout, matching ``cid/cci.py``: a missing file or missing
columns logs a warning and returns ``None`` so the caller no-ops and no
``irr_share`` column appears, rather than failing a whole run over an optional
predictor.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

CENSUS_COLUMNS = {"crop", "year", "irr_share"}


def normalize_region(name) -> str:
    """Canonicalise a region label into a join key.

    geocif county Regions read ``"Kansas Rice"`` (state + county, shapefile
    spelling); the census reports ``state_alpha="KS"``, ``county_name="RICE"``.

    Whitespace is removed entirely, not merely collapsed. The two sources
    disagree on internal spacing often enough to matter: the boundary file has
    ``Dekalb``/``Lasalle``/``Dupage``/``Laporte``/``Obrien`` where NASS has
    ``DE KALB``/``LA SALLE``/``DU PAGE``/``LA PORTE``/``O BRIEN``. Preserving
    spaces cost 8 real counties in a live check. Punctuation goes for the same
    reason (``"St. Clair"`` vs ``"ST CLAIR"``).

    Collapsing spaces cannot merge two distinct counties of one state, since
    that would need a state holding both e.g. "La Porte" and "Laporte".
    """
    s = str(name).lower().strip()
    s = s.replace("_", " ").replace("-", " ")
    s = re.sub(r"[^a-z0-9]", "", s)
    return s


STATE_ALPHA_TO_NAME = {
    "AL": "alabama", "AR": "arkansas", "AZ": "arizona", "CA": "california",
    "CO": "colorado", "CT": "connecticut", "DE": "delaware", "FL": "florida",
    "GA": "georgia", "IA": "iowa", "ID": "idaho", "IL": "illinois",
    "IN": "indiana", "KS": "kansas", "KY": "kentucky", "LA": "louisiana",
    "MA": "massachusetts", "MD": "maryland", "ME": "maine", "MI": "michigan",
    "MN": "minnesota", "MO": "missouri", "MS": "mississippi", "MT": "montana",
    "NC": "north carolina", "ND": "north dakota", "NE": "nebraska",
    "NH": "new hampshire", "NJ": "new jersey", "NM": "new mexico",
    "NV": "nevada", "NY": "new york", "OH": "ohio", "OK": "oklahoma",
    "OR": "oregon", "PA": "pennsylvania", "RI": "rhode island",
    "SC": "south carolina", "SD": "south dakota", "TN": "tennessee",
    "TX": "texas", "UT": "utah", "VA": "virginia", "VT": "vermont",
    "WA": "washington", "WI": "wisconsin", "WV": "west virginia",
    "WY": "wyoming",
}


def _interpolate_to_years(g: pd.DataFrame, years: list) -> pd.DataFrame:
    """Expand one county's census points onto ``years``.

    Linear between census years, flat hold outside. ``np.interp`` already
    clamps to the end values, which is exactly the hold we want.
    """
    g = g.sort_values("year")
    xs = g["year"].to_numpy(dtype=float)
    ys = g["irr_share"].to_numpy(dtype=float)
    if len(xs) == 0:
        return pd.DataFrame(columns=["region", "year", "irr_share"])
    if len(xs) == 1:
        vals = np.full(len(years), ys[0])
    else:
        vals = np.interp(np.asarray(years, dtype=float), xs, ys)
    return pd.DataFrame({
        "region": g["region"].iloc[0],
        "year": years,
        "irr_share": vals,
    })


def get_irrigation_frame(
    csv_path,
    crop: str,
    years: Optional[Iterable[int]] = None,
) -> Optional[pd.DataFrame]:
    """Irrigated share per (region, year) for a single crop.

    Args:
        csv_path: path to the NASS census irrigated-share CSV.
        crop: geocif crop name (``maize``, ``soybean``, ...).
        years: years to expand onto. Defaults to the span of the census years
            present, which is rarely what a forecast run wants — pass the run's
            harvest years so the hold past the last census reaches them.

    Returns:
        DataFrame ``[region, year, irr_share]``, ``None`` if the file or its
        columns are missing, or an empty frame if the crop is not covered.
    """
    p = Path(csv_path)
    if not p.exists():
        logger.warning(f"irrigation share file not found: {p}")
        return None
    try:
        df = pd.read_csv(p)
    except Exception as e:  # noqa: BLE001
        logger.warning(f"irrigation share file unreadable ({type(e).__name__}: {e})")
        return None
    if not CENSUS_COLUMNS.issubset(df.columns):
        logger.warning(
            f"irrigation share file missing required columns "
            f"{sorted(CENSUS_COLUMNS - set(df.columns))} (have {list(df.columns)})"
        )
        return None

    df = df[df["crop"].astype(str) == str(crop)].copy()
    if df.empty:
        return df  # crop not covered -> caller no-ops

    # Region key: "<state name> <county name>", matching the geocif county
    # Region convention. When state_alpha is absent (a hand-built file), fall
    # back to whatever county identity the file carries.
    if "state_alpha" in df.columns and "county_name" in df.columns:
        state = df["state_alpha"].astype(str).str.upper().map(STATE_ALPHA_TO_NAME)
        df["region"] = (state.fillna("") + " " + df["county_name"].astype(str)).map(
            normalize_region
        )
    elif "county_name" in df.columns:
        df["region"] = df["county_name"].map(normalize_region)
    else:
        logger.warning("irrigation share file has no county_name column")
        return None

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["irr_share"] = pd.to_numeric(df["irr_share"], errors="coerce")
    df = df.dropna(subset=["region", "year", "irr_share"])
    df = df[df["region"].str.strip() != ""]
    if df.empty:
        return df

    # One value per (region, census year): the source is already deduped on
    # (crop, fips, year), but two FIPS can normalise to the same region string
    # in a hand-edited file. Mean is the safe collapse.
    df = df.groupby(["region", "year"], as_index=False)["irr_share"].mean()

    if years is None:
        target_years = sorted(int(y) for y in df["year"].unique())
    else:
        target_years = sorted({int(y) for y in years})
    if not target_years:
        return pd.DataFrame(columns=["region", "year", "irr_share"])

    # Explicit loop rather than groupby.apply: the pixi env runs pandas 3.0,
    # where apply no longer passes the grouping column through.
    parts = [
        _interpolate_to_years(g, target_years)
        for _, g in df.groupby("region", sort=True)
    ]
    if not parts:
        return pd.DataFrame(columns=["region", "year", "irr_share"])
    out = pd.concat(parts, ignore_index=True)
    return out[["region", "year", "irr_share"]]


def resolve_csv_path(parser, dir_metadata) -> Path:
    """Where the irrigation CSV lives, mirroring the CCI path convention."""
    fname = parser.get(
        "NASS_IRRIGATION", "output_file",
        fallback="nass_census_irrigated_share.csv",
    ) if parser is not None and parser.has_section("NASS_IRRIGATION") else (
        "nass_census_irrigated_share.csv"
    )
    return Path(dir_metadata) / "irrigation" / fname
