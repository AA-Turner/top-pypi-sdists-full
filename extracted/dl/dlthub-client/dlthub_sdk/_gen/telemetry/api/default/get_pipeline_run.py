from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.pipeline_run_detail_response import PipelineRunDetailResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    pipeline_run_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/telemetry/v1/workspaces/{workspace_id}/pipeline-runs/{pipeline_run_id}".format(
            workspace_id=quote(str(workspace_id), safe=""),
            pipeline_run_id=quote(str(pipeline_run_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | PipelineRunDetailResponse | None:
    if response.status_code == 200:
        response_200 = PipelineRunDetailResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | PipelineRunDetailResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    pipeline_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse400 | PipelineRunDetailResponse]:
    """GetPipelineRun

    Args:
        workspace_id (UUID):
        pipeline_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | PipelineRunDetailResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        pipeline_run_id=pipeline_run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    pipeline_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse400 | PipelineRunDetailResponse | None:
    """GetPipelineRun

    Args:
        workspace_id (UUID):
        pipeline_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | PipelineRunDetailResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        pipeline_run_id=pipeline_run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    pipeline_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse400 | PipelineRunDetailResponse]:
    """GetPipelineRun

    Args:
        workspace_id (UUID):
        pipeline_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | PipelineRunDetailResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        pipeline_run_id=pipeline_run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    pipeline_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse400 | PipelineRunDetailResponse | None:
    """GetPipelineRun

    Args:
        workspace_id (UUID):
        pipeline_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | PipelineRunDetailResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            pipeline_run_id=pipeline_run_id,
            client=client,
        )
    ).parsed
