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

from datetime import datetime
import os
import platform
from types import TracebackType
from typing import Any, Mapping, Sequence, TYPE_CHECKING, Union
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, ConfigDict, Field

from datarobot._version import __version__
from datarobot.auth.datarobot.exceptions import (
    OAuthAuthorizationExpired,
    OAuthAuthorizationNotFound,
    OAuthServiceProviderNotFound,
    raise_http_exception,
)
from datarobot.auth.exceptions import OAuthFlowError, OAuthValidationErr
from datarobot.auth.oauth import (
    AsyncOAuthComponent,
    OAuthData,
    OAuthFlowSession,
    OAuthProvider,
    OAuthToken,
    Profile,
    SyncOAuthComponent,
)
from datarobot.auth.typing import Metadata
from datarobot.auth.utils import syncify
from datarobot.utils import camelize

if TYPE_CHECKING:
    import ssl


class _DRSchema(BaseModel):
    """
    The base schema that configures Pydantic to properly handle DataRobot API responses.
    """

    model_config = ConfigDict(
        alias_generator=camelize,
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )


class _DROAuthProvider(_DRSchema):
    """
    DataRobot OAuth2 provider response schema.
    """

    id: str
    created_at: datetime
    updated_at: datetime
    name: str
    org_id: str | None = None
    type: str
    status: str
    client_id: str
    secure_config_id: str | None = None
    metadata: dict[str, Any] | None = Field(default_factory=lambda: {})

    def to_data(self) -> OAuthProvider:
        """
        Convert the DataRobot OAuth provider schema to the internal OAuthProvider model.
        """
        metadata = self.metadata or {}
        metadata.update(  # pylint: disable=no-member
            {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "org_id": self.org_id,
                "secure_config_id": self.secure_config_id,
            }
        )

        return OAuthProvider(
            id=self.id,
            name=self.name,
            status=self.status,
            type=self.type,
            client_id=self.client_id,
            metadata=metadata,
        )


class _DROAuthRedirectData(_DRSchema):
    state: str
    redirect_url: str


class _DROAuthProviders(_DRSchema):
    data: list[_DROAuthProvider] = Field(default_factory=list)


class _DROAuthAuthorization(_DRSchema):
    id: str
    created_at: datetime
    user_id: str
    org_id: str | None = None
    status: str
    oauth_client_id: str
    credential_id: str
    refresh_token_expires_at: datetime | None = None
    provider: _DROAuthProvider


class _DROAuthTokenData(_DRSchema):
    """
    DataRobot OAuth token response schema.
    """

    access_token: str
    expires_at: datetime | None = None
    authorized_oauth_provider: _DROAuthAuthorization

    def to_data(self) -> OAuthToken:
        """
        Convert the DataRobot OAuth token schema to the internal OAuthToken model.
        """
        return OAuthToken(
            access_token=self.access_token,
            expires_at=self.expires_at,
        )


class _DROAuthUserProfile(_DRSchema):
    """
    DataRobot user profile response schema.
    """

    sub: str
    email: str
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    nickname: str | None = None
    description: str | None = None
    picture: str | None = None
    locale: str | None = None
    raw: Metadata | None = Field(default_factory=lambda: {})

    def to_data(self) -> Profile:
        """
        Convert the DataRobot user profile schema to the internal Profile model.
        """
        raw_data = {}

        if self.raw:
            raw_data = dict(self.raw)

        raw_data.update(
            {
                "description": self.description,
            }
        )

        return Profile(
            id=self.sub,
            email=self.email,
            name=self.name,
            first_name=self.given_name,
            last_name=self.family_name,
            preferred_username=self.nickname,
            picture=self.picture,
            locale=self.locale,
            metadata=raw_data,
        )


class _DROAuthData(_DRSchema):
    """
    DataRobot OAuth2 callback response schema.
    """

    authorized_provider: _DROAuthAuthorization
    user_info: _DROAuthUserProfile


class AsyncOAuth(AsyncOAuthComponent):
    """
    Asyncio OAuth2 implementation based on the DataRobot API.
    """

    def __init__(
        self,
        oauth_provider_ids: Sequence[str] = (),
        *,
        datarobot_endpoint: str | None = None,
        datarobot_api_token: str | None = None,
        http_client: httpx.AsyncClient | None = None,
        user_agent: str | None = None,
        follow_redirects: bool = True,
        timeout: float | httpx.Timeout | None = 5.0,
        ssl_verify: Union[
            bool, "ssl.SSLContext"
        ] = True,  # just "|" thrown "unsupported operand type" error
    ) -> None:
        """
        Initialize the AsyncOAuth client.

        Args:
            oauth_provider_ids: A sequence of OAuth provider IDs to register.
            datarobot_endpoint: The DataRobot API endpoint URL. If not provided,
                it will be read from the environment variable DATAROBOT_ENDPOINT.
            datarobot_api_token: The DataRobot API token. If not provided,
                it will be read from the environment variable DATAROBOT_API_TOKEN.
            http_client: An optional HTTP client to use for requests.
                If not provided, a new AsyncClient will be created.
            user_agent: An optional user agent string to use for requests.
            follow_redirects: Whether to follow redirects in HTTP requests.
            timeout: The timeout for HTTP requests.
            ssl_verify: Whether to verify SSL certificates or a custom SSL context.

        Raises:
            ValueError: If the DataRobot endpoint or API token is not provided.
        """
        if datarobot_endpoint is None:
            datarobot_endpoint = os.environ.get("DATAROBOT_ENDPOINT")

        if not datarobot_endpoint:
            raise ValueError(
                "DATAROBOT_ENDPOINT must be set in the environment or passed as an argument."
            )

        if datarobot_api_token is None:
            datarobot_api_token = os.environ.get("DATAROBOT_API_TOKEN")

        if not datarobot_api_token:
            raise ValueError(
                "DATAROBOT_API_TOKEN must be set in the environment or passed as arguments."
            )

        # OAuth Providers Service API is not under /api/v2/
        self._datarobot_endpoint = datarobot_endpoint.rstrip("/api/v2")
        self._datarobot_api_token = datarobot_api_token

        self._oauth_provider_ids = list(oauth_provider_ids)

        if user_agent is None:
            agent_parts = [
                f"DataRobotOAuthProviderClient/{__version__}",
                f"({platform.system()} {platform.release()} {platform.machine()})",
                f"Python-{platform.python_version()}",
            ]

            user_agent = " ".join(agent_parts)

        if http_client is None:
            http_client = httpx.AsyncClient(
                timeout=timeout,
                follow_redirects=follow_redirects,
                verify=ssl_verify,
                headers={
                    "User-Agent": user_agent,
                    "Authorization": f"Bearer {self._datarobot_api_token}",
                },
            )

        self._http_client = http_client

    def register(self, oauth_provider_id: str) -> None:
        self._oauth_provider_ids.append(oauth_provider_id)

    async def __aenter__(self) -> "AsyncOAuth":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        await self._http_client.aclose()

    async def close(self) -> None:
        """
        Close the HTTP client connection.
        This is an alias for __aexit__ to maintain compatibility with the OAuthComponent interface.
        """
        await self._http_client.aclose()

    async def get_providers(
        self,
    ) -> list[OAuthProvider]:
        """
        Get the list of OAuth providers.

        Raises:
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        if not self._oauth_provider_ids:
            return []

        resp = await self._http_client.get(
            urljoin(self._datarobot_endpoint, "/externalOAuth/providers/"),
            params={
                "ids": self._oauth_provider_ids,
            },
        )

        if not resp.is_success:
            raise_http_exception(resp)

        providers_data = _DROAuthProviders(**resp.json()).data

        return [provider.to_data() for provider in providers_data]

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
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        resp = await self._http_client.post(
            urljoin(
                self._datarobot_endpoint,
                f"/externalOAuth/providers/{provider_id}/authorize/",
            ),
            params={
                "redirect_uri": redirect_uri,
                "state": state,
                # we are not supporting other params in the OAuth Providers Service API
            },
        )

        if resp.status_code == 404:
            raise OAuthServiceProviderNotFound(
                f"The OAuth provider was not found: {resp.text}",
                provider_id=provider_id,
            )

        if not resp.is_success:
            raise_http_exception(resp, provider_id=provider_id)

        raw_data = resp.json()
        redirect_data = _DROAuthRedirectData(**raw_data)

        return OAuthFlowSession(
            provider_id=provider_id,
            redirect_uri=redirect_uri,
            state=redirect_data.state,
            authorization_url=redirect_data.redirect_url,
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
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        params = dict(params)

        if error := params.get("error"):
            raise OAuthFlowError(
                provider_id=provider_id,
                error_code=error,
                message=params.get("error_description", "OAuth flow failed"),
            )

        resp = await self._http_client.post(
            urljoin(self._datarobot_endpoint, "/externalOAuth/providers/callback/"),
            json={
                "providerId": provider_id,
                "code": params.get("code"),
                "state": sess.state,
                # we are not supporting other params like code_verifier in the OAuth Providers Service API
            },
        )

        if resp.status_code == 404:
            raise OAuthServiceProviderNotFound(
                f"The OAuth provider was not found: {resp.text}",
                provider_id=provider_id,
            )

        if not resp.is_success:
            raise_http_exception(resp, provider_id=provider_id)

        raw_data = resp.json()

        oauth_data = _DROAuthData(**raw_data)
        authorization = oauth_data.authorized_provider

        return OAuthData(
            authorization_id=authorization.id,
            provider=authorization.provider.to_data(),
            user_profile=oauth_data.user_info.to_data(),
        )

    async def refresh_access_token(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        scope: str | None = None,
        refresh_token: str | None = None,
    ) -> OAuthToken:
        """
        Refresh the access token for the specified OAuth provider.

        Raises:
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """

        if identity_id is None:
            raise OAuthValidationErr(
                "Identity ID is required to obtain new access token via DataRobot API"
            )

        resp = await self._http_client.post(
            urljoin(
                self._datarobot_endpoint,
                f"/externalOAuth/authorizedProviders/{identity_id}/token/",
            ),
        )

        if resp.status_code == 404:
            raise OAuthAuthorizationNotFound(
                f"The authorization was not found: {resp.text}",
                provider_id=provider_id,
                authorization_id=identity_id,
            )

        if resp.status_code == 410:
            raise OAuthAuthorizationExpired(
                "The authorization has expired. Please re-authorize the provider.",
                provider_id=provider_id,
                authorization_id=identity_id,
            )

        if not resp.is_success:
            raise_http_exception(resp, provider_id=provider_id, authorization_id=identity_id)

        token_data = _DROAuthTokenData(**resp.json())

        return token_data.to_data()

    async def get_user_info(
        self,
        provider_id: str | None = None,
        identity_id: str | None = None,
        access_token: str | None = None,
    ) -> Profile:
        """
        Get user information from the OAuth provider.

        Raises:
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        if identity_id is None:
            raise OAuthValidationErr(
                "Identity ID is required to obtain new access token via DataRobot API"
            )

        resp = await self._http_client.get(
            urljoin(
                self._datarobot_endpoint,
                f"/externalOAuth/authorizedProviders/{identity_id}/userinfo/",
            ),
        )

        if resp.status_code == 404:
            raise OAuthAuthorizationNotFound(
                f"The authorization was not found: {resp.text}",
                provider_id=provider_id,
                authorization_id=identity_id,
            )

        if resp.status_code == 410:
            raise OAuthAuthorizationExpired(
                "The authorization has expired. Please re-authorize the provider.",
                provider_id=provider_id,
                authorization_id=identity_id,
            )

        if not resp.is_success:
            raise_http_exception(resp, provider_id=provider_id, authorization_id=identity_id)

        user_info = _DROAuthUserProfile(**resp.json())

        return user_info.to_data()


class SyncOAuth(SyncOAuthComponent):
    """
    Synchronous OAuth client for DataRobot OAuth Providers Service API.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the SyncOAuth client.

        Args:
            oauth_provider_ids: A sequence of OAuth provider IDs to register.
            datarobot_endpoint: The DataRobot API endpoint URL. If not provided,
                it will be read from the environment variable DATAROBOT_ENDPOINT.
            datarobot_api_token: The DataRobot API token. If not provided,
                it will be read from the environment variable DATAROBOT_API_TOKEN.
            http_client: An optional HTTP client to use for requests.
                If not provided, a new AsyncClient will be created.
            user_agent: An optional user agent string to use for requests.
            follow_redirects: Whether to follow redirects in HTTP requests.
            timeout: The timeout for HTTP requests.
            ssl_verify: Whether to verify SSL certificates or a custom SSL context.

        Raises:
            ValueError: If the DataRobot endpoint or API token is not provided.
        """
        self._async_client = AsyncOAuth(*args, **kwargs)

    def __enter__(self) -> "SyncOAuth":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """
        Close the HTTP client connection.
        This is an alias for __exit__ to maintain compatibility with the OAuthComponent interface.
        """
        syncify(self._async_client.close)()

    def get_providers(self) -> list[OAuthProvider]:
        return syncify(self._async_client.get_providers)()

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
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        return syncify(self._async_client.get_authorization_url)(
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
        **kwargs: Any,
    ) -> OAuthData:
        """
        Exchange the authorization code for an access token and user profile.

        Raises:
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        return syncify(self._async_client.exchange_code)(
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
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        return syncify(self._async_client.refresh_access_token)(
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
        Get user information from the OAuth provider.

        Raises:
            OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
            OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
            OAuthServiceClientErr: For client errors (4xx status codes).
            OAuthServiceUnavailable: For server errors (5xx status codes).
            OAuthServiceError: For any other errors.
        """
        return syncify(self._async_client.get_user_info)(
            provider_id=provider_id,
            identity_id=identity_id,
            access_token=access_token,
        )
