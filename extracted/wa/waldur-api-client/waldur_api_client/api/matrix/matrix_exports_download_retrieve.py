from http import HTTPStatus
from io import BytesIO
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_exports_download_retrieve_kind import MatrixExportsDownloadRetrieveKind
from ...types import File, Response


def _get_kwargs(
    uuid: str,
    kind: MatrixExportsDownloadRetrieveKind,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/matrix/exports/{uuid}/download/{kind}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> File:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    kind: MatrixExportsDownloadRetrieveKind,
    *,
    client: AuthenticatedClient,
) -> Response[File]:
    """Download a Matrix history export file

    Args:
        uuid (str):
        kind (MatrixExportsDownloadRetrieveKind):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        kind=kind,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    kind: MatrixExportsDownloadRetrieveKind,
    *,
    client: AuthenticatedClient,
) -> File:
    """Download a Matrix history export file

    Args:
        uuid (str):
        kind (MatrixExportsDownloadRetrieveKind):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return sync_detailed(
        uuid=uuid,
        kind=kind,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    kind: MatrixExportsDownloadRetrieveKind,
    *,
    client: AuthenticatedClient,
) -> Response[File]:
    """Download a Matrix history export file

    Args:
        uuid (str):
        kind (MatrixExportsDownloadRetrieveKind):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        kind=kind,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    kind: MatrixExportsDownloadRetrieveKind,
    *,
    client: AuthenticatedClient,
) -> File:
    """Download a Matrix history export file

    Args:
        uuid (str):
        kind (MatrixExportsDownloadRetrieveKind):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            kind=kind,
            client=client,
        )
    ).parsed
