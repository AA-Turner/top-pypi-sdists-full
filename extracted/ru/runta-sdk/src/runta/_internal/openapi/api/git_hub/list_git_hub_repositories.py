from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.git_hub_repository_list_response import GitHubRepositoryListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page_token: str | Unset = UNSET,
    page_size: int | Unset = 50,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page_token"] = page_token

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v2/github/repositories",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | GitHubRepositoryListResponse:
    if response.status_code == 200:
        response_200 = GitHubRepositoryListResponse.from_dict(response.json())

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
) -> Response[ErrorEnvelope | GitHubRepositoryListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page_token: str | Unset = UNSET,
    page_size: int | Unset = 50,
) -> Response[ErrorEnvelope | GitHubRepositoryListResponse]:
    """List cached GitHub repositories

    Args:
        page_token (str | Unset):
        page_size (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GitHubRepositoryListResponse]
    """

    kwargs = _get_kwargs(
        page_token=page_token,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page_token: str | Unset = UNSET,
    page_size: int | Unset = 50,
) -> ErrorEnvelope | GitHubRepositoryListResponse | None:
    """List cached GitHub repositories

    Args:
        page_token (str | Unset):
        page_size (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GitHubRepositoryListResponse
    """

    return sync_detailed(
        client=client,
        page_token=page_token,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page_token: str | Unset = UNSET,
    page_size: int | Unset = 50,
) -> Response[ErrorEnvelope | GitHubRepositoryListResponse]:
    """List cached GitHub repositories

    Args:
        page_token (str | Unset):
        page_size (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | GitHubRepositoryListResponse]
    """

    kwargs = _get_kwargs(
        page_token=page_token,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page_token: str | Unset = UNSET,
    page_size: int | Unset = 50,
) -> ErrorEnvelope | GitHubRepositoryListResponse | None:
    """List cached GitHub repositories

    Args:
        page_token (str | Unset):
        page_size (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | GitHubRepositoryListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page_token=page_token,
            page_size=page_size,
        )
    ).parsed
