from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurm_policy_preview_request_request import SlurmPolicyPreviewRequestRequest
from ...models.slurm_policy_preview_response import SlurmPolicyPreviewResponse
from ...types import Response


def _get_kwargs(
    *,
    body: SlurmPolicyPreviewRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-slurm-periodic-usage-policies/preview_impact/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> SlurmPolicyPreviewResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = SlurmPolicyPreviewResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmPolicyPreviewResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SlurmPolicyPreviewRequestRequest,
) -> Response[SlurmPolicyPreviewResponse]:
    """Preview policy impact without saving. Returns threshold calculations, carryover projections, and QoS
    trigger points.

    Args:
        body (SlurmPolicyPreviewRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmPolicyPreviewResponse]
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
    body: SlurmPolicyPreviewRequestRequest,
) -> SlurmPolicyPreviewResponse:
    """Preview policy impact without saving. Returns threshold calculations, carryover projections, and QoS
    trigger points.

    Args:
        body (SlurmPolicyPreviewRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmPolicyPreviewResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SlurmPolicyPreviewRequestRequest,
) -> Response[SlurmPolicyPreviewResponse]:
    """Preview policy impact without saving. Returns threshold calculations, carryover projections, and QoS
    trigger points.

    Args:
        body (SlurmPolicyPreviewRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmPolicyPreviewResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SlurmPolicyPreviewRequestRequest,
) -> SlurmPolicyPreviewResponse:
    """Preview policy impact without saving. Returns threshold calculations, carryover projections, and QoS
    trigger points.

    Args:
        body (SlurmPolicyPreviewRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmPolicyPreviewResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
