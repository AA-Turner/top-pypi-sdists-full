"""
Type annotations for cloudcontrol service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudcontrol.client import CloudControlApiClient

    session = get_session()
    async with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient
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

from .paginator import ListResourceRequestsPaginator, ListResourcesPaginator
from .type_defs import (
    CancelResourceRequestInputTypeDef,
    CancelResourceRequestOutputTypeDef,
    CreateResourceInputTypeDef,
    CreateResourceOutputTypeDef,
    DeleteResourceInputTypeDef,
    DeleteResourceOutputTypeDef,
    GetResourceInputTypeDef,
    GetResourceOutputTypeDef,
    GetResourceRequestStatusInputTypeDef,
    GetResourceRequestStatusOutputTypeDef,
    ListResourceRequestsInputTypeDef,
    ListResourceRequestsOutputTypeDef,
    ListResourcesInputTypeDef,
    ListResourcesOutputTypeDef,
    UpdateResourceInputTypeDef,
    UpdateResourceOutputTypeDef,
)
from .waiter import ResourceRequestSuccessWaiter

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("CloudControlApiClient",)

class Exceptions(BaseClientExceptions):
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientTokenConflictException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentOperationException: Type[BotocoreClientError]
    GeneralServiceException: Type[BotocoreClientError]
    HandlerFailureException: Type[BotocoreClientError]
    HandlerInternalFailureException: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    NetworkFailureException: Type[BotocoreClientError]
    NotStabilizedException: Type[BotocoreClientError]
    NotUpdatableException: Type[BotocoreClientError]
    PrivateTypeException: Type[BotocoreClientError]
    RequestTokenNotFoundException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceInternalErrorException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TypeNotFoundException: Type[BotocoreClientError]
    UnsupportedActionException: Type[BotocoreClientError]

class CloudControlApiClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudControlApiClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#generate_presigned_url)
        """

    async def cancel_resource_request(
        self, **kwargs: Unpack[CancelResourceRequestInputTypeDef]
    ) -> CancelResourceRequestOutputTypeDef:
        """
        Cancels the specified resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/cancel_resource_request.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#cancel_resource_request)
        """

    async def create_resource(
        self, **kwargs: Unpack[CreateResourceInputTypeDef]
    ) -> CreateResourceOutputTypeDef:
        """
        Creates the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/create_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#create_resource)
        """

    async def delete_resource(
        self, **kwargs: Unpack[DeleteResourceInputTypeDef]
    ) -> DeleteResourceOutputTypeDef:
        """
        Deletes the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/delete_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#delete_resource)
        """

    async def get_resource(
        self, **kwargs: Unpack[GetResourceInputTypeDef]
    ) -> GetResourceOutputTypeDef:
        """
        Returns information about the current state of the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_resource)
        """

    async def get_resource_request_status(
        self, **kwargs: Unpack[GetResourceRequestStatusInputTypeDef]
    ) -> GetResourceRequestStatusOutputTypeDef:
        """
        Returns the current status of a resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_resource_request_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_resource_request_status)
        """

    async def list_resource_requests(
        self, **kwargs: Unpack[ListResourceRequestsInputTypeDef]
    ) -> ListResourceRequestsOutputTypeDef:
        """
        Returns existing resource operation requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/list_resource_requests.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#list_resource_requests)
        """

    async def list_resources(
        self, **kwargs: Unpack[ListResourcesInputTypeDef]
    ) -> ListResourcesOutputTypeDef:
        """
        Returns information about the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/list_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#list_resources)
        """

    async def update_resource(
        self, **kwargs: Unpack[UpdateResourceInputTypeDef]
    ) -> UpdateResourceOutputTypeDef:
        """
        Updates the specified property values in the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/update_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#update_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_requests"]
    ) -> ListResourceRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resources"]
    ) -> ListResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["resource_request_success"]
    ) -> ResourceRequestSuccessWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)
        """
