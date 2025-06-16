"""
Type annotations for arc-zonal-shift service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_arc_zonal_shift.client import ARCZonalShiftClient
    from types_aiobotocore_arc_zonal_shift.paginator import (
        ListAutoshiftsPaginator,
        ListManagedResourcesPaginator,
        ListZonalShiftsPaginator,
    )

    session = get_session()
    with session.create_client("arc-zonal-shift") as client:
        client: ARCZonalShiftClient

        list_autoshifts_paginator: ListAutoshiftsPaginator = client.get_paginator("list_autoshifts")
        list_managed_resources_paginator: ListManagedResourcesPaginator = client.get_paginator("list_managed_resources")
        list_zonal_shifts_paginator: ListZonalShiftsPaginator = client.get_paginator("list_zonal_shifts")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAutoshiftsRequestPaginateTypeDef,
    ListAutoshiftsResponseTypeDef,
    ListManagedResourcesRequestPaginateTypeDef,
    ListManagedResourcesResponseTypeDef,
    ListZonalShiftsRequestPaginateTypeDef,
    ListZonalShiftsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAutoshiftsPaginator", "ListManagedResourcesPaginator", "ListZonalShiftsPaginator")


if TYPE_CHECKING:
    _ListAutoshiftsPaginatorBase = AioPaginator[ListAutoshiftsResponseTypeDef]
else:
    _ListAutoshiftsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAutoshiftsPaginator(_ListAutoshiftsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListAutoshifts.html#ARCZonalShift.Paginator.ListAutoshifts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listautoshiftspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutoshiftsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAutoshiftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListAutoshifts.html#ARCZonalShift.Paginator.ListAutoshifts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listautoshiftspaginator)
        """


if TYPE_CHECKING:
    _ListManagedResourcesPaginatorBase = AioPaginator[ListManagedResourcesResponseTypeDef]
else:
    _ListManagedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListManagedResourcesPaginator(_ListManagedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListManagedResources.html#ARCZonalShift.Paginator.ListManagedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListManagedResources.html#ARCZonalShift.Paginator.ListManagedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListZonalShiftsPaginatorBase = AioPaginator[ListZonalShiftsResponseTypeDef]
else:
    _ListZonalShiftsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListZonalShiftsPaginator(_ListZonalShiftsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListZonalShifts.html#ARCZonalShift.Paginator.ListZonalShifts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listzonalshiftspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListZonalShiftsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListZonalShiftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/paginator/ListZonalShifts.html#ARCZonalShift.Paginator.ListZonalShifts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/paginators/#listzonalshiftspaginator)
        """
