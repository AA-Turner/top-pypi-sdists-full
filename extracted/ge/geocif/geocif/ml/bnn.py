"""
Bayesian neural network for county/region-level yield forecasting (model='bnn').

PyTorch reimplementation of the two-headed BNN in:
    Ma, Zhang, Kang & Ozdogan (2021). Corn yield prediction and uncertainty
    analysis based on remotely sensed variables using a Bayesian neural network
    approach. Remote Sensing of Environment 259, 112408.

Architecture (paper Fig. 3), all layers variational Bayesian:
    trunk:            in -> 256 -> 128
    yield head:       128 -> 64 -> 32 -> 1   (mu)
    uncertainty head: 128 -> 64 -> 32 -> 1   (log sigma)
ReLU, Adam, batch 512.

Deviations from the paper, all optional and flagged in the constructor:
  1. A short MSE warm-up before the uncertainty head is trained. A jointly
     trained heteroscedastic head can collapse from epoch zero: the model
     inflates sigma on hard samples, down-weights their gradient, and never
     fits them. beta-NLL (Seitzer et al. 2022) is available via ``beta_nll``
     but defaults to 0 (exact NLL) -- on a synthetic panel with known
     county-varying noise, beta = 0.5 flattened sigma_hat completely
     (corr(sigma_hat, sigma_true) fell from 0.91 to ~0).
  2. Predictive variance = aleatoric + epistemic (mixture-of-Gaussians
     variance over MC weight draws), not sigma_hat alone.
  3. KL is annealed and scaled by 1/n_train so the objective is a true ELBO
     per sample, independent of batch size.
  4. Sigma calibration, from probes on a synthetic panel with a
     noise-informative feature: under the paper's tight prior + full KL the
     sigma head collapses to a near-constant (marginally calibrated only);
     with kl_weight ~ 0.05 it learns per-sample heterogeneity but at the
     in-sample residual scale (severe under-coverage, P95 ~ 0.13). Working
     recipe: fit with a small kl_weight, then rescale sigma by
     c = std of z-scores on a held-out calibration year. In geocif's
     expanding-window/LOOCV pipeline the natural calibration fold is the
     most recent training year -- ``BNNYieldRegressor`` below implements
     exactly that (two-pass: fit on years < max for c, refit on all years).

``BNNRegressor`` is the vendored pure-torch core (numpy in/out).
``BNNYieldRegressor`` is the geocif-facing sklearn adapter that trainers.py
dispatches to for model = 'bnn'.

torch is imported at module top; this module is the ONLY geocif.ml module
allowed to do that -- trainers.py imports it lazily inside the 'bnn' branch.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger(__name__)

__all__ = [
    "BayesLinear",
    "BNNYield",
    "gaussian_nll",
    "BNNRegressor",
    "BNNYieldRegressor",
]


# --------------------------------------------------------------------------- #
# Variational layer
# --------------------------------------------------------------------------- #
class BayesLinear(nn.Module):
    """Mean-field Gaussian variational linear layer.

    Posterior  q(w) = N(mu, softplus(rho)^2), prior p(w) = N(0, prior_sigma^2).
    KL(q||p) is closed form. Training uses the local reparameterization trick
    (sample pre-activations, not weights) for lower-variance gradients;
    prediction can sample weights instead, which is what makes the epistemic
    component of the predictive variance meaningful.
    """

    def __init__(self, in_features: int, out_features: int, prior_sigma: float = 0.1):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.prior_sigma = prior_sigma

        self.weight_mu = nn.Parameter(torch.empty(out_features, in_features))
        self.weight_rho = nn.Parameter(torch.empty(out_features, in_features))
        self.bias_mu = nn.Parameter(torch.zeros(out_features))
        self.bias_rho = nn.Parameter(torch.empty(out_features))

        # He-style init on the means, small initial posterior scales.
        bound = 1.0 / math.sqrt(in_features)
        nn.init.uniform_(self.weight_mu, -bound, bound)
        nn.init.constant_(self.weight_rho, -5.0)
        nn.init.constant_(self.bias_rho, -5.0)

    @property
    def weight_sigma(self) -> torch.Tensor:
        return F.softplus(self.weight_rho)

    @property
    def bias_sigma(self) -> torch.Tensor:
        return F.softplus(self.bias_rho)

    def forward(self, x: torch.Tensor, sample_weights: bool = False) -> torch.Tensor:
        if not sample_weights:
            # Local reparameterization: pre-activations are Gaussian in closed form.
            mean = F.linear(x, self.weight_mu, self.bias_mu)
            var = F.linear(x.pow(2), self.weight_sigma.pow(2), self.bias_sigma.pow(2))
            return mean + var.clamp_min(1e-12).sqrt() * torch.randn_like(mean)
        w = self.weight_mu + self.weight_sigma * torch.randn_like(self.weight_mu)
        b = self.bias_mu + self.bias_sigma * torch.randn_like(self.bias_mu)
        return F.linear(x, w, b)

    def kl(self) -> torch.Tensor:
        def _kl(mu, sigma):
            p = self.prior_sigma
            return (
                torch.log(torch.as_tensor(p, device=mu.device) / sigma)
                + (sigma.pow(2) + mu.pow(2)) / (2 * p**2)
                - 0.5
            ).sum()

        return _kl(self.weight_mu, self.weight_sigma) + _kl(self.bias_mu, self.bias_sigma)


# --------------------------------------------------------------------------- #
# Model
# --------------------------------------------------------------------------- #
class BNNYield(nn.Module):
    """Two-headed BNN: shared feature-extraction trunk, yield net, uncertainty net."""

    def __init__(
        self,
        n_features: int,
        trunk: tuple = (256, 128),
        head: tuple = (64, 32),
        prior_sigma: float = 0.1,
        min_sigma: float = 1e-3,
    ):
        super().__init__()
        self.min_sigma = min_sigma

        def stack(sizes, n_in):
            layers, prev = [], n_in
            for s in sizes:
                layers.append(BayesLinear(prev, s, prior_sigma))
                prev = s
            return nn.ModuleList(layers), prev

        self.trunk, d = stack(trunk, n_features)
        self.yield_head, dy = stack(head, d)
        self.unc_head, du = stack(head, d)
        self.yield_out = BayesLinear(dy, 1, prior_sigma)
        self.unc_out = BayesLinear(du, 1, prior_sigma)

    def forward(self, x: torch.Tensor, sample_weights: bool = False):
        h = x
        for layer in self.trunk:
            h = F.relu(layer(h, sample_weights))
        hy = h
        for layer in self.yield_head:
            hy = F.relu(layer(hy, sample_weights))
        hu = h
        for layer in self.unc_head:
            hu = F.relu(layer(hu, sample_weights))
        mu = self.yield_out(hy, sample_weights).squeeze(-1)
        sigma = F.softplus(self.unc_out(hu, sample_weights).squeeze(-1)) + self.min_sigma
        return mu, sigma

    def kl(self) -> torch.Tensor:
        return sum(m.kl() for m in self.modules() if isinstance(m, BayesLinear))


def gaussian_nll(mu, sigma, y, beta: float = 0.0) -> torch.Tensor:
    """Heteroscedastic Gaussian NLL, optionally beta-NLL weighted.

    beta = 0 is the exact NLL and the default. beta = 1 recovers MSE-like
    gradients on mu while still training sigma, at the cost of a much less
    informative sigma; use it only if the yield head is underfitting.
    """
    var = sigma.pow(2)
    nll = 0.5 * torch.log(var) + 0.5 * (y - mu).pow(2) / var
    if beta > 0:
        nll = nll * var.detach().pow(beta)
    return nll.mean()


# --------------------------------------------------------------------------- #
# Pure-torch core (numpy in/out)
# --------------------------------------------------------------------------- #
@dataclass
class BNNRegressor:
    epochs: int = 1500
    batch_size: int = 512
    lr: float = 1e-3
    prior_sigma: float = 0.1
    kl_weight: float = 1.0          # multiplier on the 1/n_train-scaled KL
    kl_anneal_epochs: int = 200
    warmup_epochs: int = 50         # MSE-only epochs before the sigma head is trained
    beta_nll: float = 0.0           # >0 helps mu but flattens sigma; see module docstring
    trunk: tuple = (256, 128)
    head: tuple = (64, 32)
    n_mc: int = 100                 # MC weight draws at prediction time
    device: str = "cpu"
    seed: int = 0
    verbose: int = 0
    # fitted state
    model_: BNNYield | None = field(default=None, repr=False)
    x_mean_: np.ndarray | None = field(default=None, repr=False)
    x_std_: np.ndarray | None = field(default=None, repr=False)
    y_mean_: float = field(default=0.0, repr=False)
    y_std_: float = field(default=1.0, repr=False)
    n_train_: int = field(default=0, repr=False)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "BNNRegressor":
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        dev = torch.device(self.device)

        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).ravel()

        # Standardization is fit on training rows only.
        self.x_mean_ = np.nanmean(X, axis=0)
        self.x_std_ = np.nanstd(X, axis=0)
        self.x_std_[self.x_std_ < 1e-8] = 1.0
        self.y_mean_ = float(y.mean())
        self.y_std_ = float(y.std()) or 1.0

        Xt = torch.tensor(self._scale_x(X), dtype=torch.float32, device=dev)
        yt = torch.tensor((y - self.y_mean_) / self.y_std_, dtype=torch.float32, device=dev)

        n = Xt.shape[0]
        self.n_train_ = int(n)
        bs = min(self.batch_size, n)  # tiny geocif folds: never a zero-row batch loop
        self.model_ = BNNYield(
            Xt.shape[1], self.trunk, self.head, self.prior_sigma
        ).to(dev)
        opt = torch.optim.Adam(self.model_.parameters(), lr=self.lr)

        self.model_.train()
        for epoch in range(self.epochs):
            perm = torch.randperm(n, device=dev)
            kl_scale = self.kl_weight * min(1.0, (epoch + 1) / max(1, self.kl_anneal_epochs)) / n
            for i in range(0, n, bs):
                idx = perm[i : i + bs]
                mu, sigma = self.model_(Xt[idx])
                if epoch < self.warmup_epochs:
                    data_term = F.mse_loss(mu, yt[idx]) + 0.0 * sigma.mean()
                else:
                    data_term = gaussian_nll(mu, sigma, yt[idx], self.beta_nll)
                loss = data_term + kl_scale * self.model_.kl()
                opt.zero_grad(set_to_none=True)
                loss.backward()
                nn.utils.clip_grad_norm_(self.model_.parameters(), 5.0)
                opt.step()
            if self.verbose and (epoch + 1) % self.verbose == 0:
                print(f"  epoch {epoch + 1:5d}  loss {loss.item():.4f}")
        return self

    def _scale_x(self, X: np.ndarray) -> np.ndarray:
        Z = (np.asarray(X, dtype=np.float64) - self.x_mean_) / self.x_std_
        return np.nan_to_num(Z, nan=0.0, posinf=0.0, neginf=0.0)

    @torch.no_grad()
    def predict(self, X: np.ndarray, n_mc: int | None = None, return_std: bool = True):
        """Return (mu, sigma_total, sigma_aleatoric, sigma_epistemic) in yield units."""
        assert self.model_ is not None, "call fit() first"
        n_mc = n_mc or self.n_mc
        dev = torch.device(self.device)
        Xt = torch.tensor(self._scale_x(X), dtype=torch.float32, device=dev)

        self.model_.eval()
        mus, sigmas = [], []
        for _ in range(n_mc):
            mu, sigma = self.model_(Xt, sample_weights=True)
            mus.append(mu)
            sigmas.append(sigma)
        mus = torch.stack(mus)
        sigmas = torch.stack(sigmas)

        mu_bar = mus.mean(0)
        var_alea = sigmas.pow(2).mean(0)          # E[sigma^2]
        var_epis = mus.var(0, unbiased=False)     # Var[mu]

        s = self.y_std_
        mu_out = (mu_bar.cpu().numpy() * s) + self.y_mean_
        sd_alea = var_alea.clamp_min(0).sqrt().cpu().numpy() * s
        sd_epis = var_epis.clamp_min(0).sqrt().cpu().numpy() * s
        sd_tot = np.sqrt(sd_alea**2 + sd_epis**2)
        if not return_std:
            return mu_out
        return mu_out, sd_tot, sd_alea, sd_epis


# --------------------------------------------------------------------------- #
# geocif-facing sklearn adapter
# --------------------------------------------------------------------------- #
class BNNYieldRegressor:
    """sklearn-style wrapper around ``BNNRegressor`` for the geocif pipeline.

    Routed through DefaultFitter like bass/pygrf: receives the raw
    ``selected_features + cat_features`` DataFrame (cat columns are pandas
    ``category`` dtype), one-hot encodes categoricals + median-imputes like
    ``BassRegressor._numeric``, and lets the torch core do its own
    standardization / nan_to_num.

    Sigma calibration (``calibrate_sigma=True``, the working recipe from the
    module docstring): two-pass fit --
      1. fit on years < max training year, predict the held-out max year,
         c = std((y_cal - mu_cal) / sd_cal), clipped to [0.5, 20];
      2. refit on ALL rows (mu never loses the newest, most valuable year)
         and keep c as ``sigma_scale_``, applied to every predicted sd.
    Skipped (c = 1, warning) when < 3 distinct years, the calibration year
    has < ``cal_min_rows`` rows, or < ``cal_min_train_rows`` rows remain.

    NOTE: this class must NEVER grow an attribute or method named
    ``calibrate`` or ``conformalize`` -- ModelTrainer's
    _add_confidence_intervals_if_needed probes hasattr(model, 'calibrate')
    after trainers.estimate_ci early-returns the unwrapped bnn model, and
    would call it with in-sample training data (wrong data for the recipe,
    and a TypeError if the attribute is a bool). Hence ``calibrate_sigma``.
    """

    def __init__(
        self,
        epochs: int = 700,
        batch_size: int = 512,
        lr: float = 1e-3,
        prior_sigma: float = 0.1,
        kl_weight: float = 0.05,
        warmup_epochs: int = 50,
        n_mc: int = 100,
        calibrate_sigma: bool = True,
        cal_min_rows: int = 8,
        cal_min_train_rows: int = 30,
        seed: int = 0,
        device: str = "auto",
    ):
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.prior_sigma = prior_sigma
        self.kl_weight = kl_weight
        self.warmup_epochs = warmup_epochs
        self.n_mc = n_mc
        self.calibrate_sigma = calibrate_sigma
        self.cal_min_rows = cal_min_rows
        self.cal_min_train_rows = cal_min_train_rows
        self.seed = seed
        self.device = device

    def get_params(self, deep=True):
        return dict(
            epochs=self.epochs,
            batch_size=self.batch_size,
            lr=self.lr,
            prior_sigma=self.prior_sigma,
            kl_weight=self.kl_weight,
            warmup_epochs=self.warmup_epochs,
            n_mc=self.n_mc,
            calibrate_sigma=self.calibrate_sigma,
            cal_min_rows=self.cal_min_rows,
            cal_min_train_rows=self.cal_min_train_rows,
            seed=self.seed,
            device=self.device,
        )

    def set_params(self, **p):
        for k, v in p.items():
            setattr(self, k, v)
        return self

    def _numeric(self, X):
        X = pd.DataFrame(X).copy()
        obj = list(X.select_dtypes(include=["object", "category"]).columns)
        if obj:
            X = pd.get_dummies(X, columns=obj, dummy_na=False)
        return X.apply(pd.to_numeric, errors="coerce")

    @staticmethod
    def _years(X: pd.DataFrame):
        """Harvest Year as numeric, or None. It arrives as pandas CATEGORY
        dtype (geocif casts cat_features), so go through astype(str) --
        pd.to_numeric on a raw Categorical raises TypeError."""
        if "Harvest Year" not in X.columns:
            return None
        yrs = pd.to_numeric(pd.Series(X["Harvest Year"]).astype(str), errors="coerce")
        return yrs.reset_index(drop=True) if yrs.notna().any() else None

    def _make_core(self) -> BNNRegressor:
        # 'auto' -> cuda when available (gsappx GPU nodes), else cpu — same
        # semantics as tabpfn's device='auto'. Resolved here, not in __init__,
        # so get_params round-trips the configured value.
        #
        # _is_in_bad_fork guard: geocif's do_parallel_ml pool FORKS workers,
        # and if the parent process ever initialized CUDA (even a stray
        # torch.cuda.is_available() in a launcher script), every worker's
        # first CUDA call dies with "Cannot re-initialize CUDA in forked
        # subprocess" — this killed all folds of the first gsappx2 run
        # (2026-09-03). In that state, fall back to CPU instead of crashing.
        dev = self.device
        if dev == "auto":
            in_bad_fork = getattr(torch.cuda, "_is_in_bad_fork", lambda: False)()
            if in_bad_fork:
                logger.warning(
                    "bnn: CUDA was initialized in the parent before fork; "
                    "falling back to device='cpu' for this worker"
                )
                dev = "cpu"
            else:
                dev = "cuda" if torch.cuda.is_available() else "cpu"
        return BNNRegressor(
            epochs=self.epochs,
            batch_size=self.batch_size,
            lr=self.lr,
            prior_sigma=self.prior_sigma,
            kl_weight=self.kl_weight,
            warmup_epochs=self.warmup_epochs,
            n_mc=self.n_mc,
            device=dev,
            seed=self.seed,
        )

    def fit(self, X, y):
        X = pd.DataFrame(X).reset_index(drop=True)
        y = np.asarray(y, dtype=float).ravel()
        years = self._years(X)  # extracted BEFORE one-hot encoding

        Xn = self._numeric(X)
        # All-NaN columns give a NaN median -> second fillna(0.0) catches them.
        self._median = Xn.median(numeric_only=True)
        Xn = Xn.fillna(self._median).fillna(0.0)
        self.columns_ = list(Xn.columns)
        Xv = Xn.values.astype(float)

        self.sigma_scale_ = 1.0
        if self.calibrate_sigma:
            self._fit_sigma_scale(Xv, y, years)

        # Final model always trains on ALL rows -- the calibration fit above
        # is a throwaway pass whose only output is sigma_scale_.
        self._core = self._make_core().fit(Xv, y)
        return self

    def _fit_sigma_scale(self, Xv: np.ndarray, y: np.ndarray, years):
        """Pass 1 of the two-pass recipe: c from the held-out newest year."""
        if years is None:
            logger.warning(
                "bnn: no usable 'Harvest Year' column; sigma calibration skipped (c=1)"
            )
            return
        cal_year = years.max()
        mask_cal = (years == cal_year).to_numpy()
        n_cal, n_fit = int(mask_cal.sum()), int((~mask_cal).sum())
        n_years = int(years.dropna().nunique())
        if n_years < 3 or n_cal < self.cal_min_rows or n_fit < self.cal_min_train_rows:
            logger.warning(
                f"bnn: skipping sigma calibration "
                f"(years={n_years}, n_cal={n_cal}, n_fit={n_fit}); c=1"
            )
            return
        core_cal = self._make_core().fit(Xv[~mask_cal], y[~mask_cal])
        mu_c, sd_c, _, _ = core_cal.predict(Xv[mask_cal], n_mc=self.n_mc, return_std=True)
        z = (y[mask_cal] - mu_c) / np.maximum(sd_c, 1e-8)
        c = float(np.std(z))
        if np.isfinite(c) and c > 0:
            # Clip so one freak calibration year can't nuke every interval.
            self.sigma_scale_ = float(np.clip(c, 0.5, 20.0))
            logger.info(
                f"bnn: sigma recalibration c={self.sigma_scale_:.3f} "
                f"(fit on {int(cal_year)}, n_cal={n_cal})"
            )
        else:
            logger.warning(
                f"bnn: degenerate sigma-scale on cal year {int(cal_year)}; c=1"
            )

    def _encode(self, X) -> np.ndarray:
        Xn = self._numeric(pd.DataFrame(X)).reindex(columns=self.columns_, fill_value=0.0)
        Xn = Xn.fillna(self._median).fillna(0.0)
        return Xn.values.astype(float)

    def predict(self, X, return_std: bool = False):
        # Reseed so MC draws are identical call-to-call: the point path
        # (_predict_point_estimates) and the CI path (_predict_bnn_with_ci)
        # must emit the same mu for the same X.
        torch.manual_seed(self.seed + 1)
        mu, sd_tot, sd_alea, sd_epis = self._core.predict(
            self._encode(X), n_mc=self.n_mc, return_std=True
        )
        if return_std:
            c = self.sigma_scale_
            return mu, sd_tot * c, sd_alea * c, sd_epis * c
        return mu
