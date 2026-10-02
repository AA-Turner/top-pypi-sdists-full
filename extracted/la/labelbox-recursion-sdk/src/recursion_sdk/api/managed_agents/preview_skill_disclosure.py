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
from ...models.managed_agents_disclosure_preview import ManagedAgentsDisclosurePreview
from ...models.managed_agents_skill_disclosure_preview_request import ManagedAgentsSkillDisclosurePreviewRequest
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsSkillDisclosurePreviewRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/skills/disclosure-preview",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsDisclosurePreview.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsSkillDisclosurePreviewRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview]:
    """ Preview what a skill set costs the prompt

     Resolves a proposed attachment list the way a session start would -- expanding groups, fetching
    catalog references, deduplicating collisions -- and reports what the result costs tier-1 disclosure
    and which skills the budget reduced to a bare name. A skill listed without its description is still
    activatable but is unlikely to be chosen, because the description is the only signal the model has.
    Read-only: nothing is stored.

    Args:
        body (ManagedAgentsSkillDisclosurePreviewRequest): Request body for previewing tier-1
            skill disclosure. Read-only: nothing is stored, and the attachments do not have to belong
            to any agent yet. Example: {'context_window_tokens': 1, 'skills': [{'key': 'example'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview]
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
    body: ManagedAgentsSkillDisclosurePreviewRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview | None:
    """ Preview what a skill set costs the prompt

     Resolves a proposed attachment list the way a session start would -- expanding groups, fetching
    catalog references, deduplicating collisions -- and reports what the result costs tier-1 disclosure
    and which skills the budget reduced to a bare name. A skill listed without its description is still
    activatable but is unlikely to be chosen, because the description is the only signal the model has.
    Read-only: nothing is stored.

    Args:
        body (ManagedAgentsSkillDisclosurePreviewRequest): Request body for previewing tier-1
            skill disclosure. Read-only: nothing is stored, and the attachments do not have to belong
            to any agent yet. Example: {'context_window_tokens': 1, 'skills': [{'key': 'example'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsSkillDisclosurePreviewRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview]:
    """ Preview what a skill set costs the prompt

     Resolves a proposed attachment list the way a session start would -- expanding groups, fetching
    catalog references, deduplicating collisions -- and reports what the result costs tier-1 disclosure
    and which skills the budget reduced to a bare name. A skill listed without its description is still
    activatable but is unlikely to be chosen, because the description is the only signal the model has.
    Read-only: nothing is stored.

    Args:
        body (ManagedAgentsSkillDisclosurePreviewRequest): Request body for previewing tier-1
            skill disclosure. Read-only: nothing is stored, and the attachments do not have to belong
            to any agent yet. Example: {'context_window_tokens': 1, 'skills': [{'key': 'example'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview]
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
    body: ManagedAgentsSkillDisclosurePreviewRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview | None:
    """ Preview what a skill set costs the prompt

     Resolves a proposed attachment list the way a session start would -- expanding groups, fetching
    catalog references, deduplicating collisions -- and reports what the result costs tier-1 disclosure
    and which skills the budget reduced to a bare name. A skill listed without its description is still
    activatable but is unlikely to be chosen, because the description is the only signal the model has.
    Read-only: nothing is stored.

    Args:
        body (ManagedAgentsSkillDisclosurePreviewRequest): Request body for previewing tier-1
            skill disclosure. Read-only: nothing is stored, and the attachments do not have to belong
            to any agent yet. Example: {'context_window_tokens': 1, 'skills': [{'key': 'example'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsDisclosurePreview
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
