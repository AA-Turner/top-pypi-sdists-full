"""Client activity accounting, including time in operations still in flight."""

import time
from contextlib import contextmanager


class Activities:
    def __init__(self):
        self._operations = {}

    @contextmanager
    def measure(self, name):
        entry = self._operations.setdefault(
            name, {"calls": 0, "seconds": 0.0, "started": {}}
        )
        token = object()
        entry["calls"] += 1
        entry["started"][token] = time.monotonic()
        try:
            yield
        finally:
            entry["seconds"] += time.monotonic() - entry["started"].pop(token)

    def snapshot(self):
        now = time.monotonic()
        return {
            name: {
                "calls": entry["calls"],
                "active": len(entry["started"]),
                "seconds": entry["seconds"]
                + sum(now - start for start in entry["started"].values()),
            }
            for name, entry in self._operations.items()
        }
