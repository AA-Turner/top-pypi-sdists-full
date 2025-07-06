"""
Type annotations for inspector2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_inspector2.client import Inspector2Client
    from types_aiobotocore_inspector2.paginator import (
        GetCisScanResultDetailsPaginator,
        GetClustersForImagePaginator,
        ListAccountPermissionsPaginator,
        ListCisScanConfigurationsPaginator,
        ListCisScanResultsAggregatedByChecksPaginator,
        ListCisScanResultsAggregatedByTargetResourcePaginator,
        ListCisScansPaginator,
        ListCoveragePaginator,
        ListCoverageStatisticsPaginator,
        ListDelegatedAdminAccountsPaginator,
        ListFiltersPaginator,
        ListFindingAggregationsPaginator,
        ListFindingsPaginator,
        ListMembersPaginator,
        ListUsageTotalsPaginator,
        SearchVulnerabilitiesPaginator,
    )

    session = get_session()
    with session.create_client("inspector2") as client:
        client: Inspector2Client

        get_cis_scan_result_details_paginator: GetCisScanResultDetailsPaginator = client.get_paginator("get_cis_scan_result_details")
        get_clusters_for_image_paginator: GetClustersForImagePaginator = client.get_paginator("get_clusters_for_image")
        list_account_permissions_paginator: ListAccountPermissionsPaginator = client.get_paginator("list_account_permissions")
        list_cis_scan_configurations_paginator: ListCisScanConfigurationsPaginator = client.get_paginator("list_cis_scan_configurations")
        list_cis_scan_results_aggregated_by_checks_paginator: ListCisScanResultsAggregatedByChecksPaginator = client.get_paginator("list_cis_scan_results_aggregated_by_checks")
        list_cis_scan_results_aggregated_by_target_resource_paginator: ListCisScanResultsAggregatedByTargetResourcePaginator = client.get_paginator("list_cis_scan_results_aggregated_by_target_resource")
        list_cis_scans_paginator: ListCisScansPaginator = client.get_paginator("list_cis_scans")
        list_coverage_paginator: ListCoveragePaginator = client.get_paginator("list_coverage")
        list_coverage_statistics_paginator: ListCoverageStatisticsPaginator = client.get_paginator("list_coverage_statistics")
        list_delegated_admin_accounts_paginator: ListDelegatedAdminAccountsPaginator = client.get_paginator("list_delegated_admin_accounts")
        list_filters_paginator: ListFiltersPaginator = client.get_paginator("list_filters")
        list_finding_aggregations_paginator: ListFindingAggregationsPaginator = client.get_paginator("list_finding_aggregations")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_usage_totals_paginator: ListUsageTotalsPaginator = client.get_paginator("list_usage_totals")
        search_vulnerabilities_paginator: SearchVulnerabilitiesPaginator = client.get_paginator("search_vulnerabilities")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetCisScanResultDetailsRequestPaginateTypeDef,
    GetCisScanResultDetailsResponseTypeDef,
    GetClustersForImageRequestPaginateTypeDef,
    GetClustersForImageResponseTypeDef,
    ListAccountPermissionsRequestPaginateTypeDef,
    ListAccountPermissionsResponseTypeDef,
    ListCisScanConfigurationsRequestPaginateTypeDef,
    ListCisScanConfigurationsResponseTypeDef,
    ListCisScanResultsAggregatedByChecksRequestPaginateTypeDef,
    ListCisScanResultsAggregatedByChecksResponseTypeDef,
    ListCisScanResultsAggregatedByTargetResourceRequestPaginateTypeDef,
    ListCisScanResultsAggregatedByTargetResourceResponseTypeDef,
    ListCisScansRequestPaginateTypeDef,
    ListCisScansResponseTypeDef,
    ListCoverageRequestPaginateTypeDef,
    ListCoverageResponseTypeDef,
    ListCoverageStatisticsRequestPaginateTypeDef,
    ListCoverageStatisticsResponseTypeDef,
    ListDelegatedAdminAccountsRequestPaginateTypeDef,
    ListDelegatedAdminAccountsResponseTypeDef,
    ListFiltersRequestPaginateTypeDef,
    ListFiltersResponseTypeDef,
    ListFindingAggregationsRequestPaginateTypeDef,
    ListFindingAggregationsResponseTypeDef,
    ListFindingsRequestPaginateTypeDef,
    ListFindingsResponseTypeDef,
    ListMembersRequestPaginateTypeDef,
    ListMembersResponseTypeDef,
    ListUsageTotalsRequestPaginateTypeDef,
    ListUsageTotalsResponseTypeDef,
    SearchVulnerabilitiesRequestPaginateTypeDef,
    SearchVulnerabilitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetCisScanResultDetailsPaginator",
    "GetClustersForImagePaginator",
    "ListAccountPermissionsPaginator",
    "ListCisScanConfigurationsPaginator",
    "ListCisScanResultsAggregatedByChecksPaginator",
    "ListCisScanResultsAggregatedByTargetResourcePaginator",
    "ListCisScansPaginator",
    "ListCoveragePaginator",
    "ListCoverageStatisticsPaginator",
    "ListDelegatedAdminAccountsPaginator",
    "ListFiltersPaginator",
    "ListFindingAggregationsPaginator",
    "ListFindingsPaginator",
    "ListMembersPaginator",
    "ListUsageTotalsPaginator",
    "SearchVulnerabilitiesPaginator",
)


if TYPE_CHECKING:
    _GetCisScanResultDetailsPaginatorBase = AioPaginator[GetCisScanResultDetailsResponseTypeDef]
else:
    _GetCisScanResultDetailsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetCisScanResultDetailsPaginator(_GetCisScanResultDetailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/GetCisScanResultDetails.html#Inspector2.Paginator.GetCisScanResultDetails)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#getcisscanresultdetailspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCisScanResultDetailsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetCisScanResultDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/GetCisScanResultDetails.html#Inspector2.Paginator.GetCisScanResultDetails.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#getcisscanresultdetailspaginator)
        """


if TYPE_CHECKING:
    _GetClustersForImagePaginatorBase = AioPaginator[GetClustersForImageResponseTypeDef]
else:
    _GetClustersForImagePaginatorBase = AioPaginator  # type: ignore[assignment]


class GetClustersForImagePaginator(_GetClustersForImagePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/GetClustersForImage.html#Inspector2.Paginator.GetClustersForImage)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#getclustersforimagepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetClustersForImageRequestPaginateTypeDef]
    ) -> AioPageIterator[GetClustersForImageResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/GetClustersForImage.html#Inspector2.Paginator.GetClustersForImage.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#getclustersforimagepaginator)
        """


if TYPE_CHECKING:
    _ListAccountPermissionsPaginatorBase = AioPaginator[ListAccountPermissionsResponseTypeDef]
else:
    _ListAccountPermissionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccountPermissionsPaginator(_ListAccountPermissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListAccountPermissions.html#Inspector2.Paginator.ListAccountPermissions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listaccountpermissionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountPermissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListAccountPermissions.html#Inspector2.Paginator.ListAccountPermissions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listaccountpermissionspaginator)
        """


if TYPE_CHECKING:
    _ListCisScanConfigurationsPaginatorBase = AioPaginator[ListCisScanConfigurationsResponseTypeDef]
else:
    _ListCisScanConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCisScanConfigurationsPaginator(_ListCisScanConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanConfigurations.html#Inspector2.Paginator.ListCisScanConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCisScanConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCisScanConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanConfigurations.html#Inspector2.Paginator.ListCisScanConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListCisScanResultsAggregatedByChecksPaginatorBase = AioPaginator[
        ListCisScanResultsAggregatedByChecksResponseTypeDef
    ]
else:
    _ListCisScanResultsAggregatedByChecksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCisScanResultsAggregatedByChecksPaginator(
    _ListCisScanResultsAggregatedByChecksPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByChecks.html#Inspector2.Paginator.ListCisScanResultsAggregatedByChecks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbycheckspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCisScanResultsAggregatedByChecksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCisScanResultsAggregatedByChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByChecks.html#Inspector2.Paginator.ListCisScanResultsAggregatedByChecks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbycheckspaginator)
        """


if TYPE_CHECKING:
    _ListCisScanResultsAggregatedByTargetResourcePaginatorBase = AioPaginator[
        ListCisScanResultsAggregatedByTargetResourceResponseTypeDef
    ]
else:
    _ListCisScanResultsAggregatedByTargetResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCisScanResultsAggregatedByTargetResourcePaginator(
    _ListCisScanResultsAggregatedByTargetResourcePaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByTargetResource.html#Inspector2.Paginator.ListCisScanResultsAggregatedByTargetResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbytargetresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCisScanResultsAggregatedByTargetResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCisScanResultsAggregatedByTargetResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScanResultsAggregatedByTargetResource.html#Inspector2.Paginator.ListCisScanResultsAggregatedByTargetResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanresultsaggregatedbytargetresourcepaginator)
        """


if TYPE_CHECKING:
    _ListCisScansPaginatorBase = AioPaginator[ListCisScansResponseTypeDef]
else:
    _ListCisScansPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCisScansPaginator(_ListCisScansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScans.html#Inspector2.Paginator.ListCisScans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCisScansRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCisScansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCisScans.html#Inspector2.Paginator.ListCisScans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcisscanspaginator)
        """


if TYPE_CHECKING:
    _ListCoveragePaginatorBase = AioPaginator[ListCoverageResponseTypeDef]
else:
    _ListCoveragePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCoveragePaginator(_ListCoveragePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverage.html#Inspector2.Paginator.ListCoverage)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCoverageRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCoverageResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverage.html#Inspector2.Paginator.ListCoverage.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragepaginator)
        """


if TYPE_CHECKING:
    _ListCoverageStatisticsPaginatorBase = AioPaginator[ListCoverageStatisticsResponseTypeDef]
else:
    _ListCoverageStatisticsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCoverageStatisticsPaginator(_ListCoverageStatisticsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverageStatistics.html#Inspector2.Paginator.ListCoverageStatistics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragestatisticspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCoverageStatisticsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCoverageStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListCoverageStatistics.html#Inspector2.Paginator.ListCoverageStatistics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listcoveragestatisticspaginator)
        """


if TYPE_CHECKING:
    _ListDelegatedAdminAccountsPaginatorBase = AioPaginator[
        ListDelegatedAdminAccountsResponseTypeDef
    ]
else:
    _ListDelegatedAdminAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDelegatedAdminAccountsPaginator(_ListDelegatedAdminAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListDelegatedAdminAccounts.html#Inspector2.Paginator.ListDelegatedAdminAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listdelegatedadminaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDelegatedAdminAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDelegatedAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListDelegatedAdminAccounts.html#Inspector2.Paginator.ListDelegatedAdminAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listdelegatedadminaccountspaginator)
        """


if TYPE_CHECKING:
    _ListFiltersPaginatorBase = AioPaginator[ListFiltersResponseTypeDef]
else:
    _ListFiltersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFiltersPaginator(_ListFiltersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFilters.html#Inspector2.Paginator.ListFilters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfilterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFiltersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFilters.html#Inspector2.Paginator.ListFilters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfilterspaginator)
        """


if TYPE_CHECKING:
    _ListFindingAggregationsPaginatorBase = AioPaginator[ListFindingAggregationsResponseTypeDef]
else:
    _ListFindingAggregationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFindingAggregationsPaginator(_ListFindingAggregationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindingAggregations.html#Inspector2.Paginator.ListFindingAggregations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingaggregationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingAggregationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFindingAggregationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindingAggregations.html#Inspector2.Paginator.ListFindingAggregations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingaggregationspaginator)
        """


if TYPE_CHECKING:
    _ListFindingsPaginatorBase = AioPaginator[ListFindingsResponseTypeDef]
else:
    _ListFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFindingsPaginator(_ListFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindings.html#Inspector2.Paginator.ListFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListFindings.html#Inspector2.Paginator.ListFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listfindingspaginator)
        """


if TYPE_CHECKING:
    _ListMembersPaginatorBase = AioPaginator[ListMembersResponseTypeDef]
else:
    _ListMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMembersPaginator(_ListMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListMembers.html#Inspector2.Paginator.ListMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listmemberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListMembers.html#Inspector2.Paginator.ListMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listmemberspaginator)
        """


if TYPE_CHECKING:
    _ListUsageTotalsPaginatorBase = AioPaginator[ListUsageTotalsResponseTypeDef]
else:
    _ListUsageTotalsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsageTotalsPaginator(_ListUsageTotalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListUsageTotals.html#Inspector2.Paginator.ListUsageTotals)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listusagetotalspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsageTotalsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsageTotalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/ListUsageTotals.html#Inspector2.Paginator.ListUsageTotals.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#listusagetotalspaginator)
        """


if TYPE_CHECKING:
    _SearchVulnerabilitiesPaginatorBase = AioPaginator[SearchVulnerabilitiesResponseTypeDef]
else:
    _SearchVulnerabilitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchVulnerabilitiesPaginator(_SearchVulnerabilitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/SearchVulnerabilities.html#Inspector2.Paginator.SearchVulnerabilities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#searchvulnerabilitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchVulnerabilitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchVulnerabilitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/paginator/SearchVulnerabilities.html#Inspector2.Paginator.SearchVulnerabilities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector2/paginators/#searchvulnerabilitiespaginator)
        """
