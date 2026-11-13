"""Miles' per-sample training metrics (plan rl-trajectory-metrics T5): every value Miles' policy loss reduces per
sample, under Miles' own `train/<name>` keys, with the loss bookkeeping that explains how each sample entered each
optimizer update, from every data- and context-parallel train rank (`training.py`); the micro-batch row stamp
(`stamp.py`); the declaration (`plan.py`). Nothing here imports Miles or torch until a hook runs. Why: DESIGN.md
"Per-sample training metrics"."""

from typing import Any

from .plan import UNSUPPORTED, Unsupported, build_training_plan, get_unsupported_reason
from .stamp import ROWS_FIELD, RowStamp, install_stamp, read_stamp
from .training import TRAINING, MilesTraining


def install_objective(module: Any) -> None:
    """`samples/wraps.py`: Miles' loss module loaded here."""
    TRAINING.install_objective(module)


def install_torch_native(module: Any) -> None:
    """`samples/wraps.py`: the torch-native actor (FSDP, torchtitan) loaded here."""
    TRAINING.install_torch_native(module)


def install_megatron(module: Any) -> None:
    """`samples/wraps.py`: Megatron's model module loaded here."""
    TRAINING.install_megatron(module)


__all__ = [
    "ROWS_FIELD",
    "TRAINING",
    "UNSUPPORTED",
    "MilesTraining",
    "RowStamp",
    "Unsupported",
    "build_training_plan",
    "get_unsupported_reason",
    "install_megatron",
    "install_objective",
    "install_stamp",
    "install_torch_native",
    "read_stamp",
]
