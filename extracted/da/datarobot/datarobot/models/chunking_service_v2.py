#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
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
from typing import Any, Dict, List, Optional, Union

import trafaret as t
from trafaret.contrib.rfc_3339 import DateTime

from datarobot.enums import (
    ChunkingPartitionMethod,
    ChunkingStrategy,
    ChunkServiceDialect,
    DEFAULT_MAX_WAIT,
    enum_to_list,
)
from datarobot.models.api_object import APIObject
from datarobot.utils import from_api
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution


class DatasetProps(APIObject):
    """
    The dataset props for a catalog dataset.

    Attributes
    ----------
    dataset_id : str
       The ID of the AI Catalog dataset.
    dataset_version_id : str
       The ID of the AI Catalog dataset version.

    """

    _converter = t.Dict(
        {
            t.Key("dataset_id"): t.String,
            t.Key("dataset_version_id"): t.String,
        }
    ).allow_extra("*")

    def __init__(
        self,
        dataset_id: str,
        dataset_version_id: str,
    ):
        self.dataset_id = dataset_id
        self.dataset_version_id = dataset_version_id


class DatasetInfo(APIObject):
    """
    The dataset information.

    Attributes
    ----------
    total_rows : str
         The total number of rows in the dataset.
    source_size : str
         The size of the dataset.
    estimated_size_per_row : str
         The estimated size per row.
    columns : str
         The list of column names in the dataset.
    dialect : str
         The sql dialect associated with the dataset (e.g., Snowflake, BigQuery, Spark).
    version : int
         The version of the dataset definition information.
    data_store_id : str
         The ID of the data store.
    data_source_id : str
         The ID of the data request used to generate sampling and metadata.
    """

    _converter = t.Dict(
        {
            t.Key("total_rows"): t.Int,
            t.Key("source_size"): t.Int,
            t.Key("estimated_size_per_row"): t.Int,
            t.Key("columns"): t.List(t.String),
            t.Key("dialect"): t.Enum(*enum_to_list(ChunkServiceDialect)),
            t.Key("version"): t.Int,
            t.Key("data_store_id", optional=True): t.Or(t.String, t.Null),
            t.Key("data_source_id", optional=True): t.Or(t.String, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        total_rows: int,
        source_size: int,
        estimated_size_per_row: int,
        columns: List[str],
        dialect: ChunkServiceDialect,
        version: int,
        data_store_id: Optional[str] = None,
        data_source_id: Optional[str] = None,
    ):
        self.total_rows = total_rows
        self.source_size = source_size
        self.estimated_size_per_row = estimated_size_per_row
        self.columns = columns
        self.dialect = dialect
        self.version = version
        self.data_store_id = data_store_id
        self.data_source_id = data_source_id


class DynamicDatasetProps(APIObject):
    """
    The dataset props for a dynamic dataset.

    Attributes
    ----------
    credentials_id : str
        The ID of the credentials.
    """

    _converter = t.Dict(
        {
            t.Key("credentials_id"): t.String,
        }
    ).allow_extra("*")

    def __init__(
        self,
        credentials_id: str,
    ):
        self.credentials_id = credentials_id


class DatasetDefinitionInfoHistory(APIObject):
    """
    Dataset definition info history for the dataset definition.

    Attributes
    ----------
    id : str
        The ID of the dataset definition information history.
    dataset_info : DatasetInfo
        The versioned information about the dataset.
    """

    _path = "datasetDefinitions/{}/versions/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("dataset_info"): DatasetInfo._converter,
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        dataset_info: DatasetInfo,
    ):
        self.id = id
        self.dataset_info = dataset_info

    @classmethod
    def from_data(
        cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> DatasetDefinitionInfoHistory:
        """Properly convert composition classes."""
        converted_data = cls._converter.check(from_api(data))
        converted_data["dataset_info"] = DatasetInfo(**converted_data["dataset_info"])

        return cls(**converted_data)

    @classmethod
    def list(cls, dataset_definition_id: str) -> List[DatasetDefinitionInfoHistory]:
        """
        List all dataset definition info history

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.

        Returns
        -------
        A list of DatasetDefinitionInfoHistory
        """

        path = cls._path.format(dataset_definition_id)
        data = unpaginate(path, None, cls._client)
        return [cls.from_server_data(item) for item in data]


class DatasetDefinition(APIObject):
    """
    Dataset definition that holds information of dataset for API responses.

    Attributes
    ----------
    id : str
        The ID of the data source definition.
    creator_user_id : str
      The ID of the user.
    dataset_props : DatasetProps
      The properties of the dataset in catalog.
    dynamic_dataset_props : DynamicDatasetProps
      The properties of the dynamic dataset.
    dataset_info : DatasetInfo
      The information about the dataset.
    name: str
      The optional custom name of the dataset definition.
    """

    _path = "datasetDefinitions/"
    _path_with_id = _path + "{}/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("creator_user_id"): t.String,
            t.Key("dataset_props"): DatasetProps._converter,
            t.Key("dynamic_dataset_props", optional=True): t.Or(
                DynamicDatasetProps._converter, t.Null
            ),
            t.Key("dataset_info", optional=True): t.Or(DatasetInfo._converter, t.Null),
            t.Key("name", optional=True): t.Or(t.String, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        creator_user_id: str,
        dataset_props: DatasetProps,
        dynamic_dataset_props: Optional[DynamicDatasetProps] = None,
        dataset_info: Optional[DatasetInfo] = None,
        name: Optional[str] = None,
    ):
        self.id = id
        self.creator_user_id = creator_user_id
        self.dataset_props = dataset_props
        self.dynamic_dataset_props = dynamic_dataset_props
        self.dataset_info = dataset_info
        self.name = name

    @classmethod
    def from_data(cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> DatasetDefinition:
        """Properly convert composition classes."""
        converted_data = cls._converter.check(from_api(data))
        converted_data["dataset_props"] = DatasetProps(**converted_data["dataset_props"])

        if "dataset_info" in converted_data:
            converted_data["dataset_info"] = DatasetInfo(**converted_data["dataset_info"])

        if "dynamic_dataset_props" in converted_data:
            converted_data["dynamic_dataset_props"] = DynamicDatasetProps(
                **converted_data["dynamic_dataset_props"]
            )

        return cls(**converted_data)

    @classmethod
    def create(
        cls,
        dataset_id: str,
        dataset_version_id: Optional[str] = None,
        name: Optional[str] = None,
        credentials_id: Optional[str] = None,
    ) -> DatasetDefinition:
        """
        Create a dataset definition.

        In order to create a dataset definition, you must first have an existing dataset in the Data Registry.
        A dataset can be uploaded using ``dr.Dataset.create_from_file`` if you have a file for example

        If you have an existing dataset in the Data Registry:

            - Retrieve the dataset ID by the canonical name via:

                - ``[cr for cr in dr.Dataset.list() if cr.name == <name>][0].id``
            - Retrieve the dataset version ID by the name via:

                - ``[cr for cr in dr.Dataset.list() if cr.name == <name>][0].version_id``

        Parameters
        ----------
        dataset_id : str
            The ID of the AI Catalog dataset.
        dataset_version_id : str
            The optional ID of the AI Catalog dataset version.
        name: str
            The optional custom name of the dataset definition.
        credentials_id: str
            The optional ID of the credentials to access the data store.


        Returns
        -------
        dataset_definition: DatasetDefinition
            An instance of a created dataset definition.

        """
        payload = {
            "dataset_id": dataset_id,
        }

        if dataset_version_id is not None:
            payload["dataset_version_id"] = dataset_version_id

        if name is not None:
            payload["name"] = name

        if credentials_id is not None:
            payload["credentials_id"] = credentials_id

        response = cls._client.post(cls._path, data=payload)
        data = response.json()
        return cls.from_server_data(data)

    @classmethod
    def get(cls, dataset_definition_id: str, version: Optional[int] = None) -> DatasetDefinition:
        """
        Retrieve a specific dataset definition metadata.

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.
        version: Optional[int]
            The version of the dataset definition information. If not provided, the latest version will be used.

        Returns
        -------
        dataset_definition_id : DatasetDefinition
            The queried instance.
        """
        path = cls._path_with_id.format(dataset_definition_id)
        query_params = {}
        if version is not None:
            query_params["version"] = version
        response = cls._client.get(path, params=query_params)
        return cls.from_server_data(response.json())

    @classmethod
    def delete(cls, dataset_definition_id: str) -> None:
        """
        Delete a specific dataset definition

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.

        """
        path = cls._path_with_id.format(dataset_definition_id)
        cls._client.delete(path)

    @classmethod
    def list(cls) -> List[DatasetDefinition]:
        """
        List all dataset definitions

        Returns
        -------
        A list of DatasetDefinition
        """
        path = cls._path
        data = unpaginate(path, None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def analyze(cls, dataset_definition_id: str, max_wait: int = DEFAULT_MAX_WAIT) -> None:
        """
        Analyze a specific dataset definition

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.
        max_wait: Optional[int]
            Time in seconds after which analyze is considered unsuccessful

        """
        path = cls._path_with_id.format(dataset_definition_id) + "analyze/"
        resp = cls._client.post(path, data={})
        if resp.status_code == 204:
            return
        elif resp.status_code == 202:
            # ignore new location since we return None
            wait_for_async_resolution(cls._client, resp.headers["Location"], max_wait)

    @classmethod
    def list_versions(cls, dataset_definition_id: str) -> List[DatasetDefinitionInfoHistory]:
        """
        List all info history of the dataset definition.

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.

        Returns
        -------
        A list of DatasetDefinitionInfoHistory
        """
        return DatasetDefinitionInfoHistory.list(dataset_definition_id)


class RowsChunkDefinition(APIObject):
    """
    The rows chunk information.

    Attributes
    ----------
    order_by_columns : List[str]
         List of the sorting column names.
    is_descending_order : bool
         The sorting order. Defaults to False, ordering from smallest to largest.
    target_column : str
        The target column.
    target_class : str
        For binary target, one of the possible values. For zero inflated, will be '0'.
    user_group_column : str
        The user group column.
    datetime_partition_column : str
        The datetime partition column name used in OTV projects.
    otv_validation_start_date : datetime.datetime
        The start date for the validation set.
    otv_validation_end_date : datetime.datetime
        The end date for the validation set.
    otv_training_end_date : datetime.datetime
        The end date for the training set.
    otv_latest_timestamp : datetime.datetime
        The latest timestamp, this field is auto generated.
    otv_earliest_timestamp : datetime.datetime
        The earliest timestamp, this field is auto generated.
    otv_validation_downsampling_pct : float
        The percentage of the validation set to downsample, this field is auto generated.
    """

    _converter = t.Dict(
        {
            t.Key("order_by_columns"): t.List(t.String, min_length=0),
            t.Key("is_descending_order"): t.Bool,
            t.Key("target_column", optional=True): t.Or(t.String, t.Null),
            t.Key("target_class", optional=True): t.Or(t.String, t.Null),
            t.Key("user_group_column", optional=True): t.Or(t.String, t.Null),
            t.Key("datetime_partition_column", optional=True): t.Or(t.String, t.Null),
            t.Key("otv_validation_start_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("otv_validation_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("otv_training_end_date", optional=True): t.Or(DateTime(), t.Null),
            t.Key("otv_latest_timestamp", optional=True): t.Or(DateTime(), t.Null),
            t.Key("otv_earliest_timestamp", optional=True): t.Or(DateTime(), t.Null),
            t.Key("otv_validation_downsampling_pct", optional=True): t.Or(t.Float, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        order_by_columns: List[str],
        is_descending_order: bool = False,
        target_column: Optional[str] = None,
        target_class: Optional[str] = None,
        user_group_column: Optional[str] = None,
        datetime_partition_column: Optional[str] = None,
        otv_validation_start_date: Optional[datetime] = None,
        otv_validation_end_date: Optional[datetime] = None,
        otv_training_end_date: Optional[datetime] = None,
        otv_latest_timestamp: Optional[datetime] = None,
        otv_earliest_timestamp: Optional[datetime] = None,
        otv_validation_downsampling_pct: Optional[float] = None,
    ):
        self.order_by_columns = order_by_columns
        self.is_descending_order = is_descending_order
        self.target_column = target_column
        self.target_class = target_class
        self.user_group_column = user_group_column
        self.datetime_partition_column = datetime_partition_column
        self.otv_validation_start_date = otv_validation_start_date
        self.otv_validation_end_date = otv_validation_end_date
        self.otv_training_end_date = otv_training_end_date
        self.otv_latest_timestamp = otv_latest_timestamp
        self.otv_earliest_timestamp = otv_earliest_timestamp
        self.otv_validation_downsampling_pct = otv_validation_downsampling_pct


class FeaturesChunkDefinition(APIObject):
    """The features chunk information."""

    _converter = t.Dict({}).allow_extra("*")

    def __init__(self) -> None:
        pass


class ChunkDefinitionStats(APIObject):
    """
    The chunk stats information.

    Attributes
    ----------
    expected_chunk_size: int
        The expected chunk size, this field is auto generated.
    number_of_rows_per_chunk: int
        The number of rows per chunk, this field is auto generated.
    total_number_of_chunks: int
        The total number of chunks, this field is auto generated.
    """

    _converter = t.Dict(
        {
            t.Key("expected_chunk_size"): t.Int,
            t.Key("number_of_rows_per_chunk"): t.Int,
            t.Key("total_number_of_chunks"): t.Int,
        }
    ).allow_extra("*")

    def __init__(
        self,
        expected_chunk_size: int,
        number_of_rows_per_chunk: int,
        total_number_of_chunks: int,
    ):
        self.expected_chunk_size = expected_chunk_size
        self.number_of_rows_per_chunk = number_of_rows_per_chunk
        self.total_number_of_chunks = total_number_of_chunks


class ChunkDefinition(APIObject):
    """
    The chunk information.

    Attributes
    ----------
    id : str
        The ID of the chunk entity.
    dataset_definition_id : str
        The ID of the dataset definition.
    dataset_definition_info_version: int
        The version of the dataset definition information.
    name : str
        The name of the chunk entity.
    is_readonly : bool
        The read only flag.
    partition_method : str
        The partition method used to create chunks, either 'random', 'stratified', or 'date'.
    chunking_strategy_type : str
        The chunking strategy type, either 'features' or 'rows'.
    chunk_definition_stats : ChunkDefinitionStats
        The chunk stats information.
    rows_chunk_definition : RowsChunkDefinition
        The rows chunk information.
    features_chunk_definition : FeaturesChunkDefinition
        The features chunk information.
    """

    _path = "datasetDefinitions/{}/chunkDefinitions/"
    _path_with_id = _path + "{}/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("dataset_definition_id"): t.String,
            t.Key("dataset_definition_info_version"): t.Int,
            t.Key("name"): t.String,
            t.Key("is_readonly"): t.Bool,
            t.Key("partition_method"): t.Enum(*enum_to_list(ChunkingPartitionMethod)),
            t.Key("chunking_strategy_type"): t.Enum(*enum_to_list(ChunkingStrategy)),
            t.Key("chunk_definition_stats", optional=True): ChunkDefinitionStats._converter,
            t.Key("rows_chunk_definition", optional=True): RowsChunkDefinition._converter,
            t.Key("features_chunk_definition", optional=True): FeaturesChunkDefinition._converter,
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        dataset_definition_id: str,
        dataset_definition_info_version: int,
        name: str,
        is_readonly: bool,
        partition_method: ChunkingPartitionMethod,
        chunking_strategy_type: ChunkingStrategy,
        chunk_definition_stats: Optional[ChunkDefinitionStats] = None,
        rows_chunk_definition: Optional[RowsChunkDefinition] = None,
        features_chunk_definition: Optional[FeaturesChunkDefinition] = None,
    ):
        self.id = id
        self.dataset_definition_id = dataset_definition_id
        self.dataset_definition_info_version = dataset_definition_info_version
        self.name = name
        self.is_readonly = is_readonly
        self.partition_method = partition_method
        self.chunking_strategy_type = chunking_strategy_type
        self.chunk_definition_stats = chunk_definition_stats
        self.rows_chunk_definition = rows_chunk_definition
        self.features_chunk_definition = features_chunk_definition

    @classmethod
    def from_data(cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> ChunkDefinition:
        """Properly convert composition classes."""
        converted_data = cls._converter.check(from_api(data))

        if "chunk_definition_stats" in converted_data:
            converted_data["chunk_definition_stats"] = ChunkDefinitionStats(
                **converted_data["chunk_definition_stats"]
            )

        if "rows_chunk_definition" in converted_data:
            converted_data["rows_chunk_definition"] = RowsChunkDefinition(
                **converted_data["rows_chunk_definition"]
            )

        if "features_chunk_definition" in converted_data:
            converted_data["features_chunk_definition"] = FeaturesChunkDefinition(
                **converted_data["features_chunk_definition"]
            )

        return cls(**converted_data)

    @classmethod
    def create(
        cls,
        dataset_definition_id: str,
        name: Optional[str] = None,
        partition_method: Optional[ChunkingPartitionMethod] = ChunkingPartitionMethod.RANDOM,
        chunking_strategy_type: Optional[ChunkingStrategy] = ChunkingStrategy.ROWS,
        order_by_columns: Optional[List[str]] = None,
        is_descending_order: Optional[bool] = False,
        target_column: Optional[str] = None,
        target_class: Optional[str] = None,
        user_group_column: Optional[str] = None,
        datetime_partition_column: Optional[str] = None,
        otv_validation_start_date: Optional[datetime] = None,
        otv_validation_end_date: Optional[datetime] = None,
        otv_training_end_date: Optional[datetime] = None,
    ) -> ChunkDefinition:
        """
        Create a chunk definition.

        Parameters
        ----------
        dataset_definition_id : str
            The ID of the dataset definition.
        name: str
            The optional custom name of the chunk definition.
        partition_method: str
            The partition method used to create chunks, either 'random', 'stratified', or 'date'.
        chunking_strategy_type: str
            The chunking strategy type, either 'features' or 'rows'.
        order_by_columns: List[str]
            List of the sorting column names.
        is_descending_order: bool
            The sorting order. Defaults to False, ordering from smallest to largest.
        target_column: str
            The target column.
        target_class: str
            For binary target, one of the possible values. For zero inflated, will be '0'.
        user_group_column: str
            The user group column.
        datetime_partition_column: str
            The datetime partition column name used in OTV projects.
        otv_validation_start_date: datetime.datetime
            The start date for the validation set.
        otv_validation_end_date: datetime.datetime
            The end date for the validation set.
        otv_training_end_date: datetime.datetime
            The end date for the training set.

        Returns
        -------
        chunk_definition: ChunkDefinition
            An instance of a created chunk definition.

        """
        _ = (
            name,
            order_by_columns,
            target_column,
            target_class,
            user_group_column,
            datetime_partition_column,
            otv_validation_start_date,
            otv_validation_end_date,
            otv_training_end_date,
        )

        payload = {
            "partition_method": partition_method,
            "chunking_strategy_type": chunking_strategy_type,
            "is_descending_order": is_descending_order,
        }

        optional_none_value_fields = [
            "name",
            "order_by_columns",
            "target_column",
            "target_class",
            "user_group_column",
            "datetime_partition_column",
            "otv_validation_start_date",
            "otv_validation_end_date",
            "otv_training_end_date",
        ]
        for field in optional_none_value_fields:
            value = locals().get(field)
            if value is not None:
                payload[field] = value

        path = cls._path.format(dataset_definition_id)
        response = cls._client.post(path, data=payload)
        data = response.json()
        return cls.from_server_data(data)

    @classmethod
    def get(cls, dataset_definition_id: str, chunk_definition_id: str) -> ChunkDefinition:
        """
        Retrieve a specific chunk definition metadata.

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.
        chunk_definition_id: str
            The ID of the chunk definition.

        Returns
        -------
        chunk_definition : ChunkDefinition
            The queried instance.
        """
        path = cls._path_with_id.format(dataset_definition_id, chunk_definition_id)
        response = cls._client.get(path)
        return cls.from_server_data(response.json())

    @classmethod
    def delete(cls, dataset_definition_id: str, chunk_definition_id: str) -> None:
        """
        Delete a specific chunk definition

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.
        chunk_definition_id: str
            The ID of the chunk definition.

        """
        path = cls._path_with_id.format(dataset_definition_id, chunk_definition_id)
        cls._client.delete(path)

    @classmethod
    def list(cls, dataset_definition_id: str) -> List[ChunkDefinition]:
        """
        List all chunk definitions

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.

        Returns
        -------
        A list of ChunkDefinition
        """
        path = cls._path.format(dataset_definition_id)
        data = unpaginate(path, None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def analyze(
        cls, dataset_definition_id: str, chunk_definition_id: str, max_wait: int = DEFAULT_MAX_WAIT
    ) -> None:
        """
        Analyze a specific chunk definition

        Parameters
        ----------
        dataset_definition_id: str
            The ID of the dataset definition.
        chunk_definition_id: str
            The ID of the chunk definition
        max_wait: Optional[int]
            Time in seconds after which analyze is considered unsuccessful

        """
        path = cls._path_with_id.format(dataset_definition_id, chunk_definition_id) + "analyze/"
        resp = cls._client.post(path, data={})
        if resp.status_code == 204:
            return
        elif resp.status_code == 202:
            # ignore new location since we return None
            wait_for_async_resolution(cls._client, resp.headers["Location"], max_wait)

    @classmethod
    def update(
        cls,
        chunk_definition_id: str,
        dataset_definition_id: str,
        name: Optional[str] = None,
        order_by_columns: Optional[List[str]] = None,
        is_descending_order: Optional[bool] = None,
        target_column: Optional[str] = None,
        target_class: Optional[str] = None,
        user_group_column: Optional[str] = None,
        datetime_partition_column: Optional[str] = None,
        otv_validation_start_date: Optional[datetime] = None,
        otv_validation_end_date: Optional[datetime] = None,
        otv_training_end_date: Optional[datetime] = None,
        force_update: Optional[bool] = False,
    ) -> ChunkDefinition:
        """
        Update a chunk definition.

        Parameters
        ----------
        chunk_definition_id: str
            The ID of the chunk definition.
        dataset_definition_id : str
            The ID of the dataset definition.
        name: str
            The optional custom name of the chunk definition.
        order_by_columns: List[str]
            List of the sorting column names.
        is_descending_order: bool
            The sorting order. Defaults to False, ordering from smallest to largest.
        target_column: str
            The target column.
        target_class: str
            For binary target, one of the possible values. For zero inflated, will be '0'.
        user_group_column: str
            The user group column.
        datetime_partition_column: str
            The datetime partition column name used in OTV projects.
        otv_validation_start_date: datetime.datetime
            The start date for the validation set.
        otv_validation_end_date: datetime.datetime
            The end date for the validation set.
        otv_training_end_date: datetime.datetime
            The end date for the training set.
        force_update: bool
            If True, the update will be forced in some cases. For example, update after analysis is done.

        Returns
        -------
        chunk_definition: ChunkDefinition
            An update instance of a created chunk definition.

        """
        _ = (
            name,
            order_by_columns,
            is_descending_order,
            target_column,
            target_class,
            user_group_column,
            datetime_partition_column,
            otv_validation_start_date,
            otv_validation_end_date,
            otv_training_end_date,
        )

        optional_none_value_fields = [
            "name",
            "order_by_columns",
            "is_descending_order",
            "target_column",
            "target_class",
            "user_group_column",
            "datetime_partition_column",
            "otv_validation_start_date",
            "otv_validation_end_date",
            "otv_training_end_date",
        ]
        updates = {}
        for field in optional_none_value_fields:
            value = locals().get(field)
            if value is not None:
                updates[field] = value

        payload = {
            "updates": updates,
            "operations": {
                "forceUpdate": force_update,
            },
        }

        path = cls._path_with_id.format(dataset_definition_id, chunk_definition_id)
        response = cls._client.patch(path, data=payload)
        data = response.json()
        return cls.from_server_data(data)
