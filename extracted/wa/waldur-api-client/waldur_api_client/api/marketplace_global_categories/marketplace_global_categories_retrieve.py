from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_global_categories_retrieve_response_200 import MarketplaceGlobalCategoriesRetrieveResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-global-categories/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MarketplaceGlobalCategoriesRetrieveResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MarketplaceGlobalCategoriesRetrieveResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MarketplaceGlobalCategoriesRetrieveResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> Response[MarketplaceGlobalCategoriesRetrieveResponse200]:
    """Get resource counts by category


            Returns a dictionary mapping marketplace category UUIDs to the count of active (non-
    terminated)
            resources the current user has access to within that category. This is primarily used for UI
            dashboards or sidebars to display the number of resources in each category filter.

            The counts can be further filtered by providing a `project_uuid` or `customer_uuid`.


    Args:
        customer_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceGlobalCategoriesRetrieveResponse200]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        project_uuid=project_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> MarketplaceGlobalCategoriesRetrieveResponse200:
    """Get resource counts by category


            Returns a dictionary mapping marketplace category UUIDs to the count of active (non-
    terminated)
            resources the current user has access to within that category. This is primarily used for UI
            dashboards or sidebars to display the number of resources in each category filter.

            The counts can be further filtered by providing a `project_uuid` or `customer_uuid`.


    Args:
        customer_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceGlobalCategoriesRetrieveResponse200
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        project_uuid=project_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> Response[MarketplaceGlobalCategoriesRetrieveResponse200]:
    """Get resource counts by category


            Returns a dictionary mapping marketplace category UUIDs to the count of active (non-
    terminated)
            resources the current user has access to within that category. This is primarily used for UI
            dashboards or sidebars to display the number of resources in each category filter.

            The counts can be further filtered by providing a `project_uuid` or `customer_uuid`.


    Args:
        customer_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceGlobalCategoriesRetrieveResponse200]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        project_uuid=project_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> MarketplaceGlobalCategoriesRetrieveResponse200:
    """Get resource counts by category


            Returns a dictionary mapping marketplace category UUIDs to the count of active (non-
    terminated)
            resources the current user has access to within that category. This is primarily used for UI
            dashboards or sidebars to display the number of resources in each category filter.

            The counts can be further filtered by providing a `project_uuid` or `customer_uuid`.


    Args:
        customer_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceGlobalCategoriesRetrieveResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            project_uuid=project_uuid,
        )
    ).parsed
