from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.changelog_pending import ChangelogPending
from ...types import Response


def _get_kwargs(
    from_version: str,
    to_version: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/changelog/compare/{from_version}/{to_version}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ChangelogPending:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ChangelogPending.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ChangelogPending]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    from_version: str,
    to_version: str,
    *,
    client: AuthenticatedClient,
) -> Response[ChangelogPending]:
    """Compare changelog between two versions

     Returns merged delta entries between two arbitrary versions. Useful for seeing what changed between
    e.g. rc.5 and rc.12.

    Args:
        from_version (str):
        to_version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogPending]
    """

    kwargs = _get_kwargs(
        from_version=from_version,
        to_version=to_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    from_version: str,
    to_version: str,
    *,
    client: AuthenticatedClient,
) -> ChangelogPending:
    """Compare changelog between two versions

     Returns merged delta entries between two arbitrary versions. Useful for seeing what changed between
    e.g. rc.5 and rc.12.

    Args:
        from_version (str):
        to_version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogPending
    """

    return sync_detailed(
        from_version=from_version,
        to_version=to_version,
        client=client,
    ).parsed


async def asyncio_detailed(
    from_version: str,
    to_version: str,
    *,
    client: AuthenticatedClient,
) -> Response[ChangelogPending]:
    """Compare changelog between two versions

     Returns merged delta entries between two arbitrary versions. Useful for seeing what changed between
    e.g. rc.5 and rc.12.

    Args:
        from_version (str):
        to_version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogPending]
    """

    kwargs = _get_kwargs(
        from_version=from_version,
        to_version=to_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    from_version: str,
    to_version: str,
    *,
    client: AuthenticatedClient,
) -> ChangelogPending:
    """Compare changelog between two versions

     Returns merged delta entries between two arbitrary versions. Useful for seeing what changed between
    e.g. rc.5 and rc.12.

    Args:
        from_version (str):
        to_version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogPending
    """

    return (
        await asyncio_detailed(
            from_version=from_version,
            to_version=to_version,
            client=client,
        )
    ).parsed
