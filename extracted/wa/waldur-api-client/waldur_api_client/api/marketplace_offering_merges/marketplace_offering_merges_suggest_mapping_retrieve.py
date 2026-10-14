from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_merge_suggested_mapping import OfferingMergeSuggestedMapping
from ...types import UNSET, Response


def _get_kwargs(
    *,
    sources: str,
    target: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["sources"] = sources

    json_target = str(target)
    params["target"] = json_target

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-offering-merges/suggest_mapping/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> OfferingMergeSuggestedMapping:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OfferingMergeSuggestedMapping.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OfferingMergeSuggestedMapping]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    sources: str,
    target: UUID,
) -> Response[OfferingMergeSuggestedMapping]:
    """Suggest plan mappings by name and component mappings by type.

    Args:
        sources (str):
        target (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingMergeSuggestedMapping]
    """

    kwargs = _get_kwargs(
        sources=sources,
        target=target,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    sources: str,
    target: UUID,
) -> OfferingMergeSuggestedMapping:
    """Suggest plan mappings by name and component mappings by type.

    Args:
        sources (str):
        target (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingMergeSuggestedMapping
    """

    return sync_detailed(
        client=client,
        sources=sources,
        target=target,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    sources: str,
    target: UUID,
) -> Response[OfferingMergeSuggestedMapping]:
    """Suggest plan mappings by name and component mappings by type.

    Args:
        sources (str):
        target (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingMergeSuggestedMapping]
    """

    kwargs = _get_kwargs(
        sources=sources,
        target=target,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    sources: str,
    target: UUID,
) -> OfferingMergeSuggestedMapping:
    """Suggest plan mappings by name and component mappings by type.

    Args:
        sources (str):
        target (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingMergeSuggestedMapping
    """

    return (
        await asyncio_detailed(
            client=client,
            sources=sources,
            target=target,
        )
    ).parsed
