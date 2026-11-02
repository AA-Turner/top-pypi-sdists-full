"""Each new camera frame to the camera codec as it arrives (t16_latency_v1 LP, DSL-288).

A camera codec device that codes frames on arrival (``CodecWebSocketClient.wants_frame_feed``)
codes each camera's frame while it waits for the observation that will carry it, instead of after
the observation is taken. The feed is one thread: every ``period_s`` it reads each camera's latest
frame (``read``: the rig's ``camera_feed``) and hands each new one to the sink (``sink()``: the
policy's ``camera_frame_sink``, the transport's ``offer_frame``, or None while the session doesn't
code on arrival). It never raises into the run; camera failures show in the run loop's own reads.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable, Mapping
from typing import Any

log = logging.getLogger(__name__)

PERIOD_S = 0.002  # a new frame waits 1 ms on average before it is offered


class CameraFeed:
    def __init__(
        self,
        read: Callable[[], Mapping[str, Any]],
        sink: Callable[[], Callable[[str, Any, int], None] | None],
        *,
        period_s: float = PERIOD_S,
    ) -> None:
        self._read, self._sink, self._period_s = read, sink, period_s
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.offered = 0
        self.errors = 0  # iterations that raised (the first one is logged)
        self._warned = False

    def start(self) -> CameraFeed:
        if self._thread is None:
            self._thread = threading.Thread(target=self._run, name="codec-camera-feed",
                                            daemon=True)
            self._thread.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        thread, self._thread = self._thread, None
        if thread is not None:
            thread.join(timeout=1.0)

    def _run(self) -> None:
        last: dict[str, int] = {}
        while not self._stop.wait(self._period_s):
            try:
                self._offer_new(last)
            except Exception:  # noqa: BLE001 - never ends the feed; a step sends any frame not offered
                self.errors += 1
                if not self._warned:
                    self._warned = True
                    log.warning("camera feed: offering frames failed", exc_info=True)

    def _offer_new(self, last: dict[str, int]) -> None:
        offer = self._sink()
        if offer is None:
            return
        try:
            frames = self._read()
        except Exception:  # noqa: BLE001 - the run loop's own reads report camera failures
            return
        for camera, frame in frames.items():
            stamp = frame.timestamp_ns
            if last.get(camera) == stamp:
                continue
            last[camera] = stamp
            offer(camera, frame.rgb, stamp)
            self.offered += 1


def start_camera_feed(rig: Any, policy: Any) -> CameraFeed | None:
    """A running feed when the rig can read its cameras by observation key and the policy's
    camera codec codes frames on arrival; else None."""
    read = getattr(rig, "camera_feed", None)
    sink = getattr(policy, "camera_frame_sink", None)
    if read is None or sink is None or sink() is None:
        return None
    return CameraFeed(read, sink).start()
