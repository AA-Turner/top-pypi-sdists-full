from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource_req import BackendResourceReq
from ...models.backend_resource_req_request import BackendResourceReqRequest
from ...types import Response


def _get_kwargs(
    *,
    body: BackendResourceReqRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/backend-resource-requests/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> BackendResourceReq:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = BackendResourceReq.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[BackendResourceReq]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BackendResourceReqRequest,
) -> Response[BackendResourceReq]:
    """Create a backend resource request

     Creates a new request to fetch a list of importable resources from a backend. This is typically used
    by staff to trigger a site agent to report available resources.

    Args:
        body (BackendResourceReqRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendResourceReq]
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
    body: BackendResourceReqRequest,
) -> BackendResourceReq:
    """Create a backend resource request

     Creates a new request to fetch a list of importable resources from a backend. This is typically used
    by staff to trigger a site agent to report available resources.

    Args:
        body (BackendResourceReqRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendResourceReq
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BackendResourceReqRequest,
) -> Response[BackendResourceReq]:
    """Create a backend resource request

     Creates a new request to fetch a list of importable resources from a backend. This is typically used
    by staff to trigger a site agent to report available resources.

    Args:
        body (BackendResourceReqRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendResourceReq]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BackendResourceReqRequest,
) -> BackendResourceReq:
    """Create a backend resource request

     Creates a new request to fetch a list of importable resources from a backend. This is typically used
    by staff to trigger a site agent to report available resources.

    Args:
        body (BackendResourceReqRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendResourceReq
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
