"""
Matching utilities for track association.

This module provides utilities for matching tracks with detections,
including IoU distance calculation and linear assignment.
"""

import numpy as np
import scipy
from scipy.spatial.distance import cdist

try:
    import lap  # for linear_assignment
    assert lap.__version__  # verify package is not directory
except (ImportError, AssertionError, AttributeError):
    # Fallback to scipy if lap is not available
    lap = None


def linear_assignment(cost_matrix: np.ndarray, thresh: float, use_lap: bool = True):
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
    if cost_matrix.size == 0:
        return np.empty((0, 2), dtype=int), tuple(range(cost_matrix.shape[0])), tuple(range(cost_matrix.shape[1]))

    if use_lap and lap is not None:
        # Use lap.lapjv
        _, x, y = lap.lapjv(cost_matrix, extend_cost=True, cost_limit=thresh)
        matches = [[ix, mx] for ix, mx in enumerate(x) if mx >= 0]
        unmatched_a = np.where(x < 0)[0]
        unmatched_b = np.where(y < 0)[0]
    else:
        # Use scipy.optimize.linear_sum_assignment
        x, y = scipy.optimize.linear_sum_assignment(cost_matrix)  # row x, col y
        matches = np.asarray([[x[i], y[i]] for i in range(len(x)) if cost_matrix[x[i], y[i]] <= thresh])
        if len(matches) == 0:
            unmatched_a = list(np.arange(cost_matrix.shape[0]))
            unmatched_b = list(np.arange(cost_matrix.shape[1]))
        else:
            unmatched_a = list(frozenset(np.arange(cost_matrix.shape[0])) - frozenset(matches[:, 0]))
            unmatched_b = list(frozenset(np.arange(cost_matrix.shape[1])) - frozenset(matches[:, 1]))

    return matches, unmatched_a, unmatched_b


def bbox_ioa(box1: np.ndarray, box2: np.ndarray, iou: bool = True) -> np.ndarray:
    """
    Calculate the intersection over area of box1, box2. Boxes are in x1y1x2y2 format.

    Args:
        box1 (np.ndarray): First set of boxes (N, 4)
        box2 (np.ndarray): Second set of boxes (M, 4)
        iou (bool): If True, calculate IoU, otherwise calculate IoA

    Returns:
        np.ndarray: IoU/IoA matrix of shape (N, M)
    """
    # Returns the intersection over box1 area by default
    # box1: (N, 4), box2: (M, 4)
    N = box1.shape[0]
    M = box2.shape[0]

    # Calculate intersection
    tl = np.maximum(box1[:, None, :2], box2[:, :2])  # (N, M, 2)
    br = np.minimum(box1[:, None, 2:], box2[:, 2:])  # (N, M, 2)
    wh = np.maximum(0, br - tl)  # (N, M, 2)
    inter = wh[:, :, 0] * wh[:, :, 1]  # (N, M)

    # Calculate areas
    area1 = (box1[:, 2] - box1[:, 0]) * (box1[:, 3] - box1[:, 1])  # (N,)
    area2 = (box2[:, 2] - box2[:, 0]) * (box2[:, 3] - box2[:, 1])  # (M,)

    if iou:
        union = area1[:, None] + area2 - inter
        return inter / union
    else:
        return inter / area1[:, None]


def iou_distance(atracks: list, btracks: list) -> np.ndarray:
    """
    Compute cost based on Intersection over Union (IoU) between tracks.

    Args:
        atracks (List[STrack] or List[np.ndarray]): List of tracks 'a' or bounding boxes.
        btracks (List[STrack] or List[np.ndarray]): List of tracks 'b' or bounding boxes.

    Returns:
        (np.ndarray): Cost matrix computed based on IoU with shape (len(atracks), len(btracks)).
    """
    if atracks and isinstance(atracks[0], np.ndarray) or btracks and isinstance(btracks[0], np.ndarray):
        atlbrs = atracks
        btlbrs = btracks
    else:
        # Extract bounding boxes from track objects
        atlbrs = []
        btlbrs = []
        for track in atracks:
            if hasattr(track, 'xyxy'):
                atlbrs.append(track.xyxy)
            elif hasattr(track, 'tlwh'):
                tlwh = track.tlwh
                atlbrs.append([tlwh[0], tlwh[1], tlwh[0] + tlwh[2], tlwh[1] + tlwh[3]])
            else:
                atlbrs.append([0, 0, 0, 0])
        
        for track in btracks:
            if hasattr(track, 'xyxy'):
                btlbrs.append(track.xyxy)
            elif hasattr(track, 'tlwh'):
                tlwh = track.tlwh
                btlbrs.append([tlwh[0], tlwh[1], tlwh[0] + tlwh[2], tlwh[1] + tlwh[3]])
            else:
                btlbrs.append([0, 0, 0, 0])

    ious = np.zeros((len(atlbrs), len(btlbrs)), dtype=np.float32)
    if len(atlbrs) and len(btlbrs):
        ious = bbox_ioa(
            np.ascontiguousarray(atlbrs, dtype=np.float32),
            np.ascontiguousarray(btlbrs, dtype=np.float32),
            iou=True,
        )
    return 1 - ious  # cost matrix


def embedding_distance(tracks: list, detections: list, metric: str = "cosine") -> np.ndarray:
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
    cost_matrix = np.zeros((len(tracks), len(detections)), dtype=np.float32)
    if cost_matrix.size == 0:
        return cost_matrix
    
    # Extract features from detections
    det_features = []
    for det in detections:
        if hasattr(det, 'curr_feat') and det.curr_feat is not None:
            det_features.append(det.curr_feat)
        else:
            det_features.append(np.zeros(128))  # Default feature size
    
    det_features = np.asarray(det_features, dtype=np.float32)
    
    # Extract features from tracks
    track_features = []
    for track in tracks:
        if hasattr(track, 'smooth_feat') and track.smooth_feat is not None:
            track_features.append(track.smooth_feat)
        else:
            track_features.append(np.zeros(128))  # Default feature size
    
    track_features = np.asarray(track_features, dtype=np.float32)
    
    cost_matrix = np.maximum(0.0, cdist(track_features, det_features, metric))
    return cost_matrix


def fuse_score(cost_matrix: np.ndarray, detections: list) -> np.ndarray:
    """
    Fuse cost matrix with detection scores to produce a single similarity matrix.

    Args:
        cost_matrix (np.ndarray): The matrix containing cost values for assignments, with shape (N, M).
        detections (List[BaseTrack]): List of detections, each containing a score attribute.

    Returns:
        (np.ndarray): Fused similarity matrix with shape (N, M).
    """
    if cost_matrix.size == 0:
        return cost_matrix
    iou_sim = 1 - cost_matrix
    det_scores = np.array([det.score for det in detections])
    det_scores = np.expand_dims(det_scores, axis=0).repeat(cost_matrix.shape[0], axis=0)
    fuse_sim = iou_sim * det_scores
    return 1 - fuse_sim  # fuse_cost 