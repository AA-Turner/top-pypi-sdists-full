"""Build an admin_2 boundary shapefile for one Brazilian state — or the whole
country (``--state-abbrev ALL``) — from the IBGE municipality mesh
(BR_Municipios_*.shp).

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
(CD_MUN, NM_MUN, ADM1_NAME, ADM2_NAME, admin_2) that convert_tabela1612
joins on, so the yield file and the shapefile can never disagree on a name.

All-Brazil mode (``--state-abbrev ALL``):
- ``ADM1_NAME`` comes per-row from the 27-entry ``UF_DISPLAY`` map (ASCII
  spellings matching the GEOGLAM admin_1 workbooks: ``Sao Paulo``,
  ``Mato Grosso Do Sul``, ...);
- the lookup CSV always covers EVERY municipality in scope (reusable for
  other crops), while ``--keep-codes`` optionally restricts the SHAPEFILE to
  a subset of IBGE codes (e.g. only municipalities with PAM soybean data,
  since geoextract processes every polygon in the boundary file);
- outputs are ``brazil_municipalities.shp`` + ``brazil_municipality_lookup.csv``.
"""

import argparse
import sys
import unicodedata
from pathlib import Path

# SIGLA_UF -> ASCII display name, spelled as in the GEOGLAM admin_1 workbooks
# (verified against the brazil_soybean DB region list: "Mato Grosso Do Sul",
# "Sao Paulo", "Goias", "Para", ...). ADM1_NAME must be ASCII for the same
# reason as ADM2_NAME: nothing downstream folds accents.
UF_DISPLAY = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapa", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceara", "DF": "Distrito Federal",
    "ES": "Espirito Santo", "GO": "Goias", "MA": "Maranhao",
    "MT": "Mato Grosso", "MS": "Mato Grosso Do Sul", "MG": "Minas Gerais",
    "PA": "Para", "PB": "Paraiba", "PR": "Parana", "PE": "Pernambuco",
    "PI": "Piaui", "RJ": "Rio De Janeiro", "RN": "Rio Grande Do Norte",
    "RS": "Rio Grande Do Sul", "RO": "Rondonia", "RR": "Roraima",
    "SC": "Santa Catarina", "SP": "Sao Paulo", "SE": "Sergipe",
    "TO": "Tocantins",
}


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


def _read_keep_codes(path):
    """A CSV (column ``num_ID`` or ``CD_MUN``, else the first column) or a
    plain one-code-per-line file -> set of int IBGE codes."""
    import pandas as pd

    df = pd.read_csv(path)
    for col in ("num_ID", "CD_MUN"):
        if col in df.columns:
            return set(df[col].astype(int))
    return set(df.iloc[:, 0].astype(int))


def build(shp_path, state_abbrev, state_display, country_display, out_dir,
          keep_codes_csv=None):
    import geopandas as gpd

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    gdf = gpd.read_file(shp_path, engine="pyogrio")
    n_total = len(gdf)
    if state_abbrev.upper() == "ALL":
        unknown_uf = sorted(set(gdf["SIGLA_UF"]) - set(UF_DISPLAY))
        if unknown_uf:
            raise SystemExit(f"SIGLA_UF values missing from UF_DISPLAY: {unknown_uf}")
        gdf = gdf.copy()
        gdf["ADM1_NAME"] = gdf["SIGLA_UF"].map(UF_DISPLAY)
        out_stem, lookup_stem = "brazil_municipalities", "brazil_municipality_lookup"
    else:
        gdf = gdf[gdf["SIGLA_UF"] == state_abbrev].copy()
        if gdf.empty:
            raise SystemExit(f"No municipalities with SIGLA_UF == {state_abbrev!r} "
                             f"among {n_total} records in {shp_path}")
        gdf["ADM1_NAME"] = state_display
        out_stem = f"brazil_{state_abbrev.lower()}_municipalities"
        lookup_stem = f"{state_abbrev.lower()}_municipality_lookup"

    gdf["ADM0_NAME"] = country_display
    gdf["ADM2_NAME"] = [
        composite_name(adm1, n) for adm1, n in zip(gdf["ADM1_NAME"], gdf["NM_MUN"])
    ]
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

    # Lookup covers the FULL scope (before any keep-codes cut) so the yield
    # converter can name every municipality that has statistics.
    lookup = gdf[["CD_MUN", "NM_MUN", "ADM1_NAME", "ADM2_NAME"]].copy()
    lookup["admin_2"] = lookup["ADM2_NAME"].str.replace(" ", "_", regex=False)
    out_csv = out_dir / f"{lookup_stem}.csv"
    lookup.sort_values("CD_MUN").to_csv(out_csv, index=False)

    kept = gdf
    if keep_codes_csv:
        keep = _read_keep_codes(keep_codes_csv)
        kept = gdf[gdf["num_ID"].isin(keep)]
        absent = keep - set(kept["num_ID"])
        if absent:
            print(f"WARNING: {len(absent)} keep-codes not in the mesh "
                  f"(ignored): {sorted(absent)[:8]}")

    cols = ["ADM0_NAME", "ADM1_NAME", "ADM2_NAME", "num_ID", "CD_MUN", "NM_MUN", "geometry"]
    out_shp = out_dir / f"{out_stem}.shp"
    kept[cols].to_file(out_shp, engine="pyogrio")

    print(f"{len(kept)} municipalities in shapefile "
          f"({state_abbrev}; {len(gdf)} in lookup, {n_total} national)")
    if state_abbrev.upper() == "ALL":
        print(kept.groupby("ADM1_NAME")["num_ID"].count().to_string())
    print(f"shapefile : {out_shp}")
    print(f"lookup    : {out_csv}")
    return out_shp, out_csv


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--shp", default=r"C:\Users\ritvik\Downloads\BR_Municipios_2020\BR_Municipios_2020.shp")
    p.add_argument("--state-abbrev", default="MT",
                   help="two-letter UF, or ALL for every state (all-Brazil mode)")
    p.add_argument("--state-display", default="Mato Grosso",
                   help="ignored in ALL mode (UF_DISPLAY map is used per row)")
    p.add_argument("--country-display", default="Brazil")
    p.add_argument("--out-dir", default=r"D:\Users\ritvik\projects\GEO\config\brazil_mt\assets")
    p.add_argument("--keep-codes", default=None,
                   help="CSV of IBGE codes (num_ID/CD_MUN column) restricting the "
                        "SHAPEFILE (not the lookup) to those municipalities")
    a = p.parse_args(argv)
    build(a.shp, a.state_abbrev, a.state_display, a.country_display, a.out_dir,
          keep_codes_csv=a.keep_codes)


if __name__ == "__main__":
    sys.exit(main())
