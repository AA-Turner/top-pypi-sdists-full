"""
Main interface for route53globalresolver service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53globalresolver import (
        Client,
        ListAccessSourcesPaginator,
        ListAccessTokensPaginator,
        ListDNSViewsPaginator,
        ListFirewallDomainListsPaginator,
        ListFirewallDomainsPaginator,
        ListFirewallRulesPaginator,
        ListGlobalResolversPaginator,
        ListHostedZoneAssociationsPaginator,
        ListManagedFirewallDomainListsPaginator,
        Route53GlobalResolverClient,
    )

    session = get_session()
    async with session.create_client("route53globalresolver") as client:
        client: Route53GlobalResolverClient
        ...


    list_access_sources_paginator: ListAccessSourcesPaginator = client.get_paginator("list_access_sources")
    list_access_tokens_paginator: ListAccessTokensPaginator = client.get_paginator("list_access_tokens")
    list_dns_views_paginator: ListDNSViewsPaginator = client.get_paginator("list_dns_views")
    list_firewall_domain_lists_paginator: ListFirewallDomainListsPaginator = client.get_paginator("list_firewall_domain_lists")
    list_firewall_domains_paginator: ListFirewallDomainsPaginator = client.get_paginator("list_firewall_domains")
    list_firewall_rules_paginator: ListFirewallRulesPaginator = client.get_paginator("list_firewall_rules")
    list_global_resolvers_paginator: ListGlobalResolversPaginator = client.get_paginator("list_global_resolvers")
    list_hosted_zone_associations_paginator: ListHostedZoneAssociationsPaginator = client.get_paginator("list_hosted_zone_associations")
    list_managed_firewall_domain_lists_paginator: ListManagedFirewallDomainListsPaginator = client.get_paginator("list_managed_firewall_domain_lists")
    ```
"""

from .client import Route53GlobalResolverClient
from .paginator import (
    ListAccessSourcesPaginator,
    ListAccessTokensPaginator,
    ListDNSViewsPaginator,
    ListFirewallDomainListsPaginator,
    ListFirewallDomainsPaginator,
    ListFirewallRulesPaginator,
    ListGlobalResolversPaginator,
    ListHostedZoneAssociationsPaginator,
    ListManagedFirewallDomainListsPaginator,
)

Client = Route53GlobalResolverClient

__all__ = (
    "Client",
    "ListAccessSourcesPaginator",
    "ListAccessTokensPaginator",
    "ListDNSViewsPaginator",
    "ListFirewallDomainListsPaginator",
    "ListFirewallDomainsPaginator",
    "ListFirewallRulesPaginator",
    "ListGlobalResolversPaginator",
    "ListHostedZoneAssociationsPaginator",
    "ListManagedFirewallDomainListsPaginator",
    "Route53GlobalResolverClient",
)
