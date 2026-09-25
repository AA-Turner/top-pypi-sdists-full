"""The Franch et al. (2022) feature additions: elevation, dew point, season blocks.

Three things worth guarding:

* season blocks are HEMISPHERE-ALIGNED -- "winter" is the cold season on both
  sides of the equator, unlike Franch's calendar DJF;
* the static elevation file is named region-first, unlike the daily files, and
  must still be found for the right region id;
* a region without the new data keeps every feature column (NaN) and says so in
  its availability flags.
"""

import numpy as np
import pandas as pd
import pytest

from geocif.cropcal import circular, features, naming, series

N_DOY = 366
DOY = np.arange(N_DOY)


def _seasonal(peak_doy, mean=15.0, amp=10.0):
    return mean + amp * np.cos(2 * np.pi * (DOY - peak_doy) / 365.0)


def test_season_blocks_follow_the_hemisphere():
    north = features.season_block_features(_seasonal(200), None, None, hemisphere="N")
    south = features.season_block_features(_seasonal(15), None, None, hemisphere="S")
    # The warm season is "summer" in both, though it is July in one and January in the other.
    for block in (north, south):
        assert block["tmean_summer_max"] > block["tmean_winter_max"] + 10
        assert block["tmean_annual_amplitude"] == pytest.approx(
            block["tmean_annual_max"] - block["tmean_annual_min"]
        )
    assert north["tmean_summer_max"] == pytest.approx(south["tmean_summer_max"], abs=0.5)


def test_season_blocks_are_nan_without_data_and_cover_every_name():
    out = features.season_block_features(None, None, None)
    assert len(out) == 3 * 5 * 3
    assert all(np.isnan(v) for v in out.values())


def test_dewpoint_depression_marks_the_humid_season():
    tmean = _seasonal(200, mean=25.0, amp=5.0)
    tdew = _seasonal(200, mean=12.0, amp=8.0)     # air far moister than average in July
    out = features.dewpoint_features(tdew, tmean)
    assert out["tdew_max"] > out["tdew_min"]
    assert circular.circular_gap(out["doy_tdew_max"], 200) <= 5
    assert circular.circular_gap(out["doy_dewpoint_depression_min"], 200) <= 5
    assert out["dewpoint_depression_min"] < out["dewpoint_depression_max"]


def test_terrain_passthrough_and_availability_flags():
    nan_year = np.full(N_DOY, np.nan)
    common = dict(
        key="k", country="c", region="r", crop="maize", season=1, cm_group="",
        climate_zone="", hemisphere="N", lat=0.0, lon=0.0, ndvi=nan_year, gdd=nan_year,
        agdd=nan_year, peaks=[], valleys=[],
    )
    bare = features.build_row(**common)
    assert bare["terrain_available"] == 0 and bare["tdew_available"] == 0
    assert np.isnan(bare["elevation_m"]) and np.isnan(bare["tdew_min"])
    assert set(features.FEATURE_NAMES) <= set(bare)

    full = features.build_row(**common, elevation=1850.0, slope=0.004, tdew=_seasonal(200))
    assert full["elevation_m"] == 1850.0 and full["terrain_slope"] == 0.004
    assert full["terrain_available"] == 1 and full["tdew_available"] == 1


def test_new_groups_partition_the_allow_list():
    for group in ("terrain", "dewpoint", "season_blocks"):
        assert features.FEATURE_GROUPS[group]
    names = [n for g in features.FEATURE_GROUPS.values() for n in g]
    assert sorted(names) == sorted(features.FEATURE_NAMES)


def test_static_file_is_found_by_region_id_not_name(tmp_path):
    d = tmp_path / "dem"
    d.mkdir()
    pd.DataFrame({"country": ["x"], "region": ["northern_2020"], "region_id": [7],
                  "lat": [0], "lon": [0], "elevation": [412.5], "slope": [0.002]}
                 ).to_csv(d / "northern_2020_7_dem_winter_wheat.csv", index=False)
    pd.DataFrame({"country": ["x"], "region": ["other"], "region_id": [71],
                  "lat": [0], "lon": [0], "elevation": [9.0], "slope": [0.0]}
                 ).to_csv(d / "other_71_dem_winter_wheat.csv", index=False)
    assert series.load_static_region(d, 7, columns=("elevation", "slope")) == {"elevation": 412.5, "slope": 0.002}
    assert series.load_static_region(d, 71, columns=("elevation",)) == {"elevation": 9.0}
    assert series.load_static_region(d, 99, columns=("elevation",)) == {}
    assert series.load_static_region(tmp_path / "absent", 7, columns=("elevation",)) == {}


def test_climatology_loads_dewpoint_and_elevation(tmp_path):
    years = range(2019, 2025)

    def write(var, values):
        directory = series.region_dir(tmp_path, 1, "testland", "admin_1", "maize", var)
        directory.mkdir(parents=True, exist_ok=True)
        for year in years:
            pd.DataFrame({"country": "testland", "region": "central", "region_id": 42,
                          "lat": 0.0, "lon": 0.0, "year": year, "doy": np.arange(1, N_DOY + 1),
                          var: values}).to_csv(directory / f"42_central_{year}_{var}_maize.csv", index=False)

    write(series.VAR_NDVI, (0.2 + 0.5 * np.exp(-0.5 * ((DOY - 200) / 35) ** 2)) * series.NDVI_GAIN + series.NDVI_OFFSET)
    write(series.VAR_TMAX, _seasonal(200, 25))
    write(series.VAR_TMIN, _seasonal(200, 12))
    write(series.VAR_DEWPOINT, _seasonal(200, 8))
    dem = series.region_dir(tmp_path, 1, "testland", "admin_1", "maize", series.VAR_DEM)
    dem.mkdir(parents=True)
    pd.DataFrame({"country": ["testland"], "region": ["central"], "region_id": [42], "lat": [0], "lon": [0],
                  "elevation": [1234.0], "slope": [0.01]}).to_csv(dem / "central_42_dem_maize.csv", index=False)

    clim = series.build_climatology(tmp_path, 1, "testland", "admin_1", "maize", "central", 42,
                                    params=naming.crop_params("maize"), years=tuple(years))
    assert clim.tdew is not None and np.nanmax(clim.tdew) == pytest.approx(18.0, abs=0.1)
    assert clim.elevation == 1234.0 and clim.slope == 0.01
    assert clim.available[series.VAR_DEWPOINT] and clim.available[series.VAR_DEM]


def test_dewpoint_physical_range_is_enforced():
    out = series.rescale(np.array([-80.0, -10.0, 25.0, 300.0]), series.VAR_DEWPOINT)
    assert np.isnan(out[0]) and np.isnan(out[3])
    assert out[1:3].tolist() == [-10.0, 25.0]
