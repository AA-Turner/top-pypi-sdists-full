"""
Type annotations for supportauthz service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_supportauthz.client import SupportAuthZClient

    session = get_session()
    async with session.create_client("supportauthz") as client:
        client: SupportAuthZClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListActionsPaginator,
    ListSupportPermitRequestsPaginator,
    ListSupportPermitsPaginator,
)
from .type_defs import (
    CreateSupportPermitInputTypeDef,
    CreateSupportPermitOutputTypeDef,
    DeleteSupportPermitInputTypeDef,
    DeleteSupportPermitOutputTypeDef,
    GetActionInputTypeDef,
    GetActionOutputTypeDef,
    GetSupportPermitInputTypeDef,
    GetSupportPermitOutputTypeDef,
    ListActionsInputTypeDef,
    ListActionsOutputTypeDef,
    ListSupportPermitRequestsInputTypeDef,
    ListSupportPermitRequestsOutputTypeDef,
    ListSupportPermitsInputTypeDef,
    ListSupportPermitsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    RejectSupportPermitRequestInputTypeDef,
    RejectSupportPermitRequestOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("SupportAuthZClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class SupportAuthZClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz.html#SupportAuthZ.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupportAuthZClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz.html#SupportAuthZ.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#generate_presigned_url)
        """

    async def create_support_permit(
        self, **kwargs: Unpack[CreateSupportPermitInputTypeDef]
    ) -> CreateSupportPermitOutputTypeDef:
        """
        Creates a support permit that authorizes an AWS support operator to perform
        specified actions on specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/create_support_permit.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#create_support_permit)
        """

    async def delete_support_permit(
        self, **kwargs: Unpack[DeleteSupportPermitInputTypeDef]
    ) -> DeleteSupportPermitOutputTypeDef:
        """
        Deletes a support permit, revoking the authorization previously granted to the
        AWS support operator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/delete_support_permit.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#delete_support_permit)
        """

    async def get_action(self, **kwargs: Unpack[GetActionInputTypeDef]) -> GetActionOutputTypeDef:
        """
        Retrieves the description of a specific support action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#get_action)
        """

    async def get_support_permit(
        self, **kwargs: Unpack[GetSupportPermitInputTypeDef]
    ) -> GetSupportPermitOutputTypeDef:
        """
        Retrieves the details of a support permit by its ARN or name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_support_permit.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#get_support_permit)
        """

    async def list_actions(
        self, **kwargs: Unpack[ListActionsInputTypeDef]
    ) -> ListActionsOutputTypeDef:
        """
        Lists available support actions for a specified AWS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_actions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#list_actions)
        """

    async def list_support_permit_requests(
        self, **kwargs: Unpack[ListSupportPermitRequestsInputTypeDef]
    ) -> ListSupportPermitRequestsOutputTypeDef:
        """
        Lists permit requests from AWS support operators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_support_permit_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#list_support_permit_requests)
        """

    async def list_support_permits(
        self, **kwargs: Unpack[ListSupportPermitsInputTypeDef]
    ) -> ListSupportPermitsOutputTypeDef:
        """
        Lists all support permits in the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_support_permits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#list_support_permits)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with a support permit resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#list_tags_for_resource)
        """

    async def reject_support_permit_request(
        self, **kwargs: Unpack[RejectSupportPermitRequestInputTypeDef]
    ) -> RejectSupportPermitRequestOutputTypeDef:
        """
        Rejects a permit request from an AWS support operator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/reject_support_permit_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#reject_support_permit_request)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds or overwrites one or more tags for a support permit resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes one or more tags from a support permit resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_actions"]
    ) -> ListActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_support_permit_requests"]
    ) -> ListSupportPermitRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_support_permits"]
    ) -> ListSupportPermitsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz.html#SupportAuthZ.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz.html#SupportAuthZ.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/client/)
        """
