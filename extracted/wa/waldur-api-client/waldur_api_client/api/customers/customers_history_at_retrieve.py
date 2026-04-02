from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.customers_history_at_retrieve_response_400 import CustomersHistoryAtRetrieveResponse400
from ...models.customers_history_at_retrieve_response_404 import CustomersHistoryAtRetrieveResponse404
from ...models.version_history import VersionHistory
from ...types import UNSET, Response


def _get_kwargs(
    uuid: UUID,
    *,
    timestamp: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["timestamp"] = timestamp

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/customers/{uuid}/history/at/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = VersionHistory.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = CustomersHistoryAtRetrieveResponse400.from_dict(response.json())

        return response_400
    if response.status_code == 404:
        response_404 = CustomersHistoryAtRetrieveResponse404.from_dict(response.json())

        return response_404
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]]:
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
    timestamp: str,
) -> Response[Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]]:
    """Get object state at a specific timestamp

     Returns the state of the object as it was at the specified timestamp. Only accessible by staff and
    support users.

    Args:
        uuid (UUID):
        timestamp (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        timestamp=timestamp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    timestamp: str,
) -> Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]:
    """Get object state at a specific timestamp

     Returns the state of the object as it was at the specified timestamp. Only accessible by staff and
    support users.

    Args:
        uuid (UUID):
        timestamp (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        timestamp=timestamp,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    timestamp: str,
) -> Response[Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]]:
    """Get object state at a specific timestamp

     Returns the state of the object as it was at the specified timestamp. Only accessible by staff and
    support users.

    Args:
        uuid (UUID):
        timestamp (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        timestamp=timestamp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    timestamp: str,
) -> Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]:
    """Get object state at a specific timestamp

     Returns the state of the object as it was at the specified timestamp. Only accessible by staff and
    support users.

    Args:
        uuid (UUID):
        timestamp (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CustomersHistoryAtRetrieveResponse400, CustomersHistoryAtRetrieveResponse404, VersionHistory]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            timestamp=timestamp,
        )
    ).parsed
