from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.detail_response import DetailResponse
from ...types import Response


def _get_kwargs(
    uuid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-provider-resources/{uuid}/sync_user_roles/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, DetailResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == 409:
        response_409 = DetailResponse.from_dict(response.json())

        return response_409
    if response.status_code == 429:
        response_429 = DetailResponse.from_dict(response.json())

        return response_429
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, DetailResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, DetailResponse]]:
    """Trigger user role sync for this resource. Sends a notification to RabbitMQ that this resource needs
    user role synchronization; agents without event subscriptions apply the change on their next polling
    cycle.

    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DetailResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    *,
    client: AuthenticatedClient,
) -> Union[Any, DetailResponse]:
    """Trigger user role sync for this resource. Sends a notification to RabbitMQ that this resource needs
    user role synchronization; agents without event subscriptions apply the change on their next polling
    cycle.

    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DetailResponse]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, DetailResponse]]:
    """Trigger user role sync for this resource. Sends a notification to RabbitMQ that this resource needs
    user role synchronization; agents without event subscriptions apply the change on their next polling
    cycle.

    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DetailResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    *,
    client: AuthenticatedClient,
) -> Union[Any, DetailResponse]:
    """Trigger user role sync for this resource. Sends a notification to RabbitMQ that this resource needs
    user role synchronization; agents without event subscriptions apply the change on their next polling
    cycle.

    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DetailResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
