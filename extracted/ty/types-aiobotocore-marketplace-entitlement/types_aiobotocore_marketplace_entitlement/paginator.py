"""
Type annotations for marketplace-entitlement service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
    from types_aiobotocore_marketplace_entitlement.paginator import (
        GetEntitlementsPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-entitlement") as client:
        client: MarketplaceEntitlementServiceClient

        get_entitlements_paginator: GetEntitlementsPaginator = client.get_paginator("get_entitlements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import GetEntitlementsRequestPaginateTypeDef, GetEntitlementsResultTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("GetEntitlementsPaginator",)


if TYPE_CHECKING:
    _GetEntitlementsPaginatorBase = AioPaginator[GetEntitlementsResultTypeDef]
else:
    _GetEntitlementsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetEntitlementsPaginator(_GetEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/#getentitlementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEntitlementsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetEntitlementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/#getentitlementspaginator)
        """
