from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_approval_step_detail_response_200 import GetApprovalStepDetailResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    job_id: str,
    step_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/flow/approval_step_detail/{job_id}/{step_id}".format(
            workspace=workspace,
            job_id=job_id,
            step_id=step_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetApprovalStepDetailResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetApprovalStepDetailResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetApprovalStepDetailResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    job_id: str,
    step_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetApprovalStepDetailResponse200]:
    """get the approval detail of one step of a flow run

     Get the approval state of an approval (suspend) step of a flow run, by the flow run id and the step
    id, in a single query: where the step stands, its approval settings, the approvals received and,
    while it waits, whether the caller can approve. Only the run's own steps are searched: for a step
    inside a branch or loop, pass the id of the branch's or iteration's run.

    Args:
        workspace (str):
        job_id (str):
        step_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApprovalStepDetailResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
        step_id=step_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    job_id: str,
    step_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetApprovalStepDetailResponse200]:
    """get the approval detail of one step of a flow run

     Get the approval state of an approval (suspend) step of a flow run, by the flow run id and the step
    id, in a single query: where the step stands, its approval settings, the approvals received and,
    while it waits, whether the caller can approve. Only the run's own steps are searched: for a step
    inside a branch or loop, pass the id of the branch's or iteration's run.

    Args:
        workspace (str):
        job_id (str):
        step_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApprovalStepDetailResponse200
    """

    return sync_detailed(
        workspace=workspace,
        job_id=job_id,
        step_id=step_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    job_id: str,
    step_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetApprovalStepDetailResponse200]:
    """get the approval detail of one step of a flow run

     Get the approval state of an approval (suspend) step of a flow run, by the flow run id and the step
    id, in a single query: where the step stands, its approval settings, the approvals received and,
    while it waits, whether the caller can approve. Only the run's own steps are searched: for a step
    inside a branch or loop, pass the id of the branch's or iteration's run.

    Args:
        workspace (str):
        job_id (str):
        step_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApprovalStepDetailResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
        step_id=step_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    job_id: str,
    step_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetApprovalStepDetailResponse200]:
    """get the approval detail of one step of a flow run

     Get the approval state of an approval (suspend) step of a flow run, by the flow run id and the step
    id, in a single query: where the step stands, its approval settings, the approvals received and,
    while it waits, whether the caller can approve. Only the run's own steps are searched: for a step
    inside a branch or loop, pass the id of the branch's or iteration's run.

    Args:
        workspace (str):
        job_id (str):
        step_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApprovalStepDetailResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            job_id=job_id,
            step_id=step_id,
            client=client,
        )
    ).parsed
