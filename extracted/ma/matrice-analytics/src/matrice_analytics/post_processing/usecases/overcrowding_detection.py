"""
Overcrowding Detection Usecase
--------------------------------

Definition:
    Overcrowding occurs when the number of detected persons in a zone
    exceeds a configured threshold for a configured number of frames.

Zone geometry:
    Zones drawn in the UI are stored on the deployment/camera post-processing
    config. When ``stream_info`` and API credentials (or ``set_config_client``)
    are available, zone polygons are resolved to pixel coordinates via the Matrice
    post-processing config API (one or more named zones supported).

Features:
- Zone-based or global detection
- Stateful detection (persistence + recovery)
- Alert cooldown support (AlertConfig)
- Incident lifecycle tracking (start/end)
- Single-frame input: a list of detections per ``process()`` call
- Same tracker stack as ``people_counting`` (``AdvancedTracker`` / optional simple tracker)
- Canonical agg_summary using BaseProcessor helpers

No density logic.
No rolling analytics.
Pure threshold-based safety detection.
"""

from __future__ import annotations

import copy
import logging
import os
import re
import threading
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import (
    apply_category_mapping,
    filter_by_confidence,
    point_in_polygon,
)

# ------------------------------------------------------------------------------
# Post-processing config client (UI zones → pixel coords via Matrice API)
# ------------------------------------------------------------------------------

_GEOMETRY_RETRY_INTERVAL = 30  # Seconds between background retry attempts when API fails


class _DeploymentIdHelper(BaseProcessor):
    """Minimal BaseProcessor subclass to use extract_deployment_ids from base."""

    def __init__(self) -> None:
        super().__init__("deployment_id_helper")

    def process(
        self,
        data: Any,
        _config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
    ) -> ProcessingResult:
        _ = (_config,)
        return self.create_result(data or {}, context=context)


class PostProcessingConfigClient:
    """
    Wrapper for Matrice post-processing config: session, stream identifiers,
    REST fetch by app deployment, and config filtering by camera_id.
    """

    def __init__(
        self,
        session: Optional[Any] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        account_number: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self._session: Optional[Any] = session
        self._access_key = access_key or os.getenv("MATRICE_ACCESS_KEY_ID", "")
        self._secret_key = secret_key or os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
        self._account_number = account_number or os.getenv("MATRICE_ACCOUNT_NUMBER") or ""

        if self._session is None and (self._access_key and self._secret_key):
            try:
                from matrice_common.session import Session

                self._session = Session(
                    access_key=self._access_key,
                    secret_key=self._secret_key,
                    account_number=self._account_number,
                )
                self.logger.info("Initialized Matrice session for post-processing config client")
            except Exception as exc:
                self.logger.error(
                    "Failed to initialize Matrice session for post-processing config client: %s",
                    exc,
                    exc_info=True,
                )
                self._session = None
        elif self._session is not None:
            self._access_key = getattr(self._session, "access_key", None) or self._access_key
            self._secret_key = getattr(self._session, "secret_key", None) or self._secret_key
        elif not self._access_key or not self._secret_key:
            self.logger.warning(
                "Missing Matrice credentials; cannot initialize session for post-processing config client"
            )

        self._config_by_camera: Dict[str, Dict[str, Any]] = {}
        self._deployment_id_helper = _DeploymentIdHelper()

    @property
    def session(self) -> Any:
        """Return the matrice_common Session (read-only)."""
        if self._session is None:
            raise RuntimeError("Session not initialized")
        return self._session

    def _to_pixel(self, normalized: Any, dimension_size: int) -> int:
        """Convert a single normalized value (0–1) to integer pixel coordinate."""
        try:
            return int(round(float(normalized) * dimension_size))
        except (TypeError, ValueError):
            return 0

    def _denormalize_points(self, points: Any, width: int, height: int) -> List[List[int]]:
        """Convert a list of [x_norm, y_norm] to [[x_px, y_px], ...]."""
        result: List[List[int]] = []
        if not isinstance(points, list):
            return result
        for pt in points:
            if not isinstance(pt, (list, tuple)) or len(pt) < 2:
                continue
            result.append(
                [
                    self._to_pixel(pt[0], width),
                    self._to_pixel(pt[1], height),
                ]
            )
        return result

    def _denormalize_zone_config(self, zone_config: Dict[str, Any], width: int, height: int) -> Dict[str, Any]:
        """Convert zone_config lines and zones from normalized to integer pixel coords."""
        out: Dict[str, Any] = copy.deepcopy(zone_config)
        lines = out.get("lines") or {}
        zones = out.get("zones") or {}
        if isinstance(lines, dict):
            out["lines"] = {
                name: self._denormalize_points(pts, width, height)
                for name, pts in lines.items()
                if isinstance(pts, list)
            }
        if isinstance(zones, dict):
            out["zones"] = {
                name: self._denormalize_points(pts, width, height)
                for name, pts in zones.items()
                if isinstance(pts, list)
            }
        return out

    def get_stream_identifiers(self, stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Return camera_id, application_id, and app_deployment_id from stream_info."""
        result: Dict[str, str] = {
            "camera_id": "",
            "application_id": "",
            "app_deployment_id": "",
        }
        if not stream_info or not isinstance(stream_info, dict):
            return result

        deployment = self._deployment_id_helper.extract_deployment_ids(stream_info)
        result["application_id"] = (deployment.get("application_id") or "").strip()
        result["app_deployment_id"] = (deployment.get("app_deployment_id") or "").strip()

        def _to_str(value: Any) -> str:
            if value is None:
                return ""
            if isinstance(value, str):
                return value.strip()
            if isinstance(value, (int, float)):
                return str(value)
            if isinstance(value, dict):
                return ""
            if isinstance(value, (list, tuple, set)):
                for item in value:
                    s = _to_str(item)
                    if s:
                        return s
                return ""
            try:
                return str(value).strip()
            except Exception:
                return ""

        def _dict_get_str(d: Any, *keys: str) -> str:
            if not isinstance(d, dict):
                return ""
            for k in keys:
                val = _to_str(d.get(k))
                if val:
                    return val
            return ""

        def _extract_camera_id_from_topic(topic_val: Any) -> str:
            topic = _to_str(topic_val)
            if not topic:
                return ""
            for suffix in ("_input_topic", "_input-topic"):
                if topic.endswith(suffix):
                    return topic[: -len(suffix)].strip()
            for marker in ("_input_topic", "_input-topic"):
                if marker in topic:
                    return topic.split(marker)[0].strip()
            return ""

        def _extract_camera_id_from_frame_id(frame_id_val: Any) -> str:
            fid = _to_str(frame_id_val)
            if not fid or not fid.startswith("legacy_"):
                return ""
            parts = fid.split("_")
            if len(parts) >= 3:
                candidate = parts[1].strip()
                if candidate and re.fullmatch(r"[0-9a-f]{8,}", candidate, re.IGNORECASE):
                    return candidate
            return ""

        input_settings = stream_info.get("input_settings") or {}
        if not isinstance(input_settings, dict):
            input_settings = {}

        camera_info_root = stream_info.get("camera_info") or {}
        if not isinstance(camera_info_root, dict):
            camera_info_root = {}

        camera_info_input_settings = input_settings.get("camera_info") or {}
        if not isinstance(camera_info_input_settings, dict):
            camera_info_input_settings = {}

        input_stream = input_settings.get("input_stream") or {}
        if not isinstance(input_stream, dict):
            input_stream = {}

        camera_info_input_stream = input_stream.get("camera_info") or {}
        if not isinstance(camera_info_input_stream, dict):
            camera_info_input_stream = {}

        input_streams = stream_info.get("input_streams") or []
        input_stream_candidates: List[Dict[str, Any]] = []
        if isinstance(input_streams, list):
            for item in input_streams:
                if not isinstance(item, dict):
                    continue
                inner = item.get("input_stream", item)
                if not isinstance(inner, dict):
                    continue
                input_stream_candidates.append(inner)

        def _camera_id_from_camera_info(ci: Dict[str, Any]) -> str:
            return _dict_get_str(ci, "camera_id", "cameraId", "_id", "id")

        topic_camera_id = _extract_camera_id_from_topic(stream_info.get("topic")) or _extract_camera_id_from_topic(
            input_settings.get("topic")
        )
        if not topic_camera_id:
            topics_val = stream_info.get("topics")
            if isinstance(topics_val, (list, tuple, set)):
                for t in topics_val:
                    topic_camera_id = _extract_camera_id_from_topic(t)
                    if topic_camera_id:
                        break

        if topic_camera_id:
            result["camera_id"] = topic_camera_id
        if not result["camera_id"]:
            result["camera_id"] = (
                _dict_get_str(stream_info, "camera_id", "cameraId")
                or _dict_get_str(input_settings, "camera_id", "cameraId")
                or _camera_id_from_camera_info(camera_info_root)
                or _camera_id_from_camera_info(camera_info_input_settings)
                or _camera_id_from_camera_info(camera_info_input_stream)
            )
            if not result["camera_id"]:
                for candidate in input_stream_candidates:
                    result["camera_id"] = _dict_get_str(candidate, "camera_id", "cameraId", "_id", "id")
                    if result["camera_id"]:
                        break
            if not result["camera_id"]:
                result["camera_id"] = topic_camera_id or ""
        if not result["camera_id"]:
            result["camera_id"] = _extract_camera_id_from_frame_id(stream_info.get("frame_id"))

        if result["camera_id"] and not isinstance(result["camera_id"], str):
            result["camera_id"] = str(result["camera_id"])
        return result

    def get_post_processing_configs_by_app_deployment(
        self,
        app_deployment_id: str,
    ) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Fetch all post-processing configs for an app deployment via Matrice API."""
        try:
            from matrice_common.rpc import RPC
        except ImportError:
            RPC = None

        rpc = RPC(
            access_key=self._access_key,
            secret_key=self._secret_key,
        )
        path = f"/v1/inference/post_processing_configs/by_app_deployment/{app_deployment_id}"

        try:
            response = rpc.get(path)
            if isinstance(response, dict) and response.get("success"):
                return (
                    response.get("data", []),
                    None,
                    response.get("message", "Success"),
                )
            err = response.get("message", "Unknown error") if isinstance(response, dict) else str(response)
            return None, err, None
        except Exception as e:
            self.logger.exception("get_post_processing_configs_by_app_deployment failed")
            return None, str(e), None

    def filter_configs_by_camera_id(
        self,
        configs: List[Dict[str, Any]],
        camera_id: str,
    ) -> List[Dict[str, Any]]:
        """Filter config documents to those containing config for the given camera_id."""
        if not camera_id or not configs:
            return []
        out = []
        for doc in configs:
            if not isinstance(doc, dict):
                continue
            post = doc.get("postProcessing") or {}
            if isinstance(post, dict) and camera_id in post:
                out.append(doc)
        return out

    def get_config_for_camera(self, camera_id: str) -> Optional[Dict[str, Any]]:
        """Return cached post-processing config for a camera."""
        if not camera_id:
            return None
        return self._config_by_camera.get(str(camera_id))

    def set_config_cache_from_api(self, configs: List[Dict[str, Any]]) -> None:
        """Populate the config cache from a list of configs (e.g. from REST API)."""
        for doc in configs or []:
            if not isinstance(doc, dict):
                continue
            post = doc.get("postProcessing") or {}
            if not isinstance(post, dict):
                continue
            for cid, cam_cfg in post.items():
                if not cid:
                    continue
                cid = str(cid)
                self._config_by_camera[cid] = {
                    "_id": doc.get("_id"),
                    "_idCamera": doc.get("_idCamera"),
                    "_idApplication": doc.get("_idApplication"),
                    "_idAppDeployment": doc.get("_idAppDeployment"),
                    "postProcessing": {cid: cam_cfg},
                    "createdAt": doc.get("createdAt"),
                    "updatedAt": doc.get("updatedAt"),
                }
        self.logger.info("Config cache updated from API: %d camera(s)", len(self._config_by_camera))

    def get_resolution(self, camera_id: str) -> Tuple[Optional[int], Optional[int]]:
        """Get frame width and height for a camera by its ID."""
        try:
            from matrice.camera_management import CameraManagement
        except ImportError:
            self.logger.warning("matrice.camera_management not available; install py_matrice for get_resolution")
            return (None, None)
        try:
            camera_mgmt = CameraManagement(self.session)
            all_cameras, fetch_error, _ = camera_mgmt.get_camera_streams_by_account()
            if fetch_error or not all_cameras:
                self.logger.warning("get_resolution: fetch_error=%s or no cameras", fetch_error)
                return (None, None)
            for cam in all_cameras:
                if not isinstance(cam, dict):
                    continue
                cid = cam.get("id") or cam.get("_id")
                if cid != camera_id:
                    continue
                settings = cam.get("customStreamSettings") or {}
                if not isinstance(settings, dict):
                    return (None, None)
                w = settings.get("width")
                h = settings.get("height")
                if w is not None and h is not None:
                    return (int(w), int(h))
                return (None, None)
            self.logger.warning("get_resolution: camera_id %s not found", camera_id)
            return (None, None)
        except Exception:
            self.logger.exception("get_resolution failed for camera_id=%s", camera_id)
            return (None, None)

    def denormalize_config(
        self,
        config: Union[Dict[str, Any], List[Dict[str, Any]]],
        width: int,
        height: int,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Convert normalized (0–1) line/zone coordinates to integer pixel coordinates."""
        if isinstance(config, list):
            return [self.denormalize_config(doc, width, height) for doc in config]
        if not isinstance(config, dict):
            return config
        out = copy.deepcopy(config)
        post = out.get("postProcessing") or {}
        if not isinstance(post, dict):
            return out
        for cid, cam_cfg in list(post.items()):
            if not isinstance(cam_cfg, dict):
                continue
            zone_cfg = cam_cfg.get("zone_config")
            if isinstance(zone_cfg, dict):
                post[cid] = {
                    **cam_cfg,
                    "zone_config": self._denormalize_zone_config(zone_cfg, width, height),
                }
        return out


def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Fold AI-style payloads into ``postProcessing`` so denormalization and zone extraction work.

    Supported shapes:

    1. Standard Matrice document: ``{"postProcessing": {camera_id: {..., "zone_config": {...}}}}``
    2. AI export (camera id as top-level key)::

           {"<camera_id>": {"zone_config": {"lines": {}, "zones": {"Polygon 1": [[nx,ny],...], ...}}}}

       Polygon / zone labels are kept as the user defined them (e.g. ``Polygon 1``); use the same
       strings in ``count_thresholds`` / ``zone_settings`` when overriding per zone.

    Top-level camera blocks are merged into ``postProcessing`` only for camera ids that are not
    already present under ``postProcessing`` (no overwrite).
    """
    if not isinstance(doc, dict):
        return doc

    reserved = {
        "_id",
        "_idCamera",
        "_idApplication",
        "_idAppDeployment",
        "postProcessing",
        "postprocessing",
        "createdAt",
        "updatedAt",
        "created_at",
        "updated_at",
    }
    lifted: Dict[str, Any] = {}
    for k, v in doc.items():
        if k in reserved or not isinstance(v, dict):
            continue
        zc = v.get("zone_config")
        if not isinstance(zc, dict):
            continue
        if zc.get("zones") or zc.get("lines") is not None:
            lifted[k] = v
    if not lifted:
        return doc

    out = copy.deepcopy(doc)
    post = dict(out.get("postProcessing") or {})
    for k, v in lifted.items():
        if k not in post:
            post[k] = v
    out["postProcessing"] = post
    return out


# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------


@dataclass
class OvercrowdingDetectionConfig(BaseConfig):
    zone_config: Optional[ZoneConfig] = None

    # Required thresholds
    count_thresholds: Dict[str, int] = field(default_factory=lambda: {"global": 10})

    # Stability controls
    persistence_frames: int = 3
    recovery_frames: int = 3

    # Severity controls
    warning_ratio: float = 0.8
    recovery_ratio: float = 0.9  # hysteresis exit ratio

    # Category mapping
    index_to_category: Optional[Dict[int, str]] = None
    target_categories: List[str] = field(default_factory=lambda: ["person"])

    alert_config: Optional[AlertConfig] = None

    # Optional per-zone overrides (threshold, warning_ratio, recovery_ratio, cooldown).
    # None = omit; same as an empty dict.
    zone_settings: Optional[Dict[str, Dict[str, Any]]] = None

    # Tracker selection — same flags and implementation as ``people_counting`` use case.
    enable_advanced_tracker: bool = True
    enable_simple_tracker: bool = False

    def validate(self) -> List[str]:
        errors = super().validate()

        if not self.count_thresholds:
            errors.append("count_thresholds must be provided.")

        for z, t in self.count_thresholds.items():
            if t <= 0:
                errors.append(f"Threshold for zone '{z}' must be positive.")

        if self.persistence_frames <= 0:
            errors.append("persistence_frames must be positive.")

        if self.recovery_frames <= 0:
            errors.append("recovery_frames must be positive.")

        if not (0 < self.warning_ratio <= 1.0):
            errors.append("warning_ratio must be between 0 and 1.")

        if not (0 < self.recovery_ratio <= 1.0):
            errors.append("recovery_ratio must be between 0 and 1.")

        if self.zone_config:
            errors.extend(self.zone_config.validate())

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# ------------------------------------------------------------------------------
# Processor
# ------------------------------------------------------------------------------


class OvercrowdingDetectionUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("overcrowding_detection")
        self.category = "safety"
        self.CASE_TYPE = "overcrowding_detection"
        self.CASE_VERSION = "1.0"

        self._zone_states: Dict[str, Dict[str, Any]] = {}
        self._zone_alert_timestamps: Dict[str, float] = {}
        self._frame_counter = 0

        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[OvercrowdingDetectionConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False
        self.tracker: Any = None
        self._total_frame_counter: int = 0

    # --------------------------------------------------------------------------
    # API geometry resolution (Matrice post-processing config → pixel zones)
    # --------------------------------------------------------------------------

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set client used to resolve zones from deployment/camera post-processing config."""
        self._config_client = client

    def _start_geometry_resolver(
        self,
        config: OvercrowdingDetectionConfig,
        stream_info: Dict[str, Any],
    ) -> None:
        if self._geometry_thread is not None:
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info("OvercrowdingDetection: zone geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "OvercrowdingDetection: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "OvercrowdingDetection: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(
            target=_resolver,
            daemon=True,
            name="overcrowding-zone-geometry-resolver",
        )
        self._geometry_thread = t
        t.start()
        self.logger.info("OvercrowdingDetection: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: OvercrowdingDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[OvercrowdingDetectionConfig]:
        """Resolve ``zone_config`` from PostProcessingConfigClient (UI zones → pixel coords).

        Supports one or more named zones under ``zone_config.zones``. Returns a new
        config with ``zone_config`` set, or ``None`` if unavailable.
        """
        if stream_info is not None and not isinstance(stream_info, dict):
            self.logger.warning(
                "OvercrowdingDetection: _resolve_geometry_from_api skipped (stream_info must be dict, got %s)",
                type(stream_info).__name__,
            )
            return None

        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "OvercrowdingDetection: _resolve_geometry_from_api skipped "
                        "(no config_client; set MATRICE_ACCESS_KEY_ID, "
                        "MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API zone resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "OvercrowdingDetection: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info:
            self.logger.info("OvercrowdingDetection: _resolve_geometry_from_api skipped (no stream_info)")
            return None
        if not client:
            self.logger.info("OvercrowdingDetection: _resolve_geometry_from_api skipped (no config_client)")
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "OvercrowdingDetection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )

        if not app_deployment_id or not camera_id:
            self.logger.info("_resolve_geometry_from_api: returning None (missing app_deployment_id or camera_id)")
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            self.logger.info(
                "_resolve_geometry_from_api: returning None "
                "(get_post_processing_configs_by_app_deployment: err=%r, configs count=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        self.logger.info("_resolve_geometry_from_api: configs=%r", configs)

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (filter_configs_by_camera_id: no config for camera_id=%s)",
                camera_id,
            )
            return None

        doc = filtered[0]
        doc = lift_ai_camera_zones_into_post_processing(doc)
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (get_resolution: width=%r, height=%r for camera_id=%s)",
                width,
                height,
                camera_id,
            )
            return None

        self.logger.info("_resolve_geometry_from_api: width=%r, height=%r", width, height)

        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}

        if not isinstance(zones_px, dict) or not zones_px:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (no zones found in zone_config for camera_id=%s)",
                camera_id,
            )
            return None

        self.logger.info("_resolve_geometry_from_api: zones_px=%r", zones_px)

        zones_dict: Dict[str, List[List[float]]] = {}
        for name, points in zones_px.items():
            if not isinstance(points, list) or len(points) < 3:
                self.logger.warning(
                    "OvercrowdingDetection: skipping zone %r (need list of >= 3 points)",
                    name,
                )
                continue
            row: List[List[float]] = []
            for pt in points:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    row.append([float(pt[0]), float(pt[1])])
                else:
                    row = []
                    break
            if len(row) >= 3:
                zones_dict[str(name)] = row
            else:
                self.logger.warning("OvercrowdingDetection: skipping zone %r (invalid point list)", name)
        new_zone_config = ZoneConfig(zones=zones_dict)

        self.logger.info(
            "OvercrowdingDetection: resolved %d zone(s) from API: %s",
            len(zones_dict),
            list(zones_dict.keys()),
        )
        return replace(config, zone_config=new_zone_config)

    def _normalize_detection_track_ids(self, processed_data: List[Dict[str, Any]]) -> None:
        """Align with ``people_counting``: unify alternate id keys into ``track_id``."""
        for det in processed_data:
            if not isinstance(det, dict):
                continue
            if det.get("track_id") is not None:
                continue
            for key in (
                "tracker_id",
                "tracking_id",
                "trackId",
                "trackID",
                "id",
                "object_id",
            ):
                candidate = det.get(key)
                if candidate is not None:
                    det["track_id"] = candidate
                    break

    def _simple_tracker_update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Same lightweight fallback as ``people_counting`` (frame-local ids)."""
        for i, det in enumerate(detections):
            if det.get("track_id") is None:
                det["track_id"] = f"simple_{self._total_frame_counter}_{i}"
        return detections

    def _apply_tracker_like_people_counting(
        self,
        detections: List[Dict[str, Any]],
        config: OvercrowdingDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Mirror ``PeopleCountingUseCase.process`` tracker block (AdvancedTracker + simple)."""
        processed_data = detections
        if getattr(config, "enable_advanced_tracker", True):
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig

                if self.tracker is None:
                    tracker_config = TrackerConfig(
                        track_high_thresh=0.4,
                        track_low_thresh=0.05,
                        new_track_thresh=0.3,
                        match_thresh=0.8,
                        track_buffer=int(600),
                        max_time_lost=int(1200),
                        frame_rate=25,
                    )
                    tracker_namespace = None
                    if stream_info and stream_info.get("stream_key"):
                        tracker_namespace = str(hash(stream_info["stream_key"]) % 1000000)
                    self.tracker = AdvancedTracker(tracker_config, namespace=tracker_namespace)
                    self.tracker.restore_state()
                    self.logger.info(
                        "Initialized AdvancedTracker for Overcrowding Detection "
                        "(same config as people_counting; namespace=%s)",
                        tracker_namespace,
                    )
                return self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning("AdvancedTracker failed: %s", e)
                return processed_data
        elif getattr(config, "enable_simple_tracker", False):
            return self._simple_tracker_update(processed_data)
        return processed_data

    # --------------------------------------------------------------------------
    # Main Entry (single frame per call)
    # --------------------------------------------------------------------------

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        if not isinstance(config, OvercrowdingDetectionConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                "Invalid configuration",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        stream_info_dict: Optional[Dict[str, Any]] = stream_info if isinstance(stream_info, dict) else None
        if stream_info is not None and stream_info_dict is None:
            self.logger.warning(
                "OvercrowdingDetection: stream_info must be dict, got %s; continuing without stream metadata",
                type(stream_info).__name__,
            )

        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if stream_info_dict:
                self.logger.info(
                    "OvercrowdingDetection: attempting zone geometry resolution from API (first frame, blocking)"
                )
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info_dict)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info("OvercrowdingDetection: zone geometry resolved from API and cached")
                    else:
                        self.logger.warning(
                            "OvercrowdingDetection: API returned no zone config on first "
                            "attempt; starting background retry thread (every %ds). "
                            "Using zone_config from user config until resolved.",
                            _GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, stream_info_dict)
                except Exception as exc:
                    self.logger.warning(
                        "OvercrowdingDetection: zone geometry resolution raised on first "
                        "attempt (%s); starting background retry thread (every %ds). "
                        "Using zone_config from user config until resolved.",
                        exc,
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                    self._start_geometry_resolver(config, stream_info_dict)
            else:
                self.logger.info(
                    "OvercrowdingDetection: no stream_info on first frame; using zone_config from user config"
                )

        effective_config = config
        if self._resolved_geometry_cache is not None:
            effective_config = self._resolved_geometry_cache
            self.logger.debug("OvercrowdingDetection: using API-resolved zone geometry")

        # One frame: list of detection dicts (legacy: dict of frame_id -> list takes first list)
        if isinstance(data, dict):
            self.logger.warning(
                "OvercrowdingDetection: expected list of detections for one frame; "
                "using first list value from mapping (legacy)"
            )
            frame_data: List[Dict[str, Any]] = []
            for v in data.values():
                if isinstance(v, list):
                    frame_data = v
                    break
        elif isinstance(data, list):
            frame_data = data
        else:
            context.mark_completed()
            return self.create_error_result(
                "Expected a list of detections for one frame",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if self._resolved_geometry_cache is not None:
            effective_config = self._resolved_geometry_cache

        frame_key = "0"
        if stream_info_dict:
            sf = stream_info_dict.get("input_settings", {}).get("start_frame")
            if sf is not None:
                frame_key = str(sf)

        detections = self._prepare_detections(frame_data, effective_config)
        self._normalize_detection_track_ids(detections)

        adv = getattr(effective_config, "enable_advanced_tracker", True)
        simple = getattr(effective_config, "enable_simple_tracker", False)
        if adv or simple:
            detections = self._apply_tracker_like_people_counting(detections, effective_config, stream_info_dict)
        count_unique_tracks = (adv or simple) and any(d.get("track_id") is not None for d in detections)

        zone_counts = self._count_per_zone(
            detections,
            effective_config,
            count_unique_tracks=count_unique_tracks,
        )

        self._cleanup_stale_zones(zone_counts)

        zone_results = self._evaluate_overcrowding(zone_counts, effective_config)
        alerts = self._generate_alerts(zone_results, effective_config)
        incidents = self._generate_incidents(zone_results, alerts, stream_info_dict)
        tracking_stats = self._generate_tracking_stats(detections, zone_results, alerts, stream_info_dict)
        business_analytics = self._generate_business_analytics(zone_results, alerts, stream_info_dict)

        human_text = self._build_human_text(zone_results)

        self._frame_counter += 1
        self._total_frame_counter += 1

        agg_summary = self.create_frame_wise_agg_summary(
            {frame_key: incidents},
            {frame_key: tracking_stats},
            {frame_key: business_analytics},
            {frame_key: alerts},
            {frame_key: human_text},
        )

        context.mark_completed()

        return self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

    # --------------------------------------------------------------------------
    # Detection Preparation
    # --------------------------------------------------------------------------

    def _prepare_detections(self, data, config):
        detections: List[Dict[str, Any]] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    detections.append(item)
                elif isinstance(item, list):
                    detections.extend(d for d in item if isinstance(d, dict))
        elif isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    detections.extend(d for d in value if isinstance(d, dict))
                    break

        if config.confidence_threshold is not None:
            detections = filter_by_confidence(detections, config.confidence_threshold)

        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        detections = [d for d in detections if isinstance(d, dict) and d.get("category") in config.target_categories]

        return detections

    # --------------------------------------------------------------------------
    # Zone Counting
    # --------------------------------------------------------------------------

    def _count_per_zone(
        self,
        detections: List[Dict[str, Any]],
        config: OvercrowdingDetectionConfig,
        *,
        count_unique_tracks: bool = False,
    ) -> Dict[str, int]:
        if config.zone_config and config.zone_config.zones:
            zones = config.zone_config.zones
        else:
            zones = {"global": None}

        counts: Dict[str, int] = {}

        for zone_name, polygon in zones.items():
            if polygon is None:
                if count_unique_tracks:
                    tids = {d["track_id"] for d in detections if d.get("track_id") is not None}
                    counts[zone_name] = len(tids)
                else:
                    counts[zone_name] = len(detections)
                continue

            poly_points = [(p[0], p[1]) for p in polygon]

            if count_unique_tracks:
                in_zone: set[Any] = set()
                for det in detections:
                    tid = det.get("track_id")
                    if tid is None:
                        continue
                    bbox = det.get("bounding_box") or det.get("bbox")
                    if not bbox:
                        continue
                    cx, cy = self._bbox_center(bbox)
                    if point_in_polygon((cx, cy), poly_points):
                        in_zone.add(tid)
                counts[zone_name] = len(in_zone)
            else:
                count = 0
                for det in detections:
                    bbox = det.get("bounding_box") or det.get("bbox")
                    if not bbox:
                        continue
                    cx, cy = self._bbox_center(bbox)
                    if point_in_polygon((cx, cy), poly_points):
                        count += 1
                counts[zone_name] = count

        return counts

    # --------------------------------------------------------------------------
    # Stateful Evaluation
    # --------------------------------------------------------------------------

    def _compute_severity(self, _zone: str, ratio: float, is_active: bool, warning_ratio: float, config):
        # AlertConfig severity override
        _ = (_zone,)
        if config.alert_config and hasattr(config.alert_config, "severity_mapping"):
            mapping = getattr(config.alert_config, "severity_mapping", {})

            # Expect mapping like {"warning": 0.8, "critical": 1.0}
            chosen = "normal"
            for level, threshold in sorted(mapping.items(), key=lambda x: x[1]):
                if ratio >= threshold:
                    chosen = level
            return chosen

        # Default fallback
        if is_active:
            return "critical"
        elif ratio >= warning_ratio:
            return "warning"
        else:
            return "normal"

    def _evaluate_overcrowding(self, zone_counts, config):
        results = {}
        for zone, count in zone_counts.items():
            # --- Per-zone overrides ---
            zone_cfg = (config.zone_settings or {}).get(zone, {})
            threshold = zone_cfg.get(
                "threshold",
                config.count_thresholds.get(zone, config.count_thresholds.get("global")),
            )

            warning_ratio = zone_cfg.get("warning_ratio", config.warning_ratio)
            recovery_ratio = zone_cfg.get("recovery_ratio", config.recovery_ratio)

            exit_threshold = threshold * recovery_ratio
            ratio = count / threshold if threshold else 0.0

            if zone not in self._zone_states:
                self._zone_states[zone] = {
                    "violation_streak": 0,
                    "recovery_streak": 0,
                    "is_active": False,
                    "start_timestamp": None,
                }

            state = self._zone_states[zone]

            # ENTER
            if count > threshold:
                state["violation_streak"] += 1
                state["recovery_streak"] = 0

                if state["violation_streak"] >= config.persistence_frames and not state["is_active"]:
                    state["is_active"] = True
                    state["start_timestamp"] = time.time()

            # EXIT (Hysteresis)
            elif count <= exit_threshold:
                state["recovery_streak"] += 1
                state["violation_streak"] = 0

                if state["recovery_streak"] >= config.recovery_frames and state["is_active"]:
                    state["is_active"] = False

            severity = self._compute_severity(zone, ratio, state["is_active"], warning_ratio, config)

            results[zone] = {
                "count": count,
                "threshold": threshold,
                "ratio": round(ratio, 3),
                "severity": severity,
                "is_overcrowded": state["is_active"],
            }
        return results

    # --------------------------------------------------------------------------
    # Alert Generation with Cooldown
    # --------------------------------------------------------------------------

    def _generate_alerts(self, zone_results, config):
        alerts = []

        if not config.alert_config:
            return alerts

        alert_type_cfg = getattr(config.alert_config, "alert_type", ["Default"])
        alert_value_cfg = getattr(config.alert_config, "alert_value", ["JSON"])
        alert_type = alert_type_cfg[0]
        settings_map = {t: v for t, v in zip(alert_type_cfg, alert_value_cfg)}

        global_cooldown = config.alert_config.alert_cooldown or 0
        now_ts = time.time()

        for zone, stats in zone_results.items():
            if stats["severity"] != "critical":
                continue

            zone_cfg = (config.zone_settings or {}).get(zone, {})
            zone_cooldown = zone_cfg.get("cooldown", global_cooldown)

            if not self._should_trigger_alert(zone, zone_cooldown, now_ts):
                continue

            alert = self.create_alert_object(
                alert_type,
                f"alert_overcrowding_{zone}_{self._frame_counter}",
                self.CASE_TYPE,
                stats["threshold"],
                ascending=True,
                settings=settings_map,
            )

            alert["current_value"] = stats["count"]
            alert["zone"] = zone
            alert["severity"] = stats["severity"]

            alerts.append(alert)

            self._zone_alert_timestamps[zone] = now_ts

        return alerts

    def _should_trigger_alert(self, zone, cooldown, now_ts):
        last_ts = self._zone_alert_timestamps.get(zone)
        if last_ts is None:
            return True
        return (now_ts - last_ts) >= cooldown

    # --------------------------------------------------------------------------
    # Incident Generation
    # --------------------------------------------------------------------------

    def _generate_incidents(self, zone_results, alerts, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)
        incidents = []

        for zone, stats in zone_results.items():
            if not stats["is_overcrowded"]:
                continue

            state = self._zone_states.get(zone, {})
            start_time = state.get("start_timestamp")

            human_text = (
                f"Overcrowding detected in zone '{zone}' | "
                f"Count: {stats['count']} | "
                f"Threshold: {stats['threshold']} | "
                f"Severity: {stats['severity']}"
            )
            zone_alerts = [a for a in alerts if a.get("zone") == zone]

            incident = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{zone}_{self._frame_counter}",
                incident_type=self.CASE_TYPE,
                severity_level=stats["severity"],
                human_text=human_text,
                camera_info=camera_info,
                alerts=zone_alerts,
                alert_settings=[],
                start_time=start_time,
                end_time=None,
            )

            incidents.append(incident)

        return incidents

    # --------------------------------------------------------------------------
    # Tracking Stats
    # --------------------------------------------------------------------------

    def _generate_tracking_stats(self, detections, zone_results, alerts, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_count = len(detections)

        tracking_stat = self.create_tracking_stats(
            total_counts=[{"category": "person", "count": total_count}],
            current_counts=[{"category": "person", "count": total_count}],
            detections=[
                self.create_detection_object("person", d.get("bounding_box") or d.get("bbox")) for d in detections
            ],
            human_text=self._build_human_text(zone_results),
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=[],
            reset_settings=[],
        )

        tracking_stat["zone_statistics"] = zone_results

        return [tracking_stat]

    # --------------------------------------------------------------------------
    # Business Analytics
    # --------------------------------------------------------------------------

    def _generate_business_analytics(self, zone_results, alerts, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics = self.create_business_analytics(
            analysis_name="overcrowding",
            statistics=zone_results,
            human_text=self._build_human_text(zone_results),
            camera_info=camera_info,
            alerts=alerts,
        )

        return [analytics]

    # --------------------------------------------------------------------------
    # Human Text
    # --------------------------------------------------------------------------

    def _build_human_text(self, zone_results):
        lines = ["Overcrowding Status:"]
        for zone, stats in zone_results.items():
            lines.append(
                f"{zone}: {stats['count']}/{stats['threshold']} (ratio={stats['ratio']}) severity={stats['severity']}"
            )
        return "\n".join(lines)

    # --------------------------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------------------------

    def _cleanup_stale_zones(self, zone_counts):
        active_zones = set(zone_counts.keys())

        for z in list(self._zone_states.keys()):
            if z not in active_zones:
                del self._zone_states[z]

        for z in list(self._zone_alert_timestamps.keys()):
            if z not in active_zones:
                del self._zone_alert_timestamps[z]

    def _bbox_center(self, bbox: Any) -> Tuple[float, float]:
        """
        bbox formats supported:
        - dict xmin,ymin,xmax,ymax
        - dict x1,y1,x2,y2
        - list [x1,y1,x2,y2]
        """
        if not bbox:
            return (0.0, 0.0)

        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
            return ((float(x1) + float(x2)) / 2.0, (float(y1) + float(y2)) / 2.0)

        if isinstance(bbox, dict):
            if "xmin" in bbox:
                return (
                    (float(bbox.get("xmin", 0)) + float(bbox.get("xmax", 0))) / 2.0,
                    (float(bbox.get("ymin", 0)) + float(bbox.get("ymax", 0))) / 2.0,
                )
            if "x1" in bbox:
                return (
                    (float(bbox.get("x1", 0)) + float(bbox.get("x2", 0))) / 2.0,
                    (float(bbox.get("y1", 0)) + float(bbox.get("y2", 0))) / 2.0,
                )

        return (0.0, 0.0)

    # ----------------------------
    # Timestamp helpers (copied style from people_counting)
    # ----------------------------
    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

        if not isinstance(timestamp, str):
            return str(timestamp)

        timestamp_clean = timestamp.replace(" UTC", "").strip()
        if "." in timestamp_clean:
            timestamp_clean = timestamp_clean.split(".")[0]

        try:
            if timestamp_clean.count("-") >= 2:
                parts = timestamp_clean.split("-")
                if len(parts) >= 4:
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                        "input_settings", {}
                    ).get("original_fps", 30)
                _ = self._format_timestamp_for_video(start_time)
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                    "input_settings", {}
                ).get("original_fps", 30)
            _ = self._format_timestamp_for_video(start_time)
            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
        else:
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except Exception:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        if not stream_info:
            return "00:00:00"

        if precision:
            if self.start_timer is None:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        else:
            if self.start_timer is not None and self.start_timer != "NA":
                return self._format_timestamp(self.start_timer)

            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except Exception:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")
