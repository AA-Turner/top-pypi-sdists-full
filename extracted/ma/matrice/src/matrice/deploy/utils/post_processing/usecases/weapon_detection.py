from typing import Any, Dict, List, Optional
from dataclasses import asdict, dataclass, field
import time
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)
from ..core.config import BaseConfig, AlertConfig
class WeaponDetectionConfig:
    """Configuration for weapon detection use case."""
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.45
    weapon_categories: List[str] = field(default_factory=lambda: ['billete', 'bluntweapon', 'glass', 'gun', 'knife', 'monedero', 'pistol', 'smartphone', 'tarjeta'])
    target_weapon_categories: List[str] = field(default_factory=lambda: ['bluntweapon', 'glass', 'gun', 'knife', 'monedero', 'pistol', 'tarjeta'])
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "billete",
            1: "bluntweapon",
            2: "glass",
            3: "gun",
            4: "knife",
            5: "monedero",
            6: "pistol",
            7: "smartphone",
            8: "tarjeta"
        }
    )

class WeaponDetectionUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {
        "billete": "Billete",
        "bluntweapon": "Blunt Weapon",
        "glass": "Glass",
        "gun": "Gun",
        "knife": "Knife",
        "monedero": "Monedero",
        "pistol": "Pistol",
        "smartphone": "Smartphone",
        "tarjeta": "Tarjeta"
    }

    def __init__(self):
        super().__init__("weapon_detection")
        self.category = "security"
        self.CASE_TYPE: Optional[str] = 'weapon_detection'
        self.CASE_VERSION: Optional[str] = '1.0'
        self.target_categories = ['bluntweapon', 'glass', 'gun', 'knife', 'monedero', 'pistol', 'tarjeta']
        self.smoothing_tracker = None
        self.tracker = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = None

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None,
                stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        start_time = time.time()
        if not isinstance(config, WeaponDetectionConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
        if context is None:
            context = ProcessingContext()

        # Log input data
        self.logger.debug(f"Raw input data: {data}")

        # Extract detections from model_streams if necessary
        if isinstance(data, dict) and "model_streams" in data:
            data = data["model_streams"][0]["model_stream"]["model_outputs"][0]["detections"]
            self.logger.debug(f"Extracted detections from model_streams: {data}")

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold
        self.logger.info(f"Processing weapon detection with format: {input_format.value}")

        # Apply confidence filtering
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"After confidence filtering (threshold={config.confidence_threshold}): {processed_data}")
        else:
            processed_data = data
            self.logger.debug("No confidence filtering applied")

        # Apply category mapping
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug(f"After category mapping: {processed_data}")

        # Filter by target categories
        effective_targets = getattr(config, 'target_weapon_categories', self.target_categories) or self.target_categories
        processed_data = [d for d in processed_data if d.get('category') in effective_targets]
        self.logger.debug(f"After target category filtering (targets={effective_targets}): {processed_data}")

        # Log alerts for detected weapons
        for detection in processed_data:
            if detection.get('category') in effective_targets:
                self.logger.warning(f"ALERT: {detection.get('category')} detected at {self._get_current_timestamp_str(stream_info)}")

        # Apply smoothing
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold,
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)
            self.logger.debug(f"After bbox smoothing: {processed_data}")

        # Apply tracking
        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info("Initialized AdvancedTracker for Weapon Detection")
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Update tracking state
        self._update_tracking_state(processed_data)
        self.logger.debug(f"After updating tracking state: {processed_data}")
        self._total_frame_counter += 1

        # Extract frame information
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Calculate summaries
        counting_summary = self._count_categories(processed_data, config)
        self.logger.debug(f"Counting summary: {counting_summary}")
        counting_summary['total_counts'] = self.get_total_counts()
        alerts = self._check_alerts(counting_summary, frame_number, config)
        predictions = self._extract_predictions(processed_data)

        # Generate outputs
        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics(counting_summary, alerts, config, frame_number, stream_info, is_empty=True)
        summary_list = self._generate_summary(counting_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)

        # Build result
        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}
        agg_summary = {str(frame_number): {
            "incidents": incidents,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "human_text": summary
        }}

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context
        )
        self.logger.debug(f"Final result: {result}")
        return result

    def _count_categories(self, detections: List[Dict], config: WeaponDetectionConfig) -> Dict[str, Any]:
        """Count unique weapons per frame and attach detections."""
        unique_weapons = set()
        valid_detections = []
        tracks = {}
        
        # Group detections by track_id
        for det in detections:
            if not all(k in det for k in ['category', 'confidence', 'bounding_box']):
                self.logger.debug(f"Skipping detection due to missing fields: {det}")
                continue
            tid = det.get('track_id')
            if tid is None:
                tid = tuple(sorted(det.get('bounding_box', {}).items()))  # Fallback to bbox as key
            tracks.setdefault(tid, []).append(det)

        # Process each track
        for tid, dets in tracks.items():
            rep = dets[0]  # Use first detection as representative
            cat = rep.get('category', '')
            if cat not in self.target_categories:
                self.logger.debug(f"Skipping detection with non-target category: {cat}")
                continue
            bbox = rep.get('bounding_box')
            conf = rep.get('confidence')
            frame_id = rep.get('frame_id')
            unique_weapons.add(cat)  # Count unique weapon types
            valid_detections.append({
                "bounding_box": bbox,
                "category": cat,
                "confidence": conf,
                "track_id": rep.get('track_id'),
                "frame_id": frame_id,
                "masks": rep.get("masks", []),
            })

        counts = {"Weapon": len(unique_weapons)} if unique_weapons else {}
        return {
            "total_count": len(unique_weapons),
            "per_category_count": counts,
            "detections": valid_detections
        }

    def _generate_tracking_stats(self, counting_summary: Dict, alerts: List, config: WeaponDetectionConfig,
                                frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured tracking stats with frame-based keys."""
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        camera_info = self.get_camera_info_from_stream(stream_info)

        # Calculate counts for "Weapon" category and details
        weapon_count = sum(count for cat, count in per_category_count.items() if cat in self.target_categories and count > 0)
        cumulative_weapon_count = sum(count for cat, count in total_counts_dict.items() if cat in self.target_categories and count > 0)

        # Prepare current and total counts
        current_counts = [{"category": "Weapon", "count": weapon_count}] if weapon_count > 0 else []
        if weapon_count > 0:
            current_counts.append({
                "category": "Weapon Types",
                "details": [{"type": cat, "count": count} for cat, count in per_category_count.items() if count > 0 and cat in self.target_categories]
            })
        total_counts = [{"category": "Weapon", "count": cumulative_weapon_count}] if cumulative_weapon_count > 0 else []
        if cumulative_weapon_count > 0:
            total_counts.append({
                "category": "Weapon Types",
                "details": [{"type": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0 and cat in self.target_categories]
            })

        # Generate human-readable text
        human_text_lines = []
        human_text_lines.append(f"Tracking Statistics:")
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if total_detections > 0:
            category_counts = [f"{count} {self.CATEGORY_DISPLAY.get(cat, cat)}" for cat, count in per_category_count.items() if count > 0 and cat in self.target_categories]
            detection_text = f"{weapon_count} Weapon{'s' if weapon_count != 1 else ''} detected"
            human_text_lines.append(detection_text)
            # if category_counts:
            #     detection_text += f" ({', '.join(category_counts)})"
            # human_text_lines.append(f"\t- {detection_text}")
            # seen = set()
            # display_categories = []
            # for det in counting_summary.get("detections", []):
            #     track_id = det.get("track_id")
            #     cat = det.get("category")
            #     if not cat or track_id in seen or cat not in self.target_categories:
            #         continue
            #     seen.add(track_id)
            #     display_categories.append(self.CATEGORY_DISPLAY.get(cat, cat))
            # if display_categories:
            #     human_text_lines.append(f"\t- Weapon Types: {', '.join(display_categories)}")
        else:
            human_text_lines.append(f"\t- No weapons detected")

        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total Weapons Detected: {cumulative_weapon_count}")
        # if total_counts_dict:
        #     human_text_lines.append("\t- Unique Weapon Types:")
        #     for cat in sorted(set(cat for cat in total_counts_dict.keys() if cat in self.target_categories)):
        #         human_text_lines.append(f"\t\t- {self.CATEGORY_DISPLAY.get(cat, cat)}")

        # Process detections
        detections = []
        for detection in counting_summary.get("detections", []):
            cat = detection.get("category", "weapon")
            bbox = detection.get("bounding_box", {})
            if cat in self.target_categories:
                category = "Weapon"
                weapon_type = self.CATEGORY_DISPLAY.get(cat, cat)
                segmentation = detection.get("masks", detection.get("segmentation", detection.get("mask", [])))
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation, weapon_type=weapon_type)
                detections.append(detection_obj)
            else:
                category = self.CATEGORY_DISPLAY.get(cat, cat) if cat != "weapon" else cat
                segmentation = detection.get("masks", detection.get("segmentation", detection.get("mask", [])))
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
                detections.append(detection_obj)

        # Build alert settings
        alert_settings = []
        if config.alert_config:
            alert_cfg = config.alert_config
            alert_type = getattr(alert_cfg, 'alert_type', None) if not isinstance(alert_cfg, dict) else alert_cfg.get('alert_type')
            alert_value = getattr(alert_cfg, 'alert_value', None) if not isinstance(alert_cfg, dict) else alert_cfg.get('alert_value')
            count_thresholds = getattr(alert_cfg, 'count_thresholds', None) if not isinstance(alert_cfg, dict) else alert_cfg.get('count_thresholds')
            alert_type = alert_type if isinstance(alert_type, list) else (list(alert_type) if alert_type is not None else ['Default'])
            alert_value = alert_value if isinstance(alert_value, list) else (list(alert_value) if alert_value is not None else ['JSON'])
            alert_settings.append({
                "alert_type": alert_type,
                "incident_category": self.CASE_TYPE,
                "threshold_level": count_thresholds or {},
                "ascending": True,
                "settings": {t: v for t, v in zip(alert_type, alert_value)}
            })

        # Append alerts info to human text
        if alerts:
            human_text_lines.append(f"Alerts: {alerts[0].get('settings', {})} sent @ {current_timestamp}")
        else:
            human_text_lines.append("Alerts: None")

        human_text = "\n".join(human_text_lines)
        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]

        # Create tracking stats object
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
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _update_tracking_state(self, detections: List[Dict]):
        """Track unique track_ids per category."""
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def get_total_counts(self):
        """Return total unique weapons encountered so far."""
        total_counts = {}
        for cat in self._per_category_total_track_ids:
            if cat in self.target_categories:
                total_counts[cat] = len(self._per_category_total_track_ids[cat])
        return total_counts

    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        """Get detailed information about track IDs."""
        frame_track_ids = {det.get('track_id') for det in detections if det.get('track_id') is not None}
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

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes."""
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
        """Return a stable canonical ID for a raw tracker ID."""
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

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to exactly two decimal digits for milliseconds."""
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

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

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

    def _check_alerts(self, summary: Dict, frame_number: Any, config: WeaponDetectionConfig) -> List[Dict]:
        """Check if any alert thresholds are exceeded."""
        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            return increasing / (len(window) - 1) >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        total_counts_dict = summary.get("total_counts", {})
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        _alert_cfg = config.alert_config
        _thresholds = getattr(_alert_cfg, 'count_thresholds', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('count_thresholds')
        _types = getattr(_alert_cfg, 'alert_type', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_type')
        _values = getattr(_alert_cfg, 'alert_value', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_value')
        _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ['Default'])
        _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ['JSON'])
        if _thresholds:
            for category, threshold in _thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append({
                        "alert_type": _types,
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list),
                        "settings": {t: v for t, v in zip(_types, _values)}
                    })
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append({
                        "alert_type": _types,
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list),
                        "settings": {t: v for t, v in zip(_types, _values)}
                    })
        return alerts

    def _generate_incidents(self, counting_summary: Dict, alerts: List, config: WeaponDetectionConfig,
                           frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured incidents."""
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list

        if total_detections > 0:
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
            if start_timestamp and self.current_incident_end_timestamp == 'N/A':
                self.current_incident_end_timestamp = 'Incident still active'
            elif start_timestamp and self.current_incident_end_timestamp == 'Incident still active':
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif self.current_incident_end_timestamp != 'Incident still active' and self.current_incident_end_timestamp != 'N/A':
                self.current_incident_end_timestamp = 'N/A'

            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
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

            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config:
                _alert_cfg = config.alert_config
                _types = getattr(_alert_cfg, 'alert_type', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_type')
                _values = getattr(_alert_cfg, 'alert_value', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_value')
                _thresholds = getattr(_alert_cfg, 'count_thresholds', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('count_thresholds')
                _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ['Default'])
                _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ['JSON'])
                alert_settings.append({
                    "alert_type": _types,
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": _thresholds or {},
                    "ascending": True,
                    "settings": {t: v for t, v in zip(_types, _values)}
                })

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_key}",
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

    def _generate_summary(self, summary: Dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[Dict]:
        """Generate a human-readable summary."""
        lines = []
        lines.append(f"Application Name: {self.CASE_TYPE}")
        lines.append(f"Application Version: {self.CASE_VERSION}")
        if len(incidents) > 0:
            lines.append(f"Incidents: \n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append(f"Tracking Statistics: \t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append(f"Business Analytics: \t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: No Summary Data")

        return ["\n".join(lines)]

    def _extract_predictions(self, processed_data: List[Dict]) -> List[Dict]:
        """Extract predictions from processed data."""
        return processed_data