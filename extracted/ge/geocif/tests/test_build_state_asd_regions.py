"""Tests for geocif.data_prep.build_state_asd_regions (Indiana ASD agmet, 2026-10-02)."""

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import box

from geocif.data_prep import build_state_asd_regions as asd

ADM0 = "United States of America"


def _yield_rows(pairs, state="Indiana"):
    return pd.DataFrame(
        [{"admin_1": state, "num_ID": fips, "usda_district": dist} for fips, dist in pairs]
    )


def _calendar():
    def row(admin, start):
        months = {f"m{i}": int(i >= start) for i in range(4)}
        return {"admin": admin, "country": "United States", "Country2": ADM0,
                "Admin2": f"{admin} {ADM0}", **months}
    return pd.DataFrame([row("Eastern Heartland", 1), row("Northeast", 2)])


def test_every_county_gets_exactly_one_district():
    df = _yield_rows([(18001, "Northeast"), (18001, "Northeast"), (18003, "Central")])
    out = asd.county_districts(df, "Indiana", [18003, 18001])
    assert out.loc[18001] == "Northeast"
    assert out.loc[18003] == "Central"


def test_county_missing_from_yield_file_raises():
    df = _yield_rows([(18001, "Northeast")])
    with pytest.raises(ValueError, match="no ASD"):
        asd.county_districts(df, "Indiana", [18001, 18005])


def test_county_in_two_districts_raises():
    df = _yield_rows([(18001, "Northeast"), (18001, "Central")])
    with pytest.raises(ValueError, match="more than one ASD"):
        asd.county_districts(df, "Indiana", [18001])


def test_other_states_are_ignored():
    df = pd.concat([_yield_rows([(18001, "Northeast")]),
                    _yield_rows([(18001, "Delta")], state="Arkansas")])
    assert asd.county_districts(df, "Indiana", [18001]).tolist() == ["Northeast"]


def test_dissolve_gives_one_prefixed_polygon_per_district():
    gdf = gpd.GeoDataFrame(
        {"ADM0_NAME": [ADM0] * 3, "num_ID": [18001, 18003, 18005]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(5, 5, 6, 6)],
        crs="EPSG:4269",
    )
    districts = pd.Series({18001: "Northeast", 18003: "Northeast", 18005: "Southwest"})
    out = asd.dissolve_districts(gdf, districts, "Indiana")
    assert out["Name"].tolist() == ["Indiana Northeast", "Indiana Southwest"]
    assert out["n_county"].tolist() == [2, 1]
    assert out["Key"].iloc[0] == f"{ADM0} Indiana Northeast"
    assert out["Key2"].iloc[0] == f"Indiana Northeast {ADM0}"
    assert out.geometry.iloc[0].area == pytest.approx(2.0)
    assert out.crs == gdf.crs


def test_calendar_rows_copy_the_source_zone():
    names = ["Indiana Northeast", "Indiana Central"]
    out = asd.calendar_with_districts(_calendar(), "Eastern Heartland", ADM0, names)
    added = out.iloc[-2:]
    assert added["admin"].tolist() == names
    assert added["Admin2"].tolist() == [f"{n} {ADM0}" for n in names]
    src = out.iloc[0]
    for col in ("m0", "m1", "m2", "m3", "country", "Country2"):
        assert (added[col] == src[col]).all()
    # The GEOGLAM "Northeast" row is untouched.
    assert out.iloc[1]["m1"] == 0


def test_unprefixed_name_that_shadows_a_geoglam_zone_is_refused():
    # GEOGLAM has a US zone called "Northeast": a bare NASS district name would
    # silently take that zone's calendar.
    with pytest.raises(ValueError, match="already has rows"):
        asd.calendar_with_districts(_calendar(), "Eastern Heartland", ADM0, ["Northeast"])


def test_missing_source_zone_raises():
    with pytest.raises(ValueError, match="expected one"):
        asd.calendar_with_districts(_calendar(), "Corn Belt", ADM0, ["Indiana Central"])
