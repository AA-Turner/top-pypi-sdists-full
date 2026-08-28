"""Auto-generated stub for module: matching."""
from typing import Any, List, Union

# Functions
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
