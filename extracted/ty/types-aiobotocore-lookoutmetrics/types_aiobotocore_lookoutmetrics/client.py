"""
Type annotations for lookoutmetrics service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutmetrics.client import LookoutMetricsClient

    session = get_session()
    async with session.create_client("lookoutmetrics") as client:
        client: LookoutMetricsClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    ActivateAnomalyDetectorRequestTypeDef,
    BackTestAnomalyDetectorRequestTypeDef,
    CreateAlertRequestTypeDef,
    CreateAlertResponseTypeDef,
    CreateAnomalyDetectorRequestTypeDef,
    CreateAnomalyDetectorResponseTypeDef,
    CreateMetricSetRequestTypeDef,
    CreateMetricSetResponseTypeDef,
    DeactivateAnomalyDetectorRequestTypeDef,
    DeleteAlertRequestTypeDef,
    DeleteAnomalyDetectorRequestTypeDef,
    DescribeAlertRequestTypeDef,
    DescribeAlertResponseTypeDef,
    DescribeAnomalyDetectionExecutionsRequestTypeDef,
    DescribeAnomalyDetectionExecutionsResponseTypeDef,
    DescribeAnomalyDetectorRequestTypeDef,
    DescribeAnomalyDetectorResponseTypeDef,
    DescribeMetricSetRequestTypeDef,
    DescribeMetricSetResponseTypeDef,
    DetectMetricSetConfigRequestTypeDef,
    DetectMetricSetConfigResponseTypeDef,
    GetAnomalyGroupRequestTypeDef,
    GetAnomalyGroupResponseTypeDef,
    GetDataQualityMetricsRequestTypeDef,
    GetDataQualityMetricsResponseTypeDef,
    GetFeedbackRequestTypeDef,
    GetFeedbackResponseTypeDef,
    GetSampleDataRequestTypeDef,
    GetSampleDataResponseTypeDef,
    ListAlertsRequestTypeDef,
    ListAlertsResponseTypeDef,
    ListAnomalyDetectorsRequestTypeDef,
    ListAnomalyDetectorsResponseTypeDef,
    ListAnomalyGroupRelatedMetricsRequestTypeDef,
    ListAnomalyGroupRelatedMetricsResponseTypeDef,
    ListAnomalyGroupSummariesRequestTypeDef,
    ListAnomalyGroupSummariesResponseTypeDef,
    ListAnomalyGroupTimeSeriesRequestTypeDef,
    ListAnomalyGroupTimeSeriesResponseTypeDef,
    ListMetricSetsRequestTypeDef,
    ListMetricSetsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutFeedbackRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAlertRequestTypeDef,
    UpdateAlertResponseTypeDef,
    UpdateAnomalyDetectorRequestTypeDef,
    UpdateAnomalyDetectorResponseTypeDef,
    UpdateMetricSetRequestTypeDef,
    UpdateMetricSetResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("LookoutMetricsClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LookoutMetricsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutMetricsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#generate_presigned_url)
        """

    async def activate_anomaly_detector(
        self, **kwargs: Unpack[ActivateAnomalyDetectorRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Activates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/activate_anomaly_detector.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#activate_anomaly_detector)
        """

    async def back_test_anomaly_detector(
        self, **kwargs: Unpack[BackTestAnomalyDetectorRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Runs a backtest for anomaly detection for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/back_test_anomaly_detector.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#back_test_anomaly_detector)
        """

    async def create_alert(
        self, **kwargs: Unpack[CreateAlertRequestTypeDef]
    ) -> CreateAlertResponseTypeDef:
        """
        Creates an alert for an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/create_alert.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#create_alert)
        """

    async def create_anomaly_detector(
        self, **kwargs: Unpack[CreateAnomalyDetectorRequestTypeDef]
    ) -> CreateAnomalyDetectorResponseTypeDef:
        """
        Creates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/create_anomaly_detector.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#create_anomaly_detector)
        """

    async def create_metric_set(
        self, **kwargs: Unpack[CreateMetricSetRequestTypeDef]
    ) -> CreateMetricSetResponseTypeDef:
        """
        Creates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/create_metric_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#create_metric_set)
        """

    async def deactivate_anomaly_detector(
        self, **kwargs: Unpack[DeactivateAnomalyDetectorRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deactivates an anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/deactivate_anomaly_detector.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#deactivate_anomaly_detector)
        """

    async def delete_alert(self, **kwargs: Unpack[DeleteAlertRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/delete_alert.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#delete_alert)
        """

    async def delete_anomaly_detector(
        self, **kwargs: Unpack[DeleteAnomalyDetectorRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/delete_anomaly_detector.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#delete_anomaly_detector)
        """

    async def describe_alert(
        self, **kwargs: Unpack[DescribeAlertRequestTypeDef]
    ) -> DescribeAlertResponseTypeDef:
        """
        Describes an alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_alert.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_alert)
        """

    async def describe_anomaly_detection_executions(
        self, **kwargs: Unpack[DescribeAnomalyDetectionExecutionsRequestTypeDef]
    ) -> DescribeAnomalyDetectionExecutionsResponseTypeDef:
        """
        Returns information about the status of the specified anomaly detection jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_anomaly_detection_executions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_anomaly_detection_executions)
        """

    async def describe_anomaly_detector(
        self, **kwargs: Unpack[DescribeAnomalyDetectorRequestTypeDef]
    ) -> DescribeAnomalyDetectorResponseTypeDef:
        """
        Describes a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_anomaly_detector.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_anomaly_detector)
        """

    async def describe_metric_set(
        self, **kwargs: Unpack[DescribeMetricSetRequestTypeDef]
    ) -> DescribeMetricSetResponseTypeDef:
        """
        Describes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/describe_metric_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#describe_metric_set)
        """

    async def detect_metric_set_config(
        self, **kwargs: Unpack[DetectMetricSetConfigRequestTypeDef]
    ) -> DetectMetricSetConfigResponseTypeDef:
        """
        Detects an Amazon S3 dataset's file format, interval, and offset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/detect_metric_set_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#detect_metric_set_config)
        """

    async def get_anomaly_group(
        self, **kwargs: Unpack[GetAnomalyGroupRequestTypeDef]
    ) -> GetAnomalyGroupResponseTypeDef:
        """
        Returns details about a group of anomalous metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_anomaly_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_anomaly_group)
        """

    async def get_data_quality_metrics(
        self, **kwargs: Unpack[GetDataQualityMetricsRequestTypeDef]
    ) -> GetDataQualityMetricsResponseTypeDef:
        """
        Returns details about the requested data quality metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_data_quality_metrics.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_data_quality_metrics)
        """

    async def get_feedback(
        self, **kwargs: Unpack[GetFeedbackRequestTypeDef]
    ) -> GetFeedbackResponseTypeDef:
        """
        Get feedback for an anomaly group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_feedback)
        """

    async def get_sample_data(
        self, **kwargs: Unpack[GetSampleDataRequestTypeDef]
    ) -> GetSampleDataResponseTypeDef:
        """
        Returns a selection of sample records from an Amazon S3 datasource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/get_sample_data.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#get_sample_data)
        """

    async def list_alerts(
        self, **kwargs: Unpack[ListAlertsRequestTypeDef]
    ) -> ListAlertsResponseTypeDef:
        """
        Lists the alerts attached to a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_alerts.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_alerts)
        """

    async def list_anomaly_detectors(
        self, **kwargs: Unpack[ListAnomalyDetectorsRequestTypeDef]
    ) -> ListAnomalyDetectorsResponseTypeDef:
        """
        Lists the detectors in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_detectors.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_detectors)
        """

    async def list_anomaly_group_related_metrics(
        self, **kwargs: Unpack[ListAnomalyGroupRelatedMetricsRequestTypeDef]
    ) -> ListAnomalyGroupRelatedMetricsResponseTypeDef:
        """
        Returns a list of measures that are potential causes or effects of an anomaly
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_group_related_metrics.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_group_related_metrics)
        """

    async def list_anomaly_group_summaries(
        self, **kwargs: Unpack[ListAnomalyGroupSummariesRequestTypeDef]
    ) -> ListAnomalyGroupSummariesResponseTypeDef:
        """
        Returns a list of anomaly groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_group_summaries.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_group_summaries)
        """

    async def list_anomaly_group_time_series(
        self, **kwargs: Unpack[ListAnomalyGroupTimeSeriesRequestTypeDef]
    ) -> ListAnomalyGroupTimeSeriesResponseTypeDef:
        """
        Gets a list of anomalous metrics for a measure in an anomaly group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_anomaly_group_time_series.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_anomaly_group_time_series)
        """

    async def list_metric_sets(
        self, **kwargs: Unpack[ListMetricSetsRequestTypeDef]
    ) -> ListMetricSetsResponseTypeDef:
        """
        Lists the datasets in the current AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_metric_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_metric_sets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of <a
        href="https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html">tags</a>
        for a detector, dataset, or alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#list_tags_for_resource)
        """

    async def put_feedback(self, **kwargs: Unpack[PutFeedbackRequestTypeDef]) -> Dict[str, Any]:
        """
        Add feedback for an anomalous metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/put_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#put_feedback)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds <a
        href="https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html">tags</a>
        to a detector, dataset, or alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes <a
        href="https://docs.aws.amazon.com/lookoutmetrics/latest/dev/detectors-tags.html">tags</a>
        from a detector, dataset, or alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#untag_resource)
        """

    async def update_alert(
        self, **kwargs: Unpack[UpdateAlertRequestTypeDef]
    ) -> UpdateAlertResponseTypeDef:
        """
        Make changes to an existing alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/update_alert.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#update_alert)
        """

    async def update_anomaly_detector(
        self, **kwargs: Unpack[UpdateAnomalyDetectorRequestTypeDef]
    ) -> UpdateAnomalyDetectorResponseTypeDef:
        """
        Updates a detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/update_anomaly_detector.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#update_anomaly_detector)
        """

    async def update_metric_set(
        self, **kwargs: Unpack[UpdateMetricSetRequestTypeDef]
    ) -> UpdateMetricSetResponseTypeDef:
        """
        Updates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics/client/update_metric_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/#update_metric_set)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutmetrics.html#LookoutMetrics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutmetrics/client/)
        """
