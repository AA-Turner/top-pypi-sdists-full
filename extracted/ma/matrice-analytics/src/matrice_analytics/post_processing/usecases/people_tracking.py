"""
People tracking use case implementation.

This module provides people tracking with polygon/abline counting,
zone-based analysis, tracking, and alerting capabilities.
"""

from typing import Any, Dict, List, Optional, Set
from dataclasses import asdict
import time
import numpy as np
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol, ResultFormat
from ..core.config import PeopleTrackingConfig, ZoneConfig, AlertConfig, LineConfig
from ..utils import (
    filter_by_confidence,
    filter_by_categories,
    apply_category_mapping,
    count_objects_by_category,
    count_objects_in_zones,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    calculate_iou
)
from ..utils.geometry_utils import get_bbox_center, point_in_polygon, get_bbox_bottom25_center
from ..utils.counting_utils import (
    ABLineCounter,
    PolygonCounter,
    polygon_offset_inward,
    parse_line_config,
)


# ====================================================================== #
# ByteTrack wrapper – bridges ultralytics BYTETracker ↔ pipeline dicts   #
# ====================================================================== #

class _MockResults:
    """Lightweight results container compatible with ultralytics BYTETracker.

    Provides the `.conf`, `.cls`, `.xywh`, `.xyxy` attributes and boolean
    indexing that ``BYTETracker.update`` requires.
    """

    def __init__(self, xyxy: np.ndarray, conf: np.ndarray, cls: np.ndarray):
        self._xyxy = np.asarray(xyxy, dtype=np.float32).reshape(-1, 4)
        self.conf = np.asarray(conf, dtype=np.float32).ravel()
        self.cls = np.asarray(cls, dtype=np.float32).ravel()

    # --- required attributes -------------------------------------------
    @property
    def xyxy(self) -> np.ndarray:
        return self._xyxy

    @property
    def xywh(self) -> np.ndarray:
        """Convert xyxy → (center-x, center-y, width, height)."""
        x1, y1, x2, y2 = (
            self._xyxy[:, 0], self._xyxy[:, 1],
            self._xyxy[:, 2], self._xyxy[:, 3],
        )
        return np.stack([(x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1], axis=1)

    # --- container protocol --------------------------------------------
    def __len__(self) -> int:
        return len(self.conf)

    def __getitem__(self, idx):
        return _MockResults(self._xyxy[idx], self.conf[idx], self.cls[idx])


class _EmptyResults:
    """Sentinel used when there are zero detections in a frame."""
    conf = np.array([], dtype=np.float32)
    cls = np.array([], dtype=np.float32)
    xywh = np.empty((0, 4), dtype=np.float32)
    xyxy = np.empty((0, 4), dtype=np.float32)

    def __len__(self) -> int:
        return 0

    def __getitem__(self, idx):
        return self


class ByteTrackWrapper:
    """Wraps ultralytics ``BYTETracker`` so it accepts / returns pipeline
    detection dicts (``List[Dict]``) instead of raw numpy / Boxes objects.

    Follows the same tracking flow as the reference ``people_counter.py``:

    1. Convert detection dicts → ``_MockResults`` (mimics ultralytics Boxes).
    2. Call ``BYTETracker.update(det, img, feats)`` exactly like the reference.
    3. Build **new** detection dicts from the tracker output – tracked
       (Kalman-filtered) bounding boxes replace the raw detections, and every
       dict carries a ``track_id`` assigned by ByteTrack.

    Only *confirmed* tracks are returned; untracked / low-confidence detections
    that ByteTrack has not yet promoted to active tracks are dropped (standard
    ByteTrack behaviour).
    """

    def __init__(
        self,
        track_high_thresh: float = 0.3,
        track_low_thresh: float = 0.1,
        new_track_thresh: float = 0.4,
        track_buffer: int = 60,
        match_thresh: float = 0.8,
        fuse_score: bool = True,
        frame_rate: int = 30,
    ):
        from ultralytics.trackers.byte_tracker import BYTETracker
        from ultralytics.utils import IterableSimpleNamespace

        cfg = IterableSimpleNamespace(
            tracker_type="bytetrack",
            track_high_thresh=track_high_thresh,
            track_low_thresh=track_low_thresh,
            new_track_thresh=new_track_thresh,
            track_buffer=track_buffer,
            match_thresh=match_thresh,
            fuse_score=fuse_score,
        )
        self._tracker = BYTETracker(args=cfg, frame_rate=frame_rate)

    # ------------------------------------------------------------------ #
    #  Public API                                                         #
    # ------------------------------------------------------------------ #

    def update(self, detections: List[Dict]) -> List[Dict]:
        """Run one tracking step.

        Parameters
        ----------
        detections : list[dict]
            Pipeline detection dicts.  Each must contain ``bounding_box``
            (``{xmin, ymin, xmax, ymax}`` **or** ``{x1, y1, x2, y2}``)
            and ``confidence``.

        Returns
        -------
        list[dict]
            One dict per **confirmed track** with Kalman-filtered bounding
            boxes, ``track_id``, ``confidence``, ``category`` and
            ``category_id``.
        """
        if not detections:
            # Advance the internal frame counter even on empty frames
            self._tracker.update(_EmptyResults(), img=None)
            return detections

        # -- 1. Convert dicts → numpy arrays -----------------------------
        xyxy_list: List[List[float]] = []
        valid_dets: List[Dict] = []          # originals that parsed OK
        for det in detections:
            bbox = det.get("bounding_box", det.get("bbox", {}))
            coords = self._bbox_to_xyxy(bbox)
            if coords is None:
                continue
            xyxy_list.append(coords)
            valid_dets.append(det)

        if not xyxy_list:
            self._tracker.update(_EmptyResults(), img=None)
            return detections

        xyxy = np.array(xyxy_list, dtype=np.float32)
        confs = np.array(
            [d.get("confidence", 0.5) for d in valid_dets], dtype=np.float32,
        )
        cls_ids = np.array(
            [d.get("category_id", 0) for d in valid_dets], dtype=np.float32,
        )

        # -- 2. Feed _MockResults to BYTETracker (same as reference) -----
        det_mock = _MockResults(xyxy, confs, cls_ids)
        tracks = self._tracker.update(det_mock, img=None)

        if len(tracks) == 0:
            return []

        # tracks shape: (N, 8) → [x1, y1, x2, y2, track_id, score, cls, idx]

        # -- 3. Build category_id → category_name map from originals -----
        cat_map: Dict[int, str] = {}
        for d in valid_dets:
            cid = d.get("category_id", 0)
            if cid not in cat_map and "category" in d:
                cat_map[cid] = d["category"]

        # -- 4. Build new detection dicts from tracked output -------------
        tracked_dets: List[Dict] = []
        for row in tracks:
            x1, y1, x2, y2, track_id, score, cls_id, _idx = row
            tracked_dets.append({
                "bounding_box": {
                    "xmin": float(x1), "ymin": float(y1),
                    "xmax": float(x2), "ymax": float(y2),
                },
                "confidence": float(score),
                "track_id": int(track_id),
                "category_id": int(cls_id),
                "category": cat_map.get(int(cls_id), "person"),
            })

        return tracked_dets

    # ------------------------------------------------------------------ #
    #  Private helpers                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _bbox_to_xyxy(bbox) -> Optional[List[float]]:
        """Convert a bounding-box (dict or list) to ``[x1, y1, x2, y2]``."""
        if isinstance(bbox, (list, tuple)):
            return [float(v) for v in bbox[:4]] if len(bbox) >= 4 else None
        if isinstance(bbox, dict):
            if "x1" in bbox:
                return [float(bbox["x1"]), float(bbox["y1"]),
                        float(bbox["x2"]), float(bbox["y2"])]
            if "xmin" in bbox:
                return [float(bbox["xmin"]), float(bbox["ymin"]),
                        float(bbox["xmax"]), float(bbox["ymax"])]
            vals = [float(v) for v in bbox.values()]
            return vals[:4] if len(vals) >= 4 else None
        return None


class PeopleTrackingUseCase(BaseProcessor):
    """People tracking use case with polygon/abline counting, zone analysis and alerting."""
    
    def __init__(self):
        """Initialize people tracking use case."""
        super().__init__("people_tracking")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = 'People_Tracking'
        self.CASE_VERSION: Optional[str] = '2.0'
        
        # Track ID storage for total count calculation
        self._total_track_ids = set()  # Store all unique track IDs seen across calls
        self._current_frame_track_ids = set()  # Store track IDs from current frame
        self._total_count = 0  # Cached total count
        self._last_update_time = time.time()  # Track when last updated
        
        # Zone-based tracking storage
        self._zone_current_track_ids = {}  # zone_name -> set of current track IDs in zone
        self._zone_total_track_ids = {}  # zone_name -> set of all track IDs that have been in zone
        self._zone_current_counts = {}  # zone_name -> current count in zone
        self._zone_total_counts = {}  # zone_name -> total count that have been in zone
        
        # Frame counter for tracking total frames processed
        self._total_frame_counter = 0  # Total frames processed across all calls
        
        # Global frame offset for video chunk processing
        self._global_frame_offset = 0  # Offset to add to local frame IDs for global frame numbering
        self._frames_in_current_chunk = 0  # Number of frames in current chunk
        
        # Initialize smoothing tracker
        self.smoothing_tracker = None

        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = None

        # --------------------------------------------------------------------- #
        # Tracking aliasing structures to merge fragmented IDs                   #
        # --------------------------------------------------------------------- #
        # Maps raw tracker IDs generated by ByteTrack to a stable canonical ID
        # that represents a real-world person. This helps avoid double counting
        # when the tracker loses a target temporarily and assigns a new ID.
        self._track_aliases: Dict[Any, Any] = {}

        # Stores metadata about each canonical track such as its last seen
        # bounding box, last update timestamp and all raw IDs that have been
        # merged into it.
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}

        # IoU threshold above which two bounding boxes are considered to belong
        # to the same person (empirically chosen; adjust in production if
        # needed).
        self._track_merge_iou_threshold: float = 0.04

        # Only merge with canonical tracks that were updated within this time
        # window (in seconds). This prevents accidentally merging tracks that
        # left the scene long ago.
        self._track_merge_time_window: float = 10.0

        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"

        self.start_timer = None

        # Line crossing tracking storage
        self._line_crossed_tracks: Dict[str, Set[Any]] = {}  # "side1_to_side2": set of track_ids that crossed
        self._side1_label: str = "Side A"
        self._side2_label: str = "Side B"

        # ByteTrackWrapper instance (lazy-init)
        self.tracker = None

        # Counter instance (lazy-init based on config.method)
        self._counter = None
        self._counter_method: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Public entry point (flat, people_counting.py style)                 #
    # ------------------------------------------------------------------ #

    def process(self, data: Any, config: ConfigProtocol,
                context: Optional[ProcessingContext] = None,
                stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """Process a single frame of detections and return agg_summary with in/out counts.
        Args:
            data: Raw model output (detection or tracking format)
            config: People counting configuration
            context: Processing context
            stream_info: Stream information containing frame details (optional)
            
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        processing_start = time.time()

        try:
            if not isinstance(config, PeopleTrackingConfig):
                return self.create_error_result(
                    "Invalid configuration type for people tracking",
                    usecase=self.name, category=self.category, context=context
                )

            if context is None:
                context = ProcessingContext()

            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold

            # --- 1. Normalize to list (single frame) ---
            if isinstance(data, list):
                processed_data = data
            elif isinstance(data, dict):
                # Frame-keyed dict – take the first frame's detections
                processed_data = []
                for _key, value in data.items():
                    if isinstance(value, list):
                        processed_data = value
                        break
            else:
                processed_data = []

            # --- 2. Confidence filter ---
            if config.confidence_threshold is not None:
                processed_data = [d for d in processed_data if d.get("confidence", 0) >= config.confidence_threshold]

            # --- 3. Category mapping ---
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)

            # --- 4. Person category filter ---
            if config.person_categories:
                processed_data = [d for d in processed_data if d.get("category") in config.person_categories]

            # --- 5. Normalize track_id field ---
            for det in processed_data:
                if not isinstance(det, dict):
                    continue
                if det.get("track_id") is not None:
                    continue
                for key in ("tracker_id", "tracking_id", "trackId", "trackID", "id", "object_id"):
                    candidate = det.get(key)
                    if candidate is not None:
                        det["track_id"] = candidate
                        break

            # --- 6. ByteTrack tracker (ultralytics) ---
            if getattr(config, "enable_advanced_tracker", True):
                if self.tracker is None:
                    self.tracker = ByteTrackWrapper(
                        track_high_thresh=0.3,
                        track_low_thresh=0.1,
                        new_track_thresh=0.4,
                        track_buffer=60,
                        match_thresh=0.8,
                        frame_rate=30,
                    )

                processed_data = self.tracker.update(processed_data)

            # --- 7. Update tracking state ---
            counting_summary = {
                "total_objects": len(processed_data),
                "detections": processed_data,
                "categories": {}
            }
            for detection in processed_data:
                category = detection.get("category", "unknown")
                counting_summary["categories"][category] = counting_summary["categories"].get(category, 0) + 1

            # self._update_tracking_state(counting_summary)
            self._total_frame_counter += 1

            # --- 8. Determine frame number ---
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame
            if frame_number is None:
                frame_number = self._total_frame_counter

            # --- 9. Init or reuse counter, run counter.update() ---
            counter = self._get_or_create_counter(config)
            boxes, track_ids = self._extract_boxes_and_ids(processed_data)
            counter.update(boxes, track_ids)

            # --- 10. Generate alerts, incidents, tracking_stats, business_analytics, summary ---
            zone_analysis = {}
            alerts = self._check_alerts(counting_summary, zone_analysis, config, str(frame_number))
            incidents = self._generate_incidents(counting_summary, zone_analysis, alerts, config, str(frame_number), stream_info)
            incidents = []  # Keep empty as in original

            tracking_stats_list = self._generate_tracking_stats(
                counting_summary, zone_analysis, config,
                frame_id=str(frame_number), alerts=alerts, stream_info=stream_info,
                counter=counter
            )
            business_analytics = self._generate_business_analytics(counting_summary, zone_analysis, config, str(frame_number), stream_info, is_empty=True)
            summary_list = self._generate_summary(counting_summary, incidents, tracking_stats_list, business_analytics, alerts)

            incidents_out = incidents[0] if incidents else {}
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
            business_analytics_out = business_analytics[0] if business_analytics else {}
            summary = summary_list[0] if summary_list else {}

            agg_summary = {str(frame_number): {
                "incidents": incidents_out,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics_out,
                "alerts": alerts,
                "human_text": summary}
            }

            context.mark_completed()
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context
            )

            proc_time = time.time() - processing_start
            processing_latency_ms = proc_time * 1000.0
            processing_fps = (1.0 / proc_time) if proc_time > 0 else None
            print(f"[PERF] F{self._total_frame_counter} | latency={processing_latency_ms:.1f}ms fps={processing_fps:.1f}" if processing_fps else f"[PERF] F{self._total_frame_counter} | latency={processing_latency_ms:.1f}ms")
            return result

        except Exception as e:
            self.logger.error(f"People tracking failed: {str(e)}", exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(e), type(e).__name__,
                usecase=self.name, category=self.category, context=context
            )

    # ------------------------------------------------------------------ #
    # Counter management (NEW)                                            #
    # ------------------------------------------------------------------ #

    def _get_or_create_counter(self, config: PeopleTrackingConfig):
        """Return existing counter or create one from config."""
        if self._counter is not None and self._counter_method == config.method:
            return self._counter

        if config.method == "polygon":
            outer = np.array(config.outer_polygon, dtype=np.float64)
            if config.inner_polygon is not None:
                inner = np.array(config.inner_polygon, dtype=np.int32)
            else:
                inner = polygon_offset_inward(outer, config.inner_polygon_offset)
            self._counter = PolygonCounter(
                inner_polygon=inner,
                outer_polygon=np.array(config.outer_polygon, dtype=np.int32),
                initial_warmup_frames=5,
                use_foot_center=config.use_foot_center,
            )
        elif config.method == "abline":
            line_a = parse_line_config(config.line_a)
            line_b = parse_line_config(config.line_b)
            self._counter = ABLineCounter(
                line_a=line_a,
                line_b=line_b,
                in_direction=config.in_direction,
                use_foot_center=config.use_foot_center,
            )
        else:
            raise ValueError(f"Unknown counting method: {config.method}")

        self._counter_method = config.method
        self.logger.info(f"Created {config.method} counter (use_foot_center={config.use_foot_center})")
        return self._counter

    @staticmethod
    def _bbox_to_xyxy(bbox: Any) -> Optional[List[float]]:
        """Convert a bounding-box (dict or list) to [x1, y1, x2, y2]."""
        if isinstance(bbox, list):
            return bbox[:4] if len(bbox) >= 4 else None
        if isinstance(bbox, dict):
            if "x1" in bbox:
                return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
            if "xmin" in bbox:
                return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
            vals = list(bbox.values())
            return vals[:4] if len(vals) >= 4 else None
        return None

    def _extract_boxes_and_ids(self, detections: List[Dict]):
        """Return (boxes, track_ids) as numpy arrays from detection dicts."""
        boxes_list: List[List[float]] = []
        ids_list: List[int] = []

        for idx, det in enumerate(detections):
            raw_bbox = det.get("bounding_box", det.get("bbox"))
            xyxy = self._bbox_to_xyxy(raw_bbox)
            if xyxy is None:
                continue
            track_id = det.get("track_id")
            if track_id is None:
                track_id = idx
            else:
                try:
                    track_id = int(track_id)
                except (ValueError, TypeError):
                    track_id = hash(track_id) % (10**9)
            boxes_list.append([float(v) for v in xyxy])
            ids_list.append(track_id)

        if not boxes_list:
            return np.empty((0, 4)), np.array([], dtype=np.int64)
        return np.array(boxes_list, dtype=np.float64), np.array(ids_list, dtype=np.int64)

    # ------------------------------------------------------------------ #
    # Existing helper methods (preserved from original)                   #
    # ------------------------------------------------------------------ #

    def _generate_incidents(self, counting_summary: Dict, zone_analysis: Dict, alerts: List, config: PeopleTrackingConfig, frame_id: str, stream_info: Optional[Dict[str, Any]] = None, line_analysis: Optional[Dict] = None) -> List[Dict]:
        """Generate standardized incidents for the agg_summary structure."""
        
        camera_info = self.get_camera_info_from_stream(stream_info)
        incidents = []
        total_people = counting_summary.get("total_objects", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info, frame_id=frame_id)
        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list

        alert_settings=[]
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                    getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                            }
            })

        if total_people > 0:
            # Determine event level based on thresholds
            
            level = "info"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)
            if start_timestamp and self.current_incident_end_timestamp=='N/A':
                self.current_incident_end_timestamp = 'Incident still active'
            elif start_timestamp and self.current_incident_end_timestamp=='Incident still active':
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5: 
                    self.current_incident_end_timestamp = current_timestamp
            elif self.current_incident_end_timestamp!='Incident still active' and self.current_incident_end_timestamp!='N/A':
                self.current_incident_end_timestamp = 'N/A'
            
            if config.alert_config and hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 10)
                intensity = min(10.0, (total_people / threshold) * 10)
                
                if intensity >= 9:
                    level = "critical"
                    self._ascending_alert_list.append(3)
                elif intensity >= 7:
                    level = "significant"
                    self._ascending_alert_list.append(2)
                elif intensity >= 5:
                    level = "medium"
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    self._ascending_alert_list.append(0)
            else:
                if total_people > 30:
                    level = "critical"
                    intensity = 10.0
                    self._ascending_alert_list.append(3)
                elif total_people > 25:
                    level = "significant"; intensity = 9.0; self._ascending_alert_list.append(2)
                elif total_people > 15:
                    level = "medium"
                    intensity = 7.0
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    intensity = min(10.0, total_people / 3.0)
                    self._ascending_alert_list.append(0)
            
             # Generate human text in new format
            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE,level)}")
            human_text = "\n".join(human_text_lines)

            # Main people counting incident
            event= self.create_incident(incident_id=self.CASE_TYPE+'_'+str(frame_id), incident_type=self.CASE_TYPE,
                       severity_level=level, human_text=human_text, camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
                       start_time=start_timestamp, end_time=self.current_incident_end_timestamp,
                       level_settings= {"low": 1, "medium": 3, "significant":4, "critical": 7})
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})
        
        return incidents

    def _generate_tracking_stats(self, counting_summary: Dict, zone_analysis: Dict, config: PeopleTrackingConfig, frame_id: str, alerts: Any=[], stream_info: Optional[Dict[str, Any]] = None, line_analysis: Optional[Dict] = None, counter=None) -> List[Dict]:
        """Generate tracking stats using standardized methods, with in/out from counter."""
        
        total_people = counting_summary.get("total_objects", 0)
        total_unique_count = self.get_total_count()
        current_frame_count = self.get_current_frame_count()
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        # Build total_counts with in/out from counter
        total_counts = []
        if counter is not None:
            total_counts.append(self.create_count_object("in", counter.total_in))
            total_counts.append(self.create_count_object("out", counter.total_out))
        
        # Also add per-category totals from tracking state
        # for category in config.person_categories or ["person"]:
        #     category_total_count = total_unique_count
        #     if category_total_count > 0:
        #         total_counts.append(self.create_count_object(category, category_total_count))
        
        # Build current_counts with new_in/new_out from counter
        current_counts = []
        if counter is not None:
            current_counts.append(self.create_count_object("in", getattr(counter, "total_in", 0)))
            current_counts.append(self.create_count_object("out", getattr(counter, "total_out", 0)))

        # for category in config.person_categories or ["person"]:
        #     detections = counting_summary.get("detections", [])
        #     category_current_count = sum(1 for d in detections if d.get("category") == category)
        #     if category_current_count > 0 or total_people > 0:
        #         current_counts.append(self.create_count_object(category, category_current_count))
        
        # Prepare detections
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
            if detection.get("masks"):
                detection_obj = self.create_detection_object(category, bbox, segmentation=detection.get("masks", []))
            elif detection.get("segmentation"):
                detection_obj = self.create_detection_object(category, bbox, segmentation=detection.get("segmentation"))
            elif detection.get("mask"):
                detection_obj = self.create_detection_object(category, bbox, segmentation=detection.get("mask"))
            else:
                detection_obj = self.create_detection_object(category, bbox)
            detections.append(detection_obj)
        
        # Alert settings
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                    getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                            }
            })

        # Human text with counter info
        human_text = self._generate_human_text_for_tracking(total_people, total_unique_count, config, frame_id, alerts, stream_info, counter=counter)
        
        # Timestamps
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True, frame_id=frame_id)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        tracking_stat = self.create_tracking_stats(
            total_counts, current_counts, detections, human_text, camera_info, alerts, alert_settings,
            start_time=high_precision_start_timestamp, reset_time=high_precision_reset_timestamp
        )
        
        return [tracking_stat]
    
    def _generate_human_text_for_tracking(self, total_people: int, total_unique_count: int, config: PeopleTrackingConfig, frame_id: str, alerts: Any=[], stream_info: Optional[Dict[str, Any]] = None, counter=None) -> str:
        """Generate human-readable text for tracking stats."""
        human_text_lines = []
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=True, frame_id=frame_id)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        human_text_lines.append(f"\t- People Detected: {total_people}")
        if counter is not None:
            human_text_lines.append(f"\t- Present count: {counter.present_count}")
            human_text_lines.append(f"\t- New in: {getattr(counter, 'new_in', 0)}")
            human_text_lines.append(f"\t- New out: {getattr(counter, 'new_out', 0)}")

        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE @ {start_timestamp}:")
        if counter is not None:
            human_text_lines.append(f"\t- Total In: {counter.total_in}")
            human_text_lines.append(f"\t- Total Out: {counter.total_out}")
        if total_unique_count > 0:
            human_text_lines.append(f"\t- Total unique people count: {total_unique_count}")

        if alerts:
            for alert in alerts:
                human_text_lines.append(f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}")
        else:
            human_text_lines.append("Alerts: None")
        
        return "\n".join(human_text_lines)

    def _check_alerts(self, counting_summary: Dict, zone_analysis: Dict, 
                     config: PeopleTrackingConfig, frame_id: str, line_analysis: Optional[Dict] = None) -> List[Dict]:
        """Check for alert conditions and generate alerts."""
        def get_trend(data, lookback=900, threshold=0.6):
            '''
            Determine if the trend is ascending or descending based on actual value progression.
            Now works with values 0,1,2,3 (not just binary).
            '''
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True  # not enough data to determine trend
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            if ratio >= threshold:
                return True
            elif ratio <= (1 - threshold):
                return False
        alerts = []
        
        if not config.alert_config:
            return alerts
        
        total_people = counting_summary.get("total_objects", 0)
        
        # Count threshold alerts
        if hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:

            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_people >= threshold:

                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                        "alert_id": "alert_"+category+'_'+frame_id,
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                     getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                    }                    
                    })
                elif category in counting_summary.get("by_category", {}):
                    count = counting_summary["by_category"][category]
                    if count >= threshold:
                        alerts.append({
                            "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                            "alert_id": "alert_"+category+'_'+frame_id,
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                         getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])}                    
                        })
        
        return alerts

    def _generate_business_analytics(self, counting_summary: Dict, zone_analysis: Dict, config: PeopleTrackingConfig, frame_id: str, stream_info: Optional[Dict[str, Any]] = None, is_empty=False) -> List[Dict]:
        """Generate standardized business analytics for the agg_summary structure."""
        if is_empty:
            return []
        business_analytics = []
        total_people = counting_summary.get("total_objects", 0)
        
        # Get camera info using standardized method
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        if total_people > 0 or config.enable_analytics:
            analytics_stats = {
                "people_count": total_people,
                "unique_people_count": self.get_total_count(),
                "current_frame_count": self.get_current_frame_count()
            }
            
            # Add zone analytics if available
            if zone_analysis:
                zone_stats = {}
                for zone_name, zone_count in zone_analysis.items():
                    zone_total = self._robust_zone_total(zone_count)
                    zone_stats[f"{zone_name}_occupancy"] = zone_total
                analytics_stats.update(zone_stats)
            
            # Generate human text for analytics
            current_timestamp = self._get_current_timestamp_str(stream_info, frame_id=frame_id)
            start_timestamp = self._get_start_timestamp_str(stream_info)
            
            analytics_human_text = self.generate_analytics_human_text(
                "people_counting_analytics", analytics_stats, current_timestamp, start_timestamp
            )
            
            # Create business analytics using standardized method
            analytics = self.create_business_analytics(
                "people_counting_analytics", analytics_stats, analytics_human_text, camera_info
            )
            business_analytics.append(analytics)
        
        return business_analytics

    def _generate_summary(self, summary: dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: "+self.CASE_TYPE)
        lines.append("Application Version: "+self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: "+f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: "+f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: "+f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: "+"No Summary Data")

        return ["\n".join(lines)]
                
    def _extract_predictions(self, data: Any) -> List[Dict[str, Any]]:
        """Extract predictions from processed data for API compatibility."""
        predictions = []
        try:
            if isinstance(data, list):
                # Detection format
                for item in data:
                    prediction = self._normalize_prediction(item)
                    if prediction:
                        predictions.append(prediction)
            
            elif isinstance(data, dict):
                # Frame-based or tracking format
                for frame_id, items in data.items():
                    if isinstance(items, list):
                        for item in items:
                            prediction = self._normalize_prediction(item)
                            if prediction:
                                prediction["frame_id"] = frame_id
                                predictions.append(prediction)
        
        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")
        
        return predictions
    
    def _normalize_prediction(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a single prediction item."""
        if not isinstance(item, dict):
            return {}
        
        return {
            "category": item.get("category", item.get("class", "unknown")),
            "confidence": item.get("confidence", item.get("score", 0.0)),
            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
            "track_id": item.get("track_id")
        }
    
    def _get_detections_with_confidence(self, counting_summary: Dict) -> List[Dict]:
        """Extract detection items with confidence scores."""
        return counting_summary.get("detections", [])
    
    def _count_unique_tracks(self, counting_summary: Dict, config: PeopleTrackingConfig = None) -> Optional[int]:
        """Count unique tracks if tracking is enabled."""
        # Always update tracking state regardless of enable_unique_counting setting
        self._update_tracking_state(counting_summary)
        
        # Only return the count if unique counting is enabled
        if config and config.enable_unique_counting:
            return self._total_count if self._total_count > 0 else None
        else:
            return None
    
    def _update_tracking_state(self, counting_summary: Dict) -> None:
        """Update tracking state with current frame data (always called)."""
        detections = self._get_detections_with_confidence(counting_summary)

        if not detections:
            return

        # Map raw tracker IDs to canonical IDs to avoid duplicate counting
        current_frame_tracks: Set[Any] = set()

        # Local sequence to make ephemeral IDs unique within the same call
        ephemeral_seq = 0

        for detection in detections:
            # Prefer explicit tracker-provided ID when available
            raw_track_id = detection.get("track_id")

            # Always require a bbox to perform IoU-based merging
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            # For single-frame detectors (e.g., plain YOLO) there is no track_id.
            # Generate a short-lived ID and merge by IoU against recent canonical tracks.
            if raw_track_id is None:
                raw_track_id = self._generate_ephemeral_track_id(bbox, ephemeral_seq)
                ephemeral_seq += 1

            canonical_id = self._merge_or_register_track(raw_track_id, bbox)

            # Propagate canonical ID so that downstream logic (including zone
            # tracking and event generation) operates on the de-duplicated ID.
            detection["track_id"] = canonical_id
            current_frame_tracks.add(canonical_id)

        # Update total track IDs with new canonical IDs from current frame
        old_total_count = len(self._total_track_ids)
        self._total_track_ids.update(current_frame_tracks)
        self._current_frame_track_ids = current_frame_tracks

        # Update total count
        self._total_count = len(self._total_track_ids)
        self._last_update_time = time.time()

        # Log tracking state updates
        if len(current_frame_tracks) > 0:
            new_tracks = current_frame_tracks - (self._total_track_ids - current_frame_tracks)
            if new_tracks:
                self.logger.debug(
                    f"Tracking state updated: {len(new_tracks)} new canonical track IDs added, total unique tracks: {self._total_count}")
            else:
                self.logger.debug(
                    f"Tracking state updated: {len(current_frame_tracks)} current frame canonical tracks, total unique tracks: {self._total_count}")

    def _generate_ephemeral_track_id(self, bbox: Any, seq: int) -> str:
        """Create a short-lived raw track id for detections without a track_id.

        Combines a coarse hash of the bbox geometry with a per-call sequence and
        a millisecond timestamp, so the same person across adjacent frames will
        still be merged to the same canonical track via IoU and time window,
        while avoiding long-lived ID collisions across distant calls.
        """
        try:
            # Normalize bbox to xyxy list for hashing
            if isinstance(bbox, dict):
                if "x1" in bbox:
                    xyxy = [bbox.get("x1"), bbox.get("y1"), bbox.get("x2"), bbox.get("y2")]
                elif "xmin" in bbox:
                    xyxy = [bbox.get("xmin"), bbox.get("ymin"), bbox.get("xmax"), bbox.get("ymax")]
                else:
                    values = list(bbox.values())
                    xyxy = values[:4] if len(values) >= 4 else []
            elif isinstance(bbox, list):
                xyxy = bbox[:4]
            else:
                xyxy = []

            if len(xyxy) < 4:
                xyxy = [0, 0, 0, 0]

            x1, y1, x2, y2 = xyxy
            # Coarse-quantize geometry to stabilize hash across minor jitter
            cx = int(round((float(x1) + float(x2)) / 2.0))
            cy = int(round((float(y1) + float(y2)) / 2.0))
            w = int(round(abs(float(x2) - float(x1))))
            h = int(round(abs(float(y2) - float(y1))))
            geom_token = f"{cx}_{cy}_{w}_{h}"
        except Exception:
            geom_token = "0_0_0_0"

        ms = int(time.time() * 1000)
        return f"tmp_{ms}_{seq}_{abs(hash(geom_token)) % 1000003}"
    
    def get_total_count(self) -> int:
        """Get the total count of unique people tracked across all calls."""
        return self._total_count
    
    def get_current_frame_count(self) -> int:
        """Get the count of people in the current frame."""
        return len(self._current_frame_track_ids)
    
    def get_total_frames_processed(self) -> int:
        """Get the total number of frames processed across all calls."""
        return self._total_frame_counter
    
    def set_global_frame_offset(self, offset: int) -> None:
        """Set the global frame offset for video chunk processing."""
        self._global_frame_offset = offset
        self.logger.info(f"Global frame offset set to: {offset}")
    
    def get_global_frame_offset(self) -> int:
        """Get the current global frame offset."""
        return self._global_frame_offset
    
    def update_global_frame_offset(self, frames_in_chunk: int) -> None:
        """Update global frame offset after processing a chunk."""
        old_offset = self._global_frame_offset
        self._global_frame_offset += frames_in_chunk
        self.logger.info(f"Global frame offset updated: {old_offset} -> {self._global_frame_offset} (added {frames_in_chunk} frames)")
    
    def get_global_frame_id(self, local_frame_id: str) -> str:
        """Convert local frame ID to global frame ID."""
        try:
            # Try to convert local_frame_id to integer
            local_frame_num = int(local_frame_id)
            global_frame_num = local_frame_num #+ self._global_frame_offset
            return str(global_frame_num)
        except (ValueError, TypeError):
            # If local_frame_id is not a number (e.g., timestamp), return as is
            return local_frame_id
    
    def get_track_ids_info(self) -> Dict[str, Any]:
        """Get detailed information about track IDs."""
        return {
            "total_count": self._total_count,
            "current_frame_count": len(self._current_frame_track_ids),
            "total_unique_track_ids": len(self._total_track_ids),
            "current_frame_track_ids": list(self._current_frame_track_ids),
            "last_update_time": self._last_update_time,
            "total_frames_processed": self._total_frame_counter
        }
    
    def get_tracking_debug_info(self) -> Dict[str, Any]:
        """Get detailed debugging information about tracking state."""
        return {
            "total_track_ids": list(self._total_track_ids),
            "current_frame_track_ids": list(self._current_frame_track_ids),
            "total_count": self._total_count,
            "current_frame_count": len(self._current_frame_track_ids),
            "total_frames_processed": self._total_frame_counter,
            "last_update_time": self._last_update_time,
            "zone_current_track_ids": {zone: list(tracks) for zone, tracks in self._zone_current_track_ids.items()},
            "zone_total_track_ids": {zone: list(tracks) for zone, tracks in self._zone_total_track_ids.items()},
            "zone_current_counts": self._zone_current_counts.copy(),
            "zone_total_counts": self._zone_total_counts.copy(),
            "global_frame_offset": self._global_frame_offset,
            "frames_in_current_chunk": self._frames_in_current_chunk,
            "line_crossed_tracks": {dir: list(tracks) for dir, tracks in self._line_crossed_tracks.items()}
        }
    
    def get_frame_info(self) -> Dict[str, Any]:
        """Get detailed information about frame processing and global frame offset."""
        return {
            "global_frame_offset": self._global_frame_offset,
            "total_frames_processed": self._total_frame_counter,
            "frames_in_current_chunk": self._frames_in_current_chunk,
            "next_global_frame": self._global_frame_offset + self._frames_in_current_chunk
        }
    
    def reset_tracking_state(self) -> None:
        """
          WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        self._total_track_ids.clear()
        self._current_frame_track_ids.clear()
        self._total_count = 0
        self._last_update_time = time.time()
        
        # Clear zone tracking data
        self._zone_current_track_ids.clear()
        self._zone_total_track_ids.clear()
        self._zone_current_counts.clear()
        self._zone_total_counts.clear()
        
        # Reset frame counter and global frame offset
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._frames_in_current_chunk = 0

        # Clear aliasing information
        self._canonical_tracks.clear()
        self._track_aliases.clear()
        self._tracking_start_time = None

        # Clear line crossing data
        self._line_crossed_tracks.clear()
        
        self.logger.warning(" FULL tracking state reset - all track IDs, zone data, line crossing data, frame counter, and global frame offset cleared. Cumulative totals lost!")
    
    def clear_current_frame_tracking(self) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        old_current_count = len(self._current_frame_track_ids)
        self._current_frame_track_ids.clear()
        
        # Clear current zone tracking (but keep total zone tracking)
        cleared_zone_tracks = 0
        for zone_name in list(self._zone_current_track_ids.keys()):
            cleared_zone_tracks += len(self._zone_current_track_ids[zone_name])
            self._zone_current_track_ids[zone_name].clear()
            self._zone_current_counts[zone_name] = 0
        
        # Update timestamp
        self._last_update_time = time.time()
        
        self.logger.info(f"Cleared {old_current_count} current frame tracks and {cleared_zone_tracks} zone current tracks. Cumulative total preserved: {self._total_count}")
        return old_current_count
    
    def reset_frame_counter(self) -> None:
        self._total_frame_counter = 0
    
    def clear_expired_tracks(self, max_age_seconds: float = 300.0) -> int:
        current_time = time.time()
        if current_time - self._last_update_time > max_age_seconds:
            return self.clear_current_frame_tracking()
        return 0

    def _update_zone_tracking(self, zone_analysis: Dict[str, Dict[str, int]], detections: List[Dict], config: PeopleTrackingConfig) -> Dict[str, Dict[str, Any]]:
        """Update zone tracking with current frame data."""
        if not zone_analysis or not config.zone_config or not config.zone_config.zones:
            return {}
        enhanced_zone_analysis = {}
        zones = config.zone_config.zones
        current_frame_zone_tracks = {}
        for zone_name in zones.keys():
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            center_point = get_bbox_bottom25_center(bbox)
            for zone_name, zone_polygon in zones.items():
                polygon_points = [(point[0], point[1]) for point in zone_polygon]
                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)
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
                "original_counts": zone_counts
            }
        return enhanced_zone_analysis

    def get_zone_tracking_info(self) -> Dict[str, Dict[str, Any]]:
        return {
            zone_name: {
                "current_count": self._zone_current_counts.get(zone_name, 0),
                "total_count": self._zone_total_counts.get(zone_name, 0),
                "current_track_ids": list(self._zone_current_track_ids.get(zone_name, set())),
                "total_track_ids": list(self._zone_total_track_ids.get(zone_name, set()))
            }
            for zone_name in set(self._zone_current_counts.keys()) | set(self._zone_total_counts.keys())
        }
    
    def get_zone_current_count(self, zone_name: str) -> int:
        return self._zone_current_counts.get(zone_name, 0)
    
    def get_zone_total_count(self, zone_name: str) -> int:
        return self._zone_total_counts.get(zone_name, 0)
    
    def get_all_zone_counts(self) -> Dict[str, Dict[str, int]]:
        return {
            zone_name: {
                "current": self._zone_current_counts.get(zone_name, 0),
                "total": self._zone_total_counts.get(zone_name, 0)
            }
            for zone_name in set(self._zone_current_counts.keys()) | set(self._zone_total_counts.keys())
        }

    def _update_line_crossings(self, detections: List[Dict], line_config: LineConfig) -> Dict[str, Any]:
        """Update line crossing tracking with current frame data and detect crossings."""
        if not line_config or not line_config.points or len(line_config.points) != 2:
            return {}
        self._side1_label = line_config.side1_label
        self._side2_label = line_config.side2_label
        direction1 = "side1_to_side2"
        direction2 = "side2_to_side1"
        if direction1 not in self._line_crossed_tracks:
            self._line_crossed_tracks[direction1] = set()
        if direction2 not in self._line_crossed_tracks:
            self._line_crossed_tracks[direction2] = set()
        crossings_this_frame = {direction1: 0, direction2: 0}
        for detection in detections:
            canonical_id = detection.get("track_id")
            if canonical_id not in self._canonical_tracks:
                continue
            info = self._canonical_tracks[canonical_id]
            if "last_side" not in info:
                info["last_side"] = None
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            center = get_bbox_bottom25_center(bbox)
            side = self._compute_side(center, line_config.points)
            if info["last_side"] is None:
                if side != "on_line":
                    info["last_side"] = side
                continue
            if side != info["last_side"] and side != "on_line":
                direction = f"{info['last_side']}_to_{side}"
                if canonical_id not in self._line_crossed_tracks.get(direction, set()):
                    self._line_crossed_tracks[direction].add(canonical_id)
                    crossings_this_frame[direction] += 1
                info["last_side"] = side
            elif side != "on_line":
                info["last_side"] = side
        total_crossings = {dir: len(tracks) for dir, tracks in self._line_crossed_tracks.items()}
        return {"crossings_this_frame": crossings_this_frame, "total_crossings": total_crossings}

    def _compute_side(self, point: tuple, line_points: List[List[float]]) -> str:
        if not line_points or len(line_points) != 2:
            return "on_line"
        (x1, y1), (x2, y2) = line_points
        dx = x2 - x1; dy = y2 - y1
        px, py = point
        cross = (px - x1) * dy - (py - y1) * dx
        if cross > 0: return "side1"
        elif cross < 0: return "side2"
        else: return "on_line"

    def _robust_zone_total(self, zone_count):
        if isinstance(zone_count, dict):
            total = 0
            for v in zone_count.values():
                if isinstance(v, int): total += v
                elif isinstance(v, list): total += len(v)
            return total
        elif isinstance(zone_count, list): return len(zone_count)
        elif isinstance(zone_count, int): return zone_count
        else: return 0

    # --------------------------------------------------------------------- #
    # Private helpers for canonical track aliasing                          #
    # --------------------------------------------------------------------- #

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        if isinstance(box1, dict) and isinstance(box2, dict):
            return calculate_iou(box1, box2)
        def _bbox_to_list(bbox):
            if bbox is None: return []
            if isinstance(bbox, list): return bbox[:4] if len(bbox) >= 4 else []
            if isinstance(bbox, dict):
                if "xmin" in bbox: return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
                if "x1" in bbox: return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
                values = list(bbox.values())
                return values[:4] if len(values) >= 4 else []
            return []
        list1 = _bbox_to_list(box1); list2 = _bbox_to_list(box2)
        if len(list1) < 4 or len(list2) < 4: return 0.0
        x1_min, y1_min, x1_max, y1_max = list1
        x2_min, y2_min, x2_max, y2_max = list2
        x1_min, x1_max = min(x1_min, x1_max), max(x1_min, x1_max)
        y1_min, y1_max = min(y1_min, y1_max), max(y1_min, y1_max)
        x2_min, x2_max = min(x2_min, x2_max), max(x2_min, x2_max)
        y2_min, y2_max = min(y2_min, y2_max), max(y2_min, y2_max)
        inter_x_min = max(x1_min, x2_min); inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max); inter_y_max = min(y1_max, y2_max)
        inter_w = max(0.0, inter_x_max - inter_x_min)
        inter_h = max(0.0, inter_y_max - inter_y_min)
        inter_area = inter_w * inter_h
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = area1 + area2 - inter_area
        return (inter_area / union_area) if union_area > 0 else 0.0

    def _get_canonical_id(self, raw_id: Any) -> Any:
        return self._track_aliases.get(raw_id, raw_id)

    def _merge_or_register_track(self, raw_id: Any, bbox: List[float]) -> Any:
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
                info["last_bbox"] = bbox; info["last_update"] = now; info["raw_ids"].add(raw_id)
                return canonical_id
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox, "last_update": now, "raw_ids": {raw_id}, "last_side": None
        }
        return canonical_id

    # --------------------------------------------------------------------- #
    # Timestamp helpers                                                     #
    # --------------------------------------------------------------------- #

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
        else:
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        if not stream_info:
            return "00:00:00"
        if precision:
            if self.start_timer is None:
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)
        if self.start_timer is None:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)
        else:
            if self.start_timer is not None:
                return self._format_timestamp(self.start_timer)
            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()
            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _extract_frame_id_from_tracking(self, frame_detections: List[Dict], frame_key: str) -> str:
        if frame_detections and len(frame_detections) > 0:
            first_detection = frame_detections[0]
            if "frame" in first_detection:
                return str(first_detection["frame"])
            elif "frame_id" in first_detection:
                return str(first_detection["frame_id"])
        return str(frame_key)

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp so that exactly two digits follow the decimal point."""
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d-%H:%M:%S.%f UTC')
        if not isinstance(timestamp, str):
            return str(timestamp)
        if '.' not in timestamp:
            return timestamp
        main_part, fractional_and_suffix = timestamp.split('.', 1)
        if ' ' in fractional_and_suffix:
            fractional_part, suffix = fractional_and_suffix.split(' ', 1)
            suffix = ' ' + suffix
        else:
            fractional_part, suffix = fractional_and_suffix, ''
        fractional_part = (fractional_part + '00')[:2]
        return f"{main_part}.{fractional_part}{suffix}"

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()

    # --------------------------------------------------------------------- #
    # Config helpers                                                        #
    # --------------------------------------------------------------------- #

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "method": {"type": "string", "enum": ["polygon", "abline"], "default": "polygon"},
                "use_foot_center": {"type": "boolean", "default": True},
                "confidence_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5},
                "outer_polygon": {"type": "array", "description": "Outer polygon vertices [[x,y], ...]"},
                "inner_polygon": {"type": ["array", "null"]},
                "inner_polygon_offset": {"type": "integer", "default": 20},
                "line_a": {"type": ["array", "null"]},
                "line_b": {"type": ["array", "null"]},
                "in_direction": {"type": "string", "enum": ["A_to_B", "B_to_A"], "default": "A_to_B"},
                "person_categories": {"type": "array", "items": {"type": "string"}, "default": ["person", "people"]},
                "enable_advanced_tracker": {"type": "boolean", "default": True},
            },
            "required": ["method"],
            "additionalProperties": False,
        }
    
    def create_default_config(self, **overrides) -> PeopleTrackingConfig:
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "method": "polygon",
            "use_foot_center": True,
            "enable_tracking": False,
            "enable_analytics": True,
            "enable_unique_counting": True,
            "time_window_minutes": 60,
            "person_categories": ["person", "people"],
        }
        defaults.update(overrides)
        return PeopleTrackingConfig(**defaults)

    def _apply_smoothing(self, data: Any, config: PeopleTrackingConfig) -> Any:
        """Apply smoothing to tracking data if enabled."""
        if self.smoothing_tracker is None:
            smoothing_config = BBoxSmoothingConfig(
                smoothing_algorithm=config.smoothing_algorithm,
                window_size=config.smoothing_window_size,
                cooldown_frames=config.smoothing_cooldown_frames,
                confidence_threshold=config.confidence_threshold or 0.5,
                confidence_range_factor=config.smoothing_confidence_range_factor,
                enable_smoothing=True
            )
            self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
        smoothed_data = bbox_smoothing(data, self.smoothing_tracker.config, self.smoothing_tracker)
        self.logger.debug(f"Applied bbox smoothing to tracking results")
        return smoothed_data
