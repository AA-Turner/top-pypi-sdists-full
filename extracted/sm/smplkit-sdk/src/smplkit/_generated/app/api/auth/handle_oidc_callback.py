from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.oidc_provider import OidcProvider
from ...types import Unset


def _get_kwargs(
    provider: OidcProvider,
    *,
    code: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    error: None | str | Unset = UNSET,
    error_description: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_code: None | str | Unset
    if isinstance(code, Unset):
        json_code = UNSET
    else:
        json_code = code
    params["code"] = json_code

    json_state: None | str | Unset
    if isinstance(state, Unset):
        json_state = UNSET
    else:
        json_state = state
    params["state"] = json_state

    json_error: None | str | Unset
    if isinstance(error, Unset):
        json_error = UNSET
    else:
        json_error = error
    params["error"] = json_error

    json_error_description: None | str | Unset
    if isinstance(error_description, Unset):
        json_error_description = UNSET
    else:
        json_error_description = error_description
    params["error_description"] = json_error_description

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/auth/callback/{provider}".format(
            provider=quote(str(provider), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 302:
        response_302 = cast(Any, None)
        return response_302

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: OidcProvider,
    *,
    client: AuthenticatedClient | Client,
    code: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    error: None | str | Unset = UNSET,
    error_description: None | str | Unset = UNSET,
) -> Response[Any | ErrorResponse]:
    """Handle OIDC Callback

     Handles the callback from the OIDC provider, exchanges the authorization code for tokens, and
    redirects to the frontend.

    Args:
        provider (OidcProvider):
        code (None | str | Unset):
        state (None | str | Unset):
        error (None | str | Unset):
        error_description (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        provider=provider,
        code=code,
        state=state,
        error=error,
        error_description=error_description,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    provider: OidcProvider,
    *,
    client: AuthenticatedClient | Client,
    code: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    error: None | str | Unset = UNSET,
    error_description: None | str | Unset = UNSET,
) -> Any | ErrorResponse | None:
    """Handle OIDC Callback

     Handles the callback from the OIDC provider, exchanges the authorization code for tokens, and
    redirects to the frontend.

    Args:
        provider (OidcProvider):
        code (None | str | Unset):
        state (None | str | Unset):
        error (None | str | Unset):
        error_description (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return sync_detailed(
        provider=provider,
        client=client,
        code=code,
        state=state,
        error=error,
        error_description=error_description,
    ).parsed


async def asyncio_detailed(
    provider: OidcProvider,
    *,
    client: AuthenticatedClient | Client,
    code: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    error: None | str | Unset = UNSET,
    error_description: None | str | Unset = UNSET,
) -> Response[Any | ErrorResponse]:
    """Handle OIDC Callback

     Handles the callback from the OIDC provider, exchanges the authorization code for tokens, and
    redirects to the frontend.

    Args:
        provider (OidcProvider):
        code (None | str | Unset):
        state (None | str | Unset):
        error (None | str | Unset):
        error_description (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        provider=provider,
        code=code,
        state=state,
        error=error,
        error_description=error_description,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    provider: OidcProvider,
    *,
    client: AuthenticatedClient | Client,
    code: None | str | Unset = UNSET,
    state: None | str | Unset = UNSET,
    error: None | str | Unset = UNSET,
    error_description: None | str | Unset = UNSET,
) -> Any | ErrorResponse | None:
    """Handle OIDC Callback

     Handles the callback from the OIDC provider, exchanges the authorization code for tokens, and
    redirects to the frontend.

    Args:
        provider (OidcProvider):
        code (None | str | Unset):
        state (None | str | Unset):
        error (None | str | Unset):
        error_description (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            provider=provider,
            client=client,
            code=code,
            state=state,
            error=error,
            error_description=error_description,
        )
    ).parsed
