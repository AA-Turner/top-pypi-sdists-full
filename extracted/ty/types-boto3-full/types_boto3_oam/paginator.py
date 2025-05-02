"""
Type annotations for oam service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_oam/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_oam.client import CloudWatchObservabilityAccessManagerClient
    from types_boto3_oam.paginator import (
        ListAttachedLinksPaginator,
        ListLinksPaginator,
        ListSinksPaginator,
    )

    session = Session()
    client: CloudWatchObservabilityAccessManagerClient = session.client("oam")

    list_attached_links_paginator: ListAttachedLinksPaginator = client.get_paginator("list_attached_links")
    list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
    list_sinks_paginator: ListSinksPaginator = client.get_paginator("list_sinks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAttachedLinksInputPaginateTypeDef,
    ListAttachedLinksOutputTypeDef,
    ListLinksInputPaginateTypeDef,
    ListLinksOutputTypeDef,
    ListSinksInputPaginateTypeDef,
    ListSinksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAttachedLinksPaginator", "ListLinksPaginator", "ListSinksPaginator")


if TYPE_CHECKING:
    _ListAttachedLinksPaginatorBase = Paginator[ListAttachedLinksOutputTypeDef]
else:
    _ListAttachedLinksPaginatorBase = Paginator  # type: ignore[assignment]


class ListAttachedLinksPaginator(_ListAttachedLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_oam/paginators/#listattachedlinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachedLinksInputPaginateTypeDef]
    ) -> PageIterator[ListAttachedLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_oam/paginators/#listattachedlinkspaginator)
        """


if TYPE_CHECKING:
    _ListLinksPaginatorBase = Paginator[ListLinksOutputTypeDef]
else:
    _ListLinksPaginatorBase = Paginator  # type: ignore[assignment]


class ListLinksPaginator(_ListLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_oam/paginators/#listlinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLinksInputPaginateTypeDef]
    ) -> PageIterator[ListLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_oam/paginators/#listlinkspaginator)
        """


if TYPE_CHECKING:
    _ListSinksPaginatorBase = Paginator[ListSinksOutputTypeDef]
else:
    _ListSinksPaginatorBase = Paginator  # type: ignore[assignment]


class ListSinksPaginator(_ListSinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_oam/paginators/#listsinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSinksInputPaginateTypeDef]
    ) -> PageIterator[ListSinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_oam/paginators/#listsinkspaginator)
        """
