from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_503 import ApiErrorStatus503
from ...models.create_customer_secret_dto import CreateCustomerSecretDto
from ...models.customer_secret_dto import CustomerSecretDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast



def _get_kwargs(
    *,
    body: CreateCustomerSecretDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/customer-secrets",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = CustomerSecretDto.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = TargetApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = TargetApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = TargetApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 429:
        response_429 = TargetApiErrorRateLimitExceeded.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        def _parse_response_500(data: object) -> TargetApiErrorInternalError | TargetApiErrorInvariantViolation:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_500_type_0 = TargetApiErrorInternalError.from_dict(data)



                return response_500_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_500_type_1 = TargetApiErrorInvariantViolation.from_dict(data)



            return response_500_type_1

        response_500 = _parse_response_500(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = ApiErrorStatus503.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateCustomerSecretDto,

) -> Response[ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create a customer secret at a scope

    Args:
        body (CreateCustomerSecretDto): Request body for creating a customer secret. Carries the
            credential value and metadata; the value is stored securely and never returned again.
            Example: {'scope': {'level': 'env', 'id': '784e2386-e297-4f9d-a886-838422383b65'}, 'name':
            'ANTHROPIC_API_KEY', 'injectionMode': 'proxy', 'upstreamHost': 'api.anthropic.com',
            'headerName': 'x-api-key', 'value': 'paste your real Anthropic API key here'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateCustomerSecretDto,

) -> ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create a customer secret at a scope

    Args:
        body (CreateCustomerSecretDto): Request body for creating a customer secret. Carries the
            credential value and metadata; the value is stored securely and never returned again.
            Example: {'scope': {'level': 'env', 'id': '784e2386-e297-4f9d-a886-838422383b65'}, 'name':
            'ANTHROPIC_API_KEY', 'injectionMode': 'proxy', 'upstreamHost': 'api.anthropic.com',
            'headerName': 'x-api-key', 'value': 'paste your real Anthropic API key here'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateCustomerSecretDto,

) -> Response[ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create a customer secret at a scope

    Args:
        body (CreateCustomerSecretDto): Request body for creating a customer secret. Carries the
            credential value and metadata; the value is stored securely and never returned again.
            Example: {'scope': {'level': 'env', 'id': '784e2386-e297-4f9d-a886-838422383b65'}, 'name':
            'ANTHROPIC_API_KEY', 'injectionMode': 'proxy', 'upstreamHost': 'api.anthropic.com',
            'headerName': 'x-api-key', 'value': 'paste your real Anthropic API key here'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateCustomerSecretDto,

) -> ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create a customer secret at a scope

    Args:
        body (CreateCustomerSecretDto): Request body for creating a customer secret. Carries the
            credential value and metadata; the value is stored securely and never returned again.
            Example: {'scope': {'level': 'env', 'id': '784e2386-e297-4f9d-a886-838422383b65'}, 'name':
            'ANTHROPIC_API_KEY', 'injectionMode': 'proxy', 'upstreamHost': 'api.anthropic.com',
            'headerName': 'x-api-key', 'value': 'paste your real Anthropic API key here'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus503 | CustomerSecretDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
