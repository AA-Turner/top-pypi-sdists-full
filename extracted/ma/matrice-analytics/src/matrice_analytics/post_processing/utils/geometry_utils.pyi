"""Auto-generated stub for module: geometry_utils."""
from typing import Dict, List, Tuple, Union

# Functions
def calculate_bbox_overlap(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.
    
    Args:
        bbox1: First bounding box
        bbox2: Second bounding box
    
    Returns:
        float: IoU value between 0 and 1
    """
    ...
def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
    
    Returns:
        float: Euclidean distance
    """
    ...
def calculate_iou(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.
    
    Args:
        bbox1: First bounding box
        bbox2: Second bounding box
    
    Returns:
        float: IoU value between 0 and 1
    """
    ...
def denormalize_bbox(bbox: Dict[str, float], image_width: float, image_height: float) -> Dict[str, float]:
    """
    Denormalize bounding box coordinates from [0, 1] range to pixel coordinates.
    
    Args:
        bbox: Normalized bounding box dict
        image_width: Image width
        image_height: Image height
    
    Returns:
        Dict[str, float]: Denormalized bounding box
    """
    ...
def get_bbox_area(bbox: Dict[str, float]) -> float:
    """
    Calculate area of bounding box.
    
    Args:
        bbox: Bounding box dict
    
    Returns:
        float: Area of the bounding box
    """
    ...
def get_bbox_bottom25_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom 25% center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
    
    Returns:
        Tuple[float, float]: (x, y) coordinates at bottom 25% height from center X
    """
    ...
def get_bbox_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
    
    Returns:
        Tuple[float, float]: (x, y) center coordinates
    """
    ...
def line_segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    """
    Check if two line segments intersect.
    
    Args:
        p1: First point of first line segment
        p2: Second point of first line segment
        p3: First point of second line segment
        p4: Second point of second line segment
    
    Returns:
        bool: True if line segments intersect
    """
    ...
def normalize_bbox(bbox: Dict[str, float], image_width: float, image_height: float) -> Dict[str, float]:
    """
    Normalize bounding box coordinates to [0, 1] range.
    
    Args:
        bbox: Bounding box dict
        image_width: Image width
        image_height: Image height
    
    Returns:
        Dict[str, float]: Normalized bounding box
    """
    ...
def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if point is inside polygon using ray casting algorithm.
    
    Args:
        point: (x, y) coordinate tuple
        polygon: List of (x, y) coordinate tuples defining the polygon
    
    Returns:
        bool: True if point is inside polygon
    """
    ...
