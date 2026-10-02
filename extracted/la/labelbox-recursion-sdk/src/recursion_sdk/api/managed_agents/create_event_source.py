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
from ...models.managed_agents_api_error_idempotency_conflict import ManagedAgentsApiErrorIdempotencyConflict
from ...models.managed_agents_api_error_idempotency_in_progress import ManagedAgentsApiErrorIdempotencyInProgress
from ...models.managed_agents_api_error_idempotency_unavailable import ManagedAgentsApiErrorIdempotencyUnavailable
from ...models.managed_agents_api_error_internal_error import ManagedAgentsApiErrorInternalError
from ...models.managed_agents_api_error_invalid_request import ManagedAgentsApiErrorInvalidRequest
from ...models.managed_agents_api_error_invariant_violation import ManagedAgentsApiErrorInvariantViolation
from ...models.managed_agents_api_error_managed_agents_unavailable import ManagedAgentsApiErrorManagedAgentsUnavailable
from ...models.managed_agents_api_error_payload_too_large import ManagedAgentsApiErrorPayloadTooLarge
from ...models.managed_agents_api_error_rate_limit_exceeded import ManagedAgentsApiErrorRateLimitExceeded
from ...models.managed_agents_api_error_rate_limited import ManagedAgentsApiErrorRateLimited
from ...models.managed_agents_api_error_semantic_validation_failed import ManagedAgentsApiErrorSemanticValidationFailed
from ...models.managed_agents_api_error_service_unavailable import ManagedAgentsApiErrorServiceUnavailable
from ...models.managed_agents_api_error_unauthorized import ManagedAgentsApiErrorUnauthorized
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_event_source_response import ManagedAgentsEventSourceResponse
from ...models.managed_agents_github_event_source_request import ManagedAgentsGithubEventSourceRequest
from ...models.managed_agents_hmac_custom_event_source_request import ManagedAgentsHmacCustomEventSourceRequest
from ...models.managed_agents_slack_event_source_request import ManagedAgentsSlackEventSourceRequest
from ...models.managed_agents_unsigned_custom_event_source_request import ManagedAgentsUnsignedCustomEventSourceRequest
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest | ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest,
    idempotency_key: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/event-sources",
    }

    
    if isinstance(body, ManagedAgentsSlackEventSourceRequest):
        _kwargs["json"] = body.to_dict()
    elif isinstance(body, ManagedAgentsGithubEventSourceRequest):
        _kwargs["json"] = body.to_dict()
    elif isinstance(body, ManagedAgentsUnsignedCustomEventSourceRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse | None:
    if response.status_code == 201:
        response_201 = ManagedAgentsEventSourceResponse.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = ManagedAgentsApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 409:
        def _parse_response_409(data: object) -> ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_409_type_0 = ManagedAgentsApiErrorConflict.from_dict(data)



                return response_409_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_409_type_1 = ManagedAgentsApiErrorIdempotencyConflict.from_dict(data)



                return response_409_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_409_type_2 = ManagedAgentsApiErrorIdempotencyInProgress.from_dict(data)



            return response_409_type_2

        response_409 = _parse_response_409(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = ManagedAgentsApiErrorPayloadTooLarge.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

    if response.status_code == 422:
        response_422 = ManagedAgentsApiErrorSemanticValidationFailed.from_dict(response.json())



        return response_422

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
        def _parse_response_503(data: object) -> ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_0 = ManagedAgentsApiErrorIdempotencyUnavailable.from_dict(data)



                return response_503_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_1 = ManagedAgentsApiErrorManagedAgentsUnavailable.from_dict(data)



                return response_503_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_503_type_2 = ManagedAgentsApiErrorServiceUnavailable.from_dict(data)



            return response_503_type_2

        response_503 = _parse_response_503(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest | ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest,
    idempotency_key: str,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse]:
    """ Create a paused event source

     Creates a customer webhook source in the paused state. delivery.kind must be webhook; integration
    sources are connection-managed. Verification credentials are referenced from Vault and secret
    material is never returned.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest |
            ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse]
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
    body: ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest | ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest,
    idempotency_key: str,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse | None:
    """ Create a paused event source

     Creates a customer webhook source in the paused state. delivery.kind must be webhook; integration
    sources are connection-managed. Verification credentials are referenced from Vault and secret
    material is never returned.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest |
            ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse
     """


    return sync_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest | ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest,
    idempotency_key: str,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse]:
    """ Create a paused event source

     Creates a customer webhook source in the paused state. delivery.kind must be webhook; integration
    sources are connection-managed. Verification credentials are referenced from Vault and secret
    material is never returned.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest |
            ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse]
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
    body: ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest | ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest,
    idempotency_key: str,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse | None:
    """ Create a paused event source

     Creates a customer webhook source in the paused state. delivery.kind must be webhook; integration
    sources are connection-managed. Verification credentials are referenced from Vault and secret
    material is never returned.

    Args:
        idempotency_key (str): Replay-protection key in an organization-wide namespace shared by
            keyed mutations. It must contain 1 to 256 visible ASCII characters and be sent as exactly
            one header value. Request identity is the exact HTTP method, escaped path, raw query, and
            raw body bytes. The same request replays the original successful response; any different
            request returns 409 idempotency_conflict, and an active matching request returns 409
            idempotency_in_progress. Completed receipts are retained for approximately 24 hours,
            pending claims may be reclaimed after approximately 1 hour, and no deduplication is
            guaranteed after expiry.
        body (ManagedAgentsGithubEventSourceRequest | ManagedAgentsHmacCustomEventSourceRequest |
            ManagedAgentsSlackEventSourceRequest | ManagedAgentsUnsignedCustomEventSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorConflict | ManagedAgentsApiErrorIdempotencyConflict | ManagedAgentsApiErrorIdempotencyInProgress | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorIdempotencyUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorPayloadTooLarge | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSemanticValidationFailed | ManagedAgentsApiErrorUnauthorized | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventSourceResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
