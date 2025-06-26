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

from collections.abc import Sequence
from types import TracebackType
from typing import Any, Callable, Mapping, TypedDict

from pydantic import BaseModel

from datarobot.auth.exceptions import OAuthFlowError, OAuthProviderNotFound, OAuthValidationErr
from datarobot.auth.oauth import (
    AsyncOAuthComponent,
    OAuthData,
    OAuthFlowSession,
    OAuthProvider,
    OAuthToken,
    Profile,
    SyncOAuthComponent,
)
from datarobot.auth.utils import syncify

try:
    from authlib.integrations.base_client import BaseApp, BaseOAuth, FrameworkIntegration
    from authlib.integrations.base_client.async_app import AsyncOAuth2Mixin
    from authlib.integrations.base_client.async_openid import AsyncOpenIDMixin
    from authlib.integrations.httpx_client import AsyncOAuth2Client
    from authlib.oauth2.rfc6749 import OAuth2Token
except ImportError as e:
    raise ImportError(
        "Authlib-based OAuth2 implementation require installation of datarobot library, "
        "with optional `auth-authlib` dependency. To install library with image support"
        "please use `pip install datarobot[auth-authlib]`"
    ) from e


class _AsyncOAuth2App(AsyncOAuth2Mixin, AsyncOpenIDMixin, BaseApp):  # type: ignore[misc]
    client_cls = AsyncOAuth2Client


class _AgnosticFrameworkIntegration(FrameworkIntegration):  # type: ignore[misc]
    @staticmethod
    def load_config(oauth: BaseOAuth, name: str, params: list[str]) -> dict[str, Any]:
        return {}


class _AsyncAgnosticOAuth(BaseOAuth):  # type: ignore[misc]
    # we can enable oauth1 client cls here as well if needed
    oauth2_client_cls = _AsyncOAuth2App
    framework_integration_cls = _AgnosticFrameworkIntegration


UserInfoMapper = Callable[[Mapping[str, Any]], Profile]


class ServerMetadata(TypedDict, total=False):
    """
    Metadata about the OAuth2 server, including userinfo endpoint and mapper.
    """

    userinfo_endpoint: str | None
    userinfo_mapper: UserInfoMapper | None


class OAuthProviderConfig(BaseModel):
    """
    Configuration for an OAuth2 provider to be used with Authlib.
    """

    id: str
    """The unique identifier for the OAuth2 provider."""
    client_id: str
    """The OAuth2 client ID."""
    client_secret: str
    """The OAuth2 client secret."""
    scope: str | None = None
    """The OAuth2 scope to request during authorization (a space-separated string)."""
    client_kwargs: dict[str, Any] | None = None
    """Additional client configuration parameters for the OAuth2 client."""
    server_metadata_url: str | None = None
    """The URL to fetch OAuth2 provider server metadata."""
    authorize_url: str | None = None
    """The URL to redirect the user to for OAuth2 authorization consent."""
    authorize_params: dict[str, Any] | None = None
    """Additional parameters to include in the authorization request."""
    access_token_url: str | None = None
    """The URL to exchange the authorization code for an access token."""
    access_token_params: dict[str, Any] | None = None
    """Additional parameters to include in the access token request."""
    userinfo_endpoint: str | None = None
    """The URL to fetch user information after authorization."""

    userinfo_mapper: UserInfoMapper | None = None
    """A custom function to map user information from the userinfo endpoint in case it's not in the OIDC format."""

    def to_authlib_config(self) -> dict[str, Any]:
        client_kwargs = self.client_kwargs or {}

        if self.scope:
            client_kwargs["scope"] = self.scope

        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "client_kwargs": client_kwargs,
            "authorize_url": self.authorize_url,
            "authorize_params": self.authorize_params or {},
            "access_token_url": self.access_token_url,
            "access_token_params": self.access_token_params or {},
            "server_metadata_url": self.server_metadata_url,
            "userinfo_endpoint": self.userinfo_endpoint,
            # this is a custom function, authlib doesn't know about it, but it would carry it around for us
            "userinfo_mapper": self.userinfo_mapper,
        }


class AsyncOAuth(AsyncOAuthComponent):
    """
    Asyncio OAuth2 component implementation using Authlib.
    """

    def __init__(
        self,
        provider_config: Sequence[OAuthProviderConfig] = (),
    ) -> None:
        """
        Initialize the AsyncOAuth component with a list of OAuth provider configurations.

        Args:
            provider_config: A sequence of OAuthProviderConfig objects containing
                the configuration for each OAuth provider.
        """
        self.providers = _AsyncAgnosticOAuth()

        for config in provider_config:
            self.providers.register(
                config.id,
                **config.to_authlib_config(),
            )

    async def __aenter__(self) -> "AsyncOAuthComponent":
        """
        No-op implementation for the async context manager.
        Authlib implementation doesn't require any setup
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        """
        No-op implementation for the async context manager.
        Authlib implementation doesn't require any shutdown or cleanup
        """

    async def close(self) -> None:
        """
        Close the HTTP client connection.
        This is an alias for __aexit__ to maintain compatibility with the OAuthComponent interface.
        Authlib implementation doesn't require any shutdown or cleanup
        """

    async def get_providers(
        self,
    ) -> list[OAuthProvider]:
        providers = []

        for provider_id, config in self.providers._registry.items():
            _, client_config = config

            providers.append(
                OAuthProvider(
                    # we have purely system information in case of authlib
                    id=provider_id,
                    name=provider_id,
                    type=provider_id,
                    client_id=client_config.get("client_id"),
                )
            )

        return providers

    def register(self, config: OAuthProviderConfig) -> None:
        self.providers.register(
            config.id,
            **config.to_authlib_config(),
        )

    def get_provider(self, provider_id: str) -> _AsyncOAuth2App:
        """
        Get the OAuth2 provider client by its ID.

        Args:
            provider_id: The unique identifier for the OAuth2 provider.

        Raises:
            OAuthProviderNotFound: If the provider with the specified ID is not found.

        Returns:
            An instance of _AsyncOAuth2App representing the OAuth2 provider client.
        """
        provider: _AsyncOAuth2App = self.providers.create_client(provider_id)

        if provider is None:
            raise OAuthProviderNotFound(f"Provider {provider_id} not found")

        return provider

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
        Get the authorization URL for the specified OAuth provider.

        Raises:
            OAuthProviderNotFound: If the provider with the specified ID is not found.
        """
        provider = self.get_provider(provider_id)

        authz_data = await provider.create_authorization_url(
            redirect_uri=redirect_uri,
            state=state,
            code_verifier=code_verifier,
            **kwargs,
        )

        return OAuthFlowSession(
            provider_id=provider_id,
            authorization_url=authz_data["url"],
            redirect_uri=redirect_uri,
            state=authz_data.get("state"),
            nonce=authz_data.get("nonce"),
            code_verifier=authz_data.get("code_verifier"),
        )

    async def exchange_code(
        self,
        *,
        provider_id: str,
        sess: OAuthFlowSession,
        params: Mapping[str, Any],
        **kwargs: Any,
    ) -> OAuthData:
        """
        Exchange the authorization code for an access token and user profile.

        Raises:
            OAuthProviderNotFound: If the provider with the specified ID is not found.
            OAuthFlowError: If there is an error during the OAuth flow.
        """
        provider = self.get_provider(provider_id)

        params = dict(params)

        if error := params.get("error"):
            raise OAuthFlowError(
                provider_id=provider_id,
                error_code=error,
                message=params.get("error_description", "OAuth flow failed"),
            )

        if sess.code_verifier:
            params["code_verifier"] = sess.code_verifier

        if sess.redirect_uri:
            params["redirect_uri"] = sess.redirect_uri

        claims_options = kwargs.pop("claims_options", None)
        claims_cls = kwargs.pop("claims_cls", None)
        leeway = kwargs.pop("leeway", 120)

        token_data = await provider.fetch_access_token(
            **params, **kwargs
        )  # TODO: handle authlib.integrations.base_client.errors.OAuthError

        user_profile: Profile | None = None

        if "id_token" in token_data and sess.nonce is not None:
            userinfo = await provider.parse_id_token(
                token_data,
                nonce=sess.nonce,
                claims_options=claims_options,
                claims_cls=claims_cls,
                leeway=leeway,
            )

            user_profile = Profile(**userinfo)

        server_metadata: ServerMetadata = provider.server_metadata

        if not user_profile and "userinfo_endpoint" in server_metadata:
            # this is the case when OpenID Connect is not supported by provider
            user_data = await provider.userinfo(token=token_data)
            mapper = server_metadata.get("userinfo_mapper")
            user_profile = mapper(user_data) if mapper else Profile(**user_data)

        return OAuthData(
            token_data=OAuthToken.from_dict(token_data),
            provider=OAuthProvider(
                id=provider_id,
                name=provider_id,
                type=provider_id,
                client_id=token_data.get("client_id"),
            ),
            user_profile=user_profile,
        )

    async def refresh_access_token(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        scope: str | None = None,
        refresh_token: str | None = None,
    ) -> OAuthToken:
        """
        Refresh the access token for the specified OAuth provider using the refresh token.

        Raises:
            OAuthValidationErr: If the provider ID or refresh token is not provided.
            OAuthProviderNotFound: If the provider with the specified ID is not found.
        """
        if provider_id is None:
            raise OAuthValidationErr(
                "Provider ID is required to obtain new access token via Authlib"
            )

        if refresh_token is None:
            raise OAuthValidationErr(
                "Refresh token is required to obtain new access token via Authlib"
            )

        provider = self.get_provider(provider_id)

        # authlib doesn't provide any refresh token methods:
        # https://docs.authlib.org/en/latest/client/oauth2.html#automatically-refreshing-tokens
        token_data = await provider.fetch_access_token(
            grant_type="refresh_token",
            refresh_token=refresh_token,
            scope=scope,
        )

        return OAuthToken.from_dict(token_data)

    async def get_user_info(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        access_token: str | None = None,
    ) -> Profile:
        """
        Get the user profile information for the specified OAuth provider.

        Raises:
            OAuthValidationErr: If the provider ID or access token is not provided.
            OAuthProviderNotFound: If the provider with the specified ID is not found.
        """
        if provider_id is None:
            raise OAuthValidationErr(
                "Provider ID is required to obtain new access token via Authlib"
            )

        if access_token is None:
            raise OAuthValidationErr("Access token is required to get user info via Authlib")

        provider = self.providers.create_client(provider_id)

        token_data = OAuth2Token(
            {
                "access_token": access_token,
                "expires_at": 0,
            }
        )

        user_data = await provider.userinfo(token=token_data)
        server_metadata: ServerMetadata = provider.server_metadata

        if user_info_mapper := server_metadata.get("userinfo_mapper"):
            # this is the case when OpenID Connect is not supported by provider
            return user_info_mapper(user_data)

        return Profile(**user_data)


class SyncOAuth(SyncOAuthComponent):
    """
    Synchronous OAuth client for managing OAuth providers and flows via Authlib.
    """

    def __init__(
        self,
        provider_config: Sequence[OAuthProviderConfig] = (),
    ) -> None:
        self._async = AsyncOAuth(provider_config=provider_config)

    def __enter__(self) -> "SyncOAuthComponent":
        """
        No-op implementation for the synchronous context manager.
        Authlib implementation doesn't require any setup
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        """
        No-op implementation for the synchronous context manager.
        Authlib implementation doesn't require any shutdown or cleanup
        """

    def close(self) -> None:
        """
        Close the HTTP client connection.
        This is an alias for __exit__ to maintain compatibility with the OAuthComponent interface.
        Authlib implementation doesn't require any shutdown or cleanup
        """

    def get_providers(self) -> list[OAuthProvider]:
        """
        Get the list of OAuth providers.

        Raises:
            OAuthProviderNotFound: If the provider with the specified ID is not found.
        """
        return syncify(self._async.get_providers)()

    def register(self, config: OAuthProviderConfig) -> None:
        """
        Register a new OAuth provider configuration.
        """
        self._async.register(config)

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
        Get the authorization URL for the specified OAuth provider.

        Raises:
            OAuthProviderNotFound: If the provider with the specified ID is not found.
        """
        return syncify(self._async.get_authorization_url)(
            provider_id=provider_id,
            redirect_uri=redirect_uri,
            state=state,
            code_verifier=code_verifier,
            **kwargs,
        )

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
        Exchange the authorization code for an access token and user profile.

        Raises:
            OAuthProviderNotFound: If the provider with the specified ID is not found.
            OAuthFlowError: If there is an error during the OAuth flow.
        """
        return syncify(self._async.exchange_code)(
            provider_id=provider_id,
            sess=sess,
            params=params,
            **kwargs,
        )

    def refresh_access_token(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        scope: str | None = None,
        refresh_token: str | None = None,
    ) -> OAuthToken:
        """
        Refresh the access token for the specified OAuth provider.

        Raises:
            OAuthValidationErr: If the provider ID or refresh token is not provided.
            OAuthProviderNotFound: If the provider with the specified ID is not found.
        """
        return syncify(self._async.refresh_access_token)(
            provider_id=provider_id,
            identity_id=identity_id,
            scope=scope,
            refresh_token=refresh_token,
        )

    def get_user_info(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        access_token: str | None = None,
    ) -> Profile:
        """
        Get the user profile information for the specified OAuth provider.

        Raises:
            OAuthValidationErr: If the provider ID or access token is not provided.
            OAuthProviderNotFound: If the provider with the specified ID is not found.
        """
        return syncify(self._async.get_user_info)(
            provider_id=provider_id,
            identity_id=identity_id,
            access_token=access_token,
        )
