from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resolve_npm_package_version_response_200 import ResolveNpmPackageVersionResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    package: str,
    *,
    tag: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["tag"] = tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/npm_proxy/resolve/{package}".format(
            workspace=workspace,
            package=package,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ResolveNpmPackageVersionResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ResolveNpmPackageVersionResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResolveNpmPackageVersionResponse200]:
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
    tag: Union[Unset, None, str] = UNSET,
) -> Response[ResolveNpmPackageVersionResponse200]:
    """resolve npm package version from private registry

    Args:
        workspace (str):
        package (str):
        tag (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResolveNpmPackageVersionResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        package=package,
        tag=tag,
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
    tag: Union[Unset, None, str] = UNSET,
) -> Optional[ResolveNpmPackageVersionResponse200]:
    """resolve npm package version from private registry

    Args:
        workspace (str):
        package (str):
        tag (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResolveNpmPackageVersionResponse200
    """

    return sync_detailed(
        workspace=workspace,
        package=package,
        client=client,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    package: str,
    *,
    client: Union[AuthenticatedClient, Client],
    tag: Union[Unset, None, str] = UNSET,
) -> Response[ResolveNpmPackageVersionResponse200]:
    """resolve npm package version from private registry

    Args:
        workspace (str):
        package (str):
        tag (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResolveNpmPackageVersionResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        package=package,
        tag=tag,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    package: str,
    *,
    client: Union[AuthenticatedClient, Client],
    tag: Union[Unset, None, str] = UNSET,
) -> Optional[ResolveNpmPackageVersionResponse200]:
    """resolve npm package version from private registry

    Args:
        workspace (str):
        package (str):
        tag (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResolveNpmPackageVersionResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            package=package,
            client=client,
            tag=tag,
        )
    ).parsed
