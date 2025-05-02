"""
Type annotations for eks service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_eks.client import EKSClient
    from types_aiobotocore_eks.paginator import (
        DescribeAddonVersionsPaginator,
        DescribeClusterVersionsPaginator,
        ListAccessEntriesPaginator,
        ListAccessPoliciesPaginator,
        ListAddonsPaginator,
        ListAssociatedAccessPoliciesPaginator,
        ListClustersPaginator,
        ListEksAnywhereSubscriptionsPaginator,
        ListFargateProfilesPaginator,
        ListIdentityProviderConfigsPaginator,
        ListInsightsPaginator,
        ListNodegroupsPaginator,
        ListPodIdentityAssociationsPaginator,
        ListUpdatesPaginator,
    )

    session = get_session()
    with session.create_client("eks") as client:
        client: EKSClient

        describe_addon_versions_paginator: DescribeAddonVersionsPaginator = client.get_paginator("describe_addon_versions")
        describe_cluster_versions_paginator: DescribeClusterVersionsPaginator = client.get_paginator("describe_cluster_versions")
        list_access_entries_paginator: ListAccessEntriesPaginator = client.get_paginator("list_access_entries")
        list_access_policies_paginator: ListAccessPoliciesPaginator = client.get_paginator("list_access_policies")
        list_addons_paginator: ListAddonsPaginator = client.get_paginator("list_addons")
        list_associated_access_policies_paginator: ListAssociatedAccessPoliciesPaginator = client.get_paginator("list_associated_access_policies")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_eks_anywhere_subscriptions_paginator: ListEksAnywhereSubscriptionsPaginator = client.get_paginator("list_eks_anywhere_subscriptions")
        list_fargate_profiles_paginator: ListFargateProfilesPaginator = client.get_paginator("list_fargate_profiles")
        list_identity_provider_configs_paginator: ListIdentityProviderConfigsPaginator = client.get_paginator("list_identity_provider_configs")
        list_insights_paginator: ListInsightsPaginator = client.get_paginator("list_insights")
        list_nodegroups_paginator: ListNodegroupsPaginator = client.get_paginator("list_nodegroups")
        list_pod_identity_associations_paginator: ListPodIdentityAssociationsPaginator = client.get_paginator("list_pod_identity_associations")
        list_updates_paginator: ListUpdatesPaginator = client.get_paginator("list_updates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAddonVersionsRequestPaginateTypeDef,
    DescribeAddonVersionsResponseTypeDef,
    DescribeClusterVersionsRequestPaginateTypeDef,
    DescribeClusterVersionsResponseTypeDef,
    ListAccessEntriesRequestPaginateTypeDef,
    ListAccessEntriesResponseTypeDef,
    ListAccessPoliciesRequestPaginateTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListAddonsRequestPaginateTypeDef,
    ListAddonsResponseTypeDef,
    ListAssociatedAccessPoliciesRequestPaginateTypeDef,
    ListAssociatedAccessPoliciesResponseTypeDef,
    ListClustersRequestPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListEksAnywhereSubscriptionsRequestPaginateTypeDef,
    ListEksAnywhereSubscriptionsResponseTypeDef,
    ListFargateProfilesRequestPaginateTypeDef,
    ListFargateProfilesResponseTypeDef,
    ListIdentityProviderConfigsRequestPaginateTypeDef,
    ListIdentityProviderConfigsResponseTypeDef,
    ListInsightsRequestPaginateTypeDef,
    ListInsightsResponseTypeDef,
    ListNodegroupsRequestPaginateTypeDef,
    ListNodegroupsResponseTypeDef,
    ListPodIdentityAssociationsRequestPaginateTypeDef,
    ListPodIdentityAssociationsResponseTypeDef,
    ListUpdatesRequestPaginateTypeDef,
    ListUpdatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAddonVersionsPaginator",
    "DescribeClusterVersionsPaginator",
    "ListAccessEntriesPaginator",
    "ListAccessPoliciesPaginator",
    "ListAddonsPaginator",
    "ListAssociatedAccessPoliciesPaginator",
    "ListClustersPaginator",
    "ListEksAnywhereSubscriptionsPaginator",
    "ListFargateProfilesPaginator",
    "ListIdentityProviderConfigsPaginator",
    "ListInsightsPaginator",
    "ListNodegroupsPaginator",
    "ListPodIdentityAssociationsPaginator",
    "ListUpdatesPaginator",
)


if TYPE_CHECKING:
    _DescribeAddonVersionsPaginatorBase = AioPaginator[DescribeAddonVersionsResponseTypeDef]
else:
    _DescribeAddonVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAddonVersionsPaginator(_DescribeAddonVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeAddonVersions.html#EKS.Paginator.DescribeAddonVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#describeaddonversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAddonVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAddonVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeAddonVersions.html#EKS.Paginator.DescribeAddonVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#describeaddonversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeClusterVersionsPaginatorBase = AioPaginator[DescribeClusterVersionsResponseTypeDef]
else:
    _DescribeClusterVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeClusterVersionsPaginator(_DescribeClusterVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeClusterVersions.html#EKS.Paginator.DescribeClusterVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#describeclusterversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeClusterVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/DescribeClusterVersions.html#EKS.Paginator.DescribeClusterVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#describeclusterversionspaginator)
        """


if TYPE_CHECKING:
    _ListAccessEntriesPaginatorBase = AioPaginator[ListAccessEntriesResponseTypeDef]
else:
    _ListAccessEntriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccessEntriesPaginator(_ListAccessEntriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessEntries.html#EKS.Paginator.ListAccessEntries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccessentriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessEntriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccessEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessEntries.html#EKS.Paginator.ListAccessEntries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccessentriespaginator)
        """


if TYPE_CHECKING:
    _ListAccessPoliciesPaginatorBase = AioPaginator[ListAccessPoliciesResponseTypeDef]
else:
    _ListAccessPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccessPoliciesPaginator(_ListAccessPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessPolicies.html#EKS.Paginator.ListAccessPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccesspoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccessPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAccessPolicies.html#EKS.Paginator.ListAccessPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaccesspoliciespaginator)
        """


if TYPE_CHECKING:
    _ListAddonsPaginatorBase = AioPaginator[ListAddonsResponseTypeDef]
else:
    _ListAddonsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAddonsPaginator(_ListAddonsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAddons.html#EKS.Paginator.ListAddons)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaddonspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAddonsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAddonsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAddons.html#EKS.Paginator.ListAddons.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listaddonspaginator)
        """


if TYPE_CHECKING:
    _ListAssociatedAccessPoliciesPaginatorBase = AioPaginator[
        ListAssociatedAccessPoliciesResponseTypeDef
    ]
else:
    _ListAssociatedAccessPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociatedAccessPoliciesPaginator(_ListAssociatedAccessPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAssociatedAccessPolicies.html#EKS.Paginator.ListAssociatedAccessPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listassociatedaccesspoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociatedAccessPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociatedAccessPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListAssociatedAccessPolicies.html#EKS.Paginator.ListAssociatedAccessPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listassociatedaccesspoliciespaginator)
        """


if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersResponseTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListClusters.html#EKS.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListClusters.html#EKS.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listclusterspaginator)
        """


if TYPE_CHECKING:
    _ListEksAnywhereSubscriptionsPaginatorBase = AioPaginator[
        ListEksAnywhereSubscriptionsResponseTypeDef
    ]
else:
    _ListEksAnywhereSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEksAnywhereSubscriptionsPaginator(_ListEksAnywhereSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListEksAnywhereSubscriptions.html#EKS.Paginator.ListEksAnywhereSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listeksanywheresubscriptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEksAnywhereSubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEksAnywhereSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListEksAnywhereSubscriptions.html#EKS.Paginator.ListEksAnywhereSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listeksanywheresubscriptionspaginator)
        """


if TYPE_CHECKING:
    _ListFargateProfilesPaginatorBase = AioPaginator[ListFargateProfilesResponseTypeDef]
else:
    _ListFargateProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFargateProfilesPaginator(_ListFargateProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListFargateProfiles.html#EKS.Paginator.ListFargateProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listfargateprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFargateProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFargateProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListFargateProfiles.html#EKS.Paginator.ListFargateProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listfargateprofilespaginator)
        """


if TYPE_CHECKING:
    _ListIdentityProviderConfigsPaginatorBase = AioPaginator[
        ListIdentityProviderConfigsResponseTypeDef
    ]
else:
    _ListIdentityProviderConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIdentityProviderConfigsPaginator(_ListIdentityProviderConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListIdentityProviderConfigs.html#EKS.Paginator.ListIdentityProviderConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listidentityproviderconfigspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdentityProviderConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIdentityProviderConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListIdentityProviderConfigs.html#EKS.Paginator.ListIdentityProviderConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listidentityproviderconfigspaginator)
        """


if TYPE_CHECKING:
    _ListInsightsPaginatorBase = AioPaginator[ListInsightsResponseTypeDef]
else:
    _ListInsightsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInsightsPaginator(_ListInsightsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListInsights.html#EKS.Paginator.ListInsights)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listinsightspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInsightsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListInsights.html#EKS.Paginator.ListInsights.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listinsightspaginator)
        """


if TYPE_CHECKING:
    _ListNodegroupsPaginatorBase = AioPaginator[ListNodegroupsResponseTypeDef]
else:
    _ListNodegroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNodegroupsPaginator(_ListNodegroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListNodegroups.html#EKS.Paginator.ListNodegroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listnodegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNodegroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNodegroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListNodegroups.html#EKS.Paginator.ListNodegroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listnodegroupspaginator)
        """


if TYPE_CHECKING:
    _ListPodIdentityAssociationsPaginatorBase = AioPaginator[
        ListPodIdentityAssociationsResponseTypeDef
    ]
else:
    _ListPodIdentityAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPodIdentityAssociationsPaginator(_ListPodIdentityAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListPodIdentityAssociations.html#EKS.Paginator.ListPodIdentityAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listpodidentityassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPodIdentityAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPodIdentityAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListPodIdentityAssociations.html#EKS.Paginator.ListPodIdentityAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listpodidentityassociationspaginator)
        """


if TYPE_CHECKING:
    _ListUpdatesPaginatorBase = AioPaginator[ListUpdatesResponseTypeDef]
else:
    _ListUpdatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUpdatesPaginator(_ListUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListUpdates.html#EKS.Paginator.ListUpdates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listupdatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUpdatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/paginator/ListUpdates.html#EKS.Paginator.ListUpdates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/paginators/#listupdatespaginator)
        """
