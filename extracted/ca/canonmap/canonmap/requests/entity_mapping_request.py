from pathlib import Path
from typing import Optional, List, Dict, Union, Any
from pydantic import BaseModel, Field

class TableFieldFilter(BaseModel):
    """Configuration for filtering which table fields to match against.
    
    Args:
        table_name: Name of the table to include in matching
        table_fields: List of fields within that table to match
    """
    table_name: str
    table_fields: List[str]

class EntityMappingRequest(BaseModel):
    """Configuration for mapping raw entities to canonical forms.
    
    This model defines parameters for matching raw entity strings against
    previously generated canonical entities, with configurable matching strategies
    and filters.
    
    Focuses on WHAT to match rather than WHERE to find artifacts.
    Storage configuration is handled by CanonMapArtifactsConfig.

    Args:
        entities: List of raw entity strings to map
        filters: Per-table filters to restrict matching fields (default: [])
        num_results: Max number of matches per query (default: 15)
        weights: Relative weights for each matching strategy (default: semantic=0.4, fuzzy=0.4, etc)
        use_semantic_search: Whether to use semantic-search-based matching (default: True)
        threshold: Score threshold (0-100) for a metric to count as a 'pass' (default: 0.0)
    """
    
    entities: List[str]
    filters: Optional[List[TableFieldFilter]] = Field(default_factory=list)
    num_results: int = 15
    weights: Dict[str, float] = Field(
        default_factory=lambda: {
            'semantic': 0.40,
            'fuzzy':    0.40,
            'initial':  0.10,
            'keyword':  0.05,
            'phonetic': 0.05,
        }
    )
    use_semantic_search: bool = True
    threshold: float = 0.0

    class Config:
        arbitrary_types_allowed = True  # Allow pandas DataFrame and Path objects

    def to_dict(self) -> Dict[str, Any]:
        """Convert the request to a dictionary for serialization."""
        return {
            'entities': self.entities,
            'filters': [{'table_name': f.table_name, 'table_fields': f.table_fields} for f in self.filters],
            'num_results': self.num_results,
            'weights': self.weights,
            'use_semantic_search': self.use_semantic_search,
            'threshold': self.threshold,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EntityMappingRequest':
        """Create a request from a dictionary."""
        # Convert nested field objects
        filters = [TableFieldFilter(**f) for f in data.get('filters', [])]
        
        return cls(
            entities=data['entities'],
            filters=filters,
            num_results=data.get('num_results', 15),
            weights=data.get('weights', {
                'semantic': 0.40,
                'fuzzy':    0.40,
                'initial':  0.10,
                'keyword':  0.05,
                'phonetic': 0.05,
            }),
            use_semantic_search=data.get('use_semantic_search', True),
            threshold=data.get('threshold', 0.0),
        )
