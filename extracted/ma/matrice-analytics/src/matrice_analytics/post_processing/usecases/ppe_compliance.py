import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile  # noqa: E402
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    bbox_smoothing,
    match_results_structure,
)


@dataclass
class PPEComplianceConfig(BaseConfig):
    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    # If None, bbox smoothing uses no_mask_threshold (legacy behavior).
    smoothing_confidence_threshold: Optional[float] = None

    # Violation thresholds
    no_hardhat_threshold: float = 0.91
    no_mask_threshold: float = 0.4
    no_safety_vest_threshold: float = 0.4

    violation_categories: List[str] = field(default_factory=lambda: ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"])
    # Accepted from deployment API; analytics use ANALYTICS_CATEGORIES in the use case.
    target_categories: List[str] = field(
        default_factory=lambda: [
            "Person",
            "Hardhat",
            "Mask",
            "Safety Vest",
            "NO-Hardhat",
            "NO-Mask",
            "NO-Safety Vest",
        ]
    )
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "Hardhat",
            1: "Mask",
            2: "NO-Hardhat",
            3: "NO-Mask",
            4: "NO-Safety Vest",
            5: "Person",
            6: "Safety Cone",
            7: "Safety Vest",
            8: "machinery",
            9: "vehicle",
        }
    )


class PPEComplianceUseCase(BaseProcessor):
    """PPE compliance detection use case with violation smoothing and alerting."""

    ANALYTICS_CATEGORIES = (
        "Person",
        "Hardhat",
        "Mask",
        "Safety Vest",
        "NO-Hardhat",
        "NO-Mask",
        "NO-Safety Vest",
    )
    PPE_CLASSES = ("Hardhat", "Mask", "Safety Vest")
    REQUIRED_PPE = ("Hardhat", "Safety Vest")
    CATEGORY_NORMALIZE = {
        "Person": "person",
        "Hardhat": "hardhat",
        "Mask": "mask",
        "Safety Vest": "safety_vest",
        "NO-Hardhat": "no_hardhat",
        "NO-Mask": "no_mask",
        "NO-Safety Vest": "no_safety_vest",
    }

    def get_camera_info_from_stream(self, stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract camera information from stream_info dict, matching mask_detection's approach.
        """
        if not stream_info:
            return {"camera_name": None, "camera_group": None, "location": None}
        input_settings = stream_info.get("input_settings", {})
        camera_name = input_settings.get("camera_name")
        camera_group = input_settings.get("camera_group")
        location = input_settings.get("location")
        return {
            "camera_name": camera_name,
            "camera_group": camera_group,
            "location": location,
        }

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Return a stable canonical ID for a raw tracker ID, merging fragmented tracks when IoU and temporal constraints indicate they represent the same physical object."""
        if not hasattr(self, "_track_aliases"):
            self._track_aliases = {}
            self._canonical_tracks = {}
            self._canonical_id_counter = 0
        if raw_id is None or bbox is None:
            return raw_id
        now = time.time()
        # Fast path – raw_id already mapped
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id
        # Attempt to merge with an existing canonical track (IoU + time window)
        best_iou = 0.0
        best_canonical = None
        for cid, info in self._canonical_tracks.items():
            last_bbox = info.get("last_bbox")
            last_update = info.get("last_update", 0)
            if last_bbox is not None and now - last_update < 2.0:
                iou = self._iou(bbox, last_bbox)
                if iou > 0.7 and iou > best_iou:
                    best_iou = iou
                    best_canonical = cid
        if best_canonical is not None:
            self._track_aliases[raw_id] = best_canonical
            info = self._canonical_tracks[best_canonical]
            info["last_bbox"] = bbox
            info["last_update"] = now
            info["raw_ids"].add(raw_id)
            return best_canonical
        # New canonical track
        canonical_id = f"ppe_{self._canonical_id_counter}"
        self._canonical_id_counter += 1
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        """
        Get detailed information about track IDs for PPE violations (per frame).
        """
        # Collect all track_ids in this frame
        frame_track_ids = set()
        for det in detections:
            tid = det.get("track_id")
            if tid is not None:
                frame_track_ids.add(tid)
        # Use persistent total set for unique counting
        total_track_ids = set()
        for s in getattr(self, "_violation_total_track_ids", {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, "_total_frame_counter", 0),
        }

    @staticmethod
    def _iou(bbox1, bbox2):
        """Compute IoU between two bboxes (dicts with xmin/ymin/xmax/ymax)."""
        x1 = max(bbox1["xmin"], bbox2["xmin"])
        y1 = max(bbox1["ymin"], bbox2["ymin"])
        x2 = min(bbox1["xmax"], bbox2["xmax"])
        y2 = min(bbox1["ymax"], bbox2["ymax"])
        inter_w = max(0, x2 - x1)
        inter_h = max(0, y2 - y1)
        inter_area = inter_w * inter_h
        area1 = (bbox1["xmax"] - bbox1["xmin"]) * (bbox1["ymax"] - bbox1["ymin"])
        area2 = (bbox2["xmax"] - bbox2["xmin"]) * (bbox2["ymax"] - bbox2["ymin"])
        union = area1 + area2 - inter_area
        if union == 0:
            return 0.0
        return inter_area / union

    @staticmethod
    def _deduplicate_violations(detections, iou_thresh=0.7):
        """Suppress duplicate/overlapping violations with same label and high IoU."""
        filtered = []
        used = [False] * len(detections)
        for i, det in enumerate(detections):
            if used[i]:
                continue
            group = [i]
            for j in range(i + 1, len(detections)):
                if used[j]:
                    continue
                if det.get("category") == detections[j].get("category"):
                    bbox1 = det.get("bounding_box")
                    bbox2 = detections[j].get("bounding_box")
                    if bbox1 and bbox2:
                        iou = PPEComplianceUseCase._iou(bbox1, bbox2)
                        if iou > iou_thresh:
                            used[j] = True
                            group.append(j)
            # Keep the highest confidence detection in the group
            best_idx = max(group, key=lambda idx: detections[idx].get("confidence", 0))
            filtered.append(detections[best_idx])
            used[best_idx] = True
        return filtered

    def _filter_by_detection_confidence(self, detections: list, config: PPEComplianceConfig) -> list:
        """
        Drop violation detections below max(per-class no_*_threshold, confidence_threshold).
        """
        cat_min = {
            "NO-Hardhat": config.no_hardhat_threshold,
            "NO-Mask": config.no_mask_threshold,
            "NO-Safety Vest": config.no_safety_vest_threshold,
        }
        out = []
        for det in detections:
            cat = det.get("category")
            conf = det.get("confidence")
            if cat not in self.violation_categories:
                out.append(det)
                continue
            if conf is None:
                out.append(det)
                continue
            need = float(cat_min.get(cat, 0.0))
            if config.confidence_threshold is not None:
                need = max(need, float(config.confidence_threshold))
            if float(conf) >= need:
                out.append(det)
        return out

    def _update_violation_tracking_state(self, detections: list):
        """
        Track unique violation track_ids per category for total count after tracking.
        Uses canonical ID merging to avoid duplicate counting when the tracker loses and reassigns IDs.
        """
        if not hasattr(self, "_violation_total_track_ids"):
            self._violation_total_track_ids = {cat: set() for cat in self.violation_categories}
        self._violation_current_frame_track_ids = {cat: set() for cat in self.violation_categories}
        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.violation_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id  # propagate canonical ID
            self._violation_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._violation_current_frame_track_ids[cat].add(canonical_id)

    def get_total_violation_counts(self):
        """
        Return total unique track_id count for each violation category.
        """
        return {cat: len(ids) for cat, ids in getattr(self, "_violation_total_track_ids", {}).items()}

    @classmethod
    def _normalize_category(cls, category: str) -> str:
        return cls.CATEGORY_NORMALIZE.get(category, str(category).lower().replace(" ", "_").replace("-", "_"))

    def _init_analytics_tracking_state(self) -> None:
        norm_cats = tuple(self._normalize_category(c) for c in self.ANALYTICS_CATEGORIES)
        if not hasattr(self, "_analytics_total_track_ids"):
            self._analytics_total_track_ids = {cat: set() for cat in norm_cats}
            self._analytics_frame_new = {cat: set() for cat in norm_cats}
            self._analytics_frame_current = {cat: set() for cat in norm_cats}

    def _update_analytics_tracking_state(self, detections: list) -> None:
        """Track unique IDs per analytics category for redis-agg rollups."""
        self._init_analytics_tracking_state()
        norm_cats = self._analytics_total_track_ids.keys()
        self._analytics_frame_new = {cat: set() for cat in norm_cats}
        self._analytics_frame_current = {cat: set() for cat in norm_cats}

        for det in detections:
            raw_cat = det.get("category")
            cat = self._normalize_category(raw_cat)
            if cat not in self._analytics_total_track_ids:
                continue
            raw_track_id = det.get("track_id")
            bbox = det.get("bounding_box", det.get("bbox"))
            # Small PPE parts (Hardhat/Mask) often have no track_id — still count
            # them with a synthetic id so total_counts are not stuck at 0.
            if raw_track_id is None:
                if not hasattr(self, "_untracked_analytics_counter"):
                    self._untracked_analytics_counter = 0
                self._untracked_analytics_counter += 1
                canonical_id = f"untracked-{cat}-{self._untracked_analytics_counter}"
            else:
                canonical_id = self._merge_or_register_track(raw_track_id, bbox)
                det["track_id"] = canonical_id
            self._analytics_frame_current[cat].add(canonical_id)
            if canonical_id not in self._analytics_total_track_ids[cat]:
                self._analytics_frame_new[cat].add(canonical_id)
            self._analytics_total_track_ids[cat].add(canonical_id)

    def _count_direct_violations(
        self,
        violation_dets: list,
        *,
        exclude_track_ids: Optional[set] = None,
    ) -> tuple:
        """Count direct NO-* detections (single-stage PPE model path)."""
        exclude = exclude_track_ids or set()
        seen = set()
        untracked = 0
        for det in violation_dets:
            tid = det.get("track_id")
            if tid is not None:
                if tid in exclude or tid in seen:
                    continue
                seen.add(tid)
            else:
                untracked += 1
        return len(seen) + untracked, seen

    def _compute_safety_metrics(self, detections: list) -> Dict[str, Any]:
        """Per-frame SAFETY metrics aligned with SafetyProcessor semantics."""
        persons = [d for d in detections if d.get("category") == "Person"]
        ppe_dets = [d for d in detections if d.get("category") in self.PPE_CLASSES]
        violation_dets = [d for d in detections if d.get("category") in self.violation_categories]

        total_persons = len(persons)
        ppe_items_by_person: Dict[Any, set] = {}
        for det in ppe_dets:
            tid = det.get("track_id")
            if tid is None:
                continue
            ppe_items_by_person.setdefault(tid, set()).add(det.get("category", ""))

        direct_violator_ids = {det.get("track_id") for det in violation_dets if det.get("track_id") is not None}
        person_tids = {p.get("track_id") for p in persons if p.get("track_id") is not None}

        compliant_count = 0
        violation_count = 0
        frame_violator_ids: set = set()

        for person in persons:
            tid = person.get("track_id")
            if tid is None:
                violation_count += 1
                continue
            if tid in direct_violator_ids:
                violation_count += 1
                frame_violator_ids.add(tid)
                continue
            worn = ppe_items_by_person.get(tid, set())
            if set(self.REQUIRED_PPE).issubset(worn):
                compliant_count += 1
            else:
                violation_count += 1
                frame_violator_ids.add(tid)

        if total_persons == 0:
            direct_count, direct_ids = self._count_direct_violations(violation_dets)
            violation_count = direct_count
            frame_violator_ids = direct_ids
        else:
            orphan_count, orphan_ids = self._count_direct_violations(violation_dets, exclude_track_ids=person_tids)
            violation_count += orphan_count
            frame_violator_ids |= orphan_ids

        compliance_pct = (compliant_count / total_persons * 100.0) if total_persons > 0 else 0.0

        ppe_counts = {item: 0 for item in self.PPE_CLASSES}
        for det in ppe_dets:
            cat = det.get("category", "")
            if cat in ppe_counts:
                ppe_counts[cat] += 1

        return {
            "total_persons": total_persons,
            "compliant_count": compliant_count,
            "violation_count": violation_count,
            "compliance_pct": compliance_pct,
            "hardhat_count": ppe_counts.get("Hardhat", 0),
            "safety_vest_count": ppe_counts.get("Safety Vest", 0),
            "mask_count": ppe_counts.get("Mask", 0),
            "frame_person_ids": list(person_tids),
            "frame_violator_ids": list(frame_violator_ids),
            "frame_hardhat_ids": list(self._analytics_frame_current.get("hardhat", set())),
            "frame_safety_vest_ids": list(self._analytics_frame_current.get("safety_vest", set())),
            "frame_mask_ids": list(self._analytics_frame_current.get("mask", set())),
        }

    def __init__(self):
        super().__init__("ppe_compliance")
        self.category = "ppe"
        self.CASE_TYPE: Optional[str] = "ppe_compliance"
        self.CASE_VERSION: Optional[str] = "1.0"
        # List of violation categories to track
        self.violation_categories = ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]
        # Initialize smoothing tracker
        self.smoothing_tracker = None
        # Initialize advanced tracker (will be created on first use)
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        # Initialize tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        # Set of current frame track_ids (updated per frame)
        self._current_frame_track_ids = set()
        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = None

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.s format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 1)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        """Get formatted current timestamp based on stream type."""
        if not stream_info:
            return "00:00:00.00"
        # If precision is requested, use frame-based time for video files
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                        "input_settings", {}
                    ).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                return stream_time_str
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                    "input_settings", {}
                ).get("original_fps", 30)
            stream_time_str = self._format_timestamp_for_video(start_time)
            return stream_time_str
        else:
            # For streams, use stream_time from stream_info
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
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return "00:00:00"
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            return "00:00:00"
        else:
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

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """
        Main entry point for PPE compliance detection post-processing.
        Applies category mapping, violation smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs in the new agg_summary format
        """
        start_time = time.time()
        if not isinstance(config, PPEComplianceConfig):
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.no_hardhat_threshold = config.no_hardhat_threshold

        # Map detection indices to category names (PPE COCO harness fixup included)
        from ...analytics.engine_session import map_detection_categories

        detections = data if isinstance(data, list) else (data or {}).get("detections", []) or []
        mapped_data = map_detection_categories(
            [dict(d) for d in detections],
            config.index_to_category,
            ppe_coco_fixup=True,
        )
        analytics_data = [d for d in mapped_data if d.get("category") in self.ANALYTICS_CATEGORIES]
        violation_data = [d for d in analytics_data if d.get("category") in self.violation_categories]
        non_violation_data = [d for d in analytics_data if d.get("category") not in self.violation_categories]
        violation_data = self._filter_by_detection_confidence(violation_data, config)

        # Apply bbox smoothing to violation detections only
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                sm_conf = config.smoothing_confidence_threshold
                if sm_conf is None:
                    sm_conf = config.no_mask_threshold
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=sm_conf,
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True,
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            violation_data = bbox_smoothing(violation_data, self.smoothing_tracker.config, self.smoothing_tracker)

        processed_data = non_violation_data + violation_data

        # Advanced tracking (BYTETracker-like)
        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    config, stream_info, profile=TrackerProfile.DEFAULT
                )
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        self._update_violation_tracking_state(violation_data)
        self._update_analytics_tracking_state(processed_data)
        self._total_frame_counter += 1

        # Frame number logic (not chunkwise, just per call)
        frame_number = self._total_frame_counter

        # Compute summaries and alerts — counts/boxes include all analytics cats
        # (Person/Hardhat/Mask/Vest + NO-*), not violations-only (fixes empty
        # Hardhat/Person boxes when only NO-Mask was drawn).
        counting_summary = self._count_categories(processed_data, config)
        safety_metrics = self._compute_safety_metrics(processed_data)
        counting_summary["safety_metrics"] = safety_metrics
        total_violation_counts = self.get_total_violation_counts()
        counting_summary["total_violation_counts"] = total_violation_counts
        insights = self._generate_insights(counting_summary, config)
        alerts = self._check_alerts(counting_summary, config)
        predictions = self._extract_predictions(processed_data)
        summary = self._generate_summary(counting_summary, alerts)

        # Generate new-format output (agg_summary)
        incidents = self._generate_events(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats = self._generate_tracking_stats(
            counting_summary, insights, summary, config, frame_number, stream_info
        )
        business_analytics = {}
        app_name = "PPE Compliance"
        app_version = "1.2"
        agg_human_text = {
            "Application Name": app_name,
            "Application Version": app_version,
            "Incidents:": incidents.get("human_text", ""),
            "Tracking Statistics:": tracking_stats.get("human_text", ""),
        }
        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": agg_human_text,
            }
        }

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )
        result.summary = summary
        result.insights = insights
        result.predictions = predictions
        self._debug_elapsed_since(start_time)
        return result

    def reset_tracker(self) -> None:
        """
        Reset the advanced tracker instance.

        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")

    def reset_violation_tracking(self) -> None:
        """
        Reset violation tracking state (total counts, track IDs, etc.).

        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        self._violation_total_track_ids = {cat: set() for cat in self.violation_categories}
        self._analytics_total_track_ids = {self._normalize_category(cat): set() for cat in self.ANALYTICS_CATEGORIES}
        self._analytics_frame_new = {self._normalize_category(cat): set() for cat in self.ANALYTICS_CATEGORIES}
        self._analytics_frame_current = {self._normalize_category(cat): set() for cat in self.ANALYTICS_CATEGORIES}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        # Also reset canonical track merging state
        self._track_aliases = {}
        self._canonical_tracks = {}
        self._canonical_id_counter = 0
        self.logger.info("PPE violation tracking state reset")

    def reset_all_tracking(self) -> None:
        """
        Reset both advanced tracker and violation tracking state.
        """
        self.reset_tracker()
        self.reset_violation_tracking()
        self.logger.info("All PPE tracking state reset")

    def _generate_events(
        self,
        counting_summary: Dict,
        alerts: List,
        _config: PPEComplianceConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        _ = (_config,)
        total_violations = counting_summary.get("total_count", 0)
        severity = "info" if total_violations > 0 else "none"
        human_text = f"INCIDENTS DETECTED @ :\n\tSeverity Level: ('ppe_compliance', '{severity}')"
        incident = {
            "incident_id": f"ppe_compliance_{frame_number}",
            "incident_type": "ppe_compliance",
            "severity_level": severity,
            "human_text": human_text,
            "start_time": "00:00:00",
            "end_time": "00:00:00",
            "camera_info": self.get_camera_info_from_stream(stream_info),
            "level_settings": {"low": 1, "medium": 3, "significant": 4, "critical": 7},
            "alerts": alerts,
            "alert_settings": [],
        }
        return incident

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        _insights: List[str],
        _summary: str,
        _config: PPEComplianceConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        _ = (_config, _frame_number, _insights, _summary)
        total_violations = counting_summary.get("total_count", 0)
        per_cat = counting_summary.get("per_category_count", {})
        cumulative = counting_summary.get("total_violation_counts", {})
        cumulative_total = sum(cumulative.values()) if cumulative else 0
        safety_metrics = counting_summary.get("safety_metrics", {})
        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)
        self._debug_stream_timing("start_timestamp", start_timestamp)
        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if total_violations > 0:
            human_text_lines.append(f"\t- PPE Violations Detected: {total_violations}")
            for cat in ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]:
                count = per_cat.get(cat, 0)
                if count > 0:
                    label = self.CATEGORY_DISPLAY.get(cat, cat).replace(" Violations", "")
                    human_text_lines.append(f"\t\t- {label}: {count}")
        else:
            human_text_lines.append("\t- No PPE violations detected")
        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total PPE Violations Detected: {cumulative_total}")
        for cat in ["NO-Hardhat", "NO-Mask", "NO-Safety Vest"]:
            count = cumulative.get(cat, 0)
            if count > 0:
                label = self.CATEGORY_DISPLAY.get(cat, cat).replace(" Violations", "")
                human_text_lines.append(f"\t\t- {label}: {count}")
        human_text = "\n".join(human_text_lines)

        norm_cats = [self._normalize_category(c) for c in self.ANALYTICS_CATEGORIES]
        current_counts = []
        current_new_counts = []
        total_counts = []
        total_current_counts = []
        for norm_cat, raw_cat in zip(norm_cats, self.ANALYTICS_CATEGORIES):
            frame_current = len(self._analytics_frame_current.get(norm_cat, set()))
            frame_new = len(self._analytics_frame_new.get(norm_cat, set()))
            cumulative_unique = len(self._analytics_total_track_ids.get(norm_cat, set()))
            if frame_current > 0:
                current_counts.append({"category": norm_cat, "count": frame_current})
            current_new_counts.append({"category": norm_cat, "count": frame_new})
            total_counts.append({"category": norm_cat, "count": cumulative_unique})
            total_current_counts.append({"category": norm_cat, "count": frame_current})

        tracking_stat = {
            "input_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC"),
            "reset_timestamp": "00:00:00",
            "camera_info": self.get_camera_info_from_stream(stream_info),
            "total_counts": total_counts,
            "current_counts": current_counts,
            "current_new_counts": current_new_counts,
            "total_current_counts": total_current_counts,
            "safety_analytics": safety_metrics,
            "detections": counting_summary.get("detections", []),
            "alerts": [],
            "alert_settings": [],
            "reset_settings": [
                {
                    "interval_type": "daily",
                    "reset_time": {"value": 9, "time_unit": "hour"},
                }
            ],
            "human_text": human_text,
        }
        return tracking_stat

    def _count_categories(self, detections: list, _config: PPEComplianceConfig) -> dict:
        """
        Count the number of detections per category and return a summary dict.
        The detections list is expected to have 'track_id' (from tracker), 'category', 'bounding_box', etc.
        Output structure will include 'track_id' for each detection as per AdvancedTracker output.
        """
        _ = (_config,)
        counts = {}
        for det in detections:
            cat = det.get("category", "unknown")
            if cat in self.ANALYTICS_CATEGORIES:
                counts[cat] = counts.get(cat, 0) + 1
        # Publish boxes for all analytics PPE classes (not violations-only).
        filtered_detections = [
            {
                "bounding_box": det.get("bounding_box"),
                "category": det.get("category"),
                "confidence": det.get("confidence"),
                "track_id": det.get("track_id"),
                "frame_id": det.get("frame_id"),
            }
            for det in detections
            if det.get("category") in self.ANALYTICS_CATEGORIES
        ]
        violation_counts = {cat: counts.get(cat, 0) for cat in self.violation_categories if counts.get(cat, 0) > 0}
        return {
            "total_count": sum(violation_counts.values()),
            "per_category_count": violation_counts,
            "all_category_count": counts,
            "detections": filtered_detections,
        }

    # Human-friendly display names for violation categories
    CATEGORY_DISPLAY = {
        "NO-Hardhat": "No Hardhat Violations",
        "NO-Mask": "No Mask Violations",
        "NO-Safety Vest": "No Safety Vest Violations",
    }

    def _generate_insights(self, summary: dict, _config: PPEComplianceConfig) -> List[str]:
        """
        Generate human-readable insights for each violation category.
        """
        _ = (_config,)
        insights = []
        per_cat = summary.get("per_category_count", {})
        for cat, count in per_cat.items():
            display = self.CATEGORY_DISPLAY.get(cat, cat)
            insights.append(f"{display}:{count}")
        return insights

    def _check_alerts(self, summary: dict, config: PPEComplianceConfig) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """
        alerts = []
        if not config.alert_config:
            return alerts
        total = summary.get("total_count", 0)
        if config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total >= threshold:
                    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC")
                    alert_description = f"PPE violation count ({total}) exceeds threshold ({threshold})"
                    alerts.append(
                        {
                            "type": "count_threshold",
                            "severity": "warning",
                            "message": alert_description,
                            "category": category,
                            "current_count": total,
                            "threshold": threshold,
                            "human_text": f"Time: {timestamp}\n{alert_description}",
                        }
                    )
        return alerts

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        """
        Extract prediction details for output (category, confidence, bounding box).
        """
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            for det in detections
        ]

    def _generate_summary(self, summary: dict, alerts: List) -> str:
        """
        Generate a human_text string for the result, including per-category insights if available.
        Adds a tab before each violation label for better formatting.
        Also always includes the cumulative violation count so far.
        """
        total = summary.get("total_count", 0)
        per_cat = summary.get("per_category_count", {})
        cumulative = summary.get("total_violation_counts", {})
        cumulative_total = sum(cumulative.values()) if cumulative else 0
        lines = []
        if total > 0:
            lines.append(f"{total} PPE violation(s) detected")
            if per_cat:
                lines.append("violations:")
                for cat, count in per_cat.items():
                    display = self.CATEGORY_DISPLAY.get(cat, cat)
                    label = (
                        display.replace(" Violations", "")
                        .replace("No ", "No ")
                        .replace("Safety Vest", "safety vest")
                        .replace("Mask", "mask")
                        .replace("Hardhat", "hardhat")
                    )
                    if count == 1:
                        lines.append(f"\t{label}")
                    else:
                        lines.append(f"\t{label}:{count}")
        else:
            lines.append("No PPE violation detected")
        lines.append(f"Total PPE violations detected: {cumulative_total}")
        if alerts:
            lines.append(f"{len(alerts)} alert(s)")
        return "\n".join(lines)
