from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.saml_2_logout_complete import Saml2LogoutComplete
from ...models.saml_2_logout_complete_request import Saml2LogoutCompleteRequest
from ...types import Response


def _get_kwargs(
    *,
    body: Saml2LogoutCompleteRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-auth/saml2/logout/complete/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Saml2LogoutComplete:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = Saml2LogoutComplete.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Saml2LogoutComplete]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Saml2LogoutCompleteRequest,
) -> Response[Saml2LogoutComplete]:
    """For IdPs which send POST requests

    Args:
        body (Saml2LogoutCompleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Saml2LogoutComplete]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Saml2LogoutCompleteRequest,
) -> Saml2LogoutComplete:
    """For IdPs which send POST requests

    Args:
        body (Saml2LogoutCompleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Saml2LogoutComplete
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Saml2LogoutCompleteRequest,
) -> Response[Saml2LogoutComplete]:
    """For IdPs which send POST requests

    Args:
        body (Saml2LogoutCompleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Saml2LogoutComplete]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Saml2LogoutCompleteRequest,
) -> Saml2LogoutComplete:
    """For IdPs which send POST requests

    Args:
        body (Saml2LogoutCompleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Saml2LogoutComplete
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
