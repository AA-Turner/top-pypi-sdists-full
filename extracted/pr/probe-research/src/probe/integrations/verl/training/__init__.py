"""verl's per-sample training metrics (plan rl-trajectory-metrics T3): every value verl's actor loss computes per
sample, under verl's own names, with the loss bookkeeping that explains how each sample entered each optimizer update,
from the worker ranks (`training.py`); the driver's row ids and eval values (`driver.py`); the declaration
(`plan.py`). Nothing here imports verl or torch until a hook runs. Why: DESIGN.md "Per-sample training metrics"."""

from .driver import EvalPoints, stamp_update_batch
from .plan import UNSUPPORTED, build_critic_plan, build_training_plan, has_entropy_rows
from .training import PRODUCER_PREFIX, VerlTraining, get_training, install_worker_training

__all__ = [
    "PRODUCER_PREFIX",
    "UNSUPPORTED",
    "EvalPoints",
    "VerlTraining",
    "build_critic_plan",
    "build_training_plan",
    "has_entropy_rows",
    "get_training",
    "install_worker_training",
    "stamp_update_batch",
]
