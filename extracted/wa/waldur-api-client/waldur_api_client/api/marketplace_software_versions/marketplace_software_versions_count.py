import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.catalog_type_enum import CatalogTypeEnum
from ...models.software_version_o_enum import SoftwareVersionOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareVersionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_name: Union[Unset, str] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release_date_after: Union[Unset, datetime.date] = UNSET,
    release_date_before: Union[Unset, datetime.date] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
    toolchain_version: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    version_exact: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_catalog_type: Union[Unset, str] = UNSET
    if not isinstance(catalog_type, Unset):
        json_catalog_type = catalog_type.value

    params["catalog_type"] = json_catalog_type

    json_catalog_uuid: Union[Unset, str] = UNSET
    if not isinstance(catalog_uuid, Unset):
        json_catalog_uuid = str(catalog_uuid)
    params["catalog_uuid"] = json_catalog_uuid

    params["cpu_family"] = cpu_family

    params["cpu_microarchitecture"] = cpu_microarchitecture

    params["gpu_arch"] = gpu_arch

    params["has_gpu"] = has_gpu

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

    params["package_name"] = package_name

    json_package_uuid: Union[Unset, str] = UNSET
    if not isinstance(package_uuid, Unset):
        json_package_uuid = str(package_uuid)
    params["package_uuid"] = json_package_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_release_date_after: Union[Unset, str] = UNSET
    if not isinstance(release_date_after, Unset):
        json_release_date_after = release_date_after.isoformat()
    params["release_date_after"] = json_release_date_after

    json_release_date_before: Union[Unset, str] = UNSET
    if not isinstance(release_date_before, Unset):
        json_release_date_before = release_date_before.isoformat()
    params["release_date_before"] = json_release_date_before

    params["toolchain_families_compatibility"] = toolchain_families_compatibility

    params["toolchain_name"] = toolchain_name

    params["toolchain_version"] = toolchain_version

    params["version"] = version

    params["version_exact"] = version_exact

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-software-versions/",
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
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareVersionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_name: Union[Unset, str] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release_date_after: Union[Unset, datetime.date] = UNSET,
    release_date_before: Union[Unset, datetime.date] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
    toolchain_version: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    version_exact: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software versions

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareVersionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_name (Union[Unset, str]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release_date_after (Union[Unset, datetime.date]):
        release_date_before (Union[Unset, datetime.date]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):
        toolchain_version (Union[Unset, str]):
        version (Union[Unset, str]):
        version_exact (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        catalog_type=catalog_type,
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_name=package_name,
        package_uuid=package_uuid,
        page=page,
        page_size=page_size,
        release_date_after=release_date_after,
        release_date_before=release_date_before,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
        toolchain_version=toolchain_version,
        version=version,
        version_exact=version_exact,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareVersionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_name: Union[Unset, str] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release_date_after: Union[Unset, datetime.date] = UNSET,
    release_date_before: Union[Unset, datetime.date] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
    toolchain_version: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    version_exact: Union[Unset, str] = UNSET,
) -> int:
    """List software versions

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareVersionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_name (Union[Unset, str]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release_date_after (Union[Unset, datetime.date]):
        release_date_before (Union[Unset, datetime.date]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):
        toolchain_version (Union[Unset, str]):
        version (Union[Unset, str]):
        version_exact (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        catalog_type=catalog_type,
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_name=package_name,
        package_uuid=package_uuid,
        page=page,
        page_size=page_size,
        release_date_after=release_date_after,
        release_date_before=release_date_before,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
        toolchain_version=toolchain_version,
        version=version,
        version_exact=version_exact,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareVersionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_name: Union[Unset, str] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release_date_after: Union[Unset, datetime.date] = UNSET,
    release_date_before: Union[Unset, datetime.date] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
    toolchain_version: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    version_exact: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software versions

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareVersionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_name (Union[Unset, str]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release_date_after (Union[Unset, datetime.date]):
        release_date_before (Union[Unset, datetime.date]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):
        toolchain_version (Union[Unset, str]):
        version (Union[Unset, str]):
        version_exact (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        catalog_type=catalog_type,
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_name=package_name,
        package_uuid=package_uuid,
        page=page,
        page_size=page_size,
        release_date_after=release_date_after,
        release_date_before=release_date_before,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
        toolchain_version=toolchain_version,
        version=version,
        version_exact=version_exact,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    catalog_type: Union[Unset, CatalogTypeEnum] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareVersionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_name: Union[Unset, str] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release_date_after: Union[Unset, datetime.date] = UNSET,
    release_date_before: Union[Unset, datetime.date] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
    toolchain_version: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    version_exact: Union[Unset, str] = UNSET,
) -> int:
    """List software versions

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_type (Union[Unset, CatalogTypeEnum]):
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareVersionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_name (Union[Unset, str]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release_date_after (Union[Unset, datetime.date]):
        release_date_before (Union[Unset, datetime.date]):
        toolchain_families_compatibility (Union[Unset, str]):
        toolchain_name (Union[Unset, str]):
        toolchain_version (Union[Unset, str]):
        version (Union[Unset, str]):
        version_exact (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            catalog_type=catalog_type,
            catalog_uuid=catalog_uuid,
            cpu_family=cpu_family,
            cpu_microarchitecture=cpu_microarchitecture,
            gpu_arch=gpu_arch,
            has_gpu=has_gpu,
            o=o,
            offering_uuid=offering_uuid,
            package_name=package_name,
            package_uuid=package_uuid,
            page=page,
            page_size=page_size,
            release_date_after=release_date_after,
            release_date_before=release_date_before,
            toolchain_families_compatibility=toolchain_families_compatibility,
            toolchain_name=toolchain_name,
            toolchain_version=toolchain_version,
            version=version,
            version_exact=version_exact,
        )
    ).parsed
