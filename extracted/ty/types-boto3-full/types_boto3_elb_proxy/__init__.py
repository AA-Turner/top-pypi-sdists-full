"""
Main interface for elb-proxy service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_elb_proxy import (
        Client,
        ELBProxyClient,
        ListCertificateAssociationsPaginator,
        ListProxiesPaginator,
        ListProxyUpdatesPaginator,
        ListProxyVersionsPaginator,
        ProxyActiveWaiter,
        ProxyDeletedWaiter,
        ProxyUpdateCompleteWaiter,
    )

    session = Session()
    client: ELBProxyClient = session.client("elb-proxy")

    proxy_active_waiter: ProxyActiveWaiter = client.get_waiter("proxy_active")
    proxy_deleted_waiter: ProxyDeletedWaiter = client.get_waiter("proxy_deleted")
    proxy_update_complete_waiter: ProxyUpdateCompleteWaiter = client.get_waiter("proxy_update_complete")

    list_certificate_associations_paginator: ListCertificateAssociationsPaginator = client.get_paginator("list_certificate_associations")
    list_proxies_paginator: ListProxiesPaginator = client.get_paginator("list_proxies")
    list_proxy_updates_paginator: ListProxyUpdatesPaginator = client.get_paginator("list_proxy_updates")
    list_proxy_versions_paginator: ListProxyVersionsPaginator = client.get_paginator("list_proxy_versions")
    ```
"""

from .client import ELBProxyClient
from .paginator import (
    ListCertificateAssociationsPaginator,
    ListProxiesPaginator,
    ListProxyUpdatesPaginator,
    ListProxyVersionsPaginator,
)
from .waiter import ProxyActiveWaiter, ProxyDeletedWaiter, ProxyUpdateCompleteWaiter

Client = ELBProxyClient


__all__ = (
    "Client",
    "ELBProxyClient",
    "ListCertificateAssociationsPaginator",
    "ListProxiesPaginator",
    "ListProxyUpdatesPaginator",
    "ListProxyVersionsPaginator",
    "ProxyActiveWaiter",
    "ProxyDeletedWaiter",
    "ProxyUpdateCompleteWaiter",
)
