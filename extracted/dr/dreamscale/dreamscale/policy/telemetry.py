from __future__ import annotations

import math
from dataclasses import dataclass, field

from dreamscale.policy.types import LatencyStats, PolicyTimingEvent, RunTimingSummary


def publish_run_summary(policy, hooks, result, *, preserve_error=False):
    """Publish once even on cancellation, without replacing the original error."""
    policy.last_run_result = result
    for callback in (hooks.on_summary, getattr(policy, "_emit_run_summary", None)):
        if callback is not None:
            try:
                callback(result)
            except Exception:
                if not preserve_error:
                    raise


def _latency_stats(values: list[float]) -> LatencyStats:
    samples = sorted(
        float(value)
        for value in values
        if math.isfinite(float(value)) and float(value) >= 0.0
    )
    if not samples:
        return LatencyStats()

    def nearest_rank(percentile: float) -> float:
        index = max(0, math.ceil(percentile * len(samples)) - 1)
        return samples[index]

    return LatencyStats(
        samples=len(samples),
        p50_ms=nearest_rank(0.50),
        p95_ms=nearest_rank(0.95),
    )


@dataclass
class RunTelemetryAccumulator:
    _policy_response_ms: list[float] = field(default_factory=list)
    _data_plane_rtt_ms: list[float] = field(default_factory=list)
    _worker_queue_ms: list[float] = field(default_factory=list)
    _worker_preprocess_ms: list[float] = field(default_factory=list)
    _worker_inference_ms: list[float] = field(default_factory=list)
    _worker_postprocess_ms: list[float] = field(default_factory=list)

    def record(self, event: PolicyTimingEvent) -> None:
        self._policy_response_ms.append(event.obs_to_action_ms)
        self._append(self._data_plane_rtt_ms, event.data_plane_rtt_ms)
        self._append(self._worker_queue_ms, event.worker_queue_ms)
        self._append(self._worker_preprocess_ms, event.worker_preprocess_ms)
        self._append(self._worker_inference_ms, event.worker_inference_ms)
        self._append(self._worker_postprocess_ms, event.worker_postprocess_ms)

    def summary(self) -> RunTimingSummary:
        return RunTimingSummary(
            policy_response_ms=_latency_stats(self._policy_response_ms),
            data_plane_rtt_ms=_latency_stats(self._data_plane_rtt_ms),
            worker_queue_ms=_latency_stats(self._worker_queue_ms),
            worker_preprocess_ms=_latency_stats(self._worker_preprocess_ms),
            worker_inference_ms=_latency_stats(self._worker_inference_ms),
            worker_postprocess_ms=_latency_stats(self._worker_postprocess_ms),
        )

    @staticmethod
    def _append(target: list[float], value: float | None) -> None:
        if value is not None:
            target.append(value)
