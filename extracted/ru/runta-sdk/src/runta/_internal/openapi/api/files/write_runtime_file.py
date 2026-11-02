from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, File, Response


def _get_kwargs(
    runtime_id: str,
    *,
    body: File,
    path: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v2/runtimes/{runtime_id}/files".format(
            runtime_id=quote(str(runtime_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorEnvelope:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 501:
        response_501 = ErrorEnvelope.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ErrorEnvelope.from_dict(response.json())

        return response_504

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
) -> Response[Any | ErrorEnvelope]:
    """Write a single file into a runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        path (str): Absolute path to a regular file inside the runtime.
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
        body=body,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
) -> Any | ErrorEnvelope | None:
    """Write a single file into a runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        path (str): Absolute path to a regular file inside the runtime.
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorEnvelope
    """

    return sync_detailed(
        runtime_id=runtime_id,
        client=client,
        body=body,
        path=path,
    ).parsed


async def asyncio_detailed(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
) -> Response[Any | ErrorEnvelope]:
    """Write a single file into a runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        path (str): Absolute path to a regular file inside the runtime.
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
        body=body,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    path: str,
) -> Any | ErrorEnvelope | None:
    """Write a single file into a runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        path (str): Absolute path to a regular file inside the runtime.
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            runtime_id=runtime_id,
            client=client,
            body=body,
            path=path,
        )
    ).parsed
