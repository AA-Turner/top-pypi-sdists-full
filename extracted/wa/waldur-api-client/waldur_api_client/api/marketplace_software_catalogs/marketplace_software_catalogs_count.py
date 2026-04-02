from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.catalog_type_enum import CatalogTypeEnum
from ...models.software_catalog_o_enum import SoftwareCatalogOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    auto_update_enabled: Union[Unset, bool] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    description: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwareCatalogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["auto_update_enabled"] = auto_update_enabled

    json_catalog_type: Union[Unset, str] = UNSET
    if not isinstance(catalog_type, Unset):
        json_catalog_type = catalog_type.value

    params["catalog_type"] = json_catalog_type

    params["description"] = description

    params["name"] = name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["version"] = version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-software-catalogs/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    auto_update_enabled: Union[Unset, bool] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    description: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwareCatalogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software catalogs

     Get number of items in the collection matching the request parameters.

    Args:
        auto_update_enabled (Union[Unset, bool]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        description (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[SoftwareCatalogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        auto_update_enabled=auto_update_enabled,
        catalog_type=catalog_type,
        description=description,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    auto_update_enabled: Union[Unset, bool] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    description: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwareCatalogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> int:
    """List software catalogs

     Get number of items in the collection matching the request parameters.

    Args:
        auto_update_enabled (Union[Unset, bool]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        description (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[SoftwareCatalogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        auto_update_enabled=auto_update_enabled,
        catalog_type=catalog_type,
        description=description,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        version=version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    auto_update_enabled: Union[Unset, bool] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    description: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwareCatalogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software catalogs

     Get number of items in the collection matching the request parameters.

    Args:
        auto_update_enabled (Union[Unset, bool]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        description (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[SoftwareCatalogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        auto_update_enabled=auto_update_enabled,
        catalog_type=catalog_type,
        description=description,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    auto_update_enabled: Union[Unset, bool] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    description: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwareCatalogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> int:
    """List software catalogs

     Get number of items in the collection matching the request parameters.

    Args:
        auto_update_enabled (Union[Unset, bool]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        description (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[SoftwareCatalogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            auto_update_enabled=auto_update_enabled,
            catalog_type=catalog_type,
            description=description,
            name=name,
            o=o,
            page=page,
            page_size=page_size,
            version=version,
        )
    ).parsed
