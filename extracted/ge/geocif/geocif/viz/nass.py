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


# ---------------------------------------------------------------------------
# Crop condition (statisticcat_desc = CONDITION): the weekly very poor .. excellent
# shares and the 0-100 condition index, for the snake chart's USDA rows.
#
# geoprepare.datasets.CROP_CONDITION builds the same table for the ML inputs
# ([DEFAULT] cci_file); this is the in-session fallback for years that file
# lacks, with the same query, categories, weights and output columns, so a
# frame from either source reads alike (cid/cci.py consumes both).
# ---------------------------------------------------------------------------
CONDITION_COMMODITY = {"maize": "CORN", "soybean": "SOYBEANS", "sorghum": "SORGHUM",
                       "rice": "RICE", "cotton": "COTTON", "winter_wheat": "WHEAT",
                       "spring_wheat": "WHEAT"}
#: Substring of ``class_desc`` that picks the crop out of a shared commodity.
CONDITION_CLASS = {"winter_wheat": "WINTER", "spring_wheat": "SPRING", "cotton": "UPLAND"}
CONDITION_CATEGORIES = {"PCT VERY POOR": "very_poor", "PCT POOR": "poor", "PCT FAIR": "fair",
                        "PCT GOOD": "good", "PCT EXCELLENT": "excellent"}
#: The repo's index is 0-100; the plan's 100-500 variant is 100 + 4 * this.
CCI_WEIGHTS = {"very_poor": 0.0, "poor": 0.25, "fair": 0.5, "good": 0.75, "excellent": 1.0}
CONDITION_COLUMNS = ["crop", "region", "state_alpha", "year", "woy", "week_ending", "cci",
                     "cci_ge", "very_poor", "poor", "fair", "good", "excellent"]


def nass_api_key(configured=None):
    """``[NASS] api_key`` when set, else the ``NASS_API_KEY`` environment
    variable, else None."""
    import os

    key = str(configured or "").strip()
    return key or os.environ.get("NASS_API_KEY", "").strip() or None


def cci_index(very_poor, poor, fair, good, excellent, *, scale="repo"):
    """Crop condition index from the five shares (percent, summing to 100).

    ``scale="repo"`` is the 0-100 index geoprepare and cid/cci.py use
    (weights 0, 0.25, 0.5, 0.75, 1); ``scale="plan"`` the 100-500 variant
    with weights 1..5, which is ``100 + 4 * repo``. Standardized anomalies are
    identical on both scales.
    """
    repo = (CCI_WEIGHTS["very_poor"] * very_poor + CCI_WEIGHTS["poor"] * poor
            + CCI_WEIGHTS["fair"] * fair + CCI_WEIGHTS["good"] * good
            + CCI_WEIGHTS["excellent"] * excellent)
    if scale == "repo":
        return repo
    if scale == "plan":
        return 100.0 + 4.0 * repo
    raise ValueError(f"scale must be 'repo' or 'plan', got {scale!r}")


def _norm_state(name):
    return str(name).strip().lower().replace(" ", "_")


def _tidy_condition(raw, crop):
    """QuickStats CONDITION rows -> one row per (state, year, week) with the
    five shares, ``cci`` and ``cci_ge``. Weeks whose shares do not sum to
    99-101 (a withheld category) are dropped, as geoprepare does."""
    df = pd.DataFrame(raw)
    if df.empty:
        return pd.DataFrame(columns=CONDITION_COLUMNS)
    df = df[~df["state_fips_code"].astype(str).str.zfill(2).isin(_NOT_A_STATE)]
    want_class = CONDITION_CLASS.get(crop)
    if want_class and "class_desc" in df.columns:
        df = df[df["class_desc"].astype(str).str.upper().str.contains(want_class)]
    df = df.copy()
    df["cat"] = df["unit_desc"].astype(str).str.strip().str.upper().map(CONDITION_CATEGORIES)
    df = df.dropna(subset=["cat"])
    df["value"] = pd.to_numeric(df["Value"].astype(str).str.replace(",", "", regex=False),
                                errors="coerce")
    df["week_ending"] = pd.to_datetime(df["week_ending"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["value", "week_ending", "year"])
    if df.empty:
        return pd.DataFrame(columns=CONDITION_COLUMNS)
    wide = (df.pivot_table(index=["state_name", "state_alpha", "year", "week_ending"],
                           columns="cat", values="value", aggfunc="first")
            .reset_index())
    for cat in CCI_WEIGHTS:
        if cat not in wide.columns:
            wide[cat] = np.nan
    total = wide[list(CCI_WEIGHTS)].fillna(0.0).sum(axis=1)
    wide = wide[(total >= 99.0) & (total <= 101.0)].copy()
    for cat in CCI_WEIGHTS:
        wide[cat] = wide[cat].fillna(0.0)
    wide["cci"] = cci_index(wide["very_poor"], wide["poor"], wide["fair"], wide["good"],
                            wide["excellent"]).round(2)
    wide["cci_ge"] = wide["good"] + wide["excellent"]
    wide["region"] = wide["state_name"].map(_norm_state)
    wide["year"] = wide["year"].astype(int)
    wide["woy"] = wide["week_ending"].dt.isocalendar().week.astype(int)
    wide["crop"] = crop
    return wide[CONDITION_COLUMNS].sort_values(["region", "week_ending"]).reset_index(drop=True)


def fetch_condition(api_key, years, crops=("maize",), cache=None, offline=False,
                    timeout=90, session=None):
    """Weekly state crop-condition shares for ``years`` / ``crops``.

    The same contract as :func:`fetch`: a live query first (one call per
    commodity and year, ``statisticcat_desc = CONDITION``), the result
    written to ``cache`` when non-empty, the cache used when the API is
    unreachable or ``offline`` is set. Crops without a NASS commodity are
    dropped; a year with no data answers 400 and counts as empty.
    """
    cache = Path(cache) if cache else None
    years = [str(y) for y in sorted({int(y) for y in years})]
    crops = [c for c in crops if c in CONDITION_COMMODITY]
    if not crops:
        raise ValueError(f"no NASS condition commodity for crops {crops}; "
                         f"known: {sorted(CONDITION_COMMODITY)}")
    if not offline:
        import requests

        if not api_key:
            raise ValueError("a NASS API key is needed for a live condition query "
                             "([NASS] api_key or NASS_API_KEY)")
        sess = session or requests.Session()
        raw = []
        try:
            for crop in crops:
                for year in years:
                    r = sess.get(QUICKSTATS_URL, timeout=timeout, params={
                        "key": api_key, "format": "JSON",
                        "source_desc": "SURVEY", "sector_desc": "CROPS",
                        "statisticcat_desc": "CONDITION", "agg_level_desc": "STATE",
                        "commodity_desc": CONDITION_COMMODITY[crop], "year": year,
                    })
                    if r.status_code == 400:
                        continue
                    r.raise_for_status()
                    raw.append((crop, r.json().get("data", [])))
        except (requests.RequestException, ValueError) as exc:
            if cache is None or not cache.exists():
                raise
            print(f"NASS QuickStats unreachable ({type(exc).__name__}: {exc}); "
                  f"falling back to the cached condition extract {cache}")
        else:
            frames = [_tidy_condition(rows, crop) for crop, rows in raw]
            out = (pd.concat(frames, ignore_index=True) if frames
                   else pd.DataFrame(columns=CONDITION_COLUMNS))
            if cache is not None and not out.empty:
                cache.parent.mkdir(parents=True, exist_ok=True)
                out.to_csv(cache, index=False)
            return out
    if cache is None or not cache.exists():
        raise ValueError("offline NASS condition requested but no cache exists "
                         f"at {cache}")
    return _read_condition_csv(cache)


def _read_condition_csv(path):
    """A geoprepare or cached condition CSV with the columns normalised."""
    df = pd.read_csv(path)
    if "cci_ge" not in df.columns and {"good", "excellent"} <= set(df.columns):
        df["cci_ge"] = (pd.to_numeric(df["good"], errors="coerce")
                        + pd.to_numeric(df["excellent"], errors="coerce"))
    for c in CONDITION_COLUMNS:
        if c not in df.columns:
            df[c] = np.nan
    df["week_ending"] = pd.to_datetime(df["week_ending"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["week_ending", "year"]).copy()
    df["year"] = df["year"].astype(int)
    df["region"] = df["region"].map(_norm_state)
    for c in ("cci", "cci_ge", "very_poor", "poor", "fair", "good", "excellent"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[CONDITION_COLUMNS]


def load_nass_crop_condition(crop, geography, years, *, csv_path=None, api_key=None,
                             cache=None, offline=False, timeout=90, session=None):
    """Weekly crop-condition rows for ``crop``, ``geography`` and ``years``.

    In-house data first: the cleaned CSV geoprepare maintains
    (``[DEFAULT] cci_file``) is read when ``csv_path`` is given; only years it
    lacks are fetched from Quick Stats with :func:`fetch_condition` (key from
    ``api_key`` or ``NASS_API_KEY``), and skipped with a note when no key is
    available. ``geography`` is a state name, an iterable of names, or
    ``None`` / ``"all"`` for every state. One row per (region, year, week).
    """
    years = sorted({int(y) for y in years})
    frames = []
    if csv_path and Path(csv_path).exists():
        csv = _read_condition_csv(csv_path)
        frames.append(csv[csv["crop"].astype(str) == str(crop)])
    have = set(int(y) for f in frames for y in f["year"].unique())
    missing = [y for y in years if y not in have]
    if missing:
        key = nass_api_key(api_key)
        if key or offline:
            frames.append(fetch_condition(key, missing, crops=(crop,), cache=cache,
                                          offline=offline, timeout=timeout, session=session))
        else:
            print(f"NASS condition: no API key, years {missing} not fetched for {crop}")
    if not frames:
        return pd.DataFrame(columns=CONDITION_COLUMNS)
    out = pd.concat(frames, ignore_index=True)
    out = out[out["year"].isin(years)]
    if geography is not None and str(geography).lower() != "all":
        names = [geography] if isinstance(geography, str) else list(geography)
        out = out[out["region"].isin({_norm_state(n) for n in names})]
    out = (out.sort_values(["region", "year", "week_ending"])
           .drop_duplicates(["region", "year", "week_ending"], keep="last"))
    return out[CONDITION_COLUMNS].reset_index(drop=True)
