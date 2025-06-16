"""
Type annotations for license-manager-linux-subscriptions service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_license_manager_linux_subscriptions.client import LicenseManagerLinuxSubscriptionsClient

    session = get_session()
    async with session.create_client("license-manager-linux-subscriptions") as client:
        client: LicenseManagerLinuxSubscriptionsClient
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
    ListLinuxSubscriptionInstancesPaginator,
    ListLinuxSubscriptionsPaginator,
    ListRegisteredSubscriptionProvidersPaginator,
)
from .type_defs import (
    DeregisterSubscriptionProviderRequestTypeDef,
    GetRegisteredSubscriptionProviderRequestTypeDef,
    GetRegisteredSubscriptionProviderResponseTypeDef,
    GetServiceSettingsResponseTypeDef,
    ListLinuxSubscriptionInstancesRequestTypeDef,
    ListLinuxSubscriptionInstancesResponseTypeDef,
    ListLinuxSubscriptionsRequestTypeDef,
    ListLinuxSubscriptionsResponseTypeDef,
    ListRegisteredSubscriptionProvidersRequestTypeDef,
    ListRegisteredSubscriptionProvidersResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterSubscriptionProviderRequestTypeDef,
    RegisterSubscriptionProviderResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateServiceSettingsRequestTypeDef,
    UpdateServiceSettingsResponseTypeDef,
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

__all__ = ("LicenseManagerLinuxSubscriptionsClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LicenseManagerLinuxSubscriptionsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions.html#LicenseManagerLinuxSubscriptions.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LicenseManagerLinuxSubscriptionsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions.html#LicenseManagerLinuxSubscriptions.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#generate_presigned_url)
        """

    async def deregister_subscription_provider(
        self, **kwargs: Unpack[DeregisterSubscriptionProviderRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove a third-party subscription provider from the Bring Your Own License
        (BYOL) subscriptions registered to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/deregister_subscription_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#deregister_subscription_provider)
        """

    async def get_registered_subscription_provider(
        self, **kwargs: Unpack[GetRegisteredSubscriptionProviderRequestTypeDef]
    ) -> GetRegisteredSubscriptionProviderResponseTypeDef:
        """
        Get details for a Bring Your Own License (BYOL) subscription that's registered
        to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/get_registered_subscription_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#get_registered_subscription_provider)
        """

    async def get_service_settings(self) -> GetServiceSettingsResponseTypeDef:
        """
        Lists the Linux subscriptions service settings for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/get_service_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#get_service_settings)
        """

    async def list_linux_subscription_instances(
        self, **kwargs: Unpack[ListLinuxSubscriptionInstancesRequestTypeDef]
    ) -> ListLinuxSubscriptionInstancesResponseTypeDef:
        """
        Lists the running Amazon EC2 instances that were discovered with commercial
        Linux subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/list_linux_subscription_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#list_linux_subscription_instances)
        """

    async def list_linux_subscriptions(
        self, **kwargs: Unpack[ListLinuxSubscriptionsRequestTypeDef]
    ) -> ListLinuxSubscriptionsResponseTypeDef:
        """
        Lists the Linux subscriptions that have been discovered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/list_linux_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#list_linux_subscriptions)
        """

    async def list_registered_subscription_providers(
        self, **kwargs: Unpack[ListRegisteredSubscriptionProvidersRequestTypeDef]
    ) -> ListRegisteredSubscriptionProvidersResponseTypeDef:
        """
        List Bring Your Own License (BYOL) subscription registration resources for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/list_registered_subscription_providers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#list_registered_subscription_providers)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the metadata tags that are assigned to the specified Amazon Web Services
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#list_tags_for_resource)
        """

    async def register_subscription_provider(
        self, **kwargs: Unpack[RegisterSubscriptionProviderRequestTypeDef]
    ) -> RegisterSubscriptionProviderResponseTypeDef:
        """
        Register the supported third-party subscription provider for your Bring Your
        Own License (BYOL) subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/register_subscription_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#register_subscription_provider)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Add metadata tags to the specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Remove one or more metadata tag from the specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#untag_resource)
        """

    async def update_service_settings(
        self, **kwargs: Unpack[UpdateServiceSettingsRequestTypeDef]
    ) -> UpdateServiceSettingsResponseTypeDef:
        """
        Updates the service settings for Linux subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/update_service_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#update_service_settings)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_linux_subscription_instances"]
    ) -> ListLinuxSubscriptionInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_linux_subscriptions"]
    ) -> ListLinuxSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_registered_subscription_providers"]
    ) -> ListRegisteredSubscriptionProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions.html#LicenseManagerLinuxSubscriptions.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions.html#LicenseManagerLinuxSubscriptions.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/client/)
        """
