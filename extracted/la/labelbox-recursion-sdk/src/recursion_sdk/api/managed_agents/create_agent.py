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
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_create_agent_request import ManagedAgentsCreateAgentRequest
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsCreateAgentRequest,
    idempotency_key: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/agents",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsAgent.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType]:
    """ Create an agent and immutable version

     Creates an agent and its first immutable version, and returns the agent resolved to that version.
    Exactly one of model or model_ref_id is required alongside name and system. The body is also
    accepted as application/x-yaml with the same schema. Any vault named in default_vault_ids must
    already exist. Invalid model_config and unsupported reasoning_effort values return 400, including
    when a reachable gateway model publishes no exact options; an unconfigured or unreachable gateway
    that prevents verification returns 503. An optional Idempotency-Key makes an ambiguous retry safe.
    Keys contain 1 to 256 visible ASCII characters, must be sent as exactly one header value, and use an
    organization-wide namespace shared by keyed mutations. Request identity is the exact HTTP method,
    escaped path, raw query, and raw body bytes: the same organization, key, and transport identity
    replay the original successful response, while any difference returns 409 idempotency_conflict and
    an active matching request returns 409 idempotency_in_progress. The agent, first version, request
    fingerprint, and response binding commit atomically. Completed receipts are retained for
    approximately 24 hours; pending claims may be reclaimed after approximately 1 hour; no deduplication
    is guaranteed after expiry. Never retry an unkeyed create after an ambiguous timeout. The guarantee
    applies only when every intermediary preserves Idempotency-Key unchanged; a client must verify its
    ingress path does so before relying on ambiguous retry replay.

    Args:
        idempotency_key (str | Unset): Replay-protection key in an organization-wide namespace
            shared by keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent
            as exactly one header value. Request identity is the exact HTTP method, escaped path, raw
            query, and raw body bytes. The same request replays the original successful response; any
            different request returns 409 idempotency_conflict, and an active matching request returns
            409 idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsCreateAgentRequest): Request body for creating an agent: its system
            prompt, model, tool surface, and default vault grants. Sessions snapshot the agent version
            at start, so later edits do not change a running session. Example:
            {'built_in_integrations': [{'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'tools': ['example']}], 'default_credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
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
        Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType]
     """


    kwargs = _get_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentRequest,
    idempotency_key: str | Unset = UNSET,

) -> ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | None:
    """ Create an agent and immutable version

     Creates an agent and its first immutable version, and returns the agent resolved to that version.
    Exactly one of model or model_ref_id is required alongside name and system. The body is also
    accepted as application/x-yaml with the same schema. Any vault named in default_vault_ids must
    already exist. Invalid model_config and unsupported reasoning_effort values return 400, including
    when a reachable gateway model publishes no exact options; an unconfigured or unreachable gateway
    that prevents verification returns 503. An optional Idempotency-Key makes an ambiguous retry safe.
    Keys contain 1 to 256 visible ASCII characters, must be sent as exactly one header value, and use an
    organization-wide namespace shared by keyed mutations. Request identity is the exact HTTP method,
    escaped path, raw query, and raw body bytes: the same organization, key, and transport identity
    replay the original successful response, while any difference returns 409 idempotency_conflict and
    an active matching request returns 409 idempotency_in_progress. The agent, first version, request
    fingerprint, and response binding commit atomically. Completed receipts are retained for
    approximately 24 hours; pending claims may be reclaimed after approximately 1 hour; no deduplication
    is guaranteed after expiry. Never retry an unkeyed create after an ambiguous timeout. The guarantee
    applies only when every intermediary preserves Idempotency-Key unchanged; a client must verify its
    ingress path does so before relying on ambiguous retry replay.

    Args:
        idempotency_key (str | Unset): Replay-protection key in an organization-wide namespace
            shared by keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent
            as exactly one header value. Request identity is the exact HTTP method, escaped path, raw
            query, and raw body bytes. The same request replays the original successful response; any
            different request returns 409 idempotency_conflict, and an active matching request returns
            409 idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsCreateAgentRequest): Request body for creating an agent: its system
            prompt, model, tool surface, and default vault grants. Sessions snapshot the agent version
            at start, so later edits do not change a running session. Example:
            {'built_in_integrations': [{'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'tools': ['example']}], 'default_credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
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
        ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType
     """


    return sync_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType]:
    """ Create an agent and immutable version

     Creates an agent and its first immutable version, and returns the agent resolved to that version.
    Exactly one of model or model_ref_id is required alongside name and system. The body is also
    accepted as application/x-yaml with the same schema. Any vault named in default_vault_ids must
    already exist. Invalid model_config and unsupported reasoning_effort values return 400, including
    when a reachable gateway model publishes no exact options; an unconfigured or unreachable gateway
    that prevents verification returns 503. An optional Idempotency-Key makes an ambiguous retry safe.
    Keys contain 1 to 256 visible ASCII characters, must be sent as exactly one header value, and use an
    organization-wide namespace shared by keyed mutations. Request identity is the exact HTTP method,
    escaped path, raw query, and raw body bytes: the same organization, key, and transport identity
    replay the original successful response, while any difference returns 409 idempotency_conflict and
    an active matching request returns 409 idempotency_in_progress. The agent, first version, request
    fingerprint, and response binding commit atomically. Completed receipts are retained for
    approximately 24 hours; pending claims may be reclaimed after approximately 1 hour; no deduplication
    is guaranteed after expiry. Never retry an unkeyed create after an ambiguous timeout. The guarantee
    applies only when every intermediary preserves Idempotency-Key unchanged; a client must verify its
    ingress path does so before relying on ambiguous retry replay.

    Args:
        idempotency_key (str | Unset): Replay-protection key in an organization-wide namespace
            shared by keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent
            as exactly one header value. Request identity is the exact HTTP method, escaped path, raw
            query, and raw body bytes. The same request replays the original successful response; any
            different request returns 409 idempotency_conflict, and an active matching request returns
            409 idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsCreateAgentRequest): Request body for creating an agent: its system
            prompt, model, tool surface, and default vault grants. Sessions snapshot the agent version
            at start, so later edits do not change a running session. Example:
            {'built_in_integrations': [{'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'tools': ['example']}], 'default_credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
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
        Response[ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType]
     """


    kwargs = _get_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateAgentRequest,
    idempotency_key: str | Unset = UNSET,

) -> ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | None:
    """ Create an agent and immutable version

     Creates an agent and its first immutable version, and returns the agent resolved to that version.
    Exactly one of model or model_ref_id is required alongside name and system. The body is also
    accepted as application/x-yaml with the same schema. Any vault named in default_vault_ids must
    already exist. Invalid model_config and unsupported reasoning_effort values return 400, including
    when a reachable gateway model publishes no exact options; an unconfigured or unreachable gateway
    that prevents verification returns 503. An optional Idempotency-Key makes an ambiguous retry safe.
    Keys contain 1 to 256 visible ASCII characters, must be sent as exactly one header value, and use an
    organization-wide namespace shared by keyed mutations. Request identity is the exact HTTP method,
    escaped path, raw query, and raw body bytes: the same organization, key, and transport identity
    replay the original successful response, while any difference returns 409 idempotency_conflict and
    an active matching request returns 409 idempotency_in_progress. The agent, first version, request
    fingerprint, and response binding commit atomically. Completed receipts are retained for
    approximately 24 hours; pending claims may be reclaimed after approximately 1 hour; no deduplication
    is guaranteed after expiry. Never retry an unkeyed create after an ambiguous timeout. The guarantee
    applies only when every intermediary preserves Idempotency-Key unchanged; a client must verify its
    ingress path does so before relying on ambiguous retry replay.

    Args:
        idempotency_key (str | Unset): Replay-protection key in an organization-wide namespace
            shared by keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent
            as exactly one header value. Request identity is the exact HTTP method, escaped path, raw
            query, and raw body bytes. The same request replays the original successful response; any
            different request returns 409 idempotency_conflict, and an active matching request returns
            409 idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsCreateAgentRequest): Request body for creating an agent: its system
            prompt, model, tool surface, and default vault grants. Sessions snapshot the agent version
            at start, so later edits do not change a running session. Example:
            {'built_in_integrations': [{'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'tools': ['example']}], 'default_credential_refs': [{'credential_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
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
        ManagedAgentsAgent | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType
     """


    return (await asyncio_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
