from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.service_provider_account import ServiceProviderAccount
from ...models.service_provider_account_field_enum import ServiceProviderAccountFieldEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-service-provider-accounts/{uuid}/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ServiceProviderAccount:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ServiceProviderAccount.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ServiceProviderAccount]:
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
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
) -> Response[ServiceProviderAccount]:
    """Retrieve a service provider account

     Returns one provider account, including its POSIX identity and the number of offering accounts
    reading through it.

    Args:
        uuid (UUID):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProviderAccount]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
) -> ServiceProviderAccount:
    """Retrieve a service provider account

     Returns one provider account, including its POSIX identity and the number of offering accounts
    reading through it.

    Args:
        uuid (UUID):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProviderAccount
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        field=field,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
) -> Response[ServiceProviderAccount]:
    """Retrieve a service provider account

     Returns one provider account, including its POSIX identity and the number of offering accounts
    reading through it.

    Args:
        uuid (UUID):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProviderAccount]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
) -> ServiceProviderAccount:
    """Retrieve a service provider account

     Returns one provider account, including its POSIX identity and the number of offering accounts
    reading through it.

    Args:
        uuid (UUID):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProviderAccount
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            field=field,
        )
    ).parsed
