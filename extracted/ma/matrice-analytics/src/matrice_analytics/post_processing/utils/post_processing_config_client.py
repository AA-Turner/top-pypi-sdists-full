"""Matrice post-processing config fetch + zone coordinate denormalization (shared across use cases)."""

import copy
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple, Union

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from .location_name_cache import LocationNameCache

GEOMETRY_RETRY_INTERVAL = 30  # Seconds between background retry attempts when API fails

_OBJECT_ID_RE = re.compile(r"^[0-9a-f]{24}$", re.IGNORECASE)
_NULL_OBJECT_ID = "0" * 24
_location_name_cache = LocationNameCache()


def looks_like_object_id(value: Any) -> bool:
    """Return True when ``value`` looks like a MongoDB ObjectId (24 hex chars)."""
    if value is None:
        return False
    text = str(value).strip()
    return bool(text and _OBJECT_ID_RE.match(text))


def is_null_object_id(value: Any) -> bool:
    """Return True for the all-zero placeholder ObjectId (unset location)."""
    if value is None:
        return False
    return str(value).strip().lower() == _NULL_OBJECT_ID


def is_resolvable_location_id(value: Any) -> bool:
    """Return True when ``value`` is a real location ObjectId worth API lookup."""
    return looks_like_object_id(value) and not is_null_object_id(value)


def normalize_location_id(value: Any) -> str:
    """Return a stripped location id, or empty for unset / null ObjectId placeholders."""
    if value is None:
        return ""
    text = str(value).strip()
    if not text or is_null_object_id(text):
        return ""
    return text


class _DeploymentIdHelper(BaseProcessor):
    """Minimal BaseProcessor subclass only to use extract_deployment_ids from base (no logic duplication)."""

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
        self._account_number = account_number or os.getenv("MATRICE_ACCOUNT_NUMBER", "") or ""

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
            self._account_number = getattr(self._session, "account_number", None) or self._account_number
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

    @staticmethod
    def _is_normalized_points(points: Any) -> bool:
        """Return True when every coordinate value in ``points`` is in the range [0, 1].

        A polygon is considered normalized when **all** x and y values satisfy
        ``0 <= v <= 1``.  If any value exceeds 1 the points are already in pixel
        space and must not be scaled again.
        """
        if not isinstance(points, list) or not points:
            return False
        for pt in points:
            if not isinstance(pt, (list, tuple)) or len(pt) < 2:
                return False
            for v in pt[:2]:
                try:
                    fv = float(v)
                except (TypeError, ValueError):
                    return False
                if not (0.0 <= fv <= 1.0):
                    return False
        return True

    def _denormalize_points(self, points: Any, width: int, height: int) -> List[List[int]]:
        """Convert a list of [x_norm, y_norm] to [[x_px, y_px], ...].

        If the points are already in pixel space (any value > 1) they are
        returned as-is (cast to int) without any scaling.
        """
        result: List[List[int]] = []
        if not isinstance(points, list):
            return result

        if not self._is_normalized_points(points):
            for pt in points:
                if not isinstance(pt, (list, tuple)) or len(pt) < 2:
                    continue
                result.append([int(round(float(pt[0]))), int(round(float(pt[1])))])
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
        """Convert zone_config lines and zones from normalized to integer pixel coords.

        Each polygon is checked individually: if its points are already in pixel
        space (any coordinate value > 1) the polygon is left unchanged.  Only
        polygons whose coordinates are all in [0, 1] are scaled.
        """
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
            # Reuse the client's existing Session/RPC instead of building a new
            # RPC (and its thread pool) on every call. ``self.session`` raises
            # when no session is configured; that is handled the same way as a
            # failed RPC init below.
            rpc = self.session.rpc
        except Exception as e:
            self.logger.exception("Session/RPC not available for config fetch")
            return None, str(e), None
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

    @staticmethod
    def _metadata_from_camera_record(cam: Dict[str, Any]) -> Dict[str, str]:
        """Extract display fields from a CameraManagement stream record."""

        def _get(*keys: str) -> str:
            for key in keys:
                val = cam.get(key)
                if val is not None and str(val).strip():
                    return str(val).strip()
            return ""

        location_id = normalize_location_id(_get("locationId", "location_id", "_idLocation"))
        location = _get("locationName", "location", "location_name")
        if looks_like_object_id(location):
            location = ""
        return {
            "camera_name": _get("cameraName", "camera_name", "name", "streamName", "displayName"),
            "camera_group": _get("cameraGroup", "camera_group", "groupName", "group"),
            "location": location,
            "location_id": location_id,
        }

    def get_camera_metadata(self, camera_id: str) -> Dict[str, str]:
        """Look up human-readable camera fields by id via CameraManagement API."""
        empty = {"camera_name": "", "camera_group": "", "location": "", "location_id": ""}
        if not camera_id:
            return empty
        try:
            from matrice.camera_management import CameraManagement
        except ImportError:
            self.logger.warning("matrice.camera_management not available; install py_matrice for camera metadata")
            return empty
        try:
            camera_mgmt = CameraManagement(self.session)
            all_cameras, fetch_error, _ = camera_mgmt.get_camera_streams_by_account()
            if fetch_error or not all_cameras:
                self.logger.warning("get_camera_metadata: fetch_error=%s or no cameras", fetch_error)
                return empty
            for cam in all_cameras:
                if not isinstance(cam, dict):
                    continue
                cid = str(cam.get("id") or cam.get("_id") or "")
                if cid != camera_id:
                    continue
                return self._metadata_from_camera_record(cam)
            self.logger.warning("get_camera_metadata: camera_id %s not found", camera_id)
            return empty
        except Exception:
            self.logger.exception("get_camera_metadata failed for camera_id=%s", camera_id)
            return empty

    def fetch_location_name(self, location_id: str) -> str:
        """Resolve a human-readable location name from a location ObjectId."""
        if not location_id or is_null_object_id(location_id):
            return ""
        cached = _location_name_cache.resolved(location_id)
        if cached is not None:
            return cached
        if self._session is None:
            return ""
        # A recent failure suppresses the request, but only for a minute: caching the
        # failure forever pinned "" onto every row for this location (INC-2606).
        if not _location_name_cache.should_fetch(location_id):
            return ""
        try:
            endpoint = f"/v1/inference/get_location/{location_id}"
            response = self.session.rpc.get(endpoint)
            if isinstance(response, dict) and response.get("success"):
                data = response.get("data") or {}
                name = str(data.get("locationName") or "").strip()
                if name:
                    _location_name_cache.store(location_id, name)
                    return name
        except Exception:
            self.logger.exception("fetch_location_name failed for location_id=%s", location_id)
        _location_name_cache.note_failure(location_id)
        return ""

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
