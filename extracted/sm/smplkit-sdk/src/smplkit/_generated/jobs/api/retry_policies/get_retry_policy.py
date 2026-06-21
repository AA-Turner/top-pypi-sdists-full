from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.retry_policy_response import RetryPolicyResponse


def _get_kwargs(
    policy_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/retry-policies/{policy_id}".format(
            policy_id=quote(str(policy_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> RetryPolicyResponse | None:
    if response.status_code == 200:
        response_200 = RetryPolicyResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[RetryPolicyResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    policy_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[RetryPolicyResponse]:
    """Get Retry Policy

     Retrieve a single retry policy by its id.

    `Default` returns the built-in do-not-retry policy.

    Args:
        policy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RetryPolicyResponse]
    """

    kwargs = _get_kwargs(
        policy_id=policy_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    policy_id: str,
    *,
    client: AuthenticatedClient,
) -> RetryPolicyResponse | None:
    """Get Retry Policy

     Retrieve a single retry policy by its id.

    `Default` returns the built-in do-not-retry policy.

    Args:
        policy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RetryPolicyResponse
    """

    return sync_detailed(
        policy_id=policy_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    policy_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[RetryPolicyResponse]:
    """Get Retry Policy

     Retrieve a single retry policy by its id.

    `Default` returns the built-in do-not-retry policy.

    Args:
        policy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RetryPolicyResponse]
    """

    kwargs = _get_kwargs(
        policy_id=policy_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    policy_id: str,
    *,
    client: AuthenticatedClient,
) -> RetryPolicyResponse | None:
    """Get Retry Policy

     Retrieve a single retry policy by its id.

    `Default` returns the built-in do-not-retry policy.

    Args:
        policy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RetryPolicyResponse
    """

    return (
        await asyncio_detailed(
            policy_id=policy_id,
            client=client,
        )
    ).parsed
