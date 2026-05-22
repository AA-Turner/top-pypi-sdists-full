import logging
from enum import IntEnum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    from scipy.optimize import linear_sum_assignment

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logging.warning("scipy not available - tracker will use greedy matching (less optimal)")

logger = logging.getLogger(__name__)


class TrackState(IntEnum):
    TENTATIVE = 1
    CONFIRMED = 2
    LOST = 3
    REMOVED = 4


class KalmanFilterXYAH:
    """Kalman filter for bbox tracking (center_x, center_y, aspect_ratio, height)."""

    def __init__(self):
        ndim, dt = 4, 1.0
        self._motion_mat = np.eye(2 * ndim, 2 * ndim)
        for i in range(ndim):
            self._motion_mat[i, ndim + i] = dt
        self._update_mat = np.eye(ndim, 2 * ndim)
        self._std_weight_position = 1.0 / 20
        self._std_weight_velocity = 1.0 / 160

    def initiate(self, measurement: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        mean_pos = measurement
        mean_vel = np.zeros_like(mean_pos)
        mean = np.r_[mean_pos, mean_vel]
        std = [
            2 * self._std_weight_position * measurement[3],
            2 * self._std_weight_position * measurement[3],
            1e-2,
            2 * self._std_weight_position * measurement[3],
            10 * self._std_weight_velocity * measurement[3],
            10 * self._std_weight_velocity * measurement[3],
            1e-5,
            10 * self._std_weight_velocity * measurement[3],
        ]
        covariance = np.diag(np.square(std))
        return mean, covariance

    def predict(self, mean: np.ndarray, covariance: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        std_pos = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-2,
            self._std_weight_position * mean[3],
        ]
        std_vel = [
            self._std_weight_velocity * mean[3],
            self._std_weight_velocity * mean[3],
            1e-5,
            self._std_weight_velocity * mean[3],
        ]
        motion_cov = np.diag(np.square(np.r_[std_pos, std_vel]))
        mean = np.dot(self._motion_mat, mean)
        covariance = np.linalg.multi_dot([self._motion_mat, covariance, self._motion_mat.T]) + motion_cov
        return mean, covariance

    def update(
        self, mean: np.ndarray, covariance: np.ndarray, measurement: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        projected_mean, projected_cov = self.project(mean, covariance)
        if SCIPY_AVAILABLE:
            try:
                import scipy.linalg

                chol_factor, lower = scipy.linalg.cho_factor(projected_cov, lower=True, check_finite=False)
                kalman_gain = scipy.linalg.cho_solve(
                    (chol_factor, lower),
                    np.dot(covariance, self._update_mat.T).T,
                    check_finite=False,
                ).T
            except Exception:
                kalman_gain = np.dot(covariance, self._update_mat.T) @ np.linalg.pinv(projected_cov)
        else:
            kalman_gain = np.dot(covariance, self._update_mat.T) @ np.linalg.pinv(projected_cov)
        innovation = measurement - projected_mean
        new_mean = mean + np.dot(innovation, kalman_gain.T)
        new_covariance = covariance - np.linalg.multi_dot([kalman_gain, projected_cov, kalman_gain.T])
        return new_mean, new_covariance

    def project(self, mean: np.ndarray, covariance: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        std = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-1,
            self._std_weight_position * mean[3],
        ]
        innovation_cov = np.diag(np.square(std))
        mean = np.dot(self._update_mat, mean)
        covariance = np.linalg.multi_dot([self._update_mat, covariance, self._update_mat.T])
        return mean, covariance + innovation_cov


class _STrack:
    """Internal track with Kalman filtering."""

    _count = 0

    def __init__(self, tlwh: np.ndarray, score: float, class_name: str):
        self._tlwh = np.asarray(tlwh, dtype=np.float32)
        self.kalman_filter = None
        self.mean = None
        self.covariance = None
        self.score = score
        self.class_name = class_name
        self.track_id = 0
        self.is_activated = False
        self.state = TrackState.TENTATIVE
        self.frame_id = 0
        self.start_frame = 0
        self.tracklet_len = 0
        self.velocity = np.zeros(4)
        self.original_detection: Optional[Dict] = None

    @classmethod
    def next_id(cls) -> int:
        cls._count += 1
        return cls._count

    @classmethod
    def reset_id(cls):
        cls._count = 0

    def activate(self, kalman_filter: KalmanFilterXYAH, frame_id: int):
        self.kalman_filter = kalman_filter
        self.track_id = self.next_id()
        self.mean, self.covariance = self.kalman_filter.initiate(self._tlwh_to_xyah(self._tlwh))
        self.tracklet_len = 0
        self.state = TrackState.CONFIRMED
        self.is_activated = True
        self.frame_id = frame_id
        self.start_frame = frame_id

    def re_activate(self, new_track: "_STrack", frame_id: int, new_id: bool = False):
        self.mean, self.covariance = self.kalman_filter.update(
            self.mean, self.covariance, self._tlwh_to_xyah(new_track._tlwh)
        )
        self._tlwh = new_track._tlwh
        self.tracklet_len = 0
        self.state = TrackState.CONFIRMED
        self.is_activated = True
        self.frame_id = frame_id
        self.score = new_track.score
        self.class_name = new_track.class_name
        if new_track.original_detection:
            self.original_detection = new_track.original_detection
        if new_id:
            self.track_id = self.next_id()

    def update(self, new_track: "_STrack", frame_id: int):
        self.frame_id = frame_id
        self.tracklet_len += 1
        old_center = self._tlwh[:2] + self._tlwh[2:] / 2
        new_center = new_track._tlwh[:2] + new_track._tlwh[2:] / 2
        self.velocity = 0.7 * self.velocity + 0.3 * np.r_[new_center - old_center, new_track._tlwh[2:] - self._tlwh[2:]]
        self.mean, self.covariance = self.kalman_filter.update(
            self.mean, self.covariance, self._tlwh_to_xyah(new_track._tlwh)
        )
        self._tlwh = new_track._tlwh
        self.state = TrackState.CONFIRMED
        self.is_activated = True
        self.score = new_track.score
        self.class_name = new_track.class_name
        if new_track.original_detection:
            self.original_detection = new_track.original_detection

    def predict(self):
        mean_state = self.mean.copy()
        if self.state != TrackState.CONFIRMED:
            mean_state[7] = 0
        self.mean, self.covariance = self.kalman_filter.predict(mean_state, self.covariance)

    def mark_lost(self):
        self.state = TrackState.LOST

    def mark_removed(self):
        self.state = TrackState.REMOVED

    @staticmethod
    def _tlwh_to_xyah(tlwh: np.ndarray) -> np.ndarray:
        ret = tlwh.copy()
        ret[:2] += ret[2:] / 2
        ret[2] /= max(ret[3], 1e-6)
        return ret

    @property
    def tlwh(self) -> np.ndarray:
        if self.mean is None:
            return self._tlwh.copy()
        ret = self.mean[:4].copy()
        ret[2] *= ret[3]
        ret[:2] -= ret[2:] / 2
        return ret

    @property
    def xyxy(self) -> np.ndarray:
        ret = self.tlwh.copy()
        ret[2:] += ret[:2]
        return ret

    @property
    def end_frame(self) -> int:
        return self.frame_id


def _bbox_iou_vectorized(boxes1: np.ndarray, boxes2: np.ndarray) -> np.ndarray:
    if len(boxes1) == 0 or len(boxes2) == 0:
        return np.zeros((len(boxes1), len(boxes2)), dtype=np.float32)
    tl = np.maximum(boxes1[:, None, :2], boxes2[:, :2])
    br = np.minimum(boxes1[:, None, 2:], boxes2[:, 2:])
    wh = np.maximum(0, br - tl)
    inter = wh[:, :, 0] * wh[:, :, 1]
    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])
    union = area1[:, None] + area2 - inter
    return inter / np.maximum(union, 1e-6)


def _iou_distance(tracks: List[_STrack], detections: List[_STrack]) -> np.ndarray:
    if not tracks or not detections:
        return np.zeros((len(tracks), len(detections)), dtype=np.float32)
    track_boxes = np.array([t.xyxy for t in tracks])
    det_boxes = np.array([d.xyxy for d in detections])
    return 1 - _bbox_iou_vectorized(track_boxes, det_boxes)


def _linear_assignment(cost_matrix: np.ndarray, thresh: float) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
    if cost_matrix.size == 0:
        return [], list(range(cost_matrix.shape[0])), list(range(cost_matrix.shape[1]))

    if SCIPY_AVAILABLE:
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
    else:
        # Greedy fallback
        row_ind, col_ind = [], []
        used_rows, used_cols = set(), set()
        flat_indices = np.argsort(cost_matrix.flatten())
        for idx in flat_indices:
            r, c = divmod(idx, cost_matrix.shape[1])
            if r not in used_rows and c not in used_cols:
                row_ind.append(r)
                col_ind.append(c)
                used_rows.add(r)
                used_cols.add(c)

    matches = []
    unmatched_tracks = set(range(cost_matrix.shape[0]))
    unmatched_dets = set(range(cost_matrix.shape[1]))

    for r, c in zip(row_ind, col_ind):
        if cost_matrix[r, c] <= thresh:
            matches.append((r, c))
            unmatched_tracks.discard(r)
            unmatched_dets.discard(c)

    return matches, list(unmatched_tracks), list(unmatched_dets)


class ProxyAdvancedTracker:
    """
    Production-ready tracker compatible with usecase pipeline.

    Input format (detection dict):
        {
            "bounding_box": {"xmin": float, "ymin": float, "xmax": float, "ymax": float},
            "category": str,
            "confidence": float,
            ...
        }

    Output format (same dict with track_id and frame_id added):
        {
            "bounding_box": {...},
            "category": str,
            "confidence": float,
            "track_id": int,
            "frame_id": int,
            ...
        }
    """

    def __init__(self, iou_threshold: float = 0.3, max_misses: int = 30):
        self.iou_threshold = iou_threshold
        self.max_misses = max_misses
        self.frame_count = 0

        self._kalman_filter = KalmanFilterXYAH()
        self._tracked_stracks: List[_STrack] = []
        self._lost_stracks: List[_STrack] = []

        # Thresholds
        self._high_thresh = 0.5
        self._low_thresh = 0.1
        self._new_track_thresh = 0.3
        self._match_thresh = 1 - iou_threshold

        self.tracks: Dict[int, Dict] = {}

        _STrack.reset_id()
        logger.info(f"ProxyAdvancedTracker initialized (iou={iou_threshold}, max_misses={max_misses})")

    def update(self, detections: List[Dict]) -> List[Dict]:
        """
        Update tracker with detections and return detections with track_id added.

        Args:
            detections: List of detection dicts with bounding_box, category, confidence

        Returns:
            Same detections list with track_id and frame_id fields added to each detection
        """
        self.frame_count += 1

        if not detections:
            for track in self._tracked_stracks:
                track.predict()
            self._handle_lost_tracks()
            return []

        try:
            det_stracks, det_indices = self._create_stracks(detections)

            if not det_stracks:
                logger.debug(f"Frame {self.frame_count}: No valid detections after conversion")
                for det in detections:
                    det["track_id"] = det.get("track_id", -1)
                    det["frame_id"] = self.frame_count
                return detections

            # Run tracking
            matched_pairs = self._run_tracking(det_stracks)

            # Assign track IDs and frame_id to detections
            matched_det_indices = set()
            for det_idx, track in matched_pairs:
                if 0 <= det_idx < len(detections):
                    detections[det_idx]["track_id"] = track.track_id
                    detections[det_idx]["frame_id"] = self.frame_count
                    matched_det_indices.add(det_idx)

            # Assign -1 to unmatched detections, still add frame_id
            for i, det in enumerate(detections):
                if i not in matched_det_indices:
                    if "track_id" not in det:
                        det["track_id"] = -1
                    det["frame_id"] = self.frame_count

            # Update public tracks dict
            self._sync_tracks()

            logger.debug(f"Frame {self.frame_count}: {len(detections)} dets, {len(self._tracked_stracks)} tracks")

        except Exception as e:
            logger.error(f"Tracker update failed at frame {self.frame_count}: {e}")
            # Fallback: assign -1 to all, still add frame_id
            for det in detections:
                det["track_id"] = det.get("track_id", -1)
                det["frame_id"] = self.frame_count

        return detections

    def _extract_bbox(self, det: Dict) -> Optional[Tuple[float, float, float, float]]:
        """Extract bbox coordinates from detection dict. Handles multiple formats."""
        bbox = det.get("bounding_box", det.get("bbox", {}))

        if not bbox:
            return None

        # Format: xmin/ymin/xmax/ymax
        if "xmin" in bbox:
            return (
                float(bbox["xmin"]),
                float(bbox["ymin"]),
                float(bbox["xmax"]),
                float(bbox["ymax"]),
            )

        # Format: x1/y1/x2/y2
        if "x1" in bbox:
            return (
                float(bbox["x1"]),
                float(bbox["y1"]),
                float(bbox["x2"]),
                float(bbox["y2"]),
            )

        # List format
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            return (float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3]))

        return None

    def _create_stracks(self, detections: List[Dict]) -> Tuple[List[_STrack], List[int]]:
        """Convert detection dicts to internal STrack objects."""
        stracks = []
        indices = []

        for i, det in enumerate(detections):
            bbox = self._extract_bbox(det)
            if bbox is None:
                logger.warning(f"Detection {i} has invalid bbox: {det.get('bounding_box')}")
                continue

            x1, y1, x2, y2 = bbox
            w, h = x2 - x1, y2 - y1

            if w <= 0 or h <= 0:
                continue

            tlwh = np.array([x1, y1, w, h], dtype=np.float32)
            score = float(det.get("confidence", 0.5))
            class_name = det.get("category", "unknown")

            strack = _STrack(tlwh, score, class_name)
            strack.original_detection = det.copy()
            stracks.append(strack)
            indices.append(i)

        return stracks, indices

    def _run_tracking(self, det_stracks: List[_STrack]) -> List[Tuple[int, _STrack]]:
        """Run tracking and return (detection_index, track) pairs."""
        matched_pairs = []

        # Separate by confidence
        scores = np.array([d.score for d in det_stracks])
        high_mask = scores >= self._high_thresh
        low_mask = (scores < self._high_thresh) & (scores >= self._low_thresh)

        dets_high = [d for d, m in zip(det_stracks, high_mask) if m]
        dets_low = [d for d, m in zip(det_stracks, low_mask) if m]
        high_indices = [i for i, m in enumerate(high_mask) if m]
        low_indices = [i for i, m in enumerate(low_mask) if m]

        # Predict existing tracks
        strack_pool = [t for t in self._tracked_stracks if t.is_activated] + self._lost_stracks
        for track in strack_pool:
            track.predict()

        # First association: high confidence
        if dets_high and strack_pool:
            dists = _iou_distance(strack_pool, dets_high)
            matches, u_tracks, u_dets = _linear_assignment(dists, thresh=self._match_thresh)

            for t_idx, d_idx in matches:
                track = strack_pool[t_idx]
                det = dets_high[d_idx]
                if track.state == TrackState.LOST:
                    track.re_activate(det, self.frame_count)
                else:
                    track.update(det, self.frame_count)
                matched_pairs.append((high_indices[d_idx], track))

            # Remaining high-conf detections
            remaining_high = [dets_high[i] for i in u_dets]
            remaining_high_indices = [high_indices[i] for i in u_dets]
        else:
            u_tracks = list(range(len(strack_pool)))
            remaining_high = dets_high
            remaining_high_indices = high_indices

        # Second association: low confidence to remaining tracks
        if dets_low and u_tracks:
            remaining_tracks = [strack_pool[i] for i in u_tracks if strack_pool[i].state == TrackState.CONFIRMED]
            if remaining_tracks:
                dists = _iou_distance(remaining_tracks, dets_low)
                matches, _, u_dets_low = _linear_assignment(dists, thresh=0.7)

                for t_idx, d_idx in matches:
                    track = remaining_tracks[t_idx]
                    det = dets_low[d_idx]
                    track.update(det, self.frame_count)
                    matched_pairs.append((low_indices[d_idx], track))

        # Initialize new tracks from unmatched high-conf detections
        for det, det_idx in zip(remaining_high, remaining_high_indices):
            if det.score >= self._new_track_thresh:
                det.activate(self._kalman_filter, self.frame_count)
                self._tracked_stracks.append(det)
                matched_pairs.append((det_idx, det))

        # Handle lost tracks
        self._handle_lost_tracks()

        # Update tracked list
        self._tracked_stracks = [t for t in self._tracked_stracks if t.state == TrackState.CONFIRMED]

        return matched_pairs

    def _handle_lost_tracks(self):
        """Mark unmatched tracks as lost, remove old lost tracks."""
        new_lost = []
        for track in self._tracked_stracks:
            if self.frame_count - track.frame_id > 1:
                track.mark_lost()
                new_lost.append(track)

        self._lost_stracks = [t for t in self._lost_stracks if t.state == TrackState.LOST]
        self._lost_stracks.extend(new_lost)

        # Remove old lost tracks
        self._lost_stracks = [t for t in self._lost_stracks if self.frame_count - t.end_frame <= self.max_misses]

        if len(self._lost_stracks) > 1000:
            self._lost_stracks = self._lost_stracks[-999:]

    def _sync_tracks(self):
        """Sync internal state to public tracks dict."""
        self.tracks.clear()
        for strack in self._tracked_stracks:
            if strack.is_activated:
                self.tracks[strack.track_id] = {
                    "track_id": strack.track_id,
                    "bbox": strack.xyxy.tolist(),
                    "class_name": strack.class_name,
                    "confidence": strack.score,
                    "age": self.frame_count - strack.start_frame,
                }

    def reset(self):
        """Reset tracker state."""
        self.frame_count = 0
        self._tracked_stracks.clear()
        self._lost_stracks.clear()
        self.tracks.clear()
        _STrack.reset_id()
        logger.info("ProxyAdvancedTracker reset")

    def restore_state(self):
        """No-op for compatibility with AdvancedTracker API."""
        pass

    def get_tracker_stats(self) -> Dict[str, Any]:
        """Get tracker statistics."""
        return {
            "frame_count": self.frame_count,
            "active_tracks": len(self._tracked_stracks),
            "lost_tracks": len(self._lost_stracks),
            "total_ids_assigned": _STrack._count,
        }
