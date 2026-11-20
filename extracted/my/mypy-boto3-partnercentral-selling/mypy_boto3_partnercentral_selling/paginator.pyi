"""
Type annotations for partnercentral-selling service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_partnercentral_selling.client import PartnerCentralSellingAPIClient
    from mypy_boto3_partnercentral_selling.paginator import (
        ListCustomerAccountBulkJobResultsPaginator,
        ListCustomerAccountBulkJobsPaginator,
        ListEngagementByAcceptingInvitationTasksPaginator,
        ListEngagementFromOpportunityTasksPaginator,
        ListEngagementGroupsPaginator,
        ListEngagementInvitationsPaginator,
        ListEngagementMembersPaginator,
        ListEngagementResourceAssociationsPaginator,
        ListEngagementsPaginator,
        ListOpportunitiesPaginator,
        ListOpportunityBulkJobResultsPaginator,
        ListOpportunityBulkJobsPaginator,
        ListOpportunityFromEngagementTasksPaginator,
        ListProspectingFromEngagementTasksPaginator,
        ListResourceSnapshotJobsPaginator,
        ListResourceSnapshotsPaginator,
        ListSolutionsPaginator,
        SearchCustomerAccountsPaginator,
        SearchEngagementsPaginator,
        SearchOpportunitiesPaginator,
    )

    session = Session()
    client: PartnerCentralSellingAPIClient = session.client("partnercentral-selling")

    list_customer_account_bulk_job_results_paginator: ListCustomerAccountBulkJobResultsPaginator = client.get_paginator("list_customer_account_bulk_job_results")
    list_customer_account_bulk_jobs_paginator: ListCustomerAccountBulkJobsPaginator = client.get_paginator("list_customer_account_bulk_jobs")
    list_engagement_by_accepting_invitation_tasks_paginator: ListEngagementByAcceptingInvitationTasksPaginator = client.get_paginator("list_engagement_by_accepting_invitation_tasks")
    list_engagement_from_opportunity_tasks_paginator: ListEngagementFromOpportunityTasksPaginator = client.get_paginator("list_engagement_from_opportunity_tasks")
    list_engagement_groups_paginator: ListEngagementGroupsPaginator = client.get_paginator("list_engagement_groups")
    list_engagement_invitations_paginator: ListEngagementInvitationsPaginator = client.get_paginator("list_engagement_invitations")
    list_engagement_members_paginator: ListEngagementMembersPaginator = client.get_paginator("list_engagement_members")
    list_engagement_resource_associations_paginator: ListEngagementResourceAssociationsPaginator = client.get_paginator("list_engagement_resource_associations")
    list_engagements_paginator: ListEngagementsPaginator = client.get_paginator("list_engagements")
    list_opportunities_paginator: ListOpportunitiesPaginator = client.get_paginator("list_opportunities")
    list_opportunity_bulk_job_results_paginator: ListOpportunityBulkJobResultsPaginator = client.get_paginator("list_opportunity_bulk_job_results")
    list_opportunity_bulk_jobs_paginator: ListOpportunityBulkJobsPaginator = client.get_paginator("list_opportunity_bulk_jobs")
    list_opportunity_from_engagement_tasks_paginator: ListOpportunityFromEngagementTasksPaginator = client.get_paginator("list_opportunity_from_engagement_tasks")
    list_prospecting_from_engagement_tasks_paginator: ListProspectingFromEngagementTasksPaginator = client.get_paginator("list_prospecting_from_engagement_tasks")
    list_resource_snapshot_jobs_paginator: ListResourceSnapshotJobsPaginator = client.get_paginator("list_resource_snapshot_jobs")
    list_resource_snapshots_paginator: ListResourceSnapshotsPaginator = client.get_paginator("list_resource_snapshots")
    list_solutions_paginator: ListSolutionsPaginator = client.get_paginator("list_solutions")
    search_customer_accounts_paginator: SearchCustomerAccountsPaginator = client.get_paginator("search_customer_accounts")
    search_engagements_paginator: SearchEngagementsPaginator = client.get_paginator("search_engagements")
    search_opportunities_paginator: SearchOpportunitiesPaginator = client.get_paginator("search_opportunities")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCustomerAccountBulkJobResultsRequestPaginateTypeDef,
    ListCustomerAccountBulkJobResultsResponseTypeDef,
    ListCustomerAccountBulkJobsRequestPaginateTypeDef,
    ListCustomerAccountBulkJobsResponseTypeDef,
    ListEngagementByAcceptingInvitationTasksRequestPaginateTypeDef,
    ListEngagementByAcceptingInvitationTasksResponseTypeDef,
    ListEngagementFromOpportunityTasksRequestPaginateTypeDef,
    ListEngagementFromOpportunityTasksResponseTypeDef,
    ListEngagementGroupsRequestPaginateTypeDef,
    ListEngagementGroupsResponseTypeDef,
    ListEngagementInvitationsRequestPaginateTypeDef,
    ListEngagementInvitationsResponseTypeDef,
    ListEngagementMembersRequestPaginateTypeDef,
    ListEngagementMembersResponseTypeDef,
    ListEngagementResourceAssociationsRequestPaginateTypeDef,
    ListEngagementResourceAssociationsResponseTypeDef,
    ListEngagementsRequestPaginateTypeDef,
    ListEngagementsResponseTypeDef,
    ListOpportunitiesRequestPaginateTypeDef,
    ListOpportunitiesResponseTypeDef,
    ListOpportunityBulkJobResultsRequestPaginateTypeDef,
    ListOpportunityBulkJobResultsResponseTypeDef,
    ListOpportunityBulkJobsRequestPaginateTypeDef,
    ListOpportunityBulkJobsResponseTypeDef,
    ListOpportunityFromEngagementTasksRequestPaginateTypeDef,
    ListOpportunityFromEngagementTasksResponseTypeDef,
    ListProspectingFromEngagementTasksRequestPaginateTypeDef,
    ListProspectingFromEngagementTasksResponseTypeDef,
    ListResourceSnapshotJobsRequestPaginateTypeDef,
    ListResourceSnapshotJobsResponseTypeDef,
    ListResourceSnapshotsRequestPaginateTypeDef,
    ListResourceSnapshotsResponseTypeDef,
    ListSolutionsRequestPaginateTypeDef,
    ListSolutionsResponseTypeDef,
    SearchCustomerAccountsRequestPaginateTypeDef,
    SearchCustomerAccountsResponseTypeDef,
    SearchEngagementsRequestPaginateTypeDef,
    SearchEngagementsResponseTypeDef,
    SearchOpportunitiesRequestPaginateTypeDef,
    SearchOpportunitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCustomerAccountBulkJobResultsPaginator",
    "ListCustomerAccountBulkJobsPaginator",
    "ListEngagementByAcceptingInvitationTasksPaginator",
    "ListEngagementFromOpportunityTasksPaginator",
    "ListEngagementGroupsPaginator",
    "ListEngagementInvitationsPaginator",
    "ListEngagementMembersPaginator",
    "ListEngagementResourceAssociationsPaginator",
    "ListEngagementsPaginator",
    "ListOpportunitiesPaginator",
    "ListOpportunityBulkJobResultsPaginator",
    "ListOpportunityBulkJobsPaginator",
    "ListOpportunityFromEngagementTasksPaginator",
    "ListProspectingFromEngagementTasksPaginator",
    "ListResourceSnapshotJobsPaginator",
    "ListResourceSnapshotsPaginator",
    "ListSolutionsPaginator",
    "SearchCustomerAccountsPaginator",
    "SearchEngagementsPaginator",
    "SearchOpportunitiesPaginator",
)

if TYPE_CHECKING:
    _ListCustomerAccountBulkJobResultsPaginatorBase = Paginator[
        ListCustomerAccountBulkJobResultsResponseTypeDef
    ]
else:
    _ListCustomerAccountBulkJobResultsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCustomerAccountBulkJobResultsPaginator(_ListCustomerAccountBulkJobResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListCustomerAccountBulkJobResults.html#PartnerCentralSellingAPI.Paginator.ListCustomerAccountBulkJobResults)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listcustomeraccountbulkjobresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomerAccountBulkJobResultsRequestPaginateTypeDef]
    ) -> PageIterator[ListCustomerAccountBulkJobResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListCustomerAccountBulkJobResults.html#PartnerCentralSellingAPI.Paginator.ListCustomerAccountBulkJobResults.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listcustomeraccountbulkjobresultspaginator)
        """

if TYPE_CHECKING:
    _ListCustomerAccountBulkJobsPaginatorBase = Paginator[
        ListCustomerAccountBulkJobsResponseTypeDef
    ]
else:
    _ListCustomerAccountBulkJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCustomerAccountBulkJobsPaginator(_ListCustomerAccountBulkJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListCustomerAccountBulkJobs.html#PartnerCentralSellingAPI.Paginator.ListCustomerAccountBulkJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listcustomeraccountbulkjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomerAccountBulkJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListCustomerAccountBulkJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListCustomerAccountBulkJobs.html#PartnerCentralSellingAPI.Paginator.ListCustomerAccountBulkJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listcustomeraccountbulkjobspaginator)
        """

if TYPE_CHECKING:
    _ListEngagementByAcceptingInvitationTasksPaginatorBase = Paginator[
        ListEngagementByAcceptingInvitationTasksResponseTypeDef
    ]
else:
    _ListEngagementByAcceptingInvitationTasksPaginatorBase = Paginator  # type: ignore[assignment]

class ListEngagementByAcceptingInvitationTasksPaginator(
    _ListEngagementByAcceptingInvitationTasksPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementByAcceptingInvitationTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementByAcceptingInvitationTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementbyacceptinginvitationtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngagementByAcceptingInvitationTasksRequestPaginateTypeDef]
    ) -> PageIterator[ListEngagementByAcceptingInvitationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementByAcceptingInvitationTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementByAcceptingInvitationTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementbyacceptinginvitationtaskspaginator)
        """

if TYPE_CHECKING:
    _ListEngagementFromOpportunityTasksPaginatorBase = Paginator[
        ListEngagementFromOpportunityTasksResponseTypeDef
    ]
else:
    _ListEngagementFromOpportunityTasksPaginatorBase = Paginator  # type: ignore[assignment]

class ListEngagementFromOpportunityTasksPaginator(_ListEngagementFromOpportunityTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementFromOpportunityTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementFromOpportunityTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementfromopportunitytaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngagementFromOpportunityTasksRequestPaginateTypeDef]
    ) -> PageIterator[ListEngagementFromOpportunityTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementFromOpportunityTasks.html#PartnerCentralSellingAPI.Paginator.ListEngagementFromOpportunityTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementfromopportunitytaskspaginator)
        """

if TYPE_CHECKING:
    _ListEngagementGroupsPaginatorBase = Paginator[ListEngagementGroupsResponseTypeDef]
else:
    _ListEngagementGroupsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEngagementGroupsPaginator(_ListEngagementGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementGroups.html#PartnerCentralSellingAPI.Paginator.ListEngagementGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngagementGroupsRequestPaginateTypeDef]
    ) -> PageIterator[ListEngagementGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementGroups.html#PartnerCentralSellingAPI.Paginator.ListEngagementGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementgroupspaginator)
        """

if TYPE_CHECKING:
    _ListEngagementInvitationsPaginatorBase = Paginator[ListEngagementInvitationsResponseTypeDef]
else:
    _ListEngagementInvitationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEngagementInvitationsPaginator(_ListEngagementInvitationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementInvitations.html#PartnerCentralSellingAPI.Paginator.ListEngagementInvitations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementinvitationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngagementInvitationsRequestPaginateTypeDef]
    ) -> PageIterator[ListEngagementInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementInvitations.html#PartnerCentralSellingAPI.Paginator.ListEngagementInvitations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementinvitationspaginator)
        """

if TYPE_CHECKING:
    _ListEngagementMembersPaginatorBase = Paginator[ListEngagementMembersResponseTypeDef]
else:
    _ListEngagementMembersPaginatorBase = Paginator  # type: ignore[assignment]

class ListEngagementMembersPaginator(_ListEngagementMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementMembers.html#PartnerCentralSellingAPI.Paginator.ListEngagementMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementmemberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngagementMembersRequestPaginateTypeDef]
    ) -> PageIterator[ListEngagementMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementMembers.html#PartnerCentralSellingAPI.Paginator.ListEngagementMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementmemberspaginator)
        """

if TYPE_CHECKING:
    _ListEngagementResourceAssociationsPaginatorBase = Paginator[
        ListEngagementResourceAssociationsResponseTypeDef
    ]
else:
    _ListEngagementResourceAssociationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEngagementResourceAssociationsPaginator(_ListEngagementResourceAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementResourceAssociations.html#PartnerCentralSellingAPI.Paginator.ListEngagementResourceAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementresourceassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngagementResourceAssociationsRequestPaginateTypeDef]
    ) -> PageIterator[ListEngagementResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagementResourceAssociations.html#PartnerCentralSellingAPI.Paginator.ListEngagementResourceAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementresourceassociationspaginator)
        """

if TYPE_CHECKING:
    _ListEngagementsPaginatorBase = Paginator[ListEngagementsResponseTypeDef]
else:
    _ListEngagementsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEngagementsPaginator(_ListEngagementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagements.html#PartnerCentralSellingAPI.Paginator.ListEngagements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngagementsRequestPaginateTypeDef]
    ) -> PageIterator[ListEngagementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListEngagements.html#PartnerCentralSellingAPI.Paginator.ListEngagements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listengagementspaginator)
        """

if TYPE_CHECKING:
    _ListOpportunitiesPaginatorBase = Paginator[ListOpportunitiesResponseTypeDef]
else:
    _ListOpportunitiesPaginatorBase = Paginator  # type: ignore[assignment]

class ListOpportunitiesPaginator(_ListOpportunitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunities.html#PartnerCentralSellingAPI.Paginator.ListOpportunities)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpportunitiesRequestPaginateTypeDef]
    ) -> PageIterator[ListOpportunitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunities.html#PartnerCentralSellingAPI.Paginator.ListOpportunities.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitiespaginator)
        """

if TYPE_CHECKING:
    _ListOpportunityBulkJobResultsPaginatorBase = Paginator[
        ListOpportunityBulkJobResultsResponseTypeDef
    ]
else:
    _ListOpportunityBulkJobResultsPaginatorBase = Paginator  # type: ignore[assignment]

class ListOpportunityBulkJobResultsPaginator(_ListOpportunityBulkJobResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunityBulkJobResults.html#PartnerCentralSellingAPI.Paginator.ListOpportunityBulkJobResults)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitybulkjobresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpportunityBulkJobResultsRequestPaginateTypeDef]
    ) -> PageIterator[ListOpportunityBulkJobResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunityBulkJobResults.html#PartnerCentralSellingAPI.Paginator.ListOpportunityBulkJobResults.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitybulkjobresultspaginator)
        """

if TYPE_CHECKING:
    _ListOpportunityBulkJobsPaginatorBase = Paginator[ListOpportunityBulkJobsResponseTypeDef]
else:
    _ListOpportunityBulkJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListOpportunityBulkJobsPaginator(_ListOpportunityBulkJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunityBulkJobs.html#PartnerCentralSellingAPI.Paginator.ListOpportunityBulkJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitybulkjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpportunityBulkJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListOpportunityBulkJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunityBulkJobs.html#PartnerCentralSellingAPI.Paginator.ListOpportunityBulkJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunitybulkjobspaginator)
        """

if TYPE_CHECKING:
    _ListOpportunityFromEngagementTasksPaginatorBase = Paginator[
        ListOpportunityFromEngagementTasksResponseTypeDef
    ]
else:
    _ListOpportunityFromEngagementTasksPaginatorBase = Paginator  # type: ignore[assignment]

class ListOpportunityFromEngagementTasksPaginator(_ListOpportunityFromEngagementTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunityFromEngagementTasks.html#PartnerCentralSellingAPI.Paginator.ListOpportunityFromEngagementTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunityfromengagementtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpportunityFromEngagementTasksRequestPaginateTypeDef]
    ) -> PageIterator[ListOpportunityFromEngagementTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListOpportunityFromEngagementTasks.html#PartnerCentralSellingAPI.Paginator.ListOpportunityFromEngagementTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listopportunityfromengagementtaskspaginator)
        """

if TYPE_CHECKING:
    _ListProspectingFromEngagementTasksPaginatorBase = Paginator[
        ListProspectingFromEngagementTasksResponseTypeDef
    ]
else:
    _ListProspectingFromEngagementTasksPaginatorBase = Paginator  # type: ignore[assignment]

class ListProspectingFromEngagementTasksPaginator(_ListProspectingFromEngagementTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListProspectingFromEngagementTasks.html#PartnerCentralSellingAPI.Paginator.ListProspectingFromEngagementTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listprospectingfromengagementtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProspectingFromEngagementTasksRequestPaginateTypeDef]
    ) -> PageIterator[ListProspectingFromEngagementTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListProspectingFromEngagementTasks.html#PartnerCentralSellingAPI.Paginator.ListProspectingFromEngagementTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listprospectingfromengagementtaskspaginator)
        """

if TYPE_CHECKING:
    _ListResourceSnapshotJobsPaginatorBase = Paginator[ListResourceSnapshotJobsResponseTypeDef]
else:
    _ListResourceSnapshotJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourceSnapshotJobsPaginator(_ListResourceSnapshotJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshotJobs.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshotJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceSnapshotJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListResourceSnapshotJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshotJobs.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshotJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotjobspaginator)
        """

if TYPE_CHECKING:
    _ListResourceSnapshotsPaginatorBase = Paginator[ListResourceSnapshotsResponseTypeDef]
else:
    _ListResourceSnapshotsPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourceSnapshotsPaginator(_ListResourceSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshots.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceSnapshotsRequestPaginateTypeDef]
    ) -> PageIterator[ListResourceSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListResourceSnapshots.html#PartnerCentralSellingAPI.Paginator.ListResourceSnapshots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listresourcesnapshotspaginator)
        """

if TYPE_CHECKING:
    _ListSolutionsPaginatorBase = Paginator[ListSolutionsResponseTypeDef]
else:
    _ListSolutionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSolutionsPaginator(_ListSolutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListSolutions.html#PartnerCentralSellingAPI.Paginator.ListSolutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listsolutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListSolutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/ListSolutions.html#PartnerCentralSellingAPI.Paginator.ListSolutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#listsolutionspaginator)
        """

if TYPE_CHECKING:
    _SearchCustomerAccountsPaginatorBase = Paginator[SearchCustomerAccountsResponseTypeDef]
else:
    _SearchCustomerAccountsPaginatorBase = Paginator  # type: ignore[assignment]

class SearchCustomerAccountsPaginator(_SearchCustomerAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/SearchCustomerAccounts.html#PartnerCentralSellingAPI.Paginator.SearchCustomerAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#searchcustomeraccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchCustomerAccountsRequestPaginateTypeDef]
    ) -> PageIterator[SearchCustomerAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/SearchCustomerAccounts.html#PartnerCentralSellingAPI.Paginator.SearchCustomerAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#searchcustomeraccountspaginator)
        """

if TYPE_CHECKING:
    _SearchEngagementsPaginatorBase = Paginator[SearchEngagementsResponseTypeDef]
else:
    _SearchEngagementsPaginatorBase = Paginator  # type: ignore[assignment]

class SearchEngagementsPaginator(_SearchEngagementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/SearchEngagements.html#PartnerCentralSellingAPI.Paginator.SearchEngagements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#searchengagementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchEngagementsRequestPaginateTypeDef]
    ) -> PageIterator[SearchEngagementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/SearchEngagements.html#PartnerCentralSellingAPI.Paginator.SearchEngagements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#searchengagementspaginator)
        """

if TYPE_CHECKING:
    _SearchOpportunitiesPaginatorBase = Paginator[SearchOpportunitiesResponseTypeDef]
else:
    _SearchOpportunitiesPaginatorBase = Paginator  # type: ignore[assignment]

class SearchOpportunitiesPaginator(_SearchOpportunitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/SearchOpportunities.html#PartnerCentralSellingAPI.Paginator.SearchOpportunities)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#searchopportunitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchOpportunitiesRequestPaginateTypeDef]
    ) -> PageIterator[SearchOpportunitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/paginator/SearchOpportunities.html#PartnerCentralSellingAPI.Paginator.SearchOpportunities.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/paginators/#searchopportunitiespaginator)
        """
