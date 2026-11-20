"""
Main interface for partnercentral-selling service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_partnercentral_selling import (
        Client,
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
        PartnerCentralSellingAPIClient,
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

from .client import PartnerCentralSellingAPIClient
from .paginator import (
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

Client = PartnerCentralSellingAPIClient

__all__ = (
    "Client",
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
    "PartnerCentralSellingAPIClient",
    "SearchCustomerAccountsPaginator",
    "SearchEngagementsPaginator",
    "SearchOpportunitiesPaginator",
)
