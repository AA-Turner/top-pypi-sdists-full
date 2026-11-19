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
from collections.abc import Sequence

from .literals import ClientTypeType, SessionStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccessTokenTypeDef",
    "BatchRevokeSessionErrorTypeDef",
    "BatchRevokeSessionsInputTypeDef",
    "BatchRevokeSessionsOutputTypeDef",
    "CreateBearerTokenRequestTypeDef",
    "CreateBearerTokenResponseTypeDef",
    "CreateOAuth2TokenRequestBodyTypeDef",
    "CreateOAuth2TokenRequestTypeDef",
    "CreateOAuth2TokenResponseBodyTypeDef",
    "CreateOAuth2TokenResponseTypeDef",
    "CreateOAuth2TokenWithIAMRequestTypeDef",
    "CreateOAuth2TokenWithIAMResponseTypeDef",
    "CreateOAuth2TokenWithTokenExchangeRequestTypeDef",
    "CreateOAuth2TokenWithTokenExchangeResponseTypeDef",
    "DeleteConsoleAuthorizationConfigurationInputTypeDef",
    "DeleteConsoleAuthorizationConfigurationOutputTypeDef",
    "DeleteResourcePermissionStatementInputTypeDef",
    "GetConsoleAuthorizationConfigurationInputTypeDef",
    "GetConsoleAuthorizationConfigurationOutputTypeDef",
    "GetResourcePolicyOutputTypeDef",
    "GetSessionInputTypeDef",
    "GetSessionOutputTypeDef",
    "IntrospectOAuth2TokenWithIAMRequestTypeDef",
    "IntrospectOAuth2TokenWithIAMResponseTypeDef",
    "ListResourcePermissionStatementsInputPaginateTypeDef",
    "ListResourcePermissionStatementsInputTypeDef",
    "ListResourcePermissionStatementsOutputTypeDef",
    "ListSessionsInputPaginateTypeDef",
    "ListSessionsInputTypeDef",
    "ListSessionsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionStatementSummaryTypeDef",
    "PolicyStatementTypeDef",
    "PutConsoleAuthorizationConfigurationInputTypeDef",
    "PutConsoleAuthorizationConfigurationOutputTypeDef",
    "PutResourcePermissionStatementInputTypeDef",
    "PutResourcePermissionStatementOutputTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeOAuth2TokenWithIAMRequestTypeDef",
    "RevokedSessionTypeDef",
    "SessionTypeDef",
    "SigninResourceBasedPolicyTypeDef",
)


class AccessTokenTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str


class BatchRevokeSessionErrorTypeDef(TypedDict):
    sessionArn: str
    code: str
    message: str


class BatchRevokeSessionsInputTypeDef(TypedDict):
    sessionArns: Sequence[str]
    principalArn: NotRequired[str]
    reason: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class RevokedSessionTypeDef(TypedDict):
    sessionArn: str


class CreateBearerTokenRequestTypeDef(TypedDict):
    grantType: str
    resource: str
    durationSeconds: NotRequired[int]


class CreateOAuth2TokenRequestBodyTypeDef(TypedDict):
    clientId: str
    grantType: str
    code: NotRequired[str]
    redirectUri: NotRequired[str]
    codeVerifier: NotRequired[str]
    refreshToken: NotRequired[str]


class CreateOAuth2TokenWithIAMRequestTypeDef(TypedDict):
    grantType: str
    resource: str


class CreateOAuth2TokenWithTokenExchangeRequestTypeDef(TypedDict):
    grantType: str
    subjectToken: NotRequired[str]
    subjectTokenType: NotRequired[str]
    assertion: NotRequired[str]
    clientId: NotRequired[str]
    resource: NotRequired[str]
    scope: NotRequired[str]


class DeleteConsoleAuthorizationConfigurationInputTypeDef(TypedDict):
    targetId: NotRequired[str]


class DeleteResourcePermissionStatementInputTypeDef(TypedDict):
    statementId: str
    clientToken: NotRequired[str]


class GetConsoleAuthorizationConfigurationInputTypeDef(TypedDict):
    targetId: NotRequired[str]


class GetSessionInputTypeDef(TypedDict):
    sessionArn: str
    principalArn: NotRequired[str]


class IntrospectOAuth2TokenWithIAMRequestTypeDef(TypedDict):
    token: str
    tokenTypeHint: NotRequired[str]


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


class ListSessionsInputTypeDef(TypedDict):
    principalArn: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[SessionStatusType]
    clientId: NotRequired[str]
    issuedAfter: NotRequired[int]
    issuedBefore: NotRequired[int]


class SessionTypeDef(TypedDict):
    sessionArn: str
    principalArn: str
    issuedAt: int
    expiresAt: int
    role: NotRequired[str]
    status: NotRequired[SessionStatusType]
    clientId: NotRequired[str]
    clientType: NotRequired[ClientTypeType]
    resource: NotRequired[str]


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


class RevokeOAuth2TokenWithIAMRequestTypeDef(TypedDict):
    token: str


class CreateOAuth2TokenResponseBodyTypeDef(TypedDict):
    accessToken: AccessTokenTypeDef
    tokenType: str
    expiresIn: int
    refreshToken: str
    idToken: NotRequired[str]


class CreateBearerTokenResponseTypeDef(TypedDict):
    accessToken: str
    tokenType: str
    expiresIn: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOAuth2TokenWithIAMResponseTypeDef(TypedDict):
    accessToken: str
    tokenType: str
    expiresIn: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOAuth2TokenWithTokenExchangeResponseTypeDef(TypedDict):
    accessToken: str
    issuedTokenType: str
    tokenType: str
    expiresIn: int
    resource: str
    scope: str
    ResponseMetadata: ResponseMetadataTypeDef


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


class GetSessionOutputTypeDef(TypedDict):
    sessionArn: str
    principalArn: str
    role: str
    status: SessionStatusType
    clientId: str
    clientType: ClientTypeType
    resource: str
    issuedAt: int
    expiresAt: int
    lastUsedAt: int
    issuedInRegion: str
    originSessionArn: str
    userAgent: str
    ResponseMetadata: ResponseMetadataTypeDef


class IntrospectOAuth2TokenWithIAMResponseTypeDef(TypedDict):
    active: bool
    clientId: str
    userId: str
    tokenType: str
    exp: int
    iat: int
    nbf: int
    sub: str
    aud: str
    iss: str
    jti: str
    accountId: str
    signinSession: str
    resource: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutConsoleAuthorizationConfigurationOutputTypeDef(TypedDict):
    targetId: str
    scope: str
    consoleAuthorizationEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class PutResourcePermissionStatementOutputTypeDef(TypedDict):
    statementId: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchRevokeSessionsOutputTypeDef(TypedDict):
    revokedSessions: list[RevokedSessionTypeDef]
    errors: list[BatchRevokeSessionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOAuth2TokenRequestTypeDef(TypedDict):
    tokenInput: CreateOAuth2TokenRequestBodyTypeDef


class ListResourcePermissionStatementsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSessionsInputPaginateTypeDef(TypedDict):
    principalArn: NotRequired[str]
    status: NotRequired[SessionStatusType]
    clientId: NotRequired[str]
    issuedAfter: NotRequired[int]
    issuedBefore: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourcePermissionStatementsOutputTypeDef(TypedDict):
    permissionStatements: list[PermissionStatementSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSessionsOutputTypeDef(TypedDict):
    items: list[SessionTypeDef]
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
