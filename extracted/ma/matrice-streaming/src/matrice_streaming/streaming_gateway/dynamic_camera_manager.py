"""Dynamic camera manager for runtime camera add/update/delete operations."""

from __future__ import annotations

import logging
import os
import threading
from typing import Any, Callable, Dict, Optional, Tuple

from .streaming_gateway_utils import (
    InstanceStreamingGatewayUtil,
    _aggregate_camera_demand,
    _coerce_fps,
    resolve_publish_fps,
)

try:
    from .camera_streamer.nvdec.nvdec_worker_manager import NVDECWorkerManager
except (ImportError, AttributeError):
    NVDECWorkerManager = None  # type: ignore[assignment,misc]

from .constants import (
    DEFAULT_CAMERA_HEIGHT,
    DEFAULT_CAMERA_QUALITY,
    DEFAULT_CAMERA_WIDTH,
    DEFAULT_MEDIAMTX_PORT,
)

_logger = logging.getLogger(__name__)


class _MetricsStatisticsStub:
    """No-op stand-in satisfying the legacy ``camera_streamer.statistics`` probes
    in metrics/collector.py and metrics/manager.py. Real per-camera FPS now rides
    in worker health reports' ``per_camera_stats``."""

    def get_timing_stats(self, stream_key=None):
        if stream_key is None:
            return {"per_stream": {}, "active_streams": []}
        return {
            "stream_key": stream_key,
            "last_read_time_sec": 0.0,
            "last_write_time_sec": 0.0,
            "last_process_time_sec": 0.0,
            "last_frame_size_bytes": 0,
        }

    def get_timing_statistics(self, stream_key: str):
        return {}

    def clear_timing_history(self, stream_key=None):
        pass


# Volatile fields excluded from config diff — these change on every API fetch
# but don't affect streaming behavior.
#
# IMPORTANT: do NOT add any key here that affects stream identity or
# transport: source / cameraInputUrl / fps / quality / width / height /
# camera_location / simulate_video_file_stream / topic / streamingGatewayId
# / cameraGroupId — all of those MUST trip the diff so update_camera()
# actually rebuilds the underlying decoder. Adding them here would re-introduce
# the "dead worker bound to stale source" silent-skip bug (step 10 in fix plan).
_VOLATILE_KEYS = frozenset(("updatedAt", "createdAt", "timestamp", "__v"))


def _normalize_cfg_value(value: Any) -> Any:
    """Normalize nested config values for stable comparison without JSON."""
    if isinstance(value, dict):
        return tuple(sorted((k, _normalize_cfg_value(v)) for k, v in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_normalize_cfg_value(v) for v in value)
    return value


def _cfg_fingerprint(d: dict) -> str:
    """Deterministic fingerprint of a camera config dict, ignoring volatile fields.

    REFACTORING_PLAN §20: typed key comparison without per-update ``json.dumps``.
    """
    items = tuple(sorted((k, _normalize_cfg_value(v)) for k, v in d.items() if k not in _VOLATILE_KEYS))
    return repr(items)


def _resolve_camera_host(
    instance_util: Optional[InstanceStreamingGatewayUtil],
    camera_id: str,
) -> str:
    """Resolve the MediaMTX host IP for a camera via the instance IPs API.

    Falls back to MEDIAMTX_HOST env var or localhost if resolution fails.

    Args:
        instance_util: InstanceStreamingGatewayUtil instance (may be None)
        camera_id: Camera ID to resolve

    Returns:
        IP address or hostname for the camera's MediaMTX server
    """
    fallback = os.getenv("MEDIAMTX_HOST", "localhost")
    if not instance_util or not camera_id:
        return fallback
    try:
        ips = instance_util.get_camera_instance_ips([camera_id])
        resolved = ips.get(camera_id)
        if resolved:
            _logger.info(f"Resolved MediaMTX host for camera {camera_id}: {resolved}")
            return resolved
        _logger.warning(f"camera_instance_ips returned no IP for camera {camera_id}, falling back to {fallback}")
    except Exception as e:
        _logger.warning(f"Failed to resolve instance IP for camera {camera_id}: {e}, falling back to {fallback}")
    return fallback


# ---------------------------------------------------------------------------
# Config builders (backend-specific camera config creation)
# ---------------------------------------------------------------------------


def _resolve_hotadd_publish_fps(
    camera_data: Dict[str, Any],
    instance_util: Optional[InstanceStreamingGatewayUtil],
    camera_id: Optional[str],
) -> float:
    """Resolve the PUBLISH rate for a camera arriving via a runtime event.

    The startup path gets this for free: it aggregates the consuming-topics rows
    through ``_aggregate_camera_demand`` + ``_resolve_stream_demand``. The hot-add
    path had no equivalent and used ``cameraFPS`` — the camera's SOURCE rate —
    directly, which set the camera's per-camera publish target to its own source
    rate and made the publish cap a no-op for every hot-added camera.

    Demand sources, in precedence order:
      1. ``minFps`` on the event payload, when the backend includes it.
      2. The consuming-topics rows for this camera, aggregated the same way as
         the startup path (``max(minFps)`` across the apps consuming it).
      3. No demand -> ``min(operator default, cameraFPS)``.

    Never raises: a control-plane failure degrades to the no-demand fallback
    rather than dropping the camera, since publishing at the capped default is
    always safe.
    """
    camera_fps = _coerce_fps(camera_data.get("cameraFPS"), "cameraFPS")

    # 1. Demand carried on the event itself.
    demand = _coerce_fps(camera_data.get("minFps"), "minFps demand")
    if demand > 0:
        fps = resolve_publish_fps(demand, camera_fps)
        _logger.info(f"[F08] Camera {camera_id}: publish {fps:g} fps from event minFps (cameraFPS={camera_fps:g})")
        return fps

    # 2. Aggregate this camera's rows from the consuming-topics API, exactly as
    #    the startup path does. get_consuming_topics() returns [] on failure.
    if instance_util is not None and camera_id:
        try:
            rows = [t for t in (instance_util.get_consuming_topics() or []) if t.get("cameraId") == camera_id]
        except Exception as e:
            _logger.warning(f"[F08] Camera {camera_id}: consuming-topics lookup failed ({e}); using fallback")
            rows = []
        if rows:
            agg = _aggregate_camera_demand(rows).get(camera_id)
            if agg is not None:
                # Prefer the API's cameraFPS when the event omitted it.
                fps = resolve_publish_fps(agg.get("fps", 0.0), camera_fps or agg.get("camera_fps", 0.0))
                _logger.info(
                    f"[F08] Camera {camera_id}: publish {fps:g} fps from {len(rows)} consuming "
                    f"topic(s) (max minFps={agg.get('fps', 0.0):g}, cameraFPS={camera_fps:g})"
                )
                return fps

    # 3. No declared demand anywhere.
    fps = resolve_publish_fps(0.0, camera_fps)
    _logger.info(
        f"[F08] Camera {camera_id}: no declared minFps demand; publish {fps:g} fps "
        f"= min(operator default, cameraFPS={camera_fps:g})"
    )
    return fps


def _resolve_hotadd_resolution(
    camera_data: Dict[str, Any],
    instance_util: Optional[InstanceStreamingGatewayUtil],
    camera_id: Optional[str],
) -> Tuple[int, int]:
    """Resolve the per-camera target resolution (w, h) for a hot-added camera.

    Mirrors :func:`_resolve_hotadd_publish_fps` for F08 ``min_resolution``. A
    concrete target lets the decode sub-process create the ring buffer EAGERLY
    and emit ``producer_ready`` immediately, instead of deferring to the first
    decoded frame — which is what made a slow / wrong-codec hot-add miss the ACK
    deadline and get torn down + re-added in a loop.

    Uses the consuming-topics aggregation (``_aggregate_camera_demand`` already
    parses ``min_resolution`` into ``w``/``h``). Returns ``(0, 0)`` when no
    resolution is declared → native-res / lazy ring buffer, the historical
    default (unavoidable: native dims are unknown until the first frame). Never
    raises.
    """
    if instance_util is not None and camera_id:
        try:
            rows = [t for t in (instance_util.get_consuming_topics() or []) if t.get("cameraId") == camera_id]
        except Exception as e:
            _logger.warning(f"[F08] Camera {camera_id}: resolution lookup failed ({e}); native/lazy")
            rows = []
        if rows:
            agg = _aggregate_camera_demand(rows).get(camera_id)
            if agg is not None:
                try:
                    aw, ah = int(agg.get("w", 0) or 0), int(agg.get("h", 0) or 0)
                except (TypeError, ValueError):
                    aw, ah = 0, 0
                if aw > 0 and ah > 0:
                    _logger.info(
                        f"[F08] Camera {camera_id}: target resolution {aw}x{ah} "
                        f"(eager ring buffer, producer_ready without waiting for first frame)"
                    )
                    return aw, ah
    _logger.info(f"[F08] Camera {camera_id}: no declared min_resolution; native-res (lazy ring buffer)")
    return 0, 0


def build_nvdec_camera_config(
    camera_data: Dict[str, Any],
    instance_util: Optional[InstanceStreamingGatewayUtil],
) -> Optional[Dict[str, Any]]:
    """Create camera config dict for NVDECWorkerManager from event data.

    Returns:
        Dict compatible with NVDECWorkerManager or None if failed.
    """
    try:
        camera_id = camera_data.get("id") or camera_data.get("cameraId")

        mediamtx_host = _resolve_camera_host(instance_util, camera_id)
        mediamtx_port = int(os.getenv("MEDIAMTX_PORT", str(DEFAULT_MEDIAMTX_PORT)))
        source = f"rtsp://{mediamtx_host}:{mediamtx_port}/{camera_id}"
        _logger.info(f"[NVDEC] Using MediaMTX RTSP URL for camera {camera_id}: {source}")

        # PUBLISH rate = app demand (max minFps), else min(operator default,
        # cameraFPS). NOT cameraFPS — that is the source rate, and using it here
        # is what neutered the publish cap on every hot-added camera.
        fps = _resolve_hotadd_publish_fps(camera_data, instance_util, camera_id)
        # F08 target resolution: a declared min_resolution lets the sub-process
        # create the ring buffer eagerly and ACK producer_ready without waiting
        # for the first decoded frame (0/0 => native-res / lazy, as before).
        target_w, target_h = _resolve_hotadd_resolution(camera_data, instance_util, camera_id)
        camera_name = camera_data.get("cameraName", f"Camera_{camera_id}")
        simulate_video = camera_data.get("protocolType") == "FILE"

        from .camera_streamer.codec_detect import normalize_codec

        # Read codec from the backend camera record. Field-name precedence:
        #   1. cameraCodec   — canonical name in the v1 camera API (e.g. "H265")
        #   2. videoCodec    — legacy field still emitted by some callers
        #   3. video_codec   — snake-case fallback
        # If none are present, normalize_codec(None) falls back to "h264", which
        # is the prior behavior. The h264 hardcode that was previously forcing
        # every camera onto h264 was removed in commit 3005999.
        cam_codec_raw = (
            camera_data.get("cameraCodec") or camera_data.get("videoCodec") or camera_data.get("video_codec")
        )
        cam_codec = normalize_codec(cam_codec_raw)
        _logger.info(f"[NVDEC] Camera {camera_id} codec resolved: raw={cam_codec_raw!r} -> normalized={cam_codec!r}")

        return {
            "camera_id": camera_id,
            "stream_key": camera_id,
            "source": source,
            "video_path": source,
            "fps": fps,
            "width": target_w or DEFAULT_CAMERA_WIDTH,
            "height": target_h or DEFAULT_CAMERA_HEIGHT,
            "codec": cam_codec,
            "_camera_name": camera_name,
            "_original_camera_id": camera_id,
            "_camera_group": "Instance",
            "_simulate_video": simulate_video,
        }

    except Exception as e:
        _logger.exception(f"[NVDEC] Error creating camera config: {e}")
        return None


def build_worker_camera_config(
    camera_data: Dict[str, Any],
    instance_util: Optional[InstanceStreamingGatewayUtil],
) -> Optional[Dict[str, Any]]:
    """Create camera config dict for WorkerManager from event data.

    Returns:
        Dict compatible with WorkerManager/AsyncCameraWorker or None if failed.
    """
    try:
        camera_id = camera_data.get("id") or camera_data.get("cameraId")

        mediamtx_host = _resolve_camera_host(instance_util, camera_id)
        mediamtx_port = int(os.getenv("MEDIAMTX_PORT", str(DEFAULT_MEDIAMTX_PORT)))
        source = f"rtsp://{mediamtx_host}:{mediamtx_port}/{camera_id}"
        simulate_video = camera_data.get("protocolType") == "FILE"
        input_topic = camera_data.get("topicName", f"{camera_id}_input_topic")

        # Same demand-first rule as the NVDEC builder — cameraFPS is the source
        # rate, not a publish target.
        fps = _resolve_hotadd_publish_fps(camera_data, instance_util, camera_id)

        return {
            "stream_key": camera_data.get("cameraName", f"Camera_{camera_id}"),
            "stream_group_key": "Instance",
            "camera_id": camera_id,
            "source": source,
            "topic": input_topic,
            "fps": fps,
            "quality": DEFAULT_CAMERA_QUALITY,
            "width": DEFAULT_CAMERA_WIDTH,
            "height": DEFAULT_CAMERA_HEIGHT,
            "camera_location": "Unknown Location",
            "simulate_video_file_stream": simulate_video,
        }

    except Exception as e:
        _logger.exception(f"Error creating worker camera config: {e}")
        return None


# ---------------------------------------------------------------------------
# Unified DynamicCameraManager
# ---------------------------------------------------------------------------


class DynamicCameraManager:
    """Unified dynamic camera manager for runtime camera add/update/delete.

    Works with any backend (NVDECWorkerManager or WorkerManager) by accepting
    a config builder callable and a stream-key extractor.

    Args:
        backend: Backend manager (must implement add_camera/remove_camera/
            update_camera/get_worker_statistics).
        config_builder: Callable(camera_data, instance_util) -> Optional[Dict]
        stream_key_field: Key in the built config dict that holds the stream key.
        streaming_gateway_id: ID of the streaming gateway.
        session: Session object for API calls (optional).
        streaming_gateway: StreamingGateway instance for updating mappings (optional).
        instance_util: InstanceStreamingGatewayUtil (optional).
        log_prefix: Prefix for log messages (e.g. "[NVDEC] ").
    """

    def __init__(
        self,
        backend: Any,
        config_builder: Callable[
            [Dict[str, Any], Optional[InstanceStreamingGatewayUtil]],
            Optional[Dict[str, Any]],
        ],
        stream_key_field: str = "stream_key",
        streaming_gateway_id: str = "",
        session: Any = None,
        streaming_gateway: Any = None,
        instance_util: Optional[InstanceStreamingGatewayUtil] = None,
        log_prefix: str = "",
    ):
        self.backend = backend
        self.config_builder = config_builder
        self.stream_key_field = stream_key_field
        self.streaming_gateway_id = streaming_gateway_id
        self.session = session
        self.streaming_gateway = streaming_gateway
        self.instance_util = instance_util
        self._log_prefix = log_prefix
        self.logger = logging.getLogger(__name__)

        # Metrics compatibility: metrics/collector.py and metrics/manager.py access
        # camera_streamer.statistics expecting a StreamStatistics-like object. Real
        # per-camera FPS now rides in worker health reports' per_camera_stats (both
        # backends), so this object only needs to satisfy the legacy getattr/method
        # probes without ever being None.
        self.statistics = _MetricsStatisticsStub()

        # Camera storage
        self.cameras: Dict[str, Dict[str, Any]] = {}  # camera_id -> camera_data
        self.camera_topics: Dict[str, Dict[str, str]] = {}  # camera_id -> {input, output}
        self.camera_stream_keys: Dict[str, str] = {}  # camera_id -> stream_key
        self.camera_groups: Dict[str, Dict[str, Any]] = {}  # group_id -> group_data

        # Lock for thread-safe operations
        self._lock = threading.RLock()

        # Statistics
        self.stats = {
            "cameras_added": 0,
            "cameras_updated": 0,
            "cameras_removed": 0,
            "active_cameras": 0,
        }

        self.logger.info(f"{self._log_prefix}DynamicCameraManager initialized for gateway {streaming_gateway_id}")

    # -- helpers --

    def _build_config(self, camera_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Build backend-specific config from camera_data."""
        return self.config_builder(camera_data, self.instance_util)

    def _get_stream_key(self, config: Dict[str, Any]) -> str:
        """Extract the stream key from a built config dict."""
        return config[self.stream_key_field]

    def _update_gateway_mappings(self, stream_key: str, camera_id: str):
        """Update streaming gateway mappings for metrics.

        Acquires the gateway's _state_lock so concurrent metrics readers
        (e.g. get_statistics()) never observe partial state where stream_key
        is in _my_stream_keys but not yet in _stream_key_to_camera_id.
        """
        gw = self.streaming_gateway
        if gw is None:
            return
        with gw._state_lock:
            gw._stream_key_to_camera_id[stream_key] = camera_id
            gw._my_stream_keys.add(stream_key)

    def _remove_gateway_mappings(self, stream_key: str, camera_id: Optional[str] = None):
        """Remove streaming gateway mappings (atomic under gateway state lock)."""
        gw = self.streaming_gateway
        if gw is None:
            return
        with gw._state_lock:
            if camera_id is not None and gw._stream_key_to_camera_id.get(stream_key) != camera_id:
                return
            gw._stream_key_to_camera_id.pop(stream_key, None)
            gw._my_stream_keys.discard(stream_key)

    # -- public API --

    def initialize_from_config(self, input_streams: list):
        """Initialize with existing input stream configurations (tracking only).

        Args:
            input_streams: List of InputStream objects.
        """
        with self._lock:
            for input_stream in input_streams:
                camera_id = input_stream.camera_id

                self.cameras[camera_id] = {
                    "id": camera_id,
                    "cameraName": input_stream.camera_key,
                    "cameraGroupId": input_stream.camera_group_key,
                    "source": input_stream.source,
                    "fps": input_stream.fps,
                    "quality": input_stream.quality,
                    "width": input_stream.width,
                    "height": input_stream.height,
                    "camera_location": input_stream.camera_location,
                    "simulate_video_file_stream": input_stream.simulate_video_file_stream,
                }

                self.camera_topics[camera_id] = {
                    "input": input_stream.camera_input_topic,
                    "output": None,  # type: ignore[dict-item]
                }

                self.camera_stream_keys[camera_id] = input_stream.camera_key
                self.stats["active_cameras"] += 1

            self.logger.info(f"{self._log_prefix}Initialized with {len(input_streams)} cameras (tracking only)")

    def add_camera(self, camera_data: Dict[str, Any]) -> bool:
        """Add a new camera.

        Args:
            camera_data: Camera configuration data from event.

        Returns:
            True if camera was added successfully.
        """
        camera_id = camera_data.get("id")
        camera_name = camera_data.get("cameraName", "Unknown")

        with self._lock:
            if camera_id in self.cameras:
                self.logger.warning(f"{self._log_prefix}Camera {camera_id} already exists, updating instead")
                return self.update_camera(camera_data)

            try:
                config = self._build_config(camera_data)
                if not config:
                    self.logger.error(f"{self._log_prefix}Failed to create config for camera {camera_id}")
                    return False

                stream_key = self._get_stream_key(config)

                if not self.backend.add_camera(config):
                    self.logger.error(f"{self._log_prefix}Backend failed to add camera {camera_name}")
                    return False

                # Store camera data
                self.cameras[camera_id] = camera_data  # type: ignore[index]
                self.camera_stream_keys[camera_id] = stream_key  # type: ignore[index]

                # Store topic if present in config
                topic = config.get("topic")
                if topic is not None:
                    self.camera_topics[camera_id] = {  # type: ignore[index]
                        "input": topic,
                        "output": None,  # type: ignore[dict-item]
                    }

                self._update_gateway_mappings(stream_key, camera_id)

                self.stats["cameras_added"] += 1
                self.stats["active_cameras"] += 1

                self.logger.info(f"{self._log_prefix}Successfully added camera: {camera_name}")
                return True

            except Exception as e:
                self.logger.error(
                    f"{self._log_prefix}Error adding camera {camera_name}: {e}",
                    exc_info=True,
                )
                return False

    def update_camera(self, camera_data: Dict[str, Any]) -> bool:
        """Update an existing camera's configuration.

        Args:
            camera_data: Updated camera configuration data.

        Returns:
            True if camera was updated successfully.
        """
        camera_id = camera_data.get("id")
        camera_name = camera_data.get("cameraName", "Unknown")

        with self._lock:
            if camera_id not in self.cameras:
                self.logger.warning(f"{self._log_prefix}Camera {camera_id} not found, adding instead")
                return self.add_camera(camera_data)

            # Diff guard: skip if config hasn't actually changed
            existing = self.cameras.get(camera_id)
            if existing is not None and _cfg_fingerprint(existing) == _cfg_fingerprint(camera_data):
                self.logger.debug(f"{self._log_prefix}Camera {camera_id} config unchanged, skipping update")
                return True

            old_stream_key = self.camera_stream_keys.get(camera_id)
            is_currently_streaming = old_stream_key is not None

            try:
                config = self._build_config(camera_data)
                if not config:
                    self.logger.error(f"{self._log_prefix}Failed to create updated config for camera {camera_id}")
                    return False

                stream_key = self._get_stream_key(config)

                if not self.backend.update_camera(config):
                    self.logger.error(f"{self._log_prefix}Backend failed to update camera {camera_name}")
                    return False

                self.cameras[camera_id] = camera_data
                self.camera_stream_keys[camera_id] = stream_key

                topic = config.get("topic")
                if topic is not None:
                    self.camera_topics[camera_id] = {
                        "input": topic,
                        "output": None,  # type: ignore[dict-item]
                    }

                if old_stream_key and old_stream_key != stream_key:
                    self._remove_gateway_mappings(old_stream_key, camera_id)
                self._update_gateway_mappings(stream_key, camera_id)

                if not is_currently_streaming:
                    self.stats["active_cameras"] += 1
                    self.logger.info(f"{self._log_prefix}Started streaming for camera {camera_name} (now active)")
                else:
                    self.logger.info(f"{self._log_prefix}Restarted streaming for camera {camera_name}")

                self.stats["cameras_updated"] += 1
                return True

            except Exception as e:
                self.logger.error(
                    f"{self._log_prefix}Error updating camera {camera_name}: {e}",
                    exc_info=True,
                )
                return False

    def remove_camera(self, camera_id: str) -> bool:
        """Remove a camera.

        Args:
            camera_id: ID of camera to remove.

        Returns:
            True if camera was removed successfully.
        """
        with self._lock:
            camera_data = self.cameras.get(camera_id)

            if not camera_data:
                self.logger.warning(f"{self._log_prefix}Camera {camera_id} not found")
                return False

            camera_name = camera_data.get("cameraName", "Unknown")

            try:
                stream_key = self.camera_stream_keys.get(camera_id)

                if stream_key:
                    if not self.backend.remove_camera(stream_key):
                        self.logger.error(f"{self._log_prefix}Backend failed to remove camera {camera_name}")
                        return False

                    self._remove_gateway_mappings(stream_key, camera_id)

                del self.cameras[camera_id]
                self.camera_stream_keys.pop(camera_id, None)
                self.camera_topics.pop(camera_id, None)

                self.stats["cameras_removed"] += 1
                self.stats["active_cameras"] -= 1

                self.logger.info(f"{self._log_prefix}Successfully removed camera: {camera_name}")
                return True

            except Exception as e:
                self.logger.error(
                    f"{self._log_prefix}Error removing camera {camera_name}: {e}",
                    exc_info=True,
                )
                return False

    def on_backend_camera_failed(self, camera_id: str, reason: str) -> None:
        """Drop a camera that the backend reported as silently failed.

        Called by the backend (e.g. NVDECWorkerManager) when a worker reports
        add_failed AFTER the manager has already returned True from add_camera.
        Does NOT call backend.remove_camera() — the backend already considers
        the camera gone; this only reconciles DCM's own bookkeeping so the
        next periodic refresh sees the camera as absent and retries.
        """
        with self._lock:
            if camera_id not in self.cameras:
                return
            camera_name = self.cameras[camera_id].get("cameraName", camera_id)
            stream_key = self.camera_stream_keys.get(camera_id)
            if stream_key:
                self._remove_gateway_mappings(stream_key, camera_id)
            self.cameras.pop(camera_id, None)
            self.camera_stream_keys.pop(camera_id, None)
            self.camera_topics.pop(camera_id, None)
            self.stats.setdefault("cameras_failed_late", 0)
            self.stats["cameras_failed_late"] += 1
            if self.stats.get("active_cameras", 0) > 0:
                self.stats["active_cameras"] -= 1
            self.logger.error(
                f"{self._log_prefix}Camera {camera_name} ({camera_id}) dropped after late backend failure: {reason}"
            )

    def update_camera_group(self, group_data: Dict[str, Any]):
        """Update camera group information."""
        group_id = group_data.get("id")
        with self._lock:
            self.camera_groups[group_id] = group_data  # type: ignore[index]
            self.logger.info(f"{self._log_prefix}Updated camera group: {group_data.get('cameraGroupName')}")

    def remove_camera_group(self, group_id: str):
        """Remove camera group information."""
        with self._lock:
            if group_id in self.camera_groups:
                del self.camera_groups[group_id]
                self.logger.info(f"{self._log_prefix}Removed camera group: {group_id}")

    def update_cameras_in_group(self, group_id: str, group_data: Dict[str, Any]):
        """Update all cameras in a group with new default settings."""
        default_settings = group_data.get("defaultStreamSettings", {})

        with self._lock:
            cameras_to_update = [cid for cid, cdata in self.cameras.items() if cdata.get("cameraGroupId") == group_id]

            self.logger.info(
                f"{self._log_prefix}Updating {len(cameras_to_update)} cameras in group {group_id} "
                f"with new default settings"
            )

            for cid in cameras_to_update:
                cdata = self.cameras[cid].copy()
                custom_settings = cdata.get("customStreamSettings", {})
                for key, value in default_settings.items():
                    if key not in custom_settings:
                        cdata[key] = value
                self.update_camera(cdata)

    def update_camera_input_topic(self, camera_id: str, topic_name: Optional[str]):
        """Update input topic for a camera."""
        with self._lock:
            if camera_id not in self.camera_topics:
                self.camera_topics[camera_id] = {"input": None, "output": None}  # type: ignore[dict-item]

            self.camera_topics[camera_id]["input"] = topic_name  # type: ignore[assignment]
            self.logger.info(f"{self._log_prefix}Updated input topic for camera {camera_id}: {topic_name}")

            if camera_id in self.cameras and camera_id in self.camera_stream_keys:
                camera_data = self.cameras[camera_id].copy()
                self.update_camera(camera_data)

    def update_camera_output_topic(self, camera_id: str, topic_name: Optional[str]):
        """Update output topic for a camera."""
        with self._lock:
            if camera_id not in self.camera_topics:
                self.camera_topics[camera_id] = {"input": None, "output": None}  # type: ignore[dict-item]

            self.camera_topics[camera_id]["output"] = topic_name  # type: ignore[assignment]
            self.logger.info(f"{self._log_prefix}Updated output topic for camera {camera_id}: {topic_name}")

    def get_camera_assignments(self) -> Dict[str, int]:
        """Return mapping of camera_id to GPU/worker ID (if supported by backend)."""
        if hasattr(self.backend, "get_camera_assignments"):
            return self.backend.get_camera_assignments()
        return {}

    def get_statistics(self) -> Dict[str, Any]:
        """Get camera manager statistics."""
        with self._lock:
            stats = {
                **self.stats,
                "camera_ids": list(self.cameras.keys()),
                "camera_groups": len(self.camera_groups),
            }

            try:
                stats["worker_stats"] = self.backend.get_worker_statistics()
            except Exception as e:
                self.logger.warning(f"{self._log_prefix}Failed to get worker statistics: {e}")

            return stats

    @property
    def is_running(self) -> bool:
        """Check if the backend is currently running."""
        return getattr(self.backend, "is_running", False)


# ---------------------------------------------------------------------------
# Backward-compatible factory aliases
# ---------------------------------------------------------------------------


def DynamicCameraManagerForNVDEC(
    nvdec_worker_manager: NVDECWorkerManager,
    streaming_gateway_id: str = "",
    session: Any = None,
    streaming_gateway: Any = None,
    instance_util: Optional[InstanceStreamingGatewayUtil] = None,
) -> DynamicCameraManager:
    """Create a DynamicCameraManager configured for the NVDEC backend."""
    return DynamicCameraManager(
        backend=nvdec_worker_manager,
        config_builder=build_nvdec_camera_config,
        stream_key_field="camera_id",
        streaming_gateway_id=streaming_gateway_id,
        session=session,
        streaming_gateway=streaming_gateway,
        instance_util=instance_util,
        log_prefix="[NVDEC] ",
    )


def DynamicCameraManagerForWorkers(
    worker_manager: Any,
    streaming_gateway_id: str,
    session: Any = None,
    streaming_gateway: Any = None,
    instance_util: Optional[InstanceStreamingGatewayUtil] = None,
) -> DynamicCameraManager:
    """Create a DynamicCameraManager configured for the WorkerManager backend."""
    return DynamicCameraManager(
        backend=worker_manager,
        config_builder=build_worker_camera_config,
        stream_key_field="stream_key",
        streaming_gateway_id=streaming_gateway_id,
        session=session,
        streaming_gateway=streaming_gateway,
        instance_util=instance_util,
        log_prefix="",
    )
