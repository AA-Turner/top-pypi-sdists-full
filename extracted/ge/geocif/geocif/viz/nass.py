"""USDA NASS QuickStats yield estimates: the in-season reference for a cone.

NASS publishes a state yield forecast every month of the harvest run (Aug,
Sep, Oct, Nov for corn and soybeans) and a final estimate the following
January. That monthly cadence is the natural yardstick for a forecast cone:
each of our forecast issue dates has a contemporaneous USDA number, and the
final estimate is the truth both converge toward.

Two traps this module exists to handle:

1. ``freq_desc = MONTHLY`` is NOT how the monthly forecasts are stored — that
   query is rejected outright. They arrive as ``freq_desc = ANNUAL`` with a
   ``reference_period_desc`` of ``"YEAR - AUG FORECAST"``, ``"... SEP ..."``
   and so on.

2. For a season still in progress, NASS ALSO publishes a ``"YEAR"`` row that
   is merely a copy of the latest forecast — in September 2026 the 2026
   ``YEAR`` row is the August forecast, loaded 2026-08-12. Treating it as the
   final estimate would present a forecast as an observation. A ``YEAR`` row
   is only final once it was loaded AFTER its crop year, which is the test
   used here.

The API key lives in the ``[NASS] api_key`` config key (geobase.txt).
"""

from pathlib import Path

import pandas as pd

from geocif.viz._style import MONTHS

QUICKSTATS_URL = "https://quickstats.nass.usda.gov/api/api_GET/"

# geocif crop name -> (commodity_desc, short_desc) for the grain yield series.
CROP_QUERY = {
    "maize": ("CORN", "CORN, GRAIN - YIELD, MEASURED IN BU / ACRE"),
    "soybean": ("SOYBEANS", "SOYBEANS - YIELD, MEASURED IN BU / ACRE"),
}

_MONTH_NUM = {m.upper(): i + 1 for i, m in enumerate(MONTHS)}

# Aggregate pseudo-states carried in the same response ("OTHER STATES", fips 98).
_NOT_A_STATE = {"98", "99", "00"}

COLUMNS = ["crop", "year", "Region", "state_fips", "period", "ref_month",
           "is_final", "yield_bu_ac", "load_time"]


def _tidy(raw, crop):
    """QuickStats JSON rows -> the tidy per-state frame this module returns."""
    df = pd.DataFrame(raw)
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)
    df = df[~df["state_fips_code"].astype(str).str.zfill(2).isin(_NOT_A_STATE)]
    df["yield_bu_ac"] = pd.to_numeric(
        df["Value"].astype(str).str.replace(",", "", regex=False), errors="coerce")
    df = df.dropna(subset=["yield_bu_ac"])
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["load_time"] = pd.to_datetime(df["load_time"], errors="coerce")
    df["Region"] = df["state_name"].str.title()
    df["state_fips"] = df["state_fips_code"].astype(str).str.zfill(2)
    df["period"] = df["reference_period_desc"].str.strip().str.upper()

    month = df["period"].str.extract(r"YEAR\s*-\s*([A-Z]{3})\s*FORECAST")[0]
    df["ref_month"] = month.map(_MONTH_NUM).astype("Int64")

    # A "YEAR" row is the final estimate only when it was loaded after its own
    # crop year; during the season it mirrors the latest monthly forecast.
    df["is_final"] = (df["period"] == "YEAR") & (
        df["load_time"].dt.year > df["year"].astype("Int64"))
    # In-season mirrors carry no information the forecast rows lack.
    df = df[(df["ref_month"].notna()) | df["is_final"]]
    df["crop"] = crop
    return df[COLUMNS].reset_index(drop=True)


def fetch(api_key, years, crops=("maize", "soybean"), cache=None, offline=False,
          timeout=90, session=None):
    """Per-state monthly forecasts + final estimates for ``years``/``crops``.

    Always prefers a live query so the current season is up to date, writing
    a non-empty result to ``cache`` when given. If the API cannot be reached (or
    ``offline`` is set) the cache is used instead — a compute node without
    egress still renders the same figures, just without any newer NASS report.
    """
    cache = Path(cache) if cache else None
    years = [str(y) for y in sorted({int(y) for y in years})]
    crops = [c for c in crops if c in CROP_QUERY]
    if not crops:
        raise ValueError(f"no NASS query defined for crops {crops}; "
                         f"known: {sorted(CROP_QUERY)}")

    if not offline:
        import requests

        sess = session or requests.Session()
        raw = []
        try:
            for crop in crops:
                commodity, short_desc = CROP_QUERY[crop]
                for year in years:
                    r = sess.get(QUICKSTATS_URL, timeout=timeout, params={
                        "key": api_key, "format": "JSON",
                        "source_desc": "SURVEY", "sector_desc": "CROPS",
                        "statisticcat_desc": "YIELD", "agg_level_desc": "STATE",
                        "commodity_desc": commodity, "short_desc": short_desc,
                        "year": year,
                    })
                    # A year with no published estimate answers 400
                    # "bad request - invalid query"; that is a legitimately
                    # empty slice, not a failure.
                    if r.status_code == 400:
                        continue
                    r.raise_for_status()
                    raw.append((crop, r.json().get("data", [])))
        except (requests.RequestException, ValueError) as exc:  # network/DNS/HTTP/JSON
            if cache is None or not cache.exists():
                raise
            print(f"NASS QuickStats unreachable ({type(exc).__name__}: {exc}); "
                  f"falling back to the cached extract {cache}")
        else:
            # Tidying and caching happen outside the try: a failure after a
            # successful fetch must surface, not masquerade as "unreachable".
            frames = [_tidy(rows, crop) for crop, rows in raw]
            out = (pd.concat(frames, ignore_index=True) if frames
                   else pd.DataFrame(columns=COLUMNS))
            # An all-400 (or otherwise empty) answer carries no data — writing
            # it would permanently poison a cache built by an earlier run.
            if cache is not None and not out.empty:
                cache.parent.mkdir(parents=True, exist_ok=True)
                out.to_csv(cache, index=False)
            return out

    if cache is None or not cache.exists():
        raise ValueError("offline NASS reference requested but no cache exists "
                         f"at {cache}")
    out = pd.read_csv(cache)
    out["load_time"] = pd.to_datetime(out["load_time"], errors="coerce")
    for c in ("year", "ref_month"):
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")
    out["state_fips"] = out["state_fips"].astype(str).str.zfill(2)
    return out


def finals(nass, crop):
    """``{(year, Region): yield_bu_ac}`` for genuine final estimates only."""
    sub = nass[(nass["crop"] == crop) & nass["is_final"].astype(bool)]
    return {(int(r["year"]), r["Region"]): float(r["yield_bu_ac"])
            for _, r in sub.iterrows()}


def monthly(nass, crop):
    """In-season forecasts as ``{(year, month, Region): yield_bu_ac}``."""
    sub = nass[(nass["crop"] == crop) & nass["ref_month"].notna()]
    return {(int(r["year"]), int(r["ref_month"]), r["Region"]):
            float(r["yield_bu_ac"]) for _, r in sub.iterrows()}
