import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.course_account_o_enum import CourseAccountOEnum
from ...models.course_account_state_enum import CourseAccountStateEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    email: Union[Unset, str] = UNSET,
    o: Union[Unset, list[CourseAccountOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_end_date_after: Union[Unset, datetime.date] = UNSET,
    project_end_date_before: Union[Unset, datetime.date] = UNSET,
    project_start_date_after: Union[Unset, datetime.date] = UNSET,
    project_start_date_before: Union[Unset, datetime.date] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CourseAccountStateEnum]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["email"] = email

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_project_end_date_after: Union[Unset, str] = UNSET
    if not isinstance(project_end_date_after, Unset):
        json_project_end_date_after = project_end_date_after.isoformat()
    params["project_end_date_after"] = json_project_end_date_after

    json_project_end_date_before: Union[Unset, str] = UNSET
    if not isinstance(project_end_date_before, Unset):
        json_project_end_date_before = project_end_date_before.isoformat()
    params["project_end_date_before"] = json_project_end_date_before

    json_project_start_date_after: Union[Unset, str] = UNSET
    if not isinstance(project_start_date_after, Unset):
        json_project_start_date_after = project_start_date_after.isoformat()
    params["project_start_date_after"] = json_project_start_date_after

    json_project_start_date_before: Union[Unset, str] = UNSET
    if not isinstance(project_start_date_before, Unset):
        json_project_start_date_before = project_start_date_before.isoformat()
    params["project_start_date_before"] = json_project_start_date_before

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-course-accounts/",
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
    email: Union[Unset, str] = UNSET,
    o: Union[Unset, list[CourseAccountOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_end_date_after: Union[Unset, datetime.date] = UNSET,
    project_end_date_before: Union[Unset, datetime.date] = UNSET,
    project_start_date_after: Union[Unset, datetime.date] = UNSET,
    project_start_date_before: Union[Unset, datetime.date] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CourseAccountStateEnum]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List course accounts

     Get number of items in the collection matching the request parameters.

    Args:
        email (Union[Unset, str]):
        o (Union[Unset, list[CourseAccountOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_end_date_after (Union[Unset, datetime.date]):
        project_end_date_before (Union[Unset, datetime.date]):
        project_start_date_after (Union[Unset, datetime.date]):
        project_start_date_before (Union[Unset, datetime.date]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CourseAccountStateEnum]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        email=email,
        o=o,
        page=page,
        page_size=page_size,
        project_end_date_after=project_end_date_after,
        project_end_date_before=project_end_date_before,
        project_start_date_after=project_start_date_after,
        project_start_date_before=project_start_date_before,
        project_uuid=project_uuid,
        state=state,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    o: Union[Unset, list[CourseAccountOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_end_date_after: Union[Unset, datetime.date] = UNSET,
    project_end_date_before: Union[Unset, datetime.date] = UNSET,
    project_start_date_after: Union[Unset, datetime.date] = UNSET,
    project_start_date_before: Union[Unset, datetime.date] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CourseAccountStateEnum]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """List course accounts

     Get number of items in the collection matching the request parameters.

    Args:
        email (Union[Unset, str]):
        o (Union[Unset, list[CourseAccountOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_end_date_after (Union[Unset, datetime.date]):
        project_end_date_before (Union[Unset, datetime.date]):
        project_start_date_after (Union[Unset, datetime.date]):
        project_start_date_before (Union[Unset, datetime.date]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CourseAccountStateEnum]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        email=email,
        o=o,
        page=page,
        page_size=page_size,
        project_end_date_after=project_end_date_after,
        project_end_date_before=project_end_date_before,
        project_start_date_after=project_start_date_after,
        project_start_date_before=project_start_date_before,
        project_uuid=project_uuid,
        state=state,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    o: Union[Unset, list[CourseAccountOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_end_date_after: Union[Unset, datetime.date] = UNSET,
    project_end_date_before: Union[Unset, datetime.date] = UNSET,
    project_start_date_after: Union[Unset, datetime.date] = UNSET,
    project_start_date_before: Union[Unset, datetime.date] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CourseAccountStateEnum]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List course accounts

     Get number of items in the collection matching the request parameters.

    Args:
        email (Union[Unset, str]):
        o (Union[Unset, list[CourseAccountOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_end_date_after (Union[Unset, datetime.date]):
        project_end_date_before (Union[Unset, datetime.date]):
        project_start_date_after (Union[Unset, datetime.date]):
        project_start_date_before (Union[Unset, datetime.date]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CourseAccountStateEnum]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        email=email,
        o=o,
        page=page,
        page_size=page_size,
        project_end_date_after=project_end_date_after,
        project_end_date_before=project_end_date_before,
        project_start_date_after=project_start_date_after,
        project_start_date_before=project_start_date_before,
        project_uuid=project_uuid,
        state=state,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    o: Union[Unset, list[CourseAccountOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_end_date_after: Union[Unset, datetime.date] = UNSET,
    project_end_date_before: Union[Unset, datetime.date] = UNSET,
    project_start_date_after: Union[Unset, datetime.date] = UNSET,
    project_start_date_before: Union[Unset, datetime.date] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CourseAccountStateEnum]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """List course accounts

     Get number of items in the collection matching the request parameters.

    Args:
        email (Union[Unset, str]):
        o (Union[Unset, list[CourseAccountOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_end_date_after (Union[Unset, datetime.date]):
        project_end_date_before (Union[Unset, datetime.date]):
        project_start_date_after (Union[Unset, datetime.date]):
        project_start_date_before (Union[Unset, datetime.date]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CourseAccountStateEnum]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            email=email,
            o=o,
            page=page,
            page_size=page_size,
            project_end_date_after=project_end_date_after,
            project_end_date_before=project_end_date_before,
            project_start_date_after=project_start_date_after,
            project_start_date_before=project_start_date_before,
            project_uuid=project_uuid,
            state=state,
            username=username,
        )
    ).parsed
