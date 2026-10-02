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
from ...models.managed_agents_compute_offering_list_response import ManagedAgentsComputeOfferingListResponse
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/compute-offerings",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsComputeOfferingListResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse]:
    """ List compute catalog and live offerings

     Returns the stable deployment-configured accelerator catalog plus optional live machine offerings.
    Configured accelerator choices remain present when provider telemetry is stale or unavailable; quota
    evidence is an administrative ceiling and never claims physical stock. Live offerings describe the
    CPU, memory, accelerator, capacity confidence, and approximate hourly price of each reported shape.
    When the runner cannot be read, a deployment with a configured catalog answers 200 with
    telemetry_unavailable and stale evidence; one without answers 503 compute_offerings_unavailable.
    This is deployment capability, identical for every organization, and provisions nothing. Reachable
    with an API key through this API, which authorizes the caller and then calls the upstream service
    with its own credential. The upstream operation is not callable with a customer key directly.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse | None:
    """ List compute catalog and live offerings

     Returns the stable deployment-configured accelerator catalog plus optional live machine offerings.
    Configured accelerator choices remain present when provider telemetry is stale or unavailable; quota
    evidence is an administrative ceiling and never claims physical stock. Live offerings describe the
    CPU, memory, accelerator, capacity confidence, and approximate hourly price of each reported shape.
    When the runner cannot be read, a deployment with a configured catalog answers 200 with
    telemetry_unavailable and stale evidence; one without answers 503 compute_offerings_unavailable.
    This is deployment capability, identical for every organization, and provisions nothing. Reachable
    with an API key through this API, which authorizes the caller and then calls the upstream service
    with its own credential. The upstream operation is not callable with a customer key directly.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse]:
    """ List compute catalog and live offerings

     Returns the stable deployment-configured accelerator catalog plus optional live machine offerings.
    Configured accelerator choices remain present when provider telemetry is stale or unavailable; quota
    evidence is an administrative ceiling and never claims physical stock. Live offerings describe the
    CPU, memory, accelerator, capacity confidence, and approximate hourly price of each reported shape.
    When the runner cannot be read, a deployment with a configured catalog answers 200 with
    telemetry_unavailable and stale evidence; one without answers 503 compute_offerings_unavailable.
    This is deployment capability, identical for every organization, and provisions nothing. Reachable
    with an API key through this API, which authorizes the caller and then calls the upstream service
    with its own credential. The upstream operation is not callable with a customer key directly.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse | None:
    """ List compute catalog and live offerings

     Returns the stable deployment-configured accelerator catalog plus optional live machine offerings.
    Configured accelerator choices remain present when provider telemetry is stale or unavailable; quota
    evidence is an administrative ceiling and never claims physical stock. Live offerings describe the
    CPU, memory, accelerator, capacity confidence, and approximate hourly price of each reported shape.
    When the runner cannot be read, a deployment with a configured catalog answers 200 with
    telemetry_unavailable and stale evidence; one without answers 503 compute_offerings_unavailable.
    This is deployment capability, identical for every organization, and provisions nothing. Reachable
    with an API key through this API, which authorizes the caller and then calls the upstream service
    with its own credential. The upstream operation is not callable with a customer key directly.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsComputeOfferingListResponse
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
