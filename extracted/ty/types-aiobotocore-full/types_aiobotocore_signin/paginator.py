"""
Type annotations for signin service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signin/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_signin.client import SignInServiceClient
    from types_aiobotocore_signin.paginator import (
        ListResourcePermissionStatementsPaginator,
    )

    session = get_session()
    with session.create_client("signin") as client:
        client: SignInServiceClient

        list_resource_permission_statements_paginator: ListResourcePermissionStatementsPaginator = client.get_paginator("list_resource_permission_statements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListResourcePermissionStatementsInputPaginateTypeDef,
    ListResourcePermissionStatementsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListResourcePermissionStatementsPaginator",)


if TYPE_CHECKING:
    _ListResourcePermissionStatementsPaginatorBase = AioPaginator[
        ListResourcePermissionStatementsOutputTypeDef
    ]
else:
    _ListResourcePermissionStatementsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourcePermissionStatementsPaginator(_ListResourcePermissionStatementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListResourcePermissionStatements.html#SignInService.Paginator.ListResourcePermissionStatements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signin/paginators/#listresourcepermissionstatementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePermissionStatementsInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourcePermissionStatementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListResourcePermissionStatements.html#SignInService.Paginator.ListResourcePermissionStatements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signin/paginators/#listresourcepermissionstatementspaginator)
        """
