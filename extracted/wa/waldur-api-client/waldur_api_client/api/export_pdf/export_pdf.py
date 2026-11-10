from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export_pdf_request import ExportPdfRequest
from ...types import Response


def _get_kwargs(
    *,
    body: ExportPdfRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/export-pdf/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ExportPdfRequest,
) -> Response[Any]:
    """Export a table or chart as PDF

     Renders the title with either a table (columns and rows of text) or a chart (a base64-encoded PNG)
    as a PDF. Nothing is read from the database: the PDF holds only what the request sends. A table may
    have at most 10000 rows, 100 columns, 50000 cells and 1000000 characters; an image at most 5 MB and
    25000000 pixels.

    Args:
        body (ExportPdfRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ExportPdfRequest,
) -> Response[Any]:
    """Export a table or chart as PDF

     Renders the title with either a table (columns and rows of text) or a chart (a base64-encoded PNG)
    as a PDF. Nothing is read from the database: the PDF holds only what the request sends. A table may
    have at most 10000 rows, 100 columns, 50000 cells and 1000000 characters; an image at most 5 MB and
    25000000 pixels.

    Args:
        body (ExportPdfRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
