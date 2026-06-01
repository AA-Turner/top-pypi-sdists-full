from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.account_wipe_request import AccountWipeRequest
from ...models.error_response import ErrorResponse


def _get_kwargs(
    *,
    body: AccountWipeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/accounts/current/actions/wipe",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
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
    *,
    client: AuthenticatedClient,
    body: AccountWipeRequest,
) -> Response[Any | ErrorResponse]:
    r"""Wipe Account Data

     Delete every config, flag, logger, log group, context, context type, environment, and customer API
    key (except the caller's current key) on the account. The `common` config is preserved as a
    structural anchor but its items are reset. Requires `OWNER` role and a body of `{\"confirm\": true}`
    — any other value returns 400. Pass `\"generate_sample_data\": true` to re-seed the account with the
    standard sample dataset after the wipe (best-effort; seeding failures are logged but do not fail the
    wipe). Returns 204 on success; 500 if any sub-delete fails.

    Args:
        body (AccountWipeRequest): Confirmation envelope for the wipe-account action. Example:
            {'confirm': True, 'generate_sample_data': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
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
    client: AuthenticatedClient,
    body: AccountWipeRequest,
) -> Any | ErrorResponse | None:
    r"""Wipe Account Data

     Delete every config, flag, logger, log group, context, context type, environment, and customer API
    key (except the caller's current key) on the account. The `common` config is preserved as a
    structural anchor but its items are reset. Requires `OWNER` role and a body of `{\"confirm\": true}`
    — any other value returns 400. Pass `\"generate_sample_data\": true` to re-seed the account with the
    standard sample dataset after the wipe (best-effort; seeding failures are logged but do not fail the
    wipe). Returns 204 on success; 500 if any sub-delete fails.

    Args:
        body (AccountWipeRequest): Confirmation envelope for the wipe-account action. Example:
            {'confirm': True, 'generate_sample_data': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AccountWipeRequest,
) -> Response[Any | ErrorResponse]:
    r"""Wipe Account Data

     Delete every config, flag, logger, log group, context, context type, environment, and customer API
    key (except the caller's current key) on the account. The `common` config is preserved as a
    structural anchor but its items are reset. Requires `OWNER` role and a body of `{\"confirm\": true}`
    — any other value returns 400. Pass `\"generate_sample_data\": true` to re-seed the account with the
    standard sample dataset after the wipe (best-effort; seeding failures are logged but do not fail the
    wipe). Returns 204 on success; 500 if any sub-delete fails.

    Args:
        body (AccountWipeRequest): Confirmation envelope for the wipe-account action. Example:
            {'confirm': True, 'generate_sample_data': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AccountWipeRequest,
) -> Any | ErrorResponse | None:
    r"""Wipe Account Data

     Delete every config, flag, logger, log group, context, context type, environment, and customer API
    key (except the caller's current key) on the account. The `common` config is preserved as a
    structural anchor but its items are reset. Requires `OWNER` role and a body of `{\"confirm\": true}`
    — any other value returns 400. Pass `\"generate_sample_data\": true` to re-seed the account with the
    standard sample dataset after the wipe (best-effort; seeding failures are logged but do not fail the
    wipe). Returns 204 on success; 500 if any sub-delete fails.

    Args:
        body (AccountWipeRequest): Confirmation envelope for the wipe-account action. Example:
            {'confirm': True, 'generate_sample_data': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
