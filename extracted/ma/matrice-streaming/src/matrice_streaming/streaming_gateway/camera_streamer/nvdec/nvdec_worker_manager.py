"""NVDEC Worker Manager for StreamingGateway integration.

This module provides a manager for the NVDEC hardware decoding backend.
Supports fully dynamic camera configuration at runtime (add, remove, update)
with smart per-GPU restarts and debounced batching to minimize disruption.
Outputs to CUDA IPC ring buffers (NV12 format) for zero-copy GPU inference pipelines.

Threading contract:
    All mutations to camera config state (_stream_configs, _gpu_camera_assignments,
    _camera_to_gpu) are serialized by the upstream DynamicCameraManager._lock.
    The _restart_lock protects the GPU restart scheduling. These two locks must
    never be held simultaneously to avoid deadlocks.
"""

import glob
import hashlib
import logging
import multiprocessing as mp
import os
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from matrice_common.stream.cuda_shm_ring_buffer import GlobalFrameCounter
from matrice_common.stream.gpu_camera_map import GpuCameraMap

from ..shm_liveness import camera_has_live_shm as _shm_has_live_holder
from ..shm_liveness import held_shm_paths, is_shm_path_live
from .nvdec import (
    CUPY_AVAILABLE,
    DEFAULT_OUTPUT_FPS_CAP,
    ORIN_NVDEC_AVAILABLE,
    PYNVCODEC_AVAILABLE,
    RING_BUFFER_AVAILABLE,
    StreamConfig,
    nvdec_pool_process,
)

logger = logging.getLogger(__name__)

# How long add_camera() waits for a `producer_ready` ACK from the GPU worker
# before treating the add as a silent failure and cleaning up the phantom.
# Lazy ring buffers wait for the first decoded frame, so this needs to cover
# RTSP connect + GStreamer pipeline build + first-frame decode in the worst case.
# Bulk-add scenarios (200+ cameras at once) can saturate RTSP sources and
# need a longer timeout; override via MATRICE_PRODUCER_READY_TIMEOUT_SEC.
#
# INVARIANT: this MUST exceed the demuxer's own open budget, or the manager gives
# up on a camera that is still legitimately connecting and rolls back an add that
# was about to succeed. GStreamerRTPDemuxer.RETRY_DELAYS = [1, 1, 2, 3, 5, 5] is
# ~17s of sleep alone, before per-attempt pipeline-open latency and the UDP->TCP
# fallback switch. A cold hot-add against a bouncing media server was measured at
# 37s (two RTSP retries), which the old 30s default cut short — the first link in
# the wedge this fix removes. Raised 30s -> 60s.
#
# FRAME_STALL_THRESHOLD_SEC (below) must stay above this so the readiness watchdog
# does not start racing a legitimately slow add.
PRODUCER_READY_TIMEOUT_SEC = float(os.environ.get("MATRICE_PRODUCER_READY_TIMEOUT_SEC", "60.0"))

# How long remove_camera() waits for the worker's "removed" ACK before returning.
# The worker emits it after _terminate_subprocess (terminate→join 5s→kill→join 3s),
# so this must be > ~8s.
REMOVE_ACK_TIMEOUT_SEC = float(os.environ.get("MATRICE_REMOVE_ACK_TIMEOUT_SEC", "10.0"))

# If a GPU worker's command handler stops emitting "handler_alive" for this long
# while the process is alive and frames still advance, the watchdog treats the
# handler as wedged and restarts the worker.
HANDLER_STALE_SEC = float(os.environ.get("MATRICE_HANDLER_STALE_SEC", "30.0"))

# How many times add_camera() attempts the ADD -> producer_ready handshake before
# giving up and rolling the camera back. A transient RTSP blip or a media server
# mid-bounce should cost a retry, not the camera: the old single-shot behaviour
# unregistered the camera and left it to the next periodic refresh.
#
# Each retry MUST be preceded by a real worker-side teardown
# (_teardown_worker_side_camera), otherwise the retry hits the worker's
# `sub_registry.owner_for(cam) is not None` short-circuit and re-arms the very
# split brain it is trying to recover from.
HOTADD_MAX_ATTEMPTS = max(1, int(os.environ.get("MATRICE_HOTADD_MAX_ATTEMPTS", "3")))

# Backoff between hot-add attempts, in seconds. Short on purpose: the demuxer
# already owns the connect-retry budget, so this only spaces out the handshake.
HOTADD_RETRY_BACKOFF_SEC = float(os.environ.get("MATRICE_HOTADD_RETRY_BACKOFF_SEC", "2.0"))

# If a GPU worker has cameras assigned but its frame counter has not advanced
# for this many seconds, the readiness watchdog restarts the worker. The
# threshold needs to exceed PRODUCER_READY_TIMEOUT_SEC so a slow first-frame
# does not race the watchdog. Default raised 60s → 120s because a single slow
# camera on a GPU shouldn't trigger a full worker restart that takes down all
# its sibling cameras. Override via MATRICE_FRAME_STALL_THRESHOLD_SEC.
FRAME_STALL_THRESHOLD_SEC = float(os.environ.get("MATRICE_FRAME_STALL_THRESHOLD_SEC", "120.0"))

# Circuit breaker: if a single GPU worker triggers more than this many
# stuck-but-alive restarts inside CIRCUIT_BREAKER_WINDOW_SEC, the watchdog
# PARKS it -- slowing restarts to one per CIRCUIT_BREAKER_COOLDOWN_SEC rather
# than stopping them. This prevents thrashing where each restart blows away SHM
# files for all cameras on the GPU and starts the cycle again, without ever
# abandoning the GPU. Override via MATRICE_WATCHDOG_*.
CIRCUIT_BREAKER_MAX_RESTARTS = int(os.environ.get("MATRICE_WATCHDOG_MAX_RESTARTS", "3"))
CIRCUIT_BREAKER_WINDOW_SEC = float(os.environ.get("MATRICE_WATCHDOG_WINDOW_SEC", "300.0"))

#: How long a tripped breaker stays parked before it re-arms ITSELF and resumes
#: restarting. The breaker exists to stop thrashing, not to abandon a GPU: every
#: restart wipes SHM for every camera on it, so restarting once per cooldown is
#: right and restarting every 120s is not. It used to have no expiry at all --
#: a tripped GPU stayed dark for the life of the process, its cameras silently
#: at 0 fps, and only a gateway restart brought them back.
CIRCUIT_BREAKER_COOLDOWN_SEC = float(os.environ.get("MATRICE_WATCHDOG_BREAKER_COOLDOWN_SEC", "600.0"))

#: How often to say a GPU is still parked. The park used to be completely silent
#: after its one ERROR, so a GPU dark for hours was indistinguishable in the logs
#: from a healthy one.
CIRCUIT_BREAKER_WARN_INTERVAL_SEC = float(os.environ.get("MATRICE_WATCHDOG_BREAKER_WARN_SEC", "300.0"))


def is_nvdec_available() -> bool:
    """Check if NVDEC backend is available.

    On desktop/Thor: Requires CuPy, PyNvVideoCodec, ring buffer.
    On Orin (MATRICE_PLATFORM=orin): Requires CuPy, gst-launch-1.0, ring buffer.
    PyNvVideoCodec is NOT needed on Orin (CUVID API unavailable).
    """
    if ORIN_NVDEC_AVAILABLE:
        return CUPY_AVAILABLE and RING_BUFFER_AVAILABLE
    return CUPY_AVAILABLE and PYNVCODEC_AVAILABLE and RING_BUFFER_AVAILABLE


def get_available_gpu_count() -> int:
    """Detect the number of available CUDA GPUs.

    Returns:
        Number of available GPUs, or 1 if detection fails.
    """
    if not CUPY_AVAILABLE:
        return 1

    try:
        import cupy as cp

        return cp.cuda.runtime.getDeviceCount()
    except Exception as e:
        logger.warning(f"Failed to detect GPU count: {e}, defaulting to 1")
        return 1


class NVDECWorkerManager:
    """Manager for NVDEC worker processes - fully dynamic camera configuration.

    This manager wraps the existing nvdec_pool_process function to integrate
    with StreamingGateway. Key features:

    - Fully dynamic camera configuration (add, remove, update at runtime)
    - Smart per-GPU restarts: only restarts workers for GPUs whose cameras changed
    - Debounced batching: rapid successive changes are batched into a single restart
    - Stable GPU assignment: cameras are assigned to GPUs via consistent hashing,
      so add/remove of one camera doesn't shuffle other cameras across GPUs
    - Outputs to CUDA IPC ring buffers (not Redis/Kafka)
    - NV12 format output (50% smaller than RGB)
    - One worker process per GPU
    """

    def __init__(
        self,
        camera_configs: List[Dict[str, Any]],
        stream_config: Dict[str, Any],  # Unused but kept for interface consistency
        gpu_id: int = 0,
        num_gpus: int = 0,  # 0 = auto-detect all available GPUs
        nvdec_pool_size: int = 0,  # 0 = auto-size from camera count (capped at 8)
        nvdec_burst_size: Optional[int] = None,  # None = auto-tier by per-decoder camera count
        frame_width: int = 0,  # 0 = native camera resolution (default; SG writes raw NV12, inference owns preprocess)
        frame_height: int = 0,  # 0 = native camera resolution
        num_slots: int = 64,  # default ring-buffer depth; see constants.DEFAULT_NVDEC_NUM_SLOTS
        target_fps: int = 0,  # 0 = use per-camera FPS from config
        duration_sec: float = 0,  # 0 = infinite
        demuxer_type: str = "nvc",  # "nvc" or "gstreamer"
        restart_delay: float = 1.0,  # Debounce delay for batching changes (seconds)
        optimizer_config: Optional[Dict[str, Any]] = None,  # frame-skip policy (see frame_optimizer.py)
        output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP,  # publish cap; MATRICE_OUTPUT_FPS overrides
    ):
        """Initialize NVDEC Worker Manager.

        Args:
            camera_configs: List of camera configuration dicts with keys:
                - camera_id or stream_key: Unique identifier (used for ring buffer naming)
                - source: Video file path or RTSP URL
                - width: Optional frame width (default: frame_width)
                - height: Optional frame height (default: frame_height)
                - fps: FPS limit for this camera (used by default)
            stream_config: Stream configuration (unused, for interface consistency)
            gpu_id: Primary GPU device ID (starting GPU for round-robin assignment)
            num_gpus: Number of GPUs to use (0 = auto-detect all available GPUs)
            nvdec_pool_size: Number of NVDEC decoders per GPU
            nvdec_burst_size: Frames per stream before rotating to next.
                              None (default) = auto-tier by per-decoder camera
                              count (<=10 -> 1, 11-50 -> 2, >50 -> 4). Env var
                              MATRICE_NVDEC_BURST_SIZE forces an explicit value.
            frame_width: Default output frame width (used if camera config doesn't specify)
            frame_height: Default output frame height (used if camera config doesn't specify)
            num_slots: Ring buffer slots per camera
            target_fps: Global FPS override (0 = use per-camera FPS from config)
            duration_sec: Duration to run (0 = infinite until stop)
            demuxer_type: Demuxer backend - "nvc" (PyNvVideoCodec, fastest for files) or
                          "gstreamer" (provides ABSOLUTE RTP timestamps for RTSP streams)
            restart_delay: Seconds to wait before restarting after a config change,
                           allowing multiple rapid changes to be batched into one restart
        """
        if not is_nvdec_available():
            raise RuntimeError("NVDEC not available. Requires CuPy, PyNvVideoCodec, and cuda_shm_ring_buffer")

        self.camera_configs = list(camera_configs)
        self.stream_config = stream_config
        self.gpu_id = gpu_id

        # Auto-detect GPUs if num_gpus is 0
        if num_gpus <= 0:
            detected_gpus = get_available_gpu_count()
            self.num_gpus = min(detected_gpus, 8)  # Max 8 GPUs
            logger.info(f"Auto-detected {detected_gpus} GPU(s), using {self.num_gpus}")
        else:
            self.num_gpus = min(num_gpus, 8)  # Max 8 GPUs

        # Cross-GPU consume (decoupled decode/inference) needs NVLink/PCIe-P2P;
        # detect a no-P2P multi-GPU host and warn (optionally collapse to one
        # GPU). Done before pool sizing so a collapse re-sizes the decoder pool.
        self._apply_no_p2p_policy()

        # Auto-size NVDEC decoder pool: each decoder costs ~75 MB VRAM, so an
        # 8-decoder pool for a 2-camera deployment wastes ~450 MB. The auto
        # rule sizes to (cameras-per-GPU + 2) headroom, capped at 8. Env var
        # MATRICE_NVDEC_POOL_SIZE overrides explicit-pass-through behaviour.
        env_pool = os.environ.get("MATRICE_NVDEC_POOL_SIZE", "").strip()
        if env_pool:
            try:
                nvdec_pool_size = int(env_pool)
            except ValueError:
                pass
        if nvdec_pool_size <= 0:
            cameras_per_gpu = max(
                1,
                (len(camera_configs) + self.num_gpus - 1) // max(1, self.num_gpus),
            )
            nvdec_pool_size = min(8, cameras_per_gpu + 2)
        self.nvdec_pool_size = nvdec_pool_size

        # NVDEC burst size: env override > caller value > auto-tier (None).
        # Auto-tier picks burst per-decoder at decode time based on actual
        # stream count, adapting to dynamic add/remove. An explicit non-None
        # value (from caller or env) skips auto-tier in the worker.
        env_burst = os.environ.get("MATRICE_NVDEC_BURST_SIZE", "").strip()
        if env_burst:
            try:
                nvdec_burst_size = int(env_burst)
            except ValueError:
                pass
        self.nvdec_burst_size = nvdec_burst_size
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_slots = num_slots
        self.target_fps = target_fps
        self.duration_sec = duration_sec if duration_sec > 0 else float("inf")
        self.demuxer_type = demuxer_type
        self._restart_delay = restart_delay
        self.optimizer_config = optimizer_config
        self.output_fps_cap = output_fps_cap

        # Per-GPU worker tracking. Command queues are created lazily in
        # _ensure_command_queue() and reused across worker respawns so a
        # watchdog restart never orphans commands that were in flight.
        self._gpu_workers: Dict[int, mp.Process] = {}
        self._gpu_stop_events: Dict[int, Any] = {}
        self._gpu_command_queues: Dict[int, mp.Queue] = {}  # IPC for dynamic camera changes

        # Single status queue shared by ALL GPU worker processes. Workers push
        # {"type": "producer_ready"/"add_failed", "camera_id": ..., ...}
        # messages here; _status_drain_thread consumes them.
        self._worker_status_queue: Optional[mp.Queue] = None
        self._status_drain_stop: Optional[threading.Event] = None
        self._status_drain_thread: Optional[threading.Thread] = None

        # Per-camera pending-add state. Each entry is {"event": threading.Event,
        # "result": "ready"|"failed"|None, "reason": str|None}. add_camera() pre-
        # creates an entry, sends the IPC command, then waits on the event.
        self._pending_adds: Dict[str, Dict[str, Any]] = {}
        self._pending_adds_lock = threading.Lock()

        # Per-camera pending-REMOVE state, mirroring pending-adds: remove_camera()
        # arms an entry, sends the IPC command, and waits for the worker's
        # "removed" ACK so it does not blind-return success.
        self._pending_removes: Dict[str, Dict[str, Any]] = {}
        self._pending_removes_lock = threading.Lock()

        # Last time each GPU's command handler emitted a "handler_alive"
        # heartbeat. The watchdog uses this to detect a wedged handler (process
        # alive + frames advancing, but not consuming commands).
        self._handler_last_seen: Dict[int, float] = {}

        # Serializes mutations to camera_configs / _camera_to_gpu / _stream_configs
        # / _gpu_camera_assignments across the main add/remove/update threads AND
        # the status-drain / watchdog threads (which previously mutated/read them
        # with no lock — a torn-config race). Re-entrant so a holder may call
        # _prepare_camera_configs(). LOCK ORDERING: DCM._lock (outer) → this
        # (inner); never call back into DCM while holding this lock.
        self._config_lock = threading.RLock()

        # Last time the per-GPU frame counter was observed to advance. Used by
        # the readiness watchdog to detect "alive but stuck" workers.
        self._gpu_last_advance_at: Dict[int, float] = {}
        self._gpu_last_frame_count: Dict[int, int] = {}

        # Circuit breaker state: tracks recent restart timestamps per GPU so the
        # watchdog can disable itself for a GPU that keeps thrashing. Each entry
        # is a list of `time.time()` values for restarts triggered by the
        # stuck-but-alive path (NOT the dead-worker path).
        self._gpu_restart_history: Dict[int, List[float]] = {}
        # Set of GPUs the circuit breaker has tripped on; remains tripped until
        # a manual reset (e.g., via gateway restart).
        self._gpu_circuit_tripped: Set[int] = set()
        # When each parked GPU was parked, and when it last said so. Both are what
        # let the park expire and stay audible instead of being a one-line ERROR
        # followed by permanent silence.
        self._gpu_circuit_tripped_at: Dict[int, float] = {}
        self._gpu_circuit_last_warn: Dict[int, float] = {}

        # Callback into DynamicCameraManager so a worker-reported add_failed
        # cleans up the parent's `cameras` dict / GpuCameraMap entry.
        self._on_camera_failed: Optional[Callable[[str, str], None]] = None

        # Shared multiprocessing primitives (created in start(), persist across per-GPU restarts)
        self._mp_ctx: Optional[Any] = None
        self._result_queue: Optional[mp.Queue] = None
        self._shared_frame_count: Optional[Any] = None
        self._gpu_frame_counts: Dict[int, Any] = {}
        self._start_time: Optional[float] = None
        self._is_running = False

        # Debounced restart support
        self._restart_lock = threading.Lock()
        self._restart_timer: Optional[threading.Timer] = None
        self._gpus_needing_restart: Set[int] = set()
        self._gpu_map: Optional[GpuCameraMap] = None

        # Convert camera configs to StreamConfig objects and assign to GPUs
        self._stream_configs: List[StreamConfig] = []
        self._gpu_camera_assignments: Dict[int, List[StreamConfig]] = {i: [] for i in range(self.num_gpus)}
        self._camera_to_gpu: Dict[str, int] = {}

        self._prepare_camera_configs()

        logger.info(
            f"NVDECWorkerManager initialized: {len(camera_configs)} cameras, "
            f"{self.num_gpus} GPU(s), pool_size={nvdec_pool_size}, demuxer={demuxer_type}, "
            f"restart_delay={restart_delay}s"
        )

    # ========================================================================
    # GPU Assignment
    # ========================================================================

    def _apply_no_p2p_policy(self) -> None:
        """On a multi-GPU host WITHOUT a full NVLink/PCIe-P2P mesh, cross-GPU
        consume (decode on GPU A, inference on GPU B) is not possible in place.
        The supported strategy is CO-LOCATION — the IE runs each camera on its
        decode GPU (see py_common ``resolve_decode_gpu``). Detect that here and
        warn; if ``MATRICE_SG_REQUIRE_P2P=1`` collapse decode to a single GPU so
        every consume is guaranteed same-GPU zero-copy (other GPU(s) idle).

        A probe failure (e.g. matrice_common/cupy unavailable) assumes a full
        mesh and leaves placement unchanged — never breaks startup.
        """
        if self.num_gpus <= 1:
            return
        try:
            from matrice_common.stream.device_topology import topology

            full_p2p = topology.has_full_p2p(range(self.num_gpus))
        except Exception as e:  # noqa: BLE001
            logger.warning(f"P2P topology probe failed ({e}); assuming full mesh")
            return
        if full_p2p:
            return
        if os.environ.get("MATRICE_SG_REQUIRE_P2P", "0") == "1":
            logger.warning(
                "No full GPU P2P/NVLink mesh and MATRICE_SG_REQUIRE_P2P=1 -> "
                "pinning ALL decode to GPU %s (single-GPU). The other GPU(s) "
                "stay idle but every consume is same-GPU zero-copy.",
                self.gpu_id,
            )
            self.num_gpus = 1  # _get_gpu_for_camera() returns self.gpu_id for all
        else:
            logger.warning(
                "MULTI-GPU host WITHOUT NVLink/P2P (GPUs %s). Cameras are spread "
                "across GPUs; each camera MUST be consumed by inference on its OWN "
                "decode GPU (CO-LOCATION) or cross-GPU consume will host-bounce "
                "(DEGRADED, if MATRICE_XGPU_FALLBACK=host_stage) or fail. The "
                "decode GPU per camera is published in the ring-buffer header and "
                "GpuCameraMap.",
                list(range(self.num_gpus)),
            )

    def _get_gpu_for_camera(self, camera_id: str, apps_consuming: Optional[Set[str]] = None) -> int:
        """Assign a camera to a decode GPU.

        1. STICKINESS — reuse the existing assignment if the camera is already
           mapped, so respawns/refreshes never move a placed camera.
        2. Otherwise a deterministic MD5 consistent hash over ``camera_id``.

        Decode and inference GPUs are decoupled (the IE reads any camera
        cross-GPU), so decode placement only needs to spread cameras evenly and
        stay stable across SG restarts — there is no app-affinity / load scoring.

        Args:
            camera_id: Unique camera identifier.
            apps_consuming: Unused; kept for call-site compatibility.

        Returns:
            GPU ID for this camera.
        """
        # 1) Stickiness: re-use the existing assignment if any.
        existing = self._camera_to_gpu.get(camera_id)
        if existing is not None:
            logger.debug(f"respawn-preserve: camera {camera_id} sticky to GPU {existing}")
            return int(existing)

        # Degenerate guard: with <=1 GPU every camera lands on the base GPU.
        # This also prevents a modulo-by-zero when num_gpus is 0.
        if self.num_gpus <= 1:
            return self.gpu_id

        # 2) Deterministic MD5 consistent hash. Placement only, never a security
        # digest, and usedforsecurity=False is already set. Changing the algorithm
        # would re-place every existing camera onto a different GPU.
        # nosemgrep: hashlib-md5-or-sha1
        hash_bytes = hashlib.md5(camera_id.encode(), usedforsecurity=False).digest()[:4]
        hash_val = int.from_bytes(hash_bytes, "little")
        return (self.gpu_id + hash_val) % self.num_gpus

    # ========================================================================
    # Camera Config Preparation
    # ========================================================================

    def _prepare_camera_configs(self):
        """Serialized entry point for the config rebuild.

        Holds ``_config_lock`` so a status-drain / watchdog thread cannot rebuild
        the config concurrently with a main-thread add/remove (a torn-state race).
        Re-entrant: callers already holding the lock re-enter harmlessly.
        """
        with self._config_lock:
            self._prepare_camera_configs_unlocked()
        # Outside the lock: this touches only breaker state, and the watchdog thread
        # reads it without the config lock.
        self._reset_restart_circuit_breakers("camera configuration was rebuilt")

    def _prepare_camera_configs_unlocked(self):
        """Convert dict configs to StreamConfig and distribute across GPUs.

        Ring buffers are named using camera_id for SHM identification.
        Per-camera FPS from config is used by default (target_fps=0 means use config FPS).
        Uses consistent hashing for stable GPU assignment across adds/removes.

        Stickiness: a camera that already has a GPU assignment — either
        in-memory (``_camera_to_gpu``) OR previously persisted to
        ``GpuCameraMap`` SHM — re-uses that GPU on respawn/refresh as long
        as the GPU is still in range. This prevents the drift IE consumers
        observed when ``add_camera``/``update_camera`` flows re-ran the
        placer on cameras whose mapping was supposed to be stable.
        """
        # Snapshot the prior in-memory mapping AND the persisted GpuCameraMap.
        # We feed both into the stickiness path of _get_gpu_for_camera so a
        # respawn never produces a different GPU for an already-placed cam.
        prior_in_memory: Dict[str, int] = dict(self._camera_to_gpu)
        prior_persisted: Dict[str, int] = {}
        if self._gpu_map is not None:
            try:
                prior_persisted = self._gpu_map.get_all_mappings() or {}
            except Exception as e:
                logger.debug(f"GpuCameraMap.get_all_mappings() failed: {e}")

        self._stream_configs.clear()
        self._gpu_camera_assignments = {i: [] for i in range(self.num_gpus)}
        self._camera_to_gpu.clear()

        # Feed prior assignments back so stickiness works.
        # Priority: in-memory snapshot first (most recent), then persisted SHM.
        for cam_id, gpu_id in prior_in_memory.items():
            if isinstance(gpu_id, int) and 0 <= gpu_id < self.num_gpus:
                self._camera_to_gpu[cam_id] = gpu_id
        for cam_id, gpu_id in prior_persisted.items():
            if cam_id in self._camera_to_gpu:
                continue
            if isinstance(gpu_id, int) and 0 <= gpu_id < self.num_gpus:
                self._camera_to_gpu[cam_id] = gpu_id
                logger.info(f"respawn-preserve: camera {cam_id} reuses GPU {gpu_id} from persisted GpuCameraMap")

        for i, config in enumerate(self.camera_configs):
            camera_id = config.get("camera_id") or config.get("stream_key") or f"cam_{i:04d}"

            source = config.get("source") or config.get("video_path")
            if not source:
                logger.warning(f"Camera {camera_id} has no source, skipping")
                continue

            # Use per-camera width/height from API config if provided,
            # otherwise fall back to the manager's default (self.frame_width/height).
            # Set to 0 to use native camera resolution (lazy ring buffer creation).
            width = config.get("width") or self.frame_width
            height = config.get("height") or self.frame_height

            # F08 rollback kill-switch: force native decode (no SG-side resize)
            # fleet-wide, restoring pre-feature behavior with no redeploy.
            if os.getenv("MATRICE_SG_DISABLE_RESIZE", "").lower() in ("1", "true", "yes"):
                width = 0
                height = 0

            if self.target_fps > 0:
                fps = self.target_fps
            else:
                fps = config.get("fps", 10)

            gpu_id = self._get_gpu_for_camera(camera_id)
            codec = config.get("codec", "h264")

            stream_config = StreamConfig(
                camera_id=camera_id,
                video_path=source,
                width=width,
                height=height,
                target_fps=fps,
                gpu_id=gpu_id,
                demuxer_type=self.demuxer_type,
                codec=codec,
            )

            self._stream_configs.append(stream_config)
            self._gpu_camera_assignments[gpu_id].append(stream_config)
            self._camera_to_gpu[camera_id] = gpu_id

            logger.debug(f"Camera {camera_id}: source={source}, {width}x{height}@{fps}fps, GPU{gpu_id}, codec={codec}")

    def _sync_gpu_map(self) -> None:
        """Write current camera-GPU assignments to shared memory immediately.

        Called after _prepare_camera_configs() to ensure inference containers
        see the updated mapping without waiting for the debounced restart.
        """
        if self._gpu_map is None:
            return
        mappings = {sc.camera_id: sc.gpu_id for sc in self._stream_configs}
        self._gpu_map.set_bulk_mapping(mappings)
        logger.debug(f"GpuCameraMap synced: {len(mappings)} camera mappings")

    def evict_camera_mapping(self, camera_id: str, reason: str = "") -> bool:
        """Remove a camera entry from GpuCameraMap.

        Used for graceful removal, deletion events, or startup sweep of
        stale entries. Idempotent. The placer is NOT invoked.

        Args:
            camera_id: Camera identifier to evict.
            reason: Optional reason string for the log line.

        Returns:
            True if any state was actually evicted.
        """
        evicted_any = False
        # Forget the in-memory GPU assignment (the value is reused in the log).
        gpu_id = self._camera_to_gpu.pop(camera_id, None)

        if self._gpu_map is not None:
            try:
                # remove_mapping is a no-op if camera_id is absent.
                if self._gpu_map.get_gpu_id(camera_id) is not None:
                    self._gpu_map.remove_mapping(camera_id)
                    evicted_any = True
            except Exception as e:
                logger.warning(f"evict_camera_mapping({camera_id}): GpuCameraMap remove failed: {e}")

        if evicted_any:
            logger.info(
                f"stale-cleanup: evicted camera {camera_id} (prior_gpu={gpu_id}, reason={reason or 'unspecified'})"
            )
        return evicted_any

    def sweep_stale_mappings(self) -> int:
        """Sweep GpuCameraMap entries that don't correspond to active cameras.

        Active cameras are those listed in ``self.camera_configs``. Any entry
        in the persisted ``GpuCameraMap`` that isn't active AND has no
        ``/dev/shm/databus__<cam>__sg__frames`` SHM file is removed.

        Intended to be called on SG startup (before workers are spawned)
        and periodically thereafter as a safety net. Returns the number of
        cameras evicted.
        """
        if self._gpu_map is None:
            return 0
        try:
            persisted = self._gpu_map.get_all_mappings() or {}
        except Exception as e:
            logger.warning(f"sweep_stale_mappings: get_all_mappings failed: {e}")
            return 0

        active: Set[str] = set()
        for cfg in self.camera_configs:
            cid = cfg.get("camera_id") or cfg.get("stream_key")
            if cid:
                active.add(cid)

        shm_root = os.environ.get("MATRICE_SHM_PATH", "/dev/shm")  # nosec B108
        evicted = 0
        for cam_id in list(persisted.keys()):
            if cam_id in active:
                continue
            shm_file = os.path.join(shm_root, f"databus__{cam_id}__sg__frames")
            if os.path.exists(shm_file):
                # SHM still present — likely a graceful-removal-in-progress.
                # Leave it; the next sweep or remove_camera path will clear.
                continue
            if self.evict_camera_mapping(cam_id, reason="startup-sweep-orphan"):
                evicted += 1
        if evicted:
            logger.warning(
                f"sweep_stale_mappings: evicted {evicted} stale entries "
                f"(active={len(active)}, persisted_before={len(persisted)})"
            )
        return evicted

    def _snapshot_gpu_camera_ids(self) -> Dict[int, Set[str]]:
        """Take a snapshot of current camera IDs per GPU for change detection."""
        return {gpu_id: {sc.camera_id for sc in cams} for gpu_id, cams in self._gpu_camera_assignments.items()}

    def _get_affected_gpus(
        self,
        old_snapshot: Dict[int, Set[str]],
        new_snapshot: Dict[int, Set[str]],
    ) -> Set[int]:
        """Compare snapshots to find which GPUs had their camera list change."""
        affected: Set[int] = set()
        all_gpus = set(old_snapshot.keys()) | set(new_snapshot.keys())
        for gpu_id in all_gpus:
            if old_snapshot.get(gpu_id, set()) != new_snapshot.get(gpu_id, set()):
                affected.add(gpu_id)
        return affected

    # ========================================================================
    # Worker Lifecycle (per-GPU granularity)
    # ========================================================================

    def _start_gpu_worker(self, gpu_id: int) -> None:
        """Start a single GPU worker process.

        Args:
            gpu_id: GPU device ID to start worker for
        """
        gpu_cameras = self._gpu_camera_assignments.get(gpu_id, [])
        if not gpu_cameras:
            return

        if self._mp_ctx is None:
            logger.error("Cannot start GPU worker: multiprocessing context not initialized")
            return

        # Prevent duplicate workers — if an old worker is still alive, kill it first
        existing = self._gpu_workers.get(gpu_id)
        if existing is not None and existing.is_alive():
            logger.warning(f"GPU {gpu_id}: Killing stale worker PID {existing.pid} before starting new one")
            existing.terminate()
            existing.join(timeout=5)
            if existing.is_alive():
                existing.kill()
                existing.join(timeout=3)
            self._gpu_workers.pop(gpu_id, None)

        stop_event = self._mp_ctx.Event()
        self._gpu_stop_events[gpu_id] = stop_event

        if gpu_id not in self._gpu_frame_counts:
            self._gpu_frame_counts[gpu_id] = self._mp_ctx.Value("L", 0)
        else:
            # Reset counter on worker restart so the new process's monitoring
            # loop doesn't include stale frames from the previous run in its avg FPS.
            self._gpu_frame_counts[gpu_id].value = 0

        total_num_streams = len(self._stream_configs)
        total_num_gpus = len([g for g in range(self.num_gpus) if self._gpu_camera_assignments.get(g)])

        command_queue = self._ensure_command_queue(gpu_id)

        # Reset frame-stall tracking when a worker (re)starts so the watchdog
        # gives the new worker a fresh grace period before judging it stuck.
        self._gpu_last_advance_at[gpu_id] = time.time()
        self._gpu_last_frame_count[gpu_id] = (
            self._gpu_frame_counts[gpu_id].value if gpu_id in self._gpu_frame_counts else 0
        )

        p = self._mp_ctx.Process(
            target=nvdec_pool_process,
            args=(
                gpu_id,
                gpu_cameras,
                self.nvdec_pool_size,
                self.duration_sec,
                self._result_queue,
                stop_event,
                self.nvdec_burst_size,
                self.num_slots,
                self.target_fps,
                self._shared_frame_count,
                self._gpu_frame_counts,
                total_num_streams,
                total_num_gpus,
                self.demuxer_type,
            ),
            kwargs={
                "command_queue": command_queue,
                "worker_status_queue": self._worker_status_queue,
                "optimizer_config": self.optimizer_config,
                "output_fps_cap": self.output_fps_cap,
            },
            name=f"NVDECWorker-GPU{gpu_id}",
            daemon=False,
        )
        p.start()
        self._gpu_workers[gpu_id] = p
        logger.info(f"Started NVDEC worker on GPU {gpu_id} (PID: {p.pid}) with {len(gpu_cameras)} cameras")

    def _stop_gpu_worker(self, gpu_id: int, timeout: float = 15.0) -> None:
        """Stop a single GPU worker process gracefully.

        Args:
            gpu_id: GPU device ID to stop worker for
            timeout: Maximum time to wait for graceful shutdown
        """
        if gpu_id not in self._gpu_workers:
            return

        stop_event = self._gpu_stop_events.get(gpu_id)
        if stop_event:
            stop_event.set()

        p = self._gpu_workers.get(gpu_id)
        if p is None:
            return
        p.join(timeout=timeout)
        if p.is_alive():
            # Hard kill loses the cleanup window — log a memory snapshot so any
            # later "GPU memory not released" reports can be correlated with
            # this event instead of looking like a generic leak.
            self._log_memory_snapshot(f"NVDECWorker-GPU{gpu_id} hard-kill (graceful join timed out)")
            logger.warning(f"NVDECWorker-GPU{gpu_id} did not stop gracefully, terminating")
            p.terminate()
            p.join(timeout=2.0)

        self._gpu_workers.pop(gpu_id, None)
        self._gpu_stop_events.pop(gpu_id, None)
        # NOTE: do NOT pop _gpu_command_queues — the queue is persistent
        # across worker respawns so any in-flight command is still consumed
        # by the next worker (step 6 in the fix plan).
        logger.info(f"Stopped NVDEC worker on GPU {gpu_id}")

    @staticmethod
    def _log_memory_snapshot(prefix: str) -> None:
        """Best-effort memory snapshot log; never raises."""
        try:
            from matrice_common.diagnostics import format_table, snapshot  # type: ignore

            logger.warning("%s\n%s", prefix, format_table(snapshot()))
        except Exception:  # noqa: BLE001
            logger.debug("%s — memory snapshot unavailable", prefix, exc_info=True)

    def _restart_gpu_worker(self, gpu_id: int) -> None:
        """Stop and restart a single GPU worker with its current camera assignment."""
        self._stop_gpu_worker(gpu_id)
        if self._gpu_camera_assignments.get(gpu_id):
            self._start_gpu_worker(gpu_id)
        else:
            logger.info(f"GPU {gpu_id} has no cameras after config change, worker not restarted")

    # ========================================================================
    # Debounced Restart (batches rapid changes into a single restart)
    # ========================================================================

    def _schedule_restart(self, affected_gpus: Optional[Set[int]] = None) -> None:
        """Schedule a debounced restart for the affected GPUs.

        Multiple calls within the restart_delay window are batched: the timer
        resets each time, and all accumulated GPU IDs are restarted together
        when the timer finally fires.

        Args:
            affected_gpus: Set of GPU IDs that need restart, or None for all GPUs
        """
        with self._restart_lock:
            if affected_gpus:
                self._gpus_needing_restart.update(affected_gpus)
            else:
                self._gpus_needing_restart = set(range(self.num_gpus))

            if self._restart_timer is not None:
                self._restart_timer.cancel()

            self._restart_timer = threading.Timer(
                self._restart_delay,
                self._execute_scheduled_restart,
            )
            self._restart_timer.daemon = True
            self._restart_timer.start()

            logger.info(f"Restart scheduled in {self._restart_delay}s for GPU(s): {sorted(self._gpus_needing_restart)}")

    def _execute_scheduled_restart(self) -> None:
        """Execute the debounced restart (called by the timer thread).

        Grabs the accumulated set of GPU IDs atomically, then performs
        the actual stop/start outside the lock to avoid blocking callers.
        """
        with self._restart_lock:
            gpus_to_restart = self._gpus_needing_restart.copy()
            self._gpus_needing_restart.clear()
            self._restart_timer = None

        if not gpus_to_restart:
            return

        # Dynamic camera changes are now handled via IPC command queues.
        # Skip the destructive stop/restart cycle — only log what would have been restarted.
        active_workers = sum(1 for p in self._gpu_workers.values() if p.is_alive())
        if active_workers > 0:
            logger.info(
                f"Skipping scheduled restart for GPU(s) {sorted(gpus_to_restart)} — "
                f"{active_workers} workers alive, camera changes handled via IPC"
            )
            # Restart any dead workers only
            for gpu_id in gpus_to_restart:
                p = self._gpu_workers.get(gpu_id)
                if p is None or not p.is_alive():
                    logger.warning(f"GPU {gpu_id} worker is dead, restarting")
                    if self._gpu_camera_assignments.get(gpu_id):
                        self._start_gpu_worker(gpu_id)
            return

        sorted_gpus = sorted(gpus_to_restart)
        total_cams = sum(len(self._gpu_camera_assignments.get(g, [])) for g in sorted_gpus)
        logger.info(f"Executing batched restart for GPU(s) {sorted_gpus} ({total_cams} cameras affected)")

        # Update GpuCameraMap with current camera-GPU assignments
        # so inference containers see the new mapping before workers start
        if self._gpu_map is not None:
            mappings = {cfg.camera_id: cfg.gpu_id for cfg in self._stream_configs}
            self._gpu_map.set_bulk_mapping(mappings)
            logger.info(f"GpuCameraMap updated with {len(mappings)} camera mappings")

        # Stop affected workers first (in parallel they'll all get the signal)
        for gpu_id in sorted_gpus:
            self._stop_gpu_worker(gpu_id)

        # Verify all old workers are actually dead before spawning replacements
        for gpu_id in sorted_gpus:
            p = self._gpu_workers.get(gpu_id)
            if p is not None and p.is_alive():
                logger.warning(f"GPU {gpu_id} worker still alive after stop, force killing")
                p.kill()
                p.join(timeout=5)
                self._gpu_workers.pop(gpu_id, None)

        # Start workers with latest camera assignments
        for gpu_id in sorted_gpus:
            if self._gpu_camera_assignments.get(gpu_id):
                self._start_gpu_worker(gpu_id)

        logger.info(f"Batched restart complete for GPU(s) {sorted_gpus}")

    # ========================================================================
    # Public Lifecycle Methods
    # ========================================================================

    def _clean_stale_shm(self) -> None:
        """Remove stale SHM files from previous runs.

        Cleans up cuda_ipc ring buffers, gpu_camera_map, global_frame_counter,
        loky semaphores, and inference result buffers left behind by a
        previous SG/inference instance. This prevents consumers from reading
        stale frames and ensures a clean startup.

        ``shm_results_*`` was added to the pattern list to reap result buffers
        from a previous inference run; without it, those orphaned files
        contributed to the Jetson-Thor "lazy release" memory accounting where
        GPU-driver pages stay tied to inode references until ``drop_caches=2``.
        """
        shm_patterns = [  # nosec B108 - SHM cleanup is intentional
            "/dev/shm/cuda_ipc_*",
            "/dev/shm/databus__*",
            "/dev/shm/databus_status__*",
            "/dev/shm/global_frame_counter",
            "/dev/shm/gpu_camera_map",
            "/dev/shm/sem.loky-*",
            "/dev/shm/shm_results_*",
        ]
        removed = 0
        skipped = 0
        # One /proc walk for the whole sweep rather than one per candidate path.
        held = held_shm_paths()
        for pattern in shm_patterns:
            for path in glob.glob(pattern):
                # A segment a live process still holds open is not stale. On a
                # clean startup this is vacuous, but an SG restarting beside a
                # surviving producer would otherwise strand that producer's
                # consumers with ENOENT while frames are still flowing.
                if is_shm_path_live(path, held):
                    skipped += 1
                    continue
                try:
                    os.remove(path)
                    removed += 1
                except OSError as e:
                    logger.warning(f"Failed to remove stale SHM {path}: {e}")
        if removed:
            logger.warning(f"Cleaned {removed} stale SHM files from previous run")
        if skipped:
            logger.warning(f"Left {skipped} SHM file(s) in place — still held open by a live process")

    def _clean_stale_shm_for(self, camera_id: str) -> None:
        """Remove any pre-existing SHM files for a specific camera before hot-add.

        Without this, a crashed previous incarnation of the same camera_id
        leaves /dev/shm/databus__{camera_id}__sg__frames on disk; the next
        producer creation races on unlink/open/ftruncate and can leave the
        ring buffer half-initialised.

        Only genuinely orphaned files are removed. "Stale" used to be assumed
        rather than checked, so when the manager's view (0 cameras) disagreed with
        a live worker's (1 camera) — exactly the split brain
        ``_teardown_worker_side_camera`` now prevents — this unlinked the segment
        that worker was actively writing, and inference saw ENOENT while the SG
        still logged frames.
        """
        if not camera_id:
            return
        if _shm_has_live_holder(camera_id):
            logger.warning(
                f"Camera {camera_id}: SHM still held open by a live process — skipping "
                f"pre-add cleanup (worker-side teardown incomplete). Not unlinking a "
                f"segment a producer is writing."
            )
            return
        patterns = [  # nosec B108 - SHM cleanup is intentional
            f"/dev/shm/databus__{camera_id}__*",  # nosec B108
            f"/dev/shm/databus_status__{camera_id}",  # nosec B108
        ]
        removed = 0
        for pattern in patterns:
            for path in glob.glob(pattern):
                try:
                    os.remove(path)
                    removed += 1
                except OSError as e:
                    logger.warning(f"Failed to remove stale SHM {path} for {camera_id}: {e}")
        if removed:
            logger.info(f"Cleaned {removed} stale SHM file(s) for camera {camera_id} before hot-add")

    def _ensure_command_queue(self, gpu_id: int) -> Optional[mp.Queue]:
        """Return the persistent command queue for a GPU, creating one if needed.

        Queues are shared across worker respawns so any command put before
        a watchdog respawn is still consumed by the new worker (which inherits
        the same queue object on next _start_gpu_worker call).
        """
        if self._mp_ctx is None:
            return None
        q = self._gpu_command_queues.get(gpu_id)
        if q is None:
            q = self._mp_ctx.Queue()
            self._gpu_command_queues[gpu_id] = q
        return q

    def _warmup_cupy_kernels(self) -> None:
        """Pre-warm CuPy kernel cache on all GPUs.

        CuPy compiles CUDA kernels on first use via NVRTC. If multiple worker
        processes compile simultaneously, they race on the kernel cache dir
        and some may crash. Warming up here (single-threaded) ensures the
        compiled kernels are cached before any worker starts.
        """
        try:
            import cupy as _cp

            from .nvdec import _get_nv12_resize_kernel

            for _gpu_id in range(self.num_gpus):
                try:
                    _cp.cuda.Device(_gpu_id).use()
                    _get_nv12_resize_kernel()
                    _cp.get_default_memory_pool().free_all_blocks()
                except Exception as _e:
                    logger.warning(f"CuPy warm-up failed on GPU {_gpu_id}: {_e}")
            logger.info(f"CuPy kernel cache warmed on {self.num_gpus} GPUs (incl. nv12_resize)")
        except ImportError:
            logger.debug("CuPy not available, skipping kernel warm-up")

    def start(self) -> None:
        """Start NVDEC worker processes (one per GPU).

        Initializes shared multiprocessing primitives and starts a worker
        process for each GPU that has cameras assigned. If no cameras are
        configured, primitives are still created so that later add_camera
        calls can schedule per-GPU starts without a full restart.
        """
        if self._is_running:
            logger.warning("NVDECWorkerManager is already running")
            return

        # Auto-clean stale SHM files from previous runs
        self._clean_stale_shm()

        self._mp_ctx = mp.get_context("spawn")
        self._result_queue = self._mp_ctx.Queue()
        self._shared_frame_count = self._mp_ctx.Value("L", 0)
        self._start_time = time.perf_counter()

        # Single status queue shared by every GPU worker (step 1-4 in fix plan).
        self._worker_status_queue = self._mp_ctx.Queue()

        # Pre-create persistent command queues for every GPU (step 6 in fix
        # plan). Doing this here means the queue object is stable for the life
        # of the manager — watchdog respawns reuse the same queue.
        for gpu_id in range(self.num_gpus):
            self._ensure_command_queue(gpu_id)

        # Pre-create per-GPU frame counters for all GPUs
        for gpu_id in range(self.num_gpus):
            self._gpu_frame_counts[gpu_id] = self._mp_ctx.Value("L", 0)

        # GpuCameraMap removed: decode/inference GPUs are decoupled, so the IE
        # no longer needs a camera->GPU map to know where to attach (it reads
        # the producer GPU from each ring-buffer header and peer-copies). The SG
        # still decodes each camera on a GPU (chosen by _get_gpu_for_camera's
        # deterministic hash) but publishes no map. _gpu_map stays None so the
        # (kept-for-reference) write/sweep sites all no-op.

        # Initialize GlobalFrameCounter in main process before spawning workers
        self._global_frame_counter = GlobalFrameCounter(is_producer=True)
        if not self._global_frame_counter.initialize():
            raise RuntimeError("Failed to initialize GlobalFrameCounter")
        logger.info("GlobalFrameCounter initialized in main process")

        self._warmup_cupy_kernels()

        if not self._stream_configs:
            logger.info("No cameras configured, NVDEC infrastructure ready for dynamic camera addition")
        else:
            total_num_gpus = len([g for g in range(self.num_gpus) if self._gpu_camera_assignments[g]])
            logger.info(f"Starting NVDEC: {len(self._stream_configs)} cameras across {total_num_gpus} GPUs")

            for gpu_id in range(self.num_gpus):
                if self._gpu_camera_assignments[gpu_id]:
                    self._start_gpu_worker(gpu_id)

        self._is_running = True
        logger.info(f"NVDECWorkerManager started: {len(self._gpu_workers)} GPU workers active")

        # Start watchdog thread to detect dead OR stuck GPU workers.
        self._watchdog_stop = threading.Event()
        self._watchdog_thread = threading.Thread(target=self._worker_watchdog, daemon=True, name="WorkerWatchdog")
        self._watchdog_thread.start()

        # Start status drainer to consume producer_ready / add_failed messages
        # pushed by GPU workers (step 1-2 in fix plan).
        self._status_drain_stop = threading.Event()
        self._status_drain_thread = threading.Thread(
            target=self._drain_worker_status,
            daemon=True,
            name="NVDECStatusDrain",
        )
        self._status_drain_thread.start()

    @staticmethod
    def _format_exit_signal(exit_code: Optional[int]) -> str:
        """Format process exit code with signal name if applicable."""
        if exit_code is None or exit_code >= 0:
            return ""
        import signal as _sig

        try:
            return f" ({_sig.Signals(-exit_code).name})"
        except (ValueError, AttributeError):
            return f" (signal {-exit_code})"

    def _breaker_parks_gpu(self, gpu_id: int, now: float, cameras: int) -> bool:
        """True if the restart breaker is currently holding this GPU back.

        Three behaviours the old ``if gpu_id in self._gpu_circuit_tripped: continue``
        did not have:

        * **It expires.** After ``CIRCUIT_BREAKER_COOLDOWN_SEC`` the park lifts by
          itself and restarts resume, so a GPU is never abandoned for the life of
          the process. The breaker's job is to stop a 120s restart *thrash* -- each
          one wipes SHM for every camera on the GPU -- not to stop trying.
        * **It says so.** A parked GPU logs a WARNING every
          ``CIRCUIT_BREAKER_WARN_INTERVAL_SEC`` carrying how long it has been dark,
          how many cameras are on it, and when the next attempt is due. Previously
          the park emitted one ERROR and then nothing at all.
        * **It clears its strikes on re-arm**, so the next trip needs a fresh run of
          ``CIRCUIT_BREAKER_MAX_RESTARTS`` rather than tripping again on the first
          stall because the old timestamps were still inside the window.
        """
        if gpu_id not in self._gpu_circuit_tripped:
            return False

        parked_at = self._gpu_circuit_tripped_at.get(gpu_id)
        if parked_at is None:
            # Parked by an older code path (or a test) that recorded no timestamp:
            # anchor it now rather than parking it forever, which is the bug this
            # method exists to remove.
            parked_at = now
            self._gpu_circuit_tripped_at[gpu_id] = now

        parked_for = now - parked_at
        if parked_for >= CIRCUIT_BREAKER_COOLDOWN_SEC:
            self._gpu_circuit_tripped.discard(gpu_id)
            self._gpu_circuit_tripped_at.pop(gpu_id, None)
            self._gpu_circuit_last_warn.pop(gpu_id, None)
            self._gpu_restart_history.pop(gpu_id, None)
            logger.warning(
                "Watchdog: GPU %s restart breaker re-armed by itself after %.0fs parked "
                "(%d camera(s)); resuming restart attempts.",
                gpu_id,
                parked_for,
                cameras,
            )
            return False

        last_warn = self._gpu_circuit_last_warn.get(gpu_id, 0.0)
        if now - last_warn >= CIRCUIT_BREAKER_WARN_INTERVAL_SEC:
            self._gpu_circuit_last_warn[gpu_id] = now
            logger.warning(
                "Watchdog: GPU %s still parked by the restart breaker - dark %.0fs, "
                "%d camera(s) affected, next restart attempt in %.0fs. "
                "Investigate the root cause (slow RTSP source? NVDEC saturation? "
                "stale declared resolution? driver wedge?).",
                gpu_id,
                parked_for,
                cameras,
                CIRCUIT_BREAKER_COOLDOWN_SEC - parked_for,
            )
        return True

    def _breaker_admit_restart(self, gpu_id: int, now: float, cameras: int, kind: str) -> Optional[int]:
        """May the watchdog restart this GPU right now? Returns the attempt number.

        ``None`` means no: either the breaker already has the GPU parked (see
        ``_breaker_parks_gpu``), or this attempt would exceed
        ``CIRCUIT_BREAKER_MAX_RESTARTS`` inside ``CIRCUIT_BREAKER_WINDOW_SEC``, in
        which case the GPU is parked here. Restarting is expensive -- each one wipes
        the SHM segments of every camera on the GPU and cascades reconnects on the
        inference side -- so a GPU that stays stuck through repeated restarts is
        slowed to one attempt per cooldown rather than thrashed. It is never
        abandoned: the park expires by itself.

        Shared by both watchdog paths (a wedged command handler and a stalled frame
        counter), which previously carried near-identical copies of this budget logic
        and could therefore drift apart.
        """
        if self._breaker_parks_gpu(gpu_id, now, cameras):
            return None
        history = self._gpu_restart_history.setdefault(gpu_id, [])
        cutoff = now - CIRCUIT_BREAKER_WINDOW_SEC
        history[:] = [ts for ts in history if ts >= cutoff]
        if len(history) >= CIRCUIT_BREAKER_MAX_RESTARTS:
            self._gpu_circuit_tripped.add(gpu_id)
            self._gpu_circuit_tripped_at[gpu_id] = now
            logger.error(
                f"Watchdog: GPU {gpu_id} {kind} restart circuit breaker TRIPPED after "
                f"{len(history)} restarts in {CIRCUIT_BREAKER_WINDOW_SEC:.0f}s "
                f"({cameras} cameras assigned). Slowing to one attempt every "
                f"{CIRCUIT_BREAKER_COOLDOWN_SEC:.0f}s - retries continue and each is logged; "
                f"investigate the root cause (slow RTSP source? NVDEC saturation? stale "
                f"declared resolution? driver wedge?)."
            )
            return None
        history.append(now)
        return len(history)

    def _reset_restart_circuit_breakers(self, reason: str) -> None:
        """Re-arm every parked GPU, because the inputs just changed.

        A config rebuild is an operator action -- an add, a remove, an update, a
        corrected resolution. The breaker's premise ("stuck for hours despite
        repeated restarts, so stop thrashing it") no longer holds against inputs
        that just changed, so release it rather than making the operator wait out
        the cooldown. Before this existed there was no reset path at all: a
        corrected config could not revive a parked GPU and only a gateway restart
        would.

        Also clears the restart history, so the next trip needs a fresh
        CIRCUIT_BREAKER_MAX_RESTARTS run rather than inheriting old strikes.
        """
        tripped = sorted(self._gpu_circuit_tripped)
        self._gpu_circuit_tripped.clear()
        self._gpu_circuit_tripped_at.clear()
        self._gpu_circuit_last_warn.clear()
        self._gpu_restart_history.clear()
        if tripped:
            logger.warning(
                "Watchdog: restart circuit breaker re-armed for GPU(s) %s (%s). "
                "Restart attempts resume at the normal cadence.",
                tripped,
                reason,
            )

    def _worker_watchdog(self) -> None:
        """Periodically check for dead OR stuck-but-alive GPU workers.

        A worker is "stuck-but-alive" if it has cameras assigned but its
        per-GPU frame counter has not advanced for FRAME_STALL_THRESHOLD_SEC.
        Stuck workers are restarted just like dead ones — pure liveness
        (worker.is_alive()) is not sufficient because a hung GStreamer
        subprocess demuxer or wedged NVC.Demux() leaves the process
        technically alive while producing zero frames.
        """
        while not self._watchdog_stop.is_set():
            self._watchdog_stop.wait(5.0)
            if self._watchdog_stop.is_set():
                break
            now = time.time()
            for gpu_id in range(self.num_gpus):
                if not self._gpu_camera_assignments.get(gpu_id):
                    continue
                p = self._gpu_workers.get(gpu_id)

                # Dead-worker path (existing behaviour).
                if p is None or not p.is_alive():
                    exit_code = p.exitcode if p is not None else None
                    signal_name = self._format_exit_signal(exit_code)
                    logger.warning(f"Watchdog: GPU {gpu_id} worker died (exit={exit_code}{signal_name}), restarting")
                    # Signal any decode sub-processes orphaned by the dead
                    # orchestrator to stop (they watch this shared event via
                    # _AnyStop) so they stop writing their SHM before the
                    # replacement spawns on the same segments — prevents the
                    # duplicate-producer split brain. They close but do NOT unlink
                    # (unlink is REMOVE-only), so the segments are cleanly reused.
                    _old_stop = self._gpu_stop_events.get(gpu_id)
                    if _old_stop is not None:
                        try:
                            _old_stop.set()
                        except Exception:  # nosec B110
                            pass
                    self._gpu_workers.pop(gpu_id, None)
                    self._gpu_stop_events.pop(gpu_id, None)
                    self._handler_last_seen.pop(gpu_id, None)
                    # Persistent queue preserved (step 6).
                    self._start_gpu_worker(gpu_id)
                    continue

                # Handler-wedge path: the process is alive (and frames may still
                # be advancing for existing cameras), but the command handler
                # stopped consuming commands, so add/remove/update silently wedge.
                # Detect via the handler_alive heartbeat and restart to recover.
                last_hb = self._handler_last_seen.get(gpu_id)
                if last_hb is not None and (time.monotonic() - last_hb) > HANDLER_STALE_SEC:
                    cameras = len(self._gpu_camera_assignments.get(gpu_id, []))
                    attempt = self._breaker_admit_restart(gpu_id, now, cameras, "handler-wedge")
                    if attempt is None:
                        continue
                    logger.warning(
                        f"Watchdog: GPU {gpu_id} command-handler heartbeat stale "
                        f"({time.monotonic() - last_hb:.0f}s > {HANDLER_STALE_SEC:.0f}s) while the "
                        f"process is alive — handler wedged; restarting worker."
                    )
                    self._stop_gpu_worker(gpu_id, timeout=5.0)
                    self._handler_last_seen.pop(gpu_id, None)
                    self._start_gpu_worker(gpu_id)
                    continue

                # Stuck-but-alive path (step 7).
                counter = self._gpu_frame_counts.get(gpu_id)
                current = counter.value if counter is not None else 0
                prev = self._gpu_last_frame_count.get(gpu_id, current)
                if current != prev:
                    self._gpu_last_frame_count[gpu_id] = current
                    self._gpu_last_advance_at[gpu_id] = now
                    continue
                stuck_for = now - self._gpu_last_advance_at.get(gpu_id, now)
                if stuck_for > FRAME_STALL_THRESHOLD_SEC:
                    # Restarting is expensive: each one blows away all SHM files for
                    # cameras on this GPU and triggers a cascade of reconnects on the
                    # IE side. The breaker slows a persistently-stuck GPU to one
                    # attempt per cooldown -- it no longer abandons it.
                    cameras = len(self._gpu_camera_assignments.get(gpu_id, []))
                    attempt = self._breaker_admit_restart(gpu_id, now, cameras, "frame-stall")
                    if attempt is None:
                        continue
                    logger.warning(
                        f"Watchdog: GPU {gpu_id} worker alive but frame counter "
                        f"has not advanced for {stuck_for:.0f}s "
                        f"({cameras} cameras assigned). Restarting (attempt "
                        f"{attempt}/{CIRCUIT_BREAKER_MAX_RESTARTS} in "
                        f"{CIRCUIT_BREAKER_WINDOW_SEC:.0f}s window)."
                    )
                    self._stop_gpu_worker(gpu_id, timeout=5.0)
                    self._start_gpu_worker(gpu_id)

                    # Fix C — Re-publish full camera->GPU map after a stuck
                    # worker restart so the IE side doesn't see slow drift.
                    if self._gpu_map is not None:
                        try:
                            mappings = {sc.camera_id: sc.gpu_id for sc in self._stream_configs}
                            if mappings:
                                self._gpu_map.set_bulk_mapping(mappings)
                        except Exception as e:  # noqa: BLE001
                            logger.warning(
                                f"Watchdog: failed to republish GpuCameraMap after GPU {gpu_id} restart: {e}"
                            )

    # ========================================================================
    # Worker → manager status protocol (step 1-2 in fix plan)
    # ========================================================================

    def set_on_camera_failed(self, callback: Optional[Callable[[str, str], None]]) -> None:
        """Register a callback invoked when a worker reports add_failed.

        The callback receives (camera_id, reason) and is expected to drop
        the phantom camera from the upstream DynamicCameraManager so the
        next periodic refresh can retry the add cleanly.
        """
        self._on_camera_failed = callback

    def _arm_pending_add(self, camera_id: str) -> None:
        """Create/replace pending add state before sending worker command.

        This avoids a race where a very fast worker can emit producer_ready
        before add_camera()/update_camera() enters _wait_for_producer_ready().
        """
        with self._pending_adds_lock:
            self._pending_adds[camera_id] = {
                "event": threading.Event(),
                "result": None,
                "reason": None,
            }

    def _arm_pending_remove(self, camera_id: str) -> None:
        """Create/replace pending-remove state before sending the REMOVE command.

        Mirrors _arm_pending_add so a fast worker's "removed" ACK is not lost in
        the window before remove_camera() enters _wait_for_removed().
        """
        with self._pending_removes_lock:
            self._pending_removes[camera_id] = {"event": threading.Event()}

    def _drain_worker_status(self) -> None:
        """Consume producer_ready / add_failed messages from worker processes.

        - producer_ready[camera_id] → set the pending-add event with "ready";
          if no add is pending (e.g. initial-startup camera), just record it
          for the GpuCameraMap update below.
        - add_failed[camera_id] → set the pending-add event with "failed";
          if no add is pending (silent late failure of an already-active
          camera), invoke _on_camera_failed and unregister the camera so the
          next periodic refresh retries it.
        """
        stop_event = self._status_drain_stop
        if stop_event is None:
            return
        while not stop_event.is_set():
            q = self._worker_status_queue
            if q is None:
                stop_event.wait(0.5)
                continue
            try:
                msg = q.get(timeout=0.5)
            except Exception:  # nosec B110 B112 - drain Empty/EOFError/OSError
                continue
            try:
                self._handle_worker_status(msg)
            except Exception as e:
                logger.exception(f"Status drain: failed to process {msg!r}: {e}")

    def _handle_worker_status(self, msg: Dict[str, Any]) -> None:
        msg_type = msg.get("type")

        # Handler liveness heartbeat carries no camera_id — handle it before the
        # cam-id guard below.
        if msg_type == "handler_alive":
            gpu_id = msg.get("gpu_id")
            if gpu_id is not None:
                self._handler_last_seen[gpu_id] = time.monotonic()
            return

        cam_id = msg.get("camera_id")
        if not cam_id:
            return

        if msg_type == "removed":
            with self._pending_removes_lock:
                entry = self._pending_removes.get(cam_id)
                if entry is not None:
                    entry["event"].set()
            logger.info(f"Camera {cam_id}: worker ACKed removed (owned={msg.get('owned')})")
            return

        if msg_type == "producer_ready":
            gpu_id = msg.get("gpu_id")
            with self._pending_adds_lock:
                entry = self._pending_adds.get(cam_id)
                has_pending = entry is not None
                if entry is not None:
                    entry["result"] = "ready"
                    entry["event"].set()
            # S9 reconciliation: a producer_ready with NO pending add AND no
            # tracked GPU assignment means the manager already timed out and
            # rolled this camera back, but the worker produced a live producer
            # anyway (a post-timeout ACK). Do not leave it orphaned/untracked —
            # send an explicit REMOVE so the worker tears it down.
            if not has_pending and cam_id not in self._camera_to_gpu:
                logger.warning(
                    f"Camera {cam_id}: producer_ready with no pending add and not tracked "
                    f"(post-timeout orphan) — sending reconcile REMOVE to GPU {gpu_id}"
                )
                if gpu_id is not None:
                    try:
                        self._send_worker_command(gpu_id, {"type": "remove", "camera_id": cam_id})
                    except Exception as e:
                        logger.warning(f"Failed to send reconcile-REMOVE for {cam_id}: {e}")
                return
            # Publish the GpuCameraMap entry only now that the producer
            # actually exists (step 3 in fix plan).
            if gpu_id is not None and self._gpu_map is not None and (has_pending or cam_id in self._camera_to_gpu):
                try:
                    self._gpu_map.set_bulk_mapping({cam_id: gpu_id})
                except Exception as e:
                    logger.warning(f"Failed to publish GpuCameraMap for {cam_id}: {e}")
            logger.info(f"Camera {cam_id}: producer_ready on GPU {gpu_id}")
            return

        if msg_type == "add_failed":
            reason = msg.get("reason", "unknown")
            with self._pending_adds_lock:
                entry = self._pending_adds.get(cam_id)
                if entry is not None:
                    entry["result"] = "failed"
                    entry["reason"] = reason
                    entry["event"].set()
                    return
            # Late failure: a previously-ready camera reported add_failed
            # while in steady state. Tear it down so the next refresh retries.
            logger.error(
                f"Camera {cam_id}: worker reported late add_failed ({reason}); unregistering and notifying DCM"
            )
            self._unregister_failed_camera(cam_id, reason)

    def _teardown_worker_side_camera(self, camera_id: str, reason: str) -> None:
        """Tell the GPU worker to drop ``camera_id``, then evict its mapping.

        MUST run before the manager forgets its own state, because the GPU id is
        read from ``_camera_to_gpu``, which the caller is about to clear.

        Without this the sub-process keeps the camera, its NVDEC slot and its
        GStreamer demuxer alive while the manager believes the camera is gone — a
        split brain the manager cannot escape:

          * the worker's command handler short-circuits the next ADD on
            ``sub_registry.owner_for(cam) is not None`` and replies
            ``producer_ready(already_running=True)``, so the manager is ACKed for
            a producer it does not know about, and
          * the next hot-add's pre-add SHM sweep unlinks the segment that live
            worker is still writing.

        That is the observed "SG logs 20 FPS while inference sees No such file or
        directory" state, which previously needed a full SG restart to clear.
        ``remove_camera`` has always done this on the graceful path; the failure
        path simply never did.
        """
        gpu_id = self._camera_to_gpu.get(camera_id)
        if gpu_id is not None and self._is_running:
            if self._send_worker_command(gpu_id, {"type": "remove", "camera_id": camera_id}):
                logger.info(f"Camera {camera_id} → REMOVE sent to GPU {gpu_id} worker (rollback: {reason})")
            else:
                logger.warning(f"Camera {camera_id}: GPU {gpu_id} worker not running during rollback ({reason})")
        elif gpu_id is None:
            logger.debug(f"Camera {camera_id}: no GPU assignment to tear down ({reason})")

        # Explicitly evict the GpuCameraMap entry, as remove_camera does. The
        # set_bulk_mapping() rewrite below merges and would leave the stale key
        # behind, so IE consumers would keep retrying a camera with no producer.
        self.evict_camera_mapping(camera_id, reason=f"add_failed:{reason}")

    def _unregister_failed_camera(self, camera_id: str, reason: str) -> None:
        """Drop a failed camera from internal state and notify DCM.

        Runs on the status-drain thread, so the config mutations are serialized
        under ``_config_lock`` against a concurrent main-thread add/remove. The
        DCM callback is invoked OUTSIDE the lock: it may take DCM._lock, and the
        ordering is DCM._lock → _config_lock, so calling it while holding
        _config_lock could deadlock.
        """
        with self._config_lock:
            # Tear the WORKER-side camera down FIRST — while _camera_to_gpu still
            # holds its GPU assignment. See _teardown_worker_side_camera.
            self._teardown_worker_side_camera(camera_id, reason)

            # Remove from local config / assignment dicts.
            self.camera_configs = [
                c for c in self.camera_configs if (c.get("camera_id") or c.get("stream_key")) != camera_id
            ]
            self._camera_to_gpu.pop(camera_id, None)
            # Re-prepare so _stream_configs / _gpu_camera_assignments are consistent.
            try:
                self._prepare_camera_configs()
            except Exception as e:
                logger.warning(f"_prepare_camera_configs after failure cleanup raised: {e}")
            # Clear from GpuCameraMap.
            if self._gpu_map is not None:
                try:
                    mappings = {cfg.camera_id: cfg.gpu_id for cfg in self._stream_configs}
                    self._gpu_map.set_bulk_mapping(mappings)
                except Exception as e:
                    logger.warning(f"Failed to rewrite GpuCameraMap after failure: {e}")

        # Notify DCM so the upstream `cameras` dict and stats are reconciled.
        # OUTSIDE _config_lock to avoid a DCM._lock ↔ _config_lock inversion.
        cb = self._on_camera_failed
        if cb is not None:
            try:
                cb(camera_id, reason)
            except Exception as e:
                logger.exception(f"on_camera_failed callback raised for {camera_id}: {e}")

    def _classify_producer_ready_failure(self, camera_id: str, reason: str) -> str:
        """Fix D — classify producer_ready timeouts for actionable logs."""
        reason_lower = (reason or "").lower()
        if "decoder" in reason_lower or "nvdec" in reason_lower:
            return "nvdec_init_failed"
        try:
            import json as _json
            import urllib.request

            # nosec B310 - hardcoded http://localhost MediaMTX broker URL on
            # the same host network; not user-controlled, scheme is fixed http.
            with urllib.request.urlopen(  # nosec B310
                f"http://localhost:9997/v3/paths/get/{camera_id}",
                timeout=2.0,  # NOSONAR S5332: fixed internal loopback MediaMTX API, not user-controlled, scheme fixed http
            ) as r:
                info = _json.loads(r.read())
            if not info.get("ready"):
                return "mediamtx_path_idle"
            if info.get("bytesReceived", 0) == 0:
                return "mediamtx_path_idle"
            return "unknown"
        except Exception as e:
            msg = str(e).lower()
            if "404" in msg or "path not found" in msg:
                return "mediamtx_path_missing"
            return "mediamtx_unreachable"

    def _wait_for_producer_ready(
        self,
        camera_id: str,
        timeout: float = PRODUCER_READY_TIMEOUT_SEC,
    ) -> Tuple[bool, Optional[str]]:
        """Block until the GPU worker ACKs producer_ready for camera_id.

        Returns (ok, reason). On timeout the pending entry is removed and
        the camera is treated as failed.
        """
        with self._pending_adds_lock:
            entry = self._pending_adds.get(camera_id)
            if entry is None:
                entry = {"event": threading.Event(), "result": None, "reason": None}
                self._pending_adds[camera_id] = entry

        event = entry["event"]
        signalled = event.wait(timeout=timeout)
        with self._pending_adds_lock:
            popped = self._pending_adds.pop(camera_id, entry)
        if not signalled:
            return False, f"producer_ready timeout after {timeout:.0f}s"
        if popped.get("result") == "ready":
            return True, None
        return False, popped.get("reason") or "unknown failure"

    def _wait_for_removed(self, camera_id: str, timeout: float = REMOVE_ACK_TIMEOUT_SEC) -> bool:
        """Block until the GPU worker ACKs 'removed' for camera_id.

        Best-effort: returns True if the ACK arrived within ``timeout``, else
        False (the caller falls back to its SHM backstop). The pending entry is
        always cleared.
        """
        with self._pending_removes_lock:
            entry = self._pending_removes.get(camera_id)
            if entry is None:
                entry = {"event": threading.Event()}
                self._pending_removes[camera_id] = entry
        signalled = entry["event"].wait(timeout=timeout)
        with self._pending_removes_lock:
            self._pending_removes.pop(camera_id, None)
        return signalled

    def stop(self, timeout: float = 15.0) -> None:
        """Stop all worker processes and cancel any pending restart.

        Args:
            timeout: Maximum time to wait for each worker to stop gracefully
        """
        if not self._is_running:
            logger.warning("NVDECWorkerManager is not running")
            return

        logger.info("Stopping NVDECWorkerManager...")

        # Stop watchdog
        if hasattr(self, "_watchdog_stop"):
            self._watchdog_stop.set()
        # Stop status drainer
        if self._status_drain_stop is not None:
            self._status_drain_stop.set()

        # Cancel any pending debounced restart
        with self._restart_lock:
            if self._restart_timer is not None:
                self._restart_timer.cancel()
                self._restart_timer = None
            self._gpus_needing_restart.clear()

        # Wake any pending add_camera() waiters so they unblock with a failure.
        with self._pending_adds_lock:
            for cam_id, entry in list(self._pending_adds.items()):
                entry["result"] = "failed"
                entry["reason"] = "manager stopping"
                entry["event"].set()
            self._pending_adds.clear()

        # Stop all GPU workers
        for gpu_id in list(self._gpu_workers.keys()):
            self._stop_gpu_worker(gpu_id, timeout)

        self._gpu_command_queues.clear()
        self._worker_status_queue = None
        self._is_running = False
        logger.info("NVDECWorkerManager stopped")

    def restart_workers(self) -> None:
        """Full restart of all workers (stops everything, then starts fresh).

        This is the heavy-weight approach. Prefer add_camera/remove_camera/update_camera
        which use smart per-GPU restarts with debouncing.
        """
        self.stop()
        self.start()

    # ========================================================================
    # Dynamic Camera Management (smart per-GPU restarts)
    # ========================================================================

    def _send_worker_command(self, gpu_id: int, command: dict) -> bool:
        """Send a command to a running GPU worker via IPC queue.

        Returns True if the command was sent, False if the worker is not running.
        """
        cmd_queue = self._gpu_command_queues.get(gpu_id)
        worker = self._gpu_workers.get(gpu_id)
        if cmd_queue is not None and worker is not None and worker.is_alive():
            cmd_queue.put(command)
            return True
        return False

    def add_camera(self, camera_config: Dict[str, Any]) -> bool:
        """Add a new camera at runtime via IPC command to the GPU worker.

        Args:
            camera_config: Camera configuration dict

        Returns:
            True if the camera was accepted
        """
        camera_id = camera_config.get("camera_id") or camera_config.get("stream_key")
        if not camera_id:
            logger.error("Camera config missing camera_id/stream_key")
            return False

        if camera_id in self._camera_to_gpu:
            logger.debug(f"Camera {camera_id} already exists in NVDEC config, skipping add")
            return False

        with self._config_lock:
            self.camera_configs.append(camera_config)
            self._prepare_camera_configs()
        # NOTE: do NOT publish to GpuCameraMap yet — the producer SHM does
        # not exist until the worker emits producer_ready (drain thread
        # handles it). Optimistic mapping was the phantom-camera root cause
        # in the production repro.

        if not self._is_running:
            logger.info(f"Camera {camera_id} added to config (manager not yet started)")
            return True

        gpu_id = self._camera_to_gpu.get(camera_id)
        if gpu_id is None:
            logger.error(f"Camera {camera_id} not assigned to any GPU after prepare")
            return False

        # Find the StreamConfig for this camera
        stream_config = None
        for sc in self._gpu_camera_assignments.get(gpu_id, []):
            if sc.camera_id == camera_id:
                stream_config = sc
                break

        if stream_config is None:
            logger.error(f"Camera {camera_id} StreamConfig not found for GPU {gpu_id}")
            return False

        # Attempt the ADD -> producer_ready handshake up to HOTADD_MAX_ATTEMPTS
        # times. A transient RTSP blip (media server mid-bounce, source slow to
        # re-open) should cost a retry, not the camera.
        reason: Optional[str] = None
        ok = False
        for attempt in range(1, HOTADD_MAX_ATTEMPTS + 1):
            if attempt > 1:
                # A retry MUST start from a clean worker-side slate. Without this
                # the worker still owns the camera from the failed attempt, so the
                # next ADD short-circuits on `owner_for(cam) is not None` and ACKs
                # a producer whose SHM the pre-add sweep is about to unlink.
                self._teardown_worker_side_camera(camera_id, f"retry {attempt}/{HOTADD_MAX_ATTEMPTS}")
                if HOTADD_RETRY_BACKOFF_SEC > 0:
                    time.sleep(HOTADD_RETRY_BACKOFF_SEC)
                # The teardown above dropped the GPU mapping; restore it so the
                # retry targets the same GPU (stickiness) and the StreamConfig
                # stays valid.
                self._camera_to_gpu[camera_id] = gpu_id

            # Clean any orphaned SHM file from a previous incarnation of this
            # camera ID so the producer create in the sub-process doesn't race
            # on unlink/open/ftruncate (step 5 in fix plan). Live segments are
            # left alone — see _clean_stale_shm_for.
            self._clean_stale_shm_for(camera_id)
            self._arm_pending_add(camera_id)

            if self._send_worker_command(gpu_id, {"type": "add", "config": stream_config}):
                logger.info(
                    f"Camera {camera_id} → ADD command queued for GPU {gpu_id} worker "
                    f"(attempt {attempt}/{HOTADD_MAX_ATTEMPTS})"
                )
            else:
                # No running worker — start one with full config.
                self._start_gpu_worker(gpu_id)
                logger.info(
                    f"Camera {camera_id}: started new GPU {gpu_id} worker (attempt {attempt}/{HOTADD_MAX_ATTEMPTS})"
                )

            ok, reason = self._wait_for_producer_ready(camera_id)
            if ok:
                if attempt > 1:
                    logger.info(f"Camera {camera_id}: hot-add succeeded on attempt {attempt}")
                break
            logger.warning(
                f"Camera {camera_id}: producer_ready NOT received on attempt {attempt}/{HOTADD_MAX_ATTEMPTS} ({reason})"
            )

        # All attempts exhausted: treat the camera as failed and roll back local
        # state so the caller sees a clean False and the periodic refresh can
        # retry (step 3 in fix plan).
        if not ok:
            classification = self._classify_producer_ready_failure(camera_id, reason or "")
            logger.error(
                f"Camera {camera_id}: producer_ready NOT received after "
                f"{HOTADD_MAX_ATTEMPTS} attempt(s) ({reason}); "
                f"classification={classification}; rolling back hot-add"
            )
            self._unregister_failed_camera(camera_id, reason or "unknown")
            return False
        return True

    def remove_camera(self, stream_key: str) -> bool:
        """Remove a camera at runtime via IPC command to the GPU worker.

        Args:
            stream_key: Camera ID / stream key to remove

        Returns:
            True if the removal was effected (worker ACKed, or nothing was
            running to stop). False only if the command was sent but the worker
            did not ACK within the timeout — DCM then keeps the camera and the
            next refresh retries, which self-heals (the retry no-ops and ACKs).
        """
        # Capture the GPU assignment BEFORE dropping from config, then mutate the
        # config under _config_lock (serialized vs the status-drain/watchdog).
        with self._config_lock:
            old_gpu_id = self._camera_to_gpu.get(stream_key)

            found = False
            for i, config in enumerate(self.camera_configs):
                cid = config.get("camera_id") or config.get("stream_key")
                if cid == stream_key:
                    del self.camera_configs[i]
                    found = True
                    break

            if not found:
                logger.warning(f"Camera {stream_key} not found in NVDEC config")
                return False

            self._prepare_camera_configs()

        if not self._is_running:
            logger.info(f"Camera {stream_key} removed from config (manager not yet started)")
            return True

        # Send REMOVE and wait for the worker's "removed" ACK so we do not
        # blind-return success while the decoder keeps running.
        sent = False
        acked = False
        if old_gpu_id is not None:
            self._arm_pending_remove(stream_key)
            sent = self._send_worker_command(old_gpu_id, {"type": "remove", "camera_id": stream_key})
            if sent:
                logger.info(f"Camera {stream_key} → REMOVE command sent to GPU {old_gpu_id} worker")
                acked = self._wait_for_removed(stream_key)
                if not acked:
                    logger.warning(
                        f"Camera {stream_key}: no 'removed' ACK from GPU {old_gpu_id} within "
                        f"{REMOVE_ACK_TIMEOUT_SEC:.0f}s"
                    )
            else:
                logger.warning(f"Camera {stream_key}: GPU {old_gpu_id} worker not running")
                with self._pending_removes_lock:
                    self._pending_removes.pop(stream_key, None)
        else:
            logger.warning(f"Camera {stream_key}: no GPU assignment recorded; nothing to REMOVE")

        # Explicitly evict the stale GpuCameraMap + placement-registry entry
        # for the removed camera so IE consumers don't keep retrying a cam
        # that no longer has a producer (issue #5: graceful removal).
        # set_bulk_mapping below merges and would leave stale keys behind.
        self.evict_camera_mapping(stream_key, reason="remove_camera")

        if self._gpu_map is not None:
            mappings = {cfg.camera_id: cfg.gpu_id for cfg in self._stream_configs}
            self._gpu_map.set_bulk_mapping(mappings)

        # Backstop: reap a genuinely-orphaned SHM segment. _clean_stale_shm_for
        # refuses to unlink a segment a live process still holds, so this is safe
        # and only covers a sub that was SIGKILLed after the terminate grace
        # before it could self-clean.
        try:
            self._clean_stale_shm_for(stream_key)
        except Exception as e:
            logger.debug(f"remove_camera SHM backstop for {stream_key} failed: {e}")

        # Truthful outcome. Nothing to stop (no GPU / dead worker) counts as
        # removed; a sent-but-unacked removal returns False so DCM retries.
        if old_gpu_id is None or not sent:
            return True
        return acked

    @staticmethod
    def _stream_config_materially_equal(a, b) -> bool:
        """True if two StreamConfigs are equivalent for decoding, i.e. a runtime
        UPDATE between them needs no producer teardown/respawn. Compares only the
        fields that affect the decode pipeline / CUDA-IPC ring buffer (source,
        geometry, codec, demuxer, fps, GPU); metadata-only changes are no-ops."""
        for f in (
            "video_path",
            "width",
            "height",
            "codec",
            "demuxer_type",
            "target_fps",
            "gpu_id",
        ):
            if getattr(a, f, None) != getattr(b, f, None):
                return False
        return True

    def update_camera(self, camera_config: Dict[str, Any]) -> bool:
        """Update a camera's configuration at runtime via IPC command.

        Args:
            camera_config: Updated camera configuration dict

        Returns:
            True if the camera was found and updated
        """
        camera_id = camera_config.get("camera_id") or camera_config.get("stream_key")
        if not camera_id:
            logger.error("Camera config missing camera_id/stream_key")
            return False

        # Mutation + rebuild under _config_lock (serialized vs the status-drain
        # / watchdog threads); reads that must be consistent with the rebuild are
        # inside too.
        with self._config_lock:
            found = False
            for i, config in enumerate(self.camera_configs):
                cid = config.get("camera_id") or config.get("stream_key")
                if cid == camera_id:
                    self.camera_configs[i] = camera_config
                    found = True
                    break

            if not found:
                logger.warning(f"Camera {camera_id} not found in NVDEC config for update")
                return False

            old_gpu_id = self._camera_to_gpu.get(camera_id)
            # Capture the currently-running StreamConfig BEFORE reassignment so we
            # can detect a no-op update and avoid a needless producer respawn.
            old_stream_config = None
            for sc in self._gpu_camera_assignments.get(old_gpu_id or 0, []):
                if getattr(sc, "camera_id", None) == camera_id:
                    old_stream_config = sc
                    break
            self._prepare_camera_configs()
            new_gpu_id = self._camera_to_gpu.get(camera_id)

        if not self._is_running:
            logger.info(f"Camera {camera_id} updated in config (manager not yet started)")
            return True

        # Find the new StreamConfig
        stream_config = None
        for sc in self._gpu_camera_assignments.get(new_gpu_id or 0, []):
            if sc.camera_id == camera_id:
                stream_config = sc
                break

        if new_gpu_id is not None and stream_config is None:
            logger.error(f"Camera {camera_id} StreamConfig not found for GPU {new_gpu_id}")
            return False

        if old_gpu_id == new_gpu_id and new_gpu_id is not None:
            # No-op update: nothing the decoder/ring-buffer cares about changed.
            # The update path would otherwise tear down + respawn the per-camera
            # sub-process, recreating the CUDA-IPC ring buffer (new inode/handle,
            # reset counters) and forcing every consumer to reconnect. Skip it.
            if old_stream_config is not None and self._stream_config_materially_equal(old_stream_config, stream_config):
                logger.info(
                    f"Camera {camera_id}: UPDATE is a no-op "
                    f"(source/geometry/codec unchanged) — keeping existing "
                    f"producer, no respawn"
                )
                return True
            # Same GPU — send update command. The update path tears down and
            # respawns the per-camera sub-process inside the worker, so we
            # also wait for producer_ready to confirm the new producer
            # actually came up.
            self._arm_pending_add(camera_id)
            if self._send_worker_command(
                new_gpu_id,
                {"type": "update", "camera_id": camera_id, "config": stream_config},
            ):
                logger.info(f"Camera {camera_id} → UPDATE command sent to GPU {new_gpu_id}")
                ok, reason = self._wait_for_producer_ready(camera_id)
                if not ok:
                    classification = self._classify_producer_ready_failure(camera_id, reason or "")
                    logger.error(
                        f"Camera {camera_id}: producer_ready NOT received after "
                        f"UPDATE ({reason}); classification={classification}; "
                        f"rolling back"
                    )
                    self._unregister_failed_camera(camera_id, reason or "unknown")
                    return False
            else:
                # Worker may have died between diff and send; restart the GPU
                # worker so it picks up the updated full assignment.
                self._start_gpu_worker(new_gpu_id)
                ok, reason = self._wait_for_producer_ready(camera_id)
                if not ok:
                    classification = self._classify_producer_ready_failure(camera_id, reason or "")
                    logger.error(
                        f"Camera {camera_id}: producer_ready NOT received after "
                        f"worker restart ({reason}); classification={classification}; "
                        f"rolling back"
                    )
                    self._unregister_failed_camera(camera_id, reason or "unknown")
                    return False
        else:
            # GPU changed — remove from old, clean stale SHM (the camera is
            # about to be re-created on a different GPU), then add to new.
            if old_gpu_id is not None:
                self._send_worker_command(old_gpu_id, {"type": "remove", "camera_id": camera_id})
            self._clean_stale_shm_for(camera_id)
            if new_gpu_id is not None and stream_config:
                self._arm_pending_add(camera_id)
                if not self._send_worker_command(new_gpu_id, {"type": "add", "config": stream_config}):
                    self._start_gpu_worker(new_gpu_id)
                ok, reason = self._wait_for_producer_ready(camera_id)
                if not ok:
                    classification = self._classify_producer_ready_failure(camera_id, reason or "")
                    logger.error(
                        f"Camera {camera_id}: producer_ready NOT received after "
                        f"GPU change ({reason}); classification={classification}; "
                        f"rolling back"
                    )
                    self._unregister_failed_camera(camera_id, reason or "unknown")
                    return False

        # GpuCameraMap is rewritten by the drain thread on producer_ready
        # for the affected camera(s). Avoid optimistic publishing.

        logger.info(f"Camera {camera_id} updated → GPU(s) {sorted({old_gpu_id, new_gpu_id} - {None})}")
        return True

    # ========================================================================
    # Statistics & Properties
    # ========================================================================

    def _watchdog_stats(self) -> Dict[str, Any]:
        """What the restart watchdog is currently doing, for the stats payload.

        A GPU the breaker has parked used to be visible only in the one ERROR line
        logged at the moment it tripped, so a permanently dark GPU was findable by
        log archaeology and by nothing else. These fields make it alertable: which
        GPUs are parked, how long each has been parked (a number that keeps climbing
        past ``breaker_cooldown_sec`` means genuinely stuck and still being retried,
        not forgotten), how many restarts each GPU has spent in the current window,
        and the thresholds those numbers should be read against.
        """
        now = time.monotonic()
        return {
            "circuit_tripped_gpus": sorted(self._gpu_circuit_tripped),
            "parked_for_sec": {
                gpu_id: round(now - parked_at, 1) for gpu_id, parked_at in sorted(self._gpu_circuit_tripped_at.items())
            },
            "breaker_cooldown_sec": CIRCUIT_BREAKER_COOLDOWN_SEC,
            "restarts_in_window": {
                gpu_id: len(history) for gpu_id, history in sorted(self._gpu_restart_history.items()) if history
            },
            "window_sec": CIRCUIT_BREAKER_WINDOW_SEC,
            "max_restarts": CIRCUIT_BREAKER_MAX_RESTARTS,
        }

    def get_worker_statistics(self) -> Dict[str, Any]:
        """Return statistics from workers.

        Returns:
            Dict with worker count, camera count, FPS metrics, per-GPU stats, etc.
        """
        stats: Dict[str, Any] = {
            "backend": "nvdec",
            "num_workers": len(self._gpu_workers),
            "running_workers": sum(1 for p in self._gpu_workers.values() if p.is_alive()),
            "total_cameras": len(self._stream_configs),
            "gpu_assignments": {gpu_id: len(cameras) for gpu_id, cameras in self._gpu_camera_assignments.items()},
            "nvdec_config": {
                "gpu_id": self.gpu_id,
                "num_gpus": self.num_gpus,
                "pool_size": self.nvdec_pool_size,
                "burst_size": self.nvdec_burst_size,
                "frame_size": f"{self.frame_width}x{self.frame_height}",
                "num_slots": self.num_slots,
                "target_fps": self.target_fps,
                "demuxer_type": self.demuxer_type,
            },
            "watchdog": self._watchdog_stats(),
        }

        # Compute elapsed once for consistent FPS across all stats sections
        elapsed = (time.perf_counter() - self._start_time) if self._start_time else 0.0

        # Add frame count and FPS
        if self._shared_frame_count:
            total_frames = self._shared_frame_count.value  # type: ignore[attr-defined]
            stats["total_frames"] = total_frames

            if self._start_time:
                stats["elapsed_sec"] = elapsed
                stats["aggregate_fps"] = total_frames / elapsed if elapsed > 0 else 0
                stats["per_stream_fps"] = (
                    stats["aggregate_fps"] / len(self._stream_configs)  # type: ignore[operator]
                    if self._stream_configs
                    else 0
                )

        # Add per-GPU frame counts and FPS
        if self._gpu_frame_counts and self._start_time:
            gpu_stats = {}
            for gpu_id, counter in self._gpu_frame_counts.items():
                gpu_frames = counter.value  # type: ignore[attr-defined]
                num_cams = len(self._gpu_camera_assignments.get(gpu_id, []))
                gpu_fps = gpu_frames / elapsed if elapsed > 0 else 0
                gpu_per_cam = gpu_fps / num_cams if num_cams > 0 else 0
                gpu_stats[f"GPU{gpu_id}"] = {
                    "frames": gpu_frames,
                    "cameras": num_cams,
                    "fps": gpu_fps,
                    "fps_per_cam": gpu_per_cam,
                }
            stats["per_gpu_stats"] = gpu_stats

        # Synthesize per_camera_stats from GPU-level metrics so metrics code
        # doesn't need to branch on is_nvdec.
        per_camera_stats: Dict[str, Any] = {}
        if self._start_time:
            # NV12 frame size: width * height * 1.5
            frame_size_bytes = self.frame_width * self.frame_height * 3 // 2
            for gpu_id, cameras in self._gpu_camera_assignments.items():
                num_cams = len(cameras)
                if num_cams == 0:
                    continue
                counter = self._gpu_frame_counts.get(gpu_id) if self._gpu_frame_counts else None
                gpu_frames = counter.value if counter else 0  # type: ignore[attr-defined]
                gpu_fps = gpu_frames / elapsed if elapsed > 0 else 0
                per_cam_fps = gpu_fps / num_cams if num_cams > 0 else 0

                for sc in cameras:
                    per_camera_stats[sc.camera_id] = {
                        "fps": {
                            "min": per_cam_fps,
                            "max": per_cam_fps,
                            "avg": per_cam_fps,
                        },
                        "read_time_ms": {"min": 0, "max": 0, "avg": 0},
                        "write_time_ms": {"min": 0, "max": 0, "avg": 0},
                        "encoding_time_ms": {"min": 0, "max": 0, "avg": 0},
                        "frame_size_bytes": {
                            "min": frame_size_bytes,
                            "max": frame_size_bytes,
                            "avg": frame_size_bytes,
                        },
                    }
        stats["per_camera_stats"] = per_camera_stats

        # Collect any available results from queue (non-blocking)
        gpu_results = []
        if self._result_queue:
            while True:
                try:
                    result = self._result_queue.get_nowait()
                    gpu_results.append(result)
                except Exception:
                    break
        stats["gpu_results"] = gpu_results

        return stats

    def get_camera_assignments(self) -> Dict[str, int]:
        """Return mapping of camera_id to GPU ID.

        Returns:
            Dict mapping camera_id -> gpu_id
        """
        return self._camera_to_gpu.copy()

    @property
    def is_running(self) -> bool:
        """Check if the manager is currently running."""
        return self._is_running

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
