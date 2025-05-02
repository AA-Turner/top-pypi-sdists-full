"""
Main interface for route53domains service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53domains import (
        Client,
        ListDomainsPaginator,
        ListOperationsPaginator,
        ListPricesPaginator,
        Route53DomainsClient,
        ViewBillingPaginator,
    )

    session = get_session()
    async with session.create_client("route53domains") as client:
        client: Route53DomainsClient
        ...


    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    list_prices_paginator: ListPricesPaginator = client.get_paginator("list_prices")
    view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```
"""

from .client import Route53DomainsClient
from .paginator import (
    ListDomainsPaginator,
    ListOperationsPaginator,
    ListPricesPaginator,
    ViewBillingPaginator,
)

Client = Route53DomainsClient


__all__ = (
    "Client",
    "ListDomainsPaginator",
    "ListOperationsPaginator",
    "ListPricesPaginator",
    "Route53DomainsClient",
    "ViewBillingPaginator",
)
