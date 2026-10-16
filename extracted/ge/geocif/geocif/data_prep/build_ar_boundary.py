"""Build the Argentina department (admin_2) boundary shapefile from the IGN
``departamento`` layer (Instituto Geografico Nacional "Capas SIG" download:
``departamentoPolygon.shp``, 529 polygons, EPSG:4326, DBF in ISO-8859-1).

Output contract (what geoprepare's extract_EO.load_country_boundary and
geocif's yield_outlook map merge require; the same as build_mt_boundary):

- ``ADM0_NAME``  ``Argentina``
- ``ADM1_NAME``  province in the GEOGLAM ``Level_1.shp`` spelling
  (``Cordoba``, ``Santiago Del Estero``, ``Tierra Del Fuego``, ...), derived
  from the INDEC province code (first two digits of ``in1``) because the IGN
  layer carries no province column. Parent (province) aggregation in geocif
  matches these spellings against Level_1.shp.
- ``ADM2_NAME``  composite, lowercase, ASCII, **space-separated**:
  ``buenos aires adolfo alsina``. 47 department names recur across provinces
  (``Capital`` x11, ``San Martin`` x5, ...); the province prefix makes the
  name unique country-wide, so geoprepare never adds its own prefix and the
  yield_outlook map join (which lower-cases but does NOT underscore-fold the
  shapefile side) matches the ``Region`` string. Accents are stripped because
  nothing downstream folds them; digits, apostrophes and periods are kept
  (``chaco o'higgins``, ``jujuy dr. manuel belgrano``); commas and slashes
  are refused (they break geoprepare's CSV rows and file names).
- ``num_ID``     INDEC department code as int (``06007`` -> 6007; unique,
  stable; MAGyP's ``departamento_id`` is the same code). Becomes
  ``ADM_ID`` -> ``region_id`` in every extracted CSV. An int on purpose: a
  zero-padded string id is read back as an int from the extraction CSVs and
  then misses the calendar-region lookup on a fresh run.
- ``INDEC`` (5-char string), ``DEPTO`` (IGN spelling, with accents) and
  ``GNA`` (Departamento / Partido / Comuna) are carried for reference.
- CRS EPSG:4326, ``.cpg`` = UTF-8.

Dropped by default (``--keep <in1>`` overrides per unit):
- ``Antartida Argentina`` (in1 94028): the Antarctic sector, reaches 90S and
  holds 59% of the layer's vertices;
- ``Islas del Atlantico Sur`` (94021): Malvinas/Falklands, South Georgia,
  South Sandwich and South Orkney islands, east to 26W;
- the 15 CABA comunas (province code 02): fully urban, no crop pixels;
  GEOGLAM carries CABA as a single unit without yields.

Also writes ``argentina_department_lookup.csv`` (INDEC, num_ID, ADM1_NAME,
DEPTO, ADM2_NAME, admin_2) -- the canonical name table convert_magyp joins
on, so the statistics file and the shapefile can never disagree on a name --
and ``argentina_departamentos_dropped.csv`` listing every unit left out.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

COUNTRY = "Argentina"
OUT_STEM = "argentina_departamentos"

# INDEC province code -> ADM1_NAME, spelled as in GEOGLAM Level_1.shp
# (verified against the Argentina rows of Level_1.shp / Level_2.shp on
# 2026-10-14). 02 is the Ciudad Autonoma de Buenos Aires.
PROVINCES = {
    "02": "Buenos Aires D.f.",
    "06": "Buenos Aires",
    "10": "Catamarca",
    "14": "Cordoba",
    "18": "Corrientes",
    "22": "Chaco",
    "26": "Chubut",
    "30": "Entre Rios",
    "34": "Formosa",
    "38": "Jujuy",
    "42": "La Pampa",
    "46": "La Rioja",
    "50": "Mendoza",
    "54": "Misiones",
    "58": "Neuquen",
    "62": "Rio Negro",
    "66": "Salta",
    "70": "San Juan",
    "74": "San Luis",
    "78": "Santa Cruz",
    "82": "Santa Fe",
    "86": "Santiago Del Estero",
    "90": "Tucuman",
    "94": "Tierra Del Fuego",
}

POLAR = {
    "94028": "Antarctic sector (Antartida Argentina): reaches 90S, 59% of the layer's vertices",
    "94021": "South Atlantic islands (Islas del Atlantico Sur): Malvinas, South Georgia, "
             "South Sandwich, South Orkney",
}
CABA_PROVINCE = "02"
FORBIDDEN = set(",/\\")


def fold_name(text: str) -> str:
    """Accent-strip and tidy a department name.

    NFD -> drop combining marks (``Ñorquín`` -> ``Norquin``), drop the ordinal
    signs in ``1º de Mayo``, collapse whitespace. Keeps digits, apostrophes
    and periods. The geocif/geoprepare name matching does no accent folding,
    so every name we write must already be pure ASCII.
    """
    decomposed = unicodedata.normalize("NFD", str(text))
    folded = "".join(c for c in decomposed if not unicodedata.combining(c))
    folded = folded.replace("º", "").replace("°", "")
    return re.sub(r"\s+", " ", folded).strip()


def composite_name(adm1: str, depto: str) -> str:
    """``('Buenos Aires', 'Adolfo Alsina')`` -> ``'buenos aires adolfo alsina'``."""
    return f"{adm1} {fold_name(depto)}".lower().strip()


def build(shp_path, out_dir, country=COUNTRY, keep=(), overwrite=False, out_stem=OUT_STEM):
    import geopandas as gpd
    import pandas as pd

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_shp = out_dir / f"{out_stem}.shp"
    if out_shp.exists() and not overwrite:
        raise SystemExit(f"{out_shp} exists; pass --overwrite to replace it")

    # The IGN DBF ships a .cst (GeoServer) sidecar, not a .cpg, so GDAL has
    # to be told the code page explicitly.
    gdf = gpd.read_file(shp_path, engine="pyogrio", encoding="ISO-8859-1")
    n_total = len(gdf)
    for col in ("nam", "in1", "gna"):
        if col not in gdf.columns:
            raise SystemExit(f"column {col!r} missing; got {list(gdf.columns)} -- is this the IGN departamento layer?")
    gdf["in1"] = gdf["in1"].astype(str).str.strip()
    bad_codes = gdf.loc[~gdf["in1"].str.fullmatch(r"\d{5}"), "in1"].tolist()
    if bad_codes:
        raise SystemExit(f"in1 must be 5-digit INDEC codes; found {bad_codes[:8]}")
    if gdf["in1"].duplicated().any():
        raise SystemExit("duplicate in1 codes in the source layer")
    # Decoding check: Neuquen's Ñorquín (58084) must fold to 'norquin'.
    probe = gdf.loc[gdf["in1"] == "58084", "nam"]
    if len(probe) and fold_name(probe.iloc[0]).lower() != "norquin":
        raise SystemExit(f"DBF decoding looks wrong: 58084 reads as {probe.iloc[0]!r}")

    try:
        import shapely
        n_vertices = lambda g: int(shapely.get_num_coordinates(g).sum())  # noqa: E731
    except Exception:  # shapely < 2
        n_vertices = lambda g: -1  # noqa: E731
    vertices_before = n_vertices(gdf.geometry)

    keep = set(keep)
    reasons = {code: why for code, why in POLAR.items() if code not in keep}
    for code in gdf.loc[gdf["in1"].str[:2] == CABA_PROVINCE, "in1"]:
        if code not in keep and code not in reasons:
            reasons[code] = "CABA comuna: urban, no cropland"
    dropped = gdf[gdf["in1"].isin(reasons)].copy()
    kept = gdf[~gdf["in1"].isin(reasons)].copy()

    unknown = sorted(set(kept["in1"].str[:2]) - set(PROVINCES))
    if unknown:
        raise SystemExit(f"province codes missing from PROVINCES: {unknown}")

    kept["ADM0_NAME"] = country
    kept["ADM1_NAME"] = kept["in1"].str[:2].map(PROVINCES)
    kept["ADM2_NAME"] = [composite_name(a, d) for a, d in zip(kept["ADM1_NAME"], kept["nam"])]
    kept["num_ID"] = kept["in1"].astype(int)
    kept["INDEC"] = kept["in1"]
    kept["DEPTO"] = kept["nam"]
    kept["GNA"] = kept["gna"]

    if kept["ADM2_NAME"].duplicated().any():
        dupes = kept.loc[kept["ADM2_NAME"].duplicated(keep=False), "ADM2_NAME"].tolist()
        raise SystemExit(f"Composite ADM2_NAME collision(s): {sorted(set(dupes))}")
    if kept["num_ID"].duplicated().any():
        raise SystemExit("Duplicate num_ID values -- INDEC codes must be unique.")
    non_ascii = [n for n in kept["ADM2_NAME"] if not n.isascii()]
    if non_ascii:
        raise SystemExit(f"Non-ASCII names survived folding: {non_ascii[:5]}")
    forbidden = [n for n in kept["ADM2_NAME"] if FORBIDDEN & set(n)]
    if forbidden:
        raise SystemExit(f"Names with a comma or slash (break geoprepare CSVs/paths): {forbidden[:5]}")

    if kept.crs is None:
        raise SystemExit("source layer has no CRS (.prj missing)")
    kept = kept.to_crs(epsg=4326)
    invalid = ~kept.geometry.is_valid
    n_invalid = int(invalid.sum())
    if n_invalid:
        from shapely import make_valid

        kept.loc[invalid, "geometry"] = kept.loc[invalid, "geometry"].apply(make_valid)
        print(f"WARNING: repaired {n_invalid} invalid geometries with make_valid: "
              f"{kept.loc[invalid, 'ADM2_NAME'].tolist()[:8]}")
    kept = kept.sort_values("num_ID").reset_index(drop=True)

    cols = ["ADM0_NAME", "ADM1_NAME", "ADM2_NAME", "num_ID", "INDEC", "DEPTO", "GNA", "geometry"]
    try:
        kept[cols].to_file(out_shp, driver="ESRI Shapefile", engine="pyogrio", encoding="utf-8")
    except TypeError:  # older geopandas/pyogrio without the encoding kwarg
        kept[cols].to_file(out_shp, driver="ESRI Shapefile", engine="pyogrio")
    cpg = out_shp.with_suffix(".cpg")
    if not cpg.exists():
        cpg.write_text("UTF-8")

    lookup = kept[["INDEC", "num_ID", "ADM1_NAME", "DEPTO", "ADM2_NAME"]].copy()
    lookup["admin_2"] = lookup["ADM2_NAME"].str.replace(" ", "_", regex=False)
    lookup_csv = out_dir / "argentina_department_lookup.csv"
    lookup.to_csv(lookup_csv, index=False, encoding="utf-8")

    dropped_csv = out_dir / f"{out_stem}_dropped.csv"
    pd.DataFrame({
        "INDEC": dropped["in1"].values,
        "ADM1_NAME": dropped["in1"].str[:2].map(PROVINCES).values,
        "DEPTO": dropped["nam"].values,
        "GNA": dropped["gna"].values,
        "reason": [reasons[c] for c in dropped["in1"]],
    }).sort_values("INDEC").to_csv(dropped_csv, index=False, encoding="utf-8")

    vertices_after = n_vertices(kept.geometry)
    print(f"{len(kept)} departments kept of {n_total} ({len(dropped)} dropped); "
          f"vertices {vertices_before:,} -> {vertices_after:,}; "
          f"bounds {tuple(round(float(v), 3) for v in kept.total_bounds)}")
    print(kept.groupby("ADM1_NAME")["num_ID"].count().to_string())
    print(f"shapefile : {out_shp}")
    print(f"lookup    : {lookup_csv}")
    print(f"dropped   : {dropped_csv}")
    return out_shp, lookup_csv, dropped_csv


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--shp", required=True, help="IGN departamentoPolygon.shp")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--country-display", default=COUNTRY)
    p.add_argument("--keep", action="append", default=[],
                   help="in1 code of a unit to keep although it is dropped by default "
                        "(94028 Antartida, 94021 Islas del Atlantico Sur, 02xxx CABA comunas)")
    p.add_argument("--overwrite", action="store_true")
    a = p.parse_args(argv)
    build(a.shp, a.out_dir, country=a.country_display, keep=a.keep, overwrite=a.overwrite)


if __name__ == "__main__":
    sys.exit(main())
