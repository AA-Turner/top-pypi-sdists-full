from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checklist_completion import ChecklistCompletion
from ...models.checklist_response_checklist_type_enum import ChecklistResponseChecklistTypeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    checklist_type: Union[Unset, ChecklistResponseChecklistTypeEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_checklist_type: Union[Unset, str] = UNSET
    if not isinstance(checklist_type, Unset):
        json_checklist_type = checklist_type.value

    params["checklist_type"] = json_checklist_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/onboarding-verifications/{uuid}/completion_status/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ChecklistCompletion:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ChecklistCompletion.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ChecklistCompletion]:
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
    checklist_type: Union[Unset, ChecklistResponseChecklistTypeEnum] = UNSET,
) -> Response[ChecklistCompletion]:
    """Get checklist completion status. Supports both customer and intent checklists via checklist_type
    parameter.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChecklistCompletion]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        checklist_type=checklist_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistResponseChecklistTypeEnum] = UNSET,
) -> ChecklistCompletion:
    """Get checklist completion status. Supports both customer and intent checklists via checklist_type
    parameter.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChecklistCompletion
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        checklist_type=checklist_type,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistResponseChecklistTypeEnum] = UNSET,
) -> Response[ChecklistCompletion]:
    """Get checklist completion status. Supports both customer and intent checklists via checklist_type
    parameter.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChecklistCompletion]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        checklist_type=checklist_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistResponseChecklistTypeEnum] = UNSET,
) -> ChecklistCompletion:
    """Get checklist completion status. Supports both customer and intent checklists via checklist_type
    parameter.

    Args:
        uuid (UUID):
        checklist_type (Union[Unset, ChecklistResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChecklistCompletion
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            checklist_type=checklist_type,
        )
    ).parsed
