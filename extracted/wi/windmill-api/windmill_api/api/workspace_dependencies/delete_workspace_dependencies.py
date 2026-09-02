from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_workspace_dependencies_language import DeleteWorkspaceDependenciesLanguage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    language: DeleteWorkspaceDependenciesLanguage,
    *,
    name: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/w/{workspace}/workspace_dependencies/delete/{language}".format(
            workspace=workspace,
            language=language,
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
    language: DeleteWorkspaceDependenciesLanguage,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """delete workspace dependencies (require admin)

    Args:
        workspace (str):
        language (DeleteWorkspaceDependenciesLanguage):
        name (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    workspace: str,
    language: DeleteWorkspaceDependenciesLanguage,
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """delete workspace dependencies (require admin)

    Args:
        workspace (str):
        language (DeleteWorkspaceDependenciesLanguage):
        name (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        language=language,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
