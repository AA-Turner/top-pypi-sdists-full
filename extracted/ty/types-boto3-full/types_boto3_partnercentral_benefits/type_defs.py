"""
Type annotations for partnercentral-benefits service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_benefits/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_partnercentral_benefits.type_defs import AccessDetailsTypeDef

    data: AccessDetailsTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from .literals import (
    BenefitAllocationStatusType,
    BenefitApplicationStatusType,
    BenefitStatusType,
    CurrencyCodeType,
    FileTypeType,
    FulfillmentTypeType,
    ResourceTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccessDetailsTypeDef",
    "AmendBenefitApplicationInputTypeDef",
    "AmendmentTypeDef",
    "AssociateBenefitApplicationResourceInputTypeDef",
    "AssociateBenefitApplicationResourceOutputTypeDef",
    "AssociatedResourceTypeDef",
    "BenefitAllocationSummaryTypeDef",
    "BenefitApplicationSummaryTypeDef",
    "BenefitSummaryTypeDef",
    "CancelBenefitApplicationInputTypeDef",
    "ConsumableDetailsTypeDef",
    "ContactTypeDef",
    "CreateBenefitApplicationInputTypeDef",
    "CreateBenefitApplicationOutputTypeDef",
    "CreditCodeTypeDef",
    "CreditDetailsTypeDef",
    "DisassociateBenefitApplicationResourceInputTypeDef",
    "DisassociateBenefitApplicationResourceOutputTypeDef",
    "DisbursementDetailsTypeDef",
    "FileDetailTypeDef",
    "FileInputTypeDef",
    "FulfillmentDetailsTypeDef",
    "GetBenefitAllocationInputTypeDef",
    "GetBenefitAllocationOutputTypeDef",
    "GetBenefitApplicationInputTypeDef",
    "GetBenefitApplicationOutputTypeDef",
    "GetBenefitInputTypeDef",
    "GetBenefitOutputTypeDef",
    "IssuanceDetailTypeDef",
    "ListBenefitAllocationsInputPaginateTypeDef",
    "ListBenefitAllocationsInputTypeDef",
    "ListBenefitAllocationsOutputTypeDef",
    "ListBenefitApplicationsInputPaginateTypeDef",
    "ListBenefitApplicationsInputTypeDef",
    "ListBenefitApplicationsOutputTypeDef",
    "ListBenefitsInputPaginateTypeDef",
    "ListBenefitsInputTypeDef",
    "ListBenefitsOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MonetaryValueTypeDef",
    "PaginatorConfigTypeDef",
    "RecallBenefitApplicationInputTypeDef",
    "ResponseMetadataTypeDef",
    "SubmitBenefitApplicationInputTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateBenefitApplicationInputTypeDef",
    "UpdateBenefitApplicationOutputTypeDef",
)


class AccessDetailsTypeDef(TypedDict):
    Description: NotRequired[str]


class AmendmentTypeDef(TypedDict):
    FieldPath: str
    NewValue: str


class AssociateBenefitApplicationResourceInputTypeDef(TypedDict):
    Catalog: str
    BenefitApplicationIdentifier: str
    ResourceArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssociatedResourceTypeDef(TypedDict):
    ResourceType: NotRequired[ResourceTypeType]
    ResourceIdentifier: NotRequired[str]
    ResourceArn: NotRequired[str]


class BenefitAllocationSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Catalog: NotRequired[str]
    Arn: NotRequired[str]
    Status: NotRequired[BenefitAllocationStatusType]
    StatusReason: NotRequired[str]
    Name: NotRequired[str]
    BenefitId: NotRequired[str]
    BenefitApplicationId: NotRequired[str]
    FulfillmentTypes: NotRequired[list[FulfillmentTypeType]]
    CreatedAt: NotRequired[datetime]
    ExpiresAt: NotRequired[datetime]
    ApplicableBenefitIds: NotRequired[list[str]]


class BenefitApplicationSummaryTypeDef(TypedDict):
    Catalog: NotRequired[str]
    Name: NotRequired[str]
    Id: NotRequired[str]
    Arn: NotRequired[str]
    BenefitId: NotRequired[str]
    Programs: NotRequired[list[str]]
    FulfillmentTypes: NotRequired[list[FulfillmentTypeType]]
    Status: NotRequired[BenefitApplicationStatusType]
    Stage: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]
    BenefitApplicationDetails: NotRequired[dict[str, str]]
    AssociatedResources: NotRequired[list[str]]


class BenefitSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Catalog: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Programs: NotRequired[list[str]]
    FulfillmentTypes: NotRequired[list[FulfillmentTypeType]]
    Status: NotRequired[BenefitStatusType]


class CancelBenefitApplicationInputTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Identifier: str
    Reason: NotRequired[str]


class MonetaryValueTypeDef(TypedDict):
    Amount: str
    CurrencyCode: CurrencyCodeType


class ContactTypeDef(TypedDict):
    Email: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    BusinessTitle: NotRequired[str]
    Phone: NotRequired[str]


class FileInputTypeDef(TypedDict):
    FileURI: str
    BusinessUseCase: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class DisassociateBenefitApplicationResourceInputTypeDef(TypedDict):
    Catalog: str
    BenefitApplicationIdentifier: str
    ResourceArn: str


class FileDetailTypeDef(TypedDict):
    FileURI: str
    BusinessUseCase: NotRequired[str]
    FileName: NotRequired[str]
    FileStatus: NotRequired[str]
    FileStatusReason: NotRequired[str]
    FileType: NotRequired[FileTypeType]
    CreatedBy: NotRequired[str]
    CreatedAt: NotRequired[datetime]


class GetBenefitAllocationInputTypeDef(TypedDict):
    Catalog: str
    Identifier: str


class GetBenefitApplicationInputTypeDef(TypedDict):
    Catalog: str
    Identifier: str


class GetBenefitInputTypeDef(TypedDict):
    Catalog: str
    Identifier: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListBenefitAllocationsInputTypeDef(TypedDict):
    Catalog: str
    FulfillmentTypes: NotRequired[Sequence[FulfillmentTypeType]]
    BenefitIdentifiers: NotRequired[Sequence[str]]
    BenefitApplicationIdentifiers: NotRequired[Sequence[str]]
    Status: NotRequired[Sequence[BenefitAllocationStatusType]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListBenefitsInputTypeDef(TypedDict):
    Catalog: str
    Programs: NotRequired[Sequence[str]]
    FulfillmentTypes: NotRequired[Sequence[FulfillmentTypeType]]
    Status: NotRequired[Sequence[BenefitStatusType]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class RecallBenefitApplicationInputTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    Reason: str
    ClientToken: NotRequired[str]


class SubmitBenefitApplicationInputTypeDef(TypedDict):
    Catalog: str
    Identifier: str


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class AmendBenefitApplicationInputTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Revision: str
    Identifier: str
    AmendmentReason: str
    Amendments: Sequence[AmendmentTypeDef]


class AssociateBenefitApplicationResourceOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    Revision: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBenefitApplicationOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    Revision: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateBenefitApplicationResourceOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    Revision: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetBenefitOutputTypeDef(TypedDict):
    Id: str
    Catalog: str
    Arn: str
    Name: str
    Description: str
    Programs: list[str]
    FulfillmentTypes: list[FulfillmentTypeType]
    BenefitRequestSchema: dict[str, Any]
    Status: BenefitStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBenefitApplicationOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    Revision: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListBenefitApplicationsInputTypeDef(TypedDict):
    Catalog: str
    Programs: NotRequired[Sequence[str]]
    FulfillmentTypes: NotRequired[Sequence[FulfillmentTypeType]]
    BenefitIdentifiers: NotRequired[Sequence[str]]
    Status: NotRequired[Sequence[BenefitApplicationStatusType]]
    Stages: NotRequired[Sequence[str]]
    AssociatedResources: NotRequired[Sequence[AssociatedResourceTypeDef]]
    AssociatedResourceArns: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListBenefitAllocationsOutputTypeDef(TypedDict):
    BenefitAllocationSummaries: list[BenefitAllocationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBenefitApplicationsOutputTypeDef(TypedDict):
    BenefitApplicationSummaries: list[BenefitApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBenefitsOutputTypeDef(TypedDict):
    BenefitSummaries: list[BenefitSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreditCodeTypeDef(TypedDict):
    AwsAccountId: str
    Value: MonetaryValueTypeDef
    AwsCreditCode: str
    Status: BenefitAllocationStatusType
    IssuedAt: datetime
    ExpiresAt: datetime


class IssuanceDetailTypeDef(TypedDict):
    IssuanceId: NotRequired[str]
    IssuanceAmount: NotRequired[MonetaryValueTypeDef]
    IssuedAt: NotRequired[datetime]


class UpdateBenefitApplicationInputTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Identifier: str
    Revision: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    BenefitApplicationDetails: NotRequired[Mapping[str, Any]]
    PartnerContacts: NotRequired[Sequence[ContactTypeDef]]
    FileDetails: NotRequired[Sequence[FileInputTypeDef]]


class CreateBenefitApplicationInputTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    BenefitIdentifier: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    FulfillmentTypes: NotRequired[Sequence[FulfillmentTypeType]]
    BenefitApplicationDetails: NotRequired[Mapping[str, Any]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    AssociatedResources: NotRequired[Sequence[str]]
    PartnerContacts: NotRequired[Sequence[ContactTypeDef]]
    FileDetails: NotRequired[Sequence[FileInputTypeDef]]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class GetBenefitApplicationOutputTypeDef(TypedDict):
    Id: str
    Arn: str
    Catalog: str
    BenefitId: str
    Name: str
    Description: str
    FulfillmentTypes: list[FulfillmentTypeType]
    BenefitApplicationDetails: dict[str, Any]
    Programs: list[str]
    Status: BenefitApplicationStatusType
    Stage: str
    StatusReason: str
    StatusReasonCode: str
    StatusReasonCodes: list[str]
    CreatedAt: datetime
    UpdatedAt: datetime
    Revision: str
    AssociatedResources: list[str]
    PartnerContacts: list[ContactTypeDef]
    FileDetails: list[FileDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBenefitAllocationsInputPaginateTypeDef(TypedDict):
    Catalog: str
    FulfillmentTypes: NotRequired[Sequence[FulfillmentTypeType]]
    BenefitIdentifiers: NotRequired[Sequence[str]]
    BenefitApplicationIdentifiers: NotRequired[Sequence[str]]
    Status: NotRequired[Sequence[BenefitAllocationStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBenefitApplicationsInputPaginateTypeDef(TypedDict):
    Catalog: str
    Programs: NotRequired[Sequence[str]]
    FulfillmentTypes: NotRequired[Sequence[FulfillmentTypeType]]
    BenefitIdentifiers: NotRequired[Sequence[str]]
    Status: NotRequired[Sequence[BenefitApplicationStatusType]]
    Stages: NotRequired[Sequence[str]]
    AssociatedResources: NotRequired[Sequence[AssociatedResourceTypeDef]]
    AssociatedResourceArns: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBenefitsInputPaginateTypeDef(TypedDict):
    Catalog: str
    Programs: NotRequired[Sequence[str]]
    FulfillmentTypes: NotRequired[Sequence[FulfillmentTypeType]]
    Status: NotRequired[Sequence[BenefitStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class CreditDetailsTypeDef(TypedDict):
    AllocatedAmount: MonetaryValueTypeDef
    IssuedAmount: MonetaryValueTypeDef
    Codes: list[CreditCodeTypeDef]


class ConsumableDetailsTypeDef(TypedDict):
    AllocatedAmount: NotRequired[MonetaryValueTypeDef]
    RemainingAmount: NotRequired[MonetaryValueTypeDef]
    UtilizedAmount: NotRequired[MonetaryValueTypeDef]
    IssuanceDetails: NotRequired[IssuanceDetailTypeDef]


class DisbursementDetailsTypeDef(TypedDict):
    DisbursedAmount: NotRequired[MonetaryValueTypeDef]
    IssuanceDetails: NotRequired[IssuanceDetailTypeDef]


class FulfillmentDetailsTypeDef(TypedDict):
    DisbursementDetails: NotRequired[DisbursementDetailsTypeDef]
    ConsumableDetails: NotRequired[ConsumableDetailsTypeDef]
    CreditDetails: NotRequired[CreditDetailsTypeDef]
    AccessDetails: NotRequired[AccessDetailsTypeDef]


class GetBenefitAllocationOutputTypeDef(TypedDict):
    Id: str
    Catalog: str
    Arn: str
    Name: str
    Description: str
    Status: BenefitAllocationStatusType
    StatusReason: str
    BenefitApplicationId: str
    BenefitId: str
    FulfillmentType: FulfillmentTypeType
    ApplicableBenefitIds: list[str]
    FulfillmentDetail: FulfillmentDetailsTypeDef
    CreatedAt: datetime
    UpdatedAt: datetime
    StartsAt: datetime
    ExpiresAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef
