from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.load_balancer_async_operation_response import LoadBalancerAsyncOperationResponse
from ...models.load_balancer_set_security_groups_request import LoadBalancerSetSecurityGroupsRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: LoadBalancerSetSecurityGroupsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/openstack-loadbalancers/{uuid}/set_security_groups/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> LoadBalancerAsyncOperationResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 202:
        response_202 = LoadBalancerAsyncOperationResponse.from_dict(response.json())

        return response_202
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[LoadBalancerAsyncOperationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LoadBalancerSetSecurityGroupsRequest,
) -> Response[LoadBalancerAsyncOperationResponse]:
    """Set security groups on VIP port

     Set security groups on the load balancer VIP port to control access.

    Args:
        uuid (UUID):
        body (LoadBalancerSetSecurityGroupsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadBalancerAsyncOperationResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LoadBalancerSetSecurityGroupsRequest,
) -> LoadBalancerAsyncOperationResponse:
    """Set security groups on VIP port

     Set security groups on the load balancer VIP port to control access.

    Args:
        uuid (UUID):
        body (LoadBalancerSetSecurityGroupsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadBalancerAsyncOperationResponse
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LoadBalancerSetSecurityGroupsRequest,
) -> Response[LoadBalancerAsyncOperationResponse]:
    """Set security groups on VIP port

     Set security groups on the load balancer VIP port to control access.

    Args:
        uuid (UUID):
        body (LoadBalancerSetSecurityGroupsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadBalancerAsyncOperationResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LoadBalancerSetSecurityGroupsRequest,
) -> LoadBalancerAsyncOperationResponse:
    """Set security groups on VIP port

     Set security groups on the load balancer VIP port to control access.

    Args:
        uuid (UUID):
        body (LoadBalancerSetSecurityGroupsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadBalancerAsyncOperationResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
