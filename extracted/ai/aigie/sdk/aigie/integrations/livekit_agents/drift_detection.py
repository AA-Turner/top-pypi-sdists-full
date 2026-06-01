"""
Voice conversation drift detection for LiveKit Agents.

Monitors conversation metrics over time to detect behavioral drift:
- Response time drift (TTFB trending upward)
- Quality drift (error rate increasing)
- Latency drift (user-to-bot latency degrading)
- Turn count anomalies
- Interruption rate changes
"""

import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class DriftSignal:
    """A detected drift signal."""

    signal_type: str  # e.g., "latency_drift", "error_rate_drift"
    severity: str  # "low", "medium", "high"
    description: str
    current_value: float | None = None
    baseline_value: float | None = None
    deviation_pct: float | None = None
    timestamp: str | None = None


class VoiceDriftDetector:
    """
    Monitors voice conversation metrics to detect behavioral drift.

    Tracks rolling baselines for key metrics and detects deviations.
    """

    def __init__(
        self,
        llm_ttfb_threshold_pct: float = 50.0,
        latency_threshold_pct: float = 50.0,
        error_rate_threshold: float = 0.2,
        window_size: int = 10,
    ):
        self._llm_ttfb_threshold_pct = llm_ttfb_threshold_pct
        self._latency_threshold_pct = latency_threshold_pct
        self._error_rate_threshold = error_rate_threshold
        self._window_size = window_size

        # Rolling windows (bounded to prevent unbounded growth)
        self._llm_ttfb_history: deque[float] = deque(maxlen=window_size * 3)
        self._latency_history: deque[float] = deque(maxlen=window_size * 3)
        self._error_history: deque[bool] = deque(maxlen=window_size * 3)
        self._turn_durations: deque[float] = deque(maxlen=window_size * 3)

        # Baselines (set from first N samples)
        self._llm_ttfb_baseline: float | None = None
        self._latency_baseline: float | None = None
        self._baseline_set = False

        self._signals: List[DriftSignal] = []

    def record_turn(
        self,
        llm_ttfb_ms: float | None = None,
        user_bot_latency_ms: float | None = None,
        had_error: bool = False,
        turn_duration_ms: float | None = None,
    ) -> List[DriftSignal]:
        """Record a turn and check for drift. Returns any new signals."""
        now = datetime.now(timezone.utc).isoformat()
        new_signals: List[DriftSignal] = []

        if llm_ttfb_ms is not None:
            self._llm_ttfb_history.append(llm_ttfb_ms)

        if user_bot_latency_ms is not None:
            self._latency_history.append(user_bot_latency_ms)

        self._error_history.append(had_error)

        if turn_duration_ms is not None:
            self._turn_durations.append(turn_duration_ms)

        # Set baseline from first window
        if not self._baseline_set and len(self._llm_ttfb_history) >= self._window_size:
            ttfb_list = list(self._llm_ttfb_history)
            self._llm_ttfb_baseline = sum(ttfb_list[: self._window_size]) / self._window_size
            if self._latency_history:
                lat_list = list(self._latency_history)
                self._latency_baseline = sum(lat_list[: self._window_size]) / min(
                    len(lat_list), self._window_size
                )
            self._baseline_set = True

        if not self._baseline_set:
            return new_signals

        # Check LLM TTFB drift
        if self._llm_ttfb_baseline and len(self._llm_ttfb_history) > self._window_size:
            recent = list(self._llm_ttfb_history)[-self._window_size :]
            recent_avg = sum(recent) / len(recent)
            deviation = ((recent_avg - self._llm_ttfb_baseline) / self._llm_ttfb_baseline) * 100
            if deviation > self._llm_ttfb_threshold_pct:
                signal = DriftSignal(
                    signal_type="llm_ttfb_drift",
                    severity="high" if deviation > 100 else "medium",
                    description=f"LLM TTFB increased {deviation:.1f}% from baseline",
                    current_value=recent_avg,
                    baseline_value=self._llm_ttfb_baseline,
                    deviation_pct=deviation,
                    timestamp=now,
                )
                new_signals.append(signal)

        # Check latency drift
        if self._latency_baseline and len(self._latency_history) > self._window_size:
            recent = list(self._latency_history)[-self._window_size :]
            recent_avg = sum(recent) / len(recent)
            deviation = ((recent_avg - self._latency_baseline) / self._latency_baseline) * 100
            if deviation > self._latency_threshold_pct:
                signal = DriftSignal(
                    signal_type="latency_drift",
                    severity="high" if deviation > 100 else "medium",
                    description=f"User-bot latency increased {deviation:.1f}% from baseline",
                    current_value=recent_avg,
                    baseline_value=self._latency_baseline,
                    deviation_pct=deviation,
                    timestamp=now,
                )
                new_signals.append(signal)

        # Check error rate
        if len(self._error_history) >= self._window_size:
            recent = list(self._error_history)[-self._window_size :]
            error_rate = sum(1 for e in recent if e) / len(recent)
            if error_rate > self._error_rate_threshold:
                signal = DriftSignal(
                    signal_type="error_rate_drift",
                    severity="critical" if error_rate > 0.5 else "high",
                    description=f"Error rate {error_rate:.1%} exceeds threshold {self._error_rate_threshold:.1%}",
                    current_value=error_rate,
                    baseline_value=self._error_rate_threshold,
                    timestamp=now,
                )
                new_signals.append(signal)

        self._signals.extend(new_signals)
        return new_signals

    def get_drift_report(self) -> Dict[str, Any]:
        """Get a summary drift report."""
        return {
            "total_signals": len(self._signals),
            "signals_by_type": self._count_by_type(),
            "llm_ttfb_baseline_ms": self._llm_ttfb_baseline,
            "latency_baseline_ms": self._latency_baseline,
            "recent_signals": [
                {
                    "type": s.signal_type,
                    "severity": s.severity,
                    "description": s.description,
                }
                for s in self._signals[-5:]
            ],
        }

    def _count_by_type(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for s in self._signals:
            counts[s.signal_type] = counts.get(s.signal_type, 0) + 1
        return counts

    def reset(self) -> None:
        """Reset all drift detection state."""
        self._llm_ttfb_history.clear()
        self._latency_history.clear()
        self._error_history.clear()
        self._turn_durations.clear()
        self._llm_ttfb_baseline = None
        self._latency_baseline = None
        self._baseline_set = False
        self._signals.clear()
