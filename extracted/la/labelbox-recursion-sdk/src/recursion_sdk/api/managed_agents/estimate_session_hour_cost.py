from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.estimate_session_hour_cost_workload import EstimateSessionHourCostWorkload
from ...models.managed_agents_api_error_auth_unavailable import ManagedAgentsApiErrorAuthUnavailable
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
from ...models.managed_agents_session_hour_estimate import ManagedAgentsSessionHourEstimate
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    model: str,
    agent_id: str | Unset = UNSET,
    workload: EstimateSessionHourCostWorkload | Unset = EstimateSessionHourCostWorkload.INTERACTIVE,
    cpu_milli: int | Unset = 0,
    memory_mib: int | Unset = 0,
    accelerator: str | Unset = UNSET,
    accelerator_count: int | Unset = 0,
    spot: bool | Unset = False,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["model"] = model

    params["agentId"] = agent_id

    json_workload: str | Unset = UNSET
    if not isinstance(workload, Unset):
        json_workload = workload.value

    params["workload"] = json_workload

    params["cpuMilli"] = cpu_milli

    params["memoryMib"] = memory_mib

    params["accelerator"] = accelerator

    params["acceleratorCount"] = accelerator_count

    params["spot"] = spot


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/cost-estimates/session-hour",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionHourEstimate.from_dict(response.json())



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
        def _parse_response_503(data: object) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_0 = ManagedAgentsApiErrorAuthUnavailable.from_dict(data)



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    model: str,
    agent_id: str | Unset = UNSET,
    workload: EstimateSessionHourCostWorkload | Unset = EstimateSessionHourCostWorkload.INTERACTIVE,
    cpu_milli: int | Unset = 0,
    memory_mib: int | Unset = 0,
    accelerator: str | Unset = UNSET,
    accelerator_count: int | Unset = 0,
    spot: bool | Unset = False,

) -> Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate]:
    """ Estimate the cost of one session hour

     Estimates what one hour of a session costs the calling organization for a model and compute shape:
    the compute price plus the model's spend while active times how much of a session the agent is
    active. Every amount is billed cost, i.e. raw cost with the organization's current markup. The
    active rate comes from the organization's own recent sessions of the model when there are enough,
    otherwise from sessions pooled across organizations (or a prior, or a list-price scaling of a known
    model); utilization comes from the agent's own history when agentId has enough completed sessions,
    otherwise from the workload prior. Bands are 25th/50th/75th percentiles. Served from an in-memory
    snapshot refreshed in the background; provisions nothing. Reachable with an API key through this
    API, which authorizes the caller and then calls the upstream service with its own credential. The
    upstream operation is not callable with a customer key directly.

    Args:
        model (str): Model id as stored on the agent, for example litellm:anthropic/claude-
            sonnet-5.
        agent_id (str | Unset): Existing agent whose completed sessions set the utilization. Omit
            for a new agent.
        workload (EstimateSessionHourCostWorkload | Unset): Utilization prior when the agent has
            no history: interactive (waits on a person) or autonomous. Default:
            EstimateSessionHourCostWorkload.INTERACTIVE.
        cpu_milli (int | Unset): Requested sandbox CPU in millicores; 0 prices no CPU. Default: 0.
        memory_mib (int | Unset): Requested sandbox memory in MiB; 0 prices no memory. Default: 0.
        accelerator (str | Unset): Accelerator model name, for example l4 or a100. Omit for a CPU-
            only shape.
        accelerator_count (int | Unset): Accelerator count; 0 means 1 when accelerator is set.
            Default: 0.
        spot (bool | Unset): Price the shape at spot rates. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate]
     """


    kwargs = _get_kwargs(
        model=model,
agent_id=agent_id,
workload=workload,
cpu_milli=cpu_milli,
memory_mib=memory_mib,
accelerator=accelerator,
accelerator_count=accelerator_count,
spot=spot,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    model: str,
    agent_id: str | Unset = UNSET,
    workload: EstimateSessionHourCostWorkload | Unset = EstimateSessionHourCostWorkload.INTERACTIVE,
    cpu_milli: int | Unset = 0,
    memory_mib: int | Unset = 0,
    accelerator: str | Unset = UNSET,
    accelerator_count: int | Unset = 0,
    spot: bool | Unset = False,

) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate | None:
    """ Estimate the cost of one session hour

     Estimates what one hour of a session costs the calling organization for a model and compute shape:
    the compute price plus the model's spend while active times how much of a session the agent is
    active. Every amount is billed cost, i.e. raw cost with the organization's current markup. The
    active rate comes from the organization's own recent sessions of the model when there are enough,
    otherwise from sessions pooled across organizations (or a prior, or a list-price scaling of a known
    model); utilization comes from the agent's own history when agentId has enough completed sessions,
    otherwise from the workload prior. Bands are 25th/50th/75th percentiles. Served from an in-memory
    snapshot refreshed in the background; provisions nothing. Reachable with an API key through this
    API, which authorizes the caller and then calls the upstream service with its own credential. The
    upstream operation is not callable with a customer key directly.

    Args:
        model (str): Model id as stored on the agent, for example litellm:anthropic/claude-
            sonnet-5.
        agent_id (str | Unset): Existing agent whose completed sessions set the utilization. Omit
            for a new agent.
        workload (EstimateSessionHourCostWorkload | Unset): Utilization prior when the agent has
            no history: interactive (waits on a person) or autonomous. Default:
            EstimateSessionHourCostWorkload.INTERACTIVE.
        cpu_milli (int | Unset): Requested sandbox CPU in millicores; 0 prices no CPU. Default: 0.
        memory_mib (int | Unset): Requested sandbox memory in MiB; 0 prices no memory. Default: 0.
        accelerator (str | Unset): Accelerator model name, for example l4 or a100. Omit for a CPU-
            only shape.
        accelerator_count (int | Unset): Accelerator count; 0 means 1 when accelerator is set.
            Default: 0.
        spot (bool | Unset): Price the shape at spot rates. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate
     """


    return sync_detailed(
        client=client,
model=model,
agent_id=agent_id,
workload=workload,
cpu_milli=cpu_milli,
memory_mib=memory_mib,
accelerator=accelerator,
accelerator_count=accelerator_count,
spot=spot,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    model: str,
    agent_id: str | Unset = UNSET,
    workload: EstimateSessionHourCostWorkload | Unset = EstimateSessionHourCostWorkload.INTERACTIVE,
    cpu_milli: int | Unset = 0,
    memory_mib: int | Unset = 0,
    accelerator: str | Unset = UNSET,
    accelerator_count: int | Unset = 0,
    spot: bool | Unset = False,

) -> Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate]:
    """ Estimate the cost of one session hour

     Estimates what one hour of a session costs the calling organization for a model and compute shape:
    the compute price plus the model's spend while active times how much of a session the agent is
    active. Every amount is billed cost, i.e. raw cost with the organization's current markup. The
    active rate comes from the organization's own recent sessions of the model when there are enough,
    otherwise from sessions pooled across organizations (or a prior, or a list-price scaling of a known
    model); utilization comes from the agent's own history when agentId has enough completed sessions,
    otherwise from the workload prior. Bands are 25th/50th/75th percentiles. Served from an in-memory
    snapshot refreshed in the background; provisions nothing. Reachable with an API key through this
    API, which authorizes the caller and then calls the upstream service with its own credential. The
    upstream operation is not callable with a customer key directly.

    Args:
        model (str): Model id as stored on the agent, for example litellm:anthropic/claude-
            sonnet-5.
        agent_id (str | Unset): Existing agent whose completed sessions set the utilization. Omit
            for a new agent.
        workload (EstimateSessionHourCostWorkload | Unset): Utilization prior when the agent has
            no history: interactive (waits on a person) or autonomous. Default:
            EstimateSessionHourCostWorkload.INTERACTIVE.
        cpu_milli (int | Unset): Requested sandbox CPU in millicores; 0 prices no CPU. Default: 0.
        memory_mib (int | Unset): Requested sandbox memory in MiB; 0 prices no memory. Default: 0.
        accelerator (str | Unset): Accelerator model name, for example l4 or a100. Omit for a CPU-
            only shape.
        accelerator_count (int | Unset): Accelerator count; 0 means 1 when accelerator is set.
            Default: 0.
        spot (bool | Unset): Price the shape at spot rates. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate]
     """


    kwargs = _get_kwargs(
        model=model,
agent_id=agent_id,
workload=workload,
cpu_milli=cpu_milli,
memory_mib=memory_mib,
accelerator=accelerator,
accelerator_count=accelerator_count,
spot=spot,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    model: str,
    agent_id: str | Unset = UNSET,
    workload: EstimateSessionHourCostWorkload | Unset = EstimateSessionHourCostWorkload.INTERACTIVE,
    cpu_milli: int | Unset = 0,
    memory_mib: int | Unset = 0,
    accelerator: str | Unset = UNSET,
    accelerator_count: int | Unset = 0,
    spot: bool | Unset = False,

) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate | None:
    """ Estimate the cost of one session hour

     Estimates what one hour of a session costs the calling organization for a model and compute shape:
    the compute price plus the model's spend while active times how much of a session the agent is
    active. Every amount is billed cost, i.e. raw cost with the organization's current markup. The
    active rate comes from the organization's own recent sessions of the model when there are enough,
    otherwise from sessions pooled across organizations (or a prior, or a list-price scaling of a known
    model); utilization comes from the agent's own history when agentId has enough completed sessions,
    otherwise from the workload prior. Bands are 25th/50th/75th percentiles. Served from an in-memory
    snapshot refreshed in the background; provisions nothing. Reachable with an API key through this
    API, which authorizes the caller and then calls the upstream service with its own credential. The
    upstream operation is not callable with a customer key directly.

    Args:
        model (str): Model id as stored on the agent, for example litellm:anthropic/claude-
            sonnet-5.
        agent_id (str | Unset): Existing agent whose completed sessions set the utilization. Omit
            for a new agent.
        workload (EstimateSessionHourCostWorkload | Unset): Utilization prior when the agent has
            no history: interactive (waits on a person) or autonomous. Default:
            EstimateSessionHourCostWorkload.INTERACTIVE.
        cpu_milli (int | Unset): Requested sandbox CPU in millicores; 0 prices no CPU. Default: 0.
        memory_mib (int | Unset): Requested sandbox memory in MiB; 0 prices no memory. Default: 0.
        accelerator (str | Unset): Accelerator model name, for example l4 or a100. Omit for a CPU-
            only shape.
        accelerator_count (int | Unset): Accelerator count; 0 means 1 when accelerator is set.
            Default: 0.
        spot (bool | Unset): Price the shape at spot rates. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSessionHourEstimate
     """


    return (await asyncio_detailed(
        client=client,
model=model,
agent_id=agent_id,
workload=workload,
cpu_milli=cpu_milli,
memory_mib=memory_mib,
accelerator=accelerator,
accelerator_count=accelerator_count,
spot=spot,

    )).parsed
