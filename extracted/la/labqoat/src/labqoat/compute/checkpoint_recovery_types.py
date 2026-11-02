"""Supported recovery roles, continuation guarantees and inventoried state components."""

from typing import Literal

CheckpointRole = Literal["resumable-last", "validation-best", "inference-only", "final-training-state"]
CheckpointBoundary = Literal["optimizer-update", "epoch", "training-complete"]
CheckpointGuarantee = Literal["exact-continuation", "bounded-replay", "epoch-boundary"]
CheckpointState = Literal[
    "model",
    "optimizer",
    "scheduler",
    "ema",
    "amp_scaler",
    "rng_python",
    "rng_numpy",
    "rng_torch_cpu",
    "rng_torch_cuda",
    "data_cursor",
    "accumulation",
    "callbacks",
    "validation_best",
    "fit_clock",
    "completed_training",
]
