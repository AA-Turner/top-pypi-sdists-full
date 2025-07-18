"""
Type annotations for securityhub service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_securityhub.client import SecurityHubClient
    from types_aiobotocore_securityhub.paginator import (
        DescribeActionTargetsPaginator,
        DescribeProductsPaginator,
        DescribeProductsV2Paginator,
        DescribeStandardsControlsPaginator,
        DescribeStandardsPaginator,
        GetEnabledStandardsPaginator,
        GetFindingHistoryPaginator,
        GetFindingsPaginator,
        GetFindingsV2Paginator,
        GetInsightsPaginator,
        GetResourcesV2Paginator,
        ListAggregatorsV2Paginator,
        ListConfigurationPoliciesPaginator,
        ListConfigurationPolicyAssociationsPaginator,
        ListEnabledProductsForImportPaginator,
        ListFindingAggregatorsPaginator,
        ListInvitationsPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        ListSecurityControlDefinitionsPaginator,
        ListStandardsControlAssociationsPaginator,
    )

    session = get_session()
    with session.create_client("securityhub") as client:
        client: SecurityHubClient

        describe_action_targets_paginator: DescribeActionTargetsPaginator = client.get_paginator("describe_action_targets")
        describe_products_paginator: DescribeProductsPaginator = client.get_paginator("describe_products")
        describe_products_v2_paginator: DescribeProductsV2Paginator = client.get_paginator("describe_products_v2")
        describe_standards_controls_paginator: DescribeStandardsControlsPaginator = client.get_paginator("describe_standards_controls")
        describe_standards_paginator: DescribeStandardsPaginator = client.get_paginator("describe_standards")
        get_enabled_standards_paginator: GetEnabledStandardsPaginator = client.get_paginator("get_enabled_standards")
        get_finding_history_paginator: GetFindingHistoryPaginator = client.get_paginator("get_finding_history")
        get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
        get_findings_v2_paginator: GetFindingsV2Paginator = client.get_paginator("get_findings_v2")
        get_insights_paginator: GetInsightsPaginator = client.get_paginator("get_insights")
        get_resources_v2_paginator: GetResourcesV2Paginator = client.get_paginator("get_resources_v2")
        list_aggregators_v2_paginator: ListAggregatorsV2Paginator = client.get_paginator("list_aggregators_v2")
        list_configuration_policies_paginator: ListConfigurationPoliciesPaginator = client.get_paginator("list_configuration_policies")
        list_configuration_policy_associations_paginator: ListConfigurationPolicyAssociationsPaginator = client.get_paginator("list_configuration_policy_associations")
        list_enabled_products_for_import_paginator: ListEnabledProductsForImportPaginator = client.get_paginator("list_enabled_products_for_import")
        list_finding_aggregators_paginator: ListFindingAggregatorsPaginator = client.get_paginator("list_finding_aggregators")
        list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
        list_security_control_definitions_paginator: ListSecurityControlDefinitionsPaginator = client.get_paginator("list_security_control_definitions")
        list_standards_control_associations_paginator: ListStandardsControlAssociationsPaginator = client.get_paginator("list_standards_control_associations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeActionTargetsRequestPaginateTypeDef,
    DescribeActionTargetsResponseTypeDef,
    DescribeProductsRequestPaginateTypeDef,
    DescribeProductsResponseTypeDef,
    DescribeProductsV2RequestPaginateTypeDef,
    DescribeProductsV2ResponseTypeDef,
    DescribeStandardsControlsRequestPaginateTypeDef,
    DescribeStandardsControlsResponseTypeDef,
    DescribeStandardsRequestPaginateTypeDef,
    DescribeStandardsResponseTypeDef,
    GetEnabledStandardsRequestPaginateTypeDef,
    GetEnabledStandardsResponseTypeDef,
    GetFindingHistoryRequestPaginateTypeDef,
    GetFindingHistoryResponseTypeDef,
    GetFindingsRequestPaginateTypeDef,
    GetFindingsResponseTypeDef,
    GetFindingsV2RequestPaginateTypeDef,
    GetFindingsV2ResponseTypeDef,
    GetInsightsRequestPaginateTypeDef,
    GetInsightsResponseTypeDef,
    GetResourcesV2RequestPaginateTypeDef,
    GetResourcesV2ResponseTypeDef,
    ListAggregatorsV2RequestPaginateTypeDef,
    ListAggregatorsV2ResponseTypeDef,
    ListConfigurationPoliciesRequestPaginateTypeDef,
    ListConfigurationPoliciesResponseTypeDef,
    ListConfigurationPolicyAssociationsRequestPaginateTypeDef,
    ListConfigurationPolicyAssociationsResponseTypeDef,
    ListEnabledProductsForImportRequestPaginateTypeDef,
    ListEnabledProductsForImportResponseTypeDef,
    ListFindingAggregatorsRequestPaginateTypeDef,
    ListFindingAggregatorsResponseTypeDef,
    ListInvitationsRequestPaginateTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersRequestPaginateTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestPaginateTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListSecurityControlDefinitionsRequestPaginateTypeDef,
    ListSecurityControlDefinitionsResponseTypeDef,
    ListStandardsControlAssociationsRequestPaginateTypeDef,
    ListStandardsControlAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeActionTargetsPaginator",
    "DescribeProductsPaginator",
    "DescribeProductsV2Paginator",
    "DescribeStandardsControlsPaginator",
    "DescribeStandardsPaginator",
    "GetEnabledStandardsPaginator",
    "GetFindingHistoryPaginator",
    "GetFindingsPaginator",
    "GetFindingsV2Paginator",
    "GetInsightsPaginator",
    "GetResourcesV2Paginator",
    "ListAggregatorsV2Paginator",
    "ListConfigurationPoliciesPaginator",
    "ListConfigurationPolicyAssociationsPaginator",
    "ListEnabledProductsForImportPaginator",
    "ListFindingAggregatorsPaginator",
    "ListInvitationsPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "ListSecurityControlDefinitionsPaginator",
    "ListStandardsControlAssociationsPaginator",
)


if TYPE_CHECKING:
    _DescribeActionTargetsPaginatorBase = AioPaginator[DescribeActionTargetsResponseTypeDef]
else:
    _DescribeActionTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeActionTargetsPaginator(_DescribeActionTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeActionTargets.html#SecurityHub.Paginator.DescribeActionTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeactiontargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeActionTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeActionTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeActionTargets.html#SecurityHub.Paginator.DescribeActionTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeactiontargetspaginator)
        """


if TYPE_CHECKING:
    _DescribeProductsPaginatorBase = AioPaginator[DescribeProductsResponseTypeDef]
else:
    _DescribeProductsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeProductsPaginator(_DescribeProductsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProducts.html#SecurityHub.Paginator.DescribeProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeproductspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProductsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProducts.html#SecurityHub.Paginator.DescribeProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeproductspaginator)
        """


if TYPE_CHECKING:
    _DescribeProductsV2PaginatorBase = AioPaginator[DescribeProductsV2ResponseTypeDef]
else:
    _DescribeProductsV2PaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeProductsV2Paginator(_DescribeProductsV2PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProductsV2.html#SecurityHub.Paginator.DescribeProductsV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeproductsv2paginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProductsV2RequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeProductsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeProductsV2.html#SecurityHub.Paginator.DescribeProductsV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describeproductsv2paginator)
        """


if TYPE_CHECKING:
    _DescribeStandardsControlsPaginatorBase = AioPaginator[DescribeStandardsControlsResponseTypeDef]
else:
    _DescribeStandardsControlsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeStandardsControlsPaginator(_DescribeStandardsControlsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandardsControls.html#SecurityHub.Paginator.DescribeStandardsControls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardscontrolspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStandardsControlsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeStandardsControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandardsControls.html#SecurityHub.Paginator.DescribeStandardsControls.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardscontrolspaginator)
        """


if TYPE_CHECKING:
    _DescribeStandardsPaginatorBase = AioPaginator[DescribeStandardsResponseTypeDef]
else:
    _DescribeStandardsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeStandardsPaginator(_DescribeStandardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandards.html#SecurityHub.Paginator.DescribeStandards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStandardsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/DescribeStandards.html#SecurityHub.Paginator.DescribeStandards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#describestandardspaginator)
        """


if TYPE_CHECKING:
    _GetEnabledStandardsPaginatorBase = AioPaginator[GetEnabledStandardsResponseTypeDef]
else:
    _GetEnabledStandardsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetEnabledStandardsPaginator(_GetEnabledStandardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetEnabledStandards.html#SecurityHub.Paginator.GetEnabledStandards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getenabledstandardspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEnabledStandardsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetEnabledStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetEnabledStandards.html#SecurityHub.Paginator.GetEnabledStandards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getenabledstandardspaginator)
        """


if TYPE_CHECKING:
    _GetFindingHistoryPaginatorBase = AioPaginator[GetFindingHistoryResponseTypeDef]
else:
    _GetFindingHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetFindingHistoryPaginator(_GetFindingHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingHistory.html#SecurityHub.Paginator.GetFindingHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindinghistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetFindingHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetFindingHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingHistory.html#SecurityHub.Paginator.GetFindingHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindinghistorypaginator)
        """


if TYPE_CHECKING:
    _GetFindingsPaginatorBase = AioPaginator[GetFindingsResponseTypeDef]
else:
    _GetFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetFindingsPaginator(_GetFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindings.html#SecurityHub.Paginator.GetFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindings.html#SecurityHub.Paginator.GetFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindingspaginator)
        """


if TYPE_CHECKING:
    _GetFindingsV2PaginatorBase = AioPaginator[GetFindingsV2ResponseTypeDef]
else:
    _GetFindingsV2PaginatorBase = AioPaginator  # type: ignore[assignment]


class GetFindingsV2Paginator(_GetFindingsV2PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingsV2.html#SecurityHub.Paginator.GetFindingsV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindingsv2paginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetFindingsV2RequestPaginateTypeDef]
    ) -> AioPageIterator[GetFindingsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetFindingsV2.html#SecurityHub.Paginator.GetFindingsV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getfindingsv2paginator)
        """


if TYPE_CHECKING:
    _GetInsightsPaginatorBase = AioPaginator[GetInsightsResponseTypeDef]
else:
    _GetInsightsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetInsightsPaginator(_GetInsightsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetInsights.html#SecurityHub.Paginator.GetInsights)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getinsightspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetInsightsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetInsights.html#SecurityHub.Paginator.GetInsights.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getinsightspaginator)
        """


if TYPE_CHECKING:
    _GetResourcesV2PaginatorBase = AioPaginator[GetResourcesV2ResponseTypeDef]
else:
    _GetResourcesV2PaginatorBase = AioPaginator  # type: ignore[assignment]


class GetResourcesV2Paginator(_GetResourcesV2PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetResourcesV2.html#SecurityHub.Paginator.GetResourcesV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getresourcesv2paginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourcesV2RequestPaginateTypeDef]
    ) -> AioPageIterator[GetResourcesV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/GetResourcesV2.html#SecurityHub.Paginator.GetResourcesV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#getresourcesv2paginator)
        """


if TYPE_CHECKING:
    _ListAggregatorsV2PaginatorBase = AioPaginator[ListAggregatorsV2ResponseTypeDef]
else:
    _ListAggregatorsV2PaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAggregatorsV2Paginator(_ListAggregatorsV2PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListAggregatorsV2.html#SecurityHub.Paginator.ListAggregatorsV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listaggregatorsv2paginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAggregatorsV2RequestPaginateTypeDef]
    ) -> AioPageIterator[ListAggregatorsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListAggregatorsV2.html#SecurityHub.Paginator.ListAggregatorsV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listaggregatorsv2paginator)
        """


if TYPE_CHECKING:
    _ListConfigurationPoliciesPaginatorBase = AioPaginator[ListConfigurationPoliciesResponseTypeDef]
else:
    _ListConfigurationPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigurationPoliciesPaginator(_ListConfigurationPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicies.html#SecurityHub.Paginator.ListConfigurationPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfigurationPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicies.html#SecurityHub.Paginator.ListConfigurationPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListConfigurationPolicyAssociationsPaginatorBase = AioPaginator[
        ListConfigurationPolicyAssociationsResponseTypeDef
    ]
else:
    _ListConfigurationPolicyAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigurationPolicyAssociationsPaginator(
    _ListConfigurationPolicyAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicyAssociations.html#SecurityHub.Paginator.ListConfigurationPolicyAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpolicyassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationPolicyAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfigurationPolicyAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListConfigurationPolicyAssociations.html#SecurityHub.Paginator.ListConfigurationPolicyAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listconfigurationpolicyassociationspaginator)
        """


if TYPE_CHECKING:
    _ListEnabledProductsForImportPaginatorBase = AioPaginator[
        ListEnabledProductsForImportResponseTypeDef
    ]
else:
    _ListEnabledProductsForImportPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnabledProductsForImportPaginator(_ListEnabledProductsForImportPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListEnabledProductsForImport.html#SecurityHub.Paginator.ListEnabledProductsForImport)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listenabledproductsforimportpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnabledProductsForImportRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnabledProductsForImportResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListEnabledProductsForImport.html#SecurityHub.Paginator.ListEnabledProductsForImport.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listenabledproductsforimportpaginator)
        """


if TYPE_CHECKING:
    _ListFindingAggregatorsPaginatorBase = AioPaginator[ListFindingAggregatorsResponseTypeDef]
else:
    _ListFindingAggregatorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFindingAggregatorsPaginator(_ListFindingAggregatorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListFindingAggregators.html#SecurityHub.Paginator.ListFindingAggregators)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listfindingaggregatorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingAggregatorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFindingAggregatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListFindingAggregators.html#SecurityHub.Paginator.ListFindingAggregators.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listfindingaggregatorspaginator)
        """


if TYPE_CHECKING:
    _ListInvitationsPaginatorBase = AioPaginator[ListInvitationsResponseTypeDef]
else:
    _ListInvitationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInvitationsPaginator(_ListInvitationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListInvitations.html#SecurityHub.Paginator.ListInvitations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listinvitationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvitationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListInvitations.html#SecurityHub.Paginator.ListInvitations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listinvitationspaginator)
        """


if TYPE_CHECKING:
    _ListMembersPaginatorBase = AioPaginator[ListMembersResponseTypeDef]
else:
    _ListMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMembersPaginator(_ListMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListMembers.html#SecurityHub.Paginator.ListMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listmemberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListMembers.html#SecurityHub.Paginator.ListMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listmemberspaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationAdminAccountsPaginatorBase = AioPaginator[
        ListOrganizationAdminAccountsResponseTypeDef
    ]
else:
    _ListOrganizationAdminAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationAdminAccountsPaginator(_ListOrganizationAdminAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListOrganizationAdminAccounts.html#SecurityHub.Paginator.ListOrganizationAdminAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listorganizationadminaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListOrganizationAdminAccounts.html#SecurityHub.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listorganizationadminaccountspaginator)
        """


if TYPE_CHECKING:
    _ListSecurityControlDefinitionsPaginatorBase = AioPaginator[
        ListSecurityControlDefinitionsResponseTypeDef
    ]
else:
    _ListSecurityControlDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSecurityControlDefinitionsPaginator(_ListSecurityControlDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListSecurityControlDefinitions.html#SecurityHub.Paginator.ListSecurityControlDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityControlDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityControlDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListSecurityControlDefinitions.html#SecurityHub.Paginator.ListSecurityControlDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListStandardsControlAssociationsPaginatorBase = AioPaginator[
        ListStandardsControlAssociationsResponseTypeDef
    ]
else:
    _ListStandardsControlAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStandardsControlAssociationsPaginator(_ListStandardsControlAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListStandardsControlAssociations.html#SecurityHub.Paginator.ListStandardsControlAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#liststandardscontrolassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStandardsControlAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStandardsControlAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/paginator/ListStandardsControlAssociations.html#SecurityHub.Paginator.ListStandardsControlAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/paginators/#liststandardscontrolassociationspaginator)
        """
