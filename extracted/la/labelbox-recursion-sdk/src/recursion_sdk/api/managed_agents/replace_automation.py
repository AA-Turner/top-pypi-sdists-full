from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_conflict import ManagedAgentsApiErrorConflict
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_internal_error import ManagedAgentsApiErrorInternalError
from ...models.managed_agents_api_error_invalid_request import ManagedAgentsApiErrorInvalidRequest
from ...models.managed_agents_api_error_invariant_violation import ManagedAgentsApiErrorInvariantViolation
from ...models.managed_agents_api_error_managed_agents_unavailable import ManagedAgentsApiErrorManagedAgentsUnavailable
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_api_error_payload_too_large import ManagedAgentsApiErrorPayloadTooLarge
from ...models.managed_agents_api_error_precondition_failed import ManagedAgentsApiErrorPreconditionFailed
from ...models.managed_agents_api_error_precondition_required import ManagedAgentsApiErrorPreconditionRequired
from ...models.managed_agents_api_error_rate_limit_exceeded import ManagedAgentsApiErrorRateLimitExceeded
from ...models.managed_agents_api_error_rate_limited import ManagedAgentsApiErrorRateLimited
from ...models.managed_agents_api_error_semantic_validation_failed import ManagedAgentsApiErrorSemanticValidationFailed
from ...models.managed_agents_api_error_service_unavailable import ManagedAgentsApiErrorServiceUnavailable
from ...models.managed_agents_api_error_unauthorized import ManagedAgentsApiErrorUnauthorized
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_automation_definition_request import ManagedAgentsAutomationDefinitionRequest
from ...models.managed_agents_automation_definition_response import ManagedAgentsAutomationDefinitionResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    automation_id: UUID,
    *,
    body: ManagedAgentsAutomationDefinitionRequest,
    if_match: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["If-Match"] = if_match



    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/managed-agents/v1/automations/{automation_id}".format(automation_id=quote(str(automation_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsAutomationDefinitionResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = ManagedAgentsApiErrorConflict.from_dict(response.json())



        return response_409

    if response.status_code == 412:
        response_412 = ManagedAgentsApiErrorPreconditionFailed.from_dict(response.json())



        return response_412

    if response.status_code == 413:
        response_413 = ManagedAgentsApiErrorPayloadTooLarge.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

    if response.status_code == 422:
        response_422 = ManagedAgentsApiErrorSemanticValidationFailed.from_dict(response.json())



        return response_422

    if response.status_code == 428:
        response_428 = ManagedAgentsApiErrorPreconditionRequired.from_dict(response.json())



        return response_428

    if response.status_code == 429:
        def _parse_response_429(data: object) -> ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_429_type_0 = ManagedAgentsApiErrorRateLimitExceeded.from_dict(data)



                return response_429_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_429_type_1 = ManagedAgentsApiErrorRateLimited.from_dict(data)



            return response_429_type_1

        response_429 = _parse_response_429(response.json())

        return response_429

    if response.status_code == 500:
        def _parse_response_500(data: object) -> ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_500_type_0 = ManagedAgentsApiErrorInternalError.from_dict(data)



                return response_500_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_500_type_1 = ManagedAgentsApiErrorInvariantViolation.from_dict(data)



            return response_500_type_1

        response_500 = _parse_response_500(response.json())

        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        def _parse_response_503(data: object) -> ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_0 = ManagedAgentsApiErrorManagedAgentsUnavailable.from_dict(data)



                return response_503_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_503_type_1 = ManagedAgentsApiErrorServiceUnavailable.from_dict(data)



            return response_503_type_1

        response_503 = _parse_response_503(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    automation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsAutomationDefinitionRequest,
    if_match: str,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse]:
    """ Replace a canonical automation aggregate

     Replaces the complete writable aggregate and trigger set while preserving lifecycle state. Requires
    the latest strong ETag in If-Match.

    Args:
        automation_id (UUID): Stable canonical automation identifier.
        if_match (str): Strong ETag returned by the latest canonical automation member read.
        body (ManagedAgentsAutomationDefinitionRequest): Complete writable shape for creating or
            replacing a canonical automation. Example: {'agentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agentVersionId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'displayName': 'example', 'environmentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initialPrompt': {'text': 'example', 'type':
            'literal'}, 'runDefaults': {'credentialRefs': [{'credentialId': 'example', 'vaultId':
            'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example',
            'memoryStoreId': 'example'}], 'metadata': {'key': 'example'}, 'resources': [{'fileId':
            'example', 'mountPath': 'example'}], 'vaultIds': ['example']}, 'triggers': [{'enabled':
            True, 'schedule': {'catchupWindowSeconds': 10, 'cron': 'example', 'endAt':
            '2026-02-18T09:30:00Z', 'jitterSeconds': 1, 'overlapPolicy': 'skip', 'startAt':
            '2026-02-18T09:30:00Z', 'timezone': 'example'}, 'triggerId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse]
     """


    kwargs = _get_kwargs(
        automation_id=automation_id,
body=body,
if_match=if_match,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    automation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsAutomationDefinitionRequest,
    if_match: str,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse | None:
    """ Replace a canonical automation aggregate

     Replaces the complete writable aggregate and trigger set while preserving lifecycle state. Requires
    the latest strong ETag in If-Match.

    Args:
        automation_id (UUID): Stable canonical automation identifier.
        if_match (str): Strong ETag returned by the latest canonical automation member read.
        body (ManagedAgentsAutomationDefinitionRequest): Complete writable shape for creating or
            replacing a canonical automation. Example: {'agentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agentVersionId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'displayName': 'example', 'environmentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initialPrompt': {'text': 'example', 'type':
            'literal'}, 'runDefaults': {'credentialRefs': [{'credentialId': 'example', 'vaultId':
            'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example',
            'memoryStoreId': 'example'}], 'metadata': {'key': 'example'}, 'resources': [{'fileId':
            'example', 'mountPath': 'example'}], 'vaultIds': ['example']}, 'triggers': [{'enabled':
            True, 'schedule': {'catchupWindowSeconds': 10, 'cron': 'example', 'endAt':
            '2026-02-18T09:30:00Z', 'jitterSeconds': 1, 'overlapPolicy': 'skip', 'startAt':
            '2026-02-18T09:30:00Z', 'timezone': 'example'}, 'triggerId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse
     """


    return sync_detailed(
        automation_id=automation_id,
client=client,
body=body,
if_match=if_match,

    ).parsed

async def asyncio_detailed(
    automation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsAutomationDefinitionRequest,
    if_match: str,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse]:
    """ Replace a canonical automation aggregate

     Replaces the complete writable aggregate and trigger set while preserving lifecycle state. Requires
    the latest strong ETag in If-Match.

    Args:
        automation_id (UUID): Stable canonical automation identifier.
        if_match (str): Strong ETag returned by the latest canonical automation member read.
        body (ManagedAgentsAutomationDefinitionRequest): Complete writable shape for creating or
            replacing a canonical automation. Example: {'agentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agentVersionId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'displayName': 'example', 'environmentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initialPrompt': {'text': 'example', 'type':
            'literal'}, 'runDefaults': {'credentialRefs': [{'credentialId': 'example', 'vaultId':
            'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example',
            'memoryStoreId': 'example'}], 'metadata': {'key': 'example'}, 'resources': [{'fileId':
            'example', 'mountPath': 'example'}], 'vaultIds': ['example']}, 'triggers': [{'enabled':
            True, 'schedule': {'catchupWindowSeconds': 10, 'cron': 'example', 'endAt':
            '2026-02-18T09:30:00Z', 'jitterSeconds': 1, 'overlapPolicy': 'skip', 'startAt':
            '2026-02-18T09:30:00Z', 'timezone': 'example'}, 'triggerId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse]
     """


    kwargs = _get_kwargs(
        automation_id=automation_id,
body=body,
if_match=if_match,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    automation_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsAutomationDefinitionRequest,
    if_match: str,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse | None:
    """ Replace a canonical automation aggregate

     Replaces the complete writable aggregate and trigger set while preserving lifecycle state. Requires
    the latest strong ETag in If-Match.

    Args:
        automation_id (UUID): Stable canonical automation identifier.
        if_match (str): Strong ETag returned by the latest canonical automation member read.
        body (ManagedAgentsAutomationDefinitionRequest): Complete writable shape for creating or
            replacing a canonical automation. Example: {'agentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agentVersionId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'displayName': 'example', 'environmentId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initialPrompt': {'text': 'example', 'type':
            'literal'}, 'runDefaults': {'credentialRefs': [{'credentialId': 'example', 'vaultId':
            'example'}], 'memoryStores': [{'access': 'read_only', 'instructions': 'example',
            'memoryStoreId': 'example'}], 'metadata': {'key': 'example'}, 'resources': [{'fileId':
            'example', 'mountPath': 'example'}], 'vaultIds': ['example']}, 'triggers': [{'enabled':
            True, 'schedule': {'catchupWindowSeconds': 10, 'cron': 'example', 'endAt':
            '2026-02-18T09:30:00Z', 'jitterSeconds': 1, 'overlapPolicy': 'skip', 'startAt':
            '2026-02-18T09:30:00Z', 'timezone': 'example'}, 'triggerId':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorPreconditionFailed | ManagedAgentsApiErrorPreconditionRequired | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsAutomationDefinitionResponse
     """


    return (await asyncio_detailed(
        automation_id=automation_id,
client=client,
body=body,
if_match=if_match,

    )).parsed
