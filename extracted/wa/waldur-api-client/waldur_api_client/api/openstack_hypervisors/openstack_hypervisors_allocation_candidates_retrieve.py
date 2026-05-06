from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.allocation_candidates_response import AllocationCandidatesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = UNSET,
    required: Union[Unset, str] = UNSET,
    resources: str,
    settings_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["required"] = required

    params["resources"] = resources

    json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openstack-hypervisors/allocation_candidates/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> AllocationCandidatesResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AllocationCandidatesResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AllocationCandidatesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    required: Union[Unset, str] = UNSET,
    resources: str,
    settings_uuid: UUID,
) -> Response[AllocationCandidatesResponse]:
    """Pre-flight allocation candidates

     Ask Placement which compute hosts could currently satisfy a request for the given resources (and
    required traits). Useful as a pre-flight check before placing an order on a fully-booked cloud.
    Returns 0 candidates when nothing fits, with the same provider_summaries Placement returns for
    diagnostic display.

    Args:
        limit (Union[Unset, int]):
        required (Union[Unset, str]):
        resources (str):
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AllocationCandidatesResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        required=required,
        resources=resources,
        settings_uuid=settings_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    required: Union[Unset, str] = UNSET,
    resources: str,
    settings_uuid: UUID,
) -> AllocationCandidatesResponse:
    """Pre-flight allocation candidates

     Ask Placement which compute hosts could currently satisfy a request for the given resources (and
    required traits). Useful as a pre-flight check before placing an order on a fully-booked cloud.
    Returns 0 candidates when nothing fits, with the same provider_summaries Placement returns for
    diagnostic display.

    Args:
        limit (Union[Unset, int]):
        required (Union[Unset, str]):
        resources (str):
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AllocationCandidatesResponse
    """

    return sync_detailed(
        client=client,
        limit=limit,
        required=required,
        resources=resources,
        settings_uuid=settings_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    required: Union[Unset, str] = UNSET,
    resources: str,
    settings_uuid: UUID,
) -> Response[AllocationCandidatesResponse]:
    """Pre-flight allocation candidates

     Ask Placement which compute hosts could currently satisfy a request for the given resources (and
    required traits). Useful as a pre-flight check before placing an order on a fully-booked cloud.
    Returns 0 candidates when nothing fits, with the same provider_summaries Placement returns for
    diagnostic display.

    Args:
        limit (Union[Unset, int]):
        required (Union[Unset, str]):
        resources (str):
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AllocationCandidatesResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        required=required,
        resources=resources,
        settings_uuid=settings_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    required: Union[Unset, str] = UNSET,
    resources: str,
    settings_uuid: UUID,
) -> AllocationCandidatesResponse:
    """Pre-flight allocation candidates

     Ask Placement which compute hosts could currently satisfy a request for the given resources (and
    required traits). Useful as a pre-flight check before placing an order on a fully-booked cloud.
    Returns 0 candidates when nothing fits, with the same provider_summaries Placement returns for
    diagnostic display.

    Args:
        limit (Union[Unset, int]):
        required (Union[Unset, str]):
        resources (str):
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AllocationCandidatesResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            required=required,
            resources=resources,
            settings_uuid=settings_uuid,
        )
    ).parsed
