"""
Main interface for trustedadvisor service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_trustedadvisor import (
        Client,
        ListChecksPaginator,
        ListOrganizationRecommendationAccountsPaginator,
        ListOrganizationRecommendationResourcesPaginator,
        ListOrganizationRecommendationsPaginator,
        ListRecommendationResourcesPaginator,
        ListRecommendationsPaginator,
        TrustedAdvisorPublicAPIClient,
    )

    session = get_session()
    async with session.create_client("trustedadvisor") as client:
        client: TrustedAdvisorPublicAPIClient
        ...


    list_checks_paginator: ListChecksPaginator = client.get_paginator("list_checks")
    list_organization_recommendation_accounts_paginator: ListOrganizationRecommendationAccountsPaginator = client.get_paginator("list_organization_recommendation_accounts")
    list_organization_recommendation_resources_paginator: ListOrganizationRecommendationResourcesPaginator = client.get_paginator("list_organization_recommendation_resources")
    list_organization_recommendations_paginator: ListOrganizationRecommendationsPaginator = client.get_paginator("list_organization_recommendations")
    list_recommendation_resources_paginator: ListRecommendationResourcesPaginator = client.get_paginator("list_recommendation_resources")
    list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    ```
"""

from .client import TrustedAdvisorPublicAPIClient
from .paginator import (
    ListChecksPaginator,
    ListOrganizationRecommendationAccountsPaginator,
    ListOrganizationRecommendationResourcesPaginator,
    ListOrganizationRecommendationsPaginator,
    ListRecommendationResourcesPaginator,
    ListRecommendationsPaginator,
)

Client = TrustedAdvisorPublicAPIClient


__all__ = (
    "Client",
    "ListChecksPaginator",
    "ListOrganizationRecommendationAccountsPaginator",
    "ListOrganizationRecommendationResourcesPaginator",
    "ListOrganizationRecommendationsPaginator",
    "ListRecommendationResourcesPaginator",
    "ListRecommendationsPaginator",
    "TrustedAdvisorPublicAPIClient",
)
