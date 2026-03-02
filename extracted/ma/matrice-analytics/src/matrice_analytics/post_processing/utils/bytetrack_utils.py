from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    from yolox.tracker.byte_tracker import BYTETracker
except Exception:
    BYTETracker = None
    
import tempfile
from pathlib import Path
import yaml


def validate_bytetrack_cfg(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate + sanitize an Ultralytics ByteTrack YAML config dict.

    Returns:
        A cleaned cfg dict (safe types + clamped thresholds).
    Raises:
        ValueError if mandatory keys are missing or invalid beyond repair.
    """

    if not isinstance(cfg, dict):
        raise ValueError("ByteTrack cfg must be a dict")

    # Required key
    tracker_type = str(cfg.get("tracker_type", "bytetrack")).strip().lower()
    if tracker_type not in {"bytetrack"}:
        raise ValueError(f"Invalid tracker_type='{tracker_type}', expected 'bytetrack'")

    def _to_int(key: str, default: int, minv: int = 1, maxv: int = 10_000) -> int:
        v = cfg.get(key, default)
        try:
            v = int(v)
        except Exception:
            v = int(default)
        v = max(minv, min(maxv, v))
        return v

    def _to_float01(key: str, default: float) -> float:
        v = cfg.get(key, default)
        try:
            v = float(v)
        except Exception:
            v = float(default)
        # clamp [0..1]
        v = max(0.0, min(1.0, v))
        return v

    def _to_bool(key: str, default: bool) -> bool:
        v = cfg.get(key, default)
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.strip().lower() in {"1", "true", "yes", "y", "on"}
        return bool(default)

    cleaned: Dict[str, Any] = dict(cfg)

    cleaned["tracker_type"] = tracker_type
    cleaned["track_buffer"] = _to_int("track_buffer", 120, minv=1, maxv=5000)
    cleaned["match_thresh"] = _to_float01("match_thresh", 0.88)

    cleaned["track_high_thresh"] = _to_float01("track_high_thresh", 0.25)
    cleaned["track_low_thresh"] = _to_float01("track_low_thresh", 0.10)
    cleaned["new_track_thresh"] = _to_float01("new_track_thresh", 0.28)

    cleaned["fuse_score"] = _to_bool("fuse_score", True)

    # Logical consistency: low <= new <= high is typical, enforce softly
    lo = float(cleaned["track_low_thresh"])
    new = float(cleaned["new_track_thresh"])
    hi = float(cleaned["track_high_thresh"])

    if lo > hi:
        lo, hi = hi, lo
    if new < lo:
        new = lo
    if new > hi:
        new = hi

    cleaned["track_low_thresh"] = float(lo)
    cleaned["new_track_thresh"] = float(new)
    cleaned["track_high_thresh"] = float(hi)
    
    required = [
        "tracker_type",
        "track_buffer",
        "match_thresh",
        "fuse_score",
        "track_high_thresh",
        "track_low_thresh",
        "new_track_thresh",
    ]
    for k in required:
        if k not in cleaned:
            raise ValueError(f"Missing required bytetrack cfg key: {k}")

    return cleaned

    
def make_runtime_bytetrack_config(
    *,
    output_path: Optional[str] = None,
    tracker_type: str = "bytetrack",
    track_buffer: int = 120,
    match_thresh: float = 0.88,
    fuse_score: bool = True,
    track_high_thresh: float = 0.25,
    track_low_thresh: float = 0.10,
    new_track_thresh: float = 0.28,
    extra_cfg: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Create a temporary runtime ByteTrack YAML config for Ultralytics YOLO.track().
    Returns:
        str: YAML path that can be passed into YOLO.track(tracker=...)
    """
    cfg: Dict[str, Any] = {
        "tracker_type": str(tracker_type),
        "track_buffer": int(track_buffer),
        "match_thresh": float(match_thresh),
        "fuse_score": bool(fuse_score),
        "track_high_thresh": float(track_high_thresh),
        "track_low_thresh": float(track_low_thresh),
        "new_track_thresh": float(new_track_thresh),
    }
        
    if isinstance(extra_cfg, dict) and extra_cfg:
        cfg.update(extra_cfg)

    cfg = validate_bytetrack_cfg(cfg)

    if output_path:
        cfg_path = Path(output_path)
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        temp_dir = tempfile.mkdtemp(prefix="runtime_tracker_")
        cfg_path = Path(temp_dir) / "bytetrack_runtime.yaml"

    cfg_path.write_text(yaml.safe_dump(cfg))
    return str(cfg_path)



# =============================================================================
# BBox / Geometry Helpers
# =============================================================================
def bbox_to_xyxy(bbox: Dict[str, Any]) -> Tuple[float, float, float, float]:
    """
    Supports both:
      - Matrice: xmin,ymin,xmax,ymax
      - Alternate: x1,y1,x2,y2
    """
    if not isinstance(bbox, dict):
        return (0.0, 0.0, 0.0, 0.0)

    if "xmin" in bbox:
        return (
            float(bbox.get("xmin", 0.0)),
            float(bbox.get("ymin", 0.0)),
            float(bbox.get("xmax", 0.0)),
            float(bbox.get("ymax", 0.0)),
        )

    return (
        float(bbox.get("x1", 0.0)),
        float(bbox.get("y1", 0.0)),
        float(bbox.get("x2", 0.0)),
        float(bbox.get("y2", 0.0)),
    )


def bbox_centroid(bbox: Dict[str, Any]) -> Tuple[float, float]:
    x1, y1, x2, y2 = bbox_to_xyxy(bbox)
    return ((x1 + x2) * 0.5, (y1 + y2) * 0.5)


def bbox_feet_point(bbox: Dict[str, Any]) -> Tuple[float, float]:
    x1, y1, x2, y2 = bbox_to_xyxy(bbox)
    x = (x1 + x2) * 0.5
    y = y2 - 0.10 * (y2 - y1)
    return (x, y)


def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return float(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5)


def smooth_point(prev: Tuple[float, float], new: Tuple[float, float], alpha: float) -> Tuple[float, float]:
    a = float(max(0.0, min(1.0, alpha)))
    return (prev[0] * (1 - a) + new[0] * a, prev[1] * (1 - a) + new[1] * a)


def iou_xyxy(a: np.ndarray, b: np.ndarray) -> float:
    x1 = max(float(a[0]), float(b[0]))
    y1 = max(float(a[1]), float(b[1]))
    x2 = min(float(a[2]), float(b[2]))
    y2 = min(float(a[3]), float(b[3]))

    iw = max(0.0, x2 - x1)
    ih = max(0.0, y2 - y1)
    inter = iw * ih

    area_a = max(0.0, float(a[2] - a[0])) * max(0.0, float(a[3] - a[1]))
    area_b = max(0.0, float(b[2] - b[0])) * max(0.0, float(b[3] - b[1]))
    union = area_a + area_b - inter
    return float(inter / union) if union > 1e-9 else 0.0


def bbox_iou(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    ax1, ay1, ax2, ay2 = bbox_to_xyxy(a)
    bx1, by1, bx2, by2 = bbox_to_xyxy(b)

    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)

    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0

    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = max(1e-6, area_a + area_b - inter)
    return float(inter / union)


# =============================================================================
# SORT Tracker (True SORT: Kalman + Hungarian)
# =============================================================================
def _xyxy_to_z(box: np.ndarray) -> np.ndarray:
    x1, y1, x2, y2 = box.astype(np.float64)
    w = max(1e-6, x2 - x1)
    h = max(1e-6, y2 - y1)
    x = x1 + w / 2.0
    y = y1 + h / 2.0
    s = w * h
    r = w / h
    return np.array([[x], [y], [s], [r]], dtype=np.float64)


def _x_to_xyxy(x: np.ndarray) -> np.ndarray:
    x_c = float(x[0])
    y_c = float(x[1])
    s = max(1e-6, float(x[2]))
    r = max(1e-6, float(x[3]))

    w = np.sqrt(s * r)
    h = s / max(1e-6, w)

    x1 = x_c - w / 2.0
    y1 = y_c - h / 2.0
    x2 = x_c + w / 2.0
    y2 = y_c + h / 2.0
    return np.array([x1, y1, x2, y2], dtype=np.float64)


class _KalmanBoxTracker:
    def __init__(self, bbox_xyxy: np.ndarray, track_id: int):
        self.track_id = int(track_id)
        self.time_since_update = 0
        self.hits = 0
        self.hit_streak = 0
        self.age = 0

        self.dim_x = 7
        self.dim_z = 4

        self.x = np.zeros((self.dim_x, 1), dtype=np.float64)
        self.x[:4] = _xyxy_to_z(bbox_xyxy)

        self.P = np.eye(self.dim_x, dtype=np.float64) * 10.0
        self.P[4:, 4:] *= 1000.0

        self.F = np.eye(self.dim_x, dtype=np.float64)
        self.F[0, 4] = 1.0
        self.F[1, 5] = 1.0
        self.F[2, 6] = 1.0

        self.H = np.zeros((self.dim_z, self.dim_x), dtype=np.float64)
        self.H[0, 0] = 1.0
        self.H[1, 1] = 1.0
        self.H[2, 2] = 1.0
        self.H[3, 3] = 1.0

        self.Q = np.eye(self.dim_x, dtype=np.float64) * 1e-2
        self.Q[4:, 4:] *= 1e-1
        self.R = np.eye(self.dim_z, dtype=np.float64) * 1e-1

        self.last_bbox_xyxy = bbox_xyxy.astype(np.float64)

    def predict(self) -> np.ndarray:
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        self.age += 1
        self.time_since_update += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        pred = _x_to_xyxy(self.x)
        self.last_bbox_xyxy = pred
        return pred

    def update(self, bbox_xyxy: np.ndarray) -> None:
        z = _xyxy_to_z(bbox_xyxy)
        y = z - (self.H @ self.x)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)

        self.x = self.x + K @ y
        I = np.eye(self.dim_x, dtype=np.float64)
        self.P = (I - K @ self.H) @ self.P

        self.time_since_update = 0
        self.hits += 1
        self.hit_streak += 1

        upd = _x_to_xyxy(self.x)
        self.last_bbox_xyxy = upd


def _hungarian_min_cost(cost: np.ndarray) -> List[Tuple[int, int]]:
    """
    Your implementation unchanged.
    Keeping it here for full self-contained SORTTracker.
    """
    cost = np.asarray(cost, dtype=np.float64)
    n, m = cost.shape
    size = max(n, m)

    padded = np.full((size, size), fill_value=cost.max() + 1.0, dtype=np.float64)
    padded[:n, :m] = cost

    padded -= padded.min(axis=1, keepdims=True)
    padded -= padded.min(axis=0, keepdims=True)

    mask = np.zeros((size, size), dtype=np.int32)
    row_cover = np.zeros(size, dtype=bool)
    col_cover = np.zeros(size, dtype=bool)

    for i in range(size):
        for j in range(size):
            if padded[i, j] == 0 and (not row_cover[i]) and (not col_cover[j]):
                mask[i, j] = 1
                row_cover[i] = True
                col_cover[j] = True

    row_cover[:] = False
    col_cover[:] = False

    def _cover_columns_with_stars():
        col_cover[:] = False
        for j in range(size):
            if np.any(mask[:, j] == 1):
                col_cover[j] = True

    def _find_a_zero():
        for i in range(size):
            if row_cover[i]:
                continue
            for j in range(size):
                if col_cover[j]:
                    continue
                if padded[i, j] == 0:
                    return i, j
        return None

    def _find_star_in_row(r: int):
        c = np.where(mask[r] == 1)[0]
        return int(c[0]) if len(c) else None

    def _find_star_in_col(c: int):
        r = np.where(mask[:, c] == 1)[0]
        return int(r[0]) if len(r) else None

    def _find_prime_in_row(r: int):
        c = np.where(mask[r] == 2)[0]
        return int(c[0]) if len(c) else None

    def _augment_path(path: List[Tuple[int, int]]):
        for r, c in path:
            if mask[r, c] == 1:
                mask[r, c] = 0
            elif mask[r, c] == 2:
                mask[r, c] = 1

    def _clear_primes():
        mask[mask == 2] = 0

    _cover_columns_with_stars()

    while col_cover.sum() < size:
        z = _find_a_zero()
        while z is None:
            uncovered = padded[~row_cover][:, ~col_cover]
            if uncovered.size == 0:
                break
            minval = uncovered.min()
            padded[row_cover] += minval
            padded[:, ~col_cover] -= minval
            z = _find_a_zero()

        if z is None:
            break

        r, c = z
        mask[r, c] = 2

        star_c = _find_star_in_row(r)
        if star_c is None:
            path = [(r, c)]
            while True:
                star_r = _find_star_in_col(path[-1][1])
                if star_r is None:
                    break
                path.append((star_r, path[-1][1]))
                prime_c = _find_prime_in_row(path[-1][0])
                path.append((path[-1][0], prime_c))

            _augment_path(path)
            row_cover[:] = False
            col_cover[:] = False
            _clear_primes()
            _cover_columns_with_stars()
        else:
            row_cover[r] = True
            col_cover[star_c] = False

    assignments: List[Tuple[int, int]] = []
    for i in range(n):
        j_star = np.where(mask[i, :m] == 1)[0]
        if len(j_star):
            assignments.append((i, int(j_star[0])))
    return assignments


class SORTTracker:
    def __init__(self, iou_threshold: float = 0.25, max_age: int = 30, min_hits: int = 2):
        self.iou_threshold = float(iou_threshold)
        self.max_age = int(max_age)
        self.min_hits = int(min_hits)
        self._next_id = 1
        self._trackers: List[_KalmanBoxTracker] = []

    def _det_to_xyxy(self, det: Dict[str, Any]) -> Optional[np.ndarray]:
        bb = det.get("bounding_box") or det.get("bbox")
        if not isinstance(bb, dict):
            return None
        x1, y1, x2, y2 = bbox_to_xyxy(bb)
        return np.array([x1, y1, x2, y2], dtype=np.float64)

    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        dets = [d for d in (detections or []) if isinstance(d, dict)]
        if not dets:
            for trk in self._trackers:
                trk.predict()
            self._trackers = [t for t in self._trackers if t.time_since_update <= self.max_age]
            return dets

        det_boxes, valid_indices = [], []
        for i, d in enumerate(dets):
            b = self._det_to_xyxy(d)
            if b is not None:
                det_boxes.append(b)
                valid_indices.append(i)

        if not det_boxes:
            for trk in self._trackers:
                trk.predict()
            self._trackers = [t for t in self._trackers if t.time_since_update <= self.max_age]
            return dets

        det_boxes_np = np.stack(det_boxes, axis=0)

        trk_boxes = [trk.predict() for trk in self._trackers]
        trk_boxes_np = np.stack(trk_boxes, axis=0) if trk_boxes else np.zeros((0, 4), dtype=np.float64)

        matches: List[Tuple[int, int]] = []
        unmatched_det = list(range(len(det_boxes_np)))

        if len(trk_boxes_np) > 0:
            iou_mat = np.zeros((len(det_boxes_np), len(trk_boxes_np)), dtype=np.float64)
            for di in range(len(det_boxes_np)):
                for ti in range(len(trk_boxes_np)):
                    iou_mat[di, ti] = iou_xyxy(det_boxes_np[di], trk_boxes_np[ti])

            cost = 1.0 - iou_mat
            assignment = _hungarian_min_cost(cost)

            matched_d, matched_t = set(), set()
            for di, ti in assignment:
                if iou_mat[di, ti] < self.iou_threshold:
                    continue
                matches.append((di, ti))
                matched_d.add(di)
                matched_t.add(ti)

            unmatched_det = [i for i in range(len(det_boxes_np)) if i not in matched_d]

        for di, ti in matches:
            trk = self._trackers[ti]
            trk.update(det_boxes_np[di])
            det_idx = valid_indices[di]
            dets[det_idx]["track_id"] = int(trk.track_id)

        for di in unmatched_det:
            bbox = det_boxes_np[di]
            tid = self._next_id
            self._next_id += 1
            trk = _KalmanBoxTracker(bbox, track_id=tid)
            trk.hits = 1
            trk.hit_streak = 1
            trk.time_since_update = 0
            self._trackers.append(trk)

            det_idx = valid_indices[di]
            dets[det_idx]["track_id"] = int(tid)

        self._trackers = [t for t in self._trackers if t.time_since_update <= self.max_age]

        for d in dets:
            if "track_id" not in d:
                d["track_id"] = -1

        return dets


# =============================================================================
# YOLOX ByteTrack Wrapper
# =============================================================================
def matrice_dets_to_xyxy_score(dets: List[Dict[str, Any]]) -> np.ndarray:
    if not dets:
        return np.zeros((0, 5), dtype=np.float32)

    rows = []
    for d in dets:
        bb = d.get("bounding_box") or d.get("bbox") or {}
        x1, y1, x2, y2 = bbox_to_xyxy(bb)
        score = float(d.get("confidence", 0.0))
        rows.append([x1, y1, x2, y2, score])

    return np.asarray(rows, dtype=np.float32)

def ultralytics_track_to_matrice_dets(
    results: Any,
    person_class_id: int = 0,
) -> List[Dict[str, Any]]:
    """
    Convert ultralytics YOLO.track() output to Matrice detections list.

    Output schema:
    {
      "track_id": int,
      "confidence": float,
      "category": str (class id as string),
      "bounding_box": {"xmin","ymin","xmax","ymax"}
    }
    """
    dets: List[Dict[str, Any]] = []
    if results is None or len(results) == 0:
        return dets

    r0 = results[0]
    if getattr(r0, "boxes", None) is None:
        return dets

    boxes = r0.boxes
    xyxy = boxes.xyxy.cpu().numpy() if getattr(boxes, "xyxy", None) is not None else None
    conf = boxes.conf.cpu().numpy() if getattr(boxes, "conf", None) is not None else None
    cls = boxes.cls.cpu().numpy() if getattr(boxes, "cls", None) is not None else None

    ids = None
    try:
        ids = boxes.id.cpu().numpy() if getattr(boxes, "id", None) is not None else None
    except Exception:
        ids = None

    if xyxy is None or conf is None or cls is None or ids is None:
        return dets

    for i in range(len(xyxy)):
        if int(cls[i]) != int(person_class_id):
            continue

        x1, y1, x2, y2 = map(float, xyxy[i])
        dets.append(
            {
                "track_id": int(ids[i]),
                "confidence": float(conf[i]),
                "category": str(int(cls[i])),  # map later using index_to_category
                "bounding_box": {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2},
            }
        )

    return dets


@dataclass
class ByteTrackArgs:
    track_thresh: float = 0.25
    match_thresh: float = 0.80
    track_buffer: int = 30
    mot20: bool = False


class ByteTrackWrapper:
    """
    Wrapper around YOLOX BYTETracker.

    NOTE:
    - This is NOT the same as ultralytics ByteTrack
    - It assigns track_id to detections by IoU matching
    """

    def __init__(
        self,
        fps: float = 30.0,
        track_thresh: float = 0.25,
        match_thresh: float = 0.80,
        track_buffer: int = 30,
    ):
        if BYTETracker is None:
            raise ImportError("BYTETracker not found. Install yolox: pip install yolox==0.3.0")

        self.fps = float(fps)
        self.args = ByteTrackArgs(
            track_thresh=float(track_thresh),
            match_thresh=float(match_thresh),
            track_buffer=int(track_buffer),
            mot20=False,
        )
        self.tracker = BYTETracker(self.args, frame_rate=self.fps)

    def update(self, dets: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        img_h, img_w = 0, 0
        try:
            if stream_info:
                res = stream_info.get("input_settings", {}).get("stream_resolution")
                if isinstance(res, (list, tuple)) and len(res) == 2:
                    img_w, img_h = int(res[0]), int(res[1])
        except Exception:
            img_h, img_w = 0, 0

        dets_arr = matrice_dets_to_xyxy_score(dets)

        if dets_arr.shape[0] == 0:
            self.tracker.update(
                np.zeros((0, 5), dtype=np.float32),
                img_info=(img_h, img_w),
                img_size=(img_h, img_w),
            )
            return dets

        online_targets = self.tracker.update(dets_arr, img_info=(img_h, img_w), img_size=(img_h, img_w))

        track_map: List[Tuple[np.ndarray, int]] = []
        for t in online_targets:
            tlwh = t.tlwh
            x, y, w, h = float(tlwh[0]), float(tlwh[1]), float(tlwh[2]), float(tlwh[3])
            x1, y1 = x, y
            x2, y2 = x + w, y + h
            track_map.append((np.array([x1, y1, x2, y2], dtype=np.float32), int(t.track_id)))

        for d in dets:
            bb = d.get("bounding_box") or d.get("bbox") or {}
            x1, y1, x2, y2 = bbox_to_xyxy(bb)
            det_box = np.array([x1, y1, x2, y2], dtype=np.float32)

            best_iou, best_tid = 0.0, -1
            for trk_box, tid in track_map:
                iou = iou_xyxy(det_box, trk_box)
                if iou > best_iou:
                    best_iou = iou
                    best_tid = tid

            d["track_id"] = int(best_tid) if best_iou > 0.10 else -1

        return dets