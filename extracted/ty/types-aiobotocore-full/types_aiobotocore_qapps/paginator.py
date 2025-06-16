"""
Type annotations for qapps service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_qapps.client import QAppsClient
    from types_aiobotocore_qapps.paginator import (
        ListLibraryItemsPaginator,
        ListQAppsPaginator,
    )

    session = get_session()
    with session.create_client("qapps") as client:
        client: QAppsClient

        list_library_items_paginator: ListLibraryItemsPaginator = client.get_paginator("list_library_items")
        list_q_apps_paginator: ListQAppsPaginator = client.get_paginator("list_q_apps")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListLibraryItemsInputPaginateTypeDef,
    ListLibraryItemsOutputTypeDef,
    ListQAppsInputPaginateTypeDef,
    ListQAppsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListLibraryItemsPaginator", "ListQAppsPaginator")


if TYPE_CHECKING:
    _ListLibraryItemsPaginatorBase = AioPaginator[ListLibraryItemsOutputTypeDef]
else:
    _ListLibraryItemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLibraryItemsPaginator(_ListLibraryItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listlibraryitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLibraryItemsInputPaginateTypeDef]
    ) -> AioPageIterator[ListLibraryItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listlibraryitemspaginator)
        """


if TYPE_CHECKING:
    _ListQAppsPaginatorBase = AioPaginator[ListQAppsOutputTypeDef]
else:
    _ListQAppsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQAppsPaginator(_ListQAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listqappspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQAppsInputPaginateTypeDef]
    ) -> AioPageIterator[ListQAppsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/paginators/#listqappspaginator)
        """
