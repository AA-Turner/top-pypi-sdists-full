"""
Type annotations for account-access service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_account_access.type_defs import ApplicationSummaryTypeDef

    data: ApplicationSummaryTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime

from .literals import ErrorCodeType, StatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ApplicationSummaryTypeDef",
    "CreateApplicationRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateEntitlementRequestTypeDef",
    "CreateEntitlementResponseTypeDef",
    "DeleteApplicationRequestTypeDef",
    "DeleteEntitlementRequestTypeDef",
    "EntitlementDetailsTypeDef",
    "EntitlementFilterTypeDef",
    "EntitlementSummaryTypeDef",
    "EntitlementTypeDef",
    "EntitlementsListMemberTypeDef",
    "ErrorDetailsTypeDef",
    "GetApplicationRequestTypeDef",
    "GetApplicationRequestWaitTypeDef",
    "GetApplicationResponseTypeDef",
    "GetEntitlementRequestTypeDef",
    "GetEntitlementResponseTypeDef",
    "IdentityCenterDetailsTypeDef",
    "IdentityCenterPrincipalFilterTypeDef",
    "IdentityCenterPrincipalTypeDef",
    "IdentityCenterTypeDef",
    "IdentitySourceDetailsTypeDef",
    "IdentitySourceTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListEntitlementsRequestPaginateTypeDef",
    "ListEntitlementsRequestTypeDef",
    "ListEntitlementsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PrincipalFilterTypeDef",
    "PrincipalRoleEntitlementDetailsTypeDef",
    "PrincipalRoleEntitlementFilterTypeDef",
    "PrincipalRoleEntitlementSummaryTypeDef",
    "PrincipalRoleEntitlementTypeDef",
    "PrincipalTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "WaiterConfigTypeDef",
)

class ApplicationSummaryTypeDef(TypedDict):
    applicationArn: str
    createdAt: datetime
    updatedAt: datetime
    tenantId: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteApplicationRequestTypeDef(TypedDict):
    applicationArn: str

class DeleteEntitlementRequestTypeDef(TypedDict):
    applicationArn: str
    entitlementId: str

class ErrorDetailsTypeDef(TypedDict):
    code: ErrorCodeType
    message: str

class GetApplicationRequestTypeDef(TypedDict):
    applicationArn: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetEntitlementRequestTypeDef(TypedDict):
    applicationArn: str
    entitlementId: str

class IdentityCenterDetailsTypeDef(TypedDict):
    instanceArn: str
    applicationArn: NotRequired[str]

class IdentityCenterPrincipalFilterTypeDef(TypedDict):
    userId: NotRequired[str]
    groupId: NotRequired[str]

class IdentityCenterPrincipalTypeDef(TypedDict):
    userId: NotRequired[str]
    groupId: NotRequired[str]

class IdentityCenterTypeDef(TypedDict):
    instanceArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListApplicationsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class CreateApplicationResponseTypeDef(TypedDict):
    applicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEntitlementResponseTypeDef(TypedDict):
    entitlementId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationsResponseTypeDef(TypedDict):
    applications: list[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationRequestWaitTypeDef(TypedDict):
    applicationArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class IdentitySourceDetailsTypeDef(TypedDict):
    identityCenter: NotRequired[IdentityCenterDetailsTypeDef]

class PrincipalFilterTypeDef(TypedDict):
    identityCenter: NotRequired[IdentityCenterPrincipalFilterTypeDef]

class PrincipalTypeDef(TypedDict):
    identityCenter: NotRequired[IdentityCenterPrincipalTypeDef]

class IdentitySourceTypeDef(TypedDict):
    identityCenter: NotRequired[IdentityCenterTypeDef]

class ListApplicationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetApplicationResponseTypeDef(TypedDict):
    identitySource: IdentitySourceDetailsTypeDef
    status: StatusType
    tenantId: str
    createdAt: datetime
    updatedAt: datetime
    tags: dict[str, str]
    error: ErrorDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PrincipalRoleEntitlementFilterTypeDef(TypedDict):
    principal: NotRequired[PrincipalFilterTypeDef]
    roleArn: NotRequired[str]
    account: NotRequired[str]

class PrincipalRoleEntitlementDetailsTypeDef(TypedDict):
    principal: PrincipalTypeDef
    roleArn: str
    account: str
    accountName: NotRequired[str]

class PrincipalRoleEntitlementSummaryTypeDef(TypedDict):
    principal: PrincipalTypeDef
    roleArn: str
    account: str
    accountName: NotRequired[str]

class PrincipalRoleEntitlementTypeDef(TypedDict):
    principal: PrincipalTypeDef
    roleArn: str

class CreateApplicationRequestTypeDef(TypedDict):
    identitySource: IdentitySourceTypeDef
    tags: NotRequired[Mapping[str, str]]

class EntitlementFilterTypeDef(TypedDict):
    principalRole: NotRequired[PrincipalRoleEntitlementFilterTypeDef]

class EntitlementDetailsTypeDef(TypedDict):
    principalRole: NotRequired[PrincipalRoleEntitlementDetailsTypeDef]

class EntitlementSummaryTypeDef(TypedDict):
    principalRole: NotRequired[PrincipalRoleEntitlementSummaryTypeDef]

class EntitlementTypeDef(TypedDict):
    principalRole: NotRequired[PrincipalRoleEntitlementTypeDef]

ListEntitlementsRequestPaginateTypeDef = TypedDict(
    "ListEntitlementsRequestPaginateTypeDef",
    {
        "applicationArn": str,
        "filter": EntitlementFilterTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListEntitlementsRequestTypeDef = TypedDict(
    "ListEntitlementsRequestTypeDef",
    {
        "applicationArn": str,
        "filter": EntitlementFilterTypeDef,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class GetEntitlementResponseTypeDef(TypedDict):
    applicationArn: str
    entitlementId: str
    entitlement: EntitlementDetailsTypeDef
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EntitlementsListMemberTypeDef(TypedDict):
    entitlementId: str
    entitlement: EntitlementSummaryTypeDef
    createdAt: datetime

class CreateEntitlementRequestTypeDef(TypedDict):
    applicationArn: str
    entitlement: EntitlementTypeDef

class ListEntitlementsResponseTypeDef(TypedDict):
    entitlements: list[EntitlementsListMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
