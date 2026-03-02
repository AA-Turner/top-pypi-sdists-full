import os
import time
import threading
import logging
import subprocess
import multiprocessing as mp
from functools import lru_cache
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple

from matrice_inference.server.stream.worker_metrics import (
    WorkerMetrics, 
    MetricSnapshot,
    MultiprocessMetricsCollector,
)
from matrice_inference.server.stream.metric_publisher import MetricPublisher, KafkaMetricPublisher, NoOpMetricPublisher 

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_gpu_name() -> Optional[str]:
    """
    Get GPU name dynamically using nvidia-smi.
    
    This function is cached using lru_cache - the GPU detection only runs once
    and subsequent calls return the cached result. This is appropriate because
    GPU hardware doesn't change during runtime.
    
    Handles multiple edge cases:
    - Multiple GPUs: Returns the first GPU name
    - All GPUs same type: Returns just the name (no index)
    - Jetson devices: Attempts tegrastats fallback if nvidia-smi unavailable
    - No GPU / nvidia-smi not available: Returns None
    
    Returns:
        GPU name string or None if unable to detect
    
    Examples:
        "NVIDIA GeForce RTX 4090"
        "NVIDIA A100-SXM4-80GB"
        "NVIDIA Tegra X1" (Jetson)
        None (no GPU or error)
    
    Cache:
        Use get_gpu_name.cache_clear() to reset cache if needed (e.g., testing)
    """
    gpu_name = None
    
    # Try nvidia-smi first (works on most NVIDIA GPUs)
    gpu_name = _get_gpu_name_nvidia_smi()
    
    if gpu_name is None:
        # Fallback: Try Jetson-specific detection
        gpu_name = _get_gpu_name_jetson()
    
    return gpu_name


def _get_gpu_name_nvidia_smi() -> Optional[str]:
    """
    Get GPU name using nvidia-smi command.
    
    Returns:
        GPU name or None if nvidia-smi fails
    """
    try:
        # Query GPU names using nvidia-smi
        # --query-gpu=name returns GPU product name
        # --format=csv,noheader,nounits for clean output
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=10.0
        )
        
        if result.returncode != 0:
            logger.debug(
                f"nvidia-smi returned non-zero exit code: {result.returncode}, "
                f"stderr: {result.stderr.strip()}"
            )
            return None
        
        # Parse output - each line is a GPU name
        output = result.stdout.strip()
        if not output:
            logger.debug("nvidia-smi returned empty output")
            return None
        
        gpu_names = [name.strip() for name in output.split('\n') if name.strip()]
        
        if not gpu_names:
            logger.debug("No GPU names parsed from nvidia-smi output")
            return None
        
        # Handle multiple GPUs
        if len(gpu_names) == 1:
            # Single GPU
            gpu_name = gpu_names[0]
            logger.debug(f"Detected single GPU: {gpu_name}")
            return gpu_name
        
        # Multiple GPUs - check if all same type
        unique_names = set(gpu_names)
        
        if len(unique_names) == 1:
            # All GPUs are the same type - return just the name
            gpu_name = gpu_names[0]
            logger.debug(
                f"Detected {len(gpu_names)} GPUs of same type: {gpu_name}"
            )
            return gpu_name
        else:
            # Mixed GPU types - return first one
            gpu_name = gpu_names[0]
            logger.info(
                f"Detected {len(gpu_names)} GPUs with mixed types: {unique_names}. "
                f"Reporting first GPU: {gpu_name}"
            )
            return gpu_name
            
    except FileNotFoundError:
        # nvidia-smi not installed or not in PATH
        logger.debug("nvidia-smi not found in PATH")
        return None
    except subprocess.TimeoutExpired:
        logger.warning("nvidia-smi command timed out after 10 seconds")
        return None
    except PermissionError as e:
        logger.warning(f"Permission denied running nvidia-smi: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting GPU name via nvidia-smi: {e}", exc_info=True)
        return None


def _get_gpu_name_jetson() -> Optional[str]:
    """
    Get GPU name for NVIDIA Jetson devices.
    
    Jetson devices may not have nvidia-smi available.
    Uses /proc/device-tree/model to detect Jetson platform.
    
    Returns:
        Jetson GPU name or None if not a Jetson device
    """
    try:
        # Check if this is a Jetson device by reading device tree model
        model_path = "/proc/device-tree/model"
        
        if not os.path.exists(model_path):
            logger.debug("Device tree model not found - not a Jetson device")
            return None
        
        with open(model_path, "r") as f:
            model = f.read().strip().rstrip('\x00')  # Remove null terminators
        
        if not model:
            return None
        
        # Check if it's a Jetson device
        jetson_identifiers = [
            "NVIDIA Jetson",
            "Jetson-AGX",
            "Jetson Nano",
            "Jetson TX",
            "Jetson Orin",
            "Jetson Xavier"
        ]
        
        is_jetson = any(identifier.lower() in model.lower() for identifier in jetson_identifiers)
        
        if is_jetson:
            # Map model to GPU name
            gpu_name = _map_jetson_model_to_gpu(model)
            logger.debug(f"Detected Jetson device: {model}, GPU: {gpu_name}")
            return gpu_name
        
        logger.debug(f"Device model '{model}' is not a recognized Jetson device")
        return None
        
    except FileNotFoundError:
        logger.debug("Could not read device tree model")
        return None
    except PermissionError as e:
        logger.warning(f"Permission denied reading Jetson model: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error detecting Jetson GPU: {e}", exc_info=True)
        return None


def _map_jetson_model_to_gpu(model: str) -> str:
    """
    Map Jetson device model to GPU name.
    
    Args:
        model: Device model string from /proc/device-tree/model
    
    Returns:
        GPU name for the Jetson platform
    """
    model_lower = model.lower()
    
    # Jetson Orin series (newest)
    if "orin" in model_lower:
        if "agx" in model_lower:
            return "NVIDIA Jetson AGX Orin"
        elif "nano" in model_lower:
            return "NVIDIA Jetson Orin Nano"
        elif "nx" in model_lower:
            return "NVIDIA Jetson Orin NX"
        return "NVIDIA Jetson Orin"
    
    # Jetson Xavier series
    if "xavier" in model_lower:
        if "agx" in model_lower:
            return "NVIDIA Jetson AGX Xavier"
        elif "nx" in model_lower:
            return "NVIDIA Jetson Xavier NX"
        return "NVIDIA Jetson Xavier"
    
    # Jetson TX series
    if "tx2" in model_lower:
        return "NVIDIA Jetson TX2"
    if "tx1" in model_lower:
        return "NVIDIA Jetson TX1"
    
    # Jetson Nano
    if "nano" in model_lower:
        return "NVIDIA Jetson Nano"
    
    # Generic fallback - use model string directly but prefix with NVIDIA
    if not model.startswith("NVIDIA"):
        return f"NVIDIA {model}"
    return model

class InferenceMetricLogger:
    """
    Background aggregator for worker metrics with periodic publishing.
    
    This class:
    - Runs on a dedicated background thread using threading.Timer
    - Periodically collects metrics from all workers via StreamingPipeline
    - Aggregates by worker_type (merges multiple instances)
    - Produces InferenceMetricLog matching the required schema
    - Publishes via configurable MetricPublisher
    - Handles graceful shutdown with timeout
    
    Thread Safety:
        - Timer-based execution ensures single aggregator thread
        - Worker metrics use internal locks for snapshot operations
        - No shared mutable state between collection cycles
    
    Lifecycle:
        logger = InferenceMetricLogger(pipeline, ...)
        logger.start()
        # ... runs in background ...
        logger.stop(timeout=10)
    """
    
    def __init__(
        self,
        streaming_pipeline: Any,  # StreamingPipeline reference
        interval_seconds: float = 60.0,  # 2 minutes default
        publisher: Optional[MetricPublisher] = None,
        deployment_id: Optional[str] = None,
        deployment_instance_id: Optional[str] = None,
        app_deploy_id: Optional[str] = None,
        action_id: Optional[str] = None,
        app_id: Optional[str] = None,
        log_metrics_every_n: int = 5,  # Log detailed metrics every N collections
        multiprocess_metrics_queue: Optional[mp.Queue] = None,
    ):
        """
        Initialize metric logger.
        
        Args:
            streaming_pipeline: Reference to StreamingPipeline instance
            interval_seconds: Reporting interval (INFERENCE_METRIC_LOGGING_INTERVAL)
            publisher: MetricPublisher implementation (defaults to Kafka)
            deployment_id: Deployment identifier for metric log
            deployment_instance_id: Deployment instance identifier for metric log
            app_deploy_id: App deployment identifier
            action_id: Action identifier
            app_id: Application identifier
            log_metrics_every_n: Log detailed metrics every N collections (0 = never)
            multiprocess_metrics_queue: Shared queue for receiving metrics from worker processes
        """
        self.pipeline = streaming_pipeline
        self.interval_seconds = interval_seconds
        self.publisher = publisher
        self.log_metrics_every_n = log_metrics_every_n
        
        # NOTE : Opt 1: Use `action_details` but API call overhead
        # NOTE : Opt 2: Extract these params from `server.py` via streaming_pipeline
        
        # Metric log identifiers
        self.deployment_id = deployment_id 
        self.deployment_instance_id = deployment_instance_id
        self.app_deploy_id = app_deploy_id
        self.action_id = action_id
        self.app_id = app_id

        # Multiprocess metrics collector for inference and post_processing workers
        # These workers run in separate processes and send metrics via queue
        self._multiprocess_collector: Optional[MultiprocessMetricsCollector] = None
        if multiprocess_metrics_queue is not None:
            self._multiprocess_collector = MultiprocessMetricsCollector(multiprocess_metrics_queue)
            logger.info("Initialized MultiprocessMetricsCollector for worker process metrics")

        # GPU detection (cached - GPU name doesn't change during runtime)
        self._gpu_name: Optional[str] = self._detect_gpu_name()

        # State
        self._running = False
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()
        self._last_collection_time = time.time()
        
        # Statistics
        self._total_collections = 0
        self._failed_collections = 0
        self._failed_publishes = 0
        self._skipped_publishes = 0  # Count of skipped publishes due to no data
        
        logger.info(
            f"Initialized InferenceMetricLogger: "
            f"interval={interval_seconds}s, "
            f"log_metrics_every_n={log_metrics_every_n}, "
            f"deployment_id={self.deployment_id}, "
            f"deployment_instance_id={self.deployment_instance_id}, "
            f"multiprocess_collector={'enabled' if self._multiprocess_collector else 'disabled'}, "
            f"gpu_name={self._gpu_name}"
        )
    
    def _detect_gpu_name(self) -> Optional[str]:
        """
        Detect GPU name with error handling.
        
        Called once during initialization and cached for the lifetime
        of the metric logger.
        
        Returns:
            GPU name string or None if detection failed
        """
        try:
            gpu_name = get_gpu_name()
            if gpu_name:
                logger.info(f"Detected GPU: {gpu_name}")
            else:
                logger.info("No GPU detected or GPU detection not supported")
            return gpu_name
        except Exception as e:
            logger.error(f"Error detecting GPU name: {e}", exc_info=True)
            return None
    
    def start(self) -> None:
        """
        Start the background metric collection loop.
        
        Spawns a timer-based thread that wakes every interval_seconds
        to collect and publish metrics.
        
        Thread Safety:
            Uses lock to prevent multiple start calls from creating
            duplicate timer threads.
        """
        with self._lock:
            if self._running:
                logger.warning("Metric logger already running")
                return
            
            self._running = True
            self._last_collection_time = time.time()
            
            # Initialize default publisher if none provided
            if self.publisher is None:
                try:
                    self.publisher = KafkaMetricPublisher()
                except Exception as e:
                    logger.warning(
                        f"Failed to initialize Kafka publisher: {e}. "
                        f"Using NoOp publisher."
                    )
                    self.publisher = NoOpMetricPublisher()
            
            # Start timer loop
            self._schedule_next_collection()
            
            logger.info("Metric logger started")
    
    def stop(self, timeout: float = 10.0) -> None:
        """
        Stop the background metric collection loop.
        
        Args:
            timeout: Maximum time to wait for final collection (seconds)
        
        Note:
            Performs one final collection before stopping to avoid
            losing metrics from the last interval.
        """
        with self._lock:
            if not self._running:
                return
            
            self._running = False
            
            # Cancel pending timer
            if self._timer:
                self._timer.cancel()
                self._timer = None
        
        # Final collection outside lock to avoid deadlock
        try:
            logger.info("Performing final metric collection...")
            self._collect_and_publish()
        except Exception as e:
            logger.error(f"Error during final collection: {e}")
        
        # Close publisher
        if self.publisher:
            try:
                self.publisher.close()
            except Exception as e:
                logger.error(f"Error closing publisher: {e}")
        
        logger.info(
            f"Metric logger stopped. "
            f"Collections: {self._total_collections}, "
            f"Skipped (no data): {self._skipped_publishes}, "
            f"Failed: {self._failed_collections}, "
            f"Publish failures: {self._failed_publishes}"
        )
    
    def wait(self, timeout: Optional[float] = None) -> None:
        """
        Wait for the metric logger to stop.
        
        Args:
            timeout: Maximum time to wait (None = wait indefinitely)
        
        Note:
            This is a passive wait - use stop() to actually stop the logger.
        """
        start_time = time.time()
        
        while self._running:
            if timeout and (time.time() - start_time) >= timeout:
                logger.warning(f"Wait timeout after {timeout}s")
                break
            time.sleep(0.1)
    
    def _schedule_next_collection(self) -> None:
        """Schedule the next metric collection using threading.Timer."""
        if not self._running:
            return
        
        self._timer = threading.Timer(
            self.interval_seconds,
            self._timer_callback
        )
        self._timer.daemon = False  # Non-daemon for graceful shutdown
        self._timer.start()
    
    def _timer_callback(self) -> None:
        """Timer callback that performs collection and reschedules."""
        try:
            self._collect_and_publish()
        except Exception as e:
            logger.error(f"Error in metric collection: {e}", exc_info=True)
            self._failed_collections += 1
        finally:
            # Schedule next collection
            self._schedule_next_collection()
    
    def _collect_and_publish(self) -> None:
        """
        Collect metrics from all workers, aggregate, and publish.
        
        This method:
        1. Determines interval boundaries
        2. Collects snapshots from all active workers
        3. Aggregates by worker_type
        4. Builds InferenceMetricLog
        5. Publishes via configured publisher
        6. Resets worker metrics for next interval
        """
        interval_end = time.time()
        interval_start = self._last_collection_time
        self._last_collection_time = interval_end
        
        try:
            # Collect snapshots from all workers
            snapshots = self._collect_worker_snapshots(interval_start, interval_end)

            # Aggregate by worker type (empty snapshots will result in all inactive metrics)
            aggregated = self._aggregate_by_type(snapshots)

            # Check if there's any actual data to publish
            has_data = self._has_metric_data(aggregated)

            # ALWAYS publish metrics, even when all workers are inactive (zero metrics)
            # This ensures backend visibility into deployment instance health
            if not has_data:
                self._skipped_publishes += 1
                logger.debug(
                    f"Publishing zero metrics (all workers inactive) for interval={self.interval_seconds}s "
                    f"(total inactive intervals: {self._skipped_publishes})"
                )
                # Continue to build and publish metric_log (don't return early)

            # Build metric log
            metric_log = self._build_metric_log(aggregated, interval_end)
            
            # Log detailed metrics info every N collections
            # if self.log_metrics_every_n > 0 and (self._total_collections + 1) % self.log_metrics_every_n == 0:
            self._log_detailed_metrics(aggregated, metric_log)
            
            # Publish
            success = self.publisher.publish(metric_log)
            
            if success:
                self._total_collections += 1
                # List which worker types are currently active
                active_types = [k for k, v in aggregated.items() if v.get('active')]
                logger.info(
                    f"Published metrics: interval={self.interval_seconds}s, "
                    f"workers={len(snapshots)}, "
                    f"active_types={active_types}, "
                    f"timestamp={metric_log['timestamp']}"
                )
            else:
                self._failed_publishes += 1
                logger.error("Failed to publish metric log")
                
        except Exception as e:
            logger.error(f"Error collecting/publishing metrics: {e}", exc_info=True)
            self._failed_collections += 1
    
    def _collect_worker_snapshots(self, interval_start: float, interval_end: float) -> List[MetricSnapshot]:
        """
        Collect snapshots from all worker types.
        
        Collection Strategy:
        - Consumer: Threading-based, uses WorkerMetrics.get_shared() (same process)
        - Producer: Threading-based, uses WorkerMetrics.get_shared() (same process)
        - Inference: Multiprocessing-based, uses MultiprocessMetricsCollector (cross-process queue)
        - Post-processing: Multiprocessing-based, uses MultiprocessMetricsCollector (cross-process queue)
        """
        snapshots = []
        worker_types_collected = set()

        try:
            # Consumer metrics (AsyncConsumerManager - runs in main process event loop)
            # Uses threading-based WorkerMetrics (shared memory within same process)
            if self.pipeline.consumer_manager and "consumer" not in worker_types_collected:
                try:
                    snapshot = self.pipeline.consumer_manager.metrics.snapshot_and_reset(
                        interval_start, interval_end
                    )
                    snapshots.append(snapshot)
                    worker_types_collected.add("consumer")
                except Exception as e:
                    logger.warning(f"Error collecting consumer metrics: {e}")

            # Inference workers (multiprocessing pool - runs in separate processes)
            # Uses MultiprocessMetricsCollector to aggregate metrics from worker processes
            if self.pipeline.inference_pool and "inference" not in worker_types_collected:
                try:
                    if self._multiprocess_collector:
                        # Collect from multiprocess queue
                        snapshot = self._multiprocess_collector.snapshot_and_reset(
                            "inference", interval_start, interval_end
                        )
                        snapshots.append(snapshot)
                        worker_types_collected.add("inference")
                    else:
                        logger.debug("No multiprocess collector for inference metrics")
                except Exception as e:
                    logger.warning(f"Error collecting inference metrics: {e}")

            # Post-processing workers (multiprocessing pool - runs in separate processes)
            # Uses MultiprocessMetricsCollector to aggregate metrics from worker processes
            if self.pipeline.postproc_pool and "post_processing" not in worker_types_collected:
                try:
                    if self._multiprocess_collector:
                        # Collect from multiprocess queue
                        snapshot = self._multiprocess_collector.snapshot_and_reset(
                            "post_processing", interval_start, interval_end
                        )
                        snapshots.append(snapshot)
                        worker_types_collected.add("post_processing")
                    else:
                        logger.debug("No multiprocess collector for post_processing metrics")
                except Exception as e:
                    logger.warning(f"Error collecting post-processing metrics: {e}")

            # Producer pool (async pool - runs in dedicated thread with event loop)
            # Uses shared WorkerMetrics instance within AsyncProducerPool
            if self.pipeline.producer_pool and "producer" not in worker_types_collected:
                try:
                    snapshot = self.pipeline.producer_pool.metrics.snapshot_and_reset(interval_start, interval_end)
                    snapshots.append(snapshot)
                    worker_types_collected.add("producer")
                except Exception as e:
                    logger.warning(f"Error collecting producer metrics: {e}")

        except Exception as e:
            logger.error(f"Error accessing pipeline workers: {e}", exc_info=True)

        return snapshots
    
    def _aggregate_by_type(
        self,
        snapshots: List[MetricSnapshot]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Aggregate snapshots by worker_type.
        
        Combines metrics from multiple workers of the same type
        (e.g., multiple consumer instances) into single aggregated stats.
        
        Args:
            snapshots: List of MetricSnapshot objects
        
        Returns:
            Dictionary mapping worker_type to aggregated statistics
        """
        # Group snapshots by type
        by_type: Dict[str, List[MetricSnapshot]] = {
            "consumer": [],
            "inference": [],
            "post_processing": [],
            "producer": []
        }
        
        for snapshot in snapshots:
            if snapshot.worker_type in by_type:
                by_type[snapshot.worker_type].append(snapshot)
        
        # Aggregate each type
        aggregated = {}
        
        for worker_type, type_snapshots in by_type.items():
            if type_snapshots:
                aggregated[worker_type] = self._aggregate_snapshots(type_snapshots)
            else:
                # No active workers of this type - use inactive metrics
                aggregated[worker_type] = self._inactive_metrics()
        
        return aggregated
    
    def _aggregate_snapshots(self, snapshots: List[MetricSnapshot]) -> Dict[str, Any]:
        """
        Aggregate multiple snapshots into combined latency and throughput statistics.
        """
        if not snapshots:
            return self._inactive_metrics()

        all_latency_samples = []
        throughput_rates = []
        any_active = False

        # Default fallback for zero/negative intervals
        FALLBACK_INTERVAL = 1.0

        total_throughput = 0

        for snapshot in snapshots:
            # Compute per-snapshot interval with validation
            interval_seconds = snapshot.interval_end_ts - snapshot.interval_start_ts
            if interval_seconds <= 0:
                logger.warning(
                    f"Invalid interval for worker {snapshot.worker_id}: "
                    f"start={snapshot.interval_start_ts}, end={snapshot.interval_end_ts}, "
                    f"using fallback {FALLBACK_INTERVAL}s"
                )
                interval_seconds = FALLBACK_INTERVAL

            # Compute and record per-worker rate
            worker_rate = snapshot.throughput_count / interval_seconds
            throughput_rates.append(worker_rate)

            # Aggregate latency and throughput data
            all_latency_samples.extend(snapshot.latency_samples)
            total_throughput += snapshot.throughput_count
            any_active = any_active or snapshot.was_active

        # Use modular stat calculators
        latency_stats = self._compute_latency_stats(all_latency_samples)
        throughput_stats = self._compute_throughput_stats(throughput_rates)

        result = {
            "active": any_active,
            "total_throughput": total_throughput
        }
        
        # Only include stats if we have data
        if latency_stats:
            result["latency"] = latency_stats
        if throughput_stats:
            result["throughput"] = throughput_stats
        
        return result

    
    def _compute_latency_stats(self, samples: List[float]) -> Dict[str, Any]:
        """
        Compute latency statistics from samples.
        
        Args:
            samples: List of latency measurements in milliseconds
        
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
            "p50": WorkerMetrics._percentile(sorted_samples, 50),
            "p100": sorted_samples[-1],
            "unit": "ms"
        }
    
    def _compute_throughput_stats(self, rates: List[float]) -> Dict[str, Any]:
        """
        Compute throughput statistics from per-worker rates.

        Args:
            rates: List of per-worker throughput rates (msg/sec)

        Returns:
            Dictionary with min, max, avg, p0, p50, p100, unit
            Returns empty dict if no rates
        """
        if not rates:
            return {}

        sorted_rates = sorted(rates)
        n = len(sorted_rates)

        return {
            "min": sorted_rates[0],
            "max": sorted_rates[-1],
            "avg": sum(sorted_rates) / n,
            "p0": sorted_rates[0],
            "p50": WorkerMetrics._percentile(sorted_rates, 50),
            "p100": sorted_rates[-1],
            "unit": "msg/sec"
        }

    
    def _inactive_metrics(self) -> Dict[str, Any]:
        """
        Generate metrics structure for inactive worker type.
        
        Returns:
            Dictionary with only active=False, no metric data
        """
        return {
            "active": False
        }
    
    def _has_metric_data(self, aggregated: Dict[str, Dict[str, Any]]) -> bool:
        """
        Check if aggregated metrics contain any actual data.
        
        Args:
            aggregated: Aggregated metrics by worker_type
        
        Returns:
            True if any worker has latency or throughput data, False otherwise
        """
        for worker_type, metrics in aggregated.items():
            # Check if worker has any actual metric data (not just active flag)
            if "latency" in metrics or "throughput" in metrics:
                return True
        return False
    
    def _log_detailed_metrics(self, aggregated: Dict[str, Dict[str, Any]], metric_log: Dict[str, Any]) -> None:
        """
        Log detailed metrics information for debugging and monitoring.
        
        Args:
            aggregated: Aggregated metrics by worker_type
            metric_log: The complete metric log being published
        """
        logger.info("=" * 80)
        logger.info(f"DETAILED METRICS REPORT (Collection #{self._total_collections + 1})")
        logger.info(f"Timestamp: {metric_log['timestamp']}")
        logger.info(f"Deployment: {self.deployment_id} / Instance: {self.deployment_instance_id}")
        logger.info(f"GPU: {self._gpu_name or 'Not detected'}")
        logger.info("-" * 80)
        
        for worker_type in ["consumer", "inference", "post_processing", "producer"]:
            metrics = aggregated.get(worker_type, {})

            # Always show consistent structure for all worker types
            active_status = "ACTIVE" if metrics.get("active") else "INACTIVE"
            logger.info(f"{worker_type.upper()}: {active_status}")

            # Latency metrics
            if "latency" in metrics:
                lat = metrics["latency"]
                logger.info(
                    f"  Latency: "
                    f"min={lat.get('min', 0):.2f}{lat.get('unit', 'ms')}, "
                    f"avg={lat.get('avg', 0):.2f}{lat.get('unit', 'ms')}, "
                    f"p50={lat.get('p50', 0):.2f}{lat.get('unit', 'ms')}, "
                    f"max={lat.get('max', 0):.2f}{lat.get('unit', 'ms')}"
                )
            else:
                logger.info("  Latency: No data")

            # Throughput metrics
            if "throughput" in metrics:
                tput = metrics["throughput"]
                logger.info(
                    f"  Throughput: "
                    f"min={tput.get('min', 0):.2f}{tput.get('unit', '')}, "
                    f"avg={tput.get('avg', 0):.2f}{tput.get('unit', '')}, "
                    f"p50={tput.get('p50', 0):.2f}{tput.get('unit', '')}, "
                    f"max={tput.get('max', 0):.2f}{tput.get('unit', '')}"
                )
            else:
                logger.info("  Throughput: No data")

            # Total throughput if available
            if "total_throughput" in metrics:
                logger.info(f"  Total Items: {metrics['total_throughput']}")
        
        logger.info("-" * 80)
        logger.info(
            f"Stats: Total={self._total_collections + 1}, "
            f"Skipped={self._skipped_publishes}, "
            f"Failed={self._failed_collections}, "
            f"Publish Failures={self._failed_publishes}"
        )
        logger.info("=" * 80)
    
    def _build_metric_log(
        self,
        aggregated: Dict[str, Dict[str, Any]],
        timestamp: float
    ) -> Dict[str, Any]:
        """
        Build InferenceMetricLog matching required schema.
        
        Args:
            aggregated: Aggregated metrics by worker_type
            timestamp: Collection timestamp (Unix epoch)
        
        Returns:
            InferenceMetricLog dictionary ready for publishing
            Only includes worker types that have data
        """
        # Convert timestamp to ISO8601 UTC
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        iso_timestamp = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Build metrics dict - ALWAYS include all worker types for backend visibility
        # Even inactive workers should be reported so backend can distinguish:
        # - Healthy workers that are idle vs crashed/failed workers
        metrics = {}
        for worker_type in ["consumer", "inference", "post_processing", "producer"]:
            worker_metrics = aggregated.get(worker_type, self._inactive_metrics())
            # Always include - backend needs to see all workers regardless of active state
            metrics[worker_type] = worker_metrics
        
        metric_log = {
            "deployment_id": self.deployment_id,
            "deployment_instance_id": self.deployment_instance_id,
            "app_deploy_id": self.app_deploy_id,
            "action_id": self.action_id,
            "app_id": self.app_id,
            "timestamp": iso_timestamp,
            "metrics": metrics
        }
        
        # Include GPU name if detected (None means no GPU or detection failed)
        if self._gpu_name is not None:
            metric_log["gpu_name"] = self._gpu_name
        
        return metric_log
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get logger statistics.
        
        Returns:
            Dictionary with collection statistics
        """
        return {
            "running": self._running,
            "interval_seconds": self.interval_seconds,
            "log_metrics_every_n": self.log_metrics_every_n,
            "total_collections": self._total_collections,
            "skipped_publishes": self._skipped_publishes,
            "failed_collections": self._failed_collections,
            "failed_publishes": self._failed_publishes,
            "last_collection_time": self._last_collection_time,
            "gpu_name": self._gpu_name
        }