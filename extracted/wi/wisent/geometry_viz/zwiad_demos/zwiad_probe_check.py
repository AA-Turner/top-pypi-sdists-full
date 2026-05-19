"""
Honest separability check on REAL Llama-3.2-1B truthfulqa_mc1 L8 activations.

The diff-of-means projection looked weak (Cohen d 1.45, 75% threshold acc).
Is that the data or the crude discriminator? Measure properly:
  - 5-fold CV logistic-regression probe on raw 2048-dim activations
  - 5-fold CV LDA
  - diff-of-means baseline (what the earlier demo used)
  - permuted-label control (chance baseline)

Source: ../zwiad_3d_outputs/layers_l1b_tqa/layer_8.safetensors  (real, no synthetic)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from safetensors import safe_open
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score, StratifiedKFold


_HERE = Path(__file__).resolve().parent
_BLOB = _HERE.parent / "zwiad_3d_outputs" / "layers_l1b_tqa" / "layer_8.safetensors"
_SEED = 42


def main():
    with safe_open(str(_BLOB), framework="np") as f:
        pos = f.get_tensor("pos_activations").astype(np.float64)
        neg = f.get_tensor("neg_activations").astype(np.float64)
    X = np.concatenate([pos, neg], axis=0)
    y = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    print(f"REAL truthfulqa_mc1 L8: X{X.shape} y(pos={int(y.sum())}, neg={int((1-y).sum())})")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=_SEED)

    lr = LogisticRegression(max_iter=2000, C=1.0)
    lr_scores = cross_val_score(lr, X, y, cv=cv, scoring="accuracy")
    print(f"LogReg probe (raw 2048-d): folds={[round(s,3) for s in lr_scores]}  "
          f"mean={lr_scores.mean():.3f} ± {lr_scores.std():.3f}")

    lda = LinearDiscriminantAnalysis()
    lda_scores = cross_val_score(lda, X, y, cv=cv, scoring="accuracy")
    print(f"LDA            (raw 2048-d): folds={[round(s,3) for s in lda_scores]}  "
          f"mean={lda_scores.mean():.3f} ± {lda_scores.std():.3f}")

    # diff-of-means baseline (what the earlier subspace demo used)
    accs = []
    for tr, te in cv.split(X, y):
        d = X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)
        d /= np.linalg.norm(d) + 1e-9
        s_tr = X[tr] @ d
        thr = 0.5 * (s_tr[y[tr] == 1].mean() + s_tr[y[tr] == 0].mean())
        s_te = X[te] @ d
        pred = (s_te > thr).astype(float)
        accs.append((pred == y[te]).mean())
    print(f"diff-of-means  (earlier demo): folds={[round(a,3) for a in accs]}  "
          f"mean={np.mean(accs):.3f} ± {np.std(accs):.3f}")

    rng = np.random.RandomState(_SEED)
    y_perm = rng.permutation(y)
    perm_scores = cross_val_score(lr, X, y_perm, cv=cv, scoring="accuracy")
    print(f"LogReg permuted-label control: mean={perm_scores.mean():.3f} "
          f"(chance baseline ~0.50)")

    _probe_production_zwiad_step2(pos, neg)


def _probe_production_zwiad_step2(pos_np, neg_np):
    """Call the PRODUCTION Zwiad Step-2 path exactly as zwiad_protocol.test_geometry does.

    test_geometry (zwiad_protocol.py:101) calls:
        test_linearity(pos, neg, diagnostics_total_checks=...)
    but test_linearity declares 9 keyword-only params with NO defaults
    (cv_folds, gap_threshold, p_threshold, residual_threshold,
     ramsey_threshold, n_bootstrap, linearity_confidence_high/low,
     linearity_cross_context_threshold). This reproduces that exact call on
     REAL L8 activations to record what Zwiad Step-2 actually does at runtime.
    """
    import sys
    import types
    import importlib.util
    from pathlib import Path
    import torch

    repo = Path(__file__).resolve().parent.parent.parent

    def _stub(n):
        m = types.ModuleType(n)
        sys.modules[n] = m
        return m

    for n in ("wisent", "wisent.core", "wisent.core.utils",
              "wisent.core.utils.config_tools", "wisent.core.reading",
              "wisent.core.reading.modules", "wisent.core.reading.modules.modules",
              "wisent.core.reading.modules.modules.geo_utils",
              "wisent.core.reading.modules.utilities",
              "wisent.core.reading.modules.utilities.signal_analysis"):
        _stub(n)
    # Real constant values, read from
    # wisent/core/utils/config_tools/constants (validated/_validated.py,
    # cannot_be_optimized/_infrastructure.py) — not guessed.
    c = sys.modules["wisent.core.utils.config_tools.constants"] = types.ModuleType(
        "wisent.core.utils.config_tools.constants")
    c.ZERO_THRESHOLD = 1e-10
    c.DEFAULT_RANDOM_SEED = 42
    c.CONFIDENCE_LEVEL = 0.95
    c.N_COMPONENTS_2D = 2
    c.ROUNDING_PRECISION = 3
    c.STAT_ALPHA = 0.05
    c.DIAGNOSTICS_TOTAL_CHECKS = 4
    c.LOG_EPS = 1e-12
    # Recovered canonical LINEARITY_* values (validated/_validated.py),
    # the same constants zwiad_protocol.test_geometry now threads through.
    c.LINEARITY_GAP_THRESHOLD = 0.05
    c.LINEARITY_P_THRESHOLD = 0.05
    c.LINEARITY_RESIDUAL_THRESHOLD = 0.3
    c.LINEARITY_RAMSEY_THRESHOLD = 0.03
    c.LINEARITY_N_BOOTSTRAP = 30
    c.LINEARITY_CV_FOLDS = 5
    c.LINEARITY_CONFIDENCE_HIGH = 0.8
    c.LINEARITY_CONFIDENCE_LOW = 0.2
    c.LINEARITY_CROSS_CONTEXT_THRESHOLD = 0.7

    luf = repo / "wisent/core/reading/modules/modules/geo_utils/linearity_utils.py"
    sp = importlib.util.spec_from_file_location(
        "wisent.core.reading.modules.modules.geo_utils.linearity_utils", luf)
    lm = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = lm
    sp.loader.exec_module(lm)

    ilf = repo / "wisent/core/reading/modules/utilities/signal_analysis/is_linear.py"
    sp2 = importlib.util.spec_from_file_location(
        "wisent.core.reading.modules.utilities.signal_analysis.is_linear", ilf)
    im = importlib.util.module_from_spec(sp2)
    sys.modules[sp2.name] = im
    try:
        sp2.loader.exec_module(im)
    except Exception as e:
        print(f"\n[PRODUCTION Zwiad Step-2] is_linear import FAILED: "
              f"{type(e).__name__}: {e}")
        return

    pos_t = torch.from_numpy(pos_np.astype("float32"))
    neg_t = torch.from_numpy(neg_np.astype("float32"))
    print("\n[PRODUCTION Zwiad Step-2] reproducing FIXED zwiad_protocol."
          "test_geometry call: test_linearity(pos, neg, "
          "diagnostics_total_checks=4, + 9 threaded LINEARITY_* params)")
    try:
        r = im.test_linearity(
            pos_t, neg_t, diagnostics_total_checks=4,
            cv_folds=c.LINEARITY_CV_FOLDS,
            gap_threshold=c.LINEARITY_GAP_THRESHOLD,
            p_threshold=c.LINEARITY_P_THRESHOLD,
            residual_threshold=c.LINEARITY_RESIDUAL_THRESHOLD,
            ramsey_threshold=c.LINEARITY_RAMSEY_THRESHOLD,
            n_bootstrap=c.LINEARITY_N_BOOTSTRAP,
            linearity_confidence_high=c.LINEARITY_CONFIDENCE_HIGH,
            linearity_confidence_low=c.LINEARITY_CONFIDENCE_LOW,
            linearity_cross_context_threshold=c.LINEARITY_CROSS_CONTEXT_THRESHOLD,
        )
        print(f"  SUCCEEDED: diagnosis={r.diagnosis} "
              f"linear_acc={r.linear_accuracy:.3f} "
              f"nonlinear_acc={r.nonlinear_accuracy:.3f} gap={r.gap:.3f} "
              f"ramsey_sig={r.ramsey_significant} "
              f"resid_cluster={r.residuals_cluster}")
    except TypeError as e:
        print(f"  RAISED TypeError (production bug): {e}")
    except Exception as e:
        print(f"  RAISED {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
