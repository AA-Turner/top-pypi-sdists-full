"""
Type annotations for partnercentral-selling service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_selling/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_partnercentral_selling.type_defs import AcceptEngagementInvitationRequestTypeDef

    data: AcceptEngagementInvitationRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AggregatableFieldType,
    AwsClosedLostReasonType,
    AwsFundingUsedType,
    AwsMemberBusinessTitleType,
    AwsOpportunityStageType,
    BulkJobStatusType,
    BulkOperationTypeType,
    BulkRecordStatusType,
    BulkReportStatusType,
    BulkReportTypeType,
    ChannelType,
    ClosedLostReasonType,
    CompetitorNameType,
    ContactWindowType,
    CountryCodeType,
    CurrencyCodeType,
    CustomerAccountFailureReasonType,
    DayOfWeekType,
    DeliveryModelType,
    EngagementContextTypeType,
    EngagementGroupSortNameType,
    EngagementInvitationPayloadTypeType,
    EngagementScoreType,
    EngagementSearchFilterNameType,
    EngagementSearchSortNameType,
    EnrichmentStatusType,
    FilterableFieldType,
    IndustryType,
    InvitationStatusType,
    InvolvementTypeChangeReasonType,
    MarketingSourceType,
    NationalSecurityType,
    OpportunityOriginType,
    OpportunitySearchFilterNameType,
    OpportunitySearchSortNameType,
    OpportunitySortNameType,
    OpportunityTypeType,
    ParticipantTypeType,
    PrimaryNeedFromAwsType,
    ProspectingFromEngagementTaskSortNameType,
    ProspectingTaskStatusType,
    ReadinessLevelType,
    ReasonCodeType,
    ReceiverResponsibilityType,
    RelatedEntityTypeType,
    ResourceSnapshotJobStatusType,
    RevenueModelType,
    ReviewStatusType,
    SalesActivityType,
    SalesInvolvementTypeType,
    SearchEngagementScoreType,
    SolutionSortNameType,
    SolutionStatusType,
    SortableFieldType,
    SortOrderType,
    StageType,
    TaskStatusType,
    VisibilityType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptEngagementInvitationRequestTypeDef",
    "AccountCustomerTypeDef",
    "AccountPlanningInvitationPayloadOutputTypeDef",
    "AccountPlanningInvitationPayloadTypeDef",
    "AccountPlanningInvitationPayloadUnionTypeDef",
    "AccountReceiverTypeDef",
    "AccountSummaryTypeDef",
    "AccountTypeDef",
    "AddressSummaryTypeDef",
    "AddressTypeDef",
    "AggregationRequestTypeDef",
    "AggregationResultTypeDef",
    "AssignOpportunityRequestTypeDef",
    "AssigneeContactTypeDef",
    "AssociateOpportunityRequestTypeDef",
    "AwsEnrichmentCustomerSummaryTypeDef",
    "AwsEnrichmentCustomerTypeDef",
    "AwsEnrichmentInsightsSummaryTypeDef",
    "AwsEnrichmentInsightsTypeDef",
    "AwsEnrichmentSummaryTypeDef",
    "AwsEnrichmentTypeDef",
    "AwsOpportunityCustomerTypeDef",
    "AwsOpportunityInsightsTypeDef",
    "AwsOpportunityLifeCycleTypeDef",
    "AwsOpportunityProjectTypeDef",
    "AwsOpportunityRelatedEntitiesTypeDef",
    "AwsOpportunitySummaryFullViewTypeDef",
    "AwsProductDetailsTypeDef",
    "AwsProductInsightsTypeDef",
    "AwsProductOptimizationTypeDef",
    "AwsProductsSpendInsightsBySourceTypeDef",
    "AwsSoftwareRevenueTypeDef",
    "AwsSubmissionTypeDef",
    "AwsTeamMemberTypeDef",
    "BestOutreachWindowTypeDef",
    "BucketTypeDef",
    "BulkJobResultTypeDef",
    "ChannelRecommendationOutputTypeDef",
    "ChannelRecommendationTypeDef",
    "ChannelRecommendationUnionTypeDef",
    "ContactTypeDef",
    "CreateCustomerAccountRequestTypeDef",
    "CreateCustomerAccountResponseTypeDef",
    "CreateEngagementContextRequestTypeDef",
    "CreateEngagementContextResponseTypeDef",
    "CreateEngagementInvitationRequestTypeDef",
    "CreateEngagementInvitationResponseTypeDef",
    "CreateEngagementRequestTypeDef",
    "CreateEngagementResponseTypeDef",
    "CreateOpportunityRequestTypeDef",
    "CreateOpportunityResponseTypeDef",
    "CreateResourceSnapshotJobRequestTypeDef",
    "CreateResourceSnapshotJobResponseTypeDef",
    "CreateResourceSnapshotRequestTypeDef",
    "CreateResourceSnapshotResponseTypeDef",
    "CreatedDateFilterTypeDef",
    "CustomerAccountBulkJobFilterTypeDef",
    "CustomerAccountBulkJobSummaryTypeDef",
    "CustomerAccountContextTypeDef",
    "CustomerAccountDataTypeDef",
    "CustomerAccountDetailsSummaryTypeDef",
    "CustomerAccountSortTypeDef",
    "CustomerAccountSummaryTypeDef",
    "CustomerOutputTypeDef",
    "CustomerProjectsContextTypeDef",
    "CustomerSummaryTypeDef",
    "CustomerTypeDef",
    "CustomerUnionTypeDef",
    "DeleteCustomerAccountRequestTypeDef",
    "DeleteResourceSnapshotJobRequestTypeDef",
    "DisassociateOpportunityRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EngagementContextDetailsOutputTypeDef",
    "EngagementContextDetailsTypeDef",
    "EngagementContextDetailsUnionTypeDef",
    "EngagementContextPayloadOutputTypeDef",
    "EngagementContextPayloadTypeDef",
    "EngagementContextPayloadUnionTypeDef",
    "EngagementCustomerProjectDetailsTypeDef",
    "EngagementCustomerTypeDef",
    "EngagementGroupSortTypeDef",
    "EngagementGroupSummaryTypeDef",
    "EngagementInvitationSummaryTypeDef",
    "EngagementMemberSummaryTypeDef",
    "EngagementMemberTypeDef",
    "EngagementProspectingResultTypeDef",
    "EngagementResourceAssociationSummaryTypeDef",
    "EngagementSearchFilterPaginatorTypeDef",
    "EngagementSearchFilterTypeDef",
    "EngagementSearchFilterValueTypeDef",
    "EngagementSearchPredicateTypeDef",
    "EngagementSearchSortTypeDef",
    "EngagementSearchSummaryTypeDef",
    "EngagementSortTypeDef",
    "EngagementSummaryTypeDef",
    "EnrichmentContextTypeDef",
    "ExpectedContractDurationTypeDef",
    "ExpectedCustomerSpendTypeDef",
    "FilterConditionTypeDef",
    "FilterPaginatorTypeDef",
    "FilterTypeDef",
    "FilterValueTypeDef",
    "GetAwsOpportunitySummaryRequestTypeDef",
    "GetAwsOpportunitySummaryResponseTypeDef",
    "GetCustomerAccountBulkJobReportUrlRequestTypeDef",
    "GetCustomerAccountBulkJobReportUrlResponseTypeDef",
    "GetCustomerAccountBulkJobRequestTypeDef",
    "GetCustomerAccountBulkJobResponseTypeDef",
    "GetCustomerAccountRequestTypeDef",
    "GetCustomerAccountResponseTypeDef",
    "GetCustomerAccountStatisticsRequestTypeDef",
    "GetCustomerAccountStatisticsResponseTypeDef",
    "GetEngagementInvitationRequestTypeDef",
    "GetEngagementInvitationResponseTypeDef",
    "GetEngagementRequestTypeDef",
    "GetEngagementResponseTypeDef",
    "GetOpportunityBulkJobReportUrlRequestTypeDef",
    "GetOpportunityBulkJobReportUrlResponseTypeDef",
    "GetOpportunityRequestTypeDef",
    "GetOpportunityResponseTypeDef",
    "GetProspectingFromEngagementTaskRequestTypeDef",
    "GetProspectingFromEngagementTaskResponseTypeDef",
    "GetResourceSnapshotJobRequestTypeDef",
    "GetResourceSnapshotJobResponseTypeDef",
    "GetResourceSnapshotRequestTypeDef",
    "GetResourceSnapshotResponseTypeDef",
    "GetSellingSystemSettingsRequestTypeDef",
    "GetSellingSystemSettingsResponseTypeDef",
    "InvitationProspectingResultAwsTypeDef",
    "InvitationTypeDef",
    "IssueTypeDef",
    "LastModifiedDateTypeDef",
    "LeadAddressTypeDef",
    "LeadContactTypeDef",
    "LeadContextOutputTypeDef",
    "LeadContextTypeDef",
    "LeadContextUnionTypeDef",
    "LeadCustomerTypeDef",
    "LeadInsightsOutputTypeDef",
    "LeadInsightsTypeDef",
    "LeadInsightsUnionTypeDef",
    "LeadInteractionOutputTypeDef",
    "LeadInteractionTypeDef",
    "LeadInteractionUnionTypeDef",
    "LeadInvitationCustomerTypeDef",
    "LeadInvitationInteractionTypeDef",
    "LeadInvitationPayloadTypeDef",
    "LifeCycleForViewTypeDef",
    "LifeCycleOutputTypeDef",
    "LifeCycleSummaryTypeDef",
    "LifeCycleTypeDef",
    "LifeCycleUnionTypeDef",
    "ListCustomerAccountBulkJobResultsRequestPaginateTypeDef",
    "ListCustomerAccountBulkJobResultsRequestTypeDef",
    "ListCustomerAccountBulkJobResultsResponseTypeDef",
    "ListCustomerAccountBulkJobsRequestPaginateTypeDef",
    "ListCustomerAccountBulkJobsRequestTypeDef",
    "ListCustomerAccountBulkJobsResponseTypeDef",
    "ListEngagementByAcceptingInvitationTaskSummaryTypeDef",
    "ListEngagementByAcceptingInvitationTasksRequestPaginateTypeDef",
    "ListEngagementByAcceptingInvitationTasksRequestTypeDef",
    "ListEngagementByAcceptingInvitationTasksResponseTypeDef",
    "ListEngagementFromOpportunityTaskSummaryTypeDef",
    "ListEngagementFromOpportunityTasksRequestPaginateTypeDef",
    "ListEngagementFromOpportunityTasksRequestTypeDef",
    "ListEngagementFromOpportunityTasksResponseTypeDef",
    "ListEngagementGroupsRequestPaginateTypeDef",
    "ListEngagementGroupsRequestTypeDef",
    "ListEngagementGroupsResponseTypeDef",
    "ListEngagementInvitationsRequestPaginateTypeDef",
    "ListEngagementInvitationsRequestTypeDef",
    "ListEngagementInvitationsResponseTypeDef",
    "ListEngagementMembersRequestPaginateTypeDef",
    "ListEngagementMembersRequestTypeDef",
    "ListEngagementMembersResponseTypeDef",
    "ListEngagementResourceAssociationsRequestPaginateTypeDef",
    "ListEngagementResourceAssociationsRequestTypeDef",
    "ListEngagementResourceAssociationsResponseTypeDef",
    "ListEngagementsRequestPaginateTypeDef",
    "ListEngagementsRequestTypeDef",
    "ListEngagementsResponseTypeDef",
    "ListOpportunitiesRequestPaginateTypeDef",
    "ListOpportunitiesRequestTypeDef",
    "ListOpportunitiesResponseTypeDef",
    "ListOpportunityBulkJobResultsRequestPaginateTypeDef",
    "ListOpportunityBulkJobResultsRequestTypeDef",
    "ListOpportunityBulkJobResultsResponseTypeDef",
    "ListOpportunityBulkJobsRequestPaginateTypeDef",
    "ListOpportunityBulkJobsRequestTypeDef",
    "ListOpportunityBulkJobsResponseTypeDef",
    "ListOpportunityFromEngagementTaskSummaryTypeDef",
    "ListOpportunityFromEngagementTasksRequestPaginateTypeDef",
    "ListOpportunityFromEngagementTasksRequestTypeDef",
    "ListOpportunityFromEngagementTasksResponseTypeDef",
    "ListProspectingFromEngagementTasksRequestPaginateTypeDef",
    "ListProspectingFromEngagementTasksRequestTypeDef",
    "ListProspectingFromEngagementTasksResponseTypeDef",
    "ListResourceSnapshotJobsRequestPaginateTypeDef",
    "ListResourceSnapshotJobsRequestTypeDef",
    "ListResourceSnapshotJobsResponseTypeDef",
    "ListResourceSnapshotsRequestPaginateTypeDef",
    "ListResourceSnapshotsRequestTypeDef",
    "ListResourceSnapshotsResponseTypeDef",
    "ListSolutionsRequestPaginateTypeDef",
    "ListSolutionsRequestTypeDef",
    "ListSolutionsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTasksSortBaseTypeDef",
    "MarketingOutputTypeDef",
    "MarketingTypeDef",
    "MarketingUnionTypeDef",
    "MonetaryValueTypeDef",
    "NextStepsHistoryOutputTypeDef",
    "NextStepsHistoryTypeDef",
    "OpportunityBulkJobSummaryTypeDef",
    "OpportunityEngagementInvitationSortTypeDef",
    "OpportunityInvitationPayloadOutputTypeDef",
    "OpportunityInvitationPayloadTypeDef",
    "OpportunityInvitationPayloadUnionTypeDef",
    "OpportunityQualityTypeDef",
    "OpportunitySearchAccountTypeDef",
    "OpportunitySearchAddressTypeDef",
    "OpportunitySearchAwsSummaryTypeDef",
    "OpportunitySearchCustomerTypeDef",
    "OpportunitySearchExpectedCustomerSpendTypeDef",
    "OpportunitySearchFilterPaginatorTypeDef",
    "OpportunitySearchFilterTypeDef",
    "OpportunitySearchFilterValueTypeDef",
    "OpportunitySearchInsightsTypeDef",
    "OpportunitySearchLifeCycleTypeDef",
    "OpportunitySearchOpportunityQualityTypeDef",
    "OpportunitySearchPredicateTypeDef",
    "OpportunitySearchProjectTypeDef",
    "OpportunitySearchRelatedEntityIdentifiersTypeDef",
    "OpportunitySearchSortTypeDef",
    "OpportunitySearchSummaryTypeDef",
    "OpportunitySearchTeamMemberTypeDef",
    "OpportunitySortTypeDef",
    "OpportunitySummaryTypeDef",
    "OpportunitySummaryViewTypeDef",
    "PaginatorConfigTypeDef",
    "PayloadOutputTypeDef",
    "PayloadTypeDef",
    "PayloadUnionTypeDef",
    "PreferredContactWindowTypeDef",
    "ProfileNextStepsHistoryTypeDef",
    "ProjectDetailsOutputTypeDef",
    "ProjectDetailsTypeDef",
    "ProjectDetailsUnionTypeDef",
    "ProjectOutputTypeDef",
    "ProjectSummaryTypeDef",
    "ProjectTypeDef",
    "ProjectUnionTypeDef",
    "ProjectViewTypeDef",
    "ProspectingFromEngagementTaskSortTypeDef",
    "ProspectingInsightsTypeDef",
    "ProspectingResultAwsOutputTypeDef",
    "ProspectingResultAwsTypeDef",
    "ProspectingResultAwsUnionTypeDef",
    "ProspectingResultCustomerOutputTypeDef",
    "ProspectingResultCustomerTypeDef",
    "ProspectingResultCustomerUnionTypeDef",
    "ProspectingResultOutputTypeDef",
    "ProspectingResultTypeDef",
    "ProspectingResultUnionTypeDef",
    "ProspectingTaskSummaryTypeDef",
    "PutSellingSystemSettingsRequestTypeDef",
    "PutSellingSystemSettingsResponseTypeDef",
    "ReceiverTypeDef",
    "RecommendationTypeDef",
    "RejectEngagementInvitationRequestTypeDef",
    "RelatedEntityIdentifiersTypeDef",
    "ResourceSnapshotJobSummaryTypeDef",
    "ResourceSnapshotPayloadTypeDef",
    "ResourceSnapshotSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "SearchCustomerAccountsRequestPaginateTypeDef",
    "SearchCustomerAccountsRequestTypeDef",
    "SearchCustomerAccountsResponseTypeDef",
    "SearchEngagementsRequestPaginateTypeDef",
    "SearchEngagementsRequestTypeDef",
    "SearchEngagementsResponseTypeDef",
    "SearchOpportunitiesRequestPaginateTypeDef",
    "SearchOpportunitiesRequestTypeDef",
    "SearchOpportunitiesResponseTypeDef",
    "SenderContactTypeDef",
    "SoftwareRevenueTypeDef",
    "SolutionBaseTypeDef",
    "SolutionSortTypeDef",
    "SortObjectTypeDef",
    "StartCustomerAccountBulkJobRequestTypeDef",
    "StartCustomerAccountBulkJobResponseTypeDef",
    "StartEngagementByAcceptingInvitationTaskRequestTypeDef",
    "StartEngagementByAcceptingInvitationTaskResponseTypeDef",
    "StartEngagementFromOpportunityTaskRequestTypeDef",
    "StartEngagementFromOpportunityTaskResponseTypeDef",
    "StartOpportunityBulkJobRequestTypeDef",
    "StartOpportunityBulkJobResponseTypeDef",
    "StartOpportunityFromEngagementTaskRequestTypeDef",
    "StartOpportunityFromEngagementTaskResponseTypeDef",
    "StartProspectingFromEngagementTaskRequestTypeDef",
    "StartProspectingFromEngagementTaskResponseTypeDef",
    "StartResourceSnapshotJobRequestTypeDef",
    "StopResourceSnapshotJobRequestTypeDef",
    "SubmitOpportunityRequestTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TargetCloseDateFilterTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateCustomerAccountRequestTypeDef",
    "UpdateCustomerAccountResponseTypeDef",
    "UpdateEngagementContextPayloadTypeDef",
    "UpdateEngagementContextRequestTypeDef",
    "UpdateEngagementContextResponseTypeDef",
    "UpdateLeadContextTypeDef",
    "UpdateOpportunityRequestTypeDef",
    "UpdateOpportunityResponseTypeDef",
)

class AcceptEngagementInvitationRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class AccountCustomerTypeDef(TypedDict):
    CompanyName: str
    Industry: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    CountryCode: NotRequired[CountryCodeType]

class PreferredContactWindowTypeDef(TypedDict):
    Window: NotRequired[ContactWindowType]
    Timezone: NotRequired[str]

class SenderContactTypeDef(TypedDict):
    Email: str
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    BusinessTitle: NotRequired[str]
    Phone: NotRequired[str]

class AccountReceiverTypeDef(TypedDict):
    AwsAccountId: str
    Alias: NotRequired[str]

class AddressSummaryTypeDef(TypedDict):
    City: NotRequired[str]
    PostalCode: NotRequired[str]
    StateOrRegion: NotRequired[str]
    CountryCode: NotRequired[CountryCodeType]

class AddressTypeDef(TypedDict):
    City: NotRequired[str]
    PostalCode: NotRequired[str]
    StateOrRegion: NotRequired[str]
    CountryCode: NotRequired[CountryCodeType]
    StreetAddress: NotRequired[str]

class AggregationRequestTypeDef(TypedDict):
    GroupBy: Sequence[AggregatableFieldType]

class BucketTypeDef(TypedDict):
    Values: list[str]
    Count: int

class AssigneeContactTypeDef(TypedDict):
    Email: str
    FirstName: str
    LastName: str
    BusinessTitle: str
    Phone: NotRequired[str]

class AssociateOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    OpportunityIdentifier: str
    RelatedEntityType: RelatedEntityTypeType
    RelatedEntityIdentifier: str

class AwsEnrichmentCustomerSummaryTypeDef(TypedDict):
    Industry: NotRequired[str]
    AccountPlanningQualification: NotRequired[str]
    EligiblePrograms: NotRequired[list[str]]
    Geo: NotRequired[str]
    Country: NotRequired[str]
    Segment: NotRequired[str]

class AwsEnrichmentCustomerTypeDef(TypedDict):
    AccountName: NotRequired[str]
    Industry: NotRequired[str]
    SubIndustry: NotRequired[str]
    Sector: NotRequired[str]
    Segment: NotRequired[str]
    CompanySize: NotRequired[str]
    Region: NotRequired[str]
    SubRegion: NotRequired[str]
    Geo: NotRequired[str]
    Country: NotRequired[str]
    CustomerAccountPlanningQualification: NotRequired[str]
    EligiblePrograms: NotRequired[list[str]]

class AwsEnrichmentInsightsSummaryTypeDef(TypedDict):
    MarketplaceEngagementScore: NotRequired[str]
    SolutionCategory: NotRequired[str]
    SolutionScore: NotRequired[str]

class AwsEnrichmentInsightsTypeDef(TypedDict):
    MarketplaceEngagementScore: NotRequired[str]
    SolutionCategory: NotRequired[str]
    SolutionScore: NotRequired[str]
    SolutionSubCategory: NotRequired[str]

class ContactTypeDef(TypedDict):
    Email: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    BusinessTitle: NotRequired[str]
    Phone: NotRequired[str]

class OpportunityQualityTypeDef(TypedDict):
    Score: NotRequired[int]
    Trend: NotRequired[str]

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Type": str,
        "Details": str,
        "Attributes": NotRequired[dict[str, str]],
    },
)

class ProfileNextStepsHistoryTypeDef(TypedDict):
    Value: str
    Time: datetime

class ExpectedCustomerSpendTypeDef(TypedDict):
    CurrencyCode: CurrencyCodeType
    Frequency: Literal["Monthly"]
    TargetCompany: str
    Amount: NotRequired[str]
    EstimationUrl: NotRequired[str]

class AwsOpportunityRelatedEntitiesTypeDef(TypedDict):
    AwsProducts: NotRequired[list[str]]
    Solutions: NotRequired[list[str]]
    AwsMarketplaceSolutions: NotRequired[list[str]]
    AwsMarketplaceProducts: NotRequired[list[str]]

class AwsTeamMemberTypeDef(TypedDict):
    Email: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    BusinessTitle: NotRequired[AwsMemberBusinessTitleType]

class AwsProductOptimizationTypeDef(TypedDict):
    Description: str
    SavingsAmount: str

class MonetaryValueTypeDef(TypedDict):
    Amount: str
    CurrencyCode: CurrencyCodeType

class AwsSubmissionTypeDef(TypedDict):
    InvolvementType: SalesInvolvementTypeType
    Visibility: NotRequired[VisibilityType]

class BestOutreachWindowTypeDef(TypedDict):
    Day: DayOfWeekType
    StartTimeUtc: str
    EndTimeUtc: str

class BulkJobResultTypeDef(TypedDict):
    RequestId: str
    Status: BulkRecordStatusType
    ResourceIdentifier: NotRequired[str]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateResourceSnapshotRequestTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: str
    ResourceType: Literal["Opportunity"]
    ResourceIdentifier: str
    ResourceSnapshotTemplateIdentifier: str
    ClientToken: str

TimestampTypeDef = Union[datetime, str]

class CustomerAccountBulkJobFilterTypeDef(TypedDict):
    Identifier: NotRequired[str]
    Status: NotRequired[BulkJobStatusType]

class CustomerAccountBulkJobSummaryTypeDef(TypedDict):
    Arn: str
    Id: str
    Status: BulkJobStatusType
    TotalRecords: int
    ProcessedRecords: int
    SuccessCount: int
    FailureCount: int
    DeletedCount: int
    CreatedAt: datetime
    FileName: NotRequired[str]
    FailureReason: NotRequired[str]
    CompletedAt: NotRequired[datetime]

class CustomerAccountDetailsSummaryTypeDef(TypedDict):
    CompanyName: str

class CustomerAccountSortTypeDef(TypedDict):
    SortBy: SortableFieldType
    SortOrder: SortOrderType

class EngagementCustomerProjectDetailsTypeDef(TypedDict):
    Title: str
    BusinessProblem: str
    TargetCompletionDate: str

class EngagementCustomerTypeDef(TypedDict):
    Industry: IndustryType
    CompanyName: str
    WebsiteUrl: str
    CountryCode: CountryCodeType

class DeleteCustomerAccountRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class DeleteResourceSnapshotJobRequestTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobIdentifier: str

class DisassociateOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    OpportunityIdentifier: str
    RelatedEntityType: RelatedEntityTypeType
    RelatedEntityIdentifier: str

class EngagementGroupSortTypeDef(TypedDict):
    SortBy: EngagementGroupSortNameType
    SortOrder: SortOrderType

class EngagementGroupSummaryTypeDef(TypedDict):
    Id: str
    Arn: NotRequired[str]
    Catalog: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Count: NotRequired[int]
    ReadinessLevel: NotRequired[ReadinessLevelType]
    UpdatedAt: NotRequired[datetime]

class EngagementMemberSummaryTypeDef(TypedDict):
    CompanyName: NotRequired[str]
    WebsiteUrl: NotRequired[str]

class EngagementMemberTypeDef(TypedDict):
    CompanyName: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    AccountId: NotRequired[str]

class EngagementProspectingResultTypeDef(TypedDict):
    EngagementIdentifier: str
    Status: ProspectingTaskStatusType
    EngagementContextId: NotRequired[str]
    ReasonCode: NotRequired[str]
    Message: NotRequired[str]

class EngagementResourceAssociationSummaryTypeDef(TypedDict):
    Catalog: str
    EngagementId: NotRequired[str]
    ResourceType: NotRequired[Literal["Opportunity"]]
    ResourceId: NotRequired[str]
    CreatedBy: NotRequired[str]

class EngagementSearchSortTypeDef(TypedDict):
    SortBy: EngagementSearchSortNameType
    SortOrder: SortOrderType

class EngagementSortTypeDef(TypedDict):
    SortOrder: SortOrderType
    SortBy: Literal["CreatedDate"]

class EngagementSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Title: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    CreatedBy: NotRequired[str]
    MemberCount: NotRequired[int]
    ModifiedAt: NotRequired[datetime]
    ModifiedBy: NotRequired[str]
    ContextTypes: NotRequired[list[EngagementContextTypeType]]

class ExpectedContractDurationTypeDef(TypedDict):
    Term: Literal["Months"]
    Value: str

class GetAwsOpportunitySummaryRequestTypeDef(TypedDict):
    Catalog: str
    RelatedOpportunityIdentifier: str

class GetCustomerAccountBulkJobReportUrlRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    ReportType: NotRequired[BulkReportTypeType]

class GetCustomerAccountBulkJobRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class GetCustomerAccountRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class IssueTypeDef(TypedDict):
    Severity: NotRequired[str]
    Code: NotRequired[str]
    Message: NotRequired[str]

class GetEngagementInvitationRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class GetEngagementRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class GetOpportunityBulkJobReportUrlRequestTypeDef(TypedDict):
    Catalog: str
    JobId: str
    ReportFormat: Literal["CSV"]
    ReportType: NotRequired[BulkReportTypeType]

class GetOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class MarketingOutputTypeDef(TypedDict):
    CampaignName: NotRequired[str]
    Source: NotRequired[MarketingSourceType]
    UseCases: NotRequired[list[str]]
    Channels: NotRequired[list[ChannelType]]
    AwsFundingUsed: NotRequired[AwsFundingUsedType]

class RelatedEntityIdentifiersTypeDef(TypedDict):
    AwsMarketplaceOffers: NotRequired[list[str]]
    AwsMarketplaceOfferSets: NotRequired[list[str]]
    Solutions: NotRequired[list[str]]
    AwsProducts: NotRequired[list[str]]
    AwsMarketplaceSolutions: NotRequired[list[str]]
    AwsMarketplaceProducts: NotRequired[list[str]]

class GetProspectingFromEngagementTaskRequestTypeDef(TypedDict):
    Catalog: str
    TaskIdentifier: str

class GetResourceSnapshotJobRequestTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobIdentifier: str

class GetResourceSnapshotRequestTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: str
    ResourceType: Literal["Opportunity"]
    ResourceIdentifier: str
    ResourceSnapshotTemplateIdentifier: str
    Revision: NotRequired[int]

class GetSellingSystemSettingsRequestTypeDef(TypedDict):
    Catalog: str

class ProspectingInsightsTypeDef(TypedDict):
    MarketplaceEngagementScore: NotRequired[str]
    SolutionScore: NotRequired[str]
    SolutionCategory: NotRequired[str]
    SolutionSubCategory: NotRequired[str]

class ProspectingResultCustomerOutputTypeDef(TypedDict):
    AccountName: NotRequired[str]
    Geo: NotRequired[str]
    Region: NotRequired[str]
    SubRegion: NotRequired[str]
    Country: NotRequired[CountryCodeType]
    Industry: NotRequired[IndustryType]
    SubIndustry: NotRequired[str]
    Segment: NotRequired[str]
    CompanySize: NotRequired[str]
    EligiblePrograms: NotRequired[list[str]]
    PublicProfileSummary: NotRequired[str]

class LeadAddressTypeDef(TypedDict):
    City: NotRequired[str]
    PostalCode: NotRequired[str]
    StateOrRegion: NotRequired[str]
    CountryCode: NotRequired[str]

class LeadContactTypeDef(TypedDict):
    BusinessTitle: str
    Email: str
    FirstName: str
    LastName: str
    Phone: NotRequired[str]

class LeadInvitationCustomerTypeDef(TypedDict):
    CompanyName: str
    Industry: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    CountryCode: NotRequired[str]
    AwsMaturity: NotRequired[str]
    MarketSegment: NotRequired[str]

class LeadInvitationInteractionTypeDef(TypedDict):
    ContactBusinessTitle: str
    SourceType: NotRequired[str]
    SourceId: NotRequired[str]
    SourceName: NotRequired[str]
    Usecase: NotRequired[str]

class LifeCycleForViewTypeDef(TypedDict):
    TargetCloseDate: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    Stage: NotRequired[StageType]
    NextSteps: NotRequired[str]

class NextStepsHistoryOutputTypeDef(TypedDict):
    Value: str
    Time: datetime

class LifeCycleSummaryTypeDef(TypedDict):
    Stage: NotRequired[StageType]
    ClosedLostReason: NotRequired[ClosedLostReasonType]
    NextSteps: NotRequired[str]
    TargetCloseDate: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    ReviewComments: NotRequired[str]
    ReviewStatusReason: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListCustomerAccountBulkJobResultsRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    Status: NotRequired[BulkRecordStatusType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListEngagementByAcceptingInvitationTaskSummaryTypeDef(TypedDict):
    TaskId: NotRequired[str]
    TaskArn: NotRequired[str]
    StartTime: NotRequired[datetime]
    TaskStatus: NotRequired[TaskStatusType]
    Message: NotRequired[str]
    ReasonCode: NotRequired[ReasonCodeType]
    OpportunityId: NotRequired[str]
    ResourceSnapshotJobId: NotRequired[str]
    EngagementInvitationId: NotRequired[str]

class ListTasksSortBaseTypeDef(TypedDict):
    SortOrder: SortOrderType
    SortBy: Literal["StartTime"]

class ListEngagementFromOpportunityTaskSummaryTypeDef(TypedDict):
    TaskId: NotRequired[str]
    TaskArn: NotRequired[str]
    StartTime: NotRequired[datetime]
    TaskStatus: NotRequired[TaskStatusType]
    Message: NotRequired[str]
    ReasonCode: NotRequired[ReasonCodeType]
    OpportunityId: NotRequired[str]
    ResourceSnapshotJobId: NotRequired[str]
    EngagementId: NotRequired[str]
    EngagementInvitationId: NotRequired[str]

class OpportunityEngagementInvitationSortTypeDef(TypedDict):
    SortOrder: SortOrderType
    SortBy: Literal["InvitationDate"]

class ListEngagementMembersRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListEngagementResourceAssociationsRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    EngagementIdentifier: NotRequired[str]
    ResourceType: NotRequired[Literal["Opportunity"]]
    ResourceIdentifier: NotRequired[str]
    CreatedBy: NotRequired[str]

class OpportunitySortTypeDef(TypedDict):
    SortOrder: SortOrderType
    SortBy: OpportunitySortNameType

class TargetCloseDateFilterTypeDef(TypedDict):
    AfterTargetCloseDate: NotRequired[str]
    BeforeTargetCloseDate: NotRequired[str]

class ListOpportunityBulkJobResultsRequestTypeDef(TypedDict):
    Catalog: str
    JobId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Status: NotRequired[BulkRecordStatusType]

class ListOpportunityBulkJobsRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    JobId: NotRequired[str]
    Status: NotRequired[BulkJobStatusType]

class OpportunityBulkJobSummaryTypeDef(TypedDict):
    JobId: str
    Status: BulkJobStatusType
    TotalRecords: int
    ProcessedRecords: int
    SuccessCount: int
    FailureCount: int
    CreatedAt: datetime
    StartedAt: NotRequired[datetime]
    CompletedAt: NotRequired[datetime]
    FailureReason: NotRequired[str]
    FileName: NotRequired[str]
    OperationType: NotRequired[BulkOperationTypeType]

class ListOpportunityFromEngagementTaskSummaryTypeDef(TypedDict):
    TaskId: NotRequired[str]
    TaskArn: NotRequired[str]
    StartTime: NotRequired[datetime]
    TaskStatus: NotRequired[TaskStatusType]
    Message: NotRequired[str]
    ReasonCode: NotRequired[ReasonCodeType]
    OpportunityId: NotRequired[str]
    ResourceSnapshotJobId: NotRequired[str]
    EngagementId: NotRequired[str]
    ContextId: NotRequired[str]

class ProspectingFromEngagementTaskSortTypeDef(TypedDict):
    SortOrder: SortOrderType
    SortBy: ProspectingFromEngagementTaskSortNameType

class ProspectingTaskSummaryTypeDef(TypedDict):
    TaskId: str
    TaskArn: str
    TaskName: str
    StartTime: datetime
    TotalEngagementCount: int
    CompletedEngagementCount: int
    FailedEngagementCount: int
    EndTime: NotRequired[datetime]

class SortObjectTypeDef(TypedDict):
    SortBy: NotRequired[Literal["CreatedDate"]]
    SortOrder: NotRequired[SortOrderType]

class ResourceSnapshotJobSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    EngagementId: NotRequired[str]
    Status: NotRequired[ResourceSnapshotJobStatusType]

class ListResourceSnapshotsRequestTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ResourceType: NotRequired[Literal["Opportunity"]]
    ResourceIdentifier: NotRequired[str]
    ResourceSnapshotTemplateIdentifier: NotRequired[str]
    CreatedBy: NotRequired[str]

class ResourceSnapshotSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Revision: NotRequired[int]
    ResourceType: NotRequired[Literal["Opportunity"]]
    ResourceId: NotRequired[str]
    ResourceSnapshotTemplateName: NotRequired[str]
    CreatedBy: NotRequired[str]

class SolutionSortTypeDef(TypedDict):
    SortOrder: SortOrderType
    SortBy: SolutionSortNameType

class SolutionBaseTypeDef(TypedDict):
    Catalog: str
    Id: str
    Name: str
    Status: SolutionStatusType
    Category: str
    CreatedDate: datetime
    Arn: NotRequired[str]
    AwsMarketplaceSolutionArn: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str

class MarketingTypeDef(TypedDict):
    CampaignName: NotRequired[str]
    Source: NotRequired[MarketingSourceType]
    UseCases: NotRequired[Sequence[str]]
    Channels: NotRequired[Sequence[ChannelType]]
    AwsFundingUsed: NotRequired[AwsFundingUsedType]

class OpportunitySearchAddressTypeDef(TypedDict):
    CountryCode: NotRequired[CountryCodeType]

class OpportunitySearchExpectedCustomerSpendTypeDef(TypedDict):
    CurrencyCode: CurrencyCodeType
    Amount: NotRequired[str]

class OpportunitySearchOpportunityQualityTypeDef(TypedDict):
    Score: NotRequired[int]

class OpportunitySearchLifeCycleTypeDef(TypedDict):
    ReviewStatus: NotRequired[ReviewStatusType]
    Stage: NotRequired[StageType]
    NextSteps: NotRequired[str]
    TargetCloseDate: NotRequired[str]

class OpportunitySearchRelatedEntityIdentifiersTypeDef(TypedDict):
    AwsMarketplaceOffers: NotRequired[list[str]]
    AwsMarketplaceOfferSets: NotRequired[list[str]]
    AwsMarketplaceSolutions: NotRequired[list[str]]
    Solutions: NotRequired[list[str]]

class OpportunitySearchSortTypeDef(TypedDict):
    SortBy: OpportunitySearchSortNameType
    SortOrder: SortOrderType

class OpportunitySearchTeamMemberTypeDef(TypedDict):
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    BusinessTitle: NotRequired[str]

class ProspectingResultCustomerTypeDef(TypedDict):
    AccountName: NotRequired[str]
    Geo: NotRequired[str]
    Region: NotRequired[str]
    SubRegion: NotRequired[str]
    Country: NotRequired[CountryCodeType]
    Industry: NotRequired[IndustryType]
    SubIndustry: NotRequired[str]
    Segment: NotRequired[str]
    CompanySize: NotRequired[str]
    EligiblePrograms: NotRequired[Sequence[str]]
    PublicProfileSummary: NotRequired[str]

class PutSellingSystemSettingsRequestTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobRoleIdentifier: NotRequired[str]

class RejectEngagementInvitationRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    RejectionReason: NotRequired[str]

class StartCustomerAccountBulkJobRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    FileUri: str

class StartOpportunityBulkJobRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    FileURI: str
    FileFormat: Literal["CSV"]

class StartProspectingFromEngagementTaskRequestTypeDef(TypedDict):
    Catalog: str
    Identifiers: Sequence[str]
    TaskName: str
    ClientToken: str

class StartResourceSnapshotJobRequestTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobIdentifier: str

class StopResourceSnapshotJobRequestTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobIdentifier: str

class SubmitOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    InvolvementType: SalesInvolvementTypeType
    Visibility: NotRequired[VisibilityType]

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class CustomerAccountContextTypeDef(TypedDict):
    AccountIdentifier: NotRequired[str]
    Customer: NotRequired[AccountCustomerTypeDef]

class AccountPlanningInvitationPayloadOutputTypeDef(TypedDict):
    AccountIdentifier: NotRequired[str]
    Customer: NotRequired[AccountCustomerTypeDef]
    SenderContacts: NotRequired[list[SenderContactTypeDef]]
    PreferredContact: NotRequired[PreferredContactWindowTypeDef]

class AccountPlanningInvitationPayloadTypeDef(TypedDict):
    AccountIdentifier: NotRequired[str]
    Customer: NotRequired[AccountCustomerTypeDef]
    SenderContacts: NotRequired[Sequence[SenderContactTypeDef]]
    PreferredContact: NotRequired[PreferredContactWindowTypeDef]

class ReceiverTypeDef(TypedDict):
    Account: NotRequired[AccountReceiverTypeDef]

class AccountSummaryTypeDef(TypedDict):
    CompanyName: str
    Industry: NotRequired[IndustryType]
    OtherIndustry: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    Address: NotRequired[AddressSummaryTypeDef]

class AccountTypeDef(TypedDict):
    CompanyName: str
    Industry: NotRequired[IndustryType]
    OtherIndustry: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    AwsAccountId: NotRequired[str]
    Address: NotRequired[AddressTypeDef]
    Duns: NotRequired[str]

class CustomerAccountDataTypeDef(TypedDict):
    CompanyName: str
    WebsiteUrl: NotRequired[str]
    Duns: NotRequired[str]
    Address: NotRequired[AddressTypeDef]
    Industry: NotRequired[str]
    OtherIndustry: NotRequired[str]
    Domain: NotRequired[str]
    ParentCompanyName: NotRequired[str]

class AggregationResultTypeDef(TypedDict):
    GroupBy: list[AggregatableFieldType]
    Buckets: list[BucketTypeDef]
    OtherCount: int

class AssignOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    Assignee: AssigneeContactTypeDef

class AwsEnrichmentSummaryTypeDef(TypedDict):
    Customer: NotRequired[AwsEnrichmentCustomerSummaryTypeDef]
    Insights: NotRequired[AwsEnrichmentInsightsSummaryTypeDef]

class AwsEnrichmentTypeDef(TypedDict):
    Customer: NotRequired[AwsEnrichmentCustomerTypeDef]
    Insights: NotRequired[AwsEnrichmentInsightsTypeDef]

class AwsOpportunityCustomerTypeDef(TypedDict):
    Contacts: NotRequired[list[ContactTypeDef]]

class AwsOpportunityLifeCycleTypeDef(TypedDict):
    TargetCloseDate: NotRequired[str]
    ClosedLostReason: NotRequired[AwsClosedLostReasonType]
    Stage: NotRequired[AwsOpportunityStageType]
    NextSteps: NotRequired[str]
    NextStepsHistory: NotRequired[list[ProfileNextStepsHistoryTypeDef]]

class AwsOpportunityProjectTypeDef(TypedDict):
    ExpectedCustomerSpend: NotRequired[list[ExpectedCustomerSpendTypeDef]]
    AwsPartition: NotRequired[Literal["aws-eusc"]]

class ProjectDetailsOutputTypeDef(TypedDict):
    BusinessProblem: str
    Title: str
    TargetCompletionDate: str
    ExpectedCustomerSpend: list[ExpectedCustomerSpendTypeDef]

class ProjectDetailsTypeDef(TypedDict):
    BusinessProblem: str
    Title: str
    TargetCompletionDate: str
    ExpectedCustomerSpend: Sequence[ExpectedCustomerSpendTypeDef]

class AwsProductDetailsTypeDef(TypedDict):
    ProductCode: str
    Categories: list[str]
    Optimizations: list[AwsProductOptimizationTypeDef]
    ServiceCode: NotRequired[str]
    Amount: NotRequired[str]
    OptimizedAmount: NotRequired[str]
    PotentialSavingsAmount: NotRequired[str]

class AwsSoftwareRevenueTypeDef(TypedDict):
    Value: NotRequired[MonetaryValueTypeDef]
    Discount: NotRequired[str]
    EffectiveDate: NotRequired[str]
    ExpirationDate: NotRequired[str]

class SoftwareRevenueTypeDef(TypedDict):
    DeliveryModel: NotRequired[RevenueModelType]
    Value: NotRequired[MonetaryValueTypeDef]
    EffectiveDate: NotRequired[str]
    ExpirationDate: NotRequired[str]

class ChannelRecommendationOutputTypeDef(TypedDict):
    RecommendedChannel: str
    BestOutreachWindows: NotRequired[list[BestOutreachWindowTypeDef]]

class ChannelRecommendationTypeDef(TypedDict):
    RecommendedChannel: str
    BestOutreachWindows: NotRequired[Sequence[BestOutreachWindowTypeDef]]

class CreateResourceSnapshotJobRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    EngagementIdentifier: str
    ResourceType: Literal["Opportunity"]
    ResourceIdentifier: str
    ResourceSnapshotTemplateIdentifier: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartEngagementByAcceptingInvitationTaskRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Identifier: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartEngagementFromOpportunityTaskRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Identifier: str
    AwsSubmission: AwsSubmissionTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]

class StartOpportunityFromEngagementTaskRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Identifier: str
    ContextIdentifier: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class CreateCustomerAccountResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Status: EnrichmentStatusType
    Catalog: str
    PartnerAccountIdentifier: str
    CreatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEngagementContextResponseTypeDef(TypedDict):
    EngagementId: str
    EngagementArn: str
    EngagementLastModifiedAt: datetime
    ContextId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEngagementInvitationResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEngagementResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ModifiedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOpportunityResponseTypeDef(TypedDict):
    Id: str
    PartnerOpportunityIdentifier: str
    LastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourceSnapshotJobResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateResourceSnapshotResponseTypeDef(TypedDict):
    Arn: str
    Revision: int
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetCustomerAccountBulkJobReportUrlResponseTypeDef(TypedDict):
    ReportStatus: BulkReportStatusType
    ReportType: BulkReportTypeType
    Url: str
    ExpiresAt: datetime
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCustomerAccountBulkJobResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Status: BulkJobStatusType
    FileName: str
    TotalRecords: int
    ProcessedRecords: int
    SuccessCount: int
    FailureCount: int
    DeletedCount: int
    FailureReason: str
    CreatedAt: datetime
    CompletedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetOpportunityBulkJobReportUrlResponseTypeDef(TypedDict):
    ReportStatus: BulkReportStatusType
    ReportType: BulkReportTypeType
    ReportFormat: Literal["CSV"]
    Url: str
    ExpiresAt: datetime
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceSnapshotJobResponseTypeDef(TypedDict):
    Catalog: str
    Id: str
    Arn: str
    EngagementId: str
    ResourceType: Literal["Opportunity"]
    ResourceId: str
    ResourceArn: str
    ResourceSnapshotTemplateName: str
    CreatedAt: datetime
    Status: ResourceSnapshotJobStatusType
    LastSuccessfulExecutionDate: datetime
    LastFailure: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSellingSystemSettingsResponseTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobRoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListCustomerAccountBulkJobResultsResponseTypeDef(TypedDict):
    Results: list[BulkJobResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListOpportunityBulkJobResultsResponseTypeDef(TypedDict):
    Results: list[BulkJobResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutSellingSystemSettingsResponseTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobRoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartCustomerAccountBulkJobResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Status: BulkJobStatusType
    CreatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartEngagementByAcceptingInvitationTaskResponseTypeDef(TypedDict):
    TaskId: str
    TaskArn: str
    StartTime: datetime
    TaskStatus: TaskStatusType
    Message: str
    ReasonCode: ReasonCodeType
    OpportunityId: str
    ResourceSnapshotJobId: str
    EngagementInvitationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartEngagementFromOpportunityTaskResponseTypeDef(TypedDict):
    TaskId: str
    TaskArn: str
    StartTime: datetime
    TaskStatus: TaskStatusType
    Message: str
    ReasonCode: ReasonCodeType
    OpportunityId: str
    ResourceSnapshotJobId: str
    EngagementId: str
    EngagementInvitationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartOpportunityBulkJobResponseTypeDef(TypedDict):
    JobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartOpportunityFromEngagementTaskResponseTypeDef(TypedDict):
    TaskId: str
    TaskArn: str
    StartTime: datetime
    TaskStatus: TaskStatusType
    Message: str
    ReasonCode: ReasonCodeType
    OpportunityId: str
    ResourceSnapshotJobId: str
    EngagementId: str
    ContextId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartProspectingFromEngagementTaskResponseTypeDef(TypedDict):
    Identifiers: list[str]
    TaskName: str
    Message: str
    ReasonCode: str
    StartTime: datetime
    TaskId: str
    TaskArn: str
    TaskStatus: ProspectingTaskStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCustomerAccountResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Status: EnrichmentStatusType
    Catalog: str
    PartnerAccountIdentifier: str
    CreatedDate: datetime
    LastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEngagementContextResponseTypeDef(TypedDict):
    EngagementId: str
    EngagementArn: str
    EngagementLastModifiedAt: datetime
    ContextId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateOpportunityResponseTypeDef(TypedDict):
    Id: str
    LastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreatedDateFilterTypeDef(TypedDict):
    AfterCreatedDate: NotRequired[TimestampTypeDef]
    BeforeCreatedDate: NotRequired[TimestampTypeDef]

class EngagementSearchFilterValueTypeDef(TypedDict):
    StringValue: NotRequired[str]
    StringListValue: NotRequired[Sequence[str]]
    LongValue: NotRequired[int]
    DateValue: NotRequired[TimestampTypeDef]

class FilterValueTypeDef(TypedDict):
    StringValue: NotRequired[str]
    StringListValue: NotRequired[Sequence[str]]
    LongValue: NotRequired[int]
    DateValue: NotRequired[TimestampTypeDef]

class LastModifiedDateTypeDef(TypedDict):
    AfterLastModifiedDate: NotRequired[TimestampTypeDef]
    BeforeLastModifiedDate: NotRequired[TimestampTypeDef]

class NextStepsHistoryTypeDef(TypedDict):
    Value: str
    Time: TimestampTypeDef

class OpportunitySearchFilterValueTypeDef(TypedDict):
    StringValue: NotRequired[str]
    StringListValue: NotRequired[Sequence[str]]
    LongValue: NotRequired[int]
    DoubleValue: NotRequired[float]
    DateValue: NotRequired[TimestampTypeDef]

class ListCustomerAccountBulkJobsRequestTypeDef(TypedDict):
    Catalog: str
    Filter: NotRequired[CustomerAccountBulkJobFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCustomerAccountBulkJobsResponseTypeDef(TypedDict):
    items: list[CustomerAccountBulkJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CustomerProjectsContextTypeDef(TypedDict):
    Customer: NotRequired[EngagementCustomerTypeDef]
    Project: NotRequired[EngagementCustomerProjectDetailsTypeDef]

class ListEngagementGroupsRequestTypeDef(TypedDict):
    Catalog: str
    ReadinessLevel: NotRequired[ReadinessLevelType]
    Sort: NotRequired[EngagementGroupSortTypeDef]
    EngagementGroupIdentifiers: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListEngagementGroupsResponseTypeDef(TypedDict):
    EngagementGroupSummaries: list[EngagementGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEngagementMembersResponseTypeDef(TypedDict):
    EngagementMemberList: list[EngagementMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetProspectingFromEngagementTaskResponseTypeDef(TypedDict):
    TaskId: str
    TaskArn: str
    TaskName: str
    StartTime: datetime
    EndTime: datetime
    Engagements: list[EngagementProspectingResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListEngagementResourceAssociationsResponseTypeDef(TypedDict):
    EngagementResourceAssociationSummaries: list[EngagementResourceAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEngagementsRequestTypeDef(TypedDict):
    Catalog: str
    CreatedBy: NotRequired[Sequence[str]]
    ExcludeCreatedBy: NotRequired[Sequence[str]]
    ContextTypes: NotRequired[Sequence[EngagementContextTypeType]]
    ExcludeContextTypes: NotRequired[Sequence[EngagementContextTypeType]]
    Sort: NotRequired[EngagementSortTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    EngagementIdentifier: NotRequired[Sequence[str]]

class ListEngagementsResponseTypeDef(TypedDict):
    EngagementSummaryList: list[EngagementSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ProjectOutputTypeDef(TypedDict):
    DeliveryModels: NotRequired[list[DeliveryModelType]]
    ExpectedCustomerSpend: NotRequired[list[ExpectedCustomerSpendTypeDef]]
    ExpectedContractDuration: NotRequired[ExpectedContractDurationTypeDef]
    Title: NotRequired[str]
    ApnPrograms: NotRequired[list[str]]
    CustomerBusinessProblem: NotRequired[str]
    CustomerUseCase: NotRequired[str]
    RelatedOpportunityIdentifier: NotRequired[str]
    SalesActivities: NotRequired[list[SalesActivityType]]
    CompetitorName: NotRequired[CompetitorNameType]
    OtherCompetitorNames: NotRequired[str]
    OtherSolutionDescription: NotRequired[str]
    AdditionalComments: NotRequired[str]
    AwsPartition: NotRequired[Literal["aws-eusc"]]

class ProjectSummaryTypeDef(TypedDict):
    DeliveryModels: NotRequired[list[DeliveryModelType]]
    ExpectedCustomerSpend: NotRequired[list[ExpectedCustomerSpendTypeDef]]
    ExpectedContractDuration: NotRequired[ExpectedContractDurationTypeDef]

class ProjectTypeDef(TypedDict):
    DeliveryModels: NotRequired[Sequence[DeliveryModelType]]
    ExpectedCustomerSpend: NotRequired[Sequence[ExpectedCustomerSpendTypeDef]]
    ExpectedContractDuration: NotRequired[ExpectedContractDurationTypeDef]
    Title: NotRequired[str]
    ApnPrograms: NotRequired[Sequence[str]]
    CustomerBusinessProblem: NotRequired[str]
    CustomerUseCase: NotRequired[str]
    RelatedOpportunityIdentifier: NotRequired[str]
    SalesActivities: NotRequired[Sequence[SalesActivityType]]
    CompetitorName: NotRequired[CompetitorNameType]
    OtherCompetitorNames: NotRequired[str]
    OtherSolutionDescription: NotRequired[str]
    AdditionalComments: NotRequired[str]
    AwsPartition: NotRequired[Literal["aws-eusc"]]

class ProjectViewTypeDef(TypedDict):
    DeliveryModels: NotRequired[list[DeliveryModelType]]
    ExpectedCustomerSpend: NotRequired[list[ExpectedCustomerSpendTypeDef]]
    ExpectedContractDuration: NotRequired[ExpectedContractDurationTypeDef]
    CustomerUseCase: NotRequired[str]
    SalesActivities: NotRequired[list[SalesActivityType]]
    OtherSolutionDescription: NotRequired[str]

class InvitationProspectingResultAwsTypeDef(TypedDict):
    Customer: NotRequired[ProspectingResultCustomerOutputTypeDef]
    Insights: NotRequired[ProspectingInsightsTypeDef]

class ProspectingResultAwsOutputTypeDef(TypedDict):
    Customer: NotRequired[ProspectingResultCustomerOutputTypeDef]
    Insights: NotRequired[ProspectingInsightsTypeDef]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    TaskId: NotRequired[str]
    TaskArn: NotRequired[str]
    TaskName: NotRequired[str]

class LeadCustomerTypeDef(TypedDict):
    CompanyName: str
    Industry: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    Address: NotRequired[LeadAddressTypeDef]
    AwsMaturity: NotRequired[str]
    MarketSegment: NotRequired[str]

class LeadInteractionOutputTypeDef(TypedDict):
    Contact: LeadContactTypeDef
    SourceType: NotRequired[str]
    SourceId: NotRequired[str]
    SourceName: NotRequired[str]
    Usecase: NotRequired[str]
    InteractionDate: NotRequired[datetime]
    CustomerAction: NotRequired[str]
    BusinessProblem: NotRequired[str]

class LeadInteractionTypeDef(TypedDict):
    Contact: LeadContactTypeDef
    SourceType: NotRequired[str]
    SourceId: NotRequired[str]
    SourceName: NotRequired[str]
    Usecase: NotRequired[str]
    InteractionDate: NotRequired[TimestampTypeDef]
    CustomerAction: NotRequired[str]
    BusinessProblem: NotRequired[str]

class LeadInvitationPayloadTypeDef(TypedDict):
    Customer: LeadInvitationCustomerTypeDef
    Interaction: LeadInvitationInteractionTypeDef

class LifeCycleOutputTypeDef(TypedDict):
    Stage: NotRequired[StageType]
    ClosedLostReason: NotRequired[ClosedLostReasonType]
    NextSteps: NotRequired[str]
    TargetCloseDate: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    ReviewComments: NotRequired[str]
    ReviewStatusReason: NotRequired[str]
    NextStepsHistory: NotRequired[list[NextStepsHistoryOutputTypeDef]]

class ListCustomerAccountBulkJobResultsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    Status: NotRequired[BulkRecordStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomerAccountBulkJobsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Filter: NotRequired[CustomerAccountBulkJobFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementGroupsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    ReadinessLevel: NotRequired[ReadinessLevelType]
    Sort: NotRequired[EngagementGroupSortTypeDef]
    EngagementGroupIdentifiers: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementMembersRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementResourceAssociationsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: NotRequired[str]
    ResourceType: NotRequired[Literal["Opportunity"]]
    ResourceIdentifier: NotRequired[str]
    CreatedBy: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    CreatedBy: NotRequired[Sequence[str]]
    ExcludeCreatedBy: NotRequired[Sequence[str]]
    ContextTypes: NotRequired[Sequence[EngagementContextTypeType]]
    ExcludeContextTypes: NotRequired[Sequence[EngagementContextTypeType]]
    Sort: NotRequired[EngagementSortTypeDef]
    EngagementIdentifier: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOpportunityBulkJobResultsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    JobId: str
    Status: NotRequired[BulkRecordStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOpportunityBulkJobsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    JobId: NotRequired[str]
    Status: NotRequired[BulkJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceSnapshotsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: str
    ResourceType: NotRequired[Literal["Opportunity"]]
    ResourceIdentifier: NotRequired[str]
    ResourceSnapshotTemplateIdentifier: NotRequired[str]
    CreatedBy: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementByAcceptingInvitationTasksResponseTypeDef(TypedDict):
    TaskSummaries: list[ListEngagementByAcceptingInvitationTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEngagementByAcceptingInvitationTasksRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementInvitationIdentifier: NotRequired[Sequence[str]]
    TaskIdentifier: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementByAcceptingInvitationTasksRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementInvitationIdentifier: NotRequired[Sequence[str]]
    TaskIdentifier: NotRequired[Sequence[str]]

class ListEngagementFromOpportunityTasksRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    TaskIdentifier: NotRequired[Sequence[str]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementIdentifier: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementFromOpportunityTasksRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    TaskIdentifier: NotRequired[Sequence[str]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementIdentifier: NotRequired[Sequence[str]]

class ListOpportunityFromEngagementTasksRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    TaskIdentifier: NotRequired[Sequence[str]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementIdentifier: NotRequired[Sequence[str]]
    ContextIdentifier: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOpportunityFromEngagementTasksRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    TaskIdentifier: NotRequired[Sequence[str]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementIdentifier: NotRequired[Sequence[str]]
    ContextIdentifier: NotRequired[Sequence[str]]

class ListEngagementFromOpportunityTasksResponseTypeDef(TypedDict):
    TaskSummaries: list[ListEngagementFromOpportunityTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEngagementInvitationsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    ParticipantType: ParticipantTypeType
    Sort: NotRequired[OpportunityEngagementInvitationSortTypeDef]
    PayloadType: NotRequired[Sequence[EngagementInvitationPayloadTypeType]]
    Status: NotRequired[Sequence[InvitationStatusType]]
    EngagementIdentifier: NotRequired[Sequence[str]]
    SenderAwsAccountId: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementInvitationsRequestTypeDef(TypedDict):
    Catalog: str
    ParticipantType: ParticipantTypeType
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[OpportunityEngagementInvitationSortTypeDef]
    PayloadType: NotRequired[Sequence[EngagementInvitationPayloadTypeType]]
    Status: NotRequired[Sequence[InvitationStatusType]]
    EngagementIdentifier: NotRequired[Sequence[str]]
    SenderAwsAccountId: NotRequired[Sequence[str]]

class ListOpportunityBulkJobsResponseTypeDef(TypedDict):
    OpportunityBulkJobSummaries: list[OpportunityBulkJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListOpportunityFromEngagementTasksResponseTypeDef(TypedDict):
    TaskSummaries: list[ListOpportunityFromEngagementTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListProspectingFromEngagementTasksRequestPaginateTypeDef(TypedDict):
    Catalog: str
    TaskIdentifier: NotRequired[Sequence[str]]
    TaskName: NotRequired[Sequence[str]]
    StartAfter: NotRequired[TimestampTypeDef]
    StartBefore: NotRequired[TimestampTypeDef]
    Sort: NotRequired[ProspectingFromEngagementTaskSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProspectingFromEngagementTasksRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    TaskIdentifier: NotRequired[Sequence[str]]
    TaskName: NotRequired[Sequence[str]]
    StartAfter: NotRequired[TimestampTypeDef]
    StartBefore: NotRequired[TimestampTypeDef]
    Sort: NotRequired[ProspectingFromEngagementTaskSortTypeDef]

class ListProspectingFromEngagementTasksResponseTypeDef(TypedDict):
    TaskSummaries: list[ProspectingTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListResourceSnapshotJobsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: NotRequired[str]
    Status: NotRequired[ResourceSnapshotJobStatusType]
    Sort: NotRequired[SortObjectTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceSnapshotJobsRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    EngagementIdentifier: NotRequired[str]
    Status: NotRequired[ResourceSnapshotJobStatusType]
    Sort: NotRequired[SortObjectTypeDef]

class ListResourceSnapshotJobsResponseTypeDef(TypedDict):
    ResourceSnapshotJobSummaries: list[ResourceSnapshotJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListResourceSnapshotsResponseTypeDef(TypedDict):
    ResourceSnapshotSummaries: list[ResourceSnapshotSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSolutionsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[SolutionSortTypeDef]
    Status: NotRequired[Sequence[SolutionStatusType]]
    Identifier: NotRequired[Sequence[str]]
    Category: NotRequired[Sequence[str]]
    AwsMarketplaceSolutionArn: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSolutionsRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[SolutionSortTypeDef]
    Status: NotRequired[Sequence[SolutionStatusType]]
    Identifier: NotRequired[Sequence[str]]
    Category: NotRequired[Sequence[str]]
    AwsMarketplaceSolutionArn: NotRequired[Sequence[str]]

class ListSolutionsResponseTypeDef(TypedDict):
    SolutionSummaries: list[SolutionBaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

MarketingUnionTypeDef = Union[MarketingTypeDef, MarketingOutputTypeDef]

class OpportunitySearchAccountTypeDef(TypedDict):
    CompanyName: NotRequired[str]
    Industry: NotRequired[IndustryType]
    AwsAccountId: NotRequired[str]
    Address: NotRequired[OpportunitySearchAddressTypeDef]

class OpportunitySearchProjectTypeDef(TypedDict):
    Title: NotRequired[str]
    ApnPrograms: NotRequired[list[str]]
    ExpectedCustomerSpend: NotRequired[list[OpportunitySearchExpectedCustomerSpendTypeDef]]

class OpportunitySearchInsightsTypeDef(TypedDict):
    EngagementScore: NotRequired[SearchEngagementScoreType]
    OpportunityQuality: NotRequired[OpportunitySearchOpportunityQualityTypeDef]

ProspectingResultCustomerUnionTypeDef = Union[
    ProspectingResultCustomerTypeDef, ProspectingResultCustomerOutputTypeDef
]
AccountPlanningInvitationPayloadUnionTypeDef = Union[
    AccountPlanningInvitationPayloadTypeDef, AccountPlanningInvitationPayloadOutputTypeDef
]

class EngagementInvitationSummaryTypeDef(TypedDict):
    Id: str
    Catalog: str
    Arn: NotRequired[str]
    PayloadType: NotRequired[EngagementInvitationPayloadTypeType]
    EngagementId: NotRequired[str]
    EngagementTitle: NotRequired[str]
    Status: NotRequired[InvitationStatusType]
    InvitationDate: NotRequired[datetime]
    ExpirationDate: NotRequired[datetime]
    SenderAwsAccountId: NotRequired[str]
    SenderCompanyName: NotRequired[str]
    Receiver: NotRequired[ReceiverTypeDef]
    ParticipantType: NotRequired[ParticipantTypeType]

class CustomerSummaryTypeDef(TypedDict):
    Account: NotRequired[AccountSummaryTypeDef]

class CustomerOutputTypeDef(TypedDict):
    Account: NotRequired[AccountTypeDef]
    Contacts: NotRequired[list[ContactTypeDef]]

class CustomerTypeDef(TypedDict):
    Account: NotRequired[AccountTypeDef]
    Contacts: NotRequired[Sequence[ContactTypeDef]]

class CreateCustomerAccountRequestTypeDef(TypedDict):
    Catalog: str
    Account: CustomerAccountDataTypeDef
    PartnerAccountIdentifier: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]

class UpdateCustomerAccountRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    Account: CustomerAccountDataTypeDef
    LastModifiedDate: TimestampTypeDef
    PartnerAccountIdentifier: NotRequired[str]

class GetCustomerAccountStatisticsResponseTypeDef(TypedDict):
    TotalCount: int
    Aggregations: list[AggregationResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CustomerAccountSummaryTypeDef(TypedDict):
    Arn: str
    Id: str
    Catalog: str
    EnrichmentStatus: EnrichmentStatusType
    CreatedDate: datetime
    LastModifiedDate: datetime
    CustomerAccount: CustomerAccountDetailsSummaryTypeDef
    PartnerAccountIdentifier: NotRequired[str]
    AwsEnrichment: NotRequired[AwsEnrichmentSummaryTypeDef]

class GetCustomerAccountResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Catalog: str
    EnrichmentStatus: EnrichmentStatusType
    PartnerAccountIdentifier: str
    CreatedDate: datetime
    LastModifiedDate: datetime
    Issues: list[IssueTypeDef]
    AwsEnrichment: AwsEnrichmentTypeDef
    ReasonCode: CustomerAccountFailureReasonType
    Message: str
    ExistingCustomerAccountArn: str
    Account: CustomerAccountDataTypeDef
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class OpportunityInvitationPayloadOutputTypeDef(TypedDict):
    ReceiverResponsibilities: list[ReceiverResponsibilityType]
    Customer: EngagementCustomerTypeDef
    Project: ProjectDetailsOutputTypeDef
    SenderContacts: NotRequired[list[SenderContactTypeDef]]
    OpportunityType: NotRequired[OpportunityTypeType]

ProjectDetailsUnionTypeDef = Union[ProjectDetailsTypeDef, ProjectDetailsOutputTypeDef]

class AwsProductInsightsTypeDef(TypedDict):
    CurrencyCode: CurrencyCodeType
    Frequency: Literal["Monthly"]
    TotalAmountByCategory: dict[str, str]
    AwsProducts: list[AwsProductDetailsTypeDef]
    TotalAmount: NotRequired[str]
    TotalOptimizedAmount: NotRequired[str]
    TotalPotentialSavingsAmount: NotRequired[str]

class LeadInsightsOutputTypeDef(TypedDict):
    LeadReadinessScore: NotRequired[str]
    ChannelRecommendation: NotRequired[ChannelRecommendationOutputTypeDef]

ChannelRecommendationUnionTypeDef = Union[
    ChannelRecommendationTypeDef, ChannelRecommendationOutputTypeDef
]

class EngagementSearchPredicateTypeDef(TypedDict):
    Key: EngagementSearchFilterNameType
    Value: EngagementSearchFilterValueTypeDef

class FilterConditionTypeDef(TypedDict):
    Key: FilterableFieldType
    Value: FilterValueTypeDef

class ListOpportunitiesRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[OpportunitySortTypeDef]
    LastModifiedDate: NotRequired[LastModifiedDateTypeDef]
    Identifier: NotRequired[Sequence[str]]
    LifeCycleStage: NotRequired[Sequence[StageType]]
    LifeCycleReviewStatus: NotRequired[Sequence[ReviewStatusType]]
    CustomerCompanyName: NotRequired[Sequence[str]]
    CreatedDate: NotRequired[CreatedDateFilterTypeDef]
    TargetCloseDate: NotRequired[TargetCloseDateFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOpportunitiesRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[OpportunitySortTypeDef]
    LastModifiedDate: NotRequired[LastModifiedDateTypeDef]
    Identifier: NotRequired[Sequence[str]]
    LifeCycleStage: NotRequired[Sequence[StageType]]
    LifeCycleReviewStatus: NotRequired[Sequence[ReviewStatusType]]
    CustomerCompanyName: NotRequired[Sequence[str]]
    CreatedDate: NotRequired[CreatedDateFilterTypeDef]
    TargetCloseDate: NotRequired[TargetCloseDateFilterTypeDef]

class LifeCycleTypeDef(TypedDict):
    Stage: NotRequired[StageType]
    ClosedLostReason: NotRequired[ClosedLostReasonType]
    NextSteps: NotRequired[str]
    TargetCloseDate: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    ReviewComments: NotRequired[str]
    ReviewStatusReason: NotRequired[str]
    NextStepsHistory: NotRequired[Sequence[NextStepsHistoryTypeDef]]

class OpportunitySearchPredicateTypeDef(TypedDict):
    Key: OpportunitySearchFilterNameType
    Value: OpportunitySearchFilterValueTypeDef

ProjectUnionTypeDef = Union[ProjectTypeDef, ProjectOutputTypeDef]

class ProspectingResultOutputTypeDef(TypedDict):
    Aws: NotRequired[ProspectingResultAwsOutputTypeDef]

LeadInteractionUnionTypeDef = Union[LeadInteractionTypeDef, LeadInteractionOutputTypeDef]

class OpportunitySearchCustomerTypeDef(TypedDict):
    Account: NotRequired[OpportunitySearchAccountTypeDef]

class OpportunitySearchAwsSummaryTypeDef(TypedDict):
    Origin: NotRequired[OpportunityOriginType]
    CosellMotion: NotRequired[str]
    Insights: NotRequired[OpportunitySearchInsightsTypeDef]

class ProspectingResultAwsTypeDef(TypedDict):
    Customer: NotRequired[ProspectingResultCustomerUnionTypeDef]
    Insights: NotRequired[ProspectingInsightsTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    TaskId: NotRequired[str]
    TaskArn: NotRequired[str]
    TaskName: NotRequired[str]

class ListEngagementInvitationsResponseTypeDef(TypedDict):
    EngagementInvitationSummaries: list[EngagementInvitationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class OpportunitySummaryTypeDef(TypedDict):
    Catalog: str
    Id: NotRequired[str]
    Arn: NotRequired[str]
    PartnerOpportunityIdentifier: NotRequired[str]
    OpportunityType: NotRequired[OpportunityTypeType]
    LastModifiedDate: NotRequired[datetime]
    CreatedDate: NotRequired[datetime]
    LifeCycle: NotRequired[LifeCycleSummaryTypeDef]
    Customer: NotRequired[CustomerSummaryTypeDef]
    Project: NotRequired[ProjectSummaryTypeDef]

class GetOpportunityResponseTypeDef(TypedDict):
    Catalog: str
    PrimaryNeedsFromAws: list[PrimaryNeedFromAwsType]
    NationalSecurity: NationalSecurityType
    PartnerOpportunityIdentifier: str
    Customer: CustomerOutputTypeDef
    Project: ProjectOutputTypeDef
    OpportunityType: OpportunityTypeType
    Marketing: MarketingOutputTypeDef
    SoftwareRevenue: SoftwareRevenueTypeDef
    Id: str
    Arn: str
    LastModifiedDate: datetime
    CreatedDate: datetime
    RelatedEntityIdentifiers: RelatedEntityIdentifiersTypeDef
    LifeCycle: LifeCycleOutputTypeDef
    OpportunityTeam: list[ContactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class OpportunitySummaryViewTypeDef(TypedDict):
    OpportunityType: NotRequired[OpportunityTypeType]
    Lifecycle: NotRequired[LifeCycleForViewTypeDef]
    OpportunityTeam: NotRequired[list[ContactTypeDef]]
    PrimaryNeedsFromAws: NotRequired[list[PrimaryNeedFromAwsType]]
    Customer: NotRequired[CustomerOutputTypeDef]
    Project: NotRequired[ProjectViewTypeDef]
    RelatedEntityIdentifiers: NotRequired[RelatedEntityIdentifiersTypeDef]

CustomerUnionTypeDef = Union[CustomerTypeDef, CustomerOutputTypeDef]

class SearchCustomerAccountsResponseTypeDef(TypedDict):
    CustomerAccountSummaries: list[CustomerAccountSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PayloadOutputTypeDef(TypedDict):
    OpportunityInvitation: NotRequired[OpportunityInvitationPayloadOutputTypeDef]
    LeadInvitation: NotRequired[LeadInvitationPayloadTypeDef]
    AccountPlanningInvitation: NotRequired[AccountPlanningInvitationPayloadOutputTypeDef]

class OpportunityInvitationPayloadTypeDef(TypedDict):
    ReceiverResponsibilities: Sequence[ReceiverResponsibilityType]
    Customer: EngagementCustomerTypeDef
    Project: ProjectDetailsUnionTypeDef
    SenderContacts: NotRequired[Sequence[SenderContactTypeDef]]
    OpportunityType: NotRequired[OpportunityTypeType]

class AwsProductsSpendInsightsBySourceTypeDef(TypedDict):
    Partner: NotRequired[AwsProductInsightsTypeDef]
    AWS: NotRequired[AwsProductInsightsTypeDef]

class EnrichmentContextTypeDef(TypedDict):
    ProspectingResultAws: NotRequired[InvitationProspectingResultAwsTypeDef]
    LeadInsights: NotRequired[LeadInsightsOutputTypeDef]

class LeadContextOutputTypeDef(TypedDict):
    Customer: LeadCustomerTypeDef
    Interactions: list[LeadInteractionOutputTypeDef]
    Insights: NotRequired[LeadInsightsOutputTypeDef]
    QualificationStatus: NotRequired[str]

class LeadInsightsTypeDef(TypedDict):
    LeadReadinessScore: NotRequired[str]
    ChannelRecommendation: NotRequired[ChannelRecommendationUnionTypeDef]

class EngagementSearchFilterPaginatorTypeDef(TypedDict):
    AndAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    OrAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    NotFilter: NotRequired[Mapping[str, Any]]
    EqualsTo: NotRequired[EngagementSearchPredicateTypeDef]
    ContainsAny: NotRequired[EngagementSearchPredicateTypeDef]
    ContainsAll: NotRequired[EngagementSearchPredicateTypeDef]
    GreaterThan: NotRequired[EngagementSearchPredicateTypeDef]
    GreaterThanOrEquals: NotRequired[EngagementSearchPredicateTypeDef]
    LessThan: NotRequired[EngagementSearchPredicateTypeDef]
    LessThanOrEquals: NotRequired[EngagementSearchPredicateTypeDef]

class EngagementSearchFilterTypeDef(TypedDict):
    AndAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    OrAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    NotFilter: NotRequired[Mapping[str, Any]]
    EqualsTo: NotRequired[EngagementSearchPredicateTypeDef]
    ContainsAny: NotRequired[EngagementSearchPredicateTypeDef]
    ContainsAll: NotRequired[EngagementSearchPredicateTypeDef]
    GreaterThan: NotRequired[EngagementSearchPredicateTypeDef]
    GreaterThanOrEquals: NotRequired[EngagementSearchPredicateTypeDef]
    LessThan: NotRequired[EngagementSearchPredicateTypeDef]
    LessThanOrEquals: NotRequired[EngagementSearchPredicateTypeDef]

class FilterPaginatorTypeDef(TypedDict):
    AndAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    OrAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    NotFilter: NotRequired[Mapping[str, Any]]
    EqualsTo: NotRequired[FilterConditionTypeDef]
    ContainsAny: NotRequired[FilterConditionTypeDef]
    ContainsAll: NotRequired[FilterConditionTypeDef]
    GreaterThan: NotRequired[FilterConditionTypeDef]
    GreaterThanOrEquals: NotRequired[FilterConditionTypeDef]
    LessThan: NotRequired[FilterConditionTypeDef]
    LessThanOrEquals: NotRequired[FilterConditionTypeDef]

class FilterTypeDef(TypedDict):
    AndAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    OrAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    NotFilter: NotRequired[Mapping[str, Any]]
    EqualsTo: NotRequired[FilterConditionTypeDef]
    ContainsAny: NotRequired[FilterConditionTypeDef]
    ContainsAll: NotRequired[FilterConditionTypeDef]
    GreaterThan: NotRequired[FilterConditionTypeDef]
    GreaterThanOrEquals: NotRequired[FilterConditionTypeDef]
    LessThan: NotRequired[FilterConditionTypeDef]
    LessThanOrEquals: NotRequired[FilterConditionTypeDef]

LifeCycleUnionTypeDef = Union[LifeCycleTypeDef, LifeCycleOutputTypeDef]

class OpportunitySearchFilterPaginatorTypeDef(TypedDict):
    AndAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    OrAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    NotFilter: NotRequired[Mapping[str, Any]]
    EqualsTo: NotRequired[OpportunitySearchPredicateTypeDef]
    ContainsAny: NotRequired[OpportunitySearchPredicateTypeDef]
    ContainsAll: NotRequired[OpportunitySearchPredicateTypeDef]
    GreaterThan: NotRequired[OpportunitySearchPredicateTypeDef]
    GreaterThanOrEquals: NotRequired[OpportunitySearchPredicateTypeDef]
    LessThan: NotRequired[OpportunitySearchPredicateTypeDef]
    LessThanOrEquals: NotRequired[OpportunitySearchPredicateTypeDef]

class OpportunitySearchFilterTypeDef(TypedDict):
    AndAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    OrAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    NotFilter: NotRequired[Mapping[str, Any]]
    EqualsTo: NotRequired[OpportunitySearchPredicateTypeDef]
    ContainsAny: NotRequired[OpportunitySearchPredicateTypeDef]
    ContainsAll: NotRequired[OpportunitySearchPredicateTypeDef]
    GreaterThan: NotRequired[OpportunitySearchPredicateTypeDef]
    GreaterThanOrEquals: NotRequired[OpportunitySearchPredicateTypeDef]
    LessThan: NotRequired[OpportunitySearchPredicateTypeDef]
    LessThanOrEquals: NotRequired[OpportunitySearchPredicateTypeDef]

class OpportunitySearchSummaryTypeDef(TypedDict):
    Id: str
    LastModifiedDate: datetime
    CreatedDate: datetime
    OpportunityType: NotRequired[OpportunityTypeType]
    PartnerOpportunityIdentifier: NotRequired[str]
    LifeCycle: NotRequired[OpportunitySearchLifeCycleTypeDef]
    Customer: NotRequired[OpportunitySearchCustomerTypeDef]
    Project: NotRequired[OpportunitySearchProjectTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    RelatedEntityIdentifiers: NotRequired[OpportunitySearchRelatedEntityIdentifiersTypeDef]
    OpportunityTeam: NotRequired[list[OpportunitySearchTeamMemberTypeDef]]
    AwsOpportunitySummary: NotRequired[OpportunitySearchAwsSummaryTypeDef]

ProspectingResultAwsUnionTypeDef = Union[
    ProspectingResultAwsTypeDef, ProspectingResultAwsOutputTypeDef
]

class ListOpportunitiesResponseTypeDef(TypedDict):
    OpportunitySummaries: list[OpportunitySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

OpportunityInvitationPayloadUnionTypeDef = Union[
    OpportunityInvitationPayloadTypeDef, OpportunityInvitationPayloadOutputTypeDef
]

class AwsOpportunityInsightsTypeDef(TypedDict):
    NextBestActions: NotRequired[str]
    EngagementScore: NotRequired[EngagementScoreType]
    AwsProductsSpendInsightsBySource: NotRequired[AwsProductsSpendInsightsBySourceTypeDef]
    OpportunityQuality: NotRequired[OpportunityQualityTypeDef]
    Recommendations: NotRequired[list[RecommendationTypeDef]]

class GetEngagementInvitationResponseTypeDef(TypedDict):
    Arn: str
    PayloadType: EngagementInvitationPayloadTypeType
    Id: str
    EngagementId: str
    EngagementTitle: str
    Status: InvitationStatusType
    InvitationDate: datetime
    ExpirationDate: datetime
    SenderAwsAccountId: str
    SenderCompanyName: str
    Receiver: ReceiverTypeDef
    Catalog: str
    RejectionReason: str
    Payload: PayloadOutputTypeDef
    InvitationMessage: str
    EngagementDescription: str
    ExistingMembers: list[EngagementMemberSummaryTypeDef]
    EnrichmentContext: EnrichmentContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EngagementContextPayloadOutputTypeDef(TypedDict):
    CustomerProject: NotRequired[CustomerProjectsContextTypeDef]
    Lead: NotRequired[LeadContextOutputTypeDef]
    ProspectingResult: NotRequired[ProspectingResultOutputTypeDef]
    CustomerAccount: NotRequired[CustomerAccountContextTypeDef]

LeadInsightsUnionTypeDef = Union[LeadInsightsTypeDef, LeadInsightsOutputTypeDef]

class SearchEngagementsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Keyword: NotRequired[str]
    Filter: NotRequired[EngagementSearchFilterPaginatorTypeDef]
    GroupId: NotRequired[str]
    Sort: NotRequired[EngagementSearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchEngagementsRequestTypeDef(TypedDict):
    Catalog: str
    Keyword: NotRequired[str]
    Filter: NotRequired[EngagementSearchFilterTypeDef]
    GroupId: NotRequired[str]
    Sort: NotRequired[EngagementSearchSortTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SearchCustomerAccountsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Filter: NotRequired[FilterPaginatorTypeDef]
    Sort: NotRequired[CustomerAccountSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetCustomerAccountStatisticsRequestTypeDef(TypedDict):
    Catalog: str
    Filter: NotRequired[FilterTypeDef]
    Aggregations: NotRequired[Sequence[AggregationRequestTypeDef]]
    IncludeMissing: NotRequired[bool]

class SearchCustomerAccountsRequestTypeDef(TypedDict):
    Catalog: str
    Filter: NotRequired[FilterTypeDef]
    Sort: NotRequired[CustomerAccountSortTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class CreateOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    PrimaryNeedsFromAws: NotRequired[Sequence[PrimaryNeedFromAwsType]]
    NationalSecurity: NotRequired[NationalSecurityType]
    PartnerOpportunityIdentifier: NotRequired[str]
    Customer: NotRequired[CustomerUnionTypeDef]
    Project: NotRequired[ProjectUnionTypeDef]
    OpportunityType: NotRequired[OpportunityTypeType]
    Marketing: NotRequired[MarketingUnionTypeDef]
    SoftwareRevenue: NotRequired[SoftwareRevenueTypeDef]
    LifeCycle: NotRequired[LifeCycleUnionTypeDef]
    Origin: NotRequired[OpportunityOriginType]
    OpportunityTeam: NotRequired[Sequence[ContactTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    LastModifiedDate: TimestampTypeDef
    Identifier: str
    PrimaryNeedsFromAws: NotRequired[Sequence[PrimaryNeedFromAwsType]]
    NationalSecurity: NotRequired[NationalSecurityType]
    PartnerOpportunityIdentifier: NotRequired[str]
    Customer: NotRequired[CustomerUnionTypeDef]
    Project: NotRequired[ProjectUnionTypeDef]
    OpportunityType: NotRequired[OpportunityTypeType]
    Marketing: NotRequired[MarketingUnionTypeDef]
    SoftwareRevenue: NotRequired[SoftwareRevenueTypeDef]
    LifeCycle: NotRequired[LifeCycleUnionTypeDef]

class SearchOpportunitiesRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Keyword: NotRequired[str]
    Filter: NotRequired[OpportunitySearchFilterPaginatorTypeDef]
    Sort: NotRequired[OpportunitySearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchOpportunitiesRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Keyword: NotRequired[str]
    Filter: NotRequired[OpportunitySearchFilterTypeDef]
    Sort: NotRequired[OpportunitySearchSortTypeDef]

class SearchOpportunitiesResponseTypeDef(TypedDict):
    OpportunitySearchSummaries: list[OpportunitySearchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ProspectingResultTypeDef(TypedDict):
    Aws: NotRequired[ProspectingResultAwsUnionTypeDef]

class PayloadTypeDef(TypedDict):
    OpportunityInvitation: NotRequired[OpportunityInvitationPayloadUnionTypeDef]
    LeadInvitation: NotRequired[LeadInvitationPayloadTypeDef]
    AccountPlanningInvitation: NotRequired[AccountPlanningInvitationPayloadUnionTypeDef]

class AwsOpportunitySummaryFullViewTypeDef(TypedDict):
    RelatedOpportunityId: NotRequired[str]
    Origin: NotRequired[OpportunityOriginType]
    InvolvementType: NotRequired[SalesInvolvementTypeType]
    Visibility: NotRequired[VisibilityType]
    LifeCycle: NotRequired[AwsOpportunityLifeCycleTypeDef]
    OpportunityTeam: NotRequired[list[AwsTeamMemberTypeDef]]
    Insights: NotRequired[AwsOpportunityInsightsTypeDef]
    InvolvementTypeChangeReason: NotRequired[InvolvementTypeChangeReasonType]
    RelatedEntityIds: NotRequired[AwsOpportunityRelatedEntitiesTypeDef]
    Customer: NotRequired[AwsOpportunityCustomerTypeDef]
    Project: NotRequired[AwsOpportunityProjectTypeDef]
    CosellMotion: NotRequired[str]
    CosellMotionReason: NotRequired[str]
    SoftwareRevenue: NotRequired[AwsSoftwareRevenueTypeDef]

class GetAwsOpportunitySummaryResponseTypeDef(TypedDict):
    RelatedOpportunityId: str
    Origin: OpportunityOriginType
    InvolvementType: SalesInvolvementTypeType
    Visibility: VisibilityType
    LifeCycle: AwsOpportunityLifeCycleTypeDef
    OpportunityTeam: list[AwsTeamMemberTypeDef]
    Insights: AwsOpportunityInsightsTypeDef
    InvolvementTypeChangeReason: InvolvementTypeChangeReasonType
    RelatedEntityIds: AwsOpportunityRelatedEntitiesTypeDef
    Customer: AwsOpportunityCustomerTypeDef
    Project: AwsOpportunityProjectTypeDef
    CosellMotion: str
    CosellMotionReason: str
    SoftwareRevenue: AwsSoftwareRevenueTypeDef
    Catalog: str
    ResponseMetadata: ResponseMetadataTypeDef

EngagementContextDetailsOutputTypeDef = TypedDict(
    "EngagementContextDetailsOutputTypeDef",
    {
        "Type": EngagementContextTypeType,
        "Id": NotRequired[str],
        "Payload": NotRequired[EngagementContextPayloadOutputTypeDef],
    },
)

class LeadContextTypeDef(TypedDict):
    Customer: LeadCustomerTypeDef
    Interactions: Sequence[LeadInteractionUnionTypeDef]
    Insights: NotRequired[LeadInsightsUnionTypeDef]
    QualificationStatus: NotRequired[str]

class UpdateLeadContextTypeDef(TypedDict):
    Customer: LeadCustomerTypeDef
    QualificationStatus: NotRequired[str]
    Interaction: NotRequired[LeadInteractionUnionTypeDef]
    Insights: NotRequired[LeadInsightsUnionTypeDef]

ProspectingResultUnionTypeDef = Union[ProspectingResultTypeDef, ProspectingResultOutputTypeDef]
PayloadUnionTypeDef = Union[PayloadTypeDef, PayloadOutputTypeDef]

class ResourceSnapshotPayloadTypeDef(TypedDict):
    OpportunitySummary: NotRequired[OpportunitySummaryViewTypeDef]
    AwsOpportunitySummaryFullView: NotRequired[AwsOpportunitySummaryFullViewTypeDef]

class EngagementSearchSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Title: NotRequired[str]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    CreatedBy: NotRequired[str]
    MemberCount: NotRequired[int]
    ModifiedAt: NotRequired[datetime]
    ModifiedBy: NotRequired[str]
    Contexts: NotRequired[list[EngagementContextDetailsOutputTypeDef]]

class GetEngagementResponseTypeDef(TypedDict):
    Id: str
    Arn: str
    Title: str
    Description: str
    CreatedAt: datetime
    CreatedBy: str
    MemberCount: int
    ModifiedAt: datetime
    ModifiedBy: str
    Contexts: list[EngagementContextDetailsOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

LeadContextUnionTypeDef = Union[LeadContextTypeDef, LeadContextOutputTypeDef]

class UpdateEngagementContextPayloadTypeDef(TypedDict):
    Lead: NotRequired[UpdateLeadContextTypeDef]
    CustomerProject: NotRequired[CustomerProjectsContextTypeDef]
    ProspectingResult: NotRequired[ProspectingResultUnionTypeDef]

class InvitationTypeDef(TypedDict):
    Message: str
    Receiver: ReceiverTypeDef
    Payload: PayloadUnionTypeDef

class GetResourceSnapshotResponseTypeDef(TypedDict):
    Catalog: str
    Arn: str
    CreatedBy: str
    CreatedAt: datetime
    EngagementId: str
    ResourceType: Literal["Opportunity"]
    ResourceId: str
    ResourceSnapshotTemplateName: str
    Revision: int
    Payload: ResourceSnapshotPayloadTypeDef
    TargetMemberAccounts: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class SearchEngagementsResponseTypeDef(TypedDict):
    EngagementSearchSummaries: list[EngagementSearchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class EngagementContextPayloadTypeDef(TypedDict):
    CustomerProject: NotRequired[CustomerProjectsContextTypeDef]
    Lead: NotRequired[LeadContextUnionTypeDef]
    ProspectingResult: NotRequired[ProspectingResultUnionTypeDef]
    CustomerAccount: NotRequired[CustomerAccountContextTypeDef]

UpdateEngagementContextRequestTypeDef = TypedDict(
    "UpdateEngagementContextRequestTypeDef",
    {
        "Catalog": str,
        "EngagementIdentifier": str,
        "ContextIdentifier": str,
        "EngagementLastModifiedAt": TimestampTypeDef,
        "Type": EngagementContextTypeType,
        "Payload": UpdateEngagementContextPayloadTypeDef,
    },
)

class CreateEngagementInvitationRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    EngagementIdentifier: str
    Invitation: InvitationTypeDef

EngagementContextPayloadUnionTypeDef = Union[
    EngagementContextPayloadTypeDef, EngagementContextPayloadOutputTypeDef
]
CreateEngagementContextRequestTypeDef = TypedDict(
    "CreateEngagementContextRequestTypeDef",
    {
        "Catalog": str,
        "EngagementIdentifier": str,
        "ClientToken": str,
        "Type": EngagementContextTypeType,
        "Payload": EngagementContextPayloadUnionTypeDef,
    },
)
EngagementContextDetailsTypeDef = TypedDict(
    "EngagementContextDetailsTypeDef",
    {
        "Type": EngagementContextTypeType,
        "Id": NotRequired[str],
        "Payload": NotRequired[EngagementContextPayloadUnionTypeDef],
    },
)
EngagementContextDetailsUnionTypeDef = Union[
    EngagementContextDetailsTypeDef, EngagementContextDetailsOutputTypeDef
]

class CreateEngagementRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Title: NotRequired[str]
    Description: NotRequired[str]
    Contexts: NotRequired[Sequence[EngagementContextDetailsUnionTypeDef]]
