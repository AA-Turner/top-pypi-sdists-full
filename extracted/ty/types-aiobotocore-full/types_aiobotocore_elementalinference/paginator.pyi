"""
Type annotations for elementalinference service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elementalinference.client import ElementalInferenceClient
    from types_aiobotocore_elementalinference.paginator import (
        ListFeedsPaginator,
    )

    session = get_session()
    with session.create_client("elementalinference") as client:
        client: ElementalInferenceClient

        list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListFeedsRequestPaginateTypeDef, ListFeedsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListFeedsPaginator",)

if TYPE_CHECKING:
    _ListFeedsPaginatorBase = AioPaginator[ListFeedsResponseTypeDef]
else:
    _ListFeedsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFeedsPaginator(_ListFeedsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/paginators/#listfeedspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFeedsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFeedsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/paginators/#listfeedspaginator)
        """
