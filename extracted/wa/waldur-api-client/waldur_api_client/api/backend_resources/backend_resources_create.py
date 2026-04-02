from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource import BackendResource
from ...models.backend_resource_request import BackendResourceRequest
from ...types import Response


def _get_kwargs(
    *,
    body: BackendResourceRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/backend-resources/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> BackendResource:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = BackendResource.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[BackendResource]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BackendResourceRequest,
) -> Response[BackendResource]:
    """Create a backend resource

     Creates a new backend resource record. This is typically done by a site agent to report a resource
    that is available for import into the marketplace.

    Args:
        body (BackendResourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendResource]
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
    body: BackendResourceRequest,
) -> BackendResource:
    """Create a backend resource

     Creates a new backend resource record. This is typically done by a site agent to report a resource
    that is available for import into the marketplace.

    Args:
        body (BackendResourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendResource
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BackendResourceRequest,
) -> Response[BackendResource]:
    """Create a backend resource

     Creates a new backend resource record. This is typically done by a site agent to report a resource
    that is available for import into the marketplace.

    Args:
        body (BackendResourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendResource]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BackendResourceRequest,
) -> BackendResource:
    """Create a backend resource

     Creates a new backend resource record. This is typically done by a site agent to report a resource
    that is available for import into the marketplace.

    Args:
        body (BackendResourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendResource
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
