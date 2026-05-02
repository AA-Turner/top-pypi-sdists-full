# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .s3_data_source_config_param import S3DataSourceConfigParam
from .slack_data_source_config_param import SlackDataSourceConfigParam
from .mongodb_data_source_config_param import MongoDBDataSourceConfigParam
from .s3_data_source_auth_config_param import S3DataSourceAuthConfigParam
from .snowflake_data_source_config_param import SnowflakeDataSourceConfigParam
from .confluence_data_source_config_param import ConfluenceDataSourceConfigParam
from .databricks_data_source_config_param import DatabricksDataSourceConfigParam
from .slack_data_source_auth_config_param import SlackDataSourceAuthConfigParam
from .share_point_data_source_config_param import SharePointDataSourceConfigParam
from .google_drive_data_source_config_param import GoogleDriveDataSourceConfigParam
from .mongodb_data_source_auth_config_param import MongoDBDataSourceAuthConfigParam
from .shared_params.tagging_information_all import TaggingInformationAll
from .sql_database_data_source_config_param import SqlDatabaseDataSourceConfigParam
from .snowflake_data_source_auth_config_param import SnowflakeDataSourceAuthConfigParam
from .confluence_data_source_auth_config_param import ConfluenceDataSourceAuthConfigParam
from .databricks_data_source_auth_config_param import DatabricksDataSourceAuthConfigParam
from .share_point_data_source_auth_config_param import SharePointDataSourceAuthConfigParam
from .share_point_page_data_source_config_param import SharePointPageDataSourceConfigParam
from .google_drive_data_source_auth_config_param import GoogleDriveDataSourceAuthConfigParam
from .sql_database_data_source_auth_config_param import SqlDatabaseDataSourceAuthConfigParam
from .azure_blob_storage_data_source_config_param import AzureBlobStorageDataSourceConfigParam
from .google_cloud_storage_data_source_config_param import GoogleCloudStorageDataSourceConfigParam
from .share_point_page_data_source_auth_config_param import SharePointPageDataSourceAuthConfigParam
from .azure_blob_storage_data_source_auth_config_param import AzureBlobStorageDataSourceAuthConfigParam
from .google_cloud_storage_data_source_auth_config_param import GoogleCloudStorageDataSourceAuthConfigParam

__all__ = ["KnowledgeBaseDataSourceCreateParams", "DataSourceConfig", "DataSourceAuthConfig"]


class KnowledgeBaseDataSourceCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    data_source_config: Required[DataSourceConfig]

    name: Required[str]

    data_source_auth_config: DataSourceAuthConfig

    description: str

    tagging_information: TaggingInformationAll


DataSourceConfig: TypeAlias = Union[
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

DataSourceAuthConfig: TypeAlias = Union[
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
