"""Benchmark metrics utilities for the Matrice package.

Split out of ``utils.py``; re-exported from ``matrice_common.utils`` for
backward compatibility.
"""

import time
from typing import Dict, List

# =============================================================================
# Benchmark Metrics Utility
# =============================================================================


class BenchmarkMetrics:
    """Accumulates per-stage timing samples with zero overhead when disabled.

    When enabled=False, all methods return immediately with no allocations.
    When enabled=True, tracks sum/count/min/max/samples per named stage.

    Usage::

        bm = BenchmarkMetrics(enabled=True)
        t = bm.start()
        # ... do work ...
        bm.record("stage_name", t)

        # Periodic reporting:
        print(bm.get_breakdown_str("My Title", interval_seconds=5.0, total_items=100))
        bm.reset()
    """

    __slots__ = ("enabled", "_stages", "_order")

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self._stages: Dict[str, List[float]] = {}
        self._order: List[str] = []  # preserves insertion order for display

    def start(self) -> float:
        """Return current time if enabled, else 0.0."""
        if not self.enabled:
            return 0.0
        return time.perf_counter()

    def record(self, stage_name: str, start_time: float) -> float:
        """Record elapsed time since start_time for the named stage.
        Returns elapsed seconds. No-op if disabled."""
        if not self.enabled:
            return 0.0
        elapsed = time.perf_counter() - start_time
        self._accumulate(stage_name, elapsed)
        return elapsed

    def record_value(self, stage_name: str, value_seconds: float):
        """Record a pre-computed value in seconds."""
        if not self.enabled:
            return
        self._accumulate(stage_name, value_seconds)

    def _accumulate(self, name: str, value: float):
        if name not in self._stages:
            self._stages[name] = []
            self._order.append(name)
        self._stages[name].append(value)

    def _percentile(self, sorted_samples: List[float], p: float) -> float:
        """Compute percentile from sorted samples."""
        n = len(sorted_samples)
        if n == 0:
            return 0.0
        idx = p / 100.0 * (n - 1)
        lo = int(idx)
        hi = min(lo + 1, n - 1)
        frac = idx - lo
        return sorted_samples[lo] * (1 - frac) + sorted_samples[hi] * frac

    def get_breakdown_str(
        self,
        title: str = "BENCHMARK METRICS",
        interval_seconds: float = 0.0,
        total_items: int = 0,
        item_label: str = "frames",
    ) -> str:
        """Format a multi-line log string with per-stage breakdown.

        Args:
            title: Header line for the metrics block.
            interval_seconds: Wall-clock seconds for the reporting interval.
                Used to compute throughput (items/sec) per stage.
            total_items: Total items processed in the interval (e.g. frames, batches).
            item_label: Label for the items (e.g. "frames", "batches").
        """
        if not self._stages:
            return ""

        lines = [
            f"\n{'=' * 70}",
            f"{title}",
            f"{'=' * 70}",
        ]

        # Throughput summary if caller provides interval info
        if interval_seconds > 0 and total_items > 0:
            throughput = total_items / interval_seconds
            lines.append(
                f"  THROUGHPUT: {total_items:,} {item_label} in {interval_seconds:.1f}s "
                f"= {throughput:,.1f} {item_label}/sec"
            )
            lines.append("")

        lines.append("  STAGE LATENCIES:")

        # Compute total time across all stages for % breakdown
        stage_avgs: Dict[str, float] = {}
        total_avg = 0.0
        for name in self._order:
            samples = self._stages[name]
            avg = sum(samples) / len(samples) if samples else 0.0
            stage_avgs[name] = avg
            total_avg += avg

        max_name_len = max(len(n) for n in self._order) if self._order else 10

        for name in self._order:
            samples = self._stages[name]
            if not samples:
                continue
            n = len(samples)
            avg = sum(samples) / n
            mn = min(samples)
            mx = max(samples)
            sorted_s = sorted(samples)
            p50 = self._percentile(sorted_s, 50)
            p95 = self._percentile(sorted_s, 95)
            p99 = self._percentile(sorted_s, 99)
            pct = (avg / total_avg * 100) if total_avg > 0 else 0

            # Compute per-stage throughput: how many items/sec this stage alone could sustain
            stage_throughput_str = ""
            if avg > 0:
                max_throughput = 1.0 / avg
                stage_throughput_str = f"  max={max_throughput:,.0f}/s"

            lines.append(
                f"  {name:<{max_name_len}}  "
                f"avg={avg * 1000:7.2f}ms  "
                f"p50={p50 * 1000:7.2f}  p95={p95 * 1000:7.2f}  p99={p99 * 1000:7.2f}  "
                f"({pct:5.1f}%){stage_throughput_str}  n={n}"
            )

        if total_avg > 0:
            total_max_throughput = 1.0 / total_avg
            lines.append(
                f"  {'TOTAL':<{max_name_len}}  "
                f"avg={total_avg * 1000:7.2f}ms  "
                f"max={total_max_throughput:,.0f}/s (serial bottleneck)"
            )

        lines.append(f"{'=' * 70}")
        return "\n".join(lines)

    def reset(self):
        """Reset all accumulators for the next reporting interval."""
        self._stages.clear()
        self._order.clear()
