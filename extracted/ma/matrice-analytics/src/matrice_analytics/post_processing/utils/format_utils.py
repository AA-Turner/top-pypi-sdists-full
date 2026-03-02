"""
Format conversion utilities for post-processing operations.
"""

from typing import Any, Dict, List, Optional
from ..core.base import ResultFormat


def match_results_structure(results):
    """
    Match the results structure to the expected structure based on actual output formats.
    
    Based on eg_output.json:
    - Classification: {"category": str, "confidence": float}
    - Detection: [{"bounding_box": {...}, "category": str, "confidence": float}, ...]
    - Instance Segmentation: Same as detection but with "masks" field
    - Object Tracking: {"frame_id": [{"track_id": int, "category": str, "confidence": float, "bounding_box": {...}}, ...]}
    - Activity Recognition: {"frame_id": [{"category": str, "confidence": float, "bounding_box": {...}}, ...]} (no track_id)
    
    Args:
        results: Raw model output to analyze
        
    Returns:
        ResultFormat: Detected format type
    """
    if isinstance(results, list):
        # Array format - detection, instance segmentation, or face recognition
        if len(results) > 0 and isinstance(results[0], dict):
            if results[0].get("masks"):
                return ResultFormat.INSTANCE_SEGMENTATION
            elif results[0].get("embedding") or results[0].get("landmarks"):
                return ResultFormat.FACE_RECOGNITION
            elif "bounding_box" in results[0] and "category" in results[0] and "confidence" in results[0]:
                return ResultFormat.DETECTION
        return ResultFormat.DETECTION  # Default for list format
    
    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "category" in results and "confidence" in results and len(results) == 2:
            return ResultFormat.CLASSIFICATION
        
        # Check if it's frame-based (tracking or activity recognition)
        # Keys should be frame numbers or frame identifiers
        frame_keys = list(results.keys())
        if frame_keys and all(isinstance(k, (str, int)) for k in frame_keys):
            # Check the first frame's content to determine type
            first_frame_data = list(results.values())[0]
            if isinstance(first_frame_data, list) and len(first_frame_data) > 0:
                first_detection = first_frame_data[0]
                if isinstance(first_detection, dict):
                    # Check for face recognition format first (has embedding or landmarks)
                    if first_detection.get("embedding") or first_detection.get("landmarks"):
                        return ResultFormat.FACE_RECOGNITION
                    # Check if it has track_id (object tracking) or not (activity recognition)
                    elif "track_id" in first_detection:
                        return ResultFormat.OBJECT_TRACKING
                    elif "category" in first_detection and "confidence" in first_detection:
                        return ResultFormat.ACTIVITY_RECOGNITION
        
        # If we can't determine the type, check for typical classification structure
        if "category" in results and "confidence" in results:
            return ResultFormat.CLASSIFICATION
    
    return ResultFormat.UNKNOWN


def convert_to_coco_format(results: Any) -> List[Dict]:
    """
    Convert results to COCO format.
    
    Args:
        results: Input results in any supported format
        
    Returns:
        List[Dict]: Results in COCO format
    """
    if isinstance(results, list):
        # Already in detection format, convert to COCO
        coco_results = []
        for i, detection in enumerate(results):
            bbox = detection.get("bounding_box", detection.get("bbox", {}))
            
            # Convert to COCO bbox format [x, y, width, height]
            if "xmin" in bbox:
                coco_bbox = [
                    bbox["xmin"],
                    bbox["ymin"], 
                    bbox["xmax"] - bbox["xmin"],
                    bbox["ymax"] - bbox["ymin"]
                ]
            elif "x1" in bbox:
                coco_bbox = [
                    bbox["x1"],
                    bbox["y1"],
                    bbox["x2"] - bbox["x1"],
                    bbox["y2"] - bbox["y1"]
                ]
            else:
                # Assume generic format
                values = list(bbox.values())
                coco_bbox = [values[0], values[1], values[2] - values[0], values[3] - values[1]]
            
            coco_result = {
                "id": i,
                "category_id": detection.get("category_id", 0),
                "category": detection.get("category", "unknown"),
                "bbox": coco_bbox,
                "score": detection.get("confidence", 0.0),
                "area": coco_bbox[2] * coco_bbox[3]
            }
            
            if "masks" in detection:
                coco_result["segmentation"] = detection["masks"]
            
            # Add face recognition specific fields if present
            if "embedding" in detection:
                coco_result["embedding"] = detection["embedding"]
            if "landmarks" in detection:
                coco_result["landmarks"] = detection["landmarks"]
            
            coco_results.append(coco_result)
        
        return coco_results
    
    elif isinstance(results, dict):
        # Handle frame-based results
        coco_results = []
        result_id = 0
        
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                for detection in detections:
                    bbox = detection.get("bounding_box", detection.get("bbox", {}))
                    
                    # Convert to COCO bbox format
                    if "xmin" in bbox:
                        coco_bbox = [
                            bbox["xmin"],
                            bbox["ymin"],
                            bbox["xmax"] - bbox["xmin"],
                            bbox["ymax"] - bbox["ymin"]
                        ]
                    else:
                        values = list(bbox.values())
                        coco_bbox = [values[0], values[1], values[2] - values[0], values[3] - values[1]]
                    
                    coco_result = {
                        "id": result_id,
                        "frame_id": frame_id,
                        "category_id": detection.get("category_id", 0),
                        "category": detection.get("category", "unknown"),
                        "bbox": coco_bbox,
                        "score": detection.get("confidence", 0.0),
                        "area": coco_bbox[2] * coco_bbox[3]
                    }
                    
                    if "track_id" in detection:
                        coco_result["track_id"] = detection["track_id"]
                    
                    # Add face recognition specific fields if present
                    if "embedding" in detection:
                        coco_result["embedding"] = detection["embedding"]
                    if "landmarks" in detection:
                        coco_result["landmarks"] = detection["landmarks"]
                    
                    coco_results.append(coco_result)
                    result_id += 1
        
        return coco_results
    
    return []


def convert_to_yolo_format(results: Any) -> List[List[float]]:
    """
    Convert results to YOLO format (normalized coordinates).
    
    Args:
        results: Input results in any supported format
        
    Returns:
        List[List[float]]: Results in YOLO format [class_id, x_center, y_center, width, height, confidence]
    """
    yolo_results = []
    
    if isinstance(results, list):
        for detection in results:
            bbox = detection.get("bounding_box", detection.get("bbox", {}))
            
            # Convert to normalized center coordinates
            if "xmin" in bbox:
                x_center = (bbox["xmin"] + bbox["xmax"]) / 2
                y_center = (bbox["ymin"] + bbox["ymax"]) / 2
                width = bbox["xmax"] - bbox["xmin"]
                height = bbox["ymax"] - bbox["ymin"]
            else:
                values = list(bbox.values())
                x_center = (values[0] + values[2]) / 2
                y_center = (values[1] + values[3]) / 2
                width = values[2] - values[0]
                height = values[3] - values[1]
            
            yolo_result = [
                detection.get("category_id", 0),
                x_center,
                y_center,
                width,
                height,
                detection.get("confidence", 0.0)
            ]
            yolo_results.append(yolo_result)
    
    return yolo_results


def convert_to_tracking_format(detections: List[Dict], frame_id: str = "0") -> Dict:
    """
    Convert detection format to tracking format.
    
    Args:
        detections: List of detection dictionaries
        frame_id: Frame identifier
        
    Returns:
        Dict: Results in tracking format
    """
    tracking_results = {frame_id: []}
    
    for detection in detections:
        tracking_detection = {
            "track_id": detection.get("track_id", 0),
            "category": detection.get("category", "unknown"),
            "confidence": detection.get("confidence", 0.0),
            "bounding_box": detection.get("bounding_box", detection.get("bbox", {}))
        }
        
        # Add face recognition specific fields if present
        if "embedding" in detection:
            tracking_detection["embedding"] = detection["embedding"]
        if "landmarks" in detection:
            tracking_detection["landmarks"] = detection["landmarks"]
        
        tracking_results[frame_id].append(tracking_detection)
    
    return tracking_results


def convert_detection_to_tracking_format(detections: List[Dict], frame_id: str = "0") -> Dict:
    """
    Convert detection format to tracking format.
    
    Args:
        detections: List of detection dictionaries
        frame_id: Frame identifier
        
    Returns:
        Dict: Results in tracking format
    """
    return convert_to_tracking_format(detections, frame_id)


def convert_tracking_to_detection_format(tracking_results: Dict) -> List[Dict]:
    """
    Convert tracking format to detection format.
    
    Args:
        tracking_results: Tracking results dictionary
        
    Returns:
        List[Dict]: Results in detection format
    """
    detections = []
    
    for frame_id, frame_detections in tracking_results.items():
        if isinstance(frame_detections, list):
            for detection in frame_detections:
                detection_item = {
                    "category": detection.get("category", "unknown"),
                    "confidence": detection.get("confidence", 0.0),
                    "bounding_box": detection.get("bounding_box", detection.get("bbox", {}))
                }
                if "track_id" in detection:
                    detection_item["track_id"] = detection["track_id"]
                
                # Add face recognition specific fields if present
                if "embedding" in detection:
                    detection_item["embedding"] = detection["embedding"]
                if "landmarks" in detection:
                    detection_item["landmarks"] = detection["landmarks"]
                
                detections.append(detection_item)
    
    return detections 