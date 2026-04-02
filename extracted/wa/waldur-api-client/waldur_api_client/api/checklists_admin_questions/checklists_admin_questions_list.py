from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checklist_type_enum import ChecklistTypeEnum
from ...models.question_admin import QuestionAdmin
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/checklists-admin-questions/",
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
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["QuestionAdmin"]]:
    """
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
        Response[list['QuestionAdmin']]
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
) -> list["QuestionAdmin"]:
    """
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
        list['QuestionAdmin']
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
) -> Response[list["QuestionAdmin"]]:
    """
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
        Response[list['QuestionAdmin']]
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
) -> list["QuestionAdmin"]:
    """
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
        list['QuestionAdmin']
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


def sync_all(
    *,
    client: AuthenticatedClient,
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
) -> list["QuestionAdmin"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_uuid (Union[Unset, UUID]):
        has_onboarding_mapping (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['QuestionAdmin']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[QuestionAdmin] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        checklist_type=checklist_type,
        checklist_uuid=checklist_uuid,
        has_onboarding_mapping=has_onboarding_mapping,
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
    checklist_type: Union[Unset, ChecklistTypeEnum] = UNSET,
    checklist_uuid: Union[Unset, UUID] = UNSET,
    has_onboarding_mapping: Union[Unset, bool] = UNSET,
) -> list["QuestionAdmin"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        checklist_type (Union[Unset, ChecklistTypeEnum]):
        checklist_uuid (Union[Unset, UUID]):
        has_onboarding_mapping (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['QuestionAdmin']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[QuestionAdmin] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        checklist_type=checklist_type,
        checklist_uuid=checklist_uuid,
        has_onboarding_mapping=has_onboarding_mapping,
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
