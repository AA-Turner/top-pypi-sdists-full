# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..s3_data_source_config import S3DataSourceConfig
from ..local_file_source_config import LocalFileSourceConfig
from ..slack_data_source_config import SlackDataSourceConfig
from ..local_chunks_source_config import LocalChunksSourceConfig
from ..mongodb_data_source_config import MongoDBDataSourceConfig
from ..snowflake_data_source_config import SnowflakeDataSourceConfig
from ..confluence_data_source_config import ConfluenceDataSourceConfig
from ..databricks_data_source_config import DatabricksDataSourceConfig
from ..share_point_data_source_config import SharePointDataSourceConfig
from ..token_chunking_strategy_config import TokenChunkingStrategyConfig
from ..custom_chunking_strategy_config import CustomChunkingStrategyConfig
from ..google_drive_data_source_config import GoogleDriveDataSourceConfig
from ..sql_database_data_source_config import SqlDatabaseDataSourceConfig
from ..character_chunking_strategy_config import CharacterChunkingStrategyConfig
from ..share_point_page_data_source_config import SharePointPageDataSourceConfig
from ..azure_blob_storage_data_source_config import AzureBlobStorageDataSourceConfig
from ..google_cloud_storage_data_source_config import GoogleCloudStorageDataSourceConfig

__all__ = [
    "KnowledgeBaseUpload",
    "Artifact",
    "ArtifactChunksStatus",
    "ArtifactsStatus",
    "DataSourceConfig",
    "ChunkingStrategyConfig",
    "ChunkingStrategyConfigPreChunkedStrategyConfig",
    "ChunkingStrategyConfigEnhancedChunkingStrategyConfig",
]


class ArtifactChunksStatus(BaseModel):
    """Number of chunks pending, completed, and failed."""

    chunks_completed: int
    """Number of chunks uploaded successfully."""

    chunks_failed: int
    """Number of chunks that failed upload."""

    chunks_pending: int
    """Number of chunks awaiting upload."""


class Artifact(BaseModel):
    artifact_id: str
    """Unique identifier for the artifact."""

    artifact_name: str
    """Friendly name for the artifact."""

    artifact_uri: str
    """Location (e.g. URI) of the artifact in the data source."""

    chunks_status: ArtifactChunksStatus
    """Number of chunks pending, completed, and failed."""

    source: Literal[
        "S3",
        "Confluence",
        "SharePoint",
        "SharePointPage",
        "GoogleDrive",
        "GoogleCloudStorage",
        "AzureBlobStorage",
        "Slack",
        "Snowflake",
        "Databricks",
        "LocalFile",
        "LocalChunks",
    ]
    """Data source of the artifact."""

    status: str
    """Status of the artifact."""

    tags: Dict[str, object]
    """Tags associated with the artifact."""

    artifact_uri_public: Optional[str] = None
    """Public Location (e.g. URI) of the artifact in the data source."""

    status_reason: Optional[str] = None
    """Reason for the artifact's status."""

    updated_at: Optional[datetime] = None
    """Timestamp at which the artifact was last updated."""


class ArtifactsStatus(BaseModel):
    """
    Number of artifacts in each of the various states, such as completed and failed for this upload. This includes artifacts for this data source that are retried.
    """

    artifacts_chunking: int
    """Number of artifacts in the chunking state"""

    artifacts_completed: int
    """Number of artifacts uploaded successfully."""

    artifacts_embedding: int
    """Number of artifacts in the embedding state"""

    artifacts_failed: int
    """Number of artifacts that failed while being processed."""

    artifacts_pending: int
    """Previously: Number of artifacts awaiting upload.

    Note that this status will be deprecated soon and should show 0
    """

    artifacts_uploading: int
    """Number of artifacts with upload in progress."""


DataSourceConfig: TypeAlias = Annotated[
    Union[
        S3DataSourceConfig,
        SharePointDataSourceConfig,
        SharePointPageDataSourceConfig,
        GoogleDriveDataSourceConfig,
        AzureBlobStorageDataSourceConfig,
        GoogleCloudStorageDataSourceConfig,
        LocalChunksSourceConfig,
        LocalFileSourceConfig,
        ConfluenceDataSourceConfig,
        SlackDataSourceConfig,
        SnowflakeDataSourceConfig,
        DatabricksDataSourceConfig,
        SqlDatabaseDataSourceConfig,
        MongoDBDataSourceConfig,
    ],
    PropertyInfo(discriminator="source"),
]


class ChunkingStrategyConfigPreChunkedStrategyConfig(BaseModel):
    """Only compliant with the .chunks file type"""

    strategy: Literal["pre_chunked"]


class ChunkingStrategyConfigEnhancedChunkingStrategyConfig(BaseModel):
    """Enhanced document parsing and chunking"""

    advanced_options: Optional[Dict[str, object]] = None
    """Advanced options for enhanced parsing"""

    chunk_mode: Optional[Literal["variable", "section", "page", "page_sections", "block"]] = None
    """Enhanced internal chunking method"""

    experimental_options: Optional[Dict[str, object]] = None
    """Experimental options for enhanced parsing"""

    options: Optional[Dict[str, object]] = None
    """Options for enhanced parsing"""

    strategy: Optional[Literal["enhanced"]] = None

    use_async_parsing: Optional[bool] = None


ChunkingStrategyConfig: TypeAlias = Annotated[
    Union[
        CharacterChunkingStrategyConfig,
        TokenChunkingStrategyConfig,
        CustomChunkingStrategyConfig,
        ChunkingStrategyConfigPreChunkedStrategyConfig,
        ChunkingStrategyConfigEnhancedChunkingStrategyConfig,
    ],
    PropertyInfo(discriminator="strategy"),
]


class KnowledgeBaseUpload(BaseModel):
    artifacts: List[Artifact]
    """List of info for each artifacts associated with this upload.

    This includes artifacts for this data source that are retried.
    """

    artifacts_status: ArtifactsStatus
    """
    Number of artifacts in each of the various states, such as completed and failed
    for this upload. This includes artifacts for this data source that are retried.
    """

    created_at: str
    """The timestamp at which the upload job started."""

    data_source_config: DataSourceConfig
    """Configuration for downloading data from source."""

    status: Literal["Running", "Completed", "Failed", "Canceled"]
    """Sync status"""

    updated_at: str
    """The timestamp at which the upload job was last updated."""

    upload_id: str
    """Unique ID of the upload job."""

    chunking_strategy_config: Optional[ChunkingStrategyConfig] = None
    """Configuration for chunking the text content of each artifact."""

    created_by_schedule_id: Optional[str] = None
    """Id of the upload schedule that triggered this upload_id.

    Null if triggered manually.
    """

    status_reason: Optional[str] = None
    """Reason for the upload job's status."""
