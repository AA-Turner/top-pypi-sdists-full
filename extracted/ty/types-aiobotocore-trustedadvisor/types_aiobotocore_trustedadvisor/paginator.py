"""
Type annotations for trustedadvisor service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_trustedadvisor.client import TrustedAdvisorPublicAPIClient
    from types_aiobotocore_trustedadvisor.paginator import (
        ListChecksPaginator,
        ListOrganizationRecommendationAccountsPaginator,
        ListOrganizationRecommendationResourcesPaginator,
        ListOrganizationRecommendationsPaginator,
        ListRecommendationResourcesPaginator,
        ListRecommendationsPaginator,
    )

    session = get_session()
    with session.create_client("trustedadvisor") as client:
        client: TrustedAdvisorPublicAPIClient

        list_checks_paginator: ListChecksPaginator = client.get_paginator("list_checks")
        list_organization_recommendation_accounts_paginator: ListOrganizationRecommendationAccountsPaginator = client.get_paginator("list_organization_recommendation_accounts")
        list_organization_recommendation_resources_paginator: ListOrganizationRecommendationResourcesPaginator = client.get_paginator("list_organization_recommendation_resources")
        list_organization_recommendations_paginator: ListOrganizationRecommendationsPaginator = client.get_paginator("list_organization_recommendations")
        list_recommendation_resources_paginator: ListRecommendationResourcesPaginator = client.get_paginator("list_recommendation_resources")
        list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChecksRequestPaginateTypeDef,
    ListChecksResponseTypeDef,
    ListOrganizationRecommendationAccountsRequestPaginateTypeDef,
    ListOrganizationRecommendationAccountsResponseTypeDef,
    ListOrganizationRecommendationResourcesRequestPaginateTypeDef,
    ListOrganizationRecommendationResourcesResponseTypeDef,
    ListOrganizationRecommendationsRequestPaginateTypeDef,
    ListOrganizationRecommendationsResponseTypeDef,
    ListRecommendationResourcesRequestPaginateTypeDef,
    ListRecommendationResourcesResponseTypeDef,
    ListRecommendationsRequestPaginateTypeDef,
    ListRecommendationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChecksPaginator",
    "ListOrganizationRecommendationAccountsPaginator",
    "ListOrganizationRecommendationResourcesPaginator",
    "ListOrganizationRecommendationsPaginator",
    "ListRecommendationResourcesPaginator",
    "ListRecommendationsPaginator",
)


if TYPE_CHECKING:
    _ListChecksPaginatorBase = AioPaginator[ListChecksResponseTypeDef]
else:
    _ListChecksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChecksPaginator(_ListChecksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListChecks.html#TrustedAdvisorPublicAPI.Paginator.ListChecks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listcheckspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChecksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListChecks.html#TrustedAdvisorPublicAPI.Paginator.ListChecks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listcheckspaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationRecommendationAccountsPaginatorBase = AioPaginator[
        ListOrganizationRecommendationAccountsResponseTypeDef
    ]
else:
    _ListOrganizationRecommendationAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationRecommendationAccountsPaginator(
    _ListOrganizationRecommendationAccountsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListOrganizationRecommendationAccounts.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listorganizationrecommendationaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationRecommendationAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationRecommendationAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListOrganizationRecommendationAccounts.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listorganizationrecommendationaccountspaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationRecommendationResourcesPaginatorBase = AioPaginator[
        ListOrganizationRecommendationResourcesResponseTypeDef
    ]
else:
    _ListOrganizationRecommendationResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationRecommendationResourcesPaginator(
    _ListOrganizationRecommendationResourcesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListOrganizationRecommendationResources.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listorganizationrecommendationresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationRecommendationResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationRecommendationResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListOrganizationRecommendationResources.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendationResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listorganizationrecommendationresourcespaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationRecommendationsPaginatorBase = AioPaginator[
        ListOrganizationRecommendationsResponseTypeDef
    ]
else:
    _ListOrganizationRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationRecommendationsPaginator(_ListOrganizationRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListOrganizationRecommendations.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listorganizationrecommendationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListOrganizationRecommendations.html#TrustedAdvisorPublicAPI.Paginator.ListOrganizationRecommendations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listorganizationrecommendationspaginator)
        """


if TYPE_CHECKING:
    _ListRecommendationResourcesPaginatorBase = AioPaginator[
        ListRecommendationResourcesResponseTypeDef
    ]
else:
    _ListRecommendationResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecommendationResourcesPaginator(_ListRecommendationResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListRecommendationResources.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendationResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listrecommendationresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecommendationResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecommendationResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListRecommendationResources.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendationResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listrecommendationresourcespaginator)
        """


if TYPE_CHECKING:
    _ListRecommendationsPaginatorBase = AioPaginator[ListRecommendationsResponseTypeDef]
else:
    _ListRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecommendationsPaginator(_ListRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListRecommendations.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listrecommendationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/trustedadvisor/paginator/ListRecommendations.html#TrustedAdvisorPublicAPI.Paginator.ListRecommendations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_trustedadvisor/paginators/#listrecommendationspaginator)
        """
