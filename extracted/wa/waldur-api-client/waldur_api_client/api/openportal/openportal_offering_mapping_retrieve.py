from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_mapping_map import OfferingMappingMap
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    identifier: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_identifier: Union[Unset, list[str]] = UNSET
    if not isinstance(identifier, Unset):
        json_identifier = identifier

    params["identifier"] = json_identifier

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openportal/offering_mapping/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OfferingMappingMap:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OfferingMappingMap.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OfferingMappingMap]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, list[str]] = UNSET,
) -> Response[OfferingMappingMap]:
    """Map OpenPortal destination strings to Waldur Offering objects. Pass each destination as a repeated
    'identifier' query parameter. Returns a dict keyed by identifier; unknown destinations map to null.
    Accessible to all authenticated users.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingMappingMap]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, list[str]] = UNSET,
) -> OfferingMappingMap:
    """Map OpenPortal destination strings to Waldur Offering objects. Pass each destination as a repeated
    'identifier' query parameter. Returns a dict keyed by identifier; unknown destinations map to null.
    Accessible to all authenticated users.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingMappingMap
    """

    return sync_detailed(
        client=client,
        identifier=identifier,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, list[str]] = UNSET,
) -> Response[OfferingMappingMap]:
    """Map OpenPortal destination strings to Waldur Offering objects. Pass each destination as a repeated
    'identifier' query parameter. Returns a dict keyed by identifier; unknown destinations map to null.
    Accessible to all authenticated users.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingMappingMap]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, list[str]] = UNSET,
) -> OfferingMappingMap:
    """Map OpenPortal destination strings to Waldur Offering objects. Pass each destination as a repeated
    'identifier' query parameter. Returns a dict keyed by identifier; unknown destinations map to null.
    Accessible to all authenticated users.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingMappingMap
    """

    return (
        await asyncio_detailed(
            client=client,
            identifier=identifier,
        )
    ).parsed
