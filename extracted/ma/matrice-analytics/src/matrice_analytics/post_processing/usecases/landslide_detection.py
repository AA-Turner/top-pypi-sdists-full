"""
Landslide Detection Use Case for Post-Processing.

Model classes:
- 0: landslide

A single "landslide" category drives all incidents, alerts, analytics, and
visualisation outputs.  An alert is raised as soon as **at least 1** landslide
detection is present in a frame.  All landslide detections are retained;
incident severity is derived from the **total** segmentation-mask coverage in
the frame relative to the configured area reference threshold.
"""

import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    ByteTrackWrapper,
    SORTTracker,
    apply_category_mapping,
    bbox_smoothing,
    count_objects_in_zones,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class LandslideDetectionConfig(BaseConfig):
    """Configuration for landslide detection post-processing."""

    # BBox smoothing
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # Tracking (SORT / ByteTrack — same pattern as loitering_detection / area_utilization).
    enable_tracking: bool = True
    tracking_method: str = "sort"  # "sort" or "bytetrack"
    tracking_max_age: int = 30
    tracking_min_hits: int = 2
    tracking_iou_threshold: float = 0.25
    bytetrack_track_thresh: float = 0.25
    bytetrack_match_thresh: float = 0.80
    enable_simple_tracker: bool = False

    confidence_threshold: float = 0.15
    enable_class_aggregation: bool = False
    class_aggregation_window_size: int = 30

    zone_config: Optional[Dict[str, List[List[float]]]] = None

    # Only one active category for this use case.
    usecase_categories: List[str] = field(default_factory=lambda: ["landslide"])
    target_categories: List[str] = field(default_factory=lambda: ["landslide"])

    # Reference frame-coverage percentage used to map total mask area to severity
    # bands (low / medium / high / warning / critical).  Does NOT filter
    # detections — every landslide instance is counted.  Default: 50 %.
    landslide_area_percent: float = 50.0

    # Fire an alert as soon as ≥ 1 landslide detection is present.
    alert_config: Optional[AlertConfig] = field(default_factory=lambda: AlertConfig(count_thresholds={"landslide": 1}))

    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "landslide"})


# ---------------------------------------------------------------------------
# Processor
# ---------------------------------------------------------------------------


class LandslideDetectionUseCase(BaseProcessor):
    """Post-processor for landslide detection model outputs."""

    CATEGORY_DISPLAY: Dict[str, str] = {"landslide": "Landslide"}

    def _display_category(self, category: str) -> str:
        """Return human-friendly category label for outputs."""
        return self.CATEGORY_DISPLAY.get(category, category)

    def _init_tracker(self, config: LandslideDetectionConfig, stream_info: Optional[Dict[str, Any]]) -> None:
        """Initialize SORT or ByteTrack (same path as loitering_detection / area_utilization)."""
        if self.tracker is not None:
            return

        method = str(getattr(config, "tracking_method", "sort")).lower().strip()

        # F10b S9 (consolidation-plan.md Step 9): route the legacy SORT/ByteTrack
        # default onto the AdvancedTracker seam. MATRICE_LEGACY_SORT=1 keeps the
        # pre-migration path alive for one release (kill-switch, plan §7).
        if method in ("sort", "bytetrack") and os.environ.get("MATRICE_LEGACY_SORT") != "1":
            self.tracker = ConfigDrivenTracker().get_shared_tracker(
                profile=TrackerProfile.DEFAULT,
                **legacy_sort_tracker_overrides(config, method),
            )
            self.logger.info("Landslide detection: initialized AdvancedTracker (seam) for legacy %s method", method)
            return

        if method == "sort":
            self.tracker = SORTTracker(
                iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
                max_age=int(getattr(config, "tracking_max_age", 30)),
                min_hits=int(getattr(config, "tracking_min_hits", 2)),
            )
            self.logger.info("Landslide detection: initialized SORTTracker")
            return

        if method == "bytetrack":
            fps = 30.0
            try:
                if stream_info:
                    fps_val = stream_info.get("input_settings", {}).get("original_fps")
                    if fps_val and float(fps_val) > 1e-6:
                        fps = float(fps_val)
            except Exception:
                fps = 30.0

            try:
                self.tracker = ByteTrackWrapper(
                    fps=float(fps),
                    track_thresh=float(getattr(config, "bytetrack_track_thresh", 0.25)),
                    match_thresh=float(getattr(config, "bytetrack_match_thresh", 0.80)),
                    track_buffer=int(getattr(config, "tracking_max_age", 30)),
                )
                self.logger.info("Landslide detection: initialized ByteTrackWrapper (fps=%s)", fps)
            except ImportError as exc:
                self.logger.warning(
                    "Landslide detection: ByteTrack unavailable (%s); falling back to SORT",
                    exc,
                )
                self.tracker = SORTTracker(
                    iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
                    max_age=int(getattr(config, "tracking_max_age", 30)),
                    min_hits=int(getattr(config, "tracking_min_hits", 2)),
                )
            return

        self.logger.warning("Landslide detection: unknown tracking_method=%r; tracker disabled", method)
        self.tracker = None

    # ------------------------------------------------------------------
    # Camera resolution helpers
    # ------------------------------------------------------------------

    def get_resolution(self, camera_id: str) -> Tuple[Optional[int], Optional[int]]:
        """Fetch frame width/height for *camera_id* via CameraManagement API.

        Mirrors the same method in :class:`FootfallProcessor` so that landslide
        detection can normalise segmentation-mask areas to a percentage of the
        real frame.

        Returns
        -------
        tuple of (width, height) in pixels, or (None, None) on failure.
        """
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

    def _resolve_resolution(self, stream_info: Optional[Dict[str, Any]]) -> None:
        """Populate ``_frame_width`` / ``_frame_height`` from stream_info or API.

        Called once per session on the first :meth:`process` invocation.
        Priority:

        1. ``stream_info.input_settings.{width,height}``
        2. ``stream_info.{width,height}``
        3. :meth:`get_resolution` via CameraManagement API (requires py_matrice)
        4. Falls back to 1920 × 1080 if everything else fails.
        """
        if self._resolution_resolved:
            return

        w: Optional[int] = None
        h: Optional[int] = None

        if stream_info:
            inp = stream_info.get("input_settings") or {}
            try:
                w = int(inp.get("width") or stream_info.get("width") or 0) or None
                h = int(inp.get("height") or stream_info.get("height") or 0) or None
            except (TypeError, ValueError):
                w = h = None

        if not (w and h):
            # Try API look-up using camera_id extracted from stream_info
            camera_id: Optional[str] = None
            if stream_info:
                cam_info = stream_info.get("camera_info") or {}
                camera_id = (
                    cam_info.get("camera_id")
                    or stream_info.get("camera_id")
                    or (stream_info.get("input_settings") or {}).get("camera_id")
                )
            if camera_id:
                w, h = self.get_resolution(camera_id)

        self._frame_width = w or 1920
        self._frame_height = h or 1080
        self._total_frame_area = float(self._frame_width * self._frame_height)
        self._resolution_resolved = True
        self.logger.info(
            "Landslide detection: resolved frame resolution = %d x %d  (area=%.0f px, computed once)",
            self._frame_width,
            self._frame_height,
            self._total_frame_area,
        )

    # ------------------------------------------------------------------
    # Mask area helpers
    # ------------------------------------------------------------------

    def _calculate_mask_area_percentage(
        self,
        det: Dict[str, Any],
        total_frame_area: float,
    ) -> float:
        """Return the fraction of the frame covered by *det*'s segmentation mask.

        Uses ``segmentation_area`` (pixel count from backend) when present,
        otherwise estimates from bounding-box dimensions.

        ``segmentation_area`` is a pixel count taken in the mask's *own*
        array space (``det["shape"]``), which is not guaranteed to match
        the frame's resolution (e.g. YOLO masks without ``retina_masks``
        are emitted at the model's internal processed-mask resolution).
        We therefore normalise by the mask's own shape when available,
        falling back to ``total_frame_area`` only if shape metadata is
        missing.

        Parameters
        ----------
        det:
            Single normalised detection dict.
        total_frame_area:
            Total frame area in pixels (``width × height``).

        Returns
        -------
        Percentage [0, 100].
        """
        if total_frame_area <= 0:
            return 0.0

        seg_area = det.get("segmentation_area")
        if seg_area is not None:
            shape = det.get("shape")
            if isinstance(shape, (list, tuple)) and len(shape) == 2 and shape[0] and shape[1]:
                mask_space_area = float(shape[0]) * float(shape[1])
            else:
                mask_space_area = total_frame_area
            try:
                return min(100.0, (float(seg_area) / mask_space_area) * 100.0)
            except (TypeError, ValueError, ZeroDivisionError):
                pass

        # Polygon / contour area from segmentation field
        seg = det.get("segmentation")
        if isinstance(seg, (list, tuple)) and len(seg) > 0:
            try:
                polygon_array = np.array(seg, dtype=np.float32)
                if polygon_array.ndim == 2 and polygon_array.shape[1] == 2:
                    import cv2  # noqa: PLC0415

                    area = float(cv2.contourArea(polygon_array))
                    return min(100.0, (area / total_frame_area) * 100.0)
            except Exception:
                pass

        # Bounding-box area as last resort
        bbox = det.get("bounding_box", {})
        if isinstance(bbox, dict):
            bw = (bbox.get("xmax", 0) or 0) - (bbox.get("xmin", 0) or 0)
            bh = (bbox.get("ymax", 0) or 0) - (bbox.get("ymin", 0) or 0)
            bbox_area = max(0.0, float(bw)) * max(0.0, float(bh))
            return min(100.0, (bbox_area / total_frame_area) * 100.0)

        return 0.0

    @staticmethod
    def _area_pct_to_severity(area_pct: float, landslide_area_percent: float) -> str:
        """Map *area_pct* to an incident severity string.

        Severity bands are relative to the configured *landslide_area_percent*
        threshold:

        ============================================== ===========
        Condition                                      Severity
        ============================================== ===========
        threshold ≤ pct < threshold + 10               "low"
        threshold + 10 ≤ pct < threshold + 20          "medium"
        threshold + 20 ≤ pct < threshold + 40          "high"
        threshold + 40 ≤ pct < threshold + 50          "warning"
        pct ≥ threshold + 50                            "critical"
        ============================================== ===========
        """
        excess = area_pct - landslide_area_percent
        if excess < 10:
            return "low"
        elif excess < 20:
            return "medium"
        elif excess < 40:
            return "high"
        elif excess < 50:
            return "warning"
        else:
            return "critical"

    def _compute_frame_landslide_area_stats(
        self,
        counting_summary: Dict[str, Any],
        config: LandslideDetectionConfig,
    ) -> Tuple[List[Dict[str, Any]], float, float]:
        """Return target detections and frame-level mask area percentages.

        *total_area_pct* is the sum of per-detection mask coverage values for
        the current frame (used for severity).  *max_area_pct* is the largest
        single-detection coverage (retained for analytics consumers).
        """
        target_detections = [
            d for d in counting_summary.get("detections", []) if d.get("category") in config.target_categories
        ]
        area_pcts = [float(d.get("mask_area_percentage", 0.0)) for d in target_detections]
        total_area_pct = sum(area_pcts)
        max_area_pct = max(area_pcts) if area_pcts else 0.0
        return target_detections, total_area_pct, max_area_pct

    def _simple_tracker_update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Lightweight frame-local track IDs (people_counting / area_utilization fallback)."""
        for i, det in enumerate(detections):
            if not isinstance(det, dict):
                continue
            if det.get("track_id") is None:
                det["track_id"] = f"simple_{self._total_frame_counter}_{i}"
        return detections

    def __init__(self) -> None:
        super().__init__("landslide_detection")
        self.category: str = "environmental"
        self.CASE_TYPE: Optional[str] = "landslide_detection"
        self.CASE_VERSION: Optional[str] = "1.0"

        self.target_categories: List[str] = ["landslide"]

        # Tracker state
        self.smoothing_tracker: Optional[BBoxSmoothingTracker] = None
        self.tracker = None
        self._total_frame_counter: int = 0
        self._global_frame_offset: int = 0
        self._tracking_start_time: Optional[float] = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.6
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer: Optional[str] = None

        # Per-category cumulative and per-frame track-ID sets.
        self._per_category_total_track_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._new_track_ids_this_frame: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._tracked_in_zones: set = set()
        self._total_count: int = 0
        self._last_update_time: float = time.time()
        self._total_count_list: List[Any] = []

        # Zone-based tracking storage
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}

        # Frame-resolution cache (populated lazily on first process() call).
        # _total_frame_area is derived from width × height and also cached so
        # the multiplication is not repeated on every frame.
        self._frame_width: Optional[int] = None
        self._frame_height: Optional[int] = None
        self._total_frame_area: float = 0.0
        self._resolution_resolved: bool = False

        # Area-based incident episode state.
        self._landslide_incident_active: bool = False
        self._landslide_episode_id: int = 0
        self._landslide_episode_start_ts: str = ""
        self._landslide_episode_max_area_pct: float = 0.0
        self._landslide_episode_severity: str = ""
        self._landslide_last_active_wall: float = 0.0
        self._landslide_incident_cooldown: float = 60.0  # seconds
        self._landslide_last_incident: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def process(
        self,
        data: Any = None,
        config: ConfigProtocol = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """Run full landslide detection post-processing pipeline.

        Args:
            data: Raw model detections (list or YOLO-style dict).
            config: Must be a :class:`LandslideDetectionConfig` instance.
            context: Optional processing context carrying metadata.
            stream_info: Stream/video metadata used for timestamps.

        Returns:
            :class:`ProcessingResult` containing ``agg_summary`` payload.
        """
        processing_start = time.time()

        is_valid_config = isinstance(config, LandslideDetectionConfig) or (
            hasattr(config, "usecase")
            and config.usecase == "landslide_detection"
            and hasattr(config, "category")
            and config.category == "environmental"
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed in landslide_detection. "
                f"Got type={type(config).__name__}, module={type(config).__module__}, "
                f"usecase={getattr(config, 'usecase', 'N/A')}, "
                f"category={getattr(config, 'category', 'N/A')}"
            )
            return self.create_error_result(
                f"Invalid config type: expected LandslideDetectionConfig or config with "
                f"usecase='landslide_detection', got {type(config).__name__} with "
                f"usecase={getattr(config, 'usecase', 'N/A')}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        has_zones = bool(config.zone_config and config.zone_config.get("zones"))

        # Normalise YOLO-style payloads to internal schema.
        data = self._normalize_yolo_results(data, getattr(config, "index_to_category", None))
        self.logger.debug(f"[landslide_detection] normalized_input={data}")

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold
        config.confidence_threshold = 0.25

        # Confidence filtering
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data
            self.logger.debug("Skipped confidence filtering – no threshold provided")

        # Index-to-category label mapping
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        # Retain only target category detections
        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in config.target_categories]
            self.logger.debug("Applied target category filtering")

        processed_data = [d for d in processed_data if d.get("category") in self.target_categories]

        # Normalise alternative track-ID field names to ``track_id``
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

        # BBox smoothing
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold,
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True,
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Tracking: SORT / ByteTrack assign stable IDs without replacing model boxes.
        if getattr(config, "enable_tracking", True):
            self._init_tracker(config, stream_info)
            if self.tracker is not None:
                try:
                    if isinstance(self.tracker, ByteTrackWrapper):
                        processed_data = self.tracker.update(processed_data, stream_info=stream_info)
                    else:
                        processed_data = self.tracker.update(processed_data)
                except Exception as exc:
                    self.logger.warning(f"Landslide detection tracker update failed: {exc}")
        elif getattr(config, "enable_simple_tracker", False):
            processed_data = self._simple_tracker_update(processed_data)
        else:
            for idx, det in enumerate(processed_data):
                if det.get("track_id") is None:
                    det["track_id"] = f"raw_{self._total_frame_counter}_{idx}"

        # ------------------------------------------------------------------
        # Resolve frame resolution (once per session) and annotate each
        # detection with its mask_area_percentage.  All landslide detections
        # are retained; severity is computed from total frame mask coverage.
        # _resolve_resolution() is guarded by _resolution_resolved and runs
        # only on the first process() call; _total_frame_area is cached there.
        # ------------------------------------------------------------------
        self._resolve_resolution(stream_info)
        total_frame_area = self._total_frame_area
        landslide_threshold = float(getattr(config, "landslide_area_percent", 50.0))

        for det in processed_data:
            area_pct = self._calculate_mask_area_percentage(det, total_frame_area)
            det["mask_area_percentage"] = round(area_pct, 4)
            det["mask_area_pixels"] = int(area_pct / 100.0 * total_frame_area)

        self._update_tracking_state(processed_data, _has_zones=has_zones)
        self._total_frame_counter += 1

        # Resolve frame number from stream_info when available
        frame_number: Optional[int] = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Counting summaries
        counting_summary = self._count_categories(processed_data, config)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts
        counting_summary["categories"] = {}
        for detection in processed_data:
            category = detection.get("category", "unknown")
            counting_summary["categories"][category] = counting_summary["categories"].get(category, 0) + 1

        # Attach area metadata for downstream methods.
        counting_summary["landslide_area_threshold"] = landslide_threshold
        counting_summary["total_frame_area"] = total_frame_area

        # Zone analysis
        zone_analysis: Dict[str, Any] = {}
        if has_zones:
            frame_data = processed_data
            zone_analysis = count_objects_in_zones(frame_data, config.zone_config["zones"], stream_info)
            if zone_analysis:
                enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, processed_data, config)
                for zone_name, enhanced_data in enhanced_zone_analysis.items():
                    zone_analysis[zone_name] = enhanced_data

                per_category_count = {
                    cat: len(self._current_frame_track_ids.get(cat, set())) for cat in self.target_categories
                }
                counting_summary["per_category_count"] = {k: v for k, v in per_category_count.items() if v > 0}
                counting_summary["total_count"] = sum(per_category_count.values())

        # Downstream outputs
        alerts = self._check_alerts(counting_summary, zone_analysis, frame_number, config)
        self._extract_predictions(processed_data)
        incidents_list = self._generate_incidents(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info
        )
        business_analytics_list = self._generate_business_analytics(
            counting_summary, zone_analysis, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(
            counting_summary,
            zone_analysis,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}

        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "zone_analysis": zone_analysis,
                "human_text": summary,
            }
        }

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        proc_time = time.time() - processing_start
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        print(
            f"latency in ms: {processing_latency_ms} | "
            f"Throughput fps: {processing_fps} | "
            f"Frame_Number: {self._total_frame_counter}"
        )
        return result

    # ------------------------------------------------------------------
    # Zone tracking
    # ------------------------------------------------------------------

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: LandslideDetectionConfig,
    ) -> Dict[str, Dict[str, Any]]:
        """Update per-zone track-ID sets and return enhanced zone analysis.

        Args:
            zone_analysis: Raw zone counts produced by ``count_objects_in_zones``.
            detections: Detections list for the current frame (track IDs present).
            config: Use-case configuration carrying zone polygon definitions.

        Returns:
            Enhanced zone analysis dict keyed by zone name.
        """
        if not zone_analysis or not config.zone_config or not config.zone_config.get("zones"):
            return {}

        enhanced_zone_analysis: Dict[str, Dict[str, Any]] = {}
        zones = config.zone_config["zones"]

        track_to_cat: Dict[Any, str] = {
            det.get("track_id"): det.get("category") for det in detections if det.get("track_id") is not None
        }

        current_frame_zone_tracks: Dict[str, set] = {}

        for zone_name in zones:
            current_frame_zone_tracks[zone_name] = set()
            self._zone_current_track_ids.setdefault(zone_name, set())
            self._zone_total_track_ids.setdefault(zone_name, set())

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            center_point = get_bbox_bottom25_center(bbox)
            in_any_zone = False

            for zone_name, zone_polygon in zones.items():
                polygon_points = [(pt[0], pt[1]) for pt in zone_polygon]
                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)
                    in_any_zone = True
                    if track_id not in self._total_count_list:
                        self._total_count_list.append(track_id)

            if in_any_zone:
                cat = track_to_cat.get(track_id)
                if cat:
                    self._current_frame_track_ids.setdefault(cat, set()).add(track_id)
                    if track_id not in self._tracked_in_zones:
                        self._tracked_in_zones.add(track_id)

        for zone_name, zone_counts in zone_analysis.items():
            current_tracks = current_frame_zone_tracks.get(zone_name, set())
            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])

            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts,
            }

        return enhanced_zone_analysis

    # ------------------------------------------------------------------
    # YOLO normalisation
    # ------------------------------------------------------------------

    def _normalize_yolo_results(
        self,
        data: Any,
        index_to_category: Optional[Dict[int, str]] = None,
    ) -> Any:
        """Normalise YOLO-style outputs to the internal detection schema.

        Handles the backend dual-port format (``detection0`` + ``mask0`` keys),
        plain lists-of-detections, and frame_id→list mappings.  Each detection
        dict is normalised to contain at least: ``category``, ``confidence``,
        ``bounding_box``, and—when available—``mask_rle``, ``shape``, and
        ``segmentation_area``.

        Backend dual-port format (merged before or passed as-is)::

            {
                "detection0": {"data": {"detections": [...]}},
                "mask0":      {"data": {"masks":      [...]}}
            }

        Each mask record is joined to its parent detection via
        ``detection_index`` / ``mask_id``.

        Args:
            data: Raw model output.
            index_to_category: Optional int-to-label mapping.

        Returns:
            Normalised detection list.
        """

        # ------------------------------------------------------------------
        # 1. Handle backend dual-port dict: detection0 + mask0
        # ------------------------------------------------------------------
        if isinstance(data, dict) and ("detection0" in data or "mask0" in data):
            detection0_payload = data.get("detection0", {})
            mask0_payload = data.get("mask0", {})

            raw_detections: List[Dict[str, Any]] = []
            if isinstance(detection0_payload, dict):
                inner = detection0_payload.get("data", detection0_payload)
                raw_detections = inner.get("detections", []) if isinstance(inner, dict) else []

            raw_masks: List[Dict[str, Any]] = []
            if isinstance(mask0_payload, dict):
                inner = mask0_payload.get("data", mask0_payload)
                raw_masks = inner.get("masks", []) if isinstance(inner, dict) else []

            # Build a lookup: detection_index → mask record
            mask_by_index: Dict[int, Dict[str, Any]] = {}
            for m in raw_masks:
                if not isinstance(m, dict):
                    continue
                idx = m.get("detection_index", m.get("mask_id"))
                if idx is not None:
                    mask_by_index[int(idx)] = m

            merged: List[Dict[str, Any]] = []
            for det in raw_detections:
                if not isinstance(det, dict):
                    continue
                d_idx = det.get("detection_index")
                mask_info = mask_by_index.get(int(d_idx), {}) if d_idx is not None else {}

                bbox = det.get("bounding_box", {})
                # bbox from mask0 uses list format [x1,y1,x2,y2]; prefer detection0's dict
                if not bbox and mask_info:
                    raw_bbox = mask_info.get("bbox", [])
                    if isinstance(raw_bbox, (list, tuple)) and len(raw_bbox) >= 4:
                        bbox = {"xmin": raw_bbox[0], "ymin": raw_bbox[1], "xmax": raw_bbox[2], "ymax": raw_bbox[3]}

                merged_det: Dict[str, Any] = {
                    "category": det.get("category", "unknown"),
                    "confidence": det.get("confidence", 0.0),
                    "bounding_box": bbox,
                    "class_id": det.get("class_id"),
                    "detection_index": d_idx,
                }
                if mask_info:
                    merged_det["mask_rle"] = mask_info.get("mask_rle")
                    merged_det["shape"] = mask_info.get("shape")
                    merged_det["segmentation_area"] = mask_info.get("area_pixels")
                merged.append(merged_det)

            data = merged

        # ------------------------------------------------------------------
        # 2. Helpers for flat list / legacy dict normalisation
        # ------------------------------------------------------------------

        def to_bbox_dict(d: Dict[str, Any]) -> Dict[str, Any]:
            if "bounding_box" in d and isinstance(d["bounding_box"], dict):
                return d["bounding_box"]
            if "bbox" in d:
                bbox = d["bbox"]
                if isinstance(bbox, dict):
                    return bbox
                if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
                    return {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2}
            if "xyxy" in d and isinstance(d["xyxy"], (list, tuple)) and len(d["xyxy"]) >= 4:
                x1, y1, x2, y2 = d["xyxy"][0], d["xyxy"][1], d["xyxy"][2], d["xyxy"][3]
                return {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2}
            if "xywh" in d and isinstance(d["xywh"], (list, tuple)) and len(d["xywh"]) >= 4:
                cx, cy, w, h = d["xywh"][0], d["xywh"][1], d["xywh"][2], d["xywh"][3]
                x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
                return {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2}
            return {}

        def resolve_category(d: Dict[str, Any]) -> Tuple[str, Optional[int]]:
            raw_cls = d.get("category", d.get("category_id", d.get("class", d.get("cls"))))
            label_name = d.get("name")
            if isinstance(raw_cls, int):
                if index_to_category and raw_cls in index_to_category:
                    return index_to_category[raw_cls], raw_cls
                return str(raw_cls), raw_cls
            if isinstance(raw_cls, str):
                return raw_cls, None
            if label_name:
                return str(label_name), None
            return "unknown", None

        def normalize_det(det: Dict[str, Any]) -> Dict[str, Any]:
            category_name, category_id = resolve_category(det)
            confidence = det.get("confidence", det.get("conf", det.get("score", 0.0)))
            bbox = to_bbox_dict(det)
            normalised: Dict[str, Any] = {
                "category": category_name,
                "confidence": confidence,
                "bounding_box": bbox,
            }
            if category_id is not None:
                normalised["category_id"] = category_id
            # Pass through all mask/segmentation and identity fields unchanged.
            for key in (
                "track_id",
                "frame_id",
                "masks",
                "segmentation",
                "mask_rle",
                "shape",
                "segmentation_area",
                "class_id",
                "detection_index",
            ):
                if key in det and det[key] is not None:
                    normalised[key] = det[key]
            return normalised

        if isinstance(data, list):
            return [normalize_det(d) if isinstance(d, dict) else d for d in data]
        if isinstance(data, dict):
            normalised_dict: Dict[str, Any] = {}
            for k, v in data.items():
                if isinstance(v, list):
                    normalised_dict[k] = [normalize_det(d) if isinstance(d, dict) else d for d in v]
                elif isinstance(v, dict):
                    normalised_dict[k] = normalize_det(v)
                else:
                    normalised_dict[k] = v
            return normalised_dict
        return data

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    def _check_alerts(
        self,
        summary: Dict[str, Any],
        _zone_analysis: Dict[str, Any],
        frame_number: Any,
        config: LandslideDetectionConfig,
    ) -> List[Dict[str, Any]]:
        """Evaluate alert thresholds for the current frame.

        An alert is generated when the number of detected landslides in the
        current frame meets or exceeds the configured threshold (default: 1).

        Args:
            summary: Counting summary produced by ``_count_categories``.
            zone_analysis: Zone-level counts for the current frame.
            frame_number: Current frame index or ``None``.
            config: Use-case configuration with ``alert_config``.

        Returns:
            List of alert dicts (may be empty).
        """

        _ = (_zone_analysis,)

        def get_trend(data: List[int], lookback: int = 900, threshold: float = 0.6) -> bool:
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            return (increasing / (len(window) - 1)) >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts: List[Dict[str, Any]] = []

        if not config.alert_config:
            return alerts

        total_detections = summary.get("total_count", 0)
        per_category_count = summary.get("per_category_count", {})

        if not (hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds):
            return alerts

        for category, threshold in config.alert_config.count_thresholds.items():
            triggered = False
            if category == "all" and total_detections >= threshold:
                triggered = True
            elif category in per_category_count and per_category_count[category] >= threshold:
                triggered = True

            if triggered:
                alerts.append(
                    {
                        "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {
                            t: v
                            for t, v in zip(
                                getattr(config.alert_config, "alert_type", ["Default"]),
                                getattr(config.alert_config, "alert_value", ["JSON"]),
                            )
                        },
                    }
                )
        return alerts

    # ------------------------------------------------------------------
    # Incidents
    # ------------------------------------------------------------------

    def _generate_incidents(
        self,
        counting_summary: Dict[str, Any],
        _zone_analysis: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: LandslideDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Generate incident records for the current frame.

        Severity is determined by the **total** mask coverage in the frame
        relative to ``landslide_area_percent``.  Every landslide detection
        triggers an incident; none are filtered by area.

        ============================================ ===========
        excess above reference threshold             Severity
        ============================================ ===========
        0 – 10 %                                     low
        10 – 20 %                                    medium
        20 – 40 %                                    high
        40 – 50 %                                    warning
        ≥ 50 %                                       critical
        ============================================ ===========

        Episode lifecycle: an incident is created when any landslide is
        present, updated while active, and closed after
        ``_landslide_incident_cooldown`` seconds without detections. A new
        episode is also opened immediately whenever tracking registers a
        brand-new landslide track this frame
        (``_new_track_ids_this_frame["landslide"]``), even if the previous
        incident was still technically active -- so the incident count stays
        in lockstep with the same track-reset signal that drives the
        landslide count, instead of only resetting after the separate (and
        much longer) cooldown.

        Args:
            counting_summary: Frame-level counting summary.
            _zone_analysis: Zone-level counts (unused for area-based severity).
            alerts: Alerts generated for this frame.
            config: Use-case configuration.
            frame_number: Current frame index.
            stream_info: Stream metadata.

        Returns:
            List containing a single incident dict (or empty dict when no
            landslide is detected).
        """
        _ = (_zone_analysis,)

        landslide_threshold = float(
            counting_summary.get("landslide_area_threshold", getattr(config, "landslide_area_percent", 50.0))
        )
        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)
        wall_now = time.time()

        # Trim history window to avoid unbounded growth.
        self._ascending_alert_list = self._ascending_alert_list[-900:]

        target_detections, total_area_pct, _max_area_pct = self._compute_frame_landslide_area_stats(
            counting_summary, config
        )

        landslide_active_this_frame = len(target_detections) > 0

        if landslide_active_this_frame:
            self._ascending_alert_list.append(1)

            # A brand-new landslide track appearing this frame means tracking
            # already decided the gap/geometry break since the last
            # qualifying detection was enough (see _merge_or_register_track)
            # to be a genuinely new occurrence -- open a new episode right
            # away for that too, in addition to the original "incident was
            # fully cold" case, so incident numbering tracks the same signal
            # as the count.
            new_track_ids_this_frame = self._new_track_ids_this_frame.get("landslide", set())
            is_new_occurrence = bool(new_track_ids_this_frame)

            # Open or continue episode.
            if not self._landslide_incident_active or is_new_occurrence:
                self._landslide_incident_active = True
                self._landslide_episode_id += 1
                self._landslide_episode_start_ts = start_timestamp or current_timestamp
                self._landslide_episode_max_area_pct = total_area_pct
                self._landslide_episode_severity = self._area_pct_to_severity(total_area_pct, landslide_threshold)
                self.logger.info(
                    "Landslide episode #%d opened%s: total_area_pct=%.2f%%, severity=%s",
                    self._landslide_episode_id,
                    " (new landslide track)" if is_new_occurrence else "",
                    total_area_pct,
                    self._landslide_episode_severity,
                )
            else:
                # Update rolling max total coverage and escalate severity if needed.
                if total_area_pct > self._landslide_episode_max_area_pct:
                    self._landslide_episode_max_area_pct = total_area_pct
                    self._landslide_episode_severity = self._area_pct_to_severity(total_area_pct, landslide_threshold)

            self._landslide_last_active_wall = wall_now

            level = self._area_pct_to_severity(total_area_pct, landslide_threshold)

            alert_settings: List[Dict[str, Any]] = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": (
                            config.alert_config.count_thresholds
                            if hasattr(config.alert_config, "count_thresholds")
                            else {}
                        ),
                        "ascending": True,
                        "settings": {
                            t: v
                            for t, v in zip(
                                getattr(config.alert_config, "alert_type", ["Default"]),
                                getattr(config.alert_config, "alert_value", ["JSON"]),
                            )
                        },
                    }
                )

            human_text = (
                f"LANDSLIDE INCIDENT DETECTED @ {current_timestamp}:\n"
                f"\tSeverity: {level.upper()}\n"
                f"\tTotal Landslide Coverage: {total_area_pct:.1f}% of frame\n"
                f"\tSeverity Reference: {landslide_threshold:.1f}%\n"
                f"\tDetections: {len(target_detections)}"
            )

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_ep{self._landslide_episode_id}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=self._landslide_episode_start_ts,
                end_time="Incident still active",
                level_settings={"low": 1, "medium": 3, "high": 5, "warning": 7, "critical": 10},
            )
            self._landslide_last_incident = event
            return [event]

        else:
            self._ascending_alert_list.append(0)

            # Close episode after cooldown.
            if self._landslide_incident_active:
                elapsed_since_active = wall_now - self._landslide_last_active_wall
                if elapsed_since_active >= self._landslide_incident_cooldown:
                    self.logger.info(
                        "Landslide episode #%d closed after %.1fs of inactivity",
                        self._landslide_episode_id,
                        elapsed_since_active,
                    )
                    self._landslide_incident_active = False

            return [{}]

    # ------------------------------------------------------------------
    # Segmentation helpers
    # ------------------------------------------------------------------

    def _build_segmentation(self, detection: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normalise raw detection segmentation fields into the canonical schema.

        The canonical schema expected by consumers is::

            {
                "encoding": "simple_rle",
                "counts":   "<base64 / RLE string>",
                "size":     [height, width]
            }

        Multiple upstream field names are handled:
        - ``mask_rle`` + ``shape`` (backend dual-port format, preferred)
        - ``segmentation`` (may already be canonical, or a raw RLE string)
        - ``masks`` (legacy list or raw RLE string)
        - ``mask``  (legacy raw RLE string)

        Returns ``None`` when no segmentation data is present so that callers
        can omit the field entirely.

        Args:
            detection: A single normalised detection dict from ``_count_categories``.

        Returns:
            Canonical segmentation dict, or ``None``.
        """
        shape = detection.get("shape", [])
        size: List[Any] = list(shape) if shape else []

        if detection.get("mask_rle"):
            mask_rle = detection["mask_rle"]
            # Backend encodes mask_rle as the full canonical dict already.
            if isinstance(mask_rle, dict) and "encoding" in mask_rle and "counts" in mask_rle:
                return mask_rle
            # Fallback: raw RLE string — wrap into canonical form.
            return {
                "encoding": "simple_rle",
                "counts": mask_rle,
                "size": size,
            }

        if detection.get("segmentation"):
            seg = detection["segmentation"]
            if isinstance(seg, dict):
                if "encoding" in seg and "counts" in seg:
                    return seg
                return seg
            if isinstance(seg, str):
                return {
                    "encoding": "simple_rle",
                    "counts": seg,
                    "size": size,
                }
            return seg

        if detection.get("masks"):
            masks = detection["masks"]
            if isinstance(masks, str):
                return {
                    "encoding": "simple_rle",
                    "counts": masks,
                    "size": size,
                }
            return masks

        if detection.get("mask"):
            mask = detection["mask"]
            if isinstance(mask, str):
                return {
                    "encoding": "simple_rle",
                    "counts": mask,
                    "size": size,
                }
            return mask

        return None

    # ------------------------------------------------------------------
    # Tracking statistics
    # ------------------------------------------------------------------

    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        zone_analysis: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: LandslideDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Build tracking statistics for the current frame.

        Args:
            counting_summary: Frame-level counting summary.
            zone_analysis: Zone-level counts.
            alerts: Active alerts for this frame.
            config: Use-case configuration.
            frame_number: Current frame index.
            stream_info: Stream metadata.

        Returns:
            Single-element list with a tracking stats dict.
        """
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats: List[Dict[str, Any]] = []

        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        new_counts_dict = self.get_new_counts_this_frame()

        # Build per-category detection count directly from the detections list –
        # this is the most reliable source of truth.
        raw_detections = counting_summary.get("detections", [])
        detection_count_by_category: Dict[str, int] = {}
        for det in raw_detections:
            cat = det.get("category", "landslide")
            detection_count_by_category[cat] = detection_count_by_category.get(cat, 0) + 1

        total_counts = [
            {"category": self._display_category(cat), "count": count}
            for cat, count in total_counts_dict.items()
            if count > 0
        ]
        current_counts = [
            {"category": self._display_category(cat), "count": count}
            for cat, count in detection_count_by_category.items()
        ]
        if not current_counts and total_detections > 0:
            current_counts = [
                {"category": self._display_category(cat), "count": count} for cat, count in per_category_count.items()
            ]
        current_new_counts = [
            {"category": self._display_category(cat), "count": count} for cat, count in new_counts_dict.items()
        ]

        curr_total = sum(c.get("count", 0) for c in current_counts)
        new_total = sum(c.get("count", 0) for c in current_new_counts)
        total_total = sum(c.get("count", 0) for c in total_counts)
        print(f"[STATS] F{frame_number} | current={curr_total} new={new_total} total={total_total}")

        landslide_threshold = float(
            counting_summary.get("landslide_area_threshold", getattr(config, "landslide_area_percent", 50.0))
        )

        detections_output: List[Dict[str, Any]] = []
        all_area_pcts: List[float] = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category_raw = detection.get("category", "landslide")
            category = self._display_category(category_raw)
            segmentation = self._build_segmentation(detection)
            det_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            # Attach area metadata so consumers can inspect per-detection coverage.
            area_pct = float(detection.get("mask_area_percentage", 0.0))
            det_obj["mask_area_percentage"] = round(area_pct, 4)
            det_obj["mask_area_pixels"] = int(detection.get("mask_area_pixels", 0))
            detections_output.append(det_obj)
            if category_raw in config.target_categories:
                all_area_pcts.append(area_pct)

        # Build landslide_analytics summary block (severity from total frame coverage).
        max_area_pct = max(all_area_pcts) if all_area_pcts else 0.0
        total_area_pct = sum(all_area_pcts)
        severity = self._area_pct_to_severity(total_area_pct, landslide_threshold) if all_area_pcts else "none"
        landslide_analytics: Dict[str, Any] = {
            "landslide_detection_count": len(all_area_pcts),
            "max_landslide_area_pct": round(max_area_pct, 4),
            "total_landslide_area_pct": round(total_area_pct, 4),
            "landslide_area_threshold": landslide_threshold,
            "severity_level": severity,
            "episode_active": self._landslide_incident_active,
            "episode_id": self._landslide_episode_id,
        }

        alert_settings: List[Dict[str, Any]] = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds if hasattr(config.alert_config, "count_thresholds") else {}
                    ),
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    },
                }
            )

        human_text_lines: List[str] = [f"CURRENT FRAME @ {current_timestamp}:"]

        if zone_analysis:
            human_text_lines.append("\t- Landslides Detected by Zone:")
            for zone_name, zone_data in zone_analysis.items():
                if isinstance(zone_data, dict):
                    if "current_count" in zone_data:
                        zone_current = zone_data.get("current_count", 0)
                    else:
                        counts_dict = (
                            zone_data.get("original_counts")
                            if isinstance(zone_data.get("original_counts"), dict)
                            else zone_data
                        )
                        zone_current = counts_dict.get(
                            "total",
                            sum(v for v in counts_dict.values() if isinstance(v, (int, float))),
                        )
                else:
                    zone_current = 0
                human_text_lines.append(f"\t\t- {zone_name}: {int(zone_current)}")
        else:
            for cat, count in detection_count_by_category.items():
                display_cat = self._display_category(cat)
                new_count = new_counts_dict.get(cat, 0)
                human_text_lines.append(f"\t- Landslides in Frame ({display_cat}): {count}")
                human_text_lines.append(f"\t- New Landslides (just entered) ({display_cat}): {new_count}")

        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 0, "time_unit": "hour"}}]
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections_output,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stat["target_categories"] = self.target_categories
        tracking_stat["current_new_counts"] = current_new_counts
        tracking_stat["total_current_counts"] = current_counts
        tracking_stat["landslide_analytics"] = landslide_analytics
        tracking_stats.append(tracking_stat)
        return tracking_stats

    # ------------------------------------------------------------------
    # Business analytics
    # ------------------------------------------------------------------

    def _generate_business_analytics(
        self,
        _counting_summary: Dict[str, Any],
        _zone_analysis: Dict[str, Any],
        _alerts: Any,
        _config: LandslideDetectionConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty: bool = False,
    ) -> List[Dict[str, Any]]:
        """Return business analytics payload.

        Currently returns an empty list because disaster-detection use cases
        do not require business KPIs.  Override this method to add custom
        analytics (e.g., affected area estimation, risk scoring).

        Args:
            counting_summary: Frame-level counting summary.
            zone_analysis: Zone-level counts.
            alerts: Active alerts.
            config: Use-case configuration.
            stream_info: Stream metadata.
            is_empty: If ``True``, always return empty list.

        Returns:
            Empty list.
        """
        _ = (_alerts, _config, _counting_summary, _stream_info, _zone_analysis)
        if is_empty:
            return []
        return []

    # ------------------------------------------------------------------
    # Human-readable summary
    # ------------------------------------------------------------------

    def _generate_summary(
        self,
        _summary: Dict[str, Any],
        _zone_analysis: Dict[str, Any],
        incidents: List[Dict[str, Any]],
        tracking_stats: List[Dict[str, Any]],
        business_analytics: List[Dict[str, Any]],
        _alerts: List[Dict[str, Any]],
    ) -> List[str]:
        """Assemble a human-readable summary string for the frame.

        Args:
            summary: Counting summary.
            zone_analysis: Zone-level counts.
            incidents: Generated incidents.
            tracking_stats: Generated tracking stats.
            business_analytics: Generated business analytics.
            alerts: Active alerts.

        Returns:
            Single-element list with the summary string.
        """
        _ = (_alerts, _summary, _zone_analysis)
        lines: List[str] = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if incidents:
            lines.append("Incidents: \n\t" + incidents[0].get("human_text", "No incidents detected"))
        if tracking_stats:
            lines.append(
                "Tracking Statistics: \t" + tracking_stats[0].get("human_text", "No tracking statistics detected")
            )
        if business_analytics:
            lines.append(
                "Business Analytics: \t" + business_analytics[0].get("human_text", "No business analytics detected")
            )
        if not incidents and not tracking_stats and not business_analytics:
            lines.append("Summary: No Summary Data")

        return ["\n".join(lines)]

    # ------------------------------------------------------------------
    # Tracking helpers
    # ------------------------------------------------------------------

    def _update_tracking_state(self, detections: List[Dict[str, Any]], _has_zones: bool = False) -> None:
        """Update cumulative and per-frame track-ID sets.

        The update follows a strict ordering to ensure ``new`` counts are
        computed *before* the cumulative total is updated:

        1. Build ``_current_frame_track_ids`` from detections.
        2. Compute ``_new_track_ids_this_frame`` = current − total.
        3. Update ``_per_category_total_track_ids`` with current IDs.

        Args:
            detections: Processed detection list for the current frame.
            has_zones: Whether zone analysis is active.
        """
        _ = (_has_zones,)
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}

        # Step 1: Build current-frame track-ID sets.
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._current_frame_track_ids.setdefault(cat, set()).add(canonical_id)

        # Step 2: Compute new track IDs (before updating total).
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._per_category_total_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

        first_cat = self.target_categories[0] if self.target_categories else "landslide"
        current_ids = sorted(list(self._current_frame_track_ids.get(first_cat, set())))
        new_ids = sorted(list(self._new_track_ids_this_frame.get(first_cat, set())))
        total_seen = len(self._per_category_total_track_ids.get(first_cat, set()))
        print(
            f"[TRACK] F{self._total_frame_counter} | det={len(detections)} "
            f"ids={current_ids[:10]}{'...' if len(current_ids) > 10 else ''} "
            f"new={new_ids} total_seen={total_seen}"
        )

        if any(len(ids) > 0 for ids in self._new_track_ids_this_frame.values()):
            print(
                f"[NEW_TRACK] F{self._total_frame_counter} | new_ids={new_ids} total_unique={total_seen + len(new_ids)}"
            )

        # Step 3: Update cumulative totals.
        for cat, ids in self._current_frame_track_ids.items():
            self._per_category_total_track_ids.setdefault(cat, set()).update(ids)

        total_seen_after = len(self._per_category_total_track_ids.get(first_cat, set()))
        if total_seen_after > 100 and len(detections) > 0:
            ratio = total_seen_after / max(len(detections), 1)
            if ratio > 20:
                print(
                    f"[WARN] F{self._total_frame_counter} | total_seen={total_seen_after} "
                    f"vs det={len(detections)} (ratio={ratio:.1f}x) – possible tracker "
                    f"instability or use-case recreation"
                )

        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self) -> Dict[str, int]:
        """Return cumulative unique detection counts per category."""
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Return count of track IDs that appeared for the first time this frame."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Return count of all track IDs currently visible in this frame."""
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

    def _get_track_ids_info(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarise track-ID statistics for diagnostics."""
        frame_track_ids = {det.get("track_id") for det in detections if det.get("track_id") is not None}
        total_track_ids: set = set()
        for s in getattr(self, "_per_category_total_track_ids", {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, "_total_frame_counter", 0),
        }

    # ------------------------------------------------------------------
    # Track merging / deduplication
    # ------------------------------------------------------------------

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Resolve a raw tracker ID to a canonical ID, merging when IoU is high.

        High-IoU detections within the time window are assumed to be the same
        physical event and are collapsed to a single canonical track ID.

        Args:
            raw_id: ID assigned by the underlying tracker.
            bbox: Bounding box of the current detection.

        Returns:
            Canonical track ID.
        """
        if raw_id is None or bbox is None:
            return raw_id
        now = time.time()

        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id

        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id

        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute Intersection-over-Union between two bounding boxes.

        Accepts bounding boxes as lists/tuples ``[x1, y1, x2, y2]`` or dicts
        with keys ``x1/y1/x2/y2`` or ``xmin/ymin/xmax/ymax``.

        Args:
            box1: First bounding box.
            box2: Second bounding box.

        Returns:
            IoU score in ``[0.0, 1.0]``.
        """

        def _bbox_to_list(bbox: Any) -> List[float]:
            if bbox is None:
                return []
            if isinstance(bbox, (list, tuple)):
                return list(bbox[:4]) if len(bbox) >= 4 else []
            if isinstance(bbox, dict):
                if "xmin" in bbox:
                    return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
                if "x1" in bbox:
                    return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0

        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2

        x1_min, x1_max = min(x1_min, x1_max), max(x1_min, x1_max)
        y1_min, y1_max = min(y1_min, y1_max), max(y1_min, y1_max)
        x2_min, x2_max = min(x2_min, x2_max), max(x2_min, x2_max)
        y2_min, y2_max = min(y2_min, y2_max), max(y2_min, y2_max)

        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        inter_w = max(0.0, inter_x_max - inter_x_min)
        inter_h = max(0.0, inter_y_max - inter_y_min)
        inter_area = inter_w * inter_h

        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = area1 + area2 - inter_area
        return (inter_area / union_area) if union_area > 0 else 0.0

    # ------------------------------------------------------------------
    # Counting helpers
    # ------------------------------------------------------------------

    def _count_categories(self, detections: List[Dict[str, Any]], _config: LandslideDetectionConfig) -> Dict[str, Any]:
        """Count detections per category and build summary payload.

        Args:
            detections: Filtered, normalised detection list.
            config: Use-case configuration (unused directly but kept for API
                    consistency with the base class pattern).

        Returns:
            Dict with ``total_count``, ``per_category_count``, and
            ``detections`` keys.
        """
        _ = (_config,)
        counts: Dict[str, int] = {}
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1

        def _det_record(det: Dict[str, Any]) -> Dict[str, Any]:
            record: Dict[str, Any] = {
                "bounding_box": det.get("bounding_box"),
                "category": det.get("category"),
                "confidence": det.get("confidence"),
                "track_id": det.get("track_id"),
                "frame_id": det.get("frame_id"),
            }
            # Preserve instance-segmentation fields produced by the backend mask0 port.
            for key in ("mask_rle", "shape", "segmentation_area", "segmentation", "class_id"):
                val = det.get(key)
                if val is not None:
                    record[key] = val
            # Preserve the computed area-coverage fields (set in process() before
            # this function runs). Without these, downstream consumers
            # (_generate_tracking_stats' landslide_analytics block and
            # _generate_incidents' severity calc) silently see 0.0 for every
            # detection, even when the true coverage was computed correctly.
            for key in ("mask_area_percentage", "mask_area_pixels"):
                val = det.get(key)
                if val is not None:
                    record[key] = val
            return record

        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [_det_record(det) for det in detections],
        }

    def _extract_predictions(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract a minimal prediction list from processed detections.

        Args:
            detections: Processed detection list.

        Returns:
            List of ``{category, confidence, bounding_box}`` dicts.
        """
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            for det in detections
        ]

    # ------------------------------------------------------------------
    # Timestamp utilities
    # ------------------------------------------------------------------

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to ``YYYY:MM:DD HH:MM:SS``.

        Accepts a numeric Unix timestamp or a string in the form
        ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        Args:
            timestamp: Source timestamp value.

        Returns:
            Formatted string ``YYYY:MM:DD HH:MM:SS``.
        """
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
                    return f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision: bool = False,
        frame_id: Optional[str] = None,
    ) -> str:
        """Return a formatted current-frame timestamp string.

        Args:
            stream_info: Stream metadata dict.
            precision: If ``True``, return microsecond-precision ISO timestamp.
            frame_id: Optional explicit frame ID override.

        Returns:
            Formatted timestamp string.
        """
        if not stream_info:
            return "00:00:00.00"

        input_settings = stream_info.get("input_settings", {})

        if precision:
            if input_settings.get("start_frame", "na") != "na":
                return self._format_timestamp(input_settings.get("stream_time", "NA"))
            return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if input_settings.get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / input_settings.get("original_fps", 30)
            else:
                start_time = input_settings.get("start_frame", 30) / input_settings.get("original_fps", 30)
            _ = self._format_timestamp_for_video(start_time)
            return self._format_timestamp(input_settings.get("stream_time", "NA"))

        stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
        if stream_time_str:
            try:
                ts_clean = stream_time_str.replace(" UTC", "")
                dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                return self._format_timestamp_for_stream(timestamp)
            except Exception:
                return self._format_timestamp_for_stream(time.time())
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision: bool = False,
    ) -> str:
        """Return a formatted start-of-session timestamp string.

        Args:
            stream_info: Stream metadata dict.
            precision: If ``True``, return microsecond-precision ISO timestamp.

        Returns:
            Formatted timestamp string.
        """
        if not stream_info:
            return "00:00:00"

        input_settings = stream_info.get("input_settings", {})

        if precision:
            if self.start_timer is None:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
            elif input_settings.get("start_frame", "na") == 1:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        ts_clean = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
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

        if input_settings.get("start_frame", "na") == 1:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        ts_clean = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        if self.start_timer is not None and self.start_timer != "NA":
            return self._format_timestamp(self.start_timer)

        if self._tracking_start_time is None:
            stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    ts_clean = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
                    self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                except Exception:
                    self._tracking_start_time = time.time()
            else:
                self._tracking_start_time = time.time()

        dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _get_tracking_start_time(self) -> str:
        """Return the session start time as a formatted string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Capture the current wall-clock time as the tracking session start."""
        self._tracking_start_time = time.time()
