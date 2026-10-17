"""Convert an AMIS/EWCM (GEOGLAM-format) yield workbook into the hvstat-style
production-statistics CSV.

geocif reads such workbooks directly -- ``production_statistics_file =
bangladesh_rice.xlsx`` works as is (geocif.ml.stats.read_production_statistics)
-- so this is only needed when a CSV copy is wanted, e.g. to inspect the long
table or to merge it with other HarvestStat data. The conversion is
geocif.ml.stats.geoglam_workbook_to_long, the same code the join uses.

Input: a workbook laid out like the AMIS/GEOGLAM ``<crop>_<season>.xlsx``
files, e.g. ``bangladesh_rice.xlsx`` (BBS district rice statistics). One sheet
per statistic -- ``Yield (tn per ha)``, ``Area (ha)``, ``Production (tn)`` --
each with id columns ``ADM0_NAME, ADM1_NAME, [ADM2_NAME], Season,
[CM_Season], [Source], [num_ID]`` and one column per year. A missing sheet
leaves that column empty.

Harvest year. The year columns are copied unchanged into ``harvest_year``,
which is how geocif's GEOGLAM reader (``add_GEOGLAM_statistics``) interprets
them.

Season. ``Season`` becomes ``season_name`` and ``CM_Season`` becomes
``cm_season``; every season in the workbook is kept. add_statistics picks a
run's season by ``cm_season`` when the file has it (Boro = 1, Aman = 2,
Aus = 3 in bangladesh_rice.xlsx), otherwise by name.

Output: one row per (admin unit, season, harvest_year) with columns
country, fnid, admin_1, [admin_2], num_ID, product, season_name, cm_season,
crop_production_system, qc_flag, harvest_year, yield, area, production,
source -- yield in t/ha, area in ha, production in t, qc_flag 0.

Usage::

    python -m geocif.data_prep.convert_geoglam_xlsx \\
        --xlsx production_statistics/bangladesh_rice.xlsx --product Rice \\
        --out production_statistics/bangladesh_rice_hvstat.csv
"""

import argparse
import sys
from pathlib import Path

from geocif.ml.stats import geoglam_workbook_to_long


def convert(xlsx, product, country=None):
    out = geoglam_workbook_to_long(xlsx, product=product)
    if country is not None:
        out = out[out["country"].astype(str).str.lower() == country.lower()].reset_index(drop=True)
        if out.empty:
            raise ValueError(f"{xlsx} has no rows for country {country!r}")
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--xlsx", required=True, help="GEOGLAM-format workbook (one sheet per statistic)")
    p.add_argument("--product", required=True, help="geocif product name, e.g. Rice")
    p.add_argument("--country", default=None, help="keep only this ADM0_NAME (default: all)")
    p.add_argument("--out", required=True)
    a = p.parse_args(argv)

    try:
        out = convert(a.xlsx, a.product, country=a.country)
    except ValueError as exc:
        raise SystemExit(str(exc))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(a.out, index=False, encoding="utf-8")
    admin = "admin_2" if "admin_2" in out.columns else "admin_1"
    ok = out["yield"].notna()
    print(f"{len(out)} rows | {out[admin].nunique()} {admin} units | seasons "
          f"{out['season_name'].value_counts().to_dict()} | years "
          f"{out['harvest_year'].min()}-{out['harvest_year'].max()} | yield non-null {int(ok.sum())}")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    sys.exit(main())
