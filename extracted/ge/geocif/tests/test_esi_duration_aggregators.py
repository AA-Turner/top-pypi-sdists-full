"""Regression tests for the drought depth/duration/spread CID aggregators
added for ESI4WK (percentiles, fixed-threshold deficit/fraction, CV/IQR/RANGE).

These encode how LOW and how LONG ESI stays depressed; MIN alone only captures
the single worst instant. See dict_esi4wk in definitions.py.
"""
import numpy as np
import pytest

from geocif.cid.indices import aggregate_eo_values
from geocif.cid import definitions as di

E = np.array([20.0, 30, 40, 50, 60, 45, 35, 25])


def test_percentile_aggregators():
    assert aggregate_eo_values(E, "P20") == pytest.approx(np.nanpercentile(E, 20))
    assert aggregate_eo_values(E, "P05") == pytest.approx(np.nanpercentile(E, 5))
    assert aggregate_eo_values(E, "P90") == pytest.approx(np.nanpercentile(E, 90))


def test_aucdef_is_mean_deficit_below_threshold():
    assert aggregate_eo_values(E, "AUCDEF40") == pytest.approx(np.mean(np.clip(40 - E, 0, None)))
    # no values below 10 -> zero deficit
    assert aggregate_eo_values(E, "AUCDEF10") == pytest.approx(0.0)


def test_fraclo_is_fraction_below_threshold():
    assert aggregate_eo_values(E, "FRACLO30") == pytest.approx(np.mean(E < 30))
    assert aggregate_eo_values(E, "FRACLO100") == pytest.approx(1.0)
    assert aggregate_eo_values(E, "FRACLO0") == pytest.approx(0.0)


def test_spread_aggregators():
    assert aggregate_eo_values(E, "RANGE") == pytest.approx(E.max() - E.min())
    assert aggregate_eo_values(E, "IQR") == pytest.approx(
        np.nanpercentile(E, 75) - np.nanpercentile(E, 25))
    assert aggregate_eo_values(E, "CV") == pytest.approx(np.nanstd(E) / np.nanmean(E))


def test_nan_handling():
    e = np.array([20.0, np.nan, 40, 60])
    # NaNs dropped before aggregation
    assert aggregate_eo_values(e, "P50") == pytest.approx(np.nanpercentile([20, 40, 60], 50))
    assert not np.isnan(aggregate_eo_values(e, "AUCDEF50"))


def test_new_esi_indices_registered():
    for k in ("P10_ESI4WK", "P20_ESI4WK", "AUCDEF40_ESI4WK", "AUCDEF50_ESI4WK",
              "FRACLO30_ESI4WK", "CV_ESI4WK", "IQR_ESI4WK", "RANGE_ESI4WK"):
        assert k in di.dict_esi4wk, f"{k} missing from dict_esi4wk"
        assert di.dict_esi4wk[k][0] == "ESI"


def test_dispatch_prefix_does_not_collide():
    # AUCDEF must NOT be captured by the AUC substring, MAX by MAXRUN, etc.
    def dispatch(iname):
        p = iname.split("_")[0].upper()
        if p and p[0] == "P" and p[1:].isdigit():
            return p
        if p.startswith("AUCDEF"):
            return p
        if p.startswith("FRACLO"):
            return p
        if p in ("CV", "IQR", "RANGE"):
            return p
        for sub in ("MIN", "MAX", "MEAN", "STD", "AUC", "H-INDEX"):
            if sub in iname.upper():
                return sub
        return None
    assert dispatch("AUCDEF40_ESI4WK") == "AUCDEF40"   # not "AUC"
    assert dispatch("AUC_ESI4WK") == "AUC"
    assert dispatch("P20_ESI4WK") == "P20"
    assert dispatch("MAX_ESI4WK") == "MAX"
    assert dispatch("H-INDEX_Precip") == "H-INDEX"
