from __future__ import annotations

import threading
import time
import typing as t
from datetime import datetime, timedelta

from dbt_state.adapters.base import BaseAdapterExtension
from dbt_state import events


class EngineHeuristicsClock:
    def __init__(self, adapter_ext: BaseAdapterExtension) -> None:
        self._adapter_ext = adapter_ext
        self._measurement_start_ts: t.Optional[float] = None
        self._initial_timestamp_utc: t.Optional[datetime] = None
        self._lock = threading.Lock()

    def now_utc(self) -> datetime:
        """Get the current timestamp in UTC inferred from the database engine's clock.

        This method uses a monotonic clock to measure elapsed time since the initial timestamp was recorded,

        Returns:
            The current timestamp in UTC inferred from the database engine's clock.
        """

        if self._measurement_start_ts is not None and self._initial_timestamp_utc is not None:
            return self._infer_now_utc()

        with self._lock:
            if self._measurement_start_ts is None or self._initial_timestamp_utc is None:
                # Query the current timestamp to make sure that the connection is established so that
                # the overhead of connection setup is not included in the subsequent clock measurements
                self._adapter_ext.current_timestamp_utc()

                self._measurement_start_ts = time.monotonic()
                self._initial_timestamp_utc = self._adapter_ext.current_timestamp_utc()
                read_time = time.monotonic() - self._measurement_start_ts
                events.fire_debug_event(
                    "Engine clock read time: {}s, engine timestamp: {}",
                    read_time,
                    str(self._initial_timestamp_utc),
                )

            return self._infer_now_utc()

    def now_utc_epoch(self) -> int:
        """The same as now_utc() except as a millisecond epoch, useful for comparing against last_modified epochs"""
        return int(self.now_utc().timestamp() * 1000)

    def _infer_now_utc(self) -> datetime:
        assert self._initial_timestamp_utc is not None
        assert self._measurement_start_ts is not None
        elapsed = time.monotonic() - self._measurement_start_ts
        return self._initial_timestamp_utc + timedelta(seconds=elapsed)
