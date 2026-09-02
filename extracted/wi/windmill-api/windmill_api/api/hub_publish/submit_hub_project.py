from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    slug: str,
    *,
    folder: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["folder"] = folder

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/w/{workspace}/hub/projects/{slug}/submit".format(
            workspace=workspace,
            slug=slug,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
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
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
    folder: str,
) -> Response[Any]:
    """submit a hub project draft for review

     Requires the caller to be a workspace admin. Forwards the request to the
    configured Hub scoped to the `{workspace}:{folder}` source and returns
    the Hub's status code and raw response body.

    Args:
        workspace (str):
        slug (str):
        folder (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        slug=slug,
        folder=folder,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
    folder: str,
) -> Response[Any]:
    """submit a hub project draft for review

     Requires the caller to be a workspace admin. Forwards the request to the
    configured Hub scoped to the `{workspace}:{folder}` source and returns
    the Hub's status code and raw response body.

    Args:
        workspace (str):
        slug (str):
        folder (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        slug=slug,
        folder=folder,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
