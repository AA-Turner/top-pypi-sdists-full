"""
Empirical layer selection for Llama-3.2-1B truthfulqa_mc1 (real activations).

Replaces the arbitrary 'layer 12' choice with a measured sweep: for every
real layer blob, run the production NURT concept-subspace discovery and
compute contrastive separability = ||mean(pos_z) - mean(neg_z)|| / spread.

Outputs:
  ../zwiad_3d_outputs/real_layer_sweep_truthfulqa_mc1.png   (separability vs layer)
  ../zwiad_3d_outputs/real_best_layer_truthfulqa_mc1.png    (3D scatter, best layer)
"""
from __future__ import annotations

import sys
import types as _types
import importlib.util as _ilu
from pathlib import Path

import numpy as np
import torch
from safetensors import safe_open
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
sys.path.insert(0, str(_REPO))


def _stub(name: str):
    m = _types.ModuleType(name)
    sys.modules[name] = m
    return m


for n in ("wisent", "wisent.core", "wisent.core.utils",
          "wisent.core.utils.config_tools", "wisent.core.control",
          "wisent.core.control.steering_methods",
          "wisent.core.control.steering_methods.implementations",
          "wisent.core.control.steering_methods.implementations.methods",
          "wisent.core.control.steering_methods.implementations.methods.extended",
          "wisent.core.control.steering_methods.implementations.methods.extended.nurt"):
    _stub(n)
_c = sys.modules["wisent.core.utils.config_tools.constants"] = _types.ModuleType(
    "wisent.core.utils.config_tools.constants")
_c.LOG_EPS = 1e-9

_spec = _ilu.spec_from_file_location(
    "wisent.core.control.steering_methods.implementations.methods.extended.nurt.subspace",
    _REPO / "wisent/core/control/steering_methods/implementations/methods/extended/nurt/subspace.py",
)
_m = _ilu.module_from_spec(_spec)
sys.modules[_spec.name] = _m
_spec.loader.exec_module(_m)
discover_concept_subspace = _m.discover_concept_subspace
project_to_subspace = _m.project_to_subspace

_OUTDIR = _HERE.parent / "zwiad_3d_outputs"
_LAYERDIR = _OUTDIR / "layers_l1b_tqa"
_LAYERS = list(range(1, 16))


def _separability(pos: torch.Tensor, neg: torch.Tensor):
    Vh, S, k = discover_concept_subspace(
        pos, neg, variance_threshold=0.90, nurt_num_dims=0,
        nurt_max_concept_dim=64, min_concept_dim=3)
    pz = project_to_subspace(pos, Vh).cpu().numpy()
    nz = project_to_subspace(neg, Vh).cpu().numpy()
    cp, cn = pz.mean(axis=0), nz.mean(axis=0)
    sep = float(np.linalg.norm(cp - cn))
    spread = float(np.concatenate([pz, nz]).std(axis=0).mean())
    s_np = S.cpu().numpy()
    sv_conc = float((s_np[:3] ** 2).sum() / (s_np ** 2).sum())
    return sep / (spread + 1e-9), int(k), sv_conc, (pz, nz, cp, cn)


def main():
    rows = []
    best = None
    for L in _LAYERS:
        blob = _LAYERDIR / f"layer_{L}.safetensors"
        with safe_open(str(blob), framework="np") as f:
            pos = torch.from_numpy(f.get_tensor("pos_activations"))
            neg = torch.from_numpy(f.get_tensor("neg_activations"))
        ratio, k, sv_conc, proj = _separability(pos, neg)
        rows.append((L, ratio, k, sv_conc))
        if best is None or ratio > best[1]:
            best = (L, ratio, proj)
        print(f"layer {L:2d}  separability={ratio:6.3f}  k={k:2d}  sv_top3_frac={sv_conc:.3f}")

    Ls = [r[0] for r in rows]
    ratios = [r[1] for r in rows]
    best_L = best[0]
    print(f"\nBEST LAYER (measured, not guessed) = {best_L}  separability={best[1]:.3f}")
    print(f"(earlier arbitrary pick was layer 12: separability={ratios[Ls.index(12)]:.3f})")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(Ls, ratios, "o-", color="#d62728", lw=2)
    ax.axvline(best_L, color="green", ls="--", label=f"best = L{best_L}")
    ax.axvline(12, color="grey", ls=":", label="earlier guess = L12")
    ax.set_xlabel("layer"); ax.set_ylabel("separability (||Δmean|| / spread)")
    ax.set_title("Llama-3.2-1B truthfulqa_mc1 — contrastive separability per layer\n"
                 "(NURT concept subspace, REAL activations, 500 pairs/layer)")
    ax.set_xticks(Ls); ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(_OUTDIR / "real_layer_sweep_truthfulqa_mc1.png", dpi=130)
    plt.close(fig)

    pz, nz, cp, cn = best[2]
    fig = plt.figure(figsize=(8.5, 7.0))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(pz[:, 0], pz[:, 1], pz[:, 2], c="#d62728", s=12, alpha=0.55, label="pos (truthful)")
    ax.scatter(nz[:, 0], nz[:, 1], nz[:, 2], c="#1f77b4", s=12, alpha=0.55, label="neg (false)")
    ax.plot([cn[0], cp[0]], [cn[1], cp[1]], [cn[2], cp[2]], color="black", lw=3, label="concept direction")
    ax.scatter([cp[0], cn[0]], [cp[1], cn[1]], [cp[2], cn[2]], c="black", s=110, marker="X")
    ax.set_title(f"REAL Llama-3.2-1B truthfulqa_mc1 — BEST layer L{best_L} (measured)\n"
                 f"NURT concept subspace, separability={best[1]:.3f}")
    ax.set_xlabel("concept dim 1"); ax.set_ylabel("concept dim 2"); ax.set_zlabel("concept dim 3")
    ax.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig(_OUTDIR / "real_best_layer_truthfulqa_mc1.png", dpi=125)
    plt.close(fig)
    print(f"wrote real_layer_sweep_truthfulqa_mc1.png and real_best_layer_truthfulqa_mc1.png")


if __name__ == "__main__":
    main()
