from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, str] = UNSET,
    end: Union[Unset, str] = UNSET,
    provider_uuid: Union[Unset, str] = UNSET,
    start: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["customer_uuid"] = customer_uuid

    params["end"] = end

    params["provider_uuid"] = provider_uuid

    params["start"] = start

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-stats/order_stats/",
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
    customer_uuid: Union[Unset, str] = UNSET,
    end: Union[Unset, str] = UNSET,
    provider_uuid: Union[Unset, str] = UNSET,
    start: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, str]):
        end (Union[Unset, str]):
        provider_uuid (Union[Unset, str]):
        start (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        end=end,
        provider_uuid=provider_uuid,
        start=start,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, str] = UNSET,
    end: Union[Unset, str] = UNSET,
    provider_uuid: Union[Unset, str] = UNSET,
    start: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, str]):
        end (Union[Unset, str]):
        provider_uuid (Union[Unset, str]):
        start (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        end=end,
        provider_uuid=provider_uuid,
        start=start,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, str] = UNSET,
    end: Union[Unset, str] = UNSET,
    provider_uuid: Union[Unset, str] = UNSET,
    start: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, str]):
        end (Union[Unset, str]):
        provider_uuid (Union[Unset, str]):
        start (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        end=end,
        provider_uuid=provider_uuid,
        start=start,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, str] = UNSET,
    end: Union[Unset, str] = UNSET,
    provider_uuid: Union[Unset, str] = UNSET,
    start: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, str]):
        end (Union[Unset, str]):
        provider_uuid (Union[Unset, str]):
        start (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            end=end,
            provider_uuid=provider_uuid,
            start=start,
        )
    ).parsed
