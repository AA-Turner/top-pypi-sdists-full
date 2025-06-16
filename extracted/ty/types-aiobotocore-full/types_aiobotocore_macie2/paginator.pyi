"""
Type annotations for macie2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_macie2.client import Macie2Client
    from types_aiobotocore_macie2.paginator import (
        DescribeBucketsPaginator,
        GetUsageStatisticsPaginator,
        ListAllowListsPaginator,
        ListAutomatedDiscoveryAccountsPaginator,
        ListClassificationJobsPaginator,
        ListClassificationScopesPaginator,
        ListCustomDataIdentifiersPaginator,
        ListFindingsFiltersPaginator,
        ListFindingsPaginator,
        ListInvitationsPaginator,
        ListManagedDataIdentifiersPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        ListResourceProfileArtifactsPaginator,
        ListResourceProfileDetectionsPaginator,
        ListSensitivityInspectionTemplatesPaginator,
        SearchResourcesPaginator,
    )

    session = get_session()
    with session.create_client("macie2") as client:
        client: Macie2Client

        describe_buckets_paginator: DescribeBucketsPaginator = client.get_paginator("describe_buckets")
        get_usage_statistics_paginator: GetUsageStatisticsPaginator = client.get_paginator("get_usage_statistics")
        list_allow_lists_paginator: ListAllowListsPaginator = client.get_paginator("list_allow_lists")
        list_automated_discovery_accounts_paginator: ListAutomatedDiscoveryAccountsPaginator = client.get_paginator("list_automated_discovery_accounts")
        list_classification_jobs_paginator: ListClassificationJobsPaginator = client.get_paginator("list_classification_jobs")
        list_classification_scopes_paginator: ListClassificationScopesPaginator = client.get_paginator("list_classification_scopes")
        list_custom_data_identifiers_paginator: ListCustomDataIdentifiersPaginator = client.get_paginator("list_custom_data_identifiers")
        list_findings_filters_paginator: ListFindingsFiltersPaginator = client.get_paginator("list_findings_filters")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
        list_managed_data_identifiers_paginator: ListManagedDataIdentifiersPaginator = client.get_paginator("list_managed_data_identifiers")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
        list_resource_profile_artifacts_paginator: ListResourceProfileArtifactsPaginator = client.get_paginator("list_resource_profile_artifacts")
        list_resource_profile_detections_paginator: ListResourceProfileDetectionsPaginator = client.get_paginator("list_resource_profile_detections")
        list_sensitivity_inspection_templates_paginator: ListSensitivityInspectionTemplatesPaginator = client.get_paginator("list_sensitivity_inspection_templates")
        search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeBucketsRequestPaginateTypeDef,
    DescribeBucketsResponseTypeDef,
    GetUsageStatisticsRequestPaginateTypeDef,
    GetUsageStatisticsResponseTypeDef,
    ListAllowListsRequestPaginateTypeDef,
    ListAllowListsResponseTypeDef,
    ListAutomatedDiscoveryAccountsRequestPaginateTypeDef,
    ListAutomatedDiscoveryAccountsResponseTypeDef,
    ListClassificationJobsRequestPaginateTypeDef,
    ListClassificationJobsResponseTypeDef,
    ListClassificationScopesRequestPaginateTypeDef,
    ListClassificationScopesResponseTypeDef,
    ListCustomDataIdentifiersRequestPaginateTypeDef,
    ListCustomDataIdentifiersResponseTypeDef,
    ListFindingsFiltersRequestPaginateTypeDef,
    ListFindingsFiltersResponseTypeDef,
    ListFindingsRequestPaginateTypeDef,
    ListFindingsResponseTypeDef,
    ListInvitationsRequestPaginateTypeDef,
    ListInvitationsResponseTypeDef,
    ListManagedDataIdentifiersRequestPaginateTypeDef,
    ListManagedDataIdentifiersResponseTypeDef,
    ListMembersRequestPaginateTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestPaginateTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListResourceProfileArtifactsRequestPaginateTypeDef,
    ListResourceProfileArtifactsResponseTypeDef,
    ListResourceProfileDetectionsRequestPaginateTypeDef,
    ListResourceProfileDetectionsResponseTypeDef,
    ListSensitivityInspectionTemplatesRequestPaginateTypeDef,
    ListSensitivityInspectionTemplatesResponseTypeDef,
    SearchResourcesRequestPaginateTypeDef,
    SearchResourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeBucketsPaginator",
    "GetUsageStatisticsPaginator",
    "ListAllowListsPaginator",
    "ListAutomatedDiscoveryAccountsPaginator",
    "ListClassificationJobsPaginator",
    "ListClassificationScopesPaginator",
    "ListCustomDataIdentifiersPaginator",
    "ListFindingsFiltersPaginator",
    "ListFindingsPaginator",
    "ListInvitationsPaginator",
    "ListManagedDataIdentifiersPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "ListResourceProfileArtifactsPaginator",
    "ListResourceProfileDetectionsPaginator",
    "ListSensitivityInspectionTemplatesPaginator",
    "SearchResourcesPaginator",
)

if TYPE_CHECKING:
    _DescribeBucketsPaginatorBase = AioPaginator[DescribeBucketsResponseTypeDef]
else:
    _DescribeBucketsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeBucketsPaginator(_DescribeBucketsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/DescribeBuckets.html#Macie2.Paginator.DescribeBuckets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#describebucketspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBucketsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBucketsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/DescribeBuckets.html#Macie2.Paginator.DescribeBuckets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#describebucketspaginator)
        """

if TYPE_CHECKING:
    _GetUsageStatisticsPaginatorBase = AioPaginator[GetUsageStatisticsResponseTypeDef]
else:
    _GetUsageStatisticsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetUsageStatisticsPaginator(_GetUsageStatisticsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/GetUsageStatistics.html#Macie2.Paginator.GetUsageStatistics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#getusagestatisticspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetUsageStatisticsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetUsageStatisticsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/GetUsageStatistics.html#Macie2.Paginator.GetUsageStatistics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#getusagestatisticspaginator)
        """

if TYPE_CHECKING:
    _ListAllowListsPaginatorBase = AioPaginator[ListAllowListsResponseTypeDef]
else:
    _ListAllowListsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAllowListsPaginator(_ListAllowListsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAllowLists.html#Macie2.Paginator.ListAllowLists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listallowlistspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAllowListsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAllowListsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAllowLists.html#Macie2.Paginator.ListAllowLists.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listallowlistspaginator)
        """

if TYPE_CHECKING:
    _ListAutomatedDiscoveryAccountsPaginatorBase = AioPaginator[
        ListAutomatedDiscoveryAccountsResponseTypeDef
    ]
else:
    _ListAutomatedDiscoveryAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAutomatedDiscoveryAccountsPaginator(_ListAutomatedDiscoveryAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAutomatedDiscoveryAccounts.html#Macie2.Paginator.ListAutomatedDiscoveryAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listautomateddiscoveryaccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutomatedDiscoveryAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAutomatedDiscoveryAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListAutomatedDiscoveryAccounts.html#Macie2.Paginator.ListAutomatedDiscoveryAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listautomateddiscoveryaccountspaginator)
        """

if TYPE_CHECKING:
    _ListClassificationJobsPaginatorBase = AioPaginator[ListClassificationJobsResponseTypeDef]
else:
    _ListClassificationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClassificationJobsPaginator(_ListClassificationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationJobs.html#Macie2.Paginator.ListClassificationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClassificationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClassificationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationJobs.html#Macie2.Paginator.ListClassificationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationjobspaginator)
        """

if TYPE_CHECKING:
    _ListClassificationScopesPaginatorBase = AioPaginator[ListClassificationScopesResponseTypeDef]
else:
    _ListClassificationScopesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClassificationScopesPaginator(_ListClassificationScopesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationScopes.html#Macie2.Paginator.ListClassificationScopes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationscopespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClassificationScopesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClassificationScopesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListClassificationScopes.html#Macie2.Paginator.ListClassificationScopes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listclassificationscopespaginator)
        """

if TYPE_CHECKING:
    _ListCustomDataIdentifiersPaginatorBase = AioPaginator[ListCustomDataIdentifiersResponseTypeDef]
else:
    _ListCustomDataIdentifiersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCustomDataIdentifiersPaginator(_ListCustomDataIdentifiersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListCustomDataIdentifiers.html#Macie2.Paginator.ListCustomDataIdentifiers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listcustomdataidentifierspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomDataIdentifiersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomDataIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListCustomDataIdentifiers.html#Macie2.Paginator.ListCustomDataIdentifiers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listcustomdataidentifierspaginator)
        """

if TYPE_CHECKING:
    _ListFindingsFiltersPaginatorBase = AioPaginator[ListFindingsFiltersResponseTypeDef]
else:
    _ListFindingsFiltersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFindingsFiltersPaginator(_ListFindingsFiltersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindingsFilters.html#Macie2.Paginator.ListFindingsFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingsfilterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsFiltersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFindingsFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindingsFilters.html#Macie2.Paginator.ListFindingsFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingsfilterspaginator)
        """

if TYPE_CHECKING:
    _ListFindingsPaginatorBase = AioPaginator[ListFindingsResponseTypeDef]
else:
    _ListFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFindingsPaginator(_ListFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindings.html#Macie2.Paginator.ListFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListFindings.html#Macie2.Paginator.ListFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listfindingspaginator)
        """

if TYPE_CHECKING:
    _ListInvitationsPaginatorBase = AioPaginator[ListInvitationsResponseTypeDef]
else:
    _ListInvitationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInvitationsPaginator(_ListInvitationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListInvitations.html#Macie2.Paginator.ListInvitations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listinvitationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvitationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListInvitations.html#Macie2.Paginator.ListInvitations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listinvitationspaginator)
        """

if TYPE_CHECKING:
    _ListManagedDataIdentifiersPaginatorBase = AioPaginator[
        ListManagedDataIdentifiersResponseTypeDef
    ]
else:
    _ListManagedDataIdentifiersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedDataIdentifiersPaginator(_ListManagedDataIdentifiersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListManagedDataIdentifiers.html#Macie2.Paginator.ListManagedDataIdentifiers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmanageddataidentifierspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedDataIdentifiersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedDataIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListManagedDataIdentifiers.html#Macie2.Paginator.ListManagedDataIdentifiers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmanageddataidentifierspaginator)
        """

if TYPE_CHECKING:
    _ListMembersPaginatorBase = AioPaginator[ListMembersResponseTypeDef]
else:
    _ListMembersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMembersPaginator(_ListMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListMembers.html#Macie2.Paginator.ListMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmemberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListMembers.html#Macie2.Paginator.ListMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listmemberspaginator)
        """

if TYPE_CHECKING:
    _ListOrganizationAdminAccountsPaginatorBase = AioPaginator[
        ListOrganizationAdminAccountsResponseTypeDef
    ]
else:
    _ListOrganizationAdminAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOrganizationAdminAccountsPaginator(_ListOrganizationAdminAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListOrganizationAdminAccounts.html#Macie2.Paginator.ListOrganizationAdminAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listorganizationadminaccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListOrganizationAdminAccounts.html#Macie2.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listorganizationadminaccountspaginator)
        """

if TYPE_CHECKING:
    _ListResourceProfileArtifactsPaginatorBase = AioPaginator[
        ListResourceProfileArtifactsResponseTypeDef
    ]
else:
    _ListResourceProfileArtifactsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceProfileArtifactsPaginator(_ListResourceProfileArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileArtifacts.html#Macie2.Paginator.ListResourceProfileArtifacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofileartifactspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceProfileArtifactsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceProfileArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileArtifacts.html#Macie2.Paginator.ListResourceProfileArtifacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofileartifactspaginator)
        """

if TYPE_CHECKING:
    _ListResourceProfileDetectionsPaginatorBase = AioPaginator[
        ListResourceProfileDetectionsResponseTypeDef
    ]
else:
    _ListResourceProfileDetectionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceProfileDetectionsPaginator(_ListResourceProfileDetectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileDetections.html#Macie2.Paginator.ListResourceProfileDetections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofiledetectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceProfileDetectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceProfileDetectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListResourceProfileDetections.html#Macie2.Paginator.ListResourceProfileDetections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listresourceprofiledetectionspaginator)
        """

if TYPE_CHECKING:
    _ListSensitivityInspectionTemplatesPaginatorBase = AioPaginator[
        ListSensitivityInspectionTemplatesResponseTypeDef
    ]
else:
    _ListSensitivityInspectionTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSensitivityInspectionTemplatesPaginator(_ListSensitivityInspectionTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListSensitivityInspectionTemplates.html#Macie2.Paginator.ListSensitivityInspectionTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listsensitivityinspectiontemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSensitivityInspectionTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSensitivityInspectionTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/ListSensitivityInspectionTemplates.html#Macie2.Paginator.ListSensitivityInspectionTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#listsensitivityinspectiontemplatespaginator)
        """

if TYPE_CHECKING:
    _SearchResourcesPaginatorBase = AioPaginator[SearchResourcesResponseTypeDef]
else:
    _SearchResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchResourcesPaginator(_SearchResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/SearchResources.html#Macie2.Paginator.SearchResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#searchresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/paginator/SearchResources.html#Macie2.Paginator.SearchResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/paginators/#searchresourcespaginator)
        """
