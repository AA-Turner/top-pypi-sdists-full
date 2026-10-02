from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.built_in_synthesizer_dto import BuiltInSynthesizerDto
from ...models.get_built_in_built_in_synthesizer_key import GetBuiltInBuiltInSynthesizerKey
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast
from uuid import UUID



def _get_kwargs(
    environment_id: UUID,
    built_in_synthesizer_key: GetBuiltInBuiltInSynthesizerKey,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/environments/{environment_id}/built-in-synthesizers/{built_in_synthesizer_key}".format(environment_id=quote(str(environment_id), safe=""),built_in_synthesizer_key=quote(str(built_in_synthesizer_key), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = BuiltInSynthesizerDto.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = TargetApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = TargetApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = TargetApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = TargetApiErrorNotFound.from_dict(response.json())



        return response_404

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    built_in_synthesizer_key: GetBuiltInBuiltInSynthesizerKey,
    *,
    client: AuthenticatedClient | Client,

) -> Response[BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Get a hardcoded built-in synthesizer by key

     Built-in synthesizers live in code and apply to every environment; the path environment only scopes
    the caller.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        built_in_synthesizer_key (GetBuiltInBuiltInSynthesizerKey): Stable string key identifying
            a hardcoded built-in synthesizer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
built_in_synthesizer_key=built_in_synthesizer_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    built_in_synthesizer_key: GetBuiltInBuiltInSynthesizerKey,
    *,
    client: AuthenticatedClient | Client,

) -> BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Get a hardcoded built-in synthesizer by key

     Built-in synthesizers live in code and apply to every environment; the path environment only scopes
    the caller.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        built_in_synthesizer_key (GetBuiltInBuiltInSynthesizerKey): Stable string key identifying
            a hardcoded built-in synthesizer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_id=environment_id,
built_in_synthesizer_key=built_in_synthesizer_key,
client=client,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    built_in_synthesizer_key: GetBuiltInBuiltInSynthesizerKey,
    *,
    client: AuthenticatedClient | Client,

) -> Response[BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Get a hardcoded built-in synthesizer by key

     Built-in synthesizers live in code and apply to every environment; the path environment only scopes
    the caller.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        built_in_synthesizer_key (GetBuiltInBuiltInSynthesizerKey): Stable string key identifying
            a hardcoded built-in synthesizer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
built_in_synthesizer_key=built_in_synthesizer_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    built_in_synthesizer_key: GetBuiltInBuiltInSynthesizerKey,
    *,
    client: AuthenticatedClient | Client,

) -> BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Get a hardcoded built-in synthesizer by key

     Built-in synthesizers live in code and apply to every environment; the path environment only scopes
    the caller.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        built_in_synthesizer_key (GetBuiltInBuiltInSynthesizerKey): Stable string key identifying
            a hardcoded built-in synthesizer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuiltInSynthesizerDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
built_in_synthesizer_key=built_in_synthesizer_key,
client=client,

    )).parsed
