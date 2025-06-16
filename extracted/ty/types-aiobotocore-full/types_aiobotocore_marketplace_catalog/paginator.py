"""
Type annotations for marketplace-catalog service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_catalog.client import MarketplaceCatalogClient
    from types_aiobotocore_marketplace_catalog.paginator import (
        ListChangeSetsPaginator,
        ListEntitiesPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-catalog") as client:
        client: MarketplaceCatalogClient

        list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
        list_entities_paginator: ListEntitiesPaginator = client.get_paginator("list_entities")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChangeSetsRequestPaginateTypeDef,
    ListChangeSetsResponseTypeDef,
    ListEntitiesRequestPaginateTypeDef,
    ListEntitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListChangeSetsPaginator", "ListEntitiesPaginator")


if TYPE_CHECKING:
    _ListChangeSetsPaginatorBase = AioPaginator[ListChangeSetsResponseTypeDef]
else:
    _ListChangeSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChangeSetsPaginator(_ListChangeSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListChangeSets.html#MarketplaceCatalog.Paginator.ListChangeSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listchangesetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChangeSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChangeSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListChangeSets.html#MarketplaceCatalog.Paginator.ListChangeSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listchangesetspaginator)
        """


if TYPE_CHECKING:
    _ListEntitiesPaginatorBase = AioPaginator[ListEntitiesResponseTypeDef]
else:
    _ListEntitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEntitiesPaginator(_ListEntitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListEntities.html#MarketplaceCatalog.Paginator.ListEntities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listentitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListEntities.html#MarketplaceCatalog.Paginator.ListEntities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listentitiespaginator)
        """
