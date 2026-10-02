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
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_trigger_binding import ManagedAgentsTriggerBinding
from ...models.managed_agents_update_trigger_binding_request import ManagedAgentsUpdateTriggerBindingRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    binding_id: UUID,
    *,
    body: ManagedAgentsUpdateTriggerBindingRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/managed-agents/v1/trigger-bindings/{binding_id}".format(binding_id=quote(str(binding_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding | None:
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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    binding_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTriggerBindingRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]:
    """ Partially update a compatibility wake rule binding

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        binding_id (UUID): Trigger binding id (UUID) returned by the create or list operation.
        body (ManagedAgentsUpdateTriggerBindingRequest): Partial update of one trigger binding.
            Only the properties present in the request change; an omitted property keeps its stored
            value, so an explicit false or empty list is distinguishable from an omission. The merged
            binding is revalidated as a whole, which is what keeps a single-field edit from bypassing
            a provider or tenancy invariant. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]
     """


    kwargs = _get_kwargs(
        binding_id=binding_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    binding_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTriggerBindingRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding | None:
    """ Partially update a compatibility wake rule binding

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        binding_id (UUID): Trigger binding id (UUID) returned by the create or list operation.
        body (ManagedAgentsUpdateTriggerBindingRequest): Partial update of one trigger binding.
            Only the properties present in the request change; an omitted property keeps its stored
            value, so an explicit false or empty list is distinguishable from an omission. The merged
            binding is revalidated as a whole, which is what keeps a single-field edit from bypassing
            a provider or tenancy invariant. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding
     """


    return sync_detailed(
        binding_id=binding_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    binding_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTriggerBindingRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]:
    """ Partially update a compatibility wake rule binding

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        binding_id (UUID): Trigger binding id (UUID) returned by the create or list operation.
        body (ManagedAgentsUpdateTriggerBindingRequest): Partial update of one trigger binding.
            Only the properties present in the request change; an omitted property keeps its stored
            value, so an explicit false or empty list is distinguishable from an omission. The merged
            binding is revalidated as a whole, which is what keeps a single-field edit from bypassing
            a provider or tenancy invariant. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding]
     """


    kwargs = _get_kwargs(
        binding_id=binding_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    binding_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTriggerBindingRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding | None:
    """ Partially update a compatibility wake rule binding

     Reachable with an API key through this API, which authorizes the caller and then calls the upstream
    service with its own credential. The upstream operation is not callable with a customer key
    directly.

    Args:
        binding_id (UUID): Trigger binding id (UUID) returned by the create or list operation.
        body (ManagedAgentsUpdateTriggerBindingRequest): Partial update of one trigger binding.
            Only the properties present in the request change; an omitted property keeps its stored
            value, so an explicit false or empty list is distinguishable from an omission. The merged
            binding is revalidated as a whole, which is what keeps a single-field edit from bypassing
            a provider or tenancy invariant. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'],
            'wake_app_ids': ['example'], 'wake_event': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTriggerBinding
     """


    return (await asyncio_detailed(
        binding_id=binding_id,
client=client,
body=body,

    )).parsed
