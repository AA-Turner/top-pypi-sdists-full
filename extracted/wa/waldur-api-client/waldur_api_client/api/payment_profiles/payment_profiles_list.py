from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.payment_profile import PaymentProfile
from ...models.payment_profile_o_enum import PaymentProfileOEnum
from ...models.payment_type_enum import PaymentTypeEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    is_active: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[PaymentProfileOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    payment_type: Union[Unset, list[PaymentTypeEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_active"] = is_active

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["organization"] = organization

    json_organization_uuid: Union[Unset, str] = UNSET
    if not isinstance(organization_uuid, Unset):
        json_organization_uuid = str(organization_uuid)
    params["organization_uuid"] = json_organization_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_payment_type: Union[Unset, list[str]] = UNSET
    if not isinstance(payment_type, Unset):
        json_payment_type = []
        for payment_type_item_data in payment_type:
            payment_type_item = payment_type_item_data.value
            json_payment_type.append(payment_type_item)

    params["payment_type"] = json_payment_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/payment-profiles/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["PaymentProfile"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PaymentProfile.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PaymentProfile"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[PaymentProfileOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    payment_type: Union[Unset, list[PaymentTypeEnum]] = UNSET,
) -> Response[list["PaymentProfile"]]:
    """
    Args:
        is_active (Union[Unset, bool]):
        o (Union[Unset, list[PaymentProfileOEnum]]):
        organization (Union[Unset, str]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        payment_type (Union[Unset, list[PaymentTypeEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PaymentProfile']]
    """

    kwargs = _get_kwargs(
        is_active=is_active,
        o=o,
        organization=organization,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        payment_type=payment_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[PaymentProfileOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    payment_type: Union[Unset, list[PaymentTypeEnum]] = UNSET,
) -> list["PaymentProfile"]:
    """
    Args:
        is_active (Union[Unset, bool]):
        o (Union[Unset, list[PaymentProfileOEnum]]):
        organization (Union[Unset, str]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        payment_type (Union[Unset, list[PaymentTypeEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PaymentProfile']
    """

    return sync_detailed(
        client=client,
        is_active=is_active,
        o=o,
        organization=organization,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        payment_type=payment_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[PaymentProfileOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    payment_type: Union[Unset, list[PaymentTypeEnum]] = UNSET,
) -> Response[list["PaymentProfile"]]:
    """
    Args:
        is_active (Union[Unset, bool]):
        o (Union[Unset, list[PaymentProfileOEnum]]):
        organization (Union[Unset, str]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        payment_type (Union[Unset, list[PaymentTypeEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PaymentProfile']]
    """

    kwargs = _get_kwargs(
        is_active=is_active,
        o=o,
        organization=organization,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        payment_type=payment_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[PaymentProfileOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    payment_type: Union[Unset, list[PaymentTypeEnum]] = UNSET,
) -> list["PaymentProfile"]:
    """
    Args:
        is_active (Union[Unset, bool]):
        o (Union[Unset, list[PaymentProfileOEnum]]):
        organization (Union[Unset, str]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        payment_type (Union[Unset, list[PaymentTypeEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PaymentProfile']
    """

    return (
        await asyncio_detailed(
            client=client,
            is_active=is_active,
            o=o,
            organization=organization,
            organization_uuid=organization_uuid,
            page=page,
            page_size=page_size,
            payment_type=payment_type,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[PaymentProfileOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    payment_type: Union[Unset, list[PaymentTypeEnum]] = UNSET,
) -> list["PaymentProfile"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_active (Union[Unset, bool]):
        o (Union[Unset, list[PaymentProfileOEnum]]):
        organization (Union[Unset, str]):
        organization_uuid (Union[Unset, UUID]):
        payment_type (Union[Unset, list[PaymentTypeEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PaymentProfile']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PaymentProfile] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_active=is_active,
        o=o,
        organization=organization,
        organization_uuid=organization_uuid,
        payment_type=payment_type,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    is_active: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[PaymentProfileOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    payment_type: Union[Unset, list[PaymentTypeEnum]] = UNSET,
) -> list["PaymentProfile"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_active (Union[Unset, bool]):
        o (Union[Unset, list[PaymentProfileOEnum]]):
        organization (Union[Unset, str]):
        organization_uuid (Union[Unset, UUID]):
        payment_type (Union[Unset, list[PaymentTypeEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PaymentProfile']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PaymentProfile] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_active=is_active,
        o=o,
        organization=organization,
        organization_uuid=organization_uuid,
        payment_type=payment_type,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
