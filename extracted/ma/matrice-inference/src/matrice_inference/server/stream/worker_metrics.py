"""
Worker-level metrics storage with thread-safe collection and aggregation.

This module provides a lightweight, thread-safe metrics collection class for
streaming workers. Supports both instance-level and CLASS-LEVEL (shared) metrics.

CLASS-LEVEL METRICS (threading-based workers):
    One WorkerMetrics instance shared across all workers of the same type.
    Accessed via WorkerMetrics.get_shared(worker_type) class method.
    Thread-safe with internal locking for concurrent worker access.
    Works for: consumer_manager, producer_worker (same process, different threads)

MULTIPROCESS METRICS (multiprocessing-based workers):
    For workers running in separate processes (inference, post_processing),
    metrics must be sent back to the main process via multiprocessing.Queue.
    Use MultiprocessWorkerMetrics for these workers.
    The main process aggregates metrics from all worker processes.

INSTANCE-LEVEL METRICS (legacy):
    Each worker has its own WorkerMetrics instance.
    Maintained for backward compatibility and testing.
"""

import multiprocessing as mp
import threading
import time
from typing import Dict, List, Optional, Any, ClassVar
from dataclasses import dataclass


@dataclass
class MetricSnapshot:
    """Immutable snapshot of metrics for a time interval."""
    worker_id: str
    worker_type: str
    interval_start_ts: float
    interval_end_ts: float
    latency_samples: List[float]
    throughput_count: int
    was_active: bool
    # Drop tracking (new fields)
    drop_count: int = 0
    drop_reasons: Optional[Dict[str, int]] = None  # reason -> count


@dataclass
class MetricUpdate:
    """
    Lightweight metric update sent from worker process to main process.

    Used by multiprocessing workers to report their metrics without
    requiring shared memory. The main process aggregates these updates.
    """
    worker_type: str
    worker_id: str
    latency_samples: List[float]
    throughput_count: int
    timestamp: float
    # Drop tracking (new fields)
    drop_count: int = 0
    drop_reasons: Optional[Dict[str, int]] = None  # reason -> count


class WorkerMetrics:
    """
    Thread-safe metrics storage for worker instances.
    
    Supports two modes:
    1. INSTANCE MODE: Each worker creates its own WorkerMetrics (legacy)
    2. SHARED MODE: All workers of same type share one WorkerMetrics (new)
    
    SHARED MODE DESIGN:
        - One WorkerMetrics per worker_type stored in class-level registry
        - Workers access via WorkerMetrics.get_shared(worker_type)
        - All operations are thread-safe with internal locking
        - Transparent to worker code - still use self.metrics.record_*()
    
    Thread Safety:
        All public methods acquire internal lock before state modification.
        Lock is reentrant (RLock) to support nested calls if needed.
        Snapshot operation is atomic - no data corruption during collection.
    
    Memory Management:
        Shared mode significantly reduces memory overhead:
        - Instance mode: 4 workers * 1000 samples = 4000 floats
        - Shared mode: 1 shared * 1000 samples = 1000 floats (75% reduction)
    
    Backward Compatibility:
        Existing code using WorkerMetrics(worker_id, worker_type) continues
        to work unchanged. To use shared mode, workers call get_shared().
    """
    
    # Class-level registry for shared metrics instances
    _shared_metrics: ClassVar[Dict[str, 'WorkerMetrics']] = {}
    _shared_metrics_lock: ClassVar[threading.Lock] = threading.Lock()
    
    def __init__(
        self,
        worker_id: str,
        worker_type: str,
        latency_unit: str = "ms",
        throughput_unit: str = "msg/sec",
        max_samples: Optional[int] = None,
        _is_shared: bool = False
    ):
        """
        Initialize worker metrics storage.
        
        Args:
            worker_id: Unique identifier for this worker instance (or "shared" for shared mode)
            worker_type: Type of worker (consumer, inference, post_processing, producer)
            latency_unit: Unit string for latency measurements
            throughput_unit: Unit string for throughput rate
            max_samples: Maximum samples to retain (None = unlimited)
            _is_shared: Internal flag indicating this is a shared instance
        """
        self.worker_id = worker_id
        self.worker_type = worker_type
        self.latency_unit = latency_unit
        self.throughput_unit = throughput_unit
        self.max_samples = max_samples
        self._is_shared = _is_shared
        
        # Thread synchronization - use RLock for reentrancy safety
        self._lock = threading.RLock()

        # Metric storage
        self._latency_samples: List[float] = []
        self._throughput_count: int = 0
        self._is_active: bool = False

        # Drop tracking (for backpressure monitoring)
        self._drop_count: int = 0
        self._drop_reasons: Dict[str, int] = {}  # reason -> count

        # Active worker count (only meaningful for shared instances)
        self._active_worker_count: int = 0
    
    @classmethod
    def get_shared(cls, worker_type: str) -> 'WorkerMetrics':
        """
        Get or create shared WorkerMetrics instance for a worker type.
        
        This is the primary method for workers to access class-level metrics.
        Thread-safe - multiple workers can call concurrently.
        
        Args:
            worker_type: Type of worker (consumer, inference, post_processing, producer)
        
        Returns:
            Shared WorkerMetrics instance for this worker type
        
        Example:
            # In worker __init__:
            self.metrics = WorkerMetrics.get_shared("inference")
            
            # In worker _run:
            self.metrics.record_latency(latency_ms)  # Thread-safe, shared storage
        """
        with cls._shared_metrics_lock:
            if worker_type not in cls._shared_metrics:
                # Create new shared instance
                cls._shared_metrics[worker_type] = cls(
                    worker_id=f"{worker_type}_shared",
                    worker_type=worker_type,
                    _is_shared=True
                )
            return cls._shared_metrics[worker_type]
    
    @classmethod
    def clear_shared_metrics(cls) -> None:
        """
        Clear all shared metrics instances.
        
        Used for testing and cleanup. Should not be called during normal operation.
        """
        with cls._shared_metrics_lock:
            cls._shared_metrics.clear()
    
    def record_latency(self, value_ms: float, timestamp: Optional[float] = None) -> None:
        """
        Record a latency measurement.
        
        Thread-safe for concurrent calls from multiple workers.
        
        Args:
            value_ms: Latency value in milliseconds
            timestamp: Optional timestamp (unused, for future extensions)
        """
        with self._lock:
            self._latency_samples.append(value_ms)
            self._is_active = True
    
    def record_throughput(self, count: int = 1, timestamp: Optional[float] = None) -> None:
        """
        Record throughput event(s).

        Thread-safe for concurrent calls from multiple workers.

        Args:
            count: Number of items processed (default: 1)
            timestamp: Optional timestamp (unused, for future extensions)
        """
        with self._lock:
            self._throughput_count += count
            self._is_active = True

    def record_drop(self, count: int = 1, reason: str = "backpressure") -> None:
        """
        Record dropped frames due to backpressure or other reasons.

        Thread-safe for concurrent calls from multiple workers.

        Args:
            count: Number of frames dropped (default: 1)
            reason: Reason for dropping (default: "backpressure")
                    Common reasons: "backpressure", "stale", "queue_full", "error"
        """
        with self._lock:
            self._drop_count += count
            self._drop_reasons[reason] = self._drop_reasons.get(reason, 0) + count
            self._is_active = True

    def mark_active(self) -> None:
        """
        Mark this worker as active for the current interval.
        
        For shared metrics, increments active worker count.
        Thread-safe.
        """
        with self._lock:
            self._is_active = True
            if self._is_shared:
                self._active_worker_count += 1
    
    def mark_inactive(self) -> None:
        """
        Mark this worker as inactive for the current interval.
        
        For shared metrics, decrements active worker count.
        Thread-safe.
        """
        with self._lock:
            if self._is_shared:
                self._active_worker_count = max(0, self._active_worker_count - 1)
                # Only mark inactive if no workers are active
                if self._active_worker_count == 0:
                    self._is_active = False
            else:
                self._is_active = False
    
    def set_running(self, running: bool) -> None:
        """Set worker running state."""
        if running:
            self.mark_active()
        else:
            self.mark_inactive()
    
    def snapshot_and_reset(
        self,
        interval_start_ts: float,
        interval_end_ts: float
    ) -> MetricSnapshot:
        """
        Capture current metrics and reset for next interval.
        
        This method atomically:
        1. Creates a snapshot of current metrics
        2. Clears internal storage for next interval
        3. Preserves active state
        
        Thread Safety:
            Atomic operation - entire snapshot under lock.
            Safe for concurrent access from multiple workers.
        
        Args:
            interval_start_ts: Start timestamp of the interval (Unix epoch)
            interval_end_ts: End timestamp of the interval (Unix epoch)
        
        Returns:
            MetricSnapshot containing interval data
        """
        with self._lock:
            snapshot = MetricSnapshot(
                worker_id=self.worker_id,
                worker_type=self.worker_type,
                interval_start_ts=interval_start_ts,
                interval_end_ts=interval_end_ts,
                latency_samples=self._latency_samples.copy(),
                throughput_count=self._throughput_count,
                was_active=self._is_active,
                # Include drop metrics
                drop_count=self._drop_count,
                drop_reasons=dict(self._drop_reasons) if self._drop_reasons else None
            )

            # Reset for next interval
            self._latency_samples.clear()
            self._throughput_count = 0
            self._drop_count = 0
            self._drop_reasons.clear()
            # Reset active state - workers must record metrics each interval to be considered active
            # This ensures accurate active status reporting across process boundaries
            self._is_active = False

            return snapshot
    
    def to_summary_dict(self) -> Dict[str, Any]:
        """
        Generate summary statistics from current state without reset.
        
        Thread-safe.
        
        Returns:
            Dictionary with latency and throughput statistics
            
        Note:
            Omits latency metrics when no data available (inactive worker).
        """
        with self._lock:
            latency_stats = self._compute_latency_stats(self._latency_samples)
            
            # Throughput is instantaneous count (rate computed per interval elsewhere)
            throughput_stats = {
                "count": self._throughput_count,
                "unit": self.throughput_unit
            }
            
            result = {
                "worker_id": self.worker_id,
                "worker_type": self.worker_type,
                "is_active": self._is_active,
                "is_shared": self._is_shared,
                "active_worker_count": self._active_worker_count if self._is_shared else 1,
                "throughput": throughput_stats
            }

            # Only include latency if we have data
            if latency_stats:
                result["latency"] = latency_stats

            # Include drop metrics if any drops occurred
            if self._drop_count > 0:
                result["drops"] = {
                    "count": self._drop_count,
                    "reasons": dict(self._drop_reasons)
                }

            return result
    
    def _compute_latency_stats(self, samples: List[float]) -> Dict[str, Any]:
        """
        Compute latency statistics from samples.
        
        Args:
            samples: List of latency measurements
        
        Returns:
            Dictionary with min, max, avg, p0, p50, p100, unit
            Returns empty dict if no samples
        """
        if not samples:
            return {}
        
        sorted_samples = sorted(samples)
        n = len(sorted_samples)
        
        return {
            "min": sorted_samples[0],
            "max": sorted_samples[-1],
            "avg": sum(samples) / n,
            "p0": sorted_samples[0],
            "p50": self._percentile(sorted_samples, 50),
            "p100": sorted_samples[-1],
            "unit": self.latency_unit
        }
    
    @staticmethod
    def _percentile(sorted_samples: List[float], percentile: float) -> float:
        """
        Calculate percentile from sorted samples using nearest-rank method.
        
        Args:
            sorted_samples: Pre-sorted list of values
            percentile: Percentile to calculate (0-100)
        
        Returns:
            Percentile value
        
        Complexity:
            O(1) given pre-sorted input
        """
        if not sorted_samples:
            return 0
        
        if percentile <= 0:
            return sorted_samples[0]
        if percentile >= 100:
            return sorted_samples[-1]
        
        n = len(sorted_samples)
        rank = (percentile / 100.0) * (n - 1)
        lower_idx = int(rank)
        upper_idx = min(lower_idx + 1, n - 1)
        
        # Linear interpolation
        fraction = rank - lower_idx
        return sorted_samples[lower_idx] * (1 - fraction) + sorted_samples[upper_idx] * fraction
    
    @classmethod
    def merge(cls, metrics_list: List['WorkerMetrics']) -> 'WorkerMetrics':
        """
        Merge multiple WorkerMetrics instances into one aggregate.
        
        NOTE: This method is deprecated for shared metrics mode.
        When using shared metrics, no merging is needed - all workers
        already write to the same instance.
        
        Kept for backward compatibility with instance-mode usage.
        
        Args:
            metrics_list: List of WorkerMetrics to merge
        
        Returns:
            New WorkerMetrics instance with combined data
        """
        if not metrics_list:
            raise ValueError("Cannot merge empty metrics list")
        
        first = metrics_list[0]
        merged = cls(
            worker_id=f"{first.worker_type}_merged",
            worker_type=first.worker_type,
            latency_unit=first.latency_unit,
            throughput_unit=first.throughput_unit
        )
        
        # Aggregate all samples and counts
        with merged._lock:
            for metrics in metrics_list:
                with metrics._lock:
                    merged._latency_samples.extend(metrics._latency_samples)
                    merged._throughput_count += metrics._throughput_count
                    merged._is_active = merged._is_active or metrics._is_active
        
        return merged
    
    @staticmethod
    def compute_interval_summary(snapshot: MetricSnapshot) -> Dict[str, Any]:
        """
        Compute aggregated statistics from a snapshot for reporting.
        
        Args:
            snapshot: MetricSnapshot from snapshot_and_reset()
        
        Returns:
            Dictionary with latency and throughput statistics for the interval
            Omits latency if no samples available
        """
        interval_seconds = snapshot.interval_end_ts - snapshot.interval_start_ts
        
        result = {
            "active": snapshot.was_active
        }
        
        # Latency statistics - only include if we have samples
        if snapshot.latency_samples:
            sorted_samples = sorted(snapshot.latency_samples)
            n = len(sorted_samples)
            result["latency"] = {
                "min": sorted_samples[0],
                "max": sorted_samples[-1],
                "avg": sum(snapshot.latency_samples) / n,
                "p0": sorted_samples[0],
                "p50": WorkerMetrics._percentile(sorted_samples, 50),
                "p100": sorted_samples[-1],
                "unit": "ms"
            }
        
        # Throughput statistics (rate per second)
        if interval_seconds > 0:
            throughput_rate = snapshot.throughput_count / interval_seconds
        else:
            throughput_rate = 0

        result["throughput"] = {
            "min": throughput_rate,
            "max": throughput_rate,
            "avg": throughput_rate,
            "p0": throughput_rate,
            "p50": throughput_rate,
            "p100": throughput_rate,
            "unit": "msg/sec"
        }

        # Drop statistics (if any drops occurred)
        if snapshot.drop_count > 0:
            if interval_seconds > 0:
                drop_rate = snapshot.drop_count / interval_seconds
            else:
                drop_rate = 0
            result["drops"] = {
                "count": snapshot.drop_count,
                "rate": drop_rate,
                "reasons": snapshot.drop_reasons or {},
                "unit": "drops/sec"
            }

        return result


class MultiprocessMetricsCollector:
    """
    Collector for metrics from multiprocessing workers.
    
    This class runs in the MAIN PROCESS and aggregates MetricUpdate messages
    sent from worker processes via a shared multiprocessing.Queue.
    
    Architecture:
        - Worker processes call record_latency/record_throughput on their local
          MultiprocessWorkerMetrics instance
        - MultiprocessWorkerMetrics periodically flushes updates to the shared queue
        - This collector drains the queue and aggregates metrics by worker_type
        - InferenceMetricLogger calls snapshot_and_reset() to get aggregated metrics
    
    Thread Safety:
        - Uses internal lock for thread-safe aggregation
        - Queue operations are process-safe (multiprocessing.Queue)
    """
    
    def __init__(self, metrics_queue: mp.Queue):
        """
        Initialize collector with shared metrics queue.

        Args:
            metrics_queue: Shared multiprocessing.Queue for receiving MetricUpdate
        """
        self.metrics_queue = metrics_queue
        self._lock = threading.RLock()

        # Aggregated metrics by worker_type
        self._latency_samples: Dict[str, List[float]] = {}
        self._throughput_counts: Dict[str, int] = {}
        self._active_workers: Dict[str, set] = {}  # worker_type -> set of worker_ids
        # Drop tracking (aggregated by worker_type)
        self._drop_counts: Dict[str, int] = {}
        self._drop_reasons: Dict[str, Dict[str, int]] = {}  # worker_type -> {reason -> count}
        
    def drain_queue(self) -> int:
        """
        Drain all pending MetricUpdate messages from the queue.
        
        This should be called periodically (e.g., before snapshot_and_reset).
        
        Returns:
            Number of updates processed
        """
        updates_processed = 0
        
        while True:
            try:
                # Non-blocking get
                update = self.metrics_queue.get_nowait()
                self._process_update(update)
                updates_processed += 1
            except Exception:
                # Queue empty or error
                break
        
        return updates_processed
    
    def _process_update(self, update: MetricUpdate) -> None:
        """Process a single MetricUpdate and aggregate into internal state."""
        with self._lock:
            worker_type = update.worker_type

            # Initialize storage for this worker type if needed
            if worker_type not in self._latency_samples:
                self._latency_samples[worker_type] = []
                self._throughput_counts[worker_type] = 0
                self._active_workers[worker_type] = set()
                self._drop_counts[worker_type] = 0
                self._drop_reasons[worker_type] = {}

            # Aggregate metrics
            self._latency_samples[worker_type].extend(update.latency_samples)
            self._throughput_counts[worker_type] += update.throughput_count
            self._active_workers[worker_type].add(update.worker_id)

            # Aggregate drop metrics
            if update.drop_count > 0:
                self._drop_counts[worker_type] += update.drop_count
                if update.drop_reasons:
                    for reason, count in update.drop_reasons.items():
                        self._drop_reasons[worker_type][reason] = (
                            self._drop_reasons[worker_type].get(reason, 0) + count
                        )
    
    def snapshot_and_reset(
        self,
        worker_type: str,
        interval_start_ts: float,
        interval_end_ts: float
    ) -> MetricSnapshot:
        """
        Get snapshot for a worker type and reset its metrics.
        
        This first drains the queue to ensure all pending updates are included.
        
        Args:
            worker_type: Type of worker (inference, post_processing)
            interval_start_ts: Start of interval (Unix epoch)
            interval_end_ts: End of interval (Unix epoch)
        
        Returns:
            MetricSnapshot with aggregated metrics for this worker type
        """
        # Drain queue first to get latest updates
        self.drain_queue()
        
        with self._lock:
            latency_samples = self._latency_samples.get(worker_type, []).copy()
            throughput_count = self._throughput_counts.get(worker_type, 0)
            active_workers = self._active_workers.get(worker_type, set())
            drop_count = self._drop_counts.get(worker_type, 0)
            drop_reasons = dict(self._drop_reasons.get(worker_type, {}))
            was_active = len(active_workers) > 0 or throughput_count > 0 or len(latency_samples) > 0

            # Reset for next interval
            self._latency_samples[worker_type] = []
            self._throughput_counts[worker_type] = 0
            self._active_workers[worker_type] = set()
            self._drop_counts[worker_type] = 0
            self._drop_reasons[worker_type] = {}

            return MetricSnapshot(
                worker_id=f"{worker_type}_aggregated",
                worker_type=worker_type,
                interval_start_ts=interval_start_ts,
                interval_end_ts=interval_end_ts,
                latency_samples=latency_samples,
                throughput_count=throughput_count,
                was_active=was_active,
                drop_count=drop_count,
                drop_reasons=drop_reasons if drop_reasons else None
            )


class MultiprocessWorkerMetrics:
    """
    Metrics collector for workers running in separate processes.
    
    This class is used INSIDE WORKER PROCESSES. It collects metrics locally
    and periodically flushes them to a shared multiprocessing.Queue.
    
    The main process uses MultiprocessMetricsCollector to aggregate these updates.
    
    Usage in worker process:
        metrics = MultiprocessWorkerMetrics(
            worker_id="inference_0",
            worker_type="inference",
            metrics_queue=shared_queue
        )
        
        # Record metrics (batched locally)
        metrics.record_latency(latency_ms)
        metrics.record_throughput(count=1)
        
        # Periodically flush to main process (e.g., every N items or M seconds)
        metrics.flush()
    
    Thread Safety:
        - Uses internal lock for thread-safe local operations
        - Queue.put() is process-safe
    """
    
    # Flush thresholds
    # OPTIMIZATION: Increased threshold to reduce queue contention at high FPS
    # At 1250 FPS/worker, old threshold of 100 caused 12.5 flushes/sec per worker
    # New threshold of 2000 = ~0.6 flushes/sec per worker, significantly less contention
    FLUSH_INTERVAL_SECONDS = 10.0  # Flush at least every 10 seconds
    FLUSH_ITEM_THRESHOLD = 2000   # Flush after 2000 items
    
    def __init__(
        self,
        worker_id: str,
        worker_type: str,
        metrics_queue: mp.Queue
    ):
        """
        Initialize worker metrics.
        
        Args:
            worker_id: Unique identifier for this worker
            worker_type: Type of worker (inference, post_processing)
            metrics_queue: Shared queue for sending updates to main process
        """
        self.worker_id = worker_id
        self.worker_type = worker_type
        self.metrics_queue = metrics_queue
        
        self._lock = threading.RLock()
        self._latency_samples: List[float] = []
        self._throughput_count: int = 0
        self._drop_count: int = 0
        self._drop_reasons: Dict[str, int] = {}
        self._last_flush_time: float = time.time()
        self._is_active: bool = False
    
    def record_latency(self, value_ms: float, timestamp: Optional[float] = None) -> None:
        """
        Record a latency measurement.
        
        Args:
            value_ms: Latency value in milliseconds
            timestamp: Optional timestamp (unused, for API compatibility)
        """
        with self._lock:
            self._latency_samples.append(value_ms)
            self._is_active = True
            self._maybe_flush()
    
    def record_throughput(self, count: int = 1, timestamp: Optional[float] = None) -> None:
        """
        Record throughput event(s).

        Args:
            count: Number of items processed
            timestamp: Optional timestamp (unused, for API compatibility)
        """
        with self._lock:
            self._throughput_count += count
            self._is_active = True
            self._maybe_flush()

    def record_drop(self, count: int = 1, reason: str = "backpressure") -> None:
        """
        Record dropped frames due to backpressure or other reasons.

        Args:
            count: Number of frames dropped (default: 1)
            reason: Reason for dropping (default: "backpressure")
                    Common reasons: "backpressure", "stale", "queue_full", "error"
        """
        with self._lock:
            self._drop_count += count
            self._drop_reasons[reason] = self._drop_reasons.get(reason, 0) + count
            self._is_active = True
            self._maybe_flush()

    def mark_active(self) -> None:
        """Mark this worker as active."""
        with self._lock:
            self._is_active = True
    
    def mark_inactive(self) -> None:
        """Mark this worker as inactive and flush remaining metrics."""
        with self._lock:
            self._is_active = False
            self._flush_internal()
    
    def _maybe_flush(self) -> None:
        """Check if we should flush based on thresholds."""
        items = len(self._latency_samples) + (1 if self._throughput_count > 0 else 0) + (1 if self._drop_count > 0 else 0)
        time_since_flush = time.time() - self._last_flush_time

        if items >= self.FLUSH_ITEM_THRESHOLD or time_since_flush >= self.FLUSH_INTERVAL_SECONDS:
            self._flush_internal()
    
    def flush(self) -> None:
        """Manually flush metrics to the main process."""
        with self._lock:
            self._flush_internal()
    
    def _flush_internal(self) -> None:
        """Internal flush implementation (must hold lock)."""
        if not self._latency_samples and self._throughput_count == 0 and self._drop_count == 0:
            return

        try:
            update = MetricUpdate(
                worker_type=self.worker_type,
                worker_id=self.worker_id,
                latency_samples=self._latency_samples.copy(),
                throughput_count=self._throughput_count,
                timestamp=time.time(),
                drop_count=self._drop_count,
                drop_reasons=dict(self._drop_reasons) if self._drop_reasons else None
            )

            # Non-blocking put to avoid slowing down workers
            self.metrics_queue.put_nowait(update)

            # Reset local state
            self._latency_samples.clear()
            self._throughput_count = 0
            self._drop_count = 0
            self._drop_reasons.clear()
            self._last_flush_time = time.time()

        except Exception:
            # Queue full - metrics will be included in next flush
            # Don't clear local state so we retry next time
            pass