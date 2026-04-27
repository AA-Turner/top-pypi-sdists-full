"""Bounded in-memory active debug diagnostics state."""

from __future__ import annotations

import copy
import logging
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DiagnosticsStateConfig:
    max_active: int = 50
    max_last: int = 25
    max_age_seconds: float = 15 * 60


class DiagnosticsStateRegistry:
    """Bounded active/last-turn registry for opt-in debug snapshots."""

    def __init__(
        self,
        *,
        config: DiagnosticsStateConfig | None = None,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self._config = config or DiagnosticsStateConfig()
        self._clock = clock or time.monotonic
        self._active: OrderedDict[str, tuple[float, dict[str, Any]]] = OrderedDict()
        self._last: OrderedDict[str, tuple[float, dict[str, Any]]] = OrderedDict()

    def update(self, turn_id: str | None, snapshot: dict[str, Any] | None) -> None:
        """Store an active snapshot, ignoring invalid or disabled input."""
        if not turn_id or not snapshot:
            return
        try:
            self._cleanup()
            now = self._clock()
            self._active[turn_id] = (now, copy.deepcopy(snapshot))
            self._active.move_to_end(turn_id)
            self._trim(self._active, self._config.max_active)
        except Exception:
            logger.debug("Failed to update diagnostics snapshot", exc_info=True)

    def finish(self, turn_id: str | None, snapshot: dict[str, Any] | None = None) -> None:
        """Move a turn from active to last snapshots."""
        if not turn_id:
            return
        try:
            self._cleanup()
            now = self._clock()
            _ts, active_snapshot = self._active.pop(turn_id, (now, {}))
            final_snapshot = snapshot or active_snapshot
            if final_snapshot:
                self._last[turn_id] = (now, copy.deepcopy(final_snapshot))
                self._last.move_to_end(turn_id)
                self._trim(self._last, self._config.max_last)
        except Exception:
            logger.debug("Failed to finish diagnostics snapshot", exc_info=True)

    def clear(self, turn_id: str | None) -> None:
        if not turn_id:
            return
        try:
            self._active.pop(turn_id, None)
        except Exception:
            logger.debug("Failed to clear diagnostics snapshot", exc_info=True)

    def get_active(self, turn_id: str) -> dict[str, Any] | None:
        try:
            self._cleanup()
            entry = self._active.get(turn_id)
            return copy.deepcopy(entry[1]) if entry else None
        except Exception:
            logger.debug("Failed to read diagnostics snapshot", exc_info=True)
            return None

    def get_active_for_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        try:
            self._cleanup()
            for _turn_id, (_ts, snapshot) in reversed(self._active.items()):
                if snapshot.get("conversation_id") == conversation_id:
                    return copy.deepcopy(snapshot)
            return None
        except Exception:
            logger.debug("Failed to read conversation diagnostics snapshot", exc_info=True)
            return None

    def get_last(self, turn_id: str) -> dict[str, Any] | None:
        try:
            self._cleanup()
            entry = self._last.get(turn_id)
            return copy.deepcopy(entry[1]) if entry else None
        except Exception:
            logger.debug("Failed to read last diagnostics snapshot", exc_info=True)
            return None

    def _cleanup(self) -> None:
        cutoff = self._clock() - max(0.0, self._config.max_age_seconds)
        for bucket in (self._active, self._last):
            stale = [key for key, (ts, _snapshot) in bucket.items() if ts < cutoff]
            for key in stale:
                bucket.pop(key, None)
        self._trim(self._active, self._config.max_active)
        self._trim(self._last, self._config.max_last)

    @staticmethod
    def _trim(bucket: OrderedDict[str, tuple[float, dict[str, Any]]], cap: int) -> None:
        cap = max(0, cap)
        while len(bucket) > cap:
            bucket.popitem(last=False)


diagnostics_state = DiagnosticsStateRegistry()
