"""Regression test for the `monthly_only_features` filter
(`geocif.ml.stages.select_single_calendar_period_features`).

Keeps only single-calendar-month CID features (all trailing stage tokens
equal), dropping multi-month cumulative spans and Pre-/In-Season aggregates,
while preserving non-CID columns (target, Production, Season, Area, cat, lag).

Operates PRE-rename on raw ``_``-token names, so the monthly_r calendar
wraparound (e.g. Jan+Dec = tokens 1_12 = a 2-month span) is judged by token
uniqueness, not by calendar-month arithmetic — which is the correct, robust
behaviour and the main thing this test locks down.
"""
import pandas as pd

from geocif.ml.stages import (
    select_single_calendar_period_features as filt,
    select_monthly_plus_fullseason_features as filt_mpf,
)


def _kept(cols):
    df = pd.DataFrame({c: [1.0, 2.0] for c in cols})
    return set(filt(df).columns)


def _kept_mpf(cols):
    df = pd.DataFrame({c: [1.0, 2.0] for c in cols})
    return set(filt_mpf(df).columns)


class TestMonthlyOnlyFilter:
    def test_keeps_single_calendar_month(self):
        cols = ["PRCPTOT_7", "TG90p_7", "TG90p_7_7", "vDTR_10"]
        assert _kept(cols) == set(cols)

    def test_keeps_digit_in_name_cids(self):
        # name-digits (10mm, 99p, 5cm, 90p) must NOT be read as stage tokens
        cols = ["R10mm_7", "R99pTOT_12", "SD5cm_7", "TN90p_3"]
        assert _kept(cols) == set(cols)

    def test_drops_multimonth_cumulative_spans(self):
        cols = ["PRCPTOT_7_6", "TG90p_7_6_5", "R99pTOT_7_6", "CDD_4_3_2_1"]
        assert _kept(cols) == set()

    def test_drops_wraparound_two_month_span(self):
        # Jan(1)+Dec(12): tokens differ -> 2-month span -> DROP (not a single month)
        assert _kept(["vDTR_1_12"]) == set()

    def test_drops_preseason_inseason_aggregates(self):
        cols = ["SoilMoist_PS_4", "SoilMoist_IS_3", "Foo_PS", "Bar_IS"]
        assert _kept(cols) == set()

    def test_keeps_static_and_forecast_whitelist(self):
        cols = ["AEF_5", "MEAN_FLDAS_SoilMoist_tavg_LEAD1"]
        assert _kept(cols) == set(cols)

    def test_preserves_non_cid_metadata_and_target(self):
        # critical: filter must not drop bookkeeping/target/cat/lag columns
        cols = ["Yield (tn per ha)", "Production (tn)", "Season", "Area (ha)",
                "Harvest Year", "Region", "Region_ID", "t -1 Yield (tn per ha)"]
        assert _kept(cols) == set(cols)

    def test_mixed_frame_keep_and_drop(self):
        keep = ["PRCPTOT_7", "AEF_5", "Yield (tn per ha)", "Production (tn)"]
        drop = ["PRCPTOT_7_6", "SoilMoist_PS_4", "vDTR_1_12"]
        assert _kept(keep + drop) == set(keep)


class TestMonthlyPlusFullseason:
    def test_keeps_single_and_fullseason_drops_intermediate(self):
        # full season = longest chain = 6 stages
        cols = ["PRCPTOT_7", "PRCPTOT_7_6", "PRCPTOT_7_6_5",
                "PRCPTOT_7_6_5_4", "PRCPTOT_7_6_5_4_3", "PRCPTOT_7_6_5_4_3_2"]
        kept = _kept_mpf(cols)
        assert "PRCPTOT_7" in kept                    # single month
        assert "PRCPTOT_7_6_5_4_3_2" in kept          # full season (max chain)
        assert "PRCPTOT_7_6" not in kept              # intermediate dropped
        assert "PRCPTOT_7_6_5" not in kept
        assert "PRCPTOT_7_6_5_4" not in kept
        assert "PRCPTOT_7_6_5_4_3" not in kept

    def test_preserves_metadata_static_drops_psis(self):
        cols = ["CID_5", "CID_5_4_3", "CID_5_4_3_2_1", "Yield (tn per ha)",
                "Production (tn)", "Season", "AEF_5", "Region", "X_PS_4"]
        kept = _kept_mpf(cols)
        for m in ["Yield (tn per ha)", "Production (tn)", "Season", "AEF_5", "Region"]:
            assert m in kept
        assert "X_PS_4" not in kept
        assert "CID_5" in kept                         # single month
        assert "CID_5_4_3_2_1" in kept                 # full season (max chain 5)
        assert "CID_5_4_3" not in kept                 # intermediate dropped
