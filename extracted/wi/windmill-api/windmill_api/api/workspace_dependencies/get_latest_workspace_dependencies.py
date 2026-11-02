from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_latest_workspace_dependencies_language import GetLatestWorkspaceDependenciesLanguage
from ...models.get_latest_workspace_dependencies_response_200 import GetLatestWorkspaceDependenciesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    language: GetLatestWorkspaceDependenciesLanguage,
    *,
    name: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspace_dependencies/get_latest/{language}".format(
            workspace=workspace,
            language=language,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetLatestWorkspaceDependenciesResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetLatestWorkspaceDependenciesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetLatestWorkspaceDependenciesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    language: GetLatestWorkspaceDependenciesLanguage,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, None, str] = UNSET,
) -> Response[GetLatestWorkspaceDependenciesResponse200]:
    """get latest workspace dependencies by language and name

    Args:
        workspace (str):
        language (GetLatestWorkspaceDependenciesLanguage):
        name (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetLatestWorkspaceDependenciesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        language=language,
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    language: GetLatestWorkspaceDependenciesLanguage,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, None, str] = UNSET,
) -> Optional[GetLatestWorkspaceDependenciesResponse200]:
    """get latest workspace dependencies by language and name

    Args:
        workspace (str):
        language (GetLatestWorkspaceDependenciesLanguage):
        name (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetLatestWorkspaceDependenciesResponse200
    """

    return sync_detailed(
        workspace=workspace,
        language=language,
        client=client,
        name=name,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    language: GetLatestWorkspaceDependenciesLanguage,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, None, str] = UNSET,
) -> Response[GetLatestWorkspaceDependenciesResponse200]:
    """get latest workspace dependencies by language and name

    Args:
        workspace (str):
        language (GetLatestWorkspaceDependenciesLanguage):
        name (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetLatestWorkspaceDependenciesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        language=language,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    language: GetLatestWorkspaceDependenciesLanguage,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, None, str] = UNSET,
) -> Optional[GetLatestWorkspaceDependenciesResponse200]:
    """get latest workspace dependencies by language and name

    Args:
        workspace (str):
        language (GetLatestWorkspaceDependenciesLanguage):
        name (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetLatestWorkspaceDependenciesResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            language=language,
            client=client,
            name=name,
        )
    ).parsed
