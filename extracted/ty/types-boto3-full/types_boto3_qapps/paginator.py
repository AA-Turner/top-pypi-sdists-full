"""
Type annotations for qapps service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qapps/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_qapps.client import QAppsClient
    from types_boto3_qapps.paginator import (
        ListLibraryItemsPaginator,
        ListQAppsPaginator,
    )

    session = Session()
    client: QAppsClient = session.client("qapps")

    list_library_items_paginator: ListLibraryItemsPaginator = client.get_paginator("list_library_items")
    list_q_apps_paginator: ListQAppsPaginator = client.get_paginator("list_q_apps")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListLibraryItemsPaginatorBase = Paginator[ListLibraryItemsOutputTypeDef]
else:
    _ListLibraryItemsPaginatorBase = Paginator  # type: ignore[assignment]


class ListLibraryItemsPaginator(_ListLibraryItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qapps/paginators/#listlibraryitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLibraryItemsInputPaginateTypeDef]
    ) -> PageIterator[ListLibraryItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListLibraryItems.html#QApps.Paginator.ListLibraryItems.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qapps/paginators/#listlibraryitemspaginator)
        """


if TYPE_CHECKING:
    _ListQAppsPaginatorBase = Paginator[ListQAppsOutputTypeDef]
else:
    _ListQAppsPaginatorBase = Paginator  # type: ignore[assignment]


class ListQAppsPaginator(_ListQAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qapps/paginators/#listqappspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQAppsInputPaginateTypeDef]
    ) -> PageIterator[ListQAppsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/paginator/ListQApps.html#QApps.Paginator.ListQApps.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qapps/paginators/#listqappspaginator)
        """
