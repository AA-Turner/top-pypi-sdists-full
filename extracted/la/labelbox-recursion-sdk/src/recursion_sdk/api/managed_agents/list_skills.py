from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_skill_list_response import ManagedAgentsSkillListResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    skill_group_id: UUID | Unset = UNSET,
    ungrouped: bool | Unset = UNSET,
    search: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_skill_group_id: str | Unset = UNSET
    if not isinstance(skill_group_id, Unset):
        json_skill_group_id = str(skill_group_id)
    params["skill_group_id"] = json_skill_group_id

    params["ungrouped"] = ungrouped

    params["search"] = search

    params["limit"] = limit

    params["page_token"] = page_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/skills",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSkillListResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    skill_group_id: UUID | Unset = UNSET,
    ungrouped: bool | Unset = UNSET,
    search: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse]:
    """ List skills

     Returns one page of the calling organization's skills, newest first, following next_page_token until
    it is absent to read the whole catalog. Soft-deleted skills are omitted. Instructions are not
    included: attach a skill to an agent and the model receives its description in every turn, and its
    instructions only when it activates the skill. Narrow the page with skill_group_id for one folder,
    ungrouped for the skills in no folder, or search for a substring of a name, title, or description,
    or for a complete skill id.

    Args:
        skill_group_id (UUID | Unset): Return only the skills filed under this group, which is how
            a console fills one folder. Answers 404 when the group is not there. Cannot be combined
            with ungrouped.
        ungrouped (bool | Unset): Return only the skills filed under no group. This is the catalog
            tree's root bucket, and the complement of skill_group_id rather than a client-side slice
            of the whole catalog.
        search (str | Unset): Return only skills whose name, display title, or description
            contains this term, case-insensitively. Matched as a literal substring, so % and _ carry
            no special meaning. A complete skill id also matches that skill. Combines with the group
            filters, and pages like any other query.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same filters and limit to read the next page; a token used with a different query is
            rejected rather than silently skipping rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse]
     """


    kwargs = _get_kwargs(
        skill_group_id=skill_group_id,
ungrouped=ungrouped,
search=search,
limit=limit,
page_token=page_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    skill_group_id: UUID | Unset = UNSET,
    ungrouped: bool | Unset = UNSET,
    search: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse | None:
    """ List skills

     Returns one page of the calling organization's skills, newest first, following next_page_token until
    it is absent to read the whole catalog. Soft-deleted skills are omitted. Instructions are not
    included: attach a skill to an agent and the model receives its description in every turn, and its
    instructions only when it activates the skill. Narrow the page with skill_group_id for one folder,
    ungrouped for the skills in no folder, or search for a substring of a name, title, or description,
    or for a complete skill id.

    Args:
        skill_group_id (UUID | Unset): Return only the skills filed under this group, which is how
            a console fills one folder. Answers 404 when the group is not there. Cannot be combined
            with ungrouped.
        ungrouped (bool | Unset): Return only the skills filed under no group. This is the catalog
            tree's root bucket, and the complement of skill_group_id rather than a client-side slice
            of the whole catalog.
        search (str | Unset): Return only skills whose name, display title, or description
            contains this term, case-insensitively. Matched as a literal substring, so % and _ carry
            no special meaning. A complete skill id also matches that skill. Combines with the group
            filters, and pages like any other query.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same filters and limit to read the next page; a token used with a different query is
            rejected rather than silently skipping rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse
     """


    return sync_detailed(
        client=client,
skill_group_id=skill_group_id,
ungrouped=ungrouped,
search=search,
limit=limit,
page_token=page_token,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    skill_group_id: UUID | Unset = UNSET,
    ungrouped: bool | Unset = UNSET,
    search: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse]:
    """ List skills

     Returns one page of the calling organization's skills, newest first, following next_page_token until
    it is absent to read the whole catalog. Soft-deleted skills are omitted. Instructions are not
    included: attach a skill to an agent and the model receives its description in every turn, and its
    instructions only when it activates the skill. Narrow the page with skill_group_id for one folder,
    ungrouped for the skills in no folder, or search for a substring of a name, title, or description,
    or for a complete skill id.

    Args:
        skill_group_id (UUID | Unset): Return only the skills filed under this group, which is how
            a console fills one folder. Answers 404 when the group is not there. Cannot be combined
            with ungrouped.
        ungrouped (bool | Unset): Return only the skills filed under no group. This is the catalog
            tree's root bucket, and the complement of skill_group_id rather than a client-side slice
            of the whole catalog.
        search (str | Unset): Return only skills whose name, display title, or description
            contains this term, case-insensitively. Matched as a literal substring, so % and _ carry
            no special meaning. A complete skill id also matches that skill. Combines with the group
            filters, and pages like any other query.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same filters and limit to read the next page; a token used with a different query is
            rejected rather than silently skipping rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse]
     """


    kwargs = _get_kwargs(
        skill_group_id=skill_group_id,
ungrouped=ungrouped,
search=search,
limit=limit,
page_token=page_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    skill_group_id: UUID | Unset = UNSET,
    ungrouped: bool | Unset = UNSET,
    search: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse | None:
    """ List skills

     Returns one page of the calling organization's skills, newest first, following next_page_token until
    it is absent to read the whole catalog. Soft-deleted skills are omitted. Instructions are not
    included: attach a skill to an agent and the model receives its description in every turn, and its
    instructions only when it activates the skill. Narrow the page with skill_group_id for one folder,
    ungrouped for the skills in no folder, or search for a substring of a name, title, or description,
    or for a complete skill id.

    Args:
        skill_group_id (UUID | Unset): Return only the skills filed under this group, which is how
            a console fills one folder. Answers 404 when the group is not there. Cannot be combined
            with ungrouped.
        ungrouped (bool | Unset): Return only the skills filed under no group. This is the catalog
            tree's root bucket, and the complement of skill_group_id rather than a client-side slice
            of the whole catalog.
        search (str | Unset): Return only skills whose name, display title, or description
            contains this term, case-insensitively. Matched as a literal substring, so % and _ carry
            no special meaning. A complete skill id also matches that skill. Combines with the group
            filters, and pages like any other query.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same filters and limit to read the next page; a token used with a different query is
            rejected rather than silently skipping rows.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSkillListResponse
     """


    return (await asyncio_detailed(
        client=client,
skill_group_id=skill_group_id,
ungrouped=ungrouped,
search=search,
limit=limit,
page_token=page_token,

    )).parsed
