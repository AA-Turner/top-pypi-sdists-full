"""Probe for distributed Miles runs (front door; layout in DESIGN.md): the tracking backend and the sample hooks."""

from probe.foundation.front_door.retired import make_retired_getattr, retire_modules
from probe.integrations.miles.miles import (
    MilesMetricBackend,
    MilesMetricTracker,
    ProbeBackend,
    ProbeTracker,
)
from probe.integrations.miles.samples import (
    log_dropped_samples,
    log_eval_samples,
    log_samples,
    make_log_samples,
)

# The per-sample hook's old names, now writing samples (labeled points retired, W16).
per_sample_rollout_log = log_samples
make_per_sample_rollout_log = make_log_samples

#: The retired metric queue (RL plan W16), gone after its one release (rl-next W50): what to use instead.
QUEUE_RETIRED = ("the Miles metric queue was retired: new runs send through each process's own outbox; drain a queue "
                 "an older job left with CLI 0.469.0 (`python -m probe.integrations.miles` prints the command)")
RETIRED_NAMES = {
    **dict.fromkeys(("DurableMetricQueue", "QUEUE_SCHEMA_VERSION", "drain_metric_queue", "drain_miles_metric_queue",
                     "queue", "exporter"), QUEUE_RETIRED),
    "planned_labeled_points": "a Miles run plans no labeled points (per-sample numbers are samples): drop the call",
}
retire_modules({f"{__name__}.queue": QUEUE_RETIRED, f"{__name__}.exporter": QUEUE_RETIRED})
__getattr__ = make_retired_getattr(__name__, RETIRED_NAMES)

__all__ = [
    "MilesMetricBackend",
    "MilesMetricTracker",
    "ProbeBackend",
    "ProbeTracker",
    "log_dropped_samples",
    "log_eval_samples",
    "log_samples",
    "make_log_samples",
    "make_per_sample_rollout_log",
    "per_sample_rollout_log",
]
