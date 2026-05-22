"""Auto-generated stub for module: category_mapping_utils."""
from typing import Any, Dict

from .format_utils import match_results_structure

# Functions
def apply_category_mapping(results: Any, index_to_category: Dict[int, str]) -> Any:
    """
    Convenience function to apply category mapping to results.
    
    Args:
        results: Raw results to map
        index_to_category: Mapping from indices to category names
    
    Returns:
        Results with mapped categories
    """
    ...
def create_category_mapper(index_to_category: Dict[int, str]) -> Any:
    """
    Create a category mapper instance.
    
    Args:
        index_to_category: Mapping from indices to category names
    
    Returns:
        CategoryMappingLibrary instance
    """
    ...

# Classes
class CategoryMappingLibrary:
    # Library class for handling category mapping operations.

    def __init__(self: Any, index_to_category: Dict[int, str] = None) -> None: ...

    def map_results(self: Any, results: Any) -> Any:
        """
        Map category indices to category names in results.
        """
        ...

