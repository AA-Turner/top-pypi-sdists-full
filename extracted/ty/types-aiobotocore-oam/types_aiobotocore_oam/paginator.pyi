"""
Type annotations for oam service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_oam.client import CloudWatchObservabilityAccessManagerClient
    from types_aiobotocore_oam.paginator import (
        ListAttachedLinksPaginator,
        ListLinksPaginator,
        ListSinksPaginator,
    )

    session = get_session()
    with session.create_client("oam") as client:
        client: CloudWatchObservabilityAccessManagerClient

        list_attached_links_paginator: ListAttachedLinksPaginator = client.get_paginator("list_attached_links")
        list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
        list_sinks_paginator: ListSinksPaginator = client.get_paginator("list_sinks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListAttachedLinksPaginatorBase = AioPaginator[ListAttachedLinksOutputTypeDef]
else:
    _ListAttachedLinksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAttachedLinksPaginator(_ListAttachedLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listattachedlinkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachedLinksInputPaginateTypeDef]
    ) -> AioPageIterator[ListAttachedLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListAttachedLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListAttachedLinks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listattachedlinkspaginator)
        """

if TYPE_CHECKING:
    _ListLinksPaginatorBase = AioPaginator[ListLinksOutputTypeDef]
else:
    _ListLinksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLinksPaginator(_ListLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listlinkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLinksInputPaginateTypeDef]
    ) -> AioPageIterator[ListLinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListLinks.html#CloudWatchObservabilityAccessManager.Paginator.ListLinks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listlinkspaginator)
        """

if TYPE_CHECKING:
    _ListSinksPaginatorBase = AioPaginator[ListSinksOutputTypeDef]
else:
    _ListSinksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSinksPaginator(_ListSinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listsinkspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSinksInputPaginateTypeDef]
    ) -> AioPageIterator[ListSinksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/oam/paginator/ListSinks.html#CloudWatchObservabilityAccessManager.Paginator.ListSinks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/paginators/#listsinkspaginator)
        """
