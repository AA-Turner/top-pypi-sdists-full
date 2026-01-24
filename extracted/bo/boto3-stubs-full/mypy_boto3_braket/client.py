"""
Type annotations for braket service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_braket.client import BraketClient

    session = Session()
    client: BraketClient = session.client("braket")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    SearchDevicesPaginator,
    SearchJobsPaginator,
    SearchQuantumTasksPaginator,
    SearchSpendingLimitsPaginator,
)
from .type_defs import (
    CancelJobRequestTypeDef,
    CancelJobResponseTypeDef,
    CancelQuantumTaskRequestTypeDef,
    CancelQuantumTaskResponseTypeDef,
    CreateJobRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateQuantumTaskRequestTypeDef,
    CreateQuantumTaskResponseTypeDef,
    CreateSpendingLimitRequestTypeDef,
    CreateSpendingLimitResponseTypeDef,
    DeleteSpendingLimitRequestTypeDef,
    GetDeviceRequestTypeDef,
    GetDeviceResponseTypeDef,
    GetJobRequestTypeDef,
    GetJobResponseTypeDef,
    GetQuantumTaskRequestTypeDef,
    GetQuantumTaskResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchDevicesRequestTypeDef,
    SearchDevicesResponseTypeDef,
    SearchJobsRequestTypeDef,
    SearchJobsResponseTypeDef,
    SearchQuantumTasksRequestTypeDef,
    SearchQuantumTasksResponseTypeDef,
    SearchSpendingLimitsRequestTypeDef,
    SearchSpendingLimitsResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateSpendingLimitRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BraketClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    DeviceOfflineException: type[BotocoreClientError]
    DeviceRetiredException: type[BotocoreClientError]
    InternalServiceException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class BraketClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BraketClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#generate_presigned_url)
        """

    def cancel_job(self, **kwargs: Unpack[CancelJobRequestTypeDef]) -> CancelJobResponseTypeDef:
        """
        Cancels an Amazon Braket hybrid job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/cancel_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#cancel_job)
        """

    def cancel_quantum_task(
        self, **kwargs: Unpack[CancelQuantumTaskRequestTypeDef]
    ) -> CancelQuantumTaskResponseTypeDef:
        """
        Cancels the specified task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/cancel_quantum_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#cancel_quantum_task)
        """

    def create_job(self, **kwargs: Unpack[CreateJobRequestTypeDef]) -> CreateJobResponseTypeDef:
        """
        Creates an Amazon Braket hybrid job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/create_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#create_job)
        """

    def create_quantum_task(
        self, **kwargs: Unpack[CreateQuantumTaskRequestTypeDef]
    ) -> CreateQuantumTaskResponseTypeDef:
        """
        Creates a quantum task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/create_quantum_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#create_quantum_task)
        """

    def create_spending_limit(
        self, **kwargs: Unpack[CreateSpendingLimitRequestTypeDef]
    ) -> CreateSpendingLimitResponseTypeDef:
        """
        Creates a spending limit for a specified quantum device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/create_spending_limit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#create_spending_limit)
        """

    def delete_spending_limit(
        self, **kwargs: Unpack[DeleteSpendingLimitRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an existing spending limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/delete_spending_limit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#delete_spending_limit)
        """

    def get_device(self, **kwargs: Unpack[GetDeviceRequestTypeDef]) -> GetDeviceResponseTypeDef:
        """
        Retrieves the devices available in Amazon Braket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/get_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#get_device)
        """

    def get_job(self, **kwargs: Unpack[GetJobRequestTypeDef]) -> GetJobResponseTypeDef:
        """
        Retrieves the specified Amazon Braket hybrid job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/get_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#get_job)
        """

    def get_quantum_task(
        self, **kwargs: Unpack[GetQuantumTaskRequestTypeDef]
    ) -> GetQuantumTaskResponseTypeDef:
        """
        Retrieves the specified quantum task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/get_quantum_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#get_quantum_task)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Shows the tags associated with this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#list_tags_for_resource)
        """

    def search_devices(
        self, **kwargs: Unpack[SearchDevicesRequestTypeDef]
    ) -> SearchDevicesResponseTypeDef:
        """
        Searches for devices using the specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/search_devices.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#search_devices)
        """

    def search_jobs(self, **kwargs: Unpack[SearchJobsRequestTypeDef]) -> SearchJobsResponseTypeDef:
        """
        Searches for Amazon Braket hybrid jobs that match the specified filter values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/search_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#search_jobs)
        """

    def search_quantum_tasks(
        self, **kwargs: Unpack[SearchQuantumTasksRequestTypeDef]
    ) -> SearchQuantumTasksResponseTypeDef:
        """
        Searches for tasks that match the specified filter values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/search_quantum_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#search_quantum_tasks)
        """

    def search_spending_limits(
        self, **kwargs: Unpack[SearchSpendingLimitsRequestTypeDef]
    ) -> SearchSpendingLimitsResponseTypeDef:
        """
        Searches and lists spending limits based on specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/search_spending_limits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#search_spending_limits)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Add a tag to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Remove tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#untag_resource)
        """

    def update_spending_limit(
        self, **kwargs: Unpack[UpdateSpendingLimitRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates an existing spending limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/update_spending_limit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#update_spending_limit)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_devices"]
    ) -> SearchDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_jobs"]
    ) -> SearchJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_quantum_tasks"]
    ) -> SearchQuantumTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_spending_limits"]
    ) -> SearchSpendingLimitsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/client/#get_paginator)
        """
