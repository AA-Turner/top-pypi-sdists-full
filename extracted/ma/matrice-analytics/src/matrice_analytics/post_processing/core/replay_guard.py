"""Keep cache-replay frames off the analytics counting path (F26 S6 item 2).

**What a replay is.** When the inference side consumes a frame it never infers -- shed
backlog, a torn slot, a camera that lost the batch race, an FPS gate -- it republishes that
camera's *last* terminal result so the operator's display never goes silent. py_inference
builds it in ``coupled/cache_replay.py``, stamps ``cached: True`` on it, and strips every
bounding box first, because replaying a stale box draws it frozen over a frame nothing
looked at. The decoupled half forwards the same thing as a carrier marked ``cache_replay``.

**Why analytics must refuse it.** A stripped replay is, to a counting use case,
indistinguishable from a frame that genuinely held nobody. Averaged in, it does not add
noise -- it dilutes, by exactly the fraction of frames that were replayed. Measured on the
sampled pipeline: mean occupancy collapses to **1.34** against **5.20** over the analysed
frames alone, a ~4x undercount, and 1.34/5.20 = 0.258 is just the share of frames that were
really inferred. The hold exists for the display. The counting path must see only real
inference results.

**Why this is a guard and not a filter.** In the shipping topologies a replay already never
reaches a use case: the coupled pool builds it after post-processing, and the analytics
loop counts and discards carriers rather than feeding them. So this seam should never fire
in production. If it does, some route started feeding the held stream to the counting path,
and that is the regression -- which is why the first refusal per camera is a WARNING with
the marker named, not a silent drop.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from typing import Any, Dict, Final, Optional

logger = logging.getLogger(__name__)

#: The two markers py_inference sets, in the order they are checked.
#:
#: ``cached`` rides the terminal result (``cache_replay.build_replay_result``); ``cache_replay``
#: rides the decoupled carrier (``PipelineMessage.cache_replay``, serialized only when true).
#: Both are checked on the payload and on ``stream_info``, because which one carries the frame's
#: identity depends on the route, and a guard that reads only one of them is a guard with a hole.
CACHE_REPLAY_KEYS: Final[tuple[str, ...]] = ("cached", "cache_replay")


def _marker_in(mapping: Any) -> Optional[str]:
    """The first replay marker set truthily on ``mapping``, or ``None``.

    Anything that is not a mapping answers ``None`` rather than raising: ``data`` is a raw
    model output and is a list far more often than a dict.
    """
    if not isinstance(mapping, dict):
        return None
    for key in CACHE_REPLAY_KEYS:
        if mapping.get(key):
            return key
    return None


def replay_marker(data: Any, stream_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """Name the marker that makes this frame a cache replay, or ``None`` if it is a real one.

    Returns the key rather than a bool so the caller can say *which* marker it saw. A carrier
    and a republished result arrive by different routes and mean different upstream mistakes,
    and a refusal that cannot tell them apart is one nobody can act on.
    """
    return _marker_in(data) or _marker_in(stream_info)


def is_cache_replay(data: Any, stream_info: Optional[Dict[str, Any]] = None) -> bool:
    """Whether this frame is a cache replay and must not be counted."""
    return replay_marker(data, stream_info) is not None


@dataclass
class ReplayGuardHealth:
    """How many replays the counting path was asked to consume, and from where.

    Mirrors the shape of ``Trackers.integration.TrackerHealth`` deliberately: both answer the
    same question -- did this stream's counts come from every frame, or only from the ones
    that worked -- and a caller should not need two idioms to ask it.
    """

    refused: int = 0
    last_marker: Optional[str] = None
    cameras: set[str] = field(default_factory=set)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)

    @property
    def degraded(self) -> bool:
        """True once anything has been refused: no healthy stream reaches this seam at all."""
        return self.refused > 0

    def record(self, marker: str, camera_id: str = "") -> bool:
        """Record one refusal. Returns whether this is the first for ``camera_id``.

        The return value is the rate limit. A regression here is per-route, not per-frame, so
        one loud line per camera says everything a hundred would; the count carries the rest.
        """
        with self._lock:
            self.refused += 1
            self.last_marker = marker
            first = camera_id not in self.cameras
            self.cameras.add(camera_id)
            return first

    def snapshot(self) -> Dict[str, Any]:
        """A plain dict for the result payload and for tests."""
        with self._lock:
            return {
                "refused": self.refused,
                "last_marker": self.last_marker,
                "cameras": sorted(self.cameras),
                "degraded": self.refused > 0,
            }


def note_refusal(health: ReplayGuardHealth, marker: str, camera_id: str = "") -> None:
    """Record a refusal on ``health`` and log the first one for this camera at WARNING."""
    if health.record(marker, camera_id):
        logger.warning(
            "Analytics refused a cache-replay frame (marker=%r camera_id=%r): the held overlay "
            "stream is reaching the counting path. Replays carry no boxes, so counting them "
            "dilutes every occupancy figure by the replayed fraction. Route real inference "
            "results here, or disable the hold with MATRICE_CACHE_REPLAY=0.",
            marker,
            camera_id or "<unknown>",
        )
    else:
        logger.debug(
            "Analytics refused a cache-replay frame (marker=%r camera_id=%r, %d so far)",
            marker,
            camera_id or "<unknown>",
            health.refused,
        )
