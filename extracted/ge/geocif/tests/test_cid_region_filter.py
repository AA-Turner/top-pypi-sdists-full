"""
Tests for restricting CID generation to run_regions (geocif/cid/indices.py).

CID generation processed every EO-covered region even though the ML stage only
models the states named in run_regions (usa_admin2: 2,038 counties computed,
919 modelled). Filtering at READ time cuts both the parse transient and the
cached frame, and roughly halves the compute for a rebuild.

Opt-in by design: filtering couples the generated CID files to run_regions, so
adding a state later means regenerating that state's CIDs.
"""

import configparser
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.cid import indices
from geocif.ml import stats


def parser_with(**options):
    p = configparser.ConfigParser()
    p.add_section("united_states_of_america")
    for key, value in options.items():
        p.set("united_states_of_america", key, value)
    return p


# ------------------------------------------- country resolution (regression)


def test_country_is_derived_from_the_file_name():
    """self.country is "" until AFTER the CSV is read, but the filter runs
    during the read. Falling back to "" silently disabled filtering and wrote
    1,759 counties instead of 1,004 (2026-08-18)."""
    assert indices.country_from_file_name(
        "united_states_of_america_soybean_s1.csv") == "united_states_of_america"
    assert indices.country_from_file_name(
        "united_states_of_america_maize_s1.csv") == "united_states_of_america"


def test_country_from_file_name_handles_other_projects():
    assert indices.country_from_file_name("kenya_maize_s1.csv") == "kenya"
    assert indices.country_from_file_name("south_africa_maize_s2.csv") == "south_africa"


def test_country_from_file_name_is_non_fatal_on_junk():
    for name in ("", "nonsense.csv", "no_season_here.csv"):
        assert isinstance(indices.country_from_file_name(name), str)


def test_empty_country_key_selects_nothing_rather_than_matching_default():
    """The failure mode: an empty section name must not resolve a flag."""
    p = parser_with(filter_cids_to_run_regions="True", run_regions="['illinois']")
    assert indices.cid_run_region_selection(p, "", "maize") is None


# --------------------------------------------------- shared config parsing


def test_parse_run_regions_list_form():
    assert stats.parse_run_regions("['illinois', 'iowa']") == ["illinois", "iowa"]


def test_parse_run_regions_per_crop_dict():
    raw = "{'maize': ['illinois'], 'soybean': ['iowa', 'arkansas']}"
    assert stats.parse_run_regions(raw, crop="soybean") == ["iowa", "arkansas"]
    assert stats.parse_run_regions(raw, crop="maize") == ["illinois"]


def test_parse_run_regions_crop_absent_means_no_filtering():
    raw = "{'maize': ['illinois']}"
    assert stats.parse_run_regions(raw, crop="sorghum") is None


def test_parse_run_regions_malformed_is_treated_as_unset():
    for raw in ("", None, "not python", "42", "{'maize': 3}"):
        assert stats.parse_run_regions(raw, crop="maize") in (None, [])


# ------------------------------------------------------------ flag gating


def test_filtering_is_off_by_default():
    """Must not silently couple existing projects' CIDs to run_regions."""
    p = parser_with(run_regions="['illinois']")
    assert indices.cid_run_region_selection(p, "united_states_of_america", "maize") is None


def test_flag_on_returns_normalized_selection():
    p = parser_with(filter_cids_to_run_regions="True",
                    run_regions="['illinois', 'south_dakota']")
    got = indices.cid_run_region_selection(p, "united_states_of_america", "maize")
    assert got == {"illinois", "south dakota"}


def test_flag_on_but_no_run_regions_means_no_filtering():
    p = parser_with(filter_cids_to_run_regions="True")
    assert indices.cid_run_region_selection(p, "united_states_of_america", "maize") is None


def test_per_crop_selection_is_honoured():
    p = parser_with(filter_cids_to_run_regions="True",
                    run_regions="{'maize': ['illinois'], 'soybean': ['iowa']}")
    assert indices.cid_run_region_selection(p, "united_states_of_america", "soybean") == {"iowa"}


# ------------------------------------------------------- region matching


def test_parent_state_keeps_its_counties():
    regions = pd.Series(["illinois_boone", "illinois_cook", "iowa_adair"])
    mask = indices._region_keep_mask(regions, {"illinois"})
    assert list(mask) == [True, True, False]


def test_multi_word_state():
    regions = pd.Series(["south_dakota_lake", "north_dakota_cass"])
    mask = indices._region_keep_mask(regions, {"south dakota"})
    assert list(mask) == [True, False]


def test_kansas_does_not_match_arkansas():
    """The prefix trap: 'kansas' must not sweep in every Arkansas county."""
    regions = pd.Series(["kansas_allen", "arkansas_ashley"])
    mask = indices._region_keep_mask(regions, {"kansas"})
    assert list(mask) == [True, False]


def test_state_selected_alone_matches_exactly():
    """An admin_1 run: the region IS the state, with no county suffix."""
    mask = indices._region_keep_mask(pd.Series(["illinois", "iowa"]), {"illinois"})
    assert list(mask) == [True, False]


def test_partial_name_does_not_match():
    regions = pd.Series(["illinoisx_county", "illinois_boone"])
    mask = indices._region_keep_mask(regions, {"illinois"})
    assert list(mask) == [False, True]


def test_matching_is_separator_insensitive():
    regions = pd.Series(["Illinois Boone", "illinois_boone"])
    mask = indices._region_keep_mask(regions, {"illinois"})
    assert list(mask) == [True, True]


# ------------------------------------------------- filtered chunked read


@pytest.fixture
def merged_csv(tmp_path):
    rows = []
    for state, county in [("illinois", "boone"), ("illinois", "cook"),
                          ("iowa", "adair"), ("alabama", "autauga"),
                          ("south_dakota", "lake")]:
        for doy in range(1, 51):
            rows.append({
                "datetime": f"2024-01-{(doy % 28) + 1:02d}",
                "country": "united_states_of_america",
                "region": f"{state}_{county}",
                "region_id": 1001,
                "lat": 40.0, "lon": -90.0,
                "year": 2024, "doy": doy,
                "crop": "maize", "scale": "admin_2",
                "calendar_region": "midwest",
                "chirps": float(doy), "ndvi": doy / 100.0,
                "name_month": "January",
            })
    path = tmp_path / "united_states_of_america_maize_s1.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_unfiltered_read_returns_every_region(merged_csv):
    df = indices._read_input_csv(merged_csv)
    assert df["region"].nunique() == 5


def test_filtered_read_keeps_only_selected_states(merged_csv):
    df = indices._read_input_csv(merged_csv, keep_regions={"illinois", "south dakota"})
    assert set(df["region"].unique()) == {"illinois_boone", "illinois_cook", "south_dakota_lake"}
    assert len(df) == 150


def test_filtered_read_preserves_dtypes(merged_csv):
    """concat of chunks must not degrade categoricals back to object."""
    df = indices._read_input_csv(merged_csv, keep_regions={"illinois"})
    assert isinstance(df["country"].dtype, pd.CategoricalDtype)
    assert isinstance(df["region"].dtype, pd.CategoricalDtype)
    assert df["chirps"].dtype == np.float32
    assert df["lat"].dtype == np.float64


def test_filtered_read_still_drops_display_columns(merged_csv):
    df = indices._read_input_csv(merged_csv, keep_regions={"illinois"})
    assert "name_month" not in df.columns


def test_filtered_read_preserves_values(merged_csv):
    unfiltered = indices._read_input_csv(merged_csv)
    filtered = indices._read_input_csv(merged_csv, keep_regions={"iowa"})
    expected = unfiltered[unfiltered["region"].astype(str) == "iowa_adair"]
    assert len(filtered) == len(expected)
    np.testing.assert_allclose(
        np.sort(filtered["chirps"].to_numpy(dtype=float)),
        np.sort(expected["chirps"].to_numpy(dtype=float)),
    )


def test_selection_matching_nothing_returns_empty_not_everything(merged_csv):
    """A typo'd state must not silently fall back to running all regions."""
    df = indices._read_input_csv(merged_csv, keep_regions={"atlantis"})
    assert len(df) == 0
    assert list(df.columns)


def test_chunk_boundary_does_not_lose_rows(merged_csv, monkeypatch):
    """Rows must survive being split across chunk boundaries."""
    monkeypatch.setattr(indices, "_READ_CHUNK_ROWS", 7)
    df = indices._read_input_csv(merged_csv, keep_regions={"illinois"})
    assert len(df) == 100
    assert set(df["region"].unique()) == {"illinois_boone", "illinois_cook"}
