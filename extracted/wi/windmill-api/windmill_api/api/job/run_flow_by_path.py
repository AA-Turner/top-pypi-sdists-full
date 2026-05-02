import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.run_flow_by_path_json_body import RunFlowByPathJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    json_body: RunFlowByPathJsonBody,
    scheduled_for: Union[Unset, None, datetime.datetime] = UNSET,
    scheduled_in_secs: Union[Unset, None, int] = UNSET,
    skip_preprocessor: Union[Unset, None, bool] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    job_id: Union[Unset, None, str] = UNSET,
    include_header: Union[Unset, None, str] = UNSET,
    invisible_to_owner: Union[Unset, None, bool] = UNSET,
    memory_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_scheduled_for: Union[Unset, None, str] = UNSET
    if not isinstance(scheduled_for, Unset):
        json_scheduled_for = scheduled_for.isoformat() if scheduled_for else None

    params["scheduled_for"] = json_scheduled_for

    params["scheduled_in_secs"] = scheduled_in_secs

    params["skip_preprocessor"] = skip_preprocessor

    params["parent_job"] = parent_job

    params["tag"] = tag

    params["job_id"] = job_id

    params["include_header"] = include_header

    params["invisible_to_owner"] = invisible_to_owner

    params["memory_id"] = memory_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/jobs/run/f/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "json": json_json_body,
        "params": params,
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
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunFlowByPathJsonBody,
    scheduled_for: Union[Unset, None, datetime.datetime] = UNSET,
    scheduled_in_secs: Union[Unset, None, int] = UNSET,
    skip_preprocessor: Union[Unset, None, bool] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    job_id: Union[Unset, None, str] = UNSET,
    include_header: Union[Unset, None, str] = UNSET,
    invisible_to_owner: Union[Unset, None, bool] = UNSET,
    memory_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """run flow by path

    Args:
        workspace (str):
        path (str):
        scheduled_for (Union[Unset, None, datetime.datetime]):
        scheduled_in_secs (Union[Unset, None, int]):
        skip_preprocessor (Union[Unset, None, bool]):
        parent_job (Union[Unset, None, str]):
        tag (Union[Unset, None, str]):
        job_id (Union[Unset, None, str]):
        include_header (Union[Unset, None, str]):
        invisible_to_owner (Union[Unset, None, bool]):
        memory_id (Union[Unset, None, str]):
        json_body (RunFlowByPathJsonBody): The arguments to pass to the script or flow

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
        scheduled_for=scheduled_for,
        scheduled_in_secs=scheduled_in_secs,
        skip_preprocessor=skip_preprocessor,
        parent_job=parent_job,
        tag=tag,
        job_id=job_id,
        include_header=include_header,
        invisible_to_owner=invisible_to_owner,
        memory_id=memory_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunFlowByPathJsonBody,
    scheduled_for: Union[Unset, None, datetime.datetime] = UNSET,
    scheduled_in_secs: Union[Unset, None, int] = UNSET,
    skip_preprocessor: Union[Unset, None, bool] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    job_id: Union[Unset, None, str] = UNSET,
    include_header: Union[Unset, None, str] = UNSET,
    invisible_to_owner: Union[Unset, None, bool] = UNSET,
    memory_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """run flow by path

    Args:
        workspace (str):
        path (str):
        scheduled_for (Union[Unset, None, datetime.datetime]):
        scheduled_in_secs (Union[Unset, None, int]):
        skip_preprocessor (Union[Unset, None, bool]):
        parent_job (Union[Unset, None, str]):
        tag (Union[Unset, None, str]):
        job_id (Union[Unset, None, str]):
        include_header (Union[Unset, None, str]):
        invisible_to_owner (Union[Unset, None, bool]):
        memory_id (Union[Unset, None, str]):
        json_body (RunFlowByPathJsonBody): The arguments to pass to the script or flow

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
        scheduled_for=scheduled_for,
        scheduled_in_secs=scheduled_in_secs,
        skip_preprocessor=skip_preprocessor,
        parent_job=parent_job,
        tag=tag,
        job_id=job_id,
        include_header=include_header,
        invisible_to_owner=invisible_to_owner,
        memory_id=memory_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
