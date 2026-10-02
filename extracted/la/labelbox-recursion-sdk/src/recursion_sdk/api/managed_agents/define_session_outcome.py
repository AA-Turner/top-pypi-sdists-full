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
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_define_outcome_request import ManagedAgentsDefineOutcomeRequest
from ...models.managed_agents_outcome import ManagedAgentsOutcome
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    body: ManagedAgentsDefineOutcomeRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/sessions/{session_id}/outcomes".format(session_id=quote(str(session_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsOutcome.from_dict(response.json())



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

    if response.status_code == 404:
        response_404 = ManagedAgentsApiError.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = ManagedAgentsApiError.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = ManagedAgentsApiError.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsDefineOutcomeRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome]:
    """ Define what done looks like for a session

     Defines what done looks like for an existing session and returns the stored outcome. Outcomes chain
    rather than run concurrently: the request is rejected while the session still has a non-terminal
    outcome, so define the next one only after the previous is graded.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsDefineOutcomeRequest): A definition of done for a session -- the task
            plus the rubric it is graded against. Accepted both when starting a session and when
            adding an outcome to a running one. Exactly one of rubric and rubric_ref is required.
            Example: {'description': 'Export the product catalog to /out/catalog.csv', 'rubric': '-
            /out/catalog.csv exists\\n- The CSV has a header row with sku, name, and price columns\\n-
            Every price value is a number'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsDefineOutcomeRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome | None:
    """ Define what done looks like for a session

     Defines what done looks like for an existing session and returns the stored outcome. Outcomes chain
    rather than run concurrently: the request is rejected while the session still has a non-terminal
    outcome, so define the next one only after the previous is graded.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsDefineOutcomeRequest): A definition of done for a session -- the task
            plus the rubric it is graded against. Accepted both when starting a session and when
            adding an outcome to a running one. Exactly one of rubric and rubric_ref is required.
            Example: {'description': 'Export the product catalog to /out/catalog.csv', 'rubric': '-
            /out/catalog.csv exists\\n- The CSV has a header row with sku, name, and price columns\\n-
            Every price value is a number'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome
     """


    return sync_detailed(
        session_id=session_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsDefineOutcomeRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome]:
    """ Define what done looks like for a session

     Defines what done looks like for an existing session and returns the stored outcome. Outcomes chain
    rather than run concurrently: the request is rejected while the session still has a non-terminal
    outcome, so define the next one only after the previous is graded.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsDefineOutcomeRequest): A definition of done for a session -- the task
            plus the rubric it is graded against. Accepted both when starting a session and when
            adding an outcome to a running one. Exactly one of rubric and rubric_ref is required.
            Example: {'description': 'Export the product catalog to /out/catalog.csv', 'rubric': '-
            /out/catalog.csv exists\\n- The CSV has a header row with sku, name, and price columns\\n-
            Every price value is a number'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsDefineOutcomeRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome | None:
    """ Define what done looks like for a session

     Defines what done looks like for an existing session and returns the stored outcome. Outcomes chain
    rather than run concurrently: the request is rejected while the session still has a non-terminal
    outcome, so define the next one only after the previous is graded.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsDefineOutcomeRequest): A definition of done for a session -- the task
            plus the rubric it is graded against. Accepted both when starting a session and when
            adding an outcome to a running one. Exactly one of rubric and rubric_ref is required.
            Example: {'description': 'Export the product catalog to /out/catalog.csv', 'rubric': '-
            /out/catalog.csv exists\\n- The CSV has a header row with sku, name, and price columns\\n-
            Every price value is a number'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsOutcome
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,

    )).parsed
