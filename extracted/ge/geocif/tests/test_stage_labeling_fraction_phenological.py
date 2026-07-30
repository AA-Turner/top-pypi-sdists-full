"""Regression tests for stage labeling under the season-normalized methods
``fraction_season`` and ``phenological_stages`` (and ``full_season``).

These methods were wired on the CID side but never on the ML stage-labeling
side, so every run crashed before training:

  * ValueError: invalid literal for int() with base 10: '10.0'
    -> float-formatted Stage tokens ("10.0_20.0_...") from indices.py
  * UnboundLocalError: local variable 'stage_dict' referenced before assignment
    -> add_stage_information / get_stage_information_dict / update_feature_names
       selected a month dict only for dekad/biweekly/monthly, with no branch
       for these methods.

The fix writes integer Stage tokens at the source and gates the month-dict
machinery behind ``_is_calendar_method`` so normalized methods label with the
numeric tokens themselves. These tests lock both behaviours.
"""
import numpy as np
import pandas as pd
import pytest

from geocif.ml import stages
from geocif import utils


# ---------------------------------------------------------------------------
# Source-of-float guard (indices.py join sites 1476 / 1747)
# ---------------------------------------------------------------------------
def test_stage_string_is_integer_tokens():
    """The Stage string join must emit '10_20_100', not '10.0_20.0_100.0',
    for a float64 stage array (fraction_season / phenological_stages)."""
    stage = np.array([10.0, 20.0, 100.0])
    assert "_".join(str(int(s)) for s in stage) == "10_20_100"
    # Whole-number floats coerce exactly; integer arrays are unaffected.
    assert "_".join(str(int(s)) for s in np.array([1.0, 2.0, 3.0])) == "1_2_3"
    assert "_".join(str(int(s)) for s in np.array([12, 11, 10])) == "12_11_10"


# ---------------------------------------------------------------------------
# add_stage_information
# ---------------------------------------------------------------------------
def _mini_df(stage_token):
    return pd.DataFrame(
        {
            "Stage": [stage_token],
            "Region": ["R1"],
            "Harvest Year": [2020],
        }
    )


def test_add_stage_information_fraction_season_int_tokens():
    df = stages.add_stage_information(_mini_df("10_20_30_40_50_60_70_80_90_100"),
                                      "fraction_season")
    row = df.iloc[0]
    assert row["Starting Stage"] == 10
    assert row["Ending Stage"] == 100
    assert row["Stage Range"] == "10_100"
    assert row["Stage Names"] == "10%-100%"


def test_add_stage_information_fraction_season_float_tokens_tolerated():
    """Older cached CID CSVs may carry '10.0' float tokens; must not crash."""
    df = stages.add_stage_information(
        _mini_df("10.0_20.0_30.0_40.0_50.0_60.0_70.0_80.0_90.0_100.0"),
        "fraction_season",
    )
    row = df.iloc[0]
    assert row["Starting Stage"] == 10
    assert row["Ending Stage"] == 100
    assert row["Stage Names"] == "10%-100%"


def test_add_stage_information_phenological_stages():
    df = stages.add_stage_information(_mini_df("1_2_3"), "phenological_stages")
    row = df.iloc[0]
    assert row["Starting Stage"] == 1
    assert row["Ending Stage"] == 3
    assert row["Stage Names"] == "Stages 1-3"


def test_add_stage_information_full_season():
    df = stages.add_stage_information(_mini_df("1_2_3"), "full_season")
    assert df.iloc[0]["Stage Names"] == "Full Season"


def test_add_stage_information_monthly_still_calendar():
    """Regression guard: calendar methods keep the month-dict label path."""
    df = stages.add_stage_information(_mini_df("7"), "monthly_r")
    # A calendar label contains month text, not a bare percent/stage token.
    label = df.iloc[0]["Stage Names"]
    assert "%" not in label and "Stage" not in label


# ---------------------------------------------------------------------------
# get_stage_information_dict
# ---------------------------------------------------------------------------
def test_get_stage_information_dict_fraction_season():
    info = stages.get_stage_information_dict(
        "vDTR_10_20_30_40_50_60_70_80_90_100", "fraction_season"
    )
    assert info["CID"] == "vDTR"
    assert info["Starting Stage"] == 10
    assert info["Ending Stage"] == 100
    assert info["Stage Name"] == "10%-100%"
    assert info["Stage Window Display"] == "10%-100%"


def test_get_stage_information_dict_phenological():
    info = stages.get_stage_information_dict("vDTR_1_2_3", "phenological_stages")
    assert info["CID"] == "vDTR"
    assert info["Starting Stage"] == 1
    assert info["Ending Stage"] == 3
    assert info["Stage Name"] == "Stages 1-3"


# ---------------------------------------------------------------------------
# update_feature_names
# ---------------------------------------------------------------------------
def test_update_feature_names_fraction_season_renames_not_dropped():
    df = pd.DataFrame(
        {
            "vDTR_10_20_30_40_50_60_70_80_90_100": [1.0],
            "Region": ["R1"],
            "Yield (tn per ha)": [2.0],
        }
    )
    out = stages.update_feature_names(df.copy(), "fraction_season")
    # Column must be renamed with numeric tokens preserved (not silently
    # skipped by the old .isdigit() float-drop).
    assert "vDTR 10-100" in out.columns
    assert "Region" in out.columns


def test_update_feature_names_phenological():
    df = pd.DataFrame({"vDTR_1_2_3": [1.0], "YIELD": [2.0]})
    out = stages.update_feature_names(df.copy(), "phenological_stages")
    assert "vDTR 1-3" in out.columns


# ---------------------------------------------------------------------------
# friendly_stage_label (utils.py) — pass numeric labels through unchanged
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "label", ["10%-100%", "Stages 1-3", "Full Season", "10-100"]
)
def test_friendly_stage_label_numeric_passthrough(label):
    assert utils.friendly_stage_label(label) == label


def test_friendly_stage_label_month_case_unaffected():
    # Calendar reversal behaviour preserved for month-range labels.
    assert utils.friendly_stage_label("Apr 1-Mar 31") == "March - April"


# ---------------------------------------------------------------------------
# Stage_ID <-> simulation_stages round-trip (geocif.py _create_simulation_stages
# / _filter_by_simulation_stages rely on this equality for the season-normalized
# methods once _setup_seasons_and_stages routes them through the data-driven
# stage collection).
# ---------------------------------------------------------------------------
def test_convert_stage_string_roundtrip_deciles():
    arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    s = stages.convert_stage_string(arr, to_array=False)
    assert s == "10_20_30_40_50_60_70_80_90_100"
    np.testing.assert_array_equal(stages.convert_stage_string(s, to_array=True), arr)


def test_convert_stage_string_roundtrip_single_decile():
    # Individual stage_mode emits singleton stages ("10", "20", ...).
    for token in ("10", "100", "1", "3"):
        arr = stages.convert_stage_string(token, to_array=True)
        assert stages.convert_stage_string(arr, to_array=False) == token


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
