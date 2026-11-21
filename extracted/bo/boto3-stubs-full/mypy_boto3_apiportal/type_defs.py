"""
Type annotations for apiportal service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apiportal/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_apiportal.type_defs import ACMManagedTypeDef

    data: ACMManagedTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    ApiSelectionModeType,
    ClassificationType,
    ConfidenceType,
    DesiredPublishStatusType,
    DiscoveryConfigurationStatusType,
    DiscoveryFailureReasonType,
    DiscoverySourceType,
    DiscoveryStatusValueType,
    EventStatusType,
    FailedItemErrorCodeType,
    FindingReasonType,
    FineGrainedAccessControlType,
    HttpMethodType,
    ManagedByType,
    PortalStatusExceptionTypeType,
    PostureStatusType,
    PreviewStatusType,
    ProductApiPageStatusExceptionTypeType,
    ProductFailureReasonType,
    ProductStatusType,
    PublishStatusType,
    ResourceOwnerType,
    RuleFilterKeyType,
    StatusType,
    TryItStateType,
    VisibilityType,
    WafStatusType,
    WorkloadType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ACMManagedTypeDef",
    "ApiIdTypeDef",
    "ApiInventoryFiltersTypeDef",
    "ApiInventoryItemDetailTypeDef",
    "ApiInventoryItemTypeDef",
    "ApiPageDisplayContentResponseTypeDef",
    "ApiPageDisplayContentTypeDef",
    "ApiSelectionConfigurationOutputTypeDef",
    "ApiSelectionConfigurationTypeDef",
    "ApiSelectionConfigurationUnionTypeDef",
    "ApiSignatureTypeDef",
    "AssociateManagedApisRequestTypeDef",
    "AssociateManagedApisResponseTypeDef",
    "AuthorizationConfigOutputTypeDef",
    "AuthorizationConfigTypeDef",
    "AuthorizationOutputTypeDef",
    "AuthorizationTypeDef",
    "AuthorizationUnionTypeDef",
    "CognitoConfigTypeDef",
    "CreateManagedApiRequestTypeDef",
    "CreateManagedApiResponseTypeDef",
    "CreatePortalPreviewRequestTypeDef",
    "CreatePortalRequestTypeDef",
    "CreatePortalResponseTypeDef",
    "CreateProductApiPageRequestTypeDef",
    "CreateProductApiPageResponseTypeDef",
    "CreateProductPageRequestTypeDef",
    "CreateProductPageResponseTypeDef",
    "CreateProductRequestTypeDef",
    "CreateProductResponseTypeDef",
    "CustomColorsTypeDef",
    "DeleteManagedApiRequestTypeDef",
    "DeletePortalRequestTypeDef",
    "DeleteProductApiPageRequestTypeDef",
    "DeleteProductPageRequestTypeDef",
    "DeleteProductRequestTypeDef",
    "DeleteProductSharingPolicyRequestTypeDef",
    "DisassociateManagedApisRequestTypeDef",
    "DisassociateManagedApisResponseTypeDef",
    "DiscoveryConfigurationDataTypeDef",
    "DiscoveryExclusionFiltersOutputTypeDef",
    "DiscoveryExclusionFiltersTypeDef",
    "DiscoveryExclusionFiltersUnionTypeDef",
    "DiscoveryInclusionFiltersOutputTypeDef",
    "DiscoveryInclusionFiltersTypeDef",
    "DiscoveryStatusTypeDef",
    "DisplayContentOverridesTypeDef",
    "DisplayContentTypeDef",
    "DisplayOrderOutputTypeDef",
    "DisplayOrderTypeDef",
    "DisplayOrderUnionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointConfigurationRequestTypeDef",
    "EndpointConfigurationResponseTypeDef",
    "FailedManagedApiItemTypeDef",
    "GetApiInventoryItemRequestTypeDef",
    "GetApiInventoryItemResponseTypeDef",
    "GetDiscoveryConfigurationResponseTypeDef",
    "GetManagedApiRequestTypeDef",
    "GetManagedApiResponseTypeDef",
    "GetOrganizationDiscoveryConfigurationResponseTypeDef",
    "GetPortalRequestTypeDef",
    "GetPortalResponseTypeDef",
    "GetProductApiPageRequestTypeDef",
    "GetProductApiPageResponseTypeDef",
    "GetProductPageRequestTypeDef",
    "GetProductPageResponseTypeDef",
    "GetProductRequestTypeDef",
    "GetProductResponseTypeDef",
    "GetProductSharingPolicyRequestTypeDef",
    "GetProductSharingPolicyResponseTypeDef",
    "IdentifierPartsTypeDef",
    "ListApiInventoryItemsRequestPaginateTypeDef",
    "ListApiInventoryItemsRequestTypeDef",
    "ListApiInventoryItemsResponseTypeDef",
    "ListDiscoveryStatusesRequestPaginateTypeDef",
    "ListDiscoveryStatusesRequestTypeDef",
    "ListDiscoveryStatusesResponseTypeDef",
    "ListManagedApiEventsRequestPaginateTypeDef",
    "ListManagedApiEventsRequestTypeDef",
    "ListManagedApiEventsResponseTypeDef",
    "ListManagedApisRequestPaginateTypeDef",
    "ListManagedApisRequestTypeDef",
    "ListManagedApisResponseTypeDef",
    "ListPortalsRequestPaginateTypeDef",
    "ListPortalsRequestTypeDef",
    "ListPortalsResponseTypeDef",
    "ListProductApiPagesRequestPaginateTypeDef",
    "ListProductApiPagesRequestTypeDef",
    "ListProductApiPagesResponseTypeDef",
    "ListProductPagesRequestPaginateTypeDef",
    "ListProductPagesRequestTypeDef",
    "ListProductPagesResponseTypeDef",
    "ListProductsRequestPaginateTypeDef",
    "ListProductsRequestTypeDef",
    "ListProductsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ManagedApiEventSummaryTypeDef",
    "ManagedApiFindingTypeDef",
    "ManagedApiSummaryTypeDef",
    "OrganizationDiscoveryConfigurationDataTypeDef",
    "OrganizationDiscoveryFiltersOutputTypeDef",
    "OrganizationDiscoveryFiltersTypeDef",
    "OrganizationDiscoveryFiltersUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PortalContentOutputTypeDef",
    "PortalContentTypeDef",
    "PortalContentUnionTypeDef",
    "PortalStatusExceptionTypeDef",
    "PortalSummaryTypeDef",
    "PortalThemeOutputTypeDef",
    "PortalThemeTypeDef",
    "PreviewTypeDef",
    "ProductApiPageStatusExceptionTypeDef",
    "ProductApiPageSummaryNoBodyTypeDef",
    "ProductPageSummaryNoBodyTypeDef",
    "ProductSummaryTypeDef",
    "PutDiscoveryConfigurationRequestTypeDef",
    "PutDiscoveryConfigurationResponseTypeDef",
    "PutOrganizationDiscoveryConfigurationRequestTypeDef",
    "PutOrganizationDiscoveryConfigurationResponseTypeDef",
    "PutProductSharingPolicyRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RuleFilterOutputTypeDef",
    "RuleFilterTypeDef",
    "SectionOutputTypeDef",
    "SectionTypeDef",
    "StartDiscoveryRequestTypeDef",
    "StopDiscoveryRequestTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdatePortalPublishStatusRequestTypeDef",
    "UpdatePortalRequestTypeDef",
    "UpdatePortalResponseTypeDef",
    "UpdateProductApiPageRequestTypeDef",
    "UpdateProductApiPageResponseTypeDef",
    "UpdateProductPageRequestTypeDef",
    "UpdateProductPageResponseTypeDef",
    "UpdateProductRequestTypeDef",
    "UpdateProductResponseTypeDef",
    "WafApiSecurityEventDetailTypeDef",
)


class ACMManagedTypeDef(TypedDict):
    domainName: str
    certificateArn: str


class IdentifierPartsTypeDef(TypedDict):
    path: str
    method: str
    resourceArn: str


class ApiInventoryFiltersTypeDef(TypedDict):
    discoverySource: NotRequired[DiscoverySourceType]
    resourceArn: NotRequired[str]


class ApiInventoryItemDetailTypeDef(TypedDict):
    method: HttpMethodType
    host: str
    port: int
    path: str
    accountId: str
    resourceArn: str
    region: str
    discoverySource: DiscoverySourceType
    visibility: NotRequired[VisibilityType]
    wafStatus: NotRequired[WafStatusType]
    classification: NotRequired[ClassificationType]
    managedBy: NotRequired[ManagedByType]
    workloads: NotRequired[list[WorkloadType]]
    managedApiId: NotRequired[str]


class ApiInventoryItemTypeDef(TypedDict):
    method: HttpMethodType
    host: str
    port: int
    path: str
    accountId: str
    resourceArn: str
    region: str
    discoverySource: DiscoverySourceType
    firstSeen: NotRequired[datetime]
    lastSeen: NotRequired[datetime]
    visibility: NotRequired[VisibilityType]
    wafStatus: NotRequired[WafStatusType]
    classification: NotRequired[ClassificationType]
    managedBy: NotRequired[ManagedByType]
    workloads: NotRequired[list[WorkloadType]]


class ApiPageDisplayContentResponseTypeDef(TypedDict):
    apiUrl: str
    operationName: NotRequired[str]
    body: NotRequired[str]


class DisplayContentOverridesTypeDef(TypedDict):
    operationName: NotRequired[str]
    apiUrl: NotRequired[str]
    body: NotRequired[str]


class RuleFilterOutputTypeDef(TypedDict):
    key: RuleFilterKeyType
    values: list[str]


class RuleFilterTypeDef(TypedDict):
    key: RuleFilterKeyType
    values: Sequence[str]


class ApiSignatureTypeDef(TypedDict):
    resourceArn: str
    method: HttpMethodType
    hostname: str
    port: int
    path: str


class AssociateManagedApisRequestTypeDef(TypedDict):
    productId: str
    managedApiIds: Sequence[str]


class FailedManagedApiItemTypeDef(TypedDict):
    managedApiId: str
    errorCode: FailedItemErrorCodeType
    errorMessage: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CognitoConfigTypeDef(TypedDict):
    userPoolArn: str
    appClientId: str
    userPoolDomain: str
    identityPoolId: NotRequired[str]


class CreatePortalPreviewRequestTypeDef(TypedDict):
    portalId: str


class EndpointConfigurationResponseTypeDef(TypedDict):
    portalDomainHostedZoneId: str
    portalDefaultDomainName: str
    domainName: NotRequired[str]
    certificateArn: NotRequired[str]


class PortalStatusExceptionTypeDef(TypedDict):
    exception: NotRequired[PortalStatusExceptionTypeType]
    message: NotRequired[str]


class ProductApiPageStatusExceptionTypeDef(TypedDict):
    exception: NotRequired[ProductApiPageStatusExceptionTypeType]
    message: NotRequired[str]


class DisplayContentTypeDef(TypedDict):
    title: str
    body: str


class CustomColorsTypeDef(TypedDict):
    backgroundColor: str
    navigationColor: str
    headerColor: str
    textColor: str
    accentColor: str
    errorValidationColor: str


class DeleteManagedApiRequestTypeDef(TypedDict):
    managedApiId: str


class DeletePortalRequestTypeDef(TypedDict):
    portalId: str


class DeleteProductApiPageRequestTypeDef(TypedDict):
    productId: str
    productApiPageId: str


class DeleteProductPageRequestTypeDef(TypedDict):
    productId: str
    productPageId: str


class DeleteProductRequestTypeDef(TypedDict):
    productId: str


class DeleteProductSharingPolicyRequestTypeDef(TypedDict):
    productId: str


class DisassociateManagedApisRequestTypeDef(TypedDict):
    productId: str
    managedApiIds: Sequence[str]


class DiscoveryConfigurationDataTypeDef(TypedDict):
    arn: str
    status: NotRequired[DiscoveryConfigurationStatusType]
    discoverySources: NotRequired[list[DiscoverySourceType]]
    excludedResources: NotRequired[list[str]]
    features: NotRequired[list[Literal["AI_DISCOVERY"]]]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class DiscoveryExclusionFiltersOutputTypeDef(TypedDict):
    organizationalUnitIds: NotRequired[list[str]]
    accountIds: NotRequired[list[str]]
    resourceArns: NotRequired[list[str]]


class DiscoveryExclusionFiltersTypeDef(TypedDict):
    organizationalUnitIds: NotRequired[Sequence[str]]
    accountIds: NotRequired[Sequence[str]]
    resourceArns: NotRequired[Sequence[str]]


class DiscoveryInclusionFiltersOutputTypeDef(TypedDict):
    organizationalUnitIds: NotRequired[list[str]]
    accountIds: NotRequired[list[str]]


class DiscoveryInclusionFiltersTypeDef(TypedDict):
    organizationalUnitIds: NotRequired[Sequence[str]]
    accountIds: NotRequired[Sequence[str]]


class DiscoveryStatusTypeDef(TypedDict):
    discoverySource: DiscoverySourceType
    status: DiscoveryStatusValueType
    accountId: NotRequired[str]
    failureReason: NotRequired[DiscoveryFailureReasonType]


class SectionOutputTypeDef(TypedDict):
    sectionName: NotRequired[str]
    productApiPageArns: NotRequired[list[str]]


class SectionTypeDef(TypedDict):
    sectionName: NotRequired[str]
    productApiPageArns: NotRequired[Sequence[str]]


class GetApiInventoryItemRequestTypeDef(TypedDict):
    method: HttpMethodType
    host: str
    port: int
    path: str
    resourceArn: str


class GetManagedApiRequestTypeDef(TypedDict):
    managedApiId: str


class ManagedApiFindingTypeDef(TypedDict):
    postureId: NotRequired[str]
    postureStatus: NotRequired[PostureStatusType]
    reason: NotRequired[FindingReasonType]
    updatedAt: NotRequired[datetime]


class GetPortalRequestTypeDef(TypedDict):
    portalId: str


class GetProductApiPageRequestTypeDef(TypedDict):
    productId: str
    productApiPageId: str
    resourceOwnerAccountId: NotRequired[str]
    includeRawDisplayContent: NotRequired[bool]


class GetProductPageRequestTypeDef(TypedDict):
    productId: str
    productPageId: str
    resourceOwnerAccountId: NotRequired[str]


class GetProductRequestTypeDef(TypedDict):
    productId: str
    resourceOwnerAccountId: NotRequired[str]


class GetProductSharingPolicyRequestTypeDef(TypedDict):
    productId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListDiscoveryStatusesRequestTypeDef(TypedDict):
    discoverySource: NotRequired[DiscoverySourceType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListManagedApisRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    productId: NotRequired[str]


class ListPortalsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListProductApiPagesRequestTypeDef(TypedDict):
    productId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    resourceOwnerAccountId: NotRequired[str]


class ListProductPagesRequestTypeDef(TypedDict):
    productId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    resourceOwnerAccountId: NotRequired[str]


class ProductPageSummaryNoBodyTypeDef(TypedDict):
    productPageId: str
    productPageArn: str
    pageTitle: str
    updatedAt: datetime


class ListProductsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    resourceOwner: NotRequired[ResourceOwnerType]
    managedApiId: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class WafApiSecurityEventDetailTypeDef(TypedDict):
    label: NotRequired[str]
    category: NotRequired[str]
    confidence: NotRequired[ConfidenceType]
    webAclArn: NotRequired[str]


class PutDiscoveryConfigurationRequestTypeDef(TypedDict):
    discoverySources: NotRequired[Sequence[DiscoverySourceType]]
    excludedResources: NotRequired[Sequence[str]]
    features: NotRequired[Sequence[Literal["AI_DISCOVERY"]]]
    tags: NotRequired[Mapping[str, str]]


class PutProductSharingPolicyRequestTypeDef(TypedDict):
    productId: str
    policyDocument: str
    tags: NotRequired[Mapping[str, str]]


StartDiscoveryRequestTypeDef = TypedDict(
    "StartDiscoveryRequestTypeDef",
    {
        "id": str,
    },
)
StopDiscoveryRequestTypeDef = TypedDict(
    "StopDiscoveryRequestTypeDef",
    {
        "id": str,
    },
)


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdatePortalPublishStatusRequestTypeDef(TypedDict):
    portalId: str
    status: DesiredPublishStatusType
    description: NotRequired[str]


class EndpointConfigurationRequestTypeDef(TypedDict):
    none: NotRequired[Mapping[str, Any]]
    acmManaged: NotRequired[ACMManagedTypeDef]


class ApiIdTypeDef(TypedDict):
    identifierParts: NotRequired[IdentifierPartsTypeDef]


class ListApiInventoryItemsRequestTypeDef(TypedDict):
    filters: NotRequired[ApiInventoryFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ApiPageDisplayContentTypeDef(TypedDict):
    none: NotRequired[Mapping[str, Any]]
    overrides: NotRequired[DisplayContentOverridesTypeDef]


class ApiSelectionConfigurationOutputTypeDef(TypedDict):
    apiSelectionMode: ApiSelectionModeType
    ruleFilters: NotRequired[list[RuleFilterOutputTypeDef]]


class ApiSelectionConfigurationTypeDef(TypedDict):
    apiSelectionMode: ApiSelectionModeType
    ruleFilters: NotRequired[Sequence[RuleFilterTypeDef]]


class CreateManagedApiRequestTypeDef(TypedDict):
    apiSignature: ApiSignatureTypeDef
    tags: NotRequired[Mapping[str, str]]


class ManagedApiSummaryTypeDef(TypedDict):
    managedApiId: str
    managedApiArn: str
    apiSignature: ApiSignatureTypeDef
    createdAt: datetime
    updatedAt: datetime


class AssociateManagedApisResponseTypeDef(TypedDict):
    failedItems: list[FailedManagedApiItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateManagedApiResponseTypeDef(TypedDict):
    managedApiId: str
    managedApiArn: str
    apiSignature: ApiSignatureTypeDef
    createdAt: datetime
    updatedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateManagedApisResponseTypeDef(TypedDict):
    failedItems: list[FailedManagedApiItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetApiInventoryItemResponseTypeDef(TypedDict):
    item: ApiInventoryItemDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetProductSharingPolicyResponseTypeDef(TypedDict):
    productId: str
    policyDocument: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListApiInventoryItemsResponseTypeDef(TypedDict):
    items: list[ApiInventoryItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class AuthorizationConfigOutputTypeDef(TypedDict):
    none: NotRequired[dict[str, Any]]
    cognitoConfig: NotRequired[CognitoConfigTypeDef]


class AuthorizationConfigTypeDef(TypedDict):
    none: NotRequired[Mapping[str, Any]]
    cognitoConfig: NotRequired[CognitoConfigTypeDef]


class PreviewTypeDef(TypedDict):
    previewStatus: PreviewStatusType
    statusException: NotRequired[PortalStatusExceptionTypeDef]
    previewUrl: NotRequired[str]


class CreateProductPageRequestTypeDef(TypedDict):
    productId: str
    displayContent: DisplayContentTypeDef
    tags: NotRequired[Mapping[str, str]]


class CreateProductPageResponseTypeDef(TypedDict):
    productPageId: str
    productPageArn: str
    displayContent: DisplayContentTypeDef
    updatedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetProductPageResponseTypeDef(TypedDict):
    productPageId: str
    productPageArn: str
    displayContent: DisplayContentTypeDef
    updatedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProductPageRequestTypeDef(TypedDict):
    productId: str
    productPageId: str
    displayContent: NotRequired[DisplayContentTypeDef]


class UpdateProductPageResponseTypeDef(TypedDict):
    productPageId: str
    productPageArn: str
    displayContent: DisplayContentTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class PortalThemeOutputTypeDef(TypedDict):
    customColors: CustomColorsTypeDef
    logoUploadedAt: NotRequired[datetime]


class GetDiscoveryConfigurationResponseTypeDef(TypedDict):
    discoveryConfiguration: DiscoveryConfigurationDataTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutDiscoveryConfigurationResponseTypeDef(TypedDict):
    discoveryConfiguration: DiscoveryConfigurationDataTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


DiscoveryExclusionFiltersUnionTypeDef = Union[
    DiscoveryExclusionFiltersTypeDef, DiscoveryExclusionFiltersOutputTypeDef
]


class OrganizationDiscoveryFiltersOutputTypeDef(TypedDict):
    exclusionFilters: NotRequired[DiscoveryExclusionFiltersOutputTypeDef]
    inclusionFilters: NotRequired[DiscoveryInclusionFiltersOutputTypeDef]


class OrganizationDiscoveryFiltersTypeDef(TypedDict):
    exclusionFilters: NotRequired[DiscoveryExclusionFiltersTypeDef]
    inclusionFilters: NotRequired[DiscoveryInclusionFiltersTypeDef]


class ListDiscoveryStatusesResponseTypeDef(TypedDict):
    items: list[DiscoveryStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DisplayOrderOutputTypeDef(TypedDict):
    overviewPageArn: NotRequired[str]
    productPageArns: NotRequired[list[str]]
    contents: NotRequired[list[SectionOutputTypeDef]]


class DisplayOrderTypeDef(TypedDict):
    overviewPageArn: NotRequired[str]
    productPageArns: NotRequired[Sequence[str]]
    contents: NotRequired[Sequence[SectionTypeDef]]


class GetManagedApiResponseTypeDef(TypedDict):
    managedApiId: str
    managedApiArn: str
    apiSignature: ApiSignatureTypeDef
    createdAt: datetime
    updatedAt: datetime
    findings: list[ManagedApiFindingTypeDef]
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListApiInventoryItemsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[ApiInventoryFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDiscoveryStatusesRequestPaginateTypeDef(TypedDict):
    discoverySource: NotRequired[DiscoverySourceType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedApisRequestPaginateTypeDef(TypedDict):
    productId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPortalsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProductApiPagesRequestPaginateTypeDef(TypedDict):
    productId: str
    resourceOwnerAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProductPagesRequestPaginateTypeDef(TypedDict):
    productId: str
    resourceOwnerAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProductsRequestPaginateTypeDef(TypedDict):
    resourceOwner: NotRequired[ResourceOwnerType]
    managedApiId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedApiEventsRequestPaginateTypeDef(TypedDict):
    managedApiId: str
    startedAfter: NotRequired[TimestampTypeDef]
    startedBefore: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedApiEventsRequestTypeDef(TypedDict):
    managedApiId: str
    startedAfter: NotRequired[TimestampTypeDef]
    startedBefore: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class PortalThemeTypeDef(TypedDict):
    customColors: CustomColorsTypeDef
    logoUploadedAt: NotRequired[TimestampTypeDef]


class ListProductPagesResponseTypeDef(TypedDict):
    items: list[ProductPageSummaryNoBodyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ManagedApiEventSummaryTypeDef(TypedDict):
    eventId: str
    eventType: NotRequired[Literal["WAF_API_SECURITY"]]
    status: NotRequired[EventStatusType]
    wafApiSecurityEventDetail: NotRequired[WafApiSecurityEventDetailTypeDef]
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class CreateProductApiPageResponseTypeDef(TypedDict):
    productApiPageId: str
    productApiPageArn: str
    apiId: ApiIdTypeDef
    displayContent: ApiPageDisplayContentResponseTypeDef
    tryItState: TryItStateType
    updatedAt: datetime
    status: StatusType
    statusException: ProductApiPageStatusExceptionTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetProductApiPageResponseTypeDef(TypedDict):
    productApiPageId: str
    productApiPageArn: str
    apiId: ApiIdTypeDef
    displayContent: ApiPageDisplayContentResponseTypeDef
    tryItState: TryItStateType
    updatedAt: datetime
    status: StatusType
    rawDisplayContent: str
    statusException: ProductApiPageStatusExceptionTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ProductApiPageSummaryNoBodyTypeDef(TypedDict):
    productApiPageId: str
    productApiPageArn: str
    apiId: ApiIdTypeDef
    apiUrl: str
    tryItState: TryItStateType
    updatedAt: datetime
    status: StatusType
    operationName: NotRequired[str]
    statusException: NotRequired[ProductApiPageStatusExceptionTypeDef]


class UpdateProductApiPageResponseTypeDef(TypedDict):
    productApiPageId: str
    productApiPageArn: str
    apiId: ApiIdTypeDef
    displayContent: ApiPageDisplayContentResponseTypeDef
    tryItState: TryItStateType
    updatedAt: datetime
    status: StatusType
    statusException: ProductApiPageStatusExceptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProductApiPageRequestTypeDef(TypedDict):
    productId: str
    managedApiId: str
    displayContent: NotRequired[ApiPageDisplayContentTypeDef]
    tryItState: NotRequired[TryItStateType]
    tags: NotRequired[Mapping[str, str]]


class UpdateProductApiPageRequestTypeDef(TypedDict):
    productId: str
    productApiPageId: str
    displayContent: NotRequired[ApiPageDisplayContentTypeDef]
    tryItState: NotRequired[TryItStateType]


class ProductSummaryTypeDef(TypedDict):
    productId: str
    productArn: str
    displayName: str
    description: str
    updatedAt: datetime
    apiSelectionConfiguration: NotRequired[ApiSelectionConfigurationOutputTypeDef]
    status: NotRequired[ProductStatusType]
    failureReason: NotRequired[ProductFailureReasonType]


ApiSelectionConfigurationUnionTypeDef = Union[
    ApiSelectionConfigurationTypeDef, ApiSelectionConfigurationOutputTypeDef
]


class ListManagedApisResponseTypeDef(TypedDict):
    items: list[ManagedApiSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AuthorizationOutputTypeDef(TypedDict):
    authorizationConfig: AuthorizationConfigOutputTypeDef
    fineGrainedAccessControl: FineGrainedAccessControlType


class AuthorizationTypeDef(TypedDict):
    authorizationConfig: AuthorizationConfigTypeDef
    fineGrainedAccessControl: FineGrainedAccessControlType


class PortalContentOutputTypeDef(TypedDict):
    displayName: str
    theme: PortalThemeOutputTypeDef
    description: NotRequired[str]


class OrganizationDiscoveryConfigurationDataTypeDef(TypedDict):
    arn: str
    status: NotRequired[DiscoveryConfigurationStatusType]
    discoverySources: NotRequired[list[DiscoverySourceType]]
    exclusionFilters: NotRequired[DiscoveryExclusionFiltersOutputTypeDef]
    discoveryFilters: NotRequired[OrganizationDiscoveryFiltersOutputTypeDef]
    features: NotRequired[list[Literal["AI_DISCOVERY"]]]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


OrganizationDiscoveryFiltersUnionTypeDef = Union[
    OrganizationDiscoveryFiltersTypeDef, OrganizationDiscoveryFiltersOutputTypeDef
]


class CreateProductResponseTypeDef(TypedDict):
    productId: str
    productArn: str
    displayName: str
    displayOrder: DisplayOrderOutputTypeDef
    description: str
    updatedAt: datetime
    tags: dict[str, str]
    apiSelectionConfiguration: ApiSelectionConfigurationOutputTypeDef
    status: ProductStatusType
    failureReason: ProductFailureReasonType
    ResponseMetadata: ResponseMetadataTypeDef


class GetProductResponseTypeDef(TypedDict):
    productId: str
    productArn: str
    displayName: str
    displayOrder: DisplayOrderOutputTypeDef
    description: str
    updatedAt: datetime
    tags: dict[str, str]
    apiSelectionConfiguration: ApiSelectionConfigurationOutputTypeDef
    status: ProductStatusType
    failureReason: ProductFailureReasonType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProductResponseTypeDef(TypedDict):
    productId: str
    productArn: str
    displayName: str
    displayOrder: DisplayOrderOutputTypeDef
    description: str
    updatedAt: datetime
    apiSelectionConfiguration: ApiSelectionConfigurationOutputTypeDef
    status: ProductStatusType
    failureReason: ProductFailureReasonType
    ResponseMetadata: ResponseMetadataTypeDef


DisplayOrderUnionTypeDef = Union[DisplayOrderTypeDef, DisplayOrderOutputTypeDef]


class PortalContentTypeDef(TypedDict):
    displayName: str
    theme: PortalThemeTypeDef
    description: NotRequired[str]


class ListManagedApiEventsResponseTypeDef(TypedDict):
    items: list[ManagedApiEventSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProductApiPagesResponseTypeDef(TypedDict):
    items: list[ProductApiPageSummaryNoBodyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProductsResponseTypeDef(TypedDict):
    items: list[ProductSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateProductRequestTypeDef(TypedDict):
    displayName: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    apiSelectionConfiguration: NotRequired[ApiSelectionConfigurationUnionTypeDef]


AuthorizationUnionTypeDef = Union[AuthorizationTypeDef, AuthorizationOutputTypeDef]


class CreatePortalResponseTypeDef(TypedDict):
    portalId: str
    portalArn: str
    endpointConfiguration: EndpointConfigurationResponseTypeDef
    authorization: AuthorizationOutputTypeDef
    portalContent: PortalContentOutputTypeDef
    includedProductArns: list[str]
    publishStatus: PublishStatusType
    statusException: PortalStatusExceptionTypeDef
    updatedAt: datetime
    publishedAt: datetime
    publishDescription: str
    rumAppMonitorName: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetPortalResponseTypeDef(TypedDict):
    portalId: str
    portalArn: str
    endpointConfiguration: EndpointConfigurationResponseTypeDef
    authorization: AuthorizationOutputTypeDef
    portalContent: PortalContentOutputTypeDef
    includedProductArns: list[str]
    publishStatus: PublishStatusType
    statusException: PortalStatusExceptionTypeDef
    updatedAt: datetime
    publishedAt: datetime
    publishDescription: str
    rumAppMonitorName: str
    preview: PreviewTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PortalSummaryTypeDef(TypedDict):
    portalId: str
    portalArn: str
    endpointConfiguration: EndpointConfigurationResponseTypeDef
    authorization: AuthorizationOutputTypeDef
    portalContent: PortalContentOutputTypeDef
    includedProductArns: list[str]
    updatedAt: datetime
    publishStatus: NotRequired[PublishStatusType]
    statusException: NotRequired[PortalStatusExceptionTypeDef]
    publishedAt: NotRequired[datetime]
    publishDescription: NotRequired[str]
    rumAppMonitorName: NotRequired[str]
    preview: NotRequired[PreviewTypeDef]


class UpdatePortalResponseTypeDef(TypedDict):
    portalId: str
    portalArn: str
    endpointConfiguration: EndpointConfigurationResponseTypeDef
    authorization: AuthorizationOutputTypeDef
    portalContent: PortalContentOutputTypeDef
    includedProductArns: list[str]
    publishStatus: PublishStatusType
    statusException: PortalStatusExceptionTypeDef
    updatedAt: datetime
    publishedAt: datetime
    publishDescription: str
    rumAppMonitorName: str
    preview: PreviewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOrganizationDiscoveryConfigurationResponseTypeDef(TypedDict):
    discoveryConfiguration: OrganizationDiscoveryConfigurationDataTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutOrganizationDiscoveryConfigurationResponseTypeDef(TypedDict):
    discoveryConfiguration: OrganizationDiscoveryConfigurationDataTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutOrganizationDiscoveryConfigurationRequestTypeDef(TypedDict):
    discoverySources: NotRequired[Sequence[DiscoverySourceType]]
    exclusionFilters: NotRequired[DiscoveryExclusionFiltersUnionTypeDef]
    discoveryFilters: NotRequired[OrganizationDiscoveryFiltersUnionTypeDef]
    features: NotRequired[Sequence[Literal["AI_DISCOVERY"]]]
    tags: NotRequired[Mapping[str, str]]


class UpdateProductRequestTypeDef(TypedDict):
    productId: str
    displayName: NotRequired[str]
    description: NotRequired[str]
    displayOrder: NotRequired[DisplayOrderUnionTypeDef]
    apiSelectionConfiguration: NotRequired[ApiSelectionConfigurationUnionTypeDef]


PortalContentUnionTypeDef = Union[PortalContentTypeDef, PortalContentOutputTypeDef]


class ListPortalsResponseTypeDef(TypedDict):
    items: list[PortalSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreatePortalRequestTypeDef(TypedDict):
    portalContent: PortalContentUnionTypeDef
    endpointConfiguration: EndpointConfigurationRequestTypeDef
    authorization: AuthorizationUnionTypeDef
    includedProductArns: NotRequired[Sequence[str]]
    logoUri: NotRequired[str]
    rumAppMonitorName: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdatePortalRequestTypeDef(TypedDict):
    portalId: str
    portalContent: NotRequired[PortalContentUnionTypeDef]
    endpointConfiguration: NotRequired[EndpointConfigurationRequestTypeDef]
    authorization: NotRequired[AuthorizationUnionTypeDef]
    rumAppMonitorName: NotRequired[str]
    includedProductArns: NotRequired[Sequence[str]]
    logoUri: NotRequired[str]
