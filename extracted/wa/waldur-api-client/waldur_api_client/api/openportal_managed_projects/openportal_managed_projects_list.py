from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.managed_project import ManagedProject
from ...models.remote_project_update_request_state_enum import RemoteProjectUpdateRequestStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/openportal-managed-projects/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["ManagedProject"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ManagedProject.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ManagedProject"]]:
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
) -> Response[list["ManagedProject"]]:
    """List all managed projects

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
        Response[list['ManagedProject']]
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
) -> list["ManagedProject"]:
    """List all managed projects

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
        list['ManagedProject']
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
) -> Response[list["ManagedProject"]]:
    """List all managed projects

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
        Response[list['ManagedProject']]
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
) -> list["ManagedProject"]:
    """List all managed projects

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
        list['ManagedProject']
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


def sync_all(
    *,
    client: AuthenticatedClient,
    identifier: Union[Unset, str] = UNSET,
    local_identifier: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_template: Union[Unset, str] = UNSET,
    project_template_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> list["ManagedProject"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        identifier (Union[Unset, str]):
        local_identifier (Union[Unset, str]):
        project (Union[Unset, str]):
        project_template (Union[Unset, str]):
        project_template_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ManagedProject']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ManagedProject] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        identifier=identifier,
        local_identifier=local_identifier,
        project=project,
        project_template=project_template,
        project_template_uuid=project_template_uuid,
        project_uuid=project_uuid,
        state=state,
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
    identifier: Union[Unset, str] = UNSET,
    local_identifier: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_template: Union[Unset, str] = UNSET,
    project_template_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> list["ManagedProject"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        identifier (Union[Unset, str]):
        local_identifier (Union[Unset, str]):
        project (Union[Unset, str]):
        project_template (Union[Unset, str]):
        project_template_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ManagedProject']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ManagedProject] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        identifier=identifier,
        local_identifier=local_identifier,
        project=project,
        project_template=project_template,
        project_template_uuid=project_template_uuid,
        project_uuid=project_uuid,
        state=state,
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
