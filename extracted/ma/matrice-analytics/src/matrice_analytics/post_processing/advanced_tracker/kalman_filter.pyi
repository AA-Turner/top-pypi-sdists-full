"""Auto-generated stub for module: kalman_filter."""
from typing import Any

# Classes
class KalmanFilterXYAH:
    # A KalmanFilterXYAH class for tracking bounding boxes in image space using a Kalman filter.
    #
    # Implements a simple Kalman filter for tracking bounding boxes in image space. The 8-dimensional state space
    # (x, y, a, h, vx, vy, va, vh) contains the bounding box center position (x, y), aspect ratio a, height h, and their
    # respective velocities. Object motion follows a constant velocity model, and bounding box location (x, y, a, h) is
    # taken as a direct observation of the state space (linear observation model).

    def __init__(self: Any, dt: float = 1.0) -> None:
        """
        Initialize Kalman filter model matrices with motion and observation uncertainty weights.
        
        The Kalman filter is initialized with an 8-dimensional state space (x, y, a, h, vx, vy, va, vh), where (x, y)
        represents the bounding box center position, 'a' is the aspect ratio, 'h' is the height, and their respective
        velocities are (vx, vy, va, vh). The filter uses a constant velocity model for object motion and a linear
        observation model for bounding box location.
        
        Args:
            dt (float): Time step between frames for the constant-velocity model. Defaults to 1.0, which
                reproduces the historical (frame-count) behavior exactly. FPS adaptation rescales this via
                ``set_dt`` so a slow camera advances the state further per frame than a fast one.
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

    def multi_update(self: Any, means: Any.Any, covariances: Any.Any, measurements: Any.Any) -> Any:
        """
        Run the Kalman correction step for N tracks at once (vectorized).
        
                The mathematical twin of update() — projection via the eye(4,8) slice,
                gain from solving S K^T = P[:, :4]^T (np.linalg.solve on the symmetric-PD
                innovation covariance instead of per-track scipy cho_factor/cho_solve),
                then the standard mean/covariance correction. One batched call replaces N
                python->numpy->scipy round-trips per frame, which profiling showed was
                the tracker's largest remaining per-frame cost (~0.33 ms at 10 tracks).
        
                Args:
                    means: (N, 8) state means.
                    covariances: (N, 8, 8) state covariances.
                    measurements: (N, 4) measurements in this filter's space.
        
                Returns:
                    (new_means (N, 8), new_covariances (N, 8, 8))
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

    def set_dt(self: Any, dt: float) -> None:
        """
        Rescale the constant-velocity time step and rebuild F in place.
        
                No-op when ``dt`` is unchanged, so the default (dt=1.0) path never reallocates. Only F is
                rebuilt; existing track means/covariances are left untouched (the filter self-corrects within a
                frame or two — see AdvancedTracker._maybe_adapt_fps).
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

