"""
Type annotations for partnercentral-selling service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_partnercentral_selling.client import PartnerCentralSellingAPIClient

    session = Session()
    client: PartnerCentralSellingAPIClient = session.client("partnercentral-selling")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

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
from .type_defs import (
    AcceptEngagementInvitationRequestTypeDef,
    AssignOpportunityRequestTypeDef,
    AssociateOpportunityRequestTypeDef,
    CreateCustomerAccountRequestTypeDef,
    CreateCustomerAccountResponseTypeDef,
    CreateEngagementContextRequestTypeDef,
    CreateEngagementContextResponseTypeDef,
    CreateEngagementInvitationRequestTypeDef,
    CreateEngagementInvitationResponseTypeDef,
    CreateEngagementRequestTypeDef,
    CreateEngagementResponseTypeDef,
    CreateOpportunityRequestTypeDef,
    CreateOpportunityResponseTypeDef,
    CreateResourceSnapshotJobRequestTypeDef,
    CreateResourceSnapshotJobResponseTypeDef,
    CreateResourceSnapshotRequestTypeDef,
    CreateResourceSnapshotResponseTypeDef,
    DeleteCustomerAccountRequestTypeDef,
    DeleteResourceSnapshotJobRequestTypeDef,
    DisassociateOpportunityRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAwsOpportunitySummaryRequestTypeDef,
    GetAwsOpportunitySummaryResponseTypeDef,
    GetCustomerAccountBulkJobReportUrlRequestTypeDef,
    GetCustomerAccountBulkJobReportUrlResponseTypeDef,
    GetCustomerAccountBulkJobRequestTypeDef,
    GetCustomerAccountBulkJobResponseTypeDef,
    GetCustomerAccountRequestTypeDef,
    GetCustomerAccountResponseTypeDef,
    GetCustomerAccountStatisticsRequestTypeDef,
    GetCustomerAccountStatisticsResponseTypeDef,
    GetEngagementInvitationRequestTypeDef,
    GetEngagementInvitationResponseTypeDef,
    GetEngagementRequestTypeDef,
    GetEngagementResponseTypeDef,
    GetOpportunityBulkJobReportUrlRequestTypeDef,
    GetOpportunityBulkJobReportUrlResponseTypeDef,
    GetOpportunityRequestTypeDef,
    GetOpportunityResponseTypeDef,
    GetProspectingFromEngagementTaskRequestTypeDef,
    GetProspectingFromEngagementTaskResponseTypeDef,
    GetResourceSnapshotJobRequestTypeDef,
    GetResourceSnapshotJobResponseTypeDef,
    GetResourceSnapshotRequestTypeDef,
    GetResourceSnapshotResponseTypeDef,
    GetSellingSystemSettingsRequestTypeDef,
    GetSellingSystemSettingsResponseTypeDef,
    ListCustomerAccountBulkJobResultsRequestTypeDef,
    ListCustomerAccountBulkJobResultsResponseTypeDef,
    ListCustomerAccountBulkJobsRequestTypeDef,
    ListCustomerAccountBulkJobsResponseTypeDef,
    ListEngagementByAcceptingInvitationTasksRequestTypeDef,
    ListEngagementByAcceptingInvitationTasksResponseTypeDef,
    ListEngagementFromOpportunityTasksRequestTypeDef,
    ListEngagementFromOpportunityTasksResponseTypeDef,
    ListEngagementGroupsRequestTypeDef,
    ListEngagementGroupsResponseTypeDef,
    ListEngagementInvitationsRequestTypeDef,
    ListEngagementInvitationsResponseTypeDef,
    ListEngagementMembersRequestTypeDef,
    ListEngagementMembersResponseTypeDef,
    ListEngagementResourceAssociationsRequestTypeDef,
    ListEngagementResourceAssociationsResponseTypeDef,
    ListEngagementsRequestTypeDef,
    ListEngagementsResponseTypeDef,
    ListOpportunitiesRequestTypeDef,
    ListOpportunitiesResponseTypeDef,
    ListOpportunityBulkJobResultsRequestTypeDef,
    ListOpportunityBulkJobResultsResponseTypeDef,
    ListOpportunityBulkJobsRequestTypeDef,
    ListOpportunityBulkJobsResponseTypeDef,
    ListOpportunityFromEngagementTasksRequestTypeDef,
    ListOpportunityFromEngagementTasksResponseTypeDef,
    ListProspectingFromEngagementTasksRequestTypeDef,
    ListProspectingFromEngagementTasksResponseTypeDef,
    ListResourceSnapshotJobsRequestTypeDef,
    ListResourceSnapshotJobsResponseTypeDef,
    ListResourceSnapshotsRequestTypeDef,
    ListResourceSnapshotsResponseTypeDef,
    ListSolutionsRequestTypeDef,
    ListSolutionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutSellingSystemSettingsRequestTypeDef,
    PutSellingSystemSettingsResponseTypeDef,
    RejectEngagementInvitationRequestTypeDef,
    SearchCustomerAccountsRequestTypeDef,
    SearchCustomerAccountsResponseTypeDef,
    SearchEngagementsRequestTypeDef,
    SearchEngagementsResponseTypeDef,
    SearchOpportunitiesRequestTypeDef,
    SearchOpportunitiesResponseTypeDef,
    StartCustomerAccountBulkJobRequestTypeDef,
    StartCustomerAccountBulkJobResponseTypeDef,
    StartEngagementByAcceptingInvitationTaskRequestTypeDef,
    StartEngagementByAcceptingInvitationTaskResponseTypeDef,
    StartEngagementFromOpportunityTaskRequestTypeDef,
    StartEngagementFromOpportunityTaskResponseTypeDef,
    StartOpportunityBulkJobRequestTypeDef,
    StartOpportunityBulkJobResponseTypeDef,
    StartOpportunityFromEngagementTaskRequestTypeDef,
    StartOpportunityFromEngagementTaskResponseTypeDef,
    StartProspectingFromEngagementTaskRequestTypeDef,
    StartProspectingFromEngagementTaskResponseTypeDef,
    StartResourceSnapshotJobRequestTypeDef,
    StopResourceSnapshotJobRequestTypeDef,
    SubmitOpportunityRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCustomerAccountRequestTypeDef,
    UpdateCustomerAccountResponseTypeDef,
    UpdateEngagementContextRequestTypeDef,
    UpdateEngagementContextResponseTypeDef,
    UpdateOpportunityRequestTypeDef,
    UpdateOpportunityResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("PartnerCentralSellingAPIClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class PartnerCentralSellingAPIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PartnerCentralSellingAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#generate_presigned_url)
        """

    def accept_engagement_invitation(
        self, **kwargs: Unpack[AcceptEngagementInvitationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use the <code>AcceptEngagementInvitation</code> action to accept an engagement
        invitation shared by AWS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/accept_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#accept_engagement_invitation)
        """

    def assign_opportunity(
        self, **kwargs: Unpack[AssignOpportunityRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to reassign an existing <code>Opportunity</code> to another user
        within your Partner Central account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/assign_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#assign_opportunity)
        """

    def associate_opportunity(
        self, **kwargs: Unpack[AssociateOpportunityRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to create a formal association between an <code>Opportunity</code>
        and various related entities, enriching the context and details of the
        opportunity for better collaboration and decision making.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/associate_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#associate_opportunity)
        """

    def create_customer_account(
        self, **kwargs: Unpack[CreateCustomerAccountRequestTypeDef]
    ) -> CreateCustomerAccountResponseTypeDef:
        """
        Use <code>CreateCustomerAccount</code> to map a customer account from your
        records to an AWS customer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_customer_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_customer_account)
        """

    def create_engagement(
        self, **kwargs: Unpack[CreateEngagementRequestTypeDef]
    ) -> CreateEngagementResponseTypeDef:
        """
        The <code>CreateEngagement</code> action allows you to create an
        <code>Engagement</code>, which serves as a collaborative space between
        different parties such as AWS Partners and AWS Sellers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_engagement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_engagement)
        """

    def create_engagement_context(
        self, **kwargs: Unpack[CreateEngagementContextRequestTypeDef]
    ) -> CreateEngagementContextResponseTypeDef:
        """
        Creates a new context within an existing engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_engagement_context.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_engagement_context)
        """

    def create_engagement_invitation(
        self, **kwargs: Unpack[CreateEngagementInvitationRequestTypeDef]
    ) -> CreateEngagementInvitationResponseTypeDef:
        """
        This action creates an invitation from a sender to a single receiver to join an
        engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_engagement_invitation)
        """

    def create_opportunity(
        self, **kwargs: Unpack[CreateOpportunityRequestTypeDef]
    ) -> CreateOpportunityResponseTypeDef:
        """
        Creates an <code>Opportunity</code> record in Partner Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_opportunity)
        """

    def create_resource_snapshot(
        self, **kwargs: Unpack[CreateResourceSnapshotRequestTypeDef]
    ) -> CreateResourceSnapshotResponseTypeDef:
        """
        This action allows you to create an immutable snapshot of a specific resource,
        such as an opportunity, within the context of an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_resource_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_resource_snapshot)
        """

    def create_resource_snapshot_job(
        self, **kwargs: Unpack[CreateResourceSnapshotJobRequestTypeDef]
    ) -> CreateResourceSnapshotJobResponseTypeDef:
        """
        Use this action to create a job to generate a snapshot of the specified
        resource within an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#create_resource_snapshot_job)
        """

    def delete_customer_account(
        self, **kwargs: Unpack[DeleteCustomerAccountRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Use <code>DeleteCustomerAccount</code> to delete a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/delete_customer_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#delete_customer_account)
        """

    def delete_resource_snapshot_job(
        self, **kwargs: Unpack[DeleteResourceSnapshotJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this action to deletes a previously created resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/delete_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#delete_resource_snapshot_job)
        """

    def disassociate_opportunity(
        self, **kwargs: Unpack[DisassociateOpportunityRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Allows you to remove an existing association between an
        <code>Opportunity</code> and related entities, such as a Partner Solution,
        Amazon Web Services product, or an Amazon Web Services Marketplace offer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/disassociate_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#disassociate_opportunity)
        """

    def get_aws_opportunity_summary(
        self, **kwargs: Unpack[GetAwsOpportunitySummaryRequestTypeDef]
    ) -> GetAwsOpportunitySummaryResponseTypeDef:
        """
        Retrieves a summary of an AWS Opportunity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_aws_opportunity_summary.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_aws_opportunity_summary)
        """

    def get_customer_account(
        self, **kwargs: Unpack[GetCustomerAccountRequestTypeDef]
    ) -> GetCustomerAccountResponseTypeDef:
        """
        Use <code>GetCustomerAccount</code> to retrieve the details of a customer
        account, including the customer information that you provided, the enrichment
        status, and the enrichment information that AWS provides when the status is
        <code>ENRICHED</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_customer_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_customer_account)
        """

    def get_customer_account_bulk_job(
        self, **kwargs: Unpack[GetCustomerAccountBulkJobRequestTypeDef]
    ) -> GetCustomerAccountBulkJobResponseTypeDef:
        """
        Use <code>GetCustomerAccountBulkJob</code> to retrieve the status and record
        counts of a bulk job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_customer_account_bulk_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_customer_account_bulk_job)
        """

    def get_customer_account_bulk_job_report_url(
        self, **kwargs: Unpack[GetCustomerAccountBulkJobReportUrlRequestTypeDef]
    ) -> GetCustomerAccountBulkJobReportUrlResponseTypeDef:
        """
        Use <code>GetCustomerAccountBulkJobReportUrl</code> to get a temporary URL for
        downloading the report of a bulk job, such as the list of records that failed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_customer_account_bulk_job_report_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_customer_account_bulk_job_report_url)
        """

    def get_customer_account_statistics(
        self, **kwargs: Unpack[GetCustomerAccountStatisticsRequestTypeDef]
    ) -> GetCustomerAccountStatisticsResponseTypeDef:
        """
        Use <code>GetCustomerAccountStatistics</code> to count your customer accounts
        and group them by fields such as industry, geography, or enrichment status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_customer_account_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_customer_account_statistics)
        """

    def get_engagement(
        self, **kwargs: Unpack[GetEngagementRequestTypeDef]
    ) -> GetEngagementResponseTypeDef:
        """
        Use this action to retrieve the engagement record for a given
        <code>EngagementIdentifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_engagement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_engagement)
        """

    def get_engagement_invitation(
        self, **kwargs: Unpack[GetEngagementInvitationRequestTypeDef]
    ) -> GetEngagementInvitationResponseTypeDef:
        """
        Retrieves the details of an engagement invitation shared by AWS with a partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_engagement_invitation)
        """

    def get_opportunity(
        self, **kwargs: Unpack[GetOpportunityRequestTypeDef]
    ) -> GetOpportunityResponseTypeDef:
        """
        Fetches the <code>Opportunity</code> record from Partner Central by a given
        <code>Identifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_opportunity)
        """

    def get_opportunity_bulk_job_report_url(
        self, **kwargs: Unpack[GetOpportunityBulkJobReportUrlRequestTypeDef]
    ) -> GetOpportunityBulkJobReportUrlResponseTypeDef:
        """
        Gets the status of the failed-records report for a finished opportunity bulk
        job and, when the report is ready, a temporary URL to download it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_opportunity_bulk_job_report_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_opportunity_bulk_job_report_url)
        """

    def get_prospecting_from_engagement_task(
        self, **kwargs: Unpack[GetProspectingFromEngagementTaskRequestTypeDef]
    ) -> GetProspectingFromEngagementTaskResponseTypeDef:
        """
        Retrieves the details and current status of a prospecting task previously
        started with <code>StartProspectingFromEngagementTask</code> to enable polling
        for completion and access to per-engagement processing results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_prospecting_from_engagement_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_prospecting_from_engagement_task)
        """

    def get_resource_snapshot(
        self, **kwargs: Unpack[GetResourceSnapshotRequestTypeDef]
    ) -> GetResourceSnapshotResponseTypeDef:
        """
        Use this action to retrieve a specific snapshot record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_resource_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_resource_snapshot)
        """

    def get_resource_snapshot_job(
        self, **kwargs: Unpack[GetResourceSnapshotJobRequestTypeDef]
    ) -> GetResourceSnapshotJobResponseTypeDef:
        """
        Use this action to retrieves information about a specific resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_resource_snapshot_job)
        """

    def get_selling_system_settings(
        self, **kwargs: Unpack[GetSellingSystemSettingsRequestTypeDef]
    ) -> GetSellingSystemSettingsResponseTypeDef:
        """
        Retrieves the currently set system settings, which include the IAM Role used
        for resource snapshot jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_selling_system_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_selling_system_settings)
        """

    def list_customer_account_bulk_job_results(
        self, **kwargs: Unpack[ListCustomerAccountBulkJobResultsRequestTypeDef]
    ) -> ListCustomerAccountBulkJobResultsResponseTypeDef:
        """
        Use <code>ListCustomerAccountBulkJobResults</code> to list the outcome of each
        record in a bulk job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_customer_account_bulk_job_results.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_customer_account_bulk_job_results)
        """

    def list_customer_account_bulk_jobs(
        self, **kwargs: Unpack[ListCustomerAccountBulkJobsRequestTypeDef]
    ) -> ListCustomerAccountBulkJobsResponseTypeDef:
        """
        Use <code>ListCustomerAccountBulkJobs</code> to list the bulk jobs in the
        specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_customer_account_bulk_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_customer_account_bulk_jobs)
        """

    def list_engagement_by_accepting_invitation_tasks(
        self, **kwargs: Unpack[ListEngagementByAcceptingInvitationTasksRequestTypeDef]
    ) -> ListEngagementByAcceptingInvitationTasksResponseTypeDef:
        """
        Lists all in-progress, completed, or failed
        StartEngagementByAcceptingInvitationTask tasks that were initiated by the
        caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_by_accepting_invitation_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_by_accepting_invitation_tasks)
        """

    def list_engagement_from_opportunity_tasks(
        self, **kwargs: Unpack[ListEngagementFromOpportunityTasksRequestTypeDef]
    ) -> ListEngagementFromOpportunityTasksResponseTypeDef:
        """
        Lists all in-progress, completed, or failed EngagementFromOpportunity tasks
        that were initiated by the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_from_opportunity_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_from_opportunity_tasks)
        """

    def list_engagement_groups(
        self, **kwargs: Unpack[ListEngagementGroupsRequestTypeDef]
    ) -> ListEngagementGroupsResponseTypeDef:
        """
        Lists the active, fully curated AWS Partner Central engagement groups that are
        available to you in the specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_groups)
        """

    def list_engagement_invitations(
        self, **kwargs: Unpack[ListEngagementInvitationsRequestTypeDef]
    ) -> ListEngagementInvitationsResponseTypeDef:
        """
        Retrieves a list of engagement invitations sent to the partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_invitations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_invitations)
        """

    def list_engagement_members(
        self, **kwargs: Unpack[ListEngagementMembersRequestTypeDef]
    ) -> ListEngagementMembersResponseTypeDef:
        """
        Retrieves the details of member partners in an Engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_members.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_members)
        """

    def list_engagement_resource_associations(
        self, **kwargs: Unpack[ListEngagementResourceAssociationsRequestTypeDef]
    ) -> ListEngagementResourceAssociationsResponseTypeDef:
        """
        Lists the associations between resources and engagements where the caller is a
        member and has at least one snapshot in the engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_resource_associations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagement_resource_associations)
        """

    def list_engagements(
        self, **kwargs: Unpack[ListEngagementsRequestTypeDef]
    ) -> ListEngagementsResponseTypeDef:
        """
        This action allows users to retrieve a list of Engagement records from Partner
        Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_engagements)
        """

    def list_opportunities(
        self, **kwargs: Unpack[ListOpportunitiesRequestTypeDef]
    ) -> ListOpportunitiesResponseTypeDef:
        """
        This request accepts a list of filters that retrieve opportunity subsets as
        well as sort options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_opportunities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_opportunities)
        """

    def list_opportunity_bulk_job_results(
        self, **kwargs: Unpack[ListOpportunityBulkJobResultsRequestTypeDef]
    ) -> ListOpportunityBulkJobResultsResponseTypeDef:
        """
        Lists the outcome of each record in an opportunity bulk job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_opportunity_bulk_job_results.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_opportunity_bulk_job_results)
        """

    def list_opportunity_bulk_jobs(
        self, **kwargs: Unpack[ListOpportunityBulkJobsRequestTypeDef]
    ) -> ListOpportunityBulkJobsResponseTypeDef:
        """
        Lists the opportunity bulk jobs in the specified catalog, newest first.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_opportunity_bulk_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_opportunity_bulk_jobs)
        """

    def list_opportunity_from_engagement_tasks(
        self, **kwargs: Unpack[ListOpportunityFromEngagementTasksRequestTypeDef]
    ) -> ListOpportunityFromEngagementTasksResponseTypeDef:
        """
        Lists all in-progress, completed, or failed opportunity creation tasks from
        engagements that were initiated by the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_opportunity_from_engagement_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_opportunity_from_engagement_tasks)
        """

    def list_prospecting_from_engagement_tasks(
        self, **kwargs: Unpack[ListProspectingFromEngagementTasksRequestTypeDef]
    ) -> ListProspectingFromEngagementTasksResponseTypeDef:
        """
        Lists all prospecting tasks initiated by the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_prospecting_from_engagement_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_prospecting_from_engagement_tasks)
        """

    def list_resource_snapshot_jobs(
        self, **kwargs: Unpack[ListResourceSnapshotJobsRequestTypeDef]
    ) -> ListResourceSnapshotJobsResponseTypeDef:
        """
        Lists resource snapshot jobs owned by the customer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_resource_snapshot_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_resource_snapshot_jobs)
        """

    def list_resource_snapshots(
        self, **kwargs: Unpack[ListResourceSnapshotsRequestTypeDef]
    ) -> ListResourceSnapshotsResponseTypeDef:
        """
        Retrieves a list of resource view snapshots based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_resource_snapshots.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_resource_snapshots)
        """

    def list_solutions(
        self, **kwargs: Unpack[ListSolutionsRequestTypeDef]
    ) -> ListSolutionsResponseTypeDef:
        """
        Retrieves a list of Partner Solutions that the partner registered on Partner
        Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_solutions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_solutions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#list_tags_for_resource)
        """

    def put_selling_system_settings(
        self, **kwargs: Unpack[PutSellingSystemSettingsRequestTypeDef]
    ) -> PutSellingSystemSettingsResponseTypeDef:
        """
        Updates the currently set system settings, which include the IAM Role used for
        resource snapshot jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/put_selling_system_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#put_selling_system_settings)
        """

    def reject_engagement_invitation(
        self, **kwargs: Unpack[RejectEngagementInvitationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action rejects an <code>EngagementInvitation</code> that AWS shared.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/reject_engagement_invitation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#reject_engagement_invitation)
        """

    def search_customer_accounts(
        self, **kwargs: Unpack[SearchCustomerAccountsRequestTypeDef]
    ) -> SearchCustomerAccountsResponseTypeDef:
        """
        Use <code>SearchCustomerAccounts</code> to find customer accounts in the
        specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/search_customer_accounts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#search_customer_accounts)
        """

    def search_engagements(
        self, **kwargs: Unpack[SearchEngagementsRequestTypeDef]
    ) -> SearchEngagementsResponseTypeDef:
        """
        Searches the engagements in AWS Partner Central that match your criteria, such
        as customer industry or geography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/search_engagements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#search_engagements)
        """

    def search_opportunities(
        self, **kwargs: Unpack[SearchOpportunitiesRequestTypeDef]
    ) -> SearchOpportunitiesResponseTypeDef:
        """
        The <code>SearchOpportunities</code> operation in the AWS Partner Central
        Selling API searches and filters the opportunities available to you in AWS
        Partner Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/search_opportunities.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#search_opportunities)
        """

    def start_customer_account_bulk_job(
        self, **kwargs: Unpack[StartCustomerAccountBulkJobRequestTypeDef]
    ) -> StartCustomerAccountBulkJobResponseTypeDef:
        """
        Use <code>StartCustomerAccountBulkJob</code> to create many customer accounts
        from a single file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_customer_account_bulk_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_customer_account_bulk_job)
        """

    def start_engagement_by_accepting_invitation_task(
        self, **kwargs: Unpack[StartEngagementByAcceptingInvitationTaskRequestTypeDef]
    ) -> StartEngagementByAcceptingInvitationTaskResponseTypeDef:
        """
        This action starts the engagement by accepting an
        <code>EngagementInvitation</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_engagement_by_accepting_invitation_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_engagement_by_accepting_invitation_task)
        """

    def start_engagement_from_opportunity_task(
        self, **kwargs: Unpack[StartEngagementFromOpportunityTaskRequestTypeDef]
    ) -> StartEngagementFromOpportunityTaskResponseTypeDef:
        """
        Similar to <code>StartEngagementByAcceptingInvitationTask</code>, this action
        is asynchronous and performs multiple steps before completion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_engagement_from_opportunity_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_engagement_from_opportunity_task)
        """

    def start_opportunity_bulk_job(
        self, **kwargs: Unpack[StartOpportunityBulkJobRequestTypeDef]
    ) -> StartOpportunityBulkJobResponseTypeDef:
        """
        The <code>StartOpportunityBulkJob</code> operation creates or updates many
        opportunities in AWS Partner Central (Partner Central) from a single CSV file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_opportunity_bulk_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_opportunity_bulk_job)
        """

    def start_opportunity_from_engagement_task(
        self, **kwargs: Unpack[StartOpportunityFromEngagementTaskRequestTypeDef]
    ) -> StartOpportunityFromEngagementTaskResponseTypeDef:
        """
        This action creates an opportunity from an existing engagement context.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_opportunity_from_engagement_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_opportunity_from_engagement_task)
        """

    def start_prospecting_from_engagement_task(
        self, **kwargs: Unpack[StartProspectingFromEngagementTaskRequestTypeDef]
    ) -> StartProspectingFromEngagementTaskResponseTypeDef:
        """
        Starts a task to convert one or more engagement contexts into new prospecting
        leads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_prospecting_from_engagement_task.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_prospecting_from_engagement_task)
        """

    def start_resource_snapshot_job(
        self, **kwargs: Unpack[StartResourceSnapshotJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a resource snapshot job that has been previously created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#start_resource_snapshot_job)
        """

    def stop_resource_snapshot_job(
        self, **kwargs: Unpack[StopResourceSnapshotJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/stop_resource_snapshot_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#stop_resource_snapshot_job)
        """

    def submit_opportunity(
        self, **kwargs: Unpack[SubmitOpportunityRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this action to submit an Opportunity that was previously created by partner
        for AWS review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/submit_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#submit_opportunity)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes a tag or tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#untag_resource)
        """

    def update_customer_account(
        self, **kwargs: Unpack[UpdateCustomerAccountRequestTypeDef]
    ) -> UpdateCustomerAccountResponseTypeDef:
        """
        Use <code>UpdateCustomerAccount</code> to replace the customer information on
        an existing customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/update_customer_account.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#update_customer_account)
        """

    def update_engagement_context(
        self, **kwargs: Unpack[UpdateEngagementContextRequestTypeDef]
    ) -> UpdateEngagementContextResponseTypeDef:
        """
        Updates the context information for an existing engagement with new or modified
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/update_engagement_context.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#update_engagement_context)
        """

    def update_opportunity(
        self, **kwargs: Unpack[UpdateOpportunityRequestTypeDef]
    ) -> UpdateOpportunityResponseTypeDef:
        """
        Updates the <code>Opportunity</code> record identified by a given
        <code>Identifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/update_opportunity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#update_opportunity)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_customer_account_bulk_job_results"]
    ) -> ListCustomerAccountBulkJobResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_customer_account_bulk_jobs"]
    ) -> ListCustomerAccountBulkJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_by_accepting_invitation_tasks"]
    ) -> ListEngagementByAcceptingInvitationTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_from_opportunity_tasks"]
    ) -> ListEngagementFromOpportunityTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_groups"]
    ) -> ListEngagementGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_invitations"]
    ) -> ListEngagementInvitationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_members"]
    ) -> ListEngagementMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_resource_associations"]
    ) -> ListEngagementResourceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagements"]
    ) -> ListEngagementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_opportunities"]
    ) -> ListOpportunitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_opportunity_bulk_job_results"]
    ) -> ListOpportunityBulkJobResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_opportunity_bulk_jobs"]
    ) -> ListOpportunityBulkJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_opportunity_from_engagement_tasks"]
    ) -> ListOpportunityFromEngagementTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_prospecting_from_engagement_tasks"]
    ) -> ListProspectingFromEngagementTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_snapshot_jobs"]
    ) -> ListResourceSnapshotJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_snapshots"]
    ) -> ListResourceSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_solutions"]
    ) -> ListSolutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_customer_accounts"]
    ) -> SearchCustomerAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_engagements"]
    ) -> SearchEngagementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_opportunities"]
    ) -> SearchOpportunitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/client/#get_paginator)
        """
