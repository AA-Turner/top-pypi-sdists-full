"""Regression tests for the BASS (Bayesian MARS) model wiring.

BASS is a selectable pipeline model (model='bass') via a sklearn-style
BassRegressor wrapper around pyBASS, routed through DefaultFitter. HPs are
config-driven via [ML] bass_* (tuned poppy defaults max_int=1, npart=15).
pyBASS is a git-only optional dep, so these tests avoid importing it.
"""
import ast
import inspect
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.ml.trainers import BassRegressor, auto_train

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def test_bassregressor_sklearn_api():
    m = BassRegressor(max_int=1, npart=15)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["max_int"] == 1 and p["npart"] == 15
    m.set_params(max_int=2)
    assert m.get_params()["max_int"] == 2


def test_bassregressor_encodes_categoricals():
    m = BassRegressor()
    X = pd.DataFrame({"a": [1.0, 2, 3],
                      "Region": pd.Categorical(["x", "y", "x"]),
                      "b": [np.nan, 5, 6]})
    Xn = m._numeric(X)
    # object/category one-hot encoded, numerics preserved
    assert "Region_x" in Xn.columns and "Region_y" in Xn.columns
    assert "a" in Xn.columns and "b" in Xn.columns
    assert Xn.select_dtypes(include=["object", "category"]).shape[1] == 0


def test_auto_train_accepts_bass_params():
    assert "bass_params" in inspect.signature(auto_train).parameters, \
        "auto_train must accept bass_params"
    src = inspect.getsource(auto_train)
    assert 'model_name == "bass"' in src, "auto_train must have a bass model branch"


def test_geocif_parses_bass_params():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    assert "self.bass_params" in src
    assert "bass_max_int" in src and "bass_npart" in src
    assert 'bass_params=getattr(self.obj, "bass_params"' in src
