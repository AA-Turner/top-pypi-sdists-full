#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
# limitations under the License.
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import TracebackType
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Protocol

from datarobot.auth.typing import Metadata


class OAuthProvider(BaseModel):
    """
    OAuth provider data model.
    """

    id: str
    """The unique identifier for the OAuth2 provider."""
    name: str
    """The name of the OAuth2 provider."""
    status: str | None = None
    """The status of the OAuth2 provider (e.g., 'active', 'inactive')."""
    type: str
    """The type of the OAuth2 provider (e.g., 'google', 'box')."""
    client_id: str | None = None
    """The client ID for the OAuth2 provider."""
    metadata: Metadata | None = Field(default_factory=lambda: {})
    """Additional metadata about the OAuth2 provider."""

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    def collect_metadata(  # pylint: disable=no-self-argument
        cls,
        values: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Collect metadata from the raw OAuth provider data.
        """
        known = set(cls.model_fields.keys())  # pylint: disable=no-member
        extra = {k: v for k, v in values.items() if k not in known}

        if "metadata" not in values:
            values["metadata"] = {}

        values["metadata"].update(extra)

        return values


class OAuthFlowSession(BaseModel):
    """
    OAuth flow session data model.
    Holds temporary OAuth flow state from the redirect point to the callback.
    """

    provider_id: str
    """The ID of the OAuth2 provider."""
    authorization_url: str
    """The authorization URL to redirect the user to for OAuth2 authorization consent."""
    redirect_uri: str
    """The redirect URI to use after authorization."""
    state: str
    """The state parameter to maintain state between request and callback."""
    nonce: str | None = None
    """The nonce parameter for OpenID Connect flows."""
    code_verifier: str | None = None
    """The code verifier for PKCE (Proof Key for Code Exchange) flows."""

    model_config = ConfigDict(extra="ignore")


class Profile(BaseModel):
    """
    OAuth User profile data model. Based on the OpenID Connect standard (with a few more common fields).
    """

    id: str = Field(alias="sub")
    """The unique identifier for the user in the OAuth2 provider."""
    nickname: str | None = Field(None, alias="preferred_username")
    """The nickname or preferred username of the user."""
    name: str | None = None
    """The full name of the user."""
    given_name: str | None = Field(None, alias="first_name")
    """The given name of the user."""
    family_name: str | None = Field(None, alias="last_name")
    """The family name of the user."""
    email: str
    """The email address of the user."""
    email_verified: bool | None = None
    """Indicates whether the user's email address has been verified."""
    phone_number: str | None = None
    """The phone number of the user, if available."""
    photo_url: str | None = Field(None, alias="picture")
    """The URL of the user's profile picture, if available."""
    locale: str | None = None
    """The locale of the user, if available."""
    metadata: Metadata | None = Field(default_factory=lambda: {})
    """Additional metadata about the user, if available."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    @model_validator(mode="before")
    def collect_metadata(  # pylint: disable=no-self-argument
        cls,
        values: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Collect metadata from the raw profile data in order to let consumers
        access any custom data retrieved from the OAuth2 provider.
        """
        if not values:
            return values

        known = set(cls.model_fields.keys())  # pylint: disable=no-member
        extra = {k: v for k, v in values.items() if k not in known}

        if "metadata" not in values:
            values["metadata"] = {}

        values["metadata"].update(extra)

        return values


class OAuthToken(BaseModel):
    """
    OAuth2 access token data model.
    """

    access_token: str
    """The access token issued by the OAuth2 provider."""
    token_type: str | None = None
    """The type of the access token (e.g., 'Bearer')."""
    expires_in: int | None = None
    """The number of seconds until the access token expires."""
    expires_at: datetime | None = None
    """The timestamp when the access token expires, in UTC timezone."""
    refresh_token: str | None = None
    """The refresh token to use for refreshing the access token."""
    id_token: str | None = None
    """The ID token issued by the OAuth2 provider, if available."""
    scope: str | None = None
    """The scope of the access token, if available."""

    @classmethod
    def from_dict(cls, raw_data: dict[str, Any]) -> "OAuthToken":
        """
        Create an OAuthToken instance from a dictionary.
        """
        expires_in = raw_data.get("expires_in")
        expires_at = raw_data.get("expires_at")

        if expires_at:
            # let's make sure it's timezoned timestamp, otherwise we will get an error e.g.
            # TypeError: can't compare offset-naive and offset-aware datetimes
            expires_at = datetime.fromtimestamp(expires_at, timezone.utc)

        if expires_in and not expires_at:
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        return cls(
            access_token=raw_data["access_token"],
            token_type=raw_data.get("token_type"),
            expires_in=expires_in,
            expires_at=expires_at,
            scope=raw_data.get("scope"),
            refresh_token=raw_data.get("refresh_token"),
        )


class OAuthData(BaseModel):
    token_data: OAuthToken | None = None
    authorization_id: str | None = None
    provider: OAuthProvider
    user_profile: Profile | None = None


class AsyncOAuthComponent(Protocol):
    """
    Async OAuth2 component interface. All async implementations must fulfill this interface.
    """

    async def get_providers(self) -> list[OAuthProvider]:
        """
        Get the list of OAuth2 providers.
        """

    async def get_authorization_url(
        self,
        *,
        provider_id: str,
        redirect_uri: str,
        state: str | None = None,
        code_verifier: str | None = None,
        **kwargs: Any,
    ) -> OAuthFlowSession:
        """
        Get the authorization URL for the specified OAuth2 provider.
        Optionally, you can control the state and code_verifier parameters
        if the underlying OAuth implementation supports overriding them.

        Args:
            provider_id: The ID of the OAuth2 provider.
            redirect_uri: The redirect URI to use after authorization.
            state: Optional state parameter to maintain state between request and callback.
            code_verifier: Optional code verifier for PKCE flow.
            **kwargs: Additional parameters that may be required by the specific OAuth2 provider.

        Returns:
            An OAuthFlowSession object containing the authorization URL and OAuth2 state.
        """

    async def exchange_code(
        self,
        *,
        provider_id: str,
        sess: OAuthFlowSession,
        params: Mapping[str, Any],
        # TODO: we can probably do a better job informing users what kwargs & claims_options could be in typing
        **kwargs: Any,
    ) -> OAuthData:
        """
        Exchange the OAuth2 authorization code for an access token and user profile.

        Args:
            provider_id: The ID of the OAuth2 provider.
            sess: The OAuthFlowSession object containing the state of the OAuth flow.
            params: Additional parameters to pass to the token endpoint.
            **kwargs: Additional parameters that may be required by the specific OAuth2 provider.

        Returns:
            An OAuthData object containing the access token, user profile, and provider information.
        """

    async def refresh_access_token(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        scope: str | None = None,
        refresh_token: str | None = None,
    ) -> OAuthToken:
        """
        Refresh the OAuth2 access token for the specified provider and identity.

        Depending on the implementation, you may have to provide
        either `identity_id` or `refresh_token`
        (if your implementation doesn't manage tokens for you just like authlib).

        Args:
            provider_id: The ID of the OAuth2 provider.
            identity_id: The ID of the identity to refresh the token for.
            scope: Optional scope to request during the refresh.
            refresh_token: The refresh token to use for refreshing the access token.

        Returns:
            An OAuthToken object containing the refreshed access token and other token details.
        """

    async def get_user_info(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        access_token: str | None = None,
    ) -> Profile:
        """
        Get the user profile for the specified provider and identity.

        Depending on the implementation, you may have to provide
        either `identity_id` or `access_token`
        (if your implementation doesn't manage tokens for you just like authlib).

        Args:
            provider_id: The ID of the OAuth2 provider.
            identity_id: The ID of the identity to get the user profile for.
            access_token: The access token to use for retrieving the user profile.

        Returns:
            A Profile object containing the user's profile information.
        """

    async def __aenter__(self) -> "AsyncOAuthComponent":
        """
        Asynchronous context manager entry method.
        This method should be implemented if you need any initialization for your OAuth implementation.
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        """
        Asynchronous context manager exit method.
        This method should be implemented if you need any cleanup for your OAuth implementation.
        """

    async def close(self) -> None:
        """
        Close the OAuth component.
        This method should be implemented if you need to release any resources or connections.
        It is called automatically when the component is used as an asynchronous context manager.
        """


class SyncOAuthComponent(Protocol):
    """
    Sync OAuth2 component interface. All sync implementations must fulfill this interface.
    """

    def get_providers(self) -> list[OAuthProvider]:
        """
        Get the list of OAuth2 providers.
        """

    def get_authorization_url(
        self,
        *,
        provider_id: str,
        redirect_uri: str,
        state: str | None = None,
        code_verifier: str | None = None,
        **kwargs: Any,
    ) -> OAuthFlowSession:
        """
        Get the authorization URL for the specified OAuth2 provider.
        Optionally, you can control the state and code_verifier parameters
        if the underlying OAuth implementation supports overriding them.

        Args:
            provider_id: The ID of the OAuth2 provider.
            redirect_uri: The redirect URI to use after authorization.
            state: Optional state parameter to maintain state between request and callback.
            code_verifier: Optional code verifier for PKCE flow.
            **kwargs: Additional parameters that may be required by the specific OAuth2 provider.

        Returns:
            An OAuthFlowSession object containing the authorization URL and OAuth2 state.
        """

    def exchange_code(
        self,
        *,
        provider_id: str,
        sess: OAuthFlowSession,
        params: Mapping[str, Any],
        # TODO: we can probably do a better job informing users what kwargs & claims_options could be in typing
        **kwargs: Any,
    ) -> OAuthData:
        """
        Exchange the OAuth2 authorization code for an access token and user profile.

        Args:
            provider_id: The ID of the OAuth2 provider.
            sess: The OAuthFlowSession object containing the state of the OAuth flow.
            params: Additional parameters to pass to the token endpoint.
            **kwargs: Additional parameters that may be required by the specific OAuth2 provider.

        Returns:
            An OAuthData object containing the access token, user profile, and provider information.
        """

    def refresh_access_token(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        scope: str | None = None,
        refresh_token: str | None = None,
    ) -> OAuthToken:
        """
        Refresh the OAuth2 access token for the specified provider and identity.

        Depending on the implementation, you may have to provide
        either `identity_id` or `refresh_token`
        (if your implementation doesn't manage tokens for you just like authlib).

        Args:
            provider_id: The ID of the OAuth2 provider.
            identity_id: The ID of the identity to refresh the token for.
            scope: Optional scope to request during the refresh.
            refresh_token: The refresh token to use for refreshing the access token.

        Returns:
            An OAuthToken object containing the refreshed access token and other token details.
        """

    def get_user_info(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        access_token: str | None = None,
    ) -> Profile:
        """
        Get the user profile for the specified provider and identity.

        Depending on the implementation, you may have to provide
        either `identity_id` or `access_token`
        (if your implementation doesn't manage tokens for you just like authlib).

        Args:
            provider_id: The ID of the OAuth2 provider.
            identity_id: The ID of the identity to get the user profile for.
            access_token: The access token to use for retrieving the user profile.

        Returns:
            A Profile object containing the user's profile information.
        """

    def __enter__(self) -> "SyncOAuthComponent":
        """
        Synchronous Context manager entry method.
        This method should be implemented if you need any initialization for your OAuth implementation.
        """

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        """
        Synchronous context manager exit method.
        This method should be implemented if you need any cleanup for your OAuth implementation.
        """

    def close(self) -> None:
        """
        Close the OAuth component.
        This method should be implemented if you need to release any resources or connections.
        It is called automatically when the component is used as a synchronous context manager.
        """
