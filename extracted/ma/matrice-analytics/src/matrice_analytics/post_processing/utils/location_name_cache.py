"""A resolved-vs-failed cache for location-name lookups.

Six modules resolve a location ObjectId to a display name through the same
``/v1/inference/get_location/{id}`` route, and until INC-2606 all six cached the
*failure* exactly like a success::

    except Exception:
        ...
    _location_name_cache[location_id] = default_location   # forever

One 3-second timeout on the first sighting of a location therefore pinned a
placeholder -- ``""``, ``"Entry Reception"``, ``"Unknown Location"`` -- onto every
incident, business-metrics row and plate record for that location for the life of
the process. Nothing invalidated it, and the API recovering changed nothing. The
symptom is not a failure anybody sees: rows keep flowing, with the wrong label.

Caching the failure was not gratuitous, though, and simply deleting it would be a
regression: without it a permanently-unresolvable id costs an HTTP round trip on
the hot path of every frame. So the two outcomes are kept, and only their
lifetimes differ -- a resolved name is a fact and is kept, a failure is a guess
about right now and expires.

This module owns no I/O and no session: callers keep their own fetch, which is
where the six differ. It replaces only the dictionary.
"""

from __future__ import annotations

import threading
import time
from typing import Dict, Optional

__all__ = ["LocationNameCache", "RETRY_AFTER_SECONDS"]

#: How long a failed lookup is trusted before the next caller retries it.
#:
#: Monotonic, not wall clock -- this is I/O rate limiting, not analytics cadence, so
#: PY-13 does not apply, and an NTP step must not extend a cool-off into hours.
#:
#: 60s is the same interval the runner uses to re-test a deferred camera. It is long
#: enough that a hard-down API costs one request a minute per location rather than one
#: per frame, and short enough that a blip is invisible in the published data.
RETRY_AFTER_SECONDS: float = 60.0


class LocationNameCache:
    """Remember resolved names; let failures expire.

    Thread-safe: ``face_recognition`` and the plate sync sender both resolve names off
    their own threads while the frame thread is in ``process()``.
    """

    __slots__ = ("_failed_at", "_lock", "_names", "_retry_after")

    def __init__(self, retry_after: float = RETRY_AFTER_SECONDS) -> None:
        self._lock = threading.Lock()
        self._names: Dict[str, str] = {}
        self._failed_at: Dict[str, float] = {}
        self._retry_after = retry_after

    def resolved(self, location_id: str) -> Optional[str]:
        """The cached name, or ``None`` when this id has never resolved."""
        with self._lock:
            return self._names.get(location_id)

    def should_fetch(self, location_id: str) -> bool:
        """Whether a caller should spend a request on this id now.

        ``False`` only while a recent failure is still inside its cool-off. An id that
        has never been tried, or whose last failure has aged out, is always fetchable.
        """
        with self._lock:
            failed_at = self._failed_at.get(location_id)
            if failed_at is None:
                return True
            return (time.monotonic() - failed_at) >= self._retry_after

    def store(self, location_id: str, name: str) -> None:
        """Record a resolved name and clear any earlier failure for it."""
        with self._lock:
            self._names[location_id] = name
            self._failed_at.pop(location_id, None)

    def note_failure(self, location_id: str) -> None:
        """Start (or restart) the cool-off after a lookup failed."""
        with self._lock:
            self._failed_at[location_id] = time.monotonic()

    def clear(self) -> None:
        """Drop everything. For tests and for a session change."""
        with self._lock:
            self._names.clear()
            self._failed_at.clear()
