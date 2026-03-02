from typing import Any, Dict, List, Optional, Tuple
from dataclasses import asdict
import time
from datetime import datetime, timezone
import numpy as np
from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol, ResultFormat
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
    BBoxSmoothingTracker
)
from dataclasses import dataclass, field
from ..core.config import PeopleCountingConfig, BaseConfig, AlertConfig, ZoneConfig

@dataclass
class PeopleCountingInZoneConfig(BaseConfig):
    """Configuration for people counting use case."""

    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # ====== PERFORMANCE: Tracker selection ======
    enable_advanced_tracker: bool = True  # Heavy O(n³) tracker - enable only when tracking quality is critical
    enable_simple_tracker: bool = False     # Lightweight O(n) tracker - enabled by default for tracking ID assignment
    # ====== END PERFORMANCE CONFIG ======
    confidence_threshold: float = 0.245

    # Zone configuration
    zone_config: Optional[ZoneConfig] = None
    
    # Counting parameters
    enable_unique_counting: bool = True
    time_window_minutes: int = 60
    
    # Category mapping
    person_categories: List[str] = field(default_factory=lambda: ["person", "people"])
    index_to_category: Optional[Dict[int, str]] = None
    
    # Alert configuration
    alert_config: Optional[AlertConfig] = None

    target_categories: List[str] = field(
        default_factory=lambda: [
            'person', 'people', 'human', 'man', 'woman', 'male', 'female']
    )

    # Minimum lifespan filter - only count track IDs that exist for at least this many frames
    min_track_lifespan_frames: int = 60  # 2 seconds at 30fps; 0 = disabled
    
    def validate(self) -> List[str]:
        """Validate people counting configuration."""
        errors = super().validate()
        
        if self.time_window_minutes <= 0:
            errors.append("time_window_minutes must be positive")
        
        if not self.person_categories:
            errors.append("person_categories cannot be empty")

        if self.min_track_lifespan_frames < 0:
            errors.append("min_track_lifespan_frames must be >= 0")
        
        # Validate nested configurations
        if self.zone_config:
            errors.extend(self.zone_config.validate())
        
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        
        return errors

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



class PeopleCountingInZoneUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {
        "person": "Person",
        "people": "People",
        "human": "Human",
        "man": "Man",
        "woman": "Woman",
        "male": "Male",
        "female": "Female"
    }

    def __init__(self):
        super().__init__("people_counting")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = 'people_counting'
        self.CASE_VERSION: Optional[str] = '1.4'
        self.target_categories = ['person'] #['person', 'people','human','man','woman','male','female']
        self.smoothing_tracker = None
        self.tracker = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._track_lifespans: Dict[Any, Tuple[int, int]] = {}  # track_id -> (first_frame, last_frame)
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

    def _simple_tracker_update(self, detections: list) -> list:
        """
        ====== PERFORMANCE: Lightweight tracker alternative ======
        Simple tracker using frame-local indexing.
        Much faster than AdvancedTracker - O(n) complexity.
        Does not persist track IDs across frames.
        Enable via config.enable_simple_tracker = True
        """
        for i, det in enumerate(detections):
            if det.get('track_id') is None:
                det['track_id'] = f"simple_{self._total_frame_counter}_{i}"
        return detections

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None,
                stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        processing_start = time.time()
        # print(f"\n{'='*60}")
        # print(f"[DEBUG PROCESS] Starting process() - frame counter: {self._total_frame_counter}")
        # print(f"[DEBUG PROCESS] Input data type: {type(data)}, length: {len(data) if isinstance(data, (list, dict)) else 'N/A'}")
        # if isinstance(data, list) and data:
        #     print(f"[DEBUG PROCESS] First input item: {data[0] if data else 'EMPTY'}")
        # print(f"{'='*60}")
        
        if not isinstance(config, PeopleCountingInZoneConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
        if context is None:
            context = ProcessingContext()

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = 0.1

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, 0.1)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data
            self.logger.debug("Did not apply confidence filtering since no threshold provided")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        if config.target_categories:
            processed_data = [d for d in processed_data if d.get('category') in self.target_categories]
            self.logger.debug("Applied category filtering")

        # Normalize track id field (some upstreams use different keys)
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

        # Tracker selection - uses AdvancedTracker with optimized defaults for count accuracy
        if getattr(config, 'enable_advanced_tracker', True):
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig
                if self.tracker is None:
                    # # TrackerConfig defaults are optimized for count accuracy
                    # # (lower thresholds for stable IDs, track recovery, state persistence)
                    # tracker_config = TrackerConfig()
                    # # Use stream_key as namespace for track ID isolation
                    # tracker_namespace = None
                    # if stream_info and stream_info.get('stream_key'):
                    #     tracker_namespace = str(hash(stream_info['stream_key']) % 1000000)
                    # self.tracker = AdvancedTracker(tracker_config, namespace=tracker_namespace)
                    # # Restore previous state for count continuity across restarts
                    # self.tracker.restore_state()
                    # self.logger.info(f"Initialized AdvancedTracker for People Counting (namespace={tracker_namespace})")
                    self.tracker = ByteTrackWrapper(
                        track_high_thresh=0.5,
                        track_low_thresh=0.1,
                        new_track_thresh=0.5,
                        track_buffer=150,
                        match_thresh=0.7,
                        frame_rate=30,
                    )
                processed_data = self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")
        elif getattr(config, 'enable_simple_tracker', False):
            processed_data = self._simple_tracker_update(processed_data)

        self._update_tracking_state(processed_data, config)
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        total_counts = self.get_total_counts()
        counting_summary['total_counts'] = total_counts

        alerts = self._check_alerts(counting_summary, frame_number, config)
        predictions = self._extract_predictions(processed_data)

        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics(counting_summary, alerts, config, stream_info, is_empty=True)
        summary_list = self._generate_summary(counting_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}
        agg_summary = {str(frame_number): {
            "incidents": incidents,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
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
        # Log the performance metrics using the module-level logger
        print(f"[PERF] F{self._total_frame_counter} | latency={processing_latency_ms:.1f}ms fps={processing_fps:.1f}" if processing_fps else f"[PERF] F{self._total_frame_counter} | latency={processing_latency_ms:.1f}ms")
        return result

    def _check_alerts(self, summary: dict, frame_number: Any, config: PeopleCountingInZoneConfig) -> List[Dict]:
        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            return ratio >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        total_counts_dict = summary.get("total_counts", {})
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        if hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                         getattr(config.alert_config, 'alert_value', ['JSON']))}
                    })
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                         getattr(config.alert_config, 'alert_value', ['JSON']))}
                    })
        return alerts

    def _generate_incidents(self, counting_summary: Dict, alerts: List, config: PeopleCountingInZoneConfig,
                           frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list

        if total_detections > 0:
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)
            if start_timestamp and self.current_incident_end_timestamp == 'N/A':
                self.current_incident_end_timestamp = 'Incident still active'
            elif start_timestamp and self.current_incident_end_timestamp == 'Incident still active':
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif self.current_incident_end_timestamp != 'Incident still active' and self.current_incident_end_timestamp != 'N/A':
                self.current_incident_end_timestamp = 'N/A'

            if config.alert_config and config.alert_config.get('count_thresholds', None):
                threshold = config.alert_config.get('count_thresholds', {}).get("all", 15)
                intensity = min(10.0, (total_detections / threshold) * 10)
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
                if total_detections > 30:
                    level = "critical"
                    intensity = 10.0
                    self._ascending_alert_list.append(3)
                elif total_detections > 25:
                    level = "significant"
                    intensity = 9.0
                    self._ascending_alert_list.append(2)
                elif total_detections > 15:
                    level = "medium"
                    intensity = 7.0
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    intensity = min(10.0, total_detections / 3.0)
                    self._ascending_alert_list.append(0)

            human_text_lines = [f"COUNTING INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and config.alert_config.get('alert_type', None):
                alert_settings.append({
                    "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                    "ascending": True,
                    "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                     getattr(config.alert_config, 'alert_value', ['JSON']))}
                })

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_number}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7}
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})
        return incidents

    def _generate_tracking_stats(self, counting_summary: Dict, alerts: List, config: PeopleCountingInZoneConfig,
                                frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        # Get new track IDs count (people who appeared for FIRST TIME - requires tracker)
        new_counts_dict = self.get_new_counts_this_frame()

        # Count detections by category
        raw_detections = counting_summary.get("detections", [])
        detection_count_by_category = {}
        for det in raw_detections:
            cat = det.get("category", "person")
            detection_count_by_category[cat] = detection_count_by_category.get(cat, 0) + 1

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        # current_counts: ALL people currently detected in frame
        current_counts = [{"category": cat, "count": count} for cat, count in detection_count_by_category.items()]
        # Fallback: if detection_count_by_category is empty but we have total_detections
        if not current_counts and total_detections > 0:
            current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items()]
        # current_new_counts: Only NEW people who appeared for the first time
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        # ONE concise stats summary line
        curr_total = sum(c.get('count', 0) for c in current_counts)
        new_total = sum(c.get('count', 0) for c in current_new_counts)
        total_total = sum(c.get('count', 0) for c in total_counts)
        print(f"[STATS] F{frame_number} | current={curr_total} new={new_total} total={total_total}")

        # DIAGNOSTIC: Warn if new > total (should never happen!)
        if new_total > total_total:
            print(f"[BUG_DETECTED] F{frame_number} | new({new_total}) > total({total_total})! "
                  f"new_counts_dict={new_counts_dict}, total_counts_dict={total_counts_dict}")

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
            if detection.get("masks"):
                segmentation = detection.get("masks", [])
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("segmentation"):
                segmentation = detection.get("segmentation")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("mask"):
                segmentation = detection.get("mask")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            else:
                detection_obj = self.create_detection_object(category, bbox)
            detections.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                 getattr(config.alert_config, 'alert_value', ['JSON']))}
            })

        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        for cat, count in detection_count_by_category.items():
            new_count = new_counts_dict.get(cat, 0)
            human_text_lines.append(f"\t- Total People in Frame: {count}")
            human_text_lines.append(f"\t- New People (just entered): {new_count}")
        human_text_lines.append("")
        # human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        # for cat, count in total_counts_dict.items():
        #     if count > 0:
        #         human_text_lines.append("")
        #         human_text_lines.append(f"\t- Total unique people count: {count}")
        # if alerts:
        #     for alert in alerts:
        #         human_text_lines.append(f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}")
        # else:
        #     human_text_lines.append("Alerts: None")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp
        )
        tracking_stat['target_categories'] = self.target_categories
        # current_new_counts: NEW track IDs that appeared for first time in this frame/aggregation
        tracking_stat['current_new_counts'] = current_new_counts
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(self, counting_summary: Dict, alerts: Any, config: PeopleCountingInZoneConfig,
                                    stream_info: Optional[Dict[str, Any]] = None, is_empty=False) -> List[Dict]:
        if is_empty:
            return []

    def _generate_summary(self, summary: dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: "+self.CASE_TYPE)
        lines.append("Application Version: "+self.CASE_VERSION)
        # if len(incidents) > 0:
        #     lines.append("Incidents: "+f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: "+f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: "+f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: "+"No Summary Data")

        return ["\n".join(lines)]

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        frame_track_ids = set()
        for det in detections:
            tid = det.get('track_id')
            if tid is not None:
                frame_track_ids.add(tid)
        total_track_ids = set()
        for s in getattr(self, '_per_category_total_track_ids', {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, '_total_frame_counter', 0)
        }

    def _filter_tracks_by_lifespan(self, min_frames: int) -> set:
        """Return set of track IDs with lifespan >= min_frames."""
        valid = set()
        for tid, (first, last) in self._track_lifespans.items():
            if last - first + 1 >= min_frames:
                valid.add(tid)
        return valid

    def _update_tracking_state(self, detections: list, config: Optional[PeopleCountingInZoneConfig] = None):
        # Initialize tracking sets if needed
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}

        min_lifespan = 0
        if config is not None:
            min_lifespan = getattr(config, 'min_track_lifespan_frames', 0)

        # Build current frame track IDs
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        missing_track_ids = 0
        for det in detections:
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat in self.target_categories:
                if track_id is not None:
                    self._current_frame_track_ids[cat].add(track_id)
                else:
                    missing_track_ids += 1

        # DIAGNOSTIC: Warn if detections are missing track_ids
        if missing_track_ids > 0:
            print(f"[WARN_TRACKING] F{self._total_frame_counter} | {missing_track_ids}/{len(detections)} detections missing track_id!")

        # Update lifespans for all track IDs in current frame
        all_current_ids = set()
        for ids in self._current_frame_track_ids.values():
            all_current_ids.update(ids)
        for tid in all_current_ids:
            if tid in self._track_lifespans:
                first_frame, _ = self._track_lifespans[tid]
                self._track_lifespans[tid] = (first_frame, self._total_frame_counter)
            else:
                self._track_lifespans[tid] = (self._total_frame_counter, self._total_frame_counter)

        if min_lifespan > 0:
            # Deferred counting: only count IDs that have reached the lifespan threshold
            valid_ids = self._filter_tracks_by_lifespan(min_lifespan)

            # NEW = valid IDs in current frame that are not yet in total (first time crossing threshold)
            self._new_track_ids_this_frame = {}
            for cat in self.target_categories:
                current_valid = self._current_frame_track_ids.get(cat, set()) & valid_ids
                already_counted = self._per_category_total_track_ids.get(cat, set())
                self._new_track_ids_this_frame[cat] = current_valid - already_counted

            # Update totals: add only newly valid IDs
            for cat in self.target_categories:
                self._per_category_total_track_ids.setdefault(cat, set()).update(
                    self._new_track_ids_this_frame[cat]
                )
        else:
            # Original behaviour when lifespan filter is disabled
            self._new_track_ids_this_frame = {
                cat: (self._current_frame_track_ids.get(cat, set()) - self._per_category_total_track_ids.get(cat, set()))
                for cat in self.target_categories
            }
            # Update totals with all current frame IDs
            for cat, ids in self._current_frame_track_ids.items():
                self._per_category_total_track_ids.setdefault(cat, set()).update(ids)

        # ONE concise log line per frame
        current_ids = sorted(list(self._current_frame_track_ids.get('person', set())))
        new_ids = sorted(list(self._new_track_ids_this_frame.get('person', set())))
        total_seen = len(self._per_category_total_track_ids.get('person', set()))
        print(f"[TRACK] F{self._total_frame_counter} | det={len(detections)} ids={current_ids} new={new_ids} total_seen={total_seen}")

        # Only log when NEW track IDs created (helpful for debugging)
        if any(len(ids) > 0 for ids in self._new_track_ids_this_frame.values()):
            print(f"[NEW_TRACK] F{self._total_frame_counter} | new_ids={new_ids} total_unique={total_seen}")

        # DIAGNOSTIC: Warn if total_seen grows too large relative to detections
        if total_seen > 100 and len(detections) > 0:
            ratio = total_seen / max(len(detections), 1)
            if ratio > 20:
                print(f"[WARN] F{self._total_frame_counter} | total_seen={total_seen} vs det={len(detections)} "
                      f"(ratio={ratio:.1f}x) - possible tracker instability or use case recreation")

        # DIAGNOSTIC: Check if new IDs exist but total is 0 (indicates bug)
        for cat in self.target_categories:
            new_count = len(self._new_track_ids_this_frame.get(cat, set()))
            total_count = len(self._per_category_total_track_ids.get(cat, set()))
            if new_count > 0 and total_count == 0:
                print(f"[BUG_IN_UPDATE] F{self._total_frame_counter} | cat={cat} new={new_count} but total=0! "
                      f"_current_frame_track_ids={self._current_frame_track_ids}")

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self):
        return {cat: len(ids) for cat, ids in getattr(self, '_per_category_total_track_ids', {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of NEW track IDs that appeared for the FIRST TIME EVER in this frame.

        This counts only track IDs that have never been seen before (not in total set).
        Re-entries (person leaves and comes back) are NOT counted as new.
        """
        return {cat: len(ids) for cat, ids in getattr(self, '_new_track_ids_this_frame', {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame (existing + new)."""
        return {cat: len(ids) for cat, ids in getattr(self, '_current_frame_track_ids', {}).items()}

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS.

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will be converted to datetime.
        2. A string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        The returned value will be in the format: YYYY:MM:DD HH:MM:SS (no milliseconds, no UTC suffix).

        Example
        -------
        >>> self._format_timestamp("2025-10-27-19:31:20.187574 UTC")
        '2025:10:27 19:31:20'
        """

        # Convert numeric timestamps to datetime first
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # Remove ' UTC' suffix if present
        timestamp_clean = timestamp.replace(' UTC', '').strip()

        # Remove milliseconds if present (everything after the last dot)
        if '.' in timestamp_clean:
            timestamp_clean = timestamp_clean.split('.')[0]

        # Parse the timestamp string and convert to desired format
        try:
            # Handle format: YYYY-MM-DD-HH:MM:SS
            if timestamp_clean.count('-') >= 2:
                # Replace first two dashes with colons for date part, third with space
                parts = timestamp_clean.split('-')
                if len(parts) >= 4:
                    # parts = ['2025', '10', '27', '19:31:20']
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            pass

        # If parsing fails, return the cleaned string as-is
        return timestamp_clean

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)

            stream_time_str = self._format_timestamp_for_video(start_time)
           

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
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
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
            # Prefer direct input_settings.stream_time if available and not NA
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                # Fallback to nested stream_info.stream_time used by current timestamp path
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except:
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
                    except:
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
                    except:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _count_categories(self, detections: list, config: PeopleCountingInZoneConfig) -> dict:
        counts = {}
        for det in detections:
            cat = det.get('category', 'unknown')
            counts[cat] = counts.get(cat, 0) + 1
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id")
                }
                for det in detections
            ]
        }

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {})
            }
            for det in detections
        ]

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        def _bbox_to_list(bbox):
            if bbox is None:
                return []
            if isinstance(bbox, list):
                return bbox[:4] if len(bbox) >= 4 else []
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

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
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

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()