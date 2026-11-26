from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_nested_approvals_response_200 import ListNestedApprovalsResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    job_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/flow/nested_approvals/{job_id}".format(
            workspace=workspace,
            job_id=job_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListNestedApprovalsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListNestedApprovalsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListNestedApprovalsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListNestedApprovalsResponse200]:
    """list the approvals given in runs nested under a flow run

     List the approval steps that runs nested under a flow run (subflows, branch and loop runs, at any
    depth) went past, with who approved or rejected each and when. The flow run's own approval steps are
    not listed: they are in its flow status. Only the runs started by a step that can hold an approval
    step are read: a subflow, or a loop or branch whose steps hold one.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListNestedApprovalsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListNestedApprovalsResponse200]:
    """list the approvals given in runs nested under a flow run

     List the approval steps that runs nested under a flow run (subflows, branch and loop runs, at any
    depth) went past, with who approved or rejected each and when. The flow run's own approval steps are
    not listed: they are in its flow status. Only the runs started by a step that can hold an approval
    step are read: a subflow, or a loop or branch whose steps hold one.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListNestedApprovalsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListNestedApprovalsResponse200]:
    """list the approvals given in runs nested under a flow run

     List the approval steps that runs nested under a flow run (subflows, branch and loop runs, at any
    depth) went past, with who approved or rejected each and when. The flow run's own approval steps are
    not listed: they are in its flow status. Only the runs started by a step that can hold an approval
    step are read: a subflow, or a loop or branch whose steps hold one.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListNestedApprovalsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListNestedApprovalsResponse200]:
    """list the approvals given in runs nested under a flow run

     List the approval steps that runs nested under a flow run (subflows, branch and loop runs, at any
    depth) went past, with who approved or rejected each and when. The flow run's own approval steps are
    not listed: they are in its flow status. Only the runs started by a step that can hold an approval
    step are read: a subflow, or a loop or branch whose steps hold one.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListNestedApprovalsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            job_id=job_id,
            client=client,
        )
    ).parsed
