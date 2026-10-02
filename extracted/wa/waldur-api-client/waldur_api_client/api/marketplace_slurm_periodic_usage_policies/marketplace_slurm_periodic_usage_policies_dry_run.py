from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurm_policy_dry_run_response import SlurmPolicyDryRunResponse
from ...models.slurm_policy_evaluate_request_request import SlurmPolicyEvaluateRequestRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: SlurmPolicyEvaluateRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-slurm-periodic-usage-policies/{uuid}/dry-run/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> SlurmPolicyDryRunResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = SlurmPolicyDryRunResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmPolicyDryRunResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: SlurmPolicyEvaluateRequestRequest,
) -> Response[SlurmPolicyDryRunResponse]:
    """Staff-only. Dry-run evaluation: calculates usage percentages and shows what actions would be
    triggered, without applying any changes.

    Args:
        uuid (UUID):
        body (SlurmPolicyEvaluateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmPolicyDryRunResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: SlurmPolicyEvaluateRequestRequest,
) -> SlurmPolicyDryRunResponse:
    """Staff-only. Dry-run evaluation: calculates usage percentages and shows what actions would be
    triggered, without applying any changes.

    Args:
        uuid (UUID):
        body (SlurmPolicyEvaluateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmPolicyDryRunResponse
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: SlurmPolicyEvaluateRequestRequest,
) -> Response[SlurmPolicyDryRunResponse]:
    """Staff-only. Dry-run evaluation: calculates usage percentages and shows what actions would be
    triggered, without applying any changes.

    Args:
        uuid (UUID):
        body (SlurmPolicyEvaluateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmPolicyDryRunResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: SlurmPolicyEvaluateRequestRequest,
) -> SlurmPolicyDryRunResponse:
    """Staff-only. Dry-run evaluation: calculates usage percentages and shows what actions would be
    triggered, without applying any changes.

    Args:
        uuid (UUID):
        body (SlurmPolicyEvaluateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmPolicyDryRunResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
