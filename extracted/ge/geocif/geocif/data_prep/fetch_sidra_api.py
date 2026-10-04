"""Fetch IBGE SIDRA Tabela 1612 municipality crop statistics over the API and
write the hvstat-style wide CSV that geocif's ``production_statistics_file``
consumes -- the same schema ``convert_tabela1612`` produces from a manual
web export, but without the manual export step.

Why an API fetcher as well as the CSV converter: the SIDRA web export is
per-crop and has to be downloaded by hand, so adding a crop means a new
download. The API takes the crop as a parameter, so maize, rice and wheat
come from the same code path.

Table 1612 coordinates (confirmed from /agregados/1612/metadados):
- n6                 municipality level; ``D1C`` is the 7-digit IBGE code,
                     which is exactly the ``num_ID`` in the boundary shapefile
- v/216, 214, 112    area colhida (ha), quantidade produzida (t),
                     rendimento medio (kg/ha)
- c81 categories     2711 = Milho (em grao), 2713 = Soja (em grao)

The cluster has no external DNS, so this runs on a workstation and the output
is copied to ``inputs/metadata/production_statistics/``.
"""

import argparse
import csv
import gzip
import json
import sys
import time
import urllib.request
from pathlib import Path

API = "https://apisidra.ibge.gov.br/values/t/1612/n6/all/v/216,214,112/p/{year}/c81/{product}"

# SIDRA variable id -> our column
VAR = {"216": "area", "214": "production", "112": "yield_kg_ha"}

# Missing-data markers SIDRA returns in the value field
MISSING = {"-", "..", "...", "X", "", None}


def fetch_year(year, product, retries=3, timeout=240):
    """Return the raw record list for one harvest year, or [] if unavailable."""
    url = API.format(year=year, product=product)
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}
            )
            raw = urllib.request.urlopen(req, timeout=timeout).read()
            if raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            data = json.loads(raw.decode("utf-8"))
            return data[1:]  # row 0 is the header-description row
        except Exception as e:  # noqa: BLE001 - network flakiness is expected
            if attempt == retries:
                print(f"  {year}: FAILED after {retries} attempts ({type(e).__name__}: {e})")
                return []
            time.sleep(3 * attempt)
    return []


def to_float(v):
    if v in MISSING:
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def build(years, product, lookup_csv, out_path, country, product_label, season_name):
    # admin_2 names come from the boundary lookup so the yield file and the
    # shapefile can never disagree -- the stats join matches on NAME, not id.
    look = {}
    with open(lookup_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            look[str(int(r["CD_MUN"]))] = (r["ADM2_NAME"], r.get("ADM1_NAME", ""), r["NM_MUN"])
    print(f"lookup municipalities: {len(look)}")

    # (code, year) -> {area, production, yield_kg_ha}
    rec = {}
    for y in years:
        rows = fetch_year(y, product)
        n = 0
        for r in rows:
            col = VAR.get(r.get("D2C"))
            if col is None:
                continue
            code = str(r.get("D1C"))
            val = to_float(r.get("V"))
            if val is None:
                continue
            rec.setdefault((code, y), {})[col] = val
            n += 1
        print(f"  {y}: {n} values")

    unmatched = set()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cols = ["country", "fnid", "admin_1", "admin_2", "ibge_name", "num_ID", "product",
            "season_name", "crop_production_system", "qc_flag", "harvest_year",
            "yield", "area", "production"]
    written = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for (code, year), v in sorted(rec.items()):
            hit = look.get(code)
            if not hit:
                unmatched.add(code)
                continue
            adm2, adm1, nm = hit
            # Rendimento medio is kg/ha; fall back to production/area when absent.
            y_t_ha = v.get("yield_kg_ha")
            y_t_ha = y_t_ha / 1000.0 if y_t_ha is not None else None
            if y_t_ha is None and v.get("area") and v.get("production") is not None:
                y_t_ha = v["production"] / v["area"] if v["area"] > 0 else None
            if y_t_ha is None and v.get("area") is None and v.get("production") is None:
                continue
            w.writerow({
                "country": country, "fnid": code, "admin_1": adm1, "admin_2": adm2,
                "ibge_name": nm, "num_ID": int(code), "product": product_label,
                "season_name": season_name, "crop_production_system": "none",
                "qc_flag": 0, "harvest_year": year,
                "yield": y_t_ha, "area": v.get("area"), "production": v.get("production"),
            })
            written += 1
    print(f"\nrows written: {written}")
    print(f"unmatched IBGE codes (not in boundary lookup): {len(unmatched)}")
    print(f"wrote {out_path}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--product", default="2711", help="SIDRA c81 code (2711=Milho, 2713=Soja)")
    p.add_argument("--product-label", default="Maize", help="geocif crop display name")
    p.add_argument("--start-year", type=int, default=1990)
    p.add_argument("--end-year", type=int, default=2024)
    p.add_argument("--season-name", default="Main")
    p.add_argument("--country", default="Brazil")
    p.add_argument("--lookup",
                   default=r"D:\Users\ritvik\projects\GEO\config\production\brazil_admin2\assets\brazil_municipality_lookup.csv")
    p.add_argument("--out",
                   default=r"D:\Users\ritvik\projects\GEO\config\production\brazil_admin2\assets\adm_crop_production_BR_municipality_maize_wide.csv")
    a = p.parse_args(argv)
    build(range(a.start_year, a.end_year + 1), a.product, a.lookup, Path(a.out),
          a.country, a.product_label, a.season_name)


if __name__ == "__main__":
    sys.exit(main())
