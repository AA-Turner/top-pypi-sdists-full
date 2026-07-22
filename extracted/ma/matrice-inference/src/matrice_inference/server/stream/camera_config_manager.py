"""Unified camera config management: API fetch, Kafka refresh, periodic refresh, heartbeat.

Works with both CUDA SHM engine (dict configs) and streaming pipeline (CameraConfig objects).
Consolidates logic from app_deployment.py, camera_config_monitor.py, deployment_refresh_listener.py,
and relevant parts of server.py.
"""

import logging
import threading
import time
from typing import Callable, Dict, Optional

from matrice_common.session import Session

from matrice_inference.server.stream.app_deployment import AppDeployment
from matrice_inference.server.stream.deployment_refresh_listener import (
    DeploymentRefreshListener,
)
from matrice_inference.server.stream.utils import CameraConfig

logger = logging.getLogger(__name__)


class CameraConfigManager:
    """Unified camera config management: API fetch, Kafka refresh, periodic refresh, heartbeat.

    Works with both CUDA SHM engine (dict configs) and streaming pipeline (CameraConfig objects).

    Usage:
        manager = CameraConfigManager(session=..., app_deployment_id=..., ...)
        configs = manager.get_camera_configs()  # initial load
        manager.start()   # starts Kafka listener + periodic refresh + heartbeat
        ...
        manager.stop()
    """

    def __init__(
        self,
        session: Session,
        app_deployment_id: str,
        instance_id: str,
        deployment_instance_id: str,
        instance_string_id: str = "",
        action_id: str = "",
        connection_timeout: int = 1200,
        heartbeat_interval: int = 30,
        auto_refresh_interval: float = 300.0,
        on_config_changed: Optional[Callable[[Dict[str, CameraConfig]], None]] = None,
    ):
        """Initialize CameraConfigManager.

        Args:
            session: Session object for API authentication.
            app_deployment_id: App deployment ID.
            instance_id: Compute instance ID (_idComputeInstance).
            deployment_instance_id: Model deploy instance ID (_idModelDeployInstance).
            instance_string_id: Human-readable instance ID for Redis lookup.
            action_id: Action ID for Redis lookup.
            connection_timeout: Timeout (seconds) waiting for server connection info.
            heartbeat_interval: Seconds between heartbeat sends.
            auto_refresh_interval: Seconds between periodic auto-refreshes.
            on_config_changed: Callback invoked with new camera configs when they change.
        """
        # Create AppDeployment (delegates API calls + heartbeat producer)
        self._app_deployment = AppDeployment(
            session=session,
            app_deployment_id=app_deployment_id,
            deployment_instance_id=deployment_instance_id,
            instance_id=instance_id,
            connection_timeout=connection_timeout,
            action_id=action_id,
            instance_string_id=instance_string_id,
        )

        self.on_config_changed = on_config_changed
        self.camera_configs: Dict[str, CameraConfig] = {}
        self._heartbeat_interval = max(10, int(heartbeat_interval))
        self._auto_refresh_interval = auto_refresh_interval

        # Lifecycle
        self._stop_event = threading.Event()
        self._refresh_listener: Optional[DeploymentRefreshListener] = None
        self._heartbeat_thread: Optional[threading.Thread] = None

        logger.info(
            "CameraConfigManager initialized: instance_id=%s, deployment_instance_id=%s, "
            "app_deployment_id=%s, heartbeat_interval=%ds, auto_refresh_interval=%.0fs",
            instance_id,
            deployment_instance_id,
            app_deployment_id,
            self._heartbeat_interval,
            self._auto_refresh_interval,
        )

    # ------------------------------------------------------------------
    # Delegate API calls to AppDeployment
    # ------------------------------------------------------------------

    def get_camera_configs(self) -> Dict[str, CameraConfig]:
        """Fetch camera configs from API (primary + fallback endpoints)."""
        return self._app_deployment.get_camera_configs()

    def get_redis_connection_by_instance(self) -> Optional[Dict]:
        """Get Redis connection info by instance ID, with Sentinel support."""
        return self._app_deployment.get_redis_connection_by_instance()

    def get_and_wait_for_connection_info(self, server_type: str, server_id: str) -> Optional[Dict]:
        """Get connection info for Kafka/Redis server, blocking until available."""
        return self._app_deployment.get_and_wait_for_connection_info(server_type, server_id)

    @property
    def app_deployment(self) -> AppDeployment:
        """Access the underlying AppDeployment (for backward compat / analytics publisher)."""
        return self._app_deployment

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self):
        """Start Kafka refresh listener, periodic refresh, and heartbeat."""
        self._stop_event.clear()

        # 1. Create and start DeploymentRefreshListener
        self._refresh_listener = DeploymentRefreshListener(
            session=self._app_deployment.session,
            deployment_instance_id=self._app_deployment.deployment_instance_id,
            on_refresh=self._execute_refresh,
            instance_id=self._app_deployment.instance_id,
            auto_refresh_interval=self._auto_refresh_interval,
        )
        success = self._refresh_listener.start()
        if success:
            logger.info("CameraConfigManager: refresh listener started")
        else:
            logger.error("CameraConfigManager: failed to start refresh listener")

        # 2. Start heartbeat thread
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True,
            name="ConfigManager-Heartbeat",
        )
        self._heartbeat_thread.start()
        logger.info(
            "CameraConfigManager: heartbeat thread started (interval=%ds)",
            self._heartbeat_interval,
        )

    def stop(self):
        """Stop all background threads and close resources."""
        logger.info("CameraConfigManager: stopping...")
        self._stop_event.set()

        if self._refresh_listener:
            self._refresh_listener.stop()
            self._refresh_listener = None

        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=5.0)
            self._heartbeat_thread = None

        self._app_deployment.close_heartbeat_producer()
        logger.info("CameraConfigManager: stopped")

    # ------------------------------------------------------------------
    # Refresh Logic (synchronous, no event loop needed)
    # ------------------------------------------------------------------

    def _execute_refresh(self):
        """Called by refresh listener on Kafka event or periodic timer.

        Fetches latest configs from API, diffs against current state,
        and invokes on_config_changed callback if the camera set changed.
        """
        new_configs = self.get_camera_configs()

        if new_configs is None:
            raise RuntimeError("API returned None for camera configs")

        # Diff by camera ID set
        current_ids = set(self.camera_configs.keys())
        new_ids = set(new_configs.keys())

        if current_ids == new_ids:
            # Check if any config content changed (stream_config, enabled, topics)
            configs_changed = False
            for cam_id in new_ids:
                old_cfg = self.camera_configs.get(cam_id)
                new_cfg = new_configs.get(cam_id)
                if (
                    old_cfg
                    and new_cfg
                    and (
                        old_cfg.input_topic != new_cfg.input_topic
                        or old_cfg.output_topic != new_cfg.output_topic
                        or old_cfg.stream_config != new_cfg.stream_config
                        or old_cfg.enabled != new_cfg.enabled
                    )
                ):
                    configs_changed = True
                    logger.info(
                        "CameraConfigManager: config content changed for camera %s",
                        cam_id,
                    )
                    break
            if not configs_changed:
                logger.debug("CameraConfigManager: no camera set or config change detected")
                return
            logger.info("CameraConfigManager: config content change detected (same camera set)")
        else:
            added = new_ids - current_ids
            removed = current_ids - new_ids
            logger.info(
                "CameraConfigManager: config change detected: +%d added, -%d removed (added=%s, removed=%s)",
                len(added),
                len(removed),
                list(added),
                list(removed),
            )

        self.camera_configs = new_configs

        if self.on_config_changed:
            try:
                self.on_config_changed(new_configs)
            except Exception:
                logger.error(
                    "CameraConfigManager: on_config_changed callback failed",
                    exc_info=True,
                )
                raise  # Let refresh listener track via circuit breaker

    # ------------------------------------------------------------------
    # Heartbeat
    # ------------------------------------------------------------------

    def _heartbeat_loop(self):
        """Background thread that sends heartbeats at regular intervals."""
        last_sent = 0.0
        while not self._stop_event.is_set():
            try:
                now = time.time()
                if now - last_sent >= self._heartbeat_interval:
                    self.send_heartbeat()
                    last_sent = time.time()
            except Exception:
                logger.error("CameraConfigManager: heartbeat error", exc_info=True)

            # Sleep in short increments to respond to stop_event quickly
            self._stop_event.wait(timeout=1.0)

    def send_heartbeat(self):
        """Send heartbeat using current camera_configs."""
        if not self.camera_configs:
            return
        self._app_deployment.send_heartbeat(self.camera_configs)

    # ------------------------------------------------------------------
    # Config conversion (static, reusable)
    # ------------------------------------------------------------------

    @staticmethod
    def convert_configs_for_engine(
        camera_configs: Dict[str, CameraConfig],
        app_deployment_id: str = "",
        app_id: str = "",
    ) -> Dict[str, dict]:
        """Convert CameraConfig objects to engine-compatible dicts.

        Extracted from server.py _initialize_cuda_shm_engine() lines 650-737.
        Handles CameraConfig objects, plain dicts, and other object types.

        Args:
            camera_configs: Dict mapping camera_id to CameraConfig (or dict).
            app_deployment_id: App deployment ID to embed in each config.
            app_id: Application ID to embed in each config.

        Returns:
            Dict mapping camera_id to engine-compatible dict.
        """
        converted = {}

        for cam_id, cfg in camera_configs.items():
            if hasattr(cfg, "stream_config"):
                # CameraConfig object
                sc = cfg.stream_config if isinstance(cfg.stream_config, dict) else {}

                # Auto-detect stream_type from video source URL
                video_path = (
                    getattr(cfg, "video_path", None)
                    or getattr(cfg, "input_topic", None)
                    or sc.get("video_path", "")
                    or sc.get("input_topic", "")
                )
                if video_path and isinstance(video_path, str) and video_path.startswith(("rtsp://", "rtsps://")):
                    stream_type = "rtsp"
                else:
                    stream_type = "file"

                cfg_dict = {
                    "camera_id": getattr(cfg, "camera_id", cam_id),
                    "input_topic": getattr(cfg, "input_topic", None),
                    "output_topic": getattr(cfg, "output_topic", None),
                    "stream_type": stream_type,
                    "camera_name": sc.get("camera_name", cam_id),
                    "camera_group": sc.get("camera_group", "default"),
                    "location": sc.get("location", "unknown"),
                    "stream_config": {
                        "host": sc.get("host", "localhost"),
                        "port": sc.get("port", 6379),
                        "password": sc.get("password"),
                        "username": sc.get("username"),
                        "db": sc.get("db", 0),
                        "stream_type": sc.get("stream_type", "redis"),
                        "sentinel_hosts": sc.get("sentinel_hosts"),
                        "master_name": sc.get("master_name"),
                        "camera_name": sc.get("camera_name", cam_id),
                        "camera_group": sc.get("camera_group", "default"),
                        "location": sc.get("location", "unknown"),
                    },
                    "app_deployment_id": app_deployment_id or "",
                    "application_id": app_id or "",
                }
                converted[cam_id] = cfg_dict

            elif isinstance(cfg, dict):
                # Plain dict config — fix stream_type
                fixed_cfg = cfg.copy()
                video_path = cfg.get("video_path", "") or cfg.get("input_topic", "")
                if video_path and isinstance(video_path, str):
                    if video_path.startswith(("rtsp://", "rtsps://")):
                        fixed_cfg["stream_type"] = "rtsp"
                    else:
                        fixed_cfg["stream_type"] = "file"
                elif fixed_cfg.get("stream_type") == "redis":
                    fixed_cfg["stream_type"] = "file"
                fixed_cfg["app_deployment_id"] = fixed_cfg.get("app_deployment_id", "") or app_deployment_id or ""
                fixed_cfg["application_id"] = fixed_cfg.get("application_id", "") or app_id or ""
                converted[cam_id] = fixed_cfg

            else:
                # Fallback for other object types
                video_path = getattr(cfg, "video_path", None) or getattr(cfg, "input_topic", None) or ""
                if video_path and isinstance(video_path, str) and video_path.startswith(("rtsp://", "rtsps://")):
                    stream_type = "rtsp"
                else:
                    stream_type = "file"

                cfg_dict = {
                    "camera_id": getattr(cfg, "camera_id", cam_id),
                    "input_topic": getattr(cfg, "input_topic", None),
                    "output_topic": getattr(cfg, "output_topic", None),
                    "stream_type": stream_type,
                    "stream_config": {},
                    "app_deployment_id": app_deployment_id or "",
                    "application_id": app_id or "",
                }
                converted[cam_id] = cfg_dict

        logger.info("convert_configs_for_engine: converted %d camera configs", len(converted))
        return converted
