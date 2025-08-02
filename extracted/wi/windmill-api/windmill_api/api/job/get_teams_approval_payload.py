from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    *,
    approver: Union[Unset, None, str] = UNSET,
    message: Union[Unset, None, str] = UNSET,
    team_name: str,
    channel_name: str,
    flow_step_id: str,
    default_args_json: Union[Unset, None, str] = UNSET,
    dynamic_enums_json: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["approver"] = approver

    params["message"] = message

    params["team_name"] = team_name

    params["channel_name"] = channel_name

    params["flow_step_id"] = flow_step_id

    params["default_args_json"] = default_args_json

    params["dynamic_enums_json"] = dynamic_enums_json

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/teams_approval/{id}".format(
            workspace=workspace,
            id=id,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
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
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    approver: Union[Unset, None, str] = UNSET,
    message: Union[Unset, None, str] = UNSET,
    team_name: str,
    channel_name: str,
    flow_step_id: str,
    default_args_json: Union[Unset, None, str] = UNSET,
    dynamic_enums_json: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """generate interactive teams approval for suspended job

    Args:
        workspace (str):
        id (str):
        approver (Union[Unset, None, str]):
        message (Union[Unset, None, str]):
        team_name (str):
        channel_name (str):
        flow_step_id (str):
        default_args_json (Union[Unset, None, str]):
        dynamic_enums_json (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        approver=approver,
        message=message,
        team_name=team_name,
        channel_name=channel_name,
        flow_step_id=flow_step_id,
        default_args_json=default_args_json,
        dynamic_enums_json=dynamic_enums_json,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    approver: Union[Unset, None, str] = UNSET,
    message: Union[Unset, None, str] = UNSET,
    team_name: str,
    channel_name: str,
    flow_step_id: str,
    default_args_json: Union[Unset, None, str] = UNSET,
    dynamic_enums_json: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """generate interactive teams approval for suspended job

    Args:
        workspace (str):
        id (str):
        approver (Union[Unset, None, str]):
        message (Union[Unset, None, str]):
        team_name (str):
        channel_name (str):
        flow_step_id (str):
        default_args_json (Union[Unset, None, str]):
        dynamic_enums_json (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        approver=approver,
        message=message,
        team_name=team_name,
        channel_name=channel_name,
        flow_step_id=flow_step_id,
        default_args_json=default_args_json,
        dynamic_enums_json=dynamic_enums_json,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
