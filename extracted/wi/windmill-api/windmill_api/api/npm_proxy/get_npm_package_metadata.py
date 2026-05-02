from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_npm_package_metadata_response_200 import GetNpmPackageMetadataResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    package: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/npm_proxy/metadata/{package}".format(
            workspace=workspace,
            package=package,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetNpmPackageMetadataResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetNpmPackageMetadataResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetNpmPackageMetadataResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    package: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetNpmPackageMetadataResponse200]:
    """get npm package metadata from private registry

    Args:
        workspace (str):
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetNpmPackageMetadataResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        package=package,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    package: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetNpmPackageMetadataResponse200]:
    """get npm package metadata from private registry

    Args:
        workspace (str):
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetNpmPackageMetadataResponse200
    """

    return sync_detailed(
        workspace=workspace,
        package=package,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    package: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetNpmPackageMetadataResponse200]:
    """get npm package metadata from private registry

    Args:
        workspace (str):
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetNpmPackageMetadataResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        package=package,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    package: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetNpmPackageMetadataResponse200]:
    """get npm package metadata from private registry

    Args:
        workspace (str):
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetNpmPackageMetadataResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            package=package,
            client=client,
        )
    ).parsed
