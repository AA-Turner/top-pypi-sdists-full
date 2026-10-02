from __future__ import annotations

import threading
import time
from datetime import datetime, timezone

_lock = threading.Lock()
_last_timestamp_us = 0


def now_iso_timestamp() -> str:
    global _last_timestamp_us
    wall_clock_us = time.time_ns() // 1_000
    with _lock:
        _last_timestamp_us = max(wall_clock_us, _last_timestamp_us + 1)
        timestamp_us = _last_timestamp_us
    seconds, microseconds = divmod(timestamp_us, 1_000_000)
    return (
        datetime.fromtimestamp(seconds, timezone.utc)
        .replace(microsecond=microseconds)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )
