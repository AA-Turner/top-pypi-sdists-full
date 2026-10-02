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
from ...models.managed_agents_session_metadata_values_response import ManagedAgentsSessionMetadataValuesResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    key: str,
    q: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["key"] = key

    params["q"] = q

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/metadata-values",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionMetadataValuesResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    key: str,
    q: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse]:
    """ List the values one caller-defined metadata key takes

     Returns the distinct values of one caller-defined metadata key across every session the caller may
    list, sorted and optionally narrowed to a case-sensitive prefix with q, for a typeahead over
    listSessions metadata filters. Sessions the caller's access policy hides contribute nothing. A key
    no session carries returns an empty list rather than an error. When more values match than limit
    allows, truncated is true: narrow q instead of paging.

    Args:
        key (str): The caller-defined metadata key whose values to list. Same alphabet as on
            startSession: letters, digits, '_', '.', and '-', up to 64 characters.
        q (str | Unset): Case-sensitive prefix the returned values must start with, up to 512
            characters. Omit to list every value up to limit.
        limit (int | Unset): Most distinct values to return. When more match, truncated is true;
            narrow q rather than asking for more. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse]
     """


    kwargs = _get_kwargs(
        key=key,
q=q,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    key: str,
    q: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse | None:
    """ List the values one caller-defined metadata key takes

     Returns the distinct values of one caller-defined metadata key across every session the caller may
    list, sorted and optionally narrowed to a case-sensitive prefix with q, for a typeahead over
    listSessions metadata filters. Sessions the caller's access policy hides contribute nothing. A key
    no session carries returns an empty list rather than an error. When more values match than limit
    allows, truncated is true: narrow q instead of paging.

    Args:
        key (str): The caller-defined metadata key whose values to list. Same alphabet as on
            startSession: letters, digits, '_', '.', and '-', up to 64 characters.
        q (str | Unset): Case-sensitive prefix the returned values must start with, up to 512
            characters. Omit to list every value up to limit.
        limit (int | Unset): Most distinct values to return. When more match, truncated is true;
            narrow q rather than asking for more. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse
     """


    return sync_detailed(
        client=client,
key=key,
q=q,
limit=limit,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    key: str,
    q: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse]:
    """ List the values one caller-defined metadata key takes

     Returns the distinct values of one caller-defined metadata key across every session the caller may
    list, sorted and optionally narrowed to a case-sensitive prefix with q, for a typeahead over
    listSessions metadata filters. Sessions the caller's access policy hides contribute nothing. A key
    no session carries returns an empty list rather than an error. When more values match than limit
    allows, truncated is true: narrow q instead of paging.

    Args:
        key (str): The caller-defined metadata key whose values to list. Same alphabet as on
            startSession: letters, digits, '_', '.', and '-', up to 64 characters.
        q (str | Unset): Case-sensitive prefix the returned values must start with, up to 512
            characters. Omit to list every value up to limit.
        limit (int | Unset): Most distinct values to return. When more match, truncated is true;
            narrow q rather than asking for more. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse]
     """


    kwargs = _get_kwargs(
        key=key,
q=q,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    key: str,
    q: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse | None:
    """ List the values one caller-defined metadata key takes

     Returns the distinct values of one caller-defined metadata key across every session the caller may
    list, sorted and optionally narrowed to a case-sensitive prefix with q, for a typeahead over
    listSessions metadata filters. Sessions the caller's access policy hides contribute nothing. A key
    no session carries returns an empty list rather than an error. When more values match than limit
    allows, truncated is true: narrow q instead of paging.

    Args:
        key (str): The caller-defined metadata key whose values to list. Same alphabet as on
            startSession: letters, digits, '_', '.', and '-', up to 64 characters.
        q (str | Unset): Case-sensitive prefix the returned values must start with, up to 512
            characters. Omit to list every value up to limit.
        limit (int | Unset): Most distinct values to return. When more match, truncated is true;
            narrow q rather than asking for more. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionMetadataValuesResponse
     """


    return (await asyncio_detailed(
        client=client,
key=key,
q=q,
limit=limit,

    )).parsed
