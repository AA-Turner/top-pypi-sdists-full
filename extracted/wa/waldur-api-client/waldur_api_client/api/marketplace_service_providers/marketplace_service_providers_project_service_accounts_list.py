from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_service_account import ProjectServiceAccount
from ...models.service_account_state import ServiceAccountState
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    service_provider_uuid: UUID,
    *,
    email: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ServiceAccountState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["email"] = email

    params["page"] = page

    params["page_size"] = page_size

    params["project"] = project

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
        "method": "get",
        "url": f"/api/marketplace-service-providers/{service_provider_uuid}/project_service_accounts/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ProjectServiceAccount"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectServiceAccount.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ProjectServiceAccount"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ServiceAccountState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["ProjectServiceAccount"]]:
    """List project service accounts for a service provider

     Returns a paginated list of project service accounts that have access to resources managed by the
    provider.

            This includes:
            - Projects with active resources of the service provider.
            - Service accounts with non-blank usernames.


    Args:
        service_provider_uuid (UUID):
        email (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ServiceAccountState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProjectServiceAccount']]
    """

    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        email=email,
        page=page,
        page_size=page_size,
        project=project,
        project_uuid=project_uuid,
        state=state,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ServiceAccountState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ProjectServiceAccount"]:
    """List project service accounts for a service provider

     Returns a paginated list of project service accounts that have access to resources managed by the
    provider.

            This includes:
            - Projects with active resources of the service provider.
            - Service accounts with non-blank usernames.


    Args:
        service_provider_uuid (UUID):
        email (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ServiceAccountState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProjectServiceAccount']
    """

    return sync_detailed(
        service_provider_uuid=service_provider_uuid,
        client=client,
        email=email,
        page=page,
        page_size=page_size,
        project=project,
        project_uuid=project_uuid,
        state=state,
        username=username,
    ).parsed


async def asyncio_detailed(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ServiceAccountState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["ProjectServiceAccount"]]:
    """List project service accounts for a service provider

     Returns a paginated list of project service accounts that have access to resources managed by the
    provider.

            This includes:
            - Projects with active resources of the service provider.
            - Service accounts with non-blank usernames.


    Args:
        service_provider_uuid (UUID):
        email (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ServiceAccountState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProjectServiceAccount']]
    """

    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        email=email,
        page=page,
        page_size=page_size,
        project=project,
        project_uuid=project_uuid,
        state=state,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ServiceAccountState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ProjectServiceAccount"]:
    """List project service accounts for a service provider

     Returns a paginated list of project service accounts that have access to resources managed by the
    provider.

            This includes:
            - Projects with active resources of the service provider.
            - Service accounts with non-blank usernames.


    Args:
        service_provider_uuid (UUID):
        email (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ServiceAccountState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProjectServiceAccount']
    """

    return (
        await asyncio_detailed(
            service_provider_uuid=service_provider_uuid,
            client=client,
            email=email,
            page=page,
            page_size=page_size,
            project=project,
            project_uuid=project_uuid,
            state=state,
            username=username,
        )
    ).parsed


def sync_all(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ServiceAccountState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ProjectServiceAccount"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        service_provider_uuid (UUID):
        email (Union[Unset, str]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ServiceAccountState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProjectServiceAccount']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ProjectServiceAccount] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        email=email,
        project=project,
        project_uuid=project_uuid,
        state=state,
        username=username,
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
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ServiceAccountState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ProjectServiceAccount"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        service_provider_uuid (UUID):
        email (Union[Unset, str]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ServiceAccountState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProjectServiceAccount']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ProjectServiceAccount] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        email=email,
        project=project,
        project_uuid=project_uuid,
        state=state,
        username=username,
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
