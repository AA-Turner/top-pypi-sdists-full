"""Cross-check an admin_2 (municipality/county) yield file against the
admin_1 (state/province) statistics the pipeline already trusts.

Aggregating admin_2 the way a production-weighted national/state total is
formed --- ``sum(production) / sum(area)``, NOT a plain mean of yields ---
must reproduce the admin_1 series closely. Large or systematic gaps mean the
two sources disagree (different survey agencies), the units are wrong, or
municipalities are missing from the admin_2 file.

Reference (admin_1) is read from the GEOGLAM workbook ``{crop}_{season}.xlsx``
(sheets ``Yield (tn per ha)`` / ``Area (ha)`` / ``Production (tn)``, one column
per harvest year); the admin_2 side is the hvstat-style wide CSV written by
``convert_tabela1612``. Emits a per-year comparison CSV alongside the printed
summary (every figure gets a companion table).
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SHEETS = {
    "yield": "Yield (tn per ha)",
    "area": "Area (ha)",
    "production": "Production (tn)",
}


def load_admin1(xlsx_path, country, admin_1):
    """Wide GEOGLAM workbook -> DataFrame(harvest_year, yield/area/production)."""
    out = {}
    xl = pd.ExcelFile(xlsx_path)
    for key, sheet in SHEETS.items():
        if sheet not in xl.sheet_names:
            continue
        df = xl.parse(sheet)
        row = df[(df["ADM0_NAME"] == country) & (df["ADM1_NAME"] == admin_1)]
        if row.empty:
            raise SystemExit(f"{admin_1!r} not found on sheet {sheet!r} of {xlsx_path}")
        years = [c for c in row.columns if isinstance(c, (int, np.integer))]
        out[key] = row[years].iloc[0]
    ref = pd.DataFrame(out)
    ref.index.name = "harvest_year"
    return ref.reset_index()


def aggregate_admin2(csv_path, product=None):
    """Municipality rows -> production-weighted state series per year."""
    df = pd.read_csv(csv_path)
    if product:
        df = df[df["product"] == product]
    g = df.groupby("harvest_year")
    agg = g.agg(
        area=("area", "sum"),
        production=("production", "sum"),
        n_units=("admin_2", "nunique"),
    ).reset_index()
    # Weighted yield is total production over total area -- the same identity
    # the pipeline's own parent aggregation uses. A plain mean of municipality
    # yields over-weights tiny producers and will not match admin_1.
    agg["yield"] = agg["production"] / agg["area"].replace(0, np.nan)
    agg["yield_unweighted_mean"] = g["yield"].mean().values
    return agg


def compare(xlsx, csv, country, admin_1, product, out_csv=None, tol_pct=5.0):
    ref = load_admin1(xlsx, country, admin_1)
    agg = aggregate_admin2(csv, product)

    m = ref.merge(agg, on="harvest_year", suffixes=("_admin1", "_admin2"))
    m = m.dropna(subset=["yield_admin1", "yield_admin2"])
    if m.empty:
        raise SystemExit("No overlapping years with data on both sides.")

    for q in ("yield", "area", "production"):
        a1, a2 = m[f"{q}_admin1"], m[f"{q}_admin2"]
        m[f"{q}_diff_pct"] = (a2 - a1) / a1.replace(0, np.nan) * 100

    y1, y2 = m["yield_admin1"], m["yield_admin2"]
    corr = y1.corr(y2)
    mad = float((y2 - y1).abs().mean())
    mapd = float(m["yield_diff_pct"].abs().mean())
    bias = float(m["yield_diff_pct"].mean())
    within = float((m["yield_diff_pct"].abs() <= tol_pct).mean() * 100)

    print(f"Years compared      : {len(m)}  ({int(m.harvest_year.min())}-{int(m.harvest_year.max())})")
    print(f"Municipalities/year : {int(m.n_units.min())}-{int(m.n_units.max())}")
    print(f"Yield correlation   : {corr:.4f}")
    print(f"Mean |diff|         : {mad:.4f} t/ha ({mapd:.2f}%)")
    print(f"Mean signed bias    : {bias:+.2f}%  (admin_2 vs admin_1)")
    print(f"Years within +-{tol_pct:.0f}%   : {within:.0f}%")
    print(f"Area  mean diff     : {m['area_diff_pct'].mean():+.2f}%")
    print(f"Prod. mean diff     : {m['production_diff_pct'].mean():+.2f}%")

    show = m[["harvest_year", "n_units", "yield_admin1", "yield_admin2",
              "yield_diff_pct", "area_diff_pct", "production_diff_pct"]]
    print("\nPer-year (worst 8 by |yield diff|):")
    print(show.reindex(show["yield_diff_pct"].abs().sort_values(ascending=False).index)
          .head(8).to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    if out_csv:
        Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
        m.to_csv(out_csv, index=False)
        print(f"\nwrote {out_csv}")
    return m


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    base = r"D:\Users\ritvik\projects\GEO\config\brazil_mt\assets"
    p.add_argument("--admin1-xlsx", default=r"Z:\cmongp1\GEO\inputs\metadata\production_statistics\soybean_1.xlsx")
    p.add_argument("--admin2-csv", default=base + r"\adm_crop_production_BR_MT_municipality_wide.csv")
    p.add_argument("--country", default="Brazil")
    p.add_argument("--admin-1", default="Mato Grosso")
    p.add_argument("--product", default="Soybean")
    p.add_argument("--out", default=base + r"\admin1_vs_admin2_yield_comparison.csv")
    p.add_argument("--tol-pct", type=float, default=5.0)
    a = p.parse_args(argv)
    compare(a.admin1_xlsx, a.admin2_csv, a.country, a.admin_1, a.product,
            out_csv=a.out, tol_pct=a.tol_pct)


if __name__ == "__main__":
    sys.exit(main())
