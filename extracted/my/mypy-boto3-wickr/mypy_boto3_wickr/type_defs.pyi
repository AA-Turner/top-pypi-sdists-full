"""
Type annotations for wickr service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wickr/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_wickr.type_defs import BasicDeviceObjectTypeDef

    data: BasicDeviceObjectTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import AccessLevelType, DataRetentionActionTypeType, SortDirectionType, StatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BasicDeviceObjectTypeDef",
    "BatchCreateUserRequestItemTypeDef",
    "BatchCreateUserRequestTypeDef",
    "BatchCreateUserResponseTypeDef",
    "BatchDeleteUserRequestTypeDef",
    "BatchDeleteUserResponseTypeDef",
    "BatchDeviceErrorResponseItemTypeDef",
    "BatchDeviceSuccessResponseItemTypeDef",
    "BatchLookupUserUnameRequestTypeDef",
    "BatchLookupUserUnameResponseTypeDef",
    "BatchReinviteUserRequestTypeDef",
    "BatchReinviteUserResponseTypeDef",
    "BatchResetDevicesForUserRequestTypeDef",
    "BatchResetDevicesForUserResponseTypeDef",
    "BatchToggleUserSuspendStatusRequestTypeDef",
    "BatchToggleUserSuspendStatusResponseTypeDef",
    "BatchUnameErrorResponseItemTypeDef",
    "BatchUnameSuccessResponseItemTypeDef",
    "BatchUserErrorResponseItemTypeDef",
    "BatchUserSuccessResponseItemTypeDef",
    "BlockedGuestUserTypeDef",
    "BotTypeDef",
    "CallingSettingsTypeDef",
    "CreateBotRequestTypeDef",
    "CreateBotResponseTypeDef",
    "CreateDataRetentionBotChallengeRequestTypeDef",
    "CreateDataRetentionBotChallengeResponseTypeDef",
    "CreateDataRetentionBotRequestTypeDef",
    "CreateDataRetentionBotResponseTypeDef",
    "CreateNetworkRequestTypeDef",
    "CreateNetworkResponseTypeDef",
    "CreateSecurityGroupRequestTypeDef",
    "CreateSecurityGroupResponseTypeDef",
    "DeleteBotRequestTypeDef",
    "DeleteBotResponseTypeDef",
    "DeleteDataRetentionBotRequestTypeDef",
    "DeleteDataRetentionBotResponseTypeDef",
    "DeleteNetworkRequestTypeDef",
    "DeleteNetworkResponseTypeDef",
    "DeleteSecurityGroupRequestTypeDef",
    "DeleteSecurityGroupResponseTypeDef",
    "GetBotRequestTypeDef",
    "GetBotResponseTypeDef",
    "GetBotsCountRequestTypeDef",
    "GetBotsCountResponseTypeDef",
    "GetDataRetentionBotRequestTypeDef",
    "GetDataRetentionBotResponseTypeDef",
    "GetGuestUserHistoryCountRequestTypeDef",
    "GetGuestUserHistoryCountResponseTypeDef",
    "GetNetworkRequestTypeDef",
    "GetNetworkResponseTypeDef",
    "GetNetworkSettingsRequestTypeDef",
    "GetNetworkSettingsResponseTypeDef",
    "GetOidcInfoRequestTypeDef",
    "GetOidcInfoResponseTypeDef",
    "GetSecurityGroupRequestTypeDef",
    "GetSecurityGroupResponseTypeDef",
    "GetUserRequestTypeDef",
    "GetUserResponseTypeDef",
    "GetUsersCountRequestTypeDef",
    "GetUsersCountResponseTypeDef",
    "GuestUserHistoryCountTypeDef",
    "GuestUserTypeDef",
    "ListBlockedGuestUsersRequestPaginateTypeDef",
    "ListBlockedGuestUsersRequestTypeDef",
    "ListBlockedGuestUsersResponseTypeDef",
    "ListBotsRequestPaginateTypeDef",
    "ListBotsRequestTypeDef",
    "ListBotsResponseTypeDef",
    "ListDevicesForUserRequestPaginateTypeDef",
    "ListDevicesForUserRequestTypeDef",
    "ListDevicesForUserResponseTypeDef",
    "ListGuestUsersRequestPaginateTypeDef",
    "ListGuestUsersRequestTypeDef",
    "ListGuestUsersResponseTypeDef",
    "ListNetworksRequestPaginateTypeDef",
    "ListNetworksRequestTypeDef",
    "ListNetworksResponseTypeDef",
    "ListSecurityGroupUsersRequestPaginateTypeDef",
    "ListSecurityGroupUsersRequestTypeDef",
    "ListSecurityGroupUsersResponseTypeDef",
    "ListSecurityGroupsRequestPaginateTypeDef",
    "ListSecurityGroupsRequestTypeDef",
    "ListSecurityGroupsResponseTypeDef",
    "ListUsersRequestPaginateTypeDef",
    "ListUsersRequestTypeDef",
    "ListUsersResponseTypeDef",
    "NetworkSettingsTypeDef",
    "NetworkTypeDef",
    "OidcConfigInfoTypeDef",
    "OidcTokenInfoTypeDef",
    "PaginatorConfigTypeDef",
    "PasswordRequirementsTypeDef",
    "PermittedWickrEnterpriseNetworkTypeDef",
    "ReadReceiptConfigTypeDef",
    "RegisterOidcConfigRequestTypeDef",
    "RegisterOidcConfigResponseTypeDef",
    "RegisterOidcConfigTestRequestTypeDef",
    "RegisterOidcConfigTestResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SecurityGroupSettingsOutputTypeDef",
    "SecurityGroupSettingsRequestTypeDef",
    "SecurityGroupSettingsTypeDef",
    "SecurityGroupSettingsUnionTypeDef",
    "SecurityGroupTypeDef",
    "SettingTypeDef",
    "ShredderSettingsTypeDef",
    "TimestampTypeDef",
    "UpdateBotRequestTypeDef",
    "UpdateBotResponseTypeDef",
    "UpdateDataRetentionRequestTypeDef",
    "UpdateDataRetentionResponseTypeDef",
    "UpdateGuestUserRequestTypeDef",
    "UpdateGuestUserResponseTypeDef",
    "UpdateNetworkRequestTypeDef",
    "UpdateNetworkResponseTypeDef",
    "UpdateNetworkSettingsRequestTypeDef",
    "UpdateNetworkSettingsResponseTypeDef",
    "UpdateSecurityGroupRequestTypeDef",
    "UpdateSecurityGroupResponseTypeDef",
    "UpdateUserDetailsTypeDef",
    "UpdateUserRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UserTypeDef",
    "WickrAwsNetworksTypeDef",
)

BasicDeviceObjectTypeDef = TypedDict(
    "BasicDeviceObjectTypeDef",
    {
        "appId": NotRequired[str],
        "created": NotRequired[str],
        "lastLogin": NotRequired[str],
        "statusText": NotRequired[str],
        "suspend": NotRequired[bool],
        "type": NotRequired[str],
    },
)

class BatchCreateUserRequestItemTypeDef(TypedDict):
    securityGroupIds: Sequence[str]
    username: str
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    inviteCode: NotRequired[str]
    inviteCodeTtl: NotRequired[int]
    codeValidation: NotRequired[bool]

class BatchUserErrorResponseItemTypeDef(TypedDict):
    userId: str
    field: NotRequired[str]
    reason: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "userId": NotRequired[str],
        "firstName": NotRequired[str],
        "lastName": NotRequired[str],
        "username": NotRequired[str],
        "securityGroups": NotRequired[list[str]],
        "isAdmin": NotRequired[bool],
        "suspended": NotRequired[bool],
        "status": NotRequired[int],
        "otpEnabled": NotRequired[bool],
        "scimId": NotRequired[str],
        "type": NotRequired[str],
        "cell": NotRequired[str],
        "countryCode": NotRequired[str],
        "challengeFailures": NotRequired[int],
        "isInviteExpired": NotRequired[bool],
        "isUser": NotRequired[bool],
        "inviteCode": NotRequired[str],
        "codeValidation": NotRequired[bool],
        "uname": NotRequired[str],
    },
)

class BatchDeleteUserRequestTypeDef(TypedDict):
    networkId: str
    userIds: Sequence[str]
    clientToken: NotRequired[str]

class BatchUserSuccessResponseItemTypeDef(TypedDict):
    userId: str

class BatchDeviceErrorResponseItemTypeDef(TypedDict):
    appId: str
    field: NotRequired[str]
    reason: NotRequired[str]

class BatchDeviceSuccessResponseItemTypeDef(TypedDict):
    appId: str

class BatchLookupUserUnameRequestTypeDef(TypedDict):
    networkId: str
    unames: Sequence[str]
    clientToken: NotRequired[str]

class BatchUnameErrorResponseItemTypeDef(TypedDict):
    uname: str
    field: NotRequired[str]
    reason: NotRequired[str]

class BatchUnameSuccessResponseItemTypeDef(TypedDict):
    uname: str
    username: str

class BatchReinviteUserRequestTypeDef(TypedDict):
    networkId: str
    userIds: Sequence[str]
    clientToken: NotRequired[str]

class BatchResetDevicesForUserRequestTypeDef(TypedDict):
    networkId: str
    userId: str
    appIds: Sequence[str]
    clientToken: NotRequired[str]

class BatchToggleUserSuspendStatusRequestTypeDef(TypedDict):
    networkId: str
    suspend: bool
    userIds: Sequence[str]
    clientToken: NotRequired[str]

class BlockedGuestUserTypeDef(TypedDict):
    username: str
    admin: str
    modified: str
    usernameHash: str

class BotTypeDef(TypedDict):
    botId: NotRequired[str]
    displayName: NotRequired[str]
    username: NotRequired[str]
    uname: NotRequired[str]
    pubkey: NotRequired[str]
    status: NotRequired[int]
    groupId: NotRequired[str]
    hasChallenge: NotRequired[bool]
    suspended: NotRequired[bool]
    lastLogin: NotRequired[str]

class CallingSettingsTypeDef(TypedDict):
    canStart11Call: NotRequired[bool]
    canVideoCall: NotRequired[bool]
    forceTcpCall: NotRequired[bool]

class CreateBotRequestTypeDef(TypedDict):
    networkId: str
    username: str
    groupId: str
    challenge: str
    displayName: NotRequired[str]

class CreateDataRetentionBotChallengeRequestTypeDef(TypedDict):
    networkId: str

class CreateDataRetentionBotRequestTypeDef(TypedDict):
    networkId: str

class CreateNetworkRequestTypeDef(TypedDict):
    networkName: str
    accessLevel: AccessLevelType
    enablePremiumFreeTrial: NotRequired[bool]
    encryptionKeyArn: NotRequired[str]

class DeleteBotRequestTypeDef(TypedDict):
    networkId: str
    botId: str

class DeleteDataRetentionBotRequestTypeDef(TypedDict):
    networkId: str

class DeleteNetworkRequestTypeDef(TypedDict):
    networkId: str
    clientToken: NotRequired[str]

class DeleteSecurityGroupRequestTypeDef(TypedDict):
    networkId: str
    groupId: str

class GetBotRequestTypeDef(TypedDict):
    networkId: str
    botId: str

class GetBotsCountRequestTypeDef(TypedDict):
    networkId: str

class GetDataRetentionBotRequestTypeDef(TypedDict):
    networkId: str

class GetGuestUserHistoryCountRequestTypeDef(TypedDict):
    networkId: str

class GuestUserHistoryCountTypeDef(TypedDict):
    month: str
    count: str

class GetNetworkRequestTypeDef(TypedDict):
    networkId: str

class GetNetworkSettingsRequestTypeDef(TypedDict):
    networkId: str

SettingTypeDef = TypedDict(
    "SettingTypeDef",
    {
        "optionName": str,
        "value": str,
        "type": str,
    },
)

class GetOidcInfoRequestTypeDef(TypedDict):
    networkId: str
    clientId: NotRequired[str]
    code: NotRequired[str]
    grantType: NotRequired[str]
    redirectUri: NotRequired[str]
    url: NotRequired[str]
    clientSecret: NotRequired[str]
    codeVerifier: NotRequired[str]
    certificate: NotRequired[str]

class OidcConfigInfoTypeDef(TypedDict):
    companyId: str
    scopes: str
    issuer: str
    applicationName: NotRequired[str]
    clientId: NotRequired[str]
    clientSecret: NotRequired[str]
    secret: NotRequired[str]
    redirectUrl: NotRequired[str]
    userId: NotRequired[str]
    customUsername: NotRequired[str]
    caCertificate: NotRequired[str]
    applicationId: NotRequired[int]
    ssoTokenBufferMinutes: NotRequired[int]
    extraAuthParams: NotRequired[str]

class OidcTokenInfoTypeDef(TypedDict):
    codeVerifier: NotRequired[str]
    codeChallenge: NotRequired[str]
    accessToken: NotRequired[str]
    idToken: NotRequired[str]
    refreshToken: NotRequired[str]
    tokenType: NotRequired[str]
    expiresIn: NotRequired[int]

class GetSecurityGroupRequestTypeDef(TypedDict):
    networkId: str
    groupId: str

TimestampTypeDef = Union[datetime, str]

class GetUsersCountRequestTypeDef(TypedDict):
    networkId: str

class GuestUserTypeDef(TypedDict):
    billingPeriod: str
    username: str
    usernameHash: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListBlockedGuestUsersRequestTypeDef(TypedDict):
    networkId: str
    maxResults: NotRequired[int]
    sortDirection: NotRequired[SortDirectionType]
    sortFields: NotRequired[str]
    username: NotRequired[str]
    admin: NotRequired[str]
    nextToken: NotRequired[str]

class ListBotsRequestTypeDef(TypedDict):
    networkId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    displayName: NotRequired[str]
    username: NotRequired[str]
    status: NotRequired[int]
    groupId: NotRequired[str]

class ListDevicesForUserRequestTypeDef(TypedDict):
    networkId: str
    userId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]

class ListGuestUsersRequestTypeDef(TypedDict):
    networkId: str
    maxResults: NotRequired[int]
    sortDirection: NotRequired[SortDirectionType]
    sortFields: NotRequired[str]
    username: NotRequired[str]
    billingPeriod: NotRequired[str]
    nextToken: NotRequired[str]

class ListNetworksRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    nextToken: NotRequired[str]

class NetworkTypeDef(TypedDict):
    networkId: str
    networkName: str
    accessLevel: AccessLevelType
    awsAccountId: str
    networkArn: str
    standing: NotRequired[int]
    freeTrialExpiration: NotRequired[str]
    migrationState: NotRequired[int]
    encryptionKeyArn: NotRequired[str]

class ListSecurityGroupUsersRequestTypeDef(TypedDict):
    networkId: str
    groupId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]

class ListSecurityGroupsRequestTypeDef(TypedDict):
    networkId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]

class ListUsersRequestTypeDef(TypedDict):
    networkId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    username: NotRequired[str]
    status: NotRequired[int]
    groupId: NotRequired[str]

class ReadReceiptConfigTypeDef(TypedDict):
    status: NotRequired[StatusType]

class PasswordRequirementsTypeDef(TypedDict):
    lowercase: NotRequired[int]
    minLength: NotRequired[int]
    numbers: NotRequired[int]
    symbols: NotRequired[int]
    uppercase: NotRequired[int]

class PermittedWickrEnterpriseNetworkTypeDef(TypedDict):
    domain: str
    networkId: str

class RegisterOidcConfigRequestTypeDef(TypedDict):
    networkId: str
    companyId: str
    issuer: str
    scopes: str
    customUsername: NotRequired[str]
    extraAuthParams: NotRequired[str]
    secret: NotRequired[str]
    ssoTokenBufferMinutes: NotRequired[int]
    userId: NotRequired[str]

class RegisterOidcConfigTestRequestTypeDef(TypedDict):
    networkId: str
    issuer: str
    scopes: str
    extraAuthParams: NotRequired[str]
    certificate: NotRequired[str]

class ShredderSettingsTypeDef(TypedDict):
    canProcessManually: NotRequired[bool]
    intensity: NotRequired[int]

class WickrAwsNetworksTypeDef(TypedDict):
    region: str
    networkId: str

class UpdateBotRequestTypeDef(TypedDict):
    networkId: str
    botId: str
    displayName: NotRequired[str]
    groupId: NotRequired[str]
    challenge: NotRequired[str]
    suspend: NotRequired[bool]

class UpdateDataRetentionRequestTypeDef(TypedDict):
    networkId: str
    actionType: DataRetentionActionTypeType

class UpdateGuestUserRequestTypeDef(TypedDict):
    networkId: str
    usernameHash: str
    block: bool

class UpdateNetworkRequestTypeDef(TypedDict):
    networkId: str
    networkName: str
    clientToken: NotRequired[str]
    encryptionKeyArn: NotRequired[str]

class UpdateUserDetailsTypeDef(TypedDict):
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    username: NotRequired[str]
    securityGroupIds: NotRequired[Sequence[str]]
    inviteCode: NotRequired[str]
    inviteCodeTtl: NotRequired[int]
    codeValidation: NotRequired[bool]

class BatchCreateUserRequestTypeDef(TypedDict):
    networkId: str
    users: Sequence[BatchCreateUserRequestItemTypeDef]
    clientToken: NotRequired[str]

class CreateBotResponseTypeDef(TypedDict):
    message: str
    botId: str
    networkId: str
    username: str
    displayName: str
    groupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataRetentionBotChallengeResponseTypeDef(TypedDict):
    challenge: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataRetentionBotResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNetworkResponseTypeDef(TypedDict):
    networkId: str
    networkName: str
    encryptionKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBotResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDataRetentionBotResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNetworkResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteSecurityGroupResponseTypeDef(TypedDict):
    message: str
    networkId: str
    groupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBotResponseTypeDef(TypedDict):
    botId: str
    displayName: str
    username: str
    uname: str
    pubkey: str
    status: int
    groupId: str
    hasChallenge: bool
    suspended: bool
    lastLogin: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBotsCountResponseTypeDef(TypedDict):
    pending: int
    active: int
    total: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataRetentionBotResponseTypeDef(TypedDict):
    botName: str
    botExists: bool
    isBotActive: bool
    isDataRetentionBotRegistered: bool
    isDataRetentionServiceEnabled: bool
    isPubkeyMsgAcked: bool
    ResponseMetadata: ResponseMetadataTypeDef

class GetNetworkResponseTypeDef(TypedDict):
    networkId: str
    networkName: str
    accessLevel: AccessLevelType
    awsAccountId: str
    networkArn: str
    standing: int
    freeTrialExpiration: str
    migrationState: int
    encryptionKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetUserResponseTypeDef(TypedDict):
    userId: str
    firstName: str
    lastName: str
    username: str
    isAdmin: bool
    suspended: bool
    status: int
    lastActivity: int
    lastLogin: int
    securityGroupIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetUsersCountResponseTypeDef(TypedDict):
    pending: int
    active: int
    rejected: int
    remaining: int
    total: int
    ResponseMetadata: ResponseMetadataTypeDef

class ListDevicesForUserResponseTypeDef(TypedDict):
    devices: list[BasicDeviceObjectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class RegisterOidcConfigResponseTypeDef(TypedDict):
    applicationName: str
    clientId: str
    companyId: str
    scopes: str
    issuer: str
    clientSecret: str
    secret: str
    redirectUrl: str
    userId: str
    customUsername: str
    caCertificate: str
    applicationId: int
    ssoTokenBufferMinutes: int
    extraAuthParams: str
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterOidcConfigTestResponseTypeDef(TypedDict):
    tokenEndpoint: str
    userinfoEndpoint: str
    responseTypesSupported: list[str]
    scopesSupported: list[str]
    issuer: str
    authorizationEndpoint: str
    endSessionEndpoint: str
    logoutEndpoint: str
    grantTypesSupported: list[str]
    revocationEndpoint: str
    tokenEndpointAuthMethodsSupported: list[str]
    microsoftMultiRefreshToken: bool
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBotResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDataRetentionResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGuestUserResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNetworkResponseTypeDef(TypedDict):
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateUserResponseTypeDef(TypedDict):
    userId: str
    networkId: str
    securityGroupIds: list[str]
    firstName: str
    lastName: str
    middleName: str
    suspended: bool
    modified: int
    status: int
    inviteCode: str
    inviteExpiration: int
    codeValidation: bool
    ResponseMetadata: ResponseMetadataTypeDef

class BatchCreateUserResponseTypeDef(TypedDict):
    message: str
    successful: list[UserTypeDef]
    failed: list[BatchUserErrorResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListSecurityGroupUsersResponseTypeDef(TypedDict):
    users: list[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListUsersResponseTypeDef(TypedDict):
    users: list[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchDeleteUserResponseTypeDef(TypedDict):
    message: str
    successful: list[BatchUserSuccessResponseItemTypeDef]
    failed: list[BatchUserErrorResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchReinviteUserResponseTypeDef(TypedDict):
    message: str
    successful: list[BatchUserSuccessResponseItemTypeDef]
    failed: list[BatchUserErrorResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchToggleUserSuspendStatusResponseTypeDef(TypedDict):
    message: str
    successful: list[BatchUserSuccessResponseItemTypeDef]
    failed: list[BatchUserErrorResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchResetDevicesForUserResponseTypeDef(TypedDict):
    message: str
    successful: list[BatchDeviceSuccessResponseItemTypeDef]
    failed: list[BatchDeviceErrorResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchLookupUserUnameResponseTypeDef(TypedDict):
    message: str
    successful: list[BatchUnameSuccessResponseItemTypeDef]
    failed: list[BatchUnameErrorResponseItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListBlockedGuestUsersResponseTypeDef(TypedDict):
    blocklist: list[BlockedGuestUserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBotsResponseTypeDef(TypedDict):
    bots: list[BotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetGuestUserHistoryCountResponseTypeDef(TypedDict):
    history: list[GuestUserHistoryCountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetNetworkSettingsResponseTypeDef(TypedDict):
    settings: list[SettingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNetworkSettingsResponseTypeDef(TypedDict):
    settings: list[SettingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetOidcInfoResponseTypeDef(TypedDict):
    openidConnectInfo: OidcConfigInfoTypeDef
    tokenInfo: OidcTokenInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetUserRequestTypeDef(TypedDict):
    networkId: str
    userId: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]

class ListGuestUsersResponseTypeDef(TypedDict):
    guestlist: list[GuestUserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBlockedGuestUsersRequestPaginateTypeDef(TypedDict):
    networkId: str
    sortDirection: NotRequired[SortDirectionType]
    sortFields: NotRequired[str]
    username: NotRequired[str]
    admin: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBotsRequestPaginateTypeDef(TypedDict):
    networkId: str
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    displayName: NotRequired[str]
    username: NotRequired[str]
    status: NotRequired[int]
    groupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDevicesForUserRequestPaginateTypeDef(TypedDict):
    networkId: str
    userId: str
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGuestUsersRequestPaginateTypeDef(TypedDict):
    networkId: str
    sortDirection: NotRequired[SortDirectionType]
    sortFields: NotRequired[str]
    username: NotRequired[str]
    billingPeriod: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworksRequestPaginateTypeDef(TypedDict):
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSecurityGroupUsersRequestPaginateTypeDef(TypedDict):
    networkId: str
    groupId: str
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSecurityGroupsRequestPaginateTypeDef(TypedDict):
    networkId: str
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListUsersRequestPaginateTypeDef(TypedDict):
    networkId: str
    sortFields: NotRequired[str]
    sortDirection: NotRequired[SortDirectionType]
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    username: NotRequired[str]
    status: NotRequired[int]
    groupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworksResponseTypeDef(TypedDict):
    networks: list[NetworkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class NetworkSettingsTypeDef(TypedDict):
    enableClientMetrics: NotRequired[bool]
    readReceiptConfig: NotRequired[ReadReceiptConfigTypeDef]
    dataRetention: NotRequired[bool]

class SecurityGroupSettingsOutputTypeDef(TypedDict):
    alwaysReauthenticate: NotRequired[bool]
    atakPackageValues: NotRequired[list[str]]
    calling: NotRequired[CallingSettingsTypeDef]
    checkForUpdates: NotRequired[bool]
    enableAtak: NotRequired[bool]
    enableCrashReports: NotRequired[bool]
    enableFileDownload: NotRequired[bool]
    enableGuestFederation: NotRequired[bool]
    enableNotificationPreview: NotRequired[bool]
    enableOpenAccessOption: NotRequired[bool]
    enableRestrictedGlobalFederation: NotRequired[bool]
    filesEnabled: NotRequired[bool]
    forceDeviceLockout: NotRequired[int]
    forceOpenAccess: NotRequired[bool]
    forceReadReceipts: NotRequired[bool]
    globalFederation: NotRequired[bool]
    isAtoEnabled: NotRequired[bool]
    isLinkPreviewEnabled: NotRequired[bool]
    locationAllowMaps: NotRequired[bool]
    locationEnabled: NotRequired[bool]
    maxAutoDownloadSize: NotRequired[int]
    maxBor: NotRequired[int]
    maxTtl: NotRequired[int]
    messageForwardingEnabled: NotRequired[bool]
    passwordRequirements: NotRequired[PasswordRequirementsTypeDef]
    presenceEnabled: NotRequired[bool]
    quickResponses: NotRequired[list[str]]
    showMasterRecoveryKey: NotRequired[bool]
    shredder: NotRequired[ShredderSettingsTypeDef]
    ssoMaxIdleMinutes: NotRequired[int]
    federationMode: NotRequired[int]
    lockoutThreshold: NotRequired[int]
    permittedNetworks: NotRequired[list[str]]
    permittedWickrAwsNetworks: NotRequired[list[WickrAwsNetworksTypeDef]]
    permittedWickrEnterpriseNetworks: NotRequired[list[PermittedWickrEnterpriseNetworkTypeDef]]

class SecurityGroupSettingsRequestTypeDef(TypedDict):
    lockoutThreshold: NotRequired[int]
    permittedNetworks: NotRequired[Sequence[str]]
    enableGuestFederation: NotRequired[bool]
    globalFederation: NotRequired[bool]
    federationMode: NotRequired[int]
    enableRestrictedGlobalFederation: NotRequired[bool]
    permittedWickrAwsNetworks: NotRequired[Sequence[WickrAwsNetworksTypeDef]]
    permittedWickrEnterpriseNetworks: NotRequired[Sequence[PermittedWickrEnterpriseNetworkTypeDef]]

class SecurityGroupSettingsTypeDef(TypedDict):
    alwaysReauthenticate: NotRequired[bool]
    atakPackageValues: NotRequired[Sequence[str]]
    calling: NotRequired[CallingSettingsTypeDef]
    checkForUpdates: NotRequired[bool]
    enableAtak: NotRequired[bool]
    enableCrashReports: NotRequired[bool]
    enableFileDownload: NotRequired[bool]
    enableGuestFederation: NotRequired[bool]
    enableNotificationPreview: NotRequired[bool]
    enableOpenAccessOption: NotRequired[bool]
    enableRestrictedGlobalFederation: NotRequired[bool]
    filesEnabled: NotRequired[bool]
    forceDeviceLockout: NotRequired[int]
    forceOpenAccess: NotRequired[bool]
    forceReadReceipts: NotRequired[bool]
    globalFederation: NotRequired[bool]
    isAtoEnabled: NotRequired[bool]
    isLinkPreviewEnabled: NotRequired[bool]
    locationAllowMaps: NotRequired[bool]
    locationEnabled: NotRequired[bool]
    maxAutoDownloadSize: NotRequired[int]
    maxBor: NotRequired[int]
    maxTtl: NotRequired[int]
    messageForwardingEnabled: NotRequired[bool]
    passwordRequirements: NotRequired[PasswordRequirementsTypeDef]
    presenceEnabled: NotRequired[bool]
    quickResponses: NotRequired[Sequence[str]]
    showMasterRecoveryKey: NotRequired[bool]
    shredder: NotRequired[ShredderSettingsTypeDef]
    ssoMaxIdleMinutes: NotRequired[int]
    federationMode: NotRequired[int]
    lockoutThreshold: NotRequired[int]
    permittedNetworks: NotRequired[Sequence[str]]
    permittedWickrAwsNetworks: NotRequired[Sequence[WickrAwsNetworksTypeDef]]
    permittedWickrEnterpriseNetworks: NotRequired[Sequence[PermittedWickrEnterpriseNetworkTypeDef]]

class UpdateUserRequestTypeDef(TypedDict):
    networkId: str
    userId: str
    userDetails: NotRequired[UpdateUserDetailsTypeDef]

class UpdateNetworkSettingsRequestTypeDef(TypedDict):
    networkId: str
    settings: NetworkSettingsTypeDef

SecurityGroupTypeDef = TypedDict(
    "SecurityGroupTypeDef",
    {
        "activeMembers": int,
        "botMembers": int,
        "id": str,
        "isDefault": bool,
        "name": str,
        "modified": int,
        "securityGroupSettings": SecurityGroupSettingsOutputTypeDef,
        "activeDirectoryGuid": NotRequired[str],
    },
)

class CreateSecurityGroupRequestTypeDef(TypedDict):
    networkId: str
    name: str
    securityGroupSettings: SecurityGroupSettingsRequestTypeDef
    clientToken: NotRequired[str]

SecurityGroupSettingsUnionTypeDef = Union[
    SecurityGroupSettingsTypeDef, SecurityGroupSettingsOutputTypeDef
]

class CreateSecurityGroupResponseTypeDef(TypedDict):
    securityGroup: SecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSecurityGroupResponseTypeDef(TypedDict):
    securityGroup: SecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSecurityGroupsResponseTypeDef(TypedDict):
    securityGroups: list[SecurityGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateSecurityGroupResponseTypeDef(TypedDict):
    securityGroup: SecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSecurityGroupRequestTypeDef(TypedDict):
    networkId: str
    groupId: str
    name: NotRequired[str]
    securityGroupSettings: NotRequired[SecurityGroupSettingsUnionTypeDef]
