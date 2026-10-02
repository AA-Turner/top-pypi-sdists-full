from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.affinity_matrix_response import AffinityMatrixResponse
from ...models.affinity_matrix_response_scope_enum import AffinityMatrixResponseScopeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    scope: Union[Unset, AffinityMatrixResponseScopeEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_scope: Union[Unset, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/proposal-protected-calls/{uuid}/affinity-matrix/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> AffinityMatrixResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AffinityMatrixResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AffinityMatrixResponse]:
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
    scope: Union[Unset, AffinityMatrixResponseScopeEnum] = UNSET,
) -> Response[AffinityMatrixResponse]:
    """Get affinity matrix for reviewer-proposal matching.

    Args:
        uuid (UUID):
        scope (Union[Unset, AffinityMatrixResponseScopeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AffinityMatrixResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        scope=scope,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    scope: Union[Unset, AffinityMatrixResponseScopeEnum] = UNSET,
) -> AffinityMatrixResponse:
    """Get affinity matrix for reviewer-proposal matching.

    Args:
        uuid (UUID):
        scope (Union[Unset, AffinityMatrixResponseScopeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AffinityMatrixResponse
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        scope=scope,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    scope: Union[Unset, AffinityMatrixResponseScopeEnum] = UNSET,
) -> Response[AffinityMatrixResponse]:
    """Get affinity matrix for reviewer-proposal matching.

    Args:
        uuid (UUID):
        scope (Union[Unset, AffinityMatrixResponseScopeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AffinityMatrixResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        scope=scope,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    scope: Union[Unset, AffinityMatrixResponseScopeEnum] = UNSET,
) -> AffinityMatrixResponse:
    """Get affinity matrix for reviewer-proposal matching.

    Args:
        uuid (UUID):
        scope (Union[Unset, AffinityMatrixResponseScopeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AffinityMatrixResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            scope=scope,
        )
    ).parsed
