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
from ...models.managed_agents_skill_list_response import ManagedAgentsSkillListResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    skill_group_id: UUID,
    *,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["page_token"] = page_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/skill-groups/{skill_group_id}/skills".format(skill_group_id=quote(str(skill_group_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse | None:
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
        response_404 = ManagedAgentsApiError.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    skill_group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse]:
    """ List the skills in a group

     Returns one page of the live skills filed under the group, in the order a group attachment expands
    them at session start. That order matters: it decides which skill's description is dropped first if
    the disclosure budget is exceeded. Follow next_page_token to read the whole group, which is what an
    attachment resolves to.

    Args:
        skill_group_id (UUID): Skill group id (UUID) whose skills to list.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same limit to read the next page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse]
     """


    kwargs = _get_kwargs(
        skill_group_id=skill_group_id,
limit=limit,
page_token=page_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    skill_group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse | None:
    """ List the skills in a group

     Returns one page of the live skills filed under the group, in the order a group attachment expands
    them at session start. That order matters: it decides which skill's description is dropped first if
    the disclosure budget is exceeded. Follow next_page_token to read the whole group, which is what an
    attachment resolves to.

    Args:
        skill_group_id (UUID): Skill group id (UUID) whose skills to list.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same limit to read the next page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse
     """


    return sync_detailed(
        skill_group_id=skill_group_id,
client=client,
limit=limit,
page_token=page_token,

    ).parsed

async def asyncio_detailed(
    skill_group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse]:
    """ List the skills in a group

     Returns one page of the live skills filed under the group, in the order a group attachment expands
    them at session start. That order matters: it decides which skill's description is dropped first if
    the disclosure budget is exceeded. Follow next_page_token to read the whole group, which is what an
    attachment resolves to.

    Args:
        skill_group_id (UUID): Skill group id (UUID) whose skills to list.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same limit to read the next page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse]
     """


    kwargs = _get_kwargs(
        skill_group_id=skill_group_id,
limit=limit,
page_token=page_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    skill_group_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse | None:
    """ List the skills in a group

     Returns one page of the live skills filed under the group, in the order a group attachment expands
    them at session start. That order matters: it decides which skill's description is dropped first if
    the disclosure budget is exceeded. Follow next_page_token to read the whole group, which is what an
    attachment resolves to.

    Args:
        skill_group_id (UUID): Skill group id (UUID) whose skills to list.
        limit (int | Unset): How many skills to return. Defaults to 100, the maximum is 500.
        page_token (str | Unset): The next_page_token from a previous response. Pass it back with
            the same limit to read the next page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillListResponse
     """


    return (await asyncio_detailed(
        skill_group_id=skill_group_id,
client=client,
limit=limit,
page_token=page_token,

    )).parsed
