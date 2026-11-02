from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.runtime_response import RuntimeResponse
from ...types import UNSET, Response


def _get_kwargs(
    runtime_id: str,
    *,
    expected_revision: int,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["expected_revision"] = expected_revision

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/runtimes/{runtime_id}/pause".format(
            runtime_id=quote(str(runtime_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | RuntimeResponse:
    if response.status_code == 200:
        response_200 = RuntimeResponse.from_dict(response.json())

        return response_200

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
) -> Response[ErrorEnvelope | RuntimeResponse]:
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
    expected_revision: int,
) -> Response[ErrorEnvelope | RuntimeResponse]:
    """Pause a running runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        expected_revision (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | RuntimeResponse]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
        expected_revision=expected_revision,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
    expected_revision: int,
) -> ErrorEnvelope | RuntimeResponse | None:
    """Pause a running runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        expected_revision (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | RuntimeResponse
    """

    return sync_detailed(
        runtime_id=runtime_id,
        client=client,
        expected_revision=expected_revision,
    ).parsed


async def asyncio_detailed(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
    expected_revision: int,
) -> Response[ErrorEnvelope | RuntimeResponse]:
    """Pause a running runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        expected_revision (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | RuntimeResponse]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
        expected_revision=expected_revision,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
    expected_revision: int,
) -> ErrorEnvelope | RuntimeResponse | None:
    """Pause a running runtime

    Args:
        runtime_id (str): Runtime UUID or display name.
        expected_revision (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | RuntimeResponse
    """

    return (
        await asyncio_detailed(
            runtime_id=runtime_id,
            client=client,
            expected_revision=expected_revision,
        )
    ).parsed
