# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Minimal Ray actor for actor-pool stress tests.

Kept in a separate module so Ray workers loading BenchWorker do not pull in
geneva (and thus lancedb/lance), which may not be installed on cluster nodes.
"""

import os
import time
from typing import Any

import ray


@ray.remote(num_cpus=0, memory=64 * 1024**2)
class BenchWorker:
    def __init__(self) -> None:
        self._first_start: float | None = None
        self._actor_id: str = ray.get_runtime_context().get_actor_id()

    def __ray_ready__(self) -> None:
        return None

    def run(self, value: int, busy_ms: float = 0.0) -> dict[str, Any]:
        start = time.monotonic()
        if self._first_start is None:
            self._first_start = start
        if busy_ms and busy_ms > 0:
            time.sleep(busy_ms / 1000.0)
        return {
            "actor_id": self._actor_id,
            "first_start": self._first_start,
            "task_start": start,
            "value": value,
            "pid": os.getpid(),
        }
