"""
Type annotations for account-access service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_account_access.client import AccountAccessClient

    session = get_session()
    async with session.create_client("account-access") as client:
        client: AccountAccessClient
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

from .paginator import ListApplicationsPaginator, ListEntitlementsPaginator
from .type_defs import (
    CreateApplicationRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateEntitlementRequestTypeDef,
    CreateEntitlementResponseTypeDef,
    DeleteApplicationRequestTypeDef,
    DeleteEntitlementRequestTypeDef,
    GetApplicationRequestTypeDef,
    GetApplicationResponseTypeDef,
    GetEntitlementRequestTypeDef,
    GetEntitlementResponseTypeDef,
    ListApplicationsRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListEntitlementsRequestTypeDef,
    ListEntitlementsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
)
from .waiter import ApplicationActiveWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("AccountAccessClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    AlreadyCreatedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class AccountAccessClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access.html#AccountAccess.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AccountAccessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access.html#AccountAccess.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#generate_presigned_url)
        """

    async def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an account access manager instance and its Amazon Web Services account
        access application in the associated IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/create_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#create_application)
        """

    async def create_entitlement(
        self, **kwargs: Unpack[CreateEntitlementRequestTypeDef]
    ) -> CreateEntitlementResponseTypeDef:
        """
        Creates an entitlement (assignment) in account access manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/create_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#create_entitlement)
        """

    async def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an account access manager application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/delete_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#delete_application)
        """

    async def delete_entitlement(
        self, **kwargs: Unpack[DeleteEntitlementRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an entitlement from an account access manager application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/delete_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#delete_entitlement)
        """

    async def get_application(
        self, **kwargs: Unpack[GetApplicationRequestTypeDef]
    ) -> GetApplicationResponseTypeDef:
        """
        Retrieves details about an account access manager application, including its
        status, identity source, and tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/get_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#get_application)
        """

    async def get_entitlement(
        self, **kwargs: Unpack[GetEntitlementRequestTypeDef]
    ) -> GetEntitlementResponseTypeDef:
        """
        Retrieves details about a specific entitlement for an account access manager
        application, including the principal, IAM role, and target account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/get_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#get_entitlement)
        """

    async def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists the account access manager applications in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/list_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#list_applications)
        """

    async def list_entitlements(
        self, **kwargs: Unpack[ListEntitlementsRequestTypeDef]
    ) -> ListEntitlementsResponseTypeDef:
        """
        Lists the entitlements for a specified account access manager application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/list_entitlements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#list_entitlements)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags associated with an account access manager resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#list_tags_for_resource)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds tags to an account access manager resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes tags from an account access manager resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_entitlements"]
    ) -> ListEntitlementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["application_active"]
    ) -> ApplicationActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access.html#AccountAccess.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access.html#AccountAccess.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/client/)
        """
