"""Convert an IBGE SIDRA Tabela 1612 export into the hvstat-style wide
production-statistics CSV that geocif's ``production_statistics_file`` key
consumes (the vectorized path in geocif/ml/stats.py, as used by usa_admin2).

Tabela 1612 layout (as exported from sidra.ibge.gov.br):
- one title line, then up to three stacked blocks, each opened by a
  ``"Variável - <name>"`` line: Área colhida (Hectares), Quantidade produzida
  (Toneladas), Rendimento médio da produção (Quilogramas por Hectare);
- each block: a years row (paired columns per year) and a products row
  (``Total``, ``Soja (em grão)``, ...) followed by data rows
  ``"<Nível>","<Cód.>","<Name (UF)>", v, v, ...``;
- missing-data markers: ``-`` (zero/nonexistent), ``..``/``...`` (n/a),
  and IBGE marks preliminary years in the footnotes.

Output: one row per (municipality, harvest_year) with columns
country, fnid, admin_1, admin_2, ibge_name, num_ID, product, season_name,
crop_production_system, qc_flag, harvest_year, yield, area, production —
yield in t/ha (Rendimento médio / 1000, falling back to production/area),
area in ha, production in t. ``admin_2`` strings are taken from the lookup
CSV written by build_mt_boundary, joined on the IBGE code, so they match the
boundary shapefile by construction.
"""

import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MISSING = {"-", "..", "...", ""}

# Substring of the "Variável - ..." line -> canonical block key
BLOCK_KEYS = {
    "colhida": "area",
    "produzida": "production",
    "Rendimento": "yield_kg_ha",
}


def _to_float(cell):
    cell = (cell or "").strip()
    if cell in MISSING:
        return np.nan
    try:
        return float(cell.replace(",", "."))
    except ValueError:
        return np.nan


def parse_sidra_blocks(path, product_label, level="MU", code_prefix=None):
    """Parse every ``Variável`` block into a long DataFrame.

    Returns dict {block_key: DataFrame(code, name, year, value)} keeping only
    rows at administrative ``level`` (``MU`` = municipality) and, optionally,
    only codes starting with ``code_prefix`` (e.g. ``"51"`` = Mato Grosso).
    """
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))

    blocks, current = {}, None
    years, product_cols = [], []
    for row in rows:
        if not row:
            continue
        first = (row[0] or "").strip()
        if first.startswith("Variável"):
            key = next((v for k, v in BLOCK_KEYS.items() if k in first), None)
            current = key
            if key is not None and key not in blocks:
                blocks[key] = []
            years, product_cols = [], []
            continue
        if current is None:
            continue
        if first == "Nível" and len(row) > 3:
            if row[3].strip().isdigit():          # the years row
                years = row[3:]
            elif years and row[3].strip():        # the products row
                product_cols = row[3:]
            continue
        if first == level and len(row) > 3:
            code = row[1].strip()
            if code_prefix and not code.startswith(code_prefix):
                continue
            name = row[2].strip()
            # forward-fill the paired year headers onto every product column
            year_for_col, last_year = [], None
            for y in years:
                y = y.strip()
                if y.isdigit():
                    last_year = int(y)
                year_for_col.append(last_year)
            # SIDRA's years row ends ON the final year with no trailing pad
            # cell, while the products row still carries that year's full
            # column pair — pad so the last year's product columns keep it.
            if len(year_for_col) < len(product_cols):
                year_for_col += [last_year] * (len(product_cols) - len(year_for_col))
            for i, val in enumerate(row[3:]):
                if i >= len(product_cols):
                    break
                if product_cols[i].strip() != product_label:
                    continue
                year = year_for_col[i] if i < len(year_for_col) else None
                if year is None:
                    continue
                blocks[current].append(
                    {"code": code, "name": name, "year": year, "value": _to_float(val)}
                )

    return {k: pd.DataFrame(v) for k, v in blocks.items() if v}


def build_wide(blocks, lookup, country, admin_1, product, season_name="Main"):
    """Merge the parsed blocks into the hvstat wide schema."""
    merged = None
    for key in ("area", "production", "yield_kg_ha"):
        df = blocks.get(key)
        if df is None or df.empty:
            continue
        df = df.rename(columns={"value": key})[["code", "name", "year", key]]
        merged = df if merged is None else merged.merge(
            df.drop(columns="name"), on=["code", "year"], how="outer"
        )
    if merged is None:
        raise SystemExit("No data blocks parsed — is this a Tabela 1612 export?")

    for col in ("area", "production", "yield_kg_ha"):
        if col not in merged.columns:
            merged[col] = np.nan

    merged["yield"] = merged["yield_kg_ha"] / 1000.0
    fallback = merged["yield"].isna() & merged["area"].gt(0) & merged["production"].notna()
    merged.loc[fallback, "yield"] = merged.loc[fallback, "production"] / merged.loc[fallback, "area"]

    lookup = lookup.copy()
    lookup["CD_MUN"] = lookup["CD_MUN"].astype(str)
    out = merged.merge(lookup, left_on="code", right_on="CD_MUN", how="left")
    unmatched = out.loc[out["admin_2"].isna(), ["code", "name"]].drop_duplicates()
    if not unmatched.empty:
        print(f"WARNING: {len(unmatched)} municipality code(s) not in the boundary "
              f"lookup (dropped): {unmatched['name'].tolist()[:8]}")
        out = out.dropna(subset=["admin_2"])

    out = out.dropna(subset=["yield", "area", "production"], how="all")
    wide = pd.DataFrame({
        "country": country,
        "fnid": out["code"],
        "admin_1": admin_1,
        "admin_2": out["admin_2"],
        "ibge_name": out["NM_MUN"],
        "num_ID": out["code"].astype(int),
        "product": product,
        "season_name": season_name,
        "crop_production_system": "none",
        "qc_flag": 0,
        "harvest_year": out["year"].astype(int),
        "yield": out["yield"],
        "area": out["area"],
        "production": out["production"],
    })
    return wide.sort_values(["admin_2", "harvest_year"]).reset_index(drop=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--csv", default=r"C:\Users\ritvik\Downloads\tabela1612.csv")
    p.add_argument("--lookup", default=r"D:\Users\ritvik\projects\GEO\config\brazil_mt\assets\mt_municipality_lookup.csv")
    p.add_argument("--code-prefix", default="51", help="IBGE state code prefix (51 = MT)")
    p.add_argument("--product-label", default="Soja (em grão)", help="SIDRA product column")
    p.add_argument("--product", default="Soybean", help="geocif crop display name")
    p.add_argument("--country", default="Brazil")
    p.add_argument("--admin-1", default="Mato Grosso")
    p.add_argument("--out", default=r"D:\Users\ritvik\projects\GEO\config\brazil_mt\assets\adm_crop_production_BR_MT_municipality_wide.csv")
    a = p.parse_args(argv)

    blocks = parse_sidra_blocks(a.csv, a.product_label, code_prefix=a.code_prefix)
    print({k: len(v) for k, v in blocks.items()}, "raw (code,year) values per block")
    lookup = pd.read_csv(a.lookup)
    wide = build_wide(blocks, lookup, a.country, a.admin_1, a.product)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    wide.to_csv(a.out, index=False)
    ok = wide["yield"].notna()
    print(f"{len(wide)} rows | {wide['admin_2'].nunique()} municipalities | "
          f"years {wide['harvest_year'].min()}-{wide['harvest_year'].max()} | "
          f"yield non-null {ok.sum()} ({ok.mean() * 100:.1f}%), "
          f"range {wide['yield'].min():.2f}-{wide['yield'].max():.2f} t/ha")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    sys.exit(main())
