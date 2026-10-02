from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.coi_severity_level import COISeverityLevel
from ...models.coi_type_enum import CoiTypeEnum
from ...models.conflict_of_interest import ConflictOfInterest
from ...models.conflict_of_interest_o_enum import ConflictOfInterestOEnum
from ...models.conflict_of_interest_status_enum import ConflictOfInterestStatusEnum
from ...models.detection_method_enum import DetectionMethodEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    call_uuid: Union[Unset, UUID] = UNSET,
    coi_type: Union[Unset, list[CoiTypeEnum]] = UNSET,
    detection_method: Union[Unset, list[DetectionMethodEnum]] = UNSET,
    o: Union[Unset, list[ConflictOfInterestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_name: Union[Unset, str] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    severity: Union[Unset, COISeverityLevel] = UNSET,
    status: Union[Unset, list[ConflictOfInterestStatusEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    json_coi_type: Union[Unset, list[str]] = UNSET
    if not isinstance(coi_type, Unset):
        json_coi_type = []
        for coi_type_item_data in coi_type:
            coi_type_item = coi_type_item_data.value
            json_coi_type.append(coi_type_item)

    params["coi_type"] = json_coi_type

    json_detection_method: Union[Unset, list[str]] = UNSET
    if not isinstance(detection_method, Unset):
        json_detection_method = []
        for detection_method_item_data in detection_method:
            detection_method_item = detection_method_item_data.value
            json_detection_method.append(detection_method_item)

    params["detection_method"] = json_detection_method

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_proposal_uuid: Union[Unset, str] = UNSET
    if not isinstance(proposal_uuid, Unset):
        json_proposal_uuid = str(proposal_uuid)
    params["proposal_uuid"] = json_proposal_uuid

    params["reviewer_name"] = reviewer_name

    json_reviewer_uuid: Union[Unset, str] = UNSET
    if not isinstance(reviewer_uuid, Unset):
        json_reviewer_uuid = str(reviewer_uuid)
    params["reviewer_uuid"] = json_reviewer_uuid

    json_round_uuid: Union[Unset, str] = UNSET
    if not isinstance(round_uuid, Unset):
        json_round_uuid = str(round_uuid)
    params["round_uuid"] = json_round_uuid

    json_severity: Union[Unset, str] = UNSET
    if not isinstance(severity, Unset):
        json_severity = severity.value

    params["severity"] = json_severity

    json_status: Union[Unset, list[str]] = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/conflicts-of-interest/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ConflictOfInterest"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ConflictOfInterest.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ConflictOfInterest"]]:
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
    coi_type: Union[Unset, list[CoiTypeEnum]] = UNSET,
    detection_method: Union[Unset, list[DetectionMethodEnum]] = UNSET,
    o: Union[Unset, list[ConflictOfInterestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_name: Union[Unset, str] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    severity: Union[Unset, COISeverityLevel] = UNSET,
    status: Union[Unset, list[ConflictOfInterestStatusEnum]] = UNSET,
) -> Response[list["ConflictOfInterest"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        coi_type (Union[Unset, list[CoiTypeEnum]]):
        detection_method (Union[Unset, list[DetectionMethodEnum]]):
        o (Union[Unset, list[ConflictOfInterestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_name (Union[Unset, str]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        severity (Union[Unset, COISeverityLevel]):
        status (Union[Unset, list[ConflictOfInterestStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ConflictOfInterest']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        coi_type=coi_type,
        detection_method=detection_method,
        o=o,
        page=page,
        page_size=page_size,
        proposal_uuid=proposal_uuid,
        reviewer_name=reviewer_name,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
        severity=severity,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    coi_type: Union[Unset, list[CoiTypeEnum]] = UNSET,
    detection_method: Union[Unset, list[DetectionMethodEnum]] = UNSET,
    o: Union[Unset, list[ConflictOfInterestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_name: Union[Unset, str] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    severity: Union[Unset, COISeverityLevel] = UNSET,
    status: Union[Unset, list[ConflictOfInterestStatusEnum]] = UNSET,
) -> list["ConflictOfInterest"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        coi_type (Union[Unset, list[CoiTypeEnum]]):
        detection_method (Union[Unset, list[DetectionMethodEnum]]):
        o (Union[Unset, list[ConflictOfInterestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_name (Union[Unset, str]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        severity (Union[Unset, COISeverityLevel]):
        status (Union[Unset, list[ConflictOfInterestStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']
    """

    return sync_detailed(
        client=client,
        call_uuid=call_uuid,
        coi_type=coi_type,
        detection_method=detection_method,
        o=o,
        page=page,
        page_size=page_size,
        proposal_uuid=proposal_uuid,
        reviewer_name=reviewer_name,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
        severity=severity,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    coi_type: Union[Unset, list[CoiTypeEnum]] = UNSET,
    detection_method: Union[Unset, list[DetectionMethodEnum]] = UNSET,
    o: Union[Unset, list[ConflictOfInterestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_name: Union[Unset, str] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    severity: Union[Unset, COISeverityLevel] = UNSET,
    status: Union[Unset, list[ConflictOfInterestStatusEnum]] = UNSET,
) -> Response[list["ConflictOfInterest"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        coi_type (Union[Unset, list[CoiTypeEnum]]):
        detection_method (Union[Unset, list[DetectionMethodEnum]]):
        o (Union[Unset, list[ConflictOfInterestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_name (Union[Unset, str]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        severity (Union[Unset, COISeverityLevel]):
        status (Union[Unset, list[ConflictOfInterestStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ConflictOfInterest']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        coi_type=coi_type,
        detection_method=detection_method,
        o=o,
        page=page,
        page_size=page_size,
        proposal_uuid=proposal_uuid,
        reviewer_name=reviewer_name,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
        severity=severity,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    coi_type: Union[Unset, list[CoiTypeEnum]] = UNSET,
    detection_method: Union[Unset, list[DetectionMethodEnum]] = UNSET,
    o: Union[Unset, list[ConflictOfInterestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_name: Union[Unset, str] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    severity: Union[Unset, COISeverityLevel] = UNSET,
    status: Union[Unset, list[ConflictOfInterestStatusEnum]] = UNSET,
) -> list["ConflictOfInterest"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        coi_type (Union[Unset, list[CoiTypeEnum]]):
        detection_method (Union[Unset, list[DetectionMethodEnum]]):
        o (Union[Unset, list[ConflictOfInterestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_name (Union[Unset, str]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        severity (Union[Unset, COISeverityLevel]):
        status (Union[Unset, list[ConflictOfInterestStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']
    """

    return (
        await asyncio_detailed(
            client=client,
            call_uuid=call_uuid,
            coi_type=coi_type,
            detection_method=detection_method,
            o=o,
            page=page,
            page_size=page_size,
            proposal_uuid=proposal_uuid,
            reviewer_name=reviewer_name,
            reviewer_uuid=reviewer_uuid,
            round_uuid=round_uuid,
            severity=severity,
            status=status,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    coi_type: Union[Unset, list[CoiTypeEnum]] = UNSET,
    detection_method: Union[Unset, list[DetectionMethodEnum]] = UNSET,
    o: Union[Unset, list[ConflictOfInterestOEnum]] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_name: Union[Unset, str] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    severity: Union[Unset, COISeverityLevel] = UNSET,
    status: Union[Unset, list[ConflictOfInterestStatusEnum]] = UNSET,
) -> list["ConflictOfInterest"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        coi_type (Union[Unset, list[CoiTypeEnum]]):
        detection_method (Union[Unset, list[DetectionMethodEnum]]):
        o (Union[Unset, list[ConflictOfInterestOEnum]]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_name (Union[Unset, str]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        severity (Union[Unset, COISeverityLevel]):
        status (Union[Unset, list[ConflictOfInterestStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ConflictOfInterest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        coi_type=coi_type,
        detection_method=detection_method,
        o=o,
        proposal_uuid=proposal_uuid,
        reviewer_name=reviewer_name,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
        severity=severity,
        status=status,
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
    coi_type: Union[Unset, list[CoiTypeEnum]] = UNSET,
    detection_method: Union[Unset, list[DetectionMethodEnum]] = UNSET,
    o: Union[Unset, list[ConflictOfInterestOEnum]] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_name: Union[Unset, str] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    severity: Union[Unset, COISeverityLevel] = UNSET,
    status: Union[Unset, list[ConflictOfInterestStatusEnum]] = UNSET,
) -> list["ConflictOfInterest"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        coi_type (Union[Unset, list[CoiTypeEnum]]):
        detection_method (Union[Unset, list[DetectionMethodEnum]]):
        o (Union[Unset, list[ConflictOfInterestOEnum]]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_name (Union[Unset, str]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        severity (Union[Unset, COISeverityLevel]):
        status (Union[Unset, list[ConflictOfInterestStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ConflictOfInterest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        coi_type=coi_type,
        detection_method=detection_method,
        o=o,
        proposal_uuid=proposal_uuid,
        reviewer_name=reviewer_name,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
        severity=severity,
        status=status,
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
