"""
STrack class for single object tracking.

This module provides the STrack class that represents a single tracked object
with Kalman filtering for state estimation.
"""

from typing import Any, List, Optional

import numpy as np

from .base import BaseTrack, TrackState
from .kalman_filter import KalmanFilterXYAH


def xywh2ltwh(xywh: List[float]) -> List[float]:
    """
    Convert bounding box from center format (x, y, w, h) to top-left format (x, y, w, h).

    Args:
        xywh (List[float]): Bounding box in center format [x, y, w, h]

    Returns:
        List[float]: Bounding box in top-left format [x, y, w, h]
    """
    x, y, w, h = xywh
    return [x - w / 2, y - h / 2, w, h]


class STrack(BaseTrack):
    """
    Single object tracking representation that uses Kalman filtering for state estimation.

    This class is responsible for storing all the information regarding individual tracklets and performs state updates
    and predictions based on Kalman filter.

    Attributes:
        shared_kalman (KalmanFilterXYAH): Shared Kalman filter used across all STrack instances for prediction.
        _tlwh (np.ndarray): Private attribute to store top-left corner coordinates and width and height of bounding box.
        kalman_filter (KalmanFilterXYAH): Instance of Kalman filter used for this particular object track.
        mean (np.ndarray): Mean state estimate vector.
        covariance (np.ndarray): Covariance of state estimate.
        is_activated (bool): Boolean flag indicating if the track has been activated.
        score (float): Confidence score of the track.
        tracklet_len (int): Length of the tracklet.
        cls (Any): Class label for the object.
        idx (int): Index or identifier for the object.
        frame_id (int): Current frame ID.
        start_frame (int): Frame where the object was first detected.
        angle (float or None): Optional angle information for oriented bounding boxes.
    """

    shared_kalman = KalmanFilterXYAH()

    def __init__(self, xywh: List[float], score: float, cls: Any):
        """
        Initialize a new STrack instance.

        Args:
            xywh (List[float]): Bounding box coordinates and dimensions in the format (x, y, w, h, [a], idx), where
                (x, y) is the center, (w, h) are width and height, [a] is optional aspect ratio, and idx is the id.
            score (float): Confidence score of the detection.
            cls (Any): Class label for the detected object.
        """
        super().__init__()
        # xywh+idx or xywha+idx
        assert len(xywh) in {5, 6}, f"expected 5 or 6 values but got {len(xywh)}"
        self._tlwh = np.asarray(xywh2ltwh(xywh[:4]), dtype=np.float32)
        self.kalman_filter = None
        self.mean, self.covariance = None, None
        # (mean_ref, tlwh, xyxy) memo for the tlwh/xyxy properties. Keyed on the
        # IDENTITY of self.mean: every state change (predict/update/activate/
        # re_activate/multi_predict/multi_gmc) REBINDS self.mean to a new array,
        # never mutates it in place, so `cache[0] is self.mean` is a correct
        # invalidation test. The properties are the matcher's hottest call site
        # (~230 evaluations/frame at 10 tracks) — without the memo each access
        # redoes the slice+copy+arithmetic.
        self._prop_cache = None
        # codeql[py/overwritten-inherited-attribute] — subclass initialization; intentional override of BaseTrack defaults
        self.is_activated = False

        # codeql[py/overwritten-inherited-attribute]
        self.score = score
        self.tracklet_len = 0
        self.cls = cls
        self.idx = xywh[-1]
        self.angle = xywh[4] if len(xywh) == 6 else None

    def predict(self):
        """Predict the next state (mean and covariance) of the object using the Kalman filter."""
        mean_state = self.mean.copy()
        if self.state != TrackState.Tracked:
            mean_state[7] = 0
        self.mean, self.covariance = self.kalman_filter.predict(mean_state, self.covariance)

    @staticmethod
    def xyxy_matrix(tracks: List["STrack"]) -> np.ndarray:
        """Vectorized (N, 4) xyxy boxes for a list of STracks — one stacked
        computation instead of N property calls (the matcher's hottest loop).

        Row-for-row bitwise identical to [t.xyxy for t in tracks]: the same
        elementwise ops run on a stacked matrix. Lists are homogeneous in
        practice (track pools all have a KF mean; fresh detections have none);
        a mixed list falls back to the per-row property.
        """
        n = len(tracks)
        if n == 0:
            return np.zeros((0, 4), dtype=np.float32)
        means = [t.mean for t in tracks]
        if all(m is not None for m in means):
            box = np.stack(means)[:, :4].copy()
            box[:, 2] *= box[:, 3]
            box[:, :2] -= box[:, 2:] / 2
            box[:, 2:] += box[:, :2]
            return box
        if all(m is None for m in means):
            box = np.stack([t._tlwh for t in tracks]).copy()
            box[:, 2:] += box[:, :2]
            return box
        return np.stack([t.xyxy for t in tracks])

    @staticmethod
    def multi_predict(stracks: List["STrack"], kalman_filter: Optional["KalmanFilterXYAH"] = None):
        """Perform multi-object predictive tracking using Kalman filter for the provided list of STrack instances.

        Args:
            stracks: tracks to predict forward in place.
            kalman_filter: filter to predict with. Defaults to the shared singleton
                (dt=1.0). Callers pass their own instance so per-tracker FPS
                adaptation rescales dt without mutating global state; at dt=1.0 the
                result is identical to the shared filter.
        """
        if len(stracks) <= 0:
            return
        kf = kalman_filter if kalman_filter is not None else STrack.shared_kalman
        # np.asarray over a list of distinct (8,) arrays always allocates a fresh
        # 2D matrix, so the previous per-element .copy() was redundant work.
        multi_mean = np.asarray([st.mean for st in stracks])
        multi_covariance = np.asarray([st.covariance for st in stracks])
        for i, st in enumerate(stracks):
            if st.state != TrackState.Tracked:
                multi_mean[i][7] = 0
        multi_mean, multi_covariance = kf.multi_predict(multi_mean, multi_covariance)
        for i, (mean, cov) in enumerate(zip(multi_mean, multi_covariance)):
            stracks[i].mean = mean
            stracks[i].covariance = cov

    @staticmethod
    def multi_gmc(stracks: List["STrack"], H: np.ndarray = np.eye(2, 3)):
        """Update state tracks positions and covariances using a homography matrix for multiple tracks."""
        if len(stracks) > 0:
            multi_mean = np.asarray([st.mean.copy() for st in stracks])
            multi_covariance = np.asarray([st.covariance for st in stracks])

            R = H[:2, :2]
            R8x8 = np.kron(np.eye(4, dtype=float), R)
            t = H[:2, 2]

            for i, (mean, cov) in enumerate(zip(multi_mean, multi_covariance)):
                mean = R8x8.dot(mean)
                mean[:2] += t
                cov = R8x8.dot(cov).dot(R8x8.transpose())

                stracks[i].mean = mean
                stracks[i].covariance = cov

    def activate(self, kalman_filter: KalmanFilterXYAH, frame_id: int):
        """Activate a new tracklet using the provided Kalman filter and initialize its state and covariance."""
        self.kalman_filter = kalman_filter
        # Only assign new ID if not already set (e.g., by track recovery)
        if self.track_id == 0:
            self.track_id = self.next_id()
        self.mean, self.covariance = self.kalman_filter.initiate(self.convert_coords(self._tlwh))

        self.tracklet_len = 0
        self.state = TrackState.Tracked
        # Must always mark activated: _perform_tracking_update returns only is_activated stracks.
        # frame_id==1-only (legacy) left new/recovered tracks invisible on frame 2+, emptying tracker output.
        self.is_activated = True
        self.frame_id = frame_id
        self.start_frame = frame_id

    def re_activate(self, new_track: "STrack", frame_id: int, new_id: bool = False):
        """Reactivate a previously lost track using new detection data and update its state and attributes."""
        self.mean, self.covariance = self.kalman_filter.update(
            self.mean, self.covariance, self.convert_coords(new_track.tlwh)
        )
        self.tracklet_len = 0
        self.state = TrackState.Tracked
        self.is_activated = True
        self.frame_id = frame_id
        if new_id:
            self.track_id = self.next_id()
        self.score = new_track.score
        self.cls = new_track.cls
        self.angle = new_track.angle
        self.idx = new_track.idx

        # CRITICAL FIX: Preserve original detection data for face recognition fields
        if hasattr(new_track, "original_detection"):
            self.original_detection = new_track.original_detection

    def update(self, new_track: "STrack", frame_id: int):
        """
        Update the state of a matched track.

        Args:
            new_track (STrack): The new track containing updated information.
            frame_id (int): The ID of the current frame.
        """
        self.frame_id = frame_id
        self.tracklet_len += 1

        new_tlwh = new_track.tlwh
        self.mean, self.covariance = self.kalman_filter.update(
            self.mean, self.covariance, self.convert_coords(new_tlwh)
        )
        self.state = TrackState.Tracked
        self.is_activated = True

        self.score = new_track.score
        self.cls = new_track.cls
        self.angle = new_track.angle
        self.idx = new_track.idx

        # CRITICAL FIX: Preserve original detection data for face recognition fields
        if hasattr(new_track, "original_detection"):
            self.original_detection = new_track.original_detection

    @staticmethod
    def multi_kf_update(tracks: List["STrack"], new_tracks: List["STrack"]):
        """Run the Kalman correction for N matched (track, detection) pairs in ONE
        batched call — the math of update()/re_activate() without the per-track
        bookkeeping (the caller still branches on track.state for that, see
        AdvancedTracker._apply_matches). All tracks in a tracker share one
        kalman_filter instance; profiling showed the per-track update round-trips
        were the largest remaining tracker cost (~0.33 ms/frame at 10 tracks)."""
        if not tracks:
            return
        kf = tracks[0].kalman_filter or STrack.shared_kalman
        means = np.stack([t.mean for t in tracks])
        covariances = np.stack([t.covariance for t in tracks])
        measurements = np.stack([t.convert_coords(d.tlwh) for t, d in zip(tracks, new_tracks)])
        new_means, new_covs = kf.multi_update(means, covariances, measurements)
        for t, m, c in zip(tracks, new_means, new_covs):
            t.mean = m
            t.covariance = c

    def _post_kf_bookkeeping(self, new_track: "STrack", frame_id: int, reactivate: bool):
        """Everything update()/re_activate(new_id=False) does EXCEPT the KF call —
        used after multi_kf_update() has already corrected mean/covariance."""
        if reactivate:
            self.tracklet_len = 0
        else:
            self.tracklet_len += 1
        self.frame_id = frame_id
        self.state = TrackState.Tracked
        self.is_activated = True
        self.score = new_track.score
        self.cls = new_track.cls
        self.angle = new_track.angle
        self.idx = new_track.idx
        if hasattr(new_track, "original_detection"):
            self.original_detection = new_track.original_detection

    def convert_coords(self, tlwh: np.ndarray) -> np.ndarray:
        """Convert a bounding box's top-left-width-height format to its x-y-aspect-height equivalent."""
        return self.tlwh_to_xyah(tlwh)

    def _box_cache(self):
        """Compute-or-reuse the (tlwh, xyxy) pair for the current self.mean.

        Returns the cached arrays themselves — callers inside the properties
        must .copy() before handing them out so external mutation can't poison
        the cache."""
        m = self.mean
        c = self._prop_cache
        if c is not None and c[0] is m:
            return c
        tlwh = m[:4].copy()
        tlwh[2] *= tlwh[3]
        tlwh[:2] -= tlwh[2:] / 2
        xyxy = tlwh.copy()
        xyxy[2:] += xyxy[:2]
        c = (m, tlwh, xyxy)
        self._prop_cache = c
        return c

    @property
    def tlwh(self) -> np.ndarray:
        """Get the bounding box in top-left-width-height format from the current state estimate."""
        if self.mean is None:
            return self._tlwh.copy()
        return self._box_cache()[1].copy()

    @property
    def xyxy(self) -> np.ndarray:
        """Convert bounding box from (top left x, top left y, width, height) to (min x, min y, max x, max y) format."""
        if self.mean is None:
            ret = self._tlwh.copy()
            ret[2:] += ret[:2]
            return ret
        return self._box_cache()[2].copy()

    @staticmethod
    def tlwh_to_xyah(tlwh: np.ndarray) -> np.ndarray:
        """Convert bounding box from tlwh format to center-x-center-y-aspect-height (xyah) format."""
        ret = np.asarray(tlwh).copy()
        ret[:2] += ret[2:] / 2
        # Guard: zero/negative height makes aspect = width/height diverge to inf, which poisons the
        # Kalman state permanently on the next predict() (inf * 0 -> NaN in the state-transition
        # matmul). Confirmed root cause of persistent NaN bounding boxes downstream.
        ret[3] = max(ret[3], 1e-3)
        ret[2] /= ret[3]
        return ret

    @property
    def xywh(self) -> np.ndarray:
        """Get the current position of the bounding box in (center x, center y, width, height) format."""
        ret = np.asarray(self.tlwh).copy()
        ret[:2] += ret[2:] / 2
        return ret

    @property
    def xywha(self) -> np.ndarray:
        """Get position in (center x, center y, width, height, angle) format, warning if angle is missing."""
        if self.angle is None:
            return self.xywh
        return np.concatenate([self.xywh, self.angle[None]])

    @property
    def result(self) -> List[float]:
        """Get the current tracking results in the appropriate bounding box format."""
        coords = self.xyxy if self.angle is None else self.xywha
        return coords.tolist() + [self.track_id, self.score, self.cls, self.idx]

    def __repr__(self) -> str:
        """Return a string representation of the STrack object including start frame, end frame, and track ID."""
        return f"OT_{self.track_id}_({self.start_frame}-{self.end_frame})"
