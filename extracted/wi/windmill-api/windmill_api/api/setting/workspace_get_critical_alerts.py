from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.workspace_get_critical_alerts_response_200 import WorkspaceGetCriticalAlertsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["page_size"] = page_size

    params["acknowledged"] = acknowledged

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/critical_alerts".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[WorkspaceGetCriticalAlertsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceGetCriticalAlertsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[WorkspaceGetCriticalAlertsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Response[WorkspaceGetCriticalAlertsResponse200]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceGetCriticalAlertsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        page=page,
        page_size=page_size,
        acknowledged=acknowledged,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Optional[WorkspaceGetCriticalAlertsResponse200]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceGetCriticalAlertsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        page=page,
        page_size=page_size,
        acknowledged=acknowledged,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Response[WorkspaceGetCriticalAlertsResponse200]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceGetCriticalAlertsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        page=page,
        page_size=page_size,
        acknowledged=acknowledged,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Optional[WorkspaceGetCriticalAlertsResponse200]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceGetCriticalAlertsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            page=page,
            page_size=page_size,
            acknowledged=acknowledged,
        )
    ).parsed
