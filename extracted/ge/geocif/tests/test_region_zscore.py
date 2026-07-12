"""Regression tests for region z-score features: the ['all'] sentinel and the
region_zscore_replace_raw (z-score-only) flag.

['all'] must resolve to time-varying CID bases only — excluding static
embeddings (AEF / soilgrids), categorical columns, and yield-derived features —
so it generalizes to countries/crops without a hand-curated CID list.
"""
import logging
from types import MethodType, SimpleNamespace

import numpy as np
import pandas as pd

from geocif.geocif import Geocif


def _df_train():
    return pd.DataFrame({
        "Region": ["A", "A", "A", "A", "B", "B", "B", "B"],
        "Region_ID": [1, 1, 1, 1, 1, 1, 1, 1],
        "Harvest Year": [2001, 2002, 2003, 2004, 2001, 2002, 2003, 2004],
        "Season": [1] * 8,                        # bookkeeping -> exclude
        "TG90p Jan 1-Jan 31": [10.0, 12, 11, 13, 20, 22, 21, 23],
        "AEF_1": [0.5] * 8,                       # static embedding -> exclude
        "sand_0-5cm": [30.0] * 8,                 # soilgrids -> exclude
        "Area (ha)": [100.0, 110, 120, 130, 200, 210, 220, 230],  # size -> exclude
        "Production (tn)": [310.0, 352, 396, 442, 820, 882, 946, 1012],  # target proxy!
        "t -1 Yield (tn per ha)": [3, 3.1, 3.2, 3.3, 4, 4.1, 4.2, 4.3],  # yield-derived
        "Yield (tn per ha)": [3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4],   # target
    })


def _df_test():
    return pd.DataFrame({
        "Region": ["A", "B"], "Region_ID": [1, 1], "Harvest Year": [2005, 2005],
        "Season": [1, 1], "TG90p Jan 1-Jan 31": [14.0, 24.0], "AEF_1": [0.5, 0.5],
        "sand_0-5cm": [30.0, 30.0], "Area (ha)": [140.0, 240.0],
        "Production (tn)": [490.0, 1080.0],
        "t -1 Yield (tn per ha)": [3.4, 4.4], "Yield (tn per ha)": [3.5, 4.5],
    })


def _stub(replace_raw, cids):
    stub = SimpleNamespace(
        df_train=_df_train(), df_test=_df_test(),
        region_zscore_cids=cids,
        region_zscore_replace_raw=replace_raw,
        cat_features=["Harvest Year", "Region_ID", "Region"],
        target="Yield (tn per ha)",
        countries_pooled=None,
        logger=logging.getLogger("test_region_zscore"),
    )
    stub._all_zscore_bases = MethodType(Geocif._all_zscore_bases, stub)
    stub._compute_region_zscore_features = MethodType(
        Geocif._compute_region_zscore_features, stub)
    return stub


class TestRegionZscore:
    def test_all_resolves_to_climate_cids_only(self):
        stub = _stub(False, ["all"])
        bases = stub._all_zscore_bases()
        assert bases == ["TG90p"], bases  # AEF/soil/cat/yield all excluded

    def test_all_keeps_raw_and_adds_zreg_by_default(self):
        stub = _stub(False, ["all"])
        stub._compute_region_zscore_features()
        cols = stub.df_test.columns
        assert "TG90p Jan 1-Jan 31" in cols          # raw kept
        assert "TG90p_zreg Jan 1-Jan 31" in cols      # zreg added
        assert "AEF_1_zreg" not in cols               # static not z-scored
        z = stub.df_test.loc[stub.df_test["Region"] == "A", "TG90p_zreg Jan 1-Jan 31"].iloc[0]
        assert np.isfinite(z) and 1.0 < z < 3.0       # (14-11.5)/1.29 ~= 1.94

    def test_replace_raw_drops_raw_keeps_zreg(self):
        stub = _stub(True, ["all"])
        stub._compute_region_zscore_features()
        cols = stub.df_test.columns
        assert "TG90p_zreg Jan 1-Jan 31" in cols      # zreg added
        assert "TG90p Jan 1-Jan 31" not in cols       # raw dropped (z-only)
        assert "TG90p Jan 1-Jan 31" not in stub.df_train.columns

    def test_curated_list_still_works(self):
        stub = _stub(False, ["TG90p"])
        stub._compute_region_zscore_features()
        assert "TG90p_zreg Jan 1-Jan 31" in stub.df_test.columns
        assert "TG90p Jan 1-Jan 31" in stub.df_test.columns

    def test_leakage_columns_never_zscored(self):
        """Production (= yield x area) and yield/area/season bookkeeping must
        never be z-scored under 'all' — they are target proxies (leakage)."""
        bases = _stub(False, ["all"])._all_zscore_bases()
        for bad in ("Production (tn)", "Season", "Area (ha)", "Yield (tn per ha)",
                    "t -1 Yield (tn per ha)"):
            assert bad not in bases, bad
        # and no *_zreg sibling is created for them, in either mode
        for rr in (False, True):
            stub = _stub(rr, ["all"])
            stub._compute_region_zscore_features()
            cols = list(stub.df_train.columns) + list(stub.df_test.columns)
            assert not any("Production" in c and "_zreg" in c for c in cols)
            assert "Production (tn)" in stub.df_test.columns  # never dropped
