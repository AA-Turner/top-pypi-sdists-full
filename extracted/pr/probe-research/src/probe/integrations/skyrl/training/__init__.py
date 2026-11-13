"""SkyRL's per-sample training metrics (plan rl-trajectory-metrics T3): every value SkyRL's policy loss computes per
sample, under SkyRL's own names, with the loss bookkeeping that explains how each sample entered each optimizer
update, from the policy worker ranks (`training.py`, reached through the job's Ray setup hook, `setup.py`); the
training task's row ids, scales and eval rewards (`driver.py`); the declaration (`plan.py`). Nothing here imports
SkyRL or torch until a hook runs. Why: DESIGN.md "Per-sample training metrics"."""

from .driver import EvalPoints, build_eval_rows, clear_stamps, setup_trainer_wraps, stamp_training_keys
from .plan import UNSUPPORTED, build_training_plan
from .setup import SETUP_HOOK, add_setup_hook, setup_worker
from .training import PRODUCER_PREFIX, SkyrlTraining, get_training, install_worker_training

__all__ = [
    "PRODUCER_PREFIX",
    "SETUP_HOOK",
    "UNSUPPORTED",
    "EvalPoints",
    "SkyrlTraining",
    "add_setup_hook",
    "build_eval_rows",
    "build_training_plan",
    "clear_stamps",
    "get_training",
    "install_worker_training",
    "setup_trainer_wraps",
    "setup_worker",
    "stamp_training_keys",
]
