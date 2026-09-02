from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_wac_approval_urls_response_200 import GetWacApprovalUrlsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    step_key: str,
    *,
    approver: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["approver"] = approver

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/wac_approval_urls/{id}/{step_key}".format(
            workspace=workspace,
            id=id,
            step_key=step_key,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetWacApprovalUrlsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetWacApprovalUrlsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetWacApprovalUrlsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    id: str,
    step_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    approver: Union[Unset, None, str] = UNSET,
) -> Response[GetWacApprovalUrlsResponse200]:
    """get the resume urls bound to a specific wait_for_approval step of a workflow-as-code job

    Args:
        workspace (str):
        id (str):
        step_key (str):
        approver (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetWacApprovalUrlsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        step_key=step_key,
        approver=approver,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    id: str,
    step_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    approver: Union[Unset, None, str] = UNSET,
) -> Optional[GetWacApprovalUrlsResponse200]:
    """get the resume urls bound to a specific wait_for_approval step of a workflow-as-code job

    Args:
        workspace (str):
        id (str):
        step_key (str):
        approver (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetWacApprovalUrlsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        step_key=step_key,
        client=client,
        approver=approver,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    step_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    approver: Union[Unset, None, str] = UNSET,
) -> Response[GetWacApprovalUrlsResponse200]:
    """get the resume urls bound to a specific wait_for_approval step of a workflow-as-code job

    Args:
        workspace (str):
        id (str):
        step_key (str):
        approver (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetWacApprovalUrlsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        step_key=step_key,
        approver=approver,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    step_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    approver: Union[Unset, None, str] = UNSET,
) -> Optional[GetWacApprovalUrlsResponse200]:
    """get the resume urls bound to a specific wait_for_approval step of a workflow-as-code job

    Args:
        workspace (str):
        id (str):
        step_key (str):
        approver (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetWacApprovalUrlsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            step_key=step_key,
            client=client,
            approver=approver,
        )
    ).parsed
