"""Auto-generated stub for module: strack."""
from typing import Any, List, Optional

from .base import BaseTrack, TrackState
from .kalman_filter import KalmanFilterXYAH

# Functions
def xywh2ltwh(xywh: List[float]) -> List[float]:
    """
    Convert bounding box from center format (x, y, w, h) to top-left format (x, y, w, h).
    
    Args:
        xywh (List[float]): Bounding box in center format [x, y, w, h]
    
    Returns:
        List[float]: Bounding box in top-left format [x, y, w, h]
    """
    ...

# Classes
class STrack:
    # Single object tracking representation that uses Kalman filtering for state estimation.
    #
    # This class is responsible for storing all the information regarding individual tracklets and performs state updates
    # and predictions based on Kalman filter.
    #
    # Attributes:
    #     shared_kalman (KalmanFilterXYAH): Shared Kalman filter used across all STrack instances for prediction.
    #     _tlwh (np.ndarray): Private attribute to store top-left corner coordinates and width and height of bounding box.
    #     kalman_filter (KalmanFilterXYAH): Instance of Kalman filter used for this particular object track.
    #     mean (np.ndarray): Mean state estimate vector.
    #     covariance (np.ndarray): Covariance of state estimate.
    #     is_activated (bool): Boolean flag indicating if the track has been activated.
    #     score (float): Confidence score of the track.
    #     tracklet_len (int): Length of the tracklet.
    #     cls (Any): Class label for the object.
    #     idx (int): Index or identifier for the object.
    #     frame_id (int): Current frame ID.
    #     start_frame (int): Frame where the object was first detected.
    #     angle (float or None): Optional angle information for oriented bounding boxes.

    def __init__(self: Any, xywh: List[float], score: float, cls: Any) -> None:
        """
        Initialize a new STrack instance.
        
        Args:
            xywh (List[float]): Bounding box coordinates and dimensions in the format (x, y, w, h, [a], idx), where
                (x, y) is the center, (w, h) are width and height, [a] is optional aspect ratio, and idx is the id.
            score (float): Confidence score of the detection.
            cls (Any): Class label for the detected object.
        """
        ...

    shared_kalman: Any

    def activate(self: Any, kalman_filter: Any, frame_id: int) -> Any:
        """
        Activate a new tracklet using the provided Kalman filter and initialize its state and covariance.
        """
        ...

    def convert_coords(self: Any, tlwh: Any.Any) -> Any.Any:
        """
        Convert a bounding box's top-left-width-height format to its x-y-aspect-height equivalent.
        """
        ...

    def multi_gmc(stracks: List['Any'], H: Any.Any = np.eye(2, 3)) -> Any:
        """
        Update state tracks positions and covariances using a homography matrix for multiple tracks.
        """
        ...

    def multi_kf_update(tracks: List['Any'], new_tracks: List['Any']) -> Any:
        """
        Run the Kalman correction for N matched (track, detection) pairs in ONE
                batched call — the math of update()/re_activate() without the per-track
                bookkeeping (the caller still branches on track.state for that, see
                AdvancedTracker._apply_matches). All tracks in a tracker share one
                kalman_filter instance; profiling showed the per-track update round-trips
                were the largest remaining tracker cost (~0.33 ms/frame at 10 tracks).
        """
        ...

    def multi_predict(stracks: List['Any'], kalman_filter: Optional['Any'] = None) -> Any:
        """
        Perform multi-object predictive tracking using Kalman filter for the provided list of STrack instances.
        
                Args:
                    stracks: tracks to predict forward in place.
                    kalman_filter: filter to predict with. Defaults to the shared singleton
                        (dt=1.0). Callers pass their own instance so per-tracker FPS
                        adaptation rescales dt without mutating global state; at dt=1.0 the
                        result is identical to the shared filter.
        """
        ...

    def predict(self: Any) -> Any:
        """
        Predict the next state (mean and covariance) of the object using the Kalman filter.
        """
        ...

    def re_activate(self: Any, new_track: 'Any', frame_id: int, new_id: bool = False) -> Any:
        """
        Reactivate a previously lost track using new detection data and update its state and attributes.
        """
        ...

    def result(self: Any) -> List[float]:
        """
        Get the current tracking results in the appropriate bounding box format.
        """
        ...

    def tlwh(self: Any) -> Any.Any:
        """
        Get the bounding box in top-left-width-height format from the current state estimate.
        """
        ...

    def tlwh_to_xyah(tlwh: Any.Any) -> Any.Any:
        """
        Convert bounding box from tlwh format to center-x-center-y-aspect-height (xyah) format.
        """
        ...

    def update(self: Any, new_track: 'Any', frame_id: int) -> Any:
        """
        Update the state of a matched track.
        
        Args:
            new_track (STrack): The new track containing updated information.
            frame_id (int): The ID of the current frame.
        """
        ...

    def xywh(self: Any) -> Any.Any:
        """
        Get the current position of the bounding box in (center x, center y, width, height) format.
        """
        ...

    def xywha(self: Any) -> Any.Any:
        """
        Get position in (center x, center y, width, height, angle) format, warning if angle is missing.
        """
        ...

    def xyxy(self: Any) -> Any.Any:
        """
        Convert bounding box from (top left x, top left y, width, height) to (min x, min y, max x, max y) format.
        """
        ...

    def xyxy_matrix(tracks: List['Any']) -> Any.Any:
        """
        Vectorized (N, 4) xyxy boxes for a list of STracks — one stacked
                computation instead of N property calls (the matcher's hottest loop).
        
                Row-for-row bitwise identical to [t.xyxy for t in tracks]: the same
                elementwise ops run on a stacked matrix. Lists are homogeneous in
                practice (track pools all have a KF mean; fresh detections have none);
                a mixed list falls back to the per-row property.
        """
        ...

