from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_postgres_publication_response_200 import GetPostgresPublicationResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    publication: str,
    path: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/postgres_triggers/publication/get/{publication}/{path}".format(
            workspace=workspace,
            publication=publication,
            path=path,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetPostgresPublicationResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetPostgresPublicationResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetPostgresPublicationResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    publication: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetPostgresPublicationResponse200]:
    """get postgres publication

    Args:
        workspace (str):
        publication (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPostgresPublicationResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        publication=publication,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    publication: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetPostgresPublicationResponse200]:
    """get postgres publication

    Args:
        workspace (str):
        publication (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPostgresPublicationResponse200
    """

    return sync_detailed(
        workspace=workspace,
        publication=publication,
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    publication: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetPostgresPublicationResponse200]:
    """get postgres publication

    Args:
        workspace (str):
        publication (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPostgresPublicationResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        publication=publication,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    publication: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetPostgresPublicationResponse200]:
    """get postgres publication

    Args:
        workspace (str):
        publication (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPostgresPublicationResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            publication=publication,
            path=path,
            client=client,
        )
    ).parsed
