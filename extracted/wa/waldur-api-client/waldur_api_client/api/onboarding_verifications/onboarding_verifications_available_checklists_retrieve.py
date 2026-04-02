from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.available_checklists_response import AvailableChecklistsResponse
from ...models.available_checklists_response_checklist_type_enum import AvailableChecklistsResponseChecklistTypeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    checklist_type: Union[Unset, AvailableChecklistsResponseChecklistTypeEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_checklist_type: Union[Unset, str] = UNSET
    if not isinstance(checklist_type, Unset):
        json_checklist_type = checklist_type.value

    params["checklist_type"] = json_checklist_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/onboarding-verifications/available_checklists/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> AvailableChecklistsResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AvailableChecklistsResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AvailableChecklistsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, AvailableChecklistsResponseChecklistTypeEnum] = UNSET,
) -> Response[AvailableChecklistsResponse]:
    """Get available onboarding checklists (customer and intent) for preview. This endpoint allows users to
    see checklist questions before creating a verification. Supports checklist_type parameter to filter
    by customer or intent checklists. Includes questions with onboarding metadata (field mappings).

    Args:
        checklist_type (Union[Unset, AvailableChecklistsResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AvailableChecklistsResponse]
    """

    kwargs = _get_kwargs(
        checklist_type=checklist_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, AvailableChecklistsResponseChecklistTypeEnum] = UNSET,
) -> AvailableChecklistsResponse:
    """Get available onboarding checklists (customer and intent) for preview. This endpoint allows users to
    see checklist questions before creating a verification. Supports checklist_type parameter to filter
    by customer or intent checklists. Includes questions with onboarding metadata (field mappings).

    Args:
        checklist_type (Union[Unset, AvailableChecklistsResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AvailableChecklistsResponse
    """

    return sync_detailed(
        client=client,
        checklist_type=checklist_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, AvailableChecklistsResponseChecklistTypeEnum] = UNSET,
) -> Response[AvailableChecklistsResponse]:
    """Get available onboarding checklists (customer and intent) for preview. This endpoint allows users to
    see checklist questions before creating a verification. Supports checklist_type parameter to filter
    by customer or intent checklists. Includes questions with onboarding metadata (field mappings).

    Args:
        checklist_type (Union[Unset, AvailableChecklistsResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AvailableChecklistsResponse]
    """

    kwargs = _get_kwargs(
        checklist_type=checklist_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, AvailableChecklistsResponseChecklistTypeEnum] = UNSET,
) -> AvailableChecklistsResponse:
    """Get available onboarding checklists (customer and intent) for preview. This endpoint allows users to
    see checklist questions before creating a verification. Supports checklist_type parameter to filter
    by customer or intent checklists. Includes questions with onboarding metadata (field mappings).

    Args:
        checklist_type (Union[Unset, AvailableChecklistsResponseChecklistTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AvailableChecklistsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            checklist_type=checklist_type,
        )
    ).parsed
