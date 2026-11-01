"""Build the US county -> NASS Agricultural Statistics District (ASD) table.

AgMet county runs draw one district figure per ASD when ``[AGMET] district_file``
names this table (read by geocif.agmet.geoagmet.read_district_file). It lists
every county that reported a NASS county yield for one of the commodities below
in the year range, with the ASD of its latest record. The Quick Stats API key
is read from ``[NASS] api_key`` of a geobase.txt.

Columns: ``region_id`` (county FIPS as a number), ``admin_1`` (state),
``district_id`` (2-digit state FIPS + 2-digit NASS ASD code, e.g. ``1950``),
``district_name`` and ``asd_code``.

Run on the cluster::

    ~/run.sh -m geocif.data_prep.build_usa_asd_crosswalk \\
        --geobase /gpfs/data1/cmongp1/GEO/config/production/usa_admin2/geobase.txt \\
        --out usa_county_asd_crosswalk.csv
"""

from __future__ import annotations

import argparse
import configparser
import json
import urllib.parse
import urllib.request

import pandas as pd

QUICKSTATS_URL = "https://quickstats.nass.usda.gov/api/api_GET/"
SHORT_DESCS = [
    "CORN, GRAIN - YIELD, MEASURED IN BU / ACRE",
    "SOYBEANS - YIELD, MEASURED IN BU / ACRE",
    "WHEAT, WINTER - YIELD, MEASURED IN BU / ACRE",
    "WHEAT, SPRING, (EXCL DURUM) - YIELD, MEASURED IN BU / ACRE",
    "RICE - YIELD, MEASURED IN LB / ACRE",
    "SORGHUM, GRAIN - YIELD, MEASURED IN BU / ACRE",
    "COTTON, UPLAND - YIELD, MEASURED IN LB / ACRE",
]


def fetch_county_records(key: str, short_desc: str, start: int, end: int,
                         timeout: int = 300) -> pd.DataFrame:
    """County survey records of one Quick Stats series (all practices)."""
    query = {
        "key": key,
        "source_desc": "SURVEY",
        "short_desc": short_desc,
        "agg_level_desc": "COUNTY",
        "prodn_practice_desc": "ALL PRODUCTION PRACTICES",
        "year__GE": start,
        "year__LE": end,
        "format": "JSON",
    }
    url = QUICKSTATS_URL + "?" + urllib.parse.urlencode(query)
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return pd.DataFrame(json.load(response)["data"])


def latest_asd(records: pd.DataFrame) -> pd.DataFrame:
    """One row per county with the ASD of its latest record.

    Drops NASS's 'other (combined) counties' rows (county code 998). Raises
    when a county's latest year names two ASDs.
    """
    df = records[records["county_code"] != "998"].copy()
    df["fips"] = (df["state_fips_code"] + df["county_code"]).astype(int)
    df["year"] = df["year"].astype(int)
    latest = df[df["year"] == df.groupby("fips")["year"].transform("max")]

    n_asd = latest.groupby("fips")["asd_code"].nunique()
    ambiguous = sorted(n_asd[n_asd > 1].index)
    if ambiguous:
        raise ValueError(f"counties with two ASDs in their latest year: {ambiguous[:10]}")

    latest = latest.drop_duplicates("fips")
    return pd.DataFrame({
        "region_id": latest["fips"].values,
        "admin_1": latest["state_name"].str.title().values,
        "district_id": (latest["state_fips_code"] + latest["asd_code"]).values,
        "district_name": latest["asd_desc"].str.title().values,
        "asd_code": latest["asd_code"].values,
    }).sort_values("region_id").reset_index(drop=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--geobase", required=True, help="geobase.txt with a [NASS] api_key")
    ap.add_argument("--out", required=True, help="output CSV")
    ap.add_argument("--start", type=int, default=2016, help="first year of records")
    ap.add_argument("--end", type=int, default=2025, help="last year of records")
    args = ap.parse_args(argv)

    parser = configparser.ConfigParser(inline_comment_prefixes=(";",), interpolation=None)
    parser.read(args.geobase)
    key = parser.get("NASS", "api_key").strip()

    records = pd.concat(
        [fetch_county_records(key, sd, args.start, args.end) for sd in SHORT_DESCS],
        ignore_index=True,
    )
    table = latest_asd(records)
    table.to_csv(args.out, index=False)
    print(f"wrote {args.out}: {len(table)} counties in {table['district_id'].nunique()} districts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
