"""
Main interface for license-manager-user-subscriptions service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_license_manager_user_subscriptions import (
        Client,
        LicenseManagerUserSubscriptionsClient,
        ListIdentityProvidersPaginator,
        ListInstancesPaginator,
        ListLicenseServerEndpointsPaginator,
        ListProductSubscriptionsPaginator,
        ListUserAssociationsPaginator,
    )

    session = get_session()
    async with session.create_client("license-manager-user-subscriptions") as client:
        client: LicenseManagerUserSubscriptionsClient
        ...


    list_identity_providers_paginator: ListIdentityProvidersPaginator = client.get_paginator("list_identity_providers")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_license_server_endpoints_paginator: ListLicenseServerEndpointsPaginator = client.get_paginator("list_license_server_endpoints")
    list_product_subscriptions_paginator: ListProductSubscriptionsPaginator = client.get_paginator("list_product_subscriptions")
    list_user_associations_paginator: ListUserAssociationsPaginator = client.get_paginator("list_user_associations")
    ```
"""

from .client import LicenseManagerUserSubscriptionsClient
from .paginator import (
    ListIdentityProvidersPaginator,
    ListInstancesPaginator,
    ListLicenseServerEndpointsPaginator,
    ListProductSubscriptionsPaginator,
    ListUserAssociationsPaginator,
)

Client = LicenseManagerUserSubscriptionsClient


__all__ = (
    "Client",
    "LicenseManagerUserSubscriptionsClient",
    "ListIdentityProvidersPaginator",
    "ListInstancesPaginator",
    "ListLicenseServerEndpointsPaginator",
    "ListProductSubscriptionsPaginator",
    "ListUserAssociationsPaginator",
)
