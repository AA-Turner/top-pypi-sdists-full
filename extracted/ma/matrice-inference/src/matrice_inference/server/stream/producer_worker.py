import asyncio
import json
import logging
import queue
import threading
import time
import os
from typing import Any, Dict, List, Optional

import redis.asyncio as aioredis

from matrice_common.stream.matrice_stream import MatriceStream
from matrice_inference.server.stream.utils import CameraConfig

from matrice_inference.server.stream.worker_metrics import WorkerMetrics

# ============================================================================
# CONFIGURATION FLAGS
# ============================================================================
USE_SHM = os.getenv("USE_SHM", "false").lower() == "true"
SAVE_OVERLAYS_WITH_SHM = os.getenv("SAVE_OVERLAYS_WITH_SHM", "false").lower() == "true"

# Maximum concurrent stream sends per producer worker (legacy - kept for compatibility)
MAX_CONCURRENT_SENDS = 1000

# ============================================================================
# REDIS PIPELINING CONFIGURATION (from opt_prod.py)
# ============================================================================
# Batch size for pipeline operations - messages per Redis round-trip
PIPELINE_BATCH_SIZE = 64

# Maximum stream length (approximate) - old messages auto-trimmed
STREAM_MAXLEN = 50_000

# Pre-encoded field keys for performance (avoid encode() in hot path)
KEY_FRAME_ID = b"frame_id"
KEY_CAMERA_ID = b"camera_id"
KEY_MESSAGE_KEY = b"message_key"
KEY_DATA = b"data"
KEY_INPUT_STREAM = b"input_stream"


class ProducerWorker:
    """Handles message production to streams with per-camera queue handling.

    Supports sharded output queues (one per post-processing worker) to eliminate
    lock contention. Uses round-robin polling to read from all queues efficiently.
    """

    DEFAULT_DB = 0

    def __init__(
        self,
        worker_id: int,
        output_queues: List[Any],  # List of multiprocessing.Queues (one per postproc worker)
        pipeline: Any,
        camera_configs: Dict[str, CameraConfig],
        message_timeout: float,
        analytics_publisher: Optional[Any] = None,
        frame_cache: Optional[Any] = None,
        use_shared_metrics: Optional[bool] = True,
        app_deployment_id: Optional[str] = None,
    ):
        self.worker_id = worker_id
        self.output_queues = output_queues  # Dedicated mp.Queue (1:1 mapping with postproc worker)
        self.pipeline = pipeline
        self.camera_configs = camera_configs
        self.message_timeout = message_timeout
        self.analytics_publisher = analytics_publisher
        self.frame_cache = frame_cache
        self.app_deployment_id = app_deployment_id
        self.running = False
        self._analytics_warning_logged = False  # Only warn once about missing analytics_publisher
        self.producer_streams: Dict[str, MatriceStream] = {}
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
        # Semaphore for limiting concurrent stream sends (initialized in event loop)
        self._send_semaphore: Optional[asyncio.Semaphore] = None

        # Direct Redis client for pipelining (initialized in _run)
        self._redis: Optional[aioredis.Redis] = None
        # Stream topic mapping: camera_id -> topic_name
        self._stream_topics: Dict[str, str] = {}

        if use_shared_metrics:
            self.metrics = WorkerMetrics.get_shared("producer")
        else:
            self.metrics = WorkerMetrics(
                worker_id=f"producer_worker_{worker_id}",
                worker_type="producer"
            )

        self.logger = logging.getLogger(f"{__name__}.producer.{worker_id}")
    
    def start(self) -> threading.Thread:
        """Start the producer worker in a separate thread."""
        self.running = True
        self.metrics.mark_active()  # ADD
        thread = threading.Thread(
            target=self._run,
            name=f"ProducerWorker-{self.worker_id}",
            daemon=False
        )
        thread.start()
        return thread
    
    def stop(self):
        """Stop the producer worker."""
        self.running = False
        self.metrics.mark_inactive()  # ADD

    def remove_camera_stream(self, camera_id: str) -> bool:
        """Remove producer stream for a specific camera (thread-safe).

        This method can be called from any thread. It schedules the stream
        cleanup on the ProducerWorker's event loop using run_coroutine_threadsafe.

        Args:
            camera_id: ID of camera whose stream should be removed

        Returns:
            bool: True if successfully removed, False otherwise
        """
        try:
            if camera_id not in self.producer_streams:
                self.logger.warning(f"No producer stream found for camera {camera_id}")
                return False

            # Check if event loop is available
            if not self._event_loop or not self._event_loop.is_running():
                self.logger.warning(f"ProducerWorker event loop not available, cannot close stream for camera {camera_id}")
                # Still remove from dict to prevent memory leak
                if camera_id in self.producer_streams:
                    del self.producer_streams[camera_id]
                return False

            # Schedule the async close on the worker's event loop
            future = asyncio.run_coroutine_threadsafe(
                self._async_remove_camera_stream(camera_id),
                self._event_loop
            )

            # Wait for completion with timeout
            result = future.result(timeout=5.0)
            return result

        except Exception as e:
            self.logger.error(f"Error removing producer stream for camera {camera_id}: {e}")
            # Clean up dict entry even on error
            if camera_id in self.producer_streams:
                del self.producer_streams[camera_id]
            return False

    async def _async_remove_camera_stream(self, camera_id: str) -> bool:
        """Internal async method to close and remove a camera stream.

        Args:
            camera_id: ID of camera whose stream should be removed

        Returns:
            bool: True if successfully removed, False otherwise
        """
        try:
            if camera_id in self.producer_streams:
                stream = self.producer_streams[camera_id]
                await stream.async_close()
                del self.producer_streams[camera_id]
                self.logger.info(f"Removed producer stream for camera {camera_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error in async close for camera {camera_id}: {e}")
            # Clean up dict entry even on error
            if camera_id in self.producer_streams:
                del self.producer_streams[camera_id]
            return False

    def _run(self) -> None:
        """Main producer loop with proper resource management."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._event_loop = loop  # Store reference for cross-thread operations
        # Initialize semaphore for concurrent stream sends
        self._send_semaphore = asyncio.Semaphore(MAX_CONCURRENT_SENDS)

        self.logger.info(f"Started producer worker {self.worker_id} (pipelining enabled, batch_size={PIPELINE_BATCH_SIZE})")

        try:
            loop.run_until_complete(self._initialize_streams())
            loop.run_until_complete(self._initialize_direct_redis())
            self._process_messages(loop)
        except Exception as e:
            self.logger.error(f"Fatal error in producer worker: {e}")
        finally:
            self._cleanup_resources(loop)
            self._event_loop = None

    async def _initialize_direct_redis(self) -> None:
        """Initialize direct Redis client for pipelining.

        Uses connection details from the first camera's stream config.
        This client is used for high-throughput pipelined XADD operations.
        """
        # Get Redis connection details from first camera config
        if not self.camera_configs:
            self.logger.warning("No camera configs available for Redis initialization")
            return

        first_camera_config = next(iter(self.camera_configs.values()))
        stream_config = first_camera_config.stream_config

        # Only initialize for Redis streams (not Kafka)
        stream_type = stream_config.get("stream_type", "kafka").lower()
        if stream_type != "redis":
            self.logger.info("Stream type is not Redis, skipping direct Redis initialization")
            return

        host = stream_config.get("host") or "localhost"
        port = stream_config.get("port") or 6379
        password = stream_config.get("password")
        db = stream_config.get("db", self.DEFAULT_DB)

        self._redis = aioredis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=False,  # Keep bytes for performance
            socket_keepalive=True,
            socket_timeout=30,
            health_check_interval=30,
        )

        # Test connection
        try:
            await self._redis.ping()
            self.logger.info(f"Direct Redis connection established: {host}:{port}")
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis for pipelining: {e}")
            self._redis = None

        # Build stream topic mapping
        for camera_id, config in self.camera_configs.items():
            self._stream_topics[camera_id] = config.output_topic

    def _process_messages(self, loop: asyncio.AbstractEventLoop) -> None:
        """Main message processing loop (runs async tasks on event loop)."""
        loop.run_until_complete(self._async_process_messages())

    async def _async_process_messages(self) -> None:
        """Async message processing loop with Redis pipelining for maximum throughput.

        PIPELINING OPTIMIZATION (from opt_prod.py):
        - Collects up to PIPELINE_BATCH_SIZE tasks
        - Builds all messages first (frame caching, overlay storage)
        - Executes all XADD commands in single Redis pipeline (1 round-trip)
        - Falls back to individual sends if direct Redis not available
        """
        while self.running:
            try:
                start_time = time.time()

                # BATCH COLLECTION: Get multiple tasks from queue(s)
                tasks = await self._get_batch_from_queues(max_size=PIPELINE_BATCH_SIZE)

                if not tasks:
                    await asyncio.sleep(0.001)
                    continue

                # Use pipelined batch send if direct Redis is available
                if self._redis is not None:
                    await self._send_batch_pipelined(tasks)
                else:
                    # Fallback to individual sends (for Kafka or if Redis init failed)
                    await asyncio.gather(
                        *[self._send_message_safely(task) for task in tasks],
                        return_exceptions=True,
                    )

                # Record aggregate metrics for batch
                latency_ms = (time.time() - start_time) * 1000
                self.metrics.record_latency(latency_ms / len(tasks))  # Average per message
                self.metrics.record_throughput(count=len(tasks))

            except Exception as e:
                self.logger.error(f"Producer error: {e}")
                await asyncio.sleep(0.1)

    async def _send_batch_pipelined(self, tasks: List[Dict[str, Any]]) -> None:
        """Send batch of messages using Redis pipeline for maximum throughput.

        PIPELINING PATTERN (from opt_prod.py):
        - Pre-process all tasks (caching, overlays) before pipeline
        - Queue all XADD commands in pipeline (no round-trips)
        - Execute pipeline once (single round-trip for entire batch)
        - This reduces latency from N round-trips to 1 round-trip

        Args:
            tasks: List of task data dicts to send
        """
        # Pre-process all tasks (frame caching, overlay storage)
        prepared_messages = []

        # Local references for hot path
        stream_topics = self._stream_topics
        camera_configs = self.camera_configs
        use_shm = USE_SHM
        save_overlays = SAVE_OVERLAYS_WITH_SHM

        for task_data in tasks:
            try:
                camera_id = task_data.get("camera_id")
                frame_id = task_data.get("frame_id")

                if not camera_id or not frame_id:
                    continue

                if not self._validate_camera_availability(camera_id):
                    continue

                # Frame caching (non-blocking)
                if not use_shm:
                    await self._cache_frame_if_needed(task_data)

                # Overlay storage (conditional)
                if save_overlays or not use_shm:
                    await self._store_overlay_results(task_data, camera_id, frame_id)

                # Get stream topic (use local reference)
                topic = stream_topics.get(camera_id)
                if not topic:
                    # Camera added after startup - get from config
                    config = camera_configs.get(camera_id)
                    if config:
                        topic = config.output_topic
                        stream_topics[camera_id] = topic
                    else:
                        continue

                # Build message for Redis stream
                message = self._build_stream_message(task_data, camera_id, frame_id)
                if message:
                    prepared_messages.append((topic, message, task_data))

            except Exception as e:
                self.logger.error(f"Error preparing task: {e}")

        if not prepared_messages:
            return

        # Create pipeline - no transaction wrapper for performance
        pipe = self._redis.pipeline(transaction=False)

        # Queue all XADD commands
        for topic, message, _ in prepared_messages:
            topic_bytes = topic.encode() if isinstance(topic, str) else topic
            pipe.xadd(
                topic_bytes,
                message,
                maxlen=STREAM_MAXLEN,
                approximate=True,  # Faster than exact trim
            )

        # Execute entire batch in single round-trip
        try:
            results = await pipe.execute()
            # Log success count for monitoring
            success_count = sum(1 for r in results if r is not None)
            if success_count < len(prepared_messages):
                self.logger.warning(
                    f"Pipeline partial success: {success_count}/{len(prepared_messages)} messages sent"
                )
        except aioredis.ConnectionError as e:
            self.logger.error(f"Redis connection error in pipeline: {e}")
            # Connection error - messages lost, but don't crash
            return
        except Exception as e:
            self.logger.error(f"Pipeline execution error: {e}")
            return

        # Notify analytics publisher for all tasks (batch operation)
        if self.analytics_publisher:
            for _, _, task_data in prepared_messages:
                try:
                    self.analytics_publisher.enqueue_analytics_data(task_data)
                except Exception:
                    pass

    def _build_stream_message(self, task_data: Dict[str, Any], camera_id: str, frame_id: str) -> Optional[Dict[bytes, bytes]]:
        """Build message dict for Redis stream with pre-encoded keys.

        Args:
            task_data: Task data containing the results
            camera_id: Camera identifier
            frame_id: Frame identifier

        Returns:
            Dict with bytes keys/values for Redis stream, or None on error
        """
        try:
            # Build complete message structure
            message_to_send = {
                "frame_id": frame_id,
                "camera_id": camera_id,
                "message_key": task_data.get("message_key"),
                "input_stream": task_data.get("input_stream", {}),
                "data": task_data.get("data", {}),
            }

            # CRITICAL: Serialize all objects to JSON-safe types BEFORE json.dumps()
            # This handles Enums, dataclasses, bytes, custom objects, etc.
            serialized_message = self._serialize_for_json(message_to_send)

            # Serialize to JSON bytes
            message_json = json.dumps(serialized_message)

            # Return as bytes dict for Redis
            return {
                KEY_FRAME_ID: frame_id.encode() if isinstance(frame_id, str) else frame_id,
                KEY_CAMERA_ID: camera_id.encode() if isinstance(camera_id, str) else camera_id,
                KEY_DATA: message_json.encode(),
            }

        except Exception as e:
            self.logger.error(f"Error building stream message: {e}")
            return None

    async def _get_batch_from_queues(self, max_size: int = 64) -> List[Dict[str, Any]]:
        """Get a batch of tasks from output queues for batch processing.

        Phase 3 optimization: Uses single executor call to drain queue instead of
        multiple executor calls per message. This reduces ThreadPoolExecutor overhead.

        Args:
            max_size: Maximum number of tasks to collect

        Returns:
            List of task data dicts (may be empty if no tasks available)
        """
        loop = asyncio.get_running_loop()

        # First, get at least one task (with blocking wait)
        first_task = await self._get_task_from_queue()
        if not first_task:
            return []  # No tasks available

        # Drain remaining tasks in a SINGLE executor call to reduce overhead
        # This is much faster than multiple run_in_executor calls
        def drain_queue(q, remaining: int) -> List[Dict[str, Any]]:
            """Drain up to 'remaining' items from queue in one thread call."""
            items = []
            for _ in range(remaining):
                try:
                    items.append(q.get_nowait())
                except:
                    break
            return items

        # Get the queue this producer is assigned to (single queue per producer)
        q = self.output_queues[0]  # Each producer has dedicated queue now

        additional_tasks = await loop.run_in_executor(
            None,
            drain_queue,
            q,
            max_size - 1
        )

        return [first_task] + additional_tasks

    async def _get_task_from_queue(self) -> Optional[Dict[str, Any]]:
        """Get task from dedicated output queue (1:1 mapping with postproc worker).

        OPTIMIZED: Since each producer now has exactly one dedicated queue,
        we use direct blocking get instead of round-robin polling.
        This reduces CPU overhead and lambda creation.

        Returns:
            Task data or None if no tasks available
        """
        loop = asyncio.get_running_loop()

        # Direct blocking get from our single dedicated queue
        # 10ms timeout balances responsiveness vs CPU usage
        try:
            task_data = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: self.output_queues[0].get(timeout=0.01)
                ),
                timeout=0.02  # 20ms outer timeout
            )
            return task_data
        except (asyncio.TimeoutError, queue.Empty):
            return None
        except Exception:
            return None

    def _cleanup_resources(self, loop: asyncio.AbstractEventLoop) -> None:
        """Clean up streams, Redis connection, and event loop resources."""
        # Close direct Redis connection
        if self._redis is not None:
            try:
                loop.run_until_complete(self._redis.close())
                self._redis = None
            except Exception as e:
                self.logger.error(f"Error closing direct Redis connection: {e}")

        # Close MatriceStream connections
        for stream in self.producer_streams.values():
            try:
                loop.run_until_complete(stream.async_close())
            except Exception as e:
                self.logger.error(f"Error closing producer stream: {e}")

        try:
            loop.close()
        except Exception as e:
            self.logger.error(f"Error closing event loop: {e}")

        self.logger.info(f"Producer worker {self.worker_id} stopped")

    async def _initialize_streams(self) -> None:
        """Initialize producer streams for all cameras with proper error handling."""
        try:
            from matrice_common.stream.matrice_stream import MatriceStream, StreamType

            for camera_id, camera_config in self.camera_configs.items():
                try:
                    await self._initialize_camera_stream(camera_id, camera_config, StreamType)
                except Exception as e:
                    self.logger.error(f"Failed to initialize producer stream for camera {camera_id}: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"Failed to initialize producer streams: {e}")
            raise

    async def _initialize_camera_stream(
        self, camera_id: str, camera_config: CameraConfig, StreamType: Any
    ) -> None:
        """Initialize producer stream for a single camera."""
        from matrice_common.stream.matrice_stream import MatriceStream

        stream_type = self._get_stream_type(camera_config.stream_config, StreamType)
        stream_params = self._build_stream_params(camera_config.stream_config, stream_type, StreamType)

        producer_stream = MatriceStream(stream_type, **stream_params)
        await producer_stream.async_setup(camera_config.output_topic)
        self.producer_streams[camera_id] = producer_stream

        self.logger.info(
            f"Initialized {stream_type.value} producer stream for camera {camera_id} in worker {self.worker_id}"
        )

    def _get_stream_type(self, stream_config: Dict[str, Any], StreamType: Any) -> Any:
        """Determine stream type from configuration."""
        stream_type_str = stream_config.get("stream_type", "kafka").lower()
        return StreamType.KAFKA if stream_type_str == "kafka" else StreamType.REDIS

    def _build_stream_params(self, stream_config: Dict[str, Any], stream_type: Any, StreamType: Any) -> Dict[str, Any]:
        """Build stream parameters based on type."""
        if stream_type == StreamType.KAFKA:
            return {
                "bootstrap_servers": stream_config.get("bootstrap_servers", "localhost:9092"),
                "sasl_username": stream_config.get("sasl_username", os.environ.get("KAFKA_SASL_USERNAME")),
                "sasl_password": stream_config.get("sasl_password", os.environ.get("KAFKA_SASL_PASSWORD")),
                "sasl_mechanism": stream_config.get("sasl_mechanism", "SCRAM-SHA-256"),
                "security_protocol": stream_config.get("security_protocol", "SASL_PLAINTEXT"),
            }
        else:
            return {
                "host": stream_config.get("host") or "localhost",
                "port": stream_config.get("port") or 6379,
                "password": stream_config.get("password"),
                "username": stream_config.get("username"),
                "db": stream_config.get("db", self.DEFAULT_DB),
            }
    
    async def _send_message_safely(self, task_data: Dict[str, Any]) -> None:
        """Send message to the appropriate stream with validation and error handling.

        Also handles frame caching (moved from consumer to avoid blocking inference flow).
        """
        try:
            if not self._validate_task_data(task_data):
                return

            camera_id = task_data["camera_id"]
            frame_id = task_data.get("frame_id")

            # CRITICAL: Validate frame_id exists - skip if missing
            if not frame_id:
                self.logger.error(
                    f"[FRAME_ID_MISSING] camera={camera_id} - No frame_id in task_data. Skipping message."
                )
                return

            if not self._validate_camera_availability(camera_id):
                return

            # Log producer state for debugging
            self.logger.debug(
                f"[PRODUCER_PROCESSING] camera_id={camera_id}, frame_id={frame_id}, "
                f"has_frame_cache={self.frame_cache is not None}, "
                f"has_app_deployment_id={self.app_deployment_id is not None}, "
                f"app_deployment_id={self.app_deployment_id}"
            )

            # FIRE-AND-FORGET I/O - all operations scheduled as background tasks
            # This eliminates blocking and allows producer to process next frame immediately
            # Backpressure is handled via semaphore in stream sending

            # Frame caching - already fire-and-forget via frame_cache.put()
            if not USE_SHM:
                await self._cache_frame_if_needed(task_data)

            # Overlay storage - conditional based on SHM mode and flag
            # Skip overlays with SHM unless SAVE_OVERLAYS_WITH_SHM=true
            if SAVE_OVERLAYS_WITH_SHM or not USE_SHM:
                await self._store_overlay_results(task_data, camera_id, frame_id)

            # Stream sending - fire-and-forget with semaphore for backpressure
            # This is the key optimization: don't wait for Redis XADD to complete
            asyncio.create_task(self._send_message_with_semaphore(task_data, camera_id, frame_id))

        except Exception as e:
            self.logger.error(f"Error sending message: {e}", exc_info=True)

    async def _cache_frame_if_needed(self, task_data: Dict[str, Any]) -> None:
        """Cache frame to Redis asynchronously (moved from consumer).

        This caches the frame content to Redis for low-latency retrieval by clients.
        The frame_id is preserved throughout the pipeline for consistency.
        """
        frame_id = task_data.get("frame_id", "unknown")
        
        if not self.frame_cache:
            self.logger.debug(
                f"[FRAME_CACHE_SKIP] frame_id={frame_id} - frame_cache is None"
            )
            return

        try:
            if not frame_id or frame_id == "unknown":
                self.logger.warning(
                    f"[FRAME_CACHE_SKIP] No frame_id in task_data"
                )
                return

            # Get frame content from input_stream
            input_stream = task_data.get("input_stream", {})
            if not isinstance(input_stream, dict):
                self.logger.warning(
                    f"[FRAME_CACHE_SKIP] frame_id={frame_id} - input_stream is not a dict: {type(input_stream)}"
                )
                return

            content = input_stream.get("content")
            if not isinstance(content, bytes):
                self.logger.warning(
                    f"[FRAME_CACHE_SKIP] frame_id={frame_id} - content is not bytes: {type(content)}"
                )
                return
            
            if not content:
                self.logger.warning(
                    f"[FRAME_CACHE_SKIP] frame_id={frame_id} - content is empty"
                )
                return

            # Cache frame - put() is already non-blocking (uses internal queue)
            # No need for run_in_executor - put() just calls queue.put_nowait()
            self.frame_cache.put(frame_id, content)

            self.logger.debug(
                f"[FRAME_CACHE_OK] Cached frame: frame_id={frame_id}, size={len(content)} bytes"
            )

        except Exception as e:
            self.logger.error(f"[FRAME_CACHE_ERROR] frame_id={frame_id} - Failed to cache: {e}")

    def _make_json_serializable(self, obj: Any) -> Any:
        """Recursively convert non-JSON-serializable objects to serializable types.

        Handles:
        - Enum values (convert to string/value)
        - Objects with to_dict() method
        - Objects with __dict__ attribute
        - Dataclasses
        - bytes (convert to base64 string for JSON)
        - Custom objects (convert to string representation)
        """
        if obj is None:
            return None

        # Handle primitives
        if isinstance(obj, (str, int, float, bool)):
            return obj

        # Handle bytes - convert to base64 for JSON compatibility
        if isinstance(obj, bytes):
            import base64
            return base64.b64encode(obj).decode("ascii")

        # Handle Enum types (check before __dict__ since Enums have __dict__)
        if hasattr(obj, "value") and hasattr(obj, "name") and hasattr(obj, "__class__"):
            # Check if it's actually an Enum by checking if class has __members__
            if hasattr(obj.__class__, "__members__"):
                try:
                    return obj.value
                except Exception:
                    return str(obj)

        # Handle objects with to_dict() method
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            try:
                return self._make_json_serializable(obj.to_dict())
            except Exception:
                return str(obj)

        # Handle dataclasses
        if hasattr(obj, "__dataclass_fields__"):
            try:
                from dataclasses import asdict
                return self._make_json_serializable(asdict(obj))
            except Exception:
                return str(obj)

        # Handle dicts
        if isinstance(obj, dict):
            return {
                self._make_json_serializable(k): self._make_json_serializable(v)
                for k, v in obj.items()
            }

        # Handle lists/tuples
        if isinstance(obj, (list, tuple)):
            return [self._make_json_serializable(item) for item in obj]

        # Handle objects with __dict__ (custom classes)
        if hasattr(obj, "__dict__"):
            try:
                return self._make_json_serializable(vars(obj))
            except Exception:
                return str(obj)

        # Fallback: convert to string
        try:
            return str(obj)
        except Exception:
            return f"<non-serializable: {type(obj).__name__}>"

    async def _store_overlay_results(
        self, task_data: Dict[str, Any], camera_id: str, frame_id: str
    ) -> None:
        """Store overlay/results data to Redis with composite key for multiple app support.

        Key format: overlay:{frame_id}_{camera_id}_{app_deployment_id}
        This allows multiple apps to store their results for the same frame independently.

        Args:
            task_data: Task data containing the results
            camera_id: Camera identifier
            frame_id: Frame identifier
        """
        if not self.frame_cache:
            self.logger.debug(
                f"[OVERLAY_SKIP] frame_id={frame_id}, camera_id={camera_id} - frame_cache is None"
            )
            return

        if not self.app_deployment_id:
            self.logger.warning(
                f"[OVERLAY_SKIP] frame_id={frame_id}, camera_id={camera_id} - "
                f"app_deployment_id is None/empty"
            )
            return

        try:
            # Extract results data to store
            data = task_data.get("data", {})
            if not data:
                self.logger.warning(
                    f"[OVERLAY_SKIP] frame_id={frame_id}, camera_id={camera_id} - "
                    f"No data in task_data to store"
                )
                return

            # Convert data to JSON-serializable format (handles Enums, custom objects, etc.)
            serializable_data = self._make_json_serializable(data)

            # Serialize results to JSON bytes
            overlay_data = json.dumps(serializable_data).encode("utf-8")

            # Log the composite key that will be used
            composite_key = f"overlay:{frame_id}_{camera_id}_{self.app_deployment_id}"
            self.logger.debug(
                f"[OVERLAY_STORE] Storing overlay: key={composite_key}, "
                f"data_size={len(overlay_data)} bytes"
            )

            # Store overlay - put_overlay() is already non-blocking (uses internal queue)
            # No need for run_in_executor - put_overlay() just calls queue.put_nowait()
            success = self.frame_cache.put_overlay(
                frame_id,
                camera_id,
                self.app_deployment_id,
                overlay_data
            )

            if success:
                self.logger.debug(
                    f"[OVERLAY_OK] Stored overlay: key={composite_key}, "
                    f"data_size={len(overlay_data)} bytes"
                )
            else:
                self.logger.error(
                    f"[OVERLAY_FAIL] Failed to store overlay: key={composite_key}"
                )

        except Exception as e:
            self.logger.error(
                f"[OVERLAY_ERROR] frame_id={frame_id}, camera_id={camera_id}, "
                f"app_deployment_id={self.app_deployment_id}, error={e}",
                exc_info=True
            )

    def _validate_task_data(self, task_data: Dict[str, Any]) -> bool:
        """Validate that task data contains required fields."""
        required_fields = ["camera_id", "message_key", "data"]
        for field in required_fields:
            if field not in task_data:
                self.logger.error(f"Missing required field '{field}' in task data")
                return False
        return True

    def _validate_camera_availability(self, camera_id: str) -> bool:
        """Validate that camera and its stream are available."""
        if camera_id not in self.camera_configs:
            self.logger.warning(f"Camera {camera_id} not found in camera configs")
            return False

        camera_config = self.camera_configs[camera_id]
        if not camera_config.enabled:
            self.logger.debug(f"Camera {camera_id} is disabled, skipping message")
            return False

        # Stream will be created lazily if it doesn't exist yet
        if camera_id not in self.producer_streams:
            self.logger.info(f"Producer stream not found for camera {camera_id}, will be created on first send")

        return True

    def _serialize_for_json(self, obj: Any) -> Any:
        """Recursively serialize objects to JSON-safe types.

        Handles:
        - Objects with .to_dict() method (ProcessingResult, StreamMessage, etc.)
        - Dataclasses (CameraConfig, etc.)
        - Dicts and lists (recursive)
        - Primitive types (str, int, float, bool, None)
        - Bytes (keep as-is for Redis binary storage)
        """
        # Handle None
        if obj is None:
            return None

        # Handle primitives
        if isinstance(obj, (str, int, float, bool)):
            return obj

        # Handle bytes - convert to base64 for JSON serialization
        # (Redis binary storage is handled separately via DICT storage path)
        if isinstance(obj, bytes):
            import base64
            return base64.b64encode(obj).decode("ascii")

        # Handle objects with to_dict method
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return self._serialize_for_json(obj.to_dict())

        # Handle dataclasses
        if hasattr(obj, "__dataclass_fields__"):
            from dataclasses import asdict
            return self._serialize_for_json(asdict(obj))

        # Handle dicts
        if isinstance(obj, dict):
            return {k: self._serialize_for_json(v) for k, v in obj.items()}

        # Handle lists/tuples
        if isinstance(obj, (list, tuple)):
            return [self._serialize_for_json(item) for item in obj]

        # Fallback: convert to string
        try:
            return str(obj)
        except Exception:
            return None

    async def _send_message_with_semaphore(
        self, task_data: Dict[str, Any], camera_id: str, frame_id: str
    ) -> None:
        """Fire-and-forget stream send with semaphore for backpressure control.

        This method wraps _send_message_to_stream with semaphore acquisition to:
        1. Limit concurrent Redis XADD operations (prevents connection exhaustion)
        2. Provide backpressure when Redis is slow (semaphore blocks new sends)
        3. Allow producer to continue processing without waiting for Redis

        Args:
            task_data: Task data to send
            camera_id: Camera ID for routing
            frame_id: Frame ID for logging
        """
        try:
            # Acquire semaphore - blocks if too many concurrent sends
            async with self._send_semaphore:
                await self._send_message_to_stream(task_data, camera_id)
        except Exception as e:
            self.logger.error(
                f"[STREAM_SEND_ERROR] camera={camera_id}, frame={frame_id}: {e}"
            )

    async def _send_message_to_stream(self, task_data: Dict[str, Any], camera_id: str) -> None:
        """Send message to the stream for the specified camera with data validation."""
        # Create producer stream dynamically if it doesn't exist (for cameras added after startup)
        if camera_id not in self.producer_streams:
            camera_config = self.camera_configs[camera_id]
            try:
                from matrice_common.stream.matrice_stream import StreamType
                await self._initialize_camera_stream(camera_id, camera_config, StreamType)
                self.logger.info(f"Dynamically created producer stream for camera {camera_id}")
            except Exception as e:
                self.logger.error(f"Failed to create producer stream for camera {camera_id}: {e}")
                raise

        producer_stream = self.producer_streams[camera_id]
        camera_config = self.camera_configs[camera_id]

        # Build complete message structure for backend
        # Backend expects: {"frame_id": str, "camera_id": str, "input_stream": {...}, "data": {...}}
        # See be-inference-ws/internal/service/redis-service.go:455 - extracts frame_id at TOP LEVEL
        # NOTE: frame_id was already validated in _send_message_safely() - use task_data["frame_id"]
        message_to_send = {
            "frame_id": task_data["frame_id"],  # TOP LEVEL - forced, no fallback
            "camera_id": camera_id,
            "message_key": task_data.get("message_key"),
            "input_stream": task_data.get("input_stream", {}),
            "data": task_data.get("data", {}),
        }

        # Serialize all objects to JSON-safe types
        message_to_send = self._serialize_for_json(message_to_send)

        # Extract data field for validation logging
        data_to_send = message_to_send.get("data", {})
        
        # Validate post_processing_result structure
        if "post_processing_result" in data_to_send:
            post_proc_result = data_to_send["post_processing_result"]
            if isinstance(post_proc_result, dict):
                # Log successful post-processing with available data
                # PostProcessor can return different structures:
                # - agg_summary at top level (current format after flattening in post_processing_manager)
                # - data, predictions, summary (other use case results)
                # Check for agg_summary at top level (current) or nested in data field (legacy/fallback)
                agg_summary = None
                if "agg_summary" in post_proc_result:
                    # Current format: agg_summary at top level (flattened by post_processing_manager)
                    agg_summary = post_proc_result.get("agg_summary", {})
                elif "data" in post_proc_result and isinstance(post_proc_result.get("data"), dict):
                    # Legacy format: agg_summary nested in data field (kept for backward compatibility)
                    agg_summary = post_proc_result.get("data", {}).get("agg_summary")
                
                if agg_summary:
                    if isinstance(agg_summary, dict) and agg_summary:
                        frame_keys = list(agg_summary.keys())
                        self.logger.debug(
                            f"Sending message for camera={camera_id} with agg_summary containing {len(frame_keys)} frame(s): {frame_keys}"
                        )
                    else:
                        self.logger.debug(f"Message for camera={camera_id} has empty agg_summary")
                elif "data" in post_proc_result or "predictions" in post_proc_result:
                    # Modern post-processing result structure without agg_summary
                    self.logger.debug(
                        f"Sending message for camera={camera_id} with post_processing_result keys: {list(post_proc_result.keys())}"
                    )
                else:
                    # Unknown structure
                    self.logger.warning(
                        f"Message for camera={camera_id} missing 'agg_summary' in post_processing_result. "
                        f"Available keys: {list(post_proc_result.keys())}"
                    )
        else:
            self.logger.warning(
                f"Message for camera={camera_id} missing 'post_processing_result'. "
                f"Available keys: {list(data_to_send.keys())}"
            )

        # Send COMPLETE message structure to Redis as DICT (not JSON string)
        # Backend needs frame_id, camera_id, input_stream at top level as separate Redis fields
        # Redis will store each top-level key as a separate field in the stream
        # DO NOT json.dumps() - pass the dict directly so Redis stores fields at top level
        await producer_stream.async_add_message(
            camera_config.output_topic,
            message_to_send,  # Send as dict, NOT json string
            key=task_data["message_key"]
        )
        
        # Notify analytics publisher if available
        if self.analytics_publisher:
            try:
                # Log what we're sending to analytics for debugging
                data_to_send = task_data.get("data", {})
                post_proc = data_to_send.get("post_processing_result", {})
                agg_summary = post_proc.get("agg_summary")
                self.logger.debug(
                    f"[PRODUCER_TO_ANALYTICS] camera={camera_id} - "
                    f"Enqueueing analytics data. Has agg_summary: {agg_summary is not None}, "
                    f"agg_summary type: {type(agg_summary).__name__ if agg_summary else 'None'}"
                )
                self.analytics_publisher.enqueue_analytics_data(task_data)
            except Exception as e:
                self.logger.warning(
                    f"[PRODUCER_ANALYTICS_FAIL] camera={camera_id} - Failed to enqueue analytics data: {e}"
                )
        else:
            # Only warn once to avoid log spam - analytics_publisher may be lazily initialized later
            if not self._analytics_warning_logged:
                self.logger.warning(
                    f"[PRODUCER_NO_ANALYTICS] camera={camera_id} - "
                    "analytics_publisher is None, skipping analytics enqueue. "
                    "Will be updated when AnalyticsPublisher is lazily initialized."
                )
                self._analytics_warning_logged = True

