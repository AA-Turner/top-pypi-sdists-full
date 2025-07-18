"""
Type annotations for aiops service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_aiops.client import AIOpsClient
    from types_aiobotocore_aiops.paginator import (
        ListInvestigationGroupsPaginator,
    )

    session = get_session()
    with session.create_client("aiops") as client:
        client: AIOpsClient

        list_investigation_groups_paginator: ListInvestigationGroupsPaginator = client.get_paginator("list_investigation_groups")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListInvestigationGroupsInputPaginateTypeDef,
    ListInvestigationGroupsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListInvestigationGroupsPaginator",)


if TYPE_CHECKING:
    _ListInvestigationGroupsPaginatorBase = AioPaginator[ListInvestigationGroupsOutputTypeDef]
else:
    _ListInvestigationGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInvestigationGroupsPaginator(_ListInvestigationGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/paginator/ListInvestigationGroups.html#AIOps.Paginator.ListInvestigationGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/paginators/#listinvestigationgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvestigationGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListInvestigationGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/paginator/ListInvestigationGroups.html#AIOps.Paginator.ListInvestigationGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/paginators/#listinvestigationgroupspaginator)
        """
