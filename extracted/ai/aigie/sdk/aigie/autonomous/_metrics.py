"""OTel metric instruments for the autonomous pipeline.

All instruments are created lazily via register(runtime) called from
AutonomousRuntime.start(). Observable gauges reference live objects on runtime
so they reflect current state without polling overhead.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import aigie.telemetry as _telemetry

if TYPE_CHECKING:
    from aigie.autonomous.runtime import AutonomousRuntime

# Module-level meter — instruments are registered per runtime instance.
_meter = _telemetry.get_meter("aigie.autonomous")

# Eagerly created counters/histograms used by module-level hot paths.
directives_applied = _meter.create_counter(
    "aigie.autonomous.directives.applied",
    description="Directives applied, by action_type and source.",
)

outcomes_reported = _meter.create_counter(
    "aigie.autonomous.outcomes.reported",
    description="Outcome reports enqueued, by status.",
)

stream_reconnects_total = _meter.create_counter(
    "aigie.autonomous.stream.reconnects_total",
    description="Total gRPC stream reconnection attempts.",
)

config_fetches = _meter.create_counter(
    "aigie.autonomous.config.fetches",
    description="Config fetch attempts, by result (changed|unchanged|error).",
)


def register(runtime: AutonomousRuntime) -> None:
    """Register observable gauges that reference live runtime objects.

    Called once from AutonomousRuntime.start() after subsystems are wired up.
    Observable gauge callbacks must not raise.
    """
    meter = _telemetry.get_meter("aigie.autonomous")

    def _queue_depth_callback(options: Any) -> Any:
        try:
            from opentelemetry.metrics import Observation

            return [Observation(runtime.outcome_reporter.queue_size())]
        except Exception:
            return []

    def _flow_cache_size_callback(options: Any) -> Any:
        try:
            from opentelemetry.metrics import Observation

            return [Observation(len(runtime.flow_cache))]
        except Exception:
            return []

    def _stream_connected_callback(options: Any) -> Any:
        try:
            from opentelemetry.metrics import Observation

            connected = 1 if runtime.control_stream.is_connected() else 0
            return [Observation(connected)]
        except Exception:
            return []

    meter.create_observable_gauge(
        "aigie.autonomous.outcomes.queue_depth",
        callbacks=[_queue_depth_callback],
        description="Current number of buffered outcome reports.",
    )

    meter.create_observable_gauge(
        "aigie.autonomous.config.flow_cache_size",
        callbacks=[_flow_cache_size_callback],
        description="Current number of flows in the flow cache.",
    )

    meter.create_observable_gauge(
        "aigie.autonomous.stream.connected",
        callbacks=[_stream_connected_callback],
        description="1 if the gRPC control stream is connected, 0 otherwise.",
    )
