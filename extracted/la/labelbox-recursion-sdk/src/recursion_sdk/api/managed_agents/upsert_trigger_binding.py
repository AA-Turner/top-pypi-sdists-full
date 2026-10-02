from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_create_trigger_binding_request import ManagedAgentsCreateTriggerBindingRequest
from ...models.managed_agents_trigger_binding import ManagedAgentsTriggerBinding
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsCreateTriggerBindingRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/trigger-bindings",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsTriggerBinding.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiError.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateTriggerBindingRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]:
    """ Create a compatibility wake rule binding provider events to an agent

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        body (ManagedAgentsCreateTriggerBindingRequest): Request body creating a Slack wake rule:
            the connection and event to match, and the agent, environment, and vaults a match runs
            with. Every referenced object must belong to the calling organization; GitHub events use
            provider-neutral automations instead. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]
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
    body: ManagedAgentsCreateTriggerBindingRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding | None:
    """ Create a compatibility wake rule binding provider events to an agent

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        body (ManagedAgentsCreateTriggerBindingRequest): Request body creating a Slack wake rule:
            the connection and event to match, and the agent, environment, and vaults a match runs
            with. Every referenced object must belong to the calling organization; GitHub events use
            provider-neutral automations instead. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateTriggerBindingRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]:
    """ Create a compatibility wake rule binding provider events to an agent

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        body (ManagedAgentsCreateTriggerBindingRequest): Request body creating a Slack wake rule:
            the connection and event to match, and the agent, environment, and vaults a match runs
            with. Every referenced object must belong to the calling organization; GitHub events use
            provider-neutral automations instead. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]
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
    body: ManagedAgentsCreateTriggerBindingRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding | None:
    """ Create a compatibility wake rule binding provider events to an agent

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        body (ManagedAgentsCreateTriggerBindingRequest): Request body creating a Slack wake rule:
            the connection and event to match, and the agent, environment, and vaults a match runs
            with. Every referenced object must belong to the calling organization; GitHub events use
            provider-neutral automations instead. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
