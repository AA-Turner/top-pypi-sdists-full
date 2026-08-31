"""Gate-0 validation: cross-check the admin_2 boundary shapefile and the
hvstat-style yield CSV before anything is uploaded to the cluster.

Checks (hard failures exit non-zero):
1. every yield-CSV ``admin_2`` (underscore-folded) exists in the shapefile's
   ``ADM2_NAME`` set (space/underscore-insensitive, as the pipeline matches);
2. all names on both sides are pure ASCII (the pipeline never folds accents);
3. yields lie in a plausible range (default 0.3-7 t/ha) — out-of-range rows
   are listed, tolerated only below a small fraction;
4. reported yield vs production/area agreement (|rel diff| <= 5%) where all
   three are present;
5. per-year municipality counts (printed) and duplicate (admin_2, year) rows.

Writes a companion CSV of every flagged row next to the yield CSV.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def norm(s):
    return str(s).lower().replace("_", " ").strip()


def validate(shp_path, yield_csv, lo=0.3, hi=7.0, flag_frac=0.02):
    import geopandas as gpd

    gdf = gpd.read_file(shp_path, engine="pyogrio")
    df = pd.read_csv(yield_csv)
    problems = []
    failed = False

    shp_names = set(gdf["ADM2_NAME"].map(norm))
    csv_names = set(df["admin_2"].map(norm))
    missing = sorted(csv_names - shp_names)
    if missing:
        failed = True
        print(f"FAIL name-match: {len(missing)} yield regions absent from shapefile: {missing[:10]}")
    else:
        print(f"PASS name-match: all {len(csv_names)} yield regions found in shapefile "
              f"({len(shp_names)} polygons; {len(shp_names - csv_names)} polygons without yields)")

    bad_ascii = [n for n in csv_names | shp_names if not n.isascii()]
    if bad_ascii:
        failed = True
        print(f"FAIL ascii: non-ASCII names: {bad_ascii[:10]}")
    else:
        print("PASS ascii: all names pure ASCII")

    y = df["yield"].dropna()
    out_of_range = df[(df["yield"] < lo) | (df["yield"] > hi)].dropna(subset=["yield"])
    frac = len(out_of_range) / max(len(y), 1)
    print(f"{'PASS' if frac <= flag_frac else 'FAIL'} yield-range: {len(out_of_range)}/{len(y)} "
          f"rows outside [{lo}, {hi}] t/ha ({frac * 100:.2f}%); "
          f"observed range {y.min():.2f}-{y.max():.2f}")
    if frac > flag_frac:
        failed = True
    problems.append(out_of_range.assign(check="yield_range"))

    both = df.dropna(subset=["yield", "area", "production"])
    both = both[both["area"] > 0]
    rel = (both["production"] / both["area"] - both["yield"]).abs() / both["yield"].clip(lower=1e-9)
    disagree = both[rel > 0.05]
    print(f"{'PASS' if len(disagree) == 0 else 'WARN'} consistency: "
          f"{len(disagree)}/{len(both)} rows where production/area differs from yield by >5%")
    problems.append(disagree.assign(check="prod_area_vs_yield"))

    dupes = df[df.duplicated(subset=["admin_2", "harvest_year"], keep=False)]
    if len(dupes):
        failed = True
        print(f"FAIL duplicates: {len(dupes)} duplicated (admin_2, harvest_year) rows")
        problems.append(dupes.assign(check="duplicate_region_year"))
    else:
        print("PASS duplicates: (admin_2, harvest_year) unique")

    counts = df.dropna(subset=["yield"]).groupby("harvest_year")["admin_2"].nunique()
    print("municipalities with yield, by year (first/last 5):")
    print(pd.concat([counts.head(5), counts.tail(5)]).to_string())

    flagged = pd.concat([p for p in problems if not p.empty], ignore_index=True) \
        if any(not p.empty for p in problems) else pd.DataFrame()
    out = Path(yield_csv).with_name(Path(yield_csv).stem + "_validation_flags.csv")
    flagged.to_csv(out, index=False)
    print(f"{len(flagged)} flagged rows -> {out}")

    print("GATE 0:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    base = r"D:\Users\ritvik\projects\GEO\config\brazil_mt\assets"
    p.add_argument("--shp", default=base + r"\brazil_mt_municipalities.shp")
    p.add_argument("--yield-csv", default=base + r"\adm_crop_production_BR_MT_municipality_wide.csv")
    a = p.parse_args(argv)
    return validate(a.shp, a.yield_csv)


if __name__ == "__main__":
    sys.exit(main())
