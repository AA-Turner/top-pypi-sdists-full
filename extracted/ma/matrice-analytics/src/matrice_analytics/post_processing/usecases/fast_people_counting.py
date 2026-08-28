"""Fast (lean) People Counting use case for high-FPS (10K+) pipelines.

A lean variant of :class:`PeopleCountingUseCase` that strips the per-frame CPU
overhead which dominates at 10K FPS:

- **No tracker at all**: forces ``enable_advanced_tracker`` / ``enable_simple_tracker``
  / ``enable_tracking`` off, so neither the heavy AdvancedTracker/ByteTrack path
  (~25% of per-frame CPU) nor the O(n) simple tracker runs. This makes it a
  **per-frame counter** — current per-frame counts only; cross-frame cumulative
  *unique* counting is intentionally not performed (that's the speed trade-off).
- **No per-frame debug stdout**: the ``[PERF]``/``[STATS]``/``[TRACK]`` prints are
  gated off via the inherited ``_dbg`` flag, so their f-strings are never built.
- **Quiet logger**: level raised to ``WARNING`` so per-frame debug/info logging
  dispatch is skipped.

Registered separately as the ``fast_people_counting`` use case; reuses
``PeopleCountingConfig`` and keeps people_counting's ``CASE_TYPE`` /
incident categorisation and output shape.
"""

import logging
from typing import Any, Dict, Optional

from ..core.base import ConfigProtocol, ProcessingContext, ProcessingResult
from .people_counting import PeopleCountingUseCase

# Every tracker on/off switch people_counting consults — fast mode forces all off.
_TRACKER_FLAGS = ("enable_advanced_tracker", "enable_simple_tracker", "enable_tracking")


class FastPeopleCountingUseCase(PeopleCountingUseCase):
    """Trackerless, debug-free people counter for high-throughput pipelines."""

    def __init__(self) -> None:
        super().__init__()
        # Distinct use-case identity, but keep people_counting analytics/incident type.
        self.name = "fast_people_counting"
        self.CASE_TYPE = "people_counting"
        # Kill per-frame debug stdout (dominant 10K-FPS cost) — f-strings never built
        # thanks to the inherited `self._dbg and print(...)` short-circuit guards.
        self._dbg = False
        # Skip per-frame debug/info logging dispatch.
        try:
            self.logger.setLevel(logging.WARNING)
        except Exception:
            pass

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        # Fast path: disable every tracker so no per-frame tracking work runs.
        for _flag in _TRACKER_FLAGS:
            try:
                setattr(config, _flag, False)
            except Exception:
                pass
        return super().process(data, config, context, stream_info)
