"""Rewrite a GlobalCM calendar workbook into the schema geoprepare expects.

``GlobalCM_2026-09-11.xlsx`` ships one sheet per crop-season named ``Maize 1`` /
``Winter Wheat``, with columns ``Country``, ``Name``, ``Key``. Every downstream
geoprepare stage wants the older AMISCM/EWCM shape instead, and **neither
mismatch raises**:

* ``base.BaseGeo.get_calendar_sheet_name`` asks for ``maize_1`` (or the bare
  crop for the wheats). A missing sheet name makes ``pd.read_excel`` raise
  inside a path that returns an empty frame;
* ``geomerge.process_combination`` skips any combination whose calendar is empty
  **or lacks a ``country2`` column**, logging an error and returning False. With
  the shipped workbook that is every combination -- the run completes, reports
  success, and writes nothing.

So this converts rather than patching geoprepare: one workbook, readable by both
``geoprepare`` and ``geocif.cropcal.calendar`` (whose reader already accepts
either schema).

What changes
------------
========================  ==========================================
sheet ``Maize 1``         sheet ``maize_1``
sheet ``Winter Wheat``    sheet ``winter_wheat`` (wheats carry no season)
column ``Name``           column ``admin``      -> ``calendar_region``
column ``Country``        column ``Country2``   -> matched against the slug
column ``Key``            column ``Admin2``
(new)                     column ``country``    -> the config slug
========================  ==========================================

``harmonize_df`` lower-cases and underscores every string value downstream, so
``Country2`` must hold the **display** name ("United States of America"), which
becomes the config slug on read.

Rows where the crop is not grown (all ``-1``) are dropped, matching the older
workbooks, which listed only the regions a crop actually occupies. A stray
``-1`` inside an otherwise real row becomes ``0`` (out of season).

Usage::

    python -m geocif.data_prep.convert_calendar_for_geomerge \
        --calendar ".../crop_calendars/GlobalCM_2026-09-11.xlsx"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.cropcal import calendar as cropcal_calendar
from geocif.cropcal import naming

#: Crops whose sheet name carries no season suffix, per get_calendar_sheet_name.
SINGLE_SEASON_CROPS = {"winter_wheat", "spring_wheat"}

SUFFIX = "_geomerge"


def sheet_name_for(crop: str, season: int) -> str:
    """Mirror ``base.BaseGeo.get_calendar_sheet_name`` exactly."""
    return crop if crop in SINGLE_SEASON_CROPS else f"{crop}_{season}"


def convert(calendar_path: Path, out_path: Path) -> pd.DataFrame:
    """Write the converted workbook; return a per-sheet summary."""
    sheets = cropcal_calendar.read_workbook(calendar_path)
    code_columns = [f"code_{i}" for i in range(cropcal_calendar.N_BINS)]
    bimonth = list(cropcal_calendar.BIMONTH_COLS)

    rows = []
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for crop_season, frame in sorted(sheets.items()):
            crop, season = crop_season.crop, crop_season.season
            codes = frame[code_columns].to_numpy(dtype=float)
            grown = ~np.all(codes == cropcal_calendar.CODE_NOT_GROWN, axis=1)

            out = pd.DataFrame(
                {
                    "admin": frame.loc[grown, "region"].to_numpy(),
                    "country": frame.loc[grown, "country_slug"].to_numpy(),
                    "Country2": frame.loc[grown, "country"].to_numpy(),
                    "Admin2": frame.loc[grown, "key"].to_numpy(),
                }
            )
            # A stray -1 inside a real row means "not grown here"; 0 is the
            # out-of-season code geoprepare understands.
            kept = np.where(codes[grown] == cropcal_calendar.CODE_NOT_GROWN, 0.0, codes[grown])
            for index, column in enumerate(bimonth):
                out[column] = kept[:, index].astype(int)

            name = sheet_name_for(crop, season)
            out.to_excel(writer, sheet_name=name, index=False)
            rows.append(
                {
                    "source_sheet": f"{crop} {season}",
                    "written_sheet": name,
                    "rows": len(out),
                    "countries": out["country"].nunique(),
                }
            )
    return pd.DataFrame(rows)


def dedupe_zone_file(path: Path, out_path: Path) -> pd.DataFrame:
    """Write a duplicate-free copy of ``countries.csv``; return the conflicts.

    The zone merge in ``geomerge.post_process`` is a plain left join on
    ``country``, so N rows for one country duplicates **every** merged row N
    times. The damage surfaces two stages later as a non-unique MultiIndex in
    the CID step, not here.

    The live file is left untouched -- it is shared with every other project --
    and the per-project ``zone_file`` key points at this copy instead.
    """
    frame = pd.read_csv(path)
    frame["_join"] = frame["country"].map(naming.normalize)
    duplicated = frame[frame.duplicated("_join", keep=False)]
    conflicts = (
        duplicated.groupby("_join")
        .filter(lambda part: part["region"].nunique() > 1 or part["hemisphere"].nunique() > 1)
        if not duplicated.empty
        else duplicated
    )
    frame.drop_duplicates("_join", keep="first").drop(columns="_join").to_csv(
        out_path, index=False
    )
    return conflicts.drop(columns="_join") if not conflicts.empty else conflicts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--calendar", required=True, type=Path)
    ap.add_argument("--zone-file", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)

    out_path = args.out or args.calendar.with_name(
        args.calendar.stem + SUFFIX + args.calendar.suffix
    )
    summary = convert(args.calendar, out_path)
    print(f"wrote {out_path}")
    print(summary.to_string(index=False))
    print(f"\n  sheets: {len(summary)}   rows: {int(summary['rows'].sum())}")

    if args.zone_file:
        zone_out = args.zone_file.with_name(args.zone_file.stem + "_dedup.csv")
        conflicts = dedupe_zone_file(args.zone_file, zone_out)
        print(f"\nwrote {zone_out}")
        if len(conflicts):
            print("  CONFLICTING duplicate rows (first kept):")
            print(conflicts.to_string(index=False))
        else:
            print("  no conflicting duplicates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
