from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_load_balancer import CreateLoadBalancer
from ...models.create_load_balancer_request import CreateLoadBalancerRequest
from ...types import Response


def _get_kwargs(
    *,
    body: CreateLoadBalancerRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/openstack-loadbalancers/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CreateLoadBalancer:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = CreateLoadBalancer.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CreateLoadBalancer]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateLoadBalancerRequest,
) -> Response[CreateLoadBalancer]:
    """Create load balancer

     Create a new load balancer.

    Args:
        body (CreateLoadBalancerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateLoadBalancer]
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
    body: CreateLoadBalancerRequest,
) -> CreateLoadBalancer:
    """Create load balancer

     Create a new load balancer.

    Args:
        body (CreateLoadBalancerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateLoadBalancer
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateLoadBalancerRequest,
) -> Response[CreateLoadBalancer]:
    """Create load balancer

     Create a new load balancer.

    Args:
        body (CreateLoadBalancerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateLoadBalancer]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateLoadBalancerRequest,
) -> CreateLoadBalancer:
    """Create load balancer

     Create a new load balancer.

    Args:
        body (CreateLoadBalancerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateLoadBalancer
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
