from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_import_parameters_request import OfferingImportParametersRequest
from ...models.offering_import_response import OfferingImportResponse
from ...types import Response


def _get_kwargs(
    *,
    body: OfferingImportParametersRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-provider-offerings/import_offering/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OfferingImportResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OfferingImportResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OfferingImportResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: OfferingImportParametersRequest,
) -> Response[OfferingImportResponse]:
    """Import offering data

     Imports an offering and all its connected parts from YAML format. Allows configuration of which
    components to import and how to handle conflicts. Imported offerings are always created in DRAFT
    state for security.

    Args:
        body (OfferingImportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingImportResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: OfferingImportParametersRequest,
) -> OfferingImportResponse:
    """Import offering data

     Imports an offering and all its connected parts from YAML format. Allows configuration of which
    components to import and how to handle conflicts. Imported offerings are always created in DRAFT
    state for security.

    Args:
        body (OfferingImportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingImportResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: OfferingImportParametersRequest,
) -> Response[OfferingImportResponse]:
    """Import offering data

     Imports an offering and all its connected parts from YAML format. Allows configuration of which
    components to import and how to handle conflicts. Imported offerings are always created in DRAFT
    state for security.

    Args:
        body (OfferingImportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingImportResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: OfferingImportParametersRequest,
) -> OfferingImportResponse:
    """Import offering data

     Imports an offering and all its connected parts from YAML format. Allows configuration of which
    components to import and how to handle conflicts. Imported offerings are always created in DRAFT
    state for security.

    Args:
        body (OfferingImportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingImportResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
