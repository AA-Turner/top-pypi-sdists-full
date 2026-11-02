from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_all_experiments_response_200_item import ListAllExperimentsResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    subject_path: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["subject_path"] = subject_path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/ai_evals/experiments/list_all".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListAllExperimentsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListAllExperimentsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListAllExperimentsResponse200Item"]]:
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
    subject_path: Union[Unset, None, str] = UNSET,
) -> Response[List["ListAllExperimentsResponse200Item"]]:
    """list every experiment, across datasets

    Args:
        workspace (str):
        subject_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAllExperimentsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        subject_path=subject_path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    subject_path: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListAllExperimentsResponse200Item"]]:
    """list every experiment, across datasets

    Args:
        workspace (str):
        subject_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAllExperimentsResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        subject_path=subject_path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    subject_path: Union[Unset, None, str] = UNSET,
) -> Response[List["ListAllExperimentsResponse200Item"]]:
    """list every experiment, across datasets

    Args:
        workspace (str):
        subject_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAllExperimentsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        subject_path=subject_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    subject_path: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListAllExperimentsResponse200Item"]]:
    """list every experiment, across datasets

    Args:
        workspace (str):
        subject_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAllExperimentsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            subject_path=subject_path,
        )
    ).parsed
