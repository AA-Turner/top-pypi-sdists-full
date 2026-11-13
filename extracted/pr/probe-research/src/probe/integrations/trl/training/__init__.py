"""Per-sample training metrics for a TRL trainer (plan rl-trajectory-metrics T4, DESIGN.md): every loss term and
diagnostic TRL computes per sample, inside each optimizer update (train) and `evaluate()` pass (eval), under TRL's own
names, with the loss bookkeeping that explains each sample's share of the loss TRL returned."""

from .training import PRODUCER_PREFIX, TrainingRecorder

__all__ = ["PRODUCER_PREFIX", "TrainingRecorder"]
