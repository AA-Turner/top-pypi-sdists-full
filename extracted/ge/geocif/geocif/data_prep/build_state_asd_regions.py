"""Build NASS Agricultural Statistics District calendar regions for one US state.

AgMet draws one district figure per calendar region, and geomerge gives each
county its calendar region by largest-area overlap with the ``shp_region``
shapefile. The GEOGLAM zones put a whole state such as Indiana into one zone
("Eastern Heartland"), so a county run gets a single district figure. This
script makes the state's NASS Agricultural Statistics Districts (ASDs) the
calendar regions instead.

What it does

1.  Reads the county -> ASD assignment from the county yield file
    (``usda_district``, keyed by FIPS ``num_ID``) and requires every county in
    the boundary file to map to exactly one ASD.
2.  Dissolves the counties into one polygon per ASD and writes a region
    shapefile with the columns geoprepare.georegion and geoagmet read
    (``ADM0_NAME``, ``Name``, ``Key``, ``Key2``).
3.  Copies the calendar workbook and appends one row per ASD to each requested
    sheet, duplicating the row of the GEOGLAM zone that contains the state, so
    every ASD carries that zone's dates.
4.  Writes a FIPS -> ASD crosswalk CSV.

ASD names carry the state as a prefix ("Indiana Northeast") because GEOGLAM
already has US zones called "Northeast" and "Southeast". An unprefixed name
would pick up that zone's calendar row.

Needs geopandas and openpyxl, so run it on the cluster::

    ~/run.sh /gpfs/data1/cmongp1/ritvik/scripts/build_state_asd_regions.py \
        --state Indiana --abbrev in

Then point the project's ``countries.txt`` country section at the outputs::

    shp_region = usa_in_asd.shp
    calendar_file = AMISCM_2026-01-05_indiana_asd.xlsx
"""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd

DEFAULT_METADATA = Path("/gpfs/data1/cmongp1/GEO/inputs/metadata")
DEFAULT_YIELD_FILE = "adm_crop_production_US_county_wide.csv"
DEFAULT_CALENDAR = "AMISCM_2026-01-05.xlsx"
DEFAULT_SOURCE_ZONE = "Eastern Heartland"
DEFAULT_SHEETS = ["maize_1", "soybean_1"]


def _norm(text) -> str:
    """Normalise a name the way geoprepare does: lowercase, spaces -> underscores."""
    return str(text).strip().lower().replace(" ", "_")


def county_districts(df_yield: pd.DataFrame, state: str, county_ids) -> pd.Series:
    """Map each county FIPS in ``county_ids`` to its single NASS ASD.

    Raises when a county has no ASD in the yield file or more than one, since
    either would leave the county without a calendar region (geomerge drops it).
    """
    df = df_yield.loc[df_yield["admin_1"].str.lower() == state.lower(),
                      ["num_ID", "usda_district"]].dropna()
    df = df.assign(num_ID=df["num_ID"].astype(int)).drop_duplicates()

    n_asd = df.groupby("num_ID")["usda_district"].nunique()
    ambiguous = sorted(n_asd[n_asd > 1].index)
    if ambiguous:
        raise ValueError(f"counties mapped to more than one ASD: {ambiguous}")

    lookup = df.set_index("num_ID")["usda_district"]
    ids = pd.Index([int(i) for i in county_ids])
    missing = sorted(ids.difference(lookup.index))
    if missing:
        raise ValueError(f"{len(missing)} counties have no ASD in the yield file: {missing}")
    return lookup.loc[ids]


def dissolve_districts(gdf_counties: gpd.GeoDataFrame, districts: pd.Series,
                       state: str) -> gpd.GeoDataFrame:
    """Dissolve counties into one polygon per ASD with georegion's region columns."""
    gdf = gdf_counties.assign(
        ASD=districts.reindex(gdf_counties["num_ID"].astype(int)).values
    )
    adm0 = gdf["ADM0_NAME"].iloc[0]
    out = gdf.dissolve(by="ASD", aggfunc={"num_ID": "count"}).reset_index()
    out = out.rename(columns={"num_ID": "n_county"})
    out["Name"] = f"{state} " + out["ASD"]
    out["ADM0_NAME"] = adm0
    out["Key"] = adm0 + " " + out["Name"]
    out["Key2"] = out["Name"] + " " + adm0
    cols = ["ADM0_NAME", "Name", "Key", "Key2", "ASD", "n_county", "geometry"]
    return out[cols].sort_values("Name").reset_index(drop=True)


def calendar_with_districts(df_sheet: pd.DataFrame, source_zone: str, adm0: str,
                            names) -> pd.DataFrame:
    """Append one copy of ``source_zone``'s calendar row per ASD name.

    The source row is matched on ``admin`` and ``Country2`` and must be unique.
    Refuses names that already exist in the sheet, so a GEOGLAM zone row is
    never shadowed and a second run on an output workbook fails loudly.
    """
    is_src = (df_sheet["admin"].map(_norm) == _norm(source_zone)) & (
        df_sheet["Country2"].map(_norm) == _norm(adm0)
    )
    if is_src.sum() != 1:
        raise ValueError(
            f"expected one '{source_zone}' row for {adm0}, found {int(is_src.sum())}"
        )

    existing = set(df_sheet["admin"].map(_norm))
    clash = sorted(n for n in names if _norm(n) in existing)
    if clash:
        raise ValueError(f"calendar already has rows named {clash}")

    src = df_sheet.loc[is_src].iloc[0]
    rows = []
    for name in names:
        row = src.copy()
        row["admin"] = name
        row["Admin2"] = f"{name} {src['Country2']}"
        rows.append(row)
    return pd.concat([df_sheet, pd.DataFrame(rows)], ignore_index=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--state", required=True, help="state name as in admin_1, e.g. Indiana")
    ap.add_argument("--abbrev", required=True, help="lowercase postal code used in file names, e.g. in")
    ap.add_argument("--metadata-root", type=Path, default=DEFAULT_METADATA)
    ap.add_argument("--county-shp", default=None,
                    help="boundary file name (default usa_<abbrev>_counties_fips.shp)")
    ap.add_argument("--yield-file", default=DEFAULT_YIELD_FILE)
    ap.add_argument("--calendar", default=DEFAULT_CALENDAR)
    ap.add_argument("--source-zone", default=DEFAULT_SOURCE_ZONE,
                    help="calendar row whose dates every ASD copies")
    ap.add_argument("--sheets", nargs="+", default=DEFAULT_SHEETS)
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    args = ap.parse_args(argv)

    dir_bnd = args.metadata_root / "boundary_files"
    dir_cal = args.metadata_root / "crop_calendars"
    dir_stats = args.metadata_root / "production_statistics"

    path_counties = dir_bnd / (args.county_shp or f"usa_{args.abbrev}_counties_fips.shp")
    path_shp = dir_bnd / f"usa_{args.abbrev}_asd.shp"
    path_xwalk = dir_bnd / f"usa_{args.abbrev}_asd_crosswalk.csv"
    path_cal_in = dir_cal / args.calendar
    path_cal_out = dir_cal / f"{Path(args.calendar).stem}_{_norm(args.state)}_asd.xlsx"

    outputs = [path_shp, path_xwalk, path_cal_out]
    if not args.force and any(p.exists() for p in outputs):
        raise SystemExit(f"outputs exist, pass --force to overwrite: "
                         f"{[str(p) for p in outputs if p.exists()]}")

    gdf_counties = gpd.read_file(path_counties, engine="pyogrio")
    df_yield = pd.read_csv(dir_stats / args.yield_file,
                           usecols=["admin_1", "num_ID", "usda_district"])
    districts = county_districts(df_yield, args.state, gdf_counties["num_ID"])

    gdf_asd = dissolve_districts(gdf_counties, districts, args.state)
    gdf_asd.to_file(path_shp, engine="pyogrio")
    print(f"wrote {path_shp} ({len(gdf_asd)} districts, {gdf_counties.crs})")
    print(gdf_asd.drop(columns="geometry").to_string(index=False))

    xwalk = pd.DataFrame({
        "num_ID": gdf_counties["num_ID"].astype(int).values,
        "county": gdf_counties["ADM2_NAME"].values,
        "district": districts.values,
    })
    xwalk["calendar_region"] = f"{args.state} " + xwalk["district"]
    xwalk.sort_values(["district", "num_ID"]).to_csv(path_xwalk, index=False)
    print(f"wrote {path_xwalk} ({len(xwalk)} counties)")

    adm0 = gdf_asd["ADM0_NAME"].iloc[0]
    names = gdf_asd["Name"].tolist()
    sheets = pd.read_excel(path_cal_in, sheet_name=None)
    for sheet in args.sheets:
        sheets[sheet] = calendar_with_districts(sheets[sheet], args.source_zone, adm0, names)
    with pd.ExcelWriter(path_cal_out, engine="openpyxl") as writer:
        for sheet, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
    print(f"wrote {path_cal_out} (+{len(names)} rows in {args.sheets}, "
          f"copied from '{args.source_zone}')")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
