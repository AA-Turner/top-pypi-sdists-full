"""
Type annotations for codeguruprofiler service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguruprofiler.client import CodeGuruProfilerClient

    session = get_session()
    async with session.create_client("codeguruprofiler") as client:
        client: CodeGuruProfilerClient
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

from .paginator import ListProfileTimesPaginator
from .type_defs import (
    AddNotificationChannelsRequestTypeDef,
    AddNotificationChannelsResponseTypeDef,
    BatchGetFrameMetricDataRequestTypeDef,
    BatchGetFrameMetricDataResponseTypeDef,
    ConfigureAgentRequestTypeDef,
    ConfigureAgentResponseTypeDef,
    CreateProfilingGroupRequestTypeDef,
    CreateProfilingGroupResponseTypeDef,
    DeleteProfilingGroupRequestTypeDef,
    DescribeProfilingGroupRequestTypeDef,
    DescribeProfilingGroupResponseTypeDef,
    GetFindingsReportAccountSummaryRequestTypeDef,
    GetFindingsReportAccountSummaryResponseTypeDef,
    GetNotificationConfigurationRequestTypeDef,
    GetNotificationConfigurationResponseTypeDef,
    GetPolicyRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetProfileRequestTypeDef,
    GetProfileResponseTypeDef,
    GetRecommendationsRequestTypeDef,
    GetRecommendationsResponseTypeDef,
    ListFindingsReportsRequestTypeDef,
    ListFindingsReportsResponseTypeDef,
    ListProfileTimesRequestTypeDef,
    ListProfileTimesResponseTypeDef,
    ListProfilingGroupsRequestTypeDef,
    ListProfilingGroupsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PostAgentProfileRequestTypeDef,
    PutPermissionRequestTypeDef,
    PutPermissionResponseTypeDef,
    RemoveNotificationChannelRequestTypeDef,
    RemoveNotificationChannelResponseTypeDef,
    RemovePermissionRequestTypeDef,
    RemovePermissionResponseTypeDef,
    SubmitFeedbackRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateProfilingGroupRequestTypeDef,
    UpdateProfilingGroupResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("CodeGuruProfilerClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CodeGuruProfilerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeGuruProfilerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#generate_presigned_url)
        """

    async def add_notification_channels(
        self, **kwargs: Unpack[AddNotificationChannelsRequestTypeDef]
    ) -> AddNotificationChannelsResponseTypeDef:
        """
        Add up to 2 anomaly notifications channels for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/add_notification_channels.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#add_notification_channels)
        """

    async def batch_get_frame_metric_data(
        self, **kwargs: Unpack[BatchGetFrameMetricDataRequestTypeDef]
    ) -> BatchGetFrameMetricDataResponseTypeDef:
        """
        Returns the time series of values for a requested list of frame metrics from a
        time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/batch_get_frame_metric_data.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#batch_get_frame_metric_data)
        """

    async def configure_agent(
        self, **kwargs: Unpack[ConfigureAgentRequestTypeDef]
    ) -> ConfigureAgentResponseTypeDef:
        """
        Used by profiler agents to report their current state and to receive remote
        configuration updates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/configure_agent.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#configure_agent)
        """

    async def create_profiling_group(
        self, **kwargs: Unpack[CreateProfilingGroupRequestTypeDef]
    ) -> CreateProfilingGroupResponseTypeDef:
        """
        Creates a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/create_profiling_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#create_profiling_group)
        """

    async def delete_profiling_group(
        self, **kwargs: Unpack[DeleteProfilingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/delete_profiling_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#delete_profiling_group)
        """

    async def describe_profiling_group(
        self, **kwargs: Unpack[DescribeProfilingGroupRequestTypeDef]
    ) -> DescribeProfilingGroupResponseTypeDef:
        """
        Returns a <a
        href="https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ProfilingGroupDescription.html">
        <code>ProfilingGroupDescription</code> </a> object that contains information
        about the requested profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/describe_profiling_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#describe_profiling_group)
        """

    async def get_findings_report_account_summary(
        self, **kwargs: Unpack[GetFindingsReportAccountSummaryRequestTypeDef]
    ) -> GetFindingsReportAccountSummaryResponseTypeDef:
        """
        Returns a list of <a
        href="https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_FindingsReportSummary.html">
        <code>FindingsReportSummary</code> </a> objects that contain analysis results
        for all profiling groups in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/get_findings_report_account_summary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_findings_report_account_summary)
        """

    async def get_notification_configuration(
        self, **kwargs: Unpack[GetNotificationConfigurationRequestTypeDef]
    ) -> GetNotificationConfigurationResponseTypeDef:
        """
        Get the current configuration for anomaly notifications for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/get_notification_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_notification_configuration)
        """

    async def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Returns the JSON-formatted resource-based policy on a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/get_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_policy)
        """

    async def get_profile(
        self, **kwargs: Unpack[GetProfileRequestTypeDef]
    ) -> GetProfileResponseTypeDef:
        """
        Gets the aggregated profile of a profiling group for a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/get_profile.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_profile)
        """

    async def get_recommendations(
        self, **kwargs: Unpack[GetRecommendationsRequestTypeDef]
    ) -> GetRecommendationsResponseTypeDef:
        """
        Returns a list of <a
        href="https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_Recommendation.html">
        <code>Recommendation</code> </a> objects that contain recommendations for a
        profiling group for a given time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/get_recommendations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_recommendations)
        """

    async def list_findings_reports(
        self, **kwargs: Unpack[ListFindingsReportsRequestTypeDef]
    ) -> ListFindingsReportsResponseTypeDef:
        """
        List the available reports for a given profiling group and time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/list_findings_reports.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_findings_reports)
        """

    async def list_profile_times(
        self, **kwargs: Unpack[ListProfileTimesRequestTypeDef]
    ) -> ListProfileTimesResponseTypeDef:
        """
        Lists the start times of the available aggregated profiles of a profiling group
        for an aggregation period within the specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/list_profile_times.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_profile_times)
        """

    async def list_profiling_groups(
        self, **kwargs: Unpack[ListProfilingGroupsRequestTypeDef]
    ) -> ListProfilingGroupsResponseTypeDef:
        """
        Returns a list of profiling groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/list_profiling_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_profiling_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags that are assigned to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_tags_for_resource)
        """

    async def post_agent_profile(
        self, **kwargs: Unpack[PostAgentProfileRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Submits profiling data to an aggregated profile of a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/post_agent_profile.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#post_agent_profile)
        """

    async def put_permission(
        self, **kwargs: Unpack[PutPermissionRequestTypeDef]
    ) -> PutPermissionResponseTypeDef:
        """
        Adds permissions to a profiling group's resource-based policy that are provided
        using an action group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/put_permission.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#put_permission)
        """

    async def remove_notification_channel(
        self, **kwargs: Unpack[RemoveNotificationChannelRequestTypeDef]
    ) -> RemoveNotificationChannelResponseTypeDef:
        """
        Remove one anomaly notifications channel for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/remove_notification_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#remove_notification_channel)
        """

    async def remove_permission(
        self, **kwargs: Unpack[RemovePermissionRequestTypeDef]
    ) -> RemovePermissionResponseTypeDef:
        """
        Removes permissions from a profiling group's resource-based policy that are
        provided using an action group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/remove_permission.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#remove_permission)
        """

    async def submit_feedback(
        self, **kwargs: Unpack[SubmitFeedbackRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sends feedback to CodeGuru Profiler about whether the anomaly detected by the
        analysis is useful or not.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/submit_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#submit_feedback)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Use to assign one or more tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Use to remove one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#untag_resource)
        """

    async def update_profiling_group(
        self, **kwargs: Unpack[UpdateProfilingGroupRequestTypeDef]
    ) -> UpdateProfilingGroupResponseTypeDef:
        """
        Updates a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/update_profiling_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#update_profiling_group)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_profile_times"]
    ) -> ListProfileTimesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
        """
