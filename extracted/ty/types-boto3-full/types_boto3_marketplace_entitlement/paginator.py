"""
Type annotations for marketplace-entitlement service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
    from types_boto3_marketplace_entitlement.paginator import (
        GetEntitlementsPaginator,
    )

    session = Session()
    client: MarketplaceEntitlementServiceClient = session.client("marketplace-entitlement")

    get_entitlements_paginator: GetEntitlementsPaginator = client.get_paginator("get_entitlements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import GetEntitlementsRequestPaginateTypeDef, GetEntitlementsResultTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("GetEntitlementsPaginator",)


if TYPE_CHECKING:
    _GetEntitlementsPaginatorBase = Paginator[GetEntitlementsResultTypeDef]
else:
    _GetEntitlementsPaginatorBase = Paginator  # type: ignore[assignment]


class GetEntitlementsPaginator(_GetEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/paginators/#getentitlementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEntitlementsRequestPaginateTypeDef]
    ) -> PageIterator[GetEntitlementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement/paginator/GetEntitlements.html#MarketplaceEntitlementService.Paginator.GetEntitlements.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_entitlement/paginators/#getentitlementspaginator)
        """
