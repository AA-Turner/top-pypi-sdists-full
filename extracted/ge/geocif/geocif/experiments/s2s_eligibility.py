"""Which country x crop combinations can be pre-season forecast from S2S now?

Scans the geoprepare output tree for merged crop CSVs, derives each combo's
planting month and season shape from the crop-calendar columns in the data,
and reports the state of its NEXT season's pre-season S2S window:

    open        a USABLE init (>= MIN_OFFSET months of season visibility,
                i.e. issued no earlier than ``planting - MAX_USABLE_OFFSET``)
                is already available -> the pooled model can run today.
    too_early   the window has not reached a usable init yet (June-type
                truncated inits are excluded on purpose -- proven harmful);
                reports the month it becomes usable.
    in_season   planting has passed; the pre-season lens is closed and the
                in-season CID system owns the forecast.

Data checks per combo: S2S per-region CSVs present (and their latest init),
and a materialized statistics file (yields) so the combo can contribute
training rows.

Usage::

    from geocif.experiments import s2s_eligibility
    df = s2s_eligibility.run(parser=parser)          # or path_config_files
"""
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


def window_state(planting, wraps, today=None, latest_init=None):
    """Eligibility of the NEXT season's pre-season window."""
    today = today or date.today()
    # next planting date
    py = today.year if today.month <= planting else today.year + 1
    plant = date(py, planting, 1)
    harvest_year = py + 1 if wraps else py
    # usable window: planting - MAX_USABLE_OFFSET .. planting - 1
    um = planting - MAX_USABLE_OFFSET
    uy = py
    if um <= 0:
        um += 12
        uy -= 1
    usable_from = date(uy, um, 1)
    if today >= plant:
        status = "in_season"
    elif today >= usable_from:
        status = "open"
    else:
        status = "too_early"
    # is a usable init actually PUBLISHED? (S2S data reaches latest_init)
    init_ready = False
    if status == "open" and latest_init:
        ly, lm = (int(x) for x in latest_init.split("-"))
        init_ready = date(ly, lm, 1) >= usable_from
    return {"status": status, "planting": f"{py}-{planting:02d}",
            "harvest_year": harvest_year,
            "usable_from": f"{uy}-{um:02d}",
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
