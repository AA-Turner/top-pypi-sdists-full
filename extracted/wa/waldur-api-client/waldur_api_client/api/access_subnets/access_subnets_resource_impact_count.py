from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_access_subnet_uuid: Union[Unset, str] = UNSET
    if not isinstance(access_subnet_uuid, Unset):
        json_access_subnet_uuid = str(access_subnet_uuid)
    params["access_subnet_uuid"] = json_access_subnet_uuid

    json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/access-subnets/resource_impact/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> Response[int]:
    """Show which resources the access subnets reach

     Get number of items in the collection matching the request parameters.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        access_subnet_uuid=access_subnet_uuid,
        customer_uuid=customer_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> int:
    """Show which resources the access subnets reach

     Get number of items in the collection matching the request parameters.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        access_subnet_uuid=access_subnet_uuid,
        customer_uuid=customer_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> Response[int]:
    """Show which resources the access subnets reach

     Get number of items in the collection matching the request parameters.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        access_subnet_uuid=access_subnet_uuid,
        customer_uuid=customer_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> int:
    """Show which resources the access subnets reach

     Get number of items in the collection matching the request parameters.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            access_subnet_uuid=access_subnet_uuid,
            customer_uuid=customer_uuid,
        )
    ).parsed
