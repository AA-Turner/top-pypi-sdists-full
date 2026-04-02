"""
Type annotations for elementalinference service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elementalinference.client import ElementalInferenceClient
    from mypy_boto3_elementalinference.paginator import (
        ListFeedsPaginator,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

    list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListFeedsRequestPaginateTypeDef, ListFeedsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListFeedsPaginator",)


if TYPE_CHECKING:
    _ListFeedsPaginatorBase = Paginator[ListFeedsResponseTypeDef]
else:
    _ListFeedsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFeedsPaginator(_ListFeedsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#listfeedspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFeedsRequestPaginateTypeDef]
    ) -> PageIterator[ListFeedsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#listfeedspaginator)
        """
