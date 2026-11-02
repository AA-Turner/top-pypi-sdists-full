from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    job_or_input_id: str,
    *,
    input_: Union[Unset, None, bool] = UNSET,
    allow_large: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["input"] = input_

    params["allow_large"] = allow_large

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/inputs/{jobOrInputId}/args".format(
            workspace=workspace,
            jobOrInputId=job_or_input_id,
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
    job_or_input_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    input_: Union[Unset, None, bool] = UNSET,
    allow_large: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Get args from history or saved input

    Args:
        workspace (str):
        job_or_input_id (str):
        input_ (Union[Unset, None, bool]):
        allow_large (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_or_input_id=job_or_input_id,
        input_=input_,
        allow_large=allow_large,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    job_or_input_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    input_: Union[Unset, None, bool] = UNSET,
    allow_large: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Get args from history or saved input

    Args:
        workspace (str):
        job_or_input_id (str):
        input_ (Union[Unset, None, bool]):
        allow_large (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_or_input_id=job_or_input_id,
        input_=input_,
        allow_large=allow_large,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
