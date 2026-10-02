from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_internal_error import ManagedAgentsApiErrorInternalError
from ...models.managed_agents_api_error_invalid_request import ManagedAgentsApiErrorInvalidRequest
from ...models.managed_agents_api_error_invariant_violation import ManagedAgentsApiErrorInvariantViolation
from ...models.managed_agents_api_error_managed_agents_unavailable import ManagedAgentsApiErrorManagedAgentsUnavailable
from ...models.managed_agents_api_error_rate_limit_exceeded import ManagedAgentsApiErrorRateLimitExceeded
from ...models.managed_agents_api_error_rate_limited import ManagedAgentsApiErrorRateLimited
from ...models.managed_agents_api_error_service_unavailable import ManagedAgentsApiErrorServiceUnavailable
from ...models.managed_agents_api_error_unauthorized import ManagedAgentsApiErrorUnauthorized
from ...models.managed_agents_event_source_page_response import ManagedAgentsEventSourcePageResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/event-sources",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEventSourcePageResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse]:
    """ List event sources

     Returns a bounded page of non-secret source summaries, newest first. Protocol configuration is
    available only on member reads.

    Args:
        limit (int | Unset): Maximum source summaries to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse]
     """


    kwargs = _get_kwargs(
        limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse | None:
    """ List event sources

     Returns a bounded page of non-secret source summaries, newest first. Protocol configuration is
    available only on member reads.

    Args:
        limit (int | Unset): Maximum source summaries to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse
     """


    return sync_detailed(
        client=client,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse]:
    """ List event sources

     Returns a bounded page of non-secret source summaries, newest first. Protocol configuration is
    available only on member reads.

    Args:
        limit (int | Unset): Maximum source summaries to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse]
     """


    kwargs = _get_kwargs(
        limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse | None:
    """ List event sources

     Returns a bounded page of non-secret source summaries, newest first. Protocol configuration is
    available only on member reads.

    Args:
        limit (int | Unset): Maximum source summaries to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsEventSourcePageResponse
     """


    return (await asyncio_detailed(
        client=client,
limit=limit,
cursor=cursor,

    )).parsed
