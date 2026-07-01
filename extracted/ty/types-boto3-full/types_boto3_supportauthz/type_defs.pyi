"""
Type annotations for supportauthz service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_supportauthz.type_defs import ActionSetOutputTypeDef

    data: ActionSetOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import SupportPermitRequestStatusType, SupportPermitStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActionSetOutputTypeDef",
    "ActionSetTypeDef",
    "ActionSummaryTypeDef",
    "ConditionOutputTypeDef",
    "ConditionTypeDef",
    "CreateSupportPermitInputTypeDef",
    "CreateSupportPermitOutputTypeDef",
    "DeleteSupportPermitInputTypeDef",
    "DeleteSupportPermitOutputTypeDef",
    "GetActionInputTypeDef",
    "GetActionOutputTypeDef",
    "GetSupportPermitInputTypeDef",
    "GetSupportPermitOutputTypeDef",
    "ListActionsInputPaginateTypeDef",
    "ListActionsInputTypeDef",
    "ListActionsOutputTypeDef",
    "ListSupportPermitRequestsInputPaginateTypeDef",
    "ListSupportPermitRequestsInputTypeDef",
    "ListSupportPermitRequestsOutputTypeDef",
    "ListSupportPermitsInputPaginateTypeDef",
    "ListSupportPermitsInputTypeDef",
    "ListSupportPermitsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PermitOutputTypeDef",
    "PermitTypeDef",
    "PermitUnionTypeDef",
    "RejectSupportPermitRequestInputTypeDef",
    "RejectSupportPermitRequestOutputTypeDef",
    "ResourceSetOutputTypeDef",
    "ResourceSetTypeDef",
    "ResponseMetadataTypeDef",
    "SigningKeyInfoTypeDef",
    "SupportPermitRequestTypeDef",
    "SupportPermitSummaryTypeDef",
    "TagResourceInputTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputTypeDef",
)

class ActionSetOutputTypeDef(TypedDict):
    allActions: NotRequired[dict[str, Any]]
    actions: NotRequired[list[str]]

class ActionSetTypeDef(TypedDict):
    allActions: NotRequired[Mapping[str, Any]]
    actions: NotRequired[Sequence[str]]

class ActionSummaryTypeDef(TypedDict):
    action: str
    service: str
    description: str

class ConditionOutputTypeDef(TypedDict):
    allowAfter: NotRequired[datetime]
    allowBefore: NotRequired[datetime]

TimestampTypeDef = Union[datetime, str]

class SigningKeyInfoTypeDef(TypedDict):
    kmsKey: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteSupportPermitInputTypeDef(TypedDict):
    supportPermitIdentifier: str

class GetActionInputTypeDef(TypedDict):
    action: str

class GetSupportPermitInputTypeDef(TypedDict):
    supportPermitIdentifier: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListActionsInputTypeDef(TypedDict):
    service: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListSupportPermitRequestsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    supportCaseDisplayId: NotRequired[str]

class ListSupportPermitsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    supportPermitStatuses: NotRequired[Sequence[SupportPermitStatusType]]

class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str

class ResourceSetOutputTypeDef(TypedDict):
    allResourcesInRegion: NotRequired[dict[str, Any]]
    resources: NotRequired[list[str]]

class ResourceSetTypeDef(TypedDict):
    allResourcesInRegion: NotRequired[Mapping[str, Any]]
    resources: NotRequired[Sequence[str]]

class RejectSupportPermitRequestInputTypeDef(TypedDict):
    requestArn: str

class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class ConditionTypeDef(TypedDict):
    allowAfter: NotRequired[TimestampTypeDef]
    allowBefore: NotRequired[TimestampTypeDef]

class GetActionOutputTypeDef(TypedDict):
    action: str
    service: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListActionsOutputTypeDef(TypedDict):
    actionSummaries: list[ActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RejectSupportPermitRequestOutputTypeDef(TypedDict):
    requestArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListActionsInputPaginateTypeDef(TypedDict):
    service: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSupportPermitRequestsInputPaginateTypeDef(TypedDict):
    supportCaseDisplayId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSupportPermitsInputPaginateTypeDef(TypedDict):
    supportPermitStatuses: NotRequired[Sequence[SupportPermitStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class PermitOutputTypeDef(TypedDict):
    actions: ActionSetOutputTypeDef
    resources: ResourceSetOutputTypeDef
    conditions: NotRequired[list[ConditionOutputTypeDef]]

class PermitTypeDef(TypedDict):
    actions: ActionSetTypeDef
    resources: ResourceSetTypeDef
    conditions: NotRequired[Sequence[ConditionTypeDef]]

class CreateSupportPermitOutputTypeDef(TypedDict):
    name: str
    arn: str
    description: str
    permit: PermitOutputTypeDef
    status: SupportPermitStatusType
    signingKeyInfo: SigningKeyInfoTypeDef
    createdAt: datetime
    supportCaseDisplayId: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteSupportPermitOutputTypeDef(TypedDict):
    name: str
    arn: str
    description: str
    permit: PermitOutputTypeDef
    status: SupportPermitStatusType
    signingKeyInfo: SigningKeyInfoTypeDef
    createdAt: datetime
    supportCaseDisplayId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSupportPermitOutputTypeDef(TypedDict):
    name: str
    arn: str
    description: str
    permit: PermitOutputTypeDef
    status: SupportPermitStatusType
    signingKeyInfo: SigningKeyInfoTypeDef
    createdAt: datetime
    supportCaseDisplayId: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SupportPermitRequestTypeDef(TypedDict):
    requestArn: str
    permit: PermitOutputTypeDef
    supportCaseDisplayId: str
    status: SupportPermitRequestStatusType
    createdAt: datetime
    updatedAt: datetime

class SupportPermitSummaryTypeDef(TypedDict):
    name: str
    arn: str
    permit: PermitOutputTypeDef
    status: SupportPermitStatusType
    signingKeyInfo: SigningKeyInfoTypeDef
    createdAt: datetime
    supportCaseDisplayId: NotRequired[str]

PermitUnionTypeDef = Union[PermitTypeDef, PermitOutputTypeDef]

class ListSupportPermitRequestsOutputTypeDef(TypedDict):
    supportPermitRequests: list[SupportPermitRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSupportPermitsOutputTypeDef(TypedDict):
    supportPermits: list[SupportPermitSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateSupportPermitInputTypeDef(TypedDict):
    permit: PermitUnionTypeDef
    name: str
    signingKeyInfo: SigningKeyInfoTypeDef
    description: NotRequired[str]
    supportCaseDisplayId: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
