"""FPARGDD: FPAR 500 m area under the curve per growing degree day (base 10 C, cap 30 C)."""
import numpy as np
import pandas as pd
import pytest

from geocif.cid import definitions as di
from geocif.cid import indices


def _window(n_days=30, tmax=30.0, tmin=20.0, fpar=50.0):
    """A daily stage window with FPAR only on dekad starts (the merged-file layout)."""
    time = pd.date_range("2020-07-01", periods=n_days, freq="D")
    f = np.full(n_days, np.nan)
    f[::10] = fpar
    return pd.DataFrame({"time": time, "fpar_mo6": f, "tasmax": tmax, "tasmin": tmin})


def test_ratio_is_fpar_auc_over_gdd():
    # 3 dekad values of 50 -> trapezoid AUC 100; GDD = 30 days x ((30 + 20) / 2 - 10) = 450
    assert indices.fpar_auc_per_gdd(_window()) == pytest.approx(100 / 450)


def test_tmax_is_capped_and_tmin_floored():
    hot = indices.fpar_auc_per_gdd(_window(tmax=38.0, tmin=5.0))
    # clipped to (30 + 10) / 2 - 10 = 10 GDD per day -> 300 GDD
    assert hot == pytest.approx(100 / 300)


def test_warmer_window_gives_lower_ratio_for_same_canopy():
    cool = indices.fpar_auc_per_gdd(_window(tmax=26.0, tmin=14.0))
    warm = indices.fpar_auc_per_gdd(_window(tmax=32.0, tmin=22.0))
    assert warm < cool


@pytest.mark.parametrize("drop", ["fpar_mo6", "tasmax", "tasmin"])
def test_missing_input_is_nan(drop):
    assert np.isnan(indices.fpar_auc_per_gdd(_window().drop(columns=drop)))


def test_no_heat_or_no_fpar_is_nan():
    assert np.isnan(indices.fpar_auc_per_gdd(_window(tmax=9.0, tmin=2.0)))
    assert np.isnan(indices.fpar_auc_per_gdd(_window(fpar=np.nan)))
    assert np.isnan(indices.fpar_auc_per_gdd(_window().iloc[0:0]))


def test_definition_and_validation():
    assert di.dict_fpargdd == {"AUC_FPARGDD": [
        "FPARGDD", "FPAR 500 m area under the curve per growing degree day (base 10 C, cap 30 C)"]}
    indices.validate_index_definitions()


def test_compute_eo_indices_emits_one_row_per_window():
    obj = object.__new__(indices.CIDs)
    obj.crop, obj.season, obj.method, obj.harvest_year = "maize", 1, "monthly_r", 2020
    df = _window()
    df_region = pd.DataFrame({"Area": [1000.0]})
    out = obj.compute_eo_indices(df, df_region, "FPARGDD", ("united_states_of_america", "iowa"), [8, 7])
    assert len(out) == 1
    row = out.iloc[0]
    assert row["Index"] == "AUC_FPARGDD" and row["Type"] == "FPARGDD" and row["Stage"] == "8_7"
    assert row["CID"] == pytest.approx(100 / 450)
    assert row["Region"] == "Iowa" and row["Harvest Year"] == 2020
