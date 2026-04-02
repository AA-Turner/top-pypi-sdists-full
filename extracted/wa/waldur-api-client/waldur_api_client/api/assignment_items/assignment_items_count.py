from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assignment_item_o_enum import AssignmentItemOEnum
from ...models.assignment_item_status import AssignmentItemStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    batch_uuid: Union[Unset, UUID] = UNSET,
    call_uuid: Union[Unset, UUID] = UNSET,
    has_coi: Union[Unset, bool] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[AssignmentItemOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[AssignmentItemStatus]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_batch_uuid: Union[Unset, str] = UNSET
    if not isinstance(batch_uuid, Unset):
        json_batch_uuid = str(batch_uuid)
    params["batch_uuid"] = json_batch_uuid

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    params["has_coi"] = has_coi

    params["min_affinity_score"] = min_affinity_score

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

    json_reviewer_uuid: Union[Unset, str] = UNSET
    if not isinstance(reviewer_uuid, Unset):
        json_reviewer_uuid = str(reviewer_uuid)
    params["reviewer_uuid"] = json_reviewer_uuid

    json_status: Union[Unset, list[str]] = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/assignment-items/",
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
    batch_uuid: Union[Unset, UUID] = UNSET,
    call_uuid: Union[Unset, UUID] = UNSET,
    has_coi: Union[Unset, bool] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[AssignmentItemOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[AssignmentItemStatus]] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        batch_uuid (Union[Unset, UUID]):
        call_uuid (Union[Unset, UUID]):
        has_coi (Union[Unset, bool]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[AssignmentItemOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[AssignmentItemStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        batch_uuid=batch_uuid,
        call_uuid=call_uuid,
        has_coi=has_coi,
        min_affinity_score=min_affinity_score,
        o=o,
        page=page,
        page_size=page_size,
        proposal_uuid=proposal_uuid,
        reviewer_uuid=reviewer_uuid,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    batch_uuid: Union[Unset, UUID] = UNSET,
    call_uuid: Union[Unset, UUID] = UNSET,
    has_coi: Union[Unset, bool] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[AssignmentItemOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[AssignmentItemStatus]] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        batch_uuid (Union[Unset, UUID]):
        call_uuid (Union[Unset, UUID]):
        has_coi (Union[Unset, bool]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[AssignmentItemOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[AssignmentItemStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        batch_uuid=batch_uuid,
        call_uuid=call_uuid,
        has_coi=has_coi,
        min_affinity_score=min_affinity_score,
        o=o,
        page=page,
        page_size=page_size,
        proposal_uuid=proposal_uuid,
        reviewer_uuid=reviewer_uuid,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    batch_uuid: Union[Unset, UUID] = UNSET,
    call_uuid: Union[Unset, UUID] = UNSET,
    has_coi: Union[Unset, bool] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[AssignmentItemOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[AssignmentItemStatus]] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        batch_uuid (Union[Unset, UUID]):
        call_uuid (Union[Unset, UUID]):
        has_coi (Union[Unset, bool]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[AssignmentItemOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[AssignmentItemStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        batch_uuid=batch_uuid,
        call_uuid=call_uuid,
        has_coi=has_coi,
        min_affinity_score=min_affinity_score,
        o=o,
        page=page,
        page_size=page_size,
        proposal_uuid=proposal_uuid,
        reviewer_uuid=reviewer_uuid,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    batch_uuid: Union[Unset, UUID] = UNSET,
    call_uuid: Union[Unset, UUID] = UNSET,
    has_coi: Union[Unset, bool] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[AssignmentItemOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[AssignmentItemStatus]] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        batch_uuid (Union[Unset, UUID]):
        call_uuid (Union[Unset, UUID]):
        has_coi (Union[Unset, bool]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[AssignmentItemOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        proposal_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[AssignmentItemStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            batch_uuid=batch_uuid,
            call_uuid=call_uuid,
            has_coi=has_coi,
            min_affinity_score=min_affinity_score,
            o=o,
            page=page,
            page_size=page_size,
            proposal_uuid=proposal_uuid,
            reviewer_uuid=reviewer_uuid,
            status=status,
        )
    ).parsed
