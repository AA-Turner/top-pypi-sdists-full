"""Auto-generated stub for module: metrics."""
from typing import Any

# Classes
class BenchmarkMetrics:
    # Accumulates per-stage timing samples with zero overhead when disabled.
    #
    #     When enabled=False, all methods return immediately with no allocations.
    #     When enabled=True, tracks sum/count/min/max/samples per named stage.
    #
    #     Usage::
    #
    #         bm = BenchmarkMetrics(enabled=True)
    #         t = bm.start()
    #         # ... do work ...
    #         bm.record("stage_name", t)
    #
    #         # Periodic reporting:
    #         print(bm.get_breakdown_str("My Title", interval_seconds=5.0, total_items=100))
    #         bm.reset()

    def __init__(self: Any, enabled: bool = False) -> None: ...

    def get_breakdown_str(self: Any, title: str = 'BENCHMARK METRICS', interval_seconds: float = 0.0, total_items: int = 0, item_label: str = 'frames') -> str:
        """
        Format a multi-line log string with per-stage breakdown.
        
                Args:
                    title: Header line for the metrics block.
                    interval_seconds: Wall-clock seconds for the reporting interval.
                        Used to compute throughput (items/sec) per stage.
                    total_items: Total items processed in the interval (e.g. frames, batches).
                    item_label: Label for the items (e.g. "frames", "batches").
        """
        ...

    def record(self: Any, stage_name: str, start_time: float) -> float:
        """
        Record elapsed time since start_time for the named stage.
                Returns elapsed seconds. No-op if disabled.
        """
        ...

    def record_value(self: Any, stage_name: str, value_seconds: float) -> Any:
        """
        Record a pre-computed value in seconds.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset all accumulators for the next reporting interval.
        """
        ...

    def start(self: Any) -> float:
        """
        Return current time if enabled, else 0.0.
        """
        ...

