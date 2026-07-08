"""
Type annotations for partnercentral-revenue-measurement service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_partnercentral_revenue_measurement.type_defs import MarketplaceProductSummaryTypeDef

    data: MarketplaceProductSummaryTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AllocationStatusType,
    CatalogNameType,
    EntityTypeType,
    RevenueAttributionAllocationActionType,
    RevenueAttributionAllocationErrorCodeType,
    RevenueAttributionAllocationTaskStatusType,
    SortOrderType,
    TenancyModelType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AttributionSummaryTypeDef",
    "CreateMarketplaceRevenueShareAllocationInputTypeDef",
    "CreateMarketplaceRevenueShareAllocationOutputTypeDef",
    "CreateMarketplaceRevenueShareInputTypeDef",
    "CreateMarketplaceRevenueShareOutputTypeDef",
    "CreateRevenueAttributionInputTypeDef",
    "CreateRevenueAttributionOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetMarketplaceRevenueShareAllocationInputTypeDef",
    "GetMarketplaceRevenueShareAllocationOutputTypeDef",
    "GetMarketplaceRevenueShareInputTypeDef",
    "GetMarketplaceRevenueShareOutputTypeDef",
    "GetRevenueAttributionAllocationInputTypeDef",
    "GetRevenueAttributionAllocationOutputTypeDef",
    "GetRevenueAttributionAllocationsTaskInputTypeDef",
    "GetRevenueAttributionAllocationsTaskOutputTypeDef",
    "GetRevenueAttributionInputTypeDef",
    "GetRevenueAttributionOutputTypeDef",
    "ListMarketplaceRevenueShareAllocationsInputPaginateTypeDef",
    "ListMarketplaceRevenueShareAllocationsInputTypeDef",
    "ListMarketplaceRevenueShareAllocationsOutputTypeDef",
    "ListMarketplaceRevenueSharesInputPaginateTypeDef",
    "ListMarketplaceRevenueSharesInputTypeDef",
    "ListMarketplaceRevenueSharesOutputTypeDef",
    "ListRevenueAttributionAllocationsInputPaginateTypeDef",
    "ListRevenueAttributionAllocationsInputTypeDef",
    "ListRevenueAttributionAllocationsOutputTypeDef",
    "ListRevenueAttributionsInputPaginateTypeDef",
    "ListRevenueAttributionsInputTypeDef",
    "ListRevenueAttributionsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MarketplaceProductSummaryTypeDef",
    "MarketplaceRevenueShareAllocationSummaryTypeDef",
    "MarketplaceRevenueShareSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RevenueAttributionAllocationErrorDetailTypeDef",
    "RevenueAttributionAllocationSummaryTypeDef",
    "RevenueShareAllocationTypeDef",
    "StartRevenueAttributionAllocationsTaskInputTypeDef",
    "StartRevenueAttributionAllocationsTaskOutputTypeDef",
    "TagResourceInputTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateMarketplaceRevenueShareAllocationInputTypeDef",
    "UpdateMarketplaceRevenueShareAllocationOutputTypeDef",
    "UpdateRevenueAttributionInputTypeDef",
    "UpdateRevenueAttributionOutputTypeDef",
)

class MarketplaceProductSummaryTypeDef(TypedDict):
    ProductId: NotRequired[str]
    ProductCode: NotRequired[str]
    ProductName: NotRequired[str]

class CreateMarketplaceRevenueShareAllocationInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductId: str
    EffectiveFrom: str
    RevenueSharePercent: str
    ClientToken: NotRequired[str]
    EffectiveUntil: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class GetMarketplaceRevenueShareAllocationInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductId: str
    MarketplaceRevenueShareAllocationId: str
    MarketplaceRevenueShareRevision: NotRequired[str]

class GetMarketplaceRevenueShareInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductId: str
    Revision: NotRequired[int]

class GetRevenueAttributionAllocationInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    RevenueAttributionIdentifier: str
    RevenueAttributionAllocationId: str
    RevenueAttributionRevision: NotRequired[str]

class GetRevenueAttributionAllocationsTaskInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    RevenueAttributionIdentifier: str

class RevenueAttributionAllocationErrorDetailTypeDef(TypedDict):
    EntityType: EntityTypeType
    EntityId: str
    CustomerAwsAccountId: str
    EffectiveFrom: str
    EffectiveUntil: str
    Action: RevenueAttributionAllocationActionType
    ErrorCode: RevenueAttributionAllocationErrorCodeType
    ErrorMessage: str
    RevenueAttributionAllocationId: NotRequired[str]

class GetRevenueAttributionInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    Identifier: str
    Revision: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListMarketplaceRevenueShareAllocationsInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductId: str
    Status: NotRequired[AllocationStatusType]
    AfterEffectiveFrom: NotRequired[str]
    BeforeEffectiveFrom: NotRequired[str]
    SortBy: NotRequired[Literal["EffectiveFrom"]]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    MarketplaceRevenueShareRevision: NotRequired[str]

class MarketplaceRevenueShareAllocationSummaryTypeDef(TypedDict):
    MarketplaceRevenueShareAllocationId: str
    ProductId: str
    Arn: str
    EffectiveFrom: str
    RevenueSharePercent: str
    Status: AllocationStatusType
    ProductName: NotRequired[str]
    EffectiveUntil: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]

TimestampTypeDef = Union[datetime, str]

class MarketplaceRevenueShareSummaryTypeDef(TypedDict):
    ProductId: str
    Arn: str
    Catalog: NotRequired[CatalogNameType]
    ProductCode: NotRequired[str]
    ProductName: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]
    LatestRevision: NotRequired[int]
    TotalActiveMarketplaceRevenueShareAllocationCount: NotRequired[int]
    TotalMarketplaceRevenueShareAllocationCount: NotRequired[int]

class ListRevenueAttributionAllocationsInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    RevenueAttributionIdentifier: str
    EntityTypeFilters: NotRequired[Sequence[EntityTypeType]]
    EntityIdentifierFilters: NotRequired[Sequence[str]]
    CustomerAwsAccountIdFilters: NotRequired[Sequence[str]]
    StatusFilter: NotRequired[AllocationStatusType]
    AfterEffectiveFrom: NotRequired[str]
    BeforeEffectiveFrom: NotRequired[str]
    AfterEffectiveUntil: NotRequired[str]
    BeforeEffectiveUntil: NotRequired[str]
    SortBy: NotRequired[Literal["EffectiveFrom"]]
    SortOrder: NotRequired[SortOrderType]
    RevenueAttributionRevision: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class RevenueAttributionAllocationSummaryTypeDef(TypedDict):
    RevenueAttributionAllocationId: str
    RevenueAttributionIdentifier: str
    EntityType: EntityTypeType
    EntityIdentifier: str
    CustomerAwsAccountId: str
    RevenueSharePercent: str
    EffectiveFrom: str
    EffectiveUntil: str
    Status: AllocationStatusType
    EntityName: NotRequired[str]

class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str

class RevenueShareAllocationTypeDef(TypedDict):
    Action: RevenueAttributionAllocationActionType
    EntityType: EntityTypeType
    EntityIdentifier: str
    CustomerAwsAccountId: str
    RevenueSharePercent: str
    EffectiveFrom: str
    EffectiveUntil: str
    RevenueAttributionAllocationId: NotRequired[str]
    Status: NotRequired[AllocationStatusType]

class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateMarketplaceRevenueShareAllocationInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductId: str
    MarketplaceRevenueShareAllocationId: str
    MarketplaceRevenueShareRevision: str
    ClientToken: NotRequired[str]
    EffectiveFrom: NotRequired[str]
    EffectiveUntil: NotRequired[str]
    RevenueSharePercent: NotRequired[str]
    Status: NotRequired[AllocationStatusType]

class UpdateRevenueAttributionInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    Identifier: str
    Revision: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]

class AttributionSummaryTypeDef(TypedDict):
    TenancyModel: TenancyModelType
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Catalog: NotRequired[CatalogNameType]
    Name: NotRequired[str]
    MarketplaceProduct: NotRequired[MarketplaceProductSummaryTypeDef]
    CreatedDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]
    LatestRevision: NotRequired[str]
    EffectiveFrom: NotRequired[str]
    EffectiveUntil: NotRequired[str]
    TotalActiveRevenueAttributionAllocationCount: NotRequired[int]
    TotalRevenueAttributionAllocationCount: NotRequired[int]

class CreateMarketplaceRevenueShareAllocationOutputTypeDef(TypedDict):
    MarketplaceRevenueShareAllocationId: str
    ProductId: str
    ProductName: str
    Arn: str
    EffectiveFrom: str
    EffectiveUntil: str
    RevenueSharePercent: str
    Status: AllocationStatusType
    CreatedDate: datetime
    LastModifiedDate: datetime
    LatestMarketplaceRevenueShareRevision: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMarketplaceRevenueShareOutputTypeDef(TypedDict):
    ProductId: str
    Arn: str
    Catalog: CatalogNameType
    ProductCode: str
    ProductName: str
    CreatedDate: datetime
    LastModifiedDate: datetime
    Revision: int
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRevenueAttributionOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    Name: str
    Description: str
    TenancyModel: TenancyModelType
    MarketplaceProduct: MarketplaceProductSummaryTypeDef
    Revision: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetMarketplaceRevenueShareAllocationOutputTypeDef(TypedDict):
    MarketplaceRevenueShareAllocationId: str
    ProductId: str
    ProductName: str
    Arn: str
    EffectiveFrom: str
    EffectiveUntil: str
    RevenueSharePercent: str
    Status: AllocationStatusType
    CreatedDate: datetime
    LastModifiedDate: datetime
    LatestMarketplaceRevenueShareRevision: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetMarketplaceRevenueShareOutputTypeDef(TypedDict):
    ProductId: str
    Arn: str
    Catalog: CatalogNameType
    ProductCode: str
    ProductName: str
    CreatedDate: datetime
    LastModifiedDate: datetime
    Revision: int
    LatestRevision: int
    TotalActiveMarketplaceRevenueShareAllocationCount: int
    TotalMarketplaceRevenueShareAllocationCount: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetRevenueAttributionAllocationOutputTypeDef(TypedDict):
    RevenueAttributionAllocationId: str
    RevenueAttributionIdentifier: str
    EntityType: EntityTypeType
    EntityIdentifier: str
    EntityName: str
    CustomerAwsAccountId: str
    RevenueSharePercent: str
    EffectiveFrom: str
    EffectiveUntil: str
    Status: AllocationStatusType
    CreatedDate: datetime
    LastModifiedDate: datetime
    RevenueAttributionRevision: str
    RevenueAttributionLatestRevision: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRevenueAttributionOutputTypeDef(TypedDict):
    Arn: str
    Id: str
    Catalog: CatalogNameType
    Name: str
    Description: str
    TenancyModel: TenancyModelType
    MarketplaceProduct: MarketplaceProductSummaryTypeDef
    CreatedDate: datetime
    LastModifiedDate: datetime
    Revision: str
    LatestRevision: str
    EffectiveFrom: str
    EffectiveUntil: str
    TotalActiveRevenueAttributionAllocationCount: int
    TotalRevenueAttributionAllocationCount: int
    ResponseMetadata: ResponseMetadataTypeDef

class StartRevenueAttributionAllocationsTaskOutputTypeDef(TypedDict):
    TaskId: str
    Status: RevenueAttributionAllocationTaskStatusType
    Catalog: CatalogNameType
    RevenueAttributionArn: str
    StartedAt: datetime
    TotalRevenueAttributionAllocationRecords: int
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMarketplaceRevenueShareAllocationOutputTypeDef(TypedDict):
    MarketplaceRevenueShareAllocationId: str
    ProductId: str
    ProductName: str
    Arn: str
    EffectiveFrom: str
    EffectiveUntil: str
    RevenueSharePercent: str
    Status: AllocationStatusType
    CreatedDate: datetime
    LastModifiedDate: datetime
    LatestMarketplaceRevenueShareRevision: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRevenueAttributionOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    Description: str
    LastModifiedDate: datetime
    LatestRevision: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMarketplaceRevenueShareInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductId: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateRevenueAttributionInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    Name: str
    TenancyModel: TenancyModelType
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    ProductIdentifier: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class GetRevenueAttributionAllocationsTaskOutputTypeDef(TypedDict):
    TaskId: str
    Status: RevenueAttributionAllocationTaskStatusType
    Catalog: CatalogNameType
    RevenueAttributionArn: str
    StartedAt: datetime
    EndedAt: datetime
    TotalRevenueAttributionAllocationRecords: int
    Description: str
    RevenueAttributionLatestRevision: str
    ErrorDetailList: list[RevenueAttributionAllocationErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListMarketplaceRevenueShareAllocationsInputPaginateTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductId: str
    Status: NotRequired[AllocationStatusType]
    AfterEffectiveFrom: NotRequired[str]
    BeforeEffectiveFrom: NotRequired[str]
    SortBy: NotRequired[Literal["EffectiveFrom"]]
    SortOrder: NotRequired[SortOrderType]
    MarketplaceRevenueShareRevision: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRevenueAttributionAllocationsInputPaginateTypeDef(TypedDict):
    Catalog: CatalogNameType
    RevenueAttributionIdentifier: str
    EntityTypeFilters: NotRequired[Sequence[EntityTypeType]]
    EntityIdentifierFilters: NotRequired[Sequence[str]]
    CustomerAwsAccountIdFilters: NotRequired[Sequence[str]]
    StatusFilter: NotRequired[AllocationStatusType]
    AfterEffectiveFrom: NotRequired[str]
    BeforeEffectiveFrom: NotRequired[str]
    AfterEffectiveUntil: NotRequired[str]
    BeforeEffectiveUntil: NotRequired[str]
    SortBy: NotRequired[Literal["EffectiveFrom"]]
    SortOrder: NotRequired[SortOrderType]
    RevenueAttributionRevision: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMarketplaceRevenueShareAllocationsOutputTypeDef(TypedDict):
    MarketplaceRevenueShareAllocationSummaries: list[
        MarketplaceRevenueShareAllocationSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListMarketplaceRevenueSharesInputPaginateTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductIds: NotRequired[Sequence[str]]
    ProductCodes: NotRequired[Sequence[str]]
    SortBy: NotRequired[Literal["LastModifiedDate"]]
    SortOrder: NotRequired[SortOrderType]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMarketplaceRevenueSharesInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    ProductIds: NotRequired[Sequence[str]]
    ProductCodes: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[Literal["LastModifiedDate"]]
    SortOrder: NotRequired[SortOrderType]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]

class ListRevenueAttributionsInputPaginateTypeDef(TypedDict):
    Catalog: CatalogNameType
    Identifiers: NotRequired[Sequence[str]]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["LastModifiedDate"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRevenueAttributionsInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    Identifiers: NotRequired[Sequence[str]]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["LastModifiedDate"]]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListMarketplaceRevenueSharesOutputTypeDef(TypedDict):
    MarketplaceRevenueShareSummaries: list[MarketplaceRevenueShareSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRevenueAttributionAllocationsOutputTypeDef(TypedDict):
    RevenueAttributionAllocationSummaries: list[RevenueAttributionAllocationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartRevenueAttributionAllocationsTaskInputTypeDef(TypedDict):
    Catalog: CatalogNameType
    RevenueAttributionIdentifier: str
    RevenueAttributionRevision: str
    RevenueShareAllocations: Sequence[RevenueShareAllocationTypeDef]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]

class ListRevenueAttributionsOutputTypeDef(TypedDict):
    RevenueAttributionSummaries: list[AttributionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
