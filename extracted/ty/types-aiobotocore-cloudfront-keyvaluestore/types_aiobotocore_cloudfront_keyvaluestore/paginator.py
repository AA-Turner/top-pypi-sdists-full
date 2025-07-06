"""
Type annotations for cloudfront-keyvaluestore service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudfront_keyvaluestore.client import CloudFrontKeyValueStoreClient
    from types_aiobotocore_cloudfront_keyvaluestore.paginator import (
        ListKeysPaginator,
    )

    session = get_session()
    with session.create_client("cloudfront-keyvaluestore") as client:
        client: CloudFrontKeyValueStoreClient

        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListKeysRequestPaginateTypeDef, ListKeysResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListKeysPaginator",)


if TYPE_CHECKING:
    _ListKeysPaginatorBase = AioPaginator[ListKeysResponseTypeDef]
else:
    _ListKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListKeysPaginator(_ListKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/paginator/ListKeys.html#CloudFrontKeyValueStore.Paginator.ListKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/paginators/#listkeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront-keyvaluestore/paginator/ListKeys.html#CloudFrontKeyValueStore.Paginator.ListKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/paginators/#listkeyspaginator)
        """
