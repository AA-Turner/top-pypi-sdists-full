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
# pylint: disable=too-many-lines
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

import dateutil
import pandas as pd
import trafaret as t

from datarobot.enums import (
    BUCKET_SIZE,
    CustomMetricAggregationType,
    CustomMetricBucketTimeStep,
    CustomMetricDirectionality,
    DEFAULT_MAX_WAIT,
    HostedCustomMetricsTemplateMetricTypeQueryParams,
    ListHostedCustomMetricTemplatesSortQueryParams,
)
from datarobot.models.api_object import APIObject
from datarobot.models.deployment.mixins import MonitoringDataQueryBuilderMixin
from datarobot.models.registry import Job
from datarobot.models.runtime_parameters import RuntimeParameterValue
from datarobot.models.types import Schedule
from datarobot.utils import from_api, to_api, underscorize
from datarobot.utils.waiters import wait_for_async_resolution

if TYPE_CHECKING:
    from mypy_extensions import TypedDict

    class BaselineValues(TypedDict, total=False):
        value: float

    class DatasetColumn(TypedDict, total=False):
        column_name: str
        time_format: Optional[str]

    class CustomMetricSegmentFromJSON(TypedDict):
        name: str
        value: str

    class CustomMetricBucket(TypedDict):
        value: float | str
        sample_size: int
        timestamp: Optional[Union[datetime, str]]
        batch: Optional[str]
        segments: List[CustomMetricSegmentFromJSON]
        association_id: Optional[str]
        geospatial_coordinate: Optional[str]
        metadata: Optional[str]

    class CustomMetricCategory(TypedDict):
        value: str
        directionality: str
        baseline_count: Optional[int]

    class MetricCategory(TypedDict):
        category_name: str
        count: int

    class CustomMetricOverSpaceBucket(TypedDict):
        value: Optional[float]
        sample_size: Optional[int]
        categories: Optional[List[MetricCategory]]
        unknown_categories_count: Optional[int]
        hexagon: str

    class CustomMetricSegmentFromDataset(TypedDict):
        name: str
        column: str

    class Geospatial(TypedDict):
        column_name: str

    class Period(TypedDict, total=False):
        start: datetime
        end: datetime

    class Summary(TypedDict, total=False):
        period: Period

    class Bucket(TypedDict):
        period: Period
        value: int
        sample_size: int

    class Batch(TypedDict, total=False):
        id: str
        name: str
        created_at: datetime
        last_prediction_timestamp: datetime

    class BatchBucket(TypedDict):
        batch: Batch
        value: int
        sample_size: int


class CustomMetric(APIObject):
    """A DataRobot custom metric.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        The ID of the custom metric.
    deployment_id: str
        The ID of the deployment.
    name: str
        The name of the custom metric.
    units: str
        The units, or the y-axis label, of the given custom metric.
    baseline_values: BaselinesValues
        The baseline value used to add "reference dots" to the values over time chart.
    is_model_specific: bool
        Determines whether the metric is related to the model or deployment.
    type: CustomMetricAggregationType
        The aggregation type of the custom metric.
    directionality: CustomMetricDirectionality
        The directionality of the custom metric.
    time_step: CustomMetricBucketTimeStep
        Custom metric time bucket size.
    description: str
        A description of the custom metric.
    association_id: DatasetColumn
        A custom metric association_id column source when reading values from columnar dataset.
    timestamp: DatasetColumn
        A custom metric timestamp column source when reading values from columnar dataset.
    value: DatasetColumn
        A custom metric value source when reading values from columnar dataset.
    sample_count: DatasetColumn
        A custom metric sample source when reading values from columnar dataset.
    batch: str
        A custom metric batch ID source when reading values from columnar dataset.
    """

    _path = "deployments/{}/customMetrics/"
    _categories = t.Dict(
        {
            t.Key("directionality"): t.String,
            t.Key("value"): t.String,
            t.Key("baseline_count", optional=True): t.Or(t.Int, t.Null),
        }
    ).allow_extra("*")
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("units"): t.String(),
            t.Key("baseline_values", optional=True): t.Or(
                t.List(t.Dict().allow_extra("*")), t.Null
            ),
            t.Key("is_model_specific"): t.Bool(),
            t.Key("type"): t.String(),
            t.Key("directionality", optional=True): t.Or(t.String(), t.Null),
            t.Key("time_step"): t.String(),
            t.Key("description", optional=True): t.Or(t.String(allow_blank=True), t.Null),
            t.Key("association_id", optional=True): t.Dict().allow_extra("*"),
            t.Key("value", optional=True): t.Dict().allow_extra("*"),
            t.Key("sample_count", optional=True): t.Dict().allow_extra("*"),
            t.Key("timestamp", optional=True): t.Dict().allow_extra("*"),
            t.Key("batch", optional=True): t.Dict().allow_extra("*"),
            t.Key("categories", optional=True): t.Or(t.List(_categories), t.Null),
            t.Key("is_geospatial", optional=True): t.Or(t.Bool(), t.Null()),
            t.Key("geospatial_segment_attribute", optional=True): t.Or(t.String(), t.Null()),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        units: str,
        is_model_specific: bool,
        type: CustomMetricAggregationType,
        time_step: str = CustomMetricBucketTimeStep.HOUR,
        directionality: Optional[CustomMetricDirectionality] = None,
        baseline_values: Optional[BaselineValues] = None,
        description: Optional[str] = None,
        association_id: Optional[DatasetColumn] = None,
        value: Optional[DatasetColumn] = None,
        sample_count: Optional[DatasetColumn] = None,
        timestamp: Optional[DatasetColumn] = None,
        batch: Optional[DatasetColumn] = None,
        deployment_id: Optional[str] = None,
        categories: Optional[List[CustomMetricCategory]] = None,
        is_geospatial: Optional[bool] = None,
        geospatial_segment_attribute: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.units = units
        self.baseline_values = baseline_values
        self.is_model_specific = is_model_specific
        self.type = type
        self.directionality = directionality
        self.time_step = time_step
        self.description = description
        self.association_id = association_id
        self.value = value
        self.sample_count = sample_count
        self.timestamp = timestamp
        self.batch = batch
        self.deployment_id = deployment_id
        self.categories = categories
        self.is_geospatial = is_geospatial
        self.geospatial_segment_attribute = geospatial_segment_attribute

    def __repr__(self) -> str:
        return "CustomMetric({} | {})".format(self.id, self.name)

    @classmethod
    def create(
        cls,
        name: str,
        deployment_id: str,
        units: str,
        is_model_specific: bool,
        aggregation_type: CustomMetricAggregationType,
        time_step: str = CustomMetricBucketTimeStep.HOUR,
        directionality: Optional[CustomMetricDirectionality] = None,
        description: Optional[str] = None,
        baseline_value: Optional[float] = None,
        value_column_name: Optional[str] = None,
        sample_count_column_name: Optional[str] = None,
        timestamp_column_name: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        batch_column_name: Optional[str] = None,
        categories: Optional[List[CustomMetricCategory]] = None,
        is_geospatial: Optional[bool] = None,
        geospatial_segment_attribute: Optional[str] = None,
    ) -> CustomMetric:
        """Create a custom metric for a deployment

        Parameters
        ----------
        name: str
            The name of the custom metric.
        deployment_id: str
            The id of the deployment.
        units: str
            The units, or the y-axis label, of the given custom metric.
        baseline_value: float
            The baseline value used to add "reference dots" to the values over time chart.
        is_model_specific: bool
            Determines whether the metric is related to the model or deployment.
        aggregation_type: CustomMetricAggregationType
            The aggregation type of the custom metric.
        directionality: CustomMetricDirectionality
            The directionality of the custom metric.
        time_step: CustomMetricBucketTimeStep
            Custom metric time bucket size.
        description: Optional[str]
            A description of the custom metric.
        value_column_name: Optional[str]
            A custom metric value column name when reading values from columnar dataset.
        sample_count_column_name: Optional[str]
            Points to a weight column name if users provide pre-aggregated metric values from columnar dataset.
        timestamp_column_name: Optional[str]
            A custom metric timestamp column name when reading values from columnar dataset.
        timestamp_format: Optional[str]
            A custom metric timestamp format when reading values from columnar dataset.
        batch_column_name: Optional[str]
            A custom metric batch ID column name when reading values from columnar dataset.
        is_geospatial: Optional[bool]
            Determines whether the metric is geospatial or not.
        geospatial_segment_attribute: Optional[str]
            The name of  the geospatial segment attribute.

        Returns
        -------
        CustomMetric
            The custom metric object.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric
            from datarobot.enums import CustomMetricAggregationType, CustomMetricDirectionality

            custom_metric = CustomMetric.create(
                deployment_id="5c939e08962d741e34f609f0",
                name="Sample metric",
                units="Y",
                baseline_value=12,
                is_model_specific=True,
                aggregation_type=CustomMetricAggregationType.AVERAGE,
                directionality=CustomMetricDirectionality.HIGHER_IS_BETTER
                )
        """
        payload = {
            "name": name,
            "units": units,
            "baselineValues": [{"value": baseline_value}] if baseline_value else [],
            "isModelSpecific": is_model_specific,
            "type": aggregation_type,
            "directionality": directionality,
            "timeStep": time_step,
            "description": description if description else "",
        }
        if value_column_name is not None:
            payload["value"] = {"columnName": value_column_name}
        if sample_count_column_name is not None:
            payload["sampleCount"] = {"columnName": sample_count_column_name}
        if timestamp_column_name is not None:
            payload["timestamp"] = {
                "columnName": timestamp_column_name,
                "timeFormat": timestamp_format,
            }
        if batch_column_name is not None:
            payload["batch"] = {"columnName": batch_column_name}
        if categories:
            payload["categories"] = categories
        if is_geospatial is not None:
            payload["isGeospatial"] = is_geospatial
        if geospatial_segment_attribute:
            payload["geospatialSegmentAttribute"] = geospatial_segment_attribute
        path = cls._path.format(deployment_id)
        response = cls._client.post(path, json=payload)
        custom_metric_id = response.json()["id"]
        return cls.get(deployment_id, custom_metric_id)

    @classmethod
    def get(cls, deployment_id: str, custom_metric_id: str) -> CustomMetric:
        """Get a custom metric for a deployment

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        custom_metric_id: str
            The ID of the custom metric.

        Returns
        -------
        CustomMetric
            The custom metric object.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )

            custom_metric.id
            >>>'65f17bdcd2d66683cdfc1113'
        """
        path = "{}{}/".format(cls._path.format(deployment_id), custom_metric_id)
        custom_metric = cls.from_location(path)
        custom_metric.deployment_id = deployment_id
        return custom_metric

    @classmethod
    def list(cls, deployment_id: str) -> List[CustomMetric]:
        """List all custom metrics for a deployment

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.

        Returns
        -------
        custom_metrics: list
            A list of custom metrics objects.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metrics = CustomMetric.list(deployment_id="5c939e08962d741e34f609f0")
            custom_metrics[0].id
            >>>'65f17bdcd2d66683cdfc1113'
        """
        path = cls._path.format(deployment_id)
        get_response = cls._client.get(path).json()
        custom_metrics = [cls.from_server_data(data) for data in get_response["data"]]
        for custom_metric in custom_metrics:
            custom_metric.deployment_id = deployment_id
        return custom_metrics

    @classmethod
    def delete(cls, deployment_id: str, custom_metric_id: str) -> None:
        """Delete a custom metric associated with a deployment.

        Parameters
        ----------
        deployment_id: str
            The ID of the deployment.
        custom_metric_id: str
            The ID of the custom metric.

        Returns
        -------
        None

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            CustomMetric.delete(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
        """
        path = "{}{}/".format(cls._path.format(deployment_id), custom_metric_id)
        cls._client.delete(path)

    def update(
        self,
        name: Optional[str] = None,
        units: Optional[str] = None,
        aggregation_type: Optional[CustomMetricAggregationType] = None,
        directionality: Optional[CustomMetricDirectionality] = None,
        time_step: Optional[str] = None,
        description: Optional[str] = None,
        baseline_value: Optional[float] = None,
        value_column_name: Optional[str] = None,
        sample_count_column_name: Optional[str] = None,
        timestamp_column_name: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        batch_column_name: Optional[str] = None,
    ) -> CustomMetric:
        """Update metadata of a custom metric

        Parameters
        ----------
        name: Optional[str]
            The name of the custom metric.
        units: Optional[str]
            The units, or the y-axis label, of the given custom metric.
        baseline_value: Optional[float]
            The baseline value used to add "reference dots" to the values over time chart.
        aggregation_type: Optional[CustomMetricAggregationType]
            The aggregation type of the custom metric.
        directionality: Optional[CustomMetricDirectionality]
            The directionality of the custom metric.
        time_step: Optional[CustomMetricBucketTimeStep]
            Custom metric time bucket size.
        description: Optional[str]
            A description of the custom metric.
        value_column_name: Optional[str]
            A custom metric value column name when reading values from columnar dataset.
        sample_count_column_name: Optional[str]
            Points to a weight column name if users provide pre-aggregated metric values from columnar dataset.
        timestamp_column_name: Optional[str]
            A custom metric timestamp column name when reading values from columnar dataset.
        timestamp_format: Optional[str]
            A custom metric timestamp format when reading values from columnar dataset.
        batch_column_name: Optional[str]
            A custom metric batch ID column name when reading values from columnar dataset.

        Returns
        -------
        CustomMetric
            The custom metric object.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric
            from datarobot.enums import CustomMetricAggregationType, CustomMetricDirectionality

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
            custom_metric = custom_metric.update(
                deployment_id="5c939e08962d741e34f609f0",
                name="Sample metric",
                units="Y",
                baseline_value=12,
                is_model_specific=True,
                aggregation_type=CustomMetricAggregationType.AVERAGE,
                directionality=CustomMetricDirectionality.HIGHER_IS_BETTER
                )
        """
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if units is not None:
            params["units"] = units
        if aggregation_type is not None:
            params["type"] = aggregation_type
        if directionality is not None:
            params["directionality"] = directionality
        if baseline_value is not None:
            params["baselineValues"] = [{"value": baseline_value}]
        if time_step is not None:
            params["timeStep"] = time_step
        if description is not None:
            params["description"] = description
        if value_column_name is not None:
            params["value"] = {"columnName": value_column_name}
        if sample_count_column_name is not None:
            params["sampleCount"] = {"columnName": sample_count_column_name}
        if timestamp_column_name is not None:
            params["timestamp"] = {
                "columnName": timestamp_column_name,
                "timeFormat": timestamp_format,
            }
        if batch_column_name is not None:
            params["batch"] = {"columnName": batch_column_name}

        path = "{}{}/".format(self._path.format(self.deployment_id), self.id)
        self._client.patch(path, data=params)

        for param, value in params.items():
            case_converted = from_api(value)
            param_converted = underscorize(param)
            setattr(self, param_converted, case_converted)
        return self

    def unset_baseline(self) -> None:
        """Unset the baseline value of a custom metric

        Returns
        -------
        None

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric
            from datarobot.enums import CustomMetricAggregationType, CustomMetricDirectionality

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
            custom_metric.baseline_values
            >>> [{'value': 12.0}]
            custom_metric.unset_baseline()
            custom_metric.baseline_values
            >>> []
        """
        params: Dict[str, Any] = {"baselineValues": []}
        path = "{}{}/".format(self._path.format(self.deployment_id), self.id)
        self._client.patch(path, data=params)
        for param, value in params.items():
            case_converted = from_api(value)
            param_converted = underscorize(param)
            setattr(self, param_converted, case_converted)

    def submit_values(
        self,
        data: Union[pd.DataFrame, List[CustomMetricBucket]],
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        dry_run: Optional[bool] = False,
    ) -> None:
        """Submit aggregated custom metrics values from JSON.

        Parameters
        ----------
        data: pd.DataFrame or List[CustomMetricBucket]
            The data containing aggregated custom metric values.
        model_id: Optional[str]
            For a model metric: the ID of the associated champion/challenger model, used to update the metric values.
            For a deployment metric: the ID of the model is not needed.
        model_package_id: Optional[str]
            For a model metric: the ID of the associated champion/challenger model, used to update the metric values.
            For a deployment metric: the ID of the model package is not needed.
        dry_run: Optional[bool]
            Specifies whether or not metric data is submitted in production mode (where data is saved).

        Returns
        -------
        None

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )

            # data for values over time
            data = [{
                'value': 12,
                'sample_size': 3,
                'timestamp': '2024-03-15T14:00:00'
            }]

            # data witch association ID
            data = [{
                'value': 12,
                'sample_size': 3,
                'timestamp': '2024-03-15T14:00:00',
                'association_id': '65f44d04dbe192b552e752ed'
            }]

            # data for batches
            data = [{
                'value': 12,
                'sample_size': 3,
                'batch': '65f44c93fedc5de16b673a0d'
            }]

            # for deployment specific metrics
            custom_metric.submit_values(data=data)

            # for model specific metrics pass model_package_id or model_id
            custom_metric.submit_values(data=data, model_package_id="6421df32525c58cc6f991f25")

            # dry run
            custom_metric.submit_values(data=data, model_package_id="6421df32525c58cc6f991f25", dry_run=True)

        """
        if not isinstance(data, (list, pd.DataFrame)):
            raise ValueError(
                "data should be either a list of dict-like objects or a pandas.DataFrame"
            )

        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient="records")

        buckets: List[Dict[str, Any]] = []
        for row in data:
            bucket: Dict[str, Any] = {"sampleSize": row["sample_size"], "value": row["value"]}

            if "timestamp" in row and "batch" in row:
                raise ValueError("data should contain either timestamps or batch IDs")

            if "timestamp" in row:
                if isinstance(row["timestamp"], datetime):
                    bucket["timestamp"] = row["timestamp"].isoformat()
                else:
                    bucket["timestamp"] = dateutil.parser.parse(row["timestamp"]).isoformat()

            if "batch" in row:
                bucket["batch"] = row["batch"]

            if "association_id" in row:
                bucket["associationId"] = row["association_id"]
            if "segments" in row:
                bucket["segments"] = row["segments"]
            if "geospatial_coordinate" in row:
                bucket["geospatialCoordinate"] = row["geospatial_coordinate"]
            if "metadata" in row:
                bucket["metadata"] = row["metadata"]

            buckets.append(bucket)

        payload: Dict[str, Any] = {"buckets": buckets, "dryRun": dry_run}
        if model_id:
            payload["modelId"] = model_id
        if model_package_id:
            payload["modelPackageId"] = model_package_id

        path = "{}{}/fromJSON/".format(self._path.format(self.deployment_id), self.id)
        response = self._client.post(path, data=payload)
        if not dry_run:
            wait_for_async_resolution(self._client, response.headers["Location"], DEFAULT_MAX_WAIT)

    def submit_single_value(
        self,
        value: float | str,
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        dry_run: Optional[bool] = False,
        segments: Optional[List[CustomMetricSegmentFromJSON]] = None,
    ) -> None:
        """Submit a single custom metric value at the current moment.

        Parameters
        ----------
        value: float
            Single numeric custom metric value.
        model_id: Optional[str]
            For a model metric: the ID of the associated champion/challenger model, used to update the metric values.
            For a deployment metric: the ID of the model is not needed.
        model_package_id: Optional[str]
            For a model metric: the ID of the associated champion/challenger model, used to update the metric values.
            For a deployment metric: the ID of the model package is not needed.
        dry_run: Optional[bool]
            Specifies whether or not metric data is submitted in production mode (where data is saved).
        segments: Optional[CustomMetricSegmentFromJSON]
            A list of segments for a custom metric used in segmented analysis.

        Returns
        -------
        None

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )

            # for deployment specific metrics
            custom_metric.submit_single_value(value=121)

            # for model specific metrics pass model_package_id or model_id
            custom_metric.submit_single_value(value=121, model_package_id="6421df32525c58cc6f991f25")

            # dry run
            custom_metric.submit_single_value(value=121, model_package_id="6421df32525c58cc6f991f25", dry_run=True)

            # for segmented analysis
            segments = [{"name": "custom_seg", "value": "val_1"}]
            custom_metric.submit_single_value(value=121, model_package_id="6421df32525c58cc6f991f25", segments=segments)
        """
        bucket: Dict[str, Any] = {
            "sampleSize": 1,
            "value": value,
            "timestamp": datetime.now().isoformat(),
        }
        if segments:
            bucket["segments"] = segments
        payload: Dict[str, Any] = {"buckets": [bucket], "dryRun": dry_run}
        if model_id:
            payload["modelId"] = model_id
        if model_package_id:
            payload["modelPackageId"] = model_package_id

        path = "{}{}/fromJSON/".format(self._path.format(self.deployment_id), self.id)
        response = self._client.post(path, data=payload)
        if not dry_run:
            wait_for_async_resolution(self._client, response.headers["Location"], DEFAULT_MAX_WAIT)

    def submit_values_from_catalog(
        self,
        dataset_id: str,
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        batch_id: Optional[str] = None,
        segments: Optional[List[CustomMetricSegmentFromDataset]] = None,
        geospatial: Optional[Geospatial] = None,
    ) -> None:
        """Submit aggregated custom metrics values from dataset (AI catalog).
        The names of the columns in the dataset should correspond to the names of the columns that were defined in
        the custom metric. In addition, the format of the timestamps should also be the same as defined in the metric.

        Parameters
        ----------
        dataset_id: str
            The ID of the source dataset.
        model_id: Optional[str]
            For a model metric: the ID of the associated champion/challenger model, used to update the metric values.
            For a deployment metric: the ID of the model is not needed.
        model_package_id: Optional[str]
            For a model metric: the ID of the associated champion/challenger model, used to update the metric values.
            For a deployment metric: the ID of the model package is not needed.
        batch_id: Optional[str]
            Specifies a batch ID associated with all values provided by this dataset, an alternative
            to providing batch IDs as a column within a dataset (at the record level).
        segments: Optional[CustomMetricSegmentFromDataset]
            A list of segments for a custom metric used in segmented analysis.
        geospatial: Optional[Geospatial]
            A geospatial column source when reading values from columnar dataset.

        Returns
        -------
        None

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )

            # for deployment specific metrics
            custom_metric.submit_values_from_catalog(dataset_id="61093144cabd630828bca321")

            # for model specific metrics pass model_package_id or model_id
            custom_metric.submit_values_from_catalog(
                dataset_id="61093144cabd630828bca321",
                model_package_id="6421df32525c58cc6f991f25"
            )

            # for segmented analysis
            segments = [{"name": "custom_seg", "column": "column_with_segment_values"}]
            custom_metric.submit_values_from_catalog(
                dataset_id="61093144cabd630828bca321",
                model_package_id="6421df32525c58cc6f991f25",
                segments=segments
            )
        """
        payload: Dict[str, Any] = {
            "datasetId": dataset_id,
            "value": self.value,
            "timestamp": self.timestamp,
            "sampleCount": self.sample_count,
            "batch": self.batch,
            "associationId": self.association_id,
        }

        if model_id:
            payload["modelId"] = model_id
        if model_package_id:
            payload["modelPackageId"] = model_package_id
        if segments:
            payload["segments"] = segments
        if batch_id:
            payload["batchId"] = batch_id
        if geospatial:
            payload["geospatial"] = geospatial

        path = "{}{}/fromDataset/".format(self._path.format(self.deployment_id), self.id)
        response = self._client.post(path, data=to_api(payload))
        wait_for_async_resolution(self._client, response.headers["Location"], DEFAULT_MAX_WAIT)

    def get_values_over_time(
        self,
        start: Union[datetime, str],
        end: Union[datetime, str],
        model_package_id: Optional[str] = None,
        model_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
        bucket_size: str = BUCKET_SIZE.P7D,
    ) -> CustomMetricValuesOverTime:
        """Retrieve values of a single custom metric over a time period.

        Parameters
        ----------
        start: datetime or str
            Start of the time period.
        end: datetime or str
            End of the time period.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        bucket_size: Optional[str]
            Time duration of a bucket, in ISO 8601 time duration format.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_over_time: CustomMetricValuesOverTime
            The queried custom metric values over time information.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric
            from datetime import datetime, timedelta

            now=datetime.now()
            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
            values_over_time = custom_metric.get_values_over_time(start=now - timedelta(days=7), end=now)

            values_over_time.bucket_values
            >>> {datetime.datetime(2024, 3, 22, 14, 0, tzinfo=tzutc()): 1.0,
            >>> datetime.datetime(2024, 3, 22, 15, 0, tzinfo=tzutc()): 123.0}}

            values_over_time.bucket_sample_sizes
            >>> {datetime.datetime(2024, 3, 22, 14, 0, tzinfo=tzutc()): 1,
            >>>  datetime.datetime(2024, 3, 22, 15, 0, tzinfo=tzutc()): 1}}

            values_over_time.get_buckets_as_dataframe()
            >>>                        start                       end  value  sample_size
            >>> 0  2024-03-21 16:00:00+00:00 2024-03-21 17:00:00+00:00    NaN          NaN
            >>> 1  2024-03-21 17:00:00+00:00 2024-03-21 18:00:00+00:00    NaN          NaN
        """

        if not self.deployment_id:
            raise ValueError("Deployment ID is required to get custom metric values over time.")

        return CustomMetricValuesOverTime.get(
            custom_metric_id=self.id,
            deployment_id=self.deployment_id,
            start=start,
            end=end,
            model_id=model_id,
            model_package_id=model_package_id,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
            bucket_size=bucket_size,
        )

    def get_values_over_space(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
    ) -> CustomMetricValuesOverSpace:
        """Retrieve values of a custom metric over space.

        Parameters
        ----------
        start: Optional[datetime]
            Start of the time period.
        end: Optional[datetime]
            End of the time period.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.

        Returns
        -------
        custom_metric_over_space: CustomMetricValuesOverSpace
            The queried custom metric values over space information.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
            values_over_space = custom_metric.get_values_over_space(model_package_id='6421df32525c58cc6f991f25')
        """
        return CustomMetricValuesOverSpace.get(
            deployment_id=str(self.deployment_id),
            custom_metric_id=self.id,
            start=start,
            end=end,
            model_id=model_id,
            model_package_id=model_package_id,
        )

    def get_summary(
        self,
        start: Union[datetime, str],
        end: Union[datetime, str],
        model_package_id: Optional[str] = None,
        model_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ) -> CustomMetricSummary:
        """Retrieve the summary of a custom metric over a time period.

        Parameters
        ----------
        start: datetime or str
            Start of the time period.
        end: datetime or str
            End of the time period.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_summary: CustomMetricSummary
            The summary of the custom metric.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric
            from datetime import datetime, timedelta

            now=datetime.now()
            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
            summary = custom_metric.get_summary(start=now - timedelta(days=7), end=now)

            print(summary)
            >> "CustomMetricSummary(2024-03-21 15:52:13.392178+00:00 - 2024-03-22 15:52:13.392168+00:00:
            {'id': '65fd9b1c0c1a840bc6751ce0', 'name': 'Test METRIC', 'value': 215.0, 'sample_count': 13,
            'baseline_value': 12.0, 'percent_change': 24.02})"
        """

        if not self.deployment_id:
            raise ValueError("Deployment ID is required to get custom metric summary.")

        return CustomMetricSummary.get(
            custom_metric_id=self.id,
            deployment_id=self.deployment_id,
            start=start,
            end=end,
            model_id=model_id,
            model_package_id=model_package_id,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
        )

    def get_values_over_batch(
        self,
        batch_ids: Optional[List[str]] = None,
        model_package_id: Optional[str] = None,
        model_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ) -> CustomMetricValuesOverBatch:
        """Retrieve values of a single custom metric over batches.

        Parameters
        ----------
        batch_ids : Optional[List[str]]
            Specify a list of batch IDs to pull the data for.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_over_batch: CustomMetricValuesOverBatch
            The queried custom metric values over batch information.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
            # all batch metrics all model specific
            values_over_batch = custom_metric.get_values_over_batch(model_package_id='6421df32525c58cc6f991f25')

            values_over_batch.bucket_values
            >>> {'6572db2c9f9d4ad3b9de33d0': 35.0, '6572db2c9f9d4ad3b9de44e1': 105.0}

            values_over_batch.bucket_sample_sizes
            >>> {'6572db2c9f9d4ad3b9de33d0': 6, '6572db2c9f9d4ad3b9de44e1': 8}


            values_over_batch.get_buckets_as_dataframe()
            >>>                    batch_id                     batch_name  value  sample_size
            >>> 0  6572db2c9f9d4ad3b9de33d0  Batch 1 - 03/26/2024 13:04:46   35.0            6
            >>> 1  6572db2c9f9d4ad3b9de44e1  Batch 2 - 03/26/2024 13:06:04  105.0            8
        """

        if not self.deployment_id:
            raise ValueError("Deployment ID is required to get custom metric values over time.")

        if not model_package_id and not model_id:
            raise ValueError(
                "For batch metrics either the modelPackageId or the modelId must be passed."
            )

        return CustomMetricValuesOverBatch.get(
            custom_metric_id=self.id,
            deployment_id=self.deployment_id,
            batch_ids=batch_ids,
            model_id=model_id,
            model_package_id=model_package_id,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
        )

    def get_batch_summary(
        self,
        batch_ids: Optional[List[str]] = None,
        model_package_id: Optional[str] = None,
        model_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ) -> CustomMetricBatchSummary:
        """Retrieve the summary of a custom metric over a batch.

        Parameters
        ----------
        batch_ids : Optional[List[str]]
            Specify a list of batch IDs to pull the data for.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_summary: CustomMetricBatchSummary
            The batch summary of the custom metric.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.deployment import CustomMetric

            custom_metric = CustomMetric.get(
                deployment_id="5c939e08962d741e34f609f0",
                custom_metric_id="65f17bdcd2d66683cdfc1113"
            )
            # all batch metrics all model specific
            batch_summary = custom_metric.get_batch_summary(model_package_id='6421df32525c58cc6f991f25')

            print(batch_summary)
            >> CustomMetricBatchSummary({'id': '6605396413434b3a7b74342c', 'name': 'batch metric', 'value': 41.25,
            'sample_count': 28, 'baseline_value': 123.0, 'percent_change': -66.46})
        """

        if not self.deployment_id:
            raise ValueError("Deployment ID is required to get custom metric values over time.")

        if not model_package_id and not model_id:
            raise ValueError(
                "For batch metrics either the modelPackageId or the modelId must be passed."
            )

        return CustomMetricBatchSummary.get(
            custom_metric_id=self.id,
            deployment_id=self.deployment_id,
            batch_ids=batch_ids,
            model_id=model_id,
            model_package_id=model_package_id,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
        )


class CustomMetricValuesOverTime(APIObject, MonitoringDataQueryBuilderMixin):
    """Custom metric over time information.

    .. versionadded:: v3.4

    Attributes
    ----------
    buckets: List[Bucket]
        A list of bucketed time periods and the custom metric values aggregated over that period.
    summary: Summary
        The summary of values over time retrieval.
    metric: Dict
        A custom metric definition.
    deployment_id: str
        The ID of the deployment.
    segment_attribute: str
        The name of the segment on which segment analysis is being performed.
    segment_value: str
        The value of the segment_attribute to segment on.
    """

    _path = "deployments/{}/customMetrics/{}/valuesOverTime/"
    _period = t.Dict(
        {
            t.Key("start"): t.String >> dateutil.parser.parse,
            t.Key("end"): t.String >> dateutil.parser.parse,
        }
    )
    _categories = t.Dict(
        {
            t.Key("category_name"): t.String,
            t.Key("count"): t.Int,
        }
    ).allow_extra("*")
    _bucket = t.Dict(
        {
            t.Key("period"): t.Or(_period, t.Null),
            t.Key("value", optional=True): t.Or(t.Float, t.Null),
            t.Key("sample_size", optional=True): t.Or(t.Int, t.Null),
            t.Key("unknown_categories_count", optional=True): t.Or(t.Int, t.Null),
            t.Key("categories", optional=True): t.Or(t.List(_categories), t.Null),
        }
    ).allow_extra("*")
    _converter = t.Dict(
        {
            t.Key("buckets"): t.List(_bucket),
            t.Key("summary"): t.Dict(
                {
                    t.Key("start"): t.String >> dateutil.parser.parse,
                    t.Key("end"): t.String >> dateutil.parser.parse,
                }
            ),
            t.Key("metric"): t.Dict().allow_extra("*"),
            t.Key("segment_attribute", optional=True): t.String(),
            t.Key("segment_value", optional=True): t.String(),
        }
    ).allow_extra("*")

    def __init__(
        self,
        buckets: Optional[List[Bucket]] = None,
        summary: Optional[Summary] = None,
        metric: Optional[Dict[str, Any]] = None,
        deployment_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ):
        self.buckets = buckets if buckets is not None else []
        self.summary = summary if summary is not None else {}
        self.metric = metric
        self.deployment_id = deployment_id
        self.segment_attribute = segment_attribute
        self.segment_value = segment_value

    def __repr__(self) -> str:
        return "CustomMetricValuesOverTime({} - {})".format(
            self.summary.get("start"),
            self.summary.get("end"),
        )

    @classmethod
    def get(
        cls,
        deployment_id: str,
        custom_metric_id: str,
        start: Union[datetime, str],
        end: Union[datetime, str],
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
        bucket_size: str = BUCKET_SIZE.P7D,
    ) -> CustomMetricValuesOverTime:
        """Retrieve values of a single custom metric over a time period.

        Parameters
        ----------
        custom_metric_id: str
            The ID of the custom metric.
        deployment_id: str
            The ID of the deployment.
        start: datetime or str
            Start of the time period.
        end: datetime or str
            End of the time period.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        bucket_size: Optional[str]
            Time duration of a bucket, in ISO 8601 time duration format.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_over_time: CustomMetricValuesOverTime
            The queried custom metric values over time information.
        """
        path = cls._path.format(deployment_id, custom_metric_id)
        params = cls._build_query_params(
            start=start,
            end=end,
            model_id=model_id,
            model_package_id=model_package_id,
            bucket_size=bucket_size,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
        )
        data = cls._client.get(path, params=params).json()
        case_converted = from_api(data, keep_null_keys=True)
        custom_metric_over_time = cls.from_data(case_converted)
        custom_metric_over_time.deployment_id = deployment_id
        return custom_metric_over_time

    @property
    def bucket_values(self) -> Dict[datetime, int]:
        """The metric value for all time buckets, keyed by start time of the bucket.

        Returns
        -------
        bucket_values: Dict
        """
        if self.buckets:
            return {
                bucket["period"]["start"]: bucket["value"]
                for bucket in self.buckets
                if bucket.get("period")
            }
        return {}

    @property
    def bucket_sample_sizes(self) -> Dict[datetime, int]:
        """The sample size for all time buckets, keyed by start time of the bucket.

        Returns
        -------
        bucket_sample_sizes: Dict
        """
        if self.buckets:
            return {
                bucket["period"]["start"]: bucket["sample_size"]
                for bucket in self.buckets
                if bucket.get("period")
            }
        return {}

    def get_buckets_as_dataframe(self) -> pd.DataFrame:
        """Retrieves all custom metrics buckets in a pandas DataFrame.

        Returns
        -------
        buckets: pd.DataFrame
        """
        if self.buckets:
            rows = []
            for bucket in self.buckets:
                rows.append(
                    {
                        "start": bucket["period"]["start"],
                        "end": bucket["period"]["end"],
                        "value": bucket["value"],
                        "sample_size": bucket["sample_size"],
                    }
                )
            return pd.DataFrame(rows)
        return pd.DataFrame()


class CustomMetricValuesOverSpace(APIObject, MonitoringDataQueryBuilderMixin):
    """Custom metric values over space.

    .. versionadded:: v3.7

    Attributes
    ----------
    buckets: List[BatchBucket]
        A list of buckets with custom metric values aggregated over geospatial hexagons.
    metric: Dict
        A custom metric definition.
    model_id: str
        The ID of the model.
    model_package_id: str
        The ID of the model package (also known as registered model version id).
    summary: Dict
        Start-end interval over which data is retrieved.


    """

    _path = "deployments/{}/customMetrics/{}/valuesOverSpace/"
    _categories = t.Dict(
        {
            t.Key("category_name"): t.String,
            t.Key("count"): t.Int,
        }
    ).allow_extra("*")
    _bucket = t.Dict(
        {
            t.Key("value", optional=True): t.Or(t.Float, t.Null),
            t.Key("sample_size", optional=True): t.Or(t.Int, t.Null),
            t.Key("unknown_categories_count", optional=True): t.Or(t.Int, t.Null),
            t.Key("categories", optional=True): t.Or(t.List(_categories), t.Null),
            t.Key("hexagon"): t.String(),
        }
    ).allow_extra("*")
    _converter = t.Dict(
        {
            t.Key("buckets"): t.List(_bucket),
            t.Key("metric"): t.Dict().allow_extra("*"),
            t.Key("summary"): t.Dict().allow_extra("*"),
            t.Key("model_id", optional=True): t.Or(t.String(), t.Null()),
            t.Key("model_package_id", optional=True): t.Or(t.String(), t.Null()),
        }
    ).allow_extra("*")

    def __init__(
        self,
        buckets: Optional[List[CustomMetricOverSpaceBucket]] = None,
        metric: Optional[Dict[str, Any]] = None,
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        summary: Optional[Dict[str, Any]] = None,
    ):
        self.buckets = buckets
        self.metric = metric
        self.model_id = model_id
        self.model_package_id = model_package_id
        self.summary = summary

    @classmethod
    def get(
        cls,
        deployment_id: str,
        custom_metric_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        model_package_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> CustomMetricValuesOverSpace:
        """Retrieve custom metric values over space.

        Parameters
        ----------
        deployment_id: str
            The id of the deployment.
        custom_metric_id: str
            The id of the custom metric.
        start: datetime
            The start time of the interval.
        end: datetime
            The end time of the interval.
        model_package_id: str
            The id of the model package.
        model_id: str
            The id of the model.

        Returns
        -------
        values_over_space: CustomMetricValuesOverSpace
            Custom metric values over geospatial hexagons.

        """
        path = cls._path.format(deployment_id, custom_metric_id)
        params = cls._build_query_params(
            start_time=start,
            end_time=end,
            model_id=model_id,
            model_package_id=model_package_id,
        )
        data = cls._client.get(path, params=params).json()
        case_converted = from_api(data, keep_null_keys=True)
        values_over_space = cls.from_data(case_converted)
        return values_over_space


class CustomMetricSummary(APIObject, MonitoringDataQueryBuilderMixin):
    """The summary of a custom metric.

    .. versionadded:: v3.4

    Attributes
    ----------
    period: Period
        A time period defined by a start and end tie
    metric: Dict
        The summary of the custom metric.
    """

    _path = "deployments/{}/customMetrics/{}/summary/"
    _period = t.Dict(
        {
            t.Key("start"): t.String >> dateutil.parser.parse,
            t.Key("end"): t.String >> dateutil.parser.parse,
        }
    ).allow_extra("*")

    _categories = t.Dict(
        {
            t.Key("category_name"): t.String,
            t.Key("value", optional=True): t.Or(t.Float, t.Null),
            t.Key("baseline_value", optional=True): t.Or(t.Int, t.Null),
            t.Key("percent_change", optional=True): t.Or(t.Int, t.Null),
        }
    ).allow_extra("*")
    _metric = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("value", optional=True): t.Or(t.Float, t.Null),
            t.Key("sample_count", optional=True): t.Or(t.Int, t.Null),
            t.Key("baseline_value", optional=True): t.Or(t.Float, t.Null),
            t.Key("percent_change", optional=True): t.Or(t.Float, t.Null),
            t.Key("unknown_categories_count", optional=True): t.Or(t.Int, t.Null),
            t.Key("categories", optional=True): t.Or(t.List(_categories), t.Null),
        }
    ).allow_extra("*")
    _converter = t.Dict(
        {
            t.Key("period"): _period,
            t.Key("metric"): _metric,
        }
    ).allow_extra("*")

    def __init__(
        self,
        period: Period,
        metric: Dict[str, Any],
        deployment_id: Optional[str] = None,
    ):
        self.period = period
        self.metric = metric
        self.deployment_id = deployment_id

    def __repr__(self) -> str:
        return "CustomMetricSummary({} - {}: {})".format(
            self.period.get("start"), self.period.get("end"), self.metric
        )

    @classmethod
    def get(
        cls,
        deployment_id: str,
        custom_metric_id: str,
        start: Union[datetime, str],
        end: Union[datetime, str],
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ) -> CustomMetricSummary:
        """Retrieve the summary of a custom metric over a time period.

        Parameters
        ----------
        custom_metric_id: str
            The ID of the custom metric.
        deployment_id: str
            The ID of the deployment.
        start: datetime or str
            Start of the time period.
        end: datetime or str
            End of the time period.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_summary: CustomMetricSummary
            The summary of the custom metric.
        """
        path = cls._path.format(deployment_id, custom_metric_id)
        params = cls._build_query_params(
            start=start,
            end=end,
            model_id=model_id,
            model_package_id=model_package_id,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
        )
        data = cls._client.get(path, params=params).json()
        case_converted = from_api(data, keep_null_keys=True)
        custom_metric_summary = cls.from_data(case_converted)
        custom_metric_summary.deployment_id = deployment_id
        return custom_metric_summary


class CustomMetricValuesOverBatch(APIObject, MonitoringDataQueryBuilderMixin):
    """Custom metric over batch information.

    .. versionadded:: v3.4

    Attributes
    ----------
    buckets: List[BatchBucket]
        A list of buckets with custom metric values aggregated over batches.
    metric: Dict
        A custom metric definition.
    deployment_id: str
        The ID of the deployment.
    segment_attribute: str
        The name of the segment on which segment analysis is being performed.
    segment_value: str
        The value of the segment_attribute to segment on.
    """

    _path = "deployments/{}/customMetrics/{}/valuesOverBatch/"
    _batch = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("created_at"): t.String >> dateutil.parser.parse,
            t.Key("last_prediction_timestamp", optional=True): t.String >> dateutil.parser.parse,
        }
    ).allow_extra("*")
    _categories = t.Dict(
        {
            t.Key("category_name"): t.String,
            t.Key("count"): t.Int,
        }
    ).allow_extra("*")
    _bucket = t.Dict(
        {
            t.Key("batch"): t.Or(_batch),
            t.Key("value", optional=True): t.Or(t.Float, t.Null),
            t.Key("sample_size", optional=True): t.Or(t.Int, t.Null),
            t.Key("unknown_categories_count", optional=True): t.Or(t.Int, t.Null),
            t.Key("categories", optional=True): t.Or(t.List(_categories), t.Null),
        }
    ).allow_extra("*")
    _converter = t.Dict(
        {
            t.Key("buckets"): t.List(_bucket),
            t.Key("metric"): t.Dict().allow_extra("*"),
            t.Key("segment_attribute", optional=True): t.String(),
            t.Key("segment_value", optional=True): t.String(),
        }
    ).allow_extra("*")

    def __init__(
        self,
        buckets: Optional[List[BatchBucket]] = None,
        metric: Optional[Dict[str, Any]] = None,
        deployment_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ):
        self.buckets = buckets if buckets is not None else []
        self.metric = metric
        self.deployment_id = deployment_id
        self.segment_attribute = segment_attribute
        self.segment_value = segment_value

    def __repr__(self) -> str:
        first_batch = self.buckets[0]["batch"].get("id") if self.buckets else None
        last_batch = self.buckets[-1]["batch"].get("id") if self.buckets else None
        return "CustomMetricValuesOverBatch({} - {})".format(
            first_batch,
            last_batch,
        )

    @classmethod
    def get(
        cls,
        deployment_id: str,
        custom_metric_id: str,
        batch_ids: Optional[List[str]] = None,
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ) -> CustomMetricValuesOverBatch:
        """Retrieve values of a single custom metric over batches.

        Parameters
        ----------
        custom_metric_id: str
            The ID of the custom metric.
        deployment_id: str
            The ID of the deployment.
        batch_ids : Optional[List[str]]
            Specify a list of batch IDs to pull the data for.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_over_batch: CustomMetricValuesOverBatch
            The queried custom metric values over batch information.
        """
        path = cls._path.format(deployment_id, custom_metric_id)
        params = cls._build_query_params(
            batch_id=batch_ids,
            model_id=model_id,
            model_package_id=model_package_id,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
        )
        data = cls._client.get(path, params=params).json()
        case_converted = from_api(data, keep_null_keys=True)
        custom_metric_over_batch = cls.from_data(case_converted)
        custom_metric_over_batch.deployment_id = deployment_id
        return custom_metric_over_batch

    @property
    def bucket_values(self) -> Dict[str, int]:
        """The metric value for all batch buckets, keyed by batch ID

        Returns
        -------
        bucket_values: Dict
        """
        if self.buckets:
            return {bucket["batch"]["id"]: bucket["value"] for bucket in self.buckets}
        return {}

    @property
    def bucket_sample_sizes(self) -> Dict[str, int]:
        """The sample size for all batch buckets, keyed by batch ID.

        Returns
        -------
        bucket_sample_sizes: Dict
        """
        if self.buckets:
            return {bucket["batch"]["id"]: bucket["sample_size"] for bucket in self.buckets}
        return {}

    def get_buckets_as_dataframe(self) -> pd.DataFrame:
        """Retrieves all custom metrics buckets in a pandas DataFrame.

        Returns
        -------
        buckets: pd.DataFrame
        """
        if self.buckets:
            rows = []
            for bucket in self.buckets:
                rows.append(
                    {
                        "batch_id": bucket["batch"]["id"],
                        "batch_name": bucket["batch"]["name"],
                        "value": bucket["value"],
                        "sample_size": bucket["sample_size"],
                    }
                )
            return pd.DataFrame(rows)
        return pd.DataFrame()


class CustomMetricBatchSummary(APIObject, MonitoringDataQueryBuilderMixin):
    """The batch summary of a custom metric.

    .. versionadded:: v3.4

    Attributes
    ----------
    metric: Dict
        The summary of the batch custom metric.
    """

    _path = "deployments/{}/customMetrics/{}/batchSummary/"
    _categories = t.Dict(
        {
            t.Key("category_name"): t.String,
            t.Key("value", optional=True): t.Or(t.Float, t.Null),
            t.Key("baseline_value", optional=True): t.Or(t.Int, t.Null),
            t.Key("percent_change"): t.Or(t.Int, t.Null),
        }
    ).allow_extra("*")
    _metric = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("value", optional=True): t.Or(t.Float, t.Null),
            t.Key("sample_count", optional=True): t.Or(t.Int, t.Null),
            t.Key("baseline_value", optional=True): t.Or(t.Float, t.Null),
            t.Key("percent_change", optional=True): t.Or(t.Float, t.Null),
            t.Key("unknown_categories_count", optional=True): t.Or(t.Int, t.Null),
            t.Key("categories", optional=True): t.Or(t.List(_categories), t.Null),
        }
    ).allow_extra("*")
    _converter = t.Dict(
        {
            t.Key("metric"): _metric,
        }
    ).allow_extra("*")

    def __init__(
        self,
        metric: Dict[str, Any],
        deployment_id: Optional[str] = None,
    ):
        self.metric = metric
        self.deployment_id = deployment_id

    def __repr__(self) -> str:
        return "CustomMetricBatchSummary({})".format(self.metric)

    @classmethod
    def get(
        cls,
        deployment_id: str,
        custom_metric_id: str,
        batch_ids: Optional[List[str]] = None,
        model_id: Optional[str] = None,
        model_package_id: Optional[str] = None,
        segment_attribute: Optional[str] = None,
        segment_value: Optional[str] = None,
    ) -> CustomMetricBatchSummary:
        """Retrieve the summary of a custom metric over a batch.

        Parameters
        ----------
        custom_metric_id: str
            The ID of the custom metric.
        deployment_id: str
            The ID of the deployment.
        batch_ids : Optional[List[str]]
            Specify a list of batch IDs to pull the data for.
        model_id: Optional[str]
            The ID of the model.
        model_package_id: Optional[str]
            The ID of the model package.
        segment_attribute: Optional[str]
            The name of the segment on which segment analysis is being performed.
        segment_value: Optional[str]
            The value of the segment_attribute to segment on.

        Returns
        -------
        custom_metric_summary: CustomMetricBatchSummary
            The batch summary of the custom metric.
        """
        path = cls._path.format(deployment_id, custom_metric_id)
        params = cls._build_query_params(
            batch_id=batch_ids,
            model_id=model_id,
            model_package_id=model_package_id,
            segment_attribute=segment_attribute,
            segment_value=segment_value,
        )
        data = cls._client.get(path, params=params).json()
        case_converted = from_api(data, keep_null_keys=True)
        custom_metric_summary = cls.from_data(case_converted)
        custom_metric_summary.deployment_id = deployment_id
        return custom_metric_summary


class HostedCustomMetricTemplate(APIObject):
    """
    Template for hosted custom metric.
    """

    _path = "customMetricsTemplates/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("description"): t.String(),
            t.Key("custom_metric_metadata"): t.Dict().allow_extra("*"),
            t.Key("default_environment"): t.Dict().allow_extra("*"),
            t.Key("items"): t.List(t.Dict().allow_extra("*")),
            t.Key("template_metric_type"): t.String(),
            t.Key("default_resource_bundle_id", optional=True, default=None): t.Or(
                t.Null, t.String()
            ),
        }
    ).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        custom_metric_metadata: Dict[str, Any],
        default_environment: Dict[str, Any],
        items: List[Dict[str, Any]],
        template_metric_type: str,
        default_resource_bundle_id: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.custom_metric_metadata = custom_metric_metadata
        self.default_environment = default_environment
        self.items = items
        self.template_metric_type = template_metric_type
        self.default_resource_bundle_id = default_resource_bundle_id

    @classmethod
    def list(
        cls,
        search: Optional[str] = None,
        order_by: Optional[ListHostedCustomMetricTemplatesSortQueryParams] = None,
        metric_type: Optional[HostedCustomMetricsTemplateMetricTypeQueryParams] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[HostedCustomMetricTemplate]:
        """List all hosted custom metric templates.

        Parameters
        ----------
        search: Optional[str]
            Search string.
        order_by: Optional[ListHostedCustomMetricTemplatesSortQueryParams]
            Ordering field.
        metric_type: Optional[HostedCustomMetricsTemplateMetricTypeQueryParams]
            Type of the metric.
        offset: Optional[int]
            Offset for pagination.
        limit: Optional[int]
            Limit for pagination.

        Returns
        -------
        templates: List[HostedCustomMetricTemplate]
        """
        params: Dict[str, Any] = {}
        if search:
            params["search"] = search
        if order_by:
            params["orderBy"] = order_by
        if metric_type:
            params["templateMetricType"] = metric_type
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        response = cls._client.get(cls._path, params=params if params else None)
        return [cls.from_server_data(d) for d in response.json()["data"]]

    @classmethod
    def get(cls, template_id: str) -> HostedCustomMetricTemplate:
        """Get a hosted custom metric template by ID.

        Parameters
        ----------
        template_id: str
            ID of the template.

        Returns
        -------
        template : HostedCustomMetricTemplate
        """
        response = cls._client.get(f"{cls._path}{template_id}/")
        return cls.from_server_data(response.json())


class MetricTimestampSpoofing:
    """
    Custom metric timestamp spoofing. Occurs when reading values from a file, like a dataset.
    By default, replicates pd.to_datetime formatting behavior.
    """

    def __init__(self, column_name: str, time_format: Optional[str] = None):
        self.column_name = column_name
        self.time_format = time_format


class BatchField:
    """
    A custom metric batch ID source for when reading values from a columnar dataset like a file.
    """

    def __init__(self, column_name: str):
        self.column_name = column_name


class ValueField:
    """
    A custom metric value source for when reading values from a columnar dataset like a file.
    """

    def __init__(self, column_name: str):
        self.column_name = column_name


class SampleCountField:
    """
    A weight column used with columnar datasets if pre-aggregated metric values are provided.
    """

    def __init__(self, column_name: str):
        self.column_name = column_name


class MetricBaselineValue:
    """
    The baseline values for a custom metric.
    """

    def __init__(self, value: float):
        self.value = value


class DeploymentDetails:
    """
    Information about a hosted custom metric deployment.
    """

    def __init__(
        self,
        id: str,
        name: str,
        creator_first_name: Optional[str] = None,
        creator_last_name: Optional[str] = None,
        creator_username: Optional[str] = None,
        creator_gravatar_hash: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.creator_first_name = creator_first_name
        self.creator_last_name = creator_last_name
        self.creator_username = creator_username
        self.creator_gravatar_hash = creator_gravatar_hash
        self.created_at = created_at


class HostedCustomMetric(APIObject):
    """
    Hosted custom metric.
    """

    _schedule = t.Dict(
        {
            t.Key("hour"): t.List(t.Or(t.String(), t.Int())),
            t.Key("minute"): t.List(t.Or(t.String(), t.Int())),
            t.Key("day_of_week"): t.List(t.Or(t.String(), t.Int())),
            t.Key("day_of_month"): t.List(t.Or(t.String(), t.Int())),
            t.Key("month"): t.List(t.Or(t.String(), t.Int())),
        }
    ).allow_extra("*")
    _parameter_overrides = t.Dict(
        {
            t.Key("field_name"): t.String(),
            t.Key("value", optional=True): t.Or(t.String(), t.Int(), t.Float(), t.Bool(), t.Null()),
            t.Key("type"): t.String(),
        }
    ).allow_extra("*")
    _baseline_values = t.Dict(
        {
            t.Key("value"): t.Float,
        }
    ).allow_extra("*")
    _timestamp = t.Dict(
        {
            t.Key("column_name"): t.String(),
            t.Key("time_format", optional=True): t.String(),
        }
    ).allow_extra("*")
    _value = t.Dict(
        {
            t.Key("column_name"): t.String(),
        }
    ).allow_extra("*")
    _sample_count = t.Dict(
        {
            t.Key("column_name"): t.String(),
        }
    ).allow_extra("*")
    _batch = t.Dict(
        {
            t.Key("column_name"): t.String(),
        }
    ).allow_extra("*")
    _deployment = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("created_at", optional=True): t.String(),
            t.Key("creator_first_name", optional=True): t.String(),
            t.Key("creator_last_name", optional=True): t.String(),
            t.Key("creator_username", optional=True): t.String(),
            t.Key("creator_gravatar_hash", optional=True): t.String(),
        }
    ).allow_extra("*")

    _user = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("username", optional=True): t.String(),
            t.Key("first_name", optional=True): t.String(),
            t.Key("last_name", optional=True): t.String(),
            t.Key("gravatar_hash", optional=True): t.String(),
        }
    ).allow_extra("*")

    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("deployment"): _deployment,
            t.Key("schedule", optional=True): t.Or(_schedule, t.Null()),
            t.Key("units"): t.String(),
            t.Key("type"): t.String(),
            t.Key("is_model_specific"): t.Bool(),
            t.Key("directionality"): t.String(),
            t.Key("time_step"): t.String(),
            t.Key("created_at"): t.String(),
            t.Key("created_by"): t.Dict().allow_extra("*"),
            t.Key("name"): t.String(),
            t.Key(
                "description",
                optional=True,
            ): t.Or(t.String(allow_blank=True), t.Null()),
            t.Key("baseline_values", optional=True): t.Or(
                t.List(t.Dict().allow_extra("*")), t.Null()
            ),
            t.Key("timestamp", optional=True): t.Or(_timestamp, t.Null()),
            t.Key("value", optional=True): t.Or(_value, t.Null()),
            t.Key("sample_count", optional=True): t.Or(_sample_count, t.Null()),
            t.Key("batch", optional=True): t.Or(_batch, t.Null()),
            t.Key("parameter_overrides", optional=True): t.Or(
                t.List(_parameter_overrides), t.Null()
            ),
            t.Key("custom_job_id"): t.String(),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        deployment: Dict[str, Any],
        units: str,
        type: str,
        is_model_specific: bool,
        directionality: str,
        time_step: str,
        created_at: str,
        created_by: Dict[str, Any],
        name: str,
        custom_job_id: str,
        description: Optional[str] = None,
        schedule: Optional[Schedule] = None,
        baseline_values: Optional[List[Dict[str, Any]]] = None,
        timestamp: Optional[Dict[str, Any]] = None,
        value: Optional[Dict[str, Any]] = None,
        sample_count: Optional[Dict[str, Any]] = None,
        batch: Optional[Dict[str, Any]] = None,
        parameter_overrides: Optional[List[Dict[str, Any]]] = None,
    ):
        """

        Parameters
        ----------
        id: str
            ID of the hosted custom metric.
        deployment: Dict[str, Any]
            Deployment details.
        units: str
            Units of the metric.
        type: str
            Type of the metric.
        is_model_specific: bool
            Whether the metric is model specific.
        directionality: str
            Directionality of the metric.
        time_step: str
            Time step of the metric.
        created_at: str
            Creation time of the metric.
        created_by: Dict[str, Any]
            Creator details.
        name: str
            Name of the metric.
        custom_job_id: str
            ID of the custom job connected to this hosted custom metric
        description: Optional[str]
            Description of the metric.
        schedule: Optional[Dict[str, Any]]
            Schedule details.
        baseline_values: Optional[List[Dict[str, Any]]
            Baseline values.
        timestamp: Optional[Dict[str, Any]]
            Timestamp details.
        value: Optional[Dict[str, Any]]
            Value details.
        sample_count: Optional[Dict[str, Any]]
            Sample count details.
        batch: Optional[Dict[str, Any]]
            Batch details.
        parameter_overrides: Optional[List[Dict[str, Any]]
            Parameter overrides.
        """
        self.id = id
        self.deployment = DeploymentDetails(
            id=deployment["id"],
            name=deployment["name"],
            creator_first_name=deployment.get("creator_first_name"),
            creator_last_name=deployment.get("creator_last_name"),
            creator_username=deployment.get("creator_username"),
            creator_gravatar_hash=deployment.get("creator_gravatar_hash"),
            created_at=deployment.get("created_at"),
        )
        self.schedule = (
            Schedule(
                hour=schedule["hour"],
                minute=schedule["minute"],
                day_of_week=schedule["day_of_week"],
                day_of_month=schedule["day_of_month"],
                month=schedule["month"],
            )
            if schedule
            else None
        )
        self.units = units
        self.type = type
        self.is_model_specific = is_model_specific
        self.directionality = directionality
        self.time_step = time_step
        self.created_at = created_at
        self.created_by = created_by
        self.name = name
        self.custom_job_id = custom_job_id
        self.description = description
        self.baseline_values = (
            [MetricBaselineValue(**value) for value in baseline_values] if baseline_values else None
        )
        self.timestamp = (
            MetricTimestampSpoofing(
                column_name=timestamp["column_name"], time_format=timestamp.get("time_format")
            )
            if timestamp
            else None
        )
        self.value = ValueField(column_name=value["column_name"]) if value else None
        self.sample_count = (
            SampleCountField(column_name=sample_count["column_name"]) if sample_count else None
        )
        self.batch = BatchField(column_name=batch["column_name"]) if batch else None
        parameter_overrides = self._impute_null_runtime_parameter_values(parameter_overrides)
        self.parameter_overrides = (
            [
                RuntimeParameterValue(
                    field_name=param["field_name"], value=param["value"], type=param["type"]
                )
                for param in parameter_overrides
            ]
            if parameter_overrides
            else None
        )

    def _impute_null_runtime_parameter_values(
        self, values: Optional[List[Dict[str, Any]]]
    ) -> Optional[List[Dict[str, Any]]]:
        if not values:
            return values
        for param in values:
            if "value" not in values:
                param["value"] = None
        return values

    @classmethod
    def list(
        cls,
        job_id: str,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[HostedCustomMetric]:
        """List all hosted custom metrics for a job.

        Parameters
        ----------
        job_id: str
            ID of the job.

        Returns
        -------
        metrics: List[HostedCustomMetric]
        """
        params: Dict[str, Any] = {}
        if skip:
            params["skip"] = skip
        if limit:
            params["limit"] = limit
        response = cls._client.get(f"customJobs/{job_id}/customMetrics/", params=params)
        return [cls.from_server_data(d) for d in response.json()["data"]]

    @classmethod
    def create_from_template(
        cls,
        template_id: str,
        deployment_id: str,
        job_name: str,
        custom_metric_name: str,
        job_description: Optional[str] = None,
        custom_metric_description: Optional[str] = None,
        sidecar_deployment_id: Optional[str] = None,
        baseline_value: Optional[float] = None,
        timestamp: Optional[MetricTimestampSpoofing] = None,
        value: Optional[ValueField] = None,
        sample_count: Optional[SampleCountField] = None,
        batch: Optional[BatchField] = None,
        schedule: Optional[Schedule] = None,
        parameter_overrides: Optional[List[RuntimeParameterValue]] = None,
    ) -> HostedCustomMetric:
        """Create a hosted custom metric from a template.
        A shortcut for 2 calls:
        Job.from_custom_metric_template(template_id)
        HostedCustomMetrics.create_from_custom_job()

        Parameters
        ----------
        template_id: str
            ID of the template.
        deployment_id: str
            ID of the deployment.
        job_name: str
            Name of the job.
        custom_metric_name: str
            Name of the metric.
        job_description: Optional[str]
            Description of the job.
        custom_metric_description: Optional[str]
            Description of the metric.
        sidecar_deployment_id: Optional[str]
            ID of the sidecar deployment.
        baseline_value: Optional[float]
            Baseline value.
        timestamp: Optional[MetricTimestampSpoofing]
            Timestamp details.
        value: Optional[ValueField]
            Value details.
        sample_count: Optional[SampleCountField]
            Sample count details.
        batch: Optional[BatchField]
            Batch details.
        schedule: Optional[Schedule]
            Schedule details.
        parameter_overrides: Optional[List[RuntimeParameterValue]]
            Parameter overrides.

        Returns
        -------
        metric: HostedCustomMetric
        """
        job = Job.create_from_custom_metric_gallery_template(
            template_id=template_id,
            name=job_name,
            description=job_description,
            sidecar_deployment_id=sidecar_deployment_id,
        )
        hosted_custom_metric = cls.create_from_custom_job(
            custom_job_id=job.id,
            deployment_id=deployment_id,
            name=custom_metric_name,
            description=custom_metric_description,
            baseline_value=baseline_value,
            timestamp=timestamp,
            value=value,
            sample_count=sample_count,
            batch=batch,
            schedule=schedule,
            parameter_overrides=parameter_overrides,
        )
        return hosted_custom_metric

    @classmethod
    def create_from_custom_job(
        cls,
        custom_job_id: str,
        deployment_id: str,
        name: str,
        description: Optional[str] = None,
        baseline_value: Optional[float] = None,
        timestamp: Optional[MetricTimestampSpoofing] = None,
        value: Optional[ValueField] = None,
        sample_count: Optional[SampleCountField] = None,
        batch: Optional[BatchField] = None,
        schedule: Optional[Schedule] = None,
        parameter_overrides: Optional[List[RuntimeParameterValue]] = None,
        geospatial_segment_attribute: Optional[str] = None,
    ) -> HostedCustomMetric:
        """Create a hosted custom metric from existing custom job.

        Parameters
        ----------
        custom_job_id: str
            ID of the custom job.
        deployment_id: str
            ID of the deployment.
        name: str
            Name of the metric.
        description: Optional[str]
            Description of the metric.
        baseline_value: Optional[float]
            Baseline value.
        timestamp: Optional[MetricTimestampSpoofing]
            Timestamp details.
        value: Optional[ValueField]
            Value details.
        sample_count: Optional[SampleCountField]
            Sample count details.
        batch: Optional[BatchField]
            Batch details.
        schedule: Optional[Schedule]
            Schedule details.
        parameter_overrides: Optional[List[RuntimeParameterValue]]
            Parameter overrides.
        geospatial_segment_attribute: Optional[str]
            The name of the geospatial segment attribute. Only applicable for geospatial custom metrics.

        Returns
        -------
        metric: HostedCustomMetric

        """
        url = f"deployments/{deployment_id}/customMetrics/fromCustomJob/"
        payload: Dict[str, Any] = {
            "customJobId": custom_job_id,
            "name": name,
        }
        if description:
            payload["description"] = description
        if timestamp:
            payload["timestamp"] = {"columnName": timestamp.column_name}
            if timestamp.time_format:
                payload["timestamp"]["timeFormat"] = timestamp.time_format
        if value:
            payload["value"] = {"columnName": value.column_name}
        if baseline_value:
            payload["baselineValues"] = [{"value": baseline_value}]
        if sample_count:
            payload["sampleCount"] = {"columnName": sample_count.column_name}
        if batch:
            payload["batch"] = {"columnName": batch.column_name}
        if schedule:
            payload["schedule"] = to_api(schedule)
        if parameter_overrides:
            payload["parameterOverrides"] = [
                {"fieldName": param.field_name, "value": param.value, "type": param.type}
                for param in parameter_overrides
            ]
        if geospatial_segment_attribute:
            payload["geospatialSegmentAttribute"] = geospatial_segment_attribute
        result = cls._client.post(url, json=payload)
        return cls.from_server_data(result.json())

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        units: Optional[str] = None,
        directionality: Optional[str] = None,
        aggregation_type: Optional[CustomMetricAggregationType] = None,
        baseline_value: Optional[List[float]] = None,
        timestamp: Optional[MetricTimestampSpoofing] = None,
        value: Optional[ValueField] = None,
        sample_count: Optional[SampleCountField] = None,
        batch: Optional[BatchField] = None,
        schedule: Optional[Schedule] = None,
        parameter_overrides: Optional[List[RuntimeParameterValue]] = None,
    ) -> HostedCustomMetric:
        """Update the hosted custom metric.

        Parameters
        ----------
        name: Optional[str]
            Name of the metric.
        description: Optional[str]
            Description of the metric.
        units: Optional[str]
            Units of the metric.
        directionality: Optional[str]
            Directionality of the metric.
        aggregation_type: Optional[CustomMetricAggregationType]
            Aggregation type of the metric.
        baseline_value: Optional[float]
            Baseline values.
        timestamp: Optional[MetricTimestampSpoofing]
            Timestamp details.
        value: Optional[ValueField]
            Value details.
        sample_count: Optional[SampleCountField]
            Sample count details.
        batch: Optional[BatchField]
            Batch details.
        schedule: Optional[Schedule]
            Schedule details.
        parameter_overrides: Optional[List[RuntimeParameterValue]]
            Parameter overrides.

        Returns
        -------
        metric: HostedCustomMetric
        """
        url = f"customJobs/{self.custom_job_id}/customMetrics/{self.id}/"
        payload: Dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if units:
            payload["units"] = units
        if directionality:
            payload["directionality"] = directionality
        if aggregation_type:
            payload["aggregationType"] = aggregation_type
        if baseline_value:
            payload["baselineValues"] = [{"value": baseline_value}]
        if timestamp:
            payload["timestamp"] = {"columnName": timestamp.column_name}
            if timestamp.time_format:
                payload["timestamp"]["timeFormat"] = timestamp.time_format
        if value:
            payload["value"] = {"columnName": value.column_name}
        if sample_count:
            payload["sampleCount"] = {"columnName": sample_count.column_name}
        if batch:
            payload["batch"] = {"columnName": batch.column_name}
        if schedule:
            payload["schedule"] = schedule
        if parameter_overrides:
            payload["parameter_overrides"] = [
                {"fieldName": param.field_name, "value": param.value, "type": param.type}
                for param in parameter_overrides
            ]

        response = self._client.patch(url, json=payload)
        return self.from_server_data(response.json())

    def delete(self) -> None:
        """Delete the hosted custom metric."""
        url = f"customJobs/{self.custom_job_id}/customMetrics/{self.id}/"
        self._client.delete(url)


class HostedCustomMetricBlueprint(APIObject):
    """
    Hosted custom metric blueprints provide an option to share custom metric settings between multiple
    custom metrics sharing the same custom jobs. When a custom job of a hosted custom metric type is connected to the
    deployment, all the custom metric parameters from the blueprint are automatically copied.
    """

    _categories = t.Dict(
        {
            t.Key("directionality"): t.String,
            t.Key("value"): t.String,
            t.Key("baseline_count", optional=True): t.Or(t.Int, t.Null),
        }
    ).allow_extra("*")
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("directionality"): t.String(),
            t.Key("units"): t.String(),
            t.Key("type"): t.String(),
            t.Key("time_step"): t.String(),
            t.Key("is_model_specific"): t.Bool(),
            t.Key("categories", optional=True): t.Or(t.List(_categories), t.Null),
            t.Key("custom_job_id"): t.String(),
            t.Key("created_at"): t.String(),
            t.Key("updated_at"): t.String(),
            t.Key("created_by"): t.String(),
            t.Key("updated_by"): t.String(),
            t.Key("is_geospatial", optional=True): t.Or(t.Bool, t.Null()),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        directionality: str,
        units: str,
        type: str,
        time_step: str,
        is_model_specific: bool,
        custom_job_id: str,
        created_at: str,
        updated_at: str,
        created_by: str,
        updated_by: str,
        categories: Optional[List[Dict[str, Any]]] = None,
        is_geospatial: Optional[bool] = None,
    ):
        """
        Parameters
        ----------
        id: str
            ID of the hosted custom metric blueprint.
        directionality: str
            Directionality of the metric.
        units: str
            Units of the metric.
        type: str
            Type of the metric.
        time_step: str
            Time step of the metric.
        is_model_specific: bool
            Sets whether the metric is model specific.
        custom_job_id: str
            ID of the custom job connected to this hosted custom metric
        categories: List[Dict]
            Custom metric categories.
        created_at: str
            Creation time of the metric.
        updated_at: str
            Update time of the metric.
        created_by: str
            Creator of the metric.
        updated_by: str
            Updater of the metric.
        is_geospatial: Optional[bool]
            Determines whether the metric is geospatial.

        """
        self.id = id
        self.units = units
        self.type = type
        self.is_model_specific = is_model_specific
        self.directionality = directionality
        self.time_step = time_step
        self.custom_job_id = custom_job_id
        self.categories = categories
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by
        self.is_geospatial = is_geospatial

    @classmethod
    def get(cls, custom_job_id: str) -> HostedCustomMetricBlueprint:
        """Get a hosted custom metric blueprint.

        Parameters
        ----------
        custom_job_id: str
            ID of the custom job.

        Returns
        -------
        blueprint: HostedCustomMetricBlueprint
        """
        url = f"customJobs/{custom_job_id}/hostedCustomMetricTemplate/"
        response = cls._client.get(url)
        return cls.from_server_data(response.json())

    @classmethod
    def create(
        cls,
        custom_job_id: str,
        directionality: str,
        units: str,
        type: str,
        time_step: str,
        is_model_specific: bool,
        is_geospatial: Optional[bool] = None,
    ) -> HostedCustomMetricBlueprint:
        """Create a hosted custom metric blueprint.

        Parameters
        ----------
        custom_job_id: str
            ID of the custom job.
        directionality: str
            Directionality of the metric.
        units: str
            Units of the metric.
        type: str
            Type of the metric.
        time_step: str
            Time step of the metric.
        is_model_specific: bool
            Whether the metric is model specific.
        is_geospatial: Optional[bool]
            Determines whether the metric is geospatial.

        Returns
        -------
        blueprint: HostedCustomMetricBlueprint
        """
        url = f"customJobs/{custom_job_id}/hostedCustomMetricTemplate/"
        payload = {
            "directionality": directionality,
            "units": units,
            "type": type,
            "timeStep": time_step,
            "isModelSpecific": is_model_specific,
        }
        if is_geospatial:
            payload["isGeospatial"] = is_geospatial
        response = cls._client.post(url, json=payload)
        return cls.from_server_data(response.json())

    def update(
        self,
        directionality: Optional[str] = None,
        units: Optional[str] = None,
        type: Optional[str] = None,
        time_step: Optional[str] = None,
        is_model_specific: Optional[bool] = None,
        is_geospatial: Optional[bool] = None,
    ) -> HostedCustomMetricBlueprint:
        """Update a hosted custom metric blueprint.

        Parameters
        ----------
        directionality: Optional[str]
            Directionality of the metric.
        units: Optional[str]
            Units of the metric.
        type: Optional[str]
            Type of the metric.
        time_step: Optional[str]
            Time step of the metric.
        is_model_specific: Optional[bool]
            Determines whether the metric is model specific.
        is_geospatial: Optional[bool]
            Determines whether the metric is geospatial.

        Returns
        -------
        updated_blueprint: HostedCustomMetricBlueprint

        """
        url = f"customJobs/{self.custom_job_id}/hostedCustomMetricTemplate/"
        payload: Dict[str, Any] = {}
        if directionality:
            payload["directionality"] = directionality
        if units:
            payload["units"] = units
        if type:
            payload["type"] = type
        if time_step:
            payload["timeStep"] = time_step
        if is_model_specific:
            payload["isModelSpecific"] = is_model_specific
        if is_geospatial:
            payload["isGeospatial"] = is_geospatial
        response = self._client.patch(url, json=payload)
        return self.from_server_data(response.json())
