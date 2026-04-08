"""
Type annotations for uxc service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_uxc.client import UserExperienceCustomizationClient

    session = get_session()
    async with session.create_client("uxc") as client:
        client: UserExperienceCustomizationClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListServicesPaginator
from .type_defs import (
    GetAccountCustomizationsOutputTypeDef,
    ListServicesInputTypeDef,
    ListServicesOutputTypeDef,
    UpdateAccountCustomizationsInputTypeDef,
    UpdateAccountCustomizationsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("UserExperienceCustomizationClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class UserExperienceCustomizationClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc.html#UserExperienceCustomization.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        UserExperienceCustomizationClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc.html#UserExperienceCustomization.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/#generate_presigned_url)
        """

    async def get_account_customizations(self) -> GetAccountCustomizationsOutputTypeDef:
        """
        Returns the current account customization settings, including account color,
        visible services, and visible Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/client/get_account_customizations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/#get_account_customizations)
        """

    async def list_services(
        self, **kwargs: Unpack[ListServicesInputTypeDef]
    ) -> ListServicesOutputTypeDef:
        """
        Returns a paginated list of Amazon Web Services service identifiers that you
        can use as values for the <code>visibleServices</code> setting in <a
        href="https://docs.aws.amazon.com/awsconsolehelpdocs/latest/APIReference/API_UpdateAccountCustomizations.html">UpdateAccountCustomizations</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/client/list_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/#list_services)
        """

    async def update_account_customizations(
        self, **kwargs: Unpack[UpdateAccountCustomizationsInputTypeDef]
    ) -> UpdateAccountCustomizationsOutputTypeDef:
        """
        Updates one or more account customization settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/client/update_account_customizations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/#update_account_customizations)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services"]
    ) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc.html#UserExperienceCustomization.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc.html#UserExperienceCustomization.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/client/)
        """
