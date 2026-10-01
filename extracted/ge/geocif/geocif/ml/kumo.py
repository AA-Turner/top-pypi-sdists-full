"""
NVIDIA Kumo Tabular for regional yield forecasting (model = 'kumo'), run
through NVIDIA's structured-data-models library (import name ``sdm``).

Kumo Tabular (NVIDIA, 2026; https://huggingface.co/blog/nvidia/kumo-tabular)
is an in-context tabular foundation model in the TabPFN / causilo family:
the support set and the queries go through one forward pass, with no
gradient step at fit time. Its regression head emits 999 native quantiles
(``q001`` .. ``q999``), so geocif reads the point forecast (the median) and
the prediction interval off the same distribution, like causilo — see
``Geocif._predict_kumo_with_ci``.

    code      github.com/NVIDIA/structured-data-models   (Apache-2.0)
    weights   nvidia/Kumo-Tabular, revision v1.0.0       (OpenMDW 1.1, not gated)
              small / medium / large; ~0.9 GB for small + large regressors

INSTALL (git-only, no PyPI release)
-----------------------------------
sdm needs Python >= 3.11 and torch >= 2.7, both already in the production
pixi env, so it is side-installed rather than added to the shared env:

    <python with pip> -m pip install --no-deps \\
        --target /gpfs/data1/cmongp1/ritvik/sdm_site \\
        git+https://github.com/NVIDIA/structured-data-models.git

and the launch payload puts that directory on ``sys.path`` before importing
geocif. ``HF_HUB_CACHE`` should point at ``/gpfs/.../hf_cache/hub`` so the
checkpoint is not downloaded into the small ``$HOME``; huggingface_hub reads
it at import time, so it must be set in the launch command, not here.

Two practical notes the wrapper absorbs:

1. **torch first.** ``import sdm`` with torch not yet imported loads the
   system libstdc++ ahead of torch's, and ``import torch`` then fails with
   ``GLIBCXX_3.4.30 not found`` in the pixi env. The wrapper imports torch
   before sdm.
2. **One table for support + queries.** Categorical columns are encoded per
   TableTensor, so the training and test rows are stacked into one table and
   sliced; separate tables could map the same category to different codes.

CPU works (state-scale fold: a few seconds); a GPU is faster for county
scale. Smoke test 2026-09-30: synthetic target, R2 0.989, 80% interval
coverage 0.78 (large) / 0.83 (small).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SDM_INSTALL = "pip install git+https://github.com/NVIDIA/structured-data-models.git"
_TARGET = "__kumo_target__"

# geocif builds a fresh model object for every (fold, stage, region) task;
# the backbone is frozen and carries no per-fold state, so one resident model
# serves every fold instead of reloading the checkpoint each time.
_MODEL_CACHE: dict = {}


def _sdm():
    import torch  # noqa: F401  (must precede sdm, see module docstring)

    try:
        import sdm
    except ImportError as exc:
        raise ImportError(
            "model = 'kumo' needs NVIDIA structured-data-models (import name "
            f"`sdm`), which is git-only: {SDM_INSTALL} (Python >= 3.11, "
            "torch >= 2.7). On the cluster it lives in "
            "/gpfs/data1/cmongp1/ritvik/sdm_site; put that on sys.path."
        ) from exc
    return sdm


def _resolve_device(device):
    import torch

    if device and device != "auto":
        return device
    return "cuda" if torch.cuda.is_available() else "cpu"


def _model(size, device):
    key = (size, device)
    if key not in _MODEL_CACHE:
        _MODEL_CACHE.clear()
        _MODEL_CACHE[key] = _sdm().models.KumoTabular(task="regression", size=size, device=device)
    return _MODEL_CACHE[key]


def _quantile_column(p):
    k = min(max(int(round(float(p) * 1000)), 1), 999)
    return f"q{k:03d}"


def _frame(X):
    """Plain DataFrame sdm can type: numeric categories (Harvest Year,
    Region_ID) become numbers, other categories / strings stay categorical."""
    df = pd.DataFrame(X).copy()
    df.columns = [str(c) for c in df.columns]
    for c in df.columns:
        s = df[c]
        if isinstance(s.dtype, pd.CategoricalDtype):
            num = pd.to_numeric(s.astype(object), errors="coerce")
            df[c] = num.astype(float) if num.notna().sum() == s.notna().sum() else s.astype(str).astype("category")
        elif s.dtype == bool:
            df[c] = s.astype(float)
        elif not pd.api.types.is_numeric_dtype(s):
            df[c] = s.astype(str).astype("category")
    return df


class KumoTabularRegressor:
    """Kumo Tabular in-context regressor, sklearn-shaped for geocif.

    Parameters
    ----------
    size
        ``"small"``, ``"medium"`` or ``"large"`` (default, the released best).
    device
        ``"auto"`` picks cuda when available, else cpu.
    num_estimators
        Ensemble members (feature-processing variants averaged by the recipe).
        8 matches geocif's tabpfn / causilo budget.
    seed
        Seeds the recipe's sampling (column shuffles, transform choice).
    """

    def __init__(self, size="large", device="auto", num_estimators=8, seed=0):
        self.size = size
        self.device = device
        self.num_estimators = int(num_estimators)
        self.seed = int(seed)

    def fit(self, X, y):
        """Store the support set; Kumo Tabular is in-context, no training here."""
        self.X_ = _frame(X)
        self.y_ = np.asarray(y, dtype=float).ravel()
        if len(self.X_) != len(self.y_):
            raise ValueError(f"kumo: X has {len(self.X_)} rows, y has {len(self.y_)}")
        return self

    def predict_quantiles(self, X, quantiles):
        """(n, len(quantiles)) array of predictive quantiles for X."""
        import torch

        sdm = _sdm()
        device = _resolve_device(self.device)
        X_q = _frame(X).reindex(columns=self.X_.columns)
        n = len(self.X_)
        df = pd.concat([self.X_, X_q], ignore_index=True)
        df[_TARGET] = np.concatenate([self.y_, np.full(len(X_q), np.nan)])
        stypes = sdm.infer_stypes(df, overrides={_TARGET: "numerical"})
        table = sdm.TableTensor.from_pandas(df, stypes=stypes, device=device)
        x = table.drop_columns(_TARGET)
        with torch.no_grad(), torch.amp.autocast(
            "cuda" if str(device).startswith("cuda") else "cpu",
            torch.float16,
            enabled=str(device).startswith("cuda"),
        ):
            out = _model(self.size, device)(
                x_context=x[:n],
                y_context=table[:n, _TARGET],
                x_query=x[n:],
                num_estimators=self.num_estimators,
                generator=torch.Generator().manual_seed(self.seed),
            )
        q = out.to_pandas()
        return np.column_stack([q[_quantile_column(p)].to_numpy(dtype=float) for p in quantiles])

    def predict(self, X):
        """Point forecast: the predictive median."""
        return self.predict_quantiles(X, [0.5])[:, 0]

    def get_params(self, deep=True):
        return {"size": self.size, "device": self.device,
                "num_estimators": self.num_estimators, "seed": self.seed}
