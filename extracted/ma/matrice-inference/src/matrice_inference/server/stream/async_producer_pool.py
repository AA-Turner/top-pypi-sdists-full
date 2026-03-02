"""
Shared async producer pool for high-throughput Redis publishing.

Architecture:
- Single asyncio event loop (runs in dedicated thread)
- Shared aioredis connection pool (connection reuse)
- Concurrent polling of all output queues
- Batched Redis pipelining (64 messages per round-trip)
- Fire-and-forget tasks for analytics/caching

Benefits over thread-per-producer:
- 75-90% thread reduction (from N threads to 1)
- Shared Redis connections (better resource utilization)
- Simplified architecture (single event loop)
- Memory savings (~30-50% reduction in per-producer overhead)

Flow:
    PostProc Worker 0 -> output_queue[0] --+
    PostProc Worker 1 -> output_queue[1] --+--> AsyncProducerPool --> Redis
    ...                                    |
    PostProc Worker N -> output_queue[N] --+
"""

import asyncio
import base64
import json
import logging
import multiprocessing as mp
import os
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

import redis.asyncio as aioredis

from matrice_inference.server.stream.utils import CameraConfig
from matrice_inference.server.stream.worker_metrics import WorkerMetrics

# ============================================================================
# CONFIGURATION
# ============================================================================
USE_SHM = os.getenv("USE_SHM", "false").lower() == "true"
SAVE_OVERLAYS_WITH_SHM = os.getenv("SAVE_OVERLAYS_WITH_SHM", "false").lower() == "true"

# Batching configuration
PIPELINE_BATCH_SIZE = 64  # Messages per Redis pipeline
STREAM_MAXLEN = 50_000  # Redis stream max length (approximate)

# Connection pool configuration
REDIS_MAX_CONNECTIONS = 50  # Shared connection pool size (increased from 20 for high throughput)

# Concurrent processing configuration
NUM_CONCURRENT_BATCHES = 16  # Max concurrent batch operations (increased from 8)
MAX_PENDING_TASKS = 128  # Max tasks waiting on semaphore (increased from 32 to prevent message drops)

# Pre-encoded field keys for performance
KEY_FRAME_ID = b"frame_id"
KEY_CAMERA_ID = b"camera_id"
KEY_MESSAGE_KEY = b"message_key"
KEY_DATA = b"data"
KEY_INPUT_STREAM = b"input_stream"


class AsyncProducerPool:
    """
    Shared async producer pool for high-throughput Redis publishing.

    Replaces the thread-per-producer model with a single shared async pool.
    Uses one event loop and a shared Redis connection pool for all output queues.

    Architecture:
    - Single dedicated thread running asyncio event loop
    - Shared aioredis connection pool (configurable max connections)
    - Concurrent polling of all output queues using asyncio.gather
    - Batched Redis pipelining (64 messages per round-trip)
    - Bounded concurrency for batch processing (prevents unbounded task explosion)

    Thread Safety:
    - All state is accessed only from the event loop thread
    - Queue polling uses run_in_executor for blocking mp.Queue operations
    - Stop signal via threading.Event for clean shutdown
    """

    DEFAULT_DB = 0

    def __init__(
        self,
        output_queues: List[mp.Queue],
        camera_configs: Dict[str, CameraConfig],
        stream_config: Dict[str, Any],
        analytics_publisher: Optional[Any] = None,
        frame_cache: Optional[Any] = None,
        app_deployment_id: Optional[str] = None,
        num_concurrent_batches: int = NUM_CONCURRENT_BATCHES,
        batch_size: int = PIPELINE_BATCH_SIZE,
        use_shared_metrics: bool = True,
    ):
        """
        Initialize async producer pool.

        Args:
            output_queues: List of mp.Queues from post-processing workers
            camera_configs: Camera configurations for stream routing
            stream_config: Redis/stream configuration
            analytics_publisher: Optional analytics publisher
            frame_cache: Optional frame cache for Redis storage
            app_deployment_id: App deployment ID for overlay keys
            num_concurrent_batches: Max concurrent batch operations
            batch_size: Target batch size for Redis pipelining
            use_shared_metrics: Whether to use shared metrics instance
        """
        self.output_queues = output_queues
        self.camera_configs = camera_configs
        self.stream_config = stream_config
        self.analytics_publisher = analytics_publisher
        self.frame_cache = frame_cache
        self.app_deployment_id = app_deployment_id
        self.num_concurrent_batches = num_concurrent_batches
        self.batch_size = batch_size

        self.running = False
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Redis connection (initialized in event loop)
        self._redis: Optional[aioredis.Redis] = None

        # Stream topic mapping: camera_id -> topic_name
        self._stream_topics: Dict[str, str] = {}
        for camera_id, config in camera_configs.items():
            self._stream_topics[camera_id] = config.output_topic

        # Metrics
        if use_shared_metrics:
            self.metrics = WorkerMetrics.get_shared("producer")
        else:
            self.metrics = WorkerMetrics(
                worker_id="async_producer_pool",
                worker_type="producer"
            )

        # Track analytics warning (only log once)
        self._analytics_warning_logged = False

        # Track Redis connection warning (only log once to prevent spam)
        self._redis_warning_logged = False

        # Dedicated executor for queue polling (avoids default executor shutdown issues)
        self._executor = ThreadPoolExecutor(
            max_workers=max(len(output_queues), 4),
            thread_name_prefix="producer_poll_"
        )

        self.logger = logging.getLogger(f"{__name__}.AsyncProducerPool")

        # Stuck queue detection - tracks consecutive failures to drain queues that have items
        # This detects multiprocessing.Queue pipe deadlock/corruption states
        self._stuck_queue_counts = [0] * len(output_queues)
        self._on_queue_stuck_callback = None  # Optional callback for worker restart

    def start(self) -> threading.Thread:
        """Start the async producer pool in a dedicated thread.

        Returns:
            Thread running the event loop
        """
        if self.running:
            self.logger.warning("AsyncProducerPool already running")
            return self._thread

        self.running = True
        self._stop_event.clear()
        self.metrics.mark_active()

        self._thread = threading.Thread(
            target=self._run_event_loop,
            name="AsyncProducerPool",
            daemon=True
        )
        self._thread.start()

        self.logger.info(
            f"Started AsyncProducerPool with {len(self.output_queues)} output queues "
            f"(batch_size={self.batch_size}, concurrent_batches={self.num_concurrent_batches})"
        )

        return self._thread

    def stop(self) -> None:
        """Stop the async producer pool gracefully."""
        if not self.running:
            return

        self.logger.info("Stopping AsyncProducerPool...")
        self.running = False
        self._stop_event.set()
        self.metrics.mark_inactive()

        # Shutdown executor immediately to prevent new submissions
        if self._executor:
            self._executor.shutdown(wait=False)
            self._executor = None

        # Stop event loop from the loop thread
        if self._event_loop and self._event_loop.is_running():
            self._event_loop.call_soon_threadsafe(self._event_loop.stop)

        # Wait for thread to finish
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=10.0)
            if self._thread.is_alive():
                self.logger.warning("AsyncProducerPool thread did not stop cleanly")

        self._thread = None
        self.logger.info("AsyncProducerPool stopped")

    def _run_event_loop(self) -> None:
        """Main event loop thread."""
        self._event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._event_loop)

        try:
            # Initialize Redis connection
            self._event_loop.run_until_complete(self._initialize_redis())

            # Run main processing loop
            self._event_loop.run_until_complete(self._main_loop())
        except Exception as e:
            self.logger.error(f"AsyncProducerPool error: {e}", exc_info=True)
        finally:
            # Cleanup
            self._event_loop.run_until_complete(self._cleanup())
            self._event_loop.close()
            self._event_loop = None

    async def _initialize_redis(self) -> None:
        """Initialize shared Redis connection pool.
        
        Supports lazy initialization: if stream_config doesn't have complete auth info,
        Redis initialization is skipped. Call update_stream_config() later when 
        camera configs with proper auth are available.
        """
        # Check stream type
        stream_type = self.stream_config.get("stream_type", "redis").lower()
        if stream_type != "redis":
            self.logger.info(f"Stream type is {stream_type}, Redis features disabled")
            return

        host = self.stream_config.get("host") or "localhost"
        port = self.stream_config.get("port") or 6379
        password = self.stream_config.get("password")
        username = self.stream_config.get("username")  # Redis 6.0+ ACL authentication
        db = self.stream_config.get("db", self.DEFAULT_DB)

        # Skip initialization ONLY if BOTH password and username are explicitly None
        # Empty string "" is valid (means no auth required), so only skip if None
        # This handles the case where no cameras exist at startup
        if password is None and username is None:
            self.logger.info(
                "Redis auth credentials not available in stream_config - "
                "Redis will be initialized when camera configs with auth are available"
            )
            return

        await self._create_redis_connection(host, port, password, username, db)

    async def _create_redis_connection(
        self, host: str, port: int, password: Optional[str], username: Optional[str], db: int
    ) -> bool:
        """Create Redis connection with the given parameters.
        
        Args:
            host: Redis host
            port: Redis port
            password: Redis password
            username: Redis username (for ACL auth)
            db: Redis database number
            
        Returns:
            True if connection successful, False otherwise
        """
        # Close existing connection if any
        if self._redis:
            try:
                await self._redis.close()
            except Exception as e:
                self.logger.warning(f"Error closing existing Redis connection: {e}")
            self._redis = None

        # Create connection pool for efficient connection reuse
        self._redis = aioredis.Redis(
            host=host,
            port=port,
            password=password,
            username=username,
            db=db,
            decode_responses=False,
            socket_keepalive=True,
            socket_timeout=30,
            health_check_interval=30,
            max_connections=REDIS_MAX_CONNECTIONS,
        )

        # Test connection
        try:
            if not password:
                self.logger.error("Test Redis connection pool with username WITHOUT PASSWORD: %s", username)
            else:
                self.logger.info("Test Redis connection pool with username with password: %s, password: %s", username, password[:4] + "...")
            await self._redis.ping()
            self.logger.info(
                f"Redis connection pool initialized: {host}:{port} "
                f"(max_connections={REDIS_MAX_CONNECTIONS}, username={username is not None})"
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            self._redis = None
            return False

    async def _reinitialize_redis(self) -> bool:
        """Reinitialize Redis connection with current stream_config.
        
        Called when stream_config is updated with new camera config credentials.
        
        Returns:
            True if reinitialization successful, False otherwise
        """
        stream_type = self.stream_config.get("stream_type", "redis").lower()
        if stream_type != "redis":
            self.logger.info(f"Stream type is {stream_type}, Redis reinitialization skipped")
            return False

        host = self.stream_config.get("host") or "localhost"
        port = self.stream_config.get("port") or 6379
        password = self.stream_config.get("password")
        username = self.stream_config.get("username")
        db = self.stream_config.get("db", self.DEFAULT_DB)

        self.logger.info(
            f"Reinitializing Redis connection with updated config: {host}:{port}"
        )

        return await self._create_redis_connection(host, port, password, username, db)

    async def _cleanup(self) -> None:
        """Cleanup Redis connection."""
        if self._redis:
            try:
                await self._redis.close()
            except Exception as e:
                self.logger.error(f"Error closing Redis connection: {e}")
            self._redis = None

    async def _main_loop(self) -> None:
        """Main processing loop with concurrent batch handling."""
        self.logger.info("Starting main processing loop")

        # Semaphore for bounded concurrent batch processing
        batch_semaphore = asyncio.Semaphore(self.num_concurrent_batches)
        pending_tasks: set = set()

        # Monitoring counters
        backpressure_count = 0
        last_log_time = time.time()
        total_processed = 0
        consecutive_empty_polls = 0

        while self.running and not self._stop_event.is_set():
            try:
                start_time = time.time()

                # BACKPRESSURE CONTROL: Skip polling if too many tasks pending
                # This prevents task explosion when downstream is slow
                if len(pending_tasks) >= MAX_PENDING_TASKS:
                    backpressure_count += 1
                    # Log warning on first backpressure hit and periodically
                    if backpressure_count == 1 or backpressure_count % 100 == 0:
                        self.logger.warning(
                            f"Producer backpressure active: pending_tasks={len(pending_tasks)} >= {MAX_PENDING_TASKS}. "
                            f"Messages may be delayed. Consider increasing MAX_PENDING_TASKS."
                        )
                    # Clean up done tasks first
                    done = {t for t in pending_tasks if t.done()}
                    for t in done:
                        if t.exception():
                            self.logger.error(f"Batch task failed: {t.exception()}")
                    pending_tasks -= done

                    # Still too many? Wait briefly
                    if len(pending_tasks) >= MAX_PENDING_TASKS:
                        await asyncio.sleep(0.001)
                        continue

                # Poll all queues concurrently
                tasks = await self._poll_all_queues()

                if not tasks:
                    consecutive_empty_polls += 1

                    # Track per-queue stuck state - detects pipe deadlock/corruption
                    for i, q in enumerate(self.output_queues):
                        try:
                            qsize = q.qsize()
                        except:
                            qsize = 0

                        if qsize > 10:  # Queue has items but we couldn't drain
                            self._stuck_queue_counts[i] += 1

                            # Log at different thresholds
                            if self._stuck_queue_counts[i] == 100:
                                self.logger.warning(
                                    f"[PRODUCER_DEBUG] Queue[{i}] stuck: has {qsize} items "
                                    f"but cannot drain (100 consecutive failures)"
                                )
                            elif self._stuck_queue_counts[i] == 1000:
                                self.logger.error(
                                    f"[PRODUCER_DEBUG] Queue[{i}] CRITICAL: {qsize} items "
                                    f"stuck for 1000 cycles! Worker may need restart."
                                )
                                # Trigger callback for worker restart if registered
                                if self._on_queue_stuck_callback:
                                    try:
                                        self._on_queue_stuck_callback(i)
                                    except Exception as cb_err:
                                        self.logger.error(f"Queue stuck callback failed: {cb_err}")
                            elif self._stuck_queue_counts[i] % 5000 == 0:
                                # Periodic reminder for severely stuck queues
                                self.logger.error(
                                    f"[PRODUCER_DEBUG] Queue[{i}] still stuck: {qsize} items "
                                    f"for {self._stuck_queue_counts[i]} cycles"
                                )
                        else:
                            # Queue is empty or draining - reset stuck count
                            self._stuck_queue_counts[i] = 0

                    # Log overall queue states at standard intervals
                    if consecutive_empty_polls == 100 or (consecutive_empty_polls > 100 and consecutive_empty_polls % 1000 == 0):
                        self.logger.warning(
                            f"[PRODUCER_DEBUG] {consecutive_empty_polls} consecutive empty polls, checking queue states..."
                        )
                        for i, q in enumerate(self.output_queues):
                            try:
                                qsize = q.qsize()
                            except:
                                qsize = -1
                            if qsize > 0:
                                self.logger.warning(
                                    f"  output_queue[{i}].qsize = {qsize} (HAS ITEMS BUT NOT DRAINING!)"
                                )
                            else:
                                self.logger.info(f"  output_queue[{i}].qsize = {qsize}")

                    # No tasks available, brief sleep
                    await asyncio.sleep(0.001)
                    continue

                # Reset counters when we successfully poll tasks
                consecutive_empty_polls = 0
                for i in range(len(self._stuck_queue_counts)):
                    self._stuck_queue_counts[i] = 0

                # Process batch with bounded concurrency
                async def bounded_process(batch: List[Dict[str, Any]]):
                    async with batch_semaphore:
                        await self._process_batch(batch)

                # Create batch task
                batch_task = asyncio.create_task(bounded_process(tasks))
                pending_tasks.add(batch_task)
                batch_task.add_done_callback(pending_tasks.discard)

                # Update counters
                total_processed += len(tasks)

                # Record metrics
                latency_ms = (time.time() - start_time) * 1000
                self.metrics.record_latency(latency_ms / max(len(tasks), 1))
                self.metrics.record_throughput(count=len(tasks))

                # Periodic logging for monitoring
                now = time.time()
                if now - last_log_time >= 10.0:  # Log every 10 seconds
                    self.logger.info(
                        f"Producer stats: processed={total_processed}, "
                        f"pending_tasks={len(pending_tasks)}, "
                        f"backpressure_events={backpressure_count}"
                    )
                    total_processed = 0
                    backpressure_count = 0
                    last_log_time = now

                # Cleanup completed tasks periodically
                if len(pending_tasks) > self.num_concurrent_batches * 2:
                    done = {t for t in pending_tasks if t.done()}
                    for t in done:
                        if t.exception():
                            self.logger.error(f"Batch task failed: {t.exception()}")
                    pending_tasks -= done

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Main loop error: {e}", exc_info=True)
                await asyncio.sleep(0.1)

        # Wait for pending tasks to complete
        if pending_tasks:
            self.logger.info(f"Waiting for {len(pending_tasks)} pending tasks...")
            await asyncio.gather(*pending_tasks, return_exceptions=True)

        self.logger.info("Main processing loop stopped")

    async def _poll_all_queues(self) -> List[Dict[str, Any]]:
        """Poll all output queues concurrently.

        Returns:
            Combined list of tasks from all queues
        """
        # Early exit if shutting down or executor is gone
        if not self.running or not self._executor:
            return []

        loop = asyncio.get_running_loop()

        # Calculate items per queue for fair distribution
        items_per_queue = max(1, self.batch_size // len(self.output_queues))

        # Create drain tasks for each queue
        async def drain_queue(q: mp.Queue, max_items: int, queue_idx: int) -> List[Dict[str, Any]]:
            """Drain up to max_items from a single queue."""
            # Check again before submitting to executor
            if not self.running or not self._executor:
                return []

            def _drain():
                items = []
                try:
                    for _ in range(max_items):
                        try:
                            # Use 10ms timeout for better reliability under system pressure
                            item = q.get(timeout=0.01)
                            if item is not None:
                                items.append(item)
                        except queue.Empty:
                            break

                    # FIX: Always retry with longer timeout when empty
                    # Don't trust qsize() - it can return 0 even when items exist in pipe buffer
                    # due to internal buffering in multiprocessing.Queue
                    if len(items) == 0:
                        try:
                            # Always attempt a longer-timeout get, even if qsize=0
                            # This catches items that are in the pipe buffer but not yet visible
                            item = q.get(timeout=0.05)  # 50ms - balance between latency and reliability
                            if item is not None:
                                items.append(item)
                                # Log success with qsize info (but don't spam logs)
                                try:
                                    qsize_after = q.qsize()
                                    if qsize_after > 0:
                                        self.logger.info(
                                            f"[PRODUCER_DEBUG] Queue[{queue_idx}] retry succeeded! "
                                            f"qsize_after={qsize_after}"
                                        )
                                except:
                                    pass
                        except queue.Empty:
                            # Check qsize AFTER the retry - only log if there's a significant backlog
                            try:
                                qsize_after = q.qsize()
                            except (NotImplementedError, OSError):
                                qsize_after = 0

                            if qsize_after > 50:
                                self.logger.error(
                                    f"[PRODUCER_DEBUG] Queue[{queue_idx}] CRITICAL: has {qsize_after} items "
                                    "but cannot drain! Queue may be corrupted."
                                )

                except Exception as e:
                    self.logger.error(f"[PRODUCER_DEBUG] Drain exception on queue[{queue_idx}]: {e}")

                return items

            try:
                return await loop.run_in_executor(self._executor, _drain)
            except RuntimeError:
                # Executor shut down, return empty
                return []

        # Poll all queues concurrently
        results = await asyncio.gather(
            *[drain_queue(q, items_per_queue, idx) for idx, q in enumerate(self.output_queues)]
        )

        # Flatten results
        all_items = [item for sublist in results for item in sublist]

        # [PRODUCER_DEBUG] Log poll results (only when items found to avoid log spam)
        if all_items:
            self.logger.debug(
                f"[PRODUCER_DEBUG] Polled {len(all_items)} items from {len(self.output_queues)} output queues"
            )

        return all_items

    async def _process_batch(self, tasks: List[Dict[str, Any]]) -> None:
        """Process a batch of tasks with Redis pipelining.

        Args:
            tasks: List of task data dicts to process
        """
        if not tasks:
            return

        batch_start = time.time()

        # [PRODUCER_DEBUG] Log batch processing start
        self.logger.info(
            f"[PRODUCER_DEBUG] Processing batch of {len(tasks)} tasks, "
            f"redis_connected={self._redis is not None}, "
            f"num_cameras={len(self.camera_configs)}"
        )

        # Pre-process all tasks (frame caching, overlay storage)
        prepared_messages = []
        skipped_no_camera_frame = 0
        skipped_invalid_camera = 0
        skipped_no_topic = 0
        skipped_build_failed = 0

        for task_data in tasks:
            try:
                camera_id = task_data.get("camera_id")
                frame_id = task_data.get("frame_id")

                if not camera_id or not frame_id:
                    skipped_no_camera_frame += 1
                    continue

                if not self._validate_camera(camera_id):
                    skipped_invalid_camera += 1
                    continue

                # Frame caching (non-blocking)
                if not USE_SHM:
                    await self._cache_frame_if_needed(task_data)

                # Overlay storage (conditional)
                if SAVE_OVERLAYS_WITH_SHM or not USE_SHM:
                    await self._store_overlay_results(task_data, camera_id, frame_id)

                # Get stream topic
                topic = self._stream_topics.get(camera_id)
                if not topic:
                    config = self.camera_configs.get(camera_id)
                    if config:
                        topic = config.output_topic
                        self._stream_topics[camera_id] = topic
                    else:
                        skipped_no_topic += 1
                        continue

                # Build message
                message = self._build_stream_message(task_data, camera_id, frame_id)
                if message:
                    prepared_messages.append((topic, message, task_data))
                else:
                    skipped_build_failed += 1

            except Exception as e:
                self.logger.error(f"Error preparing task: {e}")

        # [PRODUCER_DEBUG] Log prepared message summary
        total_skipped = skipped_no_camera_frame + skipped_invalid_camera + skipped_no_topic + skipped_build_failed
        self.logger.info(
            f"[PRODUCER_DEBUG] Prepared {len(prepared_messages)}/{len(tasks)} messages. "
            f"Skipped: no_camera_frame={skipped_no_camera_frame}, invalid_camera={skipped_invalid_camera}, "
            f"no_topic={skipped_no_topic}, build_failed={skipped_build_failed}"
        )

        if not prepared_messages:
            self.logger.warning(f"[PRODUCER_DEBUG] No messages prepared from {len(tasks)} tasks!")
            return

        prep_time = time.time() - batch_start

        # Send to Redis with pipelining
        redis_start = time.time()
        if self._redis:
            await self._send_batch_pipelined(prepared_messages)
        else:
            # Log warning periodically (not just once) to make issue visible
            self._redis_drop_count = getattr(self, '_redis_drop_count', 0) + len(prepared_messages)
            if self._redis_drop_count == len(prepared_messages) or self._redis_drop_count % 1000 == 0:
                self.logger.warning(
                    f"[PRODUCER_DEBUG] Redis not connected - dropped {self._redis_drop_count} total messages. "
                    "Check Redis credentials and connection status."
                )
        redis_time = time.time() - redis_start

        # Notify analytics publisher
        if self.analytics_publisher:
            for _, _, task_data in prepared_messages:
                try:
                    self.analytics_publisher.enqueue_analytics_data(task_data)
                except Exception:
                    pass

        # Log slow batches for diagnostics
        total_time = time.time() - batch_start
        if total_time > 0.1:  # Log if batch takes > 100ms
            self.logger.warning(
                f"Slow batch: {len(tasks)} tasks, total={total_time*1000:.1f}ms, "
                f"prep={prep_time*1000:.1f}ms, redis={redis_time*1000:.1f}ms"
            )

    async def _send_batch_pipelined(
        self, prepared_messages: List[tuple]
    ) -> None:
        """Send batch of messages using Redis pipeline.

        Args:
            prepared_messages: List of (topic, message, task_data) tuples
        """
        if not self._redis or not prepared_messages:
            return

        # Create pipeline (no transaction for performance)
        pipe = self._redis.pipeline(transaction=False)

        # Queue all XADD commands
        for topic, message, _ in prepared_messages:
            topic_bytes = topic.encode() if isinstance(topic, str) else topic
            pipe.xadd(
                topic_bytes,
                message,
                maxlen=STREAM_MAXLEN,
                approximate=True,
            )

        # Execute batch with timeout to prevent indefinite blocking
        try:
            results = await asyncio.wait_for(pipe.execute(), timeout=5.0)
            success_count = sum(1 for r in results if r is not None)
            # [PRODUCER_DEBUG] Log pipeline execution result
            self.logger.info(
                f"[PRODUCER_DEBUG] Pipeline executed: {success_count}/{len(prepared_messages)} succeeded"
            )
            if success_count < len(prepared_messages):
                self.logger.warning(
                    f"Pipeline partial success: {success_count}/{len(prepared_messages)}"
                )
        except asyncio.TimeoutError:
            self.logger.error(f"[PRODUCER_DEBUG] Redis pipeline timeout ({len(prepared_messages)} messages)")
        except aioredis.ConnectionError as e:
            self.logger.error(f"[PRODUCER_DEBUG] Redis connection error in pipeline: {e}")
        except Exception as e:
            self.logger.error(f"[PRODUCER_DEBUG] Pipeline execution error: {e}")

    def _build_stream_message(
        self, task_data: Dict[str, Any], camera_id: str, frame_id: str
    ) -> Optional[Dict[bytes, bytes]]:
        """Build message dict for Redis stream.

        Args:
            task_data: Task data containing results
            camera_id: Camera identifier
            frame_id: Frame identifier

        Returns:
            Dict with bytes keys/values for Redis, or None on error
        """
        try:
            message_to_send = {
                "frame_id": frame_id,
                "camera_id": camera_id,
                "message_key": task_data.get("message_key"),
                "input_stream": task_data.get("input_stream", {}),
                "data": task_data.get("data", {}),
            }

            # Serialize individual fields (NOT entire message)
            serialized_data = self._serialize_for_json(message_to_send.get("data", {}))
            serialized_input_stream = self._serialize_for_json(message_to_send.get("input_stream", {}))
            message_key = message_to_send.get("message_key", "")

            # Build Redis message with TOP-LEVEL fields (matching producer_worker.py pattern)
            return {
                KEY_FRAME_ID: frame_id.encode() if isinstance(frame_id, str) else frame_id,
                KEY_CAMERA_ID: camera_id.encode() if isinstance(camera_id, str) else camera_id,
                KEY_MESSAGE_KEY: message_key.encode() if isinstance(message_key, str) else message_key.encode() if message_key else b"",
                KEY_DATA: json.dumps(serialized_data).encode(),
                KEY_INPUT_STREAM: json.dumps(serialized_input_stream).encode(),
            }

        except Exception as e:
            self.logger.error(f"Error building stream message: {e}")
            return None

    def _validate_camera(self, camera_id: str) -> bool:
        """Validate camera is available and enabled."""
        if camera_id not in self.camera_configs:
            return False

        config = self.camera_configs[camera_id]
        return config.enabled

    async def _cache_frame_if_needed(self, task_data: Dict[str, Any]) -> None:
        """Cache frame to Redis asynchronously."""
        if not self.frame_cache:
            return

        try:
            frame_id = task_data.get("frame_id")
            if not frame_id or frame_id == "unknown":
                return

            input_stream = task_data.get("input_stream", {})
            if not isinstance(input_stream, dict):
                return

            content = input_stream.get("content")
            if not isinstance(content, bytes) or not content:
                return

            # Cache frame (put is non-blocking)
            self.frame_cache.put(frame_id, content)

        except Exception as e:
            self.logger.error(f"Frame cache error: {e}")

    async def _store_overlay_results(
        self, task_data: Dict[str, Any], camera_id: str, frame_id: str
    ) -> None:
        """Store overlay results to Redis."""
        if not self.frame_cache or not self.app_deployment_id:
            return

        try:
            data = task_data.get("data", {})
            if not data:
                return

            # Serialize data
            serializable_data = self._make_json_serializable(data)
            overlay_data = json.dumps(serializable_data).encode("utf-8")

            # Store overlay (put_overlay is non-blocking)
            self.frame_cache.put_overlay(
                frame_id,
                camera_id,
                self.app_deployment_id,
                overlay_data
            )

        except Exception as e:
            self.logger.error(f"Overlay storage error: {e}")

    def _serialize_for_json(self, obj: Any) -> Any:
        """Recursively serialize objects to JSON-safe types."""
        if obj is None:
            return None

        if isinstance(obj, (str, int, float, bool)):
            return obj

        if isinstance(obj, bytes):
            import base64
            return base64.b64encode(obj).decode("ascii")

        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return self._serialize_for_json(obj.to_dict())

        if hasattr(obj, "__dataclass_fields__"):
            from dataclasses import asdict
            return self._serialize_for_json(asdict(obj))

        if isinstance(obj, dict):
            return {k: self._serialize_for_json(v) for k, v in obj.items()}

        if isinstance(obj, (list, tuple)):
            return [self._serialize_for_json(item) for item in obj]

        try:
            return str(obj)
        except Exception:
            return None

    def _make_json_serializable(self, obj: Any) -> Any:
        """Convert non-JSON-serializable objects to serializable types."""
        if obj is None:
            return None

        if isinstance(obj, (str, int, float, bool)):
            return obj

        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode("ascii")

        # Handle Enum types
        if hasattr(obj, "value") and hasattr(obj, "name") and hasattr(obj.__class__, "__members__"):
            try:
                return obj.value
            except Exception:
                return str(obj)

        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            try:
                return self._make_json_serializable(obj.to_dict())
            except Exception:
                return str(obj)

        if hasattr(obj, "__dataclass_fields__"):
            try:
                from dataclasses import asdict
                return self._make_json_serializable(asdict(obj))
            except Exception:
                return str(obj)

        if isinstance(obj, dict):
            return {
                self._make_json_serializable(k): self._make_json_serializable(v)
                for k, v in obj.items()
            }

        if isinstance(obj, (list, tuple)):
            return [self._make_json_serializable(item) for item in obj]

        if hasattr(obj, "__dict__"):
            try:
                return self._make_json_serializable(vars(obj))
            except Exception:
                return str(obj)

        try:
            return str(obj)
        except Exception:
            return f"<non-serializable: {type(obj).__name__}>"

    def update_analytics_publisher(self, analytics_publisher: Any) -> None:
        """Update analytics publisher reference (for lazy initialization).

        Args:
            analytics_publisher: New analytics publisher instance
        """
        self.analytics_publisher = analytics_publisher
        self.logger.info("Updated analytics_publisher reference")

    def update_frame_cache(self, frame_cache: Any) -> None:
        """Update frame cache reference (for lazy initialization).

        Args:
            frame_cache: New frame cache instance
        """
        self.frame_cache = frame_cache
        self.logger.info("Updated frame_cache reference")

    def update_camera_configs(self, camera_configs: Dict[str, CameraConfig]) -> None:
        """Update camera configurations.

        Args:
            camera_configs: New camera configurations
        """
        self.camera_configs = camera_configs
        # Rebuild stream topic mapping
        self._stream_topics = {}
        for camera_id, config in camera_configs.items():
            self._stream_topics[camera_id] = config.output_topic
        self.logger.info(f"Updated camera_configs ({len(camera_configs)} cameras)")

    def update_stream_config(self, stream_config: Dict[str, Any]) -> bool:
        """Update stream configuration and reinitialize Redis connection.
        
        This method is thread-safe and can be called from any thread.
        It schedules the Redis reinitialization on the event loop.
        
        Used for lazy initialization when cameras are added after startup
        and provide proper Redis auth credentials.

        Args:
            stream_config: New stream configuration with Redis connection details
            
        Returns:
            True if update was scheduled successfully, False otherwise
        """
        # Check if stream config actually changed (avoid unnecessary reconnection)
        if (
            self.stream_config.get("host") == stream_config.get("host") and
            self.stream_config.get("port") == stream_config.get("port") and
            self.stream_config.get("password") == stream_config.get("password") and
            self.stream_config.get("username") == stream_config.get("username") and
            self.stream_config.get("db") == stream_config.get("db") and
            self._redis is not None  # Already connected
        ):
            self.logger.debug("Stream config unchanged and Redis already connected, skipping update")
            return True

        self.stream_config = stream_config
        self.logger.info(
            f"Updating stream_config: host={stream_config.get('host')}, "
            f"port={stream_config.get('port')}, "
            f"has_password={stream_config.get('password') is not None}, "
            f"has_username={stream_config.get('username') is not None}"
        )

        # Schedule Redis reinitialization on event loop if running
        if self._event_loop and self._event_loop.is_running():
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._reinitialize_redis(),
                    self._event_loop
                )
                # Wait for completion with timeout
                result = future.result(timeout=10.0)
                if result:
                    self.logger.info("✓ Redis connection reinitialized with updated stream_config")
                else:
                    self.logger.warning("✗ Redis reinitialization failed")
                return result
            except Exception as e:
                self.logger.error(f"Error scheduling Redis reinitialization: {e}")
                return False
        else:
            self.logger.info(
                "Event loop not running, stream_config updated - "
                "Redis will be initialized when event loop starts"
            )
            return True

    def get_metrics(self) -> Dict[str, Any]:
        """Get producer pool metrics.

        Returns:
            Dict with metrics summary
        """
        return {
            "running": self.running,
            "num_queues": len(self.output_queues),
            "num_cameras": len(self.camera_configs),
            "batch_size": self.batch_size,
            "concurrent_batches": self.num_concurrent_batches,
            "redis_connected": self._redis is not None,
            "metrics": self.metrics.to_summary_dict() if self.metrics else None,
            "stuck_queue_counts": list(self._stuck_queue_counts),
        }

    def set_queue_stuck_callback(self, callback) -> None:
        """Set callback to be invoked when a queue is detected as stuck.

        The callback receives the queue index as its argument.
        This can be used to trigger worker restart when queue pipe deadlock is detected.

        Args:
            callback: Function that takes queue_idx (int) as argument
        """
        self._on_queue_stuck_callback = callback
        self.logger.info("Queue stuck callback registered")

    def replace_queue(self, queue_idx: int, new_queue: mp.Queue) -> bool:
        """Replace a stuck queue with a new one.

        Called by post-processing pool when it restarts a worker.
        This allows recovery from multiprocessing.Queue pipe deadlock states.

        Args:
            queue_idx: Index of the queue to replace
            new_queue: New queue instance to use

        Returns:
            True if replacement successful, False otherwise
        """
        if queue_idx < 0 or queue_idx >= len(self.output_queues):
            self.logger.error(f"Invalid queue index {queue_idx} for replacement")
            return False

        try:
            old_queue = self.output_queues[queue_idx]
            self.output_queues[queue_idx] = new_queue
            self._stuck_queue_counts[queue_idx] = 0

            self.logger.info(
                f"[PRODUCER_DEBUG] Queue[{queue_idx}] replaced with new queue"
            )

            # Try to close old queue (may fail if corrupted)
            try:
                old_queue.close()
                old_queue.join_thread()
            except Exception as close_err:
                self.logger.warning(
                    f"Error closing old queue[{queue_idx}]: {close_err}"
                )

            return True

        except Exception as e:
            self.logger.error(f"Failed to replace queue[{queue_idx}]: {e}")
            return False
