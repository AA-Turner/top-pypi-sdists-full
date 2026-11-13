"""Per-sample metrics (DESIGN.md "Per-sample metrics"): `PointWriter` behind `run.samples.log_metrics`,
`log_metrics_many` and `log_update`; `summarize_rows`, a loss hook's per-token tensors as per-row values, weights and
contributions; and what every RL adapter's training hook shares: `watch_import` (wrap a module as it loads in a
worker), `UpdateLog` (one rank's update as rows and records), `copy_to_host` (one device-to-host copy a
micro-batch), `PointsSender` (join and send off the training thread) and `TrainingGuard` (fail open). No fixed list
of metric names anywhere."""

from .guard import TrainingGuard
from .host import HostTable, copy_to_host
from .imports import watch_import
from .points import PointWriter
from .sender import PointsSender
from .tensors import RowSummary, summarize_rows
from .updates import (
    NON_FINITE_SKIP,
    MicroBatchCapture,
    RowCapture,
    Share,
    UpdateLog,
    UpdatePlace,
    get_lowest_dtype,
    get_optimizer_step,
    keep_finite,
    to_float,
)

__all__ = [
    "NON_FINITE_SKIP",
    "HostTable",
    "MicroBatchCapture",
    "PointWriter",
    "PointsSender",
    "RowCapture",
    "RowSummary",
    "Share",
    "TrainingGuard",
    "UpdateLog",
    "UpdatePlace",
    "copy_to_host",
    "get_lowest_dtype",
    "get_optimizer_step",
    "keep_finite",
    "summarize_rows",
    "to_float",
    "watch_import",
]
