# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..s3_data_source_config_param import S3DataSourceConfigParam
from ..slack_data_source_config_param import SlackDataSourceConfigParam
from ..local_chunks_source_config_param import LocalChunksSourceConfigParam
from ..mongodb_data_source_config_param import MongoDBDataSourceConfigParam
from ..s3_data_source_auth_config_param import S3DataSourceAuthConfigParam
from ..snowflake_data_source_config_param import SnowflakeDataSourceConfigParam
from ..confluence_data_source_config_param import ConfluenceDataSourceConfigParam
from ..databricks_data_source_config_param import DatabricksDataSourceConfigParam
from ..slack_data_source_auth_config_param import SlackDataSourceAuthConfigParam
from ..share_point_data_source_config_param import SharePointDataSourceConfigParam
from ..token_chunking_strategy_config_param import TokenChunkingStrategyConfigParam
from ..custom_chunking_strategy_config_param import CustomChunkingStrategyConfigParam
from ..google_drive_data_source_config_param import GoogleDriveDataSourceConfigParam
from ..mongodb_data_source_auth_config_param import MongoDBDataSourceAuthConfigParam
from ..shared_params.tagging_information_all import TaggingInformationAll
from ..sql_database_data_source_config_param import SqlDatabaseDataSourceConfigParam
from ..snowflake_data_source_auth_config_param import SnowflakeDataSourceAuthConfigParam
from ..character_chunking_strategy_config_param import CharacterChunkingStrategyConfigParam
from ..confluence_data_source_auth_config_param import ConfluenceDataSourceAuthConfigParam
from ..databricks_data_source_auth_config_param import DatabricksDataSourceAuthConfigParam
from ..share_point_data_source_auth_config_param import SharePointDataSourceAuthConfigParam
from ..share_point_page_data_source_config_param import SharePointPageDataSourceConfigParam
from ..google_drive_data_source_auth_config_param import GoogleDriveDataSourceAuthConfigParam
from ..sql_database_data_source_auth_config_param import SqlDatabaseDataSourceAuthConfigParam
from ..azure_blob_storage_data_source_config_param import AzureBlobStorageDataSourceConfigParam
from ..google_cloud_storage_data_source_config_param import GoogleCloudStorageDataSourceConfigParam
from ..share_point_page_data_source_auth_config_param import SharePointPageDataSourceAuthConfigParam
from ..azure_blob_storage_data_source_auth_config_param import AzureBlobStorageDataSourceAuthConfigParam
from ..google_cloud_storage_data_source_auth_config_param import GoogleCloudStorageDataSourceAuthConfigParam

__all__ = [
    "UploadCreateParams",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequest",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigPreChunkedStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigEnhancedChunkingStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationPerFile",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequest",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationPerFile",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequest",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigPreChunkedStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigEnhancedChunkingStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationPerFile",
]


class CreateKnowledgeBaseV2UploadFromDataSourceRequest(TypedDict, total=False):
    data_source_config: Required[CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig]
    """Configuration for the data source which describes where to find the data."""

    chunking_strategy_config: CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig
    """Configuration for the chunking strategy which describes how to chunk the data."""

    data_source_auth_config: CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig
    """
    Configuration for the data source which describes how to authenticate to the
    data source.
    """

    force_reupload: bool
    """Force reingest, regardless the change of the source file."""

    tagging_information: CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation
    """A dictionary of tags to apply to all artifacts added from the data source."""


CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig: TypeAlias = Union[
    S3DataSourceConfigParam,
    SharePointDataSourceConfigParam,
    SharePointPageDataSourceConfigParam,
    GoogleDriveDataSourceConfigParam,
    AzureBlobStorageDataSourceConfigParam,
    GoogleCloudStorageDataSourceConfigParam,
    ConfluenceDataSourceConfigParam,
    SlackDataSourceConfigParam,
    SnowflakeDataSourceConfigParam,
    DatabricksDataSourceConfigParam,
    SqlDatabaseDataSourceConfigParam,
    MongoDBDataSourceConfigParam,
]


class CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigPreChunkedStrategyConfig(
    TypedDict, total=False
):
    """Only compliant with the .chunks file type"""

    strategy: Required[Literal["pre_chunked"]]


class CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigEnhancedChunkingStrategyConfig(
    TypedDict, total=False
):
    """Enhanced document parsing and chunking"""

    advanced_options: Dict[str, object]
    """Advanced options for enhanced parsing"""

    chunk_mode: Literal["variable", "section", "page", "page_sections", "block"]
    """Enhanced internal chunking method"""

    experimental_options: Dict[str, object]
    """Experimental options for enhanced parsing"""

    options: Dict[str, object]
    """Options for enhanced parsing"""

    strategy: Literal["enhanced"]

    use_async_parsing: bool


CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig: TypeAlias = Union[
    CharacterChunkingStrategyConfigParam,
    TokenChunkingStrategyConfigParam,
    CustomChunkingStrategyConfigParam,
    CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigPreChunkedStrategyConfig,
    CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigEnhancedChunkingStrategyConfig,
]

CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig: TypeAlias = Union[
    SharePointDataSourceAuthConfigParam,
    SharePointPageDataSourceAuthConfigParam,
    AzureBlobStorageDataSourceAuthConfigParam,
    GoogleCloudStorageDataSourceAuthConfigParam,
    GoogleDriveDataSourceAuthConfigParam,
    S3DataSourceAuthConfigParam,
    ConfluenceDataSourceAuthConfigParam,
    SlackDataSourceAuthConfigParam,
    SnowflakeDataSourceAuthConfigParam,
    DatabricksDataSourceAuthConfigParam,
    SqlDatabaseDataSourceAuthConfigParam,
    MongoDBDataSourceAuthConfigParam,
]


class CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationPerFile(
    TypedDict, total=False
):
    tags_to_apply: Dict[str, Optional[Dict[str, object]]]

    type: Literal["per_file"]


CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationPerFile, TaggingInformationAll
]


class CreateKnowledgeBaseV2UploadFromLocalChunksRequest(TypedDict, total=False):
    data_source_config: Required[LocalChunksSourceConfigParam]
    """Configuration for the data source which describes where to find the data."""

    chunks: Iterable[CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk]
    """List of chunks."""

    force_reupload: bool
    """Force reingest, regardless the change of the source file."""

    tagging_information: CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation
    """A dictionary of tags to apply to all artifacts added from the data source."""


class CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk(TypedDict, total=False):
    chunk_position: Required[int]
    """Position of the chunk in the artifact."""

    text: Required[str]
    """Associated text of the chunk."""

    metadata: Dict[str, object]
    """Additional metadata associated with the chunk."""


class CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationPerFile(
    TypedDict, total=False
):
    tags_to_apply: Dict[str, Optional[Dict[str, object]]]

    type: Literal["per_file"]


CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationPerFile, TaggingInformationAll
]


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequest(TypedDict, total=False):
    chunking_strategy_config: Required[CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig]
    """Configuration for the chunking strategy which describes how to chunk the data."""

    data_source_id: Required[str]
    """Id of the data source to fetch."""

    force_reupload: bool
    """Force reingest, regardless the change of the source file."""

    tagging_information: CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation
    """A dictionary of tags to apply to all artifacts added from the data source."""


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigPreChunkedStrategyConfig(
    TypedDict, total=False
):
    """Only compliant with the .chunks file type"""

    strategy: Required[Literal["pre_chunked"]]


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigEnhancedChunkingStrategyConfig(
    TypedDict, total=False
):
    """Enhanced document parsing and chunking"""

    advanced_options: Dict[str, object]
    """Advanced options for enhanced parsing"""

    chunk_mode: Literal["variable", "section", "page", "page_sections", "block"]
    """Enhanced internal chunking method"""

    experimental_options: Dict[str, object]
    """Experimental options for enhanced parsing"""

    options: Dict[str, object]
    """Options for enhanced parsing"""

    strategy: Literal["enhanced"]

    use_async_parsing: bool


CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig: TypeAlias = Union[
    CharacterChunkingStrategyConfigParam,
    TokenChunkingStrategyConfigParam,
    CustomChunkingStrategyConfigParam,
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigPreChunkedStrategyConfig,
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigEnhancedChunkingStrategyConfig,
]


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationPerFile(
    TypedDict, total=False
):
    tags_to_apply: Dict[str, Optional[Dict[str, object]]]

    type: Literal["per_file"]


CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationPerFile, TaggingInformationAll
]

UploadCreateParams: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromDataSourceRequest,
    CreateKnowledgeBaseV2UploadFromLocalChunksRequest,
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequest,
]
