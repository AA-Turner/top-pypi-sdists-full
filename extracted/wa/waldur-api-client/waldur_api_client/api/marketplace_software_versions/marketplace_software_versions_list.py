import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.catalog_type_enum import CatalogTypeEnum
from ...models.software_version import SoftwareVersion
from ...models.software_version_o_enum import SoftwareVersionOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/marketplace-software-versions/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["SoftwareVersion"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SoftwareVersion.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["SoftwareVersion"]]:
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
) -> Response[list["SoftwareVersion"]]:
    """List software versions

     Returns a paginated list of software versions. Can be filtered by package, catalog, offering, or CPU
    architecture.

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
        Response[list['SoftwareVersion']]
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
) -> list["SoftwareVersion"]:
    """List software versions

     Returns a paginated list of software versions. Can be filtered by package, catalog, offering, or CPU
    architecture.

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
        list['SoftwareVersion']
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
) -> Response[list["SoftwareVersion"]]:
    """List software versions

     Returns a paginated list of software versions. Can be filtered by package, catalog, offering, or CPU
    architecture.

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
        Response[list['SoftwareVersion']]
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
) -> list["SoftwareVersion"]:
    """List software versions

     Returns a paginated list of software versions. Can be filtered by package, catalog, offering, or CPU
    architecture.

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
        list['SoftwareVersion']
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


def sync_all(
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
    release_date_after: Union[Unset, datetime.date] = UNSET,
    release_date_before: Union[Unset, datetime.date] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
    toolchain_version: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    version_exact: Union[Unset, str] = UNSET,
) -> list["SoftwareVersion"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

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
        list['SoftwareVersion']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SoftwareVersion] = []

    # Get initial request kwargs
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
        release_date_after=release_date_after,
        release_date_before=release_date_before,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
        toolchain_version=toolchain_version,
        version=version,
        version_exact=version_exact,
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
    release_date_after: Union[Unset, datetime.date] = UNSET,
    release_date_before: Union[Unset, datetime.date] = UNSET,
    toolchain_families_compatibility: Union[Unset, str] = UNSET,
    toolchain_name: Union[Unset, str] = UNSET,
    toolchain_version: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    version_exact: Union[Unset, str] = UNSET,
) -> list["SoftwareVersion"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

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
        list['SoftwareVersion']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SoftwareVersion] = []

    # Get initial request kwargs
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
        release_date_after=release_date_after,
        release_date_before=release_date_before,
        toolchain_families_compatibility=toolchain_families_compatibility,
        toolchain_name=toolchain_name,
        toolchain_version=toolchain_version,
        version=version,
        version_exact=version_exact,
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
