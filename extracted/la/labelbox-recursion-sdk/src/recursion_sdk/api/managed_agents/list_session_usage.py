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
from ...models.managed_agents_session_usage_list_response import ManagedAgentsSessionUsageListResponse
from typing import cast



def _get_kwargs(
    *,
    session_ids: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["session_ids"] = session_ids


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/usage",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionUsageListResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    session_ids: str,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse]:
    """ Roll up token and cost totals for a batch of sessions

     Rolls up token counts and cost for the sessions named in session_ids and returns one row per
    session. Ids that do not exist in this organization are omitted rather than erroring, so compare the
    row count against what you asked for. The request is rejected if it names more ids than the per-
    request maximum.

    Args:
        session_ids (str): Comma-separated session ids to roll up, matching the ids returned by
            GET /v1/sessions. Ids that do not exist in this organization are omitted from the response
            rather than erroring.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse]
     """


    kwargs = _get_kwargs(
        session_ids=session_ids,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    session_ids: str,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse | None:
    """ Roll up token and cost totals for a batch of sessions

     Rolls up token counts and cost for the sessions named in session_ids and returns one row per
    session. Ids that do not exist in this organization are omitted rather than erroring, so compare the
    row count against what you asked for. The request is rejected if it names more ids than the per-
    request maximum.

    Args:
        session_ids (str): Comma-separated session ids to roll up, matching the ids returned by
            GET /v1/sessions. Ids that do not exist in this organization are omitted from the response
            rather than erroring.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse
     """


    return sync_detailed(
        client=client,
session_ids=session_ids,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    session_ids: str,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse]:
    """ Roll up token and cost totals for a batch of sessions

     Rolls up token counts and cost for the sessions named in session_ids and returns one row per
    session. Ids that do not exist in this organization are omitted rather than erroring, so compare the
    row count against what you asked for. The request is rejected if it names more ids than the per-
    request maximum.

    Args:
        session_ids (str): Comma-separated session ids to roll up, matching the ids returned by
            GET /v1/sessions. Ids that do not exist in this organization are omitted from the response
            rather than erroring.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse]
     """


    kwargs = _get_kwargs(
        session_ids=session_ids,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    session_ids: str,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse | None:
    """ Roll up token and cost totals for a batch of sessions

     Rolls up token counts and cost for the sessions named in session_ids and returns one row per
    session. Ids that do not exist in this organization are omitted rather than erroring, so compare the
    row count against what you asked for. The request is rejected if it names more ids than the per-
    request maximum.

    Args:
        session_ids (str): Comma-separated session ids to roll up, matching the ids returned by
            GET /v1/sessions. Ids that do not exist in this organization are omitted from the response
            rather than erroring.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionUsageListResponse
     """


    return (await asyncio_detailed(
        client=client,
session_ids=session_ids,

    )).parsed
