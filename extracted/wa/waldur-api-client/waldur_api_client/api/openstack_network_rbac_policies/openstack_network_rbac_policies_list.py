from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.network_rbac_policy import NetworkRBACPolicy
from ...models.policy_type_enum import PolicyTypeEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["network"] = network

    json_network_uuid: Union[Unset, str] = UNSET
    if not isinstance(network_uuid, Unset):
        json_network_uuid = str(network_uuid)
    params["network_uuid"] = json_network_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_policy_type: Union[Unset, str] = UNSET
    if not isinstance(policy_type, Unset):
        json_policy_type = policy_type.value

    params["policy_type"] = json_policy_type

    params["target_tenant"] = target_tenant

    json_target_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(target_tenant_uuid, Unset):
        json_target_tenant_uuid = str(target_tenant_uuid)
    params["target_tenant_uuid"] = json_target_tenant_uuid

    params["tenant"] = tenant

    json_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(tenant_uuid, Unset):
        json_tenant_uuid = str(tenant_uuid)
    params["tenant_uuid"] = json_tenant_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openstack-network-rbac-policies/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["NetworkRBACPolicy"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = NetworkRBACPolicy.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["NetworkRBACPolicy"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["NetworkRBACPolicy"]]:
    """List network RBAC policies

     Get a list of network RBAC policies.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['NetworkRBACPolicy']]
    """

    kwargs = _get_kwargs(
        network=network,
        network_uuid=network_uuid,
        page=page,
        page_size=page_size,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["NetworkRBACPolicy"]:
    """List network RBAC policies

     Get a list of network RBAC policies.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NetworkRBACPolicy']
    """

    return sync_detailed(
        client=client,
        network=network,
        network_uuid=network_uuid,
        page=page,
        page_size=page_size,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["NetworkRBACPolicy"]]:
    """List network RBAC policies

     Get a list of network RBAC policies.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['NetworkRBACPolicy']]
    """

    kwargs = _get_kwargs(
        network=network,
        network_uuid=network_uuid,
        page=page,
        page_size=page_size,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["NetworkRBACPolicy"]:
    """List network RBAC policies

     Get a list of network RBAC policies.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NetworkRBACPolicy']
    """

    return (
        await asyncio_detailed(
            client=client,
            network=network,
            network_uuid=network_uuid,
            page=page,
            page_size=page_size,
            policy_type=policy_type,
            target_tenant=target_tenant,
            target_tenant_uuid=target_tenant_uuid,
            tenant=tenant,
            tenant_uuid=tenant_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["NetworkRBACPolicy"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NetworkRBACPolicy']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[NetworkRBACPolicy] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        network=network,
        network_uuid=network_uuid,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["NetworkRBACPolicy"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['NetworkRBACPolicy']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[NetworkRBACPolicy] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        network=network,
        network_uuid=network_uuid,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
