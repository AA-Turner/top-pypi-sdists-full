"""
Type annotations for account service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_account.client import AccountClient

    session = get_session()
    async with session.create_client("account") as client:
        client: AccountClient
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

from .paginator import ListRegionsPaginator
from .type_defs import (
    AcceptPrimaryEmailUpdateRequestTypeDef,
    AcceptPrimaryEmailUpdateResponseTypeDef,
    DeleteAlternateContactRequestTypeDef,
    DisableRegionRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableRegionRequestTypeDef,
    GetAccountInformationRequestTypeDef,
    GetAccountInformationResponseTypeDef,
    GetAlternateContactRequestTypeDef,
    GetAlternateContactResponseTypeDef,
    GetContactInformationRequestTypeDef,
    GetContactInformationResponseTypeDef,
    GetPrimaryEmailRequestTypeDef,
    GetPrimaryEmailResponseTypeDef,
    GetRegionOptStatusRequestTypeDef,
    GetRegionOptStatusResponseTypeDef,
    ListRegionsRequestTypeDef,
    ListRegionsResponseTypeDef,
    PutAccountNameRequestTypeDef,
    PutAlternateContactRequestTypeDef,
    PutContactInformationRequestTypeDef,
    StartPrimaryEmailUpdateRequestTypeDef,
    StartPrimaryEmailUpdateResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("AccountClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AccountClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AccountClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#generate_presigned_url)
        """

    async def accept_primary_email_update(
        self, **kwargs: Unpack[AcceptPrimaryEmailUpdateRequestTypeDef]
    ) -> AcceptPrimaryEmailUpdateResponseTypeDef:
        """
        Accepts the request that originated from <a>StartPrimaryEmailUpdate</a> to
        update the primary email address (also known as the root user email address)
        for the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/accept_primary_email_update.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#accept_primary_email_update)
        """

    async def delete_alternate_contact(
        self, **kwargs: Unpack[DeleteAlternateContactRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified alternate contact from an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/delete_alternate_contact.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#delete_alternate_contact)
        """

    async def disable_region(
        self, **kwargs: Unpack[DisableRegionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables (opts-out) a particular Region for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/disable_region.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#disable_region)
        """

    async def enable_region(
        self, **kwargs: Unpack[EnableRegionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables (opts-in) a particular Region for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/enable_region.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#enable_region)
        """

    async def get_account_information(
        self, **kwargs: Unpack[GetAccountInformationRequestTypeDef]
    ) -> GetAccountInformationResponseTypeDef:
        """
        Retrieves information about the specified account including its account name,
        account ID, and account creation date and time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_account_information.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#get_account_information)
        """

    async def get_alternate_contact(
        self, **kwargs: Unpack[GetAlternateContactRequestTypeDef]
    ) -> GetAlternateContactResponseTypeDef:
        """
        Retrieves the specified alternate contact attached to an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_alternate_contact.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#get_alternate_contact)
        """

    async def get_contact_information(
        self, **kwargs: Unpack[GetContactInformationRequestTypeDef]
    ) -> GetContactInformationResponseTypeDef:
        """
        Retrieves the primary contact information of an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_contact_information.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#get_contact_information)
        """

    async def get_primary_email(
        self, **kwargs: Unpack[GetPrimaryEmailRequestTypeDef]
    ) -> GetPrimaryEmailResponseTypeDef:
        """
        Retrieves the primary email address for the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_primary_email.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#get_primary_email)
        """

    async def get_region_opt_status(
        self, **kwargs: Unpack[GetRegionOptStatusRequestTypeDef]
    ) -> GetRegionOptStatusResponseTypeDef:
        """
        Retrieves the opt-in status of a particular Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_region_opt_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#get_region_opt_status)
        """

    async def list_regions(
        self, **kwargs: Unpack[ListRegionsRequestTypeDef]
    ) -> ListRegionsResponseTypeDef:
        """
        Lists all the Regions for a given account and their respective opt-in statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/list_regions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#list_regions)
        """

    async def put_account_name(
        self, **kwargs: Unpack[PutAccountNameRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the account name of the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/put_account_name.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#put_account_name)
        """

    async def put_alternate_contact(
        self, **kwargs: Unpack[PutAlternateContactRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the specified alternate contact attached to an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/put_alternate_contact.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#put_alternate_contact)
        """

    async def put_contact_information(
        self, **kwargs: Unpack[PutContactInformationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the primary contact information of an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/put_contact_information.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#put_contact_information)
        """

    async def start_primary_email_update(
        self, **kwargs: Unpack[StartPrimaryEmailUpdateRequestTypeDef]
    ) -> StartPrimaryEmailUpdateResponseTypeDef:
        """
        Starts the process to update the primary email address for the specified
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/start_primary_email_update.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#start_primary_email_update)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_regions"]
    ) -> ListRegionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account.html#Account.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/client/)
        """
