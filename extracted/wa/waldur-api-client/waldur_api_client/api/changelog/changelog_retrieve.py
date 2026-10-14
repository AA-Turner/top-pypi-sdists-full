from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.changelog_release import ChangelogRelease
from ...types import Response


def _get_kwargs(
    version: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/changelog/{version}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ChangelogRelease:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ChangelogRelease.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ChangelogRelease]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    version: str,
    *,
    client: AuthenticatedClient,
) -> Response[ChangelogRelease]:
    """Get changelog for a specific version

     Returns the full changelog for a specific release version.

    Args:
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogRelease]
    """

    kwargs = _get_kwargs(
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    version: str,
    *,
    client: AuthenticatedClient,
) -> ChangelogRelease:
    """Get changelog for a specific version

     Returns the full changelog for a specific release version.

    Args:
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogRelease
    """

    return sync_detailed(
        version=version,
        client=client,
    ).parsed


async def asyncio_detailed(
    version: str,
    *,
    client: AuthenticatedClient,
) -> Response[ChangelogRelease]:
    """Get changelog for a specific version

     Returns the full changelog for a specific release version.

    Args:
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogRelease]
    """

    kwargs = _get_kwargs(
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    version: str,
    *,
    client: AuthenticatedClient,
) -> ChangelogRelease:
    """Get changelog for a specific version

     Returns the full changelog for a specific release version.

    Args:
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogRelease
    """

    return (
        await asyncio_detailed(
            version=version,
            client=client,
        )
    ).parsed
