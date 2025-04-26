"""
Type annotations for bedrock-runtime service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_runtime.client import BedrockRuntimeClient
    from types_aiobotocore_bedrock_runtime.paginator import (
        ListAsyncInvokesPaginator,
    )

    session = get_session()
    with session.create_client("bedrock-runtime") as client:
        client: BedrockRuntimeClient

        list_async_invokes_paginator: ListAsyncInvokesPaginator = client.get_paginator("list_async_invokes")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListAsyncInvokesRequestPaginateTypeDef, ListAsyncInvokesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAsyncInvokesPaginator",)


if TYPE_CHECKING:
    _ListAsyncInvokesPaginatorBase = AioPaginator[ListAsyncInvokesResponseTypeDef]
else:
    _ListAsyncInvokesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAsyncInvokesPaginator(_ListAsyncInvokesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/paginator/ListAsyncInvokes.html#BedrockRuntime.Paginator.ListAsyncInvokes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/paginators/#listasyncinvokespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAsyncInvokesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAsyncInvokesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/paginator/ListAsyncInvokes.html#BedrockRuntime.Paginator.ListAsyncInvokes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/paginators/#listasyncinvokespaginator)
        """
