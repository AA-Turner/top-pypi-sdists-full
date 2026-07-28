from __future__ import annotations

from typing import Any

_METER_NAME = "kytte.sdk.connectivity"
_GAUGE_NAME = "aigie.sdk.heartbeat"


def register_heartbeat_gauge(meter_provider: Any) -> None:
    """Register an observable gauge that reports 1 every export cycle while alive.

    Must be created eagerly (not lazily, unlike the judge instruments) —
    observable callbacks have to exist before the reader's first collection
    tick or the SDK never calls them.
    """
    from opentelemetry.metrics import Observation

    meter = meter_provider.get_meter(_METER_NAME)

    def _callback(_options: Any) -> list[Observation]:
        return [Observation(1)]

    meter.create_observable_gauge(
        _GAUGE_NAME,
        callbacks=[_callback],
        description="Emitted once per export cycle while the SDK process is alive",
        unit="1",
    )
