"""Build an admin_2 boundary shapefile for one Brazilian state from the IBGE
municipality mesh (BR_Municipios_*.shp).

Output contract (what geoprepare's extract_EO.load_country_boundary and
geocif's yield_outlook map merge require):

- ``ADM0_NAME``  country display name, e.g. ``Brazil``
- ``ADM1_NAME``  state display name, e.g. ``Mato Grosso``
- ``ADM2_NAME``  composite, lowercase, ASCII, **space-separated**:
  ``mato grosso agua boa``. Spaces (not underscores) because the
  yield_outlook geometry merge lower-cases but does NOT underscore-fold
  the shapefile side. The composite prefix makes names unique country-wide
  and lets the CID-stage prefix filter match on the parent state.
- ``num_ID``     7-digit IBGE municipality code as int (unique, stable);
  becomes ``ADM_ID`` -> ``region_id`` in every extracted CSV.
- CRS EPSG:4326.

Also writes ``mt_municipality_lookup.csv`` — the canonical name table
(CD_MUN, NM_MUN, ADM2_NAME, admin_2) that convert_tabela1612 joins on, so
the yield file and the shapefile can never disagree on a name.
"""

import argparse
import sys
import unicodedata
from pathlib import Path


def ascii_fold(text: str) -> str:
    """Strip accents/diacritics (NFD -> drop combining marks). ``ç`` -> ``c``.

    The geocif/geoprepare name matching does no accent folding anywhere, so
    every artifact we produce must already be pure ASCII.
    """
    decomposed = unicodedata.normalize("NFD", str(text))
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def composite_name(state_display: str, municipality: str) -> str:
    """``('Mato Grosso', 'Água Boa')`` -> ``'mato grosso agua boa'``."""
    return f"{state_display} {ascii_fold(municipality)}".lower().strip()


def build(shp_path, state_abbrev, state_display, country_display, out_dir):
    import geopandas as gpd

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    gdf = gpd.read_file(shp_path, engine="pyogrio")
    n_total = len(gdf)
    gdf = gdf[gdf["SIGLA_UF"] == state_abbrev].copy()
    if gdf.empty:
        raise SystemExit(f"No municipalities with SIGLA_UF == {state_abbrev!r} "
                         f"among {n_total} records in {shp_path}")

    gdf["ADM0_NAME"] = country_display
    gdf["ADM1_NAME"] = state_display
    gdf["ADM2_NAME"] = gdf["NM_MUN"].map(lambda n: composite_name(state_display, n))
    gdf["num_ID"] = gdf["CD_MUN"].astype(int)

    if gdf["ADM2_NAME"].duplicated().any():
        dupes = gdf.loc[gdf["ADM2_NAME"].duplicated(keep=False), "ADM2_NAME"].tolist()
        raise SystemExit(f"Composite ADM2_NAME collision(s): {sorted(set(dupes))}")
    if gdf["num_ID"].duplicated().any():
        raise SystemExit("Duplicate num_ID values — IBGE codes must be unique.")
    non_ascii = [n for n in gdf["ADM2_NAME"] if not n.isascii()]
    if non_ascii:
        raise SystemExit(f"Non-ASCII names survived folding: {non_ascii[:5]}")

    gdf = gdf.to_crs(epsg=4326)

    cols = ["ADM0_NAME", "ADM1_NAME", "ADM2_NAME", "num_ID", "CD_MUN", "NM_MUN", "geometry"]
    out_shp = out_dir / f"brazil_{state_abbrev.lower()}_municipalities.shp"
    gdf[cols].to_file(out_shp, engine="pyogrio")

    lookup = gdf[["CD_MUN", "NM_MUN", "ADM2_NAME"]].copy()
    lookup["admin_2"] = lookup["ADM2_NAME"].str.replace(" ", "_", regex=False)
    out_csv = out_dir / f"{state_abbrev.lower()}_municipality_lookup.csv"
    lookup.sort_values("CD_MUN").to_csv(out_csv, index=False)

    print(f"{len(gdf)} municipalities ({state_abbrev}) of {n_total} national")
    print(f"shapefile : {out_shp}")
    print(f"lookup    : {out_csv}")
    return out_shp, out_csv


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--shp", default=r"C:\Users\ritvik\Downloads\BR_Municipios_2020\BR_Municipios_2020.shp")
    p.add_argument("--state-abbrev", default="MT")
    p.add_argument("--state-display", default="Mato Grosso")
    p.add_argument("--country-display", default="Brazil")
    p.add_argument("--out-dir", default=r"D:\Users\ritvik\projects\GEO\config\brazil_mt\assets")
    a = p.parse_args(argv)
    build(a.shp, a.state_abbrev, a.state_display, a.country_display, a.out_dir)


if __name__ == "__main__":
    sys.exit(main())
