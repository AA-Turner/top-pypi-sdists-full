"""Which country x crop combinations can be forecast from S2S now?

Scans the geoprepare output tree for merged crop CSVs, derives each combo's
planting month and season shape from the crop-calendar columns in the data,
and reports the state of the S2S window of its current or next season:

    open        the window is open: from ``planting - MAX_USABLE_OFFSET``
                (June-type truncated inits are excluded on purpose -- proven
                harmful) until the window closes after planting (see
                ``window_state``). ``phase`` says whether planting has passed.
    too_early   the window has not reached a usable init yet; reports the
                month it becomes usable.

Data checks per combo: S2S per-region CSVs present (and their latest init),
and a materialized statistics file (yields) so the combo can contribute
training rows.

Usage::

    from geocif.experiments import s2s_eligibility
    df = s2s_eligibility.run(parser=parser)          # or path_config_files
"""
import calendar
import glob
import re
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

import logging

logger = logging.getLogger(__name__)

# An init is usable when it can see at least planting..planting+2 (3 season
# months): issued at most 4 months before planting (leads reach init+6).
MAX_USABLE_OFFSET = 4
PRE_WINDOW = 6  # the full pre-season window is planting-6 .. planting-1
# The S2S model's season is planting .. planting+SEASON_LEN-1. An init issued
# in month m forecasts months m+1 .. m+6 (lead L is month m+L; NOAA's ``L`` is
# "months since reference time"), so the last init that still sees a season
# month is issued in the season's second-to-last month, and S2S coverage of
# the season ends with its last month.
SEASON_LEN = 4


def planting_and_span(merged_csv):
    """(planting_month, wraps) from a merged CSV's crop-calendar columns.

    Planting month = mode of months where crop_calendar enters 1 from 0/4.
    wraps = True when the in-season block crosses the calendar year (harvest
    year is the year AFTER planting).
    """
    want = ["region", "month", "crop_calendar", "year", "doy"]
    try:
        df = pd.read_csv(merged_csv, usecols=want, engine="pyarrow")
    except Exception:
        df = pd.read_csv(merged_csv,
                         usecols=lambda c: c in set(want))
    df = df.dropna(subset=["crop_calendar"])
    df["cc"] = pd.to_numeric(df["crop_calendar"], errors="coerce")
    df = df.dropna(subset=["cc"]).sort_values(["region", "year", "doy"])
    prev = df.groupby("region")["cc"].shift(1)
    trans = df[(df["cc"] == 1) & prev.isin([0.0, 4.0])]
    if trans.empty:
        ins = df[df["cc"].isin([1, 2, 3])]
        if ins.empty:
            return None, None
        planting = int(ins["month"].mode().iloc[0])
    else:
        planting = int(trans["month"].mode().iloc[0])
    in_months = set(int(m) for m in df[df["cc"].isin([1, 2, 3])]["month"].unique())
    # wraps when December and January are both in-season, or planting late-year
    wraps = (12 in in_months and 1 in in_months) or planting >= 8
    return planting, wraps


def s2s_status(s2s_dir):
    """(n_files, latest_init 'YYYY-MM') for a country's s2s_tprate dir."""
    files = glob.glob(str(Path(s2s_dir) / "s2s_tprate" / "*.csv"))
    if not files:
        return 0, None
    years = {}
    for f in files:
        m = re.search(r"_(\d{4})_s2s_", Path(f).name)
        if m:
            years.setdefault(int(m.group(1)), []).append(f)
    if not years:
        return len(files), None
    ymax = max(years)
    mmax = 0
    for f in years[ymax][:3]:  # a few files suffice — same months per region
        try:
            d = pd.read_csv(f, usecols=["month"])
            mmax = max(mmax, int(d["month"].max()))
        except Exception:
            pass
    return len(files), f"{ymax}-{mmax:02d}" if mmax else f"{ymax}-01"


def shift_month(year, month, k):
    """(year, month) ``k`` months after (or, for k < 0, before) year-month."""
    t = year * 12 + (month - 1) + k
    return t // 12, t % 12 + 1


def month_end(year, month):
    return date(year, month, calendar.monthrange(year, month)[1])


def close_offset(planting, harvest_month=None):
    """Months after planting whose last day closes the S2S window.

    The EARLIER of the end of S2S coverage of the season (its last month,
    ``SEASON_LEN - 1`` months after planting) and the end of the harvest
    month. A harvest month equal to the planting month reads as a full-year
    season and does not bind.
    """
    k = SEASON_LEN - 1
    if harvest_month:
        k = min(k, (int(harvest_month) - planting) % 12 or 12)
    return k


def window_state(planting, wraps, today=None, latest_init=None,
                 harvest_month=None):
    """State of the S2S window for the current season, else the next one.

    The window opens ``MAX_USABLE_OFFSET`` months before planting and stays
    open AFTER planting until ``close_offset``: the end of the harvest month
    or the end of S2S coverage of the season, whichever is earlier. It
    used to close on the 1st of the planting month; inits issued after
    planting still forecast the season's remaining months, so the cutoff
    went. A season whose window has closed rolls over to the next one.

    ``phase`` is ``pre_season`` before planting and ``in_season`` after.
    """
    today = today or date.today()
    # Next planting, unless the previous planting's window is still open.
    py = today.year if today.month <= planting else today.year + 1
    k_close = close_offset(planting, harvest_month)
    if today <= month_end(*shift_month(py - 1, planting, k_close)):
        py -= 1
    plant = date(py, planting, 1)
    harvest_year = py + 1 if wraps else py
    uy, um = shift_month(py, planting, -MAX_USABLE_OFFSET)
    usable_from = date(uy, um, 1)
    closes = month_end(*shift_month(py, planting, k_close))
    status = "open" if today >= usable_from else "too_early"
    phase = "in_season" if today >= plant else "pre_season"
    # is a usable init actually PUBLISHED? (S2S data reaches latest_init)
    init_ready = False
    if status == "open" and latest_init:
        ly, lm = (int(x) for x in latest_init.split("-"))
        init_ready = date(ly, lm, 1) >= usable_from
    return {"status": status, "phase": phase,
            "planting": f"{py}-{planting:02d}",
            "harvest_year": harvest_year,
            "usable_from": f"{uy}-{um:02d}",
            "closes": closes.isoformat(),
            "usable_init_published": bool(init_ready)}


def run(path_config_files=None, *, parser=None, logger_obj=None,
        threshold_dir="crop_t0", today=None, out_dir=None):
    """Scan all country x crop combos and write eligibility.csv."""
    if parser is None:
        from geocif import logger as log
        logger_obj, parser = log.setup_logger_parser(path_config_files)
    project = parser.get("DEFAULT", "project_name", fallback="geocif")
    root = Path(parser.get("PATHS", "dir_output")) / project
    troot = root / threshold_dir

    if not troot.exists():
        raise FileNotFoundError(f"threshold root not reachable: {troot}")
    rows = []
    for merged in sorted(glob.glob(str(troot / "*" / "*_s?.csv"))):
        name = Path(merged).stem            # {country}_{crop}_s{n}
        m = re.match(r"(.+)_([a-z_]+)_s(\d)$", name)
        if not m:
            continue
        country = Path(merged).parent.name
        crop = m.group(2)
        if not name.startswith(country):
            continue
        try:
            planting, wraps = planting_and_span(merged)
        except Exception as e:
            logger.warning(f"{name}: calendar parse failed ({e})")
            continue
        if planting is None:
            continue
        # data checks
        admin_dirs = glob.glob(str(troot / country / "admin_*"))
        s2s_n, s2s_latest = (0, None)
        for ad in admin_dirs:
            n, latest = s2s_status(Path(ad) / "cr")
            if n:
                s2s_n, s2s_latest = n, latest
                break
        stats = root / "cid" / "indices" / parser.get(
            "DEFAULT", "method", fallback="monthly_r") / "global"
        cs = country.title().replace("_", " ")
        cr = crop.title().replace("_", " ")
        has_yields = (stats / f"{cs}_{cr}_statistics_monthly_r.csv").exists()

        st = window_state(planting, wraps, today=today, latest_init=s2s_latest)
        runnable = (st["status"] == "open" and st["usable_init_published"]
                    and s2s_n > 0 and has_yields)
        rows.append({"country": country, "crop": crop, "season": int(m.group(3)),
                     "planting_month": planting, "wraps": wraps, **st,
                     "s2s_files": s2s_n, "s2s_latest_init": s2s_latest,
                     "has_yield_stats": has_yields, "runnable_now": runnable})
    if not rows:
        raise RuntimeError(
            f"eligibility scan found no country x crop combos under {troot} "
            f"(share unreachable or wrong threshold_dir?)")
    df = pd.DataFrame(rows).sort_values(
        ["runnable_now", "status", "country"], ascending=[False, True, True])
    if out_dir:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        df.to_csv(Path(out_dir) / "eligibility.csv", index=False)
    logger.info(f"eligibility: {int(df['runnable_now'].sum())} runnable of {len(df)}")
    return df
