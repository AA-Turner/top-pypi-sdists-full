"""
Fence climbing in-zone use case (simple variant).

Single-shot, stateless rule: for every detection from a YOLO-style model,
project the bbox to its bottom-center (the "leg point") and test whether
that point lies inside a user-supplied polygon. Each in-zone detection
becomes its own alert + incident.

No tracking, no consecutive-frame confirmation, no vertical-displacement
check. Compare with `fence_climbing_detection` for the stateful variant.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping
from ..utils.geometry_utils import point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Fallback camera key when stream_info carries no camera identifier.
_DEFAULT_CAMERA_ID = "camera"


def _resolve_manager_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
    """Resolve the camera key used by IncidentManager state tracking."""
    if not stream_info:
        return _DEFAULT_CAMERA_ID
    inp = stream_info.get("input_settings")
    if not isinstance(inp, dict):
        inp = {}
    camera_info = stream_info.get("camera_info")
    if not isinstance(camera_info, dict):
        camera_info = {}
    camera_id = (
        stream_info.get("camera_id")
        or inp.get("camera_id")
        or camera_info.get("camera_id")
        or stream_info.get("stream_key")
    )
    return str(camera_id) if camera_id else _DEFAULT_CAMERA_ID


# ---------------------------------------------------------------------- #
# Config
# ---------------------------------------------------------------------- #


@dataclass
class FenceClimbingWithZoneConfig(BaseConfig):
    """Configuration for `fence_climbing_with_zone`.

    Attributes:
        zone_polygon: Polygon vertices in image pixel coordinates as a list
            of [x, y] pairs. Format matches `point_in_polygon`. Must have
            at least 3 vertices.
        confidence_threshold: Minimum YOLO detection score to consider.
        target_categories: Keep only detections whose `category` is in this
            list (lower-cased). Defaults to ``["person"]``.
        index_to_category: Optional class-index -> name map (YOLO classes).
        alert_config: Optional alert channel/threshold configuration.
    """

    confidence_threshold: float = 0.5
    target_categories: List[str] = field(default_factory=lambda: ["person"])

    zone_polygon: List[List[float]] = field(default_factory=list)

    index_to_category: Optional[Dict[int, str]] = None
    alert_config: Optional[AlertConfig] = None

    # Incident-manager wiring (third flow).
    session: Optional[Any] = None
    server_id: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.alert_config, dict):
            self.alert_config = AlertConfig(**self.alert_config)
        if self.target_categories:
            self.target_categories = [c.lower() for c in self.target_categories]

    def validate(self) -> List[str]:
        errors = super().validate()

        if not 0.0 <= self.confidence_threshold <= 1.0:
            errors.append("confidence_threshold must be between 0.0 and 1.0")

        if not isinstance(self.zone_polygon, list) or len(self.zone_polygon) < 3:
            errors.append("zone_polygon must be a list of at least 3 [x, y] pairs")
        else:
            for i, pt in enumerate(self.zone_polygon):
                if (
                    not isinstance(pt, (list, tuple))
                    or len(pt) != 2
                    or not all(isinstance(v, (int, float)) for v in pt)
                ):
                    errors.append(f"zone_polygon[{i}] must be a [x, y] numeric pair")
                    break

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# ---------------------------------------------------------------------- #
# Helpers
# ---------------------------------------------------------------------- #


def _bbox_leg_point(bbox: Any) -> Optional[tuple]:
    """Return the bottom-center (x_center, y_max) of a bbox, or None on bad input.

    Accepts list ``[x1, y1, x2, y2]`` or dicts keyed by
    ``xmin/xmax/ymin/ymax`` or ``x1/x2/y1/y2``. Unlike the geometry-utils
    helpers, returns None instead of silently falling back to (0, 0).
    """
    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        try:
            x1, y1, x2, y2 = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
        except (TypeError, ValueError):
            return None
        return ((x1 + x2) / 2.0, y2)

    if isinstance(bbox, dict):
        if all(k in bbox for k in ("xmin", "xmax", "ymin", "ymax")):
            try:
                return ((float(bbox["xmin"]) + float(bbox["xmax"])) / 2.0, float(bbox["ymax"]))
            except (TypeError, ValueError):
                return None
        if all(k in bbox for k in ("x1", "x2", "y1", "y2")):
            try:
                return ((float(bbox["x1"]) + float(bbox["x2"])) / 2.0, float(bbox["y2"]))
            except (TypeError, ValueError):
                return None

    return None


def _polygon_as_tuples(polygon: List[List[float]]) -> List[tuple]:
    return [(float(pt[0]), float(pt[1])) for pt in polygon]


# ---------------------------------------------------------------------- #
# Use case
# ---------------------------------------------------------------------- #


class FenceClimbingWithZoneUseCase(BaseProcessor):
    """Per-detection in-zone check.

    For each YOLO detection that survives the confidence + category filters,
    test whether the bbox's bottom-center sits inside ``config.zone_polygon``.
    Every match emits one alert and one incident.
    """

    CASE_TYPE: Optional[str] = "fence_climbing_with_zone"
    CASE_VERSION: Optional[str] = "1.0"

    def __init__(self) -> None:
        super().__init__("fence_climbing_with_zone")
        self.category = "security"

        # Incident manager (third flow): owns the incident open/close lifecycle
        # and incident_res publishing.
        self._INCIDENT_LOG = "[INCIDENT_MANAGER]"
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

    # -- Incident manager lifecycle --------------------------------------- #

    def _initialize_incident_manager_once(self, config: "FenceClimbingWithZoneConfig") -> None:
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(f"{self._INCIDENT_LOG} Initializing incident manager for fence climbing (zone)...")
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info(f"{self._INCIDENT_LOG} Incident manager ready")
            else:
                self.logger.warning(
                    f"{self._INCIDENT_LOG} Incident manager unavailable; incidents will not be published"
                )
        except Exception as e:
            self.logger.error(
                f"{self._INCIDENT_LOG} Incident manager init failed: {e}",
                exc_info=True,
            )
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict,
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> bool:
        """Feed a representative incident to the manager and report state changes.

        Fire-style: the manager is called every frame with ``incident or {}`` (no
        early return on an empty dict) so it can count idle frames and publish the
        closing ``info`` transition once the zone is clear. Returns True only when
        the manager published a state change (open / severity change / close).
        """
        published = False
        camera_id = _resolve_manager_camera_id(stream_info)
        if self._incident_manager:
            try:
                published = bool(
                    self._incident_manager.process_incident(
                        camera_id=camera_id,
                        incident_data=incident or {},
                        stream_info=stream_info,
                    )
                )
                if published:
                    self.logger.info(f"{self._INCIDENT_LOG} Incident published for camera: {camera_id}")
            except Exception as e:
                self.logger.error(
                    f"{self._INCIDENT_LOG} Error publishing incident: {e}",
                    exc_info=True,
                )

        if context is not None:
            # When IncidentManager is active it owns the full open/close lifecycle.
            # Skip duplicate legacy incident_res publishes from PostProcessor.
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        return published

    # -- Schema / defaults ------------------------------------------------ #

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                    "description": "Minimum YOLO detection score",
                },
                "target_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["person"],
                    "description": "Categories accepted into the zone check",
                },
                "zone_polygon": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                    "minItems": 3,
                    "description": "Polygon vertices [[x,y], ...] in image pixel coordinates",
                },
                "index_to_category": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Optional class-index -> name map for YOLO outputs",
                },
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "alert_type": {"type": "array", "items": {"type": "string"}},
                        "alert_value": {"type": "array", "items": {"type": "string"}},
                        "alert_incident_category": {"type": "array", "items": {"type": "string"}},
                        "count_thresholds": {"type": "object"},
                    },
                },
            },
            "required": ["confidence_threshold", "zone_polygon"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides: Any) -> FenceClimbingWithZoneConfig:
        defaults: Dict[str, Any] = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "target_categories": ["person"],
            "zone_polygon": [],
        }
        defaults.update(overrides)
        return FenceClimbingWithZoneConfig(**defaults)

    # -- Main pipeline ---------------------------------------------------- #

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        try:
            if not isinstance(config, FenceClimbingWithZoneConfig):
                return self.create_error_result(
                    "Invalid configuration type for fence_climbing_with_zone",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if context is None:
                context = ProcessingContext()
            context.confidence_threshold = config.confidence_threshold

            if not self._incident_manager_initialized:
                self._initialize_incident_manager_once(config)

            frame_id = self._extract_frame_id(stream_info)
            camera_info = self.get_camera_info_from_stream(stream_info)

            detections = self._normalize_detections(data)
            detections = self._filter_detections(detections, config)

            polygon = _polygon_as_tuples(config.zone_polygon)
            in_zone_detections = self._select_in_zone(detections, polygon)

            alerts = self._build_alerts(in_zone_detections, config, frame_id)
            incidents = self._build_incidents(in_zone_detections, alerts, config, camera_info, frame_id)

            # Third flow: multiple people can be in-zone per frame, but the manager
            # tracks one incident lifecycle per camera. Feed it a single
            # representative incident ({} when the zone is clear) so it owns the
            # open/close on incident_res and sets incident_published_via_manager to
            # stop the PostProcessor legacy bridge from double-publishing.
            incident_for_manager = incidents[0] if incidents else {}
            self._send_incident_to_manager(incident_for_manager, stream_info, context=context)

            tracking_stats = self._build_tracking_stats(
                in_zone_detections, alerts, config, camera_info
            )

            human_text = self._build_human_text(in_zone_detections, frame_id)

            agg_summary = {
                str(frame_id): {
                    "incidents": incidents,
                    "tracking_stats": tracking_stats,
                    "business_analytics": {},
                    "alerts": alerts,
                    "human_text": human_text,
                }
            }

            context.mark_completed()
            return self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )

        except Exception as exc:
            self.logger.error("fence_climbing_with_zone failed: %s", exc, exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(exc),
                error_type=type(exc).__name__,
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # -- Stages ----------------------------------------------------------- #

    @staticmethod
    def _extract_frame_id(stream_info: Optional[Dict[str, Any]]) -> str:
        if not stream_info:
            return "current_frame"
        input_settings = stream_info.get("input_settings", {}) or {}
        start = input_settings.get("start_frame")
        end = input_settings.get("end_frame")
        if start is not None and end is not None and start == end:
            return str(start)
        if start is not None:
            return str(start)
        return "current_frame"

    @staticmethod
    def _normalize_detections(data: Any) -> List[Dict[str, Any]]:
        """Flatten YOLO data into a list of detection dicts.

        Accepts a flat list directly, or a dict whose first list-typed
        value is the per-frame detections (matches the convention used by
        other use cases in this module).
        """
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    return [d for d in value if isinstance(d, dict)]
        return []

    def _filter_detections(
        self,
        detections: List[Dict[str, Any]],
        config: FenceClimbingWithZoneConfig,
    ) -> List[Dict[str, Any]]:
        if config.confidence_threshold is not None:
            detections = [
                d for d in detections if float(d.get("confidence", 0.0)) >= config.confidence_threshold
            ]

        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        if config.target_categories:
            allowed = set(config.target_categories)
            detections = [
                d for d in detections if str(d.get("category", "")).lower() in allowed
            ]

        return detections

    def _select_in_zone(
        self,
        detections: List[Dict[str, Any]],
        polygon: List[tuple],
    ) -> List[Dict[str, Any]]:
        if len(polygon) < 3:
            return []

        in_zone: List[Dict[str, Any]] = []
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            leg = _bbox_leg_point(bbox)
            if leg is None:
                self.logger.debug("Skipping detection without usable bbox: %r", det)
                continue
            if point_in_polygon(leg, polygon):
                annotated = dict(det)
                annotated["leg_point"] = {"x": leg[0], "y": leg[1]}
                in_zone.append(annotated)
        return in_zone

    def _build_alerts(
        self,
        in_zone: List[Dict[str, Any]],
        config: FenceClimbingWithZoneConfig,
        frame_id: str,
    ) -> List[Dict[str, Any]]:
        if not in_zone:
            return []

        ac = config.alert_config
        alert_type = (ac.alert_type if ac else ["Default"]) or ["Default"]
        alert_value = (ac.alert_value if ac else ["JSON"]) or ["JSON"]
        settings = {t: v for t, v in zip(alert_type, alert_value)}

        alerts: List[Dict[str, Any]] = []
        for idx, det in enumerate(in_zone, start=1):
            track_or_idx = det.get("track_id") if det.get("track_id") is not None else idx
            alerts.append(
                {
                    "alert_type": alert_type,
                    "alert_id": f"fence_zone_{frame_id}_{track_or_idx}",
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": "in_zone",
                    "ascending": True,
                    "settings": settings,
                }
            )
        return alerts

    def _build_incidents(
        self,
        in_zone: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        config: FenceClimbingWithZoneConfig,
        camera_info: Dict[str, Any],
        frame_id: str,
    ) -> List[Dict[str, Any]]:
        if not in_zone:
            return []

        ac = config.alert_config
        alert_settings: List[Dict[str, Any]] = []
        if ac is not None:
            alert_settings.append(
                {
                    "alert_type": ac.alert_type or ["Default"],
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": ac.count_thresholds or {},
                    "ascending": True,
                    "settings": {
                        t: v for t, v in zip(ac.alert_type or ["Default"], ac.alert_value or ["JSON"])
                    },
                }
            )

        start_ts = self.get_high_precision_timestamp()
        incidents: List[Dict[str, Any]] = []
        for idx, det in enumerate(in_zone, start=1):
            track_or_idx = det.get("track_id") if det.get("track_id") is not None else idx
            human_text = (
                f"Person in fence zone @ frame {frame_id} "
                f"(leg=({det['leg_point']['x']:.1f},{det['leg_point']['y']:.1f}))"
            )
            incident = self.create_incident(
                incident_id=f"incident_{self.CASE_TYPE}_{frame_id}_{track_or_idx}",
                incident_type=self.CASE_TYPE,
                severity_level="critical",
                human_text=human_text,
                camera_info=camera_info,
                alerts=[alerts[idx - 1]] if idx - 1 < len(alerts) else [],
                alert_settings=alert_settings,
                start_time=start_ts,
                end_time=start_ts,
            )
            incident["offending_detection"] = det
            # incident_quant drives severity in the IncidentManager (third flow).
            # A person inside the fence zone is a maximum-severity event, so a fixed
            # quant of 100 -> "critical" keeps the manager's consecutive-frame
            # confirmation stable (same approach as fall/violence/unwanted-animal).
            incident["incident_quant"] = 100.0
            incidents.append(incident)
        return incidents

    def _build_tracking_stats(
        self,
        in_zone: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        config: FenceClimbingWithZoneConfig,
        camera_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        category_label = (config.target_categories or ["person"])[0]
        current_count = len(in_zone)

        detections_payload = [
            self.create_detection_object(
                category=det.get("category", category_label),
                bounding_box=det.get("bounding_box") or det.get("bbox") or {},
                track_id=det.get("track_id"),
            )
            for det in in_zone
        ]

        return self.create_tracking_stats(
            total_counts=[{"category": category_label, "count": current_count}],
            current_counts=[{"category": category_label, "count": current_count}],
            detections=detections_payload,
            human_text=f"{current_count} {category_label}(s) in zone",
            camera_info=camera_info,
            alerts=alerts,
        )

    @staticmethod
    def _build_human_text(in_zone: List[Dict[str, Any]], frame_id: str) -> str:
        if not in_zone:
            return f"Frame {frame_id}: no detections in fence zone"
        return f"Frame {frame_id}: {len(in_zone)} detection(s) inside fence zone"
