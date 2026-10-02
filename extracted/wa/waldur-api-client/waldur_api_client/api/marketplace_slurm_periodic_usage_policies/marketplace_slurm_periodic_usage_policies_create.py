from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurm_periodic_usage_policy import SlurmPeriodicUsagePolicy
from ...models.slurm_periodic_usage_policy_request import SlurmPeriodicUsagePolicyRequest
from ...types import Response


def _get_kwargs(
    *,
    body: SlurmPeriodicUsagePolicyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-slurm-periodic-usage-policies/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> SlurmPeriodicUsagePolicy:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = SlurmPeriodicUsagePolicy.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmPeriodicUsagePolicy]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SlurmPeriodicUsagePolicyRequest,
) -> Response[SlurmPeriodicUsagePolicy]:
    """
    Args:
        body (SlurmPeriodicUsagePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmPeriodicUsagePolicy]
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
    body: SlurmPeriodicUsagePolicyRequest,
) -> SlurmPeriodicUsagePolicy:
    """
    Args:
        body (SlurmPeriodicUsagePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmPeriodicUsagePolicy
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SlurmPeriodicUsagePolicyRequest,
) -> Response[SlurmPeriodicUsagePolicy]:
    """
    Args:
        body (SlurmPeriodicUsagePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmPeriodicUsagePolicy]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SlurmPeriodicUsagePolicyRequest,
) -> SlurmPeriodicUsagePolicy:
    """
    Args:
        body (SlurmPeriodicUsagePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmPeriodicUsagePolicy
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
