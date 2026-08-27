"""DataBus publish wrapper with bounded backpressure."""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BackpressurePolicy(Enum):
    DROP_OLDEST = "drop_oldest"
    DROP_TO_KEYFRAME = "drop_to_keyframe"
    BLOCK = "block"


# How often one publisher may warn about ring overwrite. The event is per frame under
# sustained lag, so an unthrottled log would be the loudest line in the file.
_OVERWRITE_WARN_INTERVAL_SEC = 60.0


@dataclass
class QueueMetrics:
    frames_enqueued: int = 0
    # Frames the PRODUCER refused to write. Wire-visible as ``frames_dropped_bp``.
    frames_dropped: int = 0
    # Frames written OVER a slot the slowest consumer had not read yet -- real data loss,
    # but on the data plane rather than at the producer. Every policy that admits a write
    # under lag (see publish()) produces these, and nothing counted them: a consumer
    # falling permanently behind under BLOCK reported ``frames_dropped=0`` forever while
    # losing frames continuously -- a zero presented as a measurement. Kept separate from
    # ``frames_dropped`` because one counter cannot carry two meanings.
    frames_overwritten: int = 0
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


# Guard so a bad value is reported once per process, not once per camera per publish.
_policy_warning_emitted = False


def _policy_from_env() -> BackpressurePolicy:
    """Resolve ``GATEWAY_BP_POLICY``, warning loudly on a value we do not honour.

    An unrecognised value used to fall through to ``DROP_OLDEST`` in silence, so a typo
    in a deployment's env produced materially different loss behaviour with nothing in
    the logs to connect the change to the config.
    """
    global _policy_warning_emitted

    raw = os.getenv("GATEWAY_BP_POLICY", "drop_oldest").strip().lower()
    for p in BackpressurePolicy:
        if p.value == raw:
            return p

    if not _policy_warning_emitted:
        _policy_warning_emitted = True
        logger.warning(
            "GATEWAY_BP_POLICY=%r is not a recognised policy - falling back to %s. Valid policies: %s.",
            raw,
            BackpressurePolicy.DROP_OLDEST.value,
            ", ".join(p.value for p in BackpressurePolicy),
        )
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
        # Per-report-window overwrite count, drained by consume_overwrite_events().
        self._overwrite_events_window = 0
        self._last_overwrite_warn = 0.0

    def _ring_capacity(self) -> int:
        """The ring's slot count, or 0 if it cannot be read.

        ``maxsize`` is the backpressure watermark and is NOT necessarily the ring's real
        capacity -- the OpenCV path defaults it to 32 from the environment. Overwrite is
        a property of the ring, so it is measured against the ring.
        """
        rb = getattr(self._producer, "rb", None)
        try:
            return max(0, int(getattr(rb, "num_slots", 0) or 0))
        except (TypeError, ValueError):
            return 0

    def consume_overwrite_events(self) -> int:
        """Return and zero the overwrite count accumulated since the last call.

        Keeps the wire counter a per-window delta so it does not smear across windows;
        ``metrics.frames_overwritten`` remains the cumulative total.
        """
        n = self._overwrite_events_window
        self._overwrite_events_window = 0
        return n

    def _note_overwrite(self, lag: int, capacity: int) -> None:
        self.metrics.frames_overwritten += 1
        self._overwrite_events_window += 1
        now = time.monotonic()
        if now - self._last_overwrite_warn < _OVERWRITE_WARN_INTERVAL_SEC:
            return
        self._last_overwrite_warn = now
        logger.warning(
            "%s: consumer lag %d has reached ring capacity %d - each new frame now "
            "overwrites one the slowest consumer never read (%d lost so far under "
            "policy %s). The producer is healthy; the consumer cannot keep up.",
            self.camera_id,
            lag,
            capacity,
            self.metrics.frames_overwritten,
            self.policy.value,
        )

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

        under_pressure = lag >= self.maxsize - 1
        if under_pressure:
            if self.policy == BackpressurePolicy.BLOCK:
                time.sleep(0.002)
            elif self.policy == BackpressurePolicy.DROP_TO_KEYFRAME:
                if not (metadata or {}).get("is_keyframe", False):
                    self.metrics.frames_dropped += 1
                    return False
            else:
                self.metrics.frames_dropped += 1
                return False

            # Anything reaching here is a write ADMITTED at a lag that puts it on top of
            # a slot the slowest consumer has not read: a frame IS lost, on the data
            # plane rather than at the producer. Count it separately from
            # frames_dropped -- one counter cannot carry two meanings -- and say so
            # periodically. A fixed-size ring always overwrites its physically-oldest
            # slot on write, and CudaIpcRingBuffer.read_next() fast-forwards the lagging
            # consumer, so the write is correct; the loss just has to be visible. On this
            # branch DROP_OLDEST refuses the write above and so counts nothing here; the
            # policies that fall through under lag (BLOCK after its sleep,
            # DROP_TO_KEYFRAME on a keyframe) are exactly the ones that overwrite, and
            # they had no accounting at all.
            capacity = self._ring_capacity()
            if capacity and lag >= capacity - 1:
                self._note_overwrite(lag, capacity)

        self._producer.publish(data, metadata)
        self.metrics.frames_enqueued += 1
        return True

    @property
    def depth(self) -> int:
        return self._estimate_lag()

    @property
    def is_full(self) -> bool:
        return self.depth >= self.maxsize - 1
