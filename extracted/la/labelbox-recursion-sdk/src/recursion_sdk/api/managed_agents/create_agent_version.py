from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_agent import ManagedAgentsAgent
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_create_agent_version_request import ManagedAgentsCreateAgentVersionRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    agent_id: UUID,
    *,
    body: ManagedAgentsCreateAgentVersionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/agents/{agent_id}/versions".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | None:
    if response.status_code == 201:
        response_201 = ManagedAgentsAgent.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentVersionRequest,

) -> Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType]:
    """ Create a new immutable agent version

     Creates a new immutable agent version from a full definition and moves the agent's latest pointer to
    it, in one atomic operation. base_agent_version_id must be the agent's current
    latest_agent_version_id or the request is rejected with 409 revision_conflict, so the caller can re-
    read and retry rather than silently racing another writer. Every field is full content, there is no
    partial-update or omit-to-inherit semantics, so an omitted field is cleared rather than carried over
    from the base version. Tags are changed only through the dedicated agent tag routes. Invalid
    model_config and unsupported reasoning_effort values return 400, including when a reachable gateway
    model publishes no exact options; an unconfigured or unreachable gateway that prevents verification
    returns 503. Of the response, only latest_agent_version_id is guaranteed to name the version this
    call minted: the other fields come from a read taken after the commit, so a concurrent writer's
    content can appear beneath that id. Read the version back with getAgentVersion when the exact
    published content matters.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.
        body (ManagedAgentsCreateAgentVersionRequest): Request body for creating a new immutable
            agent version. Every field means what it means on createAgent -- full content is always
            required, there is no partial update -- except disabled_integration_mcp_providers, whose
            omission means none here rather than the new-agent default. base_agent_version_id must be
            the agent's current version or the request is rejected with revision_conflict so the
            caller can re-read and retry. Example: {'base_agent_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'built_in_integrations': [{'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'default_credential_refs':
            [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'default_project_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids':
            ['example'], 'description': 'example', 'disabled_integration_mcp_providers': ['example'],
            'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}], 'metadata': {'key':
            'example'}, 'model': 'example', 'model_config': {'max_tokens': 1, 'provider_params':
            {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5},
            'multiagent': {'key': 'example'}, 'name': 'example-name', 'nativeIntegrations':
            [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example',
            'resources': ['example']}], 'skills': [{'key': 'example'}], 'system': 'example',
            'toolsets': [{'type': 'evaluation'}], 'web_search_enabled': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentVersionRequest,

) -> ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | None:
    """ Create a new immutable agent version

     Creates a new immutable agent version from a full definition and moves the agent's latest pointer to
    it, in one atomic operation. base_agent_version_id must be the agent's current
    latest_agent_version_id or the request is rejected with 409 revision_conflict, so the caller can re-
    read and retry rather than silently racing another writer. Every field is full content, there is no
    partial-update or omit-to-inherit semantics, so an omitted field is cleared rather than carried over
    from the base version. Tags are changed only through the dedicated agent tag routes. Invalid
    model_config and unsupported reasoning_effort values return 400, including when a reachable gateway
    model publishes no exact options; an unconfigured or unreachable gateway that prevents verification
    returns 503. Of the response, only latest_agent_version_id is guaranteed to name the version this
    call minted: the other fields come from a read taken after the commit, so a concurrent writer's
    content can appear beneath that id. Read the version back with getAgentVersion when the exact
    published content matters.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.
        body (ManagedAgentsCreateAgentVersionRequest): Request body for creating a new immutable
            agent version. Every field means what it means on createAgent -- full content is always
            required, there is no partial update -- except disabled_integration_mcp_providers, whose
            omission means none here rather than the new-agent default. base_agent_version_id must be
            the agent's current version or the request is rejected with revision_conflict so the
            caller can re-read and retry. Example: {'base_agent_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'built_in_integrations': [{'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'default_credential_refs':
            [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'default_project_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids':
            ['example'], 'description': 'example', 'disabled_integration_mcp_providers': ['example'],
            'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}], 'metadata': {'key':
            'example'}, 'model': 'example', 'model_config': {'max_tokens': 1, 'provider_params':
            {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5},
            'multiagent': {'key': 'example'}, 'name': 'example-name', 'nativeIntegrations':
            [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example',
            'resources': ['example']}], 'skills': [{'key': 'example'}], 'system': 'example',
            'toolsets': [{'type': 'evaluation'}], 'web_search_enabled': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentVersionRequest,

) -> Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType]:
    """ Create a new immutable agent version

     Creates a new immutable agent version from a full definition and moves the agent's latest pointer to
    it, in one atomic operation. base_agent_version_id must be the agent's current
    latest_agent_version_id or the request is rejected with 409 revision_conflict, so the caller can re-
    read and retry rather than silently racing another writer. Every field is full content, there is no
    partial-update or omit-to-inherit semantics, so an omitted field is cleared rather than carried over
    from the base version. Tags are changed only through the dedicated agent tag routes. Invalid
    model_config and unsupported reasoning_effort values return 400, including when a reachable gateway
    model publishes no exact options; an unconfigured or unreachable gateway that prevents verification
    returns 503. Of the response, only latest_agent_version_id is guaranteed to name the version this
    call minted: the other fields come from a read taken after the commit, so a concurrent writer's
    content can appear beneath that id. Read the version back with getAgentVersion when the exact
    published content matters.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.
        body (ManagedAgentsCreateAgentVersionRequest): Request body for creating a new immutable
            agent version. Every field means what it means on createAgent -- full content is always
            required, there is no partial update -- except disabled_integration_mcp_providers, whose
            omission means none here rather than the new-agent default. base_agent_version_id must be
            the agent's current version or the request is rejected with revision_conflict so the
            caller can re-read and retry. Example: {'base_agent_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'built_in_integrations': [{'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'default_credential_refs':
            [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'default_project_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids':
            ['example'], 'description': 'example', 'disabled_integration_mcp_providers': ['example'],
            'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}], 'metadata': {'key':
            'example'}, 'model': 'example', 'model_config': {'max_tokens': 1, 'provider_params':
            {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5},
            'multiagent': {'key': 'example'}, 'name': 'example-name', 'nativeIntegrations':
            [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example',
            'resources': ['example']}], 'skills': [{'key': 'example'}], 'system': 'example',
            'toolsets': [{'type': 'evaluation'}], 'web_search_enabled': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentVersionRequest,

) -> ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | None:
    """ Create a new immutable agent version

     Creates a new immutable agent version from a full definition and moves the agent's latest pointer to
    it, in one atomic operation. base_agent_version_id must be the agent's current
    latest_agent_version_id or the request is rejected with 409 revision_conflict, so the caller can re-
    read and retry rather than silently racing another writer. Every field is full content, there is no
    partial-update or omit-to-inherit semantics, so an omitted field is cleared rather than carried over
    from the base version. Tags are changed only through the dedicated agent tag routes. Invalid
    model_config and unsupported reasoning_effort values return 400, including when a reachable gateway
    model publishes no exact options; an unconfigured or unreachable gateway that prevents verification
    returns 503. Of the response, only latest_agent_version_id is guaranteed to name the version this
    call minted: the other fields come from a read taken after the commit, so a concurrent writer's
    content can appear beneath that id. Read the version back with getAgentVersion when the exact
    published content matters.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.
        body (ManagedAgentsCreateAgentVersionRequest): Request body for creating a new immutable
            agent version. Every field means what it means on createAgent -- full content is always
            required, there is no partial update -- except disabled_integration_mcp_providers, whose
            omission means none here rather than the new-agent default. base_agent_version_id must be
            the agent's current version or the request is rejected with revision_conflict so the
            caller can re-read and retry. Example: {'base_agent_version_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'built_in_integrations': [{'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tools': ['example']}], 'default_credential_refs':
            [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'default_project_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'default_rubric': 'example', 'default_vault_ids':
            ['example'], 'description': 'example', 'disabled_integration_mcp_providers': ['example'],
            'max_concurrent_sessions': 1, 'mcp_servers': [{'key': 'example'}], 'metadata': {'key':
            'example'}, 'model': 'example', 'model_config': {'max_tokens': 1, 'provider_params':
            {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5},
            'multiagent': {'key': 'example'}, 'name': 'example-name', 'nativeIntegrations':
            [{'connectionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'permission': 'example',
            'resources': ['example']}], 'skills': [{'key': 'example'}], 'system': 'example',
            'toolsets': [{'type': 'evaluation'}], 'web_search_enabled': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
