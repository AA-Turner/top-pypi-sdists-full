"""MO6 FPAR as a CID family (FPAR = native ~500 m, FPAR5K = 0.05-degree aggregate).

geoprepare's FPAR_MO6 dataset writes the merged columns ``fpar_mo6`` and
``fpar_mo6_5km`` (DN 0-100, dekadal, interpolated to daily by geomerge).
cid/indices.py turns each into MEAN/MAX/MIN/STD/AUC stage indices with its
own category, so either resolution can be ablated with
``[ML] exclude_cid_categories``.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.cid import definitions as di
from geocif.cid import indices as ix
from geocif.ml import stages

GEOCIF_DIR = Path(__file__).resolve().parents[1] / "geocif"
FIVE = {"MEAN", "MAX", "MIN", "STD", "AUC"}


def _cids():
    obj = ix.CIDs.__new__(ix.CIDs)
    obj.country, obj.crop, obj.season = "united_states_of_america", "maize", 1
    obj.method, obj.harvest_year = "monthly_r", 2024
    return obj


def _window(values_500m, values_5km=None):
    t = pd.date_range("2024-06-01", periods=len(values_500m), freq="D")
    df = pd.DataFrame({"time": t, "Month": t.month, "fpar_mo6": values_500m})
    if values_5km is not None:
        df["fpar_mo6_5km"] = values_5km
    return df


def test_definitions_registered_with_distinct_categories():
    assert {k.split("_")[0] for k in di.dict_fpar} == FIVE
    assert {k.split("_")[0] for k in di.dict_fpar5k} == FIVE
    assert all(k.endswith("_FPAR") for k in di.dict_fpar)
    assert all(k.endswith("_FPAR5K") for k in di.dict_fpar5k)
    assert {v[0] for v in di.dict_fpar.values()} == {"FPAR"}
    assert {v[0] for v in di.dict_fpar5k.values()} == {"FPAR5K"}
    assert not set(di.dict_fpar) & set(di.dict_fpar5k)
    assert not (set(di.dict_fpar) | set(di.dict_fpar5k)) & set(di.dict_ndvi)


def test_categories_resolve_independently():
    cmap = stages.cid_category_map()
    assert cmap["MEAN_FPAR"] == "FPAR" and cmap["MEAN_FPAR5K"] == "FPAR5K"
    drop, unmatched = stages.resolve_excluded_cids([], ["FPAR"])
    assert set(drop) == set(di.dict_fpar) and unmatched == []
    drop5, _ = stages.resolve_excluded_cids([], ["fpar5k"])
    assert set(drop5) == set(di.dict_fpar5k)


def test_fpar_indices_computed_from_the_500m_column():
    obj = _cids()
    vals = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    out = obj.compute_eo_indices(_window(vals), pd.DataFrame({"Area": [1.0]}), "FPAR",
                                 ("united_states_of_america", "iowa"), [6], set())
    got = out.set_index("Index")["CID"]
    assert set(got.index) == set(di.dict_fpar)
    assert got["MEAN_FPAR"] == 30.0 and got["MAX_FPAR"] == 50.0 and got["MIN_FPAR"] == 10.0
    assert np.isclose(got["STD_FPAR"], np.std(vals))
    assert np.isclose(got["AUC_FPAR"], np.trapezoid(vals))
    assert (out["Type"] == "FPAR").all()


def test_fpar5k_reads_the_aggregate_column_not_the_native_one():
    obj = _cids()
    out = obj.compute_eo_indices(_window([10.0] * 5, [70.0] * 5), pd.DataFrame({"Area": [1.0]}),
                                 "FPAR5K", ("united_states_of_america", "iowa"), [6], set())
    got = out.set_index("Index")["CID"]
    assert set(got.index) == set(di.dict_fpar5k)
    assert got["MEAN_FPAR5K"] == 70.0


def test_missing_column_emits_nothing():
    obj = _cids()
    out = obj.compute_eo_indices(_window([10.0] * 5), pd.DataFrame({"Area": [1.0]}), "FPAR5K",
                                 ("united_states_of_america", "iowa"), [6], set())
    assert out.empty


def test_eo_vars_are_gated_on_the_merged_columns():
    src = (GEOCIF_DIR / "cid" / "indices.py").read_text(encoding="utf-8")
    assert 'if "fpar_mo6" in df_group.columns:' in src
    assert 'if "fpar_mo6_5km" in df_group.columns:' in src
    i5, i = src.index('iname.endswith("_FPAR5K")'), src.index('iname.endswith("_FPAR")')
    assert i5 < i, "_FPAR5K must be tested before _FPAR, which is its suffix"
