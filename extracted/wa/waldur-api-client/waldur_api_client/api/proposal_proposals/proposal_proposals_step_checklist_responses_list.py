from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.proposal_o_enum import ProposalOEnum
from ...models.proposal_states import ProposalStates
from ...models.step_checklist_response_group import StepChecklistResponseGroup
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
    step: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    json_created_by_uuid: Union[Unset, str] = UNSET
    if not isinstance(created_by_uuid, Unset):
        json_created_by_uuid = str(created_by_uuid)
    params["created_by_uuid"] = json_created_by_uuid

    params["my_proposals"] = my_proposals

    params["name"] = name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_organization_uuid: Union[Unset, str] = UNSET
    if not isinstance(organization_uuid, Unset):
        json_organization_uuid = str(organization_uuid)
    params["organization_uuid"] = json_organization_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_round_: Union[Unset, str] = UNSET
    if not isinstance(round_, Unset):
        json_round_ = str(round_)
    params["round"] = json_round_

    json_round_uuid: Union[Unset, str] = UNSET
    if not isinstance(round_uuid, Unset):
        json_round_uuid = str(round_uuid)
    params["round_uuid"] = json_round_uuid

    params["slug"] = slug

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["step"] = step

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/proposal-proposals/{uuid}/step-checklist-responses/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, list["StepChecklistResponseGroup"]]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = StepChecklistResponseGroup.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = response.json()
        return response_400
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, list["StepChecklistResponseGroup"]]]:
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
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
    step: str,
) -> Response[Union[Any, list["StepChecklistResponseGroup"]]]:
    """List a workflow step's checklist answers grouped by reviewer, for the threaded technical-assessment
    view. Each technical reviewer (offering manager) answers the same checklist; this returns every
    reviewer's decision and comment.

    Args:
        uuid (UUID):
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[ProposalStates]]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['StepChecklistResponseGroup']]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        round_=round_,
        round_uuid=round_uuid,
        slug=slug,
        state=state,
        step=step,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
    step: str,
) -> Union[Any, list["StepChecklistResponseGroup"]]:
    """List a workflow step's checklist answers grouped by reviewer, for the threaded technical-assessment
    view. Each technical reviewer (offering manager) answers the same checklist; this returns every
    reviewer's decision and comment.

    Args:
        uuid (UUID):
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[ProposalStates]]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['StepChecklistResponseGroup']]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        round_=round_,
        round_uuid=round_uuid,
        slug=slug,
        state=state,
        step=step,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
    step: str,
) -> Response[Union[Any, list["StepChecklistResponseGroup"]]]:
    """List a workflow step's checklist answers grouped by reviewer, for the threaded technical-assessment
    view. Each technical reviewer (offering manager) answers the same checklist; this returns every
    reviewer's decision and comment.

    Args:
        uuid (UUID):
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[ProposalStates]]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['StepChecklistResponseGroup']]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        round_=round_,
        round_uuid=round_uuid,
        slug=slug,
        state=state,
        step=step,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
    step: str,
) -> Union[Any, list["StepChecklistResponseGroup"]]:
    """List a workflow step's checklist answers grouped by reviewer, for the threaded technical-assessment
    view. Each technical reviewer (offering manager) answers the same checklist; this returns every
    reviewer's decision and comment.

    Args:
        uuid (UUID):
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[ProposalStates]]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['StepChecklistResponseGroup']]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            call_uuid=call_uuid,
            created_by_uuid=created_by_uuid,
            my_proposals=my_proposals,
            name=name,
            o=o,
            organization_uuid=organization_uuid,
            page=page,
            page_size=page_size,
            round_=round_,
            round_uuid=round_uuid,
            slug=slug,
            state=state,
            step=step,
        )
    ).parsed
