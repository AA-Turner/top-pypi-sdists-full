"""
Type annotations for network-firewall service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_network_firewall.client import NetworkFirewallClient
    from types_aiobotocore_network_firewall.paginator import (
        GetAnalysisReportResultsPaginator,
        ListAnalysisReportsPaginator,
        ListFirewallPoliciesPaginator,
        ListFirewallsPaginator,
        ListFlowOperationResultsPaginator,
        ListFlowOperationsPaginator,
        ListRuleGroupsPaginator,
        ListTLSInspectionConfigurationsPaginator,
        ListTagsForResourcePaginator,
        ListVpcEndpointAssociationsPaginator,
    )

    session = get_session()
    with session.create_client("network-firewall") as client:
        client: NetworkFirewallClient

        get_analysis_report_results_paginator: GetAnalysisReportResultsPaginator = client.get_paginator("get_analysis_report_results")
        list_analysis_reports_paginator: ListAnalysisReportsPaginator = client.get_paginator("list_analysis_reports")
        list_firewall_policies_paginator: ListFirewallPoliciesPaginator = client.get_paginator("list_firewall_policies")
        list_firewalls_paginator: ListFirewallsPaginator = client.get_paginator("list_firewalls")
        list_flow_operation_results_paginator: ListFlowOperationResultsPaginator = client.get_paginator("list_flow_operation_results")
        list_flow_operations_paginator: ListFlowOperationsPaginator = client.get_paginator("list_flow_operations")
        list_rule_groups_paginator: ListRuleGroupsPaginator = client.get_paginator("list_rule_groups")
        list_tls_inspection_configurations_paginator: ListTLSInspectionConfigurationsPaginator = client.get_paginator("list_tls_inspection_configurations")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_vpc_endpoint_associations_paginator: ListVpcEndpointAssociationsPaginator = client.get_paginator("list_vpc_endpoint_associations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetAnalysisReportResultsRequestPaginateTypeDef,
    GetAnalysisReportResultsResponseTypeDef,
    ListAnalysisReportsRequestPaginateTypeDef,
    ListAnalysisReportsResponseTypeDef,
    ListFirewallPoliciesRequestPaginateTypeDef,
    ListFirewallPoliciesResponseTypeDef,
    ListFirewallsRequestPaginateTypeDef,
    ListFirewallsResponseTypeDef,
    ListFlowOperationResultsRequestPaginateTypeDef,
    ListFlowOperationResultsResponseTypeDef,
    ListFlowOperationsRequestPaginateTypeDef,
    ListFlowOperationsResponseTypeDef,
    ListRuleGroupsRequestPaginateTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTLSInspectionConfigurationsRequestPaginateTypeDef,
    ListTLSInspectionConfigurationsResponseTypeDef,
    ListVpcEndpointAssociationsRequestPaginateTypeDef,
    ListVpcEndpointAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetAnalysisReportResultsPaginator",
    "ListAnalysisReportsPaginator",
    "ListFirewallPoliciesPaginator",
    "ListFirewallsPaginator",
    "ListFlowOperationResultsPaginator",
    "ListFlowOperationsPaginator",
    "ListRuleGroupsPaginator",
    "ListTLSInspectionConfigurationsPaginator",
    "ListTagsForResourcePaginator",
    "ListVpcEndpointAssociationsPaginator",
)


if TYPE_CHECKING:
    _GetAnalysisReportResultsPaginatorBase = AioPaginator[GetAnalysisReportResultsResponseTypeDef]
else:
    _GetAnalysisReportResultsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetAnalysisReportResultsPaginator(_GetAnalysisReportResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/GetAnalysisReportResults.html#NetworkFirewall.Paginator.GetAnalysisReportResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#getanalysisreportresultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAnalysisReportResultsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAnalysisReportResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/GetAnalysisReportResults.html#NetworkFirewall.Paginator.GetAnalysisReportResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#getanalysisreportresultspaginator)
        """


if TYPE_CHECKING:
    _ListAnalysisReportsPaginatorBase = AioPaginator[ListAnalysisReportsResponseTypeDef]
else:
    _ListAnalysisReportsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAnalysisReportsPaginator(_ListAnalysisReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListAnalysisReports.html#NetworkFirewall.Paginator.ListAnalysisReports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listanalysisreportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAnalysisReportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAnalysisReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListAnalysisReports.html#NetworkFirewall.Paginator.ListAnalysisReports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listanalysisreportspaginator)
        """


if TYPE_CHECKING:
    _ListFirewallPoliciesPaginatorBase = AioPaginator[ListFirewallPoliciesResponseTypeDef]
else:
    _ListFirewallPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFirewallPoliciesPaginator(_ListFirewallPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFirewallPolicies.html#NetworkFirewall.Paginator.ListFirewallPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listfirewallpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFirewallPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFirewallPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFirewallPolicies.html#NetworkFirewall.Paginator.ListFirewallPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listfirewallpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListFirewallsPaginatorBase = AioPaginator[ListFirewallsResponseTypeDef]
else:
    _ListFirewallsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFirewallsPaginator(_ListFirewallsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFirewalls.html#NetworkFirewall.Paginator.ListFirewalls)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listfirewallspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFirewallsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFirewallsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFirewalls.html#NetworkFirewall.Paginator.ListFirewalls.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listfirewallspaginator)
        """


if TYPE_CHECKING:
    _ListFlowOperationResultsPaginatorBase = AioPaginator[ListFlowOperationResultsResponseTypeDef]
else:
    _ListFlowOperationResultsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFlowOperationResultsPaginator(_ListFlowOperationResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFlowOperationResults.html#NetworkFirewall.Paginator.ListFlowOperationResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listflowoperationresultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowOperationResultsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowOperationResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFlowOperationResults.html#NetworkFirewall.Paginator.ListFlowOperationResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listflowoperationresultspaginator)
        """


if TYPE_CHECKING:
    _ListFlowOperationsPaginatorBase = AioPaginator[ListFlowOperationsResponseTypeDef]
else:
    _ListFlowOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFlowOperationsPaginator(_ListFlowOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFlowOperations.html#NetworkFirewall.Paginator.ListFlowOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listflowoperationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowOperationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListFlowOperations.html#NetworkFirewall.Paginator.ListFlowOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listflowoperationspaginator)
        """


if TYPE_CHECKING:
    _ListRuleGroupsPaginatorBase = AioPaginator[ListRuleGroupsResponseTypeDef]
else:
    _ListRuleGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRuleGroupsPaginator(_ListRuleGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListRuleGroups.html#NetworkFirewall.Paginator.ListRuleGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listrulegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListRuleGroups.html#NetworkFirewall.Paginator.ListRuleGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listrulegroupspaginator)
        """


if TYPE_CHECKING:
    _ListTLSInspectionConfigurationsPaginatorBase = AioPaginator[
        ListTLSInspectionConfigurationsResponseTypeDef
    ]
else:
    _ListTLSInspectionConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTLSInspectionConfigurationsPaginator(_ListTLSInspectionConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListTLSInspectionConfigurations.html#NetworkFirewall.Paginator.ListTLSInspectionConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listtlsinspectionconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTLSInspectionConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTLSInspectionConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListTLSInspectionConfigurations.html#NetworkFirewall.Paginator.ListTLSInspectionConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listtlsinspectionconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListTagsForResource.html#NetworkFirewall.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListTagsForResource.html#NetworkFirewall.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListVpcEndpointAssociationsPaginatorBase = AioPaginator[
        ListVpcEndpointAssociationsResponseTypeDef
    ]
else:
    _ListVpcEndpointAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListVpcEndpointAssociationsPaginator(_ListVpcEndpointAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListVpcEndpointAssociations.html#NetworkFirewall.Paginator.ListVpcEndpointAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listvpcendpointassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVpcEndpointAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVpcEndpointAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/paginator/ListVpcEndpointAssociations.html#NetworkFirewall.Paginator.ListVpcEndpointAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/paginators/#listvpcendpointassociationspaginator)
        """
