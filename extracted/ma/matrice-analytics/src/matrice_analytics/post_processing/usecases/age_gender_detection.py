import copy
import logging
import math
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import numpy as np

from matrice_analytics.post_processing.core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from matrice_analytics.post_processing.core.config import AlertConfig, BaseConfig
from matrice_analytics.post_processing.Trackers import ConfigDrivenTracker, TrackerProfile
from matrice_analytics.post_processing.utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    bbox_smoothing,
    filter_by_confidence,
    match_results_structure,
)

_logger = logging.getLogger(__name__)


def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.

    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name

    Returns:
        Results with mapped category names
    """

    def map_detection(detection: Dict[str, Any], index_to_category: Dict[str, str]) -> Dict[str, Any]:
        """Map a single detection."""
        detection = detection.copy()
        category_id = str(detection.get("class_id", detection.get("class_id")))
        index_to_category = {str(k): str(v) for k, v in index_to_category.items()}
        if category_id in index_to_category:
            detection["category"] = index_to_category[category_id]
            detection["class_id"] = category_id
        return detection

    if isinstance(results, list):
        # Detection format
        return [map_detection(r, index_to_category) for r in results]

    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "category" in results or "class_id" in results:
            return map_detection(results, index_to_category)

        # Frame-based format
        mapped_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                mapped_results[frame_id] = [map_detection(d, index_to_category) for d in detections]
            else:
                mapped_results[frame_id] = detections

        return mapped_results

    return results


# ---------------------------------------------------------------------------
# Detection + classification flow: the classifier node decodes the head(s), so each detection
# carries the winning gender label / top_k plus an additive ``heads`` map (``heads['gender']``
# classification, ``heads['age']`` regression). These helpers convert that record -- or a raw
# ``predictor_output`` vector -- into the ``{gender, gender_conf, age}`` attributes this usecase
# aggregates. No in-analytics model inference is performed.
#
# TODO: gender_detection / age_detection / face_emotion decode an equivalent per-detection record;
# this logic should later be lifted into one shared multi-head decoder they all reuse.
# ---------------------------------------------------------------------------

MIN_AGE = 1
MAX_AGE = 95
AVG_AGE = 48


def _predictor_output_to_attributes(predictor_output: List[float]) -> Dict[str, Any]:
    """Convert a raw ``predictor_output`` [male_logit, female_logit, age_norm] to an attributes dict."""
    if not predictor_output or len(predictor_output) < 3:
        return {}
    gender_logits = predictor_output[:2]
    gender_id = int(max(range(len(gender_logits)), key=lambda i: gender_logits[i]))
    gender = "Female" if gender_id == 1 else "Male"

    logit0, logit1 = float(gender_logits[0]), float(gender_logits[1])
    exp0, exp1 = math.exp(logit0), math.exp(logit1)
    p0 = exp0 / (exp0 + exp1) if (exp0 + exp1) > 0 else 0.5
    p1 = 1.0 - p0
    final_gender_conf = round(max(p0, p1), 4)

    age_norm = float(predictor_output[2])
    age = age_norm * (MAX_AGE - MIN_AGE) + AVG_AGE
    age = int(round(min(MAX_AGE, max(MIN_AGE, age))))

    return {"age": age, "gender": gender, "gender_conf": final_gender_conf}


def _winning_top_k(top_k: Any) -> Optional[Dict[str, Any]]:
    """Return the highest-confidence entry of a ``top_k`` list ([{label, confidence}, ...]), or None."""
    if not isinstance(top_k, list):
        return None
    best: Optional[Dict[str, Any]] = None
    best_conf = -1.0
    for entry in top_k:
        if not isinstance(entry, dict) or "label" not in entry:
            continue
        conf = entry.get("confidence")
        conf = float(conf) if isinstance(conf, (int, float)) else 0.0
        if conf > best_conf:
            best, best_conf = entry, conf
    return best


def _apply_denorm(value: float, denorm: Optional[Dict[str, Any]]) -> int:
    """Recover a real-unit scalar from a normalized regression value.

    With an inline ``denorm`` descriptor: ``real = value * scale + offset``, clamped to
    ``[clamp_min, clamp_max]`` (bounds optional). Absent ``denorm``, fall back to this module's age
    convention -- identical math to the raw predictor_output age handling.
    """
    if isinstance(denorm, dict):
        real = value * float(denorm.get("scale", 1.0)) + float(denorm.get("offset", 0.0))
        clamp_max = denorm.get("clamp_max")
        clamp_min = denorm.get("clamp_min")
        if clamp_max is not None:
            real = min(float(clamp_max), real)
        if clamp_min is not None:
            real = max(float(clamp_min), real)
        return int(round(real))
    real = value * (MAX_AGE - MIN_AGE) + AVG_AGE
    return int(round(min(MAX_AGE, max(MIN_AGE, real))))


def _classification_record_to_attributes(det: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a decoded multi-head enrichment record into a ``{gender, gender_conf, age}`` dict.

    The primary (gender) head is read from ``heads['gender']`` when present, else the flat
    ``label`` / ``class_confidence`` / ``top_k`` fields that mirror it; the age regression head
    (``heads['age']``) is de-normalized via its inline ``Denorm`` (or this module's convention).
    """
    heads = det.get("heads")
    heads = heads if isinstance(heads, dict) else {}

    gender_head = heads.get("gender") if isinstance(heads.get("gender"), dict) else None
    gender: Any = None
    gender_conf: Any = None
    if gender_head is not None:
        gender = gender_head.get("label")
        gender_conf = gender_head.get("confidence")
        if not gender:
            win = _winning_top_k(gender_head.get("top_k"))
            if win is not None:
                gender, gender_conf = win.get("label"), win.get("confidence")
    if not gender:
        gender = det.get("label")
        gender_conf = det.get("class_confidence", gender_conf)
    if not gender:
        win = _winning_top_k(det.get("top_k"))
        if win is not None:
            gender, gender_conf = win.get("label"), win.get("confidence")
    if not gender:
        return {}

    attributes: Dict[str, Any] = {"gender": gender}
    if gender_conf is not None:
        attributes["gender_conf"] = round(float(gender_conf), 4)

    age_head = heads.get("age") if isinstance(heads.get("age"), dict) else None
    if age_head is not None and age_head.get("value") is not None:
        attributes["age"] = _apply_denorm(float(age_head["value"]), age_head.get("denorm"))

    return attributes


def _is_classification_record(det: Dict[str, Any]) -> bool:
    """True when a detection carries decoded classification fields (the enrichment flow)."""
    return any(key in det for key in ("heads", "top_k", "class_confidence", "label"))


def _normalize_predict_output(data: Any) -> Any:
    """Populate ``det['attributes']`` = {gender, gender_conf, age} from the decoded classification
    record (``heads`` / flat ``label`` + ``top_k``) or a raw ``predictor_output`` vector, for both the
    ``{'detections': [...]}`` and plain-list shapes."""

    def _fill(det: Dict[str, Any]) -> None:
        if "predictor_output" in det:
            det["attributes"] = _predictor_output_to_attributes(det["predictor_output"])
        elif _is_classification_record(det):
            det["attributes"] = _classification_record_to_attributes(det)

    if isinstance(data, dict) and "detections" in data:
        for det in data["detections"]:
            if isinstance(det, dict):
                _fill(det)
        return data
    if isinstance(data, list):
        for det in data:
            if isinstance(det, dict):
                _fill(det)
        return data
    return data


@dataclass
class AgeGenderConfig(BaseConfig):
    """Configuration for age and gender detection use case in age and gender detection."""

    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.2
    frame_skip: int = 1
    fps: Optional[float] = None
    bbox_format: str = "auto"
    # The tracked category IS the gender decoded from the classifier's gender head (Male/Female),
    # mirroring gender_detection; age rides along as a de-normed attribute in the detection label.
    usecase_categories: List[str] = field(default_factory=lambda: ["Male", "Female"])
    target_categories: List[str] = field(default_factory=lambda: ["Male", "Female"])
    alert_config: Optional[AlertConfig] = None
    # Consumed by the classifier (enrichment) node for its gender-head labels; the analytics node reads
    # the already-decoded label off the record, so this is carried for config-shape parity only.
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "Male", 1: "Female"})
    # The platform stamps this on every use_case_config alongside enable_tracking/enable_analytics;
    # accept it here as a no-op so the generic create_config(**kwargs) path does not raise.
    enable_unique_counting: bool = True

    def validate(self) -> List[str]:
        """Validate configuration parameters."""
        errors = super().validate()
        if self.confidence_threshold < 0 or self.confidence_threshold > 1:
            errors.append("confidence_threshold must be between 0 and 1")
        if self.frame_skip <= 0:
            errors.append("frame_skip must be positive")
        if self.bbox_format not in ["auto", "xmin_ymin_xmax_ymax", "x_y_width_height"]:
            errors.append("bbox_format must be one of: auto, xmin_ymin_xmax_ymax, x_y_width_height")
        if self.smoothing_window_size <= 0:
            errors.append("smoothing_window_size must be positive")
        if self.smoothing_cooldown_frames < 0:
            errors.append("smoothing_cooldown_frames cannot be negative")
        if self.smoothing_confidence_range_factor <= 0:
            errors.append("smoothing_confidence_range_factor must be positive")
        return errors


class AgeGenderUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("age_gender_detection")
        self.category = "age_gender_detection"
        # The tracked/counted category IS the gender (Male/Female), decoded from the classifier's
        # gender head -- mirrors gender_detection. Age rides along as a de-normed attribute and is
        # rendered into the per-detection label ("<gender>, <age>"). The deprecated "FACE" category
        # path is gone: age/gender come from the multi-head record, not from index->category mapping.
        self.target_categories = ["Male", "Female"]
        self.CASE_TYPE: Optional[str] = "age_gender_detection"
        self.CASE_VERSION: Optional[str] = "1.3"
        self.smoothing_tracker = None
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.all_track_data: List[str] = []

        self.start_timer = None
        self.age: Dict[str:Any] = {}
        self.gender: Dict[str:Any] = {}
        # self.reset_timer = "2025-08-19-04:22:47.187574 UTC"

    def reset_tracker(self) -> None:
        """Reset the advanced tracker instance."""
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")

    def reset_plate_tracking(self) -> None:
        """Reset plate tracking state."""
        self._seen_plate_texts = set()
        # CHANGE: Reset _tracked_plate_texts
        self._tracked_plate_texts = {}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._text_history = {}
        self._unique_plate_texts = {}
        self.logger.info("Plate tracking state reset")

    def reset_all_tracking(self) -> None:
        """Reset both advanced tracker and plate tracking state."""
        self.reset_tracker()
        self.reset_plate_tracking()
        self.logger.info("All plate tracking state reset")

    def _attributes_to_age_gender(self, detections):
        """Accumulate per-track age/gender history from detections that already carry decoded
        classification attributes (the detection + classification flow).

        Age/gender are decoded upstream by the classifier node and normalized onto
        ``det['attributes']`` by ``_normalize_predict_output``; the raw frame is never needed here.
        Returns the same ``{"Age Data": ..., "Gender Data": ...}`` structure the downstream
        aggregation (``_count_categories``) consumes, so nothing downstream changes.
        """
        for det in detections:
            attributes = det.get("attributes") or {}
            gender = attributes.get("gender")
            age = attributes.get("age")
            track_id = det.get("track_id")
            if not track_id:
                continue
            track_id = str(track_id)
            if gender is not None:
                self.gender.setdefault(track_id, []).append(gender)
            if age is not None:
                self.age.setdefault(track_id, []).append(age)
        return {"Age Data": self.age, "Gender Data": self.gender}

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        try:
            if context is None:
                context = ProcessingContext()

            if not isinstance(config, AgeGenderConfig):
                return self.create_error_result(
                    "Invalid configuration type for age gender detection",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if isinstance(getattr(config, "alert_config", None), dict):
                try:
                    config.alert_config = AlertConfig(**config.alert_config)  # type: ignore[arg-type]
                except Exception:
                    # Non-fatal: exception ignored here; execution continues per surrounding logic.
                    pass

            # Age/gender are decoded upstream by the classifier node and delivered on each detection
            # (heads / flat label+top_k, or a raw predictor_output vector) -- normalize onto
            # det["attributes"]. No in-analytics model inference or raw frame bytes are needed.
            data = _normalize_predict_output(data)

            # Unwrap the predict-output envelope ({"detections": [...]}) to a flat list of detections.
            if isinstance(data, dict) and "detections" in data:
                data = data["detections"]
            if not isinstance(data, list):
                data = [data] if data is not None else []

            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold

            self.logger.info(f"Processing age gender detection with format: {input_format.value}")

            # Step 1: Apply confidence filtering
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")

            # Step 2: Derive the tracked category from the decoded GENDER head (Male/Female) and attach
            # the dynamically de-normed AGE (years). This mirrors gender_detection's new-flow path:
            # the gender label comes from det["attributes"] (built from heads["gender"] upstream), NOT
            # from an index->category map. ``index_to_category`` in the deploy config is consumed by the
            # classifier node for its gender-head labels; the analytics node reads the decoded label.
            gender_processed = []
            for d in processed_data:
                if not isinstance(d, dict):
                    continue
                attrs = d.get("attributes") or {}
                gender = attrs.get("gender")
                if not gender:
                    continue
                gender = str(gender).capitalize()  # MALE/male -> Male, FEMALE/female -> Female
                if gender not in self.target_categories:
                    continue
                d["category"] = gender
                age = attrs.get("age")
                if age is not None:
                    d["age"] = int(age)  # already de-normed via heads["age"].denorm in _apply_denorm
                gender_processed.append(d)
            processed_data = gender_processed
            self.logger.info(
                f"[POST] frame={self._total_frame_counter} raw={len(data)} age_gender_valid={len(processed_data)}"
            )

            raw_processed_data = [copy.deepcopy(det) for det in processed_data]
            # Step 4: Apply bounding box smoothing if enabled
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
                processed_data = bbox_smoothing(
                    processed_data,
                    self.smoothing_tracker.config,
                    self.smoothing_tracker,
                )

            # Step 5: Apply advanced tracking
            try:
                if self.tracker is None:
                    self.tracker = self._tracker_seam.get_shared_tracker(
                        config, stream_info, profile=TrackerProfile.DEFAULT
                    )
                processed_data = self.tracker.update(processed_data)
            except Exception as err:
                self.logger.warning(f"AdvancedTracker failed: {err}")
            # Step 6: Update tracking state
            self._update_tracking_state(processed_data)
            # Step 7: Attach masks to detections
            processed_data = self._attach_masks_to_detections(processed_data, raw_processed_data)

            # Step 10: Update frame counter
            self._total_frame_counter += 1

            # Step 11: Extract frame information
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame

            # Step 12: Calculate summaries

            det = self._attributes_to_age_gender(processed_data)
            counting_summary = self._count_categories(processed_data, config, det)
            counting_summary["total_counts"] = self.get_total_counts()
            self.logger.debug(
                "Counting summary ready: total_count=%s detection_rows=%s",
                counting_summary.get("total_count"),
                len(counting_summary.get("detections", [])),
            )

            # Step 13: Generate alerts and summaries
            alerts = self._check_alerts(counting_summary, frame_number, config)
            incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
            tracking_stats_list = self._generate_tracking_stats(
                counting_summary, alerts, config, frame_number, stream_info
            )
            business_analytics_list = []
            summary_list = self._generate_summary(
                counting_summary,
                incidents_list,
                tracking_stats_list,
                business_analytics_list,
                alerts,
            )
            # Step 14: Build result
            incidents = incidents_list[0] if incidents_list else {}
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
            business_analytics = business_analytics_list[0] if business_analytics_list else {}
            summary = summary_list[0] if summary_list else {}
            # Mirror the per-bbox detections (gender + de-normed age label) into the incident too, so
            # both agg_summary.<frame>.tracking_stats.detections[] and .incidents.detections[] carry them.
            if isinstance(incidents, dict) and incidents and isinstance(tracking_stats, dict):
                incidents["detections"] = tracking_stats.get("detections", [])
            agg_summary = {
                str(frame_number): {
                    "incidents": incidents,
                    "tracking_stats": tracking_stats,
                    "business_analytics": business_analytics,
                    "alerts": alerts,
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
            self.logger.debug(
                "Frame perf: latency_ms=%.2f fps=%s frame_counter=%s",
                processing_latency_ms,
                f"{processing_fps:.2f}" if processing_fps is not None else "n/a",
                self._total_frame_counter,
            )

            return result

        except Exception as err:
            self.logger.error(f"Age and Gender Detection failed: {str(err)}", exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(err),
                type(err).__name__,
                usecase=self.name,
                category=self.category,
                context=context,
            )

    def _get_frame_detections(self, data: Any, frame_key: str) -> List[Dict[str, Any]]:
        """Extract detections for a specific frame from data."""
        if isinstance(data, dict):
            return data.get(frame_key, [])
        elif isinstance(data, list):
            return data
        else:
            return []

    def _count_categories(self, detections: List[Dict], _config: AgeGenderConfig, data) -> Dict[str, Any]:
        """Count unique licence-plate texts per frame and attach detections."""
        _ = (_config,)
        total_count = set()
        valid_detections: List[Dict[str, Any]] = []
        for det in detections:
            if not all(k in det for k in ["category", "confidence", "bounding_box"]):
                continue
            cat = det.get("category", "Person")
            track_id = det["track_id"]
            total_count.add(det["track_id"])

            if track_id not in self.all_track_data:
                self.all_track_data.append(track_id)

            counts = {"Person": len(total_count)} if total_count else {}

            valid_detections.append(
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": cat,
                    "gender": cat,
                    "age": det.get("age", (det.get("attributes") or {}).get("age")),
                    "confidence": det.get("confidence"),
                    "class_id": det.get("class_id"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    "masks": det.get("masks", []),
                }
            )

        # Case 1: if data is a single dict
        if isinstance(data, dict):
            cats = [data]  # wrap in list so loop works
        # Case 2: if data is already a list of dicts
        elif isinstance(data, list):
            cats = data
        else:
            raise TypeError(f"Unexpected type for data: {type(data)}")

        results = []
        latest_result = {}
        for cat in cats:
            age_data = cat.get("Age Data", {})
            gender_data = cat.get("Gender Data", {})

            latest_age = {track_id: preds[-1] for track_id, preds in age_data.items() if preds}
            latest_gender = {track_id: preds[-1] for track_id, preds in gender_data.items() if preds}
            latest_result.update({"Latest Age": latest_age, "Latest Gender": latest_gender})

            # --- Most common gender ---
            most_common_gender = {}
            for track_id, preds in gender_data.items():
                counter = Counter(preds)
                most_common, count = counter.most_common(1)[0]
                most_common_gender[track_id] = [most_common]

            # --- Mean age ---
            mean_age = {}
            for track_id, preds in age_data.items():
                if preds:  # make sure list not empty
                    mean_age[track_id] = int(np.mean(preds))

            results.append({"Mean Age": mean_age, "Most Common Gender": most_common_gender})

        return {
            "total_count": len(total_count),
            "per_category_count": counts,
            "detections": valid_detections,
            "Age_Gender_Data": results[0] if isinstance(data, dict) else results,
            "latest": latest_result,
        }

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        alerts: Any,
        config: AgeGenderConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured tracking stats with frame-based keys."""
        _ = (_frame_number,)
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts = counting_summary.get("total_count", {})
        # cumulative_total = sum(set(total_counts.values())) if total_counts else 0
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        camera_info = self.get_camera_info_from_stream(stream_info)
        age_gender_data = counting_summary.get("Age_Gender_Data")
        curr_frame_data = counting_summary.get("latest")
        current_counts = [
            f"{curr_frame_data['Latest Age'][track_id]}-{curr_frame_data['Latest Gender'].get(track_id, 'Unknown')}"
            for track_id in curr_frame_data["Latest Age"]
        ]

        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        human_text_lines.append(f"\tPerson Detected: {len(current_counts)}")
        if total_detections > 0:
            for track_id in curr_frame_data["Latest Age"]:
                age = curr_frame_data["Latest Age"][track_id]
                gender = curr_frame_data["Latest Gender"].get(track_id, "Unknown")
                human_text_lines.append(f"\t\t{age}-{gender}")
        else:
            human_text_lines.append("\t- No detections")
        age_gender_pairs = [
            f"{age_gender_data['Mean Age'][tid]}-{age_gender_data['Most Common Gender'][tid][0]}"
            for tid in age_gender_data["Mean Age"]
        ]
        pair_counts = Counter(age_gender_pairs)
        result_list = [(pair, count) for pair, count in pair_counts.items()]
        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total Detected: {len(age_gender_data['Mean Age'])}")
        for pair, count in result_list:
            human_text_lines.append(f"\t\t{pair}:{count}")

        # total_counts_list = [{"category": cat, "count": count} for cat, count in total_counts.items() if count > 0 or cumulative_total > 0]

        detections = []
        agd = counting_summary.get("Age_Gender_Data") or {}
        mean_age_by_track = agd.get("Mean Age", {}) if isinstance(agd, dict) else {}
        common_gender_by_track = agd.get("Most Common Gender", {}) if isinstance(agd, dict) else {}
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            track_id = detection.get("track_id")
            tkey = str(track_id)
            # Prefer per-track aggregates (stable across frames); fall back to this frame's values.
            gender = detection.get("gender") or detection.get("category") or "Person"
            common = common_gender_by_track.get(tkey)
            if isinstance(common, list) and common:
                gender = common[0]
            age = mean_age_by_track.get(tkey, detection.get("age"))
            # The FE renders the detection "category" as the bbox label -> "<gender>, <age>".
            label = f"{gender}, {age}" if age is not None else str(gender)
            detection_obj = self.create_detection_object(label, bbox, segmentation=None)
            if track_id is not None:
                detection_obj["track_id"] = track_id
            if detection.get("confidence") is not None:
                detection_obj["confidence"] = detection.get("confidence")
            # Structured fields alongside the composite label, for consumers that want them split.
            detection_obj["gender"] = gender
            if age is not None:
                detection_obj["age"] = age
            detections.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds if hasattr(config.alert_config, "count_thresholds") else {}
                    ),
                    "ascending": True,
                    "settings": dict(
                        zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    ),
                }
            )

        if alerts:
            human_text_lines.append(f"Alerts: {alerts[0].get('settings', {})}")
        else:
            human_text_lines.append("Alerts: None")

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
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _check_alerts(self, summary: Dict, frame_number: Any, config: AgeGenderConfig) -> List[Dict]:
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
        # total_counts_dict = summary.get("total_counts", {})
        # cumulative_total = sum(total_counts_dict.values()) if total_counts_dict else 0
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        # Extract thresholds regardless of dict/dataclass
        _alert_cfg = config.alert_config
        _thresholds = (
            getattr(_alert_cfg, "count_thresholds", None)
            if not isinstance(_alert_cfg, dict)
            else _alert_cfg.get("count_thresholds")
        )
        _types = (
            getattr(_alert_cfg, "alert_type", None)
            if not isinstance(_alert_cfg, dict)
            else _alert_cfg.get("alert_type")
        )
        _values = (
            getattr(_alert_cfg, "alert_value", None)
            if not isinstance(_alert_cfg, dict)
            else _alert_cfg.get("alert_value")
        )
        _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ["Default"])
        _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ["JSON"])
        if _thresholds:
            for category, threshold in _thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append(
                        {
                            "alert_type": _types,
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list),
                            "settings": dict(zip(_types, _values)),
                        }
                    )
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append(
                        {
                            "alert_type": _types,
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list),
                            "settings": dict(zip(_types, _values)),
                        }
                    )
        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: AgeGenderConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured incidents."""
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        if total_detections > 0:
            start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
            self._debug_stream_timing("start_timestamp", start_timestamp)
            if start_timestamp and self.current_incident_end_timestamp == "N/A":
                self.current_incident_end_timestamp = "Incident still active"
            elif start_timestamp and self.current_incident_end_timestamp == "Incident still active":
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif (
                self.current_incident_end_timestamp != "Incident still active"
                and self.current_incident_end_timestamp != "N/A"
            ):
                self.current_incident_end_timestamp = "N/A"

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
                    self._ascending_alert_list.append(3)
                elif total_detections > 25:
                    level = "significant"
                    self._ascending_alert_list.append(2)
                elif total_detections > 15:
                    level = "medium"
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    self._ascending_alert_list.append(0)

            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config:
                _alert_cfg = config.alert_config
                _types = (
                    getattr(_alert_cfg, "alert_type", None)
                    if not isinstance(_alert_cfg, dict)
                    else _alert_cfg.get("alert_type")
                )
                _values = (
                    getattr(_alert_cfg, "alert_value", None)
                    if not isinstance(_alert_cfg, dict)
                    else _alert_cfg.get("alert_value")
                )
                _thresholds = (
                    getattr(_alert_cfg, "count_thresholds", None)
                    if not isinstance(_alert_cfg, dict)
                    else _alert_cfg.get("count_thresholds")
                )
                _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ["Default"])
                _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ["JSON"])
                alert_settings.append(
                    {
                        "alert_type": _types,
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": _thresholds or {},
                        "ascending": True,
                        "settings": dict(zip(_types, _values)),
                    }
                )

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
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    def _generate_summary(
        self,
        _summary: Dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[Dict]:
        """Generate a human-readable summary."""
        _ = (_alerts, _summary)
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: " + f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append(
                "Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}"
            )
        if len(business_analytics) > 0:
            lines.append(
                "Business Analytics: "
                + f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}"
            )

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: " + "No Summary Data")

        return ["\n".join(lines)]

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
        """Return total unique age-gender encountered so far."""
        return {"FACE": len(self.all_track_data)}

    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        """Get detailed information about track IDs."""
        frame_track_ids = {det.get("track_id") for det in detections if det.get("track_id") is not None}
        total_track_ids = set()
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
        """Format a timestamp so that exactly two digits follow the decimal point (milliseconds).

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will first be converted to a
           string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.
        2. A string already following the same layout.

        The returned value preserves the overall format of the input but truncates or pads
        the fractional seconds portion to **exactly two digits**.

        Example
        -------
        >>> self._format_timestamp("2025-08-19-04:22:47.187574 UTC")
        '2025-08-19-04:22:47.18 UTC'
        """

        # Convert numeric timestamps to the expected string representation first
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # If there is no fractional component, simply return the original string
        if "." not in timestamp:
            return timestamp

        # Split out the main portion (up to the decimal point)
        main_part, fractional_and_suffix = timestamp.split(".", 1)

        # Separate fractional digits from the suffix (typically ' UTC')
        if " " in fractional_and_suffix:
            fractional_part, suffix = fractional_and_suffix.split(" ", 1)
            suffix = " " + suffix  # Re-attach the space removed by split
        else:
            fractional_part, suffix = fractional_and_suffix, ""

        # Guarantee exactly two digits for the fractional part
        fractional_part = (fractional_part + "00")[:2]

        return f"{main_part}.{fractional_part}{suffix}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        """Get formatted current timestamp based on stream type."""

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
                stream_time_str = self._format_timestamp_for_video(start_time)
                self._debug_stream_timing("stream_time_str", stream_time_str)
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

            stream_time_str = self._format_timestamp_for_video(start_time)

            self._debug_stream_timing("stream_time_str", stream_time_str)
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
                    except Exception:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _get_tracking_start_time(self) -> str:
        """Get the tracking start time, formatted as a string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Set the tracking start time to the current time."""
        self._tracking_start_time = time.time()

    def _attach_masks_to_detections(
        self,
        processed_detections: List[Dict[str, Any]],
        raw_detections: List[Dict[str, Any]],
        iou_threshold: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """Attach segmentation masks from raw detections to processed detections."""
        if not processed_detections or not raw_detections:
            for det in processed_detections:
                det.setdefault("masks", [])
            return processed_detections

        used_raw_indices = set()
        for det in processed_detections:
            best_iou = 0.0
            best_idx = None
            for idx, raw_det in enumerate(raw_detections):
                if idx in used_raw_indices:
                    continue
                iou = self._compute_iou(det.get("bounding_box"), raw_det.get("bounding_box"))
                if iou > best_iou:
                    best_iou = iou
                    best_idx = idx
            if best_idx is not None and best_iou >= iou_threshold:
                raw_det = raw_detections[best_idx]
                masks = raw_det.get("masks", raw_det.get("mask"))
                if masks is not None:
                    det["masks"] = masks
                used_raw_indices.add(best_idx)
            else:
                det.setdefault("masks", ["EMPTY"])
        return processed_detections
