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
from ...models.managed_agents_create_skill_version_request import ManagedAgentsCreateSkillVersionRequest
from ...models.managed_agents_form_data_skill_version_bundle_upload_request import ManagedAgentsFormDataSkillVersionBundleUploadRequest
from ...models.managed_agents_skill_version import ManagedAgentsSkillVersion
from typing import cast
from uuid import UUID



def _get_kwargs(
    skill_id: UUID,
    *,
    body:    ManagedAgentsCreateSkillVersionRequest  |     ManagedAgentsFormDataSkillVersionBundleUploadRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/skills/{skill_id}/versions".format(skill_id=quote(str(skill_id), safe=""),),
    }

    if isinstance(body, ManagedAgentsCreateSkillVersionRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ManagedAgentsFormDataSkillVersionBundleUploadRequest):
        _kwargs["files"] = body.to_multipart()

        headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion | None:
    if response.status_code == 201:
        response_201 = ManagedAgentsSkillVersion.from_dict(response.json())



        return response_201

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion]:
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
    body:    ManagedAgentsCreateSkillVersionRequest  |     ManagedAgentsFormDataSkillVersionBundleUploadRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion]:
    """ Publish a new version of a skill

     Mints a new immutable version from an uploaded zip or a SKILL.md document and returns it, because an
    author who just published needs the version id to pin an agent to it. Sessions already running keep
    the version they froze. base_skill_version_id must be the skill's current latest_skill_version_id or
    the request is rejected with 409 revision_conflict, so the caller can re-read and retry rather than
    silently racing another writer. Every field is full content, there is no partial-update or omit-to-
    inherit semantics, so an omitted display_title or metadata is cleared rather than kept. Filing is
    not published here -- a skill keeps the group it is in, and skill_group_id is rejected rather than
    ignored; move a skill between groups with updateSkill, which refiles without minting a version.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsCreateSkillVersionRequest): Request body for creating a new immutable
            skill version. Every field means what it means on createSkill -- full content is always
            required, there is no partial update. base_skill_version_id must be the skill's current
            version or the request is rejected with revision_conflict so the caller can re-read and
            retry. Example: {'base_skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}}.
        body (ManagedAgentsFormDataSkillVersionBundleUploadRequest): Multipart body carrying a
            zipped skill directory in the bundle part, plus the base version it advances from.
            Replaces every file in the skill: parts left out are cleared, not inherited from the
            current version. Example: {'base_skill_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'bundle': 'example', 'display_title': 'example',
            'metadata': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion]
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
    body:    ManagedAgentsCreateSkillVersionRequest  |     ManagedAgentsFormDataSkillVersionBundleUploadRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion | None:
    """ Publish a new version of a skill

     Mints a new immutable version from an uploaded zip or a SKILL.md document and returns it, because an
    author who just published needs the version id to pin an agent to it. Sessions already running keep
    the version they froze. base_skill_version_id must be the skill's current latest_skill_version_id or
    the request is rejected with 409 revision_conflict, so the caller can re-read and retry rather than
    silently racing another writer. Every field is full content, there is no partial-update or omit-to-
    inherit semantics, so an omitted display_title or metadata is cleared rather than kept. Filing is
    not published here -- a skill keeps the group it is in, and skill_group_id is rejected rather than
    ignored; move a skill between groups with updateSkill, which refiles without minting a version.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsCreateSkillVersionRequest): Request body for creating a new immutable
            skill version. Every field means what it means on createSkill -- full content is always
            required, there is no partial update. base_skill_version_id must be the skill's current
            version or the request is rejected with revision_conflict so the caller can re-read and
            retry. Example: {'base_skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}}.
        body (ManagedAgentsFormDataSkillVersionBundleUploadRequest): Multipart body carrying a
            zipped skill directory in the bundle part, plus the base version it advances from.
            Replaces every file in the skill: parts left out are cleared, not inherited from the
            current version. Example: {'base_skill_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'bundle': 'example', 'display_title': 'example',
            'metadata': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion
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
    body:    ManagedAgentsCreateSkillVersionRequest  |     ManagedAgentsFormDataSkillVersionBundleUploadRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion]:
    """ Publish a new version of a skill

     Mints a new immutable version from an uploaded zip or a SKILL.md document and returns it, because an
    author who just published needs the version id to pin an agent to it. Sessions already running keep
    the version they froze. base_skill_version_id must be the skill's current latest_skill_version_id or
    the request is rejected with 409 revision_conflict, so the caller can re-read and retry rather than
    silently racing another writer. Every field is full content, there is no partial-update or omit-to-
    inherit semantics, so an omitted display_title or metadata is cleared rather than kept. Filing is
    not published here -- a skill keeps the group it is in, and skill_group_id is rejected rather than
    ignored; move a skill between groups with updateSkill, which refiles without minting a version.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsCreateSkillVersionRequest): Request body for creating a new immutable
            skill version. Every field means what it means on createSkill -- full content is always
            required, there is no partial update. base_skill_version_id must be the skill's current
            version or the request is rejected with revision_conflict so the caller can re-read and
            retry. Example: {'base_skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}}.
        body (ManagedAgentsFormDataSkillVersionBundleUploadRequest): Multipart body carrying a
            zipped skill directory in the bundle part, plus the base version it advances from.
            Replaces every file in the skill: parts left out are cleared, not inherited from the
            current version. Example: {'base_skill_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'bundle': 'example', 'display_title': 'example',
            'metadata': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion]
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
    body:    ManagedAgentsCreateSkillVersionRequest  |     ManagedAgentsFormDataSkillVersionBundleUploadRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion | None:
    """ Publish a new version of a skill

     Mints a new immutable version from an uploaded zip or a SKILL.md document and returns it, because an
    author who just published needs the version id to pin an agent to it. Sessions already running keep
    the version they froze. base_skill_version_id must be the skill's current latest_skill_version_id or
    the request is rejected with 409 revision_conflict, so the caller can re-read and retry rather than
    silently racing another writer. Every field is full content, there is no partial-update or omit-to-
    inherit semantics, so an omitted display_title or metadata is cleared rather than kept. Filing is
    not published here -- a skill keeps the group it is in, and skill_group_id is rejected rather than
    ignored; move a skill between groups with updateSkill, which refiles without minting a version.

    Args:
        skill_id (UUID): Skill id (UUID) as returned by createSkill or listSkills.
        body (ManagedAgentsCreateSkillVersionRequest): Request body for creating a new immutable
            skill version. Every field means what it means on createSkill -- full content is always
            required, there is no partial update. base_skill_version_id must be the skill's current
            version or the request is rejected with revision_conflict so the caller can re-read and
            retry. Example: {'base_skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}}.
        body (ManagedAgentsFormDataSkillVersionBundleUploadRequest): Multipart body carrying a
            zipped skill directory in the bundle part, plus the base version it advances from.
            Replaces every file in the skill: parts left out are cleared, not inherited from the
            current version. Example: {'base_skill_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'bundle': 'example', 'display_title': 'example',
            'metadata': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkillVersion
     """


    return (await asyncio_detailed(
        skill_id=skill_id,
client=client,
body=body,

    )).parsed
