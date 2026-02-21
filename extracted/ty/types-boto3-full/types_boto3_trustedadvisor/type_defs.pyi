"""
Type annotations for trustedadvisor service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_trustedadvisor/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_trustedadvisor.type_defs import AccountRecommendationLifecycleSummaryTypeDef

    data: AccountRecommendationLifecycleSummaryTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ExclusionStatusType,
    RecommendationLanguageType,
    RecommendationLifecycleStageType,
    RecommendationPillarType,
    RecommendationSourceType,
    RecommendationStatusType,
    RecommendationTypeType,
    ResourceStatusType,
    UpdateRecommendationLifecycleStageReasonCodeType,
    UpdateRecommendationLifecycleStageType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountRecommendationLifecycleSummaryTypeDef",
    "BatchUpdateRecommendationResourceExclusionRequestTypeDef",
    "BatchUpdateRecommendationResourceExclusionResponseTypeDef",
    "CheckSummaryTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetOrganizationRecommendationRequestTypeDef",
    "GetOrganizationRecommendationResponseTypeDef",
    "GetRecommendationRequestTypeDef",
    "GetRecommendationResponseTypeDef",
    "ListChecksRequestPaginateTypeDef",
    "ListChecksRequestTypeDef",
    "ListChecksResponseTypeDef",
    "ListOrganizationRecommendationAccountsRequestPaginateTypeDef",
    "ListOrganizationRecommendationAccountsRequestTypeDef",
    "ListOrganizationRecommendationAccountsResponseTypeDef",
    "ListOrganizationRecommendationResourcesRequestPaginateTypeDef",
    "ListOrganizationRecommendationResourcesRequestTypeDef",
    "ListOrganizationRecommendationResourcesResponseTypeDef",
    "ListOrganizationRecommendationsRequestPaginateTypeDef",
    "ListOrganizationRecommendationsRequestTypeDef",
    "ListOrganizationRecommendationsResponseTypeDef",
    "ListRecommendationResourcesRequestPaginateTypeDef",
    "ListRecommendationResourcesRequestTypeDef",
    "ListRecommendationResourcesResponseTypeDef",
    "ListRecommendationsRequestPaginateTypeDef",
    "ListRecommendationsRequestTypeDef",
    "ListRecommendationsResponseTypeDef",
    "OrganizationRecommendationResourceSummaryTypeDef",
    "OrganizationRecommendationSummaryTypeDef",
    "OrganizationRecommendationTypeDef",
    "PaginatorConfigTypeDef",
    "RecommendationCostOptimizingAggregatesTypeDef",
    "RecommendationPillarSpecificAggregatesTypeDef",
    "RecommendationResourceExclusionTypeDef",
    "RecommendationResourceSummaryTypeDef",
    "RecommendationResourcesAggregatesTypeDef",
    "RecommendationSummaryTypeDef",
    "RecommendationTypeDef",
    "ResponseMetadataTypeDef",
    "TimestampTypeDef",
    "UpdateOrganizationRecommendationLifecycleRequestTypeDef",
    "UpdateRecommendationLifecycleRequestTypeDef",
    "UpdateRecommendationResourceExclusionErrorTypeDef",
)

class AccountRecommendationLifecycleSummaryTypeDef(TypedDict):
    accountId: NotRequired[str]
    accountRecommendationArn: NotRequired[str]
    lifecycleStage: NotRequired[RecommendationLifecycleStageType]
    updatedOnBehalfOf: NotRequired[str]
    updatedOnBehalfOfJobTitle: NotRequired[str]
    updateReason: NotRequired[str]
    updateReasonCode: NotRequired[UpdateRecommendationLifecycleStageReasonCodeType]
    lastUpdatedAt: NotRequired[datetime]

class RecommendationResourceExclusionTypeDef(TypedDict):
    arn: str
    isExcluded: bool

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class UpdateRecommendationResourceExclusionErrorTypeDef(TypedDict):
    arn: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]

CheckSummaryTypeDef = TypedDict(
    "CheckSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "pillars": list[RecommendationPillarType],
        "awsServices": list[str],
        "source": RecommendationSourceType,
        "metadata": dict[str, str],
    },
)

class GetOrganizationRecommendationRequestTypeDef(TypedDict):
    organizationRecommendationIdentifier: str

class GetRecommendationRequestTypeDef(TypedDict):
    recommendationIdentifier: str
    language: NotRequired[RecommendationLanguageType]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListChecksRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    pillar: NotRequired[RecommendationPillarType]
    awsService: NotRequired[str]
    source: NotRequired[RecommendationSourceType]
    language: NotRequired[RecommendationLanguageType]

class ListOrganizationRecommendationAccountsRequestTypeDef(TypedDict):
    organizationRecommendationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    affectedAccountId: NotRequired[str]

class ListOrganizationRecommendationResourcesRequestTypeDef(TypedDict):
    organizationRecommendationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    status: NotRequired[ResourceStatusType]
    exclusionStatus: NotRequired[ExclusionStatusType]
    regionCode: NotRequired[str]
    affectedAccountId: NotRequired[str]

OrganizationRecommendationResourceSummaryTypeDef = TypedDict(
    "OrganizationRecommendationResourceSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "awsResourceId": str,
        "regionCode": str,
        "status": ResourceStatusType,
        "metadata": dict[str, str],
        "lastUpdatedAt": datetime,
        "recommendationArn": str,
        "exclusionStatus": NotRequired[ExclusionStatusType],
        "accountId": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]

class ListRecommendationResourcesRequestTypeDef(TypedDict):
    recommendationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    status: NotRequired[ResourceStatusType]
    exclusionStatus: NotRequired[ExclusionStatusType]
    regionCode: NotRequired[str]
    language: NotRequired[RecommendationLanguageType]

RecommendationResourceSummaryTypeDef = TypedDict(
    "RecommendationResourceSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "awsResourceId": str,
        "regionCode": str,
        "status": ResourceStatusType,
        "metadata": dict[str, str],
        "lastUpdatedAt": datetime,
        "recommendationArn": str,
        "exclusionStatus": NotRequired[ExclusionStatusType],
    },
)

class RecommendationResourcesAggregatesTypeDef(TypedDict):
    okCount: int
    warningCount: int
    errorCount: int
    excludedCount: NotRequired[int]

class RecommendationCostOptimizingAggregatesTypeDef(TypedDict):
    estimatedMonthlySavings: float
    estimatedPercentMonthlySavings: float

class UpdateOrganizationRecommendationLifecycleRequestTypeDef(TypedDict):
    lifecycleStage: UpdateRecommendationLifecycleStageType
    organizationRecommendationIdentifier: str
    updateReason: NotRequired[str]
    updateReasonCode: NotRequired[UpdateRecommendationLifecycleStageReasonCodeType]

class UpdateRecommendationLifecycleRequestTypeDef(TypedDict):
    lifecycleStage: UpdateRecommendationLifecycleStageType
    recommendationIdentifier: str
    updateReason: NotRequired[str]
    updateReasonCode: NotRequired[UpdateRecommendationLifecycleStageReasonCodeType]

class BatchUpdateRecommendationResourceExclusionRequestTypeDef(TypedDict):
    recommendationResourceExclusions: Sequence[RecommendationResourceExclusionTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListOrganizationRecommendationAccountsResponseTypeDef(TypedDict):
    accountRecommendationLifecycleSummaries: list[AccountRecommendationLifecycleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchUpdateRecommendationResourceExclusionResponseTypeDef(TypedDict):
    batchUpdateRecommendationResourceExclusionErrors: list[
        UpdateRecommendationResourceExclusionErrorTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef

class ListChecksResponseTypeDef(TypedDict):
    checkSummaries: list[CheckSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListChecksRequestPaginateTypeDef(TypedDict):
    pillar: NotRequired[RecommendationPillarType]
    awsService: NotRequired[str]
    source: NotRequired[RecommendationSourceType]
    language: NotRequired[RecommendationLanguageType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrganizationRecommendationAccountsRequestPaginateTypeDef(TypedDict):
    organizationRecommendationIdentifier: str
    affectedAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrganizationRecommendationResourcesRequestPaginateTypeDef(TypedDict):
    organizationRecommendationIdentifier: str
    status: NotRequired[ResourceStatusType]
    exclusionStatus: NotRequired[ExclusionStatusType]
    regionCode: NotRequired[str]
    affectedAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRecommendationResourcesRequestPaginateTypeDef(TypedDict):
    recommendationIdentifier: str
    status: NotRequired[ResourceStatusType]
    exclusionStatus: NotRequired[ExclusionStatusType]
    regionCode: NotRequired[str]
    language: NotRequired[RecommendationLanguageType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrganizationRecommendationResourcesResponseTypeDef(TypedDict):
    organizationRecommendationResourceSummaries: list[
        OrganizationRecommendationResourceSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ListOrganizationRecommendationsRequestPaginateTypeDef = TypedDict(
    "ListOrganizationRecommendationsRequestPaginateTypeDef",
    {
        "type": NotRequired[RecommendationTypeType],
        "status": NotRequired[RecommendationStatusType],
        "pillar": NotRequired[RecommendationPillarType],
        "awsService": NotRequired[str],
        "source": NotRequired[RecommendationSourceType],
        "checkIdentifier": NotRequired[str],
        "afterLastUpdatedAt": NotRequired[TimestampTypeDef],
        "beforeLastUpdatedAt": NotRequired[TimestampTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListOrganizationRecommendationsRequestTypeDef = TypedDict(
    "ListOrganizationRecommendationsRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "type": NotRequired[RecommendationTypeType],
        "status": NotRequired[RecommendationStatusType],
        "pillar": NotRequired[RecommendationPillarType],
        "awsService": NotRequired[str],
        "source": NotRequired[RecommendationSourceType],
        "checkIdentifier": NotRequired[str],
        "afterLastUpdatedAt": NotRequired[TimestampTypeDef],
        "beforeLastUpdatedAt": NotRequired[TimestampTypeDef],
    },
)
ListRecommendationsRequestPaginateTypeDef = TypedDict(
    "ListRecommendationsRequestPaginateTypeDef",
    {
        "type": NotRequired[RecommendationTypeType],
        "status": NotRequired[RecommendationStatusType],
        "pillar": NotRequired[RecommendationPillarType],
        "awsService": NotRequired[str],
        "source": NotRequired[RecommendationSourceType],
        "checkIdentifier": NotRequired[str],
        "afterLastUpdatedAt": NotRequired[TimestampTypeDef],
        "beforeLastUpdatedAt": NotRequired[TimestampTypeDef],
        "language": NotRequired[RecommendationLanguageType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListRecommendationsRequestTypeDef = TypedDict(
    "ListRecommendationsRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "type": NotRequired[RecommendationTypeType],
        "status": NotRequired[RecommendationStatusType],
        "pillar": NotRequired[RecommendationPillarType],
        "awsService": NotRequired[str],
        "source": NotRequired[RecommendationSourceType],
        "checkIdentifier": NotRequired[str],
        "afterLastUpdatedAt": NotRequired[TimestampTypeDef],
        "beforeLastUpdatedAt": NotRequired[TimestampTypeDef],
        "language": NotRequired[RecommendationLanguageType],
    },
)

class ListRecommendationResourcesResponseTypeDef(TypedDict):
    recommendationResourceSummaries: list[RecommendationResourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RecommendationPillarSpecificAggregatesTypeDef(TypedDict):
    costOptimizing: NotRequired[RecommendationCostOptimizingAggregatesTypeDef]

OrganizationRecommendationSummaryTypeDef = TypedDict(
    "OrganizationRecommendationSummaryTypeDef",
    {
        "id": str,
        "type": RecommendationTypeType,
        "status": RecommendationStatusType,
        "pillars": list[RecommendationPillarType],
        "source": RecommendationSourceType,
        "name": str,
        "resourcesAggregates": RecommendationResourcesAggregatesTypeDef,
        "arn": str,
        "checkArn": NotRequired[str],
        "lifecycleStage": NotRequired[RecommendationLifecycleStageType],
        "awsServices": NotRequired[list[str]],
        "pillarSpecificAggregates": NotRequired[RecommendationPillarSpecificAggregatesTypeDef],
        "createdAt": NotRequired[datetime],
        "lastUpdatedAt": NotRequired[datetime],
    },
)
OrganizationRecommendationTypeDef = TypedDict(
    "OrganizationRecommendationTypeDef",
    {
        "id": str,
        "type": RecommendationTypeType,
        "status": RecommendationStatusType,
        "pillars": list[RecommendationPillarType],
        "source": RecommendationSourceType,
        "name": str,
        "resourcesAggregates": RecommendationResourcesAggregatesTypeDef,
        "arn": str,
        "description": str,
        "checkArn": NotRequired[str],
        "lifecycleStage": NotRequired[RecommendationLifecycleStageType],
        "awsServices": NotRequired[list[str]],
        "pillarSpecificAggregates": NotRequired[RecommendationPillarSpecificAggregatesTypeDef],
        "createdAt": NotRequired[datetime],
        "lastUpdatedAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "updatedOnBehalfOf": NotRequired[str],
        "updatedOnBehalfOfJobTitle": NotRequired[str],
        "updateReason": NotRequired[str],
        "updateReasonCode": NotRequired[UpdateRecommendationLifecycleStageReasonCodeType],
        "resolvedAt": NotRequired[datetime],
    },
)
RecommendationSummaryTypeDef = TypedDict(
    "RecommendationSummaryTypeDef",
    {
        "id": str,
        "type": RecommendationTypeType,
        "status": RecommendationStatusType,
        "pillars": list[RecommendationPillarType],
        "source": RecommendationSourceType,
        "name": str,
        "resourcesAggregates": RecommendationResourcesAggregatesTypeDef,
        "arn": str,
        "checkArn": NotRequired[str],
        "lifecycleStage": NotRequired[RecommendationLifecycleStageType],
        "awsServices": NotRequired[list[str]],
        "pillarSpecificAggregates": NotRequired[RecommendationPillarSpecificAggregatesTypeDef],
        "createdAt": NotRequired[datetime],
        "lastUpdatedAt": NotRequired[datetime],
        "statusReason": NotRequired[Literal["no_data_ok"]],
    },
)
RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "id": str,
        "type": RecommendationTypeType,
        "status": RecommendationStatusType,
        "pillars": list[RecommendationPillarType],
        "source": RecommendationSourceType,
        "name": str,
        "resourcesAggregates": RecommendationResourcesAggregatesTypeDef,
        "arn": str,
        "description": str,
        "checkArn": NotRequired[str],
        "lifecycleStage": NotRequired[RecommendationLifecycleStageType],
        "awsServices": NotRequired[list[str]],
        "pillarSpecificAggregates": NotRequired[RecommendationPillarSpecificAggregatesTypeDef],
        "createdAt": NotRequired[datetime],
        "lastUpdatedAt": NotRequired[datetime],
        "statusReason": NotRequired[Literal["no_data_ok"]],
        "createdBy": NotRequired[str],
        "updatedOnBehalfOf": NotRequired[str],
        "updatedOnBehalfOfJobTitle": NotRequired[str],
        "updateReason": NotRequired[str],
        "updateReasonCode": NotRequired[UpdateRecommendationLifecycleStageReasonCodeType],
        "resolvedAt": NotRequired[datetime],
    },
)

class ListOrganizationRecommendationsResponseTypeDef(TypedDict):
    organizationRecommendationSummaries: list[OrganizationRecommendationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetOrganizationRecommendationResponseTypeDef(TypedDict):
    organizationRecommendation: OrganizationRecommendationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRecommendationsResponseTypeDef(TypedDict):
    recommendationSummaries: list[RecommendationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetRecommendationResponseTypeDef(TypedDict):
    recommendation: RecommendationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
