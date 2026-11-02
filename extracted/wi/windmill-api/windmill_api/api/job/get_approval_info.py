from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_approval_info_response_200 import GetApprovalInfoResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    job_id: str,
    *,
    token: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["token"] = token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs_u/flow/approval_info/{job_id}".format(
            workspace=workspace,
            job_id=job_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetApprovalInfoResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetApprovalInfoResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetApprovalInfoResponse200]:
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
    token: Union[Unset, None, str] = UNSET,
) -> Response[GetApprovalInfoResponse200]:
    """get approval info for a suspended flow/WAC job

     Get approval info for a suspended flow/WAC job. Returns form schema, approval rules, and whether the
    current user can approve. Either a valid token query parameter or an authenticated session is
    required.

    Args:
        workspace (str):
        job_id (str):
        token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApprovalInfoResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
        token=token,
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
    token: Union[Unset, None, str] = UNSET,
) -> Optional[GetApprovalInfoResponse200]:
    """get approval info for a suspended flow/WAC job

     Get approval info for a suspended flow/WAC job. Returns form schema, approval rules, and whether the
    current user can approve. Either a valid token query parameter or an authenticated session is
    required.

    Args:
        workspace (str):
        job_id (str):
        token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApprovalInfoResponse200
    """

    return sync_detailed(
        workspace=workspace,
        job_id=job_id,
        client=client,
        token=token,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    token: Union[Unset, None, str] = UNSET,
) -> Response[GetApprovalInfoResponse200]:
    """get approval info for a suspended flow/WAC job

     Get approval info for a suspended flow/WAC job. Returns form schema, approval rules, and whether the
    current user can approve. Either a valid token query parameter or an authenticated session is
    required.

    Args:
        workspace (str):
        job_id (str):
        token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApprovalInfoResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
        token=token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    token: Union[Unset, None, str] = UNSET,
) -> Optional[GetApprovalInfoResponse200]:
    """get approval info for a suspended flow/WAC job

     Get approval info for a suspended flow/WAC job. Returns form schema, approval rules, and whether the
    current user can approve. Either a valid token query parameter or an authenticated session is
    required.

    Args:
        workspace (str):
        job_id (str):
        token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApprovalInfoResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            job_id=job_id,
            client=client,
            token=token,
        )
    ).parsed
