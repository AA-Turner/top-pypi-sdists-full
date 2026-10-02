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
from ...models.managed_agents_create_vault_credential_request import ManagedAgentsCreateVaultCredentialRequest
from ...models.managed_agents_vault_credential import ManagedAgentsVaultCredential
from typing import cast
from uuid import UUID



def _get_kwargs(
    vault_id: UUID,
    *,
    body: ManagedAgentsCreateVaultCredentialRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/vaults/{vault_id}/credentials".format(vault_id=quote(str(vault_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsVaultCredential.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vault_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateVaultCredentialRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential]:
    """ Register a credential reference in a vault

     Registers one credential in a vault and returns the stored reference. Supply exactly one of
    secret_value (encrypted under the organization's key and stored as ciphertext) or secret_ref
    (material you already stored yourself) for secret-backed kinds. Integration grants carry neither;
    they reference a connected account that mints short-lived credentials. Secret material is never
    echoed back on this or any later response.

    Args:
        vault_id (UUID): Vault id (UUID) as returned by createVault or listVaults.
        body (ManagedAgentsCreateVaultCredentialRequest): Request body for adding one credential
            to a vault. Its shape depends on credential_type. bearer_token and env_var accept exactly
            one of secret_value or secret_ref; webhook_secret requires secret_value; integration
            accepts neither. Secret material is encrypted at rest and never returned. Example:
            {'allowed_hosts': ['example'], 'credential_type': 'bearer_token', 'display_name':
            'example-name', 'injection_locations': ['headers'], 'integration_connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'integration_permission': 'example',
            'integration_resources': ['example'], 'labelbox_scope': {'mode': 'projects',
            'project_ids': ['project-id']}, 'mcp_server_url': 'https://example.com', 'metadata':
            {'key': 'example'}, 'network_mode': 'limited', 'secret_name': 'example', 'secret_ref':
            'example', 'secret_value': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential]
     """


    kwargs = _get_kwargs(
        vault_id=vault_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    vault_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateVaultCredentialRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential | None:
    """ Register a credential reference in a vault

     Registers one credential in a vault and returns the stored reference. Supply exactly one of
    secret_value (encrypted under the organization's key and stored as ciphertext) or secret_ref
    (material you already stored yourself) for secret-backed kinds. Integration grants carry neither;
    they reference a connected account that mints short-lived credentials. Secret material is never
    echoed back on this or any later response.

    Args:
        vault_id (UUID): Vault id (UUID) as returned by createVault or listVaults.
        body (ManagedAgentsCreateVaultCredentialRequest): Request body for adding one credential
            to a vault. Its shape depends on credential_type. bearer_token and env_var accept exactly
            one of secret_value or secret_ref; webhook_secret requires secret_value; integration
            accepts neither. Secret material is encrypted at rest and never returned. Example:
            {'allowed_hosts': ['example'], 'credential_type': 'bearer_token', 'display_name':
            'example-name', 'injection_locations': ['headers'], 'integration_connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'integration_permission': 'example',
            'integration_resources': ['example'], 'labelbox_scope': {'mode': 'projects',
            'project_ids': ['project-id']}, 'mcp_server_url': 'https://example.com', 'metadata':
            {'key': 'example'}, 'network_mode': 'limited', 'secret_name': 'example', 'secret_ref':
            'example', 'secret_value': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential
     """


    return sync_detailed(
        vault_id=vault_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    vault_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateVaultCredentialRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential]:
    """ Register a credential reference in a vault

     Registers one credential in a vault and returns the stored reference. Supply exactly one of
    secret_value (encrypted under the organization's key and stored as ciphertext) or secret_ref
    (material you already stored yourself) for secret-backed kinds. Integration grants carry neither;
    they reference a connected account that mints short-lived credentials. Secret material is never
    echoed back on this or any later response.

    Args:
        vault_id (UUID): Vault id (UUID) as returned by createVault or listVaults.
        body (ManagedAgentsCreateVaultCredentialRequest): Request body for adding one credential
            to a vault. Its shape depends on credential_type. bearer_token and env_var accept exactly
            one of secret_value or secret_ref; webhook_secret requires secret_value; integration
            accepts neither. Secret material is encrypted at rest and never returned. Example:
            {'allowed_hosts': ['example'], 'credential_type': 'bearer_token', 'display_name':
            'example-name', 'injection_locations': ['headers'], 'integration_connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'integration_permission': 'example',
            'integration_resources': ['example'], 'labelbox_scope': {'mode': 'projects',
            'project_ids': ['project-id']}, 'mcp_server_url': 'https://example.com', 'metadata':
            {'key': 'example'}, 'network_mode': 'limited', 'secret_name': 'example', 'secret_ref':
            'example', 'secret_value': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential]
     """


    kwargs = _get_kwargs(
        vault_id=vault_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    vault_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsCreateVaultCredentialRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential | None:
    """ Register a credential reference in a vault

     Registers one credential in a vault and returns the stored reference. Supply exactly one of
    secret_value (encrypted under the organization's key and stored as ciphertext) or secret_ref
    (material you already stored yourself) for secret-backed kinds. Integration grants carry neither;
    they reference a connected account that mints short-lived credentials. Secret material is never
    echoed back on this or any later response.

    Args:
        vault_id (UUID): Vault id (UUID) as returned by createVault or listVaults.
        body (ManagedAgentsCreateVaultCredentialRequest): Request body for adding one credential
            to a vault. Its shape depends on credential_type. bearer_token and env_var accept exactly
            one of secret_value or secret_ref; webhook_secret requires secret_value; integration
            accepts neither. Secret material is encrypted at rest and never returned. Example:
            {'allowed_hosts': ['example'], 'credential_type': 'bearer_token', 'display_name':
            'example-name', 'injection_locations': ['headers'], 'integration_connection_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'integration_permission': 'example',
            'integration_resources': ['example'], 'labelbox_scope': {'mode': 'projects',
            'project_ids': ['project-id']}, 'mcp_server_url': 'https://example.com', 'metadata':
            {'key': 'example'}, 'network_mode': 'limited', 'secret_name': 'example', 'secret_ref':
            'example', 'secret_value': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsVaultCredential
     """


    return (await asyncio_detailed(
        vault_id=vault_id,
client=client,
body=body,

    )).parsed
