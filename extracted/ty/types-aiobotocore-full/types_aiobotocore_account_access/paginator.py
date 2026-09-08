"""
Type annotations for account-access service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_account_access.client import AccountAccessClient
    from types_aiobotocore_account_access.paginator import (
        ListApplicationsPaginator,
        ListEntitlementsPaginator,
    )

    session = get_session()
    with session.create_client("account-access") as client:
        client: AccountAccessClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_entitlements_paginator: ListEntitlementsPaginator = client.get_paginator("list_entitlements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListEntitlementsRequestPaginateTypeDef,
    ListEntitlementsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListApplicationsPaginator", "ListEntitlementsPaginator")


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/paginator/ListApplications.html#AccountAccess.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/paginator/ListApplications.html#AccountAccess.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListEntitlementsPaginatorBase = AioPaginator[ListEntitlementsResponseTypeDef]
else:
    _ListEntitlementsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEntitlementsPaginator(_ListEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/paginator/ListEntitlements.html#AccountAccess.Paginator.ListEntitlements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/paginators/#listentitlementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntitlementsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEntitlementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access/paginator/ListEntitlements.html#AccountAccess.Paginator.ListEntitlements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_account_access/paginators/#listentitlementspaginator)
        """
