from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hpc_file_content import HpcFileContent
from ...types import UNSET, Response


def _get_kwargs(
    uuid: UUID,
    *,
    path: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/hpc-workspaces/{uuid}/file_content/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> HpcFileContent:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = HpcFileContent.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HpcFileContent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    path: str,
) -> Response[HpcFileContent]:
    """View a file on the cluster

     Content of a small text file (bounded by FirecREST's operation size limit).

    Args:
        uuid (UUID):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcFileContent]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    path: str,
) -> HpcFileContent:
    """View a file on the cluster

     Content of a small text file (bounded by FirecREST's operation size limit).

    Args:
        uuid (UUID):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcFileContent
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        path=path,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    path: str,
) -> Response[HpcFileContent]:
    """View a file on the cluster

     Content of a small text file (bounded by FirecREST's operation size limit).

    Args:
        uuid (UUID):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcFileContent]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    path: str,
) -> HpcFileContent:
    """View a file on the cluster

     Content of a small text file (bounded by FirecREST's operation size limit).

    Args:
        uuid (UUID):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcFileContent
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            path=path,
        )
    ).parsed
