# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias, TypedDict

from .s3_data_source_auth_config_param import S3DataSourceAuthConfigParam
from .slack_data_source_auth_config_param import SlackDataSourceAuthConfigParam
from .mongodb_data_source_auth_config_param import MongoDBDataSourceAuthConfigParam
from .shared_params.tagging_information_all import TaggingInformationAll
from .snowflake_data_source_auth_config_param import SnowflakeDataSourceAuthConfigParam
from .confluence_data_source_auth_config_param import ConfluenceDataSourceAuthConfigParam
from .databricks_data_source_auth_config_param import DatabricksDataSourceAuthConfigParam
from .share_point_data_source_auth_config_param import SharePointDataSourceAuthConfigParam
from .google_drive_data_source_auth_config_param import GoogleDriveDataSourceAuthConfigParam
from .sql_database_data_source_auth_config_param import SqlDatabaseDataSourceAuthConfigParam
from .share_point_page_data_source_auth_config_param import SharePointPageDataSourceAuthConfigParam
from .azure_blob_storage_data_source_auth_config_param import AzureBlobStorageDataSourceAuthConfigParam
from .google_cloud_storage_data_source_auth_config_param import GoogleCloudStorageDataSourceAuthConfigParam

__all__ = ["KnowledgeBaseDataSourceUpdateParams", "DataSourceAuthConfig"]


class KnowledgeBaseDataSourceUpdateParams(TypedDict, total=False):
    data_source_auth_config: DataSourceAuthConfig

    description: str

    name: str

    tagging_information: TaggingInformationAll


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
