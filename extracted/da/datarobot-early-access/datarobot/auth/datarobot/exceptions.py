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

import httpx

from datarobot.auth.exceptions import OAuthProviderNotFound


class OAuthServiceError(Exception):
    """
    The DR OAuth Providers Service request has failed
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message)

        self.provider_id = provider_id
        self.authorization_id = authorization_id
        self.status_code = status_code


class OAuthServiceClientErr(OAuthServiceError):
    """
    The OAuth Providers Service request has failed due to a client error
    """

    def __init__(
        self,
        message: str,
        status_code: int = 422,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message, status_code, provider_id, authorization_id)


class OAuthServiceNotAuthenticated(OAuthServiceClientErr):
    """
    The OAuth Providers Service request has failed due to not being properly authenticated
    """

    def __init__(
        self,
        message: str,
        status_code: int = 401,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message, status_code, provider_id, authorization_id)


class OAuthServiceProviderNotFound(OAuthProviderNotFound, OAuthServiceClientErr):
    """
    The OAuth Providers Service doesn't recognize the provider ID.
    The provider could be accidentally deleted, never existed, or you don't have access to it.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 404,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message, status_code, provider_id, authorization_id)


class OAuthAuthorizationNotFound(OAuthServiceClientErr):
    """
    The OAuth Providers Service could not find the authorization with the given ID.
    This can happen if the authorization was deleted by DataRobot User (there is a way to do that via DataRobot UI),
    never existed, or you don't have access to it.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 404,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message, status_code, provider_id, authorization_id)


class OAuthAuthorizationExpired(OAuthServiceClientErr):
    """
    The OAuth Providers Service request has failed due to the authorization being expired.
    This can happen if
     - OAuth provider limits the lifetime of the refresh token
     - The user has revoked the authorization from this provider's account ahead of time
    """

    def __init__(
        self,
        message: str,
        status_code: int = 410,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message, status_code, provider_id, authorization_id)


class OAuthProviderUnavailable(OAuthServiceError):
    """
    The OAuth Providers Service request has failed due to the provider being unavailable
    """

    def __init__(
        self,
        message: str,
        status_code: int = 502,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message, status_code, provider_id, authorization_id)


class OAuthServiceUnavailable(OAuthServiceError):
    """
    The OAuth Providers Service request has failed due to the service being unavailable
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        provider_id: str | None = None,
        authorization_id: str | None = None,
    ) -> None:
        super().__init__(message, status_code, provider_id, authorization_id)


def raise_http_exception(
    resp: httpx.Response,
    provider_id: str | None = None,
    authorization_id: str | None = None,
) -> None:
    """
    Raise an exception based on the response status code.
    This is a placeholder function to handle errors in a more structured way.

    Args:
        resp (httpx.Response): The HTTP response object.
        provider_id (str | None): The ID of the OAuth provider, if applicable.
        authorization_id (str | None): The ID of the authorization, if applicable.

    Raises:
        OAuthServiceNotAuthenticated: If DataRobot credentials are revoked, corrupted or invalid in other way.
        OAuthProviderUnavailable: If the external OAuth provider is currently unavailable.
        OAuthServiceClientErr: For client errors (4xx status codes).
        OAuthServiceUnavailable: For server errors (5xx status codes).
        OAuthServiceError: For any other errors.
    """
    code = resp.status_code

    if code == 401:
        raise OAuthServiceNotAuthenticated(
            "Unauthorized access. Please check your DataRobot credentials.",
            provider_id=provider_id,
            authorization_id=authorization_id,
        )
    elif code == 502:
        raise OAuthProviderUnavailable(
            f"External OAuth provider is currently unavailable: {resp.text}",
            code,
            provider_id=provider_id,
            authorization_id=authorization_id,
        )
    elif 400 <= code < 500:
        raise OAuthServiceClientErr(
            f"Client error occurred: {resp.text}",
            code,
            provider_id=provider_id,
            authorization_id=authorization_id,
        )
    elif code >= 500:
        raise OAuthServiceUnavailable(
            f"The OAuth Providers Service or external OAuth provider is currently unavailable: {resp.text}",
            code,
            provider_id=provider_id,
            authorization_id=authorization_id,
        )
    else:
        raise OAuthServiceError(
            f"An error occurred while communicating with the OAuth provider: {resp.text}",
            code,
            provider_id=provider_id,
            authorization_id=authorization_id,
        )
