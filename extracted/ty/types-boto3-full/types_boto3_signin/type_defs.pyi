"""
Type annotations for signin service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_signin.type_defs import AccessTokenTypeDef

    data: AccessTokenTypeDef = ...
    ```
"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AccessTokenTypeDef",
    "CreateOAuth2TokenRequestBodyTypeDef",
    "CreateOAuth2TokenRequestTypeDef",
    "CreateOAuth2TokenResponseBodyTypeDef",
    "CreateOAuth2TokenResponseTypeDef",
    "DeleteConsoleAuthorizationConfigurationInputTypeDef",
    "DeleteConsoleAuthorizationConfigurationOutputTypeDef",
    "DeleteResourcePermissionStatementInputTypeDef",
    "GetConsoleAuthorizationConfigurationInputTypeDef",
    "GetConsoleAuthorizationConfigurationOutputTypeDef",
    "GetResourcePolicyOutputTypeDef",
    "ListResourcePermissionStatementsInputPaginateTypeDef",
    "ListResourcePermissionStatementsInputTypeDef",
    "ListResourcePermissionStatementsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionStatementSummaryTypeDef",
    "PolicyStatementTypeDef",
    "PutConsoleAuthorizationConfigurationInputTypeDef",
    "PutConsoleAuthorizationConfigurationOutputTypeDef",
    "PutResourcePermissionStatementInputTypeDef",
    "PutResourcePermissionStatementOutputTypeDef",
    "ResponseMetadataTypeDef",
    "SigninResourceBasedPolicyTypeDef",
)

class AccessTokenTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str

class CreateOAuth2TokenRequestBodyTypeDef(TypedDict):
    clientId: str
    grantType: str
    code: NotRequired[str]
    redirectUri: NotRequired[str]
    codeVerifier: NotRequired[str]
    refreshToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteConsoleAuthorizationConfigurationInputTypeDef(TypedDict):
    targetId: NotRequired[str]

class DeleteResourcePermissionStatementInputTypeDef(TypedDict):
    statementId: str
    clientToken: NotRequired[str]

class GetConsoleAuthorizationConfigurationInputTypeDef(TypedDict):
    targetId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListResourcePermissionStatementsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PermissionStatementSummaryTypeDef(TypedDict):
    sid: str
    condition: NotRequired[dict[str, dict[str, list[str]]]]

class PolicyStatementTypeDef(TypedDict):
    effect: NotRequired[str]
    principal: NotRequired[dict[str, str]]
    action: NotRequired[list[str]]
    resource: NotRequired[str]
    condition: NotRequired[dict[str, dict[str, list[str]]]]

class PutConsoleAuthorizationConfigurationInputTypeDef(TypedDict):
    targetId: NotRequired[str]

class PutResourcePermissionStatementInputTypeDef(TypedDict):
    sourceVpc: NotRequired[str]
    signinSourceVpce: NotRequired[str]
    consoleSourceVpce: NotRequired[str]
    vpcSourceIp: NotRequired[str]
    sourceIp: NotRequired[str]
    requestedRegion: NotRequired[str]
    excludedPrincipal: NotRequired[str]
    clientToken: NotRequired[str]

class CreateOAuth2TokenResponseBodyTypeDef(TypedDict):
    accessToken: AccessTokenTypeDef
    tokenType: str
    expiresIn: int
    refreshToken: str
    idToken: NotRequired[str]

class CreateOAuth2TokenRequestTypeDef(TypedDict):
    tokenInput: CreateOAuth2TokenRequestBodyTypeDef

class DeleteConsoleAuthorizationConfigurationOutputTypeDef(TypedDict):
    targetId: str
    scope: str
    consoleAuthorizationEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetConsoleAuthorizationConfigurationOutputTypeDef(TypedDict):
    targetId: str
    scope: str
    consoleAuthorizationEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef

class PutConsoleAuthorizationConfigurationOutputTypeDef(TypedDict):
    targetId: str
    scope: str
    consoleAuthorizationEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef

class PutResourcePermissionStatementOutputTypeDef(TypedDict):
    statementId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourcePermissionStatementsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourcePermissionStatementsOutputTypeDef(TypedDict):
    permissionStatements: list[PermissionStatementSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SigninResourceBasedPolicyTypeDef(TypedDict):
    version: NotRequired[str]
    statement: NotRequired[list[PolicyStatementTypeDef]]

class CreateOAuth2TokenResponseTypeDef(TypedDict):
    tokenOutput: CreateOAuth2TokenResponseBodyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyOutputTypeDef(TypedDict):
    signinResourceBasedPolicy: SigninResourceBasedPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
