"""Stub file for post_processing.advanced_tracker directory."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from .base import BaseTrack, TrackState
from .config import TrackerConfig
from .kalman_filter import KalmanFilterXYAH
from .matching import fuse_score, iou_distance, linear_assignment
from .strack import STrack
from .track_class_aggregator import TrackClassAggregator

# Constants
logger: Any = ...  # From proxy_tracker
logger: Any = ...  # From track_class_aggregator
logger: Any = ...  # From tracker

# Functions
# From matching
def bbox_ioa(box1: Any.Any, box2: Any.Any, iou: bool = True) -> Any.Any:
    """
    Calculate the intersection over area of box1, box2. Boxes are in x1y1x2y2 format.
    
    Args:
        box1 (np.ndarray): First set of boxes (N, 4)
        box2 (np.ndarray): Second set of boxes (M, 4)
        iou (bool): If True, calculate IoU, otherwise calculate IoA
    
    Returns:
        np.ndarray: IoU/IoA matrix of shape (N, M)
    """
    ...

# From matching
def embedding_distance(tracks: list, detections: list, metric: str = 'cosine') -> Any.Any:
    """
    Compute distance between tracks and detections based on embeddings.
    
    Args:
        tracks (List[STrack] or List[np.ndarray]): List of tracks, where each track contains embedding features.
        detections (List[BaseTrack]): List of detections, where each detection contains embedding features.
        metric (str): Metric for distance computation. Supported metrics include 'cosine', 'euclidean', etc.
    
    Returns:
        (np.ndarray): Cost matrix computed based on embeddings with shape (N, M), where N is the number of tracks
            and M is the number of detections.
    """
    ...

# From matching
def fuse_score(cost_matrix: Any.Any, detections: list) -> Any.Any:
    """
    Fuse cost matrix with detection scores to produce a single similarity matrix.
    
    Args:
        cost_matrix (np.ndarray): The matrix containing cost values for assignments, with shape (N, M).
        detections (List[BaseTrack]): List of detections, each containing a score attribute.
    
    Returns:
        (np.ndarray): Fused similarity matrix with shape (N, M).
    """
    ...

# From matching
def iou_distance(atracks: list, btracks: list) -> Any.Any:
    """
    Compute cost based on Intersection over Union (IoU) between tracks.
    
    Args:
        atracks (List[STrack] or List[np.ndarray]): List of tracks 'a' or bounding boxes.
        btracks (List[STrack] or List[np.ndarray]): List of tracks 'b' or bounding boxes.
    
    Returns:
        (np.ndarray): Cost matrix computed based on IoU with shape (len(atracks), len(btracks)).
    """
    ...

# From matching
def linear_assignment(cost_matrix: Any.Any, thresh: float, use_lap: bool = True) -> Any:
    """
    Perform linear assignment using either the scipy or lap.lapjv method.
    
    Args:
        cost_matrix (np.ndarray): The matrix containing cost values for assignments, with shape (N, M).
        thresh (float): Threshold for considering an assignment valid.
        use_lap (bool): Use lap.lapjv for the assignment. If False, scipy.optimize.linear_sum_assignment is used.
    
    Returns:
        matched_indices (np.ndarray): Array of matched indices of shape (K, 2), where K is the number of matches.
        unmatched_a (np.ndarray): Array of unmatched indices from the first set, with shape (L,).
        unmatched_b (np.ndarray): Array of unmatched indices from the second set, with shape (M,).
    """
    ...

# From strack
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
# From base
class BaseTrack:
    # Base class for object tracking, providing foundational attributes and methods.
    #
    # Attributes:
    #     _count (int): Class-level counter for unique track IDs (fallback for global mode).
    #     _id_counter (dict): Per-namespace ID counters for camera isolation.
    #     track_id (int): Unique identifier for the track (numeric part).
    #     track_id_namespaced (str): Fully namespaced track ID ({namespace}_{id}).
    #     is_activated (bool): Flag indicating whether the track is currently active.
    #     state (TrackState): Current state of the track.
    #     history (OrderedDict): Ordered history of the track's states.
    #     features (list): List of features extracted from the object for tracking.
    #     curr_feature (Any): The current feature of the object being tracked.
    #     score (float): The confidence score of the tracking.
    #     start_frame (int): The frame number where tracking started.
    #     frame_id (int): The most recent frame ID processed by the track.
    #     time_since_update (int): Frames passed since the last update.
    #     location (tuple): The location of the object in the context of multi-camera tracking.

    def __init__(self: Any) -> None:
        """
        Initialize a new track with a unique ID and foundational tracking attributes.
        """
        ...

    def activate(self: Any, *args: Any) -> None:
        """
        Activate the track with provided arguments, initializing necessary attributes for tracking.
        """
        ...

    def end_frame(self: Any) -> int:
        """
        Return the ID of the most recent frame where the object was tracked.
        """
        ...

    def get_namespaced_id(track_id: int) -> str:
        """
        Get the fully namespaced track ID string.
        
                Returns format: '{namespace}_{track_id}' or just '{track_id}' if no namespace.
        """
        ...

    def mark_lost(self: Any) -> None:
        """
        Mark the track as lost by updating its state to TrackState.Lost.
        """
        ...

    def mark_removed(self: Any) -> None:
        """
        Mark the track as removed by setting its state to TrackState.Removed.
        """
        ...

    def next_id() -> int:
        """
        Increment and return the next unique track ID.
        
                If a namespace is set, uses per-namespace counter for isolation.
                Otherwise falls back to global counter for backward compatibility.
        """
        ...

    def predict(self: Any) -> None:
        """
        Predict the next state of the track based on the current state and tracking model.
        """
        ...

    def reset_all_ids() -> None:
        """
        Reset all ID counters (global and all namespaces).
        """
        ...

    def reset_id(namespace: str = None) -> None:
        """
        Reset track ID counter.
        
                Args:
                    namespace: If provided, only reset that namespace's counter.
                              If None and a current namespace is set, reset current namespace.
                              If None and no namespace set, reset global counter.
        """
        ...

    def set_namespace(namespace: str) -> None:
        """
        Set the current namespace for track ID generation.
        
                Call this before creating/activating tracks to assign them to a namespace.
                Typically called with camera_id or a hash of camera_id.
        """
        ...

    def update(self: Any, *args: Any, **kwargs: Any) -> None:
        """
        Update the track with new observations and data, modifying its state and attributes accordingly.
        """
        ...


# From base
class TrackState:
    # Enumeration class representing the possible states of an object being tracked.
    #
    # Attributes:
    #     New (int): State when the object is newly detected.
    #     Tracked (int): State when the object is successfully tracked in subsequent frames.
    #     Lost (int): State when the object is no longer tracked.
    #     Removed (int): State when the object is removed from tracking.

    Lost: int
    New: int
    Removed: int
    Tracked: int


# From config
class TrackerConfig:
    # Configuration for advanced tracker.
    #
    # This class contains all the parameters needed to configure the tracking algorithm,
    # including thresholds, buffer sizes, and algorithm-specific settings.
    #
    # Threshold Tuning Guide:
    # - Lower thresholds = more lenient matching = fewer new track IDs = more stable counts
    # - Higher thresholds = stricter matching = more new track IDs = potential count inflation
    #
    # Recommended defaults are optimized for count accuracy over precision.

    ...

# From kalman_filter
class KalmanFilterXYAH:
    # A KalmanFilterXYAH class for tracking bounding boxes in image space using a Kalman filter.
    #
    # Implements a simple Kalman filter for tracking bounding boxes in image space. The 8-dimensional state space
    # (x, y, a, h, vx, vy, va, vh) contains the bounding box center position (x, y), aspect ratio a, height h, and their
    # respective velocities. Object motion follows a constant velocity model, and bounding box location (x, y, a, h) is
    # taken as a direct observation of the state space (linear observation model).

    def __init__(self: Any) -> None:
        """
        Initialize Kalman filter model matrices with motion and observation uncertainty weights.
        
        The Kalman filter is initialized with an 8-dimensional state space (x, y, a, h, vx, vy, va, vh), where (x, y)
        represents the bounding box center position, 'a' is the aspect ratio, 'h' is the height, and their respective
        velocities are (vx, vy, va, vh). The filter uses a constant velocity model for object motion and a linear
        observation model for bounding box location.
        """
        ...

    def gating_distance(self: Any, mean: Any.Any, covariance: Any.Any, measurements: Any.Any, only_position: bool = False, metric: str = 'maha') -> Any.Any:
        """
        Compute gating distance between state distribution and measurements.
        
        Args:
            mean (np.ndarray): Mean vector over the state distribution (8 dimensional).
            covariance (np.ndarray): Covariance of the state distribution (8x8 dimensional).
            measurements (np.ndarray): An (N, 4) matrix of N measurements, each in format (x, y, a, h) where (x, y) is the
                bounding box center position, a the aspect ratio, and h the height.
            only_position (bool, optional): If True, distance computation is done with respect to box center position only.
            metric (str, optional): The metric to use for calculating the distance. Options are 'gaussian' for the squared
                Euclidean distance and 'maha' for the squared Mahalanobis distance.
        
        Returns:
            (np.ndarray): Returns an array of length N, where the i-th element contains the squared distance between
                (mean, covariance) and `measurements[i]`.
        """
        ...

    def initiate(self: Any, measurement: Any.Any) -> Any:
        """
        Create a track from an unassociated measurement.
        
        Args:
            measurement (np.ndarray): Bounding box coordinates (x, y, a, h) with center position (x, y), aspect ratio a,
                and height h.
        
        Returns:
            mean (np.ndarray): Mean vector (8-dimensional) of the new track. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix (8x8 dimensional) of the new track.
        """
        ...

    def multi_predict(self: Any, mean: Any.Any, covariance: Any.Any) -> Any:
        """
        Run Kalman filter prediction step for multiple object states (Vectorized version).
        
        Args:
            mean (np.ndarray): The Nx8 dimensional mean matrix of the object states at the previous time step.
            covariance (np.ndarray): The Nx8x8 covariance matrix of the object states at the previous time step.
        
        Returns:
            mean (np.ndarray): Mean matrix of the predicted states with shape (N, 8).
            covariance (np.ndarray): Covariance matrix of the predicted states with shape (N, 8, 8).
        """
        ...

    def predict(self: Any, mean: Any.Any, covariance: Any.Any) -> Any:
        """
        Run Kalman filter prediction step.
        
        Args:
            mean (np.ndarray): The 8-dimensional mean vector of the object state at the previous time step.
            covariance (np.ndarray): The 8x8-dimensional covariance matrix of the object state at the previous time step.
        
        Returns:
            mean (np.ndarray): Mean vector of the predicted state. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix of the predicted state.
        """
        ...

    def project(self: Any, mean: Any.Any, covariance: Any.Any) -> Any:
        """
        Project state distribution to measurement space.
        
        Args:
            mean (np.ndarray): The state's mean vector (8 dimensional array).
            covariance (np.ndarray): The state's covariance matrix (8x8 dimensional).
        
        Returns:
            mean (np.ndarray): Projected mean of the given state estimate.
            covariance (np.ndarray): Projected covariance matrix of the given state estimate.
        """
        ...

    def update(self: Any, mean: Any.Any, covariance: Any.Any, measurement: Any.Any) -> Any:
        """
        Run Kalman filter correction step.
        
        Args:
            mean (np.ndarray): The predicted state's mean vector (8 dimensional).
            covariance (np.ndarray): The state's covariance matrix (8x8 dimensional).
            measurement (np.ndarray): The 4 dimensional measurement vector (x, y, a, h), where (x, y) is the center
                position, a the aspect ratio, and h the height of the bounding box.
        
        Returns:
            new_mean (np.ndarray): Measurement-corrected state mean.
            new_covariance (np.ndarray): Measurement-corrected state covariance.
        """
        ...


# From kalman_filter
class KalmanFilterXYWH:
    # A KalmanFilterXYWH class for tracking bounding boxes in image space using a Kalman filter.
    #
    # Implements a Kalman filter for tracking bounding boxes with state space (x, y, w, h, vx, vy, vw, vh), where
    # (x, y) is the center position, w is the width, h is the height, and vx, vy, vw, vh are their respective velocities.
    # The object motion follows a constant velocity model, and the bounding box location (x, y, w, h) is taken as a direct
    # observation of the state space (linear observation model).

    def initiate(self: Any, measurement: Any.Any) -> Any:
        """
        Create track from unassociated measurement.
        
        Args:
            measurement (np.ndarray): Bounding box coordinates (x, y, w, h) with center position (x, y), width, and height.
        
        Returns:
            mean (np.ndarray): Mean vector (8 dimensional) of the new track. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix (8x8 dimensional) of the new track.
        """
        ...

    def multi_predict(self: Any, mean: Any.Any, covariance: Any.Any) -> Any:
        """
        Run Kalman filter prediction step (Vectorized version).
        
        Args:
            mean (np.ndarray): The Nx8 dimensional mean matrix of the object states at the previous time step.
            covariance (np.ndarray): The Nx8x8 covariance matrix of the object states at the previous time step.
        
        Returns:
            mean (np.ndarray): Mean matrix of the predicted states with shape (N, 8).
            covariance (np.ndarray): Covariance matrix of the predicted states with shape (N, 8, 8).
        """
        ...

    def predict(self: Any, mean: Any.Any, covariance: Any.Any) -> Any:
        """
        Run Kalman filter prediction step.
        
        Args:
            mean (np.ndarray): The 8-dimensional mean vector of the object state at the previous time step.
            covariance (np.ndarray): The 8x8-dimensional covariance matrix of the object state at the previous time step.
        
        Returns:
            mean (np.ndarray): Mean vector of the predicted state. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix of the predicted state.
        """
        ...

    def project(self: Any, mean: Any.Any, covariance: Any.Any) -> Any:
        """
        Project state distribution to measurement space.
        
        Args:
            mean (np.ndarray): The state's mean vector (8 dimensional array).
            covariance (np.ndarray): The state's covariance matrix (8x8 dimensional).
        
        Returns:
            mean (np.ndarray): Projected mean of the given state estimate.
            covariance (np.ndarray): Projected covariance matrix of the given state estimate.
        """
        ...

    def update(self: Any, mean: Any.Any, covariance: Any.Any, measurement: Any.Any) -> Any:
        """
        Run Kalman filter correction step.
        
        Args:
            mean (np.ndarray): The predicted state's mean vector (8 dimensional).
            covariance (np.ndarray): The state's covariance matrix (8x8 dimensional).
            measurement (np.ndarray): The 4 dimensional measurement vector (x, y, w, h), where (x, y) is the center
                position, w the width, and h the height of the bounding box.
        
        Returns:
            new_mean (np.ndarray): Measurement-corrected state mean.
            new_covariance (np.ndarray): Measurement-corrected state covariance.
        """
        ...


# From proxy_tracker
class KalmanFilterXYAH:
    # Kalman filter for bbox tracking (center_x, center_y, aspect_ratio, height).

    def __init__(self: Any) -> None: ...

    def initiate(self: Any, measurement: Any.Any) -> Tuple[Any.Any, Any.Any]: ...

    def predict(self: Any, mean: Any.Any, covariance: Any.Any) -> Tuple[Any.Any, Any.Any]: ...

    def project(self: Any, mean: Any.Any, covariance: Any.Any) -> Tuple[Any.Any, Any.Any]: ...

    def update(self: Any, mean: Any.Any, covariance: Any.Any, measurement: Any.Any) -> Tuple[Any.Any, Any.Any]: ...


# From proxy_tracker
class ProxyAdvancedTracker:
    # Production-ready tracker compatible with usecase pipeline.
    #
    # Input format (detection dict):
    #     {
    #         "bounding_box": {"xmin": float, "ymin": float, "xmax": float, "ymax": float},
    #         "category": str,
    #         "confidence": float,
    #         ...
    #     }
    #
    # Output format (same dict with track_id and frame_id added):
    #     {
    #         "bounding_box": {...},
    #         "category": str,
    #         "confidence": float,
    #         "track_id": int,
    #         "frame_id": int,
    #         ...
    #     }

    def __init__(self: Any, iou_threshold: float = 0.3, max_misses: int = 30) -> None: ...

    def get_tracker_stats(self: Any) -> Dict[str, Any]:
        """
        Get tracker statistics.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset tracker state.
        """
        ...

    def restore_state(self: Any) -> Any:
        """
        No-op for compatibility with AdvancedTracker API.
        """
        ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Update tracker with detections and return detections with track_id added.
        
        Args:
            detections: List of detection dicts with bounding_box, category, confidence
        
        Returns:
            Same detections list with track_id and frame_id fields added to each detection
        """
        ...


# From proxy_tracker
class TrackState:
    CONFIRMED: int
    LOST: int
    REMOVED: int
    TENTATIVE: int


# From strack
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

    def multi_predict(stracks: List['Any']) -> Any:
        """
        Perform multi-object predictive tracking using Kalman filter for the provided list of STrack instances.
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


# From track_class_aggregator
class TrackClassAggregator:
    # Maintains per-track sliding windows of class labels and returns the most frequent.
    #
    # This aggregator reduces class label flickering in tracking results by applying
    # temporal voting based on historical observations within a sliding window.
    #
    # Attributes:
    #     window_size (int): Maximum number of frames to keep in the sliding window.
    #     track_windows (Dict[int, deque]): Per-track sliding windows of class labels.

    def __init__(self: Any, window_size: int = 30) -> None:
        """
        Initialize the TrackClassAggregator.
        
        Args:
            window_size (int): Number of recent frames to consider for aggregation.
                Must be positive. Larger windows provide more stability but slower
                adaptation to genuine class changes.
        """
        ...

    def get_active_track_count(self: Any) -> int:
        """
        Get the number of tracks currently being aggregated.
        """
        ...

    def get_aggregated_class(self: Any, track_id: int, fallback_class: Any) -> Any:
        """
        Get the aggregated class for a track without updating the window.
        
        Args:
            track_id (int): Unique identifier for the track.
            fallback_class (Any): Class to return if track has no history.
        
        Returns:
            Any: The aggregated class label, or fallback_class if no history exists.
        """
        ...

    def remove_track(self: Any, track_id: int) -> None:
        """
        Remove a track's window from memory.
        
        Args:
            track_id (int): Unique identifier for the track to remove.
        """
        ...

    def remove_tracks(self: Any, track_ids: list) -> None:
        """
        Remove multiple tracks' windows from memory (batch operation).
        
        Args:
            track_ids (list): List of track IDs to remove.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear all track windows.
        """
        ...

    def update_and_aggregate(self: Any, track_id: int, observed_class: Any) -> Any:
        """
        Update the sliding window for a track and return the aggregated class label.
        
        This method:
        1. Adds the new observation to the track's window
        2. Maintains window size by removing oldest entries if needed
        3. Returns the most frequent class in the window
        
        Args:
            track_id (int): Unique identifier for the track.
            observed_class (Any): The class label observed in the current frame.
        
        Returns:
            Any: The aggregated class label (most frequent in the window).
                If there's a tie, returns the most recent among tied classes.
        """
        ...


# From tracker
class AdvancedTracker:
    # AdvancedTracker: A tracking algorithm similar to BYTETracker for object detection and tracking.
    #
    # This class encapsulates the functionality for initializing, updating, and managing the tracks for detected objects in a
    # video sequence. It maintains the state of tracked, lost, and removed tracks over frames, utilizes Kalman filtering for
    # predicting the new object locations, and performs data association.
    #
    # Attributes:
    #     tracked_stracks (List[STrack]): List of successfully activated tracks.
    #     lost_stracks (List[STrack]): List of lost tracks.
    #     removed_stracks (List[STrack]): List of removed tracks.
    #     frame_id (int): The current frame ID.
    #     config (TrackerConfig): Tracker configuration.
    #     max_time_lost (int): The maximum frames for a track to be considered as 'lost'.
    #     kalman_filter (KalmanFilterXYAH): Kalman Filter object.
    #     class_smoother (Optional[ClassSmoother]): Optional class smoother for class label smoothing over flicker.

    def __init__(self: Any, config: Any, namespace: Optional[str] = None) -> None:
        """
        Initialize an AdvancedTracker instance for object tracking.
        
        Args:
            config (TrackerConfig): Tracker configuration object.
            namespace (Optional[str]): Namespace for track ID generation (e.g., camera_id).
                If provided, track IDs are isolated to this namespace to prevent
                cross-camera collisions. Recommended to use hash of camera_id.
        """
        ...

    def clear_saved_state(self: Any) -> bool:
        """
        Clear saved tracker state (use when intentionally resetting counts).
        
        Returns:
            bool: True if state was cleared successfully
        """
        ...

    def get_category_counts(self: Any) -> Dict[str, int]:
        """
        Get unique track counts by category since tracker start.
        """
        ...

    def get_dists(self: Any, tracks: List[Any], detections: List[Any]) -> Any.Any:
        """
        Calculate the distance between tracks and detections using IoU and optionally fuse scores.
        """
        ...

    def get_kalmanfilter(self: Any) -> Any:
        """
        Return a Kalman filter object for tracking bounding boxes using KalmanFilterXYAH.
        """
        ...

    def get_new_tracks_this_frame(self: Any, previous_ids: Set[int]) -> Set[int]:
        """
        Get track IDs that are new compared to a previous set.
        """
        ...

    def get_state_file_path(self: Any) -> str:
        """
        Get the file path for state persistence.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get total unique track count since tracker start.
        """
        ...

    def joint_stracks(tlista: List[Any], tlistb: List[Any]) -> List[Any]:
        """
        Combine two lists of STrack objects into a single list, ensuring no duplicates based on track IDs.
        """
        ...

    def multi_predict(self: Any, tracks: List[Any]) -> Any:
        """
        Predict the next states for multiple tracks using Kalman filter.
        """
        ...

    def remove_duplicate_stracks(self: Any, stracksa: List[Any], stracksb: List[Any]) -> Tuple[List[Any], List[Any]]:
        """
        Remove duplicate stracks from two lists based on Intersection over Union (IoU) distance.
        
                Uses the configurable duplicate_removal_iou_thresh from config.
                Higher thresholds are more permissive (reduce false duplicates).
                Lower thresholds are more aggressive (remove more duplicates).
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset the tracker by clearing all tracked, lost, and removed tracks and reinitializing the Kalman filter.
        """
        ...

    def reset_id() -> Any:
        """
        Reset the ID counter for STrack instances to ensure unique track IDs across tracking sessions.
        """
        ...

    def restore_state(self: Any) -> bool:
        """
        Restore tracker state from persistent storage.
        
        Call this after creating a new tracker instance to recover accumulated counts.
        
        Returns:
            bool: True if state was restored successfully
        """
        ...

    def save_state(self: Any) -> bool:
        """
        Save tracker state to persistent storage.
        
        This preserves count accuracy across restarts or tracker recreation.
        
        Returns:
            bool: True if state was saved successfully
        """
        ...

    def sub_stracks(tlista: List[Any], tlistb: List[Any]) -> List[Any]:
        """
        Filter out the stracks present in the second list from the first list.
        """
        ...

    def update(self: Any, detections: Union[List[Dict], Dict[str, List[Dict]]], img: Optional[Any.Any] = None) -> Union[List[Dict], Dict[str, List[Dict]]]:
        """
        Update the tracker with new detections and return the current list of tracked objects.
        
        Args:
            detections: Detection results in various formats:
                - List[Dict]: Single frame detections
                - Dict[str, List[Dict]]: Multi-frame detections with frame keys
            img: Optional image for motion compensation
        
        Returns:
            Tracking results in the same format as input
        """
        ...


from . import base, config, kalman_filter, matching, proxy_tracker, strack, track_class_aggregator, tracker