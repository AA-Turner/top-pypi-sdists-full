from pathlib import Path
from typing import Optional, List, Dict, Union, Any
import pandas as pd
from pydantic import BaseModel, Field
import warnings
import types

class EntityField(BaseModel):
    """Configuration for a field to be canonicalized."""
    table_name: str
    field_name: str

class SemanticField(BaseModel):
    """Configuration for a field to be extracted as semantic text."""
    table_name: str
    field_name: str

class SemanticTextTitleField(BaseModel):
    """Configuration for specifying which field to use as the title for semantic text files."""
    table_name: str
    field_name: str

class CommaSeparatedField(BaseModel):
    """Configuration for a field that should be split on commas."""
    table_name: str
    field_name: str



class InputConfig(BaseModel):
    source_name: str = "data"
    table_name: Optional[str] = None
    recursive: bool = False
    file_pattern: Union[str, List[str]] = ["*.csv", "*.json"]
    table_name_from_file: bool = True
    num_rows: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_name": "my_data",
                "table_name": "custom_name",
                "recursive": True,
                "file_pattern": ["*.csv", "*.json"],
                "table_name_from_file": False,
                "num_rows": 1000
            }
        }

class ProcessingConfig(BaseModel):
    normalize_table_names: bool = True
    normalize_field_names: bool = True
    use_other_fields_as_metadata: bool = True

class FieldMappingConfig(BaseModel):
    entity_fields: Optional[List[EntityField]] = Field(default_factory=list)
    semantic_fields: Optional[List[SemanticField]] = Field(default_factory=list)
    semantic_text_title_fields: Optional[List[SemanticTextTitleField]] = Field(default_factory=list)
    comma_separated_fields: Optional[List[CommaSeparatedField]] = Field(default_factory=list)

class ArtifactGenerationConfig(BaseModel):
    generate_canonical_entities: bool = True
    generate_schemas: bool = True
    generate_embeddings: bool = True
    generate_semantic_texts: bool = True
    save_processed_data: bool = True
    database_type: str = "mariadb"
    upload_artifacts_to_gcs: bool = False


class ArtifactGenerationRequest(BaseModel):
    """Configuration for generating canonicalization artifacts.
    
    Focuses on WHAT to generate rather than WHERE to store it.
    Storage configuration is handled by CanonMapArtifactsConfig.
    If 'upload_artifacts_to_gcs' is True, generated artifacts will be uploaded to GCS according to the sync strategy in the config.
    
    Table Naming Behavior:
        The table naming depends on the input type and configuration:
        
        1. Single File Input:
           - If table_name is provided: Uses the provided name
           - If table_name is None: Uses filename without extension
           
        2. Directory Input (Multiple Files):
           - If table_name is provided AND table_name_from_file=False:
             * Single file found: Uses the provided table_name
             * Multiple files found: Uses table_name as prefix (e.g., "custom_1", "custom_2")
           - If table_name is provided AND table_name_from_file=True:
             * Ignores table_name, uses file-based names (with warning)
           - If table_name is None AND table_name_from_file=False:
             * Single file found: Uses source_name
             * Multiple files found: Uses "source_name_table_1", "source_name_table_2", etc.
           - If table_name is None AND table_name_from_file=True (default):
             * Uses file-based names (e.g., "main", "subdir1_file1")
    
    Examples:
        # Single file pattern
        request = ArtifactGenerationRequest(
            input_path="/path/to/data",
            file_pattern="*.csv"
        )
        
        # Multiple file patterns
        request = ArtifactGenerationRequest(
            input_path="/path/to/data",
            file_pattern=["*.csv", "*.tsv", "*.xlsx"]
        )
        
        # With recursive search (handles naming conflicts automatically)
        request = ArtifactGenerationRequest(
            input_path="/path/to/data",
            file_pattern=["*.csv", "*.json"],
            recursive=True
        )
        
        # Custom table naming for directory input
        request = ArtifactGenerationRequest(
            input_path="/path/to/data",
            table_name="my_data",
            table_name_from_file=False,
            recursive=True
        )
        
        # Generic naming using source_name
        request = ArtifactGenerationRequest(
            input_path="/path/to/data",
            source_name="customer_data",
            table_name=None,
            table_name_from_file=False,
            recursive=True
        )
        # Results in: "customer_data_table_1", "customer_data_table_2", etc.
        
    Note:
        When recursive=True, table names are derived from the relative path to avoid conflicts.
        For example, "subdir/file.csv" becomes "subdir_file" as the table name.
        If conflicts still occur, incremental counters are appended (e.g., "table_1", "table_2").
        
    Deprecation Notice:
        The following parameters are deprecated and will be removed in future releases.
        Use the corresponding nested configs instead:
        - table_name → input_config.table_name
        - recursive → input_config.recursive  
        - file_pattern → input_config.file_pattern
        - table_name_from_file → input_config.table_name_from_file
        - num_rows → input_config.num_rows
        - normalize_table_names → processing_config.normalize_table_names
        - normalize_field_names → processing_config.normalize_field_names
        - use_other_fields_as_metadata → processing_config.use_other_fields_as_metadata
        - entity_fields → field_mapping_config.entity_fields
        - semantic_fields → field_mapping_config.semantic_fields
        - semantic_text_title_fields → field_mapping_config.semantic_text_title_fields
        - comma_separated_fields → field_mapping_config.comma_separated_fields
        - generate_canonical_entities → artifact_generation_config.generate_canonical_entities
        - generate_schemas → artifact_generation_config.generate_schemas
        - generate_embeddings → artifact_generation_config.generate_embeddings
        - generate_semantic_texts → artifact_generation_config.generate_semantic_texts
        - save_processed_data → artifact_generation_config.save_processed_data
        - database_type → artifact_generation_config.database_type
        - upload_artifacts_to_gcs → artifact_generation_config.upload_artifacts_to_gcs
    """
    
    input_path: str  # Restrict to str for FastAPI compatibility

    input_config: InputConfig = InputConfig()
    processing_config: ProcessingConfig = ProcessingConfig()
    field_mapping_config: FieldMappingConfig = FieldMappingConfig()
    artifact_generation_config: ArtifactGenerationConfig = ArtifactGenerationConfig()
    
    # Legacy parameters - DEPRECATED
    source_name: Optional[str] = Field(
        default="data",
        description="DEPRECATED: Use input_config.source_name instead. Will be removed in future releases."
    )
    table_name: Optional[str] = Field(
        default=None,
        description="DEPRECATED: Use input_config.table_name instead. Will be removed in future releases."
    )
    normalize_table_names: bool = Field(
        default=True,
        description="DEPRECATED: Use processing_config.normalize_table_names instead. Will be removed in future releases."
    )
    recursive: bool = Field(
        default=False,
        description="DEPRECATED: Use input_config.recursive instead. Will be removed in future releases."
    )
    file_pattern: Union[str, List[str]] = Field(
        default=["*.csv", "*.json"],
        description="DEPRECATED: Use input_config.file_pattern instead. Will be removed in future releases."
    )
    table_name_from_file: bool = Field(
        default=True,
        description="DEPRECATED: Use input_config.table_name_from_file instead. Will be removed in future releases."
    )
    entity_fields: Optional[List[EntityField]] = Field(
        default_factory=list,
        description="DEPRECATED: Use field_mapping_config.entity_fields instead. Will be removed in future releases."
    )
    semantic_fields: Optional[List[SemanticField]] = Field(
        default_factory=list,
        description="DEPRECATED: Use field_mapping_config.semantic_fields instead. Will be removed in future releases."
    )
    semantic_text_title_fields: Optional[List[SemanticTextTitleField]] = Field(
        default_factory=list,
        description="DEPRECATED: Use field_mapping_config.semantic_text_title_fields instead. Will be removed in future releases."
    )
    comma_separated_fields: Optional[List[CommaSeparatedField]] = Field(
        default_factory=list,
        description="DEPRECATED: Use field_mapping_config.comma_separated_fields instead. Will be removed in future releases."
    )
    use_other_fields_as_metadata: bool = Field(
        default=True,
        description="DEPRECATED: Use processing_config.use_other_fields_as_metadata instead. Will be removed in future releases."
    )
    num_rows: Optional[int] = Field(
        default=None,
        description="DEPRECATED: Use input_config.num_rows instead. Will be removed in future releases."
    )
    generate_canonical_entities: bool = Field(
        default=True,
        description="DEPRECATED: Use artifact_generation_config.generate_canonical_entities instead. Will be removed in future releases."
    )
    generate_schemas: bool = Field(
        default=True,
        description="DEPRECATED: Use artifact_generation_config.generate_schemas instead. Will be removed in future releases."
    )
    generate_embeddings: bool = Field(
        default=True,
        description="DEPRECATED: Use artifact_generation_config.generate_embeddings instead. Will be removed in future releases."
    )
    generate_semantic_texts: bool = Field(
        default=True,
        description="DEPRECATED: Use artifact_generation_config.generate_semantic_texts instead. Will be removed in future releases."
    )
    save_processed_data: bool = Field(
        default=True,
        description="DEPRECATED: Use artifact_generation_config.save_processed_data instead. Will be removed in future releases."
    )
    database_type: str = Field(
        default="mariadb",
        description="DEPRECATED: Use artifact_generation_config.database_type instead. Will be removed in future releases."
    )
    normalize_field_names: bool = Field(
        default=True,
        description="DEPRECATED: Use processing_config.normalize_field_names instead. Will be removed in future releases."
    )
    upload_artifacts_to_gcs: bool = Field(
        default=False,
        description="DEPRECATED: Use artifact_generation_config.upload_artifacts_to_gcs instead. Will be removed in future releases."
    )

    class Config:
        arbitrary_types_allowed = True  # Allow pandas DataFrame and Path objects

    def __init__(self, **data):
        super().__init__(**data)
        # Only warn if any legacy/deprecated fields are actually passed in
        legacy_fields = [
            'table_name', 'normalize_table_names', 'recursive', 'file_pattern',
            'table_name_from_file', 'entity_fields', 'semantic_fields',
            'semantic_text_title_fields', 'comma_separated_fields',
            'use_other_fields_as_metadata', 'num_rows', 'generate_canonical_entities',
            'generate_schemas', 'generate_embeddings', 'generate_semantic_texts',
            'save_processed_data', 'database_type', 'normalize_field_names',
            'upload_artifacts_to_gcs'
        ]
        # Only warn if user passed in any of these fields (i.e. present in data)
        if any(field in data for field in legacy_fields):
            self._warn_deprecated_params()

    def _warn_deprecated_params(self):
        """Warn about deprecated parameters that are being used."""
        deprecated_params = [
            'table_name', 'normalize_table_names', 'recursive', 'file_pattern',
            'table_name_from_file', 'entity_fields', 'semantic_fields',
            'semantic_text_title_fields', 'comma_separated_fields',
            'use_other_fields_as_metadata', 'num_rows', 'generate_canonical_entities',
            'generate_schemas', 'generate_embeddings', 'generate_semantic_texts',
            'save_processed_data', 'database_type', 'normalize_field_names',
            'upload_artifacts_to_gcs'
        ]
        used_deprecated = []
        default_values = {
            'table_name': None, 'normalize_table_names': True, 'recursive': False,
            'file_pattern': ["*.csv", "*.json"], 'table_name_from_file': True,
            'entity_fields': [], 'semantic_fields': [], 'semantic_text_title_fields': [],
            'comma_separated_fields': [], 'use_other_fields_as_metadata': True,
            'num_rows': None, 'generate_canonical_entities': True, 'generate_schemas': True,
            'generate_embeddings': True, 'generate_semantic_texts': True,
            'save_processed_data': True, 'database_type': "mariadb",
            'normalize_field_names': True, 'upload_artifacts_to_gcs': False
        }
        for param in deprecated_params:
            value = getattr(self, param, None)
            default = default_values.get(param)
            if param in ['table_name', 'num_rows']:
                if value is not None:
                    used_deprecated.append(param)
            elif param in ['entity_fields', 'semantic_fields', 'semantic_text_title_fields', 'comma_separated_fields']:
                if isinstance(value, list) and len(value) > 0:
                    used_deprecated.append(param)
            else:
                if value != default:
                    used_deprecated.append(param)
        if used_deprecated:
            warnings.warn(
                f"Deprecated parameters detected: {', '.join(used_deprecated)}. "
                "These will be removed in future releases. Use the corresponding nested configs instead. "
                "See the class docstring for migration guide.",
                DeprecationWarning,
                stacklevel=2
            )

    @classmethod
    def from_legacy_params(cls, **kwargs) -> 'ArtifactGenerationRequest':
        """
        Create a request from legacy parameters, automatically migrating to new config structure.
        """
        input_path = kwargs.pop('input_path', None)
        if input_path is None:
            raise ValueError("input_path is required")
        # Directly map legacy params to nested configs
        input_fields = ['source_name', 'table_name', 'recursive', 'file_pattern', 'table_name_from_file', 'num_rows']
        processing_fields = ['normalize_table_names', 'normalize_field_names', 'use_other_fields_as_metadata']
        field_mapping_fields = ['entity_fields', 'semantic_fields', 'semantic_text_title_fields', 'comma_separated_fields']
        artifact_fields = ['generate_canonical_entities', 'generate_schemas', 'generate_embeddings', 'generate_semantic_texts',
                           'save_processed_data', 'database_type', 'upload_artifacts_to_gcs']
        input_config_kwargs = {k: kwargs.pop(k) for k in input_fields if k in kwargs}
        processing_config_kwargs = {k: kwargs.pop(k) for k in processing_fields if k in kwargs}
        field_mapping_config_kwargs = {k: kwargs.pop(k) for k in field_mapping_fields if k in kwargs}
        artifact_generation_config_kwargs = {k: kwargs.pop(k) for k in artifact_fields if k in kwargs}
        input_config = InputConfig(**input_config_kwargs) if input_config_kwargs else InputConfig()
        processing_config = ProcessingConfig(**processing_config_kwargs) if processing_config_kwargs else ProcessingConfig()
        field_mapping_config = FieldMappingConfig(**field_mapping_config_kwargs) if field_mapping_config_kwargs else FieldMappingConfig()
        artifact_generation_config = ArtifactGenerationConfig(**artifact_generation_config_kwargs) if artifact_generation_config_kwargs else ArtifactGenerationConfig()
        if kwargs:
            warnings.warn(
                f"Unknown parameters detected: {', '.join(kwargs.keys())}. "
                "These will be ignored.",
                UserWarning,
                stacklevel=2
            )
        return cls(
            input_path=input_path,
            input_config=input_config,
            processing_config=processing_config,
            field_mapping_config=field_mapping_config,
            artifact_generation_config=artifact_generation_config,
            **kwargs
        )