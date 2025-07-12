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

from typing import Any, cast, Dict, List, Optional, Type, Union
from urllib.parse import urlencode

import trafaret as t

from datarobot.enums import (
    DataWranglingDataSourceTypes,
    DataWranglingDialect,
    DataWranglingSnapshotPolicy,
    DEFAULT_MAX_WAIT,
    enum_to_list,
    RecipeInputType,
    RecipeType,
)
from datarobot.models.api_object import APIObject
from datarobot.models.data_store import DataStore
from datarobot.models.dataset import Dataset
from datarobot.models.recipe_operation import (
    DatetimeSamplingOperation,
    DownsamplingOperation,
    RandomSamplingOperation,
    SamplingOperation,
    WranglingOperation,
)
from datarobot.models.use_cases.use_case import UseCase
from datarobot.utils import to_api
from datarobot.utils.waiters import wait_for_async_resolution


class DataSourceInput(APIObject):
    """Inputs required to create a new recipe from data store."""

    _converter = t.Dict(
        {
            t.Key("canonical_name"): t.String,
            t.Key("table"): t.String,
            t.Key("schema", optional=True): t.Or(t.String(), t.Null),
            t.Key("catalog", optional=True): t.Or(t.String(), t.Null),
            t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        canonical_name: str,
        table: str,
        schema: Optional[str] = None,
        catalog: Optional[str] = None,
        sampling: Optional[Union[RandomSamplingOperation, DatetimeSamplingOperation]] = None,
    ):
        self.canonical_name = canonical_name
        self.table = table
        self.schema = schema
        self.catalog = catalog
        self.sampling = sampling


class DatasetInput(APIObject):
    _converter = t.Dict(
        {
            t.Key("sampling"): SamplingOperation._converter,
        }
    ).allow_extra("*")

    def __init__(self, sampling: SamplingOperation):
        self.sampling = (
            SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling
        )


class RecipeDatasetInput(APIObject):
    """Object, describing inputs for recipe transformations."""

    _converter = t.Dict(
        {
            t.Key("input_type"): t.Atom(RecipeInputType.DATASET),
            t.Key("dataset_id"): t.String,
            t.Key("dataset_version_id", optional=True): t.Or(t.String, t.Null),
            t.Key("snapshot_policy", optional=True): t.Or(
                t.Enum(*enum_to_list(DataWranglingSnapshotPolicy)), t.Null
            ),
            t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
            t.Key("alias", optional=True): t.Or(t.String(), t.Null),
        }
    ).allow_extra("*")

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
        self.dataset_version_id = (
            dataset_version_id if snapshot_policy != DataWranglingSnapshotPolicy.LATEST else None
        )
        self.sampling = (
            SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling
        )
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


class JDBCTableDataSourceInput(APIObject):
    """Object, describing inputs for recipe transformations."""

    _converter = t.Dict(
        {
            t.Key("input_type"): t.Atom(RecipeInputType.DATASOURCE),
            t.Key("data_source_id"): t.String,
            t.Key("data_store_id"): t.String,
            t.Key("dataset_id", optional=True): t.Or(t.String(), t.Null),
            t.Key("sampling", optional=True): t.Or(SamplingOperation._converter, t.Null),
            t.Key("alias", optional=True): t.Or(t.String(), t.Null),
        }
    ).allow_extra("*")

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
        self.sampling = (
            SamplingOperation.from_server_data(sampling) if isinstance(sampling, dict) else sampling
        )
        self.alias = alias

    def to_api(
        self, keep_attrs: Optional[Union[List[str], List[List[str]]]] = None
    ) -> Union[str, Dict[str, Any], List[Dict[str, Any]]]:
        return to_api(self, keep_attrs=keep_attrs)


class RecipeSettings(APIObject):
    """Settings, for example to apply at downsampling stage."""

    _converter = t.Dict(
        {
            t.Key("target", optional=True): t.Or(t.String(), t.Null),
            t.Key("weights_feature", optional=True): t.Or(t.String(), t.Null),
            t.Key("prediction_point", optional=True, default=None): t.Or(t.String(), t.Null),
            t.Key("relationships_configuration_id", optional=True, default=None): t.Or(
                t.String(), t.Null
            ),
            t.Key(
                "feature_discovery_supervised_feature_reduction", optional=True, default=None
            ): t.Or(t.Bool(), t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        target: Optional[str] = None,
        weights_feature: Optional[str] = None,
        prediction_point: Optional[str] = None,
        relationships_configuration_id: Optional[str] = None,
        feature_discovery_supervised_feature_reduction: Optional[bool] = None,
    ):
        self.target = target
        self.weights_feature = weights_feature
        self.prediction_point = prediction_point
        self.relationships_configuration_id = relationships_configuration_id
        self.feature_discovery_supervised_feature_reduction = (
            feature_discovery_supervised_feature_reduction
        )


class RecipeMetadata(APIObject):
    """The recipe metadata includes the name, description, recipe type, and sql"""

    _converter = t.Dict(
        {
            t.Key("name", optional=True): t.String(),
            t.Key("description", optional=True): t.String(allow_blank=True, max_length=1000),
            t.Key("recipe_type", optional=True): t.Enum(*enum_to_list(RecipeType)),
            t.Key("sql", optional=True): t.String(allow_blank=True, max_length=64000),
        }
    )

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


class Recipe(APIObject):
    """Data wrangling entity, which contains all information needed to transform dataset and generate SQL."""

    _path = "recipes/"

    _converter = t.Dict(
        {
            t.Key("dialect"): t.String,
            t.Key("recipe_id"): t.String,
            t.Key("status"): t.String,
            t.Key("inputs"): t.List(
                t.Or(JDBCTableDataSourceInput._converter, RecipeDatasetInput._converter)
            ),
            t.Key("operations", optional=True): t.List(WranglingOperation._converter),
            t.Key("downsampling", optional=True): t.Or(DownsamplingOperation._converter, t.Null),
            t.Key("settings", optional=True): t.Or(RecipeSettings._converter, t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        dialect: DataWranglingDialect,
        recipe_id: str,
        status: str,
        inputs: List[Dict[str, Any]],
        operations: Optional[List[Dict[str, Any]]] = None,
        downsampling: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.dialect = dialect
        self.id = recipe_id
        self.status = status
        self.inputs = []
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
            [WranglingOperation.from_server_data(op) for op in operations]
            if operations is not None
            else None
        )
        self.downsampling = (
            DownsamplingOperation.from_server_data(downsampling)
            if isinstance(downsampling, dict)
            else downsampling
        )
        self.settings = (
            RecipeSettings.from_server_data(settings) if isinstance(settings, dict) else settings
        )

    @classmethod
    def update_downsampling(cls, recipe_id: str, downsampling: DownsamplingOperation) -> Recipe:
        """Set downsampling for the recipe, applied during publishing."""
        path = f"{cls._path}{recipe_id}/downsampling/"
        payload = {"downsampling": to_api(downsampling)}
        response = cls._client.put(path, json=payload)
        return Recipe.from_server_data(response.json())

    def retrieve_preview(
        self, max_wait: int = DEFAULT_MAX_WAIT, number_of_operations_to_use: Optional[int] = None
    ) -> Dict[str, Any]:
        """Retrieve preview and compute it, if absent.

        Parameters
        ----------
        max_wait: int
            The number of seconds to wait for the result.
        number_of_operations_to_use: Optional[int]
            Request preview for particular number of operations.

        Returns
        -------
        preview: dict

        """
        path = f"{self._path}{self.id}/preview/"
        payload = {}
        if number_of_operations_to_use is not None:
            payload = {"numberOfOperationsToUse": number_of_operations_to_use}
        response = self._client.post(path, json=payload)
        finished_url = wait_for_async_resolution(
            self._client, response.headers["Location"], max_wait=max_wait
        )
        r_data = self._client.get(finished_url).json()
        # TODO: create an ApiObject for Preview
        return r_data  # type: ignore[no-any-return]

    def retrieve_insights(
        self, max_wait: int = DEFAULT_MAX_WAIT, number_of_operations_to_use: Optional[int] = None
    ) -> Any:
        """Retrieve insights for the sample. When preview is requested, the insights job starts automatically.

        Parameters
        ----------
        max_wait: int
            The number of seconds to wait for the result.
        number_of_operations_to_use: Optional[int]
            Retrieves insights for the specified number of operations. First, preview computation for the same
            number of operations must be submitted.

        Returns
        -------

        """
        url = f"recipes/{self.id}/insights/"
        if number_of_operations_to_use is not None:
            query_params = {"numberOfOperationsToUse": number_of_operations_to_use}
            url = f"{url}?{urlencode(query_params)}"
        return wait_for_async_resolution(self._client, url, max_wait)

    @classmethod
    def set_inputs(
        cls, recipe_id: str, inputs: List[Union[JDBCTableDataSourceInput, RecipeDatasetInput]]
    ) -> Recipe:
        """Set inputs for the recipe."""
        path = f"{cls._path}{recipe_id}/inputs/"
        payload = {"inputs": [input_.to_api() for input_ in inputs]}
        response = cls._client.put(path, json=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def set_operations(cls, recipe_id: str, operations: List[WranglingOperation]) -> Recipe:
        """Set operations for the recipe."""
        path = f"{cls._path}{recipe_id}/operations/"
        payload = {"operations": [to_api(operation) for operation in operations]}
        response = cls._client.put(path, json=payload)
        return Recipe.from_server_data(response.json())

    @classmethod
    def set_recipe_metadata(cls, recipe_id: str, metadata: Dict[str, str]) -> Recipe:
        """
        Update metadata for the recipe.

        Parameters
        ----------
        recipe_id: str
            Recipe ID.
        metadata: Dict[str, str]
            Dictionary of metadata to be updated.

        Returns
        -------
        recipe: Recipe
            New recipe with updated metadata.
        """
        RecipeMetadata._converter.check(metadata)
        path = f"{cls._path}{recipe_id}/"
        response = cls._client.patch(path, json=metadata)
        return Recipe.from_server_data(response.json())

    @classmethod
    def get(cls, recipe_id: str) -> Recipe:
        path = f"{cls._path}{recipe_id}/"
        return cls.from_location(path)

    def get_sql(self, operations: Optional[List[WranglingOperation]] = None) -> str:
        """Generate sql for the given recipe in a transient way, recipe is not modified.
        if operations is None, recipe operations are used to generate sql.
        if operations = [], recipe operations are ignored during sql generation.
        if operations is not empty list, generate sql for them.
        """
        path = f"{self._path}{self.id}/sql/"
        payload = {
            "operations": (
                [to_api(operation) for operation in operations] if operations else operations
            )
        }
        response = self._client.post(path, data=payload)
        return response.json()["sql"]  # type: ignore[no-any-return]

    @classmethod
    def from_data_store(
        cls,
        use_case: UseCase,
        data_store: DataStore,
        data_source_type: DataWranglingDataSourceTypes,
        dialect: DataWranglingDialect,
        data_source_inputs: List[DataSourceInput],
        recipe_type: Optional[RecipeType] = RecipeType.WRANGLING,
    ) -> Recipe:
        """Create a wrangling recipe from data store."""
        payload = {
            "use_case_id": use_case.id,
            "data_store_id": data_store.id,
            "data_source_type": data_source_type,
            "dialect": dialect,
            "inputs": [to_api(input_) for input_ in data_source_inputs],
            "recipe_type": recipe_type,
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
        recipe_type: Optional[RecipeType] = RecipeType.WRANGLING,
        snapshot_policy: Optional[DataWranglingSnapshotPolicy] = DataWranglingSnapshotPolicy.LATEST,
    ) -> Recipe:
        """Create a wrangling recipe from dataset."""

        payload = {
            "use_case_id": use_case.id,
            "dataset_id": dataset.id,
            "dataset_version_id": (
                None
                if snapshot_policy == DataWranglingSnapshotPolicy.LATEST
                else dataset.version_id
            ),
            "dialect": dialect,
            "inputs": [to_api(input) for input in inputs] if inputs else None,
            "recipe_type": recipe_type,
            "snapshot_policy": snapshot_policy,
        }
        path = f"{cls._path}fromDataset/"
        response = cls._client.post(path, data=payload)
        return Recipe.from_server_data(response.json())
