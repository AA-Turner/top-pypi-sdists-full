from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_automation_runs_status import ListAutomationRunsStatus
from ...models.list_automation_runs_trigger_type import ListAutomationRunsTriggerType
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
from ...models.managed_agents_automation_definition_run_page_response import ManagedAgentsAutomationDefinitionRunPageResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    *,
    automation_id: UUID | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    event_source_id: UUID | Unset = UNSET,
    trigger_type: ListAutomationRunsTriggerType | Unset = UNSET,
    status: ListAutomationRunsStatus | Unset = UNSET,
    created_at_gte: datetime.datetime | Unset = UNSET,
    created_at_lt: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_automation_id: str | Unset = UNSET
    if not isinstance(automation_id, Unset):
        json_automation_id = str(automation_id)
    params["automationId"] = json_automation_id

    json_trigger_id: str | Unset = UNSET
    if not isinstance(trigger_id, Unset):
        json_trigger_id = str(trigger_id)
    params["triggerId"] = json_trigger_id

    json_event_source_id: str | Unset = UNSET
    if not isinstance(event_source_id, Unset):
        json_event_source_id = str(event_source_id)
    params["eventSourceId"] = json_event_source_id

    json_trigger_type: str | Unset = UNSET
    if not isinstance(trigger_type, Unset):
        json_trigger_type = trigger_type.value

    params["triggerType"] = json_trigger_type

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    json_created_at_gte: str | Unset = UNSET
    if not isinstance(created_at_gte, Unset):
        json_created_at_gte = created_at_gte.isoformat()
    params["createdAtGte"] = json_created_at_gte

    json_created_at_lt: str | Unset = UNSET
    if not isinstance(created_at_lt, Unset):
        json_created_at_lt = created_at_lt.isoformat()
    params["createdAtLt"] = json_created_at_lt

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/automation-runs",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsAutomationDefinitionRunPageResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    automation_id: UUID | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    event_source_id: UUID | Unset = UNSET,
    trigger_type: ListAutomationRunsTriggerType | Unset = UNSET,
    status: ListAutomationRunsStatus | Unset = UNSET,
    created_at_gte: datetime.datetime | Unset = UNSET,
    created_at_lt: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse]:
    """ List canonical automation runs

     Returns a snapshot-consistent page of canonical automation runs. Filters combine with AND and
    continuation cursors bind organization, normalized filters, order, and the exact database read
    timestamp.

    Args:
        automation_id (UUID | Unset): Narrow to one automation.
        trigger_id (UUID | Unset): Narrow to one stored trigger. Manual runs have no trigger id.
        event_source_id (UUID | Unset): Narrow to one event source.
        trigger_type (ListAutomationRunsTriggerType | Unset): Narrow to one admission kind.
        status (ListAutomationRunsStatus | Unset): Narrow to one session-creation outcome.
        created_at_gte (datetime.datetime | Unset): Only runs recorded at or after this RFC 3339
            instant.
        created_at_lt (datetime.datetime | Unset): Only runs recorded before this RFC 3339
            instant.
        limit (int | Unset): Maximum run records to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            normalized filters and limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse]
     """


    kwargs = _get_kwargs(
        automation_id=automation_id,
trigger_id=trigger_id,
event_source_id=event_source_id,
trigger_type=trigger_type,
status=status,
created_at_gte=created_at_gte,
created_at_lt=created_at_lt,
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
    automation_id: UUID | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    event_source_id: UUID | Unset = UNSET,
    trigger_type: ListAutomationRunsTriggerType | Unset = UNSET,
    status: ListAutomationRunsStatus | Unset = UNSET,
    created_at_gte: datetime.datetime | Unset = UNSET,
    created_at_lt: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse | None:
    """ List canonical automation runs

     Returns a snapshot-consistent page of canonical automation runs. Filters combine with AND and
    continuation cursors bind organization, normalized filters, order, and the exact database read
    timestamp.

    Args:
        automation_id (UUID | Unset): Narrow to one automation.
        trigger_id (UUID | Unset): Narrow to one stored trigger. Manual runs have no trigger id.
        event_source_id (UUID | Unset): Narrow to one event source.
        trigger_type (ListAutomationRunsTriggerType | Unset): Narrow to one admission kind.
        status (ListAutomationRunsStatus | Unset): Narrow to one session-creation outcome.
        created_at_gte (datetime.datetime | Unset): Only runs recorded at or after this RFC 3339
            instant.
        created_at_lt (datetime.datetime | Unset): Only runs recorded before this RFC 3339
            instant.
        limit (int | Unset): Maximum run records to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            normalized filters and limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse
     """


    return sync_detailed(
        client=client,
automation_id=automation_id,
trigger_id=trigger_id,
event_source_id=event_source_id,
trigger_type=trigger_type,
status=status,
created_at_gte=created_at_gte,
created_at_lt=created_at_lt,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    automation_id: UUID | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    event_source_id: UUID | Unset = UNSET,
    trigger_type: ListAutomationRunsTriggerType | Unset = UNSET,
    status: ListAutomationRunsStatus | Unset = UNSET,
    created_at_gte: datetime.datetime | Unset = UNSET,
    created_at_lt: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse]:
    """ List canonical automation runs

     Returns a snapshot-consistent page of canonical automation runs. Filters combine with AND and
    continuation cursors bind organization, normalized filters, order, and the exact database read
    timestamp.

    Args:
        automation_id (UUID | Unset): Narrow to one automation.
        trigger_id (UUID | Unset): Narrow to one stored trigger. Manual runs have no trigger id.
        event_source_id (UUID | Unset): Narrow to one event source.
        trigger_type (ListAutomationRunsTriggerType | Unset): Narrow to one admission kind.
        status (ListAutomationRunsStatus | Unset): Narrow to one session-creation outcome.
        created_at_gte (datetime.datetime | Unset): Only runs recorded at or after this RFC 3339
            instant.
        created_at_lt (datetime.datetime | Unset): Only runs recorded before this RFC 3339
            instant.
        limit (int | Unset): Maximum run records to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            normalized filters and limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse]
     """


    kwargs = _get_kwargs(
        automation_id=automation_id,
trigger_id=trigger_id,
event_source_id=event_source_id,
trigger_type=trigger_type,
status=status,
created_at_gte=created_at_gte,
created_at_lt=created_at_lt,
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
    automation_id: UUID | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    event_source_id: UUID | Unset = UNSET,
    trigger_type: ListAutomationRunsTriggerType | Unset = UNSET,
    status: ListAutomationRunsStatus | Unset = UNSET,
    created_at_gte: datetime.datetime | Unset = UNSET,
    created_at_lt: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse | None:
    """ List canonical automation runs

     Returns a snapshot-consistent page of canonical automation runs. Filters combine with AND and
    continuation cursors bind organization, normalized filters, order, and the exact database read
    timestamp.

    Args:
        automation_id (UUID | Unset): Narrow to one automation.
        trigger_id (UUID | Unset): Narrow to one stored trigger. Manual runs have no trigger id.
        event_source_id (UUID | Unset): Narrow to one event source.
        trigger_type (ListAutomationRunsTriggerType | Unset): Narrow to one admission kind.
        status (ListAutomationRunsStatus | Unset): Narrow to one session-creation outcome.
        created_at_gte (datetime.datetime | Unset): Only runs recorded at or after this RFC 3339
            instant.
        created_at_lt (datetime.datetime | Unset): Only runs recorded before this RFC 3339
            instant.
        limit (int | Unset): Maximum run records to return. Defaults to 50. Default: 50.
        cursor (str | Unset): Opaque cursor from nextCursor. Pass it unchanged with the same
            normalized filters and limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsAutomationDefinitionRunPageResponse
     """


    return (await asyncio_detailed(
        client=client,
automation_id=automation_id,
trigger_id=trigger_id,
event_source_id=event_source_id,
trigger_type=trigger_type,
status=status,
created_at_gte=created_at_gte,
created_at_lt=created_at_lt,
limit=limit,
cursor=cursor,

    )).parsed
