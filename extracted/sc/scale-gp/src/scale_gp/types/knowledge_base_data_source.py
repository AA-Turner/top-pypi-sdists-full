# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .s3_data_source_config import S3DataSourceConfig
from .slack_data_source_config import SlackDataSourceConfig
from .mongodb_data_source_config import MongoDBDataSourceConfig
from .snowflake_data_source_config import SnowflakeDataSourceConfig
from .confluence_data_source_config import ConfluenceDataSourceConfig
from .databricks_data_source_config import DatabricksDataSourceConfig
from .share_point_data_source_config import SharePointDataSourceConfig
from .shared.tagging_information_all import TaggingInformationAll
from .google_drive_data_source_config import GoogleDriveDataSourceConfig
from .sql_database_data_source_config import SqlDatabaseDataSourceConfig
from .share_point_page_data_source_config import SharePointPageDataSourceConfig
from .azure_blob_storage_data_source_config import AzureBlobStorageDataSourceConfig
from .google_cloud_storage_data_source_config import GoogleCloudStorageDataSourceConfig

__all__ = ["KnowledgeBaseDataSource", "DataSourceConfig"]

DataSourceConfig: TypeAlias = Annotated[
    Union[
        S3DataSourceConfig,
        SharePointDataSourceConfig,
        SharePointPageDataSourceConfig,
        GoogleDriveDataSourceConfig,
        AzureBlobStorageDataSourceConfig,
        GoogleCloudStorageDataSourceConfig,
        ConfluenceDataSourceConfig,
        SlackDataSourceConfig,
        SnowflakeDataSourceConfig,
        DatabricksDataSourceConfig,
        SqlDatabaseDataSourceConfig,
        MongoDBDataSourceConfig,
    ],
    PropertyInfo(discriminator="source"),
]


class KnowledgeBaseDataSource(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    data_source_config: DataSourceConfig

    name: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    description: Optional[str] = None

    tagging_information: Optional[TaggingInformationAll] = None
