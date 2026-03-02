"""
Category mapping utilities for post-processing operations.
"""

from typing import List, Dict, Any
from .format_utils import match_results_structure


class CategoryMappingLibrary:
    """Library class for handling category mapping operations."""
    
    def __init__(self, index_to_category: Dict[int, str] = None):
        self.index_to_category = index_to_category or {}
    
    def map_results(self, results: Any) -> Any:
        """Map category indices to category names in results."""
        if not self.index_to_category:
            return results
            
        results_type = match_results_structure(results)
        
        if results_type == "detection":
            return self._map_detection_results(results)
        elif results_type == "classification":
            return self._map_classification_results(results)
        elif results_type == "object_tracking":
            return self._map_tracking_results(results)
        elif results_type == "activity_recognition":
            return self._map_activity_results(results)
        
        return results
    
    def _map_detection_results(self, results: List[Dict]) -> List[Dict]:
        """Map categories in detection results."""
        mapped_results = []
        for result in results:
            mapped_result = result.copy()
            if "category" in result and isinstance(result["category"], int):
                if result["category"] in self.index_to_category:
                    mapped_result["category"] = self.index_to_category[result["category"]]
            mapped_results.append(mapped_result)
        return mapped_results
    
    def _map_classification_results(self, results: Dict) -> Dict:
        """Map categories in classification results."""
        mapped_results = {}
        for key, value in results.items():
            if isinstance(value, int) and value in self.index_to_category:
                mapped_results[key] = self.index_to_category[value]
            else:
                mapped_results[key] = value
        return mapped_results
    
    def _map_tracking_results(self, results: Dict) -> Dict:
        """Map categories in tracking results."""
        mapped_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                mapped_results[frame_id] = self._map_detection_results(detections)
            else:
                mapped_results[frame_id] = detections
        return mapped_results
    
    def _map_activity_results(self, results: List[Dict]) -> List[Dict]:
        """Map categories in activity recognition results."""
        return self._map_detection_results(results)


def apply_category_mapping(results: Any, index_to_category: Dict[int, str]) -> Any:
    """
    Convenience function to apply category mapping to results.
    
    Args:
        results: Raw results to map
        index_to_category: Mapping from indices to category names
        
    Returns:
        Results with mapped categories
    """
    mapper = CategoryMappingLibrary(index_to_category)
    return mapper.map_results(results)


def create_category_mapper(index_to_category: Dict[int, str]) -> CategoryMappingLibrary:
    """
    Create a category mapper instance.
    
    Args:
        index_to_category: Mapping from indices to category names
        
    Returns:
        CategoryMappingLibrary instance
    """
    return CategoryMappingLibrary(index_to_category) 