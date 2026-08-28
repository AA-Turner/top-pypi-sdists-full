"""
Fence climbing detection with a pose-estimation gate.

Same behaviour as FenceClimbingDetectionUseCase (zones, displacement, framing),
except a climbing alert fires only when COCO-format keypoints on the detection show
hands raised visibly above the head (wrists higher in the frame than facial keypoints).

Upstream models (e.g. YOLO-pose, RTMPose) should attach flattened or nested keypoints
to each person detection dict; see ``_extract_coco17_keypoints``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..utils.geometry_utils import (
    get_bbox_bottom25_center,
    get_bbox_center,
    point_in_polygon,
)

from .fence_climbing_detection import FenceClimbingDetectionConfig, FenceClimbingDetectionUseCase

# COCO 17 topology (Ultralytics / OpenPose-compatible ordering)
_KP_NOSE = 0
_KP_LEFT_EYE = 1
_KP_RIGHT_EYE = 2
_KP_LEFT_EAR = 3
_KP_RIGHT_EAR = 4
_KP_LEFT_WRIST = 9
_KP_RIGHT_WRIST = 10


def _extract_coco17_keypoints(detection: Dict[str, Any]) -> Optional[List[Tuple[float, float, float]]]:
    """
    Return 17 tuples (x, y, confidence), or None if keypoints cannot be parsed.

    Supported shapes on ``detection["keypoints"]``:
      * Flat list of length 51: [x0,y0,c0, x1,y1,c1, ...]
      * Length 34: xy only, confidence assumed 1.0
      * Length 17: each element is [x,y] or [x,y,c]
    """
    raw = detection.get("keypoints")
    if raw is None:
        return None

    if isinstance(raw, dict):
        xy = raw.get("xy") or raw.get("data") or raw.get("coords")
        conf = raw.get("conf") or raw.get("visibility")
        if xy is None:
            return None
        try:
            flat_xy = []
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
        out = []
        try:
            for i in range(17):
                b = i * 3
                out.append((float(raw[b]), float(raw[b + 1]), float(raw[b + 2])))
            return out
        except (TypeError, ValueError, IndexError):
            return None

    if len(raw) == 34:
        try:
            return [
                (float(raw[i * 2]), float(raw[i * 2 + 1]), 1.0) for i in range(17)
            ]
        except (TypeError, ValueError, IndexError):
            return None

    if len(raw) == 17:
        out = []
        try:
            for i, triple in enumerate(raw):
                seq: Sequence[float] = triple  # type: ignore[assignment]
                x, y = float(seq[0]), float(seq[1])
                cf = float(seq[2]) if len(seq) > 2 else 1.0
                out.append((x, y, cf))
            return out
        except (TypeError, ValueError, IndexError):
            return None

    return None


def hands_raised_above_head(
    detection: Dict[str, Any],
    kp_conf_thresh: float,
    margin_px: float,
    require_both_wrists: bool,
) -> Tuple[bool, Optional[float], Optional[float]]:
    """
    In image coords (y downward), wrists must sit above facial keypoints:

        wrist_y < head_ref_y - margin_px

    head_ref_y is the minimum y among visible nose / eyes / ears (highest visible
    facial landmark in frame).

    Returns (passed, head_ref_y, best_wrist_y) for telemetry; refs may be None if no pass.
    """
    kps = _extract_coco17_keypoints(detection)
    if kps is None:
        return False, None, None

    face_idx = [_KP_NOSE, _KP_LEFT_EYE, _KP_RIGHT_EYE, _KP_LEFT_EAR, _KP_RIGHT_EAR]
    head_ys = [kps[i][1] for i in face_idx if kps[i][2] >= kp_conf_thresh]
    if not head_ys:
        return False, None, None

    head_ref_y = min(head_ys)
    thresh_y = head_ref_y - margin_px

    lw = kps[_KP_LEFT_WRIST]
    rw = kps[_KP_RIGHT_WRIST]
    ok_l = lw[2] >= kp_conf_thresh and lw[1] < thresh_y
    ok_r = rw[2] >= kp_conf_thresh and rw[1] < thresh_y

    wrist_ys_above = []
    if ok_l:
        wrist_ys_above.append(lw[1])
    if ok_r:
        wrist_ys_above.append(rw[1])
    best = min(wrist_ys_above) if wrist_ys_above else None

    if require_both_wrists:
        ok = (
            lw[2] >= kp_conf_thresh
            and rw[2] >= kp_conf_thresh
            and lw[1] < thresh_y
            and rw[1] < thresh_y
        )
        return ok, head_ref_y, best

    ok = ok_l or ok_r
    return ok, head_ref_y, best


@dataclass
class FenceClimbingPoseGatedDetectionConfig(FenceClimbingDetectionConfig):
    """Adds pose gating thresholds on top of `FenceClimbingDetectionConfig`."""

    pose_keypoint_confidence_threshold: float = 0.25
    hands_above_head_margin_px: float = 0.0
    """Positive values require wrists further above facial landmarks (stricter gate)."""

    require_both_wrists_above_head: bool = False

    def validate(self) -> List[str]:
        errors = super().validate()
        if not 0.0 <= self.pose_keypoint_confidence_threshold <= 1.0:
            errors.append("pose_keypoint_confidence_threshold must be between 0.0 and 1.0")
        if self.hands_above_head_margin_px < 0:
            errors.append("hands_above_head_margin_px must be >= 0")
        return errors


class FenceClimbingPoseGatedDetectionUseCase(FenceClimbingDetectionUseCase):
    """
    Fence climbing use case requiring raised hands above head from pose keypoints.
    """

    def __init__(self) -> None:
        FenceClimbingDetectionUseCase.__init__(self)
        self.name = "fence_climbing_detection_pose"
        self.CASE_TYPE = "fence_climbing_detection_pose"
        self.CASE_VERSION = "1.4"

    def get_config_schema(self) -> Dict[str, Any]:
        schema = FenceClimbingDetectionUseCase.get_config_schema(self)
        props = schema.get("properties") or {}
        props["pose_keypoint_confidence_threshold"] = {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "default": 0.25,
            "description": "Minimum landmark confidence before using it for wrist/head geometry",
        }
        props["hands_above_head_margin_px"] = {
            "type": "number",
            "minimum": 0.0,
            "default": 0.0,
            "description": "Extra clearance (pixels) above facial landmarks — larger is stricter",
        }
        props["require_both_wrists_above_head"] = {
            "type": "boolean",
            "default": False,
            "description": "Require both wrists above head (when both landmarks meet confidence)",
        }
        schema["properties"] = props
        return schema

    def create_default_config(self, **overrides: Any) -> FenceClimbingPoseGatedDetectionConfig:
        raw = FenceClimbingDetectionUseCase.create_default_config(self, **overrides)
        payload = asdict(raw)
        payload.update(overrides)
        return FenceClimbingPoseGatedDetectionConfig(**payload)

    # ------------------------------------------------------------------ #
    # Zone tracking — clone of parent with pose gate before tagging event
    # ------------------------------------------------------------------ #

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: FenceClimbingDetectionConfig,
    ) -> Dict[str, Dict[str, Any]]:
        if config.zone_config and config.zone_config.zones:
            zones = config.zone_config.zones
        else:
            return {}

        if not isinstance(config, FenceClimbingPoseGatedDetectionConfig):
            self.logger.warning(
                "FenceClimbingPose: expected FenceClimbingPoseGatedDetectionConfig; "
                "using default pose thresholds"
            )
            config = FenceClimbingPoseGatedDetectionConfig(**asdict(config))

        enhanced_zone_analysis: Dict[str, Dict[str, Any]] = {}
        current_frame_zone_tracks: Dict[str, set] = {}

        for zone_name in zones:
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()
            if zone_name not in self._zone_alerted_tracks:
                self._zone_alerted_tracks[zone_name] = set()
            if zone_name not in self._zone_inside_frames:
                self._zone_inside_frames[zone_name] = {}
            if zone_name not in self._zone_outside_frames:
                self._zone_outside_frames[zone_name] = {}
            if zone_name not in self._zone_track_initial_y:
                self._zone_track_initial_y[zone_name] = {}

        min_vert = config.min_vertical_displacement
        kp_thresh = config.pose_keypoint_confidence_threshold
        margin_px = config.hands_above_head_margin_px
        both_wrists = config.require_both_wrists_above_head

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            pose_ok, head_y, wrist_y = hands_raised_above_head(
                detection,
                kp_conf_thresh=kp_thresh,
                margin_px=margin_px,
                require_both_wrists=both_wrists,
            )

            center_point = get_bbox_bottom25_center(bbox)
            _, current_center_y = get_bbox_center(bbox)

            for zone_name, zone_polygon in zones.items():
                polygon_points = [(pt[0], pt[1]) for pt in zone_polygon]

                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)

                    prev = self._zone_inside_frames[zone_name].get(track_id, 0)
                    self._zone_inside_frames[zone_name][track_id] = prev + 1
                    self._zone_outside_frames[zone_name].pop(track_id, None)

                    if track_id not in self._zone_track_initial_y[zone_name]:
                        self._zone_track_initial_y[zone_name][track_id] = current_center_y

                    inside_count = self._zone_inside_frames[zone_name][track_id]

                    if (
                        inside_count >= config.min_climbing_frames
                        and track_id not in self._zone_alerted_tracks[zone_name]
                        and pose_ok
                    ):
                        initial_y = self._zone_track_initial_y[zone_name].get(track_id, current_center_y)
                        vertical_displacement = abs(current_center_y - initial_y)

                        if vertical_displacement >= min_vert:
                            detection["_fence_climbing_event"] = {
                                "zone_name": zone_name,
                                "track_id": track_id,
                                "vertical_displacement": round(vertical_displacement, 1),
                                "pose_head_reference_y": None if head_y is None else round(head_y, 2),
                                "pose_wrist_y_min": None if wrist_y is None else round(wrist_y, 2),
                            }
                else:
                    outside = self._zone_outside_frames[zone_name].get(track_id, 0) + 1
                    self._zone_outside_frames[zone_name][track_id] = outside

                    if outside >= config.exit_grace_frames and track_id not in current_frame_zone_tracks[zone_name]:
                        self._zone_inside_frames[zone_name].pop(track_id, None)
                        self._zone_outside_frames[zone_name].pop(track_id, None)
                        self._zone_alerted_tracks[zone_name].discard(track_id)
                        self._zone_track_initial_y[zone_name].pop(track_id, None)

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
