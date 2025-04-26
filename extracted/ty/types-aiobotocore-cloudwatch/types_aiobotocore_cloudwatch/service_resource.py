"""
Type annotations for cloudwatch service ServiceResource.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudwatch.service_resource import CloudWatchServiceResource
    import types_aiobotocore_cloudwatch.service_resource as cloudwatch_resources

    session = get_session()
    async with session.resource("cloudwatch") as resource:
        resource: CloudWatchServiceResource

        my_alarm: cloudwatch_resources.Alarm = resource.Alarm(...)
        my_metric: cloudwatch_resources.Metric = resource.Metric(...)
```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import NoReturn

from aioboto3.resources.base import AIOBoto3ServiceResource
from aioboto3.resources.collection import AIOResourceCollection

from .client import CloudWatchClient
from .literals import (
    AlarmTypeType,
    ComparisonOperatorType,
    StandardUnitType,
    StateValueType,
    StatisticType,
)
from .type_defs import (
    DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef,
    DescribeAlarmHistoryOutputTypeDef,
    DimensionFilterTypeDef,
    DimensionTypeDef,
    GetMetricStatisticsInputMetricGetStatisticsTypeDef,
    GetMetricStatisticsOutputTypeDef,
    MetricDataQueryAlarmTypeDef,
    PutMetricAlarmInputMetricPutAlarmTypeDef,
    PutMetricDataInputMetricPutDataTypeDef,
    SetAlarmStateInputAlarmSetStateTypeDef,
)

try:
    from boto3.resources.base import ResourceMeta
except ImportError:
    from builtins import object as ResourceMeta  # type: ignore[assignment]
if sys.version_info >= (3, 9):
    from builtins import list as List
    from collections.abc import AsyncIterator, Awaitable, Sequence
else:
    from typing import AsyncIterator, Awaitable, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = (
    "Alarm",
    "CloudWatchServiceResource",
    "Metric",
    "MetricAlarmsCollection",
    "ServiceResourceAlarmsCollection",
    "ServiceResourceMetricsCollection",
)


class ServiceResourceAlarmsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#CloudWatch.ServiceResource.alarms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
    """

    def all(self) -> ServiceResourceAlarmsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#CloudWatch.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        AlarmNames: Sequence[str] = ...,
        AlarmNamePrefix: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        ChildrenOfAlarmName: str = ...,
        ParentsOfAlarmName: str = ...,
        StateValue: StateValueType = ...,
        ActionPrefix: str = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
    ) -> ServiceResourceAlarmsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    async def delete(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    async def disable_actions(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#disable_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    async def enable_actions(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#enable_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def limit(self, count: int) -> ServiceResourceAlarmsCollection:
        """
        Return at most this many Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def page_size(self, count: int) -> ServiceResourceAlarmsCollection:
        """
        Fetch at most this many Alarms per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Alarm]]:
        """
        A generator which yields pages of Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """

    def __aiter__(self) -> AsyncIterator[Alarm]:
        """
        A generator which yields Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/alarms.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcealarmscollection)
        """


class ServiceResourceMetricsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#CloudWatch.ServiceResource.metrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
    """

    def all(self) -> ServiceResourceMetricsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#CloudWatch.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        Namespace: str = ...,
        MetricName: str = ...,
        Dimensions: Sequence[DimensionFilterTypeDef] = ...,
        NextToken: str = ...,
        RecentlyActive: Literal["PT3H"] = ...,
        IncludeLinkedAccounts: bool = ...,
        OwningAccount: str = ...,
    ) -> ServiceResourceMetricsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def limit(self, count: int) -> ServiceResourceMetricsCollection:
        """
        Return at most this many Metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def page_size(self, count: int) -> ServiceResourceMetricsCollection:
        """
        Fetch at most this many Metrics per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Metric]]:
        """
        A generator which yields pages of Metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """

    def __aiter__(self) -> AsyncIterator[Metric]:
        """
        A generator which yields Metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/metrics.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#serviceresourcemetricscollection)
        """


class MetricAlarmsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#CloudWatch.Metric.alarms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
    """

    def all(self) -> MetricAlarmsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#CloudWatch.Metric.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    def filter(  # type: ignore[override]
        self,
        *,
        Statistic: StatisticType = ...,
        ExtendedStatistic: str = ...,
        Dimensions: Sequence[DimensionTypeDef] = ...,
        Period: int = ...,
        Unit: StandardUnitType = ...,
    ) -> MetricAlarmsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    async def delete(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    async def disable_actions(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#disable_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    async def enable_actions(self) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#enable_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    def limit(self, count: int) -> MetricAlarmsCollection:
        """
        Return at most this many Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    def page_size(self, count: int) -> MetricAlarmsCollection:
        """
        Fetch at most this many Alarms per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Alarm]]:
        """
        A generator which yields pages of Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """

    def __aiter__(self) -> AsyncIterator[Alarm]:
        """
        A generator which yields Alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/alarms.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricalarms)
        """


class Alarm(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/index.html#CloudWatch.Alarm)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarm)
    """

    name: str
    metric: Metric
    alarm_name: Awaitable[str]
    alarm_arn: Awaitable[str]
    alarm_description: Awaitable[str]
    alarm_configuration_updated_timestamp: Awaitable[datetime]
    actions_enabled: Awaitable[bool]
    ok_actions: Awaitable[List[str]]
    alarm_actions: Awaitable[List[str]]
    insufficient_data_actions: Awaitable[List[str]]
    state_value: Awaitable[StateValueType]
    state_reason: Awaitable[str]
    state_reason_data: Awaitable[str]
    state_updated_timestamp: Awaitable[datetime]
    metric_name: Awaitable[str]
    namespace: Awaitable[str]
    statistic: Awaitable[StatisticType]
    extended_statistic: Awaitable[str]
    dimensions: Awaitable[List[DimensionTypeDef]]
    period: Awaitable[int]
    unit: Awaitable[StandardUnitType]
    evaluation_periods: Awaitable[int]
    datapoints_to_alarm: Awaitable[int]
    threshold: Awaitable[float]
    comparison_operator: Awaitable[ComparisonOperatorType]
    treat_missing_data: Awaitable[str]
    evaluate_low_sample_count_percentile: Awaitable[str]
    metrics: Awaitable[List[MetricDataQueryAlarmTypeDef]]
    threshold_metric_id: Awaitable[str]
    evaluation_state: Awaitable[Literal["PARTIAL_DATA"]]
    state_transitioned_timestamp: Awaitable[datetime]
    meta: CloudWatchResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmget_available_subresources-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmdelete-method)
        """

    async def describe_history(
        self, **kwargs: Unpack[DescribeAlarmHistoryInputAlarmDescribeHistoryTypeDef]
    ) -> DescribeAlarmHistoryOutputTypeDef:
        """
        Retrieves the history for the specified alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/describe_history.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmdescribe_history-method)
        """

    async def disable_actions(self) -> None:
        """
        Disables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/disable_actions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmdisable_actions-method)
        """

    async def enable_actions(self) -> None:
        """
        Enables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/enable_actions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmenable_actions-method)
        """

    async def set_state(self, **kwargs: Unpack[SetAlarmStateInputAlarmSetStateTypeDef]) -> None:
        """
        Temporarily sets the state of an alarm for testing purposes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/set_state.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmset_state-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/alarm/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#alarmreload-method)
        """


_Alarm = Alarm


class Metric(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/index.html#CloudWatch.Metric)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metric)
    """

    namespace: str
    name: str
    alarms: MetricAlarmsCollection
    metric_name: Awaitable[str]
    dimensions: Awaitable[List[DimensionTypeDef]]
    meta: CloudWatchResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricget_available_subresources-method)
        """

    async def get_statistics(
        self, **kwargs: Unpack[GetMetricStatisticsInputMetricGetStatisticsTypeDef]
    ) -> GetMetricStatisticsOutputTypeDef:
        """
        Gets statistics for the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/get_statistics.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricget_statistics-method)
        """

    async def put_alarm(self, **kwargs: Unpack[PutMetricAlarmInputMetricPutAlarmTypeDef]) -> _Alarm:
        """
        Creates or updates an alarm and associates it with the specified metric, metric
        math expression, anomaly detection model, or Metrics Insights query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/put_alarm.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricput_alarm-method)
        """

    async def put_data(self, **kwargs: Unpack[PutMetricDataInputMetricPutDataTypeDef]) -> None:
        """
        Publishes metric data to Amazon CloudWatch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/put_data.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricput_data-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/metric/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#metricreload-method)
        """


_Metric = Metric


class CloudWatchResourceMeta(ResourceMeta):
    client: CloudWatchClient  # type: ignore[override]


class CloudWatchServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/index.html)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/)
    """

    meta: CloudWatchResourceMeta  # type: ignore[override]
    alarms: ServiceResourceAlarmsCollection
    metrics: ServiceResourceMetricsCollection

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#cloudwatchserviceresourceget_available_subresources-method)
        """

    async def Alarm(self, name: str) -> _Alarm:
        """
        Creates a Alarm resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/Alarm.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#cloudwatchserviceresourcealarm-method)
        """

    async def Metric(self, namespace: str, name: str) -> _Metric:
        """
        Creates a Metric resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/service-resource/Metric.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/service_resource/#cloudwatchserviceresourcemetric-method)
        """
