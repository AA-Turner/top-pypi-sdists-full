"""
Single async event loop consumer manager for 1000 cameras.

Architecture:
- Single async event loop handles all 1000 camera streams
- Async Redis operations (non-blocking) via direct redis.asyncio
- Direct frame bytes extraction and forwarding
- No codec-specific processing (simplified)
- No frame caching (moved to producer)
- Backpressure handling (drop frames if queue full)

Optimizations (matching optimized.py pattern):
- Direct redis.asyncio client (no MatriceStream abstraction)
- Single XREAD for ALL streams (not XREADGROUP with consumer groups)
- Pre-encoded byte keys for field access
- At-most-once delivery (drop under backpressure, no ACK)
- Lightweight FrameTask tuples instead of Dict[str, Any]
"""

import asyncio
import logging
import os
import queue
import time
from typing import Any, Dict, NamedTuple, Optional

import redis.asyncio as aioredis
from matrice_common.stream.shm_ring_buffer import ShmRingBuffer

from matrice_inference.server.stream.utils import CameraConfig
from matrice_inference.server.stream.worker_metrics import WorkerMetrics

USE_SHM = os.getenv("USE_SHM", "false").lower() == "true"
# ============================================================================
# PRE-ENCODED FIELD KEYS (avoid repeated string encoding at high FPS)
# ============================================================================
KEY_CAM_ID = b"cam_id"
KEY_CAMERA_ID = b"camera_id"
KEY_SHM_NAME = b"shm_name"
KEY_FRAME_IDX = b"frame_idx"
KEY_TS_NS = b"ts_ns"
KEY_WIDTH = b"width"
KEY_HEIGHT = b"height"
KEY_SHM_MODE = b"shm_mode"
KEY_FORMAT = b"format"
KEY_FRAME_ID = b"frame_id"
KEY_IS_SIMILAR = b"is_similar"
KEY_REFERENCE_FRAME_IDX = b"reference_frame_idx"
KEY_CONTENT = b"content"
KEY_INPUT_STREAM_CONTENT = b"input_stream__content"


class FrameTask(NamedTuple):
    """Lightweight frame task for minimal overhead message passing.

    Using NamedTuple instead of Dict[str, Any] reduces:
    - Memory allocation (no dict overhead)
    - Attribute access time (direct vs hash lookup)
    - Serialization cost (fixed structure)

    Supports both SHM mode (shm_name/frame_idx) and legacy mode (frame_bytes).
    """

    camera_id: str
    shm_name: bytes
    frame_idx: int
    width: int
    height: int
    ts_ns: int
    frame_format: str = "BGR"
    is_similar: bool = False
    reference_frame_idx: Optional[int] = None
    frame_bytes: Optional[bytes] = None  # For legacy (non-SHM) mode
    is_shm_mode: bool = True  # True for SHM mode, False for legacy mode
    frame_id: Optional[str] = None  # Frame ID from streaming message (legacy mode)
    cached_frame_id: Optional[str] = None  # Cached frame reference for similar frames


class AsyncConsumerManager:
    """
    Manages 1000 camera streams with single async event loop.

    HIGH-PERFORMANCE ARCHITECTURE (optimized.py pattern):
    - Direct redis.asyncio client (no MatriceStream abstraction)
    - Single XREAD call for ALL streams (not per-stream XREADGROUP)
    - Pre-encoded byte keys for field access
    - At-most-once delivery (drop under backpressure, no ACK)
    - asyncio.Queue with put_nowait() (no feeder threads)
    - Lightweight FrameTask tuples instead of Dict[str, Any]

    Key Features:
    - Single event loop for all cameras (not 1000 threads)
    - Non-blocking async stream reads
    - Backpressure handling (drop frames if queue full)
    - Dynamic camera add/remove support
    """

    # ================================================================
    # HIGH-PERFORMANCE CONFIGURATION (optimized from opt_cons_xread.py)
    # ================================================================
    BATCH_SIZE = 2000  # Messages to read per XREAD (2000 balances throughput vs latency)
    BLOCK_MS = 1000  # XREAD block time in ms (returns immediately on message, only waits when idle)
    QUEUE_MAX = 50_000  # Internal queue size (larger buffer for burst absorption)
    BACKPRESSURE_THRESHOLD = 0.9  # Skip frames when queue exceeds threshold
    FRAME_STALENESS_NS = 500_000_000  # 500ms in nanoseconds - skip frames older than this

    # Circuit breaker configuration for Redis failures
    # Prevents hammering Redis during outages with exponential backoff
    CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5  # Consecutive failures before opening circuit
    CIRCUIT_BREAKER_RESET_TIMEOUT = 30.0  # Seconds before trying again after circuit opens
    CIRCUIT_BREAKER_MIN_BACKOFF = 0.1  # Initial backoff in seconds
    CIRCUIT_BREAKER_MAX_BACKOFF = 5.0  # Maximum backoff in seconds

    # ================================================================
    # METRIC AGGREGATION
    # ================================================================
    # Problem: Per-frame metrics recording adds lock contention + overhead
    # At 10000 FPS, function calls dominate CPU time
    #
    # Solution: Aggregate metrics and flush periodically (every 1000 frames)
    # ================================================================
    METRICS_AGGREGATION_COUNT = 1000  # Aggregate N frames before recording

    def __init__(
        self,
        camera_configs: Dict[str, CameraConfig],
        stream_config: Dict[str, Any],
        app_deployment_id: str,
        pipeline: Any,
        message_timeout: float = 0.5,  # 500ms - must be well under SHM buffer lifetime
        # ================================================================
        # SHM_MODE: New parameters for shared memory architecture
        # ================================================================
        use_shm: bool = USE_SHM,  # Feature flag for SHM mode
        # ================================================================
        # FLOW CONTROL: Token-based backpressure (DISABLED - was causing 90%+ drops)
        # ================================================================
        enable_flow_control: bool = False,  # DISABLED - was dropping 90%+ frames
        max_in_flight_frames: int = 8000,  # Increased from 256 (was too aggressive)
        enable_drop_on_backpressure: bool = True,
    ):
        self.camera_configs = camera_configs
        self.stream_config = stream_config
        self.pipeline = pipeline
        self.message_timeout = message_timeout
        self.running = False

        # Initialize metrics (shared across all cameras)
        self.metrics = WorkerMetrics.get_shared("consumer")

        # Generate unique app instance identifier for consumer groups
        self.app_deployment_id = app_deployment_id

        self.logger = logging.getLogger(f"{__name__}.AsyncConsumerManager")

        # ================================================================
        # SHM_MODE: Shared memory configuration
        # ================================================================
        self.use_shm = use_shm

        # SHM buffers (attached on demand per camera)
        self._shm_buffers: Dict[str, ShmRingBuffer] = {}

        if use_shm:
            self.logger.info("SHM_MODE ENABLED: Will read frames from shared memory")

        # ================================================================
        # DIRECT REDIS.ASYNCIO CLIENT (no MatriceStream abstraction)
        # ================================================================
        # Single redis connection for ALL streams - much more efficient than
        # one MatriceStream per shard with consumer groups
        self._redis: Optional[aioredis.Redis] = None

        # Stream cursors: {stream_name_bytes: last_id_bytes}
        # Use "$" to start reading only new messages (like optimized.py)
        self._stream_cursors: Dict[bytes, bytes] = {}

        # Reverse mapping: stream_name -> camera_id for message routing
        self._stream_to_camera: Dict[str, str] = {}

        # ================================================================
        # ASYNCIO.QUEUE FOR DIRECT MESSAGE PASSING (no feeder threads)
        # ================================================================
        # Problem: feeder threads add context switch overhead and complexity
        # Solution: asyncio.Queue with put_nowait() for instant non-blocking enqueue
        # Workers read directly from asyncio.Queue in their event loop
        self._task_queue: Optional[asyncio.Queue] = None

        # ================================================================
        # CONSUMER TASK AND BRIDGE TASK
        # ================================================================
        # Single consumer task reads ALL streams with one XREAD call
        self._consumer_task: Optional[asyncio.Task] = None
        # Bridge task transfers from asyncio.Queue to mp.Queues for workers
        self._bridge_task: Optional[asyncio.Task] = None

        # ================================================================
        # FLOW CONTROL: Token-based backpressure (Phase 2 optimization)
        # ================================================================
        self.enable_flow_control = enable_flow_control
        self.max_in_flight_frames = max_in_flight_frames
        self.enable_drop_on_backpressure = enable_drop_on_backpressure
        self._flow_semaphore: Optional[asyncio.Semaphore] = None

        # ================================================================
        # METRIC AGGREGATION STATE
        # ================================================================
        self._metrics_frame_count = 0
        self._metrics_latency_sum_ns = 0
        self._metrics_max_latency_ns = 0
        self._metrics_last_flush = time.time()

    async def start(self):
        """Start optimized consumer using single XREAD for all streams.

        HIGH-PERFORMANCE ARCHITECTURE:
        - Single redis.asyncio connection for ALL streams
        - Single XREAD call reads from ALL streams at once
        - asyncio.Queue for direct message passing (no feeder threads)
        - At-most-once delivery (drop under backpressure, no ACK)
        """
        self.running = True
        self.metrics.mark_active()

        num_cameras = len(self.camera_configs)

        self.logger.info(
            f"Starting HIGH-PERFORMANCE async consumer manager for {num_cameras} cameras "
            f"using single XREAD (app_deployment_id={self.app_deployment_id})"
        )

        # Initialize direct redis.asyncio client
        await self._initialize_redis()

        # Build stream cursors for all cameras
        await self._initialize_stream_cursors()

        # Create asyncio.Queue for direct message passing
        self._task_queue = asyncio.Queue(maxsize=self.QUEUE_MAX)

        # Initialize flow control semaphore (Phase 2 optimization)
        if self.enable_flow_control:
            self._flow_semaphore = asyncio.Semaphore(self.max_in_flight_frames)
            self.logger.info(f"Flow control enabled: max_in_flight={self.max_in_flight_frames}")

        # Start single consumer task that reads ALL streams and routes DIRECTLY to mp.Queues
        # OPTIMIZATION: Removed bridge task - direct routing eliminates queue hop latency
        self._consumer_task = asyncio.create_task(
            self._consume_all_streams_direct(), name="consumer_all_streams_direct"
        )

        self.logger.info(
            f"Started high-performance consumer for {len(self._stream_cursors)} streams "
            f"(BATCH_SIZE={self.BATCH_SIZE}, BLOCK_MS={self.BLOCK_MS}, direct_routing=True)"
        )

    async def stop(self):
        """Stop consumer and clean up resources."""
        self.running = False
        self.metrics.mark_inactive()

        # Cancel main consumer task
        if self._consumer_task:
            self._consumer_task.cancel()
            try:
                await asyncio.wait_for(self._consumer_task, timeout=2.0)
            except (asyncio.CancelledError, asyncio.TimeoutError) as e:
                self.logger.warning(f"Consumer task cancellation timed out or failed: {e}")
            self._consumer_task = None

        # Note: Bridge task removed in optimization - direct routing to mp.Queues

        # Flush any pending aggregated metrics
        self._flush_aggregated_metrics()

        # Close redis connection
        if self._redis:
            try:
                await self._redis.close()
            except Exception as e:
                self.logger.error(f"Error closing redis connection: {e}")
            self._redis = None

        # Clear stream cursors
        self._stream_cursors.clear()
        self._stream_to_camera.clear()

        # ================================================================
        # SHM_MODE: Detach from SHM buffers (consumer does NOT unlink)
        # ================================================================
        if self.use_shm:
            for camera_id, shm_buffer in self._shm_buffers.items():
                try:
                    shm_buffer.close()  # Detach only (consumer doesn't unlink)
                    self.logger.debug(f"Detached from SHM buffer for camera {camera_id}")
                except Exception as e:
                    self.logger.warning(f"Error detaching from SHM {camera_id}: {e}")
            self._shm_buffers.clear()

        self.logger.info("Stopped async consumer manager")

    async def add_camera(self, camera_id: str, config: CameraConfig):
        """
        Add a new camera dynamically.

        The camera's stream will be added to the single XREAD on the next iteration.

        Args:
            camera_id: Unique camera identifier
            config: Camera configuration
        """
        if not config.enabled:
            self.logger.warning(f"Camera {camera_id} is disabled, skipping add")
            return

        stream_name = config.input_topic
        if stream_name in self._stream_to_camera:
            self.logger.warning(f"Stream {stream_name} already registered, skipping add")
            return

        try:
            # Store camera config
            self.camera_configs[camera_id] = config

            # Add to stream cursors (will be picked up by next XREAD)
            stream_name_bytes = stream_name.encode() if isinstance(stream_name, str) else stream_name
            self._stream_cursors[stream_name_bytes] = b"$"  # Read only new messages
            self._stream_to_camera[stream_name] = camera_id

            self.logger.info(f"Added camera {camera_id} -> stream {stream_name}")

        except Exception as e:
            self.logger.error(f"Failed to add camera {camera_id}: {e}")

    async def remove_camera(self, camera_id: str):
        """
        Remove a camera dynamically.

        The camera's stream will be removed from the XREAD on the next iteration.

        Args:
            camera_id: Unique camera identifier
        """
        try:
            # Get stream name from camera config
            config = self.camera_configs.pop(camera_id, None)
            if config:
                stream_name = config.input_topic
                stream_name_bytes = stream_name.encode() if isinstance(stream_name, str) else stream_name

                # Remove from stream cursors
                self._stream_cursors.pop(stream_name_bytes, None)
                self._stream_to_camera.pop(stream_name, None)

            # Detach from SHM buffer if present
            if camera_id in self._shm_buffers:
                try:
                    self._shm_buffers[camera_id].close()
                except Exception as e:
                    self.logger.error(f"Error closing SHM buffer for camera {camera_id}: {e}")
                del self._shm_buffers[camera_id]

            self.logger.info(f"Removed camera {camera_id} from consumer manager")

        except Exception as e:
            self.logger.error(f"Failed to remove camera {camera_id}: {e}")

    # ========================================================================
    # HIGH-PERFORMANCE REDIS INITIALIZATION
    # ========================================================================

    async def _initialize_redis(self) -> None:
        """Initialize direct redis.asyncio client.

        Single connection for ALL streams - much more efficient than
        MatriceStream abstraction with consumer groups.
        Supports Redis Sentinel for HA when sentinel_hosts/master_name are in stream_config.
        """
        from .utils import create_async_redis_client

        host = self.stream_config.get("host") or "localhost"
        port = self.stream_config.get("port") or 6379
        password = self.stream_config.get("password")
        db = self.stream_config.get("db", 0)
        sentinel_hosts = self.stream_config.get("sentinel_hosts")
        master_name = self.stream_config.get("master_name")

        self._redis = create_async_redis_client(
            host=host,
            port=port,
            password=password,
            db=db,
            sentinel_hosts=sentinel_hosts,
            master_name=master_name,
        )

        # Test connection
        try:
            await self._redis.ping()
            self.logger.info(
                f"Connected to Redis at {host}:{port}, db={db}, "
                f"sentinel={'yes' if sentinel_hosts else 'no'}, "
                f"password_present={password is not None and len(str(password)) > 0}"
            )
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def _initialize_stream_cursors(self) -> None:
        """Build stream cursors for all enabled cameras.

        Each camera's input_topic becomes a stream to read from.
        Use "$" to start reading only new messages (like optimized.py).
        """
        for camera_id, config in self.camera_configs.items():
            if not config.enabled:
                continue

            stream_name = config.input_topic
            stream_name_bytes = stream_name.encode() if isinstance(stream_name, str) else stream_name

            # Use "$" to read only new messages (no historical backlog)
            self._stream_cursors[stream_name_bytes] = b"$"
            self._stream_to_camera[stream_name] = camera_id

            # DEBUG: Verify stream exists by checking XLEN
            try:
                stream_len = await self._redis.xlen(stream_name)
                self.logger.warning(
                    f"[STREAM_DEBUG] Stream '{stream_name}' XLEN={stream_len} - "
                    f"stream {'EXISTS' if stream_len > 0 else 'EMPTY/NOT_FOUND'}"
                )
            except Exception as xlen_err:
                self.logger.error(f"[STREAM_DEBUG] XLEN failed for '{stream_name}': {xlen_err}")

        self.logger.info(f"Initialized {len(self._stream_cursors)} stream cursors for cameras")

    # ========================================================================
    # HIGH-PERFORMANCE SINGLE XREAD CONSUMER
    # ========================================================================

    def _parse_entry_to_frame_task(
        self,
        camera_id: str,
        fields: Dict[bytes, bytes],
        now_ns: int,
        first_frame: bool,
        stale_debug: bool,
    ) -> tuple:
        """Parse a single stream entry into a FrameTask (SHM or legacy).

        Returns a ``(frame_task, is_stale)`` tuple. ``frame_task`` is ``None`` when
        parsing failed; ``is_stale`` is ``True`` when a valid SHM frame was dropped
        for exceeding the staleness window. Behavior mirrors the previous inline
        block exactly (including debug logging gated on ``first_frame``).
        """
        # Fast field extraction using pre-encoded keys
        shm_mode = fields.get(KEY_SHM_MODE)

        # DEBUG: Log shm_mode
        if first_frame:
            self.logger.debug(f"[FRAME_DEBUG] shm_mode={shm_mode}, fields_keys={list(fields.keys())[:5]}")

        if shm_mode in (b"1", b"true", b"True"):
            # SHM mode: extract metadata for worker to read from SHM
            frame_task = self._parse_shm_message(camera_id, fields, now_ns)

            # REDIS-LEVEL SKIP: Check if frame is too old before queueing
            # This saves CPU by avoiding inference queue hop for stale frames
            # OPTIMIZATION: Time-based staleness (more accurate than frame-count)
            if frame_task is not None:
                # Time-based staleness check - more accurate than frame-count
                frame_age_ns = now_ns - frame_task.ts_ns
                if frame_age_ns > self.FRAME_STALENESS_NS:
                    if stale_debug:
                        self.logger.debug(
                            f"[FRAME_DEBUG] Frame STALE: age={frame_age_ns / 1e6:.1f}ms > {self.FRAME_STALENESS_NS / 1e6:.1f}ms"
                        )
                    return None, True  # Skip stale frame at Redis level
            else:
                if first_frame:
                    self.logger.debug("[FRAME_DEBUG] SHM frame_task is None after _parse_shm_message")
        else:
            # Legacy mode: parse embedded frame bytes
            frame_task = self._parse_legacy_message(camera_id, fields, now_ns)
            if frame_task is None and first_frame:
                self.logger.debug("[FRAME_DEBUG] Legacy frame_task is None after _parse_legacy_message")

        return frame_task, False

    async def _handle_redis_connection_error(
        self,
        e: Exception,
        consecutive_failures: int,
        circuit_open: bool,
        circuit_open_time: float,
        current_backoff: float,
    ) -> tuple:
        """Apply circuit-breaker + exponential backoff for a Redis connection error.

        Returns the updated ``(consecutive_failures, circuit_open, circuit_open_time,
        current_backoff, should_continue)``. ``should_continue`` is ``True`` when the
        caller must skip to the next loop iteration (half-open wait). Behavior mirrors
        the previous inline handler exactly.
        """
        consecutive_failures += 1

        if consecutive_failures >= self.CIRCUIT_BREAKER_FAILURE_THRESHOLD and not circuit_open:
            circuit_open = True
            circuit_open_time = time.time()
            self.logger.error(
                f"Circuit breaker OPEN after {consecutive_failures} failures, "
                f"will retry in {self.CIRCUIT_BREAKER_RESET_TIMEOUT}s"
            )

        if circuit_open:
            # Check if circuit should try to close (half-open state)
            if time.time() - circuit_open_time > self.CIRCUIT_BREAKER_RESET_TIMEOUT:
                self.logger.info("Circuit breaker attempting reconnection (half-open)")
                circuit_open = False
                consecutive_failures = self.CIRCUIT_BREAKER_FAILURE_THRESHOLD - 1
            else:
                await asyncio.sleep(self.CIRCUIT_BREAKER_RESET_TIMEOUT / 10)
                return consecutive_failures, circuit_open, circuit_open_time, current_backoff, True

        self.logger.warning(
            f"Redis connection error ({consecutive_failures}x): {e}, backoff={current_backoff:.2f}s"
        )
        await asyncio.sleep(current_backoff)
        # Exponential backoff with cap
        current_backoff = min(current_backoff * 2, self.CIRCUIT_BREAKER_MAX_BACKOFF)
        return consecutive_failures, circuit_open, circuit_open_time, current_backoff, False

    async def _consume_all_streams_direct(self) -> None:
        """Consume ALL streams and route DIRECTLY to mp.Queues (no bridge task).

        DIRECT ROUTING OPTIMIZATION (from opt_cons_xread.py):
        - Single XREAD reads from ALL camera streams at once
        - NO consumer groups, NO XACK (at-most-once delivery)
        - Routes directly to inference worker mp.Queues (no asyncio.Queue hop)
        - Eliminates bridge task latency overhead
        - Result: 15,000+ FPS throughput

        Flow:
            XREAD → parse message → hash(camera_id) % num_workers → mp.Queue
        """
        self.logger.info(f"Starting DIRECT routing consumer for {len(self._stream_cursors)} streams")

        # Get inference queues directly from pipeline
        inference_queues = self.pipeline.inference_queues
        if not inference_queues:
            self.logger.error("No inference queues available, consumer stopping")
            return

        num_workers = len(inference_queues)

        # Local references for speed (avoid attribute lookup in hot loop)
        redis_client = self._redis
        xread = redis_client.xread
        stream_cursors = self._stream_cursors
        stream_to_camera = self._stream_to_camera
        time_ns = time.time_ns
        batch_size = self.BATCH_SIZE
        block_ms = self.BLOCK_MS

        # Pre-compute camera_id -> worker_id mapping for faster routing
        # This avoids hash() calls in the hot loop for known cameras
        camera_to_worker: Dict[str, int] = {}
        for camera_id in self.camera_configs:
            camera_to_worker[camera_id] = hash(camera_id) % num_workers

        # Local reference to metrics for hot path (avoid self.metrics lookup)
        metrics = self.metrics
        record_aggregated = self._record_aggregated_metrics_ns

        frames_processed = 0
        frames_dropped = 0
        frames_stale_skipped = 0  # Stale frames skipped at Redis level
        last_log_time = time.time()

        # Adaptive backpressure: skip XREAD when downstream queues are saturated
        # This prevents wasted CPU on frames that will be dropped anyway
        # NOTE: mp.Queue doesn't expose maxsize as public attribute, use pipeline's configured value
        queue_maxsize = getattr(self.pipeline, "inference_queue_maxsize", 5000)
        max_queue_capacity = num_workers * queue_maxsize
        backpressure_threshold = int(max_queue_capacity * 0.8)
        backpressure_skipped = 0

        # Circuit breaker state for Redis failures
        consecutive_failures = 0
        circuit_open = False
        circuit_open_time = 0.0
        current_backoff = self.CIRCUIT_BREAKER_MIN_BACKOFF

        self.logger.info(
            f"Direct routing to {num_workers} inference workers "
            f"(BATCH_SIZE={batch_size}, BLOCK_MS={block_ms}, backpressure_threshold={backpressure_threshold})"
        )

        while self.running:
            try:
                # ADAPTIVE BACKPRESSURE: Check downstream queue fill level
                # Skip XREAD cycle when queues are >80% full to prevent wasted work
                total_queued = sum(q.qsize() for q in inference_queues)
                if total_queued > backpressure_threshold:
                    backpressure_skipped += 1
                    # Log periodically
                    if backpressure_skipped % 10000 == 0:
                        self.logger.warning(
                            f"Backpressure active: {total_queued}/{max_queue_capacity} queued, "
                            f"skipped {backpressure_skipped} XREAD cycles"
                        )
                    await asyncio.sleep(0.0005)  # 0.5ms micro-sleep
                    continue

                # SINGLE XREAD for ALL streams at once
                # Startup diagnostic (DEBUG only): log the XREAD attempt while no
                # frames have been processed yet. The per-iteration XLEN probes
                # that used to run here were removed (extra Redis load in the hot
                # path); XLEN can be checked out-of-band when debugging.
                if (
                    self.logger.isEnabledFor(logging.DEBUG)
                    and frames_processed == 0
                    and frames_dropped == 0
                    and (time.time() - last_log_time) > 5.0
                ):
                    stream_names = [k.decode() if isinstance(k, bytes) else k for k in stream_cursors.keys()]
                    self.logger.debug(
                        f"[XREAD_DEBUG] Attempting XREAD: streams={stream_names}, "
                        f"cursor_count={len(stream_cursors)}, batch_size={batch_size}, block_ms={block_ms}"
                    )

                try:
                    messages = await xread(
                        streams=stream_cursors,
                        count=batch_size,
                        block=block_ms,
                    )
                except Exception as xread_error:
                    self.logger.error(f"[XREAD_DEBUG] XREAD failed: {type(xread_error).__name__}: {xread_error}")
                    await asyncio.sleep(0.1)
                    continue

                if not messages:
                    # DEBUG: Log empty XREAD periodically when no frames processed
                    if frames_processed == 0 and (time.time() - last_log_time) > 10.0:
                        self.logger.debug(f"[XREAD_DEBUG] XREAD returned empty, streams={len(stream_cursors)}")
                        last_log_time = time.time()
                    continue

                now_ns = time_ns()

                for stream_name_bytes, entries in messages:
                    # Update stream cursor to last message ID
                    stream_cursors[stream_name_bytes] = entries[-1][0]

                    # DEBUG: Log entries received
                    if frames_processed == 0:
                        self.logger.debug(f"[FRAME_DEBUG] Got {len(entries)} entries from stream {stream_name_bytes}")

                    # Decode stream name for camera lookup
                    stream_name = (
                        stream_name_bytes.decode() if isinstance(stream_name_bytes, bytes) else stream_name_bytes
                    )
                    camera_id = stream_to_camera.get(stream_name)

                    if not camera_id:
                        if frames_processed == 0:
                            self.logger.debug(
                                f"[FRAME_DEBUG] camera_id NOT FOUND for stream '{stream_name}', available={list(stream_to_camera.keys())}"
                            )
                        continue

                    for msg_id, fields in entries:
                        # Fast field extraction using pre-encoded keys
                        frame_task, is_stale = self._parse_entry_to_frame_task(
                            camera_id,
                            fields,
                            now_ns,
                            first_frame=(frames_processed == 0),
                            stale_debug=(frames_processed == 0 and frames_stale_skipped < 5),
                        )

                        if is_stale:
                            frames_stale_skipped += 1
                            continue  # Skip stale frame at Redis level

                        if frame_task is None:
                            continue

                        # DIRECT ROUTING to inference worker queue
                        # Pre-computed mapping ensures same camera always goes to same worker
                        task_data = self._frame_task_to_dict(frame_task)
                        # Use cached worker_id or compute for new cameras
                        worker_id = camera_to_worker.get(camera_id)
                        if worker_id is None:
                            worker_id = hash(camera_id) % num_workers
                            camera_to_worker[camera_id] = worker_id
                        target_queue = inference_queues[worker_id]

                        # Non-blocking put to mp.Queue
                        try:
                            target_queue.put_nowait(task_data)
                            frames_processed += 1

                            # Record latency metrics (using local reference)
                            latency_ns = now_ns - frame_task.ts_ns
                            record_aggregated(latency_ns)

                        except queue.Full:
                            # Queue full - drop frame (expected backpressure)
                            frames_dropped += 1
                            if metrics:
                                metrics.record_drop(count=1, reason="backpressure")
                        except Exception as e:
                            # Unexpected error - log and continue
                            self.logger.warning(f"Error putting to queue: {e}")
                            frames_dropped += 1

                # Periodic logging (every 30 seconds)
                now = time.time()
                if now - last_log_time > 30.0:
                    self.logger.info(
                        f"Consumer (direct): {frames_processed} processed, "
                        f"{frames_dropped} dropped, {frames_stale_skipped} stale_skipped"
                    )
                    last_log_time = now

                # Reset circuit breaker on successful iteration
                if consecutive_failures > 0:
                    self.logger.info(f"Redis connection recovered after {consecutive_failures} failures")
                    consecutive_failures = 0
                    circuit_open = False
                    current_backoff = self.CIRCUIT_BREAKER_MIN_BACKOFF

            except asyncio.CancelledError:
                raise
            except (aioredis.ConnectionError, aioredis.TimeoutError) as e:
                # Circuit breaker with exponential backoff for Redis failures
                (
                    consecutive_failures,
                    circuit_open,
                    circuit_open_time,
                    current_backoff,
                    _cb_continue,
                ) = await self._handle_redis_connection_error(
                    e,
                    consecutive_failures,
                    circuit_open,
                    circuit_open_time,
                    current_backoff,
                )
                if _cb_continue:
                    continue

            except Exception as e:
                self.logger.error(f"Consumer error: {e}")
                await asyncio.sleep(0.1)

        self.logger.info(
            f"Consumer stopped: {frames_processed} processed, {frames_dropped} dropped, "
            f"{frames_stale_skipped} stale_skipped"
        )

    def _route_messages_to_task_queue(
        self, messages, stream_cursors, stream_to_camera, task_queue, now_ns: int
    ) -> tuple:
        """Route XREAD results into the internal asyncio task queue (legacy path).

        Updates stream cursors, parses each entry (SHM or legacy), and enqueues
        with backpressure drop. Returns ``(frames_processed, frames_dropped)``.
        Behavior mirrors the previous inline nested loop exactly.
        """
        frames_processed = 0
        frames_dropped = 0

        for stream_name_bytes, entries in messages:
            # Update stream cursor to last message ID
            stream_cursors[stream_name_bytes] = entries[-1][0]

            # Decode stream name for camera lookup
            stream_name = stream_name_bytes.decode() if isinstance(stream_name_bytes, bytes) else stream_name_bytes
            camera_id = stream_to_camera.get(stream_name)

            if not camera_id:
                continue

            for msg_id, fields in entries:
                # Fast field extraction using pre-encoded keys
                shm_mode = fields.get(KEY_SHM_MODE)

                if shm_mode in (b"1", b"true", b"True"):
                    # SHM mode: extract metadata for worker to read from SHM
                    frame_task = self._parse_shm_message(camera_id, fields, now_ns)
                else:
                    # Legacy mode: parse embedded frame bytes
                    frame_task = self._parse_legacy_message(camera_id, fields, now_ns)

                if frame_task is None:
                    continue

                # Non-blocking enqueue with backpressure drop
                try:
                    task_queue.put_nowait(frame_task)
                    frames_processed += 1
                except asyncio.QueueFull:
                    frames_dropped += 1

        return frames_processed, frames_dropped

    async def _consume_all_streams(self) -> None:
        """LEGACY: Consume ALL streams with single XREAD call.

        NOTE: This method is kept for backwards compatibility.
        Use _consume_all_streams_direct() for direct routing optimization.

        HIGH-THROUGHPUT DESIGN:
        - Single XREAD reads from ALL camera streams at once
        - NO consumer groups, NO XACK (at-most-once delivery)
        - Pre-encoded byte keys for field access
        - put_nowait() with backpressure drop
        - Lightweight FrameTask tuples
        - Result: 10,000+ FPS throughput
        """
        self.logger.info(f"Starting single XREAD consumer for {len(self._stream_cursors)} streams")

        # Local references for speed (avoid attribute lookup in hot loop)
        redis_client = self._redis
        xread = redis_client.xread
        stream_cursors = self._stream_cursors
        stream_to_camera = self._stream_to_camera
        task_queue = self._task_queue
        time_ns = time.time_ns
        batch_size = self.BATCH_SIZE
        block_ms = self.BLOCK_MS

        frames_processed = 0
        frames_dropped = 0
        frames_backpressure_skipped = 0
        last_log_time = time.time()

        # Backpressure threshold: skip XREAD when queue exceeds threshold
        # This saves CPU by avoiding SHM parsing + routing work when downstream is saturated
        backpressure_threshold = int(self.QUEUE_MAX * self.BACKPRESSURE_THRESHOLD)

        while self.running:
            try:
                # EARLY BACKPRESSURE CHECK: Skip work when downstream is saturated
                # This saves CPU by avoiding XREAD + SHM parsing when queue is nearly full
                current_queue_size = task_queue.qsize()
                if current_queue_size > backpressure_threshold:
                    frames_backpressure_skipped += 1
                    await asyncio.sleep(0.001)  # Brief backoff (1ms)
                    continue

                # SINGLE XREAD for ALL streams at once
                messages = await xread(
                    streams=stream_cursors,
                    count=batch_size,
                    block=block_ms,
                )

                if not messages:
                    continue

                now_ns = time_ns()

                processed_delta, dropped_delta = self._route_messages_to_task_queue(
                    messages, stream_cursors, stream_to_camera, task_queue, now_ns
                )
                frames_processed += processed_delta
                frames_dropped += dropped_delta

                # Periodic logging (every 30 seconds)
                now = time.time()
                if now - last_log_time > 30.0:
                    self.logger.info(
                        f"Consumer: {frames_processed} processed, "
                        f"{frames_dropped} dropped, {frames_backpressure_skipped} backpressure_skipped, "
                        f"queue_size={task_queue.qsize()}"
                    )
                    last_log_time = now

            except asyncio.CancelledError:
                raise
            except (aioredis.ConnectionError, aioredis.TimeoutError) as e:
                self.logger.warning(f"Redis connection error: {e}, reconnecting...")
                await asyncio.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Consumer error: {e}")
                await asyncio.sleep(0.1)

        self.logger.info(f"Consumer stopped: {frames_processed} processed, {frames_dropped} dropped")

    async def _drain_task_batch(self, task_queue, batch_size: int):
        """Drain up to ``batch_size`` frames from the internal asyncio task queue.

        Waits (10ms) for the first frame, then non-blocking-drains the rest. Returns
        ``None`` when the initial wait times out (caller loops for shutdown check),
        otherwise a list (possibly empty). Behavior mirrors the previous inline block.
        """
        batch = []

        # First, wait for at least one frame (with timeout for shutdown check)
        try:
            frame_task = await asyncio.wait_for(
                task_queue.get(),
                timeout=0.01,  # 10ms timeout for responsiveness
            )
            if frame_task is not None:
                batch.append(frame_task)
        except asyncio.TimeoutError:
            return None

        # Then, drain additional frames without waiting (non-blocking)
        for _ in range(batch_size - 1):
            try:
                frame_task = task_queue.get_nowait()
                if frame_task is not None:
                    batch.append(frame_task)
            except asyncio.QueueEmpty:
                break

        return batch

    def _bridge_batch_to_workers(self, batch, inference_queues, num_workers: int, now_ns: int) -> tuple:
        """Route a drained batch of FrameTasks to per-worker mp.Queues.

        Applies flow control, converts each FrameTask to dict, routes by camera hash,
        and records latency/drop metrics. Returns ``(frames_bridged, frames_dropped)``.
        Behavior mirrors the previous inline batch-processing loop exactly.
        """
        frames_bridged = 0
        frames_dropped = 0

        for frame_task in batch:
            # Flow control: check total in-flight across all queues
            if self.enable_flow_control:
                total_queued = sum(q.qsize() for q in inference_queues)
                if total_queued >= self.max_in_flight_frames:
                    # Too many in-flight - drop frame to prevent backlog
                    frames_dropped += 1
                    if self.metrics:
                        self.metrics.record_drop(count=1, reason="flow_control")
                    continue

            # Convert FrameTask to dict format expected by inference workers
            task_data = self._frame_task_to_dict(frame_task)

            # Route to correct worker based on camera_id hash
            camera_id = frame_task.camera_id
            worker_id = hash(camera_id) % num_workers
            target_queue = inference_queues[worker_id]

            # Non-blocking put to mp.Queue
            try:
                target_queue.put_nowait(task_data)
                frames_bridged += 1

                # Record latency metrics
                latency_ns = now_ns - frame_task.ts_ns
                self._record_aggregated_metrics_ns(latency_ns)

            except Exception:
                # Queue full - drop
                frames_dropped += 1
                if self.metrics:
                    self.metrics.record_drop(count=1, reason="backpressure")

        return frames_bridged, frames_dropped

    async def _bridge_to_mp_queues(self) -> None:
        """Bridge from asyncio.Queue to mp.Queues for inference workers.

        This task runs concurrently with _consume_all_streams and transfers
        FrameTask tuples from the internal asyncio.Queue to the mp.Queues
        that inference workers read from.

        Features:
        - BATCH TRANSFERS: Processes 64 frames per iteration for 10-20x latency improvement
        - Converts FrameTask tuples to dict format expected by workers
        - Routes to correct worker queue based on camera_id hash
        - Backpressure handling (drop if mp.Queue full)
        """
        self.logger.info("Starting queue bridge to mp.Queues (batch mode)")

        # Get inference queues from pipeline
        inference_queues = self.pipeline.inference_queues
        if not inference_queues:
            self.logger.error("No inference queues available, bridge stopping")
            return

        num_workers = len(inference_queues)
        task_queue = self._task_queue
        time_ns = time.time_ns

        frames_bridged = 0
        frames_dropped = 0
        last_log_time = time.time()

        # Batch configuration for throughput optimization
        BRIDGE_BATCH_SIZE = 64  # Process up to 64 frames per iteration

        while self.running:
            try:
                # BATCH DRAIN: Collect multiple frames from asyncio.Queue
                batch = await self._drain_task_batch(task_queue, BRIDGE_BATCH_SIZE)

                if batch is None:
                    # First get timed out (no frame available) - loop for shutdown check
                    continue

                if not batch:
                    continue

                # Process entire batch
                now_ns = time_ns()
                bridged_delta, dropped_delta = self._bridge_batch_to_workers(
                    batch, inference_queues, num_workers, now_ns
                )
                frames_bridged += bridged_delta
                frames_dropped += dropped_delta

                # Periodic logging (every 30 seconds)
                now = time.time()
                if now - last_log_time > 30.0:
                    self.logger.info(
                        f"Queue bridge: {frames_bridged} bridged, {frames_dropped} dropped, batch_size={len(batch)}"
                    )
                    last_log_time = now

            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.logger.error(f"Queue bridge error: {e}")
                await asyncio.sleep(0.01)

        self.logger.info(f"Queue bridge stopped: {frames_bridged} bridged, {frames_dropped} dropped")

    def _frame_task_to_dict(self, frame_task: FrameTask) -> Dict[str, Any]:
        """Convert FrameTask namedtuple to dict format expected by inference workers.

        The inference workers expect a dict with specific fields.
        - SHM mode: 'shm_ref' for SHM-based frame loading
        - Legacy mode: 'frame_bytes' for direct frame bytes

        Args:
            frame_task: FrameTask namedtuple from consumer

        Returns:
            Dict in format expected by inference workers
        """
        camera_id = frame_task.camera_id
        camera_config = self.camera_configs.get(camera_id)

        # Get metadata from camera_config.stream_config for stream_info reconstruction
        cfg = camera_config.stream_config if camera_config else {}
        input_topic = camera_config.input_topic if camera_config else f"{camera_id}_input"

        # Build broker string from stream_config
        broker_host = self.stream_config.get("host", "localhost")
        broker_port = self.stream_config.get("port", 6379)
        broker = f"{broker_host}:{broker_port}"

        # Build stream_info (matching py_streaming format for py_analytics compatibility)
        stream_info = {
            "broker": broker,
            "topic": input_topic,
            "stream_time": self._get_high_precision_timestamp(),
            "camera_info": {
                "camera_name": cfg.get("camera_name", camera_id),
                "camera_group": cfg.get("camera_group", camera_id),
                "location": cfg.get("location", "Unknown Location"),
            },
        }

        if frame_task.is_shm_mode:
            # SHM MODE: Worker reads frame from shared memory
            frame_idx = frame_task.frame_idx
            frame_id = f"shm_{camera_id}_{frame_idx}"

            # SHM reference for worker to read frame directly
            shm_ref = {
                "camera_id": camera_id,
                "shm_name": frame_task.shm_name.decode()
                if isinstance(frame_task.shm_name, bytes)
                else frame_task.shm_name,
                "frame_idx": frame_idx,
                "width": frame_task.width,
                "height": frame_task.height,
                "format": frame_task.frame_format,
            }

            # Build task dict (compatible with existing inference worker)
            task_data = {
                "camera_id": camera_id,
                "frame_bytes": None,  # ZERO-COPY: No frame bytes, use shm_ref
                "frame_id": frame_id,
                "message": None,  # Lightweight path - no StreamMessage
                "input_stream": {
                    "shm_mode": True,
                    "frame_idx": frame_idx,
                    "width": frame_task.width,
                    "height": frame_task.height,
                    "format": frame_task.frame_format,
                    "stream_info": stream_info,
                },
                "shm_ref": shm_ref,  # Worker uses this to read from SHM
                "stream_key": camera_id,
                "extra_params": {},
                "camera_config": camera_config,
                "ts_ns": frame_task.ts_ns,
            }

            # Handle similar frames (use cached result)
            if frame_task.is_similar and frame_task.reference_frame_idx is not None:
                ref_frame_id = f"shm_{camera_id}_{frame_task.reference_frame_idx}"
                task_data["input_stream"]["use_cached_result"] = True
                task_data["input_stream"]["cached_frame_id"] = ref_frame_id

        else:
            # LEGACY MODE: Worker uses embedded frame bytes directly
            # Use frame_id from streaming message (already extracted in _parse_legacy_message)
            frame_id = frame_task.frame_id
            if not frame_id:
                # Fallback: Generate frame_id if not provided by streaming (should be rare)
                import uuid

                frame_id = f"fallback_{camera_id}_{uuid.uuid4().hex[:8]}"
                self.logger.warning(
                    f"[LEGACY_MODE] No frame_id from streaming for camera {camera_id}, generated fallback: {frame_id}"
                )

            task_data = {
                "camera_id": camera_id,
                "frame_bytes": frame_task.frame_bytes,  # Direct bytes for worker
                "frame_id": frame_id,
                "message": None,  # Lightweight path - no StreamMessage
                "input_stream": {
                    "shm_mode": False,
                    "width": frame_task.width,
                    "height": frame_task.height,
                    "format": frame_task.frame_format,
                    "content": frame_task.frame_bytes,
                    "stream_info": stream_info,
                },
                "shm_ref": None,  # No SHM reference in legacy mode
                "stream_key": camera_id,
                "extra_params": {},
                "camera_config": camera_config,
                "ts_ns": frame_task.ts_ns,
            }

            # Handle cached frames in legacy mode (similar to SHM mode)
            if frame_task.cached_frame_id:
                task_data["input_stream"]["use_cached_result"] = True
                task_data["input_stream"]["cached_frame_id"] = frame_task.cached_frame_id

        return task_data

    def _parse_shm_message(self, camera_id: str, fields: Dict[bytes, bytes], recv_ns: int) -> Optional[FrameTask]:
        """Parse SHM message fields into lightweight FrameTask.

        Uses pre-encoded byte keys for fast field access.
        Returns None if required fields are missing.

        Args:
            camera_id: Camera identifier
            fields: Raw message fields from XREAD
            recv_ns: Receive timestamp in nanoseconds

        Returns:
            FrameTask or None if invalid
        """
        try:
            # Extract required fields using pre-encoded keys
            shm_name = fields.get(KEY_SHM_NAME)
            frame_idx_raw = fields.get(KEY_FRAME_IDX)
            width_raw = fields.get(KEY_WIDTH)
            height_raw = fields.get(KEY_HEIGHT)
            ts_ns_raw = fields.get(KEY_TS_NS)

            if not all([shm_name, frame_idx_raw, width_raw, height_raw]):
                return None

            # Parse integer fields
            frame_idx = int(frame_idx_raw)
            width = int(width_raw)
            height = int(height_raw)
            ts_ns = int(ts_ns_raw) if ts_ns_raw else recv_ns

            # Optional fields
            frame_format_raw = fields.get(KEY_FORMAT)
            frame_format = frame_format_raw.decode() if frame_format_raw else "BGR"

            is_similar_raw = fields.get(KEY_IS_SIMILAR)
            is_similar = is_similar_raw in (b"1", b"true", b"True") if is_similar_raw else False

            reference_frame_idx = None
            if is_similar:
                ref_raw = fields.get(KEY_REFERENCE_FRAME_IDX)
                if ref_raw:
                    reference_frame_idx = int(ref_raw)

            return FrameTask(
                camera_id=camera_id,
                shm_name=shm_name,
                frame_idx=frame_idx,
                width=width,
                height=height,
                ts_ns=ts_ns,
                frame_format=frame_format,
                is_similar=is_similar,
                reference_frame_idx=reference_frame_idx,
                frame_bytes=None,  # SHM mode - no embedded bytes
                is_shm_mode=True,
            )

        except (ValueError, TypeError):
            return None

    def _parse_legacy_message(self, camera_id: str, fields: Dict[bytes, bytes], recv_ns: int) -> Optional[FrameTask]:
        """Parse legacy (non-SHM) message with embedded frame bytes.

        Legacy mode embeds JPEG-encoded frame bytes directly in Redis message.
        This is used when USE_SHM=false in the upstream camera streamer.

        Args:
            camera_id: Camera identifier
            fields: Raw message fields from XREAD
            recv_ns: Receive timestamp in nanoseconds

        Returns:
            FrameTask or None if invalid
        """
        try:
            # Extract frame_id from Redis fields (from streaming side)
            frame_id_raw = fields.get(KEY_FRAME_ID)
            frame_id = frame_id_raw.decode() if frame_id_raw else None

            # Extract frame content - try multiple field names for compatibility
            content = fields.get(KEY_CONTENT) or fields.get(KEY_INPUT_STREAM_CONTENT)

            if not content:
                return None

            # Extract optional dimensions (may not be present in legacy messages)
            width_raw = fields.get(KEY_WIDTH)
            height_raw = fields.get(KEY_HEIGHT)

            width = int(width_raw) if width_raw else 0
            height = int(height_raw) if height_raw else 0

            ts_ns_raw = fields.get(KEY_TS_NS)
            ts_ns = int(ts_ns_raw) if ts_ns_raw else recv_ns

            # Extract input_stream JSON to get cached_frame_id
            input_stream_raw = fields.get(b"input_stream")
            cached_frame_id = None
            if input_stream_raw:
                import json

                try:
                    input_stream = json.loads(input_stream_raw)
                    cached_frame_id = input_stream.get("cached_frame_id")
                except (json.JSONDecodeError, TypeError):
                    pass  # Ignore JSON parsing errors

            return FrameTask(
                camera_id=camera_id,
                shm_name=b"",  # Not used in legacy mode
                frame_idx=0,  # Not used in legacy mode
                width=width,
                height=height,
                ts_ns=ts_ns,
                frame_format="JPEG",  # Legacy uses JPEG encoding
                is_similar=bool(cached_frame_id),  # Similar if has cached reference
                reference_frame_idx=None,
                frame_bytes=content,  # Embedded frame bytes
                is_shm_mode=False,  # Legacy mode flag
                frame_id=frame_id,  # From streaming message
                cached_frame_id=cached_frame_id,  # For similar frames
            )

        except (ValueError, TypeError):
            return None

    def _is_stream_recoverable_error(self, error: Exception) -> bool:
        """Check if the error is a recoverable stream error.

        Args:
            error: The exception to check

        Returns:
            True if this is a recoverable error
        """
        error_str = str(error).lower()

        recoverable_patterns = [
            "no such key",  # Stream doesn't exist
            "connection",  # Connection issues
            "timeout",  # Timeout issues
        ]

        for pattern in recoverable_patterns:
            if pattern in error_str:
                return True

        return False

    # ========================================================================
    # METRIC AGGREGATION (optimized for nanosecond precision)
    # ========================================================================

    def _record_aggregated_metrics_ns(self, latency_ns: int) -> None:
        """Record metrics in aggregation buffer, flush periodically.

        Uses nanosecond precision for accurate latency tracking at high FPS.
        Flushes every N frames to reduce lock contention.
        """
        self._metrics_frame_count += 1
        self._metrics_latency_sum_ns += latency_ns
        if latency_ns > self._metrics_max_latency_ns:
            self._metrics_max_latency_ns = latency_ns

        # Flush every N frames
        if self._metrics_frame_count >= self.METRICS_AGGREGATION_COUNT:
            self._flush_aggregated_metrics()

    def _flush_aggregated_metrics(self) -> None:
        """Flush aggregated metrics to the metrics system."""
        if self._metrics_frame_count == 0:
            return

        # Convert nanoseconds to milliseconds for metrics system
        avg_latency_ms = (self._metrics_latency_sum_ns / self._metrics_frame_count) / 1_000_000

        # Record batch to metrics system
        self.metrics.record_latency(avg_latency_ms)
        self.metrics.record_throughput(count=self._metrics_frame_count)

        # Reset aggregation state
        self._metrics_frame_count = 0
        self._metrics_latency_sum_ns = 0
        self._metrics_max_latency_ns = 0
        self._metrics_last_flush = time.time()

    @staticmethod
    def _get_high_precision_timestamp() -> str:
        """Get high precision timestamp matching py_streaming format."""
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

    # ========================================================================
    # SHM_MODE: Shared Memory Methods (used by inference worker)
    # ========================================================================

    def get_task_queue(self) -> Optional[asyncio.Queue]:
        """Get the task queue for inference workers to consume from.

        Returns:
            asyncio.Queue containing FrameTask tuples
        """
        return self._task_queue

    def _get_frame_from_shm(self, data: Dict[str, Any]) -> Optional[bytes]:
        """Read frame from shared memory using metadata (LEGACY - use SHM refs instead).

        NOTE: The new zero-copy path passes SHM references to workers which read
        directly from SHM. This function is kept for backwards compatibility only.
        Frames are expected to be BGR format - no conversion is performed.

        Args:
            data: SHM metadata from Redis message

        Returns:
            Frame bytes (BGR format), or None if unavailable
        """
        camera_id = data.get("cam_id")
        shm_name = data.get("shm_name")
        frame_idx_str = data.get("frame_idx")
        width_str = data.get("width")
        height_str = data.get("height")
        frame_format = data.get("format", "NV12")

        # Parse string values
        try:
            frame_idx = int(frame_idx_str) if frame_idx_str else None
            width = int(width_str) if width_str else None
            height = int(height_str) if height_str else None
        except (ValueError, TypeError):
            self.logger.error(f"Invalid SHM metadata values: {data}")
            return None

        if not all([camera_id, shm_name, frame_idx is not None, width, height]):
            self.logger.error(f"Incomplete SHM metadata: {data}")
            return None

        # Get or attach to SHM buffer
        try:
            shm_buffer = self._get_or_attach_shm_buffer(camera_id, shm_name, width, height, frame_format)
        except Exception as e:
            self.logger.error(f"Failed to attach to SHM {shm_name}: {e}")
            return None

        # Calculate consumer lag for monitoring
        header = shm_buffer.get_header()
        current_write_idx = header["write_idx"]
        consumer_lag = current_write_idx - frame_idx

        # Log warning if consumer is falling behind (>70% of buffer)
        lag_threshold_warning = shm_buffer.slot_count * 0.7
        lag_threshold_critical = shm_buffer.slot_count * 0.8
        if consumer_lag > lag_threshold_warning:
            self.logger.warning(
                f"Consumer lag warning: camera={camera_id}, "
                f"lag={consumer_lag}/{shm_buffer.slot_count} frames "
                f"({consumer_lag * 100 / shm_buffer.slot_count:.1f}%)"
            )

        # If severely behind (>80% of buffer), skip to latest frame
        if consumer_lag > lag_threshold_critical:
            self.logger.warning(
                f"Consumer severely behind, skipping {consumer_lag} frames to latest for camera {camera_id}"
            )
            frame_idx = current_write_idx  # Use latest frame instead

        # Check if frame is still valid (not overwritten)
        if not shm_buffer.is_frame_valid(frame_idx):
            self.logger.debug(f"Frame {frame_idx} overwritten in SHM {shm_name}")
            return None

        # Read frame from SHM with torn frame detection
        # read_frame_copy() checks sequence counters to detect if producer
        # was writing during our read (torn frame)
        raw_bytes = shm_buffer.read_frame_copy(frame_idx)
        if raw_bytes is None:
            self.logger.debug(f"Frame {frame_idx} torn or overwritten in SHM {shm_name}")
            return None

        # Return raw bytes - frames are already BGR format (no conversion needed)
        return raw_bytes

    def _get_or_attach_shm_buffer(
        self, camera_id: str, shm_name: str, width: int, height: int, frame_format: str
    ) -> ShmRingBuffer:
        """Attach to existing SHM buffer (consumer side).

        Dynamically reads slot_count from SHM header to match producer config.

        Args:
            camera_id: Camera identifier
            shm_name: SHM segment name
            width: Frame width
            height: Frame height
            frame_format: Frame format string

        Returns:
            ShmRingBuffer instance
        """
        if camera_id not in self._shm_buffers:
            format_map = {
                "BGR": ShmRingBuffer.FORMAT_BGR,
                "RGB": ShmRingBuffer.FORMAT_RGB,
                "NV12": ShmRingBuffer.FORMAT_NV12,
            }
            frame_format_int = format_map.get(frame_format, ShmRingBuffer.FORMAT_BGR)

            # First attach with temporary slot_count to read header
            temp_buffer = ShmRingBuffer(
                camera_id=camera_id,
                width=width,
                height=height,
                frame_format=frame_format_int,
                slot_count=1000,  # Temporary - will read actual from header
                create=False,
            )

            # Read actual slot_count from producer's header
            header = temp_buffer.get_header()
            actual_slot_count = header.get("slot_count", 1000)
            temp_buffer.close()

            # Create final buffer with correct slot_count from producer
            self._shm_buffers[camera_id] = ShmRingBuffer(
                camera_id=camera_id,
                width=width,
                height=height,
                frame_format=frame_format_int,
                slot_count=actual_slot_count,  # Match producer's config
                create=False,  # Consumer attaches (does NOT create)
            )
            self.logger.info(
                f"Attached to SHM buffer for camera {camera_id}: "
                f"{width}x{height} {frame_format}, slot_count={actual_slot_count}"
            )

        return self._shm_buffers[camera_id]
