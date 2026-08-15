"""Regression tests for the memory-lean input reader (_read_input_csv).

Stage-1 memory fix (0.4.909): at county scale each parallel year-task holds
its own full copy of the merged input frame, and object-dtype string columns
dominated it (~16 GB/worker on usa_admin2). _read_input_csv reads the
repeated-label columns as ``category`` and skips display-only columns.

The dangerous interaction is groupby: enumeration over categorical keys with
pandas' observed=False default yields one (empty) group per unused category
level — e.g. discover_regions would report 3,111 phantom counties for a
frame filtered to a handful. These tests pin the reader contract and the
observed=True behavior at the enumeration sites.
"""
import os
import tempfile

import pandas as pd
import pytest

from geocif.cid.indices import (
    _READ_CATEGORY_COLS,
    _READ_DROP_COLS,
    _read_input_csv,
)

_CSV = """datetime,country,region,region_id,lat,lon,year,doy,day,abbr_month,name_month,month,crop,scale,growing_season,calendar_region,crop_calendar,harvest_season,chirps
2020-01-01,united_states_of_america,iowa_adair,19001,41.3,-94.5,2020,1,1,Jan,January,1,soybean,admin_2,1,iowa,1,2020,0.5
2020-01-02,united_states_of_america,missouri_adair,29001,40.2,-92.6,2020,2,2,Jan,January,1,soybean,admin_2,1,missouri,1,2020,1.5
2020-01-03,united_states_of_america,iowa_adair,19001,41.3,-94.5,2020,3,3,Jan,January,1,soybean,admin_2,1,iowa,2,2020,0.0
"""


@pytest.fixture()
def input_csv(tmp_path):
    p = tmp_path / "united_states_of_america_soybean_s1.csv"
    p.write_text(_CSV)
    return p


def test_display_columns_dropped(input_csv):
    df = _read_input_csv(input_csv)
    leaked = set(df.columns) & _READ_DROP_COLS
    assert not leaked, f"display-only columns not dropped: {leaked}"


def test_string_columns_are_categorical(input_csv):
    df = _read_input_csv(input_csv)
    present = set(df.columns) & _READ_CATEGORY_COLS
    assert present, "no category-candidate columns in fixture"
    for c in present:
        assert isinstance(df[c].dtype, pd.CategoricalDtype), (
            f"{c} should be category, got {df[c].dtype}"
        )


def test_numeric_columns_unaffected(input_csv):
    df = _read_input_csv(input_csv)
    for c in ("region_id", "lat", "lon", "year", "doy", "chirps"):
        assert pd.api.types.is_numeric_dtype(df[c]), f"{c} lost numeric dtype"


def test_missing_columns_tolerated(tmp_path):
    # A minimal input without any drop/category candidates must still read.
    p = tmp_path / "minimal.csv"
    p.write_text("datetime,year,doy,chirps\n2020-01-01,2020,1,0.5\n")
    df = _read_input_csv(p)
    assert len(df) == 1


def test_observed_groupby_excludes_phantom_regions(input_csv):
    # The contract behind the observed=True additions at the enumeration
    # sites (process_data / process_data_pre_season / discover_regions /
    # add_season_information): after filtering, unused category levels must
    # not surface as (empty) groups.
    df = _read_input_csv(input_csv)
    sub = df[df["region"] == "iowa_adair"]
    keys = list(sub.groupby(["country", "region"], observed=True).groups.keys())
    assert keys == [("united_states_of_america", "iowa_adair")], keys
