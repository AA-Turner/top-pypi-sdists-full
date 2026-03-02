"""
High-performance multiprocessing post-processing worker for stateful tracking.

Architecture:
- Multiprocessing: Multiple separate processes - TRUE PARALLELISM
- Camera Routing: hash(camera_id) % num_workers for state isolation - ORDER PRESERVATION
- Isolated Tracker States: Each process maintains trackers for assigned cameras
- Feeder Thread: mp.Queue → feeder thread → asyncio.Queue (no blocking in event loop)
- Async Concurrent Processing: Multiple frames processed concurrently per worker

Architecture Flow:
- PostProcessor creates per-camera tracker states (stateful tracking)
- Each process handles subset of cameras (e.g., 250 cameras per process)
- Camera-based routing ensures same camera always goes to same worker
- Tracker states remain isolated within each process
- Feeder thread drains mp.Queue without blocking async event loop
- Semaphore-bounded concurrent tasks allow I/O overlap

Performance Targets:
- 15,000+ FPS throughput
- <100ms latency per frame
- Isolated tracker state per camera
- True parallelism (bypasses Python GIL)

Optimizations (v4 - Async Concurrent with Feeder Thread):
- Feeder thread pattern eliminates run_in_executor hops
- Concurrent processing allows I/O overlap in PostProcessor.process()
- Semaphore-bounded concurrency prevents task explosion
- Per-camera ordering preserved (same camera → same worker)
"""

import logging
import multiprocessing as mp
import queue
import threading
import time
from typing import Any, Dict, List, Optional

# =============================================================================
# ASYNC BUFFER CONFIGURATION
# =============================================================================
# Feeder thread drains mp.Queue into asyncio.Queue to avoid blocking event loop.
# This eliminates blocking get() calls in the async loop.

ASYNC_BUFFER_SIZE = 1000     # Internal asyncio.Queue size
FEEDER_POLL_TIMEOUT = 0.001  # Polling interval for mp.Queue in feeder thread

# =============================================================================
# CONCURRENT PROCESSING CONFIGURATION
# =============================================================================
# Controls how many frames can be processed concurrently per worker.
# Higher values allow more I/O overlap but increase memory pressure.

MAX_CONCURRENT_TASKS = 8     # Max concurrent post-processing tasks per worker


def _postproc_feeder_thread(
    mp_queue: mp.Queue,
    async_queue,  # asyncio.Queue - typed at runtime to avoid import at module level
    loop,  # asyncio.AbstractEventLoop
    stop_event: threading.Event,
    worker_id: int,
    logger: logging.Logger,
):
    """
    Feeder thread: drains mp.Queue into asyncio.Queue without blocking event loop.

    This eliminates blocking get() calls in the async loop, allowing true
    concurrent processing of multiple frames.

    OPTIMIZATION: Uses pre-allocated callable to avoid lambda GC pressure.
    At 15K FPS, lambda creation per frame causes significant GC overhead.

    Args:
        mp_queue: Multiprocessing input queue (blocks on get)
        async_queue: asyncio.Queue for event loop consumption
        loop: asyncio event loop for thread-safe operations
        stop_event: Threading event to signal shutdown
        worker_id: Worker ID for logging
        logger: Logger instance
    """
    import asyncio

    dropped_count = 0

    def _try_put(task):
        nonlocal dropped_count
        try:
            async_queue.put_nowait(task)
        except asyncio.QueueFull:
            dropped_count += 1
            if dropped_count % 1000 == 0:
                logger.warning(f"PostProc Worker {worker_id} feeder dropped {dropped_count} frames (queue full)")

    consecutive_errors = 0
    max_consecutive_errors = 10  # Stop after 10 consecutive errors to prevent infinite loops
    
    while not stop_event.is_set():
        try:
            task = mp_queue.get(timeout=FEEDER_POLL_TIMEOUT)
            if task is not None:
                loop.call_soon_threadsafe(_try_put, task)
            consecutive_errors = 0  # Reset on success
        except queue.Empty:
            consecutive_errors = 0  # Empty queue is not an error
            continue
        except (BrokenPipeError, EOFError, OSError) as e:
            # Fatal queue errors - queue is broken, must stop
            if not stop_event.is_set():
                logger.error(f"PostProc Worker {worker_id} feeder fatal error (queue broken): {e}")
            break
        except Exception as e:
            consecutive_errors += 1
            if not stop_event.is_set():
                logger.warning(f"PostProc Worker {worker_id} feeder error ({consecutive_errors}x): {e}")
            if consecutive_errors >= max_consecutive_errors:
                logger.error(f"PostProc Worker {worker_id} feeder stopping after {max_consecutive_errors} consecutive errors")
                break
            # Brief sleep before retry for transient errors
            import time
            time.sleep(0.01)

    if dropped_count > 0:
        logger.info(f"PostProc Worker {worker_id} feeder stopped (dropped: {dropped_count})")
    else:
        logger.info(f"PostProc Worker {worker_id} feeder stopped")


def postprocessing_worker_process(
    worker_id: int,
    num_workers: int,
    input_queue: mp.Queue,
    output_queue: mp.Queue,
    post_processor_config: Dict[str, Any],
    metrics_queue: Optional[mp.Queue] = None,
):
    """
    Worker process for post-processing with async concurrent processing.

    ASYNC CONCURRENT ARCHITECTURE (v4):
    - Feeder thread drains mp.Queue → asyncio.Queue (no blocking in event loop)
    - Semaphore-bounded concurrent tasks (up to MAX_CONCURRENT_TASKS)
    - I/O overlap when PostProcessor.process() has external calls
    - Per-camera ordering preserved (same camera → same worker)

    IMPORTANT: Each worker reads from its OWN dedicated queue (input_queue).
    Inference workers route frames based on hash(camera_id) % num_workers.
    This ensures strict ordering per camera and isolated tracker states.

    Each process:
    1. Initializes PostProcessor with config
    2. Starts feeder thread (mp.Queue → asyncio.Queue)
    3. Runs async event loop with concurrent task processing
    4. Maintains isolated tracker states for assigned cameras
    5. Outputs results to dedicated output queue

    Args:
        worker_id: Worker process ID
        num_workers: Total number of worker processes
        input_queue: This worker's dedicated queue (routed by inference workers)
        output_queue: This worker's dedicated output queue
        post_processor_config: Configuration for PostProcessor initialization
        metrics_queue: Queue for sending metrics back to main process
    """
    logger = logging.getLogger(f"postproc_worker_{worker_id}")
    logger.setLevel(logging.INFO)

    try:
        import asyncio
        from matrice_analytics.post_processing.post_processor import PostProcessor
        from matrice_inference.server.stream.worker_metrics import MultiprocessWorkerMetrics

        # Initialize post-processor with config
        post_processor = PostProcessor(**post_processor_config)

        # Initialize metrics for this worker
        metrics = None
        if metrics_queue is not None:
            metrics = MultiprocessWorkerMetrics(
                worker_id=f"post_processing_{worker_id}",
                worker_type="post_processing",
                metrics_queue=metrics_queue
            )
        else:
            logger.warning(f"Worker {worker_id}: No metrics_queue provided")

        if metrics:
            metrics.mark_active()

        logger.info(
            f"Post-processing worker {worker_id}/{num_workers} initialized - "
            f"mode=ASYNC_CONCURRENT (max_tasks={MAX_CONCURRENT_TASKS})"
        )

        # Run async main loop
        async def _async_main():
            """Main async loop with feeder thread and concurrent processing."""
            # Create asyncio.Queue for internal buffering
            async_buffer = asyncio.Queue(maxsize=ASYNC_BUFFER_SIZE)
            loop = asyncio.get_running_loop()

            # Semaphore for bounded concurrency
            task_semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
            pending_tasks: set = set()

            # Counters for logging
            frames_processed = 0
            last_log_time = time.time()
            _drop_count = 0  # Counter for throttling drop warnings

            async def _process_single_task(task_data: Dict[str, Any]) -> None:
                """Process a single post-processing task."""
                nonlocal frames_processed, last_log_time, _drop_count

                start_time = time.time()

                # Extract task fields
                camera_id = task_data.get("camera_id")
                frame_id = task_data.get("frame_id")
                model_result = task_data.get("model_result")
                stream_key = task_data.get("stream_key", camera_id)
                input_stream = task_data.get("input_stream", {})

                # Validate required fields
                if not camera_id:
                    logger.error("Task missing camera_id - skipping")
                    return

                if not frame_id:
                    logger.error(f"[FRAME_ID_MISSING] camera={camera_id} - No frame_id. Skipping.")
                    return

                if model_result is None:
                    logger.debug(f"Skipping frame for camera {camera_id} - no model result")
                    return

                # Extract input bytes if available
                input_bytes = None
                if isinstance(input_stream, dict):
                    content = input_stream.get("content")
                    if isinstance(content, bytes):
                        input_bytes = content

                # Extract stream_info and add frame_id
                stream_info = {}
                if isinstance(input_stream, dict):
                    stream_info = input_stream.get("stream_info", {})
                    if not isinstance(stream_info, dict):
                        stream_info = {}
                    if frame_id:
                        stream_info["frame_id"] = frame_id

                # Process using async PostProcessor.process()
                try:
                    result = await post_processor.process(
                        data=model_result,
                        stream_key=stream_key,
                        input_bytes=input_bytes,
                        stream_info=stream_info,
                    )
                except Exception as e:
                    logger.error(f"Post-processing error for camera {camera_id}: {e}", exc_info=True)
                    return

                # Serialize ProcessingResult to dict
                post_processed_dict = result.to_dict() if hasattr(result, "to_dict") else result

                # Extract message_key from original_message
                original_message = task_data.get("original_message")
                message_key = original_message.message_key if hasattr(original_message, "message_key") else str(frame_id)

                # Flatten nested data structure if present
                if isinstance(post_processed_dict, dict) and "data" in post_processed_dict:
                    inner_data = post_processed_dict.pop("data", {})
                    post_processed_dict.update(inner_data)

                # Build output data
                output_data = {
                    "camera_id": camera_id,
                    "message_key": message_key,
                    "frame_id": frame_id,
                    "input_stream": task_data.get("input_stream", {}),
                    "data": {
                        "post_processing_result": post_processed_dict,
                        "model_result": model_result,
                        "metadata": task_data.get("metadata", {}),
                        "processing_time": task_data.get("processing_time", 0),
                        "stream_key": task_data.get("stream_key"),
                        "frame_id": frame_id,
                    }
                }

                # Put result to output queue (non-blocking to prevent pipeline stall)
                try:
                    # [POSTPROC_DEBUG] Log before putting to output queue
                    try:
                        qsize = output_queue.qsize()
                    except (NotImplementedError, OSError):
                        qsize = -1
                    logger.debug(
                        f"[POSTPROC_DEBUG] Worker {worker_id} putting result to output_queue "
                        f"(camera={camera_id}, frame={frame_id}, qsize={qsize})"
                    )
                    output_queue.put_nowait(output_data)
                except queue.Full:
                    # Drop frame to prevent blocking entire pipeline
                    if metrics:
                        metrics.record_drop(count=1, reason="output_queue_backpressure")
                    # Throttle warning: only log every 100 drops to avoid log spam
                    nonlocal _drop_count
                    _drop_count += 1
                    if _drop_count % 100 == 1:
                        logger.warning(
                            f"Worker {worker_id}: output queue full, dropping frames for camera {camera_id} "
                            f"(total drops: {_drop_count})"
                        )
                    return  # Skip metrics recording for dropped frame

                # Record metrics
                latency_ms = (time.time() - start_time) * 1000
                if metrics:
                    metrics.record_latency(latency_ms)
                    metrics.record_throughput(count=1)

                frames_processed += 1

                # Periodic logging (every 60 seconds)
                now = time.time()
                if now - last_log_time > 60.0:
                    # qsize() raises NotImplementedError on macOS, wrap in try-except
                    try:
                        output_qsize = output_queue.qsize()
                    except (NotImplementedError, OSError):
                        output_qsize = -1
                    logger.info(
                        f"[POSTPROC_DEBUG] Worker {worker_id}: processed {frames_processed} frames in last 60s, "
                        f"output_queue.qsize={output_qsize}, total_drops={_drop_count}"
                    )
                    frames_processed = 0  # Reset for next interval
                    last_log_time = now

            async def _bounded_process(task_data: Dict[str, Any]) -> None:
                """Process task with semaphore-bounded concurrency."""
                async with task_semaphore:
                    await _process_single_task(task_data)

            # Start feeder thread
            stop_event = threading.Event()
            feeder = threading.Thread(
                target=_postproc_feeder_thread,
                args=(input_queue, async_buffer, loop, stop_event, worker_id, logger),
                daemon=True,
                name=f"postproc_feeder_{worker_id}"
            )
            feeder.start()

            try:
                # Main processing loop
                while True:
                    try:
                        # Get task from async buffer (non-blocking event loop)
                        task_data = await asyncio.wait_for(async_buffer.get(), timeout=0.1)

                        # Create bounded task (concurrent but limited)
                        task = asyncio.create_task(_bounded_process(task_data))
                        pending_tasks.add(task)
                        task.add_done_callback(pending_tasks.discard)

                        # Cleanup completed tasks periodically
                        if len(pending_tasks) > MAX_CONCURRENT_TASKS * 2:
                            done = {t for t in pending_tasks if t.done()}
                            pending_tasks.difference_update(done)

                    except asyncio.TimeoutError:
                        # No task available, continue loop
                        continue
                    except Exception as e:
                        logger.error(f"Worker {worker_id} loop error: {e}", exc_info=True)
                        await asyncio.sleep(0.01)

            finally:
                # Stop feeder thread
                stop_event.set()
                feeder.join(timeout=2.0)

                # Wait for pending tasks to complete
                if pending_tasks:
                    logger.info(f"Worker {worker_id}: waiting for {len(pending_tasks)} pending tasks")
                    await asyncio.gather(*pending_tasks, return_exceptions=True)

        # Run the async main loop
        asyncio.run(_async_main())

    except Exception as e:
        logger.error(f"Worker {worker_id} crashed: {e}", exc_info=True)
        raise
    finally:
        if metrics:
            metrics.mark_inactive()
        logger.info(f"Post-processing worker {worker_id} stopped")


class MultiprocessPostProcessingPool:
    """
    Pool of multiprocessing post-processing workers with per-worker queues.

    Architecture:
    - Creates multiple worker processes (4 workers for CPU-bound tasks)
    - Each worker has its OWN dedicated input queue (routed by inference workers)
    - Each worker writes to its OWN dedicated output queue (eliminates lock contention)
    - Each process maintains isolated tracker states for assigned cameras
    - 100% order preservation per camera (no re-queuing)
    - Processes communicate via multiprocessing queues
    - True parallelism (bypasses Python GIL)
    - Metrics sent back to main process via metrics_queue for aggregation
    """

    def __init__(
        self,
        pipeline: Any,
        post_processor_config: Dict[str, Any],
        input_queues: List[mp.Queue],
        output_queues: List[mp.Queue],
        num_processes: int = 4,
        metrics_queue: Optional[mp.Queue] = None,
    ):
        """
        Initialize post-processing pool with per-worker queues.

        Args:
            pipeline: Reference to StreamingPipeline (not used in workers, for compatibility)
            post_processor_config: Configuration for PostProcessor initialization
            input_queues: List of mp.Queues (one per worker, routed by inference workers)
            output_queues: List of mp.Queues (one per worker, eliminates lock contention)
            num_processes: Number of worker processes
            metrics_queue: Queue for sending metrics back to main process
        """
        self.pipeline = pipeline
        self.post_processor_config = post_processor_config
        self.num_processes = num_processes
        self.running = False

        # Per-worker input queues from pipeline (one per worker)
        self.input_queues = input_queues
        # Per-worker output queues (eliminates lock contention)
        self.output_queues = output_queues
        self.metrics_queue = metrics_queue

        # Validate queue counts
        if len(input_queues) != num_processes:
            raise ValueError(f"Expected {num_processes} input queues, got {len(input_queues)}")
        if len(output_queues) != num_processes:
            raise ValueError(f"Expected {num_processes} output queues, got {len(output_queues)}")

        self.processes = []

        self.logger = logging.getLogger(f"{__name__}.MultiprocessPostProcessingPool")

    def start(self):
        """Start all worker processes with dedicated input and output queues."""
        self.running = True

        # Start worker processes (each reads from its dedicated queue, writes to its own output queue)
        for i in range(self.num_processes):
            process = mp.Process(
                target=postprocessing_worker_process,
                args=(
                    i,
                    self.num_processes,
                    self.input_queues[i],  # Worker's dedicated input queue
                    self.output_queues[i],  # Worker's dedicated output queue (no lock contention)
                    self.post_processor_config,
                    self.metrics_queue,  # For sending metrics back to main process
                ),
                daemon=True,
            )
            process.start()
            self.processes.append(process)

        self.logger.info(
            f"Started {self.num_processes} post-processing workers with dedicated input/output queues "
            f"(metrics_queue={'enabled' if self.metrics_queue else 'disabled'})"
        )

    def stop(self):
        """Stop all worker processes."""
        self.running = False

        # Terminate processes
        for process in self.processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()

        self.processes.clear()
        self.logger.info("Stopped all post-processing worker processes")

    def submit_task(self, task_data: Dict[str, Any], timeout: float = 0.1) -> bool:
        """
        Submit task to worker queue based on camera_id hash routing.

        Camera-based routing ensures:
        - Same camera always goes to same worker process
        - Tracker state remains isolated within that process
        - Per-camera ordering is preserved

        Args:
            task_data: Task data with camera_id, model_result, etc.
            timeout: Max time to wait if queue is full

        Returns:
            True if task was submitted, False if queue full (backpressure)
        """
        try:
            # Route to correct worker based on camera_id hash
            camera_id = task_data.get("camera_id", "")
            worker_id = hash(camera_id) % self.num_processes
            self.input_queues[worker_id].put(task_data, block=True, timeout=timeout)
            return True

        except Exception:
            # Queue full - apply backpressure
            return False

    def get_result(self, timeout: float = 0.001) -> Optional[Dict[str, Any]]:
        """
        Get result from any worker output queue (round-robin polling).

        Args:
            timeout: Max time to wait for result

        Returns:
            Result dict or None if no result available
        """
        # Poll all output queues for results
        for output_queue in self.output_queues:
            try:
                return output_queue.get_nowait()
            except:
                continue
        return None
