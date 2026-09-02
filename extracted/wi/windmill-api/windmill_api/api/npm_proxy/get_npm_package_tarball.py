from http import HTTPStatus
from io import BytesIO
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import File, Response


def _get_kwargs(
    workspace: str,
    package: str,
    version: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/npm_proxy/tarball/{package}/{version}".format(
            workspace=workspace,
            package=package,
            version=version,
        ),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[File]:
    if response.status_code == HTTPStatus.OK:
        response_200 = File(payload=BytesIO(response.content))

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    package: str,
    version: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[File]:
    """get npm package tarball from private registry

    Args:
        workspace (str):
        package (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        package=package,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    package: str,
    version: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[File]:
    """get npm package tarball from private registry

    Args:
        workspace (str):
        package (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return sync_detailed(
        workspace=workspace,
        package=package,
        version=version,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    package: str,
    version: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[File]:
    """get npm package tarball from private registry

    Args:
        workspace (str):
        package (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        package=package,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    package: str,
    version: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[File]:
    """get npm package tarball from private registry

    Args:
        workspace (str):
        package (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            package=package,
            version=version,
            client=client,
        )
    ).parsed
