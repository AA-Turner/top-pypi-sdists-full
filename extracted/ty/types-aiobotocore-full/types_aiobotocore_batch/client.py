"""
Type annotations for batch service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_batch.client import BatchClient

    session = get_session()
    async with session.create_client("batch") as client:
        client: BatchClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeComputeEnvironmentsPaginator,
    DescribeJobDefinitionsPaginator,
    DescribeJobQueuesPaginator,
    ListConsumableResourcesPaginator,
    ListJobsByConsumableResourcePaginator,
    ListJobsPaginator,
    ListSchedulingPoliciesPaginator,
)
from .type_defs import (
    CancelJobRequestTypeDef,
    CreateComputeEnvironmentRequestTypeDef,
    CreateComputeEnvironmentResponseTypeDef,
    CreateConsumableResourceRequestTypeDef,
    CreateConsumableResourceResponseTypeDef,
    CreateJobQueueRequestTypeDef,
    CreateJobQueueResponseTypeDef,
    CreateSchedulingPolicyRequestTypeDef,
    CreateSchedulingPolicyResponseTypeDef,
    DeleteComputeEnvironmentRequestTypeDef,
    DeleteConsumableResourceRequestTypeDef,
    DeleteJobQueueRequestTypeDef,
    DeleteSchedulingPolicyRequestTypeDef,
    DeregisterJobDefinitionRequestTypeDef,
    DescribeComputeEnvironmentsRequestTypeDef,
    DescribeComputeEnvironmentsResponseTypeDef,
    DescribeConsumableResourceRequestTypeDef,
    DescribeConsumableResourceResponseTypeDef,
    DescribeJobDefinitionsRequestTypeDef,
    DescribeJobDefinitionsResponseTypeDef,
    DescribeJobQueuesRequestTypeDef,
    DescribeJobQueuesResponseTypeDef,
    DescribeJobsRequestTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeSchedulingPoliciesRequestTypeDef,
    DescribeSchedulingPoliciesResponseTypeDef,
    GetJobQueueSnapshotRequestTypeDef,
    GetJobQueueSnapshotResponseTypeDef,
    ListConsumableResourcesRequestTypeDef,
    ListConsumableResourcesResponseTypeDef,
    ListJobsByConsumableResourceRequestTypeDef,
    ListJobsByConsumableResourceResponseTypeDef,
    ListJobsRequestTypeDef,
    ListJobsResponseTypeDef,
    ListSchedulingPoliciesRequestTypeDef,
    ListSchedulingPoliciesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterJobDefinitionRequestTypeDef,
    RegisterJobDefinitionResponseTypeDef,
    SubmitJobRequestTypeDef,
    SubmitJobResponseTypeDef,
    TagResourceRequestTypeDef,
    TerminateJobRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateComputeEnvironmentRequestTypeDef,
    UpdateComputeEnvironmentResponseTypeDef,
    UpdateConsumableResourceRequestTypeDef,
    UpdateConsumableResourceResponseTypeDef,
    UpdateJobQueueRequestTypeDef,
    UpdateJobQueueResponseTypeDef,
    UpdateSchedulingPolicyRequestTypeDef,
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


__all__ = ("BatchClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]


class BatchClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BatchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#generate_presigned_url)
        """

    async def cancel_job(self, **kwargs: Unpack[CancelJobRequestTypeDef]) -> Dict[str, Any]:
        """
        Cancels a job in an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/cancel_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#cancel_job)
        """

    async def create_compute_environment(
        self, **kwargs: Unpack[CreateComputeEnvironmentRequestTypeDef]
    ) -> CreateComputeEnvironmentResponseTypeDef:
        """
        Creates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/create_compute_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#create_compute_environment)
        """

    async def create_consumable_resource(
        self, **kwargs: Unpack[CreateConsumableResourceRequestTypeDef]
    ) -> CreateConsumableResourceResponseTypeDef:
        """
        Creates an Batch consumable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/create_consumable_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#create_consumable_resource)
        """

    async def create_job_queue(
        self, **kwargs: Unpack[CreateJobQueueRequestTypeDef]
    ) -> CreateJobQueueResponseTypeDef:
        """
        Creates an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/create_job_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#create_job_queue)
        """

    async def create_scheduling_policy(
        self, **kwargs: Unpack[CreateSchedulingPolicyRequestTypeDef]
    ) -> CreateSchedulingPolicyResponseTypeDef:
        """
        Creates an Batch scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/create_scheduling_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#create_scheduling_policy)
        """

    async def delete_compute_environment(
        self, **kwargs: Unpack[DeleteComputeEnvironmentRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/delete_compute_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#delete_compute_environment)
        """

    async def delete_consumable_resource(
        self, **kwargs: Unpack[DeleteConsumableResourceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified consumable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/delete_consumable_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#delete_consumable_resource)
        """

    async def delete_job_queue(
        self, **kwargs: Unpack[DeleteJobQueueRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/delete_job_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#delete_job_queue)
        """

    async def delete_scheduling_policy(
        self, **kwargs: Unpack[DeleteSchedulingPolicyRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/delete_scheduling_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#delete_scheduling_policy)
        """

    async def deregister_job_definition(
        self, **kwargs: Unpack[DeregisterJobDefinitionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/deregister_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#deregister_job_definition)
        """

    async def describe_compute_environments(
        self, **kwargs: Unpack[DescribeComputeEnvironmentsRequestTypeDef]
    ) -> DescribeComputeEnvironmentsResponseTypeDef:
        """
        Describes one or more of your compute environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_compute_environments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_compute_environments)
        """

    async def describe_consumable_resource(
        self, **kwargs: Unpack[DescribeConsumableResourceRequestTypeDef]
    ) -> DescribeConsumableResourceResponseTypeDef:
        """
        Returns a description of the specified consumable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_consumable_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_consumable_resource)
        """

    async def describe_job_definitions(
        self, **kwargs: Unpack[DescribeJobDefinitionsRequestTypeDef]
    ) -> DescribeJobDefinitionsResponseTypeDef:
        """
        Describes a list of job definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_job_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_job_definitions)
        """

    async def describe_job_queues(
        self, **kwargs: Unpack[DescribeJobQueuesRequestTypeDef]
    ) -> DescribeJobQueuesResponseTypeDef:
        """
        Describes one or more of your job queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_job_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_job_queues)
        """

    async def describe_jobs(
        self, **kwargs: Unpack[DescribeJobsRequestTypeDef]
    ) -> DescribeJobsResponseTypeDef:
        """
        Describes a list of Batch jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_jobs)
        """

    async def describe_scheduling_policies(
        self, **kwargs: Unpack[DescribeSchedulingPoliciesRequestTypeDef]
    ) -> DescribeSchedulingPoliciesResponseTypeDef:
        """
        Describes one or more of your scheduling policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_scheduling_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_scheduling_policies)
        """

    async def get_job_queue_snapshot(
        self, **kwargs: Unpack[GetJobQueueSnapshotRequestTypeDef]
    ) -> GetJobQueueSnapshotResponseTypeDef:
        """
        Provides a list of the first 100 <code>RUNNABLE</code> jobs associated to a
        single job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_job_queue_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_job_queue_snapshot)
        """

    async def list_consumable_resources(
        self, **kwargs: Unpack[ListConsumableResourcesRequestTypeDef]
    ) -> ListConsumableResourcesResponseTypeDef:
        """
        Returns a list of Batch consumable resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_consumable_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_consumable_resources)
        """

    async def list_jobs(self, **kwargs: Unpack[ListJobsRequestTypeDef]) -> ListJobsResponseTypeDef:
        """
        Returns a list of Batch jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_jobs)
        """

    async def list_jobs_by_consumable_resource(
        self, **kwargs: Unpack[ListJobsByConsumableResourceRequestTypeDef]
    ) -> ListJobsByConsumableResourceResponseTypeDef:
        """
        Returns a list of Batch jobs that require a specific consumable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_jobs_by_consumable_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_jobs_by_consumable_resource)
        """

    async def list_scheduling_policies(
        self, **kwargs: Unpack[ListSchedulingPoliciesRequestTypeDef]
    ) -> ListSchedulingPoliciesResponseTypeDef:
        """
        Returns a list of Batch scheduling policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_scheduling_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_scheduling_policies)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_tags_for_resource)
        """

    async def register_job_definition(
        self, **kwargs: Unpack[RegisterJobDefinitionRequestTypeDef]
    ) -> RegisterJobDefinitionResponseTypeDef:
        """
        Registers an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/register_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#register_job_definition)
        """

    async def submit_job(
        self, **kwargs: Unpack[SubmitJobRequestTypeDef]
    ) -> SubmitJobResponseTypeDef:
        """
        Submits an Batch job from a job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/submit_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#submit_job)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#tag_resource)
        """

    async def terminate_job(self, **kwargs: Unpack[TerminateJobRequestTypeDef]) -> Dict[str, Any]:
        """
        Terminates a job in a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/terminate_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#terminate_job)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes specified tags from an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#untag_resource)
        """

    async def update_compute_environment(
        self, **kwargs: Unpack[UpdateComputeEnvironmentRequestTypeDef]
    ) -> UpdateComputeEnvironmentResponseTypeDef:
        """
        Updates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/update_compute_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#update_compute_environment)
        """

    async def update_consumable_resource(
        self, **kwargs: Unpack[UpdateConsumableResourceRequestTypeDef]
    ) -> UpdateConsumableResourceResponseTypeDef:
        """
        Updates a consumable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/update_consumable_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#update_consumable_resource)
        """

    async def update_job_queue(
        self, **kwargs: Unpack[UpdateJobQueueRequestTypeDef]
    ) -> UpdateJobQueueResponseTypeDef:
        """
        Updates a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/update_job_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#update_job_queue)
        """

    async def update_scheduling_policy(
        self, **kwargs: Unpack[UpdateSchedulingPolicyRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/update_scheduling_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#update_scheduling_policy)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_compute_environments"]
    ) -> DescribeComputeEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_job_definitions"]
    ) -> DescribeJobDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_job_queues"]
    ) -> DescribeJobQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_consumable_resources"]
    ) -> ListConsumableResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs_by_consumable_resource"]
    ) -> ListJobsByConsumableResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scheduling_policies"]
    ) -> ListSchedulingPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)
        """
