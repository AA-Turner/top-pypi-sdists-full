"""
Intapp DealCloud SDK - HTTPX-based DealCloud API client.

New for DealCloud 2610 release: A full rewrite of the dealcloud-sdk, built on the new intapp_rest_client (HTTPX) instead of requests.
Benefit from modern async support and improved retry handling, this sdk is a near drop-in replacement for the original sdk.
Make sure to see the migration section of the documentation.
"""

from .dealcloud import DealCloud

# Schema models
from .models.schema import Object, Field, ChoiceValue, User, Schema, ObjectWithFields
from .models.data import Rows, EntryIdCache

# Configuration models
from .models.factory_models import (
    DealCloudConfig,
    DealCloudFactoryArgs,
    QuerySettings,
    ConcurrencyLimits,
    ResponseRetrySettings,
)

# Data operation models
from intapp_rest_client.models import ErrorHandling  # Moved to intapp-rest-client
from .data.models import (
    BatchResult,
    RowsWriteResult,
    ModifiedEntry,
    DeltaSyncResult,
    ReferenceFormat,
    ReferenceCache,
)

# File export models
from .files.dealcloud_files import ExportResult
from .storage import (
    FsspecStreamingStorage,
    LocalStorage,
    StorageBackend,
    StreamingStorageBackend,
)

# Exceptions
from .utils.process_response_errors import (
    DealCloudApiError,
    DealCloudValidationError,
    DealCloudRateLimitError,
    DealCloudAuthError,
    finalize_list_response,
    resolve_raise_on_row_errors,
    split_row_results,
    map_row_errors_to_indices,
    format_row_error_message,
)

# Opt-in error enrichment (not used by standard write paths)
from .utils.error_enrichment import (
    FieldLookup,
    build_field_lookup,
    enrich_row_errors,
    field_lookup_from_fields,
    format_error_message_english,
    format_error_with_metadata,
    format_row_error_message_english,
    format_row_error_with_metadata,
    iter_row_error_items,
)

# Schema caching
from .utils.schema_cache import SchemaCache, get_schema_cache

# Field type utilities
from .constants.field_types import (
    FIELD_TYPE_NAMES,
    FIELD_TYPE_IDS,
    get_field_type_name,
    get_field_type_id,
    TEXT, CHOICE, NUMBER, DATE, REFERENCE, BOOLEAN, USER,
    BINARY, ENTRY_LIST_ID, COUNTER, IMAGE, DATA_SOURCE, CURRENCY,
)

# Data profiling utilities
from .utils.profiling import (
    DataType,
    PROFILE_COLUMNS,
    estimate_field_type,
    detect_choice_field,
    analyze_field_values,
    most_common,
    profile_series,
    profile_dataframe,
    profile_files,
)

# File utilities
from .utils.file_utils import (
    detect_encoding,
    is_supported_file,
    should_skip_file,
    read_csv,
    read_excel,
    read_file,
    get_data_files,
    SUPPORTED_CSV_EXTENSIONS,
    SUPPORTED_EXCEL_EXTENSIONS,
    ALL_SUPPORTED_EXTENSIONS,
)

# Excel export utilities
from .utils.excel_utils import (
    sanitize_sheet_name,
    sanitize_cell_value,
    sanitize_dataframe,
    export_to_excel,
    export_with_formatting,
    create_data_validation_dropdown,
    read_excel_sheets,
    append_to_excel,
    ILLEGAL_CHARACTERS_RE,
    INVALID_SHEET_NAME_CHARS,
)

# API-specific classes (for advanced usage)
from .base.dealcloud_base import DealCloudBase
from .schema.dealcloud_schema import DealCloudSchema
from .reports.dealcloud_reports import DealCloudReports
from .data.dealcloud_data import DealCloudData
from .cells.dealcloud_cells import DealCloudCells
from .history.dealcloud_history import DealCloudHistory
from .history import DateTimeBehavior
from .files.dealcloud_files import DealCloudFiles
from .usermanagement.dealcloud_usermanagement import DealCloudUserManagement
from .publications.dealcloud_publications import DealCloudPublications
from .backups.dealcloud_backups import DealCloudBackups
from .relationshipintelligence.dealcloud_ri import DealCloudRelationshipIntelligence
from .merge.dealcloud_merge import DealCloudMerge
from ._version import __version__, SDK_VERSION, PACKAGE_NAME

__all__ = [
    # Main client
    "DealCloud",
    
    # Version info
    "__version__",
    "SDK_VERSION",
    "PACKAGE_NAME",
    
    # Schema models
    "Object",
    "Field", 
    "ChoiceValue",
    "User",
    "Schema",
    "ObjectWithFields",
    
    # Data models
    "Rows",
    "EntryIdCache",
    "ErrorHandling",
    "BatchResult",
    "RowsWriteResult",
    "ModifiedEntry",
    "DeltaSyncResult",
    "ReferenceFormat",
    "ReferenceCache",
    
    # File export models
    "StorageBackend",
    "LocalStorage",
    "StreamingStorageBackend",
    "FsspecStreamingStorage",
    "ExportResult",
    
    # Configuration models
    "DealCloudConfig",
    "DealCloudFactoryArgs",
    "QuerySettings",
    "ConcurrencyLimits",
    "ResponseRetrySettings",
    
    # Schema caching
    "SchemaCache",
    "get_schema_cache",
    
    # Field type constants and utilities
    "FIELD_TYPE_NAMES",
    "FIELD_TYPE_IDS",
    "get_field_type_name",
    "get_field_type_id",
    "TEXT", "CHOICE", "NUMBER", "DATE", "REFERENCE", "BOOLEAN", "USER",
    "BINARY", "ENTRY_LIST_ID", "COUNTER", "IMAGE", "DATA_SOURCE", "CURRENCY",
    
    # Data profiling utilities
    "DataType",
    "PROFILE_COLUMNS",
    "estimate_field_type",
    "detect_choice_field",
    "analyze_field_values",
    "most_common",
    "profile_series",
    "profile_dataframe",
    "profile_files",
    
    # File utilities
    "detect_encoding",
    "is_supported_file",
    "should_skip_file",
    "read_csv",
    "read_excel",
    "read_file",
    "get_data_files",
    "SUPPORTED_CSV_EXTENSIONS",
    "SUPPORTED_EXCEL_EXTENSIONS",
    "ALL_SUPPORTED_EXTENSIONS",
    
    # Excel export utilities
    "sanitize_sheet_name",
    "sanitize_cell_value",
    "sanitize_dataframe",
    "export_to_excel",
    "export_with_formatting",
    "create_data_validation_dropdown",
    "read_excel_sheets",
    "append_to_excel",
    "ILLEGAL_CHARACTERS_RE",
    "INVALID_SHEET_NAME_CHARS",
    
    # Exceptions
    "DealCloudApiError",
    "DealCloudValidationError",
    "DealCloudRateLimitError",
    "DealCloudAuthError",
    "finalize_list_response",
    "resolve_raise_on_row_errors",
    "split_row_results",
    "map_row_errors_to_indices",
    "format_row_error_message",
    "FieldLookup",
    "build_field_lookup",
    "field_lookup_from_fields",
    "enrich_row_errors",
    "iter_row_error_items",
    "format_error_with_metadata",
    "format_error_message_english",
    "format_row_error_with_metadata",
    "format_row_error_message_english",
    "DealCloudBase",
    "DealCloudSchema",
    "DealCloudReports",
    "DealCloudData",
    "DealCloudCells",
    "DealCloudHistory",
    "DateTimeBehavior",
    "DealCloudFiles",
    "DealCloudUserManagement",
    "DealCloudPublications",
    "DealCloudBackups",
    "DealCloudRelationshipIntelligence",
    "DealCloudMerge",
]
