"""
Type annotations for amp service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amp.client import PrometheusServiceClient
    from types_aiobotocore_amp.paginator import (
        ListRuleGroupsNamespacesPaginator,
        ListScrapersPaginator,
        ListWorkspacesPaginator,
    )

    session = get_session()
    with session.create_client("amp") as client:
        client: PrometheusServiceClient

        list_rule_groups_namespaces_paginator: ListRuleGroupsNamespacesPaginator = client.get_paginator("list_rule_groups_namespaces")
        list_scrapers_paginator: ListScrapersPaginator = client.get_paginator("list_scrapers")
        list_workspaces_paginator: ListWorkspacesPaginator = client.get_paginator("list_workspaces")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListRuleGroupsNamespacesRequestPaginateTypeDef,
    ListRuleGroupsNamespacesResponseTypeDef,
    ListScrapersRequestPaginateTypeDef,
    ListScrapersResponseTypeDef,
    ListWorkspacesRequestPaginateTypeDef,
    ListWorkspacesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRuleGroupsNamespacesPaginator", "ListScrapersPaginator", "ListWorkspacesPaginator")


if TYPE_CHECKING:
    _ListRuleGroupsNamespacesPaginatorBase = AioPaginator[ListRuleGroupsNamespacesResponseTypeDef]
else:
    _ListRuleGroupsNamespacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRuleGroupsNamespacesPaginator(_ListRuleGroupsNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListRuleGroupsNamespaces.html#PrometheusService.Paginator.ListRuleGroupsNamespaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listrulegroupsnamespacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleGroupsNamespacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRuleGroupsNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListRuleGroupsNamespaces.html#PrometheusService.Paginator.ListRuleGroupsNamespaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listrulegroupsnamespacespaginator)
        """


if TYPE_CHECKING:
    _ListScrapersPaginatorBase = AioPaginator[ListScrapersResponseTypeDef]
else:
    _ListScrapersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScrapersPaginator(_ListScrapersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListScrapers.html#PrometheusService.Paginator.ListScrapers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listscraperspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScrapersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListScrapersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListScrapers.html#PrometheusService.Paginator.ListScrapers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listscraperspaginator)
        """


if TYPE_CHECKING:
    _ListWorkspacesPaginatorBase = AioPaginator[ListWorkspacesResponseTypeDef]
else:
    _ListWorkspacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkspacesPaginator(_ListWorkspacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListWorkspaces.html#PrometheusService.Paginator.ListWorkspaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listworkspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkspacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkspacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/paginator/ListWorkspaces.html#PrometheusService.Paginator.ListWorkspaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/paginators/#listworkspacespaginator)
        """
