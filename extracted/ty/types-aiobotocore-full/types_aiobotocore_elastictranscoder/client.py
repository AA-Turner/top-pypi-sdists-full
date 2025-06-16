"""
Type annotations for elastictranscoder service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elastictranscoder.client import ElasticTranscoderClient

    session = get_session()
    async with session.create_client("elastictranscoder") as client:
        client: ElasticTranscoderClient
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
    ListJobsByPipelinePaginator,
    ListJobsByStatusPaginator,
    ListPipelinesPaginator,
    ListPresetsPaginator,
)
from .type_defs import (
    CancelJobRequestTypeDef,
    CreateJobRequestTypeDef,
    CreateJobResponseTypeDef,
    CreatePipelineRequestTypeDef,
    CreatePipelineResponseTypeDef,
    CreatePresetRequestTypeDef,
    CreatePresetResponseTypeDef,
    DeletePipelineRequestTypeDef,
    DeletePresetRequestTypeDef,
    ListJobsByPipelineRequestTypeDef,
    ListJobsByPipelineResponseTypeDef,
    ListJobsByStatusRequestTypeDef,
    ListJobsByStatusResponseTypeDef,
    ListPipelinesRequestTypeDef,
    ListPipelinesResponseTypeDef,
    ListPresetsRequestTypeDef,
    ListPresetsResponseTypeDef,
    ReadJobRequestTypeDef,
    ReadJobResponseTypeDef,
    ReadPipelineRequestTypeDef,
    ReadPipelineResponseTypeDef,
    ReadPresetRequestTypeDef,
    ReadPresetResponseTypeDef,
    TestRoleRequestTypeDef,
    TestRoleResponseTypeDef,
    UpdatePipelineNotificationsRequestTypeDef,
    UpdatePipelineNotificationsResponseTypeDef,
    UpdatePipelineRequestTypeDef,
    UpdatePipelineResponseTypeDef,
    UpdatePipelineStatusRequestTypeDef,
    UpdatePipelineStatusResponseTypeDef,
)
from .waiter import JobCompleteWaiter

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


__all__ = ("ElasticTranscoderClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IncompatibleVersionException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ElasticTranscoderClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticTranscoderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#generate_presigned_url)
        """

    async def cancel_job(self, **kwargs: Unpack[CancelJobRequestTypeDef]) -> Dict[str, Any]:
        """
        The CancelJob operation cancels an unfinished job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/cancel_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#cancel_job)
        """

    async def create_job(
        self, **kwargs: Unpack[CreateJobRequestTypeDef]
    ) -> CreateJobResponseTypeDef:
        """
        When you create a job, Elastic Transcoder returns JSON data that includes the
        values that you specified plus information about the job that is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/create_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#create_job)
        """

    async def create_pipeline(
        self, **kwargs: Unpack[CreatePipelineRequestTypeDef]
    ) -> CreatePipelineResponseTypeDef:
        """
        The CreatePipeline operation creates a pipeline with settings that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/create_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#create_pipeline)
        """

    async def create_preset(
        self, **kwargs: Unpack[CreatePresetRequestTypeDef]
    ) -> CreatePresetResponseTypeDef:
        """
        The CreatePreset operation creates a preset with settings that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/create_preset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#create_preset)
        """

    async def delete_pipeline(
        self, **kwargs: Unpack[DeletePipelineRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The DeletePipeline operation removes a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/delete_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#delete_pipeline)
        """

    async def delete_preset(self, **kwargs: Unpack[DeletePresetRequestTypeDef]) -> Dict[str, Any]:
        """
        The DeletePreset operation removes a preset that you've added in an AWS region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/delete_preset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#delete_preset)
        """

    async def list_jobs_by_pipeline(
        self, **kwargs: Unpack[ListJobsByPipelineRequestTypeDef]
    ) -> ListJobsByPipelineResponseTypeDef:
        """
        The ListJobsByPipeline operation gets a list of the jobs currently in a
        pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_jobs_by_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#list_jobs_by_pipeline)
        """

    async def list_jobs_by_status(
        self, **kwargs: Unpack[ListJobsByStatusRequestTypeDef]
    ) -> ListJobsByStatusResponseTypeDef:
        """
        The ListJobsByStatus operation gets a list of jobs that have a specified status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_jobs_by_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#list_jobs_by_status)
        """

    async def list_pipelines(
        self, **kwargs: Unpack[ListPipelinesRequestTypeDef]
    ) -> ListPipelinesResponseTypeDef:
        """
        The ListPipelines operation gets a list of the pipelines associated with the
        current AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_pipelines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#list_pipelines)
        """

    async def list_presets(
        self, **kwargs: Unpack[ListPresetsRequestTypeDef]
    ) -> ListPresetsResponseTypeDef:
        """
        The ListPresets operation gets a list of the default presets included with
        Elastic Transcoder and the presets that you've added in an AWS region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/list_presets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#list_presets)
        """

    async def read_job(self, **kwargs: Unpack[ReadJobRequestTypeDef]) -> ReadJobResponseTypeDef:
        """
        The ReadJob operation returns detailed information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/read_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#read_job)
        """

    async def read_pipeline(
        self, **kwargs: Unpack[ReadPipelineRequestTypeDef]
    ) -> ReadPipelineResponseTypeDef:
        """
        The ReadPipeline operation gets detailed information about a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/read_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#read_pipeline)
        """

    async def read_preset(
        self, **kwargs: Unpack[ReadPresetRequestTypeDef]
    ) -> ReadPresetResponseTypeDef:
        """
        The ReadPreset operation gets detailed information about a preset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/read_preset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#read_preset)
        """

    async def test_role(self, **kwargs: Unpack[TestRoleRequestTypeDef]) -> TestRoleResponseTypeDef:
        """
        The TestRole operation tests the IAM role used to create the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/test_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#test_role)
        """

    async def update_pipeline(
        self, **kwargs: Unpack[UpdatePipelineRequestTypeDef]
    ) -> UpdatePipelineResponseTypeDef:
        """
        Use the <code>UpdatePipeline</code> operation to update settings for a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/update_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#update_pipeline)
        """

    async def update_pipeline_notifications(
        self, **kwargs: Unpack[UpdatePipelineNotificationsRequestTypeDef]
    ) -> UpdatePipelineNotificationsResponseTypeDef:
        """
        With the UpdatePipelineNotifications operation, you can update Amazon Simple
        Notification Service (Amazon SNS) notifications for a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/update_pipeline_notifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#update_pipeline_notifications)
        """

    async def update_pipeline_status(
        self, **kwargs: Unpack[UpdatePipelineStatusRequestTypeDef]
    ) -> UpdatePipelineStatusResponseTypeDef:
        """
        The UpdatePipelineStatus operation pauses or reactivates a pipeline, so that
        the pipeline stops or restarts the processing of jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/update_pipeline_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#update_pipeline_status)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs_by_pipeline"]
    ) -> ListJobsByPipelinePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs_by_status"]
    ) -> ListJobsByStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pipelines"]
    ) -> ListPipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_presets"]
    ) -> ListPresetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["job_complete"]
    ) -> JobCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/client/)
        """
