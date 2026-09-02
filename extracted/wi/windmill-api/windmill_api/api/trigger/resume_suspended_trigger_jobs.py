from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resume_suspended_trigger_jobs_json_body import ResumeSuspendedTriggerJobsJsonBody
from ...models.resume_suspended_trigger_jobs_trigger_kind import ResumeSuspendedTriggerJobsTriggerKind
from ...types import Response


def _get_kwargs(
    workspace: str,
    trigger_kind: ResumeSuspendedTriggerJobsTriggerKind,
    trigger_path: str,
    *,
    json_body: ResumeSuspendedTriggerJobsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/trigger/{trigger_kind}/resume_suspended_trigger_jobs/{trigger_path}".format(
            workspace=workspace,
            trigger_kind=trigger_kind,
            trigger_path=trigger_path,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[str]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    trigger_kind: ResumeSuspendedTriggerJobsTriggerKind,
    trigger_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ResumeSuspendedTriggerJobsJsonBody,
) -> Response[str]:
    """resume all suspended jobs for a specific trigger

    Args:
        workspace (str):
        trigger_kind (ResumeSuspendedTriggerJobsTriggerKind): job trigger kind (schedule, http,
            websocket...)
        trigger_path (str):
        json_body (ResumeSuspendedTriggerJobsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        trigger_kind=trigger_kind,
        trigger_path=trigger_path,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    trigger_kind: ResumeSuspendedTriggerJobsTriggerKind,
    trigger_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ResumeSuspendedTriggerJobsJsonBody,
) -> Optional[str]:
    """resume all suspended jobs for a specific trigger

    Args:
        workspace (str):
        trigger_kind (ResumeSuspendedTriggerJobsTriggerKind): job trigger kind (schedule, http,
            websocket...)
        trigger_path (str):
        json_body (ResumeSuspendedTriggerJobsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return sync_detailed(
        workspace=workspace,
        trigger_kind=trigger_kind,
        trigger_path=trigger_path,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    trigger_kind: ResumeSuspendedTriggerJobsTriggerKind,
    trigger_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ResumeSuspendedTriggerJobsJsonBody,
) -> Response[str]:
    """resume all suspended jobs for a specific trigger

    Args:
        workspace (str):
        trigger_kind (ResumeSuspendedTriggerJobsTriggerKind): job trigger kind (schedule, http,
            websocket...)
        trigger_path (str):
        json_body (ResumeSuspendedTriggerJobsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        trigger_kind=trigger_kind,
        trigger_path=trigger_path,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    trigger_kind: ResumeSuspendedTriggerJobsTriggerKind,
    trigger_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ResumeSuspendedTriggerJobsJsonBody,
) -> Optional[str]:
    """resume all suspended jobs for a specific trigger

    Args:
        workspace (str):
        trigger_kind (ResumeSuspendedTriggerJobsTriggerKind): job trigger kind (schedule, http,
            websocket...)
        trigger_path (str):
        json_body (ResumeSuspendedTriggerJobsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            trigger_kind=trigger_kind,
            trigger_path=trigger_path,
            client=client,
            json_body=json_body,
        )
    ).parsed
