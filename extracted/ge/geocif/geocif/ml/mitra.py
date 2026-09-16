"""
Mitra-v2 tabular foundation model for regional yield forecasting
(model = 'mitra' zero-shot / 'mitra_ft' fine-tuned).

Mitra-v2 (Tao, Zhang, Liu, Han et al., 2026, *Mitra-v2 Technical Report*,
arXiv:2609.04540; Amazon/AutoGluon) is an in-context tabular foundation model
pretrained ONLY on synthetic data. Backbone: a 12-layer element-wise 2D
Transformer (hidden 512, 4 heads, ~76.7 M parameters for the regressor) that
attends twice per layer — once across rows, once across columns. Weights are
Apache-2.0 on the HF Hub:

    classification   autogluon/mitra-classifier-2
    regression       autogluon/mitra-regressor-2      <- what this module loads

Pretraining task shape (paper §2.4 / Table 1) — the envelope geocif folds
should stay inside:

    support rows   160 – 5,120        (geocif LOOCV folds: ~200 – 5,000  OK)
    query rows     1,280              (geocif: 1 – ~300 regions           OK)
    features       1 – 50             (feature_selection = gOMP_medium
                                       caps at 50                         OK)

Above 256 features the released recipe reduces regression tables with a
train-only truncated SVD to 256 components; ``max_features`` reproduces that.
Running with ``feature_selection = none`` (~1,000 monthly_r columns) is far
outside the pretraining envelope — use gOMP_medium.

WHY THIS MODULE EXISTS RATHER THAN A ONE-LINE trainers.py BRANCH
----------------------------------------------------------------
The Mitra *code* ships inside ``autogluon.tabular`` but its public sklearn
wrapper (``MitraRegressor``) cannot drive the v2 regression checkpoint:

1. ``MitraBase._create_config`` hardcodes ``regression_loss = "mse"`` and
   ``MitraRegressor.fit`` passes ``dim_output = 1`` — i.e. v1's SCALAR head.
   The v2 regressor is a **1,000-bin cross-entropy head**
   (``config.json``: ``dim_output = 1000``): regression as classification over
   value bins. AutoGluon already contains the whole binned path — it is simply
   not reachable through a public hyperparameter. We build the ``ConfigRun``
   ourselves with ``regression_loss = CROSS_ENTROPY`` and
   ``dim_output = <checkpoint's own>``.
2. Stock AutoGluon decodes that head with ``argmax`` over bins (the modal
   bin centre). The released Mitra-v2 recipe decodes with the **softmax-
   weighted MEAN over bin centres**, which its authors call the only
   quality-critical delta from stock ("materially lowers RMSE"). We decode
   with the mean, and keep the full histogram so the model has NATIVE
   predictive intervals (see ``predict_quantiles``).

The upstream ``mitra-finetune`` package implements the same two deltas by
monkey-patching AutoGluon at import time, but it is built for the TabArena
benchmark harness: CUDA-only, one 8-fold bagged 50-step fine-tune per
``predict`` call with a 3,600 s default budget, executed in a spawned
subprocess, and it drags in ``tabarena`` (openml, ray, bencheval). geocif fits
thousands of small LOOCV folds per run, so that shape is unusable here. This
module is the same recipe without the harness.

ATTRIBUTION
-----------
The recipe above — cross-entropy head + mean decode + mirror-aware grid
mapping — was learned by reading the reference implementation in
``autogluon/mitra-finetune`` (https://huggingface.co/autogluon/mitra-finetune,
Boran Han et al., Amazon; Apache License 2.0), in particular
``patches.install_reg_ce_patches``, ``patches._mean_decode_source`` and
``patches._member_grid_in_target_units``. ``_member_histogram`` below follows
that last function's edge/probability flip and its ``nan_to_num`` guard. No
code from that package is vendored and geocif does not depend on it; the
rest of this module (zero-shot path, encoder, single-grid quantile inversion,
RNG handling, caching) is original to geocif. The backbone, weight loader and
in-context trainer are AutoGluon's own (``autogluon.tabular``, Apache-2.0),
used as a library. The checkpoint repo ``autogluon/mitra-regressor-2``
contains weights and a config only, no code.

BINS AND THE TARGET SCALE (why intervals come for free)
-------------------------------------------------------
Mitra min-max normalises y to [0, 1] on the SUPPORT set, and the 1,000 bins
span ``linspace(-0.5, 1.5)`` in that normalised space — so the head can place
mass 50 % of the training range beyond the training min and max. The softmax
over bins is a genuine predictive distribution in target units, giving
quantile intervals with no conformal wrapper (like ``bnn``, unlike tabpfn's
quantile head).

TRAPS ENCODED BELOW (each one cost a real debugging cycle upstream)
-------------------------------------------------------------------
* ``Preprocessor.fit`` / ``transform_X`` impute NaN **in place**
  (``x[inds] = ...``). geocif hands the same X to several models per fold, so
  every array reaching AutoGluon here is a private copy.
* ``Preprocessor`` draws its mirror augmentations from the **global** numpy
  RNG, not the ``rng`` it is handed. ``_numpy_seed`` pins and restores global
  state around every member so folds are reproducible and ensemble members
  still differ.
* The 307 MB checkpoint is cached per (repo, device) at module level. Loading
  it per ``auto_train`` call is what made plain ``tabfm`` unusable
  (0 rows in 2 h). A fine-tuning member deep-copies the cached backbone so it
  never mutates the shared weights.
* CPU autocast supports bfloat16/float16 only; ``precision="auto"`` resolves
  to float32 on CPU (and the gsapp EPYC 7H12 nodes have no AVX512-BF16, so
  bf16 there is emulated and slower) and bfloat16 on CUDA.
* This class must NEVER grow an attribute named ``calibrate`` or
  ``conformalize`` — ``_add_confidence_intervals_if_needed`` probes
  ``hasattr(model, "calibrate")`` and would call it with in-sample data
  (the same trap documented on ``BNNYieldRegressor``).

``autogluon.tabular[mitra]`` is an optional dependency (``geocif[mitra]``);
everything is imported lazily so the module is importable without it. Note that
``transformers`` is a HARD runtime requirement of the path we use, not an
optional nicety: AutoGluon's ``get_scheduler`` imports it at module scope and
``TrainerFinetune`` imports ``get_scheduler``, so a side-install that omits it
fails at import, not at fine-tune time.
"""

from __future__ import annotations

import contextlib
import logging
import warnings
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

__all__ = [
    "MitraYieldRegressor",
    "MITRA_V2_REGRESSOR",
    "MITRA_V1_REGRESSOR",
    "PRETRAIN_MAX_FEATURES",
    "DEPLOY_FEATURE_BUDGET",
]

# HF Hub repo ids. '-2' is Mitra-v2 (1,000-bin cross-entropy head); the
# unsuffixed repo is Mitra-v1 (scalar MSE head) and is still supported here so
# a v1-vs-v2 A/B needs only a config key.
MITRA_V2_REGRESSOR = "autogluon/mitra-regressor-2"
MITRA_V1_REGRESSOR = "autogluon/mitra-regressor"

# Paper §2.4 / Table 1: pretraining sampled 1-50 features per task.
PRETRAIN_MAX_FEATURES = 50
# Paper §2.6: deployment-time budget for wide tables (train-only SVD for
# regression). Our default cap.
DEPLOY_FEATURE_BUDGET = 256

_IMPORT_HINT = (
    "model = 'mitra' requires AutoGluon's Mitra extra (the Mitra-v2 weights "
    "and backbone ship inside autogluon.tabular):\n"
    "    pip install 'geocif[mitra]'\n"
    "or, without touching a production env, side-install it and prepend "
    "PYTHONPATH:\n"
    "    uv pip install --target <dir> --no-deps autogluon.tabular==1.6.1 "
    "autogluon.core==1.6.1 autogluon.common==1.6.1 autogluon.features==1.6.1 "
    "loguru einx omegaconf transformers"
)

# (repo_or_path, device) -> Tab2D. Populated lazily, once per process.
_BACKBONE_CACHE: dict = {}


# ---------------------------------------------------------------------------
# lazy autogluon plumbing
# ---------------------------------------------------------------------------
def _mitra_internals():
    """Import the AutoGluon Mitra internals, or raise with an install hint."""
    try:
        from autogluon.tabular.models.mitra._internal.config.config_run import (
            ConfigRun,
        )
        from autogluon.tabular.models.mitra._internal.config.enums import (
            LossName,
            ModelName,
            Task,
        )
        from autogluon.tabular.models.mitra._internal.core.trainer_finetune import (
            TrainerFinetune,
        )
        from autogluon.tabular.models.mitra._internal.data.dataset_finetune import (
            DatasetFinetune,
        )
        from autogluon.tabular.models.mitra._internal.models.tab2d import Tab2D
    except ImportError as exc:  # pragma: no cover - exercised on the cluster
        raise ImportError(_IMPORT_HINT) from exc

    return {
        "ConfigRun": ConfigRun,
        "LossName": LossName,
        "ModelName": ModelName,
        "Task": Task,
        "TrainerFinetune": TrainerFinetune,
        "DatasetFinetune": DatasetFinetune,
        "Tab2D": Tab2D,
    }


def _resolve_device(device: str) -> str:
    """'auto' -> cuda when usable, else cpu.

    Mirrors ``BNNYieldRegressor._make_core``: geocif's ``do_parallel_ml`` pool
    FORKS its workers, and a parent process that already touched CUDA poisons
    every child ("Cannot re-initialize CUDA in forked subprocess"). Fall back
    to CPU rather than killing the fold.
    """
    if device != "auto":
        return device

    try:
        import torch
    except ImportError:  # pragma: no cover
        return "cpu"

    if not torch.cuda.is_available():
        return "cpu"
    if getattr(torch.cuda, "_is_in_bad_fork", lambda: False)():
        logger.warning(
            "mitra: CUDA was initialized in the parent before this worker "
            "forked; falling back to CPU for this fold"
        )
        return "cpu"
    return "cuda"


def _resolve_precision(precision: str, device: str) -> Optional[str]:
    """Autocast dtype name, or None for 'run in float32, no autocast'.

    torch's CPU autocast accepts bfloat16/float16 only, so float32 must be
    expressed as "no autocast context" rather than ``dtype=torch.float32``.
    """
    if precision == "auto":
        return "bfloat16" if str(device).startswith("cuda") else None
    if precision in ("float32", "fp32", "none", None):
        return None
    return precision


@contextlib.contextmanager
def _numpy_seed(seed: int):
    """Pin the GLOBAL numpy RNG, then restore it.

    AutoGluon's ``Preprocessor`` draws ``random_mirror_regression`` /
    ``random_mirror_x`` / feature shuffling from ``np.random.*`` rather than
    from the ``rng`` it is constructed with. Without this, two runs of the
    same fold disagree and geocif's global RNG state is silently perturbed.
    """
    state = np.random.get_state()
    try:
        np.random.seed(int(seed) % (2**32 - 1))
        yield
    finally:
        np.random.set_state(state)


def _load_backbone(hf_model: str, device: str, cache: bool = True):
    """Load (and memoise) the pretrained Tab2D for (hf_model, device).

    ``Tab2D.from_pretrained`` accepts an HF repo id (downloaded through
    ``huggingface_hub`` into HF_HOME) or a local directory holding
    ``config.json`` + ``model.safetensors``.
    """
    key = (hf_model, device)
    if cache and key in _BACKBONE_CACHE:
        return _BACKBONE_CACHE[key]

    Tab2D = _mitra_internals()["Tab2D"]
    model = Tab2D.from_pretrained(hf_model, device=device)
    model.eval()
    if cache:
        _BACKBONE_CACHE[key] = model
    return model


# ---------------------------------------------------------------------------
# feature preparation
# ---------------------------------------------------------------------------
class _NumericEncoder:
    """DataFrame -> dense float32 matrix, with a fit-time categorical map.

    Mitra consumes a 2-D numeric array (``MitraBase.fit`` does ``X.values``
    and ``np.nanmean`` over it), so geocif's ``category``/object columns
    (Region, Region_ID, Harvest Year) must be encoded first.

    * Categorical columns whose LEVELS are numeric (``Harvest Year``,
      ``Region_ID``) keep their numeric value — encoding them as factorize
      codes would destroy the ordering of years, which the model can use.
    * Genuinely nominal columns (Region) get a fit-time level -> code map;
      unseen or missing levels at predict time map to -1, a distinct
      "unknown" code (the convention already used by the exaone wrapper).
    """

    def __init__(self) -> None:
        self.columns_: list = []
        self.cat_maps_: dict = {}
        self.numeric_levels_: set = set()

    @staticmethod
    def _is_categorical(s: pd.Series) -> bool:
        return (
            isinstance(s.dtype, pd.CategoricalDtype)
            or s.dtype == object
            or str(s.dtype).startswith("string")
        )

    @staticmethod
    def _as_numeric_levels(s: pd.Series) -> Optional[np.ndarray]:
        """Numeric view of a categorical column, or None if it is nominal."""
        values = pd.to_numeric(pd.Series(s).astype(str), errors="coerce")
        # `.astype(str)` turns NaN into the literal 'nan', which to_numeric
        # maps back to NaN -- so "all-non-null values parsed" is the test.
        parsed = values.notna().to_numpy()
        present = pd.Series(s).notna().to_numpy()
        if present.any() and bool((parsed | ~present).all()):
            return values.to_numpy(dtype="float64")
        return None

    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        X = pd.DataFrame(X)
        self.columns_ = list(X.columns)
        self.cat_maps_ = {}
        self.numeric_levels_ = set()

        columns = []
        for name in self.columns_:
            s = X[name]
            if self._is_categorical(s):
                numeric = self._as_numeric_levels(s)
                if numeric is not None:
                    self.numeric_levels_.add(name)
                    columns.append(numeric)
                    continue
                codes, uniques = pd.factorize(s, sort=False)  # NaN -> -1
                self.cat_maps_[name] = {v: i for i, v in enumerate(uniques)}
                columns.append(codes.astype("float64"))
            else:
                columns.append(
                    pd.to_numeric(s, errors="coerce").to_numpy(dtype="float64")
                )
        return self._stack(columns, len(X))

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        X = pd.DataFrame(X).reindex(columns=self.columns_)

        columns = []
        for name in self.columns_:
            s = X[name]
            if name in self.numeric_levels_:
                columns.append(
                    pd.to_numeric(pd.Series(s).astype(str), errors="coerce").to_numpy(
                        dtype="float64"
                    )
                )
            elif name in self.cat_maps_:
                mapped = pd.Series(s).map(self.cat_maps_[name]).to_numpy(dtype="float64")
                columns.append(np.where(np.isnan(mapped), -1.0, mapped))
            else:
                columns.append(
                    pd.to_numeric(s, errors="coerce").to_numpy(dtype="float64")
                )
        return self._stack(columns, len(X))

    @staticmethod
    def _stack(columns: list, n_rows: int) -> np.ndarray:
        if not columns:
            return np.empty((n_rows, 0), dtype="float32")
        return np.column_stack(columns).astype("float32", copy=False)


# ---------------------------------------------------------------------------
# the geocif-facing model
# ---------------------------------------------------------------------------
class MitraYieldRegressor:
    """Mitra-v2 in-context regressor, sklearn-shaped for geocif.

    Parameters
    ----------
    hf_model
        HF repo id or local checkpoint directory. Defaults to the Mitra-v2
        regressor; pass ``MITRA_V1_REGRESSOR`` (or any local
        ``save_pretrained`` dir) to A/B another checkpoint. The head type is
        read from the checkpoint itself (``dim_output``), so v1's scalar head
        and v2's 1,000-bin head both work.
    n_estimators
        In-context ensemble members. Each re-runs the same frozen backbone
        under a different preprocessor augmentation draw (mirror / feature
        order), so cost is linear and the weights are loaded once.
    fine_tune
        ``False`` (model = 'mitra'): zero-shot, forward passes only.
        ``True`` (model = 'mitra_ft'): the released 50-step full fine-tune per
        member, which is what the paper's headline numbers use — but the paper
        also runs it 8-fold bagged on an H100. Expect minutes per fold; use it
        only with ``run_time_steps = latest``.
    max_samples_support / max_samples_query
        In-context caps. Above them ``DatasetFinetune`` subsamples the support
        set and chunks the queries.
    max_features
        Train-only truncated-SVD reduction above this many columns (paper
        §2.6). ``0`` disables it.

    Not implemented: CLASSIFICATION. geocif's classification path has never
    worked end-to-end, and the classifier is a different checkpoint.
    """

    def __init__(
        self,
        hf_model: str = MITRA_V2_REGRESSOR,
        device: str = "auto",
        n_estimators: int = 1,
        fine_tune: bool = False,
        fine_tune_steps: int = 50,
        lr: float = 1e-5,
        warmup_steps: int = 10,
        weight_decay: float = 0.3,
        max_samples_support: int = 8192,
        max_samples_query: int = 1024,
        max_features: int = DEPLOY_FEATURE_BUDGET,
        val_frac: float = 0.2,
        precision: str = "auto",
        seed: int = 0,
        verbose: bool = False,
    ) -> None:
        self.hf_model = hf_model
        self.device = device
        self.n_estimators = n_estimators
        self.fine_tune = fine_tune
        self.fine_tune_steps = fine_tune_steps
        self.lr = lr
        self.warmup_steps = warmup_steps
        self.weight_decay = weight_decay
        self.max_samples_support = max_samples_support
        self.max_samples_query = max_samples_query
        self.max_features = max_features
        self.val_frac = val_frac
        self.precision = precision
        self.seed = seed
        self.verbose = verbose

    # -- sklearn surface ---------------------------------------------------
    def get_params(self, deep=True):
        return dict(
            hf_model=self.hf_model,
            device=self.device,
            n_estimators=self.n_estimators,
            fine_tune=self.fine_tune,
            fine_tune_steps=self.fine_tune_steps,
            lr=self.lr,
            warmup_steps=self.warmup_steps,
            weight_decay=self.weight_decay,
            max_samples_support=self.max_samples_support,
            max_samples_query=self.max_samples_query,
            max_features=self.max_features,
            val_frac=self.val_frac,
            precision=self.precision,
            seed=self.seed,
            verbose=self.verbose,
        )

    def set_params(self, **p):
        for k, v in p.items():
            setattr(self, k, v)
        return self

    # -- config ------------------------------------------------------------
    def _build_config(self, dim_output: int, device: str):
        """The stock ``MitraBase._create_config`` hyperparams, with the two
        deltas that make a v2 regression checkpoint work: cross-entropy loss
        and the checkpoint's own ``dim_output``."""
        api = _mitra_internals()
        ConfigRun, LossName = api["ConfigRun"], api["LossName"]
        ModelName, Task = api["ModelName"], api["Task"]

        binned = dim_output > 1
        cfg = ConfigRun(
            device=device,
            model_name=ModelName.TAB2D,
            seed=int(self.seed),
            hyperparams={
                "dim_embedding": None,
                "early_stopping_data_split": "VALID",
                "early_stopping_max_samples": 2048,
                # Fine-tuning is step-capped (fine_tune_steps), so patience
                # only needs to exceed it to stay out of the way.
                "early_stopping_patience": max(int(self.fine_tune_steps), 1) + 1,
                "grad_scaler_enabled": False,
                "grad_scaler_growth_interval": 1000,
                "grad_scaler_scale_init": 65536.0,
                "grad_scaler_scale_min": 65536.0,
                "label_smoothing": 0.0,
                "lr_scheduler": False,
                "lr_scheduler_patience": 25,
                "max_epochs": int(self.fine_tune_steps) if self.fine_tune else 0,
                "max_samples_query": int(self.max_samples_query),
                "max_samples_support": int(self.max_samples_support),
                "optimizer": "adamw",
                "lr": float(self.lr),
                "weight_decay": float(self.weight_decay),
                "warmup_steps": int(self.warmup_steps),
                # Only consulted inside torch.autocast, which we skip on CPU.
                "precision": _resolve_precision(self.precision, device) or "bfloat16",
                "random_mirror_regression": True,
                "random_mirror_x": True,
                "shuffle_classes": False,
                "shuffle_features": False,
                "use_random_transforms": False,
                "use_feature_count_scaling": False,
                "use_pretrained_weights": False,
                "use_quantile_transformer": False,
                "budget": None,
                "metric": "mse",
                "n_ensembles": 1,
                "dim": 512,
                "n_layers": 12,
                "n_heads": 4,
                "dim_output": int(dim_output),
                # THE delta vs stock MitraRegressor, which hardcodes "mse" +
                # dim_output=1 and so cannot drive a binned v2 checkpoint.
                "regression_loss": (
                    LossName.CROSS_ENTROPY if binned else LossName.MSE
                ),
            },
        )
        cfg.task = Task.REGRESSION
        return cfg

    # -- fit ---------------------------------------------------------------
    def fit(self, X, y):
        api = _mitra_internals()

        device = _resolve_device(self.device)
        self.device_ = device
        self.encoder_ = _NumericEncoder()

        X_num = self.encoder_.fit_transform(pd.DataFrame(X))
        y_num = np.asarray(
            pd.to_numeric(pd.Series(np.asarray(y).ravel()), errors="coerce"),
            dtype="float32",
        )
        if X_num.shape[0] != y_num.shape[0]:
            raise ValueError(
                f"mitra: X has {X_num.shape[0]} rows but y has {y_num.shape[0]}"
            )
        finite = np.isfinite(y_num)
        if not finite.all():
            # Mitra min-max scales y; a NaN target would poison y_min/y_max.
            X_num, y_num = X_num[finite], y_num[finite]
        if y_num.size == 0:
            raise ValueError("mitra: no finite training targets")
        if float(y_num.min()) == float(y_num.max()):
            # Preprocessor.determine_mix_max_scale asserts on this; fail with
            # a message that names the model instead of a bare AssertionError.
            raise ValueError(
                "mitra: every training target is identical, so the min-max "
                "target scaling is undefined for this fold"
            )

        X_num = self._fit_feature_reduction(X_num, y_num)
        self.n_features_in_ = X_num.shape[1]
        if self.n_features_in_ > PRETRAIN_MAX_FEATURES:
            logger.info(
                f"mitra: {self.n_features_in_} features exceeds the "
                f"{PRETRAIN_MAX_FEATURES}-feature pretraining envelope "
                f"(paper Table 1); feature_selection = gOMP_medium keeps folds "
                f"inside it"
            )

        backbone = _load_backbone(self.hf_model, device, cache=not self.fine_tune)
        self.dim_output_ = int(backbone.dim_output)
        self.binned_ = self.dim_output_ > 1

        # The FULL fold is the in-context support at predict time, including
        # the rows a fine-tuning member held out for validation. That is the
        # released recipe's "heldout in support" rule, and for the zero-shot
        # arm it is simply all the training data.
        self.X_support_ = X_num
        self.y_support_ = y_num
        self.trainers_ = []

        for member in range(max(int(self.n_estimators), 1)):
            seed = int(self.seed) + member
            cfg = self._build_config(self.dim_output_, device)
            cfg.seed = seed

            if self.fine_tune:
                import copy

                model = copy.deepcopy(backbone)
            else:
                model = backbone

            trainer = api["TrainerFinetune"](
                cfg,
                model,
                n_classes=0,
                device=device,
                rng=np.random.RandomState(seed),
                verbose=bool(self.verbose),
            )
            # DatasetFinetune draws its support permutation from trainer.rng,
            # which ADVANCES on every predict -- so a second predict() on the
            # same fitted model reorders the in-context rows and, through
            # float summation order, shifts predictions by ~1e-4. Harmless in
            # isolation, but it would make the point estimate and the interval
            # disagree, and it makes permutation XAI noisy. Remember the seed
            # and reset the stream before every forward instead (the same fix
            # BNNYieldRegressor applies by reseeding per call).
            trainer._geocif_seed = seed

            with _numpy_seed(seed):
                if self.fine_tune:
                    # Upstream caveat: TrainerFinetune's `Checkpoint` snapshots
                    # weights with `state_dict()[k].to("cpu")`, which is a no-op
                    # returning the SAME tensor when the model is already on
                    # CPU -- so on CPU "restore the best epoch" restores the
                    # last epoch instead. Another reason to fine-tune on a GPU.
                    X_tr, y_tr, X_va, y_va = self._split(X_num, y_num, seed)
                    trainer.train(X_tr.copy(), y_tr.copy(), X_va.copy(), y_va.copy())
                else:
                    # Zero-shot: no gradient step, so skip TrainerFinetune.train
                    # entirely (it would burn a full validation forward pass and
                    # an O(n^2) index split for nothing) and fit only the
                    # preprocessor that predict() needs. `.copy()` because
                    # Preprocessor.fit imputes NaN into the array in place.
                    trainer.preprocessor.fit(X_num.copy(), y_num.copy())

            trainer.model.eval()
            # Frees the AdamW state, the LR schedulers and -- the reason this
            # matters -- TrainerFinetune's `Checkpoint`, which on CUDA holds a
            # full 307 MB CPU copy of the weights per member. predict() needs
            # only the preprocessor, cfg, bins and model, all of which survive.
            trainer.post_fit_optimize()
            self.trainers_.append(trainer)

        return self

    def _split(self, X: np.ndarray, y: np.ndarray, seed: int):
        """Deterministic train/validation split for the fine-tuning path.

        Replaces ``MitraBase._split_data``, which is O(n^2) (``i not in
        list``) and draws from the global RNG.
        """
        n = X.shape[0]
        n_val = int(np.clip(round(self.val_frac * n), 1, max(n - 1, 1)))
        order = np.random.RandomState(seed).permutation(n)
        val_idx, train_idx = order[:n_val], order[n_val:]
        if train_idx.size == 0:  # tiny fold: validate on the training rows
            train_idx, val_idx = order, order
        return X[train_idx], y[train_idx], X[val_idx], y[val_idx]

    def _fit_feature_reduction(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Train-only truncated SVD above ``max_features`` (paper §2.6)."""
        self.svd_ = None
        cap = int(self.max_features or 0)
        if cap <= 0 or X.shape[1] <= cap:
            return X

        from sklearn.decomposition import TruncatedSVD

        logger.warning(
            f"mitra: {X.shape[1]} features exceeds max_features={cap}; "
            f"reducing with a train-only truncated SVD. Prefer "
            f"feature_selection = gOMP_medium (<= {PRETRAIN_MAX_FEATURES} "
            f"features) over relying on this."
        )
        filled = self._nan_to_column_mean(X)
        n_components = int(min(cap, min(filled.shape) - 1))
        self.svd_ = TruncatedSVD(
            n_components=max(n_components, 1), random_state=int(self.seed)
        )
        return self.svd_.fit_transform(filled).astype("float32", copy=False)

    def _apply_feature_reduction(self, X: np.ndarray) -> np.ndarray:
        if getattr(self, "svd_", None) is None:
            return X
        return self.svd_.transform(self._nan_to_column_mean(X)).astype(
            "float32", copy=False
        )

    @staticmethod
    def _nan_to_column_mean(X: np.ndarray) -> np.ndarray:
        out = np.array(X, dtype="float64", copy=True)
        with np.errstate(invalid="ignore"), warnings.catch_warnings():
            # An all-NaN column is legitimate here (a CID absent for the whole
            # fold); nanmean warns, and the 0.0 fallback below is the answer.
            warnings.simplefilter("ignore", RuntimeWarning)
            means = np.nanmean(np.where(np.isfinite(out), out, np.nan), axis=0)
        means = np.where(np.isfinite(means), means, 0.0)
        bad = ~np.isfinite(out)
        if bad.any():
            out[bad] = np.take(means, np.where(bad)[1])
        return out

    # -- predict -----------------------------------------------------------
    def predict(self, X):
        """Point prediction: the MEAN of the predicted bin distribution.

        Stock AutoGluon returns the argmax bin centre instead; the mean is the
        released Mitra-v2 decode and the only quality-critical delta from
        stock (module docstring).
        """
        if self.binned_:
            edges, probs = self._predict_distribution(X)
            centres = 0.5 * (edges[:-1] + edges[1:])
            return (probs * centres[None, :]).sum(axis=1)
        return self._predict_scalar(X)

    def predict_distribution(self, X):
        """``(bin_edges (n_bins+1,), probabilities (n_rows, n_bins))``.

        Edges are in TARGET units. Only available for a binned (v2)
        checkpoint.
        """
        if not self.binned_:
            raise RuntimeError(
                "mitra: this checkpoint has a scalar regression head "
                f"(dim_output = {self.dim_output_}); predictive distributions "
                f"need the binned Mitra-v2 regressor ({MITRA_V2_REGRESSOR})"
            )
        return self._predict_distribution(X)

    def predict_quantiles(self, X, quantiles):
        """Quantiles of the predictive distribution, shape ``(n, len(q))``.

        Exact under the model's own piecewise-uniform-within-bin reading of
        the histogram, so ``predict_quantiles(X, [0.5])`` is the median while
        ``predict`` is the mean.
        """
        edges, probs = self.predict_distribution(X)
        return self._quantiles_from_histogram(edges, probs, np.asarray(quantiles, float))

    def predict_with_quantiles(self, X, quantiles):
        """``(mean, quantiles)`` from ONE forward pass over the query rows.

        The CI path needs both the point estimate and the interval bounds;
        calling ``predict`` and ``predict_quantiles`` separately would run the
        in-context transformer twice over the same rows, which at geocif's
        fold count is the difference between one run and two.
        """
        edges, probs = self.predict_distribution(X)
        centres = 0.5 * (edges[:-1] + edges[1:])
        mean = (probs * centres[None, :]).sum(axis=1)
        bounds = self._quantiles_from_histogram(
            edges, probs, np.asarray(quantiles, float)
        )
        return mean, bounds

    # -- internals ---------------------------------------------------------
    def _prepare_query(self, X) -> np.ndarray:
        X_num = self.encoder_.transform(pd.DataFrame(X))
        return self._apply_feature_reduction(X_num)

    def _autocast(self, device: str):
        dtype = _resolve_precision(self.precision, device)
        if dtype is None:
            return contextlib.nullcontext()
        import torch

        return torch.autocast(
            device_type="cuda" if str(device).startswith("cuda") else "cpu",
            dtype=getattr(torch, dtype),
        )

    def _forward(self, trainer, X_query: np.ndarray) -> np.ndarray:
        """One member's raw head output for the query rows.

        Reimplements ``TrainerFinetune.predict``'s loop because we need the
        pre-decode logits (for the distribution), and because every array
        handed to the preprocessor must be a private copy — ``transform_X``
        imputes NaN in place.
        """
        api = _mitra_internals()
        import torch

        cfg = trainer.cfg
        pre = trainer.preprocessor

        x_support = pre.transform_X(self.X_support_.copy())
        x_query = pre.transform_X(np.asarray(X_query, dtype="float32").copy())
        y_support = pre.transform_y(self.y_support_.copy())

        dataset = api["DatasetFinetune"](
            cfg,
            x_support=x_support,
            y_support=y_support,
            x_query=x_query,
            y_query=None,
            max_samples_support=cfg.hyperparams["max_samples_support"],
            max_samples_query=cfg.hyperparams["max_samples_query"],
            rng=trainer.rng,
        )
        loader = trainer.make_loader(dataset, training=False)
        trainer.model.eval()

        chunks = []
        with torch.no_grad():
            for batch in loader:
                with self._autocast(self.device_):
                    x_s = batch["x_support"].to(self.device_, non_blocking=True)
                    y_s = batch["y_support"].to(self.device_, non_blocking=True)
                    x_q = batch["x_query"].to(self.device_, non_blocking=True)
                    pad_f = batch["padding_features"].to(self.device_, non_blocking=True)
                    pad_s = batch["padding_obs_support"].to(
                        self.device_, non_blocking=True
                    )
                    pad_q = batch["padding_obs_query"].to(
                        self.device_, non_blocking=True
                    )

                    if self.binned_:
                        # Support labels enter the model as bin ids, exactly as
                        # TrainerFinetune does for a cross-entropy head.
                        y_s = torch.bucketize(y_s, trainer.bins) - 1
                        y_s = torch.clamp(y_s, 0, self.dim_output_ - 1).to(torch.int64)

                    y_hat = trainer.model(x_s, y_s, x_q, pad_f, pad_s, pad_q)

                chunks.append(y_hat[0].float().cpu())

        return torch.cat(chunks, dim=0).numpy()

    def _member_histogram(self, trainer, logits: np.ndarray):
        """One member's ``(edges_in_target_units, probabilities)``.

        ``trainer.bins`` lives in the NORMALISED target space; the stock
        inverse transform undoes an optional mirror (``y -> 1 - y``) and then
        the min-max scaling. Both are affine, so the edges map exactly — but
        the mirror REVERSES the grid, so the probabilities must be flipped
        with it to keep the edges ascending.
        """
        import torch

        scores = torch.as_tensor(logits, dtype=torch.float32)
        if not torch.isfinite(scores).all():
            scores = torch.nan_to_num(scores, nan=0.0, posinf=1e4, neginf=-1e4)
        probs = torch.softmax(scores, dim=-1).numpy().astype("float64")

        # trainer.bins is a float32 torch.linspace(-0.5, 1.5, n_bins + 1). Two
        # members' grids are equal in exact arithmetic (the grid is symmetric
        # about 0.5, so mirroring maps it onto itself) but NOT bit-for-bit once
        # float32 rounding and the mirror's `1 - e` reversal are applied --
        # which made the equal-grid check below fail for n_estimators > 1.
        # Rebuild the same grid in float64 and verify it against the tensor, so
        # every member lands on one canonical grid and the decode is exact.
        raw = trainer.bins.detach().to(device="cpu", dtype=torch.float64).numpy()
        edges = np.linspace(-0.5, 1.5, raw.size)
        if not np.allclose(edges, raw, rtol=0, atol=1e-4):
            raise RuntimeError(
                "mitra: the checkpoint's bin grid is not the expected "
                "linspace(-0.5, 1.5) over the normalised target; AutoGluon's "
                "TrainerFinetune binning has changed and the decode in "
                "ml/mitra.py must be updated"
            )
        pre = trainer.preprocessor
        mirrored = bool(getattr(pre, "random_mirror_regression", False)) and bool(
            getattr(pre, "regression_mirror", False)
        )
        if mirrored:
            edges = (1.0 - edges)[::-1]
            probs = probs[:, ::-1]

        y_min, y_max = float(pre.y_min), float(pre.y_max)
        edges = edges * (y_max - y_min) + y_min
        return np.ascontiguousarray(edges), np.ascontiguousarray(probs)

    def _reset_member_rngs(self):
        """Rewind every member's support-sampling stream so repeated predicts
        on the same fitted model return identical numbers."""
        for trainer in self.trainers_:
            trainer.rng = np.random.RandomState(int(trainer._geocif_seed))

    def _predict_distribution(self, X):
        self._reset_member_rngs()
        X_query = self._prepare_query(X)

        edges_ref = None
        stacked = None
        for trainer in self.trainers_:
            edges, probs = self._member_histogram(trainer, self._forward(trainer, X_query))
            if edges_ref is None:
                edges_ref, stacked = edges, probs
                continue
            # Every member scales y with the same y_min/y_max, and the bin grid
            # linspace(-0.5, 1.5) is symmetric about 0.5, so a mirrored member's
            # flipped grid coincides with the unmirrored one. Equal grids make
            # the bagged mixture a plain average of the probability vectors --
            # assert rather than assume.
            span = float(abs(edges_ref[-1] - edges_ref[0])) or 1.0
            if not np.allclose(edges, edges_ref, rtol=0, atol=1e-9 * span):
                raise RuntimeError(
                    "mitra: ensemble members produced different bin grids; the "
                    "mixture can no longer be averaged bin-wise"
                )
            stacked = stacked + probs

        probs = stacked / float(len(self.trainers_))
        total = probs.sum(axis=1, keepdims=True)
        probs = np.divide(probs, np.where(total > 0, total, 1.0))
        return edges_ref, probs

    def _predict_scalar(self, X):
        """Mitra-v1 fallback: a scalar head, decoded by the stock inverse
        transform (mirror + min-max)."""
        self._reset_member_rngs()
        X_query = self._prepare_query(X)
        preds = []
        for trainer in self.trainers_:
            raw = self._forward(trainer, X_query)
            preds.append(
                np.asarray(trainer.preprocessor.inverse_transform_y(raw.ravel()), float)
            )
        return np.mean(np.vstack(preds), axis=0)

    @staticmethod
    def _quantiles_from_histogram(edges, probs, quantiles):
        """Invert the piecewise-uniform CDF of each row's histogram.

        Mass inside a bin is treated as uniform, matching the model's own
        reading of its head (and the upstream ``RegressionDistribution``), so
        the result is exact rather than a bin-centre approximation.
        """
        edges = np.asarray(edges, dtype="float64")
        p = np.asarray(probs, dtype="float64")
        # Normalise HERE rather than trusting the caller: cdf and per-bin mass
        # must live on the same scale or the within-bin interpolation is off.
        totals = p.sum(axis=1, keepdims=True)
        p = np.divide(p, np.where(totals > 0, totals, 1.0))

        cdf = np.cumsum(p, axis=1)
        cdf[:, -1] = 1.0  # exact, so `cdf >= 1.0` always matches somewhere
        lower = np.concatenate([np.zeros((cdf.shape[0], 1)), cdf[:, :-1]], axis=1)
        widths = np.diff(edges)
        rows = np.arange(p.shape[0])

        out = np.empty((p.shape[0], len(quantiles)), dtype="float64")
        for j, q in enumerate(quantiles):
            q = float(np.clip(q, 0.0, 1.0))
            hit = cdf >= q
            idx = np.where(hit.any(axis=1), np.argmax(hit, axis=1), p.shape[1] - 1)
            mass = p[rows, idx]
            frac = np.where(
                mass > 0,
                (q - lower[rows, idx]) / np.where(mass > 0, mass, 1.0),
                0.0,
            )
            out[:, j] = edges[idx] + np.clip(frac, 0.0, 1.0) * widths[idx]
        return out
