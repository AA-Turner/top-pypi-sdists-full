"""
Type annotations for cognito-idp service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_idp.client import CognitoIdentityProviderClient

    session = get_session()
    async with session.create_client("cognito-idp") as client:
        client: CognitoIdentityProviderClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    AdminListGroupsForUserPaginator,
    AdminListUserAuthEventsPaginator,
    ListGroupsPaginator,
    ListIdentityProvidersPaginator,
    ListResourceServersPaginator,
    ListUserPoolClientsPaginator,
    ListUserPoolsPaginator,
    ListUsersInGroupPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AddCustomAttributesRequestTypeDef,
    AdminAddUserToGroupRequestTypeDef,
    AdminConfirmSignUpRequestTypeDef,
    AdminCreateUserRequestTypeDef,
    AdminCreateUserResponseTypeDef,
    AdminDeleteUserAttributesRequestTypeDef,
    AdminDeleteUserRequestTypeDef,
    AdminDisableProviderForUserRequestTypeDef,
    AdminDisableUserRequestTypeDef,
    AdminEnableUserRequestTypeDef,
    AdminForgetDeviceRequestTypeDef,
    AdminGetDeviceRequestTypeDef,
    AdminGetDeviceResponseTypeDef,
    AdminGetUserRequestTypeDef,
    AdminGetUserResponseTypeDef,
    AdminInitiateAuthRequestTypeDef,
    AdminInitiateAuthResponseTypeDef,
    AdminLinkProviderForUserRequestTypeDef,
    AdminListDevicesRequestTypeDef,
    AdminListDevicesResponseTypeDef,
    AdminListGroupsForUserRequestTypeDef,
    AdminListGroupsForUserResponseTypeDef,
    AdminListUserAuthEventsRequestTypeDef,
    AdminListUserAuthEventsResponseTypeDef,
    AdminRemoveUserFromGroupRequestTypeDef,
    AdminResetUserPasswordRequestTypeDef,
    AdminRespondToAuthChallengeRequestTypeDef,
    AdminRespondToAuthChallengeResponseTypeDef,
    AdminSetUserMFAPreferenceRequestTypeDef,
    AdminSetUserPasswordRequestTypeDef,
    AdminSetUserSettingsRequestTypeDef,
    AdminUpdateAuthEventFeedbackRequestTypeDef,
    AdminUpdateDeviceStatusRequestTypeDef,
    AdminUpdateUserAttributesRequestTypeDef,
    AdminUserGlobalSignOutRequestTypeDef,
    AssociateSoftwareTokenRequestTypeDef,
    AssociateSoftwareTokenResponseTypeDef,
    ChangePasswordRequestTypeDef,
    CompleteWebAuthnRegistrationRequestTypeDef,
    ConfirmDeviceRequestTypeDef,
    ConfirmDeviceResponseTypeDef,
    ConfirmForgotPasswordRequestTypeDef,
    ConfirmSignUpRequestTypeDef,
    ConfirmSignUpResponseTypeDef,
    CreateGroupRequestTypeDef,
    CreateGroupResponseTypeDef,
    CreateIdentityProviderRequestTypeDef,
    CreateIdentityProviderResponseTypeDef,
    CreateManagedLoginBrandingRequestTypeDef,
    CreateManagedLoginBrandingResponseTypeDef,
    CreateResourceServerRequestTypeDef,
    CreateResourceServerResponseTypeDef,
    CreateUserImportJobRequestTypeDef,
    CreateUserImportJobResponseTypeDef,
    CreateUserPoolClientRequestTypeDef,
    CreateUserPoolClientResponseTypeDef,
    CreateUserPoolDomainRequestTypeDef,
    CreateUserPoolDomainResponseTypeDef,
    CreateUserPoolRequestTypeDef,
    CreateUserPoolResponseTypeDef,
    DeleteGroupRequestTypeDef,
    DeleteIdentityProviderRequestTypeDef,
    DeleteManagedLoginBrandingRequestTypeDef,
    DeleteResourceServerRequestTypeDef,
    DeleteUserAttributesRequestTypeDef,
    DeleteUserPoolClientRequestTypeDef,
    DeleteUserPoolDomainRequestTypeDef,
    DeleteUserPoolRequestTypeDef,
    DeleteUserRequestTypeDef,
    DeleteWebAuthnCredentialRequestTypeDef,
    DescribeIdentityProviderRequestTypeDef,
    DescribeIdentityProviderResponseTypeDef,
    DescribeManagedLoginBrandingByClientRequestTypeDef,
    DescribeManagedLoginBrandingByClientResponseTypeDef,
    DescribeManagedLoginBrandingRequestTypeDef,
    DescribeManagedLoginBrandingResponseTypeDef,
    DescribeResourceServerRequestTypeDef,
    DescribeResourceServerResponseTypeDef,
    DescribeRiskConfigurationRequestTypeDef,
    DescribeRiskConfigurationResponseTypeDef,
    DescribeUserImportJobRequestTypeDef,
    DescribeUserImportJobResponseTypeDef,
    DescribeUserPoolClientRequestTypeDef,
    DescribeUserPoolClientResponseTypeDef,
    DescribeUserPoolDomainRequestTypeDef,
    DescribeUserPoolDomainResponseTypeDef,
    DescribeUserPoolRequestTypeDef,
    DescribeUserPoolResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ForgetDeviceRequestTypeDef,
    ForgotPasswordRequestTypeDef,
    ForgotPasswordResponseTypeDef,
    GetCSVHeaderRequestTypeDef,
    GetCSVHeaderResponseTypeDef,
    GetDeviceRequestTypeDef,
    GetDeviceResponseTypeDef,
    GetGroupRequestTypeDef,
    GetGroupResponseTypeDef,
    GetIdentityProviderByIdentifierRequestTypeDef,
    GetIdentityProviderByIdentifierResponseTypeDef,
    GetLogDeliveryConfigurationRequestTypeDef,
    GetLogDeliveryConfigurationResponseTypeDef,
    GetSigningCertificateRequestTypeDef,
    GetSigningCertificateResponseTypeDef,
    GetUICustomizationRequestTypeDef,
    GetUICustomizationResponseTypeDef,
    GetUserAttributeVerificationCodeRequestTypeDef,
    GetUserAttributeVerificationCodeResponseTypeDef,
    GetUserAuthFactorsRequestTypeDef,
    GetUserAuthFactorsResponseTypeDef,
    GetUserPoolMfaConfigRequestTypeDef,
    GetUserPoolMfaConfigResponseTypeDef,
    GetUserRequestTypeDef,
    GetUserResponseTypeDef,
    GlobalSignOutRequestTypeDef,
    InitiateAuthRequestTypeDef,
    InitiateAuthResponseTypeDef,
    ListDevicesRequestTypeDef,
    ListDevicesResponseTypeDef,
    ListGroupsRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListIdentityProvidersRequestTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListResourceServersRequestTypeDef,
    ListResourceServersResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUserImportJobsRequestTypeDef,
    ListUserImportJobsResponseTypeDef,
    ListUserPoolClientsRequestTypeDef,
    ListUserPoolClientsResponseTypeDef,
    ListUserPoolsRequestTypeDef,
    ListUserPoolsResponseTypeDef,
    ListUsersInGroupRequestTypeDef,
    ListUsersInGroupResponseTypeDef,
    ListUsersRequestTypeDef,
    ListUsersResponseTypeDef,
    ListWebAuthnCredentialsRequestTypeDef,
    ListWebAuthnCredentialsResponseTypeDef,
    ResendConfirmationCodeRequestTypeDef,
    ResendConfirmationCodeResponseTypeDef,
    RespondToAuthChallengeRequestTypeDef,
    RespondToAuthChallengeResponseTypeDef,
    RevokeTokenRequestTypeDef,
    SetLogDeliveryConfigurationRequestTypeDef,
    SetLogDeliveryConfigurationResponseTypeDef,
    SetRiskConfigurationRequestTypeDef,
    SetRiskConfigurationResponseTypeDef,
    SetUICustomizationRequestTypeDef,
    SetUICustomizationResponseTypeDef,
    SetUserMFAPreferenceRequestTypeDef,
    SetUserPoolMfaConfigRequestTypeDef,
    SetUserPoolMfaConfigResponseTypeDef,
    SetUserSettingsRequestTypeDef,
    SignUpRequestTypeDef,
    SignUpResponseTypeDef,
    StartUserImportJobRequestTypeDef,
    StartUserImportJobResponseTypeDef,
    StartWebAuthnRegistrationRequestTypeDef,
    StartWebAuthnRegistrationResponseTypeDef,
    StopUserImportJobRequestTypeDef,
    StopUserImportJobResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAuthEventFeedbackRequestTypeDef,
    UpdateDeviceStatusRequestTypeDef,
    UpdateGroupRequestTypeDef,
    UpdateGroupResponseTypeDef,
    UpdateIdentityProviderRequestTypeDef,
    UpdateIdentityProviderResponseTypeDef,
    UpdateManagedLoginBrandingRequestTypeDef,
    UpdateManagedLoginBrandingResponseTypeDef,
    UpdateResourceServerRequestTypeDef,
    UpdateResourceServerResponseTypeDef,
    UpdateUserAttributesRequestTypeDef,
    UpdateUserAttributesResponseTypeDef,
    UpdateUserPoolClientRequestTypeDef,
    UpdateUserPoolClientResponseTypeDef,
    UpdateUserPoolDomainRequestTypeDef,
    UpdateUserPoolDomainResponseTypeDef,
    UpdateUserPoolRequestTypeDef,
    VerifySoftwareTokenRequestTypeDef,
    VerifySoftwareTokenResponseTypeDef,
    VerifyUserAttributeRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("CognitoIdentityProviderClient",)

class Exceptions(BaseClientExceptions):
    AliasExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CodeDeliveryFailureException: Type[BotocoreClientError]
    CodeMismatchException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DuplicateProviderException: Type[BotocoreClientError]
    EnableSoftwareTokenMFAException: Type[BotocoreClientError]
    ExpiredCodeException: Type[BotocoreClientError]
    FeatureUnavailableInTierException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GroupExistsException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidEmailRoleAccessPolicyException: Type[BotocoreClientError]
    InvalidLambdaResponseException: Type[BotocoreClientError]
    InvalidOAuthFlowException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPasswordException: Type[BotocoreClientError]
    InvalidSmsRoleAccessPolicyException: Type[BotocoreClientError]
    InvalidSmsRoleTrustRelationshipException: Type[BotocoreClientError]
    InvalidUserPoolConfigurationException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MFAMethodNotFoundException: Type[BotocoreClientError]
    ManagedLoginBrandingExistsException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    PasswordHistoryPolicyViolationException: Type[BotocoreClientError]
    PasswordResetRequiredException: Type[BotocoreClientError]
    PreconditionNotMetException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ScopeDoesNotExistException: Type[BotocoreClientError]
    SoftwareTokenMFANotFoundException: Type[BotocoreClientError]
    TierChangeNotAllowedException: Type[BotocoreClientError]
    TooManyFailedAttemptsException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnexpectedLambdaException: Type[BotocoreClientError]
    UnsupportedIdentityProviderException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    UnsupportedTokenTypeException: Type[BotocoreClientError]
    UnsupportedUserStateException: Type[BotocoreClientError]
    UserImportInProgressException: Type[BotocoreClientError]
    UserLambdaValidationException: Type[BotocoreClientError]
    UserNotConfirmedException: Type[BotocoreClientError]
    UserNotFoundException: Type[BotocoreClientError]
    UserPoolAddOnNotEnabledException: Type[BotocoreClientError]
    UserPoolTaggingException: Type[BotocoreClientError]
    UsernameExistsException: Type[BotocoreClientError]
    WebAuthnChallengeNotFoundException: Type[BotocoreClientError]
    WebAuthnClientMismatchException: Type[BotocoreClientError]
    WebAuthnConfigurationMissingException: Type[BotocoreClientError]
    WebAuthnCredentialNotSupportedException: Type[BotocoreClientError]
    WebAuthnNotEnabledException: Type[BotocoreClientError]
    WebAuthnOriginNotAllowedException: Type[BotocoreClientError]
    WebAuthnRelyingPartyMismatchException: Type[BotocoreClientError]

class CognitoIdentityProviderClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CognitoIdentityProviderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#generate_presigned_url)
        """

    async def add_custom_attributes(
        self, **kwargs: Unpack[AddCustomAttributesRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds additional user attributes to the user pool schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/add_custom_attributes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#add_custom_attributes)
        """

    async def admin_add_user_to_group(
        self, **kwargs: Unpack[AdminAddUserToGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds a user to a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_add_user_to_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_add_user_to_group)
        """

    async def admin_confirm_sign_up(
        self, **kwargs: Unpack[AdminConfirmSignUpRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Confirms user sign-up as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_confirm_sign_up.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_confirm_sign_up)
        """

    async def admin_create_user(
        self, **kwargs: Unpack[AdminCreateUserRequestTypeDef]
    ) -> AdminCreateUserResponseTypeDef:
        """
        Creates a new user in the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_create_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_create_user)
        """

    async def admin_delete_user(
        self, **kwargs: Unpack[AdminDeleteUserRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user profile in your user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_delete_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_delete_user)
        """

    async def admin_delete_user_attributes(
        self, **kwargs: Unpack[AdminDeleteUserAttributesRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes attribute values from a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_delete_user_attributes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_delete_user_attributes)
        """

    async def admin_disable_provider_for_user(
        self, **kwargs: Unpack[AdminDisableProviderForUserRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Prevents the user from signing in with the specified external (SAML or social)
        identity provider (IdP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_disable_provider_for_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_disable_provider_for_user)
        """

    async def admin_disable_user(
        self, **kwargs: Unpack[AdminDisableUserRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deactivates a user profile and revokes all access tokens for the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_disable_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_disable_user)
        """

    async def admin_enable_user(
        self, **kwargs: Unpack[AdminEnableUserRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Activate sign-in for a user profile that previously had sign-in access disabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_enable_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_enable_user)
        """

    async def admin_forget_device(
        self, **kwargs: Unpack[AdminForgetDeviceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Forgets, or deletes, a remembered device from a user's profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_forget_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_forget_device)
        """

    async def admin_get_device(
        self, **kwargs: Unpack[AdminGetDeviceRequestTypeDef]
    ) -> AdminGetDeviceResponseTypeDef:
        """
        Given the device key, returns details for a user' device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_get_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_get_device)
        """

    async def admin_get_user(
        self, **kwargs: Unpack[AdminGetUserRequestTypeDef]
    ) -> AdminGetUserResponseTypeDef:
        """
        Given the username, returns details about a user profile in a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_get_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_get_user)
        """

    async def admin_initiate_auth(
        self, **kwargs: Unpack[AdminInitiateAuthRequestTypeDef]
    ) -> AdminInitiateAuthResponseTypeDef:
        """
        Starts sign-in for applications with a server-side component, for example a
        traditional web application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_initiate_auth.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_initiate_auth)
        """

    async def admin_link_provider_for_user(
        self, **kwargs: Unpack[AdminLinkProviderForUserRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Links an existing user account in a user pool (<code>DestinationUser</code>) to
        an identity from an external IdP (<code>SourceUser</code>) based on a specified
        attribute name and value from the external IdP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_link_provider_for_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_link_provider_for_user)
        """

    async def admin_list_devices(
        self, **kwargs: Unpack[AdminListDevicesRequestTypeDef]
    ) -> AdminListDevicesResponseTypeDef:
        """
        Lists a user's registered devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_list_devices.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_list_devices)
        """

    async def admin_list_groups_for_user(
        self, **kwargs: Unpack[AdminListGroupsForUserRequestTypeDef]
    ) -> AdminListGroupsForUserResponseTypeDef:
        """
        Lists the groups that a user belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_list_groups_for_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_list_groups_for_user)
        """

    async def admin_list_user_auth_events(
        self, **kwargs: Unpack[AdminListUserAuthEventsRequestTypeDef]
    ) -> AdminListUserAuthEventsResponseTypeDef:
        """
        Requests a history of user activity and any risks detected as part of Amazon
        Cognito threat protection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_list_user_auth_events.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_list_user_auth_events)
        """

    async def admin_remove_user_from_group(
        self, **kwargs: Unpack[AdminRemoveUserFromGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Given a username and a group name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_remove_user_from_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_remove_user_from_group)
        """

    async def admin_reset_user_password(
        self, **kwargs: Unpack[AdminResetUserPasswordRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Resets the specified user's password in a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_reset_user_password.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_reset_user_password)
        """

    async def admin_respond_to_auth_challenge(
        self, **kwargs: Unpack[AdminRespondToAuthChallengeRequestTypeDef]
    ) -> AdminRespondToAuthChallengeResponseTypeDef:
        """
        Some API operations in a user pool generate a challenge, like a prompt for an
        MFA code, for device authentication that bypasses MFA, or for a custom
        authentication challenge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_respond_to_auth_challenge.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_respond_to_auth_challenge)
        """

    async def admin_set_user_mfa_preference(
        self, **kwargs: Unpack[AdminSetUserMFAPreferenceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the user's multi-factor authentication (MFA) preference, including which
        MFA options are activated, and if any are preferred.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_set_user_mfa_preference.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_set_user_mfa_preference)
        """

    async def admin_set_user_password(
        self, **kwargs: Unpack[AdminSetUserPasswordRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the specified user's password in a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_set_user_password.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_set_user_password)
        """

    async def admin_set_user_settings(
        self, **kwargs: Unpack[AdminSetUserSettingsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        <i>This action is no longer supported.</i> You can use it to configure only SMS
        MFA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_set_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_set_user_settings)
        """

    async def admin_update_auth_event_feedback(
        self, **kwargs: Unpack[AdminUpdateAuthEventFeedbackRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Provides feedback for an authentication event indicating if it was from a valid
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_update_auth_event_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_update_auth_event_feedback)
        """

    async def admin_update_device_status(
        self, **kwargs: Unpack[AdminUpdateDeviceStatusRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the status of a user's device so that it is marked as remembered or not
        remembered for the purpose of device authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_update_device_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_update_device_status)
        """

    async def admin_update_user_attributes(
        self, **kwargs: Unpack[AdminUpdateUserAttributesRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This action might generate an SMS text message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_update_user_attributes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_update_user_attributes)
        """

    async def admin_user_global_sign_out(
        self, **kwargs: Unpack[AdminUserGlobalSignOutRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Invalidates the identity, access, and refresh tokens that Amazon Cognito issued
        to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/admin_user_global_sign_out.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_user_global_sign_out)
        """

    async def associate_software_token(
        self, **kwargs: Unpack[AssociateSoftwareTokenRequestTypeDef]
    ) -> AssociateSoftwareTokenResponseTypeDef:
        """
        Begins setup of time-based one-time password (TOTP) multi-factor authentication
        (MFA) for a user, with a unique private key that Amazon Cognito generates and
        returns in the API response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/associate_software_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#associate_software_token)
        """

    async def change_password(
        self, **kwargs: Unpack[ChangePasswordRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the password for a specified user in a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/change_password.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#change_password)
        """

    async def complete_web_authn_registration(
        self, **kwargs: Unpack[CompleteWebAuthnRegistrationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Completes registration of a passkey authenticator for the current user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/complete_web_authn_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#complete_web_authn_registration)
        """

    async def confirm_device(
        self, **kwargs: Unpack[ConfirmDeviceRequestTypeDef]
    ) -> ConfirmDeviceResponseTypeDef:
        """
        Confirms a device that a user wants to remember.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/confirm_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#confirm_device)
        """

    async def confirm_forgot_password(
        self, **kwargs: Unpack[ConfirmForgotPasswordRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This public API operation accepts a confirmation code that Amazon Cognito sent
        to a user and accepts a new password for that user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/confirm_forgot_password.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#confirm_forgot_password)
        """

    async def confirm_sign_up(
        self, **kwargs: Unpack[ConfirmSignUpRequestTypeDef]
    ) -> ConfirmSignUpResponseTypeDef:
        """
        This public API operation submits a code that Amazon Cognito sent to your user
        when they signed up in your user pool via the <a
        href="https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SignUp.html">SignUp</a>
        API operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/confirm_sign_up.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#confirm_sign_up)
        """

    async def create_group(
        self, **kwargs: Unpack[CreateGroupRequestTypeDef]
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a new group in the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_group)
        """

    async def create_identity_provider(
        self, **kwargs: Unpack[CreateIdentityProviderRequestTypeDef]
    ) -> CreateIdentityProviderResponseTypeDef:
        """
        Adds a configuration and trust relationship between a third-party identity
        provider (IdP) and a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_identity_provider)
        """

    async def create_managed_login_branding(
        self, **kwargs: Unpack[CreateManagedLoginBrandingRequestTypeDef]
    ) -> CreateManagedLoginBrandingResponseTypeDef:
        """
        Creates a new set of branding settings for a user pool style and associates it
        with an app client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_managed_login_branding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_managed_login_branding)
        """

    async def create_resource_server(
        self, **kwargs: Unpack[CreateResourceServerRequestTypeDef]
    ) -> CreateResourceServerResponseTypeDef:
        """
        Creates a new OAuth2.0 resource server and defines custom scopes within it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_resource_server.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_resource_server)
        """

    async def create_user_import_job(
        self, **kwargs: Unpack[CreateUserImportJobRequestTypeDef]
    ) -> CreateUserImportJobResponseTypeDef:
        """
        Creates a user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_user_import_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_import_job)
        """

    async def create_user_pool(
        self, **kwargs: Unpack[CreateUserPoolRequestTypeDef]
    ) -> CreateUserPoolResponseTypeDef:
        """
        This action might generate an SMS text message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_user_pool.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_pool)
        """

    async def create_user_pool_client(
        self, **kwargs: Unpack[CreateUserPoolClientRequestTypeDef]
    ) -> CreateUserPoolClientResponseTypeDef:
        """
        Creates an app client in a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_user_pool_client.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_pool_client)
        """

    async def create_user_pool_domain(
        self, **kwargs: Unpack[CreateUserPoolDomainRequestTypeDef]
    ) -> CreateUserPoolDomainResponseTypeDef:
        """
        A user pool domain hosts managed login, an authorization server and web server
        for authentication in your application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/create_user_pool_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_pool_domain)
        """

    async def delete_group(
        self, **kwargs: Unpack[DeleteGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a group from the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_group)
        """

    async def delete_identity_provider(
        self, **kwargs: Unpack[DeleteIdentityProviderRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user pool identity provider (IdP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_identity_provider)
        """

    async def delete_managed_login_branding(
        self, **kwargs: Unpack[DeleteManagedLoginBrandingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a managed login branding style.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_managed_login_branding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_managed_login_branding)
        """

    async def delete_resource_server(
        self, **kwargs: Unpack[DeleteResourceServerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a resource server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_resource_server.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_resource_server)
        """

    async def delete_user(
        self, **kwargs: Unpack[DeleteUserRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Self-deletes a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user)
        """

    async def delete_user_attributes(
        self, **kwargs: Unpack[DeleteUserAttributesRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Self-deletes attributes for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_user_attributes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_attributes)
        """

    async def delete_user_pool(
        self, **kwargs: Unpack[DeleteUserPoolRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_user_pool.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_pool)
        """

    async def delete_user_pool_client(
        self, **kwargs: Unpack[DeleteUserPoolClientRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user pool app client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_user_pool_client.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_pool_client)
        """

    async def delete_user_pool_domain(
        self, **kwargs: Unpack[DeleteUserPoolDomainRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Given a user pool ID and domain identifier, deletes a user pool domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_user_pool_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_pool_domain)
        """

    async def delete_web_authn_credential(
        self, **kwargs: Unpack[DeleteWebAuthnCredentialRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a registered passkey, or webauthN, authenticator for the currently
        signed-in user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/delete_web_authn_credential.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_web_authn_credential)
        """

    async def describe_identity_provider(
        self, **kwargs: Unpack[DescribeIdentityProviderRequestTypeDef]
    ) -> DescribeIdentityProviderResponseTypeDef:
        """
        Given a user pool ID and identity provider (IdP) name, returns details about
        the IdP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_identity_provider)
        """

    async def describe_managed_login_branding(
        self, **kwargs: Unpack[DescribeManagedLoginBrandingRequestTypeDef]
    ) -> DescribeManagedLoginBrandingResponseTypeDef:
        """
        Given the ID of a managed login branding style, returns detailed information
        about the style.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_managed_login_branding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_managed_login_branding)
        """

    async def describe_managed_login_branding_by_client(
        self, **kwargs: Unpack[DescribeManagedLoginBrandingByClientRequestTypeDef]
    ) -> DescribeManagedLoginBrandingByClientResponseTypeDef:
        """
        Given the ID of a user pool app client, returns detailed information about the
        style assigned to the app client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_managed_login_branding_by_client.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_managed_login_branding_by_client)
        """

    async def describe_resource_server(
        self, **kwargs: Unpack[DescribeResourceServerRequestTypeDef]
    ) -> DescribeResourceServerResponseTypeDef:
        """
        Describes a resource server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_resource_server.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_resource_server)
        """

    async def describe_risk_configuration(
        self, **kwargs: Unpack[DescribeRiskConfigurationRequestTypeDef]
    ) -> DescribeRiskConfigurationResponseTypeDef:
        """
        Given an app client or user pool ID where threat protection is configured,
        describes the risk configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_risk_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_risk_configuration)
        """

    async def describe_user_import_job(
        self, **kwargs: Unpack[DescribeUserImportJobRequestTypeDef]
    ) -> DescribeUserImportJobResponseTypeDef:
        """
        Describes a user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_user_import_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_import_job)
        """

    async def describe_user_pool(
        self, **kwargs: Unpack[DescribeUserPoolRequestTypeDef]
    ) -> DescribeUserPoolResponseTypeDef:
        """
        Given a user pool ID, returns configuration information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_user_pool.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_pool)
        """

    async def describe_user_pool_client(
        self, **kwargs: Unpack[DescribeUserPoolClientRequestTypeDef]
    ) -> DescribeUserPoolClientResponseTypeDef:
        """
        Given an app client ID, returns configuration information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_user_pool_client.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_pool_client)
        """

    async def describe_user_pool_domain(
        self, **kwargs: Unpack[DescribeUserPoolDomainRequestTypeDef]
    ) -> DescribeUserPoolDomainResponseTypeDef:
        """
        Given a user pool domain name, returns information about the domain
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/describe_user_pool_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_pool_domain)
        """

    async def forget_device(
        self, **kwargs: Unpack[ForgetDeviceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Forgets the specified device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/forget_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#forget_device)
        """

    async def forgot_password(
        self, **kwargs: Unpack[ForgotPasswordRequestTypeDef]
    ) -> ForgotPasswordResponseTypeDef:
        """
        Calling this API causes a message to be sent to the end user with a
        confirmation code that is required to change the user's password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/forgot_password.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#forgot_password)
        """

    async def get_csv_header(
        self, **kwargs: Unpack[GetCSVHeaderRequestTypeDef]
    ) -> GetCSVHeaderResponseTypeDef:
        """
        Gets the header information for the comma-separated value (CSV) file to be used
        as input for the user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_csv_header.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_csv_header)
        """

    async def get_device(
        self, **kwargs: Unpack[GetDeviceRequestTypeDef]
    ) -> GetDeviceResponseTypeDef:
        """
        Gets the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_device)
        """

    async def get_group(self, **kwargs: Unpack[GetGroupRequestTypeDef]) -> GetGroupResponseTypeDef:
        """
        Gets a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_group)
        """

    async def get_identity_provider_by_identifier(
        self, **kwargs: Unpack[GetIdentityProviderByIdentifierRequestTypeDef]
    ) -> GetIdentityProviderByIdentifierResponseTypeDef:
        """
        Gets the specified IdP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_identity_provider_by_identifier.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_identity_provider_by_identifier)
        """

    async def get_log_delivery_configuration(
        self, **kwargs: Unpack[GetLogDeliveryConfigurationRequestTypeDef]
    ) -> GetLogDeliveryConfigurationResponseTypeDef:
        """
        Gets the logging configuration of a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_log_delivery_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_log_delivery_configuration)
        """

    async def get_signing_certificate(
        self, **kwargs: Unpack[GetSigningCertificateRequestTypeDef]
    ) -> GetSigningCertificateResponseTypeDef:
        """
        This method takes a user pool ID, and returns the signing certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_signing_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_signing_certificate)
        """

    async def get_ui_customization(
        self, **kwargs: Unpack[GetUICustomizationRequestTypeDef]
    ) -> GetUICustomizationResponseTypeDef:
        """
        Gets the user interface (UI) Customization information for a particular app
        client's app UI, if any such information exists for the client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_ui_customization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_ui_customization)
        """

    async def get_user(self, **kwargs: Unpack[GetUserRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Gets the user attributes and metadata for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_user)
        """

    async def get_user_attribute_verification_code(
        self, **kwargs: Unpack[GetUserAttributeVerificationCodeRequestTypeDef]
    ) -> GetUserAttributeVerificationCodeResponseTypeDef:
        """
        Generates a user attribute verification code for the specified attribute name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_user_attribute_verification_code.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_user_attribute_verification_code)
        """

    async def get_user_auth_factors(
        self, **kwargs: Unpack[GetUserAuthFactorsRequestTypeDef]
    ) -> GetUserAuthFactorsResponseTypeDef:
        """
        Lists the authentication options for the currently signed-in user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_user_auth_factors.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_user_auth_factors)
        """

    async def get_user_pool_mfa_config(
        self, **kwargs: Unpack[GetUserPoolMfaConfigRequestTypeDef]
    ) -> GetUserPoolMfaConfigResponseTypeDef:
        """
        Gets the user pool multi-factor authentication (MFA) configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_user_pool_mfa_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_user_pool_mfa_config)
        """

    async def global_sign_out(
        self, **kwargs: Unpack[GlobalSignOutRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Invalidates the identity, access, and refresh tokens that Amazon Cognito issued
        to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/global_sign_out.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#global_sign_out)
        """

    async def initiate_auth(
        self, **kwargs: Unpack[InitiateAuthRequestTypeDef]
    ) -> InitiateAuthResponseTypeDef:
        """
        Initiates sign-in for a user in the Amazon Cognito user directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/initiate_auth.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#initiate_auth)
        """

    async def list_devices(
        self, **kwargs: Unpack[ListDevicesRequestTypeDef]
    ) -> ListDevicesResponseTypeDef:
        """
        Lists the sign-in devices that Amazon Cognito has registered to the current
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_devices.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_devices)
        """

    async def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestTypeDef]
    ) -> ListGroupsResponseTypeDef:
        """
        Lists the groups associated with a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_groups)
        """

    async def list_identity_providers(
        self, **kwargs: Unpack[ListIdentityProvidersRequestTypeDef]
    ) -> ListIdentityProvidersResponseTypeDef:
        """
        Lists information about all IdPs for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_identity_providers.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_identity_providers)
        """

    async def list_resource_servers(
        self, **kwargs: Unpack[ListResourceServersRequestTypeDef]
    ) -> ListResourceServersResponseTypeDef:
        """
        Lists the resource servers for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_resource_servers.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_resource_servers)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are assigned to an Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_tags_for_resource)
        """

    async def list_user_import_jobs(
        self, **kwargs: Unpack[ListUserImportJobsRequestTypeDef]
    ) -> ListUserImportJobsResponseTypeDef:
        """
        Lists user import jobs for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_user_import_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_user_import_jobs)
        """

    async def list_user_pool_clients(
        self, **kwargs: Unpack[ListUserPoolClientsRequestTypeDef]
    ) -> ListUserPoolClientsResponseTypeDef:
        """
        Lists the clients that have been created for the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_user_pool_clients.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_user_pool_clients)
        """

    async def list_user_pools(
        self, **kwargs: Unpack[ListUserPoolsRequestTypeDef]
    ) -> ListUserPoolsResponseTypeDef:
        """
        Lists the user pools associated with an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_user_pools.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_user_pools)
        """

    async def list_users(
        self, **kwargs: Unpack[ListUsersRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Lists users and their basic details in a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_users.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_users)
        """

    async def list_users_in_group(
        self, **kwargs: Unpack[ListUsersInGroupRequestTypeDef]
    ) -> ListUsersInGroupResponseTypeDef:
        """
        Lists the users in the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_users_in_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_users_in_group)
        """

    async def list_web_authn_credentials(
        self, **kwargs: Unpack[ListWebAuthnCredentialsRequestTypeDef]
    ) -> ListWebAuthnCredentialsResponseTypeDef:
        """
        Generates a list of the current user's registered passkey, or webauthN,
        credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_web_authn_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_web_authn_credentials)
        """

    async def resend_confirmation_code(
        self, **kwargs: Unpack[ResendConfirmationCodeRequestTypeDef]
    ) -> ResendConfirmationCodeResponseTypeDef:
        """
        Resends the confirmation (for confirmation of registration) to a specific user
        in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/resend_confirmation_code.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#resend_confirmation_code)
        """

    async def respond_to_auth_challenge(
        self, **kwargs: Unpack[RespondToAuthChallengeRequestTypeDef]
    ) -> RespondToAuthChallengeResponseTypeDef:
        """
        Some API operations in a user pool generate a challenge, like a prompt for an
        MFA code, for device authentication that bypasses MFA, or for a custom
        authentication challenge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/respond_to_auth_challenge.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#respond_to_auth_challenge)
        """

    async def revoke_token(self, **kwargs: Unpack[RevokeTokenRequestTypeDef]) -> Dict[str, Any]:
        """
        Revokes all of the access tokens generated by, and at the same time as, the
        specified refresh token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/revoke_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#revoke_token)
        """

    async def set_log_delivery_configuration(
        self, **kwargs: Unpack[SetLogDeliveryConfigurationRequestTypeDef]
    ) -> SetLogDeliveryConfigurationResponseTypeDef:
        """
        Sets up or modifies the logging configuration of a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/set_log_delivery_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_log_delivery_configuration)
        """

    async def set_risk_configuration(
        self, **kwargs: Unpack[SetRiskConfigurationRequestTypeDef]
    ) -> SetRiskConfigurationResponseTypeDef:
        """
        Configures actions on detected risks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/set_risk_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_risk_configuration)
        """

    async def set_ui_customization(
        self, **kwargs: Unpack[SetUICustomizationRequestTypeDef]
    ) -> SetUICustomizationResponseTypeDef:
        """
        Sets the user interface (UI) customization information for a user pool's
        built-in app UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/set_ui_customization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_ui_customization)
        """

    async def set_user_mfa_preference(
        self, **kwargs: Unpack[SetUserMFAPreferenceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set the user's multi-factor authentication (MFA) method preference, including
        which MFA factors are activated and if any are preferred.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/set_user_mfa_preference.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_user_mfa_preference)
        """

    async def set_user_pool_mfa_config(
        self, **kwargs: Unpack[SetUserPoolMfaConfigRequestTypeDef]
    ) -> SetUserPoolMfaConfigResponseTypeDef:
        """
        Sets the user pool multi-factor authentication (MFA) and passkey configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/set_user_pool_mfa_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_user_pool_mfa_config)
        """

    async def set_user_settings(
        self, **kwargs: Unpack[SetUserSettingsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        <i>This action is no longer supported.</i> You can use it to configure only SMS
        MFA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/set_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_user_settings)
        """

    async def sign_up(self, **kwargs: Unpack[SignUpRequestTypeDef]) -> SignUpResponseTypeDef:
        """
        Registers the user in the specified user pool and creates a user name,
        password, and user attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/sign_up.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#sign_up)
        """

    async def start_user_import_job(
        self, **kwargs: Unpack[StartUserImportJobRequestTypeDef]
    ) -> StartUserImportJobResponseTypeDef:
        """
        Starts the user import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/start_user_import_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#start_user_import_job)
        """

    async def start_web_authn_registration(
        self, **kwargs: Unpack[StartWebAuthnRegistrationRequestTypeDef]
    ) -> StartWebAuthnRegistrationResponseTypeDef:
        """
        Requests credential creation options from your user pool for registration of a
        passkey authenticator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/start_web_authn_registration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#start_web_authn_registration)
        """

    async def stop_user_import_job(
        self, **kwargs: Unpack[StopUserImportJobRequestTypeDef]
    ) -> StopUserImportJobResponseTypeDef:
        """
        Stops the user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/stop_user_import_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#stop_user_import_job)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns a set of tags to an Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from an Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#untag_resource)
        """

    async def update_auth_event_feedback(
        self, **kwargs: Unpack[UpdateAuthEventFeedbackRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Provides the feedback for an authentication event, whether it was from a valid
        user or not.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_auth_event_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_auth_event_feedback)
        """

    async def update_device_status(
        self, **kwargs: Unpack[UpdateDeviceStatusRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the device status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_device_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_device_status)
        """

    async def update_group(
        self, **kwargs: Unpack[UpdateGroupRequestTypeDef]
    ) -> UpdateGroupResponseTypeDef:
        """
        Updates the specified group with the specified attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_group)
        """

    async def update_identity_provider(
        self, **kwargs: Unpack[UpdateIdentityProviderRequestTypeDef]
    ) -> UpdateIdentityProviderResponseTypeDef:
        """
        Updates IdP information for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_identity_provider)
        """

    async def update_managed_login_branding(
        self, **kwargs: Unpack[UpdateManagedLoginBrandingRequestTypeDef]
    ) -> UpdateManagedLoginBrandingResponseTypeDef:
        """
        Configures the branding settings for a user pool style.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_managed_login_branding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_managed_login_branding)
        """

    async def update_resource_server(
        self, **kwargs: Unpack[UpdateResourceServerRequestTypeDef]
    ) -> UpdateResourceServerResponseTypeDef:
        """
        Updates the name and scopes of resource server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_resource_server.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_resource_server)
        """

    async def update_user_attributes(
        self, **kwargs: Unpack[UpdateUserAttributesRequestTypeDef]
    ) -> UpdateUserAttributesResponseTypeDef:
        """
        With this operation, your users can update one or more of their attributes with
        their own credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_user_attributes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_attributes)
        """

    async def update_user_pool(
        self, **kwargs: Unpack[UpdateUserPoolRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This action might generate an SMS text message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_user_pool.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_pool)
        """

    async def update_user_pool_client(
        self, **kwargs: Unpack[UpdateUserPoolClientRequestTypeDef]
    ) -> UpdateUserPoolClientResponseTypeDef:
        """
        Updates the specified user pool app client with the specified attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_user_pool_client.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_pool_client)
        """

    async def update_user_pool_domain(
        self, **kwargs: Unpack[UpdateUserPoolDomainRequestTypeDef]
    ) -> UpdateUserPoolDomainResponseTypeDef:
        """
        A user pool domain hosts managed login, an authorization server and web server
        for authentication in your application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/update_user_pool_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_pool_domain)
        """

    async def verify_software_token(
        self, **kwargs: Unpack[VerifySoftwareTokenRequestTypeDef]
    ) -> VerifySoftwareTokenResponseTypeDef:
        """
        Use this API to register a user's entered time-based one-time password (TOTP)
        code and mark the user's software token MFA status as "verified" if successful.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/verify_software_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#verify_software_token)
        """

    async def verify_user_attribute(
        self, **kwargs: Unpack[VerifyUserAttributeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Verifies the specified user attributes in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/verify_user_attribute.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#verify_user_attribute)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["admin_list_groups_for_user"]
    ) -> AdminListGroupsForUserPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["admin_list_user_auth_events"]
    ) -> AdminListUserAuthEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_groups"]
    ) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_identity_providers"]
    ) -> ListIdentityProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_servers"]
    ) -> ListResourceServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_user_pool_clients"]
    ) -> ListUserPoolClientsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_user_pools"]
    ) -> ListUserPoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_users_in_group"]
    ) -> ListUsersInGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_users"]
    ) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)
        """
