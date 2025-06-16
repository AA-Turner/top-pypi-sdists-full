"""
Type annotations for freetier service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_freetier/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_freetier.client import FreeTierClient
    from types_aiobotocore_freetier.paginator import (
        GetFreeTierUsagePaginator,
    )

    session = get_session()
    with session.create_client("freetier") as client:
        client: FreeTierClient

        get_free_tier_usage_paginator: GetFreeTierUsagePaginator = client.get_paginator("get_free_tier_usage")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import GetFreeTierUsageRequestPaginateTypeDef, GetFreeTierUsageResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetFreeTierUsagePaginator",)

if TYPE_CHECKING:
    _GetFreeTierUsagePaginatorBase = AioPaginator[GetFreeTierUsageResponseTypeDef]
else:
    _GetFreeTierUsagePaginatorBase = AioPaginator  # type: ignore[assignment]

class GetFreeTierUsagePaginator(_GetFreeTierUsagePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/freetier/paginator/GetFreeTierUsage.html#FreeTier.Paginator.GetFreeTierUsage)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_freetier/paginators/#getfreetierusagepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetFreeTierUsageRequestPaginateTypeDef]
    ) -> AioPageIterator[GetFreeTierUsageResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/freetier/paginator/GetFreeTierUsage.html#FreeTier.Paginator.GetFreeTierUsage.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_freetier/paginators/#getfreetierusagepaginator)
        """
