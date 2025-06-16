"""
Type annotations for mediastore-data service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediastore_data.client import MediaStoreDataClient
    from types_aiobotocore_mediastore_data.paginator import (
        ListItemsPaginator,
    )

    session = get_session()
    with session.create_client("mediastore-data") as client:
        client: MediaStoreDataClient

        list_items_paginator: ListItemsPaginator = client.get_paginator("list_items")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListItemsRequestPaginateTypeDef, ListItemsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListItemsPaginator",)


if TYPE_CHECKING:
    _ListItemsPaginatorBase = AioPaginator[ListItemsResponseTypeDef]
else:
    _ListItemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListItemsPaginator(_ListItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/paginator/ListItems.html#MediaStoreData.Paginator.ListItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators/#listitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/paginator/ListItems.html#MediaStoreData.Paginator.ListItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/paginators/#listitemspaginator)
        """
