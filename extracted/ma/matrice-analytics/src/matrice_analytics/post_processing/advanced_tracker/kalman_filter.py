"""
Kalman filter implementation for advanced tracker.

This module provides Kalman filter implementations for tracking bounding boxes,
including both XYAH and XYWH formats.
"""

import numpy as np
import scipy.linalg


class KalmanFilterXYAH:
    """
    A KalmanFilterXYAH class for tracking bounding boxes in image space using a Kalman filter.

    Implements a simple Kalman filter for tracking bounding boxes in image space. The 8-dimensional state space
    (x, y, a, h, vx, vy, va, vh) contains the bounding box center position (x, y), aspect ratio a, height h, and their
    respective velocities. Object motion follows a constant velocity model, and bounding box location (x, y, a, h) is
    taken as a direct observation of the state space (linear observation model).
    """

    def __init__(self, dt: float = 1.0):
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
        self._ndim = 4
        self._dt = float(dt)

        # Create Kalman filter model matrices
        self._build_motion_mat()
        self._update_mat = np.eye(self._ndim, 2 * self._ndim)

        # Motion and observation uncertainty are chosen relative to the current state estimate
        self._std_weight_position = 1.0 / 20
        self._std_weight_velocity = 1.0 / 160

    def _build_motion_mat(self) -> None:
        """(Re)build the state-transition matrix F for the current ``_dt``.

        F is identity with the velocity blocks scaled by dt. dt=1.0 reproduces the historical matrix
        byte-for-byte; only the four ``[i, ndim + i]`` entries depend on dt."""
        ndim = self._ndim
        self._motion_mat = np.eye(2 * ndim, 2 * ndim)
        for i in range(ndim):
            self._motion_mat[i, ndim + i] = self._dt

    def set_dt(self, dt: float) -> None:
        """Rescale the constant-velocity time step and rebuild F in place.

        No-op when ``dt`` is unchanged, so the default (dt=1.0) path never reallocates. Only F is
        rebuilt; existing track means/covariances are left untouched (the filter self-corrects within a
        frame or two — see AdvancedTracker._maybe_adapt_fps)."""
        dt = float(dt)
        if dt == self._dt:
            return
        self._dt = dt
        self._build_motion_mat()

    def initiate(self, measurement: np.ndarray):
        """
        Create a track from an unassociated measurement.

        Args:
            measurement (np.ndarray): Bounding box coordinates (x, y, a, h) with center position (x, y), aspect ratio a,
                and height h.

        Returns:
            mean (np.ndarray): Mean vector (8-dimensional) of the new track. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix (8x8 dimensional) of the new track.
        """
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

    def predict(self, mean: np.ndarray, covariance: np.ndarray):
        """
        Run Kalman filter prediction step.

        Args:
            mean (np.ndarray): The 8-dimensional mean vector of the object state at the previous time step.
            covariance (np.ndarray): The 8x8-dimensional covariance matrix of the object state at the previous time step.

        Returns:
            mean (np.ndarray): Mean vector of the predicted state. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix of the predicted state.
        """
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

        mean = np.dot(mean, self._motion_mat.T)
        # multi_dot's order analysis ties for 8x8 chains and picks A@(B@C) — same
        # explicit form, minus multi_dot's per-call planning overhead.
        covariance = np.dot(self._motion_mat, np.dot(covariance, self._motion_mat.T)) + motion_cov

        return mean, covariance

    def project(self, mean: np.ndarray, covariance: np.ndarray):
        """
        Project state distribution to measurement space.

        Args:
            mean (np.ndarray): The state's mean vector (8 dimensional array).
            covariance (np.ndarray): The state's covariance matrix (8x8 dimensional).

        Returns:
            mean (np.ndarray): Projected mean of the given state estimate.
            covariance (np.ndarray): Projected covariance matrix of the given state estimate.
        """
        std = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-1,
            self._std_weight_position * mean[3],
        ]
        innovation_cov = np.diag(np.square(std))

        # _update_mat is eye(4, 8) and never modified, so U@mean selects mean[:4]
        # and U@cov@U.T selects cov[:4, :4] — bitwise-identical to the matmuls,
        # without two 8x8 products per call (this runs once per track per frame).
        mean = mean[:4]
        covariance = covariance[:4, :4]
        return mean, covariance + innovation_cov

    def multi_predict(self, mean: np.ndarray, covariance: np.ndarray):
        """
        Run Kalman filter prediction step for multiple object states (Vectorized version).

        Args:
            mean (np.ndarray): The Nx8 dimensional mean matrix of the object states at the previous time step.
            covariance (np.ndarray): The Nx8x8 covariance matrix of the object states at the previous time step.

        Returns:
            mean (np.ndarray): Mean matrix of the predicted states with shape (N, 8).
            covariance (np.ndarray): Covariance matrix of the predicted states with shape (N, 8, 8).
        """
        std_pos = [
            self._std_weight_position * mean[:, 3],
            self._std_weight_position * mean[:, 3],
            1e-2 * np.ones_like(mean[:, 3]),
            self._std_weight_position * mean[:, 3],
        ]
        std_vel = [
            self._std_weight_velocity * mean[:, 3],
            self._std_weight_velocity * mean[:, 3],
            1e-5 * np.ones_like(mean[:, 3]),
            self._std_weight_velocity * mean[:, 3],
        ]
        sqr = np.square(np.r_[std_pos, std_vel]).T

        # Vectorized diagonal fill — identical values to the old per-track
        # [np.diag(sqr[i]) ...] loop without N python-level diag() calls.
        n = len(mean)
        motion_cov = np.zeros((n, 8, 8), dtype=sqr.dtype)
        _idx = np.arange(8)
        motion_cov[:, _idx, _idx] = sqr

        mean = np.dot(mean, self._motion_mat.T)
        left = np.dot(self._motion_mat, covariance).transpose((1, 0, 2))
        covariance = np.dot(left, self._motion_mat.T) + motion_cov

        return mean, covariance

    def update(self, mean: np.ndarray, covariance: np.ndarray, measurement: np.ndarray):
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
        projected_mean, projected_cov = self.project(mean, covariance)

        chol_factor, lower = scipy.linalg.cho_factor(projected_cov, lower=True, check_finite=False)
        # covariance @ _update_mat.T == covariance[:, :4] exactly (eye selection).
        kalman_gain = scipy.linalg.cho_solve(
            (chol_factor, lower),
            covariance[:, :4].T,
            check_finite=False,
        ).T
        innovation = measurement - projected_mean

        new_mean = mean + np.dot(innovation, kalman_gain.T)
        # multi_dot ties on this shape and picks A@(B@C) — same explicit order.
        new_covariance = covariance - np.dot(kalman_gain, np.dot(projected_cov, kalman_gain.T))
        return new_mean, new_covariance

    def _multi_innovation_var(self, means: np.ndarray) -> np.ndarray:
        """Per-state innovation VARIANCES (squared stds) for the batched update.

        Mirrors the std list in project() — XYAH: [wp*h, wp*h, 1e-1, wp*h]."""
        h = self._std_weight_position * means[:, 3]
        var = np.empty((len(means), 4), dtype=np.float64)
        var[:, 0] = h
        var[:, 1] = h
        var[:, 2] = 1e-1
        var[:, 3] = h
        return np.square(var)

    def multi_update(self, means: np.ndarray, covariances: np.ndarray, measurements: np.ndarray):
        """Run the Kalman correction step for N tracks at once (vectorized).

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
        proj_means = means[:, :4]
        proj_covs = covariances[:, :4, :4].copy()
        _idx = np.arange(4)
        proj_covs[:, _idx, _idx] += self._multi_innovation_var(means)

        b = covariances[:, :, :4]  # P @ U.T == P[:, :, :4] exactly (eye selection)
        # S is symmetric PD; batched solve(S, B^T) gives K^T -> transpose to (N, 8, 4)
        kalman_gains = np.linalg.solve(proj_covs, b.transpose(0, 2, 1)).transpose(0, 2, 1)
        innovations = measurements - proj_means  # (N, 4)

        new_means = means + np.einsum("nij,nj->ni", kalman_gains, innovations)
        new_covs = covariances - np.matmul(kalman_gains, np.matmul(proj_covs, kalman_gains.transpose(0, 2, 1)))
        return new_means, new_covs

    def gating_distance(
        self,
        mean: np.ndarray,
        covariance: np.ndarray,
        measurements: np.ndarray,
        only_position: bool = False,
        metric: str = "maha",
    ) -> np.ndarray:
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
        mean, covariance = self.project(mean, covariance)
        if only_position:
            mean, covariance = mean[:2], covariance[:2, :2]
            measurements = measurements[:, :2]

        d = measurements - mean
        if metric == "gaussian":
            return np.sum(d * d, axis=1)
        elif metric == "maha":
            cholesky_factor = np.linalg.cholesky(covariance)
            z = scipy.linalg.solve_triangular(cholesky_factor, d.T, lower=True, check_finite=False, overwrite_b=True)
            return np.sum(z * z, axis=0)  # square maha
        else:
            raise ValueError("Invalid distance metric")


class KalmanFilterXYWH(KalmanFilterXYAH):
    """
    A KalmanFilterXYWH class for tracking bounding boxes in image space using a Kalman filter.

    Implements a Kalman filter for tracking bounding boxes with state space (x, y, w, h, vx, vy, vw, vh), where
    (x, y) is the center position, w is the width, h is the height, and vx, vy, vw, vh are their respective velocities.
    The object motion follows a constant velocity model, and the bounding box location (x, y, w, h) is taken as a direct
    observation of the state space (linear observation model).
    """

    def initiate(self, measurement: np.ndarray):
        """
        Create track from unassociated measurement.

        Args:
            measurement (np.ndarray): Bounding box coordinates (x, y, w, h) with center position (x, y), width, and height.

        Returns:
            mean (np.ndarray): Mean vector (8 dimensional) of the new track. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix (8x8 dimensional) of the new track.
        """
        mean_pos = measurement
        mean_vel = np.zeros_like(mean_pos)
        mean = np.r_[mean_pos, mean_vel]

        std = [
            2 * self._std_weight_position * measurement[2],
            2 * self._std_weight_position * measurement[3],
            2 * self._std_weight_position * measurement[2],
            2 * self._std_weight_position * measurement[3],
            10 * self._std_weight_velocity * measurement[2],
            10 * self._std_weight_velocity * measurement[3],
            10 * self._std_weight_velocity * measurement[2],
            10 * self._std_weight_velocity * measurement[3],
        ]
        covariance = np.diag(np.square(std))
        return mean, covariance

    def predict(self, mean: np.ndarray, covariance: np.ndarray):
        """
        Run Kalman filter prediction step.

        Args:
            mean (np.ndarray): The 8-dimensional mean vector of the object state at the previous time step.
            covariance (np.ndarray): The 8x8-dimensional covariance matrix of the object state at the previous time step.

        Returns:
            mean (np.ndarray): Mean vector of the predicted state. Unobserved velocities are initialized to 0 mean.
            covariance (np.ndarray): Covariance matrix of the predicted state.
        """
        std_pos = [
            self._std_weight_position * mean[2],
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[2],
            self._std_weight_position * mean[3],
        ]
        std_vel = [
            self._std_weight_velocity * mean[2],
            self._std_weight_velocity * mean[3],
            self._std_weight_velocity * mean[2],
            self._std_weight_velocity * mean[3],
        ]
        motion_cov = np.diag(np.square(np.r_[std_pos, std_vel]))

        mean = np.dot(mean, self._motion_mat.T)
        # Same explicit A@(B@C) order multi_dot picks for 8x8 chains.
        covariance = np.dot(self._motion_mat, np.dot(covariance, self._motion_mat.T)) + motion_cov

        return mean, covariance

    def project(self, mean: np.ndarray, covariance: np.ndarray):
        """
        Project state distribution to measurement space.

        Args:
            mean (np.ndarray): The state's mean vector (8 dimensional array).
            covariance (np.ndarray): The state's covariance matrix (8x8 dimensional).

        Returns:
            mean (np.ndarray): Projected mean of the given state estimate.
            covariance (np.ndarray): Projected covariance matrix of the given state estimate.
        """
        std = [
            self._std_weight_position * mean[2],
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[2],
            self._std_weight_position * mean[3],
        ]
        innovation_cov = np.diag(np.square(std))

        # _update_mat is eye(4, 8): exact slice instead of two 8x8 matmuls.
        mean = mean[:4]
        covariance = covariance[:4, :4]
        return mean, covariance + innovation_cov

    def _multi_innovation_var(self, means: np.ndarray) -> np.ndarray:
        """XYWH innovation variances — mirrors this class's project() std list."""
        w = self._std_weight_position * means[:, 2]
        h = self._std_weight_position * means[:, 3]
        var = np.empty((len(means), 4), dtype=np.float64)
        var[:, 0] = w
        var[:, 1] = h
        var[:, 2] = w
        var[:, 3] = h
        return np.square(var)

    def multi_predict(self, mean: np.ndarray, covariance: np.ndarray):
        """
        Run Kalman filter prediction step (Vectorized version).

        Args:
            mean (np.ndarray): The Nx8 dimensional mean matrix of the object states at the previous time step.
            covariance (np.ndarray): The Nx8x8 covariance matrix of the object states at the previous time step.

        Returns:
            mean (np.ndarray): Mean matrix of the predicted states with shape (N, 8).
            covariance (np.ndarray): Covariance matrix of the predicted states with shape (N, 8, 8).
        """
        std_pos = [
            self._std_weight_position * mean[:, 2],
            self._std_weight_position * mean[:, 3],
            self._std_weight_position * mean[:, 2],
            self._std_weight_position * mean[:, 3],
        ]
        std_vel = [
            self._std_weight_velocity * mean[:, 2],
            self._std_weight_velocity * mean[:, 3],
            self._std_weight_velocity * mean[:, 2],
            self._std_weight_velocity * mean[:, 3],
        ]
        sqr = np.square(np.r_[std_pos, std_vel]).T

        # Vectorized diagonal fill — identical values, no per-track diag() loop.
        n = len(mean)
        motion_cov = np.zeros((n, 8, 8), dtype=sqr.dtype)
        _idx = np.arange(8)
        motion_cov[:, _idx, _idx] = sqr

        mean = np.dot(mean, self._motion_mat.T)
        left = np.dot(self._motion_mat, covariance).transpose((1, 0, 2))
        covariance = np.dot(left, self._motion_mat.T) + motion_cov

        return mean, covariance

    def update(self, mean: np.ndarray, covariance: np.ndarray, measurement: np.ndarray):
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
        return super().update(mean, covariance, measurement)
