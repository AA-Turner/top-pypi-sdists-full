#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import datetime
import inspect
from typing import Any, Dict, List, Optional, Union

import trafaret as t
from trafaret.contrib.rfc_3339 import DateTime

from datarobot._experimental.models.enums import ChunkingType, ChunkStorageType, OriginStorageType
from datarobot.enums import DEFAULT_MAX_WAIT, enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import camelize
from datarobot.utils.waiters import wait_for_async_resolution


class ChunkStorage(APIObject):
    """
    The chunk storage location for the data chunks.

    Attributes
    ----------
     storage_reference_id : str
        The ID of the storage entity.
     chunk_storage_type : str
        The type of the chunk storage.
     version_id : str
        The catalog version ID. This will only be used if the storage type is "AI Catalog".

    """

    _converter = t.Dict(
        {
            t.Key("storage_reference_id"): t.String,
            t.Key("chunk_storage_type"): t.String,
            t.Key("version_id", optional=True): t.Or(t.String, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        storage_reference_id: str,
        chunk_storage_type: str,
        version_id: Optional[str] = None,
    ):
        self.storage_reference_id = storage_reference_id
        self.chunk_storage_type = chunk_storage_type
        self.version_id = version_id


class Chunk(APIObject):
    """
    Data chunk object that holds metadata about a chunk.

    Attributes
    ----------
    id : str
        The ID of the chunk entity.
    chunk_definition_id : str
        The ID of the dataset chunk definition the chunk belongs to.
    limit : int
        The number of rows in the chunk.
    offset : int
        The offset in the dataset to create the chunk.
    chunk_index : str
        The index of the chunk if chunks are divided uniformly. Otherwise, it is None.
    data_source_id : str
        The ID of the data request used to create the chunk.
    chunk_storage : ChunkStorage
        A list of storage locations where the chunk is stored.

    """

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("chunk_definition_id"): t.String,
            t.Key("limit"): t.Int,
            t.Key("offset"): t.Int,
            t.Key("chunk_index", optional=True): t.Or(t.Int, t.Null),
            t.Key("data_source_id", optional=True): t.Or(t.String, t.Null),
            t.Key("chunk_storage", optional=True): t.Or(t.List(ChunkStorage._converter), t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        chunk_definition_id: str,
        limit: int,
        offset: int,
        chunk_index: Optional[int] = None,
        data_source_id: Optional[str] = None,
        chunk_storage: Optional[List[ChunkStorage]] = None,
    ):
        self.id = id
        self.chunk_definition_id = chunk_definition_id
        self.chunk_index = chunk_index
        self.offset = offset
        self.limit = limit
        self.data_source_id = data_source_id
        self.chunk_storage = chunk_storage

    def get_chunk_storage_id(self, storage_type: ChunkStorageType) -> Optional[str]:
        """
        Get storage location ID for the chunk.

        Parameters
        ----------
        storage_type: ChunkStorageType
            The storage type where the chunk is stored.

        Returns
        -------
        storage_reference_id: str
            An ID that references the storage location for the chunk.

        """
        if self.chunk_storage is None:
            return None

        for chunk_storage in self.chunk_storage:
            if isinstance(chunk_storage, Dict):
                chunk_storage = ChunkStorage(**chunk_storage)

            if chunk_storage.chunk_storage_type == storage_type:
                return chunk_storage.storage_reference_id
        return None

    def get_chunk_storage_version_id(self, storage_type: ChunkStorageType) -> Optional[str]:
        """
        Get storage version ID for the chunk.

        Parameters
        ----------
        storage_type: ChunkStorageType
            The storage type where the chunk is stored.

        Returns
        -------
        storage_reference_id: str
            A catalog version ID associated with the AI Catalog dataset ID.

        """
        if self.chunk_storage is None:
            return None

        for chunk_storage in self.chunk_storage:
            if isinstance(chunk_storage, Dict):
                chunk_storage = ChunkStorage(**chunk_storage)

            if chunk_storage.chunk_storage_type == storage_type:
                return chunk_storage.version_id
        return None


class DatasourceDefinition(APIObject):
    """
    Data source definition that holds information of data source for API responses.
    Do not use this to 'create' DatasourceDefinition objects directly, use
    DatasourceAICatalogInfo and DatasourceDataWarehouseInfo.

    Attributes
    ----------
    id : str
        The ID of the data source definition.
    data_store_id : str
        The ID of the data store.
    credentials_id : str
      The ID of the credentials.
    table : str
        The data source table name.
    schema : str
        The offset into the dataset to create the chunk.
    catalog : str
        The database or catalog name.
    storage_origin : str
        The origin data source or data warehouse (e.g., Snowflake, BigQuery).
    data_source_id : str
        The ID of the data request used to generate sampling and metadata.
    total_rows : str
        The total number of rows in the dataset.
    source_size : str
        The size of the dataset.
    estimated_size_per_row : str
        The estimated size per row.
    columns : str
        The list of column names in the dataset.
    order_by_columns : List[str]
        A list of columns used to sort the dataset.
    is_descending_order : bool
        Orders the direction of the data. Defaults to False, ordering from smallest to largest.
    select_columns : List[str]
        A list of columns to select from the dataset.
    datetime_partition_column : str
        The datetime partition column name used in OTV projects.
    validation_pct : float
        The percentage threshold between 0.1 and 1.0 for the first chunk validation.
    validation_limit_pct : float
        The percentage threshold between 0.1 and 1.0 for the validation kept.
    validation_start_date : datetime.datetime
        The start date for validation.
    validation_end_date : datetime.datetime
        The end date for validation.
    training_end_date : datetime.datetime
        The end date for training.
    latest_timestamp : datetime.datetime
        The latest timestamp.
    earliest_timestamp : datetime.datetime
        The earliest timestamp.

    """

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("data_store_id", optional=True): t.Or(t.String, t.Null),
            t.Key("credentials_id", optional=True): t.Or(t.String, t.Null),
            t.Key("table", optional=True): t.Or(t.String, t.Null),
            t.Key("schema", optional=True): t.Or(t.String, t.Null),
            t.Key("catalog", optional=True): t.Or(t.String, t.Null),
            t.Key("storage_origin"): t.Enum(*enum_to_list(OriginStorageType)),
            t.Key("name", optional=True): t.Or(t.String, t.Null),
            t.Key("data_source_id", optional=True): t.Or(t.String, t.Null),
            t.Key("total_rows", optional=True): t.Or(t.Int, t.Null),
            t.Key("source_size", optional=True): t.Or(t.Int, t.Null),
            t.Key("estimated_size_per_row", optional=True): t.Or(t.Int, t.Null),
            t.Key("columns", optional=True): t.Or(t.List(t.String), t.Null),
            t.Key("catalog_id", optional=True): t.Or(t.String, t.Null),
            t.Key("catalog_version_id", optional=True): t.Or(t.String, t.Null),
            t.Key("order_by_columns"): t.List(t.String, min_length=0),
            t.Key("is_descending_order", optional=True): t.Bool,
            t.Key("select_columns", optional=True): t.Or(t.List(t.String), t.Null),
            t.Key("datetime_partition_column", optional=True): t.Or(t.String, t.Null),
            t.Key("validation_pct", optional=True): t.Or(t.Float, t.Null),
            t.Key("validation_limit_pct", optional=True): t.Or(t.Float, t.Null),
            t.Key("validation_start_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("validation_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("training_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("latest_timestamp", optional=True): t.Or(DateTime(), t.Null),
            t.Key("earliest_timestamp", optional=True): t.Or(DateTime(), t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        storage_origin: OriginStorageType,
        order_by_columns: Optional[List[str]] = None,
        is_descending_order: Optional[bool] = False,
        table: Optional[str] = None,
        data_store_id: Optional[str] = None,
        credentials_id: Optional[str] = None,
        schema: Optional[str] = None,
        catalog: Optional[str] = None,
        name: Optional[str] = None,
        data_source_id: Optional[str] = None,
        total_rows: Optional[int] = None,
        source_size: Optional[int] = None,
        estimated_size_per_row: Optional[int] = None,
        columns: Optional[List[str]] = None,
        catalog_id: Optional[str] = None,
        catalog_version_id: Optional[str] = None,
        select_columns: Optional[List[str]] = None,
        datetime_partition_column: Optional[str] = None,
        validation_pct: Optional[float] = None,
        validation_limit_pct: Optional[float] = None,
        validation_start_date: Optional[datetime] = None,
        validation_end_date: Optional[datetime] = None,
        training_end_date: Optional[datetime] = None,
        latest_timestamp: Optional[datetime] = None,
        earliest_timestamp: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.data_store_id = data_store_id
        self.credentials_id = credentials_id
        self.table = table
        self.schema = schema
        self.catalog = catalog
        self.storage_origin = storage_origin
        self.data_source_id = data_source_id
        self.total_rows = total_rows
        self.source_size = source_size
        self.estimated_size_per_row = estimated_size_per_row
        self.columns = columns
        self.catalog_id = catalog_id
        self.catalog_version_id = catalog_version_id
        self.order_by_columns = [] if order_by_columns is None else order_by_columns
        self.is_descending_order = is_descending_order
        self.select_columns = select_columns
        self.datetime_partition_column = datetime_partition_column
        self.validation_pct = validation_pct
        self.validation_limit_pct = validation_limit_pct
        self.validation_start_date = validation_start_date
        self.validation_end_date = validation_end_date
        self.training_end_date = training_end_date
        self.latest_timestamp = latest_timestamp
        self.earliest_timestamp = earliest_timestamp


class DatasourceDataWarehouseInfo(APIObject):
    """
    Data source information used at creation time with dataset chunk definition.
    Data warehouses supported: Snowflake, BigQuery, Databricks


    Attributes
    ----------
    name: str
        The optional custom name of the data source.
    table : str
        The data source table name or AI Catalog dataset name.
    storage_origin : str
        The origin data source or data warehouse (e.g., Snowflake, BigQuery).
    data_store_id : str
        The ID of the data store.
    credentials_id : str
        The ID of the credentials.
    schema : str
        The offset into the dataset to create the chunk.
    catalog : str
        The database or catalog name.
    data_source_id : str
        The ID of the data request used to generate sampling and metadata.
    order_by_columns : List[str]
        A list of columns used to sort the dataset.
    is_descending_order : bool
        Orders the direction of the data. Defaults to False, ordering from smallest to largest.
    select_columns: List[str]
        A list of columns to select from the dataset.
    datetime_partition_column : str
        The datetime partition column name used in OTV projects.
    validation_pct : float
        The percentage threshold between 0.1 and 1.0 for the first chunk validation.
    validation_limit_pct : float
        The percentage threshold between 0.1 and 1.0 for the validation kept.
    validation_start_date : datetime.datetime
        The start date for validation.
    validation_end_date : datetime.datetime
        The end date for validation.
    training_end_date : datetime.datetime
        The end date for training.
    latest_timestamp : datetime.datetime
        The latest timestamp.
    earliest_timestamp : datetime.datetime
        The earliest timestamp.

    """

    _converter = t.Dict(
        {
            t.Key("data_store_id"): t.String,
            t.Key("credentials_id"): t.String,
            t.Key("table"): t.String,
            t.Key("order_by_columns"): t.List(t.String),
            t.Key("is_descending_order", optional=True): t.Bool,
            t.Key("storage_origin"): t.Enum(
                OriginStorageType.SNOWFLAKE,
                OriginStorageType.BIGQUERY,
                OriginStorageType.AI_CATALOG,
                OriginStorageType.DATABRICKS,
            ),
            t.Key("schema", optional=True): t.Or(t.String, t.Null),
            t.Key("catalog", optional=True): t.Or(t.String, t.Null),
            t.Key("name", optional=True): t.Or(t.String, t.Null),
            t.Key("data_source_id", optional=True): t.Or(t.String, t.Null),
            t.Key("select_columns", optional=True): t.Or(t.List(t.String), t.Null),
            t.Key("datetime_partition_column", optional=True): t.Or(t.String, t.Null),
            t.Key("validation_pct", optional=True): t.Or(t.Float, t.Null),
            t.Key("validation_limit_pct", optional=True): t.Or(t.Float, t.Null),
            t.Key("validation_start_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("validation_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("training_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("latest_timestamp", optional=True): t.Or(DateTime(), t.Null),
            t.Key("earliest_timestamp", optional=True): t.Or(DateTime(), t.Null),
        }
    )

    def __init__(
        self,
        data_store_id: str,
        credentials_id: str,
        table: str,
        storage_origin: OriginStorageType,
        order_by_columns: List[str],
        is_descending_order: bool = False,
        schema: Optional[str] = None,
        catalog: Optional[str] = None,
        name: Optional[str] = None,
        data_source_id: Optional[str] = None,
        select_columns: Optional[List[str]] = None,
        datetime_partition_column: Optional[str] = None,
        validation_pct: Optional[float] = None,
        validation_limit_pct: Optional[float] = None,
        validation_start_date: Optional[datetime] = None,
        validation_end_date: Optional[datetime] = None,
        training_end_date: Optional[datetime] = None,
        latest_timestamp: Optional[datetime] = None,
        earliest_timestamp: Optional[datetime] = None,
    ):
        self.name = name
        self.data_store_id = data_store_id
        self.credentials_id = credentials_id
        self.table = table
        self.schema = schema
        self.catalog = catalog
        self.storage_origin = storage_origin
        self.data_source_id = data_source_id
        self.order_by_columns = order_by_columns
        self.is_descending_order = is_descending_order
        self.select_columns = select_columns
        self.datetime_partition_column = datetime_partition_column
        self.validation_pct = validation_pct
        self.validation_limit_pct = validation_limit_pct
        self.validation_start_date = validation_start_date
        self.validation_end_date = validation_end_date
        self.training_end_date = training_end_date
        self.latest_timestamp = latest_timestamp
        self.earliest_timestamp = earliest_timestamp
        self._converter.check(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        self_dict = {
            attr[0]: attr[1]
            for attr in inspect.getmembers(self)
            if (not attr[0].startswith("_") and not inspect.ismethod(attr[1]))
        }
        return self_dict


class DatasourceAICatalogInfo(APIObject):
    """
    AI Catalog data source information used at creation time with dataset chunk definition.


    Attributes
    ----------
    name: str
        The optional custom name of the data source.
    table : str
        The data source table name or AI Catalog dataset name.
    storage_origin : str
        The origin data source, always AI Catalog type.
    catalog_id : str
        The ID of the AI Catalog dataset.
    catalog_version_id : str
        The ID of the AI Catalog dataset version.
    order_by_columns : List[str]
        A list of columns used to sort the dataset.
    is_descending_order : bool
        Orders the direction of the data. Defaults to False, ordering from smallest to largest.
    select_columns: List[str]
        A list of columns to select from the dataset.
    datetime_partition_column : str
        The datetime partition column name used in OTV projects.
    validation_pct : float
        The percentage threshold between 0.1 and 1.0 for the first chunk validation.
    validation_limit_pct : float
        The percentage threshold between 0.1 and 1.0 for the validation kept.
    validation_start_date : datetime.datetime
        The start date for validation.
    validation_end_date : datetime.datetime
        The end date for validation.
    training_end_date : datetime.datetime
        The end date for training.
    latest_timestamp : datetime.datetime
        The latest timestamp.
    earliest_timestamp : datetime.datetime
        The earliest timestamp.

    """

    _converter = t.Dict(
        {
            t.Key("catalog_version_id"): t.String,
            t.Key("catalog_id", optional=True): t.Or(t.String, t.Null),
            t.Key("storage_origin"): t.Enum(OriginStorageType.AI_CATALOG),
            t.Key("table", optional=True): t.Or(t.String, t.Null),
            t.Key("name", optional=True): t.Or(t.String, t.Null),
            t.Key("order_by_columns", optional=True): t.List(t.String, min_length=0),
            t.Key("is_descending_order", optional=True): t.Bool,
            t.Key("select_columns", optional=True): t.Or(t.List(t.String), t.Null),
            t.Key("datetime_partition_column", optional=True): t.Or(t.String, t.Null),
            t.Key("validation_pct", optional=True): t.Or(t.Float, t.Null),
            t.Key("validation_limit_pct", optional=True): t.Or(t.Float, t.Null),
            t.Key("validation_start_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("validation_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("training_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("latest_timestamp", optional=True): t.Or(DateTime(), t.Null),
            t.Key("earliest_timestamp", optional=True): t.Or(DateTime(), t.Null),
        }
    )

    def __init__(
        self,
        catalog_version_id: str,
        catalog_id: Optional[str] = None,
        table: Optional[str] = None,
        name: Optional[str] = None,
        order_by_columns: Optional[List[str]] = None,
        is_descending_order: Optional[bool] = False,
        select_columns: Optional[List[str]] = None,
        datetime_partition_column: Optional[str] = None,
        validation_pct: Optional[float] = None,
        validation_limit_pct: Optional[float] = None,
        validation_start_date: Optional[datetime] = None,
        validation_end_date: Optional[datetime] = None,
        training_end_date: Optional[datetime] = None,
        latest_timestamp: Optional[datetime] = None,
        earliest_timestamp: Optional[datetime] = None,
    ):
        self.name = name
        self.catalog_version_id = catalog_version_id
        self.catalog_id = catalog_id
        self.table = table
        self.storage_origin = OriginStorageType.AI_CATALOG
        self.order_by_columns = [] if order_by_columns is None else order_by_columns
        self.is_descending_order = is_descending_order
        self.select_columns = select_columns
        self.datetime_partition_column = datetime_partition_column
        self.validation_pct = validation_pct
        self.validation_limit_pct = validation_limit_pct
        self.validation_start_date = validation_start_date
        self.validation_end_date = validation_end_date
        self.training_end_date = training_end_date
        self.latest_timestamp = latest_timestamp
        self.earliest_timestamp = earliest_timestamp
        self._converter.check(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        self_dict = {
            attr[0]: attr[1]
            for attr in inspect.getmembers(self)
            if (not attr[0].startswith("_") and not inspect.ismethod(attr[1]))
        }
        return self_dict


class DatasetChunkDefinition(APIObject):
    """
    Dataset chunking definition that holds information about how to chunk the dataset.

    Attributes
    ----------
    id : str
        The ID of the dataset chunk definition.
    user_id : str
        The ID of the user who created the definition.
    name : str
        The name of the dataset chunk definition.
    project_starter_chunk_size : int
        The size, in bytes, of the project starter chunk.
    user_chunk_size : int
        Chunk size in bytes.
    datasource_definition_id : str
        The data source definition ID associated with the dataset chunk definition.
    chunking_type : ChunkingType
        The type of chunk creation from the dataset.
        All possible chunking types can be found under ChunkingType enum, that can be
        imported from datarobot._experimental.models.enums
        Types include:

            - INCREMENTAL_LEARNING for non-time aware projects that use a chunk index to create chunks.
            - INCREMENTAL_LEARNING_OTV for OTV projects that use a chunk index to create chunks.
            - SLICED_OFFSET_LIMIT for any dataset in which user provides offset and limit to create chunks.

        SLICED_OFFSET_LIMIT has no indexed based chunks aka method create_by_index() not supported.

    """

    _path = "datasetChunkDefinitions/"
    _path_with_id = _path + "{}/"
    _path_datasource = _path + "{}/datasourceDefinition/"
    _path_chunks = _path + "{}/chunks/"
    _path_chunk = _path_chunks + "{}/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("user_id"): t.String,
            t.Key("name"): t.String,
            t.Key("project_starter_chunk_size"): t.Int,
            t.Key("user_chunk_size"): t.Int,
            t.Key("datasource_definition_id", optional=True): t.Or(t.String, t.Null),
            t.Key("chunking_type", optional=True): t.Or(
                t.Enum(*enum_to_list(ChunkingType)), t.Null
            ),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        user_id: str,
        name: str,
        project_starter_chunk_size: int,
        user_chunk_size: int,
        datasource_definition_id: Optional[str] = None,
        chunking_type: Optional[ChunkingType] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.project_starter_chunk_size = project_starter_chunk_size
        self.user_chunk_size = user_chunk_size
        self.datasource_definition_id = datasource_definition_id
        self.chunking_type = chunking_type

    @classmethod
    def get(cls, dataset_chunk_definition_id: str) -> DatasetChunkDefinition:
        """
        Retrieve a specific dataset chunk definition metadata.

        Parameters
        ----------
        dataset_chunk_definition_id: str
            The ID of the dataset chunk definition.

        Returns
        -------
        dataset_chunk_definition : DatasetChunkDefinition
            The queried instance.
        """
        path = cls._path_with_id.format(dataset_chunk_definition_id)
        response = cls._client.get(path)
        return cls.from_server_data(response.json())

    @classmethod
    def list(cls, limit: int = 50, offset: int = 0) -> List[DatasetChunkDefinition]:
        """
        Retrieves a list of dataset chunk definitions

        Parameters
        ----------
        limit: int
            The maximum number of objects to return. Default is 50.
        offset: int
            The starting offset of the results. Default is 0.
        Returns
        -------
        dataset_chunk_definitions : List[DatasetChunkDefinition]
            The list of dataset chunk definitions.

        """
        params: Dict[str, Union[str, int]] = {"limit": limit, "offset": offset}
        response = cls._client.get(cls._path, params=params)
        r_data = response.json()
        return [cls.from_server_data(item) for item in r_data["data"]]

    @classmethod
    def create(
        cls,
        name: str,
        project_starter_chunk_size: int,
        user_chunk_size: int,
        datasource_info: Union[DatasourceDataWarehouseInfo, DatasourceAICatalogInfo],
        chunking_type: ChunkingType = ChunkingType.INCREMENTAL_LEARNING,
    ) -> DatasetChunkDefinition:
        """
        Create a dataset chunk definition. Required for both index-based and custom chunks.

        In order to create a dataset chunk definition, you must first:

            - Create a data connection to the target data source via ``dr.DataStore.create()``
            - Create credentials that must be attached to the data connection via ``dr.Credential.create()``

        If you have an existing data connections and credentials:

            - Retrieve the data store ID by the canonical name via:

                - ``[ds for ds in dr.DataStore.list() if ds.canonical_name == <name>][0].id``
            - Retrieve the credential ID by the name via:

                - ``[cr for cr in dr.Credential.list() if ds.name == <name>][0].id``

        You must create the required 'datasource_info' object with the datasource information
        that corresponds to your use case:

            - DatasourceAICatalogInfo for AI catalog datasets.
            - DatasourceDataWarehouseInfo for Snowflake, BigQuery, or other data warehouse.

        Parameters
        ----------
        name : str
            The name of the dataset chunk definition.
        project_starter_chunk_size : int
            The size, in bytes, of the first chunk. Used to start a DataRobot project.
        user_chunk_size : int
            The size, in bytes, of the user-defined incremental chunk.
        datasource_info : Union[DatasourceDataWarehouseInfo, DatasourceAICatalogInfo]
            The object that contains the information of the data source.
        chunking_type : ChunkingType
            The type of chunk creation from the dataset.
            All possible chunking types can be found under ChunkingType enum, that can be
            imported from datarobot._experimental.models.enums
            Types include:

                - INCREMENTAL_LEARNING for non-time aware projects that use a chunk index to create chunks.
                - INCREMENTAL_LEARNING_OTV for OTV projects that use a chunk index to create chunks.
                - SLICED_OFFSET_LIMIT for any dataset in which user provides offset and limit to create chunks.

            SLICED_OFFSET_LIMIT has no indexed based chunks aka method create_by_index() not supported.
            The default type is ChunkingType.INCREMENTAL_LEARNING


        Returns
        -------
        dataset_chunk_definition: DatasetChunkDefinition
            An instance of a created dataset chunk definition.

        """
        if not isinstance(datasource_info, (DatasourceAICatalogInfo, DatasourceDataWarehouseInfo)):
            raise TypeError(
                "'datasource_info' expects object of ('DatasourceAICatalogInfo', 'DatasourceDataWarehouseInfo')"
            )
        datasource_info_dict = datasource_info.to_dict()
        payload = {
            "name": name,
            "starterChunkSize": project_starter_chunk_size,
            "chunkSize": user_chunk_size,
            "chunkingType": chunking_type,
            "datasourceInfo": {camelize(key): val for key, val in datasource_info_dict.items()},
        }
        response = cls._client.post(cls._path, data=payload)
        data = response.json()
        return cls.from_server_data(data)

    @classmethod
    def get_datasource_definition(cls, dataset_chunk_definition_id: str) -> DatasourceDefinition:
        """
        Retrieves the data source definition associated with a dataset chunk definition.

        Parameters
        ----------
        dataset_chunk_definition_id: str
            id of the dataset chunk definition

        Returns
        -------
        datasource_definition: DatasourceDefinition
            an instance of created datasource definition
        """
        path = cls._path_datasource.format(dataset_chunk_definition_id)
        response = cls._client.get(path)
        return DatasourceDefinition.from_server_data(response.json())

    @classmethod
    def get_chunk(cls, dataset_chunk_definition_id: str, chunk_id: str) -> Chunk:
        """
        Retrieves a specific data chunk associated with a dataset chunk definition

        Parameters
        ----------
        dataset_chunk_definition_id: str
            id of the dataset chunk definition
        chunk_id:
            id of the chunk

        Returns
        -------
        chunk: Chunk
            an instance of created chunk
        """
        path = cls._path_chunk.format(dataset_chunk_definition_id, chunk_id)
        response = cls._client.get(path)
        return Chunk.from_server_data(response.json())

    @classmethod
    def list_chunks(cls, dataset_chunk_definition_id: str) -> List[Chunk]:
        """
        Retrieves all data chunks associated with a dataset chunk definition

        Parameters
        ----------
        dataset_chunk_definition_id: str
            id of the dataset chunk definition

        Returns
        -------
        chunks: List[Chunk]
            a list of chunks
        """
        path = cls._path_chunks.format(dataset_chunk_definition_id)
        response = cls._client.get(path)
        r_data = response.json()
        return [Chunk.from_server_data(item) for item in r_data["data"]]

    def analyze_dataset(self, max_wait_time: int = DEFAULT_MAX_WAIT) -> DatasourceDefinition:
        """
        Analyzes the data source to retrieve and compute metadata about the dataset.

        Depending on the size of the data set, adding ``order_by_columns`` to the dataset chunking definition
        will increase the execution time to create the data chunk.
        Set the ``max_wait_time`` for the appropriate wait time.

        Parameters
        ----------
        max_wait_time
            maximum time to wait for completion
        Returns
        -------
        datasource_definition: DatasourceDefinition
            an instance of created datasource definition
        """
        path = self._path_with_id + "analyzeDataset"
        response = self._client.post(path.format(self.id))
        async_loc = response.headers["Location"]
        datasource_location = wait_for_async_resolution(
            self._client, async_loc, max_wait=max_wait_time
        )
        return DatasourceDefinition.from_location(datasource_location)

    def create_chunk(
        self,
        limit: int,
        offset: int = 0,
        storage_type: ChunkStorageType = ChunkStorageType.DATASTAGE,
        max_wait_time: int = DEFAULT_MAX_WAIT,
    ) -> Chunk:
        """
        Creates a data chunk using the limit and offset. By default, the data chunk is stored in data stages.

        Depending on the size of the data set, adding ``order_by_columns`` to the dataset chunking definition
        will increase the execution time to retrieve or create the data chunk.
        Set the ``max_wait_time`` for the appropriate wait time.

        Parameters
        ----------
        limit: int
            The maximum number of rows.
        offset: int
            The offset into the dataset (where reading begins).
        storage_type: ChunkStorageType
            The storage location of the chunk.
        max_wait_time
            maximum time to wait for completion
        Returns
        -------
        chunk: Chunk
            An instance of a created or updated chunk.
        """
        payload = {
            "limit": limit,
            "offset": offset,
            "storageType": storage_type,
        }

        url = self._path_with_id + "createChunk"
        path = url.format(self.id)
        return self._create_chunk(path, payload, max_wait_time=max_wait_time)

    def create_chunk_by_index(
        self,
        index: int,
        storage_type: ChunkStorageType = ChunkStorageType.DATASTAGE,
        max_wait_time: int = DEFAULT_MAX_WAIT,
    ) -> Chunk:
        """
        Creates a data chunk using the limit and offset. By default, the data chunk is stored in data stages.

        Depending on the size of the data set, adding ``order_by_columns`` to the dataset chunking definition
        will increase the execution time to retrieve or create the data chunk.
        Set the ``max_wait_time`` for the appropriate wait time.

        Parameters
        ----------
        index: int
            The index of the chunk.
        storage_type: ChunkStorageType
            The storage location of the chunk.
        max_wait_time
            maximum time to wait for completion

        Returns
        -------
        chunk: Chunk
            An instance of a created or updated chunk.
        """
        payload = {
            "index": index,
            "storageType": storage_type,
        }
        url = self._path_with_id + "createIndexChunk"
        path = url.format(self.id)
        return self._create_chunk(path, payload, max_wait_time=max_wait_time)

    def _create_chunk(
        self, path: str, payload: Dict[str, Any], max_wait_time: int = DEFAULT_MAX_WAIT
    ) -> Chunk:
        response = self._client.post(path, data=payload)
        async_loc = response.headers["Location"]
        chunk_location = wait_for_async_resolution(self._client, async_loc, max_wait=max_wait_time)
        return Chunk.from_location(chunk_location)

    @classmethod
    def patch_validation_dates(
        cls,
        dataset_chunk_definition_id: str,
        validation_start_date: datetime,
        validation_end_date: datetime,
    ) -> DatasourceDefinition:
        """
        Updates the data source definition validation dates associated with a dataset chunk definition.
        In order to set the validation dates appropriately, both start and end dates should be specified.
        This method can only be used for INCREMENTAL_LEARNING_OTV dataset chunk definitions and
        its associated datasource definition.

        Parameters
        ----------
        dataset_chunk_definition_id: str
            The ID of the dataset chunk definition.
        validation_start_date: datetime.datetime
            The start date of validation scoring data.
            Internally converted to format '%Y-%m-%d %H:%M:%S', the timezone defaults to UTC.
        validation_end_date: datetime.datetime
            The end date of validation scoring data.
            Internally converted to format '%Y-%m-%d %H:%M:%S', the timezone defaults to UTC.

        Returns
        -------
        datasource_definition: DatasourceDefinition
            An instance of created datasource definition.
        """
        path = cls._path_datasource.format(dataset_chunk_definition_id)
        if not isinstance(validation_start_date, datetime):
            raise ValueError("expected validation_start_date to be a datetime.datetime")
        if not isinstance(validation_end_date, datetime):
            raise ValueError("expected validation_end_date to be a datetime.datetime")
        date_format = "%Y-%m-%d %H:%M:%S"
        validation_start_date_str = validation_start_date.strftime(date_format)
        validation_end_date_str = validation_end_date.strftime(date_format)
        body = {
            "validationStartDate": validation_start_date_str,
            "validationEndDate": validation_end_date_str,
        }
        response = cls._client.patch(path, json=body)
        return DatasourceDefinition.from_server_data(response.json())
