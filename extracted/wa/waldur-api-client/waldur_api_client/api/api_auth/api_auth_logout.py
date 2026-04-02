from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.logout import Logout
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-auth/logout/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Union[Any, Logout]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = Logout.from_dict(response.json())

        return response_200
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Logout]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, Logout]]:
    """Log out

     Logs out the current user by deleting their authentication token. If single logout (SLO) is
    supported for the current authentication method (e.g., SAML2 or OIDC), this endpoint may return a
    logout URL to which the user should be redirected to complete the logout process on the identity
    provider side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Logout]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Union[Any, Logout]:
    """Log out

     Logs out the current user by deleting their authentication token. If single logout (SLO) is
    supported for the current authentication method (e.g., SAML2 or OIDC), this endpoint may return a
    logout URL to which the user should be redirected to complete the logout process on the identity
    provider side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Logout]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, Logout]]:
    """Log out

     Logs out the current user by deleting their authentication token. If single logout (SLO) is
    supported for the current authentication method (e.g., SAML2 or OIDC), this endpoint may return a
    logout URL to which the user should be redirected to complete the logout process on the identity
    provider side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Logout]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Union[Any, Logout]:
    """Log out

     Logs out the current user by deleting their authentication token. If single logout (SLO) is
    supported for the current authentication method (e.g., SAML2 or OIDC), this endpoint may return a
    logout URL to which the user should be redirected to complete the logout process on the identity
    provider side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Logout]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
