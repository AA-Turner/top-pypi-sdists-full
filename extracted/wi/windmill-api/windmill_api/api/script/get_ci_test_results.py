from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_ci_test_results_kind import GetCiTestResultsKind
from ...models.get_ci_test_results_response_200_item import GetCiTestResultsResponse200Item
from ...types import Response


def _get_kwargs(
    workspace: str,
    kind: GetCiTestResultsKind,
    path: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/scripts/ci_test_results/{kind}/{path}".format(
            workspace=workspace,
            kind=kind,
            path=path,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["GetCiTestResultsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetCiTestResultsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["GetCiTestResultsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    kind: GetCiTestResultsKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["GetCiTestResultsResponse200Item"]]:
    """get CI test results for a script, flow, or resource

    Args:
        workspace (str):
        kind (GetCiTestResultsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetCiTestResultsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    kind: GetCiTestResultsKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["GetCiTestResultsResponse200Item"]]:
    """get CI test results for a script, flow, or resource

    Args:
        workspace (str):
        kind (GetCiTestResultsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetCiTestResultsResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        kind=kind,
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    kind: GetCiTestResultsKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["GetCiTestResultsResponse200Item"]]:
    """get CI test results for a script, flow, or resource

    Args:
        workspace (str):
        kind (GetCiTestResultsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetCiTestResultsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    kind: GetCiTestResultsKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["GetCiTestResultsResponse200Item"]]:
    """get CI test results for a script, flow, or resource

    Args:
        workspace (str):
        kind (GetCiTestResultsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetCiTestResultsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            kind=kind,
            path=path,
            client=client,
        )
    ).parsed
