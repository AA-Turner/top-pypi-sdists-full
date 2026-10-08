from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.issue_swap_code_session_request import IssueSwapCodeSessionRequest
from ...models.issue_swap_code_session_response import IssueSwapCodeSessionResponse
from ...types import Response


def _get_kwargs(
    *,
    body: IssueSwapCodeSessionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/v1/sessions/-issue-swap-code",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | IssueSwapCodeSessionResponse | None:
    if response.status_code == 200:
        response_200 = IssueSwapCodeSessionResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | IssueSwapCodeSessionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: IssueSwapCodeSessionRequest,
) -> Response[ErrorResponse | IssueSwapCodeSessionResponse]:
    """Mint a short-lived, single-use code to swap a CLI session into the web app

    Args:
        body (IssueSwapCodeSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IssueSwapCodeSessionResponse]
    """
    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: IssueSwapCodeSessionRequest,
) -> ErrorResponse | IssueSwapCodeSessionResponse | None:
    """Mint a short-lived, single-use code to swap a CLI session into the web app

    Args:
        body (IssueSwapCodeSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IssueSwapCodeSessionResponse
    """
    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: IssueSwapCodeSessionRequest,
) -> Response[ErrorResponse | IssueSwapCodeSessionResponse]:
    """Mint a short-lived, single-use code to swap a CLI session into the web app

    Args:
        body (IssueSwapCodeSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IssueSwapCodeSessionResponse]
    """
    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: IssueSwapCodeSessionRequest,
) -> ErrorResponse | IssueSwapCodeSessionResponse | None:
    """Mint a short-lived, single-use code to swap a CLI session into the web app

    Args:
        body (IssueSwapCodeSessionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IssueSwapCodeSessionResponse
    """
    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
