"""Prepare the GEOGLAM Crop Monitor calendar-region shapefile for geoextract.

``Global_Regions_202609.shp`` as shipped cannot be used as a geoprepare
``boundary_file``: it has no numeric ID column, and
``geoprepare.extract.extract_EO.load_country_boundary`` requires ``ADM_ID``
unconditionally. A country whose boundary lacks it is **silently dropped** --
``build_combinations`` does ``if df_country is None: continue`` -- so the run
reports success and writes nothing. This script adds the ID and everything else
the validator needs, and writes an audit report so a future calendar drop is
diffable.

What it does

1.  Assigns ``num_ID = 1..N`` over ``Key`` sorted lexicographically, matching
    the ``[GlobalCM_Regions_2025-11] id_col = num_ID`` convention already in
    geobase.txt. The ID is deliberately numeric: geoextract puts ``region_id``
    verbatim into the output filename ``{region_id}_{region}_{year}_{var}_{crop}.csv``
    and ``Key`` contains spaces, ``&``, ``'`` and ``()``.
2.  Dissolves the duplicate ``Lebanon Lebanon`` geometry (two features, one key).
3.  Carries the ``Region`` sub-continental grouping forward from the previous
    ``GlobalCM_Regions_2025-11.shp`` (joined on its ``Key2``), which the new file
    dropped. Regions with no match are listed for manual assignment.
4.  Checks the join against the calendar workbook and reports every key that
    fails, after alias resolution.
5.  Proposes ``region``/``hemisphere`` rows for countries missing from
    ``metadata/countries.csv``, into a **separate** file. It never edits the live
    one: measured against the 127 countries already in it, a centroid rule
    disagrees on 9 hemispheres and 10 climate zones, because those labels encode
    agro-climatic judgement rather than geometry.

Usage::

    python -m geocif.data_prep.prepare_calendar_regions \
        --shp "C:/.../Global_Regions_202609.shp" \
        --calendar "C:/.../GlobalCM_2026-09-11.xlsx"

Outputs land under ``--out-root`` (the local mirror of the HPC metadata tree by
default); push them to the cluster with the printed ``scp`` lines.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from geocif.cropcal import calendar as cropcal_calendar
from geocif.cropcal import naming

DEFAULT_OUT_ROOT = Path(r"D:/Users/ritvik/projects/GEO/inputs/metadata")
DEFAULT_OLD_SHP = DEFAULT_OUT_ROOT / "boundary_files" / "GlobalCM_Regions_2025-11.shp"
DEFAULT_COUNTRIES_CSV = DEFAULT_OUT_ROOT / "countries.csv"

HPC_METADATA = "/gpfs/data1/cmongp1/GEO/inputs/metadata"

#: Latitude below which a country centroid is called Tropical, for the
#: *proposed* rows only. The Tropic of Cancer/Capricorn.
TROPICS_LAT = 23.44

#: Shapefile sidecar extensions to copy/report alongside the .shp.
SHP_PARTS = (".shp", ".shx", ".dbf", ".prj", ".cpg")


# --------------------------------------------------------------------------
# Shapefile
# --------------------------------------------------------------------------
def load_regions(path: Path) -> gpd.GeoDataFrame:
    """Read the shipped region shapefile and normalise its text columns."""
    gdf = gpd.read_file(path, engine="pyogrio")
    required = {"ADM0_NAME", "Name", "Key", "CM_Group"}
    missing = required - set(gdf.columns)
    if missing:
        raise SystemExit(f"{path.name} is missing columns: {sorted(missing)}")

    for col in ("ADM0_NAME", "Name", "Key", "CM_Group"):
        gdf[col] = gdf[col].map(naming.clean_text)

    rebuilt = [naming.build_key(n, c) for n, c in zip(gdf["Name"], gdf["ADM0_NAME"])]
    drift = gdf.loc[gdf["Key"] != pd.Series(rebuilt, index=gdf.index), "Key"]
    if len(drift):
        print(f"  NOTE: {len(drift)} Key value(s) are not '<Name> <ADM0_NAME>'; rebuilding")
    gdf["Key"] = rebuilt
    return gdf


def dissolve_duplicate_keys(gdf: gpd.GeoDataFrame) -> tuple[gpd.GeoDataFrame, list[str]]:
    """Merge features that share a ``Key`` into one geometry."""
    dupes = sorted(gdf.loc[gdf["Key"].duplicated(keep=False), "Key"].unique())
    if not dupes:
        return gdf, []
    attrs = {"ADM0_NAME": "first", "Name": "first", "CM_Group": "first"}
    merged = gdf.dissolve(by="Key", aggfunc=attrs, as_index=False)
    return merged, dupes


def attach_region_grouping(
    gdf: gpd.GeoDataFrame, old_shp: Path | None
) -> tuple[gpd.GeoDataFrame, list[str]]:
    """Carry ``Region`` forward from the previous region file, joined on ``Key2``.

    The new file dropped the sub-continental grouping that the original's
    region x crop summaries were built on.
    """
    gdf = gdf.copy()
    gdf["Region"] = pd.NA
    if old_shp is None or not old_shp.is_file():
        print(f"  NOTE: {old_shp} not found; Region left empty for every polygon")
        return gdf, sorted(gdf["Key"])

    old = gpd.read_file(old_shp, engine="pyogrio")
    key_col = "Key2" if "Key2" in old.columns else "Key"
    lookup = {
        naming.clean_text(k): naming.clean_text(r)
        for k, r in zip(old[key_col], old.get("Region", pd.Series(dtype=object)))
        if isinstance(r, str) and r.strip()
    }
    gdf["Region"] = gdf["Key"].map(lookup)
    unassigned = sorted(gdf.loc[gdf["Region"].isna(), "Key"])
    return gdf, unassigned


def add_numeric_id(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Assign ``num_ID = 1..N`` over ``Key`` sorted lexicographically.

    Deterministic, so re-running this script on the same input reproduces the
    same IDs and the extraction cache stays valid.
    """
    gdf = gdf.sort_values("Key", kind="stable").reset_index(drop=True)
    gdf.insert(0, "num_ID", np.arange(1, len(gdf) + 1, dtype="int64"))
    return gdf


# --------------------------------------------------------------------------
# Calendar join
# --------------------------------------------------------------------------
def calendar_keys(calendar_path: Path) -> tuple[set[str], pd.DataFrame]:
    """Every alias-resolved key in the workbook, plus per-sheet active counts."""
    sheets = cropcal_calendar.read_workbook(calendar_path)
    keys: set[str] = set()
    rows = []
    for crop_season, frame in sheets.items():
        codes = frame[cropcal_calendar.code_columns(frame)].to_numpy(dtype=float)
        active = ~np.all(codes == cropcal_calendar.CODE_NOT_GROWN, axis=1)
        keys.update(frame["key"])
        rows.append(
            {
                "crop": crop_season.crop,
                "season": crop_season.season,
                "rows": len(frame),
                "active_rows": int(active.sum()),
                "countries": frame.loc[active, "country"].nunique(),
                "skip_reason": naming.skip_reason_for_crop(crop_season.crop) or "",
            }
        )
    return keys, pd.DataFrame(rows).sort_values(["crop", "season"])


# --------------------------------------------------------------------------
# countries.csv
# --------------------------------------------------------------------------
def propose_country_metadata(
    gdf: gpd.GeoDataFrame, countries_csv: Path | None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """``(proposed_rows, disagreements)`` for the country zone file.

    ``proposed_rows`` covers only countries absent from the live file.
    ``disagreements`` shows where the centroid rule contradicts the rows that
    are already there -- evidence that the file must not be regenerated.

    Both sides are matched on :func:`geocif.cropcal.naming.normalize`, not on a
    bare lower-and-strip: the live file spells Iran with a double space
    (``"iran  (islamic republic of)"``), which a naive match reports as a
    missing country and then proposes a duplicate row for.
    """
    countries = gdf.dissolve("ADM0_NAME")
    # Centroids of a geographic CRS are not meaningful (and geopandas warns).
    # Equal Earth is equal-area and global, so a country centroid computed in it
    # sits inside the country; reproject the point back to get its latitude.
    lat = countries.geometry.to_crs("+proj=eqearth").centroid.to_crs(epsg=4326).y

    proposal = pd.DataFrame(
        {
            "country": [naming.clean_text(c).lower() for c in lat.index],
            "region": np.where(lat.abs() < TROPICS_LAT, "Tropical", "Temperate"),
            "hemisphere": np.where(lat >= 0, "N", "S"),
            "centroid_lat": lat.round(3).to_numpy(),
        }
    )
    proposal["_join"] = proposal["country"].map(naming.normalize)

    if countries_csv is None or not countries_csv.is_file():
        return proposal.drop(columns="_join"), pd.DataFrame()

    live = pd.read_csv(countries_csv)
    live["_join"] = live["country"].map(naming.normalize)
    known = set(live["_join"])

    merged = proposal.merge(
        live.drop(columns="country"), on="_join", how="inner", suffixes=("_pred", "_live")
    )
    disagree = merged.loc[
        (merged["region_pred"] != merged["region_live"])
        | (merged["hemisphere_pred"] != merged["hemisphere_live"])
    ].drop(columns="_join")
    missing = proposal.loc[~proposal["_join"].isin(known)].drop(columns="_join")
    return missing.copy(), disagree


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--shp", required=True, type=Path, help="Global_Regions_202609.shp")
    ap.add_argument("--calendar", required=True, type=Path, help="GlobalCM_*.xlsx")
    ap.add_argument("--old-shp", type=Path, default=DEFAULT_OLD_SHP)
    ap.add_argument("--countries-csv", type=Path, default=DEFAULT_COUNTRIES_CSV)
    ap.add_argument("--out-root", type=Path, default=DEFAULT_OUT_ROOT)
    args = ap.parse_args(argv)

    out_boundary = args.out_root / "boundary_files"
    out_calendar = args.out_root / "crop_calendars"
    out_report = args.out_root / "cropcal_audit"
    for directory in (out_boundary, out_calendar, out_report):
        directory.mkdir(parents=True, exist_ok=True)

    print(f"Reading {args.shp}")
    gdf = load_regions(args.shp)
    print(f"  {len(gdf)} features, {gdf['ADM0_NAME'].nunique()} countries, crs={gdf.crs}")

    gdf, dupes = dissolve_duplicate_keys(gdf)
    if dupes:
        print(f"  dissolved duplicate key(s): {dupes} -> {len(gdf)} features")

    gdf, unassigned_region = attach_region_grouping(gdf, args.old_shp)
    print(
        f"  Region carried forward for {len(gdf) - len(unassigned_region)}/{len(gdf)}; "
        f"{len(unassigned_region)} need manual assignment"
    )

    gdf = add_numeric_id(gdf)

    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        print(f"  reprojecting {gdf.crs} -> EPSG:4326")
        gdf = gdf.to_crs(epsg=4326)

    # --- calendar join -----------------------------------------------------
    print(f"Reading {args.calendar}")
    cal_keys, sheet_summary = calendar_keys(args.calendar)
    shp_keys = set(gdf["Key"])
    only_cal = sorted(cal_keys - shp_keys)
    only_shp = sorted(shp_keys - cal_keys)
    print(
        f"  keys: {len(shp_keys)} shapefile, {len(cal_keys)} calendar, "
        f"{len(shp_keys & cal_keys)} joined"
    )
    if only_cal:
        print(f"  UNJOINED calendar keys ({len(only_cal)}): {only_cal}")
    if only_shp:
        print(f"  shapefile keys absent from the calendar ({len(only_shp)}): {only_shp[:5]}")

    # --- country metadata --------------------------------------------------
    proposed, disagree = propose_country_metadata(gdf, args.countries_csv)
    print(
        f"  countries.csv: {len(proposed)} country(ies) missing; the centroid rule "
        f"disagrees with {len(disagree)} existing row(s) -- NOT regenerating it"
    )

    # --- write -------------------------------------------------------------
    out_shp = out_boundary / args.shp.name
    gdf.to_file(out_shp, engine="pyogrio")
    print(f"\nwrote {out_shp} ({len(gdf)} features, num_ID 1..{len(gdf)})")

    lookup = gdf.drop(columns="geometry").copy()
    lookup["country_slug"] = lookup["ADM0_NAME"].map(naming.country_slug)
    lookup_path = out_report / "calendar_regions_lookup.csv"
    lookup.to_csv(lookup_path, index=False)

    sheet_summary.to_csv(out_report / "calendar_sheet_summary.csv", index=False)
    pd.DataFrame({"key": only_cal}).to_csv(
        out_report / "unjoined_calendar_keys.csv", index=False
    )
    pd.DataFrame({"key": unassigned_region}).to_csv(
        out_report / "regions_without_grouping.csv", index=False
    )
    proposed.to_csv(out_report / "countries_new_rows_proposed.csv", index=False)
    disagree.to_csv(out_report / "countries_centroid_disagreements.csv", index=False)

    calendar_copy = out_calendar / args.calendar.name
    if calendar_copy.resolve() != args.calendar.resolve():
        calendar_copy.write_bytes(args.calendar.read_bytes())
    print(f"wrote {calendar_copy} (verbatim copy; aliases live in geocif.cropcal.naming)")
    print(f"wrote audit CSVs to {out_report}")

    print("\nPush to the cluster with:")
    for ext in SHP_PARTS:
        part = out_shp.with_suffix(ext)
        if part.is_file():
            print(f"  scp '{part}' gsapp18:{HPC_METADATA}/boundary_files/")
    print(f"  scp '{calendar_copy}' gsapp18:{HPC_METADATA}/crop_calendars/")

    if only_cal:
        print(
            f"\nERROR: {len(only_cal)} calendar key(s) do not join to a polygon; "
            f"add them to geocif.cropcal.naming.COUNTRY_ALIASES / REGION_ALIASES"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
