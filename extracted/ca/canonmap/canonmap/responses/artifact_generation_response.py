from pathlib import Path
from typing import Optional, List, Dict, Union, Any
from pydantic import BaseModel, Field
from datetime import datetime

class GeneratedArtifact(BaseModel):
    """Information about a single generated artifact file."""
    artifact_type: str
    file_path: str
    file_size_bytes: Optional[int] = None
    table_name: Optional[str] = None
    source_name: Optional[str] = None

class ProcessingStats(BaseModel):
    """Statistics about the processing operation."""
    total_tables_processed: int
    total_rows_processed: int
    total_entities_generated: int
    total_embeddings_generated: int
    processing_time_seconds: float
    start_time: datetime
    end_time: datetime

class ErrorInfo(BaseModel):
    """Information about any errors that occurred during processing."""
    error_type: str
    error_message: str
    table_name: Optional[str] = None
    field_name: Optional[str] = None
    row_index: Optional[int] = None

class ArtifactGenerationResponse(BaseModel):
    """Response model for artifact generation operations.
    
    This model provides comprehensive information about the artifact generation process,
    including generated files, processing statistics, and any errors that occurred.
    """
    
    # Core response information
    status: str = "success"  # "success", "partial_success", "error"
    message: str = "Artifact generation completed successfully"
    
    # Generated artifacts
    generated_artifacts: List[GeneratedArtifact] = Field(default_factory=list)
    
    # Processing statistics
    processing_stats: Optional[ProcessingStats] = None
    
    # Error information
    errors: List[ErrorInfo] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # Configuration summary
    source_name: str
    table_names: List[str] = Field(default_factory=list)
    
    # Artifact paths (for convenience)
    schema_path: Optional[str] = None
    entity_fields_schema_path: Optional[str] = None
    semantic_fields_schema_path: Optional[str] = None
    processed_data_path: Optional[str] = None
    canonical_entities_path: Optional[str] = None
    canonical_entity_embeddings_path: Optional[str] = None
    semantic_texts_path: Optional[str] = None
    data_loader_script_path: Optional[str] = None
    
    # GCP upload information (if applicable)
    gcp_upload_info: Optional[Dict[str, Any]] = None
    
    # Metadata
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            Path: str,
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary for serialization."""
        return {
            'status': self.status,
            'message': self.message,
            'generated_artifacts': [artifact.dict() for artifact in self.generated_artifacts],
            'processing_stats': self.processing_stats.dict() if self.processing_stats else None,
            'errors': [error.dict() for error in self.errors],
            'warnings': self.warnings,
            'source_name': self.source_name,
            'table_names': self.table_names,
            'schema_path': self.schema_path,
            'entity_fields_schema_path': self.entity_fields_schema_path,
            'semantic_fields_schema_path': self.semantic_fields_schema_path,
            'processed_data_path': self.processed_data_path,
            'canonical_entities_path': self.canonical_entities_path,
            'canonical_entity_embeddings_path': self.canonical_entity_embeddings_path,
            'semantic_texts_path': self.semantic_texts_path,
            'data_loader_script_path': self.data_loader_script_path,
            'gcp_upload_info': self.gcp_upload_info,
            'request_id': self.request_id,
            'timestamp': self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArtifactGenerationResponse':
        """Create a response from a dictionary."""
        # Convert nested objects
        generated_artifacts = [GeneratedArtifact(**artifact) for artifact in data.get('generated_artifacts', [])]
        processing_stats = ProcessingStats(**data['processing_stats']) if data.get('processing_stats') else None
        errors = [ErrorInfo(**error) for error in data.get('errors', [])]
        
        return cls(
            status=data.get('status', 'success'),
            message=data.get('message', 'Artifact generation completed successfully'),
            generated_artifacts=generated_artifacts,
            processing_stats=processing_stats,
            errors=errors,
            warnings=data.get('warnings', []),
            source_name=data['source_name'],
            table_names=data.get('table_names', []),
            schema_path=data.get('schema_path'),
            entity_fields_schema_path=data.get('entity_fields_schema_path'),
            semantic_fields_schema_path=data.get('semantic_fields_schema_path'),
            processed_data_path=data.get('processed_data_path'),
            canonical_entities_path=data.get('canonical_entities_path'),
            canonical_entity_embeddings_path=data.get('canonical_entity_embeddings_path'),
            semantic_texts_path=data.get('semantic_texts_path'),
            data_loader_script_path=data.get('data_loader_script_path'),
            gcp_upload_info=data.get('gcp_upload_info'),
            request_id=data.get('request_id'),
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.now(),
        )
    
    def add_artifact(self, artifact_type: str, file_path: str, table_name: Optional[str] = None, 
                    source_name: Optional[str] = None, file_size_bytes: Optional[int] = None):
        """Add a generated artifact to the response."""
        artifact = GeneratedArtifact(
            artifact_type=artifact_type,
            file_path=str(file_path),
            file_size_bytes=file_size_bytes,
            table_name=table_name,
            source_name=source_name
        )
        self.generated_artifacts.append(artifact)
    
    def add_error(self, error_type: str, error_message: str, table_name: Optional[str] = None,
                 field_name: Optional[str] = None, row_index: Optional[int] = None):
        """Add an error to the response."""
        error = ErrorInfo(
            error_type=error_type,
            error_message=error_message,
            table_name=table_name,
            field_name=field_name,
            row_index=row_index
        )
        self.errors.append(error)
        if self.status == "success":
            self.status = "partial_success"
    
    def add_warning(self, warning_message: str):
        """Add a warning to the response."""
        self.warnings.append(warning_message)
    
    def set_processing_stats(self, total_tables: int, total_rows: int, total_entities: int,
                           total_embeddings: int, processing_time: float, start_time: datetime, end_time: datetime):
        """Set processing statistics."""
        self.processing_stats = ProcessingStats(
            total_tables_processed=total_tables,
            total_rows_processed=total_rows,
            total_entities_generated=total_entities,
            total_embeddings_generated=total_embeddings,
            processing_time_seconds=processing_time,
            start_time=start_time,
            end_time=end_time
        ) 