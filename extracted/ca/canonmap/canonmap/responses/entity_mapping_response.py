from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class MatchItem(BaseModel):
    """A single match result for an entity."""
    entity: str
    score: float
    passes: int
    metadata: Dict[str, Any]
    field_name: Optional[str] = None
    table_name: Optional[str] = None
    source_name: Optional[str] = None

class SingleMapping(BaseModel):
    """Mapping results for a single input entity."""
    query: str
    matches: List[MatchItem]
    best_match: Optional[MatchItem] = None
    total_matches: int = 0
    processing_time_ms: Optional[float] = None

class EntityMappingResponse(BaseModel):
    """Response containing all entity mapping results.
    
    This model provides comprehensive information about the entity mapping process,
    including all matches, statistics, and any errors that occurred.
    """
    
    # Core response information
    status: str = "success"  # "success", "partial_success", "error"
    message: str = "Entity mapping completed successfully"
    
    # Mapping results
    results: List[SingleMapping] = Field(default_factory=list)
    
    # Processing statistics
    total_entities_processed: int = 0
    total_matches_found: int = 0
    average_processing_time_ms: Optional[float] = None
    processing_time_seconds: Optional[float] = None
    
    # Error information
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # Configuration summary
    num_results_requested: int = 15
    threshold_used: float = 0.0
    weights_used: Dict[str, float] = Field(default_factory=dict)
    use_semantic_search: bool = True
    
    # Metadata
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary for serialization."""
        return {
            'status': self.status,
            'message': self.message,
            'results': [result.dict() for result in self.results],
            'total_entities_processed': self.total_entities_processed,
            'total_matches_found': self.total_matches_found,
            'average_processing_time_ms': self.average_processing_time_ms,
            'processing_time_seconds': self.processing_time_seconds,
            'errors': self.errors,
            'warnings': self.warnings,
            'num_results_requested': self.num_results_requested,
            'threshold_used': self.threshold_used,
            'weights_used': self.weights_used,
            'use_semantic_search': self.use_semantic_search,
            'request_id': self.request_id,
            'timestamp': self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EntityMappingResponse':
        """Create a response from a dictionary."""
        # Convert nested objects
        results = [SingleMapping(**result) for result in data.get('results', [])]
        
        return cls(
            status=data.get('status', 'success'),
            message=data.get('message', 'Entity mapping completed successfully'),
            results=results,
            total_entities_processed=data.get('total_entities_processed', 0),
            total_matches_found=data.get('total_matches_found', 0),
            average_processing_time_ms=data.get('average_processing_time_ms'),
            processing_time_seconds=data.get('processing_time_seconds'),
            errors=data.get('errors', []),
            warnings=data.get('warnings', []),
            num_results_requested=data.get('num_results_requested', 15),
            threshold_used=data.get('threshold_used', 0.0),
            weights_used=data.get('weights_used', {}),
            use_semantic_search=data.get('use_semantic_search', True),
            request_id=data.get('request_id'),
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.now(),
        )
    
    def add_mapping(self, query: str, matches: List[MatchItem], processing_time_ms: Optional[float] = None):
        """Add a mapping result for a single entity."""
        best_match = max(matches, key=lambda m: m.score) if matches else None
        mapping = SingleMapping(
            query=query,
            matches=matches,
            best_match=best_match,
            total_matches=len(matches),
            processing_time_ms=processing_time_ms
        )
        self.results.append(mapping)
        self.total_entities_processed += 1
        self.total_matches_found += len(matches)
    
    def add_error(self, error_type: str, error_message: str, entity: Optional[str] = None):
        """Add an error to the response."""
        error = {
            'error_type': error_type,
            'error_message': error_message,
            'entity': entity
        }
        self.errors.append(error)
        if self.status == "success":
            self.status = "partial_success"
    
    def add_warning(self, warning_message: str):
        """Add a warning to the response."""
        self.warnings.append(warning_message)
    
    def set_processing_stats(self, total_entities: int, total_matches: int, 
                           processing_time_seconds: float, average_time_ms: Optional[float] = None):
        """Set processing statistics."""
        self.total_entities_processed = total_entities
        self.total_matches_found = total_matches
        self.processing_time_seconds = processing_time_seconds
        self.average_processing_time_ms = average_time_ms
    
    def set_config_summary(self, num_results: int, threshold: float, weights: Dict[str, float], 
                          use_semantic_search: bool):
        """Set configuration summary."""
        self.num_results_requested = num_results
        self.threshold_used = threshold
        self.weights_used = weights
        self.use_semantic_search = use_semantic_search 