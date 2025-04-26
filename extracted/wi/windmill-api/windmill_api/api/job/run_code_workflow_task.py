from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.run_code_workflow_task_json_body import RunCodeWorkflowTaskJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    job_id: str,
    entrypoint: str,
    *,
    json_body: RunCodeWorkflowTaskJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/jobs/workflow_as_code/{job_id}/{entrypoint}".format(
            workspace=workspace,
            job_id=job_id,
            entrypoint=entrypoint,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    job_id: str,
    entrypoint: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunCodeWorkflowTaskJsonBody,
) -> Response[Any]:
    """run code-workflow task

    Args:
        workspace (str):
        job_id (str):
        entrypoint (str):
        json_body (RunCodeWorkflowTaskJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
        entrypoint=entrypoint,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    job_id: str,
    entrypoint: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunCodeWorkflowTaskJsonBody,
) -> Response[Any]:
    """run code-workflow task

    Args:
        workspace (str):
        job_id (str):
        entrypoint (str):
        json_body (RunCodeWorkflowTaskJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
        entrypoint=entrypoint,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
