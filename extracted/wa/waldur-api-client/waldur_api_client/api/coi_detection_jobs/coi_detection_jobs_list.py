from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.coi_detection_job import COIDetectionJob
from ...models.coi_detection_job_job_type_enum import COIDetectionJobJobTypeEnum
from ...models.coi_detection_job_o_enum import COIDetectionJobOEnum
from ...models.coi_detection_job_state_enum import COIDetectionJobStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    call_uuid: Union[Unset, UUID] = UNSET,
    job_type: Union[Unset, COIDetectionJobJobTypeEnum] = UNSET,
    o: Union[Unset, list[COIDetectionJobOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[COIDetectionJobStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    json_job_type: Union[Unset, str] = UNSET
    if not isinstance(job_type, Unset):
        json_job_type = job_type.value

    params["job_type"] = json_job_type

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/coi-detection-jobs/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["COIDetectionJob"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = COIDetectionJob.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["COIDetectionJob"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    job_type: Union[Unset, COIDetectionJobJobTypeEnum] = UNSET,
    o: Union[Unset, list[COIDetectionJobOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[COIDetectionJobStateEnum]] = UNSET,
) -> Response[list["COIDetectionJob"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        job_type (Union[Unset, COIDetectionJobJobTypeEnum]):
        o (Union[Unset, list[COIDetectionJobOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[COIDetectionJobStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['COIDetectionJob']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        job_type=job_type,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    job_type: Union[Unset, COIDetectionJobJobTypeEnum] = UNSET,
    o: Union[Unset, list[COIDetectionJobOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[COIDetectionJobStateEnum]] = UNSET,
) -> list["COIDetectionJob"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        job_type (Union[Unset, COIDetectionJobJobTypeEnum]):
        o (Union[Unset, list[COIDetectionJobOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[COIDetectionJobStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['COIDetectionJob']
    """

    return sync_detailed(
        client=client,
        call_uuid=call_uuid,
        job_type=job_type,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    job_type: Union[Unset, COIDetectionJobJobTypeEnum] = UNSET,
    o: Union[Unset, list[COIDetectionJobOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[COIDetectionJobStateEnum]] = UNSET,
) -> Response[list["COIDetectionJob"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        job_type (Union[Unset, COIDetectionJobJobTypeEnum]):
        o (Union[Unset, list[COIDetectionJobOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[COIDetectionJobStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['COIDetectionJob']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        job_type=job_type,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    job_type: Union[Unset, COIDetectionJobJobTypeEnum] = UNSET,
    o: Union[Unset, list[COIDetectionJobOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[COIDetectionJobStateEnum]] = UNSET,
) -> list["COIDetectionJob"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        job_type (Union[Unset, COIDetectionJobJobTypeEnum]):
        o (Union[Unset, list[COIDetectionJobOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[COIDetectionJobStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['COIDetectionJob']
    """

    return (
        await asyncio_detailed(
            client=client,
            call_uuid=call_uuid,
            job_type=job_type,
            o=o,
            page=page,
            page_size=page_size,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    job_type: Union[Unset, COIDetectionJobJobTypeEnum] = UNSET,
    o: Union[Unset, list[COIDetectionJobOEnum]] = UNSET,
    state: Union[Unset, list[COIDetectionJobStateEnum]] = UNSET,
) -> list["COIDetectionJob"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        job_type (Union[Unset, COIDetectionJobJobTypeEnum]):
        o (Union[Unset, list[COIDetectionJobOEnum]]):
        state (Union[Unset, list[COIDetectionJobStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['COIDetectionJob']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[COIDetectionJob] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        job_type=job_type,
        o=o,
        state=state,
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
    call_uuid: Union[Unset, UUID] = UNSET,
    job_type: Union[Unset, COIDetectionJobJobTypeEnum] = UNSET,
    o: Union[Unset, list[COIDetectionJobOEnum]] = UNSET,
    state: Union[Unset, list[COIDetectionJobStateEnum]] = UNSET,
) -> list["COIDetectionJob"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        job_type (Union[Unset, COIDetectionJobJobTypeEnum]):
        o (Union[Unset, list[COIDetectionJobOEnum]]):
        state (Union[Unset, list[COIDetectionJobStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['COIDetectionJob']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[COIDetectionJob] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        job_type=job_type,
        o=o,
        state=state,
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
