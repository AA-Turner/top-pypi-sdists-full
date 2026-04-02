from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.external_link import ExternalLink
from ...models.external_link_request import ExternalLinkRequest
from ...models.external_link_request_form import ExternalLinkRequestForm
from ...models.external_link_request_multipart import ExternalLinkRequestMultipart
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        ExternalLinkRequest,
        ExternalLinkRequestForm,
        ExternalLinkRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/external-links/",
    }

    if isinstance(body, ExternalLinkRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ExternalLinkRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, ExternalLinkRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ExternalLink:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = ExternalLink.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ExternalLink]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        ExternalLinkRequest,
        ExternalLinkRequestForm,
        ExternalLinkRequestMultipart,
    ],
) -> Response[ExternalLink]:
    """Create an external link

     Create a new external link. This action is restricted to staff users.

    Args:
        body (ExternalLinkRequest):
        body (ExternalLinkRequestForm):
        body (ExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalLink]
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
    client: AuthenticatedClient,
    body: Union[
        ExternalLinkRequest,
        ExternalLinkRequestForm,
        ExternalLinkRequestMultipart,
    ],
) -> ExternalLink:
    """Create an external link

     Create a new external link. This action is restricted to staff users.

    Args:
        body (ExternalLinkRequest):
        body (ExternalLinkRequestForm):
        body (ExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalLink
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        ExternalLinkRequest,
        ExternalLinkRequestForm,
        ExternalLinkRequestMultipart,
    ],
) -> Response[ExternalLink]:
    """Create an external link

     Create a new external link. This action is restricted to staff users.

    Args:
        body (ExternalLinkRequest):
        body (ExternalLinkRequestForm):
        body (ExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalLink]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        ExternalLinkRequest,
        ExternalLinkRequestForm,
        ExternalLinkRequestMultipart,
    ],
) -> ExternalLink:
    """Create an external link

     Create a new external link. This action is restricted to staff users.

    Args:
        body (ExternalLinkRequest):
        body (ExternalLinkRequestForm):
        body (ExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalLink
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
