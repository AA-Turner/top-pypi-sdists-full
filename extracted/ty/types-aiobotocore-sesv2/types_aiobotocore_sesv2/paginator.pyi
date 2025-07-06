"""
Type annotations for sesv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sesv2.client import SESV2Client
    from types_aiobotocore_sesv2.paginator import (
        ListMultiRegionEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("sesv2") as client:
        client: SESV2Client

        list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListMultiRegionEndpointsRequestPaginateTypeDef,
    ListMultiRegionEndpointsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListMultiRegionEndpointsPaginator",)

if TYPE_CHECKING:
    _ListMultiRegionEndpointsPaginatorBase = AioPaginator[ListMultiRegionEndpointsResponseTypeDef]
else:
    _ListMultiRegionEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMultiRegionEndpointsPaginator(_ListMultiRegionEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listmultiregionendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMultiRegionEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMultiRegionEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listmultiregionendpointspaginator)
        """
