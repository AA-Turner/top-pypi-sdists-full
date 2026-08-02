from __future__ import annotations

import atexit
import logging
import os
import threading
import time
from typing import Any, ClassVar, Dict, List, Optional

from .camera_streamer.opencv.worker_manager import WorkerManager
from .constants import DEFAULT_NVDEC_NUM_SLOTS, GatewayStatus
from .dynamic_camera_manager import DynamicCameraManagerForNVDEC, DynamicCameraManagerForWorkers
from .instance_event_listener import InstanceEventListener
from .streaming_gateway_utils import (
    InputStream,
    InstanceStreamingGatewayUtil,
    StreamingGatewayUtil,
    build_stream_config_for_instance,
    input_stream_to_camera_config,
)

logger = logging.getLogger(__name__)

USE_NVDEC = os.getenv("USE_NVDEC", "false").lower() == "true"


def _build_optimizer_config_from_env() -> Optional[Dict[str, Any]]:
    """F08: build the frame-skip optimizer config from env (global toggle).

    ``MATRICE_MOTION_OPTIMIZER=1|true|yes`` enables the motion (SSIM) gate for
    every camera; it composes AFTER the per-camera FPS decimator. Threshold and
    thumbnail size are tunable. Returns ``None`` (no-op, publish every frame)
    when disabled — preserving today's default.
    """
    if os.getenv("MATRICE_MOTION_OPTIMIZER", "").lower() not in ("1", "true", "yes"):
        return None
    try:
        threshold = float(os.getenv("MATRICE_MOTION_THRESHOLD", "0.02"))
    except ValueError:
        threshold = 0.02
    try:
        thumb = int(os.getenv("MATRICE_MOTION_THUMB", "64"))
    except ValueError:
        thumb = 64
    logger.info("[F08] Motion optimizer ENABLED (threshold=%.3f, thumb=%d) for all cameras", threshold, thumb)
    return {"optimizer": "motion", "threshold": threshold, "thumb_height": thumb, "thumb_width": thumb}

# NVDEC imports (optional - graceful degradation)
NVDEC_AVAILABLE = False
# Default per-camera publish (output) FPS cap. Mirrors nvdec.DEFAULT_OUTPUT_FPS_CAP
# but is always defined so the gateway signature default holds even on hosts
# where the optional NVDEC stack fails to import.
DEFAULT_OUTPUT_FPS_CAP = 10.0
try:
    from .camera_streamer.nvdec.nvdec import (
        DEFAULT_OUTPUT_FPS_CAP,  # noqa: F811 — authoritative value when NVDEC is present
    )
    from .camera_streamer.nvdec.nvdec_worker_manager import (
        NVDECWorkerManager,
        is_nvdec_available,
    )

    NVDEC_AVAILABLE = is_nvdec_available()
except (ImportError, AttributeError, RuntimeError, TypeError, ValueError):
    # NVDEC not available (requires CuPy, PyNvVideoCodec, cuda_shm_ring_buffer)
    # Suppress warnings - these are optional dependencies
    pass


class KafkaConsumerWatchdog:
    """Restarts the gateway's event listener when its Kafka consumer goes silent.

    The underlying ``EventListener`` exposes ``last_poll_monotonic`` (advanced on
    every poll, even empty ones). If it stops advancing past ``stale_threshold``
    while the listener still claims to be active, the consumer was silently evicted
    from its group (e.g. after a backend/broker outage) and will never rejoin on
    its own — so we stop and restart the listener (full close + re-subscribe). This
    is the supervisor that was missing during the 2026-06-03 61h gateway outage,
    where the consumer left its group and camera discovery stayed dead for 61h.
    """

    def __init__(
        self,
        event_listener,
        is_active_fn,
        check_interval_sec=60.0,
        stale_threshold_sec=300.0,
    ):
        self._event_listener = event_listener
        self._is_active_fn = is_active_fn
        self._check_interval = check_interval_sec
        self._stale_threshold = stale_threshold_sec
        # Brief settle pause between stopping and restarting the listener.
        self._restart_pause_sec = 2.0
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._watch, name="KafkaConsumerWatchdog", daemon=True)
        self._thread.start()
        logger.info(
            "KafkaConsumerWatchdog started (check=%.0fs, stale=%.0fs)",
            self._check_interval,
            self._stale_threshold,
        )

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=5.0)

    def _watch(self) -> None:
        while not self._stop_event.wait(timeout=self._check_interval):
            try:
                if not self._is_active_fn():
                    continue
                el = self._event_listener
                if el is None or not el.is_listening:
                    continue
                inner = getattr(el, "_listener", None)
                last_poll = getattr(inner, "last_poll_monotonic", None)
                if last_poll is None:
                    continue
                idle = time.monotonic() - last_poll
                if idle <= self._stale_threshold:
                    continue
                logger.error(
                    "KafkaConsumerWatchdog: consumer silent for %.0fs (> %.0fs); "
                    "restarting event listener to rejoin the group",
                    idle,
                    self._stale_threshold,
                )
                try:
                    el.stop()
                except Exception as exc:
                    logger.exception("KafkaConsumerWatchdog: listener stop failed: %s", exc)
                if self._stop_event.wait(timeout=self._restart_pause_sec):
                    break
                try:
                    el.start()
                    logger.info("KafkaConsumerWatchdog: event listener restarted")
                except Exception as exc:
                    logger.exception("KafkaConsumerWatchdog: listener restart failed: %s", exc)
            except Exception as exc:
                logger.warning("KafkaConsumerWatchdog error: %s", exc)
        logger.info("KafkaConsumerWatchdog stopped")


class StreamingGateway:
    """Simplified streaming gateway for managing camera streams."""

    # Class-level tracking of active instances
    _active_instances: ClassVar[Dict[str, StreamingGateway]] = {}
    _class_lock: ClassVar[threading.RLock] = threading.RLock()

    def __init__(
        self,
        session: Any,
        streaming_gateway_id: Optional[str] = None,
        instance_id: Optional[str] = None,
        instance_string_id: Optional[str] = None,
        server_id: Optional[str] = None,
        server_type: Optional[str] = None,
        inputs_config: Optional[List[InputStream]] = None,
        video_codec: Optional[str] = None,
        force_restart: bool = False,
        enable_event_listening: bool = True,
        action_id: Optional[str] = None,
        num_workers: Optional[int] = None,  # Auto-calculate based on CPU cores and camera count
        max_cameras_per_worker: int = 50,
        allow_empty_start: bool = True,
        # NVDEC options (CUDA IPC ring buffer output)
        use_nvdec: bool = USE_NVDEC,  # Use NVDEC hardware decode + CUDA IPC output
        nvdec_gpu_id: int = 0,  # Primary GPU device ID (starting GPU)
        nvdec_num_gpus: int = 0,  # Number of GPUs (0=auto-detect all available)
        nvdec_pool_size: int = 8,  # NVDEC decoders per GPU
        nvdec_burst_size: Optional[int] = None,  # None = auto-tier by per-decoder camera count
        nvdec_frame_width: int = 0,  # 0 = native camera resolution (no SG-side preprocess; inference owns letterbox via Ultralytics)
        nvdec_frame_height: int = 0,  # 0 = native camera resolution
        nvdec_num_slots: int = DEFAULT_NVDEC_NUM_SLOTS,  # Ring buffer slots per camera
        nvdec_target_fps: int = 0,  # FPS override (0=use per-camera FPS from config)
        nvdec_output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP,  # publish cap; MATRICE_OUTPUT_FPS overrides (0 disables)
        # SHM configuration (centralized)
        shm_slot_count: int = 1000,  # Ring buffer size per camera (increased for consumer lag)
    ):
        """Initialize StreamingGateway.

        Args:
            session: Session object for authentication
            streaming_gateway_id: ID of the streaming gateway
            server_id: ID of the server (Kafka/Redis)
            server_type: Type of server (kafka or redis)
            inputs_config: List of InputStream configurations
            video_codec: Video codec (h264 or h265)
            force_restart: Force stop existing streams and restart
            enable_event_listening: Enable dynamic event listening for configuration updates
            action_id: Optional action ID to pass in API requests
            num_workers: Number of worker processes for async flow
            max_cameras_per_worker: Maximum cameras per worker process
            allow_empty_start: Allow starting with zero cameras (default True)
            use_nvdec: Use NVDEC hardware decode with CUDA IPC output (requires CuPy, PyNvVideoCodec)
            nvdec_gpu_id: Primary/starting GPU device ID for round-robin camera assignment
            nvdec_num_gpus: Number of GPUs to use (0=auto-detect all available GPUs)
            nvdec_pool_size: Number of NVDEC decoders per GPU
            nvdec_burst_size: Frames per stream before rotating to next stream.
                              None (default) = auto-tier by per-decoder stream
                              count (<=10 -> 1, 11-50 -> 2, >50 -> 4). Env var
                              MATRICE_NVDEC_BURST_SIZE forces an explicit value.
            nvdec_frame_width: Default output frame width (used if camera config doesn't specify)
            nvdec_frame_height: Default output frame height (used if camera config doesn't specify)
            nvdec_num_slots: Ring buffer slots per camera (named by camera_id)
            nvdec_target_fps: Global FPS override (0=use per-camera FPS from camera config)
            nvdec_output_fps_cap: Per-camera publish (output) FPS cap, default
                DEFAULT_OUTPUT_FPS_CAP (10). Env MATRICE_OUTPUT_FPS overrides it
                per deployment (0 disables the cap). Separate from the decode pacer.
            shm_slot_count: Number of frame slots per camera ring buffer for SHM mode (default: 300)
        """
        if not session:
            raise ValueError("Session is required")
        if not instance_id:
            raise ValueError("instance_id is required")

        self.session = session
        self.streaming_gateway_id = streaming_gateway_id
        self.instance_id = instance_id
        self.instance_string_id = instance_string_id
        self.instance_util: Optional[InstanceStreamingGatewayUtil] = None  # Set below
        self.force_restart = force_restart
        self.enable_event_listening = enable_event_listening
        self.num_workers = num_workers
        self.max_cameras_per_worker = max_cameras_per_worker
        self.video_codec = video_codec

        # NVDEC configuration
        self.use_nvdec = use_nvdec
        self.nvdec_gpu_id = nvdec_gpu_id
        self.nvdec_num_gpus = nvdec_num_gpus
        self.nvdec_pool_size = nvdec_pool_size
        self.nvdec_burst_size = nvdec_burst_size
        self.nvdec_frame_width = nvdec_frame_width
        self.nvdec_frame_height = nvdec_frame_height
        self.nvdec_num_slots = nvdec_num_slots
        self.nvdec_target_fps = nvdec_target_fps
        self.nvdec_output_fps_cap = nvdec_output_fps_cap

        # SHM configuration (centralized for all workers)
        self.shm_slot_count = shm_slot_count

        # Validate NVDEC availability if requested
        if use_nvdec and not NVDEC_AVAILABLE:
            raise RuntimeError(
                "NVDEC requested but not available. Requires CuPy, PyNvVideoCodec, and cuda_shm_ring_buffer module."
            )

        # Initialize instance-based utility for API interactions
        self.instance_util = InstanceStreamingGatewayUtil(
            session,
            self.instance_id,
            action_id=action_id,
            instance_string_id=self.instance_string_id,
        )
        logger.info(
            f"Using instance-based flow with instance_id={self.instance_id}, instance_string_id={self.instance_string_id}"
        )

        # Fetch consuming topics to discover streaming_gateway_id and server info
        consuming_topics = self.instance_util.get_consuming_topics()
        if consuming_topics:
            first_topic = consuming_topics[0]
            if not self.streaming_gateway_id:
                self.streaming_gateway_id = first_topic.get("streamingGatewayId")
            if server_id is None:
                server_id = first_topic.get("serverId")
            if server_type is None:
                server_type = first_topic.get("serverType")
            logger.info(
                f"Resolved from consuming topics: gateway_id={self.streaming_gateway_id}, "
                f"server_id={server_id}, server_type={server_type}"
            )

        # Create gateway_util for lifecycle APIs (start/stop/status)
        self.gateway_util = StreamingGatewayUtil(session, self.streaming_gateway_id, server_id, action_id=action_id)

        # Determine server_type - fetch from API if not provided
        if server_type is None:
            gateway_info = self.gateway_util.get_streaming_gateway_by_id()
            if gateway_info:
                server_type = gateway_info.get("serverType")
                logger.info(f"Retrieved server_type from API: {server_type}")
            else:
                raise ValueError("server_type is required but could not be retrieved from API")

        if not server_type:
            raise ValueError("server_type is required (kafka or redis)")

        self.server_type = server_type
        self.allow_empty_start = allow_empty_start

        # Get input configurations
        if inputs_config is None:
            logger.info("Fetching input configurations from API")
            try:
                if self.use_nvdec:
                    self.inputs_config = self.instance_util.get_nvdec_input_streams()
                else:
                    self.inputs_config = self.instance_util.get_input_streams()
            except Exception as exc:
                logger.warning(f"Failed to fetch cameras from API: {exc}")
                if allow_empty_start:
                    logger.info("Continuing with zero cameras (allow_empty_start=True)")
                    self.inputs_config = []
                else:
                    raise
        else:
            self.inputs_config = inputs_config if isinstance(inputs_config, list) else [inputs_config]  # type: ignore[list-item]

        # Check if we have cameras
        if not self.inputs_config:
            if allow_empty_start:
                logger.warning(
                    "Starting gateway with zero cameras - use camera_manager.add_camera() to add dynamically"
                )
            else:
                raise ValueError("No input configurations available and allow_empty_start=False")

        # Validate inputs (only if we have any)
        for i, config in enumerate(self.inputs_config):
            if not isinstance(config, InputStream):
                raise ValueError(f"Input config {i} must be an InputStream instance")

        # Initialize streaming backend
        self.worker_manager: Optional[WorkerManager] = None
        self.nvdec_worker_manager: Optional[Any] = None  # NVDECWorkerManager

        if self.use_nvdec:
            # NVDEC-based streaming flow (now supports dynamic camera events)
            logger.info(
                f"Initializing NVDEC worker flow - GPUs: {nvdec_num_gpus}, "
                f"pool_size: {nvdec_pool_size}, output: NV12 ({nvdec_frame_width}x{nvdec_frame_height})"
            )

            # Build stream config (unused by NVDEC but needed for interface consistency)
            stream_config = build_stream_config_for_instance(
                instance_util=self.instance_util,
                service_id=self.streaming_gateway_id,
                stream_maxlen=self.shm_slot_count,
            )

            # Convert InputStream configs to camera_config dicts
            camera_configs = [input_stream_to_camera_config(inp) for inp in self.inputs_config]

            self.nvdec_worker_manager = NVDECWorkerManager(
                camera_configs=camera_configs,
                stream_config=stream_config,
                gpu_id=nvdec_gpu_id,
                num_gpus=nvdec_num_gpus,
                nvdec_pool_size=nvdec_pool_size,
                nvdec_burst_size=nvdec_burst_size,
                frame_width=nvdec_frame_width,
                frame_height=nvdec_frame_height,
                num_slots=nvdec_num_slots,
                target_fps=nvdec_target_fps,
                output_fps_cap=nvdec_output_fps_cap,
                optimizer_config=_build_optimizer_config_from_env(),
                demuxer_type="gstreamer",
            )

            # Use DynamicCameraManagerForNVDEC as the camera_manager for event-driven updates
            self.camera_manager = DynamicCameraManagerForNVDEC(
                nvdec_worker_manager=self.nvdec_worker_manager,
                streaming_gateway_id=self.streaming_gateway_id,
                session=self.session,
                streaming_gateway=self,
                instance_util=self.instance_util,
            )
            # Let the NVDEC backend escalate late add_failed events into a DCM
            # cleanup so phantom cameras are reaped (step 2 in fix plan).
            if hasattr(self.nvdec_worker_manager, "set_on_camera_failed"):
                self.nvdec_worker_manager.set_on_camera_failed(self.camera_manager.on_backend_camera_failed)
            logger.info("NVDEC backend initialized (dynamic camera manager in use)")

        else:
            # Async worker flow using WorkerManager (DataBus, same as NVDEC)
            logger.info("Initializing async worker flow with WorkerManager (DataBus)")

            # Convert InputStream configs to camera_config dicts
            camera_configs = [input_stream_to_camera_config(inp) for inp in self.inputs_config]

            self.worker_manager = WorkerManager(
                camera_configs=camera_configs,
                num_workers=num_workers,
                max_cameras_per_worker=max_cameras_per_worker,
            )

            # Initialize dynamic camera manager for workers
            self.camera_manager = DynamicCameraManagerForWorkers(
                worker_manager=self.worker_manager,
                streaming_gateway_id=self.streaming_gateway_id,
                session=self.session,
                streaming_gateway=self,
                instance_util=self.instance_util,
            )

        # Initialize with current camera configurations
        # (skip for NVDEC which uses static configuration)
        if self.camera_manager is not None:
            self.camera_manager.initialize_from_config(self.inputs_config)

        # Initialize event system (if enabled and camera_manager exists)
        self.event_listener = None  # InstanceEventListener
        self._kafka_watchdog: Optional[KafkaConsumerWatchdog] = None

        if self.enable_event_listening and self.camera_manager is not None:
            try:
                self.event_listener = InstanceEventListener(
                    session=self.session,
                    instance_id=self.instance_id,
                    camera_manager=self.camera_manager,
                    instance_util=self.instance_util,
                )
            except Exception as e:
                logger.warning(f"Could not initialize event system: {e}")
                logger.info("Continuing without event listening")

        # State management
        self.is_streaming = False
        self._stop_event = threading.Event()
        self._state_lock = threading.RLock()
        self._my_stream_keys: set[str] = set()
        self._stream_key_to_camera_id: Dict[str, str] = {}  # Mapping of stream_key -> camera_id
        self._cleanup_registered = False

        # Statistics
        self.stats: Dict[str, Any] = {
            "start_time": None,
            "current_status": GatewayStatus.INITIALIZED,
        }

        # Register cleanup handler to ensure status is updated on unexpected shutdown
        atexit.register(self._emergency_cleanup)
        self._cleanup_registered = True

        logger.info(f"StreamingGateway initialized for {self.streaming_gateway_id}")

    def _register_as_active(self):
        """Register this instance as active."""
        with self.__class__._class_lock:
            self.__class__._active_instances[self.streaming_gateway_id] = self
        logger.info(f"Registered as active: {self.streaming_gateway_id}")

    def _unregister_as_active(self):
        """Unregister this instance from active tracking."""
        with self.__class__._class_lock:
            if self.streaming_gateway_id in self.__class__._active_instances:
                if self.__class__._active_instances[self.streaming_gateway_id] is self:
                    del self.__class__._active_instances[self.streaming_gateway_id]
        logger.info(f"Unregistered: {self.streaming_gateway_id}")

    def _stop_existing_streams(self):
        """Stop existing streams if force_restart is enabled."""
        if not self.force_restart:
            return

        logger.warning(f"Force stopping existing streams for {self.streaming_gateway_id}")

        with self.__class__._class_lock:
            if self.streaming_gateway_id in self.__class__._active_instances:
                existing_instance = self.__class__._active_instances[self.streaming_gateway_id]
                try:
                    existing_instance.stop_streaming()
                    logger.info(f"Force stopped existing streams for {self.streaming_gateway_id}")
                except Exception as e:
                    logger.warning(f"Error during force stop: {e}")
                time.sleep(1.0)

    def start_streaming(self) -> bool:
        """Start streaming.

        Returns:
            bool: True if streaming started successfully, False otherwise
        """
        with self._state_lock:
            if self.is_streaming:
                logger.warning("Streaming is already active")
                return False

        # Check if we have cameras (allow empty if flag is set)
        if not self.inputs_config:
            if self.allow_empty_start:
                logger.warning("Starting streaming with zero cameras - awaiting dynamic camera addition")
            else:
                logger.error("No input configurations available")
                return False

        # Force stop existing streams if requested
        self._stop_existing_streams()

        # Register as active
        self._register_as_active()

        try:
            if self.use_nvdec:
                success = self._start_nvdec_worker_streaming()
            else:
                success = self._start_async_worker_streaming()

            if not success:
                return False

            with self._state_lock:
                self._stop_event.clear()
                self.is_streaming = True
                self.stats["start_time"] = time.time()
                self.stats["current_status"] = GatewayStatus.RUNNING

            # Start event listener if enabled
            if self.event_listener and not self.event_listener.is_listening:
                logger.info("Starting event listener for dynamic updates")
                self.event_listener.start()

                # Supervise the Kafka consumer so a silent eviction self-heals
                # (rejoin the group) instead of leaving camera discovery dead.
                if self._kafka_watchdog is None:
                    self._kafka_watchdog = KafkaConsumerWatchdog(
                        event_listener=self.event_listener,
                        is_active_fn=lambda: self.is_streaming,
                        check_interval_sec=float(os.environ.get("MATRICE_KAFKA_WATCHDOG_INTERVAL_SEC", "60.0")),
                        stale_threshold_sec=float(os.environ.get("MATRICE_KAFKA_WATCHDOG_STALE_SEC", "300.0")),
                    )
                self._kafka_watchdog.start()

            logger.info(f"Started streaming with {len(self.inputs_config)} inputs")
            return True

        except Exception as exc:
            logger.exception(f"Error starting streaming: {exc}")
            try:
                self.stop_streaming()
            except Exception as cleanup_exc:
                logger.exception(f"Error during cleanup: {cleanup_exc}")
            return False

    def _start_async_worker_streaming(self) -> bool:
        """Start streaming using async worker flow.

        Returns:
            bool: True if started successfully, False otherwise
        """
        num_cameras = len(self.inputs_config) if self.inputs_config else 0
        logger.info(f"Starting async worker streaming flow with {num_cameras} cameras")

        # Build stream key mappings (if we have cameras)
        if self.inputs_config:
            with self._state_lock:
                for i, input_config in enumerate(self.inputs_config):
                    stream_key = input_config.camera_key or f"stream_{i}"
                    camera_id = input_config.camera_id or stream_key
                    self._stream_key_to_camera_id[stream_key] = camera_id
                    self._my_stream_keys.add(stream_key)

        # Start the worker manager (this starts all worker processes)
        # WorkerManager handles empty camera lists gracefully
        try:
            if not self.worker_manager:
                logger.error("WorkerManager not initialized")
                return False
            self.worker_manager.start()
            logger.info(f"Started WorkerManager with {self.num_workers} workers, {num_cameras} cameras")
            return True
        except Exception as exc:
            logger.exception(f"Failed to start WorkerManager: {exc}")
            return False

    def _start_nvdec_worker_streaming(self) -> bool:
        """Start streaming using NVDEC hardware decode with CUDA IPC output.

        NVDEC outputs NV12 frames to CUDA IPC ring buffers for zero-copy
        GPU inference pipelines. Unlike other backends, NVDEC:
        - Supports dynamic camera add/remove/update (restarts workers on change)
        - Outputs to CUDA IPC ring buffers (not Redis/Kafka)
        - Outputs NV12 format (50% smaller than RGB)

        Returns:
            bool: True if started successfully, False otherwise
        """
        num_cameras = len(self.inputs_config) if self.inputs_config else 0
        logger.info(
            f"Starting NVDEC worker streaming with {num_cameras} cameras "
            f"(GPUs: {self.nvdec_num_gpus}, pool_size: {self.nvdec_pool_size}, "
            f"output: NV12 {self.nvdec_frame_width}x{self.nvdec_frame_height})"
        )

        # Build stream key mappings for tracking
        if self.inputs_config:
            with self._state_lock:
                for i, input_config in enumerate(self.inputs_config):
                    stream_key = input_config.camera_key or f"stream_{i}"
                    camera_id = input_config.camera_id or stream_key
                    self._stream_key_to_camera_id[stream_key] = camera_id
                    self._my_stream_keys.add(stream_key)

        # Start the NVDEC worker manager
        try:
            if not self.nvdec_worker_manager:
                logger.error("NVDECWorkerManager not initialized")
                return False
            self.nvdec_worker_manager.start()
            logger.info(f"Started NVDECWorkerManager with {self.nvdec_num_gpus} GPU(s), {num_cameras} cameras")
            return True
        except Exception as exc:
            logger.exception(f"Failed to start NVDECWorkerManager: {exc}")
            return False

    def stop_streaming(self):
        """Stop all streaming operations."""
        with self._state_lock:
            if not self.is_streaming:
                logger.warning("Streaming is not active")
                return

            logger.info("Stopping streaming...")
            self._stop_event.set()
            self.is_streaming = False
            self.stats["current_status"] = GatewayStatus.STOPPED

        mem_before = self._capture_memory_snapshot()

        # Stop the Kafka consumer watchdog before the listener it supervises.
        if self._kafka_watchdog is not None:
            try:
                self._kafka_watchdog.stop()
            except Exception as exc:
                logger.exception(f"Error stopping Kafka consumer watchdog: {exc}")

        # Stop event listener first
        if self.event_listener and self.event_listener.is_listening:
            logger.info("Stopping event listener")
            try:
                self.event_listener.stop()
            except Exception as exc:
                logger.exception(f"Error stopping event listener: {exc}")

        # Stop streaming backend
        if self.use_nvdec:
            if self.nvdec_worker_manager:
                try:
                    logger.info("Stopping NVDECWorkerManager")
                    self.nvdec_worker_manager.stop()
                    logger.info("NVDEC worker manager stopped")
                except Exception as exc:
                    logger.exception(f"Error stopping NVDECWorkerManager: {exc}")
        else:
            if self.worker_manager:
                try:
                    logger.info("Stopping WorkerManager")
                    self.worker_manager.stop()
                except Exception as exc:
                    logger.exception(f"Error stopping WorkerManager: {exc}")

        # Always attempt to update status to "stopped", even if other steps fail
        # This is critical for proper gateway lifecycle management
        status_updated = False
        try:
            self.gateway_util.stop_streaming()
        except Exception as exc:
            logger.exception(f"Error calling stop_streaming API: {exc}")

        try:
            # Update status to "stopped" - this should always succeed
            self.gateway_util.update_status(GatewayStatus.STOPPED)
            status_updated = True
            logger.info("Gateway status updated to 'stopped'")
        except Exception as exc:
            logger.exception(f"CRITICAL: Failed to update gateway status to 'stopped': {exc}")
            logger.error("This may cause issues with gateway lifecycle tracking")

        # Unregister
        self._unregister_as_active()

        # Clear stream keys
        with self._state_lock:
            self._my_stream_keys.clear()
            self._stream_key_to_camera_id.clear()

        # Unregister atexit handler since we've successfully cleaned up
        if self._cleanup_registered:
            try:
                atexit.unregister(self._emergency_cleanup)
                self._cleanup_registered = False
            except Exception:  # nosec B110
                pass

        # Reap SHM files we own so the next start sees a clean /dev/shm and
        # GPU-driver pages tied to those inodes can be reclaimed by the kernel.
        self._cleanup_owned_shm()

        # Log the memory delta around the stop sequence; on Jetson Thor this
        # is the regression detector for "shutdown-released-memory" health.
        self._log_memory_delta(mem_before)

        logger.info(f"Streaming stopped (status updated: {status_updated})")

    @staticmethod
    def _capture_memory_snapshot():
        """Take a memory snapshot. Returns None if py_common diagnostics absent."""
        try:
            from matrice_common.diagnostics import snapshot  # type: ignore

            return snapshot()
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _log_memory_delta(before) -> None:
        """Log the delta between ``before`` and a fresh snapshot. Best-effort."""
        if before is None:
            return
        try:
            from matrice_common.diagnostics import delta, format_table, snapshot  # type: ignore

            after = snapshot()
            logger.info(
                "memory delta around stop_streaming():\n%s",
                format_table(delta(before, after)),
            )
        except Exception:  # noqa: BLE001
            logger.debug("memory delta unavailable", exc_info=True)

    @staticmethod
    def _cleanup_owned_shm() -> None:
        """Reap SHM files this gateway is responsible for. Best-effort."""
        try:
            from matrice_common.lifecycle import cleanup_owned_shm  # type: ignore

            removed = cleanup_owned_shm(
                (
                    "cuda_ipc_",
                    "databus__",
                    "databus_status__",
                    "global_frame_counter",
                    "sem.loky-",
                    "shm_results_",
                    # Note: gpu_camera_map intentionally NOT included here —
                    # consumers may still hold it mapped across the SG restart.
                )
            )
            if removed:
                logger.info("cleaned %d owned SHM files on stop", len(removed))
        except Exception:  # noqa: BLE001
            logger.debug("cleanup_owned_shm unavailable", exc_info=True)

    @property
    def active_worker_manager(self):
        """Return whichever worker backend is in use (NVDEC or OpenCV WorkerManager)."""
        if self.use_nvdec:
            return self.nvdec_worker_manager
        return self.worker_manager

    def get_camera_id_for_stream_key(self, stream_key: str) -> Optional[str]:
        """Get camera_id for a given stream_key."""
        with self._state_lock:
            return self._stream_key_to_camera_id.get(stream_key)

    def get_statistics(self) -> Dict:
        """Get streaming statistics."""
        with self._state_lock:
            stats = self.stats.copy()
            stats["my_stream_keys"] = list(self._my_stream_keys)
            stats["stream_key_to_camera_id"] = self._stream_key_to_camera_id.copy()

        if stats["start_time"]:
            stats["runtime_seconds"] = time.time() - stats["start_time"]
        else:
            stats["runtime_seconds"] = 0

        stats["is_streaming"] = self.is_streaming
        stats["event_listening_enabled"] = self.enable_event_listening
        stats["use_nvdec"] = self.use_nvdec

        # Add backend-specific statistics
        if self.use_nvdec:
            stats["nvdec_config"] = {
                "gpu_id": self.nvdec_gpu_id,
                "num_gpus": self.nvdec_num_gpus,
                "pool_size": self.nvdec_pool_size,
                "burst_size": self.nvdec_burst_size,
                "frame_width": self.nvdec_frame_width,
                "frame_height": self.nvdec_frame_height,
                "num_slots": self.nvdec_num_slots,
                "target_fps": self.nvdec_target_fps,
            }
            if self.nvdec_worker_manager:
                try:
                    stats["worker_stats"] = self.nvdec_worker_manager.get_worker_statistics()
                    stats["camera_assignments"] = self.nvdec_worker_manager.get_camera_assignments()
                except Exception as exc:
                    logger.warning(f"Failed to get NVDEC worker stats: {exc}")
        else:
            if self.worker_manager:
                try:
                    stats["worker_stats"] = self.worker_manager.get_worker_statistics()
                    stats["camera_assignments"] = self.worker_manager.get_camera_assignments()
                except Exception as exc:
                    logger.warning(f"Failed to get worker manager stats: {exc}")

        # Add camera manager statistics
        if self.camera_manager:
            try:
                stats["camera_manager_stats"] = self.camera_manager.get_statistics()
            except Exception as exc:
                logger.warning(f"Failed to get camera manager stats: {exc}")

        # Add event listener statistics
        if self.event_listener:
            try:
                stats["event_listener_stats"] = self.event_listener.get_statistics()
            except Exception as exc:
                logger.warning(f"Failed to get event listener stats: {exc}")

        return stats

    def get_config(self) -> Dict:
        """Get current configuration."""
        inputs_config_dict = []
        for config in self.inputs_config:
            inputs_config_dict.append(
                {
                    "source": config.source,
                    "fps": config.fps,
                    "quality": config.quality,
                    "width": config.width,
                    "height": config.height,
                    "camera_id": config.camera_id,
                    "camera_key": config.camera_key,
                    "camera_group_key": config.camera_group_key,
                    "camera_location": config.camera_location,
                    "simulate_video_file_stream": config.simulate_video_file_stream,
                }
            )

        return {
            "streaming_gateway_id": self.streaming_gateway_id,
            "inputs_config": inputs_config_dict,
            "force_restart": self.force_restart,
            "num_workers": self.num_workers,
            "max_cameras_per_worker": self.max_cameras_per_worker,
            # NVDEC configuration
            "use_nvdec": self.use_nvdec,
            "nvdec_gpu_id": self.nvdec_gpu_id,
            "nvdec_num_gpus": self.nvdec_num_gpus,
            "nvdec_pool_size": self.nvdec_pool_size,
            "nvdec_burst_size": self.nvdec_burst_size,
            "nvdec_frame_width": self.nvdec_frame_width,
            "nvdec_frame_height": self.nvdec_frame_height,
            "nvdec_num_slots": self.nvdec_num_slots,
            "nvdec_target_fps": self.nvdec_target_fps,
        }

    def _emergency_cleanup(self):
        """Emergency cleanup handler for unexpected shutdowns."""
        try:
            # Only run if streaming is still active
            if self.is_streaming:
                logger.warning("Emergency cleanup triggered - attempting to update gateway status")
                try:
                    self.gateway_util.update_status(GatewayStatus.STOPPED)
                    logger.info("Emergency status update successful")
                except Exception as exc:
                    logger.exception(f"Emergency status update failed: {exc}")
        except Exception as exc:
            # Catch any errors to prevent atexit handler from failing
            logger.exception(f"Error in emergency cleanup: {exc}")

    def __del__(self):
        """Destructor - ensure cleanup on garbage collection."""
        try:
            if hasattr(self, "is_streaming") and self.is_streaming:
                logger.warning("StreamingGateway being destroyed while still streaming")
                self.stop_streaming()
        except Exception as exc:
            logger.exception(f"Error in destructor: {exc}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_streaming()
        # Unregister atexit handler since we're doing controlled cleanup
        if self._cleanup_registered:
            try:
                atexit.unregister(self._emergency_cleanup)
                self._cleanup_registered = False
            except Exception:  # nosec B110
                pass
