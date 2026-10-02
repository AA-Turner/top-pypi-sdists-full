from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_mapping_map import ProjectMappingMap
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
        "url": "/api/openportal/project_mapping/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ProjectMappingMap:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProjectMappingMap.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProjectMappingMap]:
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
) -> Response[ProjectMappingMap]:
    """Map OpenPortal ProjectIdentifier strings to Waldur Project objects. Pass each identifier as a
    repeated 'identifier' query parameter. Returns a dict keyed by identifier; unknown identifiers map
    to null. Staff and support see all projects; regular users see only projects they are a member of.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectMappingMap]
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
) -> ProjectMappingMap:
    """Map OpenPortal ProjectIdentifier strings to Waldur Project objects. Pass each identifier as a
    repeated 'identifier' query parameter. Returns a dict keyed by identifier; unknown identifiers map
    to null. Staff and support see all projects; regular users see only projects they are a member of.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectMappingMap
    """

    return sync_detailed(
        client=client,
        identifier=identifier,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, list[str]] = UNSET,
) -> Response[ProjectMappingMap]:
    """Map OpenPortal ProjectIdentifier strings to Waldur Project objects. Pass each identifier as a
    repeated 'identifier' query parameter. Returns a dict keyed by identifier; unknown identifiers map
    to null. Staff and support see all projects; regular users see only projects they are a member of.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectMappingMap]
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
) -> ProjectMappingMap:
    """Map OpenPortal ProjectIdentifier strings to Waldur Project objects. Pass each identifier as a
    repeated 'identifier' query parameter. Returns a dict keyed by identifier; unknown identifiers map
    to null. Staff and support see all projects; regular users see only projects they are a member of.

    Args:
        identifier (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectMappingMap
    """

    return (
        await asyncio_detailed(
            client=client,
            identifier=identifier,
        )
    ).parsed
