"""
Type annotations for sagemaker-a2i-runtime service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_a2i_runtime/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient
    from types_aiobotocore_sagemaker_a2i_runtime.paginator import (
        ListHumanLoopsPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker-a2i-runtime") as client:
        client: AugmentedAIRuntimeClient

        list_human_loops_paginator: ListHumanLoopsPaginator = client.get_paginator("list_human_loops")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListHumanLoopsRequestPaginateTypeDef, ListHumanLoopsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListHumanLoopsPaginator",)

if TYPE_CHECKING:
    _ListHumanLoopsPaginatorBase = AioPaginator[ListHumanLoopsResponseTypeDef]
else:
    _ListHumanLoopsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHumanLoopsPaginator(_ListHumanLoopsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/paginator/ListHumanLoops.html#AugmentedAIRuntime.Paginator.ListHumanLoops)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_a2i_runtime/paginators/#listhumanloopspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHumanLoopsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHumanLoopsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/paginator/ListHumanLoops.html#AugmentedAIRuntime.Paginator.ListHumanLoops.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_a2i_runtime/paginators/#listhumanloopspaginator)
        """
