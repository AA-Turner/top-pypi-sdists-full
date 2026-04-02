from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.remote_project_update_request_state_enum import RemoteProjectUpdateRequestStateEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    identifier: Union[Unset, str] = UNSET,
    local_identifier: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_template: Union[Unset, str] = UNSET,
    project_template_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["identifier"] = identifier

    params["local_identifier"] = local_identifier

    params["page"] = page

    params["page_size"] = page_size

    params["project"] = project

    params["project_template"] = project_template

    json_project_template_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_template_uuid, Unset):
        json_project_template_uuid = str(project_template_uuid)
    params["project_template_uuid"] = json_project_template_uuid

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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/openportal-managed-projects/",
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
    identifier: Union[Unset, str] = UNSET,
    local_identifier: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_template: Union[Unset, str] = UNSET,
    project_template_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        identifier (Union[Unset, str]):
        local_identifier (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_template (Union[Unset, str]):
        project_template_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        local_identifier=local_identifier,
        page=page,
        page_size=page_size,
        project=project,
        project_template=project_template,
        project_template_uuid=project_template_uuid,
        project_uuid=project_uuid,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, str] = UNSET,
    local_identifier: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_template: Union[Unset, str] = UNSET,
    project_template_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        identifier (Union[Unset, str]):
        local_identifier (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_template (Union[Unset, str]):
        project_template_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        identifier=identifier,
        local_identifier=local_identifier,
        page=page,
        page_size=page_size,
        project=project,
        project_template=project_template,
        project_template_uuid=project_template_uuid,
        project_uuid=project_uuid,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, str] = UNSET,
    local_identifier: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_template: Union[Unset, str] = UNSET,
    project_template_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        identifier (Union[Unset, str]):
        local_identifier (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_template (Union[Unset, str]):
        project_template_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        local_identifier=local_identifier,
        page=page,
        page_size=page_size,
        project=project,
        project_template=project_template,
        project_template_uuid=project_template_uuid,
        project_uuid=project_uuid,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, str] = UNSET,
    local_identifier: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_template: Union[Unset, str] = UNSET,
    project_template_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        identifier (Union[Unset, str]):
        local_identifier (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_template (Union[Unset, str]):
        project_template_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
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
            identifier=identifier,
            local_identifier=local_identifier,
            page=page,
            page_size=page_size,
            project=project,
            project_template=project_template,
            project_template_uuid=project_template_uuid,
            project_uuid=project_uuid,
            state=state,
        )
    ).parsed
