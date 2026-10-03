"""model = 'kumo' — NVIDIA Kumo Tabular via structured-data-models (ml/kumo.py).

Most tests use a fake ``sdm`` so they run without the git-only package and
its checkpoint; the last one runs the real model when sdm is installed.
"""
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from geocif.geocif import Geocif
from geocif.ml import kumo
from geocif.ml import trainers


class _Table:
    def __init__(self, df):
        self.df = df.reset_index(drop=True)

    def drop_columns(self, c):
        return _Table(self.df.drop(columns=[c]))

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            rows, col = idx
            return _Table(self.df.iloc[rows][[col]])
        return _Table(self.df.iloc[idx])


class _Out:
    def __init__(self, df):
        self.df = df

    def to_pandas(self):
        return self.df


class _FakeModel:
    """Median = query feature 'a' + mean context target; q_k = median + (k-500)/100."""

    def __init__(self):
        self.calls = []

    def __call__(self, x_context, y_context, x_query, num_estimators, generator):
        self.calls.append(dict(n_ctx=len(x_context.df), n_q=len(x_query.df), y=y_context.df.iloc[:, 0].to_numpy(),
                               ctx_cols=list(x_context.df.columns), num_estimators=num_estimators))
        med = x_query.df["a"].to_numpy(float) + y_context.df.iloc[:, 0].mean()
        return _Out(pd.DataFrame({f"q{k:03d}": med + (k - 500) / 100.0 for k in range(1, 1000)}))


@pytest.fixture
def fake(monkeypatch):
    model = _FakeModel()
    stypes_seen = {}

    def infer_stypes(df, overrides=None):
        st = {c: ("categorical" if isinstance(df[c].dtype, pd.CategoricalDtype) else "numerical") for c in df.columns}
        st.update(overrides or {})
        stypes_seen.update(st)
        return st

    fake_sdm = SimpleNamespace(infer_stypes=infer_stypes,
                               TableTensor=SimpleNamespace(from_pandas=lambda df, stypes, device=None: _Table(df)))
    monkeypatch.setattr(kumo, "_sdm", lambda: fake_sdm)
    monkeypatch.setattr(kumo, "_model", lambda size, device: model)
    monkeypatch.setattr(kumo, "_resolve_device", lambda d: "cpu")
    return SimpleNamespace(model=model, stypes=stypes_seen)


def _xy(n=12, m=3):
    X = pd.DataFrame({
        "a": np.arange(n + m, dtype=float),
        "Harvest Year": pd.Categorical(np.arange(2001, 2001 + n + m)),
        "Region": pd.Categorical(["Iowa", "Ohio", "Kansas"] * ((n + m) // 3)),
    })
    y = np.linspace(5, 10, n)
    return X.iloc[:n], y, X.iloc[n:]


def test_frame_types_columns_for_sdm():
    X, _, _ = _xy()
    X = X.assign(flag=[True, False] * 6, name=["x"] * 12)
    f = kumo._frame(X)
    assert f["Harvest Year"].dtype == float, "numeric categories become numbers"
    assert isinstance(f["Region"].dtype, pd.CategoricalDtype)
    assert isinstance(f["name"].dtype, pd.CategoricalDtype)
    assert f["flag"].dtype == float


@pytest.mark.parametrize("p,col", [(0.1, "q100"), (0.5, "q500"), (0.9, "q900"), (0.0001, "q001"), (1.0, "q999")])
def test_quantile_column(p, col):
    assert kumo._quantile_column(p) == col


def test_predict_quantiles_passes_support_and_queries(fake):
    X, y, Xq = _xy()
    m = kumo.KumoTabularRegressor(num_estimators=4).fit(X, y)
    q = m.predict_quantiles(Xq, [0.1, 0.5, 0.9])
    call = fake.model.calls[-1]
    assert call["n_ctx"] == 12 and call["n_q"] == 3 and call["num_estimators"] == 4
    assert np.allclose(call["y"], y), "context targets must be the training targets"
    assert kumo._TARGET not in call["ctx_cols"], "the target must not be a feature"
    med = Xq["a"].to_numpy(float) + y.mean()
    assert np.allclose(q[:, 1], med) and np.allclose(q[:, 0], med - 4.0) and np.allclose(q[:, 2], med + 4.0)
    assert fake.stypes[kumo._TARGET] == "numerical"


def test_predict_is_the_median(fake):
    X, y, Xq = _xy()
    m = kumo.KumoTabularRegressor().fit(X, y)
    assert np.allclose(m.predict(Xq), m.predict_quantiles(Xq, [0.5])[:, 0])


def test_query_columns_follow_training_order(fake):
    X, y, Xq = _xy()
    m = kumo.KumoTabularRegressor().fit(X, y)
    m.predict_quantiles(Xq[["Region", "a", "Harvest Year"]], [0.5])
    assert fake.model.calls[-1]["ctx_cols"] == list(kumo._frame(X).columns)


def test_fit_rejects_mismatched_lengths():
    X, y, _ = _xy()
    with pytest.raises(ValueError):
        kumo.KumoTabularRegressor().fit(X, y[:-1])


def test_estimate_ci_leaves_kumo_unwrapped():
    sentinel = object()
    assert trainers.estimate_ci("REGRESSION", "kumo", sentinel, 0.2, "crepes") is sentinel


def test_geocif_ci_path_reads_native_quantiles():
    class M:
        def predict_quantiles(self, X, qs):
            assert qs == [0.1, 0.5, 0.9]
            return np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

        def get_params(self):
            return {"size": "large"}

    o = SimpleNamespace(alpha=0.2, model=M())
    y, ci, hp = Geocif._predict_kumo_with_ci(o, pd.DataFrame({"a": [0, 1]}))
    assert np.allclose(y, [2.0, 5.0]) and ci.shape == (2, 2, 1)
    assert np.allclose(ci[:, 0, 0], [1.0, 4.0]) and np.allclose(ci[:, 1, 0], [3.0, 6.0])
    assert hp == {"size": "large"}


def test_real_sdm_regression_smoke():
    pytest.importorskip("sdm")
    rng = np.random.default_rng(0)
    X = pd.DataFrame({"a": rng.normal(size=120), "b": rng.normal(size=120)})
    y = 50 + 4 * X["a"] - 2 * X["b"]
    m = kumo.KumoTabularRegressor(size="small", num_estimators=2).fit(X.iloc[:100], y.iloc[:100])
    q = m.predict_quantiles(X.iloc[100:], [0.1, 0.5, 0.9])
    assert q.shape == (20, 3) and np.all(q[:, 0] <= q[:, 1]) and np.all(q[:, 1] <= q[:, 2])
    truth = y.iloc[100:].to_numpy()
    assert 1 - ((truth - q[:, 1]) ** 2).sum() / ((truth - truth.mean()) ** 2).sum() > 0.8


def test_generator_follows_the_model_device(monkeypatch):
    """A CPU generator on a CUDA model failed every fit on the first GPU run."""
    import torch

    seen = []

    class _Gen:
        def __init__(self, device="cpu"):
            seen.append(device)

        def manual_seed(self, seed):
            return self

    monkeypatch.setattr(torch, "Generator", _Gen)
    kumo._generator("cuda:0", 3)
    kumo._generator("cpu", 3)
    assert seen == ["cuda", "cpu"]
