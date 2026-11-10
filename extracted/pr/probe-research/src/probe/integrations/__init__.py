"""Optional stack integrations built on the Probe SDK."""

from probe.foundation.front_door.retired import make_retired_getattr

from .miles import QUEUE_RETIRED, MilesMetricBackend, MilesMetricTracker

__getattr__ = make_retired_getattr(__name__, dict.fromkeys(("DurableMetricQueue", "drain_miles_metric_queue"),
                                                           QUEUE_RETIRED))

__all__ = [
    "MilesMetricBackend",
    "MilesMetricTracker",
]
