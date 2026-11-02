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
    suspended_job: Union[Unset, None, str] = UNSET,
    resume_id: Union[Unset, None, int] = UNSET,
    secret: Union[Unset, None, str] = UNSET,
    approver: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["suspended_job"] = suspended_job

    params["resume_id"] = resume_id

    params["secret"] = secret

    params["approver"] = approver

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs_u/completed/get_result/{id}".format(
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
    suspended_job: Union[Unset, None, str] = UNSET,
    resume_id: Union[Unset, None, int] = UNSET,
    secret: Union[Unset, None, str] = UNSET,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """get completed job result

    Args:
        workspace (str):
        id (str):
        suspended_job (Union[Unset, None, str]):
        resume_id (Union[Unset, None, int]):
        secret (Union[Unset, None, str]):
        approver (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        suspended_job=suspended_job,
        resume_id=resume_id,
        secret=secret,
        approver=approver,
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
    suspended_job: Union[Unset, None, str] = UNSET,
    resume_id: Union[Unset, None, int] = UNSET,
    secret: Union[Unset, None, str] = UNSET,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """get completed job result

    Args:
        workspace (str):
        id (str):
        suspended_job (Union[Unset, None, str]):
        resume_id (Union[Unset, None, int]):
        secret (Union[Unset, None, str]):
        approver (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        suspended_job=suspended_job,
        resume_id=resume_id,
        secret=secret,
        approver=approver,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
