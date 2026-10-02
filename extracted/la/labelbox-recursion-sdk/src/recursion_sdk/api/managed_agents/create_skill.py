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
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_form_data_skill_bundle_upload_request import ManagedAgentsFormDataSkillBundleUploadRequest
from ...models.managed_agents_skill import ManagedAgentsSkill
from ...models.managed_agents_skill_request import ManagedAgentsSkillRequest
from typing import cast



def _get_kwargs(
    *,
    body:    ManagedAgentsSkillRequest  |     ManagedAgentsFormDataSkillBundleUploadRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/skills",
    }

    if isinstance(body, ManagedAgentsSkillRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ManagedAgentsFormDataSkillBundleUploadRequest):
        _kwargs["files"] = body.to_multipart()

        headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill | None:
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
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body:    ManagedAgentsSkillRequest  |     ManagedAgentsFormDataSkillBundleUploadRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]:
    """ Create a skill and immutable version

     Creates a skill from a SKILL.md document and returns it. The document's frontmatter supplies the
    skill's name and description, which are validated against the Agent Skills standard: the name must
    be lowercase letters, digits, and single hyphens, and a description is required because it is the
    only signal the model has when deciding whether to use the skill. Send a multipart/form-data body
    with a `bundle` part instead to upload a zipped skill directory, whose scripts/ and references/ are
    mounted into the sandbox for sessions that attach it.

    Args:
        body (ManagedAgentsSkillRequest): Request body for creating or updating a skill. The
            document is the source of truth: the skill's name and description come from its
            frontmatter. Publishing a new version of an existing skill goes through
            createSkillVersion, which mints one rather than editing the last. Example:
            {'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}, 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
        body (ManagedAgentsFormDataSkillBundleUploadRequest): Multipart body carrying a zipped
            skill directory in the bundle part. The document, name and description still come from the
            archive's SKILL.md. Example: {'bundle': 'example', 'display_title': 'example', 'metadata':
            'example', 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body:    ManagedAgentsSkillRequest  |     ManagedAgentsFormDataSkillBundleUploadRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill | None:
    """ Create a skill and immutable version

     Creates a skill from a SKILL.md document and returns it. The document's frontmatter supplies the
    skill's name and description, which are validated against the Agent Skills standard: the name must
    be lowercase letters, digits, and single hyphens, and a description is required because it is the
    only signal the model has when deciding whether to use the skill. Send a multipart/form-data body
    with a `bundle` part instead to upload a zipped skill directory, whose scripts/ and references/ are
    mounted into the sandbox for sessions that attach it.

    Args:
        body (ManagedAgentsSkillRequest): Request body for creating or updating a skill. The
            document is the source of truth: the skill's name and description come from its
            frontmatter. Publishing a new version of an existing skill goes through
            createSkillVersion, which mints one rather than editing the last. Example:
            {'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}, 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
        body (ManagedAgentsFormDataSkillBundleUploadRequest): Multipart body carrying a zipped
            skill directory in the bundle part. The document, name and description still come from the
            archive's SKILL.md. Example: {'bundle': 'example', 'display_title': 'example', 'metadata':
            'example', 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body:    ManagedAgentsSkillRequest  |     ManagedAgentsFormDataSkillBundleUploadRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]:
    """ Create a skill and immutable version

     Creates a skill from a SKILL.md document and returns it. The document's frontmatter supplies the
    skill's name and description, which are validated against the Agent Skills standard: the name must
    be lowercase letters, digits, and single hyphens, and a description is required because it is the
    only signal the model has when deciding whether to use the skill. Send a multipart/form-data body
    with a `bundle` part instead to upload a zipped skill directory, whose scripts/ and references/ are
    mounted into the sandbox for sessions that attach it.

    Args:
        body (ManagedAgentsSkillRequest): Request body for creating or updating a skill. The
            document is the source of truth: the skill's name and description come from its
            frontmatter. Publishing a new version of an existing skill goes through
            createSkillVersion, which mints one rather than editing the last. Example:
            {'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}, 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
        body (ManagedAgentsFormDataSkillBundleUploadRequest): Multipart body carrying a zipped
            skill directory in the bundle part. The document, name and description still come from the
            archive's SKILL.md. Example: {'bundle': 'example', 'display_title': 'example', 'metadata':
            'example', 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body:    ManagedAgentsSkillRequest  |     ManagedAgentsFormDataSkillBundleUploadRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill | None:
    """ Create a skill and immutable version

     Creates a skill from a SKILL.md document and returns it. The document's frontmatter supplies the
    skill's name and description, which are validated against the Agent Skills standard: the name must
    be lowercase letters, digits, and single hyphens, and a description is required because it is the
    only signal the model has when deciding whether to use the skill. Send a multipart/form-data body
    with a `bundle` part instead to upload a zipped skill directory, whose scripts/ and references/ are
    mounted into the sandbox for sessions that attach it.

    Args:
        body (ManagedAgentsSkillRequest): Request body for creating or updating a skill. The
            document is the source of truth: the skill's name and description come from its
            frontmatter. Publishing a new version of an existing skill goes through
            createSkillVersion, which mints one rather than editing the last. Example:
            {'display_title': 'example', 'document': 'example', 'manifest': ['example'], 'metadata':
            {'key': 'example'}, 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
        body (ManagedAgentsFormDataSkillBundleUploadRequest): Multipart body carrying a zipped
            skill directory in the bundle part. The document, name and description still come from the
            archive's SKILL.md. Example: {'bundle': 'example', 'display_title': 'example', 'metadata':
            'example', 'skill_group_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSkill
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
