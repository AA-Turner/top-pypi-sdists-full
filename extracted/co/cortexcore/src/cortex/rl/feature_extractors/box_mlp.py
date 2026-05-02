from __future__ import annotations

import math

import torch
import torch.nn as nn

from cortex.rl.feature_extractors.config import BoxMLPFeatureExtractorConfig


class BoxMLPFeatureExtractor(nn.Module):
    def __init__(self, config: BoxMLPFeatureExtractorConfig, *, input_shape: tuple[int, ...]) -> None:
        super().__init__()
        self.config = config

        input_dim = math.prod(int(dim) for dim in input_shape)
        if input_dim <= 0:
            raise ValueError(f"Box MLP extractor requires a positive input size, got input_shape={input_shape}")

        layers: list[nn.Module] = []
        in_features = int(input_dim)
        for hidden_features in config.hidden_features:
            out_features = int(hidden_features)
            layers.extend([nn.Linear(in_features, out_features), nn.ReLU()])
            in_features = out_features
        layers.append(nn.Linear(in_features, int(config.output_dim)))
        self.network = nn.Sequential(*layers)

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        return self.network(observations.reshape(observations.shape[0], -1))


__all__ = ["BoxMLPFeatureExtractor"]
