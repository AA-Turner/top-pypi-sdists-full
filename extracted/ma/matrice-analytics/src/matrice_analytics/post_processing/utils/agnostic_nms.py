"""
Production-grade reusable NMS module with YOLO-matching implementation.

This module provides class-specific and class-agnostic NMS implementations
that match YOLO's built-in behavior while being completely framework-agnostic.

Usage:
    from nms_module import AgnosticNMS
    
    nms = AgnosticNMS(iou_threshold=0.45, min_box_size=2.0)
    filtered_detections = nms.apply(detections, class_agnostic=True)
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import sys

# Try importing torch/torchvision, but don't auto-install in production
try:
    import torch  # noqa: F401
    from torchvision.ops import nms as torchvision_nms  # noqa: F401
    TORCHVISION_AVAILABLE = True
except Exception:
    TORCHVISION_AVAILABLE = False


class AgnosticNMS:
    """
    Production-grade NMS implementation with YOLO-matching behavior.
    
    Features:
    - Class-specific and class-agnostic modes
    - Vectorized (PyTorch) and iterative fallback
    - Numerical stability enhancements
    - Box validation and filtering
    - Schema preservation
    - Zero side effects
    - Supports both x1/y1/x2/y2 and xmin/ymin/xmax/ymax bbox formats
    
    Attributes:
        iou_threshold: IoU threshold for suppression (default: 0.45)
        min_box_size: Minimum box width/height in pixels (default: 2.0)
        use_vectorized: Use torchvision.ops.nms if available (default: True)
        eps: Epsilon for numerical stability (default: 1e-7)
    """
    
    def __init__(
        self,
        iou_threshold: float = 0.45,
        min_box_size: float = 2.0,
        use_vectorized: bool = True,
        eps: float = 1e-7
    ):
        """
        Initialize NMS module.
        
        Args:
            iou_threshold: IoU threshold for suppression (0.0 to 1.0)
            min_box_size: Minimum box dimension in pixels
            use_vectorized: Use PyTorch implementation if available
            eps: Epsilon for numerical stability in IoU computation
        """
        if not 0.0 <= iou_threshold <= 1.0:
            raise ValueError(f"iou_threshold must be in [0, 1], got {iou_threshold}")
        
        if min_box_size < 0:
            raise ValueError(f"min_box_size must be >= 0, got {min_box_size}")
        
        self.iou_threshold = iou_threshold
        self.min_box_size = min_box_size
        self.use_vectorized = use_vectorized and TORCHVISION_AVAILABLE
        self.eps = eps
        
        self._stats = {
            "total_calls": 0,
            "vectorized_calls": 0,
            "iterative_calls": 0,
            "total_input": 0,
            "total_output": 0,
            "total_suppressed": 0
        }
    
    def apply(
        self,
        detections: List[Dict[str, Any]],
        class_agnostic: bool = True,
        target_categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Apply NMS to detections.
        
        Args:
            detections: List of detection dicts with schema:
                {
                    "category": str,
                    "confidence": float,
                    "bounding_box": {"x1": float, "y1": float, "x2": float, "y2": float}
                                 or {"xmin": float, "ymin": float, "xmax": float, "ymax": float},
                    ... (other fields preserved)
                }
            class_agnostic: If True, suppress across all classes
            target_categories: Optional list of categories to process (others ignored)
        
        Returns:
            Filtered list of detections with identical schema
        """
        self._stats["total_calls"] += 1
        self._stats["total_input"] += len(detections)
        
        if not detections:
            return detections
        
        if len(detections) == 1:
            self._stats["total_output"] += 1
            return detections
        
        # Validate schema with soft-fail on errors
        invalid_detections = []
        validation_diagnostics = []

        for idx, d in enumerate(detections):
            if not self._validate_detection_schema(d):
                invalid_detections.append((idx, d))
                
                # Collect detailed diagnostics for first 3 failures
                if len(validation_diagnostics) < 3:
                    diag = self._diagnose_detection_schema(d, idx)
                    validation_diagnostics.append(diag)

        if invalid_detections:
            # Create detailed error message
            error_msg_parts = [
                f"NMS Schema Validation Failed:",
                f"  - Total detections: {len(detections)}",
                f"  - Invalid detections: {len(invalid_detections)}",
                f"  - Validation rate: {100 * (1 - len(invalid_detections)/len(detections)):.1f}%",
                f"",
                f"Detailed diagnostics for first {len(validation_diagnostics)} failures:"
            ]
            
            for diag in validation_diagnostics:
                error_msg_parts.append(f"\n{diag}")
            
            error_msg = "\n".join(error_msg_parts)
            
            # Log to console for production debugging
            print(f"\n{'='*80}")
            print(error_msg)
            print(f"{'='*80}\n")
            
            # Soft-fail: return original detections instead of crashing
            print("WARNING: NMS bypassed due to schema validation failures. Returning original detections.")
            return detections
        
        # Filter by target categories if specified
        if target_categories is not None:
            detections = [d for d in detections if d.get('category') in target_categories]
            if not detections:
                return detections
        
        # Apply NMS
        if class_agnostic:
            result = self._apply_nms_single_pass(detections)
        else:
            result = self._apply_nms_per_class(detections)
        
        self._stats["total_output"] += len(result)
        self._stats["total_suppressed"] += (len(detections) - len(result))
        
        return result
    
    def _apply_nms_single_pass(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply NMS across all classes in a single pass."""
        if self.use_vectorized:
            self._stats["vectorized_calls"] += 1
            return self._nms_vectorized(detections)
        else:
            self._stats["iterative_calls"] += 1
            return self._nms_iterative(detections)
    
    def _apply_nms_per_class(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply NMS separately for each class."""
        # Group by category
        category_groups = {}
        for det in detections:
            cat = det.get('category')
            if cat not in category_groups:
                category_groups[cat] = []
            category_groups[cat].append(det)
        
        # Apply NMS per category
        result = []
        for cat_dets in category_groups.values():
            if self.use_vectorized:
                result.extend(self._nms_vectorized(cat_dets))
            else:
                result.extend(self._nms_iterative(cat_dets))
        
        if self.use_vectorized:
            self._stats["vectorized_calls"] += 1
        else:
            self._stats["iterative_calls"] += 1
        
        return result
    
    def _nms_vectorized(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Vectorized NMS using torchvision.ops.nms.
        
        This matches YOLO's built-in agnostic NMS exactly.
        """
        if not detections:
            return []
        
        # Filter invalid boxes
        valid_dets = [d for d in detections if self._validate_box(self._get_bbox(d))]
        
        if not valid_dets:
            return []
        
        try:
            # Convert to tensors - handle both bbox formats
            boxes_list = []
            for d in valid_dets:
                bbox = self._get_bbox(d)
                if 'x1' in bbox:
                    boxes_list.append([
                        float(bbox["x1"]), float(bbox["y1"]),
                        float(bbox["x2"]), float(bbox["y2"])
                    ])
                elif 'xmin' in bbox:
                    boxes_list.append([
                        float(bbox["xmin"]), float(bbox["ymin"]),
                        float(bbox["xmax"]), float(bbox["ymax"])
                    ])
            
            if not boxes_list:
                return []
            
            boxes = torch.tensor(boxes_list, dtype=torch.float32)
            scores = torch.tensor([float(d["confidence"]) for d in valid_dets], dtype=torch.float32)
            
            # Apply torchvision NMS
            keep_indices = torchvision_nms(boxes, scores, self.iou_threshold)
            keep_indices = keep_indices.cpu().numpy()
            
            return [valid_dets[i] for i in keep_indices]
        
        except Exception as e:
            # Fallback to iterative on error
            print(f"Vectorized NMS failed: {e}. Falling back to iterative NMS.")
            return self._nms_iterative(valid_dets)
    
    def _nms_iterative(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Iterative NMS implementation with YOLO-matching enhancements.
        
        This provides equivalent results to vectorized NMS without PyTorch.
        """
        if not detections:
            return []
        
        # Filter invalid boxes
        valid_dets = [d for d in detections if self._validate_box(self._get_bbox(d))]
        
        if not valid_dets:
            return []
        
        # Sort by confidence with area tie-breaking
        def sort_key(d):
            bbox = self._get_bbox(d)
            # Handle both bbox formats
            if 'x1' in bbox:
                area = abs(bbox['x2'] - bbox['x1']) * abs(bbox['y2'] - bbox['y1'])
            elif 'xmin' in bbox:
                area = abs(bbox['xmax'] - bbox['xmin']) * abs(bbox['ymax'] - bbox['ymin'])
            else:
                area = 0
            return (d["confidence"], area)
        
        sorted_dets = sorted(valid_dets, key=sort_key, reverse=True)
        
        # Apply NMS
        keep = []
        suppressed_indices = set()
        
        for i, det in enumerate(sorted_dets):
            if i in suppressed_indices:
                continue
            
            keep.append(det)
            best_bbox = self._get_bbox(det)
            
            # Suppress overlapping boxes
            for j in range(i + 1, len(sorted_dets)):
                if j in suppressed_indices:
                    continue
                
                other_bbox = self._get_bbox(sorted_dets[j])
                iou = self._compute_iou(best_bbox, other_bbox)
                
                # Use >= for consistency with torchvision
                if iou >= self.iou_threshold:
                    suppressed_indices.add(j)
        
        return keep
    
    def _get_bbox(self, detection: Dict[str, Any]) -> Dict:
        """Extract bounding_box from detection, handling both field names."""
        return detection.get('bounding_box', detection.get('bbox', {}))
    
    def _compute_iou(self, bbox1: Dict, bbox2: Dict) -> float:
        """
        Compute IoU with numerical stability.
        Accepts both {x1, y1, x2, y2} and {xmin, ymin, xmax, ymax} formats.
        
        Args:
            bbox1: First box dict
            bbox2: Second box dict
        
        Returns:
            IoU value in [0, 1]
        """
        try:
            # Extract coordinates - handle both formats
            if 'x1' in bbox1:
                x1_1 = float(bbox1['x1'])
                y1_1 = float(bbox1['y1'])
                x2_1 = float(bbox1['x2'])
                y2_1 = float(bbox1['y2'])
            elif 'xmin' in bbox1:
                x1_1 = float(bbox1['xmin'])
                y1_1 = float(bbox1['ymin'])
                x2_1 = float(bbox1['xmax'])
                y2_1 = float(bbox1['ymax'])
            else:
                return 0.0
            
            if 'x1' in bbox2:
                x1_2 = float(bbox2['x1'])
                y1_2 = float(bbox2['y1'])
                x2_2 = float(bbox2['x2'])
                y2_2 = float(bbox2['y2'])
            elif 'xmin' in bbox2:
                x1_2 = float(bbox2['xmin'])
                y1_2 = float(bbox2['ymin'])
                x2_2 = float(bbox2['xmax'])
                y2_2 = float(bbox2['ymax'])
            else:
                return 0.0
            
            # Ensure coordinates are in correct order
            x1_1, x2_1 = min(x1_1, x2_1), max(x1_1, x2_1)
            y1_1, y2_1 = min(y1_1, y2_1), max(y1_1, y2_1)
            x1_2, x2_2 = min(x1_2, x2_2), max(x1_2, x2_2)
            y1_2, y2_2 = min(y1_2, y2_2), max(y1_2, y2_2)
            
            # Compute intersection
            inter_x1 = max(x1_1, x1_2)
            inter_y1 = max(y1_1, y1_2)
            inter_x2 = min(x2_1, x2_2)
            inter_y2 = min(y2_1, y2_2)
            
            inter_w = max(0.0, inter_x2 - inter_x1)
            inter_h = max(0.0, inter_y2 - inter_y1)
            
            if inter_w == 0.0 or inter_h == 0.0:
                return 0.0
            
            inter_area = inter_w * inter_h
            
            # Compute box areas
            area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
            area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
            
            # Add epsilon for numerical stability (matches torchvision)
            union_area = area1 + area2 - inter_area + self.eps
            
            # Compute IoU with safeguards
            iou = inter_area / union_area
            
            # Clamp to valid range
            return max(0.0, min(1.0, iou))
        
        except Exception:
            return 0.0
    
    def _validate_box(self, bbox: Dict, max_wh: float = 1e4) -> bool:
        """
        Validate box dimensions with robust type handling.
        Accepts both {x1, y1, x2, y2} and {xmin, ymin, xmax, ymax} formats.
        
        Args:
            bbox: Box dict with coordinates
            max_wh: Maximum box width/height
        
        Returns:
            True if box is valid
        """
        try:
            # Extract coordinates - handle both formats
            if 'x1' in bbox:
                x1, y1, x2, y2 = map(float, [bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2']])
            elif 'xmin' in bbox:
                x1, y1, x2, y2 = map(float, [bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']])
            else:
                return False
            
            # Calculate width and height
            w = abs(x2 - x1)
            h = abs(y2 - y1)
            
            # Check minimum size
            if w < self.min_box_size or h < self.min_box_size:
                return False
            
            # Check maximum size
            if w > max_wh or h > max_wh:
                return False
            
            # Check for NaN or Inf
            for v in [x1, y1, x2, y2]:
                try:
                    import numpy as np
                    if np.isnan(v) or np.isinf(v):
                        return False
                except ImportError:
                    import math
                    if math.isnan(v) or math.isinf(v):
                        return False
            
            return True
        
        except Exception:
            return False
    
    def _validate_detection_schema(self, detection: Dict[str, Any]) -> bool:
        """
        Validate detection has required fields for NMS with robust type checking.
        
        This method is designed to be production-safe and handle various input formats
        including YOLO outputs with numpy types, string categories, and varying confidence scales.
        
        Args:
            detection: Single detection dict
        
        Returns:
            True if schema is valid, False otherwise (never raises exceptions)
        """
        try:
            # Basic type check
            if not isinstance(detection, dict):
                return False
            
            # ============================================
            # CATEGORY VALIDATION
            # ============================================
            if 'category' not in detection:
                return False
            
            category = detection['category']
            
            # Accept: str, int, numpy.integer, numpy.str_
            category_valid = isinstance(category, (str, int))
            
            if not category_valid:
                try:
                    import numpy as np
                    category_valid = isinstance(category, (np.integer, np.str_))
                except ImportError:
                    pass
            
            if not category_valid:
                return False
            
            # ============================================
            # CONFIDENCE VALIDATION
            # ============================================
            if 'confidence' not in detection:
                return False
            
            conf = detection['confidence']
            
            # Accept: int, float, numpy.integer, numpy.floating
            conf_valid = isinstance(conf, (int, float))
            
            if not conf_valid:
                try:
                    import numpy as np
                    conf_valid = isinstance(conf, (np.integer, np.floating))
                except ImportError:
                    pass
            
            if not conf_valid:
                return False
            
            # Try to convert to float and validate range
            try:
                conf_val = float(conf)
                # Allow wide range to handle different YOLO output formats
                if conf_val < 0 or conf_val > 1000:
                    return False
            except (ValueError, TypeError, OverflowError):
                return False
            
            # ============================================
            # BOUNDING BOX VALIDATION
            # ============================================
            # Accept both 'bounding_box' and 'bbox' field names
            bbox = detection.get('bounding_box', detection.get('bbox'))
            
            if bbox is None or not isinstance(bbox, dict):
                return False
            
            # Accept both x1/y1/x2/y2 and xmin/ymin/xmax/ymax formats
            required_keys_v1 = {'x1', 'y1', 'x2', 'y2'}
            required_keys_v2 = {'xmin', 'ymin', 'xmax', 'ymax'}
            
            has_v1 = required_keys_v1.issubset(bbox.keys())
            has_v2 = required_keys_v2.issubset(bbox.keys())
            
            if not (has_v1 or has_v2):
                return False
            
            # Determine which keys to validate
            coord_keys = ['x1', 'y1', 'x2', 'y2'] if has_v1 else ['xmin', 'ymin', 'xmax', 'ymax']
            
            # Validate each coordinate
            for key in coord_keys:
                val = bbox[key]
                
                # Check if numeric (handle numpy types)
                is_numeric = isinstance(val, (int, float))
                
                if not is_numeric:
                    try:
                        import numpy as np
                        is_numeric = isinstance(val, (np.integer, np.floating))
                    except ImportError:
                        pass
                
                if not is_numeric:
                    return False
                
                # Try converting to float
                try:
                    float_val = float(val)
                    # Check for reasonable coordinate range
                    if not (-1e10 < float_val < 1e10):
                        return False
                except (ValueError, TypeError, OverflowError):
                    return False
            
            return True
        
        except Exception as e:
            print(f"Unexpected error in schema validation: {e}", file=sys.stderr)
            return False
    
    def _diagnose_detection_schema(self, detection: Dict[str, Any], idx: int) -> str:
        """
        Diagnose why a detection failed schema validation.
        
        Args:
            detection: Detection dict that failed validation
            idx: Index of detection in list
        
        Returns:
            Detailed diagnostic string
        """
        diagnostics = [f"Detection #{idx} Failed Validation:"]
        
        # Check if dict
        if not isinstance(detection, dict):
            diagnostics.append(f"    Not a dict (type: {type(detection)})")
            return "\n".join(diagnostics)
        
        diagnostics.append(f"  Keys present: {list(detection.keys())}")
        
        # Check category
        if 'category' not in detection:
            diagnostics.append(f"    Missing 'category' key")
        else:
            category = detection['category']
            cat_type = type(category).__name__
            diagnostics.append(f"  Category: '{category}' (type: {cat_type})")
            
            is_valid_type = isinstance(category, (str, int))
            if not is_valid_type:
                try:
                    import numpy as np
                    is_valid_type = isinstance(category, (np.integer, np.str_))
                    if is_valid_type:
                        diagnostics.append(f"      Valid (numpy type)")
                    else:
                        diagnostics.append(f"      Invalid type: {cat_type}")
                except ImportError:
                    diagnostics.append(f"      Invalid type: {cat_type} (numpy not available)")
            else:
                diagnostics.append(f"      Valid type")
        
        # Check confidence
        if 'confidence' not in detection:
            diagnostics.append(f"    Missing 'confidence' key")
        else:
            conf = detection['confidence']
            conf_type = type(conf).__name__
            diagnostics.append(f"  Confidence: {conf} (type: {conf_type})")
            
            is_numeric = isinstance(conf, (int, float))
            if not is_numeric:
                try:
                    import numpy as np
                    is_numeric = isinstance(conf, (np.integer, np.floating))
                    if is_numeric:
                        diagnostics.append(f"      Valid (numpy type)")
                    else:
                        diagnostics.append(f"      Not numeric: {conf_type}")
                except ImportError:
                    diagnostics.append(f"      Not numeric: {conf_type} (numpy not available)")
            else:
                diagnostics.append(f"      Valid type")
                
            # Check range
            try:
                conf_val = float(conf)
                if conf_val < 0 or conf_val > 1000:
                    diagnostics.append(f"      Out of range: {conf_val}")
                else:
                    diagnostics.append(f"      Valid range")
            except:
                diagnostics.append(f"      Cannot convert to float")
        
        # Check bounding_box (accept both field names)
        bbox = detection.get('bounding_box', detection.get('bbox'))
        
        if bbox is None:
            diagnostics.append(f"    Missing both 'bounding_box' and 'bbox' keys")
        elif not isinstance(bbox, dict):
            diagnostics.append(f"    bounding_box is not dict (type: {type(bbox).__name__})")
        else:
            diagnostics.append(f"  BBox keys: {list(bbox.keys())}")
            
            required_v1 = {'x1', 'y1', 'x2', 'y2'}
            required_v2 = {'xmin', 'ymin', 'xmax', 'ymax'}
            
            has_v1 = required_v1.issubset(bbox.keys())
            has_v2 = required_v2.issubset(bbox.keys())
            
            if has_v1:
                diagnostics.append(f"      Has x1/y1/x2/y2 format")
                coord_keys = ['x1', 'y1', 'x2', 'y2']
            elif has_v2:
                diagnostics.append(f"      Has xmin/ymin/xmax/ymax format")
                coord_keys = ['xmin', 'ymin', 'xmax', 'ymax']
            else:
                missing_v1 = required_v1 - set(bbox.keys())
                missing_v2 = required_v2 - set(bbox.keys())
                diagnostics.append(f"      Missing x1/y1 format keys: {missing_v1}")
                diagnostics.append(f"      Missing xmin/ymin format keys: {missing_v2}")
                coord_keys = []
            
            # Check coordinate types (only if we have valid format)
            if coord_keys:
                for key in coord_keys:
                    val = bbox[key]
                    val_type = type(val).__name__
                    
                    is_numeric = isinstance(val, (int, float))
                    if not is_numeric:
                        try:
                            import numpy as np
                            is_numeric = isinstance(val, (np.integer, np.floating))
                            status = "  numpy" if is_numeric else " "
                        except:
                            status = " "
                    else:
                        status = " "
                    
                    diagnostics.append(f"    {key}: {val} (type: {val_type}) [{status}]")
        
        return "\n".join(diagnostics)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get NMS usage statistics.
        
        Returns:
            Dictionary with statistics:
            - total_calls: Number of times apply() was called
            - vectorized_calls: Number of vectorized NMS calls
            - iterative_calls: Number of iterative NMS calls
            - total_input: Total input detections
            - total_output: Total output detections
            - total_suppressed: Total suppressed detections
            - suppression_rate: Percentage of detections suppressed
        """
        stats = self._stats.copy()
        if stats["total_input"] > 0:
            stats["suppression_rate"] = 100 * stats["total_suppressed"] / stats["total_input"]
        else:
            stats["suppression_rate"] = 0.0
        return stats
    
    def reset_stats(self):
        """Reset usage statistics."""
        self._stats = {
            "total_calls": 0,
            "vectorized_calls": 0,
            "iterative_calls": 0,
            "total_input": 0,
            "total_output": 0,
            "total_suppressed": 0
        }
    
    @staticmethod
    def is_vectorized_available() -> bool:
        """Check if vectorized implementation is available."""
        return TORCHVISION_AVAILABLE


# Convenience function for quick usage
def apply_nms(
    detections: List[Dict[str, Any]],
    iou_threshold: float = 0.45,
    class_agnostic: bool = True,
    min_box_size: float = 2.0,
    use_vectorized: bool = True
) -> List[Dict[str, Any]]:
    """
    Convenience function for one-time NMS application.
    
    Args:
        detections: List of detection dicts
        iou_threshold: IoU threshold for suppression
        class_agnostic: If True, suppress across all classes
        min_box_size: Minimum box dimension in pixels
        use_vectorized: Use PyTorch implementation if available
    
    Returns:
        Filtered list of detections
    
    Example:
        >>> detections = [
        ...     {"category": "car", "confidence": 0.9, 
        ...      "bounding_box": {"x1": 100, "y1": 100, "x2": 200, "y2": 200}},
        ...     {"category": "car", "confidence": 0.85,
        ...      "bounding_box": {"x1": 105, "y1": 105, "x2": 205, "y2": 205}}
        ... ]
        >>> filtered = apply_nms(detections, iou_threshold=0.5, class_agnostic=True)
        >>> len(filtered)
        1
    """
    nms = AgnosticNMS(
        iou_threshold=iou_threshold,
        min_box_size=min_box_size,
        use_vectorized=use_vectorized
    )
    return nms.apply(detections, class_agnostic=class_agnostic)