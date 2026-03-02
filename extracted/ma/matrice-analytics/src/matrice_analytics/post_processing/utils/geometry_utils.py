"""
Geometry utility functions for post-processing operations.
"""

import math
from typing import List, Dict, Tuple, Union


def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if point is inside polygon using ray casting algorithm.
    
    Args:
        point: (x, y) coordinate tuple
        polygon: List of (x, y) coordinate tuples defining the polygon
        
    Returns:
        bool: True if point is inside polygon
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def get_bbox_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
        
    Returns:
        Tuple[float, float]: (x, y) center coordinates
    """
    if isinstance(bbox, list):
        # Handle list format [x1, y1, x2, y2]
        if len(bbox) >= 4:
            return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
        return (0, 0)
    
    elif isinstance(bbox, dict):
        # Handle dict formats
        if "xmin" in bbox and "xmax" in bbox and "ymin" in bbox and "ymax" in bbox:
            return ((bbox["xmin"] + bbox["xmax"]) / 2, (bbox["ymin"] + bbox["ymax"]) / 2)
        elif "x1" in bbox and "x2" in bbox and "y1" in bbox and "y2" in bbox:
            return ((bbox["x1"] + bbox["x2"]) / 2, (bbox["y1"] + bbox["y2"]) / 2)
        else:
            # Handle different bbox formats
            keys = list(bbox.keys())
            if len(keys) >= 4:
                values = list(bbox.values())
                return ((values[0] + values[2]) / 2, (values[1] + values[3]) / 2)
    
    return (0, 0)
    
def get_bbox_bottom25_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom 25% center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
        
    Returns:
        Tuple[float, float]: (x, y) coordinates at bottom 25% height from center X
    """
    if isinstance(bbox, list):
        # Handle list format [x1, y1, x2, y2]
        if len(bbox) >= 4:
            x_center = (bbox[0] + bbox[2]) / 2
            height = bbox[3] - bbox[1]
            y_target = bbox[3] - 0.25 * height
            return (x_center, y_target)
        return (0, 0)
    
    elif isinstance(bbox, dict):
        # Handle dict formats
        if "xmin" in bbox and "xmax" in bbox and "ymin" in bbox and "ymax" in bbox:
            x_center = (bbox["xmin"] + bbox["xmax"]) / 2
            height = bbox["ymax"] - bbox["ymin"]
            y_target = bbox["ymax"] - 0.25 * height
            return (x_center, y_target)
        elif "x1" in bbox and "x2" in bbox and "y1" in bbox and "y2" in bbox:
            x_center = (bbox["x1"] + bbox["x2"]) / 2
            height = bbox["y2"] - bbox["y1"]
            y_target = bbox["y2"] - 0.25 * height
            return (x_center, y_target)
        else:
            # Handle different bbox formats
            keys = list(bbox.keys())
            if len(keys) >= 4:
                values = list(bbox.values())
                x_center = (values[0] + values[2]) / 2
                height = values[3] - values[1]
                y_target = values[3] - 0.25 * height
                return (x_center, y_target)
    
    return (0, 0)

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
        
    Returns:
        float: Euclidean distance
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def calculate_bbox_overlap(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.
    
    Args:
        bbox1: First bounding box
        bbox2: Second bounding box
        
    Returns:
        float: IoU value between 0 and 1
    """
    return calculate_iou(bbox1, bbox2)


def calculate_iou(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.
    
    Args:
        bbox1: First bounding box
        bbox2: Second bounding box
        
    Returns:
        float: IoU value between 0 and 1
    """
    # Normalize bbox format
    def normalize_bbox_coords(bbox):
        if "xmin" in bbox:
            return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
        elif "x1" in bbox:
            return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
        else:
            values = list(bbox.values())
            return values[:4]
    
    box1 = normalize_bbox_coords(bbox1)
    box2 = normalize_bbox_coords(bbox2)
    
    # Calculate intersection
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    if x2 < x1 or y2 < y1:
        return 0.0
    
    intersection = (x2 - x1) * (y2 - y1)
    
    # Calculate union
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0.0


def get_bbox_area(bbox: Dict[str, float]) -> float:
    """
    Calculate area of bounding box.
    
    Args:
        bbox: Bounding box dict
        
    Returns:
        float: Area of the bounding box
    """
    if "xmin" in bbox and "xmax" in bbox and "ymin" in bbox and "ymax" in bbox:
        return (bbox["xmax"] - bbox["xmin"]) * (bbox["ymax"] - bbox["ymin"])
    elif "x1" in bbox and "x2" in bbox and "y1" in bbox and "y2" in bbox:
        return (bbox["x2"] - bbox["x1"]) * (bbox["y2"] - bbox["y1"])
    else:
        values = list(bbox.values())
        if len(values) >= 4:
            return (values[2] - values[0]) * (values[3] - values[1])
    return 0.0


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
    if "xmin" in bbox:
        return {
            "xmin": bbox["xmin"] / image_width,
            "ymin": bbox["ymin"] / image_height,
            "xmax": bbox["xmax"] / image_width,
            "ymax": bbox["ymax"] / image_height
        }
    elif "x1" in bbox:
        return {
            "x1": bbox["x1"] / image_width,
            "y1": bbox["y1"] / image_height,
            "x2": bbox["x2"] / image_width,
            "y2": bbox["y2"] / image_height
        }
    else:
        # Handle generic format
        keys = list(bbox.keys())
        values = list(bbox.values())
        normalized_values = [
            values[0] / image_width,
            values[1] / image_height,
            values[2] / image_width,
            values[3] / image_height
        ]
        return dict(zip(keys, normalized_values))


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
    if "xmin" in bbox:
        return {
            "xmin": bbox["xmin"] * image_width,
            "ymin": bbox["ymin"] * image_height,
            "xmax": bbox["xmax"] * image_width,
            "ymax": bbox["ymax"] * image_height
        }
    elif "x1" in bbox:
        return {
            "x1": bbox["x1"] * image_width,
            "y1": bbox["y1"] * image_height,
            "x2": bbox["x2"] * image_width,
            "y2": bbox["y2"] * image_height
        }
    else:
        # Handle generic format
        keys = list(bbox.keys())
        values = list(bbox.values())
        denormalized_values = [
            values[0] * image_width,
            values[1] * image_height,
            values[2] * image_width,
            values[3] * image_height
        ]
        return dict(zip(keys, denormalized_values))


def line_segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float], 
                           p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
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
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4) 