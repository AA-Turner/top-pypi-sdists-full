from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.catalog_type_enum import CatalogTypeEnum
from ...models.software_package_o_enum import SoftwarePackageOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    extension_name: Union[Unset, str] = UNSET,
    extension_type: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    is_extension: Union[Unset, bool] = UNSET,
    license_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwarePackageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_software_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["catalog_name"] = catalog_name

    json_catalog_type: Union[Unset, str] = UNSET
    if not isinstance(catalog_type, Unset):
        json_catalog_type = catalog_type.value

    params["catalog_type"] = json_catalog_type

    json_catalog_uuid: Union[Unset, str] = UNSET
    if not isinstance(catalog_uuid, Unset):
        json_catalog_uuid = str(catalog_uuid)
    params["catalog_uuid"] = json_catalog_uuid

    params["catalog_version"] = catalog_version

    params["category"] = category

    params["cpu_family"] = cpu_family

    params["cpu_microarchitecture"] = cpu_microarchitecture

    params["description"] = description

    params["extension_name"] = extension_name

    params["extension_type"] = extension_type

    params["gpu_arch"] = gpu_arch

    params["has_gpu"] = has_gpu

    params["has_version"] = has_version

    params["is_extension"] = is_extension

    params["license"] = license_

    params["name"] = name

    params["name_exact"] = name_exact

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_parent_software_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_software_uuid, Unset):
        json_parent_software_uuid = str(parent_software_uuid)
    params["parent_software_uuid"] = json_parent_software_uuid

    params["query"] = query

    params["toolchain_families_compatibility"] = toolchain_families_compatibility

    params["toolchain_name"] = toolchain_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-software-packages/",
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
    catalog_name: Union[Unset, str] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    extension_name: Union[Unset, str] = UNSET,
    extension_type: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    is_extension: Union[Unset, bool] = UNSET,
    license_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwarePackageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_software_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        category (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        extension_name (Union[Unset, str]):
        extension_type (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        has_version (Union[Unset, str]):
        is_extension (Union[Unset, bool]):
        license_ (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SoftwarePackageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_software_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        catalog_name=catalog_name,
        catalog_type=catalog_type,
        catalog_uuid=catalog_uuid,
        catalog_version=catalog_version,
        category=category,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        description=description,
        extension_name=extension_name,
        extension_type=extension_type,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        has_version=has_version,
        is_extension=is_extension,
        license_=license_,
        name=name,
        name_exact=name_exact,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_software_uuid=parent_software_uuid,
        query=query,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    extension_name: Union[Unset, str] = UNSET,
    extension_type: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    is_extension: Union[Unset, bool] = UNSET,
    license_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwarePackageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_software_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
) -> int:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        category (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        extension_name (Union[Unset, str]):
        extension_type (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        has_version (Union[Unset, str]):
        is_extension (Union[Unset, bool]):
        license_ (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SoftwarePackageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_software_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        catalog_name=catalog_name,
        catalog_type=catalog_type,
        catalog_uuid=catalog_uuid,
        catalog_version=catalog_version,
        category=category,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        description=description,
        extension_name=extension_name,
        extension_type=extension_type,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        has_version=has_version,
        is_extension=is_extension,
        license_=license_,
        name=name,
        name_exact=name_exact,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_software_uuid=parent_software_uuid,
        query=query,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    extension_name: Union[Unset, str] = UNSET,
    extension_type: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    is_extension: Union[Unset, bool] = UNSET,
    license_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwarePackageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_software_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        category (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        extension_name (Union[Unset, str]):
        extension_type (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        has_version (Union[Unset, str]):
        is_extension (Union[Unset, bool]):
        license_ (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SoftwarePackageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_software_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        catalog_name=catalog_name,
        catalog_type=catalog_type,
        catalog_uuid=catalog_uuid,
        catalog_version=catalog_version,
        category=category,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        description=description,
        extension_name=extension_name,
        extension_type=extension_type,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        has_version=has_version,
        is_extension=is_extension,
        license_=license_,
        name=name,
        name_exact=name_exact,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_software_uuid=parent_software_uuid,
        query=query,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    extension_name: Union[Unset, str] = UNSET,
    extension_type: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    is_extension: Union[Unset, bool] = UNSET,
    license_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SoftwarePackageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_software_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
) -> int:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        category (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        extension_name (Union[Unset, str]):
        extension_type (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        has_version (Union[Unset, str]):
        is_extension (Union[Unset, bool]):
        license_ (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SoftwarePackageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_software_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            catalog_name=catalog_name,
            catalog_type=catalog_type,
            catalog_uuid=catalog_uuid,
            catalog_version=catalog_version,
            category=category,
            cpu_family=cpu_family,
            cpu_microarchitecture=cpu_microarchitecture,
            description=description,
            extension_name=extension_name,
            extension_type=extension_type,
            gpu_arch=gpu_arch,
            has_gpu=has_gpu,
            has_version=has_version,
            is_extension=is_extension,
            license_=license_,
            name=name,
            name_exact=name_exact,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            parent_software_uuid=parent_software_uuid,
            query=query,
            toolchain_families_compatibility=toolchain_families_compatibility,
            toolchain_name=toolchain_name,
        )
    ).parsed
