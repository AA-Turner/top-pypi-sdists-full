"""Tests for the shapiq / NumPy>=2.3 compatibility shim in ml/xai_shapiq.

The failure this guards against was fully silent: NumPy 2.3 removed the
size-1-array -> float coercion, shapiq<=1.4's TabPFNImputer.value_function
does ``float(self.predict(...))`` per coalition, so every ``explain()``
raised, the per-sample except blocks logged-and-continued, and the run
produced beeswarm/waterfall/feature-importance built on an all-zeros SHAP
matrix while exiting rc=0 (observed 2026-09-08: 636 swallowed failures,
"valid-looking" plots of nothing).
"""

import sys
import types

import numpy as np
import pytest

from geocif.ml import xai_shapiq as xs


# ------------------------------------------------------------- _as_scalar
@pytest.mark.parametrize(
    "value,expected",
    [
        (1.5, 1.5),
        (np.float64(2.5), 2.5),
        (np.array(3.0), 3.0),               # 0-d array
        (np.array([4.5]), 4.5),             # THE case float() rejects
        (np.array([[5.0]]), 5.0),           # (1,1) from a predict()
        ([6.0], 6.0),
    ],
)
def test_as_scalar_accepts_scalar_likes(value, expected):
    assert xs._as_scalar(value) == expected


def test_as_scalar_rejects_multi_element():
    """A genuinely non-scalar value must raise, not quietly take arr[0]."""
    with pytest.raises(ValueError, match="size 2"):
        xs._as_scalar(np.array([1.0, 2.0]))


def test_coercion_probe_matches_numpy_behavior():
    """The probe must report exactly what this NumPy does, warning-free."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")         # a leaked warning = failure
        probed = xs._numpy_dropped_size1_coercion()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        try:
            float(np.ones(1))
            actual = False
        except TypeError:
            actual = True
    assert probed is actual


# ------------------------------------------- _ensure_shapiq_numpy2_compat
def _fake_shapiq(monkeypatch):
    """Install a minimal fake shapiq.imputer.tabpfn_imputer whose
    value_function reproduces the upstream bug, so the shim's behavior is
    testable without shapiq (and without a 200 MB TabPFN download)."""

    class TabPFNImputer:
        def value_function(self, coalitions):  # pragma: no cover - replaced
            return float(np.ones(1))           # the upstream bug

    mod = types.ModuleType("shapiq.imputer.tabpfn_imputer")
    mod.TabPFNImputer = TabPFNImputer
    imputer_pkg = types.ModuleType("shapiq.imputer")
    imputer_pkg.tabpfn_imputer = mod
    shapiq_pkg = types.ModuleType("shapiq")
    shapiq_pkg.imputer = imputer_pkg
    monkeypatch.setitem(sys.modules, "shapiq", shapiq_pkg)
    monkeypatch.setitem(sys.modules, "shapiq.imputer", imputer_pkg)
    monkeypatch.setitem(sys.modules, "shapiq.imputer.tabpfn_imputer", mod)
    return TabPFNImputer


class _StubModel:
    """Records fit calls; predict returns a size-1 array like TabPFN.
    ``raise_on_fit`` marks fit-call indices that raise TabPFN's
    constant-features error."""

    def __init__(self, values, raise_on_fit=()):
        self._values = list(values)
        self._i = 0
        self.fit_calls = []
        self._raise_on_fit = set(raise_on_fit)

    def fit(self, X, y):
        idx = len(self.fit_calls)
        self.fit_calls.append(np.asarray(X).shape)
        if idx in self._raise_on_fit:
            raise ValueError(
                "All features are constant and would have been removed! "
                "Unable to predict using TabPFN."
            )

    def predict(self, X):
        v = self._values[min(self._i, len(self._values) - 1)]
        self._i += 1
        return np.array([v])                   # the size-1 array


def test_shim_patches_fake_shapiq(monkeypatch):
    monkeypatch.setattr(xs, "_numpy_dropped_size1_coercion", lambda: True)
    cls = _fake_shapiq(monkeypatch)
    xs._ensure_shapiq_numpy2_compat()
    assert getattr(cls.value_function, "_np2_patched", False), (
        "value_function was not replaced"
    )

    # and the replacement actually computes on size-1-array predictions
    imp = cls.__new__(cls)
    imp.x_train = np.arange(12.0).reshape(4, 3)
    imp.y_train = np.arange(4.0)
    imp.x = np.array([[9.0, 9.0, 9.0]])
    imp.empty_prediction = np.array([7.0])     # size-1 array here too
    imp.model = _StubModel([1.5, 2.5])
    imp.predict = imp.model.predict

    coalitions = np.array([
        [False, False, False],                 # empty -> empty_prediction
        [True, False, True],
        [True, True, True],
    ])
    out = cls.value_function(imp, coalitions)
    assert out.tolist() == [7.0, 1.5, 2.5]
    # final refit on the FULL training matrix (the original's contract)
    assert imp.model.fit_calls[-1] == (4, 3)


def test_constant_coalition_falls_back_to_empty_prediction(monkeypatch):
    """A coalition of only-constant features makes TabPFN raise; the patched
    value_function must substitute empty_prediction for THAT coalition and
    keep going, not lose the whole sample."""
    monkeypatch.setattr(xs, "_numpy_dropped_size1_coercion", lambda: True)
    cls = _fake_shapiq(monkeypatch)
    xs._ensure_shapiq_numpy2_compat()

    imp = cls.__new__(cls)
    imp.x_train = np.arange(12.0).reshape(4, 3)
    imp.y_train = np.arange(4.0)
    imp.x = np.array([[9.0, 9.0, 9.0]])
    imp.empty_prediction = np.array([7.0])
    # fit call 0 (first coalition) raises the constant-features error
    imp.model = _StubModel([1.5], raise_on_fit=(0,))
    imp.predict = imp.model.predict

    coalitions = np.array([
        [True, False, False],                  # raises -> empty_prediction
        [True, True, True],                    # normal
    ])
    out = cls.value_function(imp, coalitions)
    assert out.tolist() == [7.0, 1.5]


def test_non_constant_fit_errors_still_propagate(monkeypatch):
    """Only the constant-features refusal is absorbed; anything else must
    surface so real failures are not silently zeroed again."""
    monkeypatch.setattr(xs, "_numpy_dropped_size1_coercion", lambda: True)
    cls = _fake_shapiq(monkeypatch)
    xs._ensure_shapiq_numpy2_compat()

    class _Boom(_StubModel):
        def fit(self, X, y):
            raise RuntimeError("CUDA out of memory")

    imp = cls.__new__(cls)
    imp.x_train = np.arange(12.0).reshape(4, 3)
    imp.y_train = np.arange(4.0)
    imp.x = np.array([[9.0, 9.0, 9.0]])
    imp.empty_prediction = 7.0
    imp.model = _Boom([1.5])
    imp.predict = imp.model.predict
    with pytest.raises(RuntimeError, match="CUDA"):
        cls.value_function(imp, np.array([[True, True, True]]))


def test_shim_is_idempotent(monkeypatch):
    monkeypatch.setattr(xs, "_numpy_dropped_size1_coercion", lambda: True)
    cls = _fake_shapiq(monkeypatch)
    xs._ensure_shapiq_numpy2_compat()
    first = cls.value_function
    xs._ensure_shapiq_numpy2_compat()
    assert cls.value_function is first, "second call re-patched"


def test_shim_noop_without_shapiq(monkeypatch):
    """Absent shapiq must not raise -- the caller treats XAI as optional."""
    for name in [m for m in sys.modules if m.startswith("shapiq")]:
        monkeypatch.delitem(sys.modules, name, raising=False)
    import builtins
    real_import = builtins.__import__

    def block_shapiq(name, *a, **k):
        if name.startswith("shapiq"):
            raise ImportError(name)
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", block_shapiq)
    monkeypatch.setattr(xs, "_numpy_dropped_size1_coercion", lambda: True)
    xs._ensure_shapiq_numpy2_compat()          # must simply return


# ------------------------------------------------- entry points are wired
def test_all_explainers_invoke_the_shim():
    """Each shapiq entry point must call the shim before constructing an
    explainer; a new entry point added without it re-introduces the silent
    all-zeros failure."""
    import inspect

    for fn in (xs.explain_local, xs.explain_interactions,
               xs.explain_shap_compat):
        src = inspect.getsource(fn)
        assert "_ensure_shapiq_numpy2_compat()" in src, fn.__name__


def test_no_bare_float_on_explainer_outputs():
    """The wrapper's own scalar extractions must use _as_scalar."""
    import inspect

    src = inspect.getsource(xs)
    assert "float(iv.baseline_value)" not in src
    assert 'float(getattr(iv, "baseline_value"' not in src
