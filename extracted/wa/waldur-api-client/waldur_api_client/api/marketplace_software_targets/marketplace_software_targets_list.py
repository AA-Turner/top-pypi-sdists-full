from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.software_target import SoftwareTarget
from ...models.software_target_o_enum import SoftwareTargetOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareTargetOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    target_name: Union[Unset, str] = UNSET,
    target_subtype: Union[Unset, str] = UNSET,
    target_type: Union[Unset, str] = UNSET,
    version_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

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

    json_package_uuid: Union[Unset, str] = UNSET
    if not isinstance(package_uuid, Unset):
        json_package_uuid = str(package_uuid)
    params["package_uuid"] = json_package_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["path"] = path

    params["target_name"] = target_name

    params["target_subtype"] = target_subtype

    params["target_type"] = target_type

    json_version_uuid: Union[Unset, str] = UNSET
    if not isinstance(version_uuid, Unset):
        json_version_uuid = str(version_uuid)
    params["version_uuid"] = json_version_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-software-targets/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["SoftwareTarget"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SoftwareTarget.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["SoftwareTarget"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareTargetOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    target_name: Union[Unset, str] = UNSET,
    target_subtype: Union[Unset, str] = UNSET,
    target_type: Union[Unset, str] = UNSET,
    version_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["SoftwareTarget"]]:
    """List software targets

     Returns a paginated list of software targets, which represent specific builds of a software version
    for a given CPU architecture.

    Args:
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareTargetOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        path (Union[Unset, str]):
        target_name (Union[Unset, str]):
        target_subtype (Union[Unset, str]):
        target_type (Union[Unset, str]):
        version_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SoftwareTarget']]
    """

    kwargs = _get_kwargs(
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_uuid=package_uuid,
        page=page,
        page_size=page_size,
        path=path,
        target_name=target_name,
        target_subtype=target_subtype,
        target_type=target_type,
        version_uuid=version_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareTargetOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    target_name: Union[Unset, str] = UNSET,
    target_subtype: Union[Unset, str] = UNSET,
    target_type: Union[Unset, str] = UNSET,
    version_uuid: Union[Unset, UUID] = UNSET,
) -> list["SoftwareTarget"]:
    """List software targets

     Returns a paginated list of software targets, which represent specific builds of a software version
    for a given CPU architecture.

    Args:
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareTargetOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        path (Union[Unset, str]):
        target_name (Union[Unset, str]):
        target_subtype (Union[Unset, str]):
        target_type (Union[Unset, str]):
        version_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SoftwareTarget']
    """

    return sync_detailed(
        client=client,
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_uuid=package_uuid,
        page=page,
        page_size=page_size,
        path=path,
        target_name=target_name,
        target_subtype=target_subtype,
        target_type=target_type,
        version_uuid=version_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareTargetOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    target_name: Union[Unset, str] = UNSET,
    target_subtype: Union[Unset, str] = UNSET,
    target_type: Union[Unset, str] = UNSET,
    version_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["SoftwareTarget"]]:
    """List software targets

     Returns a paginated list of software targets, which represent specific builds of a software version
    for a given CPU architecture.

    Args:
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareTargetOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        path (Union[Unset, str]):
        target_name (Union[Unset, str]):
        target_subtype (Union[Unset, str]):
        target_type (Union[Unset, str]):
        version_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SoftwareTarget']]
    """

    kwargs = _get_kwargs(
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_uuid=package_uuid,
        page=page,
        page_size=page_size,
        path=path,
        target_name=target_name,
        target_subtype=target_subtype,
        target_type=target_type,
        version_uuid=version_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareTargetOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    target_name: Union[Unset, str] = UNSET,
    target_subtype: Union[Unset, str] = UNSET,
    target_type: Union[Unset, str] = UNSET,
    version_uuid: Union[Unset, UUID] = UNSET,
) -> list["SoftwareTarget"]:
    """List software targets

     Returns a paginated list of software targets, which represent specific builds of a software version
    for a given CPU architecture.

    Args:
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareTargetOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        path (Union[Unset, str]):
        target_name (Union[Unset, str]):
        target_subtype (Union[Unset, str]):
        target_type (Union[Unset, str]):
        version_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SoftwareTarget']
    """

    return (
        await asyncio_detailed(
            client=client,
            catalog_uuid=catalog_uuid,
            cpu_family=cpu_family,
            cpu_microarchitecture=cpu_microarchitecture,
            gpu_arch=gpu_arch,
            has_gpu=has_gpu,
            o=o,
            offering_uuid=offering_uuid,
            package_uuid=package_uuid,
            page=page,
            page_size=page_size,
            path=path,
            target_name=target_name,
            target_subtype=target_subtype,
            target_type=target_type,
            version_uuid=version_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareTargetOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    path: Union[Unset, str] = UNSET,
    target_name: Union[Unset, str] = UNSET,
    target_subtype: Union[Unset, str] = UNSET,
    target_type: Union[Unset, str] = UNSET,
    version_uuid: Union[Unset, UUID] = UNSET,
) -> list["SoftwareTarget"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareTargetOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_uuid (Union[Unset, UUID]):
        path (Union[Unset, str]):
        target_name (Union[Unset, str]):
        target_subtype (Union[Unset, str]):
        target_type (Union[Unset, str]):
        version_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SoftwareTarget']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SoftwareTarget] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_uuid=package_uuid,
        path=path,
        target_name=target_name,
        target_subtype=target_subtype,
        target_type=target_type,
        version_uuid=version_uuid,
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
    catalog_uuid: Union[Unset, UUID] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    gpu_arch: Union[Unset, str] = UNSET,
    has_gpu: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[SoftwareTargetOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    package_uuid: Union[Unset, UUID] = UNSET,
    path: Union[Unset, str] = UNSET,
    target_name: Union[Unset, str] = UNSET,
    target_subtype: Union[Unset, str] = UNSET,
    target_type: Union[Unset, str] = UNSET,
    version_uuid: Union[Unset, UUID] = UNSET,
) -> list["SoftwareTarget"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        catalog_uuid (Union[Unset, UUID]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        gpu_arch (Union[Unset, str]):
        has_gpu (Union[Unset, bool]):
        o (Union[Unset, list[SoftwareTargetOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        package_uuid (Union[Unset, UUID]):
        path (Union[Unset, str]):
        target_name (Union[Unset, str]):
        target_subtype (Union[Unset, str]):
        target_type (Union[Unset, str]):
        version_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SoftwareTarget']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SoftwareTarget] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        catalog_uuid=catalog_uuid,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        gpu_arch=gpu_arch,
        has_gpu=has_gpu,
        o=o,
        offering_uuid=offering_uuid,
        package_uuid=package_uuid,
        path=path,
        target_name=target_name,
        target_subtype=target_subtype,
        target_type=target_type,
        version_uuid=version_uuid,
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
