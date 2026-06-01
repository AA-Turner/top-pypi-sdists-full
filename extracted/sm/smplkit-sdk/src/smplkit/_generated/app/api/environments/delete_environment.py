from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...types import Unset


def _get_kwargs(
    id: str,
    *,
    cascade: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["cascade"] = cascade

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/environments/{id}".format(
            id=quote(str(id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorResponse]:
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
    cascade: bool | Unset = False,
) -> Response[Any | ErrorResponse]:
    """Delete Environment

     Delete an environment by id. When `cascade=true` is set, also remove every per-environment reference
    held by flags, configs, and loggers in the corresponding services before deleting the environment
    row. The default `cascade=false` deletes only the environment row, leaving downstream references in
    place.

    Args:
        id (str):
        cascade (bool | Unset): When `true`, remove every flag rule, env-level flag default,
            config override, and logger override scoped to this environment before deleting the
            environment row. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        cascade=cascade,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    cascade: bool | Unset = False,
) -> Any | ErrorResponse | None:
    """Delete Environment

     Delete an environment by id. When `cascade=true` is set, also remove every per-environment reference
    held by flags, configs, and loggers in the corresponding services before deleting the environment
    row. The default `cascade=false` deletes only the environment row, leaving downstream references in
    place.

    Args:
        id (str):
        cascade (bool | Unset): When `true`, remove every flag rule, env-level flag default,
            config override, and logger override scoped to this environment before deleting the
            environment row. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        cascade=cascade,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    cascade: bool | Unset = False,
) -> Response[Any | ErrorResponse]:
    """Delete Environment

     Delete an environment by id. When `cascade=true` is set, also remove every per-environment reference
    held by flags, configs, and loggers in the corresponding services before deleting the environment
    row. The default `cascade=false` deletes only the environment row, leaving downstream references in
    place.

    Args:
        id (str):
        cascade (bool | Unset): When `true`, remove every flag rule, env-level flag default,
            config override, and logger override scoped to this environment before deleting the
            environment row. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        cascade=cascade,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    cascade: bool | Unset = False,
) -> Any | ErrorResponse | None:
    """Delete Environment

     Delete an environment by id. When `cascade=true` is set, also remove every per-environment reference
    held by flags, configs, and loggers in the corresponding services before deleting the environment
    row. The default `cascade=false` deletes only the environment row, leaving downstream references in
    place.

    Args:
        id (str):
        cascade (bool | Unset): When `true`, remove every flag rule, env-level flag default,
            config override, and logger override scoped to this environment before deleting the
            environment row. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            cascade=cascade,
        )
    ).parsed
