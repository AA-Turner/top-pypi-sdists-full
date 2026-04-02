from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checklist_type_enum import ChecklistTypeEnum
from ...models.question_admin import QuestionAdmin
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_type_in: Union[Unset, list[ChecklistTypeEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_checklist_type: Union[Unset, str] = UNSET
    if not isinstance(checklist_type, Unset):
        json_checklist_type = checklist_type.value

    params["checklist_type"] = json_checklist_type

    json_checklist_type_in: Union[Unset, list[str]] = UNSET
    if not isinstance(checklist_type_in, Unset):
        json_checklist_type_in = []
        for checklist_type_in_item_data in checklist_type_in:
            checklist_type_in_item = checklist_type_in_item_data.value
            json_checklist_type_in.append(checklist_type_in_item)

    params["checklist_type__in"] = json_checklist_type_in

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/checklists-admin/{uuid}/questions/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["QuestionAdmin"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = QuestionAdmin.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["QuestionAdmin"]]:
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
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_type_in: Union[Unset, list[ChecklistTypeEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["QuestionAdmin"]]:
    """Return checklist questions.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_type_in (Union[Unset, list[ChecklistTypeEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['QuestionAdmin']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        checklist_type=checklist_type,
        checklist_type_in=checklist_type_in,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_type_in: Union[Unset, list[ChecklistTypeEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["QuestionAdmin"]:
    """Return checklist questions.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_type_in (Union[Unset, list[ChecklistTypeEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['QuestionAdmin']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        checklist_type=checklist_type,
        checklist_type_in=checklist_type_in,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_type_in: Union[Unset, list[ChecklistTypeEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["QuestionAdmin"]]:
    """Return checklist questions.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_type_in (Union[Unset, list[ChecklistTypeEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['QuestionAdmin']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        checklist_type=checklist_type,
        checklist_type_in=checklist_type_in,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_type_in: Union[Unset, list[ChecklistTypeEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["QuestionAdmin"]:
    """Return checklist questions.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_type_in (Union[Unset, list[ChecklistTypeEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['QuestionAdmin']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            checklist_type=checklist_type,
            checklist_type_in=checklist_type_in,
            page=page,
            page_size=page_size,
        )
    ).parsed
