"""
Type annotations for codeguruprofiler service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codeguruprofiler.client import CodeGuruProfilerClient
    from types_aiobotocore_codeguruprofiler.paginator import (
        ListProfileTimesPaginator,
    )

    session = get_session()
    with session.create_client("codeguruprofiler") as client:
        client: CodeGuruProfilerClient

        list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListProfileTimesRequestPaginateTypeDef, ListProfileTimesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListProfileTimesPaginator",)

if TYPE_CHECKING:
    _ListProfileTimesPaginatorBase = AioPaginator[ListProfileTimesResponseTypeDef]
else:
    _ListProfileTimesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProfileTimesPaginator(_ListProfileTimesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/paginator/ListProfileTimes.html#CodeGuruProfiler.Paginator.ListProfileTimes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/paginators/#listprofiletimespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProfileTimesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProfileTimesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler/paginator/ListProfileTimes.html#CodeGuruProfiler.Paginator.ListProfileTimes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/paginators/#listprofiletimespaginator)
        """
