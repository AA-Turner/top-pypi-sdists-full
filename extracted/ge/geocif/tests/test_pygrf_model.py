"""Regression tests for the PyGRF (Geographical Random Forest) model wiring.

PyGRF (geoai-lab) is a selectable pipeline model (model='pygrf') via the
sklearn-style PyGRFRegressor wrapper: coords are popped from the lat/lon
feature columns, PyGRF's DataFrame/Series/3-tuple API quirks are absorbed,
band_width defaults to an adaptive heuristic and local_weight to the global
Moran's I of y. Routed through the tree flags (_setup_tree_flags) and
DefaultFitter. PyGRF is a core dep (pure-Python sdist on PyPI).
"""
import inspect
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from geocif.ml.trainers import PyGRFRegressor, auto_train

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def _spatial_frame(n=60, seed=0):
    """Synthetic frame with a spatially varying signal + a categorical."""
    rng = np.random.default_rng(seed)
    lon = rng.uniform(34.0, 42.0, n)
    lat = rng.uniform(-4.0, 4.0, n)
    a = rng.normal(size=n)
    b = rng.normal(size=n)
    region = np.where(lon > 38.0, "east", "west")
    # coefficient on `a` varies with longitude -> spatial non-stationarity
    y = (1.0 + 0.5 * (lon - 38.0)) * a + 0.3 * b + rng.normal(scale=0.1, size=n)
    X = pd.DataFrame({
        "a": a, "b": b, "lat": lat, "lon": lon,
        "Region": pd.Categorical(region),
    })
    return X, pd.Series(y)


def test_pygrf_sklearn_api():
    m = PyGRFRegressor(band_width=10, local_weight=0.4, n_estimators=25)
    assert hasattr(m, "fit") and hasattr(m, "predict")
    p = m.get_params()
    assert p["band_width"] == 10 and p["local_weight"] == 0.4
    m.set_params(local_weight=0.2)
    assert m.get_params()["local_weight"] == 0.2


def test_pygrf_requires_lat_lon():
    m = PyGRFRegressor()
    X = pd.DataFrame({"a": [1.0, 2, 3]})
    with pytest.raises(ValueError, match="include_lat_lon_as_feature"):
        m.fit(X, [1.0, 2.0, 3.0])


def test_pygrf_split_pops_coords_and_encodes():
    m = PyGRFRegressor()
    X, y = _spatial_frame(n=20)
    X.loc[X.index[:2], "lat"] = np.nan  # regions missing from centroid merge
    feats, coords = m._split(X, fit=True)
    assert "lat" not in feats.columns and "lon" not in feats.columns
    assert "Region_east" in feats.columns and "Region_west" in feats.columns
    assert coords.shape == (20, 2)
    assert np.all(np.isfinite(coords))  # NaN coords imputed with train mean


def test_pygrf_projection_is_metric():
    """1 degree of longitude at the equator ~ 111 km; at 60N ~ 55.7 km."""
    m = PyGRFRegressor()
    m._lat0 = 0.0
    d_eq = np.diff(m._project([[0.0, 0.0], [1.0, 0.0]])[:, 0])[0]
    m._lat0 = 60.0
    d_60 = np.diff(m._project([[0.0, 60.0], [1.0, 60.0]])[:, 0])[0]
    assert d_eq == pytest.approx(111.32, abs=0.01)
    assert d_60 == pytest.approx(111.32 / 2, rel=0.01)


def test_pygrf_fit_predict_roundtrip():
    pytest.importorskip("PyGRF")
    X, y = _spatial_frame(n=60)
    m = PyGRFRegressor(n_estimators=20, seed=0).fit(X, y)
    # heuristic bandwidth: max(round(0.15*60)=9, 20) = 20, and Moran's I in [0,1]
    assert m.band_width_ == 20
    assert 0.0 <= m.local_weight_ <= 1.0
    pred = m.predict(X)
    assert pred.shape == (60,)
    assert np.all(np.isfinite(pred))
    assert np.corrcoef(pred, y)[0, 1] > 0.8
    # unseen categorical level at predict must not crash (one-hot reindex)
    X_new = X.head(5).copy()
    X_new["Region"] = "north"
    assert np.all(np.isfinite(m.predict(X_new)))


def test_pygrf_explicit_band_width_clamped():
    pytest.importorskip("PyGRF")
    X, y = _spatial_frame(n=25)
    m = PyGRFRegressor(band_width=500, local_weight=0.3, n_estimators=10)
    m.fit(X, y)
    assert m.band_width_ == 24  # clamped to n - 1


def _panel_frame(n_regions, n_years, seed=0):
    """geocif-shaped panel: per-region centroids REPEATED for every year —
    the exact duplicate-coordinate shape _add_lat_lon_to_data produces."""
    rng = np.random.default_rng(seed)
    lon_r = rng.uniform(34.0, 42.0, n_regions)
    lat_r = rng.uniform(-4.0, 4.0, n_regions)
    rows = []
    for r in range(n_regions):
        for yr in range(n_years):
            a = rng.normal()
            rows.append({
                "a": a, "b": rng.normal(),
                "lat": lat_r[r], "lon": lon_r[r],
                "Region": f"region_{r}",
                "_y": (1.0 + 0.1 * r) * a + rng.normal(scale=0.1),
            })
    df = pd.DataFrame(rows)
    y = df.pop("_y")
    df["Region"] = pd.Categorical(df["Region"])
    return df, y


def test_pygrf_duplicate_centroids_pooled():
    """Review finding (critical): >= band_width rows sharing one centroid
    made PyGRF's adaptive bandwidth 0 -> 0/0 NaN sample weights -> sklearn
    ValueError. 5 regions x 25 years with default bw=20 <= 25 rows/region
    hits it; the ~1 mm jitter must keep fit+predict finite."""
    pytest.importorskip("PyGRF")
    X, y = _panel_frame(n_regions=5, n_years=25)
    m = PyGRFRegressor(n_estimators=10, seed=0).fit(X, y)
    pred = m.predict(X.head(10))
    assert np.all(np.isfinite(pred))


def test_pygrf_single_region_identical_coords():
    """'individual' cluster strategy: ALL rows share one centroid."""
    pytest.importorskip("PyGRF")
    X, y = _panel_frame(n_regions=1, n_years=20)
    m = PyGRFRegressor(n_estimators=10, seed=0).fit(X, y)
    pred = m.predict(X.head(5))
    assert np.all(np.isfinite(pred))


def test_pygrf_band_width_floor_two():
    """band_width=1 crashes PyGRF even with unique coords (train bandwidth
    becomes the 0 self-distance) — must be clamped to 2."""
    pytest.importorskip("PyGRF")
    X, y = _spatial_frame(n=15)
    m = PyGRFRegressor(band_width=1, local_weight=0.3, n_estimators=10)
    m.fit(X, y)
    assert m.band_width_ == 2
    assert np.all(np.isfinite(m.predict(X.head(3))))


def test_pygrf_fixed_kernel_semantics():
    """kernel='fixed': band_width is a radius in km — no count clamp; and
    it must be explicit (the 15%-of-n heuristic has no distance meaning)."""
    pytest.importorskip("PyGRF")
    X, y = _spatial_frame(n=30)
    with pytest.raises(ValueError, match="radius in km"):
        PyGRFRegressor(kernel="fixed").fit(X, y)
    # generous radius (degrees span ~8 deg lon x 8 deg lat -> < 2000 km)
    m = PyGRFRegressor(kernel="fixed", band_width=2000.0, local_weight=0.3,
                       n_estimators=10, seed=0).fit(X, y)
    assert m.band_width_ == 2000.0  # NOT clamped to n-1
    assert np.all(np.isfinite(m.predict(X.head(5))))


def test_latlon_survives_correlation_selection_fallback():
    """Production bug (usa_admin1, 0.4.931): when correlation-selection is
    empty, _create_feature_names_for_region bypasses create_feature_names,
    so feature_names lost lat/lon while apply_feature_selector still
    force-appended them -> df_region never carried the columns ->
    _prepare_training_data raised KeyError for all 2555 folds.

    Both sides must now agree: the fallback appends lat/lon (when present)
    and the force-append is guarded on presence in df_train.
    """
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    fallback = src.split("correlation-selection empty")[0]
    tail = fallback[-1200:]
    assert "self.feature_names = self.get_cid_column_names(self.df_train)" in tail
    assert "if self.include_lat_lon_as_feature:" in tail, (
        "fallback branch must still append lat/lon"
    )
    # force-append guarded on actual presence in the frame
    assert '_c in self.df_train.columns' in src
    # and the silent-degradation guard exists
    assert "_warn_if_coords_degenerate" in src
    assert "spatial component is inert" in src


def test_auto_train_pygrf_branch():
    assert "pygrf_params" in inspect.signature(auto_train).parameters
    src = inspect.getsource(auto_train)
    assert 'model_name == "pygrf"' in src


def test_geocif_wiring_for_pygrf():
    src = (ROOT / "geocif.py").read_text(encoding="utf-8")
    assert '"ydf", "pygrf"]' in src  # tree flags (no CI, no XAI)
    assert "self.pygrf_params" in src
    assert "pygrf_band_width" in src and "pygrf_local_weight" in src
    assert 'pygrf_params=getattr(self.obj, "pygrf_params"' in src
    # fail-fast: missing include_lat_lon_as_feature must raise at setup,
    # not be swallowed per-region by loop_ml (review finding). Matched on the
    # guard's shape rather than the exact tuple literal -- the set of
    # centroid-consuming models grows (tabfm_gsa joined pygrf/tabpfn_gsa), and
    # a literal match turns every such addition into a spurious failure here.
    assert 'self.dispatch_name in ("pygrf", "tabpfn_gsa"' in src
    assert "and not self.include_lat_lon_as_feature" in src
    assert "include_lat_lon_as_feature = True — region" in src
    # max_features accepts sklearn strings, band_width parses as float
    assert "_cast_max_features" in src
    assert '("pygrf_band_width", self.parser.getfloat)' in src
