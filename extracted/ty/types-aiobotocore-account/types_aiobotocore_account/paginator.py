"""
Type annotations for account service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_account.client import AccountClient
    from types_aiobotocore_account.paginator import (
        ListRegionsPaginator,
    )

    session = get_session()
    with session.create_client("account") as client:
        client: AccountClient

        list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListRegionsRequestPaginateTypeDef, ListRegionsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRegionsPaginator",)


if TYPE_CHECKING:
    _ListRegionsPaginatorBase = AioPaginator[ListRegionsResponseTypeDef]
else:
    _ListRegionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRegionsPaginator(_ListRegionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/paginator/ListRegions.html#Account.Paginator.ListRegions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/paginators/#listregionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/paginator/ListRegions.html#Account.Paginator.ListRegions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account/paginators/#listregionspaginator)
        """
