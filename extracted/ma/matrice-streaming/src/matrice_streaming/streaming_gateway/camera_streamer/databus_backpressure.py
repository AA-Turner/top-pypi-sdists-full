"""DataBus publish wrapper with bounded backpressure."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class BackpressurePolicy(Enum):
    DROP_OLDEST = "drop_oldest"
    DROP_TO_KEYFRAME = "drop_to_keyframe"
    BLOCK = "block"


@dataclass
class QueueMetrics:
    frames_enqueued: int = 0
    frames_dropped: int = 0
    depth_samples: list = field(default_factory=list)

    @property
    def drop_rate(self) -> float:
        total = self.frames_enqueued + self.frames_dropped
        return self.frames_dropped / total if total else 0.0

    def p99_depth(self) -> float:
        if not self.depth_samples:
            return 0.0
        ordered = sorted(self.depth_samples)
        idx = min(len(ordered) - 1, int(len(ordered) * 0.99))
        return float(ordered[idx])


def _policy_from_env() -> BackpressurePolicy:
    raw = os.getenv("GATEWAY_BP_POLICY", "drop_oldest").strip().lower()
    for p in BackpressurePolicy:
        if p.value == raw:
            return p
    return BackpressurePolicy.DROP_OLDEST


class BackpressurePublisher:
    """Wraps ``DataBusProducer.publish`` with lag-aware backpressure."""

    def __init__(
        self,
        producer: Any,
        camera_id: str,
        maxsize: Optional[int] = None,
        policy: Optional[BackpressurePolicy] = None,
    ):
        self._producer = producer
        self.camera_id = camera_id
        self.maxsize = maxsize or int(os.getenv("GATEWAY_QUEUE_MAXSIZE", "32"))
        self.policy = policy or _policy_from_env()
        self.metrics = QueueMetrics()

    def _estimate_lag(self) -> int:
        rb = getattr(self._producer, "rb", None)
        if rb is None:
            return 0
        try:
            write_idx = rb.get_write_idx()
            consumers = rb.get_registered_consumers()
            if not consumers:
                return 0
            min_cursor = min(c["cursor"] for c in consumers.values())
            return max(0, write_idx - min_cursor)
        except Exception:
            return 0

    def publish(self, data: Any, metadata: Optional[Dict] = None) -> bool:
        lag = self._estimate_lag()
        self.metrics.depth_samples.append(lag)
        if len(self.metrics.depth_samples) > 1000:
            self.metrics.depth_samples = self.metrics.depth_samples[-500:]

        if lag >= self.maxsize - 1:
            if self.policy == BackpressurePolicy.BLOCK:
                time.sleep(0.002)
            elif self.policy == BackpressurePolicy.DROP_TO_KEYFRAME:
                if not (metadata or {}).get("is_keyframe", False):
                    self.metrics.frames_dropped += 1
                    return False
            else:
                self.metrics.frames_dropped += 1
                return False

        self._producer.publish(data, metadata)
        self.metrics.frames_enqueued += 1
        return True

    @property
    def depth(self) -> int:
        return self._estimate_lag()

    @property
    def is_full(self) -> bool:
        return self.depth >= self.maxsize - 1
