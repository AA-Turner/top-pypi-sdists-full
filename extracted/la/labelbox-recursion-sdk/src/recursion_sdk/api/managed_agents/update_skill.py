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
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_skill import ManagedAgentsSkill
from ...models.managed_agents_skill_patch_request import ManagedAgentsSkillPatchRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    skill_id: UUID,
    *,
    body: ManagedAgentsSkillPatchRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/managed-agents/v1/skills/{skill_id}".format(skill_id=quote(str(skill_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSkill.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = ManagedAgentsApiError.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = ManagedAgentsApiError.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsSkillPatchRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]:
    """ Refile a skill into a catalog group

     Moves a skill between catalog groups, or out of one, and returns the skill. Filing is not authoring:
    this mints no version and leaves the skill's document, title, metadata and bundled files exactly as
    they are, because advancing latest_skill_version_id for a move would make every agent following this
    skill re-resolve to a revision identical to the last one. Publish new content with
    createSkillVersion, which takes a base version id for a compare-and-swap check. Send an empty
    skill_group_id to remove the skill from its group; skill_group_id is required, so a body that
    carries nothing is rejected rather than answered as a save that changed nothing.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsSkillPatchRequest): Request body for refiling a skill between catalog
            groups. Filing is not authoring: this leaves the skill's versions untouched and mints
            nothing. Publish new content with createSkillVersion. Example: {'skill_group_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]
     """


    kwargs = _get_kwargs(
        skill_id=skill_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsSkillPatchRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill | None:
    """ Refile a skill into a catalog group

     Moves a skill between catalog groups, or out of one, and returns the skill. Filing is not authoring:
    this mints no version and leaves the skill's document, title, metadata and bundled files exactly as
    they are, because advancing latest_skill_version_id for a move would make every agent following this
    skill re-resolve to a revision identical to the last one. Publish new content with
    createSkillVersion, which takes a base version id for a compare-and-swap check. Send an empty
    skill_group_id to remove the skill from its group; skill_group_id is required, so a body that
    carries nothing is rejected rather than answered as a save that changed nothing.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsSkillPatchRequest): Request body for refiling a skill between catalog
            groups. Filing is not authoring: this leaves the skill's versions untouched and mints
            nothing. Publish new content with createSkillVersion. Example: {'skill_group_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill
     """


    return sync_detailed(
        skill_id=skill_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsSkillPatchRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]:
    """ Refile a skill into a catalog group

     Moves a skill between catalog groups, or out of one, and returns the skill. Filing is not authoring:
    this mints no version and leaves the skill's document, title, metadata and bundled files exactly as
    they are, because advancing latest_skill_version_id for a move would make every agent following this
    skill re-resolve to a revision identical to the last one. Publish new content with
    createSkillVersion, which takes a base version id for a compare-and-swap check. Send an empty
    skill_group_id to remove the skill from its group; skill_group_id is required, so a body that
    carries nothing is rejected rather than answered as a save that changed nothing.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsSkillPatchRequest): Request body for refiling a skill between catalog
            groups. Filing is not authoring: this leaves the skill's versions untouched and mints
            nothing. Publish new content with createSkillVersion. Example: {'skill_group_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]
     """


    kwargs = _get_kwargs(
        skill_id=skill_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsSkillPatchRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill | None:
    """ Refile a skill into a catalog group

     Moves a skill between catalog groups, or out of one, and returns the skill. Filing is not authoring:
    this mints no version and leaves the skill's document, title, metadata and bundled files exactly as
    they are, because advancing latest_skill_version_id for a move would make every agent following this
    skill re-resolve to a revision identical to the last one. Publish new content with
    createSkillVersion, which takes a base version id for a compare-and-swap check. Send an empty
    skill_group_id to remove the skill from its group; skill_group_id is required, so a body that
    carries nothing is rejected rather than answered as a save that changed nothing.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsSkillPatchRequest): Request body for refiling a skill between catalog
            groups. Filing is not authoring: this leaves the skill's versions untouched and mints
            nothing. Publish new content with createSkillVersion. Example: {'skill_group_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill
     """


    return (await asyncio_detailed(
        skill_id=skill_id,
client=client,
body=body,

    )).parsed
