from __future__ import annotations

import torch.nn as nn


def make_mlp(in_features: int, hidden_features: int, out_features: int) -> nn.Sequential:
    return nn.Sequential(
        nn.LayerNorm(in_features),
        nn.Linear(in_features, hidden_features),
        nn.SiLU(),
        nn.Linear(hidden_features, out_features),
    )


__all__ = ["make_mlp"]
