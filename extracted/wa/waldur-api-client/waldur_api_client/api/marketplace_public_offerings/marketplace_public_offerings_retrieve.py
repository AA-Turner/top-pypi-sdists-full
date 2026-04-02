from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.public_offering_details import PublicOfferingDetails
from ...models.public_offering_details_field_enum import PublicOfferingDetailsFieldEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    field: Union[Unset, list[PublicOfferingDetailsFieldEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-public-offerings/{uuid}/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> PublicOfferingDetails:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = PublicOfferingDetails.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PublicOfferingDetails]:
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
    field: Union[Unset, list[PublicOfferingDetailsFieldEnum]] = UNSET,
) -> Response[PublicOfferingDetails]:
    """Retrieve a public offering

     Returns the details of a specific public offering. Access is granted if the offering is available
    for ordering by the current user or if anonymous access is enabled.

    Args:
        uuid (UUID):
        field (Union[Unset, list[PublicOfferingDetailsFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublicOfferingDetails]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[PublicOfferingDetailsFieldEnum]] = UNSET,
) -> PublicOfferingDetails:
    """Retrieve a public offering

     Returns the details of a specific public offering. Access is granted if the offering is available
    for ordering by the current user or if anonymous access is enabled.

    Args:
        uuid (UUID):
        field (Union[Unset, list[PublicOfferingDetailsFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PublicOfferingDetails
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        field=field,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[PublicOfferingDetailsFieldEnum]] = UNSET,
) -> Response[PublicOfferingDetails]:
    """Retrieve a public offering

     Returns the details of a specific public offering. Access is granted if the offering is available
    for ordering by the current user or if anonymous access is enabled.

    Args:
        uuid (UUID):
        field (Union[Unset, list[PublicOfferingDetailsFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublicOfferingDetails]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[PublicOfferingDetailsFieldEnum]] = UNSET,
) -> PublicOfferingDetails:
    """Retrieve a public offering

     Returns the details of a specific public offering. Access is granted if the offering is available
    for ordering by the current user or if anonymous access is enabled.

    Args:
        uuid (UUID):
        field (Union[Unset, list[PublicOfferingDetailsFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PublicOfferingDetails
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            field=field,
        )
    ).parsed
