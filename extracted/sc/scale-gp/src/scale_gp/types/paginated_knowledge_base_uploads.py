# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .s3_data_source_config import S3DataSourceConfig
from .local_file_source_config import LocalFileSourceConfig
from .slack_data_source_config import SlackDataSourceConfig
from .local_chunks_source_config import LocalChunksSourceConfig
from .mongodb_data_source_config import MongoDBDataSourceConfig
from .snowflake_data_source_config import SnowflakeDataSourceConfig
from .confluence_data_source_config import ConfluenceDataSourceConfig
from .databricks_data_source_config import DatabricksDataSourceConfig
from .share_point_data_source_config import SharePointDataSourceConfig
from .token_chunking_strategy_config import TokenChunkingStrategyConfig
from .custom_chunking_strategy_config import CustomChunkingStrategyConfig
from .google_drive_data_source_config import GoogleDriveDataSourceConfig
from .sql_database_data_source_config import SqlDatabaseDataSourceConfig
from .character_chunking_strategy_config import CharacterChunkingStrategyConfig
from .share_point_page_data_source_config import SharePointPageDataSourceConfig
from .azure_blob_storage_data_source_config import AzureBlobStorageDataSourceConfig
from .google_cloud_storage_data_source_config import GoogleCloudStorageDataSourceConfig

__all__ = [
    "PaginatedKnowledgeBaseUploads",
    "Item",
    "ItemDataSourceConfig",
    "ItemChunkingStrategyConfig",
    "ItemChunkingStrategyConfigPreChunkedStrategyConfig",
    "ItemChunkingStrategyConfigEnhancedChunkingStrategyConfig",
]

ItemDataSourceConfig: TypeAlias = Annotated[
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


class ItemChunkingStrategyConfigPreChunkedStrategyConfig(BaseModel):
    """Only compliant with the .chunks file type"""

    strategy: Literal["pre_chunked"]


class ItemChunkingStrategyConfigEnhancedChunkingStrategyConfig(BaseModel):
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


ItemChunkingStrategyConfig: TypeAlias = Annotated[
    Union[
        CharacterChunkingStrategyConfig,
        TokenChunkingStrategyConfig,
        CustomChunkingStrategyConfig,
        ItemChunkingStrategyConfigPreChunkedStrategyConfig,
        ItemChunkingStrategyConfigEnhancedChunkingStrategyConfig,
    ],
    PropertyInfo(discriminator="strategy"),
]


class Item(BaseModel):
    id: str

    data_source_config: ItemDataSourceConfig

    knowledge_base_id: str

    chunking_strategy_config: Optional[ItemChunkingStrategyConfig] = None
    """Only compliant with the .chunks file type"""

    created_at: Union[str, datetime, None] = None

    created_by_schedule_id: Optional[str] = None

    data_source_idempotency_key: Optional[str] = None

    status: Optional[str] = None

    status_reason: Optional[str] = None

    updated_at: Union[str, datetime, None] = None


class PaginatedKnowledgeBaseUploads(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
