"""
LimiX-2 tabular foundation model for regional yield forecasting
(model = 'limix').

LimiX-2 (StableAI, released 2026-09-16; https://huggingface.co/stable-ai/LimiX-2)
is an in-context tabular foundation model covering classification, regression
and missing-value imputation with one 400M-parameter backbone. Like TabPFN and
Mitra it is *transductive*: there is no gradient step at fit time — the support
set (X_train, y_train) and the queries (X_test) are passed together in a single
forward pass.

    weights   stable-ai/LimiX-2   ->   LimiX-2.ckpt  (~1.63 GB)
    code      github.com/limix-ldm-ai/LimiX

LICENSE — READ BEFORE USING RESULTS
-----------------------------------
The *weights* are released under the **StableAI LimiX Non-Commercial License
v1.0**: commercial use is prohibited. (The code is Apache-2.0 with added
attribution/naming clauses, but the checkpoint is not.) geocif treats this the
same way as `causilo`: fine for research evaluation and papers, NOT for an
operational or commercial forecast product. Anything quoted from a `limix` run
must carry that caveat.

WHY THIS MODULE EXISTS RATHER THAN A ONE-LINE trainers.py BRANCH
----------------------------------------------------------------
Three practical reasons, all of which would otherwise leak into trainers.py:

1. **LimiX is not sklearn-shaped.** Its entry point is
   ``LimiXPredictor.predict(X_train, y_train, X_test, task_type="Regression")``
   — one call taking both the support set and the queries. geocif's trainers
   expect ``fit(X, y)`` then ``predict(X)``, so `fit` here only *stores* the
   support set and `predict` performs the forward pass.

2. **It needs its own interpreter.** LimiX declares
   ``requires-python = ">=3.12"`` and expects a CUDA device; the production
   pixi env is Python 3.11 with CPU-only torch. A `limix` run therefore has to
   go through the side env at ``/gpfs/data1/cmongp1/ritvik/limix_env`` on a GPU
   node (gsappx1/x3/x4) — see ``~/run_limix.sh``. Importing this module in the
   production env raises a clear error rather than a bare ImportError.

3. **The released package has a hardcoded cache path.**
   ``inference/v2_0/predictor.py`` constructs its CacheManager with a
   developer-local directory (``/mnt/public/...``) that does not exist off
   their machine, so a stock clone dies with ``PermissionError`` before the
   first prediction. Our clone is patched to honour ``LIMIX_CACHE_DIR``; this
   module sets that variable defensively so an unpatched clone still works if
   the directory happens to be writable.

Envelope: geocif LOOCV folds are small (tens of regions x ~10-25 years, and
``feature_selection = gOMP_medium`` caps the matrix at ~50-100 columns), which
sits well inside any in-context context limit. No subsampling is applied.
"""

from __future__ import annotations

import logging
import os

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Repo default; overridable via [limix] limix_root or $LIMIX_ROOT.
LIMIX_ROOT_DEFAULT = "/gpfs/data1/cmongp1/ritvik/LimiX"
LIMIX_REPO_ID = "stable-ai/LimiX-2"
LIMIX_CKPT_NAME = "LimiX-2.ckpt"
LIMIX_REG_CONFIG = os.path.join("config", "reg_default_noretrieval_v2.json")


def _resolve_device(device: str) -> str:
    import torch

    if device and device != "auto":
        return device
    return "cuda" if torch.cuda.is_available() else "cpu"


# ---------------------------------------------------------------------------
# Process-wide predictor cache.
#
# geocif builds a FRESH model object for every (fold, stage, region) task, so
# a per-instance predictor would re-load the 1.63 GB checkpoint onto the GPU
# each time. The backbone is frozen and carries no per-fold state — the
# support set is passed in at predict() — so one resident predictor serves
# every fold. Without this, a Kenya run climbed to 22.1 GB of the RTX 6000's
# 23.0 GB within four folds and was heading for an OOM kill.
#
# Keyed on (checkpoint, config, device); only ONE predictor is kept, since
# a run never mixes checkpoints. Holding the reference here (not on the
# instance) is what lets the per-fold objects be garbage collected.
# ---------------------------------------------------------------------------
_PREDICTOR_CACHE: dict = {}
_CKPT_CACHE: dict = {}


def _cached_predictor(key, build):
    hit = _PREDICTOR_CACHE.get(key)
    if hit is not None:
        return hit
    if _PREDICTOR_CACHE:
        _PREDICTOR_CACHE.clear()
        try:
            import gc
            import torch

            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:  # pragma: no cover - best-effort VRAM release
            pass
    predictor = build()
    _PREDICTOR_CACHE[key] = predictor
    return predictor


def _limix_api(limix_root: str):
    """Import LimiXPredictor, adding the repo to sys.path if pip -e didn't.

    Raises a message that names the side env rather than a bare ImportError,
    because the usual cause is running in the 3.11 production env.
    """
    import sys

    # LimiX's torch.distributed init reads these; it is a single-process run.
    os.environ.setdefault("RANK", "0")
    os.environ.setdefault("WORLD_SIZE", "1")
    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    os.environ.setdefault("MASTER_PORT", "29500")

    try:
        from inference.predictor import LimiXPredictor  # noqa: F401
    except ImportError:
        if limix_root and os.path.isdir(limix_root) and limix_root not in sys.path:
            sys.path.insert(0, limix_root)
        try:
            from inference.predictor import LimiXPredictor  # noqa: F811
        except ImportError as exc:
            raise ImportError(
                "model = 'limix' needs the LimiX package (requires-python "
                ">=3.12 + CUDA), which is NOT in the production pixi env "
                "(Python 3.11, CPU torch). Run it from the side env on a GPU "
                "node: /gpfs/data1/cmongp1/ritvik/limix_env via ~/run_limix.sh "
                f"(looked for the repo at {limix_root!r}). Original: {exc}"
            ) from exc
    from inference.predictor import LimiXPredictor  # noqa: F811

    return LimiXPredictor


class LimiXYieldRegressor:
    """LimiX-2 in-context regressor, sklearn-shaped for geocif.

    Parameters
    ----------
    limix_root
        Checkout of github.com/limix-ldm-ai/LimiX (supplies the inference
        config JSONs). Defaults to ``LIMIX_ROOT_DEFAULT`` / ``$LIMIX_ROOT``.
    model_path
        Local ``.ckpt``. When empty the checkpoint is pulled from the HF Hub
        (``stable-ai/LimiX-2``) into ``cache_dir`` and reused thereafter.
    inference_config
        Path to a LimiX inference-config JSON, or a name relative to
        ``limix_root``. Defaults to the released no-retrieval regression
        recipe.
    device
        ``"auto"`` picks cuda when available, else cpu. LimiX is designed for
        GPU; cpu works but is very slow.
    seed
        Recorded for reproducibility. LimiX's released regression recipe is
        deterministic given the config, so this does not reseed the backbone.

    Not implemented: CLASSIFICATION — geocif's classification path has never
    worked end to end (see the classification-mode note in the docs), and the
    task would need a different inference config.
    """

    def __init__(
        self,
        limix_root: str = "",
        model_path: str = "",
        inference_config: str = "",
        device: str = "auto",
        cache_dir: str = "",
        seed: int = 0,
        verbose: bool = False,
    ) -> None:
        self.limix_root = limix_root or os.environ.get("LIMIX_ROOT", LIMIX_ROOT_DEFAULT)
        self.model_path = model_path
        self.inference_config = inference_config
        self.device = device
        self.cache_dir = cache_dir or os.environ.get(
            "LIMIX_CACHE_DIR", "/gpfs/data1/cmongp1/ritvik/limix_cache"
        )
        self.seed = int(seed)
        self.verbose = verbose
        self._predictor = None

    # ------------------------------------------------------------------
    def _resolve_checkpoint(self) -> str:
        if self.model_path and os.path.isfile(self.model_path):
            return self.model_path
        # Memoised: geocif instantiates the model per fold, and an
        # un-memoised hf_hub_download issues an HTTP HEAD to the Hub every
        # time — thousands of needless round-trips over a run, and a hard
        # failure if the Hub is unreachable mid-run.
        cached = _CKPT_CACHE.get(self.cache_dir)
        if cached:
            return cached
        from huggingface_hub import hf_hub_download

        local_dir = os.path.join(self.cache_dir, "ckpt")
        path = hf_hub_download(
            repo_id=LIMIX_REPO_ID, filename=LIMIX_CKPT_NAME, local_dir=local_dir
        )
        logger.info(f"limix: checkpoint {path}")
        _CKPT_CACHE[self.cache_dir] = path
        return path

    def _resolve_config(self) -> str:
        cfg = self.inference_config or LIMIX_REG_CONFIG
        if not os.path.isabs(cfg):
            cfg = os.path.join(self.limix_root, cfg)
        if not os.path.isfile(cfg):
            raise FileNotFoundError(
                f"limix: inference config not found at {cfg}. Set [limix] "
                "limix_root to the LimiX checkout, or inference_config to an "
                "absolute path."
            )
        return cfg

    def _build(self):
        import torch

        LimiXPredictor = _limix_api(self.limix_root)
        # Patched upstream call site reads this; harmless if already set.
        os.environ.setdefault("LIMIX_CACHE_DIR", self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)

        device = _resolve_device(self.device)
        self.device_ = device
        if device == "cpu":
            logger.warning(
                "limix: no CUDA device — running the 400M backbone on CPU is "
                "very slow. Launch on a GPU node (gsappx1/x3/x4)."
            )
        ckpt = self._resolve_checkpoint()
        cfg = self._resolve_config()
        return _cached_predictor(
            (ckpt, cfg, device),
            lambda: LimiXPredictor(
                device=torch.device(device),
                model_path=ckpt,
                inference_config=cfg,
            ),
        )

    # ------------------------------------------------------------------
    def fit(self, X, y):
        """Store the support set. LimiX is in-context — no gradient step here.

        Mirrors the hygiene in ml/mitra.py: numeric-encode the frame, drop
        rows whose target is not finite, and fail with a model-named message
        on a degenerate target rather than deep inside the backbone.
        """
        from .mitra import _NumericEncoder

        self.encoder_ = _NumericEncoder()
        X_num = self.encoder_.fit_transform(pd.DataFrame(X))
        y_num = np.asarray(
            pd.to_numeric(pd.Series(np.asarray(y).ravel()), errors="coerce"),
            dtype="float32",
        )
        if X_num.shape[0] != y_num.shape[0]:
            raise ValueError(
                f"limix: X has {X_num.shape[0]} rows but y has {y_num.shape[0]}"
            )
        finite = np.isfinite(y_num)
        if not finite.all():
            X_num, y_num = X_num[finite], y_num[finite]
        if y_num.size == 0:
            raise ValueError("limix: no finite training targets")
        if float(y_num.min()) == float(y_num.max()):
            raise ValueError(
                "limix: all training targets are identical — the in-context "
                "target scaler cannot normalise a zero-range support set."
            )

        self.X_train_ = np.ascontiguousarray(X_num, dtype="float32")
        self.y_train_ = y_num
        self.n_features_in_ = self.X_train_.shape[1]
        if self._predictor is None:
            self._predictor = self._build()
        return self

    def predict(self, X):
        """Forward pass over (support set, queries). Returns a 1-D array."""
        if self._predictor is None:
            raise RuntimeError("limix: predict() called before fit()")
        X_num = np.ascontiguousarray(
            self.encoder_.transform(pd.DataFrame(X)), dtype="float32"
        )
        if X_num.shape[1] != self.n_features_in_:
            raise ValueError(
                f"limix: fit saw {self.n_features_in_} features, predict got "
                f"{X_num.shape[1]}"
            )
        preds = self._predictor.predict(
            self.X_train_, self.y_train_, X_num, task_type="Regression"
        )
        return np.asarray(preds, dtype="float64").ravel()
