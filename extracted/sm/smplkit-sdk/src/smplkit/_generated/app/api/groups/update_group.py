from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.group_request import GroupRequest
from ...models.group_response import GroupResponse


def _get_kwargs(
    id: str,
    *,
    body: GroupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/groups/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GroupResponse | None:
    if response.status_code == 200:
        response_200 = GroupResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | GroupResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GroupRequest,
) -> Response[ErrorResponse | GroupResponse]:
    """Update Group

     Update a group's name, description, and managed environments. Whole-resource semantics — submit
    every writable attribute. For the reserved `default` group, `managed_environments` may be changed
    (this is the lever that narrows the account-wide baseline), but renaming or other identity changes
    are rejected with `409`. Invalid `managed_environments` is `422`.

    Args:
        id (str):
        body (GroupRequest): JSON:API request envelope for updating a group.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GroupResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GroupRequest,
) -> ErrorResponse | GroupResponse | None:
    """Update Group

     Update a group's name, description, and managed environments. Whole-resource semantics — submit
    every writable attribute. For the reserved `default` group, `managed_environments` may be changed
    (this is the lever that narrows the account-wide baseline), but renaming or other identity changes
    are rejected with `409`. Invalid `managed_environments` is `422`.

    Args:
        id (str):
        body (GroupRequest): JSON:API request envelope for updating a group.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GroupResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GroupRequest,
) -> Response[ErrorResponse | GroupResponse]:
    """Update Group

     Update a group's name, description, and managed environments. Whole-resource semantics — submit
    every writable attribute. For the reserved `default` group, `managed_environments` may be changed
    (this is the lever that narrows the account-wide baseline), but renaming or other identity changes
    are rejected with `409`. Invalid `managed_environments` is `422`.

    Args:
        id (str):
        body (GroupRequest): JSON:API request envelope for updating a group.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GroupResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GroupRequest,
) -> ErrorResponse | GroupResponse | None:
    """Update Group

     Update a group's name, description, and managed environments. Whole-resource semantics — submit
    every writable attribute. For the reserved `default` group, `managed_environments` may be changed
    (this is the lever that narrows the account-wide baseline), but renaming or other identity changes
    are rejected with `409`. Invalid `managed_environments` is `422`.

    Args:
        id (str):
        body (GroupRequest): JSON:API request envelope for updating a group.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GroupResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
