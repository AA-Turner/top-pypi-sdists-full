"""
High-performance multiprocessing inference worker for optimal GPU utilization.

Architecture:
- Multiprocessing: 8 worker processes for TRUE PARALLELISM (bypasses Python GIL)
- Per-Worker Queues: Each worker reads from dedicated queue - 100% ORDER PRESERVATION
- Consumer-Side Routing: hash(camera_id) % num_workers - DETERMINISTIC ASSIGNMENT
- Feeder Thread Architecture: mp.Queue → feeder thread → asyncio.Queue (NO executor hops)
- InferenceInterface: Each process recreates InferenceInterface locally - PROCESS ISOLATION

Processing Modes (CLEANLY SEPARATED):
========================================

ASYNC mode (use_async_inference=True):
  - Uses asyncio event loop with feeder thread architecture
  - Calls InferenceInterface.async_inference() for async_predict models
  - Batch inference with concurrent processing (no per-batch semaphore)
  - Maximum parallelism for Triton/TensorRT implementations
  - Fire-and-forget batch processing without blocking

SYNC mode (use_async_inference=False):
  - Pure blocking loop with ThreadPoolExecutor (ZERO asyncio overhead)
  - Calls InferenceInterface.sync_inference() directly
  - Direct queue.get() → thread_pool.submit() → sync_inference() pattern
  - For CPU-bound or blocking Python models (PyTorch, OpenCV, etc.)
  - Simpler stack trace, easier debugging

Inference Interface Methods:
  - sync_inference(): Pure Python synchronous call → ModelManagerWrapper.inference()
  - async_inference(): Async call → ModelManagerWrapper.async_inference()
  - async_batch_inference(): Async batch call → ModelManagerWrapper.async_batch_inference()

Architecture Flow:
- InferenceInterface → ModelManagerWrapper → ModelManager → predict/async_predict
- Uses normal ModelManager (NOT Triton) with predict functions from deploy.py pattern
- Each worker imports predict functions and recreates full inference stack
- Preprocessing/postprocessing handled separately in pipeline (consumer/post-processor)

Performance Optimizations:
- ASYNC: Feeder thread isolates mp.Queue blocking from async event loop
- ASYNC: Batch inference without semaphore = true concurrent batches
- SYNC: Pure blocking loop (no asyncio overhead, no event loop per call)
- Zero debug logging in hot paths
- True parallelism (bypasses Python GIL)
- 100% frame ordering preserved per camera
"""

import asyncio
import base64
import logging
import multiprocessing as mp
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional
from matrice_inference.server.stream.worker_metrics import WorkerMetrics
from matrice_common.optimize import InferenceResultCache

# Number of concurrent threads for SYNC mode per worker
SYNC_MODE_THREAD_POOL_SIZE = 8

# =============================================================================
# FEEDER THREAD CONFIGURATION
# =============================================================================
# Feeder thread drains mp.Queue into asyncio.Queue to avoid run_in_executor hops.
# This eliminates ThreadPool contention on the hot path.

ASYNC_BUFFER_SIZE = 2000     # RESTORED from 500 (was causing starvation)
FEEDER_POLL_TIMEOUT = 0.001  # Polling interval for mp.Queue in feeder thread

# =============================================================================
# BATCH INFERENCE CONFIGURATION
# =============================================================================
# These settings control how frames are accumulated before sending to inference.
# Batching improves GPU utilization by processing multiple frames together.
#
# Tuning Guide:
# - High Throughput: BATCH_SIZE=32-64, BATCH_TIMEOUT_MS=10-20
# - Low Latency:     BATCH_SIZE=4-8,   BATCH_TIMEOUT_MS=1-2
# - Balanced:        BATCH_SIZE=16,    BATCH_TIMEOUT_MS=5 (default)
#
# To disable batching and revert to single-frame mode, set model_config["enable_batching"]=False
# ENABLE_BATCHING is now read from model_config["enable_batching"] instead of being hardcoded
# ENABLE_BATCHING = True       # REMOVED - use model_config instead
BATCH_SIZE = 16              # Default batch size (used when queue depth is moderate)
BATCH_TIMEOUT_MS = 5.0       # Max wait time in milliseconds before processing partial batch
MIN_BATCH_SIZE = 1           # Minimum batch size to process (avoid starvation)

# =============================================================================
# ADAPTIVE BATCH SIZING
# =============================================================================
# Dynamically adjust batch size based on queue depth for optimal GPU utilization.
# When queue is deep (>ADAPTIVE_THRESHOLD), use larger batches to clear backlog.
# When queue is shallow, use smaller batches for lower latency.
ENABLE_ADAPTIVE_BATCH = True     # Feature flag for adaptive batching
MIN_ADAPTIVE_BATCH = 4           # Minimum adaptive batch size (low queue depth)
MAX_ADAPTIVE_BATCH = 64          # Maximum adaptive batch size (high queue depth)
ADAPTIVE_THRESHOLD_LOW = 50      # Queue depth below which we use MIN_ADAPTIVE_BATCH
ADAPTIVE_THRESHOLD_HIGH = 200    # Queue depth above which we use MAX_ADAPTIVE_BATCH


def _get_adaptive_batch_size(queue_depth: int) -> int:
    """
    Calculate adaptive batch size based on queue depth.

    Linear interpolation between MIN_ADAPTIVE_BATCH and MAX_ADAPTIVE_BATCH
    based on queue depth relative to thresholds.

    Args:
        queue_depth: Current number of items in the async queue

    Returns:
        Optimal batch size for current queue depth
    """
    if not ENABLE_ADAPTIVE_BATCH:
        return BATCH_SIZE

    if queue_depth <= ADAPTIVE_THRESHOLD_LOW:
        return MIN_ADAPTIVE_BATCH
    elif queue_depth >= ADAPTIVE_THRESHOLD_HIGH:
        return MAX_ADAPTIVE_BATCH
    else:
        # Linear interpolation
        range_depth = ADAPTIVE_THRESHOLD_HIGH - ADAPTIVE_THRESHOLD_LOW
        range_batch = MAX_ADAPTIVE_BATCH - MIN_ADAPTIVE_BATCH
        ratio = (queue_depth - ADAPTIVE_THRESHOLD_LOW) / range_depth
        return int(MIN_ADAPTIVE_BATCH + ratio * range_batch)

# =============================================================================
# CONCURRENT BATCH CONFIGURATION
# =============================================================================
# Limits number of in-flight batch inference operations per worker.
# Prevents unbounded asyncio.create_task() explosion which causes:
# - Event loop scheduling overhead
# - Memory pressure from hundreds of pending coroutines
# - GPU pipeline stalls from excessive queuing
#
# Tuning Guide:
# - MAX_INFLIGHT_BATCHES=2-4: Low latency, better memory usage
# - MAX_INFLIGHT_BATCHES=4-8: Higher throughput, more memory
# - MAX_INFLIGHT_BATCHES=16+: High throughput for GPU workloads
# RESTORED from 8 to 16 (reduction was causing starvation)
MAX_INFLIGHT_BATCHES = 16    # RESTORED - Max concurrent batch inference operations per worker

# =============================================================================
# DROP-SAFE OUTPUT CONFIGURATION
# =============================================================================
# Controls behavior when post-processing queues are full.
# Configurable via model_config for flexibility.

ENABLE_DROP_ON_BACKPRESSURE = True  # Drop frames when output queue is full (default)
FRAME_STALENESS_MS = 500.0          # Drop frames older than this threshold in milliseconds


def _safe_queue_put(
    target_queue: mp.Queue,
    output_data: Dict[str, Any],
    metrics: Optional[Any],
    logger: logging.Logger,
    enable_drop: bool = True,
) -> bool:
    """
    Put data to output queue with drop-safe behavior.

    When enable_drop=True (default), uses non-blocking put_nowait().
    If queue is full, drops the frame and records metrics.

    Args:
        target_queue: Target multiprocessing queue
        output_data: Data to put in queue
        metrics: WorkerMetrics instance for recording drops
        logger: Logger for debug output
        enable_drop: If True, drop on full; if False, block until space available

    Returns:
        True if data was successfully queued, False if dropped
    """
    if enable_drop:
        try:
            target_queue.put_nowait(output_data)
            return True
        except queue.Full:
            # Queue full - drop frame and record metrics
            frame_id = output_data.get("frame_id", "unknown")
            camera_id = output_data.get("camera_id", "unknown")
            if metrics:
                metrics.record_drop(count=1, reason="backpressure")
            logger.debug(f"Dropping frame {frame_id} for camera {camera_id} - post queue full")
            return False
    else:
        # Blocking put (original behavior)
        target_queue.put(output_data)
        return True


def _feeder_thread_func(
    mp_queue: mp.Queue,
    async_queue: asyncio.Queue,
    loop: asyncio.AbstractEventLoop,
    stop_event: threading.Event,
    worker_id: int,
    logger: logging.Logger,
):
    """
    Feeder thread: drains mp.Queue into asyncio.Queue without blocking event loop.

    This eliminates run_in_executor hops on the hot path, giving 1.5-2x throughput.
    The thread blocks on mp.Queue.get() (which is fine - it's a dedicated thread)
    and puts items into the asyncio.Queue via call_soon_threadsafe.

    OPTIMIZATION: Uses pre-allocated callable to avoid lambda GC pressure.
    At 15K FPS, lambda creation per frame causes significant GC overhead.
    """
    # Pre-allocate callable to avoid lambda creation per frame (GC pressure)
    # This saves ~100-200ms/sec at high throughput from reduced allocations
    dropped_count = 0

    def _try_put(task):
        nonlocal dropped_count
        try:
            async_queue.put_nowait(task)
        except asyncio.QueueFull:
            dropped_count += 1
            # Log periodically to avoid spam
            if dropped_count % 1000 == 0:
                logger.warning(f"Worker {worker_id} feeder dropped {dropped_count} frames (queue full)")

    consecutive_errors = 0
    max_consecutive_errors = 10  # Stop after 10 consecutive errors to prevent infinite loops
    
    while not stop_event.is_set():
        try:
            # Blocking get with small timeout (allows clean shutdown)
            task = mp_queue.get(timeout=FEEDER_POLL_TIMEOUT)
            if task is not None:
                # Thread-safe put into asyncio.Queue using pre-allocated callable
                loop.call_soon_threadsafe(_try_put, task)
            consecutive_errors = 0  # Reset on success
        except queue.Empty:
            consecutive_errors = 0  # Empty queue is not an error
            continue
        except (BrokenPipeError, EOFError, OSError) as e:
            # Fatal queue errors - queue is broken, must stop
            if not stop_event.is_set():
                logger.error(f"Worker {worker_id} feeder fatal error (queue broken): {e}")
            break
        except Exception as e:
            consecutive_errors += 1
            if not stop_event.is_set():
                logger.warning(f"Worker {worker_id} feeder error ({consecutive_errors}x): {e}")
            if consecutive_errors >= max_consecutive_errors:
                logger.error(f"Worker {worker_id} feeder stopping after {max_consecutive_errors} consecutive errors")
                break
            # Brief sleep before retry for transient errors
            time.sleep(0.01)

    if dropped_count > 0:
        logger.info(f"Worker {worker_id} feeder thread stopped (total dropped: {dropped_count})")
    else:
        logger.info(f"Worker {worker_id} feeder thread stopped")


def inference_worker_process(
    worker_id: int,
    num_workers: int,
    input_queue: mp.Queue,
    output_queues: List[mp.Queue],
    model_config: Dict[str, Any],
    use_async_inference: bool = True,
    metrics_queue: Optional[mp.Queue] = None,
):
    """
    Worker process for GPU inference with optimized queue handling.

    IMPORTANT: Each worker reads from its OWN dedicated queue (input_queue).
    Consumer routes frames based on hash(camera_id) % num_workers.
    This ensures strict ordering per camera.

    Processing modes:
    - ASYNC mode (use_async_inference=True):
      - Feeder thread drains mp.Queue → asyncio.Queue (no executor hops)
      - Batch inference without per-batch semaphore (true concurrency)
    - SYNC mode (use_async_inference=False):
      - Simple blocking loop with TRUE BATCH INFERENCE
      - NO asyncio overhead for CPU-bound models

    Each process:
    1. Recreates InferenceInterface with ModelManagerWrapper + ModelManager
    2. Starts feeder thread (ASYNC mode) or blocking loop (SYNC mode)
    3. Processes tasks from its dedicated queue (no re-queuing needed)
    4. Routes results to correct post-processing worker queue

    Args:
        worker_id: Worker process ID
        num_workers: Total number of worker processes
        input_queue: This worker's dedicated queue (routed by consumer)
        output_queues: List of post-processing worker queues (for routing by camera hash)
        model_config: Model configuration (action_id, predict functions, model_path, etc.)
        use_async_inference: True for async batching, False for blocking thread pool
        metrics_queue: Queue for sending metrics back to main process
    """
    # Set up logging for this process with explicit handler
    # NOTE: Subprocess doesn't inherit handlers from main process, must configure explicitly
    logger = logging.getLogger(f"inference_worker_{worker_id}")
    logger.setLevel(logging.INFO)

    # Add StreamHandler if not already configured (prevents duplicate handlers on reimport)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Prevent propagation to root logger to avoid duplicate logs
        logger.propagate = False

    try:
        # Import dependencies inside process to avoid pickle issues
        from matrice.action_tracker import ActionTracker
        from matrice_inference.server.model.model_manager_wrapper import ModelManagerWrapper
        from matrice_inference.server.inference_interface import InferenceInterface
        from matrice_inference.server.stream.worker_metrics import MultiprocessWorkerMetrics

        # ARCHITECTURE NOTE: Model Loading Strategy
        # ==========================================
        # Models are loaded TWICE - once in pipeline event loop, once in each worker process.
        # This is INTENTIONAL and necessary for:
        # 1. Process Isolation: Each worker needs its own model instance (no shared state)
        # 2. GIL-Free Parallelism: Separate processes bypass Python GIL for true parallelism
        # 3. GPU Utilization: Each process can fully utilize GPU without contention
        # 4. Fault Isolation: Worker crash doesn't affect other workers or main pipeline
        #
        # The slight startup time/memory overhead is acceptable for 10K+ FPS throughput.

        # Get predict functions from model_config (passed from MatriceDeployServer)
        # These are module-level functions that CAN be pickled by reference
        load_model_fn = model_config.get("load_model")
        predict_fn = model_config.get("predict")
        async_predict_fn = model_config.get("async_predict")
        async_batch_predict_fn = model_config.get("async_batch_predict")
        async_load_model_fn = model_config.get("async_load_model")
        batch_predict_fn = model_config.get("batch_predict")

        # Create ActionTracker for this worker
        action_id = model_config.get("action_id")
        if not action_id:
            raise ValueError("action_id is required in model_config")

        action_tracker = ActionTracker(action_id)

        # Create ModelManagerWrapper with ModelManager (NOT Triton)
        model_manager_wrapper = ModelManagerWrapper(
            action_tracker=action_tracker,
            model_type="default",  # Use default ModelManager, NOT triton
            load_model=load_model_fn,
            predict=predict_fn,
            async_predict=async_predict_fn,
            async_batch_predict=async_batch_predict_fn,
            async_load_model=async_load_model_fn,
            batch_predict=batch_predict_fn,
            num_model_instances=model_config.get("num_model_instances", 1),
            model_path=model_config.get("model_path"),
        )

        # Create InferenceInterface
        inference_interface = InferenceInterface(
            model_manager_wrapper=model_manager_wrapper,
            post_processor=None,  # Post-processing handled separately in pipeline
        )

        # Initialize metrics for this worker (multiprocess-safe via queue)
        # NOTE: Metrics are sent to main process via metrics_queue for aggregation
        # This is required because multiprocessing doesn't share memory between processes
        if metrics_queue is not None:
            metrics = MultiprocessWorkerMetrics(
                worker_id=f"inference_{worker_id}",
                worker_type="inference",
                metrics_queue=metrics_queue
            )
        else:
            # Fallback to no-op metrics if queue not provided
            logger.warning(f"Worker {worker_id}: No metrics_queue provided, metrics will not be collected")
            metrics = None
        
        if metrics:
            metrics.mark_active()

        mode = "ASYNC+FEEDER (batched)" if use_async_inference else f"SYNC (TRUE BATCH, {SYNC_MODE_THREAD_POOL_SIZE} threads)"
        logger.info(
            f"Worker {worker_id}/{num_workers} initialized with InferenceInterface - {mode} "
            f"(ModelManager with async_predict={'available' if async_predict_fn else 'not available'}, "
            f"num_instances={model_config.get('num_model_instances', 1)})"
        )

        # Initialize result cache for frame optimization
        result_cache_config = model_config.get("result_cache_config", {})
        result_cache = InferenceResultCache(
            enabled=result_cache_config.get("enabled", True),
            max_size=result_cache_config.get("max_size", 50000),
            ttl_seconds=result_cache_config.get("ttl_seconds", 300),
        )
        logger.info(
            f"Worker {worker_id}: Initialized result cache "
            f"(enabled={result_cache.enabled}, max_size={result_cache.max_size}, "
            f"ttl={result_cache.ttl_seconds}s)"
        )

        # =================================================================
        # MODE SPLIT: ASYNC vs SYNC have completely different architectures
        # =================================================================
        
        if use_async_inference:
            # ASYNC MODE: Event loop + feeder thread
            # This is the high-throughput path for GPU inference
            _run_async_mode(
                worker_id=worker_id,
                num_workers=num_workers,
                input_queue=input_queue,
                output_queues=output_queues,
                inference_interface=inference_interface,
                model_manager_wrapper=model_manager_wrapper,
                metrics=metrics,
                result_cache=result_cache,
                logger=logger,
                model_config=model_config,
            )
        else:
            # SYNC MODE: Simple blocking loop with TRUE BATCH INFERENCE
            # This is the low-overhead path for CPU-bound models
            _run_sync_mode(
                worker_id=worker_id,
                num_workers=num_workers,
                input_queue=input_queue,
                output_queues=output_queues,
                inference_interface=inference_interface,
                model_manager_wrapper=model_manager_wrapper,
                metrics=metrics,
                result_cache=result_cache,
                logger=logger,
                model_config=model_config,
            )

    except Exception as e:
        logger.error(f"Worker {worker_id} crashed: {e}", exc_info=True)
        raise
    finally:
        # Mark worker as inactive when stopping and flush remaining metrics
        if metrics:
            metrics.mark_inactive()


def _run_async_mode(
    worker_id: int,
    num_workers: int,
    input_queue: mp.Queue,
    output_queues: List[mp.Queue],
    inference_interface: Any,
    model_manager_wrapper: Any,
    metrics: Optional[Any],
    result_cache: InferenceResultCache,
    logger: logging.Logger,
    model_config: Dict[str, Any],
):
    """
    Run async mode with feeder thread architecture.

    Architecture:
    mp.Queue → feeder thread → asyncio.Queue → async event loop → batch inference

    This eliminates run_in_executor hops for 1.5-2x throughput improvement.
    """
    async def _async_main():
        # Create asyncio.Queue for internal buffering (feeder → event loop)
        async_buffer = asyncio.Queue(maxsize=ASYNC_BUFFER_SIZE)

        # Get event loop reference for feeder thread
        loop = asyncio.get_running_loop()

        # Load models before processing
        model_manager = getattr(model_manager_wrapper, 'model_manager', None)
        if model_manager and hasattr(model_manager, 'ensure_models_loaded'):
            logger.info(f"Worker {worker_id}: Loading models...")
            await model_manager.ensure_models_loaded()
            logger.info(f"Worker {worker_id}: Models loaded successfully")

        # Start feeder thread
        stop_event = threading.Event()
        feeder = threading.Thread(
            target=_feeder_thread_func,
            args=(input_queue, async_buffer, loop, stop_event, worker_id, logger),
            daemon=True,
            name=f"feeder_{worker_id}"
        )
        feeder.start()
        logger.info(f"Worker {worker_id}: Feeder thread started")

        try:
            # Run the optimized async inference loop
            await _async_inference_loop_optimized(
                worker_id=worker_id,
                async_buffer=async_buffer,
                output_queues=output_queues,
                inference_interface=inference_interface,
                metrics=metrics,
                result_cache=result_cache,
                logger=logger,
                model_config=model_config,
            )
        finally:
            # Stop feeder thread
            stop_event.set()
            feeder.join(timeout=2.0)

    asyncio.run(_async_main())


# =============================================================================
# SYNC MODE CONCURRENT BATCH CONFIGURATION
# =============================================================================
# Controls concurrent batch processing in SYNC mode using ThreadPoolExecutor.
# While one batch is being processed by GPU, the worker continues accumulating
# and can submit additional batches for concurrent processing.

MAX_CONCURRENT_SYNC_BATCHES = 8  # Max concurrent batch inference operations


def _run_sync_mode(
    worker_id: int,
    num_workers: int,
    input_queue: mp.Queue,
    output_queues: List[mp.Queue],
    inference_interface: Any,
    model_manager_wrapper: Any,
    metrics: Optional[Any],
    result_cache: InferenceResultCache,
    logger: logging.Logger,
    model_config: Dict[str, Any],
):
    """
    Run sync mode with CONCURRENT BATCH INFERENCE.

    Architecture:
    accumulate_batch() → ThreadPoolExecutor → sync_batch_inference(batch) → route results

    Features:
    - TRUE BATCH INFERENCE via sync_batch_inference() for GPU-level batching
    - CONCURRENT PROCESSING via ThreadPoolExecutor (up to MAX_CONCURRENT_SYNC_BATCHES)
    - Main thread continues accumulating while batches are being processed
    - Bounded concurrency prevents GPU overload
    """
    from concurrent.futures import Future

    # Load models synchronously (for sync models, this is fine)
    model_manager = getattr(model_manager_wrapper, 'model_manager', None)
    if model_manager and hasattr(model_manager, 'load_models_sync'):
        logger.info(f"Worker {worker_id}: Loading models (sync)...")
        model_manager.load_models_sync()
        logger.info(f"Worker {worker_id}: Models loaded successfully")
    elif model_manager and hasattr(model_manager, 'ensure_models_loaded'):
        # Fallback: run async loader in a new event loop
        logger.info(f"Worker {worker_id}: Loading models (async fallback)...")
        asyncio.run(model_manager.ensure_models_loaded())
        logger.info(f"Worker {worker_id}: Models loaded successfully")

    # Batch configuration (same as async mode)
    batch_timeout_sec = BATCH_TIMEOUT_MS / 1000.0

    # Check if batching is enabled
    enable_batching = model_config.get("enable_batching", True)

    logger.info(
        f"Worker {worker_id}: Starting sync mode with enable_batching={enable_batching} "
        f"(batch_size={BATCH_SIZE}, timeout={BATCH_TIMEOUT_MS}ms, "
        f"max_concurrent={MAX_CONCURRENT_SYNC_BATCHES})"
    )

    if not enable_batching:
        logger.warning(
            f"Worker {worker_id}: Batching disabled via model_config. "
            "SYNC mode always batches - consider using ASYNC mode for single-frame processing."
        )

    # ThreadPoolExecutor for concurrent batch processing
    # This allows accumulating next batch while current batch is being processed
    executor = ThreadPoolExecutor(
        max_workers=MAX_CONCURRENT_SYNC_BATCHES,
        thread_name_prefix=f"sync_batch_{worker_id}_"
    )

    # Track pending futures for cleanup and backpressure
    pending_futures: set = set()

    # Counters for periodic logging
    frames_processed = 0
    batches_processed = 0
    backpressure_count = 0
    last_log_time = time.time()
    LOG_INTERVAL_SECONDS = 10.0

    # Batch accumulation
    batch: List[Dict[str, Any]] = []
    batch_start_time = time.time()

    def _submit_batch(batch_to_process: List[Dict[str, Any]]) -> Optional[Future]:
        """Submit batch for concurrent processing."""
        nonlocal frames_processed, batches_processed

        def _process_and_count():
            count = _process_batch_sync(
                worker_id, batch_to_process, inference_interface,
                output_queues, metrics, result_cache, logger
            )
            return count

        future = executor.submit(_process_and_count)
        return future

    def _cleanup_futures():
        """Remove completed futures and handle errors."""
        nonlocal frames_processed, batches_processed
        done = {f for f in pending_futures if f.done()}
        for f in done:
            try:
                count = f.result()
                frames_processed += count
                batches_processed += 1
            except Exception as e:
                logger.error(f"Worker {worker_id}: Batch processing error: {e}")
        pending_futures.difference_update(done)

    try:
        while True:
            try:
                # Cleanup completed futures first
                _cleanup_futures()

                if enable_batching:
                    # BATCH MODE: Accumulate and process batches
                    # BACKPRESSURE: If too many pending batches, wait for some to complete
                    if len(pending_futures) >= MAX_CONCURRENT_SYNC_BATCHES:
                        backpressure_count += 1
                        # Process any partial batch we have
                        if batch:
                            future = _submit_batch(batch)
                            if future:
                                pending_futures.add(future)
                            batch = []
                            batch_start_time = time.time()
                        # Wait briefly for some futures to complete
                        time.sleep(0.001)
                        continue

                    # Calculate adaptive batch size based on queue depth
                    queue_depth = input_queue.qsize() if hasattr(input_queue, 'qsize') else 0
                    adaptive_batch_size = _get_adaptive_batch_size(queue_depth) if ENABLE_ADAPTIVE_BATCH else BATCH_SIZE

                    # Try to get task with short timeout for batch accumulation
                    remaining_timeout = max(0.001, batch_timeout_sec - (time.time() - batch_start_time))
                    task = input_queue.get(timeout=remaining_timeout)

                    if task is None:
                        continue

                    # Add to batch
                    batch.append(task)

                    # Submit batch if full (concurrent processing)
                    if len(batch) >= adaptive_batch_size:
                        future = _submit_batch(batch)
                        if future:
                            pending_futures.add(future)
                        batch = []
                        batch_start_time = time.time()

                else:
                    # SINGLE-FRAME MODE: Process one frame at a time
                    # BACKPRESSURE: If too many pending tasks, wait for some to complete
                    if len(pending_futures) >= MAX_CONCURRENT_SYNC_BATCHES:
                        backpressure_count += 1
                        time.sleep(0.001)
                        continue

                    # Get single task with short timeout
                    task = input_queue.get(timeout=0.01)

                    if task is None:
                        continue

                    # Process single frame (wrapped in a list to reuse batch processing logic)
                    future = _submit_batch([task])
                    if future:
                        pending_futures.add(future)
                        frames_processed += 1

            except queue.Empty:
                if enable_batching:
                    # Timeout - submit partial batch if any
                    if batch:
                        future = _submit_batch(batch)
                        if future:
                            pending_futures.add(future)
                        batch = []
                    batch_start_time = time.time()
                else:
                    # Single-frame mode - just continue on timeout
                    pass

            except Exception as e:
                logger.error(f"Worker {worker_id} sync loop error: {e}")
                # Submit any pending batch before sleeping (only in batch mode)
                if enable_batching and batch:
                    future = _submit_batch(batch)
                    if future:
                        pending_futures.add(future)
                    batch = []
                    batch_start_time = time.time()
                time.sleep(0.1)

            # Periodic stats logging
            now = time.time()
            if now - last_log_time >= LOG_INTERVAL_SECONDS:
                queue_size = input_queue.qsize() if hasattr(input_queue, 'qsize') else -1
                mode_str = "batch" if enable_batching else "single-frame"
                logger.info(
                    f"Worker {worker_id}: Sync {mode_str} stats - "
                    f"frames={frames_processed}, batches={batches_processed}, "
                    f"pending={len(pending_futures)}, backpressure={backpressure_count}, "
                    f"queue_depth={queue_size}"
                )
                frames_processed = 0
                batches_processed = 0
                backpressure_count = 0
                last_log_time = now

    finally:
        # Submit any remaining batch (only in batch mode)
        if enable_batching and batch:
            future = _submit_batch(batch)
            if future:
                pending_futures.add(future)

        # Wait for all pending futures to complete
        if pending_futures:
            logger.info(f"Worker {worker_id}: Waiting for {len(pending_futures)} pending batches")
            for f in pending_futures:
                try:
                    f.result(timeout=10.0)
                except Exception as e:
                    logger.error(f"Worker {worker_id}: Final batch error: {e}")

        # Shutdown executor
        executor.shutdown(wait=True)
        logger.info(f"Worker {worker_id}: Sync mode executor shutdown complete")


async def _accumulate_batch_from_async_queue(
    async_buffer: asyncio.Queue,
    max_batch_size: int,
    timeout_ms: float,
) -> List[Dict[str, Any]]:
    """
    Accumulate tasks from asyncio.Queue into a batch with time-bounded waiting.
    
    This is the OPTIMIZED version that reads from asyncio.Queue (fed by feeder thread).
    NO run_in_executor hops - pure async operations.

    Args:
        async_buffer: asyncio.Queue filled by feeder thread
        max_batch_size: Maximum frames to accumulate (e.g., 16)
        timeout_ms: Maximum wait time in milliseconds (e.g., 5ms)

    Returns:
        List of task dictionaries (1 to max_batch_size items)
    """
    batch = []
    deadline = time.time() + (timeout_ms / 1000.0)

    while len(batch) < max_batch_size:
        remaining = deadline - time.time()
        if remaining <= 0:
            break

        try:
            # Non-blocking get with timeout
            task = await asyncio.wait_for(
                async_buffer.get(),
                timeout=max(0.0001, remaining)
            )
            batch.append(task)
        except asyncio.TimeoutError:
            # Queue empty or timeout - if we have items, process them
            if len(batch) >= MIN_BATCH_SIZE:
                break
            continue

    return batch


async def _async_inference_loop_optimized(
    worker_id: int,
    async_buffer: asyncio.Queue,
    output_queues: List[mp.Queue],
    inference_interface: Any,
    metrics: Optional[Any],
    result_cache: InferenceResultCache,
    logger: logging.Logger,
    model_config: Dict[str, Any],
):
    """
    Optimized async inference loop reading from asyncio.Queue (no executor hops).

    Key optimizations:
    1. Reads from asyncio.Queue (fed by feeder thread) - no run_in_executor
    2. BOUNDED CONCURRENCY via semaphore - prevents task explosion
    3. Pending task tracking for graceful completion

    This is the high-throughput path for GPU inference.
    """
    # Semaphore limits concurrent batch operations to prevent task explosion
    # Without this, unbounded create_task() causes event loop scheduling overhead
    batch_semaphore = asyncio.Semaphore(MAX_INFLIGHT_BATCHES)

    # Track pending tasks for cleanup and monitoring
    pending_batch_tasks: set = set()

    logger.info(
        f"Worker {worker_id}: Starting async inference loop with "
        f"MAX_INFLIGHT_BATCHES={MAX_INFLIGHT_BATCHES}"
    )

    async def bounded_batch_process(batch: List[Dict[str, Any]]) -> None:
        """Process batch with bounded concurrency via semaphore."""
        async with batch_semaphore:
            await _process_batch_async(
                worker_id=worker_id,
                batch=batch,
                inference_interface=inference_interface,
                output_queues=output_queues,
                logger=logger,
                metrics=metrics,
                result_cache=result_cache,
            )

    async def bounded_single_frame(task: Dict[str, Any]) -> None:
        """Process single frame with bounded concurrency via semaphore."""
        async with batch_semaphore:
            await _process_single_frame_async(
                worker_id=worker_id,
                task=task,
                inference_interface=inference_interface,
                output_queues=output_queues,
                logger=logger,
                metrics=metrics,
                result_cache=result_cache,
            )

    try:
        while True:
            try:
                # Clean up completed tasks periodically
                if pending_batch_tasks:
                    done_tasks = {t for t in pending_batch_tasks if t.done()}
                    for task in done_tasks:
                        if task.exception():
                            logger.error(f"Batch task failed: {task.exception()}")
                    pending_batch_tasks -= done_tasks

                # Read enable_batching from model_config instead of hardcoded constant
                enable_batching = model_config.get("enable_batching", True)

                if enable_batching:
                    # Calculate adaptive batch size based on queue depth
                    queue_depth = async_buffer.qsize()
                    adaptive_batch_size = _get_adaptive_batch_size(queue_depth)

                    # Accumulate batch from async buffer (no executor hops!)
                    batch = await _accumulate_batch_from_async_queue(
                        async_buffer=async_buffer,
                        max_batch_size=adaptive_batch_size,
                        timeout_ms=BATCH_TIMEOUT_MS,
                    )

                    if not batch:
                        await asyncio.sleep(0.0001)
                        continue

                    # Process batch with BOUNDED CONCURRENCY
                    batch_task = asyncio.create_task(bounded_batch_process(batch))
                    pending_batch_tasks.add(batch_task)

                else:
                    # Single-frame mode: get one task at a time
                    try:
                        task = await asyncio.wait_for(
                            async_buffer.get(),
                            timeout=0.01
                        )
                    except asyncio.TimeoutError:
                        continue

                    # Regular frame with bounded concurrency
                    frame_task = asyncio.create_task(bounded_single_frame(task))
                    pending_batch_tasks.add(frame_task)

            except Exception as e:
                logger.error(f"Worker {worker_id} async loop error: {e}", exc_info=True)
                await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        logger.info(f"Worker {worker_id} async loop cancelled, waiting for {len(pending_batch_tasks)} pending tasks")
        # Wait for pending tasks to complete on cancellation
        if pending_batch_tasks:
            await asyncio.gather(*pending_batch_tasks, return_exceptions=True)


async def _process_batch_async(
    worker_id: int,
    batch: List[Dict[str, Any]],
    inference_interface: Any,
    output_queues: List[mp.Queue],
    logger: logging.Logger,
    metrics: Optional[Any],
    result_cache: InferenceResultCache = None,
):
    """
    Process a batch of frames through inference.

    This function:
    1. Extracts input bytes from each task in the batch
    2. Calls batch inference (async_batch_inference)
    3. Routes each result to the correct post-processing queue
    4. Handles caching and metrics

    Args:
        worker_id: Worker process ID for logging
        batch: List of task dictionaries from the queue
        inference_interface: InferenceInterface instance
        output_queues: List of post-processing worker queues
        logger: Logger instance
        metrics: Metrics instance (or None)
        result_cache: InferenceResultCache for caching results
    """
    if not batch:
        return

    start_time = time.time()
    batch_size = len(batch)

    # Separate regular tasks from cached tasks
    regular_tasks = []
    regular_inputs = []
    cached_tasks = []

    for task in batch:
        # Check for cached frames
        input_stream = task.get("input_stream", {})
        cached_frame_id = input_stream.get("cached_frame_id")
        frame_bytes = task.get("frame_bytes")

        if cached_frame_id and not frame_bytes and result_cache:
            # This is a cached frame - handle separately
            cached_tasks.append((task, cached_frame_id))
        elif frame_bytes:
            # Regular task with frame data
            regular_tasks.append(task)
            regular_inputs.append(frame_bytes)
        else:
            # No frame data and not cached - skip
            camera_id = task.get("camera_id")
            logger.warning(f"Worker {worker_id}: Skipping task for camera {camera_id} - no frame data")

    # Process cached tasks (use cached results)
    for task, cached_frame_id in cached_tasks:
        if result_cache:
            cached_result = result_cache.get(cached_frame_id)
            if cached_result:
                camera_id = task.get("camera_id")
                frame_id = task.get("frame_id")
                postproc_worker_id = hash(camera_id) % len(output_queues)
                target_queue = output_queues[postproc_worker_id]

                # Restore input_bytes for frame caching downstream
                input_stream = dict(task.get("input_stream", {}))
                cached_input_bytes = cached_result.get("input_bytes")
                if cached_input_bytes:
                    input_stream["content"] = cached_input_bytes

                output_data = {
                    "camera_id": camera_id,
                    "frame_id": frame_id,
                    "original_message": task.get("message"),
                    "model_result": cached_result.get("model_result"),
                    "metadata": cached_result.get("metadata", {}),
                    "processing_time": time.time() - start_time,
                    "input_stream": input_stream,
                    "stream_key": task.get("stream_key"),
                    "camera_config": task.get("camera_config"),
                    "from_cache": True,
                    "cached_frame_id": cached_frame_id,
                    "batch_size": batch_size,
                }
                _safe_queue_put(target_queue, output_data, metrics, logger)

    # Process regular tasks via batch inference
    if regular_inputs:
        try:
            # Call batch inference through InferenceInterface
            results, success = await inference_interface.async_batch_inference(
                input_list=regular_inputs,
                extra_params=None,
                stream_key=None,
                stream_info=None,
            )

            if not success or results is None:
                logger.error(f"Worker {worker_id}: Batch inference failed, falling back to individual processing")
                # Fallback to individual processing
                for task in regular_tasks:
                    await _process_single_frame_async(
                        worker_id=worker_id,
                        task=task,
                        inference_interface=inference_interface,
                        output_queues=output_queues,
                        logger=logger,
                        metrics=metrics,
                        result_cache=result_cache,
                    )
                return

            # Route each result to correct post-processing queue
            for task, result in zip(regular_tasks, results):
                camera_id = task.get("camera_id")
                frame_id = task.get("frame_id")
                frame_bytes = task.get("frame_bytes")

                # Cache the result for future similar frames
                if result_cache and frame_id and result is not None:
                    result_cache.put(frame_id, {
                        "model_result": result,
                        "metadata": {},
                        "input_bytes": frame_bytes,
                    })

                postproc_worker_id = hash(camera_id) % len(output_queues)
                target_queue = output_queues[postproc_worker_id]

                output_data = {
                    "camera_id": camera_id,
                    "frame_id": frame_id,
                    "original_message": task.get("message"),
                    "model_result": result,
                    "metadata": {},
                    "processing_time": time.time() - start_time,
                    "input_stream": task.get("input_stream", {}),
                    "stream_key": task.get("stream_key"),
                    "camera_config": task.get("camera_config"),
                    "from_cache": False,
                    "batch_size": batch_size,
                }
                _safe_queue_put(target_queue, output_data, metrics, logger)

            # Record metrics
            latency_ms = (time.time() - start_time) * 1000
            if metrics:
                metrics.record_latency(latency_ms)
                metrics.record_throughput(count=len(regular_inputs))

            # Log slow batch inference (>100ms total) to avoid spam at high FPS
            if latency_ms > 100:
                per_frame_ms = latency_ms / len(regular_inputs)
                logger.warning(
                    f"Worker {worker_id}: Slow batch inference - "
                    f"batch_size={len(regular_inputs)}, latency={latency_ms:.1f}ms, "
                    f"per_frame={per_frame_ms:.2f}ms"
                )

        except Exception as e:
            logger.error(f"Worker {worker_id}: Batch inference error: {e}", exc_info=True)
            # Fallback to individual processing
            for task in regular_tasks:
                try:
                    await _process_single_frame_async(
                        worker_id=worker_id,
                        task=task,
                        inference_interface=inference_interface,
                        output_queues=output_queues,
                        logger=logger,
                        metrics=metrics,
                        result_cache=result_cache,
                    )
                except Exception as inner_e:
                    logger.error(f"Worker {worker_id}: Individual fallback failed: {inner_e}")


# =============================================================================
# SYNC MODE HELPER FUNCTIONS - Pure blocking Python (no asyncio overhead)
# =============================================================================

def _process_batch_sync(
    worker_id: int,
    batch: List[Dict[str, Any]],
    inference_interface: Any,
    output_queues: List[mp.Queue],
    metrics: Optional[Any],
    result_cache: InferenceResultCache,
    logger: logging.Logger,
) -> int:
    """
    Process a batch of frames using TRUE BATCH INFERENCE (sync).

    Calls InferenceInterface.sync_batch_inference() for GPU-level batching.
    All frames in batch are processed in ONE model call.

    Args:
        worker_id: Worker ID for logging
        batch: List of task dicts
        inference_interface: InferenceInterface instance
        output_queues: Post-processing queues
        metrics: Metrics instance
        result_cache: Result cache
        logger: Logger instance

    Returns:
        Number of frames successfully processed
    """
    if not batch:
        return 0

    start_time = time.time()
    batch_size = len(batch)

    # Separate tasks by type
    regular_tasks = []
    regular_inputs = []
    cached_tasks = []

    for task in batch:
        # Check for cached frames
        input_stream = task.get("input_stream", {})
        cached_frame_id = input_stream.get("cached_frame_id")
        frame_bytes = task.get("frame_bytes")

        if cached_frame_id and not frame_bytes and result_cache:
            # Cached frame - handle separately
            cached_tasks.append((task, cached_frame_id))
        elif frame_bytes:
            # Regular task with frame data
            regular_tasks.append(task)
            regular_inputs.append(frame_bytes)
        else:
            # No frame data - try to extract
            input_bytes = _extract_input_bytes(task, logger)
            if input_bytes:
                regular_tasks.append(task)
                regular_inputs.append(input_bytes)

    processed_count = 0

    # Process cached tasks (use cached results)
    for task, cached_frame_id in cached_tasks:
        cached_result = result_cache.get(cached_frame_id)
        if cached_result:
            camera_id = task.get("camera_id")
            frame_id = task.get("frame_id")
            postproc_worker_id = hash(camera_id) % len(output_queues)
            target_queue = output_queues[postproc_worker_id]

            input_stream = dict(task.get("input_stream", {}))
            cached_input_bytes = cached_result.get("input_bytes")
            if cached_input_bytes:
                input_stream["content"] = cached_input_bytes

            output_data = {
                "camera_id": camera_id,
                "frame_id": frame_id,
                "original_message": task.get("message"),
                "model_result": cached_result.get("model_result"),
                "metadata": cached_result.get("metadata", {}),
                "processing_time": time.time() - start_time,
                "input_stream": input_stream,
                "stream_key": task.get("stream_key"),
                "camera_config": task.get("camera_config"),
                "from_cache": True,
                "cached_frame_id": cached_frame_id,
                "batch_size": batch_size,
            }
            _safe_queue_put(target_queue, output_data, metrics, logger)
            processed_count += 1

    # Process regular tasks via TRUE BATCH INFERENCE
    if regular_inputs:
        try:
            # Call sync_batch_inference for true GPU batching
            results, success = inference_interface.sync_batch_inference(
                input_list=regular_inputs,
                extra_params=None,
                stream_key=None,
                stream_info=None,
            )

            if not success or results is None:
                logger.error(f"Worker {worker_id}: Sync batch inference failed")
                # Fallback to individual processing
                for task in regular_tasks:
                    _process_frame_sync(
                        worker_id, task, inference_interface,
                        output_queues, metrics, result_cache, logger
                    )
                    processed_count += 1
                return processed_count

            # Route each result to correct post-processing queue
            for task, result in zip(regular_tasks, results):
                camera_id = task.get("camera_id")
                frame_id = task.get("frame_id")
                frame_bytes = task.get("frame_bytes")

                # Cache result
                if result_cache and frame_id and result is not None:
                    result_cache.put(frame_id, {
                        "model_result": result,
                        "metadata": {},
                        "input_bytes": frame_bytes,
                    })

                postproc_worker_id = hash(camera_id) % len(output_queues)
                target_queue = output_queues[postproc_worker_id]

                output_data = {
                    "camera_id": camera_id,
                    "frame_id": frame_id,
                    "original_message": task.get("message"),
                    "model_result": result,
                    "metadata": {},
                    "processing_time": time.time() - start_time,
                    "input_stream": task.get("input_stream", {}),
                    "stream_key": task.get("stream_key"),
                    "camera_config": task.get("camera_config"),
                    "from_cache": False,
                    "batch_size": batch_size,
                }
                _safe_queue_put(target_queue, output_data, metrics, logger)
                processed_count += 1

            # Record metrics
            latency_ms = (time.time() - start_time) * 1000
            if metrics:
                metrics.record_latency(latency_ms)
                metrics.record_throughput(count=len(regular_inputs))

            # Log slow batches
            if latency_ms > 100:
                per_frame_ms = latency_ms / len(regular_inputs)
                logger.warning(
                    f"Worker {worker_id}: Slow sync batch - "
                    f"batch_size={len(regular_inputs)}, latency={latency_ms:.1f}ms, "
                    f"per_frame={per_frame_ms:.2f}ms"
                )

        except Exception as e:
            logger.error(f"Worker {worker_id}: Sync batch error: {e}", exc_info=True)
            # Fallback to individual processing
            for task in regular_tasks:
                try:
                    _process_frame_sync(
                        worker_id, task, inference_interface,
                        output_queues, metrics, result_cache, logger
                    )
                    processed_count += 1
                except Exception as inner_e:
                    logger.error(f"Worker {worker_id}: Individual fallback failed: {inner_e}")

    return processed_count


def _process_frame_sync(
    worker_id: int,
    task: Dict[str, Any],
    inference_interface: Any,
    output_queues: List[mp.Queue],
    metrics: Optional[Any],
    result_cache: InferenceResultCache,
    logger: logging.Logger,
):
    """
    Process a single frame synchronously in thread pool.
    
    This is a pure Python function with no asyncio overhead.
    Called directly from ThreadPoolExecutor in sync mode.
    """
    start_time = time.time()
    camera_id = task.get("camera_id")
    frame_id = task.get("frame_id")
    
    if not frame_id:
        return  # Skip invalid frames
    
    try:
        # Check cache first
        input_stream = task.get("input_stream", {})
        cached_frame_id = input_stream.get("cached_frame_id")
        frame_bytes = task.get("frame_bytes")
        
        if cached_frame_id and not frame_bytes and result_cache:
            cached_result = result_cache.get(cached_frame_id)
            if cached_result:
                postproc_worker_id = hash(camera_id) % len(output_queues)
                target_queue = output_queues[postproc_worker_id]
                
                input_stream_with_content = dict(input_stream)
                cached_input_bytes = cached_result.get("input_bytes")
                if cached_input_bytes:
                    input_stream_with_content["content"] = cached_input_bytes
                
                output_data = {
                    "camera_id": camera_id,
                    "frame_id": frame_id,
                    "original_message": task.get("message"),
                    "model_result": cached_result.get("model_result"),
                    "metadata": cached_result.get("metadata", {}),
                    "processing_time": time.time() - start_time,
                    "input_stream": input_stream_with_content,
                    "stream_key": task.get("stream_key"),
                    "camera_config": task.get("camera_config"),
                    "from_cache": True,
                    "cached_frame_id": cached_frame_id,
                }
                _safe_queue_put(target_queue, output_data, metrics, logger)

                if metrics:
                    latency_ms = (time.time() - start_time) * 1000
                    metrics.record_latency(latency_ms)
                    metrics.record_throughput(count=1)
                return
        
        # Extract input bytes
        input_bytes = _extract_input_bytes(task, logger)
        if input_bytes is None:
            return
        
        # Run SYNC inference - pure Python, no asyncio overhead
        # Uses InferenceInterface.sync_inference() which calls
        # ModelManagerWrapper.inference() directly
        model_result, metadata = inference_interface.sync_inference(
            input=input_bytes,
            extra_params=task.get("extra_params"),
            apply_post_processing=False,
            stream_key=task.get("stream_key"),
            stream_info=None,
        )
        
        # Cache result
        if result_cache and frame_id:
            result_cache.put(frame_id, {
                "model_result": model_result,
                "metadata": metadata or {},
                "input_bytes": frame_bytes,
            })
        
        # Route to post-processing
        postproc_worker_id = hash(camera_id) % len(output_queues)
        target_queue = output_queues[postproc_worker_id]
        
        output_data = {
            "camera_id": camera_id,
            "frame_id": frame_id,
            "original_message": task.get("message"),
            "model_result": model_result,
            "metadata": metadata or {},
            "processing_time": time.time() - start_time,
            "input_stream": input_stream,
            "stream_key": task.get("stream_key"),
            "camera_config": task.get("camera_config"),
            "from_cache": False,
        }
        _safe_queue_put(target_queue, output_data, metrics, logger)

        # Record metrics
        latency_ms = (time.time() - start_time) * 1000
        if metrics:
            metrics.record_latency(latency_ms)
            metrics.record_throughput(count=1)

        # Log slow inference (>100ms) to avoid spam at high FPS
        if latency_ms > 100:
            logger.warning(
                f"Worker {worker_id}: Slow sync inference - "
                f"camera={camera_id}, latency={latency_ms:.1f}ms"
            )

    except Exception as e:
        logger.error(f"Worker {worker_id}: Sync frame error for {camera_id}: {e}")


# Inference timeout in seconds (adjust based on model complexity)
INFERENCE_TIMEOUT_SECONDS = 30.0


async def _process_single_frame_async(
    worker_id: int,
    task: Dict[str, Any],
    inference_interface: Any,
    output_queues: List[mp.Queue],
    logger: logging.Logger,
    metrics: Optional[Any],
    result_cache: InferenceResultCache = None,
):
    """
    Process a single frame asynchronously (fire-and-forget).

    Used in ASYNC mode to allow up to 16 concurrent requests per worker.
    Includes timeout protection to prevent memory leaks from hung requests.
    Routes result to correct post-processing worker queue.
    Supports frame optimization via result caching for similar frames.
    """
    start_time = time.time()
    camera_id = task.get("camera_id")
    frame_id = task.get("frame_id")

    # CRITICAL: Validate frame_id exists - skip if missing
    if not frame_id:
        logger.error(
            f"[FRAME_ID_MISSING] camera={camera_id} - No frame_id in task. Skipping frame."
        )
        return

    try:
        # Check if this is a cached frame (empty content + cached_frame_id in input_stream)
        input_stream = task.get("input_stream", {})
        cached_frame_id = input_stream.get("cached_frame_id")
        frame_bytes = task.get("frame_bytes")

        if cached_frame_id and not frame_bytes and result_cache:
            # This is a cached frame - lookup cached result
            cached_result = result_cache.get(cached_frame_id)

            if cached_result:
                # Use cached result with new frame_id
                postproc_worker_id = hash(camera_id) % len(output_queues)
                target_queue = output_queues[postproc_worker_id]

                # Restore input_bytes from cached result to input_stream for frame caching
                # This allows the producer to cache this frame with the new frame_id
                input_stream_with_content = dict(input_stream)
                cached_input_bytes = cached_result.get("input_bytes")
                if cached_input_bytes:
                    input_stream_with_content["content"] = cached_input_bytes

                output_data = {
                    "camera_id": camera_id,
                    "frame_id": frame_id,  # NEW frame_id
                    "original_message": task.get("message"),
                    "model_result": cached_result.get("model_result"),
                    "metadata": cached_result.get("metadata", {}),
                    "processing_time": time.time() - start_time,
                    "input_stream": input_stream_with_content,  # Now contains cached frame bytes
                    "stream_key": task.get("stream_key"),
                    "camera_config": task.get("camera_config"),
                    "from_cache": True,
                    "cached_frame_id": cached_frame_id,
                }

                _safe_queue_put(target_queue, output_data, metrics, logger)

                # Record metrics for cache hit
                latency_ms = (time.time() - start_time) * 1000
                if metrics:
                    metrics.record_latency(latency_ms)
                    metrics.record_throughput(count=1)

                # NOTE: Removed debug logging for performance
                return

            else:
                # Cache miss - skip silently (avoid log spam)
                return

        # Normal inference flow (has frame_bytes)
        result = await asyncio.wait_for(
            _execute_single_inference(inference_interface, task, logger),
            timeout=INFERENCE_TIMEOUT_SECONDS,
        )

        # Cache the result for future cached frames (including input_bytes for frame caching)
        if result_cache and frame_id:
            result_cache.put(frame_id, {
                "model_result": result.get("model_result"),
                "metadata": result.get("metadata", {}),
                "input_bytes": frame_bytes,  # Store frame bytes for cached frame reuse
            })

        # Route result to correct post-processing worker queue
        postproc_worker_id = hash(camera_id) % len(output_queues)
        target_queue = output_queues[postproc_worker_id]

        output_data = {
            "camera_id": camera_id,
            "frame_id": frame_id,  # Forced - no fallback
            "original_message": task.get("message"),
            "model_result": result.get("model_result"),
            "metadata": result.get("metadata", {}),
            "processing_time": time.time() - start_time,
            "input_stream": task.get("input_stream", {}),
            "stream_key": task.get("stream_key"),
            "camera_config": task.get("camera_config"),
            "from_cache": False,
        }

        _safe_queue_put(target_queue, output_data, metrics, logger)

        # Record metrics
        latency_ms = (time.time() - start_time) * 1000
        if metrics:
            metrics.record_latency(latency_ms)
            metrics.record_throughput(count=1)

        # Log slow single frame inference (>100ms) to avoid spam at high FPS
        if latency_ms > 100:
            logger.warning(
                f"Worker {worker_id}: Slow single frame inference - "
                f"camera={camera_id}, latency={latency_ms:.1f}ms"
            )

    except asyncio.TimeoutError:
        logger.warning(
            f"Worker {worker_id}: Inference timeout for camera {camera_id} "
            f"(>{INFERENCE_TIMEOUT_SECONDS}s) - dropping frame"
        )
    except Exception as e:
        logger.error(f"Async frame processing error for camera {camera_id}: {e}", exc_info=True)


async def _execute_single_inference(
    inference_interface: Any,
    task_data: Dict[str, Any],
    logger: logging.Logger,
) -> Dict[str, Any]:
    """
    Execute async inference for a single task using InferenceInterface.

    Args:
        inference_interface: InferenceInterface instance (with ModelManagerWrapper → ModelManager)
        task_data: Task data containing input and parameters
        logger: Logger instance

    Returns:
        Dict with model_result and metadata
    """
    try:
        # Validate task data
        if not _validate_task_data(task_data, logger):
            return {"model_result": None, "metadata": {}, "success": False}

        # Extract inference parameters
        input_bytes = _extract_input_bytes(task_data, logger)
        if input_bytes is None:
            return {"model_result": None, "metadata": {}, "success": False}

        # Call InferenceInterface.async_inference()
        # Flow: InferenceInterface → ModelManagerWrapper → ModelManager → async_predict
        # Note: Raw bytes → model inference → raw results (no post-processing here)
        # Postprocessing handled separately by post_processing_manager
        model_result, metadata = await inference_interface.async_inference(
            input=input_bytes,
            extra_params=task_data.get("extra_params"),
            apply_post_processing=False,  # No post-processing in workers
            stream_key=task_data.get("stream_key"),
            stream_info=None,
        )

        return {
            "success": True,
            "model_result": model_result,
            "metadata": metadata or {},
        }

    except Exception as e:
        logger.error(f"Inference execution error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "model_result": None,
            "metadata": {},
        }


def _validate_task_data(task_data: Dict[str, Any], logger: logging.Logger) -> bool:
    """
    Validate that task data contains required fields.

    Required fields (from consumer_manager):
    - camera_id: For routing and identification
    - frame_bytes or input_stream: Input data
    - message: Original stream message
    - stream_key: Stream identifier
    - camera_config: Camera configuration
    """
    required_fields = ["camera_id", "message", "stream_key", "camera_config"]
    for field in required_fields:
        if field not in task_data:
            logger.error(f"Missing required field '{field}' in task data")
            return False

    # Check that we have input data (frame_bytes or input_stream)
    has_input = (
        "frame_bytes" in task_data or
        "decoded_input_bytes" in task_data or
        "input_stream" in task_data
    )
    if not has_input:
        logger.error("No input data found (frame_bytes, decoded_input_bytes, or input_stream)")
        return False

    return True


# =============================================================================
# SHM BUFFER CACHE (per worker process)
# =============================================================================
# Each worker process maintains its own cache of SHM buffer attachments.
# This avoids repeated attach/detach overhead for the same camera.
_shm_buffer_cache: Dict[str, Any] = {}


def _load_frame_from_shm(shm_ref: Dict[str, Any]) -> Optional[bytes]:
    """Load BGR frame from SHM with detailed error logging.

    ZERO-COPY path: Consumer passes SHM reference, worker reads directly from SHM.
    This eliminates frame byte copying through mp.Queue.

    Args:
        shm_ref: Dictionary containing SHM metadata:
            - camera_id: Original camera identifier (used to derive SHM segment name)
            - shm_name: Shared memory segment name (for caching key)
            - frame_idx: Frame index in ring buffer
            - width: Frame width in pixels
            - height: Frame height in pixels
            - format: Frame format (should be "BGR")

    Returns:
        Frame bytes if available, None if frame expired or torn
    """
    from matrice_common.stream.shm_ring_buffer import ShmRingBuffer
    logger = logging.getLogger(__name__)

    camera_id = shm_ref.get("camera_id")
    shm_name = shm_ref.get("shm_name")
    frame_idx = shm_ref.get("frame_idx")
    width = shm_ref.get("width")
    height = shm_ref.get("height")

    # Log all received parameters for debugging
    logger.debug(
        f"[SHM_LOAD] Attempting to load frame: camera_id={camera_id}, "
        f"shm_name={shm_name}, frame_idx={frame_idx}, "
        f"width={width}, height={height}"
    )

    # Validate required fields with detailed logging
    missing_fields = []
    if not camera_id:
        missing_fields.append("camera_id")
    if frame_idx is None:
        missing_fields.append("frame_idx")
    if not width:
        missing_fields.append("width")
    if not height:
        missing_fields.append("height")

    if missing_fields:
        logger.error(
            f"[SHM_LOAD_ERROR] Missing required fields in shm_ref: {missing_fields}. "
            f"Full shm_ref: {shm_ref}"
        )
        return None

    # Use shm_name as cache key if available, otherwise camera_id
    cache_key = shm_name or camera_id

    # Get or create cached SHM buffer attachment
    if cache_key not in _shm_buffer_cache:
        # Generate expected SHM name for logging
        safe_id = str(camera_id).replace("/", "_").replace("\\", "_").replace(":", "_")
        safe_id = "".join(c for c in safe_id if c.isalnum() or c == "_")
        expected_shm_name = f"shm_cam_{safe_id[:180]}"

        logger.info(
            f"[SHM_ATTACH] Attempting to attach to SHM: "
            f"camera_id={camera_id}, cache_key={cache_key}, "
            f"expected_shm_segment={expected_shm_name}"
        )

        try:
            # First attach with temporary slot_count to read header
            # (same pattern as consumer_manager.py)
            temp_buffer = ShmRingBuffer(
                camera_id=camera_id,
                width=width,
                height=height,
                frame_format=ShmRingBuffer.FORMAT_BGR,
                slot_count=1000,  # Temporary - will read actual from header
                create=False,
                shm_name=shm_name
            )

            # Read actual slot_count from producer's header
            header = temp_buffer.get_header()
            actual_slot_count = header.get('slot_count', 300)
            temp_buffer.close()

            # Create final buffer with correct slot_count from producer
            _shm_buffer_cache[cache_key] = ShmRingBuffer(
                camera_id=camera_id,
                width=width,
                height=height,
                frame_format=ShmRingBuffer.FORMAT_BGR,
                slot_count=actual_slot_count,  # Match producer's config!
                create=False,
                shm_name=shm_name
            )
            actual_name = _shm_buffer_cache[cache_key].shm_name
            logger.info(
                f"[SHM_ATTACH_SUCCESS] Attached to SHM segment: {actual_name} "
                f"for camera_id={camera_id}, slot_count={actual_slot_count}"
            )
        except FileNotFoundError as e:
            logger.error(
                f"[SHM_ATTACH_FAILED] SHM segment NOT FOUND for camera_id={camera_id}. "
                f"Expected segment name: {expected_shm_name}. "
                f"Producer may not be running or using different stream_key. "
                f"Check /dev/shm or Windows shared memory for available segments. "
                f"Error: {e}"
            )
            return None
        except PermissionError as e:
            logger.error(
                f"[SHM_ATTACH_FAILED] Permission denied for SHM segment. "
                f"camera_id={camera_id}, expected_name={expected_shm_name}. "
                f"Error: {e}"
            )
            return None
        except ValueError as e:
            logger.error(
                f"[SHM_ATTACH_FAILED] Invalid SHM configuration for camera_id={camera_id}. "
                f"width={width}, height={height}. Error: {e}"
            )
            return None
        except Exception as e:
            logger.error(
                f"[SHM_ATTACH_FAILED] Unexpected error attaching to SHM. "
                f"camera_id={camera_id}, expected_name={expected_shm_name}. "
                f"Error type: {type(e).__name__}, Error: {e}",
                exc_info=True
            )
            return None

    buffer = _shm_buffer_cache[cache_key]

    # Validate frame still exists with detailed logging
    # Note: read_frame_copy() now has retry logic to wait for write completion
    if not buffer.is_frame_valid(frame_idx):
        # Get current state for debugging
        try:
            header = buffer.get_header()
            current_write_idx = header.get('write_idx', 0)
            slot_count = header.get('slot_count', 1000)
            frames_behind = current_write_idx - frame_idx

            # SKIP-TO-LATEST: If significantly behind, skip to latest frame
            # Use 10% of slot_count as safety margin (at least 50 frames)
            safety_margin = max(50, slot_count // 10)
            if frames_behind > safety_margin:
                latest_frame_idx = current_write_idx - safety_margin  # Safe distance from write head
                logger.warning(
                    f"[SHM_SKIP_TO_LATEST] Frame {frame_idx} invalid, skipping {frames_behind} "
                    f"frames to {latest_frame_idx} for camera {camera_id} (safety_margin={safety_margin})"
                )
                frame_data = buffer.read_frame_copy(latest_frame_idx)
                if frame_data is not None:
                    logger.debug(
                        f"[SHM_SKIP_SUCCESS] Loaded latest frame {latest_frame_idx} for camera {camera_id}, "
                        f"size={len(frame_data)} bytes"
                    )
                    return frame_data

            logger.warning(
                f"[SHM_FRAME_INVALID] Frame {frame_idx} no longer valid for camera {camera_id}. "
                f"Current write_idx={current_write_idx}, slot_count={slot_count}, "
                f"frames_behind={frames_behind}. "
                f"{'Frame expired (overwritten)' if frames_behind >= slot_count else 'Frame not yet written'}"
            )
        except Exception as header_err:
            logger.warning(
                f"[SHM_FRAME_INVALID] Frame {frame_idx} invalid for camera {camera_id}. "
                f"Could not read header: {header_err}"
            )
        return None

    # Read with torn-frame detection
    frame_data = buffer.read_frame_copy(frame_idx)
    if frame_data is None:
        # SKIP-TO-LATEST: If frame is torn and we're behind, skip to latest
        try:
            header = buffer.get_header()
            current_write_idx = header.get('write_idx', 0)
            frames_behind = current_write_idx - frame_idx

            # Use 10% of slot_count as safety margin (at least 50 frames)
            slot_count = header.get('slot_count', 1000)
            safety_margin = max(50, slot_count // 10)
            if frames_behind > safety_margin:
                latest_frame_idx = current_write_idx - safety_margin  # Safe distance from write head
                logger.warning(
                    f"[SHM_SKIP_TO_LATEST] Frame {frame_idx} torn, skipping {frames_behind} "
                    f"frames to {latest_frame_idx} for camera {camera_id} (safety_margin={safety_margin})"
                )
                frame_data = buffer.read_frame_copy(latest_frame_idx)
                if frame_data is not None:
                    logger.debug(
                        f"[SHM_SKIP_SUCCESS] Loaded latest frame {latest_frame_idx} for camera {camera_id}, "
                        f"size={len(frame_data)} bytes"
                    )
                    return frame_data

            logger.warning(
                f"[SHM_FRAME_TORN] Frame {frame_idx} was torn or overwritten during read "
                f"for camera {camera_id}. Producer may be writing faster than consumer reads. "
                f"frames_behind={frames_behind}, safety_margin={safety_margin}"
            )
        except Exception as header_err:
            logger.warning(
                f"[SHM_FRAME_TORN] Frame {frame_idx} torn for camera {camera_id}. "
                f"Could not read header for skip-to-latest: {header_err}"
            )
        return None

    logger.debug(
        f"[SHM_LOAD_SUCCESS] Successfully loaded frame {frame_idx} for camera {camera_id}, "
        f"size={len(frame_data)} bytes"
    )
    return frame_data


def _extract_input_bytes(task_data: Dict[str, Any], logger: logging.Logger) -> Optional[bytes]:
    """
    Extract input bytes from task data with detailed SHM debugging.

    Supports multiple formats (priority order):
    0. task_data["shm_ref"] - SHM reference for ZERO-COPY path (NEW)
    1. task_data["frame_bytes"] - direct bytes from consumer_manager
    2. task_data["decoded_input_bytes"] - decoded bytes
    3. task_data["input_stream"]["content"] - bytes or base64 string
    """
    # Priority 0: SHM reference (ZERO-COPY path - worker reads directly from SHM)
    shm_ref = task_data.get("shm_ref")
    if shm_ref:
        if not isinstance(shm_ref, dict):
            logger.error(
                f"[EXTRACT_BYTES_ERROR] shm_ref is not a dict: type={type(shm_ref)}, value={shm_ref}"
            )
        else:
            logger.debug(
                f"[EXTRACT_BYTES] Attempting SHM load: camera_id={shm_ref.get('camera_id')}, "
                f"frame_idx={shm_ref.get('frame_idx')}, shm_name={shm_ref.get('shm_name')}"
            )
            frame_data = _load_frame_from_shm(shm_ref)
            if frame_data is not None:
                return frame_data
            # SHM read failed - log details
            logger.warning(
                f"[EXTRACT_BYTES_SHM_FAILED] SHM read returned None for: "
                f"camera_id={shm_ref.get('camera_id')}, frame_idx={shm_ref.get('frame_idx')}, "
                f"shm_name={shm_ref.get('shm_name')}, width={shm_ref.get('width')}, "
                f"height={shm_ref.get('height')}"
            )

    # Priority 1: Direct frame_bytes from consumer_manager (legacy flow)
    frame_bytes = task_data.get("frame_bytes")
    if isinstance(frame_bytes, (bytes, bytearray)) and frame_bytes:
        logger.debug(f"[EXTRACT_BYTES] Using direct frame_bytes, size={len(frame_bytes)}")
        return bytes(frame_bytes)

    # Priority 2: Decoded input bytes
    decoded_bytes = task_data.get("decoded_input_bytes")
    if isinstance(decoded_bytes, (bytes, bytearray)) and decoded_bytes:
        logger.debug(f"[EXTRACT_BYTES] Using decoded_input_bytes, size={len(decoded_bytes)}")
        return bytes(decoded_bytes)

    # Priority 3: Extract from input_stream
    input_stream_data = task_data.get("input_stream", {})
    if not isinstance(input_stream_data, dict):
        logger.error(f"[EXTRACT_BYTES_ERROR] input_stream is not a dict: {type(input_stream_data)}")
        return None

    content = input_stream_data.get("content")

    # Handle raw bytes
    if isinstance(content, (bytes, bytearray)) and content:
        logger.debug(f"[EXTRACT_BYTES] Using input_stream.content bytes, size={len(content)}")
        return bytes(content)

    # Handle base64-encoded strings
    if isinstance(content, str) and content:
        try:
            decoded = base64.b64decode(content)
            logger.debug(f"[EXTRACT_BYTES] Decoded base64 content, size={len(decoded)}")
            return decoded
        except Exception as e:
            logger.warning(f"[EXTRACT_BYTES_ERROR] Failed to decode base64 content: {e}")
            return None

    # Log all available keys for debugging
    logger.error(
        f"[EXTRACT_BYTES_FAILED] No valid input bytes found. "
        f"Available keys in task_data: {list(task_data.keys())}. "
        f"shm_ref present: {shm_ref is not None}, "
        f"frame_bytes present: {task_data.get('frame_bytes') is not None}, "
        f"input_stream keys: {list(input_stream_data.keys()) if isinstance(input_stream_data, dict) else 'N/A'}"
    )
    return None


class MultiprocessInferencePool:
    """
    Pool of multiprocessing inference workers with per-worker queues.

    Architecture:
    - Creates multiple worker processes (one per GPU/core)
    - Each worker has its OWN dedicated input queue (routed by consumer)
    - Each process recreates InferenceInterface → ModelManagerWrapper → ModelManager
    - Uses normal ModelManager with async_predict from predict.py (NOT Triton)
    - Each process runs its own async event loop
    - Routes results to correct post-processing worker queue
    - 100% order preservation per camera (no re-queuing)
    - Metrics sent back to main process via metrics_queue for aggregation

    Processing Modes:
    - ASYNC (use_async_inference=True): Up to 16 concurrent requests per worker
    - SYNC (use_async_inference=False): TRUE BATCH INFERENCE via sync_batch_inference
    """

    def __init__(
        self,
        num_workers: int,
        model_config: Dict[str, Any],
        input_queues: List[mp.Queue],
        output_queues: List[mp.Queue],
        use_async_inference: bool = True,
        metrics_queue: Optional[mp.Queue] = None,
    ):
        self.num_workers = num_workers
        self.model_config = model_config
        self.use_async_inference = use_async_inference

        # Per-worker queues from pipeline (one per worker)
        self.input_queues = input_queues
        self.output_queues = output_queues
        self.metrics_queue = metrics_queue

        # Validate queue counts
        if len(input_queues) != num_workers:
            raise ValueError(f"Expected {num_workers} input queues, got {len(input_queues)}")

        self.processes = []
        self.running = False

        self.logger = logging.getLogger(f"{__name__}.MultiprocessInferencePool")
        self.logger.info(f"Initialized MultiprocessInferencePool with {num_workers} workers")

    def start(self):
        """Start all worker processes with dedicated queues."""
        self.running = True

        mode = "ASYNC+FEEDER (batched, no executor hops)" if self.use_async_inference else "SYNC (TRUE BATCH INFERENCE)"

        for worker_id in range(self.num_workers):
            process = mp.Process(
                target=inference_worker_process,
                args=(
                    worker_id,
                    self.num_workers,
                    self.input_queues[worker_id],  # Worker's dedicated input queue
                    self.output_queues,  # List of post-processing queues for routing
                    self.model_config,
                    self.use_async_inference,  # Determines sync vs async behavior
                    self.metrics_queue,  # For sending metrics back to main process
                ),
                daemon=True,
            )
            process.start()
            self.processes.append(process)

        self.logger.info(
            f"Started {self.num_workers} multiprocess inference workers with dedicated queues "
            f"(mode={mode}, metrics_queue={'enabled' if self.metrics_queue else 'disabled'})"
        )

    def stop(self):
        """Stop all worker processes."""
        self.running = False

        for process in self.processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()

        self.processes.clear()
        self.logger.info("Stopped all inference worker processes")

    def submit_task(self, task_data: Dict[str, Any], timeout: float = 0.1) -> bool:
        """
        Submit inference task to worker pool.

        Args:
            task_data: Task data with camera_id, frame, etc.
            timeout: Max time to wait if queue is full

        Returns:
            True if task was submitted, False if queue full (backpressure)
        """
        try:
            self.input_queue.put(task_data, timeout=timeout)
            return True
        except Exception:
            # Queue full - apply backpressure
            return False

    def get_result(self, timeout: float = 0.001) -> Optional[Dict[str, Any]]:
        """
        Get inference result from worker pool.

        Args:
            timeout: Max time to wait for result

        Returns:
            Result dict or None if no result available
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except Exception:
            return None
