"""
Type annotations for pricing-plan-manager service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing_plan_manager/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_pricing_plan_manager.type_defs import ApprovePaidSubscriptionInputTypeDef

    data: ApprovePaidSubscriptionInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime

from .literals import ApprovalModeType, ScheduledChangeTypeType, StatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ApprovePaidSubscriptionInputTypeDef",
    "ApprovePaidSubscriptionOutputTypeDef",
    "AssociateResourcesToSubscriptionInputTypeDef",
    "AssociateResourcesToSubscriptionOutputTypeDef",
    "CancelSubscriptionChangeInputTypeDef",
    "CancelSubscriptionChangeOutputTypeDef",
    "CancelSubscriptionInputTypeDef",
    "CancelSubscriptionOutputTypeDef",
    "CreateSubscriptionInputTypeDef",
    "CreateSubscriptionOutputTypeDef",
    "DisassociateResourcesFromSubscriptionInputTypeDef",
    "DisassociateResourcesFromSubscriptionOutputTypeDef",
    "GetSubscriptionInputTypeDef",
    "GetSubscriptionOutputTypeDef",
    "ListSubscriptionsInputPaginateTypeDef",
    "ListSubscriptionsInputTypeDef",
    "ListSubscriptionsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "ScheduledChangeTypeDef",
    "SubscriptionSummaryTypeDef",
    "SubscriptionTypeDef",
    "UpdateSubscriptionInputTypeDef",
    "UpdateSubscriptionOutputTypeDef",
)

class ApprovePaidSubscriptionInputTypeDef(TypedDict):
    arn: str
    ifMatch: str
    clientToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociateResourcesToSubscriptionInputTypeDef(TypedDict):
    arn: str
    resourceArns: Sequence[str]
    ifMatch: str
    clientToken: NotRequired[str]

class CancelSubscriptionChangeInputTypeDef(TypedDict):
    arn: str
    ifMatch: str
    clientToken: NotRequired[str]

class CancelSubscriptionInputTypeDef(TypedDict):
    arn: str
    ifMatch: str
    clientToken: NotRequired[str]

class CreateSubscriptionInputTypeDef(TypedDict):
    planFamily: str
    planTier: str
    resourceArns: Sequence[str]
    usageLevel: NotRequired[str]
    approvalMode: NotRequired[ApprovalModeType]
    clientToken: NotRequired[str]

class DisassociateResourcesFromSubscriptionInputTypeDef(TypedDict):
    arn: str
    resourceArns: Sequence[str]
    ifMatch: str
    clientToken: NotRequired[str]

class GetSubscriptionInputTypeDef(TypedDict):
    arn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListSubscriptionsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]

class ScheduledChangeTypeDef(TypedDict):
    changeType: ScheduledChangeTypeType
    effectiveDate: NotRequired[datetime]
    planTier: NotRequired[str]
    usageLevel: NotRequired[str]

class UpdateSubscriptionInputTypeDef(TypedDict):
    arn: str
    planTier: str
    ifMatch: str
    usageLevel: NotRequired[str]
    clientToken: NotRequired[str]

class ListSubscriptionsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SubscriptionSummaryTypeDef(TypedDict):
    arn: str
    planFamily: str
    planTier: str
    status: StatusType
    resourceArns: list[str]
    createdAt: datetime
    updatedAt: datetime
    eTag: str
    usageLevel: NotRequired[str]
    scheduledChange: NotRequired[ScheduledChangeTypeDef]
    statusReason: NotRequired[str]

class SubscriptionTypeDef(TypedDict):
    arn: str
    planFamily: str
    planTier: str
    status: StatusType
    resourceArns: list[str]
    createdAt: datetime
    updatedAt: datetime
    usageLevel: NotRequired[str]
    scheduledChange: NotRequired[ScheduledChangeTypeDef]
    statusReason: NotRequired[str]

class ListSubscriptionsOutputTypeDef(TypedDict):
    subscriptionSummaries: list[SubscriptionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ApprovePaidSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateResourcesToSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class CancelSubscriptionChangeOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class CancelSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateResourcesFromSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSubscriptionOutputTypeDef(TypedDict):
    subscription: SubscriptionTypeDef
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef
