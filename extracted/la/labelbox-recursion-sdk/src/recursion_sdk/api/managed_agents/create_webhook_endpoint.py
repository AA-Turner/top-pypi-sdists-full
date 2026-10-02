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
from ...models.managed_agents_webhook_endpoint import ManagedAgentsWebhookEndpoint
from ...models.managed_agents_webhook_endpoint_request import ManagedAgentsWebhookEndpointRequest
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsWebhookEndpointRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/webhook-endpoints",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint | None:
    if response.status_code == 201:
        response_201 = ManagedAgentsWebhookEndpoint.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsWebhookEndpointRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint]:
    """ Create a configurable webhook endpoint

    Args:
        body (ManagedAgentsWebhookEndpointRequest): Provider-neutral configuration for creating or
            replacing a webhook endpoint. Example: {'acknowledgement': {'body': {'key': 'example'},
            'challenge_response_field': 'example', 'challenge_selector': {'body_pointer': 'example',
            'header': 'example', 'source': 'body'}, 'status_code': 1}, 'delivery_key':
            {'body_pointer': 'example', 'header': 'example', 'selectors': [{'body_pointer': 'example',
            'header': 'example', 'source': 'body'}], 'source': 'body'}, 'display_name': 'example-
            name', 'enabled': True, 'verification': {'invalid_signature_status': 1,
            'maximum_age_seconds': 1, 'secret_credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'secret_vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'signature_header': 'example',
            'signature_prefix': 'example', 'signed_parts': [{'kind': 'body', 'value': 'example'}],
            'timestamp_header': 'example', 'type': 'hmac_sha256'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint]
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
    body: ManagedAgentsWebhookEndpointRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint | None:
    """ Create a configurable webhook endpoint

    Args:
        body (ManagedAgentsWebhookEndpointRequest): Provider-neutral configuration for creating or
            replacing a webhook endpoint. Example: {'acknowledgement': {'body': {'key': 'example'},
            'challenge_response_field': 'example', 'challenge_selector': {'body_pointer': 'example',
            'header': 'example', 'source': 'body'}, 'status_code': 1}, 'delivery_key':
            {'body_pointer': 'example', 'header': 'example', 'selectors': [{'body_pointer': 'example',
            'header': 'example', 'source': 'body'}], 'source': 'body'}, 'display_name': 'example-
            name', 'enabled': True, 'verification': {'invalid_signature_status': 1,
            'maximum_age_seconds': 1, 'secret_credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'secret_vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'signature_header': 'example',
            'signature_prefix': 'example', 'signed_parts': [{'kind': 'body', 'value': 'example'}],
            'timestamp_header': 'example', 'type': 'hmac_sha256'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsWebhookEndpointRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint]:
    """ Create a configurable webhook endpoint

    Args:
        body (ManagedAgentsWebhookEndpointRequest): Provider-neutral configuration for creating or
            replacing a webhook endpoint. Example: {'acknowledgement': {'body': {'key': 'example'},
            'challenge_response_field': 'example', 'challenge_selector': {'body_pointer': 'example',
            'header': 'example', 'source': 'body'}, 'status_code': 1}, 'delivery_key':
            {'body_pointer': 'example', 'header': 'example', 'selectors': [{'body_pointer': 'example',
            'header': 'example', 'source': 'body'}], 'source': 'body'}, 'display_name': 'example-
            name', 'enabled': True, 'verification': {'invalid_signature_status': 1,
            'maximum_age_seconds': 1, 'secret_credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'secret_vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'signature_header': 'example',
            'signature_prefix': 'example', 'signed_parts': [{'kind': 'body', 'value': 'example'}],
            'timestamp_header': 'example', 'type': 'hmac_sha256'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint]
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
    body: ManagedAgentsWebhookEndpointRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint | None:
    """ Create a configurable webhook endpoint

    Args:
        body (ManagedAgentsWebhookEndpointRequest): Provider-neutral configuration for creating or
            replacing a webhook endpoint. Example: {'acknowledgement': {'body': {'key': 'example'},
            'challenge_response_field': 'example', 'challenge_selector': {'body_pointer': 'example',
            'header': 'example', 'source': 'body'}, 'status_code': 1}, 'delivery_key':
            {'body_pointer': 'example', 'header': 'example', 'selectors': [{'body_pointer': 'example',
            'header': 'example', 'source': 'body'}], 'source': 'body'}, 'display_name': 'example-
            name', 'enabled': True, 'verification': {'invalid_signature_status': 1,
            'maximum_age_seconds': 1, 'secret_credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'secret_vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'signature_header': 'example',
            'signature_prefix': 'example', 'signed_parts': [{'kind': 'body', 'value': 'example'}],
            'timestamp_header': 'example', 'type': 'hmac_sha256'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsWebhookEndpoint
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
