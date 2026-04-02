from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.proposal_review_o_enum import ProposalReviewOEnum
from ...models.remote_project_update_request_state_enum import RemoteProjectUpdateRequestStateEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_by: Union[Unset, str] = UNSET
    if not isinstance(created_by, Unset):
        json_created_by = str(created_by)
    params["created_by"] = json_created_by

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_invitation: Union[Unset, str] = UNSET
    if not isinstance(invitation, Unset):
        json_invitation = str(invitation)
    params["invitation"] = json_invitation

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["scope"] = scope

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/user-permission-requests/",
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
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> Response[int]:
    """List permission requests

     Get number of items in the collection matching the request parameters.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        page=page,
        page_size=page_size,
        scope=scope,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> int:
    """List permission requests

     Get number of items in the collection matching the request parameters.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        page=page,
        page_size=page_size,
        scope=scope,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> Response[int]:
    """List permission requests

     Get number of items in the collection matching the request parameters.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        page=page,
        page_size=page_size,
        scope=scope,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> int:
    """List permission requests

     Get number of items in the collection matching the request parameters.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            created_by=created_by,
            customer_uuid=customer_uuid,
            invitation=invitation,
            o=o,
            page=page,
            page_size=page_size,
            scope=scope,
            state=state,
        )
    ).parsed
