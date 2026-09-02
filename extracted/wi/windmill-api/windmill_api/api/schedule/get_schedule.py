from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_schedule_response_200 import GetScheduleResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    get_draft: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["get_draft"] = get_draft

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/schedules/get/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetScheduleResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetScheduleResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetScheduleResponse200]:
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
    get_draft: Union[Unset, None, bool] = UNSET,
) -> Response[GetScheduleResponse200]:
    """get schedule

    Args:
        workspace (str):
        path (str):
        get_draft (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetScheduleResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        get_draft=get_draft,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    get_draft: Union[Unset, None, bool] = UNSET,
) -> Optional[GetScheduleResponse200]:
    """get schedule

    Args:
        workspace (str):
        path (str):
        get_draft (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetScheduleResponse200
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
        get_draft=get_draft,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    get_draft: Union[Unset, None, bool] = UNSET,
) -> Response[GetScheduleResponse200]:
    """get schedule

    Args:
        workspace (str):
        path (str):
        get_draft (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetScheduleResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        get_draft=get_draft,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    get_draft: Union[Unset, None, bool] = UNSET,
) -> Optional[GetScheduleResponse200]:
    """get schedule

    Args:
        workspace (str):
        path (str):
        get_draft (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetScheduleResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
            get_draft=get_draft,
        )
    ).parsed
