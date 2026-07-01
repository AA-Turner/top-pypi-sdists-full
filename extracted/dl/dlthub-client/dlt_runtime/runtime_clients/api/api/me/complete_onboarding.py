from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.error_response_409 import ErrorResponse409
from ...models.me_response import MeResponse
from ...models.onboarding_request import OnboardingRequest
from ...types import Response


def _get_kwargs(
    *,
    body: OnboardingRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/me/onboarding",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ErrorResponse409
    | MeResponse
    | None
):
    if response.status_code == 201:
        response_201 = MeResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ErrorResponse409
    | MeResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: OnboardingRequest,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ErrorResponse409
    | MeResponse
]:
    r"""CompleteOnboarding


    Bootstrap the caller's organization with a playground workspace, making them its owner, and create
    the User row.

    Body fields are all optional — the API falls back to the first available dataplane
    and ``\"Personal Workspaces\"`` when omitted. ``workspace_name`` is deprecated and
    ignored; onboarding always creates exactly one workspace, the personal playground.

    Returns the same shape as ``GET /me`` so the client can proceed to the dashboard
    without a follow-up call. Returns 409 if the caller already has an active organization membership.

    Requires Authorization Header.

    Args:
        body (OnboardingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ErrorResponse409 | MeResponse]
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
    body: OnboardingRequest,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ErrorResponse409
    | MeResponse
    | None
):
    r"""CompleteOnboarding


    Bootstrap the caller's organization with a playground workspace, making them its owner, and create
    the User row.

    Body fields are all optional — the API falls back to the first available dataplane
    and ``\"Personal Workspaces\"`` when omitted. ``workspace_name`` is deprecated and
    ignored; onboarding always creates exactly one workspace, the personal playground.

    Returns the same shape as ``GET /me`` so the client can proceed to the dashboard
    without a follow-up call. Returns 409 if the caller already has an active organization membership.

    Requires Authorization Header.

    Args:
        body (OnboardingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ErrorResponse409 | MeResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: OnboardingRequest,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ErrorResponse409
    | MeResponse
]:
    r"""CompleteOnboarding


    Bootstrap the caller's organization with a playground workspace, making them its owner, and create
    the User row.

    Body fields are all optional — the API falls back to the first available dataplane
    and ``\"Personal Workspaces\"`` when omitted. ``workspace_name`` is deprecated and
    ignored; onboarding always creates exactly one workspace, the personal playground.

    Returns the same shape as ``GET /me`` so the client can proceed to the dashboard
    without a follow-up call. Returns 409 if the caller already has an active organization membership.

    Requires Authorization Header.

    Args:
        body (OnboardingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ErrorResponse409 | MeResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: OnboardingRequest,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ErrorResponse409
    | MeResponse
    | None
):
    r"""CompleteOnboarding


    Bootstrap the caller's organization with a playground workspace, making them its owner, and create
    the User row.

    Body fields are all optional — the API falls back to the first available dataplane
    and ``\"Personal Workspaces\"`` when omitted. ``workspace_name`` is deprecated and
    ignored; onboarding always creates exactly one workspace, the personal playground.

    Returns the same shape as ``GET /me`` so the client can proceed to the dashboard
    without a follow-up call. Returns 409 if the caller already has an active organization membership.

    Requires Authorization Header.

    Args:
        body (OnboardingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ErrorResponse409 | MeResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
