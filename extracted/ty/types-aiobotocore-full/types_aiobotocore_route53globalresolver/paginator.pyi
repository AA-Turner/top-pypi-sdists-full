"""
Type annotations for route53globalresolver service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53globalresolver.client import Route53GlobalResolverClient
    from types_aiobotocore_route53globalresolver.paginator import (
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

    session = get_session()
    with session.create_client("route53globalresolver") as client:
        client: Route53GlobalResolverClient

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

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccessSourcesInputPaginateTypeDef,
    ListAccessSourcesOutputTypeDef,
    ListAccessTokensInputPaginateTypeDef,
    ListAccessTokensOutputTypeDef,
    ListDNSViewsInputPaginateTypeDef,
    ListDNSViewsOutputTypeDef,
    ListFirewallDomainListsInputPaginateTypeDef,
    ListFirewallDomainListsOutputTypeDef,
    ListFirewallDomainsInputPaginateTypeDef,
    ListFirewallDomainsOutputTypeDef,
    ListFirewallRulesInputPaginateTypeDef,
    ListFirewallRulesOutputTypeDef,
    ListGlobalResolversInputPaginateTypeDef,
    ListGlobalResolversOutputTypeDef,
    ListHostedZoneAssociationsInputPaginateTypeDef,
    ListHostedZoneAssociationsOutputTypeDef,
    ListManagedFirewallDomainListsInputPaginateTypeDef,
    ListManagedFirewallDomainListsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccessSourcesPaginator",
    "ListAccessTokensPaginator",
    "ListDNSViewsPaginator",
    "ListFirewallDomainListsPaginator",
    "ListFirewallDomainsPaginator",
    "ListFirewallRulesPaginator",
    "ListGlobalResolversPaginator",
    "ListHostedZoneAssociationsPaginator",
    "ListManagedFirewallDomainListsPaginator",
)

if TYPE_CHECKING:
    _ListAccessSourcesPaginatorBase = AioPaginator[ListAccessSourcesOutputTypeDef]
else:
    _ListAccessSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessSourcesPaginator(_ListAccessSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListAccessSources.html#Route53GlobalResolver.Paginator.ListAccessSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listaccesssourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessSourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAccessSourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListAccessSources.html#Route53GlobalResolver.Paginator.ListAccessSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listaccesssourcespaginator)
        """

if TYPE_CHECKING:
    _ListAccessTokensPaginatorBase = AioPaginator[ListAccessTokensOutputTypeDef]
else:
    _ListAccessTokensPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessTokensPaginator(_ListAccessTokensPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListAccessTokens.html#Route53GlobalResolver.Paginator.ListAccessTokens)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listaccesstokenspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessTokensInputPaginateTypeDef]
    ) -> AioPageIterator[ListAccessTokensOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListAccessTokens.html#Route53GlobalResolver.Paginator.ListAccessTokens.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listaccesstokenspaginator)
        """

if TYPE_CHECKING:
    _ListDNSViewsPaginatorBase = AioPaginator[ListDNSViewsOutputTypeDef]
else:
    _ListDNSViewsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDNSViewsPaginator(_ListDNSViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListDNSViews.html#Route53GlobalResolver.Paginator.ListDNSViews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listdnsviewspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDNSViewsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDNSViewsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListDNSViews.html#Route53GlobalResolver.Paginator.ListDNSViews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listdnsviewspaginator)
        """

if TYPE_CHECKING:
    _ListFirewallDomainListsPaginatorBase = AioPaginator[ListFirewallDomainListsOutputTypeDef]
else:
    _ListFirewallDomainListsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFirewallDomainListsPaginator(_ListFirewallDomainListsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListFirewallDomainLists.html#Route53GlobalResolver.Paginator.ListFirewallDomainLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listfirewalldomainlistspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFirewallDomainListsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFirewallDomainListsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListFirewallDomainLists.html#Route53GlobalResolver.Paginator.ListFirewallDomainLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listfirewalldomainlistspaginator)
        """

if TYPE_CHECKING:
    _ListFirewallDomainsPaginatorBase = AioPaginator[ListFirewallDomainsOutputTypeDef]
else:
    _ListFirewallDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFirewallDomainsPaginator(_ListFirewallDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListFirewallDomains.html#Route53GlobalResolver.Paginator.ListFirewallDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listfirewalldomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFirewallDomainsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFirewallDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListFirewallDomains.html#Route53GlobalResolver.Paginator.ListFirewallDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listfirewalldomainspaginator)
        """

if TYPE_CHECKING:
    _ListFirewallRulesPaginatorBase = AioPaginator[ListFirewallRulesOutputTypeDef]
else:
    _ListFirewallRulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFirewallRulesPaginator(_ListFirewallRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListFirewallRules.html#Route53GlobalResolver.Paginator.ListFirewallRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listfirewallrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFirewallRulesInputPaginateTypeDef]
    ) -> AioPageIterator[ListFirewallRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListFirewallRules.html#Route53GlobalResolver.Paginator.ListFirewallRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listfirewallrulespaginator)
        """

if TYPE_CHECKING:
    _ListGlobalResolversPaginatorBase = AioPaginator[ListGlobalResolversOutputTypeDef]
else:
    _ListGlobalResolversPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGlobalResolversPaginator(_ListGlobalResolversPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListGlobalResolvers.html#Route53GlobalResolver.Paginator.ListGlobalResolvers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listglobalresolverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGlobalResolversInputPaginateTypeDef]
    ) -> AioPageIterator[ListGlobalResolversOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListGlobalResolvers.html#Route53GlobalResolver.Paginator.ListGlobalResolvers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listglobalresolverspaginator)
        """

if TYPE_CHECKING:
    _ListHostedZoneAssociationsPaginatorBase = AioPaginator[ListHostedZoneAssociationsOutputTypeDef]
else:
    _ListHostedZoneAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHostedZoneAssociationsPaginator(_ListHostedZoneAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListHostedZoneAssociations.html#Route53GlobalResolver.Paginator.ListHostedZoneAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listhostedzoneassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHostedZoneAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListHostedZoneAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListHostedZoneAssociations.html#Route53GlobalResolver.Paginator.ListHostedZoneAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listhostedzoneassociationspaginator)
        """

if TYPE_CHECKING:
    _ListManagedFirewallDomainListsPaginatorBase = AioPaginator[
        ListManagedFirewallDomainListsOutputTypeDef
    ]
else:
    _ListManagedFirewallDomainListsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedFirewallDomainListsPaginator(_ListManagedFirewallDomainListsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListManagedFirewallDomainLists.html#Route53GlobalResolver.Paginator.ListManagedFirewallDomainLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listmanagedfirewalldomainlistspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedFirewallDomainListsInputPaginateTypeDef]
    ) -> AioPageIterator[ListManagedFirewallDomainListsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53globalresolver/paginator/ListManagedFirewallDomainLists.html#Route53GlobalResolver.Paginator.ListManagedFirewallDomainLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53globalresolver/paginators/#listmanagedfirewalldomainlistspaginator)
        """
