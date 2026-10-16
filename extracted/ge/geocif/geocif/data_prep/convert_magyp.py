"""Convert the MAGyP "Estimaciones Agricolas" CSV into the hvstat-style
production-statistics CSV that geocif's ``production_statistics_file`` key
consumes (the vectorized path in geocif/ml/stats.py, as used by usa_admin2
and brazil_admin2).

Source: Ministerio de Agricultura, Ganaderia y Pesca, Direccion de
Estimaciones Agricolas -- datos.magyp.gob.ar dataset ``estimaciones-agricolas``,
resource ``estimaciones-agricolas-YYYY-MM.csv`` (the full series; the
per-crop ``<cultivo>-siembra-cosecha-produccion-rendimiento`` series share
the schema). One row per (cultivo, campania, provincia, departamento):
``cultivo, anio, campania ("2022/23"), provincia, provincia_id, departamento,
departamento_id, superficie_sembrada_ha, superficie_cosechada_ha,
produccion_tm, rendimiento_kgxha``. ``departamento_id`` is the 5-digit INDEC
code (``06854`` = 25 de Mayo, Buenos Aires), the code build_ar_boundary
stores as ``INDEC``/``num_ID`` -- so the join is by code, never by name, and
``admin_2`` is copied from the boundary lookup CSV.

Harvest year. geocif joins yields on (Region, Harvest Year), and the harvest
year of a merged EO row is set by geoprepare's
``geomerge.assign_harvest_season`` from the crop calendar of the
department's calendar region: a season is labelled with the calendar year in
which its in-season block ENDS. A campaign ``2022/23`` therefore maps to

- 2023 where the calendar wraps the year boundary (every Argentine region
  for soybean_1 and maize_1; Buenos Aires and La Pampa for winter_wheat,
  whose harvest runs into mid-January), and
- 2022 where it does not (Cordoba, Santa Fe, Entre Rios, Northern and
  Northwest for winter_wheat: harvest ends in December).

The rule is evaluated here from the calendar workbook (``--calendar``, the
AMIS workbook; sheet ``<crop>_<season>`` or ``winter_wheat``) with the same
stage logic as geomerge, per calendar region; the department -> calendar
region mapping is the lookup CSV's ``calendar_region`` column (written by the
project's validate step from geoprepare's overlay). The GEOGLAM admin_1
workbooks label every campaign by its END year, which is one year off from
geomerge for the non-wrapping wheat regions -- do not copy that convention.

Output: one row per (department, product, harvest_year) with columns
country, fnid, admin_1, admin_2, magyp_name, num_ID, product, season_name,
crop_production_system, qc_flag, harvest_year, yield, area, production --
yield in t/ha (rendimiento_kgxha / 1000, falling back to production/area),
area = superficie_cosechada_ha (ha), production = produccion_tm (t).
"""

import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# geocif product name -> candidate MAGyP ``cultivo`` labels, first present
# wins. Sub-series such as "Soja 1ra" / "Soja 2da" are deliberately NOT
# listed: the total is what the department yield means.
CROP_LABELS = {
    "Soybean": ["Soja total", "Soja", "SOJA TOTAL", "SOJA"],
    "Maize": ["Maíz", "Maiz", "MAÍZ", "MAIZ", "Maíz total", "Maiz total"],
    "Winter Wheat": ["Trigo total", "Trigo", "TRIGO TOTAL", "TRIGO"],
}
# geocif crop slug -> calendar sheet (geoprepare: "<crop>_<season>", wheat has no season suffix)
CALENDAR_SHEET = {"Soybean": "soybean_1", "Maize": "maize_1", "Winter Wheat": "winter_wheat"}
COUNTRY = "Argentina"
COUNTRY_SLUG = "argentina"
# Plausible department-mean yield range (t/ha) per product. Rows outside it get
# qc_flag = 1 (geocif keeps only qc_flag == 0 rows), which is what MAGyP's
# tiny-area artefacts (3 ha reported at 33 t/ha) need; zeros are left alone
# because geocif already treats a zero yield as missing.
PLAUSIBLE = {"Soybean": (0.2, 6.0), "Maize": (0.3, 16.0), "Winter Wheat": (0.2, 8.0)}
# MAGyP departamento_id -> INDEC code used by the IGN layer. INDEC renumbered
# Chascomus from 06217 to 06218 when Lezama (06466) was split off in 2009; MAGyP
# still reports Chascomus as 06217 for every campaign. Pre-2009 rows therefore
# describe the larger pre-split partido but are joined to today's polygon.
CODE_ALIASES = {"06217": "06218"}
HALF_MONTHS = [f"{m}_{d}" for m in ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                                     "sep", "oct", "nov", "dec") for d in ("1", "15")]
REQUIRED = ["cultivo", "campania", "departamento", "departamento_id",
            "superficie_cosechada_ha", "produccion_tm", "rendimiento_kgxha"]


def normalize_region(name):
    """geoprepare.georegion._normalize: strip, lower, spaces -> underscores."""
    return str(name).strip().lower().replace(" ", "_")


def normalize_label(text):
    """Case- and accent-insensitive key for MAGyP ``cultivo`` labels
    (``Maíz`` == ``maiz`` == ``MAIZ``)."""
    import unicodedata

    decomposed = unicodedata.normalize("NFD", str(text))
    return " ".join("".join(c for c in decomposed if not unicodedata.combining(c)).lower().split())


def season_wraps(calendar_values):
    """True when geomerge.assign_harvest_season labels the season with the
    NEXT calendar year for its planting half (0.6.334 logic): stage 4 counts
    as off-season (0); a row that is in-season at both ends of the year with
    an off-season gap in between wraps. Returns None for a row with no season
    (all -1 / all 0)."""
    cal = np.array([0 if v == 4 else v for v in calendar_values], dtype=float)
    if np.all(cal < 0) or not np.any(cal > 0):
        return None
    cal[cal < 0] = 0
    if cal[0] == 0 or cal[-1] == 0:
        return False
    return bool(np.any(cal == 0))


def harvest_year_rules(calendar_xlsx, country_slug=COUNTRY_SLUG):
    """{product: {calendar_region: wraps(bool) | None}} from the AMIS workbook."""
    rules = {}
    xl = pd.ExcelFile(calendar_xlsx)
    for product, sheet in CALENDAR_SHEET.items():
        if sheet not in xl.sheet_names:
            raise SystemExit(f"sheet {sheet!r} not in {calendar_xlsx}: {xl.sheet_names}")
        df = xl.parse(sheet)
        country_col = next((c for c in df.columns if str(c).lower() == "country"), None)
        admin_col = next((c for c in df.columns if str(c).lower() == "admin"), None)
        missing = [c for c in HALF_MONTHS if c not in df.columns]
        if country_col is None or admin_col is None or missing:
            raise SystemExit(f"sheet {sheet!r}: need country/admin + {HALF_MONTHS}; missing {missing}")
        sub = df[df[country_col].astype(str).str.lower().str.replace(" ", "_") == country_slug]
        if sub.empty:
            raise SystemExit(f"sheet {sheet!r} has no {country_slug} rows")
        rules[product] = {
            normalize_region(r[admin_col]): season_wraps([r[c] for c in HALF_MONTHS])
            for _, r in sub.iterrows()
        }
    return rules


def parse_campaign(value):
    """'2022/23' -> (2022, 2023); '1999/00' -> (1999, 2000); '2022' -> (2022, 2023)."""
    s = str(value).strip()
    m = re.fullmatch(r"(\d{4})\s*/\s*(\d{2,4})", s)
    if m:
        start = int(m.group(1))
        end = int(m.group(2))
        if end < 100:
            end = (start // 100) * 100 + end
            if end < start:
                end += 100
        return start, end
    if re.fullmatch(r"\d{4}", s):
        return int(s), int(s) + 1
    raise ValueError(f"unrecognised campania {value!r}")


def _read_magyp(path):
    for enc in ("utf-8-sig", "latin-1"):
        try:
            df = pd.read_csv(path, dtype=str, encoding=enc, keep_default_na=False)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise SystemExit(f"could not decode {path}")
    df.columns = [c.strip().lower() for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise SystemExit(f"{path}: missing columns {missing}; got {list(df.columns)}")
    return df


def _to_num(series):
    s = series.astype(str).str.strip().str.replace(",", ".", regex=False)
    return pd.to_numeric(s.where(~s.isin(["", "-", "..", "...", "nan", "NaN", "SD", "s/d"])), errors="coerce")


def convert(magyp_csv, lookup_csv, calendar_xlsx, products=("Soybean", "Maize", "Winter Wheat"),
            label_overrides=None, country=COUNTRY):
    raw = _read_magyp(magyp_csv)
    labels_present = sorted(raw["cultivo"].str.strip().unique())
    print(f"{len(raw)} MAGyP rows; cultivo labels: {labels_present}")

    lookup = pd.read_csv(lookup_csv, dtype={"INDEC": str})
    for col in ("INDEC", "num_ID", "ADM1_NAME", "ADM2_NAME", "admin_2"):
        if col not in lookup.columns:
            raise SystemExit(f"lookup {lookup_csv} lacks column {col!r}")
    lookup["INDEC"] = lookup["INDEC"].str.zfill(5)
    if "calendar_region" not in lookup.columns:
        raise SystemExit("lookup has no calendar_region column: run the validate step's overlay first")
    lookup["calendar_region"] = lookup["calendar_region"].map(
        lambda v: normalize_region(v) if isinstance(v, str) and v.strip() else None)

    rules = harvest_year_rules(calendar_xlsx)
    raw["code"] = raw["departamento_id"].str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(5)
    raw["code"] = raw["code"].replace(CODE_ALIASES)
    # "sin definir" = province totals not assigned to a department (code XX000)
    undefined = raw["code"].str.endswith("000")
    if undefined.any():
        print(f"NOTE: {int(undefined.sum())} rows are province-level 'sin definir' (department code XX000); dropped")
        raw = raw[~undefined].copy()
    raw["cultivo"] = raw["cultivo"].str.strip()
    for col in ("superficie_cosechada_ha", "produccion_tm", "rendimiento_kgxha"):
        raw[col] = _to_num(raw[col])
    campaigns = raw["campania"].map(parse_campaign)
    raw["start_year"] = [c[0] for c in campaigns]
    raw["end_year"] = [c[1] for c in campaigns]

    frames = []
    present_by_key = {normalize_label(l): l for l in labels_present}
    for product in products:
        candidates = (label_overrides or {}).get(product) or CROP_LABELS[product]
        label = next((present_by_key[normalize_label(c)] for c in candidates
                      if normalize_label(c) in present_by_key), None)
        if label is None:
            raise SystemExit(f"no cultivo label for {product}: tried {candidates}; present {labels_present}. "
                             f"Pass --cultivo '<label>={product}'.")
        sub = raw[raw["cultivo"] == label].copy()
        sub = sub.merge(lookup, left_on="code", right_on="INDEC", how="left")
        unmatched = sub.loc[sub["admin_2"].isna(), ["code", "departamento", "provincia"]].drop_duplicates()
        if not unmatched.empty:
            print(f"WARNING {product}: {len(unmatched)} departamento_id(s) not in the boundary lookup "
                  f"(dropped): {unmatched[['code', 'departamento']].values.tolist()[:10]}")
            sub = sub.dropna(subset=["admin_2"])
        region_rules = rules[product]
        no_region = sub["calendar_region"].isna()
        wraps = sub["calendar_region"].map(lambda r: region_rules.get(r, "missing"))
        not_grown = wraps.isna()
        missing_rule = wraps.eq("missing")
        if missing_rule.any():
            raise SystemExit(f"{product}: calendar regions without a calendar row: "
                             f"{sorted(sub.loc[missing_rule, 'calendar_region'].unique())}")
        n_dropped = int((no_region | not_grown).sum())
        if n_dropped:
            print(f"NOTE {product}: {n_dropped} rows in departments with no calendar region or a -1 "
                  f"calendar dropped (geomerge drops those regions too): "
                  f"{sorted(sub.loc[no_region | not_grown, 'admin_2'].unique())[:8]} ...")
        sub = sub[~(no_region | not_grown)].copy()
        wraps = wraps[sub.index].astype(bool)
        sub["harvest_year"] = np.where(wraps, sub["end_year"], sub["start_year"]).astype(int)

        sub["yield"] = sub["rendimiento_kgxha"] / 1000.0
        fallback = sub["yield"].isna() & sub["superficie_cosechada_ha"].gt(0) & sub["produccion_tm"].notna()
        sub.loc[fallback, "yield"] = sub.loc[fallback, "produccion_tm"] / sub.loc[fallback, "superficie_cosechada_ha"]
        sub = sub.rename(columns={"superficie_cosechada_ha": "area", "produccion_tm": "production"})
        sub = sub.dropna(subset=["yield", "area", "production"], how="all")

        key = ["num_ID", "harvest_year"]
        dup = sub.duplicated(subset=key, keep=False)
        if dup.any():
            print(f"WARNING {product}: {int(dup.sum())} rows share a (department, harvest_year); "
                  f"summing area/production and recomputing yield")
            agg = (sub.groupby(key, as_index=False)
                      .agg(area=("area", "sum"), production=("production", "sum"),
                           admin_1=("ADM1_NAME", "first"), admin_2=("admin_2", "first"),
                           magyp_name=("departamento", "first")))
            agg["yield"] = agg["production"] / agg["area"].replace(0, np.nan)
        else:
            agg = pd.DataFrame({
                "num_ID": sub["num_ID"].values, "harvest_year": sub["harvest_year"].values,
                "area": sub["area"].values, "production": sub["production"].values,
                "admin_1": sub["ADM1_NAME"].values, "admin_2": sub["admin_2"].values,
                "magyp_name": sub["departamento"].values, "yield": sub["yield"].values,
            })
        lo, hi = PLAUSIBLE[product]
        implausible = agg["yield"].notna() & (agg["yield"] > 0) & ~agg["yield"].between(lo, hi)
        frames.append(pd.DataFrame({
            "country": country,
            "fnid": agg["num_ID"].astype(int),
            "admin_1": agg["admin_1"],
            "admin_2": agg["admin_2"],
            "magyp_name": agg["magyp_name"],
            "num_ID": agg["num_ID"].astype(int),
            "product": product,
            "season_name": "Main",
            "crop_production_system": "none",
            "qc_flag": implausible.astype(int),
            "harvest_year": agg["harvest_year"].astype(int),
            "yield": agg["yield"],
            "area": agg["area"],
            "production": agg["production"],
        }))
        n_wrap = int(wraps.sum())
        print(f"{product} <- {label!r}: {len(frames[-1])} department-years, "
              f"{agg['num_ID'].nunique()} departments, harvest years "
              f"{agg['harvest_year'].min()}-{agg['harvest_year'].max()}; "
              f"campaign end-year used for {n_wrap} rows, start-year for {len(wraps) - n_wrap}; "
              f"qc_flag = 1 on {int(implausible.sum())} rows outside {lo}-{hi} t/ha")

    wide = pd.concat(frames, ignore_index=True)
    return wide.sort_values(["product", "admin_2", "harvest_year"]).reset_index(drop=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--csv", required=True, help="MAGyP estimaciones-agricolas CSV")
    p.add_argument("--lookup", required=True, help="argentina_department_lookup.csv with calendar_region")
    p.add_argument("--calendar", required=True, help="AMISCM_*.xlsx crop-calendar workbook")
    p.add_argument("--out", required=True)
    p.add_argument("--product", action="append", default=None,
                   help="geocif product to include (default: Soybean, Maize, Winter Wheat)")
    p.add_argument("--cultivo", action="append", default=[],
                   help="override a MAGyP label: '<cultivo label>=<Product>'")
    a = p.parse_args(argv)

    overrides = {}
    for item in a.cultivo:
        label, _, product = item.rpartition("=")
        if not label or product not in CROP_LABELS:
            raise SystemExit(f"--cultivo expects '<label>=<Product>' with Product in {list(CROP_LABELS)}: {item!r}")
        overrides.setdefault(product, []).insert(0, label)
    products = tuple(a.product) if a.product else ("Soybean", "Maize", "Winter Wheat")

    wide = convert(a.csv, a.lookup, a.calendar, products=products, label_overrides=overrides)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    wide.to_csv(a.out, index=False, encoding="utf-8")
    ok = wide["yield"].notna()
    print(f"{len(wide)} rows | {wide['admin_2'].nunique()} departments | products {sorted(wide['product'].unique())} | "
          f"years {wide['harvest_year'].min()}-{wide['harvest_year'].max()} | yield non-null {int(ok.sum())} "
          f"({ok.mean() * 100:.1f}%), range {wide['yield'].min():.2f}-{wide['yield'].max():.2f} t/ha")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    sys.exit(main())
