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


def aggregate_admin2(csv_path, product=None, admin_1=None):
    """Municipality rows -> production-weighted state series per year."""
    df = pd.read_csv(csv_path)
    if product:
        df = df[df["product"] == product]
    if admin_1:
        df = df[df["admin_1"].str.casefold() == str(admin_1).casefold()]
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


def compare(xlsx, csv, country, admin_1, product, out_csv=None, tol_pct=5.0,
            filter_admin_1=None, quiet=False):
    ref = load_admin1(xlsx, country, admin_1)
    agg = aggregate_admin2(csv, product, admin_1=filter_admin_1)

    m = ref.merge(agg, on="harvest_year", suffixes=("_admin1", "_admin2"))
    m = m.dropna(subset=["yield_admin1", "yield_admin2"])
    if m.empty:
        raise SystemExit("No overlapping years with data on both sides.")

    for q in ("yield", "area", "production"):
        a1, a2 = m[f"{q}_admin1"], m[f"{q}_admin2"]
        m[f"{q}_diff_pct"] = (a2 - a1) / a1.replace(0, np.nan) * 100

    y1, y2 = m["yield_admin1"], m["yield_admin2"]
    summary = {
        "admin_1": admin_1,
        "n_years": len(m),
        "year_min": int(m.harvest_year.min()),
        "year_max": int(m.harvest_year.max()),
        "corr": float(y1.corr(y2)),
        "mean_abs_diff_tha": float((y2 - y1).abs().mean()),
        "mapd_pct": float(m["yield_diff_pct"].abs().mean()),
        "bias_pct": float(m["yield_diff_pct"].mean()),
        "within_tol_pct": float((m["yield_diff_pct"].abs() <= tol_pct).mean() * 100),
    }

    if not quiet:
        print(f"Years compared      : {summary['n_years']}  "
              f"({summary['year_min']}-{summary['year_max']})")
        print(f"Municipalities/year : {int(m.n_units.min())}-{int(m.n_units.max())}")
        print(f"Yield correlation   : {summary['corr']:.4f}")
        print(f"Mean |diff|         : {summary['mean_abs_diff_tha']:.4f} t/ha "
              f"({summary['mapd_pct']:.2f}%)")
        print(f"Mean signed bias    : {summary['bias_pct']:+.2f}%  (admin_2 vs admin_1)")
        print(f"Years within +-{tol_pct:.0f}%   : {summary['within_tol_pct']:.0f}%")
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
        if not quiet:
            print(f"\nwrote {out_csv}")
    return m, summary


def compare_all_states(xlsx, csv, country, product, out_csv=None, tol_pct=5.0):
    """One comparison per state present on BOTH sides; per-state summary table.

    States are matched case-insensitively between the wide CSV's ``admin_1``
    column and the GEOGLAM sheet's ``ADM1_NAME`` values.
    """
    xl = pd.ExcelFile(xlsx)
    ref_states = xl.parse(SHEETS["yield"])
    ref_states = ref_states.loc[ref_states["ADM0_NAME"] == country, "ADM1_NAME"].dropna()
    ref_by_fold = {str(s).casefold(): s for s in ref_states}

    csv_states = sorted(pd.read_csv(csv, usecols=["admin_1"])["admin_1"].unique())
    rows, per_year = [], []
    skipped = [s for s in csv_states if s.casefold() not in ref_by_fold]
    for state in csv_states:
        ref_name = ref_by_fold.get(state.casefold())
        if ref_name is None:
            continue
        m, summary = compare(xlsx, csv, country, ref_name, product,
                             tol_pct=tol_pct, filter_admin_1=state, quiet=True)
        rows.append(summary)
        per_year.append(m.assign(admin_1=ref_name))

    summary_df = pd.DataFrame(rows).sort_values("mapd_pct")
    print(f"{len(rows)} states compared; {len(skipped)} CSV states absent from "
          f"the GEOGLAM workbook (skipped): {skipped}")
    print(summary_df.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    w = summary_df["n_years"]
    has_corr = summary_df["corr"].notna()  # single-year states have no corr
    print(f"\nAcross states (year-weighted): "
          f"corr {np.average(summary_df.loc[has_corr, 'corr'], weights=w[has_corr]):.4f} | "
          f"MAPD {np.average(summary_df['mapd_pct'], weights=w):.2f}% | "
          f"bias {np.average(summary_df['bias_pct'], weights=w):+.2f}%")

    if out_csv:
        out_csv = Path(out_csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        summary_df.to_csv(out_csv, index=False)
        long_csv = out_csv.with_name(out_csv.stem + "_per_year.csv")
        pd.concat(per_year, ignore_index=True).to_csv(long_csv, index=False)
        print(f"\nwrote {out_csv}\nwrote {long_csv}")
    return summary_df


def check_national_vs_br_row(sidra_csv, wide_csv, product_label, product):
    """Sum every municipality in the wide CSV and compare against SIDRA's own
    Brasil (level ``BR``) row — a parser/aggregation exactness check."""
    from .convert_tabela1612 import parse_sidra_blocks

    blocks = parse_sidra_blocks(sidra_csv, product_label, level="BR")
    br = blocks["area"].rename(columns={"value": "area"})[["year", "area"]].merge(
        blocks["production"].rename(columns={"value": "production"})[["year", "production"]],
        on="year")
    br["yield_br"] = br["production"] / br["area"]

    df = pd.read_csv(wide_csv)
    df = df[df["product"] == product]
    agg = df.groupby("harvest_year").agg(area=("area", "sum"),
                                         production=("production", "sum")).reset_index()
    agg["yield_mu"] = agg["production"] / agg["area"]

    m = br.merge(agg, left_on="year", right_on="harvest_year",
                 suffixes=("_br", "_mu")).dropna(subset=["yield_br", "yield_mu"])
    m["yield_diff_pct"] = (m["yield_mu"] - m["yield_br"]) / m["yield_br"] * 100
    m["prod_diff_pct"] = (m["production_mu"] - m["production_br"]) / m["production_br"] * 100
    worst = m["yield_diff_pct"].abs().max()
    print(f"National check vs SIDRA BR row: {len(m)} years, "
          f"max |yield diff| {worst:.4f}%, max |production diff| "
          f"{m['prod_diff_pct'].abs().max():.4f}%")
    return m


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    base = r"D:\Users\ritvik\projects\GEO\config\brazil_mt\assets"
    p.add_argument("--admin1-xlsx", default=r"Z:\cmongp1\GEO\inputs\metadata\production_statistics\soybean_1.xlsx")
    p.add_argument("--admin2-csv", default=base + r"\adm_crop_production_BR_MT_municipality_wide.csv")
    p.add_argument("--country", default="Brazil")
    p.add_argument("--admin-1", default="Mato Grosso",
                   help="one ADM1_NAME, or ALL for a per-state sweep (needs the "
                        "wide CSV's admin_1 column to be per-municipality)")
    p.add_argument("--product", default="Soybean")
    p.add_argument("--product-label", default="Soja (em grão)",
                   help="SIDRA product column (only used with --sidra-csv)")
    p.add_argument("--sidra-csv", default=None,
                   help="raw Tabela 1612 export; adds the national-vs-BR-row check")
    p.add_argument("--out", default=base + r"\admin1_vs_admin2_yield_comparison.csv")
    p.add_argument("--tol-pct", type=float, default=5.0)
    a = p.parse_args(argv)
    if a.admin_1.upper() == "ALL":
        compare_all_states(a.admin1_xlsx, a.admin2_csv, a.country, a.product,
                           out_csv=a.out, tol_pct=a.tol_pct)
    else:
        compare(a.admin1_xlsx, a.admin2_csv, a.country, a.admin_1, a.product,
                out_csv=a.out, tol_pct=a.tol_pct, filter_admin_1=a.admin_1)
    if a.sidra_csv:
        check_national_vs_br_row(a.sidra_csv, a.admin2_csv, a.product_label, a.product)


if __name__ == "__main__":
    sys.exit(main())
