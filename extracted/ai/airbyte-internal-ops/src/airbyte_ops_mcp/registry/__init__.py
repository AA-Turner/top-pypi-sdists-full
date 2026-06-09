# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry operations for Airbyte connectors.

This package provides functionality for reading, listing, publishing, compiling,
and validating connector registry artifacts.
"""

from __future__ import annotations

from airbyte_ops_mcp.registry._constants import (
    DEFAULT_METADATA_SERVICE_BUCKET_NAME,
    DEV_METADATA_SERVICE_BUCKET_NAME,
    LATEST_GCS_FOLDER_NAME,
    METADATA_FILE_NAME,
    METADATA_FOLDER,
    PROD_METADATA_SERVICE_BUCKET_NAME,
    RELEASE_CANDIDATE_GCS_FOLDER_NAME,
    SONAR_DEV_BUCKET_NAME,
    SONAR_PROD_BUCKET_NAME,
)
from airbyte_ops_mcp.registry._enums import (
    ConnectorLanguage,
    ConnectorType,
    SupportLevel,
)
from airbyte_ops_mcp.registry.audit import (
    AuditResult,
    UnpublishedConnector,
    find_unpublished_connectors,
)
from airbyte_ops_mcp.registry.compile import (
    CompileResult,
    PurgeLatestResult,
    compile_registry,
    purge_latest_dirs,
)
from airbyte_ops_mcp.registry.generate import (
    GenerateResult,
    generate_version_artifacts,
)
from airbyte_ops_mcp.registry.models import (
    ConnectorListResult,
    ConnectorMetadata,
    MetadataPublishResult,
    RegistryEntryResult,
    VersionListResult,
)
from airbyte_ops_mcp.registry.operations import (
    get_registry_entry,
    get_registry_spec,
    list_connector_versions,
    list_registry_connectors,
    list_registry_connectors_filtered,
)
from airbyte_ops_mcp.registry.publish import (
    CONNECTOR_PATH_PREFIX,
    get_connector_metadata,
    get_gcs_publish_path,
    publish_connector_metadata,
)
from airbyte_ops_mcp.registry.publish_artifacts import (
    PublishArtifactsResult,
    publish_version_artifacts,
)
from airbyte_ops_mcp.registry.rebuild import (
    OutputMode,
    RebuildResult,
    rebuild_registry,
)
from airbyte_ops_mcp.registry.registry_store_base import (
    Registry,
    get_registry,
)
from airbyte_ops_mcp.registry.store import (
    REGISTRY_STORE_ENV_VAR,
    RegistryStore,
    StoreType,
    resolve_registry_store,
)
from airbyte_ops_mcp.registry.validate import (
    ValidateOptions,
    ValidationResult,
    validate_metadata,
)
from airbyte_ops_mcp.registry.yank import (
    YANK_FILE_NAME,
    YankResult,
    unyank_connector_version,
    yank_connector_version,
)

__all__ = [
    "CONNECTOR_PATH_PREFIX",
    "DEFAULT_METADATA_SERVICE_BUCKET_NAME",
    "DEV_METADATA_SERVICE_BUCKET_NAME",
    "LATEST_GCS_FOLDER_NAME",
    "METADATA_FILE_NAME",
    "METADATA_FOLDER",
    "PROD_METADATA_SERVICE_BUCKET_NAME",
    "REGISTRY_STORE_ENV_VAR",
    "RELEASE_CANDIDATE_GCS_FOLDER_NAME",
    "SONAR_DEV_BUCKET_NAME",
    "SONAR_PROD_BUCKET_NAME",
    "YANK_FILE_NAME",
    "AuditResult",
    "CompileResult",
    "ConnectorLanguage",
    "ConnectorListResult",
    "ConnectorMetadata",
    "ConnectorType",
    "GenerateResult",
    "MetadataPublishResult",
    "OutputMode",
    "PublishArtifactsResult",
    "PurgeLatestResult",
    "RebuildResult",
    "Registry",
    "RegistryEntryResult",
    "RegistryStore",
    "StoreType",
    "SupportLevel",
    "UnpublishedConnector",
    "ValidateOptions",
    "ValidationResult",
    "VersionListResult",
    "YankResult",
    "compile_registry",
    "find_unpublished_connectors",
    "generate_version_artifacts",
    "get_connector_metadata",
    "get_gcs_publish_path",
    "get_registry",
    "get_registry_entry",
    "get_registry_spec",
    "list_connector_versions",
    "list_registry_connectors",
    "list_registry_connectors_filtered",
    "publish_connector_metadata",
    "publish_version_artifacts",
    "purge_latest_dirs",
    "rebuild_registry",
    "resolve_registry_store",
    "unyank_connector_version",
    "validate_metadata",
    "yank_connector_version",
]
