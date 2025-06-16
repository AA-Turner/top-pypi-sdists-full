"""
Type annotations for license-manager-user-subscriptions service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_license_manager_user_subscriptions.client import LicenseManagerUserSubscriptionsClient
    from types_aiobotocore_license_manager_user_subscriptions.paginator import (
        ListIdentityProvidersPaginator,
        ListInstancesPaginator,
        ListLicenseServerEndpointsPaginator,
        ListProductSubscriptionsPaginator,
        ListUserAssociationsPaginator,
    )

    session = get_session()
    with session.create_client("license-manager-user-subscriptions") as client:
        client: LicenseManagerUserSubscriptionsClient

        list_identity_providers_paginator: ListIdentityProvidersPaginator = client.get_paginator("list_identity_providers")
        list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
        list_license_server_endpoints_paginator: ListLicenseServerEndpointsPaginator = client.get_paginator("list_license_server_endpoints")
        list_product_subscriptions_paginator: ListProductSubscriptionsPaginator = client.get_paginator("list_product_subscriptions")
        list_user_associations_paginator: ListUserAssociationsPaginator = client.get_paginator("list_user_associations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListIdentityProvidersRequestPaginateTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListInstancesRequestPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListLicenseServerEndpointsRequestPaginateTypeDef,
    ListLicenseServerEndpointsResponseTypeDef,
    ListProductSubscriptionsRequestPaginateTypeDef,
    ListProductSubscriptionsResponseTypeDef,
    ListUserAssociationsRequestPaginateTypeDef,
    ListUserAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListIdentityProvidersPaginator",
    "ListInstancesPaginator",
    "ListLicenseServerEndpointsPaginator",
    "ListProductSubscriptionsPaginator",
    "ListUserAssociationsPaginator",
)

if TYPE_CHECKING:
    _ListIdentityProvidersPaginatorBase = AioPaginator[ListIdentityProvidersResponseTypeDef]
else:
    _ListIdentityProvidersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIdentityProvidersPaginator(_ListIdentityProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListIdentityProviders.html#LicenseManagerUserSubscriptions.Paginator.ListIdentityProviders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listidentityproviderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdentityProvidersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIdentityProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListIdentityProviders.html#LicenseManagerUserSubscriptions.Paginator.ListIdentityProviders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listidentityproviderspaginator)
        """

if TYPE_CHECKING:
    _ListInstancesPaginatorBase = AioPaginator[ListInstancesResponseTypeDef]
else:
    _ListInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListInstances.html#LicenseManagerUserSubscriptions.Paginator.ListInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListInstances.html#LicenseManagerUserSubscriptions.Paginator.ListInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listinstancespaginator)
        """

if TYPE_CHECKING:
    _ListLicenseServerEndpointsPaginatorBase = AioPaginator[
        ListLicenseServerEndpointsResponseTypeDef
    ]
else:
    _ListLicenseServerEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLicenseServerEndpointsPaginator(_ListLicenseServerEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListLicenseServerEndpoints.html#LicenseManagerUserSubscriptions.Paginator.ListLicenseServerEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listlicenseserverendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLicenseServerEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLicenseServerEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListLicenseServerEndpoints.html#LicenseManagerUserSubscriptions.Paginator.ListLicenseServerEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listlicenseserverendpointspaginator)
        """

if TYPE_CHECKING:
    _ListProductSubscriptionsPaginatorBase = AioPaginator[ListProductSubscriptionsResponseTypeDef]
else:
    _ListProductSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProductSubscriptionsPaginator(_ListProductSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListProductSubscriptions.html#LicenseManagerUserSubscriptions.Paginator.ListProductSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listproductsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProductSubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProductSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListProductSubscriptions.html#LicenseManagerUserSubscriptions.Paginator.ListProductSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listproductsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _ListUserAssociationsPaginatorBase = AioPaginator[ListUserAssociationsResponseTypeDef]
else:
    _ListUserAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserAssociationsPaginator(_ListUserAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListUserAssociations.html#LicenseManagerUserSubscriptions.Paginator.ListUserAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listuserassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/paginator/ListUserAssociations.html#LicenseManagerUserSubscriptions.Paginator.ListUserAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/paginators/#listuserassociationspaginator)
        """
