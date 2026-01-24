#
# Copyright 2023-2025 DataRobot, Inc. and its affiliates.
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

from typing import Any, Dict, List, Optional, Type, Union, cast
from urllib.parse import urlencode

import pandas as pd
import trafaret as t

from datarobot.enums import (
    DEFAULT_MAX_WAIT,
    DataWranglingDataSourceTypes,
    DataWranglingDialect,
    DataWranglingSnapshotPolicy,
    RecipeInputType,
    RecipeType,
    SparkInstanceSizes,
    enum_to_list,
)
from datarobot.models.api_object import APIObject
from datarobot.models.credential import Credential
from datarobot.models.data_store import DataStore
from datarobot.models.dataset import Dataset, MaterializationDestination
from datarobot.models.recipe_operation import (
    DownsamplingOperation,
    SamplingOperation,
    WranglingOperation,
)
from datarobot.models.use_cases.use_case import UseCase
from datarobot.models.user_blueprints.models import HumanReadable
from datarobot.utils import to_api
from datarobot.utils.deprecation import deprecated, deprecation_warning
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution


class DataSourceInput(APIObject):
    """
    Data source input configuration used to create a new recipe from a data store.

    Parameters
    ----------
    canonical_name:
        The unique name of the data source.
    table:
        Table or view name in the data store.
    schema:
        Schema associated with the table or view in the data store.
    catalog:
        Catalog name in the data source, if supported.
    sampling: SamplingOperation
        Sampling operation to apply to the data source input. This determines how much data is used from the data source
        for generating a data preview of the recipe. If specifying multiple data source inputs, only provide sampling
        for the first data source input.

    Examples
    --------
    Note: Canonical name must be unique to avoid collisions when creating a recipe from a data store. Append a unique
    identifier if necessary.

    .. code-block:: python

        >>> from datarobot.models.recipe import DataSourceInput
        >>> from datarobot.models.recipe_operation import RandomSamplingOperation
        >>> from datetime import datetime
        >>> now = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
        >>> input_config = DataSourceInput(
        ...     canonical_name=f'Snowflake connection stock_prices_{now}',
        ...     table='stock_prices',
        ...     schema='PUBLIC',
        ...     sampling=RandomSamplingOperation(rows=500)
        ... )
    """

    _converter = t.Dict({
        t.Key("canonical_name"): t.String,
        t.Key("table"): t.String,
        t.Key("schema", optional=True): t.Or(t.String(), t.Null),
        t.Key("catalog", optional=True): t.Or(t.String(), t.Null),
        t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
    }).allow_extra("*")

    def __init__(
        self,
        canonical_name: str,
        table: str,
        schema: Optional[str] = None,
        catalog: Optional[str] = None,
        sampling: Optional[SamplingOperation] = None,
    ):
        self.canonical_name = canonical_name
        self.table = table
        self.schema = schema
        self.catalog = catalog
        self.sampling = sampling


class DatasetInput(APIObject):
    """
    Wrapper for dataset input configuration passed when creating a new recipe from dataset.

    deprecated:: 3.10
        This class is deprecated and may be removed in 3.12 or later. Use the `sampling` parameter of
        :meth:`Recipe.from_dataset` instead.

    Parameters
    ----------
    sampling: SamplingOperation
        Sampling operation to apply to the dataset input.

    Examples
    --------
    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe import DatasetInput
        >>> from datarobot.models.recipe_operation import LimitSamplingOperation
        >>> from datarobot.enums import DataWranglingDialect, RecipeType
        >>> my_use_case = dr.UseCase.list(search_params={"search": "My Use Case"})[0]
        >>> dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f123')
        >>> input_config = DatasetInput(
        ...     sampling=LimitSamplingOperation(rows=250)
        ... )
        >>> recipe = dr.Recipe.from_dataset(
        ...     use_case=my_use_case,
        ...     dataset=dataset,
        ...     dialect=DataWranglingDialect.SPARK,
        ...     recipe_type=RecipeType.SQL,
        ...     inputs=[input_config]
        ... )

    """

    _converter = t.Dict({
        t.Key("sampling"): SamplingOperation._converter,
    }).allow_extra("*")

    def __init__(self, sampling: SamplingOperation):
        self.sampling = SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling


class RecipeDatasetInput(APIObject):
    """
    Dataset input configuration used to specify a dataset as an input to a recipe.

    Parameters
    ----------
    input_type:
        The type of the recipe input. Must be `RecipeInputType.DATASET`.
    dataset_id:
        Id of the dataset to use as an input.
    dataset_version_id:
        Id of the dataset version to use as an input, if the snapshot policy is not set to latest.
    snapshot_policy:
        The snapshot policy to use when selecting the dataset version.
    sampling:
        Sampling operation to apply to the dataset input. This determines how much data is used from the
        dataset when generating a data preview of the recipe. Only required if this dataset is the primary input.
    alias:
        Alias for the dataset input. Useful when crafting SQL statements used in transformations.

    Examples
    --------
    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe import RecipeDatasetInput
        >>> from datarobot.enums import RecipeInputType, DataWranglingSnapshotPolicy
        >>> from datarobot.models.recipe_operation import LimitSamplingOperation
        >>> input_dataset = RecipeDatasetInput(
        ...     input_type=RecipeInputType.DATASET,
        ...     dataset_id='5f43a1b2c9e77f0001e6f123',
        ...     snapshot_policy=DataWranglingSnapshotPolicy.LATEST,
        ...     sampling=LimitSamplingOperation(rows=250)
        ... )

    Create a :class:`RecipeDatasetInput <datarobot.models.recipe.RecipeDatasetInput>` from a
    :class:`Dataset <datarobot.models.dataset.Dataset>`.

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe import RecipeDatasetInput
        >>> from datarobot.models.recipe_operation import LimitSamplingOperation
        >>> dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f123')
        >>> input_dataset = RecipeDatasetInput.from_dataset(
        ...     dataset=dataset,
        ...     sampling=LimitSamplingOperation(rows=250),
        ...     alias='my_dataset'
        ... )
    """

    _converter = t.Dict({
        t.Key("input_type"): t.Atom(RecipeInputType.DATASET),
        t.Key("dataset_id"): t.String,
        t.Key("dataset_version_id", optional=True): t.Or(t.String, t.Null),
        t.Key("snapshot_policy", optional=True): t.Or(t.Enum(*enum_to_list(DataWranglingSnapshotPolicy)), t.Null),
        t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
        t.Key("alias", optional=True): t.Or(t.String(), t.Null),
    }).allow_extra("*")

    def __init__(
        self,
        input_type: RecipeInputType,
        dataset_id: str,
        dataset_version_id: Optional[str] = None,
        snapshot_policy: Optional[DataWranglingSnapshotPolicy] = DataWranglingSnapshotPolicy.LATEST,
        sampling: Optional[Union[SamplingOperation, Dict[str, Any]]] = None,
        alias: Optional[str] = None,
    ):
        self.input_type = input_type
        self.dataset_id = dataset_id
        self.snapshot_policy = snapshot_policy
        self.dataset_version_id = dataset_version_id if snapshot_policy != DataWranglingSnapshotPolicy.LATEST else None
        self.sampling = SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling
        self.alias = alias

    def to_api(
        self, keep_attrs: Optional[Union[List[str], List[List[str]]]] = None
    ) -> Union[str, Dict[str, Any], List[Dict[str, Any]]]:
        res = cast(Dict[str, Any], to_api(self, keep_attrs=keep_attrs))
        if self.snapshot_policy == DataWranglingSnapshotPolicy.LATEST:
            res["datasetVersionId"] = None
        # make sure we sent string and not enum
        if not isinstance(res["snapshotPolicy"], str):
            res["snapshotPolicy"] = str(res["snapshotPolicy"])
        return res

    @classmethod
    def from_dataset(
        cls,
        dataset: Dataset,
        snapshot_policy: Optional[DataWranglingSnapshotPolicy] = DataWranglingSnapshotPolicy.LATEST,
        sampling: Optional[SamplingOperation] = None,
        alias: Optional[str] = None,
    ) -> RecipeDatasetInput:
        """
        Create :class:`RecipeDatasetInput <datarobot.models.recipe.RecipeDatasetInput>` configuration for a
        :class:`Dataset <datarobot.models.dataset.Dataset>`.

        Parameters
        ----------
        dataset:
            Dataset to create RecipeDatasetInput from.
        snapshot_policy:
            Snapshot policy to use when selecting the dataset version.
        sampling:
            Sampling operation to apply to the input dataset. This determines how much data is used from the dataset
            when generating a data preview of the recipe. Only required if this dataset is the primary input.
        alias:
            Alias for the dataset input. Useful when crafting SQL statements used in transformations.

        Returns
        -------
        :class:`RecipeDatasetInput <datarobot.models.recipe.RecipeDatasetInput>`
            The recipe dataset input created.
        """
        return cls(
            input_type=RecipeInputType.DATASET,
            dataset_id=dataset.id,
            dataset_version_id=dataset.version_id,
            snapshot_policy=snapshot_policy,
            sampling=sampling,
            alias=alias,
        )


class JDBCTableDataSourceInput(APIObject):
    """
    JDBC data source input configuration used to specify a table from a JDBC data source as an input to a recipe.

    Parameters
    ----------
    input_type:
        The type of the input. Must be `RecipeInputType.DATASOURCE`.
    data_source_id:
        Id of the JDBC data source.
    data_store_id:
        Id of the data store the data source connects to.
    dataset_id:
        The ID of the dataset created from the data source.
    sampling:
        Sampling operation to apply to the input dataset. This determines how much data is used from the
        dataset when generating a data preview of the recipe. Only required if this dataset is the primary input.
    alias:
        Alias for the JDBC data source input. Useful when crafting SQL statements used in transformations.

    Examples
    --------
    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.models.recipe import JDBCTableDataSourceInput
        >>> from datarobot.enums import RecipeInputType
        >>> from datarobot.models.recipe_operation import LimitSamplingOperation
        >>> data_store = dr.DataStore.list(name="Snowflake Connection")[0]
        >>> data_source = DataSource.create(
        ...     data_source_type="jdbc",
        ...     canonical_name="My Snowflake connection",
        ...     params=dr.DataSourceParameters(
        ...         data_store_id=data_store.id,
        ...         schema="PUBLIC",
        ...         table="stock_prices",
        ...     )
        ... )
        >>> dataset = data_source.create_dataset(do_snapshot=True)
        >>> input = JDBCTableDataSourceInput(
        ...     input_type=RecipeInputType.DATASOURCE,
        ...     data_source_id=data_source.id,
        ...     data_store_id=data_store.id,
        ...     dataset_id=dataset.id,
        ...     sampling=LimitSamplingOperation(rows=250),
        ...     alias='my_table_alias'
        ... )
        >>> recipe = dr.Recipe.get('690e0ee89676e54e365b32e5')
        >>> recipe.update(inputs=[input])
    """

    _converter = t.Dict({
        t.Key("input_type"): t.Atom(RecipeInputType.DATASOURCE),
        t.Key("data_source_id"): t.String,
        t.Key("data_store_id"): t.String,
        t.Key("dataset_id", optional=True): t.Or(t.String(), t.Null),
        t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
        t.Key("alias", optional=True): t.Or(t.String(), t.Null),
    }).allow_extra("*")

    def __init__(
        self,
        input_type: RecipeInputType,
        data_source_id: str,
        data_store_id: str,
        dataset_id: Optional[str] = None,
        sampling: Optional[Union[SamplingOperation, Dict[str, Any]]] = None,
        alias: Optional[str] = None,
    ):
        self.input_type = input_type
        self.data_source_id = data_source_id
        self.data_store_id = data_store_id
        self.dataset_id = dataset_id
        self.sampling = SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling
        self.alias = alias

    def to_api(
        self, keep_attrs: Optional[Union[List[str], List[List[str]]]] = None
    ) -> Union[str, Dict[str, Any], List[Dict[str, Any]]]:
        return to_api(self, keep_attrs=keep_attrs)


class RecipeSettings(APIObject):
    """
    Recipe settings for optional parameters that can be set to support or modify other recipe features or interactions.
    E.g. Using some downsampling strategies require `target` and `weights_feature` to be set.

    Parameters
    ----------
    target:
        The feature to use as the target at the modeling stage.
    weights_feature:
        The feature denoting weights.
    prediction_point:
        The date column to be used as the prediction point for time-based feature engineering.
    relationships_configuration_id:
        Deprecated:: 3.10. `relationships_configuration_id` is deprecated and has no effect. Will be removed in 3.12 or
        later.
    feature_discovery_supervised_feature_reduction:
        Whether to run supervised feature reduction for feature discovery.
    spark_instance_size:
        The Spark instance size to use, if applicable.
    """

    _converter = t.Dict({
        t.Key("target", optional=True): t.Or(t.String(), t.Null),
        t.Key("weights_feature", optional=True): t.Or(t.String(), t.Null),
        t.Key("prediction_point", optional=True, default=None): t.Or(t.String(), t.Null),
        t.Key("relationships_configuration_id", optional=True, default=None): t.Or(t.String(), t.Null),
        t.Key("feature_discovery_supervised_feature_reduction", optional=True, default=None): t.Or(t.Bool(), t.Null),
        t.Key("spark_instance_size", optional=True, default=None): t.Or(
            t.Enum(*enum_to_list(SparkInstanceSizes)), t.Null
        ),
    }).allow_extra("*")

    def __init__(
        self,
        target: Optional[str] = None,
        weights_feature: Optional[str] = None,
        prediction_point: Optional[str] = None,
        relationships_configuration_id: Optional[str] = None,
        feature_discovery_supervised_feature_reduction: Optional[bool] = None,
        spark_instance_size: Optional[SparkInstanceSizes] = None,
    ):
        self.target = target
        self.weights_feature = weights_feature
        self.prediction_point = prediction_point
        self.relationships_configuration_id = relationships_configuration_id
        self.feature_discovery_supervised_feature_reduction = feature_discovery_supervised_feature_reduction
        self.spark_instance_size = spark_instance_size


class RecipeMetadata(APIObject):
    """
    Recipe metadata for metadata fields that can be set on a recipe, e.g. name, description, etc.

    Attributes
    ----------
    name: Optional[str]
        The name of the recipe.
    description: Optional[str]
        The description of the recipe.
    recipe_type: Optional[RecipeType]
        The type of the recipe.
    sql: Optional[str]
        The SQL query of the transformation that the recipe performs.
    """

    _converter = t.Dict({
        t.Key("name", optional=True): t.String(),
        t.Key("description", optional=True): t.String(allow_blank=True, max_length=1000),
        t.Key("recipe_type", optional=True): t.Enum(*enum_to_list(RecipeType)),
        t.Key("sql", optional=True): t.String(allow_blank=True, max_length=64000),
    })

    def __init__(
        self,
        name: Optional[str],
        description: Optional[str],
        recipe_type: Optional[RecipeType],
        sql: Optional[str],
    ):
        self.name = name
        self.description = description
        self.recipe_type = recipe_type
        self.sql = sql


class Recipe(APIObject, HumanReadable):
    """
    Data wrangling entity containing information required to transform one or more datasets and generate SQL.

    A recipe acts like a blueprint for creating a dataset by applying a series of operations (filters,
    aggregations, etc.) to one or more input datasets or datasources.

    Attributes
    ----------
    id: str
        The unique identifier of the recipe.
    name: str
        The name of the recipe. Not unique.
    status: str
        The status of the recipe.
    dialect: :class:`DataWranglingDialect <datarobot.enums.DataWranglingDialect>`
        The dialect of the recipe.
    recipe_type: :class:`RecipeType <datarobot.enums.RecipeType>`
        The type of the recipe.
    inputs: List[Union[JDBCTableDataSourceInput, RecipeDatasetInput]]
        The list of inputs for the recipe. Each input can be either a
        :class:`JDBCTableDataSourceInput <datarobot.models.recipe.JDBCTableDataSourceInput>` or a
        :class:`RecipeDatasetInput <datarobot.models.recipe.RecipeDatasetInput>`. The first input is the primary input.
        All other secondary inputs must be joined or otherwise combined with the primary input to appear in the recipe
        data preview and published dataset.
    operations: Optional[List[WranglingOperation]]
        The list of operations for the recipe.
    downsampling: Optional[DownsamplingOperation]
        The downsampling operation applied to the recipe. Used when publishing the recipe to a dataset.
    settings: Optional[RecipeSettings]
        The settings for the recipe.

    Examples
    --------
    Create a recipe from a dataset or data source,

    .. code-block:: python

        >>> import datarobot as dr
        >>> from datarobot.enums import DataWranglingDialect, RecipeType
        >>> from datarobot.models.recipe_operation import RandomSamplingOperation
        >>> my_use_case = dr.UseCase.list(search_params={"search": "My Use Case"})[0]
        >>> dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f123')
        >>> recipe = dr.Recipe.from_dataset(
        ...     use_case=my_use_case,
        ...     dataset=dataset,
        ...     dialect=DataWranglingDialect.SPARK,
        ...     recipe_type=RecipeType.WRANGLING,
        ...     sampling=RandomSamplingOperation(rows=500)
        ... )

    or use an existing recipe.

    .. code-block:: python

        >>> recipe = dr.Recipe.list(search="My Recipe")[0]
        >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')

    Adjust the recipe's name, description or other metadata fields.

    .. code-block:: python

        >>> recipe.update(
        ...     name='My updated recipe name',
        ...     description='Updated description for my recipe'
        ... )

    Then add additional datasets or data sources as inputs into the recipe.

    .. code-block:: python

        >>> from datarobot.models.recipe import RecipeDatasetInput
        >>> my_other_dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f456')
        >>> recipe.update(
        ...     inputs=[
        ...         recipe.inputs[0],
        ...         RecipeDatasetInput.from_dataset(
        ...             dataset=my_other_dataset,
        ...             alias='dataset_B'
        ...         )
        ...     ]
        ... )

    Apply wrangling operations to the recipe to join, filter, aggregate, or transform the recipe's data,

    .. code-block:: python

        >>> from datarobot.models.recipe_operation import JoinOperation, FilterOperation, FilterCondition
        >>> from datarobot.enums import JoinType, FilterOperationFunctions
        >>> join_op = JoinOperation.join_dataset(
        ...     dataset=my_other_dataset,
        ...     join_type=JoinType.INNER,
        ...     right_prefix='B_',
        ...     left_keys=['id'],
        ...     right_keys=['id']
        ... )
        >>> filter_op = FilterOperation(
        ...     conditions=[
        ...         FilterCondition(
        ...             column='B_value',
        ...             function=FilterOperationFunctions.GREATER_THAN,
        ...             function_arguments=[100]
        ...         )
        ...     ]
        ... )
        >>> recipe.update(operations=[join_op, filter_op])

    or manually set the SQL for the recipe if you prefer to write your own SQL transformations:

    .. code-block:: python

        >>> recipe.update(sql=(
        ...     "SELECT A.*, B.value AS B_value FROM dataset_A AS A "
        ...     "INNER JOIN dataset_B AS B ON A.id = B.id "
        ...     "WHERE B.value > 100"
        ... ))

    Then review the data preview generated for the recipe.

    .. code-block:: python

        >>> preview = recipe.get_preview()
        >>> preview.df

    Finally, publish the recipe to create a new dataset.

    .. code-block:: python

        >>> published_dataset = recipe.publish_to_dataset(
        ...     name='My new Dataset built from recipe',
        ...     do_snapshot=True,
        ...     use_cases=my_use_case,
        ...     max_wait=600
        ... )
    """

    _path = "recipes/"

    _converter = t.Dict({
        t.Key("dialect"): t.String,
        t.Key("recipe_id"): t.String,
        t.Key("name"): t.String,
        t.Key("status"): t.String,
        t.Key("recipe_type", optional=True, default=RecipeType.WRANGLING): t.Enum(*enum_to_list(RecipeType)),
        t.Key("inputs"): t.List(t.Or(JDBCTableDataSourceInput._converter, RecipeDatasetInput._converter)),
        t.Key("operations", optional=True): t.List(WranglingOperation._converter),
        t.Key("downsampling", optional=True): t.Or(DownsamplingOperation._converter, t.Null),
        t.Key("settings", optional=True): t.Or(RecipeSettings._converter, t.Null),
    }).allow_extra("*")

    def __init__(
        self,
        dialect: DataWranglingDialect,
        recipe_id: str,
        name: str,
        status: str,
        inputs: List[Dict[str, Any]],
        recipe_type: RecipeType = RecipeType.WRANGLING,
        operations: Optional[List[Dict[str, Any]]] = None,
        downsampling: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.dialect = dialect
        self.id = recipe_id
        self.name = name
        self.status = status
        self.recipe_type = recipe_type
        self.inputs: List[Union[RecipeDatasetInput, JDBCTableDataSourceInput]] = []
        for input in inputs:
            input_clz: Union[Type[JDBCTableDataSourceInput], Type[RecipeDatasetInput]]
            if input["input_type"] == RecipeInputType.DATASOURCE:
                input_clz = JDBCTableDataSourceInput
            elif input["input_type"] == RecipeInputType.DATASET:
                input_clz = RecipeDatasetInput
            else:
                raise RuntimeError("unknown input_type")
            self.inputs.append(input_clz.from_server_data(input))
        self.operations = (
            [WranglingOperation.from_server_data(op) for op in operations] if operations is not None else None
        )
        self.downsampling = (
            DownsamplingOperation.from_server_data(downsampling) if isinstance(downsampling, dict) else downsampling
        )
        self.settings = RecipeSettings.from_server_data(settings) if isinstance(settings, dict) else settings

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        sql: Optional[str] = None,
        recipe_type: Optional[RecipeType] = None,
        inputs: Optional[List[JDBCTableDataSourceInput | RecipeDatasetInput]] = None,
        operations: Optional[List[WranglingOperation]] = None,
        settings: Optional[RecipeSettings] = None,
        **kwargs: Any,
    ) -> None:
        """Update the recipe.

        Parameters
        ----------
        name:
            The new recipe name.
        description:
            The new recipe description.
        sql:
            The new wrangling sql. Only applicable for the SQL recipe_type.
        recipe_type:
            The new type of the recipe. Only switching between SQL and WRANGLING is applicable.
        inputs:
            The new list of recipe inputs. You can update sampling and/or aliases using this parameter. Only specify
            sampling on the primary input (the first input in the list).
        operations:
            The new list of operations. Only applicable for the WRANGLING recipe_type.
        settings:
            The new recipe settings.

        Other Parameters
        ----------------
        downsampling: Optional[DownsamplingOperation]
            The new downsampling or None if you wouldn't like to apply any downsampling on publishing.

        Examples
        --------
        Update recipe metadata fields name and description:

        .. code-block:: python

            >>> import datarobot as dr
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> recipe.update(
            ...     name='My updated recipe name',
            ...     description='Updated description for my recipe'
            ... )

        Update recipe inputs to include 2 datasets to allow for joining data:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe import RecipeDatasetInput
            >>> from datarobot.models.recipe_operation import RandomSamplingOperation
            >>> primary_dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f123')
            >>> secondary_dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f456')
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> recipe.update(
            ...     inputs=[
            ...         RecipeDatasetInput.from_dataset(
            ...             dataset=primary_dataset,
            ...             sampling=RandomSamplingOperation(rows=500),
            ...             alias='dataset_A'
            ...         ),
            ...         RecipeDatasetInput.from_dataset(
            ...             dataset=secondary_dataset,
            ...             alias='dataset_B'
            ...         )
            ...     ]
            ... )

        Update recipe operations to filter out users younger than 18 years old:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe_operation import FilterOperation, FilterCondition
            >>> from datarobot.enums import FilterOperationFunctions
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> filter_op = FilterOperation(
            ...     conditions=[
            ...         FilterCondition(
            ...             column='age',
            ...             function=FilterOperationFunctions.GREATER_THAN_OR_EQUAL,
            ...             function_arguments=[18]
            ...         )
            ...     ]
            ... )
            >>> recipe.update(operations=[filter_op])

        Update recipe settings to change the column used for feature weights:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe import RecipeSettings
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> recipe.update(
            ...     settings=RecipeSettings(
            ...         weights_feature='observation_weights'
            ...     )
            ... )

        Update downsampling to only keep 500 random rows when publishing:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe_operation import RandomDownsamplingOperation
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> recipe.update(
            ...     downsampling=RandomDownsamplingOperation(max_rows=500)
            ... )

        Notes
        -----
        Setting the `sql` metadata field on a non-SQL type recipe will convert the recipe to a SQL type recipe.
        """
        new_recipe = None
        if inputs is not None:
            new_recipe = self.set_inputs(self.id, inputs=inputs)

        if operations is not None:
            new_recipe = self.set_operations(self.id, operations=operations)

        if settings is not None:
            new_recipe = self.set_settings(self.id, settings=settings)

        if "downsampling" in kwargs:
            downsampling = kwargs.pop("downsampling")
            if not (isinstance(downsampling, DownsamplingOperation) or downsampling is None):
                raise TypeError("downsampling must be a DownsamplingOperation instance or None")
            new_recipe = self.update_downsampling(self.id, downsampling=downsampling)

        # Consider all remaining additional fields as metadata fields
        kwargs.update({'name': name, 'description': description, 'sql': sql, 'recipe_type': recipe_type})
        metadata_fields = {k: v for k, v in kwargs.items() if v is not None}
        if metadata_fields:
            new_recipe = self.set_recipe_metadata(self.id, metadata=metadata_fields)

        if new_recipe is not None:
            for field in self._fields():
                if field != 'recipe_id':
                    setattr(self, field, getattr(new_recipe, field))

        else:
            raise ValueError(
                'You must specify at least one parameter to update. '
                '*None* is invalid value for anything except downsampling.'
            )

    def get_preview(
        self, max_wait: int = DEFAULT_MAX_WAIT, number_of_operations_to_use: Optional[int] = None
    ) -> RecipePreview:
        """
        Retrieve preview of sample data. Compute preview if absent.

        Parameters
        ----------
        max_wait: int
            Maximum number of seconds to wait when retrieving the preview.
        number_of_operations_to_use: Optional[int]
            Number of operations to use when computing the preview. If provided, the first N operations will be used.
            If not provided, all operations will be used.

        Returns
        -------
        preview: RecipePreview
            The preview of the application of the recipe.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> preview = recipe.get_preview()
            >>> preview
            RecipePreview(
                columns=['feature_1', 'feature_2', 'feature_3'],
                count=4,
                data=[['5', 'true', 'James'], ['-7', 'false', 'Bryan'], ['2', 'false', 'Jamie'], ['4', 'true', 'Lyra']],
                total_count=4,
                byte_size=46,
                result_schema=[
                    {'data_type': 'INT_TYPE', 'name': 'feature_1'},
                    {'data_type': 'BOOLEAN_TYPE', 'name': 'feature_2'},
                    {'data_type': 'STRING_TYPE', 'name': 'feature_3'}
                ],
                stored_count=4,
                estimated_size_exceeds_limit=False,
            )
            >>> preview.df
              feature_1 feature_2 feature_3
            0         5      true     James
            1        -7     false     Bryan
            2         2     false     Jamie
            3         4      true      Lyra
        """
        data = self._retrieve_preview(max_wait=max_wait, number_of_operations_to_use=number_of_operations_to_use)
        return RecipePreview.from_server_data(data)

    def publish_to_dataset(
        self,
        name: Optional[str] = None,
        do_snapshot: Optional[bool] = None,
        persist_data_after_ingestion: Optional[bool] = None,
        categories: Optional[List[str]] = None,
        credential: Optional[Credential] = None,
        credential_id: Optional[str] = None,
        use_kerberos: Optional[bool] = None,
        materialization_destination: Optional[MaterializationDestination] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
        use_cases: Optional[Union[List[UseCase], UseCase, List[str], str]] = None,
    ) -> Dataset:
        """
        A blocking call to publish the recipe to a new :class:`Dataset <datarobot.models.dataset.Dataset>`.

        Parameters
        ----------
        name:
            The name for the new dataset.
        do_snapshot:
            If true, create a snapshot dataset.
        persist_data_after_ingestion:
            If true, will enforce saving all data for download and sampling.
        categories:
            A list of strings describing the intended use of the dataset.
        credential:
            The credential to use to authenticate with the database, if required.
        credential_id:
            The ID of the set of credentials to use to authenticate with the database, if required.
        use_kerberos:
            If true, use kerberos authentication for database authentication.
        materialization_destination:
            Destination table information to create and materialize the recipe to. If None, the recipe will be
            materialized in DataRobot.
        max_wait:
            Number of seconds to wait for the dataset to be created.
        use_cases:
            One or more use cases to which the published dataset will be added. Can pass
            :class:`UseCase <datarobot.models.use_cases.use_case.UseCase>` instances or use case IDs.

        Returns
        -------
        dataset: :class:`Dataset <datarobot.models.dataset.Dataset>`
            The newly created dataset.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> dataset = recipe.publish_to_dataset(
            ...     name='Published Dataset from Recipe',
            ...     do_snapshot=True,
            ...     max_wait=600
            ... )
        """
        return Dataset.create_from_recipe(
            self,
            name=name,
            do_snapshot=do_snapshot,
            persist_data_after_ingestion=persist_data_after_ingestion,
            categories=categories,
            credential=credential,
            credential_id=credential_id,
            use_kerberos=use_kerberos,
            materialization_destination=materialization_destination,
            max_wait=max_wait,
            use_cases=use_cases,
        )

    @classmethod
    def update_downsampling(cls, recipe_id: str, downsampling: Optional[DownsamplingOperation]) -> Recipe:
        """
        Set the downsampling operation for the recipe. Downsampling is applied during publishing.
        Consider using :meth:`update() <datarobot.models.recipe.Recipe.update>` instead to update a Recipe instance.

        Parameters
        ----------
        recipe_id:
            Recipe ID.
        downsampling:
            Downsampling operation to be applied during publishing. If None, no downsampling will be applied.
        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            Recipe with updated downsampling.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe_operation import RandomDownsamplingOperation
            >>> recipe = dr.Recipe.get('690bbf77aa31530d8287ae5f')
            >>> recipe = dr.Recipe.update_downsampling(
            ...     recipe_id=recipe.id,
            ...     downsampling=RandomDownsamplingOperation(max_rows=1000)
            ... )

        See Also
        --------
        :meth:`Recipe.update <datarobot.models.recipe.Recipe.update>`
        """
        path = f"{cls._path}{recipe_id}/downsampling/"
        payload = {"downsampling": downsampling}
        response = cls._client.put(path, json=payload, keep_attrs=['downsampling'] if downsampling is None else [])
        return Recipe.from_server_data(response.json())

    @deprecated(
        deprecated_since_version="3.10",
        will_remove_version="3.12",
        message="Use `Recipe.get_preview` method instead.",
    )
    def retrieve_preview(
        self, max_wait: int = DEFAULT_MAX_WAIT, number_of_operations_to_use: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Retrieve preview of sample data. Compute preview if absent.

        .. deprecated:: 3.10
           This method is deprecated and will be removed in 3.12.
           Use :meth:`Recipe.get_preview <datarobot.models.recipe.Recipe.get_preview>` instead.

        Parameters
        ----------
        max_wait: int
            Maximum number of seconds to wait when retrieving the preview.
        number_of_operations_to_use: Optional[int]
            Number of operations to use when computing the preview. If provided, the first N operations will be used.
            If not provided, all operations will be used.

        Returns
        -------
        preview: Dict[str, Any]
            Preview data computed.

        See Also
        --------
        :meth:`Recipe.get_preview <datarobot.models.recipe.Recipe.get_preview>`
        """
        return self._retrieve_preview(max_wait=max_wait, number_of_operations_to_use=number_of_operations_to_use)

    def _retrieve_preview(
        self, max_wait: int = DEFAULT_MAX_WAIT, number_of_operations_to_use: Optional[int] = None
    ) -> Dict[str, Any]:
        path = f"{self._path}{self.id}/preview/"
        payload = {}
        if number_of_operations_to_use is not None:
            payload = {"numberOfOperationsToUse": number_of_operations_to_use}
        response = self._client.post(path, json=payload)
        finished_url = wait_for_async_resolution(self._client, response.headers["Location"], max_wait=max_wait)
        r_data = self._client.get(finished_url).json()
        return r_data  # type: ignore[no-any-return]

    def retrieve_insights(
        self, max_wait: int = DEFAULT_MAX_WAIT, number_of_operations_to_use: Optional[int] = None
    ) -> Any:
        """
        Retrieve insights for the recipe sample data. Requires a preview of sample data to be computed first
        with `.get_preview()`. Computing the preview starts the insights job in the background automatically
        if it not already running. Will block thread until insights are ready or max_wait is exceeded.

        Parameters
        ----------
        max_wait:
            Maximum number of seconds to wait when retrieving the insights.
        number_of_operations_to_use:
            Number of operations to use when computing insights. A preview must be computed first for the same number
            of operations. If provided, the first N operations will be used. If not provided, all operations will be
            used.

        Returns
        -------
        insights: Dict[str, Any]
            The insights for the recipe sample data.
        """
        url = f"recipes/{self.id}/insights/"
        if number_of_operations_to_use is not None:
            query_params = {"numberOfOperationsToUse": number_of_operations_to_use}
            url = f"{url}?{urlencode(query_params)}"
        return wait_for_async_resolution(self._client, url, max_wait)

    @classmethod
    def set_inputs(cls, recipe_id: str, inputs: List[Union[JDBCTableDataSourceInput, RecipeDatasetInput]]) -> Recipe:
        """
        Set the inputs for the recipe. Inputs can be a dataset or a JDBC data source table.
        Consider using :meth:`update() <datarobot.models.recipe.Recipe.update>` instead to update a Recipe instance.

        Parameters
        ----------
        recipe_id:
            Recipe ID.
        inputs:
            List of inputs to use in the recipe.

        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            Recipe with updated inputs.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe import RecipeDatasetInput
            >>> from datarobot.models.recipe_operation import RandomSamplingOperation
            >>> primary_dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f123')
            >>> secondary_dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f456')
            >>> recipe = dr.Recipe.set_inputs(
            ...     recipe_id='690bbf77aa31530d8287ae5f',
            ...     inputs=[
            ...         RecipeDatasetInput.from_dataset(
            ...             dataset=primary_dataset,
            ...             sampling=RandomSamplingOperation(rows=500),
            ...             alias='dataset_A'
            ...         ),
            ...         RecipeDatasetInput.from_dataset(
            ...             dataset=secondary_dataset,
            ...             alias='dataset_B'
            ...         )
            ...     ]
            ... )

        See Also
        --------
        :meth:`Recipe.update <datarobot.models.recipe.Recipe.update>`
        """
        path = f"{cls._path}{recipe_id}/inputs/"
        payload = {"inputs": inputs}
        response = cls._client.put(path, json=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def set_operations(cls, recipe_id: str, operations: List[WranglingOperation]) -> Recipe:
        """
        Set the list of operations to use in the recipe. Operations are applied in order on the input(s).
        Consider using :meth:`update() <datarobot.models.recipe.Recipe.update>` instead to update a Recipe instance.

        Parameters
        ----------
        recipe_id:
            Recipe ID.
        operations:
            List of operations to set in the recipe.

        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            Recipe with updated list of operations.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe_operation import FilterOperation, FilterCondition
            >>> from datarobot.enums import FilterOperationFunctions
            >>> recipe = dr.Recipe.get("690bbf77aa31530d8287ae5f")
            >>> new_operations = [
            ...    FilterOperation(
            ...        conditions=[
            ...            FilterCondition(
            ...                column="column_A",
            ...                function=FilterOperationFunctions.GREATER_THAN,
            ...                function_arguments=[100]
            ...            )
            ...        ]
            ...    )
            ... ]
            >>> recipe = dr.Recipe.set_operations(recipe.id, operations=new_operations)

        See Also
        --------
        :meth:`Recipe.update <datarobot.models.recipe.Recipe.update>`
        """
        path = f"{cls._path}{recipe_id}/operations/"
        payload = {"operations": operations}
        response = cls._client.put(path, json=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def set_recipe_metadata(cls, recipe_id: str, metadata: Dict[str, str]) -> Recipe:
        """
        Update metadata for a recipe. Consider using :meth:`update() <datarobot.models.recipe.Recipe.update>` instead
        to update a Recipe instance.

        Parameters
        ----------
        recipe_id:
            Recipe ID.
        metadata:
            Dictionary of metadata fields to update.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> recipe = dr.Recipe.get("690bbf77aa31530d8287ae5f")
            >>> new_metadata = {
            ...     "name": "Updated Recipe Name",
            ...     "description": "This is an updated description for the recipe."
            ... }
            >>> recipe = dr.Recipe.set_recipe_metadata(recipe.id, metadata=new_metadata)

        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            New recipe with updated metadata.

        See Also
        --------
        :meth:`Recipe.update <datarobot.models.recipe.Recipe.update>`

        Notes
        -----
        Updating the `sql` metadata field on a non-SQL type recipe will convert the recipe to a SQL type recipe.
        """
        RecipeMetadata._converter.check(metadata)
        path = f"{cls._path}{recipe_id}/"
        response = cls._client.patch(path, json=metadata)
        return Recipe.from_server_data(response.json())

    @classmethod
    def set_settings(cls, recipe_id: str, settings: RecipeSettings) -> Recipe:
        """
        Update the settings for a recipe. Consider using :meth:`update() <datarobot.models.recipe.Recipe.update>`
        instead to update a Recipe instance.

        Parameters
        ----------
        recipe_id:
            Recipe ID.
        settings:
            RecipeSettings containing the settings to be applied.

        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            Recipe with updated settings.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe_settings import RecipeSettings
            >>> recipe = dr.Recipe.get("690bbf77aa31530d8287ae5f")
            >>> new_settings = RecipeSettings(
            ...     weights_feature="feature_weights"
            ... )
            >>> recipe = dr.Recipe.set_settings(recipe.id, settings=new_settings)

        See Also
        --------
        :meth:`Recipe.update <datarobot.models.recipe.Recipe.update>`
        """
        path = f"{cls._path}{recipe_id}/settings/"
        cls._client.patch(
            path, json=settings
        )  # Response returned is the updated settings object, use .get to match existing pattern
        return cls.get(recipe_id)

    @classmethod
    def list(
        cls,
        search: Optional[str] = None,
        dialect: Optional[DataWranglingDialect] = None,
        status: Optional[str] = None,
        recipe_type: Optional[RecipeType] = None,
        order_by: Optional[str] = None,
        created_by_user_id: Optional[str] = None,
        created_by_username: Optional[str] = None,
    ) -> List[Recipe]:
        """
        List recipes. Apply filters to narrow down results.

        Parameters
        ----------
        search:
            Recipe name to filter by.
        dialect:
            Recipe dialect to filter by.
        status:
            Recipe status to filter by. E.g., draft, published.
        recipe_type:
            Recipe type to filter by.
        order_by:
            Field to order results by. For reverse ordering prefix with '-', e.g. -recipe_id.
        created_by_user_id:
            User ID to filter recipes by. Return recipes created by user(s) associated with a user ID.
        created_by_username:
            User name to filter recipes by. Return recipes created by user(s) associated with username.

        Returns
        -------
        recipes: List[Recipe]
            List of recipes matching the filter criteria.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> recipes = dr.Recipe.list()
            >>> recipes
            [Recipe(
                dialect='spark',
                id='690bbf77aa31530d8287ae5f',
                name='Sample Recipe',
                status='draft',
                recipe_type='SQL',
                inputs=[...],
                operations=[...],
                downsampling=...,
                settings=...,
            ), ...]

        See Also
        --------
        :meth:`Recipe.get <datarobot.models.recipe.Recipe.get>`
        """
        path = f"{cls._path}"

        params = {}
        if search is not None:
            params["search"] = search
        if dialect is not None:
            params["dialect"] = dialect.value
        if status is not None:
            params["status"] = status
        if recipe_type is not None:
            params["recipeType"] = recipe_type.value
        if order_by is not None:
            params["orderBy"] = order_by
        if created_by_user_id is not None:
            params["creatorUserId"] = created_by_user_id
        if created_by_username is not None:
            params["creatorUsername"] = created_by_username

        return [Recipe.from_server_data(recipe_data) for recipe_data in unpaginate(path, params, cls._client)]

    @classmethod
    def get(cls, recipe_id: str) -> Recipe:
        """
        Retrieve a recipe by ID.

        Parameters
        ----------
        recipe_id:
            The ID of the recipe to retrieve.

        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            The recipe with the specified ID.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> recipe = dr.Recipe.get("690bbf77aa31530d8287ae5f")
            >>> recipe
            Recipe(
                dialect='spark',
                id='690bbf77aa31530d8287ae5f',
                name='Sample Recipe',
                status='draft',
                recipe_type='SQL',
                inputs=[...],
                operations=[...],
                downsampling=...,
                settings=...,
            )

        See Also
        --------
        :meth:`Recipe.list <datarobot.models.recipe.Recipe.list>`
        """

        path = f"{cls._path}{recipe_id}/"
        return cls.from_location(path)

    def get_sql(self, operations: Optional[List[WranglingOperation]] = None) -> str:
        """
        Generate SQL for the recipe, taking into account its operations and inputs.
        This does not modify the recipe.

        Parameters
        ----------
        operations: Optional[List[WranglingOperation]]
            If provided, generate SQL for the given list of operations instead of the recipe's operations,
            using the recipe's inputs as the base.
            .. deprecated:: 3.10
            `operations` is deprecated and will be removed in 3.12. Use `generate_sql_for_operations` class method
            instead.

        Returns
        -------
        sql: str
            Generated SQL string.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe_operation import FilterOperation, FilterCondition
            >>> from datarobot.enums import FilterOperationFunctions
            >>> recipe = dr.Recipe.get("690bbf77aa31530d8287ae5f")
            >>> recipe.update(operations=[
            ...    FilterOperation(
            ...        conditions=[
            ...            FilterCondition(
            ...                column="column_A",
            ...                function=FilterOperationFunctions.GREATER_THAN,
            ...                function_arguments=[100]
            ...            )
            ...        ]
            ...    )
            ... ])
            >>> recipe.get_sql()
            "SELECT `sample_dataset`.`column_A` FROM `sample_dataset` WHERE `sample_dataset`.`column_A` > 100"

        See Also
        --------
        :meth:`Recipe.generate_sql_for_operations <datarobot.models.recipe.Recipe.generate_sql_for_operations>`
        """
        if operations is not None:
            deprecation_warning(
                subject="operations",
                message=(
                    "The `operations` parameter is deprecated and will be removed in 3.12. "
                    "Use `generate_sql_for_operations` class method instead."
                ),
                deprecated_since_version="3.10",
                will_remove_version="3.12",
            )
        payload = {"operations": operations}
        path = f"{self._path}{self.id}/sql/"
        response = self._client.post(path, data=payload)
        return response.json()["sql"]  # type: ignore[no-any-return]

    @classmethod
    def generate_sql_for_operations(cls, recipe_id: str, operations: List[WranglingOperation]) -> str:
        """
        Generate SQL for an arbitrary list of operations, using an existing recipe as a base. This does not modify the
        recipe. If you want to generate SQL for a recipe's operations, use `get_sql()` instead.

        Parameters
        ----------
        recipe_id:
            The ID of the recipe to use as a base. The SQL generation will use the recipe's inputs and dialect.
        operations:
            The list of operations to generate SQL for.

        Returns
        -------
        sql: str
            Generated SQL string.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.recipe_operation import FilterOperation, FilterCondition
            >>> from datarobot.enums import FilterOperationFunctions
            >>> dr.Recipe.generate_sql_for_operations(
            ...    recipe_id="690bbf77aa31530d8287ae5f",
            ...    operations=[
            ...        FilterOperation(
            ...            conditions=[
            ...                FilterCondition(
            ...                    column="column_A",
            ...                    function=FilterOperationFunctions.LESS_THAN,
            ...                    function_arguments=[20]
            ...                )
            ...            ]
            ...        )
            ...    ]
            ... )
            "SELECT `sample_dataset`.`column_A` FROM `sample_dataset` WHERE `sample_dataset`.`column_A` < 20"
        """
        path = f"{cls._path}{recipe_id}/sql/"
        payload = {"operations": operations}
        response = cls._client.post(path, data=payload)
        return response.json()["sql"]  # type: ignore[no-any-return]

    @classmethod
    def from_data_store(
        cls,
        use_case: UseCase,
        data_store: DataStore,
        data_source_type: DataWranglingDataSourceTypes,
        dialect: DataWranglingDialect,
        data_source_inputs: List[DataSourceInput],
        recipe_type: RecipeType = RecipeType.WRANGLING,
    ) -> Recipe:
        """
        Create a recipe using one or more data sources from a data store as input.

        Parameters
        ----------
        use_case:
            The use case where the recipe should be created.
        data_store:
            The data store containing the data to use as input for the recipe.
        data_source_type:
            The type of data source to use when connecting to the data store.
        dialect:
            The dialect of the recipe.
        data_source_inputs:
            List of data source inputs for the recipe. Each input will be used to create a data source. If specifying
            multiple data source inputs, the first input is used as the primary data input. Secondary data sources
            must be joined or otherwise combined with the primary data source to appear in the data preview or
            published dataset.
        recipe_type:
            The type of the recipe. Only supports sql and wrangling recipe types.

        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            The recipe created.

        Examples
        --------
        Create a wrangling recipe with 2 Snowflake tables as inputs from a data store:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.enums import DataWranglingDialect, DataWranglingDataSourceTypes, RecipeType
            >>> from datarobot.models.recipe import DataSourceInput
            >>> from datarobot.models.recipe_operation import LimitSamplingOperation
            >>> from datetime import datetime
            >>> my_use_case = dr.UseCase.list(search_params={"search": "My Use Case"})[0]
            >>> data_store = dr.DataStore.list(name="Snowflake Data Store")[0]
            >>> now = datetime.now().strftime("%Y%m%d_%H%M%S")
            >>> primary_input = DataSourceInput(
            ...     canonical_name=f"Data source for stock_trades {now}",
            ...     table="stock_trades",
            ...     schema="PUBLIC",
            ...     sampling=LimitSamplingOperation(rows=1000)
            ... )
            >>> secondary_input = DataSourceInput(
            ...     canonical_name=f"Data source for hist_stock_prices {now}",
            ...     table="hist_stock_prices",
            ...     schema="PUBLIC"
            ... )
            >>> recipe = dr.Recipe.from_data_store(
            ...     use_case=my_use_case,
            ...     data_store=data_store,
            ...     data_source_type=DataWranglingDataSourceTypes.JDBC,
            ...     dialect=DataWranglingDialect.SNOWFLAKE,
            ...     data_source_inputs=[primary_input, secondary_input],
            ...     recipe_type=RecipeType.WRANGLING
            ... )
            >>> recipe.update(name="My Snowflake wrangling recipe for stock trades and historical prices")
        """
        payload = {
            "use_case_id": use_case.id,
            "data_store_id": data_store.id,
            "data_source_type": data_source_type,
            "dialect": dialect,
            "inputs": [to_api(input_) for input_ in data_source_inputs],
            "recipe_type": recipe_type.lower(),
        }
        path = f"{cls._path}fromDataStore/"
        response = cls._client.post(path, data=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def from_dataset(
        cls,
        use_case: UseCase,
        dataset: Dataset,
        dialect: Optional[DataWranglingDialect] = None,
        inputs: Optional[List[DatasetInput]] = None,
        recipe_type: RecipeType = RecipeType.WRANGLING,
        snapshot_policy: Optional[DataWranglingSnapshotPolicy] = DataWranglingSnapshotPolicy.LATEST,
        sampling: Optional[SamplingOperation] = None,
    ) -> Recipe:
        """
        Create a recipe using a dataset as input.

        Parameters
        ----------
        use_case:
            The use case where the recipe should be created.
        dataset:
            The dataset to use as input for the recipe.
        dialect:
            The dialect of the recipe. Required for most recipe types.
        inputs:
            The configuration for the dataset input of the recipe. Currently only supports sampling configuration. Must
            be a list of length 1.

            .. deprecated:: 3.10
                This parameter is deprecated and will be removed in 3.12. Use the `sampling` parameter instead.
        recipe_type:
            The type of the recipe.
        snapshot_policy:
            The snapshot policy to use for the dataset input.
        sampling:
            The sampling configuration to use for the input dataset. This determines which rows from the dataset are
            used when generating a data preview. If not provided the full dataset will be used.

        Returns
        -------
        recipe: :class:`Recipe <datarobot.models.recipe.Recipe>`
            The recipe created.

        Examples
        --------
        Create a wrangling recipe to work with a snowflake dataset:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.enums import DataWranglingDialect, RecipeType
            >>> from datarobot.models.recipe_operation import RandomSamplingOperation
            >>> my_use_case = dr.UseCase.list(search_params={"search": "My Use Case"})[0]
            >>> dataset = dr.Dataset.get('5f43a1b2c9e77f0001e6f123')
            >>> recipe = dr.Recipe.from_dataset(
            ...     use_case=my_use_case,
            ...     dataset=dataset,
            ...     dialect=DataWranglingDialect.SNOWFLAKE,
            ...     recipe_type=RecipeType.WRANGLING,
            ...     sampling=RandomSamplingOperation(rows=200)
            ... )
            >>> recipe.update(name='My Snowflake wrangling recipe for dataset X')
        """

        if inputs is not None:
            deprecation_warning(
                subject="inputs",
                message=(
                    "The `inputs` parameter is deprecated and will be removed in 3.12. "
                    "Use the `sampling` parameter instead to pass dataset input sampling operations."
                ),
                deprecated_since_version="3.10",
                will_remove_version="3.12",
            )

        input_data = None
        if sampling is not None and inputs is not None:
            raise ValueError("You can only provide one of `sampling` or `inputs` parameters, not both.")
        elif sampling is not None:
            input_data = [{"sampling": sampling}]
        elif inputs is not None:
            input_data = [to_api(input) for input in inputs]  # type: ignore[misc]

        payload = {
            "use_case_id": use_case.id,
            "dataset_id": dataset.id,
            "dataset_version_id": (
                None if snapshot_policy == DataWranglingSnapshotPolicy.LATEST else dataset.version_id
            ),
            "dialect": dialect,
            "inputs": input_data,
            "recipe_type": recipe_type,
            "snapshot_policy": snapshot_policy,
        }
        path = f"{cls._path}fromDataset/"
        response = cls._client.post(path, data=payload)
        return Recipe.from_server_data(response.json())


class RecipePreview(APIObject, HumanReadable):
    """A preview of data output from the application of a recipe.

    Attributes
    ----------
    columns: List[str]
        List of column names in the preview.
    count: int
        Number of rows in the preview.
    data: List[List[Any]]
        The preview data as a list of rows, where each row is a list of values.
    total_count: int
        Total number of rows in the dataset.
    byte_size: int
        Data memory usage in bytes.
    result_schema: List[Dict[Any]]
        JDBC result schema for the preview data.
    stored_count: int
        Number of rows available for preview.
    estimated_size_exceeds_limit: bool
        If downsampling should be done based on sample size.
    next: Optional[RecipePreview]
        The next set of preview data, if available, otherwise None.
    previous: Optional[RecipePreview]
        The previous set of preview data, if available, otherwise None.
    df: pandas.DataFrame
        The preview data as a pandas DataFrame.
    """

    _converter = t.Dict({
        t.Key("columns"): t.List(t.String),
        t.Key("count"): t.Int,
        t.Key("data"): t.List(t.List(t.Any)),
        t.Key("total_count"): t.Int,
        t.Key("byte_size"): t.Int,
        t.Key("next", optional=True): t.String,
        t.Key("previous", optional=True): t.String,
        t.Key("result_schema"): t.List(t.Dict().allow_extra("*")),
        t.Key("stored_count"): t.Int,
        t.Key("estimated_size_exceeds_limit"): t.Bool,
    }).allow_extra("*")

    def __init__(
        self,
        columns: List[str],
        count: int,
        data: List[List[Any]],
        total_count: int,
        byte_size: int,
        result_schema: List[Dict[str, Any]],
        stored_count: int,
        estimated_size_exceeds_limit: bool,
        next: Optional[str] = None,
        previous: Optional[str] = None,
    ):
        self.columns = columns
        self.count = count
        self.data = data
        self.total_count = total_count
        self.byte_size = byte_size
        self.result_schema = result_schema
        self.stored_count = stored_count
        self.estimated_size_exceeds_limit = estimated_size_exceeds_limit
        self.__next_page_url = next
        self.__previous_page_url = previous

    @property
    def next(self) -> Optional[RecipePreview]:
        if not self.__next_page_url:
            return None
        return RecipePreview.from_server_data(self._client.get(self.__next_page_url).json())

    @property
    def previous(self) -> Optional[RecipePreview]:
        if not self.__previous_page_url:
            return None
        return RecipePreview.from_server_data(self._client.get(self.__previous_page_url).json())

    @property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame(data=self.data, columns=self.columns)
