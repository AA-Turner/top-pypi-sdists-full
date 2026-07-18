"""
Type annotations for grafana service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_grafana/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_grafana.type_defs import AssertionAttributesTypeDef

    data: AssertionAttributesTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AccountAccessTypeType,
    AuthenticationProviderTypesType,
    DataSourceTypeType,
    IPAddressTypeType,
    LicenseTypeType,
    PermissionTypeType,
    RoleType,
    SamlConfigurationStatusType,
    UpdateActionType,
    UserTypeType,
    WorkspaceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AssertionAttributesTypeDef",
    "AssociateLicenseRequestTypeDef",
    "AssociateLicenseResponseTypeDef",
    "AuthenticationDescriptionTypeDef",
    "AuthenticationSummaryTypeDef",
    "AwsSsoAuthenticationTypeDef",
    "CreateWorkspaceApiKeyRequestTypeDef",
    "CreateWorkspaceApiKeyResponseTypeDef",
    "CreateWorkspaceRequestTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "CreateWorkspaceServiceAccountRequestTypeDef",
    "CreateWorkspaceServiceAccountResponseTypeDef",
    "CreateWorkspaceServiceAccountTokenRequestTypeDef",
    "CreateWorkspaceServiceAccountTokenResponseTypeDef",
    "DeleteWorkspaceApiKeyRequestTypeDef",
    "DeleteWorkspaceApiKeyResponseTypeDef",
    "DeleteWorkspaceRequestTypeDef",
    "DeleteWorkspaceResponseTypeDef",
    "DeleteWorkspaceServiceAccountRequestTypeDef",
    "DeleteWorkspaceServiceAccountResponseTypeDef",
    "DeleteWorkspaceServiceAccountTokenRequestTypeDef",
    "DeleteWorkspaceServiceAccountTokenResponseTypeDef",
    "DescribeWorkspaceAuthenticationRequestTypeDef",
    "DescribeWorkspaceAuthenticationResponseTypeDef",
    "DescribeWorkspaceConfigurationRequestTypeDef",
    "DescribeWorkspaceConfigurationResponseTypeDef",
    "DescribeWorkspaceRequestTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "DisassociateLicenseRequestTypeDef",
    "DisassociateLicenseResponseTypeDef",
    "IdpMetadataTypeDef",
    "ListPermissionsRequestPaginateTypeDef",
    "ListPermissionsRequestTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVersionsRequestPaginateTypeDef",
    "ListVersionsRequestTypeDef",
    "ListVersionsResponseTypeDef",
    "ListWorkspaceServiceAccountTokensRequestPaginateTypeDef",
    "ListWorkspaceServiceAccountTokensRequestTypeDef",
    "ListWorkspaceServiceAccountTokensResponseTypeDef",
    "ListWorkspaceServiceAccountsRequestPaginateTypeDef",
    "ListWorkspaceServiceAccountsRequestTypeDef",
    "ListWorkspaceServiceAccountsResponseTypeDef",
    "ListWorkspacesRequestPaginateTypeDef",
    "ListWorkspacesRequestTypeDef",
    "ListWorkspacesResponseTypeDef",
    "NetworkAccessConfigurationOutputTypeDef",
    "NetworkAccessConfigurationTypeDef",
    "NetworkAccessConfigurationUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionEntryTypeDef",
    "ResponseMetadataTypeDef",
    "RoleValuesOutputTypeDef",
    "RoleValuesTypeDef",
    "SamlAuthenticationTypeDef",
    "SamlConfigurationOutputTypeDef",
    "SamlConfigurationTypeDef",
    "SamlConfigurationUnionTypeDef",
    "ServiceAccountSummaryTypeDef",
    "ServiceAccountTokenSummaryTypeDef",
    "ServiceAccountTokenSummaryWithKeyTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateErrorTypeDef",
    "UpdateInstructionOutputTypeDef",
    "UpdateInstructionTypeDef",
    "UpdateInstructionUnionTypeDef",
    "UpdatePermissionsRequestTypeDef",
    "UpdatePermissionsResponseTypeDef",
    "UpdateWorkspaceAuthenticationRequestTypeDef",
    "UpdateWorkspaceAuthenticationResponseTypeDef",
    "UpdateWorkspaceConfigurationRequestTypeDef",
    "UpdateWorkspaceRequestTypeDef",
    "UpdateWorkspaceResponseTypeDef",
    "UserTypeDef",
    "VpcConfigurationOutputTypeDef",
    "VpcConfigurationTypeDef",
    "VpcConfigurationUnionTypeDef",
    "WorkspaceDescriptionTypeDef",
    "WorkspaceSummaryTypeDef",
)


class AssertionAttributesTypeDef(TypedDict):
    name: NotRequired[str]
    login: NotRequired[str]
    email: NotRequired[str]
    groups: NotRequired[str]
    role: NotRequired[str]
    org: NotRequired[str]


class AssociateLicenseRequestTypeDef(TypedDict):
    workspaceId: str
    licenseType: LicenseTypeType
    grafanaToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AwsSsoAuthenticationTypeDef(TypedDict):
    ssoClientId: NotRequired[str]


class AuthenticationSummaryTypeDef(TypedDict):
    providers: list[AuthenticationProviderTypesType]
    samlConfigurationStatus: NotRequired[SamlConfigurationStatusType]


class CreateWorkspaceApiKeyRequestTypeDef(TypedDict):
    keyName: str
    keyRole: str
    secondsToLive: int
    workspaceId: str


class CreateWorkspaceServiceAccountRequestTypeDef(TypedDict):
    name: str
    grafanaRole: RoleType
    workspaceId: str


class CreateWorkspaceServiceAccountTokenRequestTypeDef(TypedDict):
    name: str
    secondsToLive: int
    serviceAccountId: str
    workspaceId: str


ServiceAccountTokenSummaryWithKeyTypeDef = TypedDict(
    "ServiceAccountTokenSummaryWithKeyTypeDef",
    {
        "id": str,
        "name": str,
        "key": str,
    },
)


class DeleteWorkspaceApiKeyRequestTypeDef(TypedDict):
    keyName: str
    workspaceId: str


class DeleteWorkspaceRequestTypeDef(TypedDict):
    workspaceId: str


class DeleteWorkspaceServiceAccountRequestTypeDef(TypedDict):
    serviceAccountId: str
    workspaceId: str


class DeleteWorkspaceServiceAccountTokenRequestTypeDef(TypedDict):
    tokenId: str
    serviceAccountId: str
    workspaceId: str


class DescribeWorkspaceAuthenticationRequestTypeDef(TypedDict):
    workspaceId: str


class DescribeWorkspaceConfigurationRequestTypeDef(TypedDict):
    workspaceId: str


class DescribeWorkspaceRequestTypeDef(TypedDict):
    workspaceId: str


class DisassociateLicenseRequestTypeDef(TypedDict):
    workspaceId: str
    licenseType: LicenseTypeType


class IdpMetadataTypeDef(TypedDict):
    url: NotRequired[str]
    xml: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListPermissionsRequestTypeDef(TypedDict):
    workspaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    userType: NotRequired[UserTypeType]
    userId: NotRequired[str]
    groupId: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class ListVersionsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    workspaceId: NotRequired[str]


class ListWorkspaceServiceAccountTokensRequestTypeDef(TypedDict):
    serviceAccountId: str
    workspaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ServiceAccountTokenSummaryTypeDef = TypedDict(
    "ServiceAccountTokenSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "createdAt": datetime,
        "expiresAt": datetime,
        "lastUsedAt": NotRequired[datetime],
    },
)


class ListWorkspaceServiceAccountsRequestTypeDef(TypedDict):
    workspaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ServiceAccountSummaryTypeDef = TypedDict(
    "ServiceAccountSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "isDisabled": str,
        "grafanaRole": RoleType,
    },
)


class ListWorkspacesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class NetworkAccessConfigurationOutputTypeDef(TypedDict):
    prefixListIds: list[str]
    vpceIds: list[str]


class NetworkAccessConfigurationTypeDef(TypedDict):
    prefixListIds: Sequence[str]
    vpceIds: Sequence[str]


UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "id": str,
        "type": UserTypeType,
    },
)


class RoleValuesOutputTypeDef(TypedDict):
    editor: NotRequired[list[str]]
    admin: NotRequired[list[str]]


class RoleValuesTypeDef(TypedDict):
    editor: NotRequired[Sequence[str]]
    admin: NotRequired[Sequence[str]]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateWorkspaceConfigurationRequestTypeDef(TypedDict):
    configuration: str
    workspaceId: str
    grafanaVersion: NotRequired[str]


class VpcConfigurationOutputTypeDef(TypedDict):
    securityGroupIds: list[str]
    subnetIds: list[str]


class VpcConfigurationTypeDef(TypedDict):
    securityGroupIds: Sequence[str]
    subnetIds: Sequence[str]


class CreateWorkspaceApiKeyResponseTypeDef(TypedDict):
    keyName: str
    key: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


CreateWorkspaceServiceAccountResponseTypeDef = TypedDict(
    "CreateWorkspaceServiceAccountResponseTypeDef",
    {
        "id": str,
        "name": str,
        "grafanaRole": RoleType,
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DeleteWorkspaceApiKeyResponseTypeDef(TypedDict):
    keyName: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkspaceServiceAccountResponseTypeDef(TypedDict):
    serviceAccountId: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkspaceServiceAccountTokenResponseTypeDef(TypedDict):
    tokenId: str
    serviceAccountId: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeWorkspaceConfigurationResponseTypeDef(TypedDict):
    configuration: str
    grafanaVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListVersionsResponseTypeDef(TypedDict):
    grafanaVersions: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


WorkspaceSummaryTypeDef = TypedDict(
    "WorkspaceSummaryTypeDef",
    {
        "created": datetime,
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
        "authentication": AuthenticationSummaryTypeDef,
        "description": NotRequired[str],
        "name": NotRequired[str],
        "notificationDestinations": NotRequired[list[Literal["SNS"]]],
        "tags": NotRequired[dict[str, str]],
        "licenseType": NotRequired[LicenseTypeType],
        "grafanaToken": NotRequired[str],
    },
)


class CreateWorkspaceServiceAccountTokenResponseTypeDef(TypedDict):
    serviceAccountToken: ServiceAccountTokenSummaryWithKeyTypeDef
    serviceAccountId: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPermissionsRequestPaginateTypeDef(TypedDict):
    workspaceId: str
    userType: NotRequired[UserTypeType]
    userId: NotRequired[str]
    groupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVersionsRequestPaginateTypeDef(TypedDict):
    workspaceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspaceServiceAccountTokensRequestPaginateTypeDef(TypedDict):
    serviceAccountId: str
    workspaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspaceServiceAccountsRequestPaginateTypeDef(TypedDict):
    workspaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspacesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkspaceServiceAccountTokensResponseTypeDef(TypedDict):
    serviceAccountTokens: list[ServiceAccountTokenSummaryTypeDef]
    serviceAccountId: str
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWorkspaceServiceAccountsResponseTypeDef(TypedDict):
    serviceAccounts: list[ServiceAccountSummaryTypeDef]
    workspaceId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


NetworkAccessConfigurationUnionTypeDef = Union[
    NetworkAccessConfigurationTypeDef, NetworkAccessConfigurationOutputTypeDef
]


class PermissionEntryTypeDef(TypedDict):
    user: UserTypeDef
    role: RoleType


class UpdateInstructionOutputTypeDef(TypedDict):
    action: UpdateActionType
    role: RoleType
    users: list[UserTypeDef]


class UpdateInstructionTypeDef(TypedDict):
    action: UpdateActionType
    role: RoleType
    users: Sequence[UserTypeDef]


class SamlConfigurationOutputTypeDef(TypedDict):
    idpMetadata: IdpMetadataTypeDef
    assertionAttributes: NotRequired[AssertionAttributesTypeDef]
    roleValues: NotRequired[RoleValuesOutputTypeDef]
    allowedOrganizations: NotRequired[list[str]]
    loginValidityDuration: NotRequired[int]


class SamlConfigurationTypeDef(TypedDict):
    idpMetadata: IdpMetadataTypeDef
    assertionAttributes: NotRequired[AssertionAttributesTypeDef]
    roleValues: NotRequired[RoleValuesTypeDef]
    allowedOrganizations: NotRequired[Sequence[str]]
    loginValidityDuration: NotRequired[int]


WorkspaceDescriptionTypeDef = TypedDict(
    "WorkspaceDescriptionTypeDef",
    {
        "created": datetime,
        "dataSources": list[DataSourceTypeType],
        "endpoint": str,
        "grafanaVersion": str,
        "id": str,
        "modified": datetime,
        "status": WorkspaceStatusType,
        "authentication": AuthenticationSummaryTypeDef,
        "accountAccessType": NotRequired[AccountAccessTypeType],
        "description": NotRequired[str],
        "name": NotRequired[str],
        "organizationRoleName": NotRequired[str],
        "notificationDestinations": NotRequired[list[Literal["SNS"]]],
        "organizationalUnits": NotRequired[list[str]],
        "permissionType": NotRequired[PermissionTypeType],
        "stackSetName": NotRequired[str],
        "workspaceRoleArn": NotRequired[str],
        "licenseType": NotRequired[LicenseTypeType],
        "freeTrialConsumed": NotRequired[bool],
        "licenseExpiration": NotRequired[datetime],
        "freeTrialExpiration": NotRequired[datetime],
        "tags": NotRequired[dict[str, str]],
        "vpcConfiguration": NotRequired[VpcConfigurationOutputTypeDef],
        "networkAccessControl": NotRequired[NetworkAccessConfigurationOutputTypeDef],
        "grafanaToken": NotRequired[str],
        "ipAddressType": NotRequired[IPAddressTypeType],
        "kmsKeyId": NotRequired[str],
        "degradedWorkspaceReason": NotRequired[str],
    },
)
VpcConfigurationUnionTypeDef = Union[VpcConfigurationTypeDef, VpcConfigurationOutputTypeDef]


class ListWorkspacesResponseTypeDef(TypedDict):
    workspaces: list[WorkspaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPermissionsResponseTypeDef(TypedDict):
    permissions: list[PermissionEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateErrorTypeDef(TypedDict):
    code: int
    message: str
    causedBy: UpdateInstructionOutputTypeDef


UpdateInstructionUnionTypeDef = Union[UpdateInstructionTypeDef, UpdateInstructionOutputTypeDef]


class SamlAuthenticationTypeDef(TypedDict):
    status: SamlConfigurationStatusType
    configuration: NotRequired[SamlConfigurationOutputTypeDef]


SamlConfigurationUnionTypeDef = Union[SamlConfigurationTypeDef, SamlConfigurationOutputTypeDef]


class AssociateLicenseResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateLicenseResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWorkspaceResponseTypeDef(TypedDict):
    workspace: WorkspaceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkspaceRequestTypeDef(TypedDict):
    accountAccessType: AccountAccessTypeType
    permissionType: PermissionTypeType
    authenticationProviders: Sequence[AuthenticationProviderTypesType]
    clientToken: NotRequired[str]
    organizationRoleName: NotRequired[str]
    stackSetName: NotRequired[str]
    workspaceDataSources: NotRequired[Sequence[DataSourceTypeType]]
    workspaceDescription: NotRequired[str]
    workspaceName: NotRequired[str]
    workspaceNotificationDestinations: NotRequired[Sequence[Literal["SNS"]]]
    workspaceOrganizationalUnits: NotRequired[Sequence[str]]
    workspaceRoleArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    vpcConfiguration: NotRequired[VpcConfigurationUnionTypeDef]
    configuration: NotRequired[str]
    networkAccessControl: NotRequired[NetworkAccessConfigurationUnionTypeDef]
    grafanaVersion: NotRequired[str]
    ipAddressType: NotRequired[IPAddressTypeType]
    kmsKeyId: NotRequired[str]


class UpdateWorkspaceRequestTypeDef(TypedDict):
    workspaceId: str
    accountAccessType: NotRequired[AccountAccessTypeType]
    organizationRoleName: NotRequired[str]
    permissionType: NotRequired[PermissionTypeType]
    stackSetName: NotRequired[str]
    workspaceDataSources: NotRequired[Sequence[DataSourceTypeType]]
    workspaceDescription: NotRequired[str]
    workspaceName: NotRequired[str]
    workspaceNotificationDestinations: NotRequired[Sequence[Literal["SNS"]]]
    workspaceOrganizationalUnits: NotRequired[Sequence[str]]
    workspaceRoleArn: NotRequired[str]
    vpcConfiguration: NotRequired[VpcConfigurationUnionTypeDef]
    removeVpcConfiguration: NotRequired[bool]
    networkAccessControl: NotRequired[NetworkAccessConfigurationUnionTypeDef]
    removeNetworkAccessConfiguration: NotRequired[bool]
    ipAddressType: NotRequired[IPAddressTypeType]


class UpdatePermissionsResponseTypeDef(TypedDict):
    errors: list[UpdateErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePermissionsRequestTypeDef(TypedDict):
    updateInstructionBatch: Sequence[UpdateInstructionUnionTypeDef]
    workspaceId: str


class AuthenticationDescriptionTypeDef(TypedDict):
    providers: list[AuthenticationProviderTypesType]
    saml: NotRequired[SamlAuthenticationTypeDef]
    awsSso: NotRequired[AwsSsoAuthenticationTypeDef]


class UpdateWorkspaceAuthenticationRequestTypeDef(TypedDict):
    workspaceId: str
    authenticationProviders: Sequence[AuthenticationProviderTypesType]
    samlConfiguration: NotRequired[SamlConfigurationUnionTypeDef]


class DescribeWorkspaceAuthenticationResponseTypeDef(TypedDict):
    authentication: AuthenticationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWorkspaceAuthenticationResponseTypeDef(TypedDict):
    authentication: AuthenticationDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
