"""
Vehicle Segmentation Use Case for Post-Processing.

Segmentation-output based use case for the ``rfdetr_segmentation_codebase``
backend, which emits a dual-port payload (``detection0`` + ``mask0``) joined
via ``detection_index``/``mask_id`` — the same shape ``flood_detection``
consumes, see :meth:`VehicleSegmentationUseCase._normalize_yolo_results`.

Model classes (standard 1-indexed MS COCO category ids):
- 3: car
- 4: motorcycle
- 6: bus
- 8: truck

``usecase_categories`` covers all 91 MS COCO category id slots (0-90, 0-indexed,
including the ``background`` slot and the unused ``N/A`` placeholder ids) since
the upstream model's output vector allocates a slot for each of them; only the
four vehicle categories above are kept as ``target_categories``. RF-DETR is NMS-free, so the same box can carry
more than one label even after confidence filtering — a class-agnostic IoU
dedup pass (:class:`~..utils.AgnosticNMS`) removes the lower-confidence
duplicate before category filtering. Target-category detections are then
tracked across frames with the shared ``AdvancedTracker`` seam (same
mechanism as ``vehicle_monitoring.py``) so ``total_counts`` reflects unique
vehicles rather than raw per-frame detections. No incidents or alerts are
produced.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..utils import (
    AgnosticNMS,
    apply_category_mapping,
    filter_by_confidence,
    match_results_structure,
)

# ---------------------------------------------------------------------------
# MS COCO 91-class category map (standard 0-90 gapped numbering scheme,
# including the ``background`` slot and the unused ``N/A`` placeholder ids).
# ---------------------------------------------------------------------------

COCO_CATEGORY_ID_TO_NAME: Dict[int, str] = {
    0: "background",
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorcycle",
    5: "airplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    12: "N/A",
    13: "stop sign",
    14: "parking meter",
    15: "bench",
    16: "bird",
    17: "cat",
    18: "dog",
    19: "horse",
    20: "sheep",
    21: "cow",
    22: "elephant",
    23: "bear",
    24: "zebra",
    25: "giraffe",
    26: "N/A",
    27: "backpack",
    28: "umbrella",
    29: "N/A",
    30: "N/A",
    31: "handbag",
    32: "tie",
    33: "suitcase",
    34: "frisbee",
    35: "skis",
    36: "snowboard",
    37: "sports ball",
    38: "kite",
    39: "baseball bat",
    40: "baseball glove",
    41: "skateboard",
    42: "surfboard",
    43: "tennis racket",
    44: "bottle",
    45: "N/A",
    46: "wine glass",
    47: "cup",
    48: "fork",
    49: "knife",
    50: "spoon",
    51: "bowl",
    52: "banana",
    53: "apple",
    54: "sandwich",
    55: "orange",
    56: "broccoli",
    57: "carrot",
    58: "hot dog",
    59: "pizza",
    60: "donut",
    61: "cake",
    62: "chair",
    63: "couch",
    64: "potted plant",
    65: "bed",
    66: "N/A",
    67: "dining table",
    68: "N/A",
    69: "N/A",
    70: "toilet",
    71: "N/A",
    72: "tv",
    73: "laptop",
    74: "mouse",
    75: "remote",
    76: "keyboard",
    77: "cell phone",
    78: "microwave",
    79: "oven",
    80: "toaster",
    81: "sink",
    82: "refrigerator",
    83: "N/A",
    84: "book",
    85: "clock",
    86: "vase",
    87: "scissors",
    88: "teddy bear",
    89: "hair drier",
    90: "toothbrush",
}

COCO_91_CATEGORIES: List[str] = list(COCO_CATEGORY_ID_TO_NAME.values())

VEHICLE_TARGET_CATEGORIES: List[str] = ["car", "motorcycle", "bus", "truck"]


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class VehicleSegmentationConfig(BaseConfig):
    """Configuration for vehicle segmentation post-processing."""

    confidence_threshold: float = 0.4

    # Explicit overrides of the BaseConfig defaults (rather than left implicit
    # via inheritance) since this use case now runs a real cross-frame
    # AdvancedTracker (see VehicleSegmentationUseCase.process) instead of
    # per-frame-only counting.
    enable_tracking: bool = True
    enable_analytics: bool = True
    enable_unique_counting: bool = True

    # Model detects the full 91-slot COCO label set; only vehicles are kept downstream.
    usecase_categories: List[str] = field(default_factory=lambda: list(COCO_91_CATEGORIES))
    target_categories: List[str] = field(default_factory=lambda: list(VEHICLE_TARGET_CATEGORIES))
    index_to_category: Dict[int, str] | None = field(default_factory=lambda: dict(COCO_CATEGORY_ID_TO_NAME))

    # No incidents/alerts for this use case.
    alert_config: AlertConfig | None = None

    # RF-DETR is NMS-free: dedupe same-box/different-label detections that
    # survive confidence filtering, keeping the higher-confidence one.
    enable_nms: bool = True
    nms_iou_threshold: float = 0.5


# ---------------------------------------------------------------------------
# Processor
# ---------------------------------------------------------------------------


class VehicleSegmentationUseCase(BaseProcessor):
    """Post-processor for vehicle segmentation model outputs."""

    def __init__(self) -> None:
        super().__init__("vehicle_segmentation")
        self.category: str = "traffic"
        self.CASE_TYPE: str | None = "vehicle_segmentation"
        self.CASE_VERSION: str | None = "1.0"

        self.target_categories: List[str] = list(VEHICLE_TARGET_CATEGORIES)
        self._total_frame_counter: int = 0
        self.start_timer: str | None = None
        self._tracking_start_time: float | None = None

        # Cross-frame object tracking (AdvancedTracker via the shared
        # ConfigDrivenTracker seam — same mechanism as vehicle_monitoring.py).
        self.tracker = None
        self._tracker_seam: ConfigDrivenTracker | None = None
        self._per_category_total_track_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._new_track_ids_this_frame: Dict[str, set] = {cat: set() for cat in self.target_categories}

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def process(
        self,
        data: Any = None,
        config: ConfigProtocol = None,
        context: ProcessingContext | None = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> ProcessingResult:
        """Run vehicle segmentation post-processing on one frame.

        Args:
            data: Raw model output — either the backend dual-port
                ``{"detection0": ..., "mask0": ...}`` payload or an
                already-flat detection list.
            config: Must be a :class:`VehicleSegmentationConfig` instance.
            context: Optional processing context carrying metadata.
            stream_info: Stream/video metadata used for frame numbering.

        Returns:
            :class:`ProcessingResult` containing an ``agg_summary`` payload
            whose detections carry only encoded segmentation values.
        """
        is_valid_config = isinstance(config, VehicleSegmentationConfig) or (
            hasattr(config, "usecase")
            and config.usecase == "vehicle_segmentation"
            and hasattr(config, "category")
            and config.category == "traffic"
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed in vehicle_segmentation. "
                f"Got type={type(config).__name__}, "
                f"usecase={getattr(config, 'usecase', 'N/A')}, "
                f"category={getattr(config, 'category', 'N/A')}"
            )
            return self.create_error_result(
                f"Invalid config type: expected VehicleSegmentationConfig or config with "
                f"usecase='vehicle_segmentation', got {type(config).__name__} with "
                f"usecase={getattr(config, 'usecase', 'N/A')}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        # Normalise the backend's detection0 + mask0 dual-port payload (or an
        # already-flat detection list) to the internal detection schema.
        data = self._normalize_yolo_results(data, getattr(config, "index_to_category", None))
        self.logger.debug(f"[vehicle_segmentation] normalized_input={data}")

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        # Confidence filtering.
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
        else:
            processed_data = data
            self.logger.debug("Skipped confidence filtering – no threshold provided")

        # Index-to-category label mapping.
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        # RF-DETR is NMS-free: the same box can survive confidence filtering
        # under more than one label. Class-agnostic IoU dedup keeps only the
        # higher-confidence detection for each duplicated box, run across the
        # full label set (a duplicate's second label need not itself be a
        # target category) and before target-category filtering.
        if getattr(config, "enable_nms", True):
            # min_box_size=0.0 is load-bearing. It defaults to 2.0 *pixels*, but this
            # use case is fed by the matrice_inference BYOM contract, whose detection
            # boxes are normalized to [0, 1] (detection0.data.coordinate_frame.space ==
            # "normalized"). Against a pixel floor every such box is "too small", so
            # AgnosticNMS dropped every box and returned [] -- silently emptying the
            # frame whenever 2+ detections survived filter_by_confidence (apply()
            # short-circuits at len == 1, which is why single-detection frames still
            # worked and the loss looked intermittent rather than total).
            nms = AgnosticNMS(
                iou_threshold=float(getattr(config, "nms_iou_threshold", 0.5)),
                min_box_size=0.0,
            )
            processed_data = nms.apply(processed_data, class_agnostic=True)

        # Retain only target category detections.
        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in config.target_categories]

        # Cross-frame tracking: assign a persistent track_id per vehicle so
        # total/new counts reflect unique objects, not per-frame detections.
        if getattr(config, "enable_tracking", True):
            if self.tracker is None:
                if self._tracker_seam is None:
                    self._tracker_seam = ConfigDrivenTracker()
                self.tracker = self._tracker_seam.get_shared_tracker(
                    config=config,
                    stream_info=stream_info,
                    profile=TrackerProfile.NEW_FLOW,
                    namespace=True,
                    restore=True,
                )
                self.logger.info("Initialized AdvancedTracker for vehicle_segmentation")
            try:
                processed_data = self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")
            self._update_tracking_state(processed_data)

        self._total_frame_counter += 1

        # Resolve frame number from stream_info when available.
        frame_number: int | None = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(processed_data)
        self._extract_predictions(processed_data)

        tracking_stats_list = self._generate_tracking_stats(counting_summary, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics()
        summary_list = self._generate_summary(tracking_stats_list, business_analytics_list)

        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else ""

        agg_summary = {
            str(frame_number): {
                "incidents": {},
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": [],
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
        return result

    # ------------------------------------------------------------------
    # Normalisation
    # ------------------------------------------------------------------

    def _normalize_yolo_results(
        self,
        data: Any,
        index_to_category: Dict[int, str] | None = None,
    ) -> Any:
        """Normalise model outputs to the internal detection schema.

        Handles the backend dual-port format (``detection0`` + ``mask0`` keys),
        plain lists-of-detections, and frame_id→list mappings. Each detection
        dict is normalised to contain at least: ``category``, ``confidence``,
        ``bounding_box``, and—when available—``mask_rle``, ``shape``, and
        ``segmentation_area``.

        Backend dual-port format::

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

        def resolve_category(d: Dict[str, Any]) -> Tuple[str, int | None]:
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
    # Segmentation helpers
    # ------------------------------------------------------------------

    def _build_segmentation(self, detection: Dict[str, Any]) -> Dict[str, Any] | None:
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
        can omit the field entirely. Only encoded values are ever returned —
        never a decoded/raw mask array.

        Args:
            detection: A single normalised detection dict.

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
    # Tracking state
    # ------------------------------------------------------------------

    def _update_tracking_state(self, detections: List[Dict[str, Any]]) -> None:
        """Update per-category current/new/total track-id sets from one frame's tracked detections."""
        current_frame_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        for det in detections:
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat not in self.target_categories or track_id is None:
                continue
            current_frame_ids.setdefault(cat, set()).add(track_id)

        self._new_track_ids_this_frame = {
            cat: current_frame_ids.get(cat, set()) - self._per_category_total_track_ids.get(cat, set())
            for cat in self.target_categories
        }
        self._current_frame_track_ids = current_frame_ids
        for cat, ids in current_frame_ids.items():
            self._per_category_total_track_ids.setdefault(cat, set()).update(ids)

    def get_total_counts(self) -> Dict[str, int]:
        """Cumulative unique vehicle count per category, across all frames seen so far."""
        return {cat: len(ids) for cat, ids in self._per_category_total_track_ids.items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Vehicles per category that appeared for the first time in the current frame."""
        return {cat: len(ids) for cat, ids in self._new_track_ids_this_frame.items()}

    # ------------------------------------------------------------------
    # Counting
    # ------------------------------------------------------------------

    def _count_categories(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Count detections per category and build summary payload.

        Args:
            detections: Filtered, normalised detection list.

        Returns:
            Dict with ``total_count``, ``per_category_count``, and
            ``detections`` keys.
        """
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
            }
            # Preserve instance-segmentation fields so _build_segmentation can
            # still encode them further downstream.
            for key in ("mask_rle", "segmentation", "masks", "mask", "shape", "segmentation_area", "class_id"):
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
    # Tracking statistics (total_counts is the cumulative unique-track-id
    # count per category since stream start; current_counts is this frame's
    # per-category detection count — see _update_tracking_state)
    # ------------------------------------------------------------------

    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        config: VehicleSegmentationConfig,
        frame_number: int | None = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        """Build tracking statistics for the current frame.

        ``detections`` in the returned stats carry only the encoded
        segmentation value (via :meth:`_build_segmentation`) — never a
        raw/decoded mask.

        Args:
            counting_summary: Frame-level counting summary.
            config: Use-case configuration.
            frame_number: Current frame index.
            stream_info: Stream metadata.

        Returns:
            Single-element list with a tracking stats dict.
        """
        camera_info = self.get_camera_info_from_stream(stream_info)
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        per_category_count = counting_summary.get("per_category_count", {})
        current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0]

        if getattr(config, "enable_tracking", True):
            total_counts_dict = self.get_total_counts()
            new_counts_dict = self.get_new_counts_this_frame()
        else:
            total_counts_dict = per_category_count
            new_counts_dict = {}
        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items() if count > 0]

        detections_output: List[Dict[str, Any]] = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "unknown")
            segmentation = self._build_segmentation(detection)
            det_obj = self.create_detection_object(
                category, bbox, segmentation=segmentation, track_id=detection.get("track_id")
            )
            detections_output.append(det_obj)

        human_text_lines: List[str] = [f"CURRENT FRAME @ {current_timestamp}:"]
        for cat, count in per_category_count.items():
            human_text_lines.append(f"\t- {cat}: {count}")
        if not per_category_count:
            human_text_lines.append("\t- No vehicles detected")
        human_text = "\n".join(human_text_lines)

        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections_output,
            human_text=human_text,
            camera_info=camera_info,
            alerts=[],
            alert_settings=[],
            reset_settings=[],
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stat["target_categories"] = self.target_categories
        tracking_stat["current_new_counts"] = current_new_counts
        return [tracking_stat]

    # ------------------------------------------------------------------
    # Business analytics (not needed for this use case)
    # ------------------------------------------------------------------

    def _generate_business_analytics(self) -> List[Dict[str, Any]]:
        """Return business analytics payload.

        Always empty — this use case does not require business KPIs.
        """
        return []

    # ------------------------------------------------------------------
    # Human-readable summary
    # ------------------------------------------------------------------

    def _generate_summary(
        self,
        tracking_stats: List[Dict[str, Any]],
        business_analytics: List[Dict[str, Any]],
    ) -> List[str]:
        """Assemble a human-readable summary string for the frame.

        Args:
            tracking_stats: Generated tracking stats.
            business_analytics: Generated business analytics.

        Returns:
            Single-element list with the summary string.
        """
        lines: List[str] = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if tracking_stats:
            lines.append(
                "Tracking Statistics: \t" + tracking_stats[0].get("human_text", "No tracking statistics detected")
            )
        if business_analytics:
            lines.append(
                "Business Analytics: \t" + business_analytics[0].get("human_text", "No business analytics detected")
            )
        if not tracking_stats and not business_analytics:
            lines.append("Summary: No Summary Data")

        return ["\n".join(lines)]

    # ------------------------------------------------------------------
    # Timestamp utilities
    # ------------------------------------------------------------------

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

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
        stream_info: Dict[str, Any] | None,
        precision: bool = False,
    ) -> str:
        """Return a formatted current-frame timestamp string.

        Args:
            stream_info: Stream metadata dict.
            precision: If ``True``, return microsecond-precision ISO timestamp.

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
        stream_info: Dict[str, Any] | None,
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

        if self.start_timer is None:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate

        if precision:
            return self._format_timestamp(self.start_timer)

        return self._format_timestamp(self.start_timer)
