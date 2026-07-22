"""
High-throughput async streaming pipeline optimized for 10K+ FPS inference at scale.

Architecture (Async + Multiprocessing):
Consumer (async event loop + ProcessPool for decode) -> asyncio.Queue ->
Inference (async workers with dynamic batching) -> asyncio.Queue ->
Post-processing (multiprocess with per-camera routing) -> asyncio.Queue ->
Producer (async output with batching)

Key Optimizations:
- Async event loop for 1000+ camera streams (no GIL contention)
- ProcessPoolExecutor for CPU-bound H.265 decode (true parallelism)
- 8 async inference workers with dynamic batching (80%+ GPU utilization)
- Multiprocess post-processing with camera-based routing (stateful tracking isolation)
- asyncio.Queue with backpressure (prevents OOM under load)
- Shared Triton client on pipeline event loop (eliminates event loop conflicts)

Performance Targets:
- Throughput: 10,000 FPS
- Latency: <500ms (P50), <800ms (P99)
- GPU Utilization: 85%+
- Memory: Stable under sustained load
"""

import asyncio
import logging
import multiprocessing as mp
import os
import sys
import threading
from typing import Any, Dict, List, Optional

from matrice_inference.server.inference_interface import InferenceInterface
from matrice_inference.server.stream.analytics_publisher import AnalyticsPublisher
from matrice_inference.server.stream.async_producer_pool import AsyncProducerPool
from matrice_inference.server.stream.consumer_manager import AsyncConsumerManager
from matrice_inference.server.stream.inference_worker import MultiprocessInferencePool
from matrice_inference.server.stream.post_processing_manager import (
    MultiprocessPostProcessingPool,
)
from matrice_inference.server.stream.utils import CameraConfig

# Set multiprocessing start method to 'spawn' for CUDA compatibility
# This must be done before any multiprocessing.Process is created
# 'spawn' is required for CUDA because 'fork' doesn't work with CUDA contexts
try:
    mp.set_start_method("spawn", force=True)
except RuntimeError:
    # Already set, ignore
    pass


class StreamingPipeline:
    """Optimized streaming pipeline with dynamic camera configuration and clean resource management."""

    DEFAULT_QUEUE_SIZE = 5000  # RESTORED from 1000 (was causing starvation)
    DEFAULT_MESSAGE_TIMEOUT = 10.0
    DEFAULT_INFERENCE_TIMEOUT = 30.0
    DEFAULT_SHUTDOWN_TIMEOUT = 30.0
    DEFAULT_METRIC_INTERVAL = 60.0  # 1 minutes (consistent with inference_metric_logger default)

    def __init__(
        self,
        inference_interface: Optional[InferenceInterface] = None,
        inference_queue_maxsize: int = DEFAULT_QUEUE_SIZE,
        postproc_queue_maxsize: int = DEFAULT_QUEUE_SIZE,
        output_queue_maxsize: int = DEFAULT_QUEUE_SIZE,
        message_timeout: float = DEFAULT_MESSAGE_TIMEOUT,
        inference_timeout: float = DEFAULT_INFERENCE_TIMEOUT,
        shutdown_timeout: float = DEFAULT_SHUTDOWN_TIMEOUT,
        camera_configs: Optional[Dict[str, CameraConfig]] = None,
        app_deployment_id: Optional[str] = None,
        inference_pipeline_id: Optional[str] = None,
        enable_analytics_publisher: bool = True,
        deployment_id: Optional[str] = None,
        deployment_instance_id: Optional[str] = None,
        action_id: Optional[str] = None,
        app_id: Optional[str] = None,
        app_name: Optional[str] = None,
        app_version: Optional[str] = None,
        use_shared_metrics: Optional[bool] = True,
        enable_metric_logging: bool = True,
        metric_logging_interval: float = DEFAULT_METRIC_INTERVAL,
        frame_cache_worker_threads: int = 20,
        frame_cache_max_queue: int = 50000,
        frame_cache_max_connections: int = 200,
        # Predict functions from MatriceDeployServer (passed to inference workers)
        load_model: Optional[Any] = None,
        predict: Optional[Any] = None,
        async_predict: Optional[Any] = None,
        async_batch_predict: Optional[Any] = None,
        async_load_model: Optional[Any] = None,
        batch_predict: Optional[Any] = None,
        # Post-processing configuration (passed as dict instead of extracted from post_processor)
        post_processing_config: Optional[Dict[str, Any]] = None,
        index_to_category: Optional[Any] = None,
        target_categories: Optional[Any] = None,
        # Flow control and drop behavior (Phase 1 optimization)
        enable_flow_control: bool = True,
        max_in_flight_frames: int = 256,
        enable_drop_on_backpressure: bool = True,
        drop_stale_frames: bool = True,
        frame_staleness_ms: float = 500.0,
        # Queue tuning (configurable overrides)
        consumer_queue_max: int = 2000,
        consumer_batch_size: int = 500,
        # Worker count control
        is_inference_API: bool = False,
    ):
        self.inference_interface = inference_interface
        self.is_inference_API = is_inference_API
        self.message_timeout = message_timeout
        self.inference_timeout = inference_timeout
        self.shutdown_timeout = shutdown_timeout
        self.app_deployment_id = app_deployment_id
        self.inference_pipeline_id = inference_pipeline_id
        self.enable_analytics_publisher = enable_analytics_publisher

        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.action_id = action_id
        self.app_id = app_id
        self.app_name = app_name
        self.app_version = app_version

        # Store post-processing configuration (passed as dict, not extracted from post_processor)
        self.post_processing_config = post_processing_config or {}
        self.index_to_category = index_to_category
        self.target_categories = target_categories

        # Metric logging configuration
        self.enable_metric_logging = enable_metric_logging
        self.metric_logging_interval = metric_logging_interval
        self.use_shared_metrics = use_shared_metrics

        # Frame cache configuration
        self.frame_cache_worker_threads = frame_cache_worker_threads
        self.frame_cache_max_queue = frame_cache_max_queue
        self.frame_cache_max_connections = frame_cache_max_connections

        # Store predict functions from MatriceDeployServer (for passing to workers)
        self.load_model = load_model
        self.predict = predict
        self.async_predict = async_predict
        self.async_batch_predict = async_batch_predict
        self.async_load_model = async_load_model
        self.batch_predict = batch_predict

        # Flow control and drop behavior (Phase 1 optimization)
        self.enable_flow_control = enable_flow_control
        self.max_in_flight_frames = max_in_flight_frames
        self.enable_drop_on_backpressure = enable_drop_on_backpressure
        self.drop_stale_frames = drop_stale_frames
        self.frame_staleness_ms = frame_staleness_ms
        self.consumer_queue_max = consumer_queue_max
        self.consumer_batch_size = consumer_batch_size

        self.camera_configs: Dict[str, CameraConfig] = camera_configs or {}
        self.running = False
        self.logger = logging.getLogger(__name__)

        # Event loop reference for async operations (set when pipeline starts)
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
        self._event_loop_thread: Optional[threading.Thread] = None
        self._loop_thread_running = False
        # Signalled by the event-loop thread once it is ready (or has failed),
        # so startup can wait on an Event instead of busy-polling a flag.
        self._loop_ready_event = threading.Event()

        self._setup_queues(inference_queue_maxsize, postproc_queue_maxsize, output_queue_maxsize)
        self._setup_executors()
        self._setup_workers()
        # Frame cache instance (initialized lazily at start)
        self.frame_cache = None
        # Analytics publisher instance (initialized lazily at start)
        self.analytics_publisher = None
        # Metric logger instance (initialized lazily at start)
        self.metric_logger = None

    def _setup_queues(self, inference_size: int, postproc_size: int, output_size: int) -> None:
        """Initialize multiprocessing queues for pipeline stages.

        Uses PER-WORKER queues for inference and post-processing stages:
        - Consumer routes frames to specific worker queue based on hash(camera_id)
        - Each worker only reads from its assigned queue
        - No re-queuing → No race conditions → Order preserved per camera
        - True parallelism across different cameras

        Output queue remains single (producer is single-threaded).

        OPTIMIZATION: Uses native mp.Queue on Linux for 30-50% better throughput.
        On Windows with spawn mode, mp.Queue cannot be pickled, so Manager queues are used.
        """

        # Platform detection for optimal queue selection
        # Linux: Native mp.Queue (30-50% faster, no proxy overhead)
        # Windows: Manager().Queue() (required for spawn mode pickling)
        self._use_native_queues = sys.platform != "win32"

        if self._use_native_queues:
            self.queue_manager = None  # Not needed on Linux
            self.logger.info("Using native mp.Queue for optimal Linux performance")
        else:
            # Create a Manager for creating shared queues that can be pickled (Windows)
            self.queue_manager = mp.Manager()
            self.logger.info("Using Manager.Queue for Windows compatibility")

        # Store maxsize for per-worker queue creation (queues created in _setup_executors)
        self.inference_queue_maxsize = inference_size
        self.postproc_queue_maxsize = postproc_size
        self.output_queue_maxsize = output_size

        # Per-worker queues will be created in _setup_executors() after worker counts are known
        self.inference_queues = []  # List[Queue] - one per inference worker
        self.postproc_queues = []  # List[Queue] - one per postproc worker

        # Per-worker output queues (one per postproc worker) for reduced lock contention
        # Producer polls from all queues using round-robin
        # Note: output_queues created in _setup_executors() after worker count is known
        self.output_queues = []  # List[Queue] - one per postproc worker

        # NOTE: Direct API calls (e.g., identity images from proxy_interface) now use
        # the main process model directly via InferenceInterface.inference().
        # This avoids worker queue routing overhead and simplifies the architecture.
        # The streaming pipeline handles continuous frame processing separately.

        # Shared metrics queue for multiprocessing workers (inference + post_processing)
        # Workers in separate processes send MetricUpdate messages to this queue
        # The InferenceMetricLogger drains this queue and aggregates metrics
        self.multiprocess_metrics_queue = self._create_queue(maxsize=10000)

    def _create_queue(self, maxsize: int) -> mp.Queue:
        """Create a queue using the optimal method for the platform.

        Linux: Native mp.Queue (30-50% faster, no proxy overhead)
        Windows: Manager().Queue() (required for spawn mode pickling)

        Args:
            maxsize: Maximum queue size

        Returns:
            Multiprocessing queue instance
        """
        if self._use_native_queues:
            return mp.Queue(maxsize=maxsize)
        return self.queue_manager.Queue(maxsize=maxsize)

    def _setup_executors(self) -> None:
        """Initialize per-worker queues and worker counts for ordering-preserving parallelism.

        Uses PER-WORKER QUEUES with consumer-side routing:
        - Consumer routes frames to worker queue based on hash(camera_id) % num_workers
        - Each worker reads from its dedicated queue only
        - No re-queuing → No race conditions → 100% order preserved per camera
        - True parallelism across different cameras

        Worker count is dynamic based on CPU cores:
        - 50% of CPU count (int) - Phase 2 optimized
        - Minimum: 4 workers
        - Maximum: 16 workers
        """

        cpu_count = os.cpu_count() or 4

        # Calculate dynamic worker count: 100% of CPU count, min 4, max 16
        # Phase 3 optimization: Increased from 50% to 100% to match inference throughput
        dynamic_worker_count = max(4, min(8, cpu_count))

        # Inference workers: Use dynamic count for true parallelism (no GIL)
        # Each worker process has its own model instance
        self.use_async_inference = self.inference_interface.has_async_predict() if self.inference_interface else False

        # Override worker count if not an inference API
        # When is_inference_API=False, use only 1 worker to avoid loading model multiple times
        if not self.is_inference_API:
            self.num_inference_workers = 1
            self.logger.info(
                "is_inference_API=False: Using single inference worker to avoid loading model multiple times"
            )
        else:
            self.num_inference_workers = dynamic_worker_count

        # Post-processing workers: Match inference workers for balanced pipeline
        self.num_postproc_workers = dynamic_worker_count

        # Create per-worker inference queues (one queue per worker)
        # Uses native mp.Queue on Linux, Manager.Queue on Windows
        self.inference_queues = [
            self._create_queue(maxsize=self.inference_queue_maxsize) for _ in range(self.num_inference_workers)
        ]
        queue_type = "mp.Queue" if self._use_native_queues else "Manager.Queue"
        self.logger.info(
            f"Created {len(self.inference_queues)} inference queues ({queue_type}) "
            f"(one per worker, maxsize={self.inference_queue_maxsize})"
        )

        # Create per-worker post-processing queues (one queue per worker)
        # Uses native mp.Queue on Linux, Manager.Queue on Windows
        self.postproc_queues = [
            self._create_queue(maxsize=self.postproc_queue_maxsize) for _ in range(self.num_postproc_workers)
        ]
        self.logger.info(
            f"Created {len(self.postproc_queues)} post-processing queues ({queue_type}) "
            f"(one per worker, maxsize={self.postproc_queue_maxsize})"
        )

        # Create per-worker OUTPUT queues (one per postproc worker)
        # This eliminates lock contention when multiple workers write to output
        # Producer polls from all queues using round-robin
        self.output_queues = [
            self._create_queue(maxsize=self.output_queue_maxsize) for _ in range(self.num_postproc_workers)
        ]
        self.logger.info(
            f"Created {len(self.output_queues)} output queues ({queue_type}) "
            f"(one per postproc worker, maxsize={self.output_queue_maxsize})"
        )

        # Note: No ThreadPoolExecutor - workers manage their own async tasks
        self.inference_executor = None
        self.postprocessing_executor = None

        self.logger.info(
            f"Initialized per-worker queue architecture: "
            f"inference_workers={self.num_inference_workers}, "
            f"postproc_workers={self.num_postproc_workers} "
            f"(cpu_count={cpu_count}, dynamic={dynamic_worker_count}, min=4, max=8, ordering=PRESERVED)"
        )

    def _setup_workers(self) -> None:
        """Initialize worker containers."""
        self.consumer_manager: Optional[AsyncConsumerManager] = None  # Async consumer manager
        self.inference_pool: Optional[MultiprocessInferencePool] = None  # Multiprocess inference pool
        self.postproc_pool: Optional[MultiprocessPostProcessingPool] = None  # Multiprocess post-processing pool
        self.producer_pool: Optional[AsyncProducerPool] = None  # Shared async producer pool
        self.worker_threads: List = []

    def _run_event_loop(self) -> None:
        """Run event loop in dedicated thread for the lifetime of the pipeline."""
        try:
            self._event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._event_loop)
            self._loop_thread_running = True
        finally:
            # Always wake the startup waiter, even if loop creation failed,
            # so start() does not block for the full timeout on failure.
            self._loop_ready_event.set()

        self.logger.info("Event loop thread started")

        try:
            # Run the event loop forever until stop() is called
            self._event_loop.run_forever()
        finally:
            self.logger.info("Event loop thread stopping")
            # Clean up pending tasks
            pending = asyncio.all_tasks(self._event_loop)
            for task in pending:
                task.cancel()
            # Allow tasks to complete cancellation
            self._event_loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            self._event_loop.close()
            self._loop_thread_running = False
            self.logger.info("Event loop thread stopped")

    def start(self) -> None:
        """Start the pipeline with proper error handling."""
        if self.running:
            self.logger.warning("Pipeline already running")
            return

        self.running = True

        # Start dedicated event loop thread
        self._event_loop_thread = threading.Thread(target=self._run_event_loop, daemon=True, name="PipelineEventLoop")
        self._event_loop_thread.start()

        # Wait for the event loop thread to signal readiness
        max_wait = 5.0
        self._loop_ready_event.wait(timeout=max_wait)

        if not self._loop_thread_running:
            self.logger.error("Event loop thread failed to start")
            self.running = False
            raise RuntimeError("Event loop thread failed to start")

        self.logger.info("Event loop thread ready")
        self.logger.info("Starting streaming pipeline...")

        try:
            # Initialize frame cache and analytics publisher ONLY if we have cameras
            # Otherwise, they'll be lazy-initialized when first camera arrives via refresh event
            if len(self.camera_configs) > 0:
                self._initialize_frame_cache()
                self._initialize_analytics_publisher()
                self.logger.info(
                    f"Initialized frame cache and analytics publisher with {len(self.camera_configs)} cameras at startup"
                )
            else:
                self.logger.info(
                    "No cameras at startup - frame cache and analytics publisher will be "
                    "lazy-initialized when first camera arrives via refresh event"
                )

            # Register event loop with InferenceInterface for thread-safe inference
            # Note: Models are NOT loaded here - inference workers load models independently
            # in each process for true parallelism (see inference_worker.py lines 101-118)
            if self.inference_interface:
                self.inference_interface.set_pipeline_event_loop(self._event_loop)
                self.logger.info("✓ Registered pipeline event loop with InferenceInterface")
            else:
                self.logger.info("No InferenceInterface provided, skipping event loop registration")

            # Create workers (producer needs analytics publisher reference)
            # Note: Inference workers load models independently in each process (multiprocessing)
            # This is INTENTIONAL for process isolation - each worker needs its own model instance
            # The duplicate loading ensures no shared state between processes (GIL-free parallelism)
            # Schedule the async operation on the event loop
            future = asyncio.run_coroutine_threadsafe(self._create_workers(), self._event_loop)
            future.result(timeout=30.0)  # Wait for completion
            # Start all workers including analytics publisher
            self._start_workers()
            # Initialize and start metric logger after workers are started
            self._initialize_metric_logger()
            self._log_startup_info()
        except Exception as e:
            self.logger.error(f"Failed to start pipeline: {e}")
            self.stop()
            raise

    def _initialize_metric_logger(self) -> None:
        """
        Initialize and start InferenceMetricLogger for periodic metric reporting.

        The metric logger:
        - Runs on a background thread with configurable interval
        - Collects metrics from all active workers
        - Aggregates by worker type (consumer/inference/post_processing/producer)
        - Uses MultiprocessMetricsCollector for inference/post_processing workers (cross-process)
        - Uses WorkerMetrics for consumer/producer workers (same process)
        - Publishes to Kafka via RPC
        - Gracefully handles initialization failures (logs warning, continues)
        """
        if not self.enable_metric_logging:
            self.logger.info("Metric logging disabled")
            return

        try:
            from matrice_inference.server.stream.inference_metric_logger import (
                InferenceMetricLogger,
            )

            self.metric_logger = InferenceMetricLogger(
                streaming_pipeline=self,
                interval_seconds=self.metric_logging_interval,
                # Will auto-initialize KafkaMetricPublisher
                publisher=None,
                deployment_id=self.deployment_id,
                deployment_instance_id=self.deployment_instance_id,
                app_deploy_id=self.app_deployment_id,
                action_id=self.action_id,
                app_id=self.app_id,
                # Pass the shared metrics queue for collecting from multiprocessing workers
                multiprocess_metrics_queue=self.multiprocess_metrics_queue,
            )

            # Start background collection
            self.metric_logger.start()

            self.logger.info(
                f"Initialized metric logger: interval={self.metric_logging_interval}s, "
                f"deployment_id={self.deployment_id}, "
                f"deployment_instance_id={self.deployment_instance_id}, "
                f"multiprocess_metrics_queue=enabled"
            )

        except ImportError as e:
            self.logger.warning(f"Metric logging dependencies not available: {e}. Continuing without metric logging.")
            self.metric_logger = None
        except Exception as e:
            self.logger.warning(f"Failed to initialize metric logger: {e}. Continuing without metric logging.")
            self.metric_logger = None

    def _log_startup_info(self) -> None:
        """Log pipeline startup information."""
        inference_info = f"InferencePool({self.num_inference_workers} workers)" if self.inference_pool else "None"
        consumer_info = "AsyncConsumerManager" if self.consumer_manager else "None"
        postproc_info = f"PostProcPool({self.num_postproc_workers} workers)" if self.postproc_pool else "None"
        producer_info = "AsyncProducerPool" if self.producer_pool else "None"

        if len(self.camera_configs) == 0:
            self.logger.info(
                f"Pipeline started with NO cameras - ready to accept dynamic camera configurations. "
                f"Inference: {inference_info}, PostProc: {postproc_info}, Producer: {producer_info}"
            )
        else:
            self.logger.info(
                f"Pipeline started - Cameras: {len(self.camera_configs)}, "
                f"Consumer: {consumer_info}, Inference: {inference_info}, "
                f"PostProc: {postproc_info}, Producer: {producer_info}"
            )

    def stop(self) -> None:
        """Stop the pipeline gracefully with proper cleanup."""
        if not self.running:
            return

        self.logger.info("Stopping pipeline...")
        self.running = False

        # Stop metric logger first (before stopping workers)
        if self.metric_logger:
            try:
                self.logger.info("Stopping metric logger...")
                self.metric_logger.stop(timeout=10.0)
                self.logger.info("Metric logger stopped")
            except Exception as e:
                self.logger.error(f"Error stopping metric logger: {e}")

        self._stop_workers()
        self._wait_for_threads()
        self._shutdown_executors()

        # Stop frame cache if running
        try:
            if self.frame_cache:
                self.frame_cache.stop()
                self.logger.info("Frame cache stopped")
        except Exception as e:
            self.logger.error(f"Error stopping frame cache: {e}")

        # Note: analytics_publisher.stop() is called in _stop_workers() before _wait_for_threads()
        # to ensure the thread is signaled to stop before we wait for it to complete

        # Stop event loop thread
        if self._event_loop and self._loop_thread_running:
            try:
                self.logger.info("Stopping event loop thread...")
                self._event_loop.call_soon_threadsafe(self._event_loop.stop)
                if self._event_loop_thread:
                    self._event_loop_thread.join(timeout=5.0)
                self.logger.info("Event loop thread stopped")
            except Exception as e:
                self.logger.error(f"Error stopping event loop thread: {e}")

        # Shutdown queue manager (None on Linux, where native mp.Queue is used)
        if getattr(self, "queue_manager", None) is not None:
            try:
                self.logger.info("Shutting down queue manager...")
                self.queue_manager.shutdown()
                self.logger.info("Queue manager shutdown complete")
            except Exception as e:
                self.logger.error(f"Error shutting down queue manager: {e}")

        self.logger.info("Pipeline stopped")

    def _wait_for_threads(self) -> None:
        """Wait for all worker threads to complete."""
        for thread in self.worker_threads:
            if thread.is_alive():
                thread.join(timeout=self.shutdown_timeout)

    def _shutdown_executors(self) -> None:
        """Shutdown thread pool executors (if they exist)."""
        if self.inference_executor is not None:
            self.inference_executor.shutdown(wait=False)
        if self.postprocessing_executor is not None:
            self.postprocessing_executor.shutdown(wait=False)

    async def add_camera_config(self, camera_config: CameraConfig) -> bool:
        """
        Add a camera configuration dynamically while pipeline is running.

        Args:
            camera_config: Camera configuration to add

        Returns:
            bool: True if successfully added, False otherwise
        """
        try:
            camera_id = camera_config.camera_id

            if camera_id in self.camera_configs:
                self.logger.warning(f"Camera {camera_id} already exists, updating configuration")
                # Stop existing workers for this camera
                await self._stop_camera_workers(camera_id)

            # Add camera config
            self.camera_configs[camera_id] = camera_config

            # Lazy-initialize frame cache if this is first Redis camera
            self._ensure_frame_cache_initialized()

            # Lazy-initialize analytics publisher if this is first Redis camera
            self._ensure_analytics_publisher_initialized()

            # Ensure producer Redis connection has proper auth from camera config
            self._ensure_producer_redis_initialized()

            # Update analytics publisher with current camera configs
            if self.analytics_publisher is not None:
                self.analytics_publisher.update_camera_configs(self.camera_configs)

            # Add camera to consumer manager if pipeline is running
            if self.running:
                # Lazy-create consumer manager if this is first camera added after startup
                if not self.consumer_manager:
                    self.logger.info("First camera added - initializing consumer manager")
                    await self._create_consumer_workers()
                    # Start the newly created consumer manager
                    if self.consumer_manager:
                        await self.consumer_manager.start()
                        self.logger.info("✓ Consumer manager started")
                elif self.consumer_manager:
                    # Consumer manager exists, add camera to it
                    await self.consumer_manager.add_camera(camera_id, camera_config)

            self.logger.info(f"Successfully added camera configuration for {camera_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add camera config for {camera_config.camera_id}: {e!s}")
            return False

    async def remove_camera_config(self, camera_id: str) -> bool:
        """
        Remove a camera configuration dynamically.

        Args:
            camera_id: ID of camera to remove

        Returns:
            bool: True if successfully removed, False otherwise
        """
        try:
            if camera_id not in self.camera_configs:
                # Camera already removed - return True since desired state is achieved
                self.logger.debug(f"Camera {camera_id} not found in configs, already removed")
                return True

            # Stop workers for this camera
            await self._stop_camera_workers(camera_id)

            # Remove camera config
            del self.camera_configs[camera_id]

            # Update analytics publisher with current camera configs
            if self.analytics_publisher is not None:
                self.analytics_publisher.update_camera_configs(self.camera_configs)

            self.logger.info(f"Successfully removed camera configuration for {camera_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to remove camera config for {camera_id}: {e!s}")
            return False

    async def update_camera_config(self, camera_config: CameraConfig) -> bool:
        """
        Update an existing camera configuration.

        Args:
            camera_config: Updated camera configuration

        Returns:
            bool: True if successfully updated, False otherwise
        """
        return await self.add_camera_config(camera_config)

    async def reconcile_camera_configs(self, new_camera_configs: Dict[str, CameraConfig]) -> Dict[str, Any]:
        """
        Perform full reconciliation of camera configurations.

        This method replaces the current camera configurations with the provided
        snapshot, performing adds, updates, and removals as needed.

        Args:
            new_camera_configs: Complete snapshot of camera configurations

        Returns:
            Dict with reconciliation results:
                {
                    "success": bool,
                    "added": int,
                    "updated": int,
                    "removed": int,
                    "total_cameras": int,
                    "errors": List[str]
                }
        """
        result = {
            "success": True,
            "added": 0,
            "updated": 0,
            "removed": 0,
            "total_cameras": 0,
            "errors": [],
        }

        try:
            # Validate input
            if new_camera_configs is None:
                error_msg = "new_camera_configs cannot be None"
                result["errors"].append(error_msg)
                result["success"] = False
                self.logger.error(error_msg)
                return result

            if not isinstance(new_camera_configs, dict):
                error_msg = f"new_camera_configs must be a dict, got {type(new_camera_configs)}"
                result["errors"].append(error_msg)
                result["success"] = False
                self.logger.error(error_msg)
                return result

            # Get current camera IDs
            current_ids = set(self.camera_configs.keys())
            new_ids = set(new_camera_configs.keys())

            # Determine operations
            cameras_to_remove = current_ids - new_ids
            cameras_to_add = new_ids - current_ids
            cameras_to_check_update = new_ids & current_ids

            self.logger.info(
                f"Reconciliation plan: "
                f"remove={len(cameras_to_remove)}, "
                f"add={len(cameras_to_add)}, "
                f"check_update={len(cameras_to_check_update)}"
            )

            # Step 1: Remove cameras no longer in config
            for camera_id in cameras_to_remove:
                try:
                    success = await self.remove_camera_config(camera_id)
                    if success:
                        result["removed"] += 1
                        self.logger.info(f"Removed camera {camera_id}")
                    else:
                        error_msg = f"Failed to remove camera {camera_id}"
                        result["errors"].append(error_msg)
                        self.logger.warning(error_msg)
                except Exception as e:
                    error_msg = f"Error removing camera {camera_id}: {e}"
                    result["errors"].append(error_msg)
                    self.logger.error(error_msg, exc_info=True)

            # Step 2: Check and update existing cameras
            for camera_id in cameras_to_check_update:
                try:
                    new_config = new_camera_configs[camera_id]
                    current_config = self.camera_configs.get(camera_id)

                    # Check if config has actually changed
                    config_changed = (
                        not current_config
                        or current_config.input_topic != new_config.input_topic
                        or current_config.output_topic != new_config.output_topic
                        or current_config.stream_config != new_config.stream_config
                        or current_config.enabled != new_config.enabled
                    )

                    if config_changed:
                        success = await self.update_camera_config(new_config)
                        if success:
                            result["updated"] += 1
                            self.logger.info(f"Updated camera {camera_id}")
                        else:
                            error_msg = f"Failed to update camera {camera_id}"
                            result["errors"].append(error_msg)
                            self.logger.warning(error_msg)
                    else:
                        self.logger.debug(f"Camera {camera_id} config unchanged, skipping update")

                except Exception as e:
                    error_msg = f"Error updating camera {camera_id}: {e}"
                    result["errors"].append(error_msg)
                    self.logger.error(error_msg, exc_info=True)

            # Step 3: Add new cameras
            for camera_id in cameras_to_add:
                try:
                    new_config = new_camera_configs[camera_id]
                    success = await self.add_camera_config(new_config)
                    if success:
                        result["added"] += 1
                        self.logger.info(f"Added camera {camera_id}")
                    else:
                        error_msg = f"Failed to add camera {camera_id}"
                        result["errors"].append(error_msg)
                        self.logger.warning(error_msg)
                except Exception as e:
                    error_msg = f"Error adding camera {camera_id}: {e}"
                    result["errors"].append(error_msg)
                    self.logger.error(error_msg, exc_info=True)

            # Update result
            result["total_cameras"] = len(self.camera_configs)
            result["success"] = len(result["errors"]) == 0

            if result["success"]:
                self.logger.info(
                    f"Reconciliation completed successfully: "
                    f"{result['total_cameras']} cameras active "
                    f"(+{result['added']}, ~{result['updated']}, -{result['removed']})"
                )
            else:
                self.logger.warning(
                    f"Reconciliation completed with {len(result['errors'])} errors: "
                    f"{result['total_cameras']} cameras active "
                    f"(+{result['added']}, ~{result['updated']}, -{result['removed']})"
                )

            return result

        except Exception as e:
            error_msg = f"Critical error during reconciliation: {e}"
            result["errors"].append(error_msg)
            result["success"] = False
            self.logger.error(error_msg, exc_info=True)
            return result

    def enable_camera(self, camera_id: str) -> bool:
        """Enable a camera configuration."""
        return self._set_camera_state(camera_id, True, "enabled")

    def disable_camera(self, camera_id: str) -> bool:
        """Disable a camera configuration."""
        return self._set_camera_state(camera_id, False, "disabled")

    def _set_camera_state(self, camera_id: str, enabled: bool, state_name: str) -> bool:
        """Set camera enabled state."""
        if camera_id in self.camera_configs:
            self.camera_configs[camera_id].enabled = enabled
            self.logger.info(f"Camera {camera_id} {state_name}")
            return True
        return False

    async def _create_workers(self) -> None:
        """Create all worker instances for the pipeline."""
        # Create consumer + inference workers
        await self._create_consumer_workers()
        self._create_inference_worker()

        # Post-processing and producer
        self._create_postprocessing_worker()
        self._create_producer_pool()

    async def _create_consumer_workers(self) -> None:
        """Create consumer manager for all cameras.

        Uses AsyncConsumerManager (single async event loop for all cameras).
        """
        if len(self.camera_configs) > 0:
            # Extract stream config from first camera (assuming all use same stream config)
            first_camera = next(iter(self.camera_configs.values()))
            stream_config = first_camera.stream_config

            self.consumer_manager = AsyncConsumerManager(
                camera_configs=self.camera_configs,
                stream_config=stream_config,
                app_deployment_id=self.app_deployment_id,
                pipeline=self,
                message_timeout=self.message_timeout,
            )

            self.logger.info(f"Created async consumer manager for {len(self.camera_configs)} cameras")

    def _create_inference_worker(self) -> None:
        """Create multiprocess inference pool with async event loops.

        Architecture:
        - Multiple separate processes (one per GPU/core)
        - Each process recreates InferenceInterface → ModelManagerWrapper → ModelManager
        - Uses normal ModelManager with predict functions from MatriceDeployServer (NOT Triton)
        - Each process runs its own async event loop
        - Multiple concurrent inference requests per process
        - True parallelism (bypasses Python GIL)

        Note: Workers receive predict functions via model_config (passed from MatriceDeployServer).
        Functions are module-level and can be pickled by reference for multiprocessing.
        """
        # Extract configuration for ModelManager (NOT Triton)
        # Workers will recreate InferenceInterface with ModelManager using predict functions
        model_manager_wrapper = (
            getattr(self.inference_interface, "model_manager_wrapper", None) if self.inference_interface else None
        )

        if model_manager_wrapper:
            # Extract action_id from action_tracker
            action_tracker = getattr(model_manager_wrapper, "action_tracker", None)
            action_id = getattr(action_tracker, "action_id", None) if action_tracker else None

            # Extract model manager config
            model_manager = getattr(model_manager_wrapper, "model_manager", None)
            num_instances = len(getattr(model_manager, "model_instances", [])) if model_manager else 1
            model_path = getattr(model_manager, "model_path", None) if model_manager else None

            # Check if batch_predict is available - if not, disable batching
            has_batch_predict = self.batch_predict is not None or self.async_batch_predict is not None
            enable_batching = has_batch_predict

            model_config = {
                "action_id": action_id,
                "model_path": model_path,
                "num_model_instances": num_instances,
                # Predict functions from MatriceDeployServer (module-level, picklable by reference)
                "load_model": self.load_model,
                "predict": self.predict,
                "async_predict": self.async_predict,
                "async_batch_predict": self.async_batch_predict,
                "async_load_model": self.async_load_model,
                "batch_predict": self.batch_predict,
                # Batching control - disable if no batch functions available
                "enable_batching": enable_batching,
            }

            if not action_id:
                self.logger.warning("No action_id found in action_tracker, workers may fail to initialize")

            if not enable_batching:
                self.logger.warning(
                    "Batch inference disabled - no batch_predict or async_batch_predict function available"
                )
        else:
            # Fallback defaults if config not available
            self.logger.error("Could not extract ModelManager config from inference_interface")

            # Check if batch_predict is available - if not, disable batching
            has_batch_predict = self.batch_predict is not None or self.async_batch_predict is not None
            enable_batching = has_batch_predict

            model_config = {
                "action_id": self.action_id,  # Use action_id passed to StreamingPipeline
                "model_path": None,
                "num_model_instances": 1,
                # Predict functions from MatriceDeployServer
                "load_model": self.load_model,
                "predict": self.predict,
                "async_predict": self.async_predict,
                "async_batch_predict": self.async_batch_predict,
                "async_load_model": self.async_load_model,
                "batch_predict": self.batch_predict,
                # Batching control - disable if no batch functions available
                "enable_batching": enable_batching,
            }

            if not enable_batching:
                self.logger.warning(
                    "Batch inference disabled - no batch_predict or async_batch_predict function available"
                )

        self.inference_pool = MultiprocessInferencePool(
            num_workers=self.num_inference_workers,
            model_config=model_config,
            input_queues=self.inference_queues,  # Per-worker queues (one per worker)
            output_queues=self.postproc_queues,  # Per-worker output queues for routing to postproc
            use_async_inference=self.use_async_inference,  # Determines sync vs async behavior
            metrics_queue=self.multiprocess_metrics_queue,  # For sending metrics to main process
        )

        mode = "ASYNC+FEEDER (batched, no executor hops)" if self.use_async_inference else "SYNC (TRUE BATCH INFERENCE)"
        self.logger.info(
            f"Created multiprocess inference pool with {self.num_inference_workers} workers "
            f"- {mode} - PER-WORKER QUEUES for ordering"
        )

    def _create_postprocessing_worker(self) -> None:
        """Create multiprocess post-processing pool with camera routing.

        Architecture:
        - ProcessPoolExecutor with 4 workers (true parallelism, no GIL)
        - Camera-based hash routing (preserves per-camera ordering)
        - Each process maintains isolated tracker state
        - Process camera subsets (e.g., 250 cameras per process)
        """
        # Use post-processing configuration passed during initialization (as dict)
        # instead of extracting from post_processor object
        post_processor_config = {
            "post_processing_config": self.post_processing_config,
            "app_name": self.app_name,
            "index_to_category": self.index_to_category,
            "target_categories": self.target_categories,
        }

        self.postproc_pool = MultiprocessPostProcessingPool(
            pipeline=self,
            post_processor_config=post_processor_config,
            input_queues=self.postproc_queues,  # Per-worker queues (one per worker)
            output_queues=self.output_queues,  # Per-worker output queues (eliminates lock contention)
            num_processes=self.num_postproc_workers,
            metrics_queue=self.multiprocess_metrics_queue,  # For sending metrics to main process
        )

        self.logger.info(
            f"Created multiprocess post-processing pool with {self.num_postproc_workers} workers "
            f"- PER-WORKER QUEUES for ordering"
        )

    def _create_producer_pool(self) -> None:
        """Create shared async producer pool.

        Replaces the thread-per-producer model with a single shared async pool.
        Benefits:
        - 75-90% thread reduction (from N threads to 1)
        - Shared Redis connections (better resource utilization)
        - Simplified architecture (single event loop)
        - Memory savings (~30-50% reduction)

        The pool handles:
        - Frame caching (moved from consumer to avoid blocking inference flow)
        - Overlay storage for results
        - Redis stream publishing with pipelining
        - Analytics data enqueuing
        """
        # Get stream config from first camera (all cameras share stream config)
        if self.camera_configs:
            first_camera = next(iter(self.camera_configs.values()))
            stream_config = first_camera.stream_config
        else:
            # Default stream config if no cameras yet
            stream_config = {"stream_type": "redis", "host": "localhost", "port": 6379}

        self.producer_pool = AsyncProducerPool(
            output_queues=self.output_queues,
            camera_configs=self.camera_configs,
            stream_config=stream_config,
            analytics_publisher=self.analytics_publisher,
            frame_cache=self.frame_cache,
            app_deployment_id=self.app_deployment_id,
            use_shared_metrics=self.use_shared_metrics,
        )

        self.logger.info(
            f"Created AsyncProducerPool for {len(self.output_queues)} output queues "
            f"(replaces {len(self.output_queues)} producer threads)"
        )

    def _start_workers(self) -> None:
        """Start all worker instances and track their threads."""
        # Start consumer manager (async, single event loop for all cameras)
        if self.consumer_manager:
            asyncio.run_coroutine_threadsafe(self.consumer_manager.start(), self._event_loop)
            self.logger.info("Started async consumer manager")

        # Start inference pool (multiprocessing)
        if self.inference_pool:
            self.inference_pool.start()
            self.logger.info("Started multiprocess inference pool")

        # Start post-processing pool (multiprocessing)
        if self.postproc_pool:
            self.postproc_pool.start()
            self.logger.info("Started multiprocess post-processing pool")

        # Start shared async producer pool
        if self.producer_pool:
            producer_thread = self.producer_pool.start()
            self.worker_threads.append(producer_thread)
            self.logger.info("Started async producer pool")

        # Start analytics publisher if initialized
        if self.analytics_publisher:
            try:
                analytics_thread = self.analytics_publisher.start()
                self.worker_threads.append(analytics_thread)
                self.logger.info("Started analytics publisher thread")
            except Exception as e:
                self.logger.error(f"Failed to start analytics publisher: {e}")

    def _start_worker_group(self, workers: List) -> None:
        """Start a group of workers (handles both threading and async workers)."""
        for worker in workers:
            # Check if worker has async start method
            if hasattr(worker, "start") and asyncio.iscoroutinefunction(worker.start):
                # Async worker - schedule on event loop
                asyncio.run_coroutine_threadsafe(worker.start(), self._event_loop)
            else:
                # Threading worker - traditional start
                thread = worker.start()
                if thread:
                    self.worker_threads.append(thread)

    def _stop_workers(self) -> None:
        """Stop all worker instances gracefully."""
        # Stop consumer manager (async) - MUST wait for completion before stopping event loop
        if self.consumer_manager and self._event_loop:
            try:
                future = asyncio.run_coroutine_threadsafe(self.consumer_manager.stop(), self._event_loop)
                # Wait for consumer manager to fully stop (with timeout)
                future.result(timeout=10.0)
                self.logger.info("Stopped async consumer manager")
            except TimeoutError:
                self.logger.warning("Consumer manager stop timed out after 10 seconds")
            except Exception as e:
                self.logger.error(f"Error stopping consumer manager: {e}")

        # Stop inference pool (multiprocessing)
        if self.inference_pool:
            self.inference_pool.stop()
            self.logger.info("Stopped multiprocess inference pool")

        # Stop post-processing pool (multiprocessing)
        if self.postproc_pool:
            self.postproc_pool.stop()
            self.logger.info("Stopped multiprocess post-processing pool")

        # Stop shared async producer pool
        if self.producer_pool:
            self.producer_pool.stop()
            self.logger.info("Stopped async producer pool")

        # Stop analytics publisher BEFORE waiting for threads
        # (analytics thread is in worker_threads, must signal stop before join)
        if self.analytics_publisher:
            try:
                self.analytics_publisher.stop()
                self.logger.info("Signaled analytics publisher to stop")
            except Exception as e:
                self.logger.error(f"Error stopping analytics publisher: {e}")

    def _stop_worker_group(self, workers: List) -> None:
        """Stop a group of workers."""
        for worker in workers:
            worker.stop()

    async def _stop_camera_workers(self, camera_id: str) -> None:
        """Clean up resources for a specific camera."""
        # Remove camera from consumer manager
        if self.consumer_manager:
            await self.consumer_manager.remove_camera(camera_id)

        # Update producer pool camera configs (it will skip this camera on next publish)
        # Note: AsyncProducerPool automatically validates camera availability on each message

    def get_metrics(self) -> Dict[str, Any]:
        """Get pipeline metrics including frame cache statistics."""
        # Get per-worker queue sizes
        inference_qsizes = (
            [q.qsize() for q in self.inference_queues]
            if hasattr(self, "inference_queues") and self.inference_queues
            else []
        )
        postproc_qsizes = (
            [q.qsize() for q in self.postproc_queues]
            if hasattr(self, "postproc_queues") and self.postproc_queues
            else []
        )
        output_qsizes = (
            [q.qsize() for q in self.output_queues] if hasattr(self, "output_queues") and self.output_queues else []
        )

        # Calculate queue health metrics
        inference_total_capacity = len(inference_qsizes) * self.inference_queue_maxsize if inference_qsizes else 1
        postproc_total_capacity = len(postproc_qsizes) * self.postproc_queue_maxsize if postproc_qsizes else 1
        output_total_capacity = len(output_qsizes) * self.output_queue_maxsize if output_qsizes else 1

        inference_utilization = sum(inference_qsizes) / inference_total_capacity if inference_total_capacity > 0 else 0
        postproc_utilization = sum(postproc_qsizes) / postproc_total_capacity if postproc_total_capacity > 0 else 0
        output_utilization = sum(output_qsizes) / output_total_capacity if output_total_capacity > 0 else 0

        # Backpressure is active if any queue is over 80% capacity
        backpressure_threshold = 0.8
        inference_backpressure = any(
            q > backpressure_threshold * self.inference_queue_maxsize for q in inference_qsizes
        )
        postproc_backpressure = any(q > backpressure_threshold * self.postproc_queue_maxsize for q in postproc_qsizes)
        output_backpressure = any(q > backpressure_threshold * self.output_queue_maxsize for q in output_qsizes)

        metrics = {
            "running": self.running,
            "camera_count": len(self.camera_configs),
            "enabled_cameras": sum(1 for config in self.camera_configs.values() if config.enabled),
            "queue_sizes": {
                "inference_queues": inference_qsizes,
                "inference_queue_total": sum(inference_qsizes),
                "postproc_queues": postproc_qsizes,
                "postproc_queue_total": sum(postproc_qsizes),
                "output_queues": output_qsizes,
                "output_queue_total": sum(output_qsizes),
                "queue_architecture": "per_worker_queues_for_ordering",
            },
            "queue_health": {
                "inference_utilization": round(inference_utilization, 3),
                "postproc_utilization": round(postproc_utilization, 3),
                "output_utilization": round(output_utilization, 3),
                "inference_backpressure": inference_backpressure,
                "postproc_backpressure": postproc_backpressure,
                "output_backpressure": output_backpressure,
                "any_backpressure": inference_backpressure or postproc_backpressure or output_backpressure,
            },
            "worker_counts": {
                "consumer_manager": "AsyncConsumerManager" if self.consumer_manager else None,
                "inference_pool_workers": self.num_inference_workers if self.inference_pool else 0,
                "postproc_pool_workers": self.num_postproc_workers if self.postproc_pool else 0,
                "producer_pool": "AsyncProducerPool" if self.producer_pool else None,
            },
            "thread_counts": {
                "total_threads": len(self.worker_threads),
                "active_threads": len([t for t in self.worker_threads if t.is_alive()]),
            },
            "camera_configs": {
                camera_id: {
                    "input_topic": config.input_topic,
                    "output_topic": config.output_topic,
                    "enabled": config.enabled,
                    "stream_type": config.stream_config.get("stream_type", "kafka"),
                }
                for camera_id, config in self.camera_configs.items()
            },
        }

        # Add frame cache metrics if available
        if self.frame_cache:
            try:
                metrics["frame_cache"] = self.frame_cache.get_metrics()
            except Exception as e:
                self.logger.warning(f"Failed to get frame cache metrics: {e}")
                metrics["frame_cache"] = {"error": str(e)}
        else:
            metrics["frame_cache"] = {"enabled": False}

        # Add analytics publisher metrics if available
        if self.analytics_publisher:
            try:
                metrics["analytics_publisher"] = self.analytics_publisher.get_metrics()
            except Exception as e:
                self.logger.warning(f"Failed to get analytics publisher metrics: {e}")
                metrics["analytics_publisher"] = {"error": str(e)}
        else:
            metrics["analytics_publisher"] = {"enabled": False}

        # Add Metric logger statistics
        if self.metric_logger:
            try:
                metrics["metric_logger"] = self.metric_logger.get_stats()
            except Exception as e:
                self.logger.warning(f"Failed to get metric logger stats: {e}")
                metrics["metric_logger"] = {"error": str(e)}
        else:
            metrics["metric_logger"] = {"enabled": False}

        return metrics

    def _initialize_frame_cache(self) -> None:
        """Initialize RedisFrameCache with TTL 10 minutes, deriving connection from Redis cameras if available."""
        try:
            # Check if we have any Redis cameras - if not, skip initialization
            has_redis_cameras = False
            for cfg in self.camera_configs.values():
                sc = cfg.stream_config or {}
                st = sc.get("stream_type", "redis").lower()
                if st == "redis":
                    has_redis_cameras = True
                    break

            if not has_redis_cameras:
                self.logger.info(
                    "No Redis cameras found - skipping frame cache initialization. "
                    "Frame cache will be initialized when first Redis camera arrives."
                )
                return

            # Find Redis camera config for connection params
            host = "localhost"
            port = 6379
            password = None
            username = None
            db = 0
            sentinel_hosts = None
            master_name = None

            for cfg in self.camera_configs.values():
                sc = cfg.stream_config or {}
                st = sc.get("stream_type", "redis").lower()
                self.logger.info(
                    f"Frame cache init - Camera {cfg.camera_id}: stream_type={st}, config_keys={list(sc.keys())}"
                )
                self.logger.info(f"Camera Config {cfg.camera_id} {st}")
                if st == "redis":
                    host = sc.get("host") or host
                    port = sc.get("port") or port
                    password = sc.get("password", password)
                    username = sc.get("username", username)
                    db = sc.get("db", db)
                    sentinel_hosts = sc.get("sentinel_hosts")
                    master_name = sc.get("master_name")
                    self.logger.info(f"Using Redis config from camera {cfg.camera_id}: {host}:{port}")
                    break

            # Lazy import to avoid dependency issues if not used
            from matrice_inference.server.stream.frame_cache import RedisFrameCache

            self.frame_cache = RedisFrameCache(
                host=host,
                port=port,
                db=db,
                password=password,
                username=username,
                ttl_seconds=600,  # 10 minutes
                worker_threads=self.frame_cache_worker_threads,
                max_queue=self.frame_cache_max_queue,
                max_connections=self.frame_cache_max_connections,
                sentinel_hosts=sentinel_hosts,
                master_name=master_name,
            )
            self.frame_cache.start()
            self.logger.info(
                f"Initialized RedisFrameCache with TTL=600s, workers={self.frame_cache_worker_threads}, "
                f"queue={self.frame_cache_max_queue}, max_connections={self.frame_cache_max_connections}"
            )
        except Exception as e:
            self.frame_cache = None
            self.logger.warning(f"Frame cache initialization failed; proceeding without cache: {e}")

    def _initialize_analytics_publisher(self) -> None:
        """Initialize AnalyticsPublisher to send aggregated stats to Redis only."""
        if not self.enable_analytics_publisher:
            self.logger.warning(
                "[ANALYTICS_INIT_SKIP] Analytics publisher disabled via enable_analytics_publisher=False"
            )
            return

        try:
            # Check if we have any Redis cameras - if not, skip initialization
            has_redis_cameras = False
            redis_camera_count = 0
            non_redis_camera_count = 0

            for cfg in self.camera_configs.values():
                sc = cfg.stream_config or {}
                st = sc.get("stream_type", "redis").lower()
                if st == "redis":
                    has_redis_cameras = True
                    redis_camera_count += 1
                else:
                    non_redis_camera_count += 1

            if not has_redis_cameras:
                self.logger.warning(
                    f"[ANALYTICS_INIT_SKIP] No Redis cameras found. "
                    f"Total cameras: {len(self.camera_configs)}, "
                    f"Non-Redis cameras: {non_redis_camera_count}. "
                    "AnalyticsPublisher requires at least one Redis camera."
                )
                return

            self.logger.info(
                f"[ANALYTICS_INIT] Found {redis_camera_count} Redis cameras, "
                f"{non_redis_camera_count} non-Redis cameras. Proceeding with initialization."
            )

            # Find connection params from camera configs
            redis_host = "localhost"
            redis_port = 6379
            redis_password = None
            redis_username = None
            redis_db = 0

            sentinel_hosts = None
            master_name = None
            for cfg in self.camera_configs.values():
                sc = cfg.stream_config or {}
                st = sc.get("stream_type", "redis").lower()

                # Log for debugging
                self.logger.info(
                    f"Analytics init - Camera {cfg.camera_id}: stream_type={st}, config_keys={list(sc.keys())}"
                )

                if st == "redis":
                    redis_host = sc.get("host") or redis_host
                    redis_port = sc.get("port") or redis_port
                    redis_password = sc.get("password", redis_password)
                    redis_username = sc.get("username", redis_username)
                    redis_db = sc.get("db", redis_db)
                    sentinel_hosts = sc.get("sentinel_hosts")
                    master_name = sc.get("master_name")
                    self.logger.info(
                        f"Using Redis config from camera {cfg.camera_id} for analytics publisher: "
                        f"{redis_host}:{redis_port}, db={redis_db}"
                    )
                    break

            # Initialize analytics publisher (don't start yet) - Redis only
            self.analytics_publisher = AnalyticsPublisher(
                camera_configs=self.camera_configs,
                aggregation_interval=300,  # 5 minutes
                publish_interval=60,  # Publish every 60 seconds
                app_deployment_id=self.app_deployment_id,
                inference_pipeline_id=self.inference_pipeline_id,
                deployment_instance_id=self.deployment_instance_id,
                app_id=self.app_id,
                app_name=self.app_name,
                app_version=self.app_version,
                redis_host=redis_host,
                redis_port=redis_port,
                redis_password=redis_password,
                redis_username=redis_username,
                redis_db=redis_db,
                sentinel_hosts=sentinel_hosts,
                master_name=master_name,
                kafka_bootstrap_servers=None,
                enable_kafka=False,  # Disable Kafka publishing
            )

            self.logger.info(
                f"[ANALYTICS_INIT_SUCCESS] Initialized AnalyticsPublisher "
                f"(Redis: {redis_host}:{redis_port}, aggregation: 5min, publish: 60s)"
            )
        except Exception as e:
            self.analytics_publisher = None
            self.logger.warning(
                f"[ANALYTICS_INIT_FAIL] Analytics publisher initialization failed: {e}. "
                "Proceeding without analytics publishing."
            )

    def _ensure_frame_cache_initialized(self) -> None:
        """
        Ensure frame cache is initialized if we have Redis cameras.
        This is called when cameras are added dynamically to enable lazy initialization.
        """
        if self.frame_cache is not None:
            # Already initialized
            return

        # Check if we have Redis cameras now
        has_redis = any(
            cfg.stream_config.get("stream_type", "").lower() == "redis" for cfg in self.camera_configs.values()
        )

        if has_redis:
            self.logger.info("Redis camera detected - lazy initializing frame cache...")
            try:
                self._initialize_frame_cache()
                if self.frame_cache:
                    self.logger.info("✓ Frame cache lazy initialization successful")

                    # CRITICAL: Update AsyncProducerPool's reference to the newly initialized frame_cache
                    # Without this, producer_pool would still have frame_cache=None
                    if self.producer_pool:
                        self.producer_pool.update_frame_cache(self.frame_cache)
                        self.logger.info("✓ Updated AsyncProducerPool with frame_cache reference")
                else:
                    self.logger.warning("✗ Frame cache initialization returned None")
            except Exception as e:
                self.logger.error(f"✗ Frame cache lazy initialization failed: {e}", exc_info=True)

    def _ensure_analytics_publisher_initialized(self) -> None:
        """
        Ensure analytics publisher is initialized and started if we have Redis cameras.
        This is called when cameras are added dynamically to enable lazy initialization.
        """
        if self.analytics_publisher is not None:
            # Already initialized
            return

        if not self.enable_analytics_publisher:
            # Disabled
            return

        # Check if we have Redis cameras now
        has_redis = any(
            cfg.stream_config.get("stream_type", "").lower() == "redis" for cfg in self.camera_configs.values()
        )

        if has_redis:
            self.logger.info("Redis camera detected - lazy initializing analytics publisher...")
            try:
                self._initialize_analytics_publisher()

                # Start the analytics publisher thread if pipeline is running and publisher was initialized
                if self.running and self.analytics_publisher:
                    try:
                        analytics_thread = self.analytics_publisher.start()
                        self.worker_threads.append(analytics_thread)
                        self.logger.info("✓ Analytics publisher lazy initialization successful and thread started")

                        # CRITICAL: Update AsyncProducerPool's reference to the newly initialized analytics_publisher
                        # Without this, producer_pool would still have analytics_publisher=None
                        if self.producer_pool:
                            self.producer_pool.update_analytics_publisher(self.analytics_publisher)
                            self.logger.info("✓ Updated AsyncProducerPool with analytics_publisher reference")
                    except Exception as e:
                        self.logger.error(
                            f"✗ Failed to start analytics publisher thread: {e}",
                            exc_info=True,
                        )
                elif self.analytics_publisher:
                    self.logger.info("✓ Analytics publisher initialized but pipeline not running yet")
                    # Still update producer pool reference for when pipeline starts
                    if self.producer_pool:
                        self.producer_pool.update_analytics_publisher(self.analytics_publisher)
                else:
                    self.logger.warning("✗ Analytics publisher initialization returned None")
            except Exception as e:
                self.logger.error(
                    f"✗ Analytics publisher lazy initialization failed: {e}",
                    exc_info=True,
                )

    def _ensure_producer_redis_initialized(self) -> None:
        """
        Ensure AsyncProducerPool has Redis connection initialized with proper auth.
        This is called when cameras are added dynamically to provide Redis credentials.

        Similar to _ensure_frame_cache_initialized() and _ensure_analytics_publisher_initialized(),
        this extracts Redis connection details from camera configs and updates the producer pool.
        """
        if not self.producer_pool:
            # Producer pool not created yet
            return

        # Check if we have Redis cameras
        redis_camera_config = None
        for cfg in self.camera_configs.values():
            sc = cfg.stream_config or {}
            st = sc.get("stream_type", "redis").lower()
            if st == "redis":
                redis_camera_config = cfg
                break

        if not redis_camera_config:
            # No Redis cameras, nothing to do
            return

        # Extract Redis connection details from camera config
        stream_config = redis_camera_config.stream_config or {}

        # Build complete stream config with auth details
        redis_stream_config = {
            "stream_type": "redis",
            "host": stream_config.get("host") or "localhost",
            "port": stream_config.get("port") or 6379,
            "password": stream_config.get("password"),
            "username": stream_config.get("username"),
            "db": stream_config.get("db", 0),
        }

        self.logger.info(
            f"Ensuring producer Redis connection with camera config: "
            f"host={redis_stream_config['host']}:{redis_stream_config['port']}, "
            f"has_auth={redis_stream_config['password'] is not None or redis_stream_config['username'] is not None}"
        )

        try:
            success = self.producer_pool.update_stream_config(redis_stream_config)
            if success:
                self.logger.info("✓ Producer Redis connection ensured with camera auth credentials")
            else:
                self.logger.warning("✗ Failed to update producer Redis connection")
        except Exception as e:
            self.logger.error(f"✗ Error updating producer Redis connection: {e}", exc_info=True)
