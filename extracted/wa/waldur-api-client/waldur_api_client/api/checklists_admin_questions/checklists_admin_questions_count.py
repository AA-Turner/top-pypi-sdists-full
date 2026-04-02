from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checklist_type_enum import ChecklistTypeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_checklist_type: Union[Unset, str] = UNSET
    if not isinstance(checklist_type, Unset):
        json_checklist_type = checklist_type.value

    params["checklist_type"] = json_checklist_type

    json_checklist_uuid: Union[Unset, str] = UNSET
    if not isinstance(checklist_uuid, Unset):
        json_checklist_uuid = str(checklist_uuid)
    params["checklist_uuid"] = json_checklist_uuid

    params["has_onboarding_mapping"] = has_onboarding_mapping

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/checklists-admin-questions/",
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
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_uuid (Union[Unset, UUID]):
        has_onboarding_mapping (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        checklist_type=checklist_type,
        checklist_uuid=checklist_uuid,
        has_onboarding_mapping=has_onboarding_mapping,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_uuid (Union[Unset, UUID]):
        has_onboarding_mapping (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        checklist_type=checklist_type,
        checklist_uuid=checklist_uuid,
        has_onboarding_mapping=has_onboarding_mapping,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_uuid (Union[Unset, UUID]):
        has_onboarding_mapping (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        checklist_type=checklist_type,
        checklist_uuid=checklist_uuid,
        has_onboarding_mapping=has_onboarding_mapping,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_uuid (Union[Unset, UUID]):
        has_onboarding_mapping (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            checklist_type=checklist_type,
            checklist_uuid=checklist_uuid,
            has_onboarding_mapping=has_onboarding_mapping,
            page=page,
            page_size=page_size,
        )
    ).parsed
