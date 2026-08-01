"""Regression tests for the custom numpy CID indices DD and KDD.

DD  = number of dry days (pr < 1 mm), complement of RR1, distinct from CDD.
KDD = killing degree days, sum of daily Tmax excess above 32 C.

Both are computed directly with numpy (indices._cid_dry_days /
_cid_killing_degree_days); compute_indices short-circuits to
_compute_numpy_index for them (no icclim). The definitions test needs no
icclim; the indices tests skip where icclim isn't installed (importing
indices pulls icclim at module top).
"""
import pytest

from geocif.cid import definitions as di


def test_dd_kdd_in_definitions():
    assert di.dict_indices["DD"][0] == "Drought"
    assert "dry" in di.dict_indices["DD"][1].lower()
    assert di.dict_indices["KDD"][0] == "Heat"
    assert "killing" in di.dict_indices["KDD"][1].lower()


def test_dd_reducer_counts_dry_days():
    pytest.importorskip("icclim")
    import pandas as pd
    from geocif.cid import indices as ix
    # 300 dry (0 mm) + 65 wet (5 mm) -> 300 dry days
    assert ix._cid_dry_days(pd.Series([0.0] * 300 + [5.0] * 65)) == 300.0
    # strict < 1 mm: 0.5 is dry, exactly 1.0 is not
    assert ix._cid_dry_days(pd.Series([0.5, 1.0, 2.0])) == 1.0


def test_kdd_reducer_sums_excess_over_32():
    pytest.importorskip("icclim")
    import pandas as pd
    from geocif.cid import indices as ix
    assert ix.KDD_THRESHOLD_C == 32.0
    # 10 days at 35 C (excess 3 each) + 20 at 30 C -> 30
    assert ix._cid_killing_degree_days(pd.Series([35.0] * 10 + [30.0] * 20)) == 30.0
    # exactly at threshold contributes 0; 33 -> 1
    assert ix._cid_killing_degree_days(pd.Series([32.0, 33.0])) == 1.0


def test_compute_indices_routes_dd_kdd_to_numpy():
    pytest.importorskip("icclim")
    import pandas as pd
    from geocif.cid import indices as ix
    t = pd.date_range("2010-01-01", periods=30, freq="D")
    df = pd.DataFrame({
        "lat": 0.0, "lon": 0.0, "time": t, "Season": 2010,
        "pr": [0.0] * 20 + [5.0] * 10,        # 20 dry days
        "tasmax": [35.0] * 10 + [30.0] * 20,  # KDD = 10 * 3 = 30
    })
    dd = ix.compute_indices(df, df, "DD")
    kdd = ix.compute_indices(df, df, "KDD")
    assert float(dd.to_dataframe().reset_index()["DD"].iloc[0]) == 20.0
    assert float(kdd.to_dataframe().reset_index()["KDD"].iloc[0]) == 30.0
