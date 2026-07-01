"""
Type annotations for partnercentral-selling service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_partnercentral_selling.type_defs import AcceptEngagementInvitationRequestTypeDef

    data: AcceptEngagementInvitationRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AwsClosedLostReasonType,
    AwsFundingUsedType,
    AwsMemberBusinessTitleType,
    AwsOpportunityStageType,
    ChannelType,
    ClosedLostReasonType,
    CompetitorNameType,
    CountryCodeType,
    CurrencyCodeType,
    DeliveryModelType,
    EngagementContextTypeType,
    EngagementInvitationPayloadTypeType,
    EngagementScoreType,
    IndustryType,
    InvitationStatusType,
    InvolvementTypeChangeReasonType,
    MarketingSourceType,
    MarketSegmentType,
    NationalSecurityType,
    OpportunityOriginType,
    OpportunitySortNameType,
    OpportunityTypeType,
    ParticipantTypeType,
    PrimaryNeedFromAwsType,
    ProspectingFromEngagementTaskSortNameType,
    ProspectingTaskStatusType,
    ReasonCodeType,
    ReceiverResponsibilityType,
    RelatedEntityTypeType,
    ResourceSnapshotJobStatusType,
    RevenueModelType,
    ReviewStatusType,
    SalesActivityType,
    SalesInvolvementTypeType,
    SolutionSortNameType,
    SolutionStatusType,
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
    "AccountReceiverTypeDef",
    "AccountSummaryTypeDef",
    "AccountTypeDef",
    "AddressSummaryTypeDef",
    "AddressTypeDef",
    "AssignOpportunityRequestTypeDef",
    "AssigneeContactTypeDef",
    "AssociateOpportunityRequestTypeDef",
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
    "AwsSubmissionTypeDef",
    "AwsTeamMemberTypeDef",
    "ContactTypeDef",
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
    "CustomerOutputTypeDef",
    "CustomerProjectsContextTypeDef",
    "CustomerSummaryTypeDef",
    "CustomerTypeDef",
    "CustomerUnionTypeDef",
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
    "EngagementInvitationSummaryTypeDef",
    "EngagementMemberSummaryTypeDef",
    "EngagementMemberTypeDef",
    "EngagementProspectingResultTypeDef",
    "EngagementResourceAssociationSummaryTypeDef",
    "EngagementSortTypeDef",
    "EngagementSummaryTypeDef",
    "ExpectedContractDurationTypeDef",
    "ExpectedCustomerSpendTypeDef",
    "GetAwsOpportunitySummaryRequestTypeDef",
    "GetAwsOpportunitySummaryResponseTypeDef",
    "GetEngagementInvitationRequestTypeDef",
    "GetEngagementInvitationResponseTypeDef",
    "GetEngagementRequestTypeDef",
    "GetEngagementResponseTypeDef",
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
    "InvitationTypeDef",
    "LastModifiedDateTypeDef",
    "LeadContactTypeDef",
    "LeadContextOutputTypeDef",
    "LeadContextTypeDef",
    "LeadContextUnionTypeDef",
    "LeadCustomerTypeDef",
    "LeadInsightsTypeDef",
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
    "ListEngagementByAcceptingInvitationTaskSummaryTypeDef",
    "ListEngagementByAcceptingInvitationTasksRequestPaginateTypeDef",
    "ListEngagementByAcceptingInvitationTasksRequestTypeDef",
    "ListEngagementByAcceptingInvitationTasksResponseTypeDef",
    "ListEngagementFromOpportunityTaskSummaryTypeDef",
    "ListEngagementFromOpportunityTasksRequestPaginateTypeDef",
    "ListEngagementFromOpportunityTasksRequestTypeDef",
    "ListEngagementFromOpportunityTasksResponseTypeDef",
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
    "OpportunityEngagementInvitationSortTypeDef",
    "OpportunityInvitationPayloadOutputTypeDef",
    "OpportunityInvitationPayloadTypeDef",
    "OpportunityInvitationPayloadUnionTypeDef",
    "OpportunityQualityTypeDef",
    "OpportunitySortTypeDef",
    "OpportunitySummaryTypeDef",
    "OpportunitySummaryViewTypeDef",
    "PaginatorConfigTypeDef",
    "PayloadOutputTypeDef",
    "PayloadTypeDef",
    "PayloadUnionTypeDef",
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
    "SenderContactTypeDef",
    "SoftwareRevenueTypeDef",
    "SolutionBaseTypeDef",
    "SolutionSortTypeDef",
    "SortObjectTypeDef",
    "StartEngagementByAcceptingInvitationTaskRequestTypeDef",
    "StartEngagementByAcceptingInvitationTaskResponseTypeDef",
    "StartEngagementFromOpportunityTaskRequestTypeDef",
    "StartEngagementFromOpportunityTaskResponseTypeDef",
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

class AwsSubmissionTypeDef(TypedDict):
    InvolvementType: SalesInvolvementTypeType
    Visibility: NotRequired[VisibilityType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CreateResourceSnapshotRequestTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: str
    ResourceType: Literal["Opportunity"]
    ResourceIdentifier: str
    ResourceSnapshotTemplateIdentifier: str
    ClientToken: str

TimestampTypeDef = Union[datetime, str]

class EngagementCustomerProjectDetailsTypeDef(TypedDict):
    Title: str
    BusinessProblem: str
    TargetCompletionDate: str

class EngagementCustomerTypeDef(TypedDict):
    Industry: IndustryType
    CompanyName: str
    WebsiteUrl: str
    CountryCode: CountryCodeType

class DeleteResourceSnapshotJobRequestTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobIdentifier: str

class DisassociateOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    OpportunityIdentifier: str
    RelatedEntityType: RelatedEntityTypeType
    RelatedEntityIdentifier: str

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

class GetEngagementInvitationRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class GetEngagementRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

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

class LeadContactTypeDef(TypedDict):
    BusinessTitle: str
    Email: str
    FirstName: str
    LastName: str
    Phone: NotRequired[str]

class LeadInsightsTypeDef(TypedDict):
    LeadReadinessScore: NotRequired[str]

class LeadInvitationCustomerTypeDef(TypedDict):
    CompanyName: str
    CountryCode: CountryCodeType
    Industry: NotRequired[IndustryType]
    WebsiteUrl: NotRequired[str]
    AwsMaturity: NotRequired[str]
    MarketSegment: NotRequired[MarketSegmentType]

class LeadInvitationInteractionTypeDef(TypedDict):
    SourceType: str
    SourceId: str
    SourceName: str
    ContactBusinessTitle: str
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

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

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

class MonetaryValueTypeDef(TypedDict):
    Amount: str
    CurrencyCode: CurrencyCodeType

class SenderContactTypeDef(TypedDict):
    Email: str
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    BusinessTitle: NotRequired[str]
    Phone: NotRequired[str]

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

class ReceiverTypeDef(TypedDict):
    Account: NotRequired[AccountReceiverTypeDef]

class AccountSummaryTypeDef(TypedDict):
    CompanyName: str
    Industry: NotRequired[IndustryType]
    OtherIndustry: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    Address: NotRequired[AddressSummaryTypeDef]

class LeadCustomerTypeDef(TypedDict):
    CompanyName: str
    Address: AddressSummaryTypeDef
    Industry: NotRequired[IndustryType]
    WebsiteUrl: NotRequired[str]
    AwsMaturity: NotRequired[str]
    MarketSegment: NotRequired[MarketSegmentType]

class AccountTypeDef(TypedDict):
    CompanyName: str
    Industry: NotRequired[IndustryType]
    OtherIndustry: NotRequired[str]
    WebsiteUrl: NotRequired[str]
    AwsAccountId: NotRequired[str]
    Address: NotRequired[AddressTypeDef]
    Duns: NotRequired[str]

class AssignOpportunityRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    Assignee: AssigneeContactTypeDef

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

class PutSellingSystemSettingsResponseTypeDef(TypedDict):
    Catalog: str
    ResourceSnapshotJobRoleArn: str
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

class CreateResourceSnapshotJobRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    EngagementIdentifier: str
    ResourceType: Literal["Opportunity"]
    ResourceIdentifier: str
    ResourceSnapshotTemplateIdentifier: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

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

class CreatedDateFilterTypeDef(TypedDict):
    AfterCreatedDate: NotRequired[TimestampTypeDef]
    BeforeCreatedDate: NotRequired[TimestampTypeDef]

class LastModifiedDateTypeDef(TypedDict):
    AfterLastModifiedDate: NotRequired[TimestampTypeDef]
    BeforeLastModifiedDate: NotRequired[TimestampTypeDef]

class NextStepsHistoryTypeDef(TypedDict):
    Value: str
    Time: TimestampTypeDef

class CustomerProjectsContextTypeDef(TypedDict):
    Customer: NotRequired[EngagementCustomerTypeDef]
    Project: NotRequired[EngagementCustomerProjectDetailsTypeDef]

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

class LeadInteractionOutputTypeDef(TypedDict):
    SourceType: str
    SourceId: str
    SourceName: str
    CustomerAction: str
    Contact: LeadContactTypeDef
    Usecase: NotRequired[str]
    InteractionDate: NotRequired[datetime]
    BusinessProblem: NotRequired[str]

class LeadInteractionTypeDef(TypedDict):
    SourceType: str
    SourceId: str
    SourceName: str
    CustomerAction: str
    Contact: LeadContactTypeDef
    Usecase: NotRequired[str]
    InteractionDate: NotRequired[TimestampTypeDef]
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

class ListEngagementByAcceptingInvitationTasksResponseTypeDef(TypedDict):
    TaskSummaries: list[ListEngagementByAcceptingInvitationTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEngagementByAcceptingInvitationTasksRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementInvitationIdentifier: NotRequired[Sequence[str]]
    TaskIdentifier: NotRequired[Sequence[str]]

class ListEngagementFromOpportunityTasksRequestTypeDef(TypedDict):
    Catalog: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    TaskIdentifier: NotRequired[Sequence[str]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementIdentifier: NotRequired[Sequence[str]]

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

class ListEngagementByAcceptingInvitationTasksRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementInvitationIdentifier: NotRequired[Sequence[str]]
    TaskIdentifier: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEngagementFromOpportunityTasksRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    TaskIdentifier: NotRequired[Sequence[str]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementIdentifier: NotRequired[Sequence[str]]
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

class ListOpportunityFromEngagementTasksRequestPaginateTypeDef(TypedDict):
    Catalog: str
    Sort: NotRequired[ListTasksSortBaseTypeDef]
    TaskStatus: NotRequired[Sequence[TaskStatusType]]
    TaskIdentifier: NotRequired[Sequence[str]]
    OpportunityIdentifier: NotRequired[Sequence[str]]
    EngagementIdentifier: NotRequired[Sequence[str]]
    ContextIdentifier: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceSnapshotsRequestPaginateTypeDef(TypedDict):
    Catalog: str
    EngagementIdentifier: str
    ResourceType: NotRequired[Literal["Opportunity"]]
    ResourceIdentifier: NotRequired[str]
    ResourceSnapshotTemplateIdentifier: NotRequired[str]
    CreatedBy: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

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

class SoftwareRevenueTypeDef(TypedDict):
    DeliveryModel: NotRequired[RevenueModelType]
    Value: NotRequired[MonetaryValueTypeDef]
    EffectiveDate: NotRequired[str]
    ExpirationDate: NotRequired[str]

class ProspectingResultAwsOutputTypeDef(TypedDict):
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    TaskId: NotRequired[str]
    TaskArn: NotRequired[str]
    TaskName: NotRequired[str]
    Customer: NotRequired[ProspectingResultCustomerOutputTypeDef]
    Insights: NotRequired[ProspectingInsightsTypeDef]

ProspectingResultCustomerUnionTypeDef = Union[
    ProspectingResultCustomerTypeDef, ProspectingResultCustomerOutputTypeDef
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

class OpportunityInvitationPayloadOutputTypeDef(TypedDict):
    ReceiverResponsibilities: list[ReceiverResponsibilityType]
    Customer: EngagementCustomerTypeDef
    Project: ProjectDetailsOutputTypeDef
    SenderContacts: NotRequired[list[SenderContactTypeDef]]

ProjectDetailsUnionTypeDef = Union[ProjectDetailsTypeDef, ProjectDetailsOutputTypeDef]

class AwsProductInsightsTypeDef(TypedDict):
    CurrencyCode: CurrencyCodeType
    Frequency: Literal["Monthly"]
    TotalAmountByCategory: dict[str, str]
    AwsProducts: list[AwsProductDetailsTypeDef]
    TotalAmount: NotRequired[str]
    TotalOptimizedAmount: NotRequired[str]
    TotalPotentialSavingsAmount: NotRequired[str]

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

ProjectUnionTypeDef = Union[ProjectTypeDef, ProjectOutputTypeDef]

class LeadContextOutputTypeDef(TypedDict):
    Customer: LeadCustomerTypeDef
    Interactions: list[LeadInteractionOutputTypeDef]
    Insights: NotRequired[LeadInsightsTypeDef]
    QualificationStatus: NotRequired[str]

LeadInteractionUnionTypeDef = Union[LeadInteractionTypeDef, LeadInteractionOutputTypeDef]

class ProspectingResultOutputTypeDef(TypedDict):
    Aws: NotRequired[ProspectingResultAwsOutputTypeDef]

class ProspectingResultAwsTypeDef(TypedDict):
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    TaskId: NotRequired[str]
    TaskArn: NotRequired[str]
    TaskName: NotRequired[str]
    Customer: NotRequired[ProspectingResultCustomerUnionTypeDef]
    Insights: NotRequired[ProspectingInsightsTypeDef]

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

class PayloadOutputTypeDef(TypedDict):
    OpportunityInvitation: NotRequired[OpportunityInvitationPayloadOutputTypeDef]
    LeadInvitation: NotRequired[LeadInvitationPayloadTypeDef]

class OpportunityInvitationPayloadTypeDef(TypedDict):
    ReceiverResponsibilities: Sequence[ReceiverResponsibilityType]
    Customer: EngagementCustomerTypeDef
    Project: ProjectDetailsUnionTypeDef
    SenderContacts: NotRequired[Sequence[SenderContactTypeDef]]

class AwsProductsSpendInsightsBySourceTypeDef(TypedDict):
    Partner: NotRequired[AwsProductInsightsTypeDef]
    AWS: NotRequired[AwsProductInsightsTypeDef]

LifeCycleUnionTypeDef = Union[LifeCycleTypeDef, LifeCycleOutputTypeDef]

class LeadContextTypeDef(TypedDict):
    Customer: LeadCustomerTypeDef
    Interactions: Sequence[LeadInteractionUnionTypeDef]
    Insights: NotRequired[LeadInsightsTypeDef]
    QualificationStatus: NotRequired[str]

class UpdateLeadContextTypeDef(TypedDict):
    Customer: LeadCustomerTypeDef
    QualificationStatus: NotRequired[str]
    Interaction: NotRequired[LeadInteractionUnionTypeDef]
    Insights: NotRequired[LeadInsightsTypeDef]

class EngagementContextPayloadOutputTypeDef(TypedDict):
    CustomerProject: NotRequired[CustomerProjectsContextTypeDef]
    Lead: NotRequired[LeadContextOutputTypeDef]
    ProspectingResult: NotRequired[ProspectingResultOutputTypeDef]

ProspectingResultAwsUnionTypeDef = Union[
    ProspectingResultAwsTypeDef, ProspectingResultAwsOutputTypeDef
]

class ListOpportunitiesResponseTypeDef(TypedDict):
    OpportunitySummaries: list[OpportunitySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

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
    ResponseMetadata: ResponseMetadataTypeDef

OpportunityInvitationPayloadUnionTypeDef = Union[
    OpportunityInvitationPayloadTypeDef, OpportunityInvitationPayloadOutputTypeDef
]

class AwsOpportunityInsightsTypeDef(TypedDict):
    NextBestActions: NotRequired[str]
    EngagementScore: NotRequired[EngagementScoreType]
    AwsProductsSpendInsightsBySource: NotRequired[AwsProductsSpendInsightsBySourceTypeDef]
    OpportunityQuality: NotRequired[OpportunityQualityTypeDef]
    Recommendations: NotRequired[list[RecommendationTypeDef]]

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

LeadContextUnionTypeDef = Union[LeadContextTypeDef, LeadContextOutputTypeDef]
EngagementContextDetailsOutputTypeDef = TypedDict(
    "EngagementContextDetailsOutputTypeDef",
    {
        "Type": EngagementContextTypeType,
        "Id": NotRequired[str],
        "Payload": NotRequired[EngagementContextPayloadOutputTypeDef],
    },
)

class ProspectingResultTypeDef(TypedDict):
    Aws: NotRequired[ProspectingResultAwsUnionTypeDef]

class PayloadTypeDef(TypedDict):
    OpportunityInvitation: NotRequired[OpportunityInvitationPayloadUnionTypeDef]
    LeadInvitation: NotRequired[LeadInvitationPayloadTypeDef]

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
    Catalog: str
    ResponseMetadata: ResponseMetadataTypeDef

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

ProspectingResultUnionTypeDef = Union[ProspectingResultTypeDef, ProspectingResultOutputTypeDef]
PayloadUnionTypeDef = Union[PayloadTypeDef, PayloadOutputTypeDef]

class ResourceSnapshotPayloadTypeDef(TypedDict):
    OpportunitySummary: NotRequired[OpportunitySummaryViewTypeDef]
    AwsOpportunitySummaryFullView: NotRequired[AwsOpportunitySummaryFullViewTypeDef]

class EngagementContextPayloadTypeDef(TypedDict):
    CustomerProject: NotRequired[CustomerProjectsContextTypeDef]
    Lead: NotRequired[LeadContextUnionTypeDef]
    ProspectingResult: NotRequired[ProspectingResultUnionTypeDef]

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

EngagementContextPayloadUnionTypeDef = Union[
    EngagementContextPayloadTypeDef, EngagementContextPayloadOutputTypeDef
]
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
    Title: str
    Description: str
    Contexts: NotRequired[Sequence[EngagementContextDetailsUnionTypeDef]]
