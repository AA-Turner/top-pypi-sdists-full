"""Regression: cubist must not abort prediction on predict-only regions.

Bug (2026-07-16, Malawi agmet_hvstat): the Python `cubist` package's C engine
aborts the entire predict batch when a *string* categorical column (Region)
holds a level that was absent from the fold's training rows — e.g. Malawi's 4
no-yield city districts (Blantyre/Lilongwe/Mzuzu/Zomba City) which have EO/CIDs
(so they're in the prediction set) but no HarvestStat maize yield (so they're
never in training):

    cubist.exceptions.CubistError:
        *** line 3 of `undefined.cases':
            bad value of `Blantyre City' for attribute `Region'
        Error limit exceeded

catboost/tabpfn tolerate unseen levels; cubist does not. Fix: the cubist branch
in trainers.auto_train wraps Cubist so predict rows with an unseen non-numeric
categorical level get NaN (region ignored for prediction) instead of crashing.
Numeric columns (Harvest Year, numeric Region_ID) are excluded from the check —
cubist treats them as continuous, so the LOOCV held-out year never trips it.

Structural test (the guard is a local class inside auto_train, not importable),
plus a standalone check of the level-filter logic the guard implements.
"""
import pathlib
import numpy as np
import pandas as pd

TRAINERS = pathlib.Path(__file__).resolve().parents[1] / "geocif" / "ml" / "trainers.py"


def test_cubist_unseen_safe_guard_present():
    t = TRAINERS.read_text(encoding="utf-8")
    # cubist branch must wrap Cubist with the unseen-level guard
    assert "_CubistUnseenSafe" in t, "cubist unseen-level guard removed"
    assert "model = _CubistUnseenSafe(" in t, "cubist no longer uses the guard wrapper"
    # predict must NaN-fill rather than feed unseen-level rows to the C engine
    assert "np.full(len(X), np.nan" in t
    # numeric columns (e.g. Harvest Year) must be excluded from the level check
    assert "_is_numeric" in t


def test_level_filter_logic():
    """Mirror the guard's fit/predict level logic to lock in its behavior:
    unseen *string* levels are filtered (NaN), numeric year levels are not."""
    def is_numeric(s):
        return pd.to_numeric(s, errors="coerce").notna().all()

    X_train = pd.DataFrame({
        "Region": ["dedza", "dowa", "kasungu"],
        "Harvest Year": [2015, 2016, 2017],
        "ndvi": [0.4, 0.5, 0.6],
    })
    # record non-numeric categorical levels seen at fit. is_string_dtype
    # catches pandas<3 object AND pandas>=3 str (mirrors the guard fix —
    # `dtype == object` misses string columns under pandas 3).
    levels = {}
    for c in X_train.columns:
        s = X_train[c].astype(str)
        if pd.api.types.is_string_dtype(X_train[c]) and not is_numeric(s):
            levels[c] = set(s.unique())
    assert "Region" in levels          # string categorical tracked
    assert "Harvest Year" not in levels  # numeric year NOT tracked

    # predict frame includes a predict-only region + an unseen (held-out) year
    X_test = pd.DataFrame({
        "Region": ["dedza", "blantyre city"],   # 2nd = zero-training region
        "Harvest Year": [2026, 2026],            # unseen year — must be ignored
        "ndvi": [0.45, 0.30],
    })
    keep = pd.Series(True, index=X_test.index)
    for c, lv in levels.items():
        if c in X_test.columns:
            keep &= X_test[c].astype(str).isin(lv)
    assert keep.tolist() == [True, False]  # only the unseen-Region row dropped

    out = np.full(len(X_test), np.nan, dtype=float)
    out[keep.to_numpy()] = [1.23]  # stand-in for the C-engine prediction
    assert not np.isnan(out[0]) and np.isnan(out[1])
