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
from ...models.managed_agents_skill_version import ManagedAgentsSkillVersion
from typing import cast
from uuid import UUID



def _get_kwargs(
    skill_id: UUID,
    skill_version_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/skills/{skill_id}/versions/{skill_version_id}".format(skill_id=quote(str(skill_id), safe=""),skill_version_id=quote(str(skill_version_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSkillVersion.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    skill_id: UUID,
    skill_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion]:
    """ Get one immutable skill version

     Returns one immutable skill version by id, including its full instructions. The version must belong
    to the skill in the path; a mismatch is a 404 rather than a cross-skill read.

    Args:
        skill_id (UUID): Skill id (UUID) the version belongs to.
        skill_version_id (UUID): Immutable skill version id (UUID), as listed by listSkillVersions
            or reported as a skill's latest_skill_version_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion]
     """


    kwargs = _get_kwargs(
        skill_id=skill_id,
skill_version_id=skill_version_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    skill_id: UUID,
    skill_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion | None:
    """ Get one immutable skill version

     Returns one immutable skill version by id, including its full instructions. The version must belong
    to the skill in the path; a mismatch is a 404 rather than a cross-skill read.

    Args:
        skill_id (UUID): Skill id (UUID) the version belongs to.
        skill_version_id (UUID): Immutable skill version id (UUID), as listed by listSkillVersions
            or reported as a skill's latest_skill_version_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion
     """


    return sync_detailed(
        skill_id=skill_id,
skill_version_id=skill_version_id,
client=client,

    ).parsed

async def asyncio_detailed(
    skill_id: UUID,
    skill_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion]:
    """ Get one immutable skill version

     Returns one immutable skill version by id, including its full instructions. The version must belong
    to the skill in the path; a mismatch is a 404 rather than a cross-skill read.

    Args:
        skill_id (UUID): Skill id (UUID) the version belongs to.
        skill_version_id (UUID): Immutable skill version id (UUID), as listed by listSkillVersions
            or reported as a skill's latest_skill_version_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion]
     """


    kwargs = _get_kwargs(
        skill_id=skill_id,
skill_version_id=skill_version_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    skill_id: UUID,
    skill_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion | None:
    """ Get one immutable skill version

     Returns one immutable skill version by id, including its full instructions. The version must belong
    to the skill in the path; a mismatch is a 404 rather than a cross-skill read.

    Args:
        skill_id (UUID): Skill id (UUID) the version belongs to.
        skill_version_id (UUID): Immutable skill version id (UUID), as listed by listSkillVersions
            or reported as a skill's latest_skill_version_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSkillVersion
     """


    return (await asyncio_detailed(
        skill_id=skill_id,
skill_version_id=skill_version_id,
client=client,

    )).parsed
