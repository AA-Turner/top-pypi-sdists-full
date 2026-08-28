"""
Face covering detection using pose-guided head crops + RetinaFace.

Post-processing pipeline (same logical steps as ``extract_faces.py`` and
``annotate_faces.py``):

  1. **Pose / head region** — COCO-style keypoints on each person detection define
     the head crop (shoulder line vs box top), matching ``extract_faces.py``.
     If keypoints are missing, an optional YOLO pose model can be run once per
     frame and matched to detections by IoU.

  2. **Face visibility** — RetinaFace scores each head crop (batch inference as in
     ``annotate_faces.py``). Low max score or no face suggests covering / occlusion.

Expects an optional BGR frame in ``stream_info["frame"]`` (``numpy.ndarray``) for
cropping. Without a frame, pose metrics from upstream detections are still parsed
but RetinaFace cannot run; detections pass through unchanged.

Architecture mirrors ``FenceClimbingDetectionUseCase``: optional zones, per-track
consecutive-frame confirmation, incident manager, ``agg_summary`` output shape.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, PeopleCountingConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..utils import apply_category_mapping, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

_GEOMETRY_RETRY_INTERVAL = 30

# COCO keypoint indices (Ultralytics pose) — same as extract_faces.py
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6

_DEFAULT_FULL_FRAME_ZONE: Dict[str, List[List[float]]] = {
    "roi": [[0.0, 0.0], [10000.0, 0.0], [10000.0, 10000.0], [0.0, 10000.0]]
}


def _extract_coco17_keypoints(detection: Dict[str, Any]) -> Optional[List[Tuple[float, float, float]]]:
    raw = detection.get("keypoints")
    if raw is None:
        return None

    if isinstance(raw, dict):
        xy = raw.get("xy") or raw.get("data") or raw.get("coords")
        conf = raw.get("conf") or raw.get("visibility")
        if xy is None:
            return None
        try:
            flat_xy: List[float] = []
            if xy and isinstance(xy[0], (list, tuple)) and len(xy[0]) >= 2:
                for row in xy[:17]:
                    flat_xy.extend([float(row[0]), float(row[1])])
            elif len(xy) >= 34:
                flat_xy = [float(x) for x in xy[:34]]
            else:
                return None

            cfs: List[float] = []
            if conf is not None and len(conf) >= 17:
                cfs = [float(conf[i]) for i in range(17)]
            else:
                cfs = [1.0] * 17

            out: List[Tuple[float, float, float]] = []
            for i in range(17):
                bx = i * 2
                out.append((flat_xy[bx], flat_xy[bx + 1], cfs[i]))
            return out
        except (TypeError, ValueError, IndexError):
            return None

    if not isinstance(raw, (list, tuple)):
        return None

    if len(raw) == 51:
        try:
            return [(float(raw[i * 3]), float(raw[i * 3 + 1]), float(raw[i * 3 + 2])) for i in range(17)]
        except (TypeError, ValueError, IndexError):
            return None

    if len(raw) == 34:
        try:
            return [(float(raw[i * 2]), float(raw[i * 2 + 1]), 1.0) for i in range(17)]
        except (TypeError, ValueError, IndexError):
            return None

    if len(raw) == 17:
        try:
            out = []
            for triple in raw:
                seq: Sequence[float] = triple  # type: ignore[assignment]
                x, y = float(seq[0]), float(seq[1])
                cf = float(seq[2]) if len(seq) > 2 else 1.0
                out.append((x, y, cf))
            return out
        except (TypeError, ValueError, IndexError):
            return None

    return None


def _bbox_xyxy(detection: Dict[str, Any]) -> Optional[Tuple[float, float, float, float]]:
    bbox = detection.get("bounding_box", detection.get("bbox"))
    if bbox is None:
        return None
    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        return float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
    if isinstance(bbox, dict):
        if all(k in bbox for k in ("x1", "y1", "x2", "y2")):
            return float(bbox["x1"]), float(bbox["y1"]), float(bbox["x2"]), float(bbox["y2"])
        x, y = float(bbox.get("x", 0)), float(bbox.get("y", 0))
        w, h = float(bbox.get("width", 0)), float(bbox.get("height", 0))
        if w > 0 and h > 0:
            return x, y, x + w, y + h
    return None


def _iou_xyxy(a: Tuple[float, float, float, float], b: Tuple[float, float, float, float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def head_crop_from_pose(
    frame_shape: Tuple[int, int],
    box_xyxy: Tuple[float, float, float, float],
    kps: List[Tuple[float, float, float]],
    *,
    kp_conf_thresh: float,
    padding: float,
    min_size: int,
) -> Optional[Tuple[int, int, int, int]]:
    """Head crop in pixel coords; logic aligned with extract_faces.py."""
    h, w = frame_shape[0], frame_shape[1]
    x1, y1, x2, y2 = box_xyxy

    ls = kps[LEFT_SHOULDER]
    rs = kps[RIGHT_SHOULDER]
    ls_ok = ls[2] >= kp_conf_thresh
    rs_ok = rs[2] >= kp_conf_thresh

    if ls_ok and rs_ok:
        shoulder_y = min(ls[1], rs[1])
    elif ls_ok:
        shoulder_y = ls[1]
    elif rs_ok:
        shoulder_y = rs[1]
    else:
        return None

    head_h = shoulder_y - y1
    if head_h <= 0:
        return None

    pad = head_h * padding
    cx1 = int(max(0, x1 - pad))
    cy1 = int(max(0, y1 - pad))
    cx2 = int(min(w, x2 + pad))
    cy2 = int(min(h, shoulder_y))

    if cx2 - cx1 < min_size or cy2 - cy1 < min_size:
        return None

    return cx1, cy1, cx2, cy2


@dataclass
class FaceCoveringDetectionPoseConfig(PeopleCountingConfig):
    """Configuration for face covering detection (pose head crop + RetinaFace)."""

    zone_config: Optional[ZoneConfig] = None

    min_covering_frames: int = 3
    exit_grace_frames: int = 3

    shoulder_keypoint_confidence_threshold: float = 0.5
    head_crop_padding: float = 0.15
    head_crop_min_size_px: int = 20

    face_covering_score_threshold: float = 0.7
    """Max RetinaFace score below this (or no detections) counts as likely covering."""

    run_yolo_pose_in_postprocessor: bool = True
    yolo_pose_model: str = "yolo11n-pose.pt"
    yolo_device: str = "0"
    retinaface_gpu_id: int = 0
    retinaface_batch_size: int = 16

    yolo_match_iou_threshold: float = 0.5

    def __post_init__(self) -> None:
        if isinstance(self.zone_config, dict):
            self.zone_config = ZoneConfig(**self.zone_config)
        if isinstance(self.alert_config, dict):
            self.alert_config = AlertConfig(**self.alert_config)

    def validate(self) -> List[str]:
        errors = super().validate()
        if self.min_covering_frames < 1:
            errors.append("min_covering_frames must be >= 1")
        if self.exit_grace_frames < 0:
            errors.append("exit_grace_frames must be >= 0")
        if not 0.0 <= self.shoulder_keypoint_confidence_threshold <= 1.0:
            errors.append("shoulder_keypoint_confidence_threshold must be between 0.0 and 1.0")
        if self.head_crop_padding < 0:
            errors.append("head_crop_padding must be >= 0")
        if self.head_crop_min_size_px < 1:
            errors.append("head_crop_min_size_px must be >= 1")
        if not 0.0 <= self.face_covering_score_threshold <= 1.0:
            errors.append("face_covering_score_threshold must be between 0.0 and 1.0")
        if self.retinaface_batch_size < 1:
            errors.append("retinaface_batch_size must be >= 1")
        if not 0.0 <= self.yolo_match_iou_threshold <= 1.0:
            errors.append("yolo_match_iou_threshold must be between 0.0 and 1.0")
        if self.zone_config:
            errors.extend(self.zone_config.validate())
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        return errors


class FaceCoveringDetectionPoseUseCase(BaseProcessor):
    """Pose-guided head crops + RetinaFace for face covering / occlusion alerts."""

    def __init__(self) -> None:
        super().__init__("face_covering_detection_pose")
        self.category = "general"
        self.CASE_TYPE: Optional[str] = "face_covering_detection_pose"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = ["person"]
        self.tracker = None
        self._tracker_seam = None

        self._total_frame_counter = 0
        self._ascending_alert_list: List[int] = []

        self._zone_inside_frames: Dict[str, Dict[Any, int]] = {}
        self._zone_covering_frames: Dict[str, Dict[Any, int]] = {}
        self._zone_outside_frames: Dict[str, Dict[Any, int]] = {}
        self._zone_alerted_tracks: Dict[str, set] = defaultdict(set)
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}

        self._consecutive_track_frames: Dict[Any, int] = {}
        self._min_confirm_frames: int = 3

        self._zone_resolution_attempted: bool = False
        self._resolved_geometry_cache: Optional[FaceCoveringDetectionPoseConfig] = None
        self._config_client: Optional[Any] = None
        self._geometry_thread: Optional[threading.Thread] = None

        self._incident_manager_factory: Optional[Any] = None
        self._incident_manager: Optional[Any] = None
        self._incident_manager_initialized: bool = False

        self._yolo_pose: Optional[Any] = None
        self._retinaface: Optional[Any] = None

    def set_config_client(self, client: Any) -> None:
        self._config_client = client

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                },
                "face_covering_score_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.7,
                    "description": "RetinaFace scores below this imply likely face covering",
                },
                "min_covering_frames": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 3,
                },
                "exit_grace_frames": {"type": "integer", "minimum": 0, "default": 3},
                "shoulder_keypoint_confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                },
                "run_yolo_pose_in_postprocessor": {
                    "type": "boolean",
                    "default": True,
                    "description": "Run YOLO pose on stream_info['frame'] when keypoints are missing",
                },
                "yolo_pose_model": {"type": "string", "default": "yolo11n-pose.pt"},
                "yolo_device": {"type": "string", "default": "0"},
                "retinaface_gpu_id": {"type": "integer", "default": 0},
                "retinaface_batch_size": {"type": "integer", "minimum": 1, "default": 16},
                "target_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["person"],
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides: Any) -> FaceCoveringDetectionPoseConfig:
        defaults: Dict[str, Any] = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "target_categories": ["person"],
            "zone_config": ZoneConfig(zones=_DEFAULT_FULL_FRAME_ZONE),
            "face_covering_score_threshold": 0.7,
            "min_covering_frames": 3,
            "exit_grace_frames": 3,
            "shoulder_keypoint_confidence_threshold": 0.5,
            "head_crop_padding": 0.15,
            "head_crop_min_size_px": 20,
            "run_yolo_pose_in_postprocessor": True,
            "yolo_pose_model": "yolo11n-pose.pt",
            "yolo_device": "0",
            "retinaface_gpu_id": 0,
            "retinaface_batch_size": 16,
            "yolo_match_iou_threshold": 0.5,
        }
        defaults.update(overrides)
        return FaceCoveringDetectionPoseConfig(**defaults)

    def _start_geometry_resolver(
        self,
        config: FaceCoveringDetectionPoseConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> None:
        if self._geometry_thread and self._geometry_thread.is_alive():
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info(
                            "FaceCoveringPose: zone geometry resolved from API (background thread)"
                        )
                        return
                    self.logger.info(
                        "FaceCoveringPose: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "FaceCoveringPose: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(
            target=_resolver,
            daemon=True,
            name="face-covering-geometry-resolver",
        )
        self._geometry_thread = t
        t.start()
        self.logger.info("FaceCoveringPose: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: FaceCoveringDetectionPoseConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[FaceCoveringDetectionPoseConfig]:
        from .hazard_zone_entry import PostProcessingConfigClient

        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info("FaceCoveringPose: _resolve_geometry_from_api skipped (no config_client)")
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "FaceCoveringPose: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info or not client:
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""

        if not app_deployment_id or not camera_id:
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            return None

        doc = filtered[0]
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            return None

        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}

        if not isinstance(zones_px, dict) or not zones_px:
            return None

        zones_dict = {name: [list(pt) for pt in points] for name, points in zones_px.items()}
        new_zone_config = ZoneConfig(zones=zones_dict)

        self.logger.info(
            "FaceCoveringPose: resolved %d zone(s) from API: %s",
            len(zones_dict),
            list(zones_dict.keys()),
        )
        return replace(config, zone_config=new_zone_config)

    def _initialize_incident_manager_once(self, config: FaceCoveringDetectionPoseConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            from ..utils.incident_manager_utils import IncidentManagerFactory

            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info("FaceCoveringPose: incident manager initialized")
        except Exception as exc:
            self.logger.warning("FaceCoveringPose: incident manager init failed: %s", exc)
        finally:
            self._incident_manager_initialized = True

    def _ensure_yolo(self, config: FaceCoveringDetectionPoseConfig) -> Any:
        if self._yolo_pose is None:
            from ultralytics import YOLO

            self._yolo_pose = YOLO(config.yolo_pose_model)
            self.logger.info("FaceCoveringPose: loaded YOLO pose model %s", config.yolo_pose_model)
        return self._yolo_pose

    def _ensure_retinaface(self, config: FaceCoveringDetectionPoseConfig) -> Any:
        if self._retinaface is None:
            from batch_face import RetinaFace

            self._retinaface = RetinaFace(gpu_id=config.retinaface_gpu_id)
            self.logger.info("FaceCoveringPose: initialized RetinaFace (gpu_id=%s)", config.retinaface_gpu_id)
        return self._retinaface

    def _yolo_keypoints_for_frame(
        self,
        frame: Any,
        config: FaceCoveringDetectionPoseConfig,
    ) -> List[Tuple[Tuple[float, float, float, float], List[Tuple[float, float, float]]]]:
        """Returns list of (xyxy_box, coco17_kps) from YOLO pose on frame."""
        model = self._ensure_yolo(config)
        results = model.predict(frame, device=config.yolo_device, verbose=False)
        out: List[Tuple[Tuple[float, float, float, float], List[Tuple[float, float, float]]]] = []
        for r in results:
            if r.boxes is None or r.keypoints is None:
                continue
            boxes = r.boxes.xyxy.cpu().numpy()
            kps_xy = r.keypoints.xy.cpu().numpy()
            kps_conf = r.keypoints.conf.cpu().numpy() if r.keypoints.conf is not None else None
            for person_idx, box in enumerate(boxes):
                x1, y1, x2, y2 = float(box[0]), float(box[1]), float(box[2]), float(box[3])
                kp_row = kps_xy[person_idx]
                cfs = kps_conf[person_idx] if kps_conf is not None else None
                kps17: List[Tuple[float, float, float]] = []
                for k in range(17):
                    conf = float(cfs[k]) if cfs is not None else 1.0
                    kps17.append((float(kp_row[k][0]), float(kp_row[k][1]), conf))
                out.append(((x1, y1, x2, y2), kps17))
        return out

    def _match_yolo_kps_to_detection(
        self,
        det_box: Tuple[float, float, float, float],
        yolo_pairs: List[Tuple[Tuple[float, float, float, float], List[Tuple[float, float, float]]]],
        iou_threshold: float,
    ) -> Optional[List[Tuple[float, float, float]]]:
        best_iou = 0.0
        best_kps: Optional[List[Tuple[float, float, float]]] = None
        for ybox, kps in yolo_pairs:
            iou = _iou_xyxy(det_box, ybox)
            if iou > best_iou:
                best_iou = iou
                best_kps = kps
        if best_iou >= iou_threshold and best_kps is not None:
            return best_kps
        return None

    def _run_face_pipeline_on_frame(
        self,
        frame: Any,
        detections: List[Dict[str, Any]],
        config: FaceCoveringDetectionPoseConfig,
    ) -> None:
        """Mutates detections in place with face_covering fields; sets _face_covering_event flags."""
        if frame is None:
            return

        h, w = frame.shape[:2]
        shape = (h, w)

        yolo_cache: Optional[List[Tuple[Tuple[float, float, float, float], List[Tuple[float, float, float]]]]] = None

        work_items: List[Tuple[int, Optional[Tuple[int, int, int, int]], Dict[str, Any]]] = []

        for idx, det in enumerate(detections):
            box = _bbox_xyxy(det)
            if box is None:
                continue

            kps = _extract_coco17_keypoints(det)
            if kps is None and config.run_yolo_pose_in_postprocessor:
                if yolo_cache is None:
                    try:
                        yolo_cache = self._yolo_keypoints_for_frame(frame, config)
                    except Exception as e:
                        self.logger.warning("FaceCoveringPose: YOLO pose failed: %s", e)
                        yolo_cache = []
                kps = (
                    self._match_yolo_kps_to_detection(box, yolo_cache, config.yolo_match_iou_threshold)
                    if yolo_cache
                    else None
                )

            crop_rc = None
            if kps is not None:
                crop_rc = head_crop_from_pose(
                    shape,
                    box,
                    kps,
                    kp_conf_thresh=config.shoulder_keypoint_confidence_threshold,
                    padding=config.head_crop_padding,
                    min_size=config.head_crop_min_size_px,
                )

            work_items.append((idx, crop_rc, det))

        batches: List[Tuple[int, Tuple[int, int, int, int], Any]] = []
        for idx, crop_rc, det in work_items:
            if crop_rc is None:
                det["face_covering_head_crop"] = None
                det["face_covering_max_score"] = None
                det["face_covering_no_valid_head_region"] = True
                det["face_covering_likely"] = False
                continue
            cx1, cy1, cx2, cy2 = crop_rc
            det["face_covering_head_crop"] = list(crop_rc)
            crop = frame[cy1:cy2, cx1:cx2]
            if crop.size == 0:
                det["face_covering_max_score"] = None
                det["face_covering_no_valid_head_region"] = True
                det["face_covering_likely"] = False
                continue
            det["face_covering_no_valid_head_region"] = False
            batches.append((idx, crop_rc, crop))

        if not batches:
            return

        try:
            detector = self._ensure_retinaface(config)
        except Exception as e:
            self.logger.warning("FaceCoveringPose: RetinaFace unavailable: %s", e)
            for det_idx, _, _ in batches:
                det = detections[det_idx]
                det["face_covering_max_score"] = None
                det["face_covering_likely"] = False
            return

        bs = config.retinaface_batch_size
        for start in range(0, len(batches), bs):
            chunk = batches[start : start + bs]
            crops = [c for _, _, c in chunk]
            try:
                face_results = detector(crops, cv=True)
            except Exception as e:
                self.logger.warning("FaceCoveringPose: RetinaFace inference failed: %s", e)
                continue

            for (det_idx, _crop_rc, _), faces in zip(chunk, face_results):
                det = detections[det_idx]
                max_score = 0.0
                if faces:
                    for _box, _lm, score in faces:
                        max_score = max(max_score, float(score))
                det["face_covering_max_score"] = round(max_score, 4)
                cov = max_score < config.face_covering_score_threshold
                det["face_covering_likely"] = bool(cov)

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        try:
            if not isinstance(config, FaceCoveringDetectionPoseConfig):
                return self.create_error_result(
                    "Invalid configuration type for face covering detection (pose)",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if context is None:
                context = ProcessingContext()

            self._initialize_incident_manager_once(config)

            if not self._zone_resolution_attempted:
                self._zone_resolution_attempted = True
                if stream_info:
                    try:
                        resolved = self._resolve_geometry_from_api(config, stream_info)
                        if resolved is not None:
                            self._resolved_geometry_cache = resolved
                            self.logger.info("FaceCoveringPose: zone geometry resolved from API and cached")
                        else:
                            self.logger.warning(
                                "FaceCoveringPose: API returned no zone config; "
                                "starting background retry (every %ds). Using fallback zone.",
                                _GEOMETRY_RETRY_INTERVAL,
                            )
                            self._start_geometry_resolver(config, stream_info)
                    except Exception as exc:
                        self.logger.warning(
                            "FaceCoveringPose: zone resolution raised (%s); background retry.",
                            exc,
                        )
                        self._start_geometry_resolver(config, stream_info)
                else:
                    self.logger.info("FaceCoveringPose: no stream_info on first frame; using config zone")

            if self._resolved_geometry_cache is not None:
                config = self._resolved_geometry_cache

            if not config.zone_config or not config.zone_config.zones:
                config = replace(config, zone_config=ZoneConfig(zones=_DEFAULT_FULL_FRAME_ZONE))

            context.input_format = match_results_structure(data)
            context.confidence_threshold = config.confidence_threshold

            if isinstance(data, list):
                processed_data = data
            elif isinstance(data, dict):
                processed_data = []
                for _key, value in data.items():
                    if isinstance(value, list):
                        processed_data = value
                        break
            else:
                processed_data = []

            self._total_frame_counter += 1

            frame_number: Any = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {}) or {}
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame
            if frame_number is None:
                frame_number = self._total_frame_counter

            frame = None
            if stream_info:
                frame = stream_info.get("frame") or stream_info.get("numpy_frame")

            (
                alerts,
                incidents_list,
                tracking_stats_list,
                business_analytics_list,
                summary_list,
            ) = self._process_frame_detections(
                processed_data,
                config,
                str(frame_number),
                stream_info,
                frame,
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
                    "human_text": summary,
                }
            }

            context.mark_completed()

            proc_ms = (time.time() - processing_start) * 1000.0
            self.logger.debug(
                "FaceCoveringPose: frame %s processed in %.1f ms",
                frame_number,
                proc_ms,
            )

            return self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )

        except Exception as e:
            self.logger.error("FaceCoveringPose.process failed: %s", e, exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context,
            )

    def _process_frame_detections(
        self,
        frame_data: Any,
        config: FaceCoveringDetectionPoseConfig,
        frame_id: str,
        stream_info: Optional[Dict[str, Any]],
        frame: Any,
    ) -> tuple:
        if isinstance(frame_data, list):
            frame_detections = frame_data
        else:
            frame_detections = []

        if config.confidence_threshold is not None:
            frame_detections = [
                d for d in frame_detections if d.get("confidence", 0) >= config.confidence_threshold
            ]

        if config.index_to_category:
            frame_detections = apply_category_mapping(frame_detections, config.index_to_category)

        target_cats = config.target_categories or self.target_categories
        frame_detections = [d for d in frame_detections if d.get("category") in target_cats]

        needs_tracking = bool(config.enable_tracking)
        if self.tracker is None and needs_tracking:
            try:
                fps = 30
                try:
                    if stream_info:
                        fps = int(stream_info.get("input_settings", {}).get("original_fps", 30))
                        if fps <= 0:
                            fps = 30
                except Exception:
                    fps = 30

                # F10b S6/S7 gap closure: LEGACY_40's base kwargs (0.4/0.05/0.3/0.8) are this
                # site's literals; track_buffer/max_time_lost/frame_rate are fps-derived overrides.
                if self._tracker_seam is None:
                    self._tracker_seam = ConfigDrivenTracker()
                self.tracker = self._tracker_seam.get_shared_tracker(
                    profile=TrackerProfile.LEGACY_40,
                    track_buffer=int(3 * fps),
                    max_time_lost=int(3 * fps),
                    frame_rate=fps,
                )
                self.logger.info("Initialized AdvancedTracker for FaceCoveringPose")
            except Exception as e:
                self.logger.warning("AdvancedTracker init failed, using raw detections: %s", e)

        tracked_detections = frame_detections
        if self.tracker is not None and needs_tracking:
            try:
                tracked_detections = self.tracker.update(frame_detections)
            except Exception as e:
                self.logger.warning("AdvancedTracker update failed, using raw detections: %s", e)
                tracked_detections = frame_detections

        if frame is not None:
            try:
                self._run_face_pipeline_on_frame(frame, tracked_detections, config)
            except Exception as e:
                self.logger.warning("FaceCoveringPose: face pipeline error: %s", e)
        else:
            self.logger.debug("FaceCoveringPose: no frame in stream_info; skipping RetinaFace/YOLO crops")

        counting_summary = {
            "total_objects": len(tracked_detections),
            "detections": tracked_detections,
            "categories": {},
        }
        for det in tracked_detections:
            cat = det.get("category", "unknown")
            counting_summary["categories"][cat] = counting_summary["categories"].get(cat, 0) + 1

        self._update_tracking_state(counting_summary)

        resolved_zones: Dict[str, Any] = (
            config.zone_config.zones if config.zone_config and config.zone_config.zones else {}
        )
        zone_analysis: Dict[str, Any] = {zn: {} for zn in resolved_zones}
        if resolved_zones:
            enhanced = self._update_zone_tracking_face_covering(zone_analysis, counting_summary["detections"], config)
            for zn, edata in enhanced.items():
                zone_analysis[zn] = edata

        alerts = self._check_alerts(counting_summary, zone_analysis, config, frame_id)
        incidents = self._generate_incidents(counting_summary, zone_analysis, alerts, config, frame_id, stream_info)
        tracking_stats = self._generate_tracking_stats(
            counting_summary, zone_analysis, config, frame_id, alerts, stream_info
        )
        business_analytics = self._generate_business_analytics(
            counting_summary, zone_analysis, config, frame_id, stream_info
        )
        summary = self._generate_summary(counting_summary, incidents, tracking_stats, business_analytics, alerts)

        return alerts, incidents, tracking_stats, business_analytics, summary

    def _update_zone_tracking_face_covering(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: FaceCoveringDetectionPoseConfig,
    ) -> Dict[str, Dict[str, Any]]:
        zones = config.zone_config.zones if config.zone_config and config.zone_config.zones else {}
        if not zones:
            return {}

        enhanced_zone_analysis: Dict[str, Dict[str, Any]] = {}
        current_frame_zone_tracks: Dict[str, set] = {}

        for zone_name in zones:
            current_frame_zone_tracks[zone_name] = set()
            self._zone_total_track_ids.setdefault(zone_name, set())
            self._zone_alerted_tracks.setdefault(zone_name, set())
            self._zone_inside_frames.setdefault(zone_name, {})
            self._zone_covering_frames.setdefault(zone_name, {})
            self._zone_outside_frames.setdefault(zone_name, {})

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            likely = detection.get("face_covering_likely")
            no_head = detection.get("face_covering_no_valid_head_region")

            center_point = get_bbox_bottom25_center(bbox)

            for zone_name, zone_polygon in zones.items():
                polygon_points = [(pt[0], pt[1]) for pt in zone_polygon]

                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)

                    prev_in = self._zone_inside_frames[zone_name].get(track_id, 0)
                    self._zone_inside_frames[zone_name][track_id] = prev_in + 1
                    self._zone_outside_frames[zone_name].pop(track_id, None)

                    if likely is True and not no_head:
                        prev_cov = self._zone_covering_frames[zone_name].get(track_id, 0)
                        self._zone_covering_frames[zone_name][track_id] = prev_cov + 1
                    else:
                        self._zone_covering_frames[zone_name][track_id] = 0

                    covering_streak = self._zone_covering_frames[zone_name].get(track_id, 0)

                    if (
                        covering_streak >= config.min_covering_frames
                        and track_id not in self._zone_alerted_tracks[zone_name]
                        and likely is True
                        and not no_head
                    ):
                        detection["_face_covering_event"] = {
                            "zone_name": zone_name,
                            "track_id": track_id,
                            "max_face_score": detection.get("face_covering_max_score"),
                        }
                else:
                    outside = self._zone_outside_frames[zone_name].get(track_id, 0) + 1
                    self._zone_outside_frames[zone_name][track_id] = outside

                    if outside >= config.exit_grace_frames and track_id not in current_frame_zone_tracks[zone_name]:
                        self._zone_inside_frames[zone_name].pop(track_id, None)
                        self._zone_covering_frames[zone_name].pop(track_id, None)
                        self._zone_outside_frames[zone_name].pop(track_id, None)
                        self._zone_alerted_tracks[zone_name].discard(track_id)

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

    def _update_tracking_state(self, counting_summary: Dict) -> None:
        detections = counting_summary.get("detections", [])
        current_frame_tracks: set = set()

        if not detections:
            for tid in list(self._consecutive_track_frames.keys()):
                self._consecutive_track_frames[tid] = max(0, self._consecutive_track_frames[tid] - 1)
            self._current_frame_track_ids = set()
            return

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                current_frame_tracks.add(track_id)

        updated: Dict[Any, int] = {}
        for tid in current_frame_tracks:
            prev = self._consecutive_track_frames.get(tid, 0)
            updated[tid] = min(self._min_confirm_frames, prev + 1)
        for tid, prev in self._consecutive_track_frames.items():
            if tid not in updated:
                updated[tid] = max(0, prev - 1)
        self._consecutive_track_frames = updated

        if not hasattr(self, "_total_track_ids"):
            self._total_track_ids: set = set()

        for tid, count in self._consecutive_track_frames.items():
            if count >= self._min_confirm_frames and tid not in self._total_track_ids:
                self._total_track_ids.add(tid)

        self._current_frame_track_ids = current_frame_tracks
        self._total_count = len(self._total_track_ids)

    def get_total_count(self) -> int:
        return getattr(self, "_total_count", 0)

    def get_current_frame_count(self) -> int:
        return len(getattr(self, "_current_frame_track_ids", set()))

    def _check_alerts(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        config: FaceCoveringDetectionPoseConfig,
        frame_id: str,
    ) -> List[Dict]:
        _ = (_zone_analysis,)
        alerts: List[Dict] = []

        for det in counting_summary.get("detections", []):
            evt = det.get("_face_covering_event")
            if not evt:
                continue
            settings: Dict[str, Any] = {}
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                settings = {
                    t: v
                    for t, v in zip(
                        getattr(config.alert_config, "alert_type", ["Default"]),
                        getattr(config.alert_config, "alert_value", ["JSON"]),
                    )
                }
            alerts.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"])
                    if config.alert_config
                    else ["Default"],
                    "alert_id": f"face_cover_{evt['zone_name']}_{evt['track_id']}_{frame_id}",
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": "face_covering_confirmed",
                    "ascending": True,
                    "settings": settings,
                }
            )
            self._zone_alerted_tracks[evt["zone_name"]].add(evt["track_id"])
            det.pop("_face_covering_event", None)

        total_people = counting_summary.get("total_objects", 0)
        if config.alert_config and hasattr(config.alert_config, "count_thresholds"):
            thresholds = getattr(config.alert_config, "count_thresholds", None) or {}
            for category, threshold in thresholds.items():
                if category == "all" and total_people >= threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_id}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
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

        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        alerts: List,
        config: FaceCoveringDetectionPoseConfig,
        frame_id: str,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        _ = (_zone_analysis,)
        camera_info = self.get_camera_info_from_stream(stream_info)
        incidents = []
        total_people = counting_summary.get("total_objects", 0)
        covering_now = sum(
            1
            for d in counting_summary.get("detections", [])
            if d.get("face_covering_likely") and not d.get("face_covering_no_valid_head_region")
        )
        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

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
                    "settings": {
                        t: v
                        for t, v in zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    },
                }
            )

        if alerts or covering_now > 0:
            if covering_now > 5:
                level = "critical"
                self._ascending_alert_list.append(3)
            elif covering_now > 2:
                level = "significant"
                self._ascending_alert_list.append(2)
            elif covering_now > 0:
                level = "medium"
                self._ascending_alert_list.append(1)
            else:
                level = "low"
                self._ascending_alert_list.append(0)

            human_text = (
                f"FACE COVERING (POSE+FACE) @ {current_timestamp}:\n"
                f"\tSeverity Level: {level}\n"
                f"\tPersons in scene: {total_people}\n"
                f"\tLikely covering (visible head crop): {covering_now}"
            )

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_id}_{int(time.time())}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        config: FaceCoveringDetectionPoseConfig,
        frame_id: str,
        alerts: Any = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        if alerts is None:
            alerts = []

        total_people = counting_summary.get("total_objects", 0)
        total_unique_count = self.get_total_count()
        camera_info = self.get_camera_info_from_stream(stream_info)

        total_counts = []
        current_counts = []
        for category in config.person_categories or ["person"]:
            if total_unique_count > 0:
                total_counts.append(self.create_count_object(category, total_unique_count))
            current_frame_count = self.get_current_frame_count()
            if current_frame_count > 0 or total_people > 0:
                current_counts.append(self.create_count_object(category, current_frame_count))

        detections_out = []
        for det in counting_summary.get("detections", []):
            bbox = det.get("bounding_box", {})
            category = det.get("category", "person")
            detections_out.append(self.create_detection_object(category, bbox))

        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        covering_now = sum(
            1
            for d in counting_summary.get("detections", [])
            if d.get("face_covering_likely") and not d.get("face_covering_no_valid_head_region")
        )

        human_text_lines = [f"FACE COVERING STATUS @ {current_timestamp}:"]
        human_text_lines.append(f"\t- Persons detected: {total_people}")
        human_text_lines.append(f"\t- Likely face covering (head crop): {covering_now}")

        if zone_analysis:
            for zone_name, zone_data in zone_analysis.items():
                zc = zone_data.get("current_count", 0)
                zt = zone_data.get("total_count", 0)
                human_text_lines.append(f"\t- {zone_name}: {zc} current, {zt} total")

        human_text_lines.append(f"\t- Total unique tracked: {total_unique_count}")
        if not alerts:
            human_text_lines.append("Alerts: None")
        human_text = "\n".join(human_text_lines)

        tracking_stat = self.create_tracking_stats(
            total_counts,
            current_counts,
            detections_out,
            human_text,
            camera_info,
            alerts,
        )

        if zone_analysis:
            tracking_stat["zone_stats"] = [
                {
                    "zone_name": zn,
                    "current_count": zd.get("current_count", 0),
                    "total_count": zd.get("total_count", 0),
                    "current_track_ids": zd.get("current_track_ids", []),
                    "total_track_ids": zd.get("total_track_ids", []),
                }
                for zn, zd in zone_analysis.items()
            ]

        return [tracking_stat]

    def _generate_business_analytics(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        config: FaceCoveringDetectionPoseConfig,
        frame_id: str,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_people = counting_summary.get("total_objects", 0)
        covering_now = sum(
            1
            for d in counting_summary.get("detections", [])
            if d.get("face_covering_likely") and not d.get("face_covering_no_valid_head_region")
        )

        if total_people == 0 and not config.enable_analytics:
            return []

        analytics_stats = {
            "person_count": total_people,
            "likely_face_covering_count": covering_now,
            "unique_persons_tracked": self.get_total_count(),
            "current_frame_count": self.get_current_frame_count(),
        }

        if zone_analysis:
            for zone_name, zone_data in zone_analysis.items():
                analytics_stats[f"{zone_name}_occupancy"] = zone_data.get("current_count", 0)

        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        analytics_human_text = self.generate_analytics_human_text(
            "face_covering_pose_analytics",
            analytics_stats,
            current_timestamp,
            current_timestamp,
        )

        analytics = self.create_business_analytics(
            "face_covering_pose_analytics",
            analytics_stats,
            analytics_human_text,
            camera_info,
        )
        return [analytics]

    def _generate_summary(
        self,
        _summary: dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        _ = (_alerts, _summary)
        lines = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if incidents:
            lines.append("Incidents: " + f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if tracking_stats:
            lines.append("Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', 'No tracking stats')}")
        if business_analytics:
            lines.append("Business Analytics: " + f"\t{business_analytics[0].get('human_text', 'No analytics')}")
        if not incidents and not tracking_stats and not business_analytics:
            lines.append("Summary: No Summary Data")

        return ["\n".join(lines)]
