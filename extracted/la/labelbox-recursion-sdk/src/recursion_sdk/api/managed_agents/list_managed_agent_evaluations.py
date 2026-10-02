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
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_evaluation_list_response import ManagedAgentsEvaluationListResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    target_session_id: UUID | Unset = UNSET,
    target_agent_id: UUID | Unset = UNSET,
    evaluator_agent_id: UUID | Unset = UNSET,
    run_session_id: UUID | Unset = UNSET,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_target_session_id: str | Unset = UNSET
    if not isinstance(target_session_id, Unset):
        json_target_session_id = str(target_session_id)
    params["target_session_id"] = json_target_session_id

    json_target_agent_id: str | Unset = UNSET
    if not isinstance(target_agent_id, Unset):
        json_target_agent_id = str(target_agent_id)
    params["target_agent_id"] = json_target_agent_id

    json_evaluator_agent_id: str | Unset = UNSET
    if not isinstance(evaluator_agent_id, Unset):
        json_evaluator_agent_id = str(evaluator_agent_id)
    params["evaluator_agent_id"] = json_evaluator_agent_id

    json_run_session_id: str | Unset = UNSET
    if not isinstance(run_session_id, Unset):
        json_run_session_id = str(run_session_id)
    params["run_session_id"] = json_run_session_id

    params["limit"] = limit

    params["page_token"] = page_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/evaluations",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEvaluationListResponse.from_dict(response.json())



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
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



        return response_404

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    target_session_id: UUID | Unset = UNSET,
    target_agent_id: UUID | Unset = UNSET,
    evaluator_agent_id: UUID | Unset = UNSET,
    run_session_id: UUID | Unset = UNSET,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse]:
    """ List immutable evaluation verdicts

     Returns an organization-scoped, newest-first page of immutable evaluator verdicts. Optional filters
    are combined with AND. Retained same-organization evaluation history remains readable after
    referenced sessions or agents are deleted; unknown and cross-organization references are
    indistinguishable 404 responses.

    Args:
        target_session_id (UUID | Unset): Narrow to one target session. Unknown, deleted-without-
            history, and cross-organization ids return 404.
        target_agent_id (UUID | Unset): Narrow to verdicts for one target agent. Retained same-
            organization history remains readable after deletion.
        evaluator_agent_id (UUID | Unset): Narrow to verdicts produced by one evaluator agent.
            Retained same-organization history remains readable after deletion.
        run_session_id (UUID | Unset): Narrow to one root platform-internal evaluation run.
        limit (int | Unset): Maximum verdicts to return. Defaults to 50. Default: 50.
        page_token (str | Unset): Opaque signed continuation from next_page_token. It is bound to
            this organization, filters, and effective limit and expires after one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse]
     """


    kwargs = _get_kwargs(
        target_session_id=target_session_id,
target_agent_id=target_agent_id,
evaluator_agent_id=evaluator_agent_id,
run_session_id=run_session_id,
limit=limit,
page_token=page_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    target_session_id: UUID | Unset = UNSET,
    target_agent_id: UUID | Unset = UNSET,
    evaluator_agent_id: UUID | Unset = UNSET,
    run_session_id: UUID | Unset = UNSET,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse | None:
    """ List immutable evaluation verdicts

     Returns an organization-scoped, newest-first page of immutable evaluator verdicts. Optional filters
    are combined with AND. Retained same-organization evaluation history remains readable after
    referenced sessions or agents are deleted; unknown and cross-organization references are
    indistinguishable 404 responses.

    Args:
        target_session_id (UUID | Unset): Narrow to one target session. Unknown, deleted-without-
            history, and cross-organization ids return 404.
        target_agent_id (UUID | Unset): Narrow to verdicts for one target agent. Retained same-
            organization history remains readable after deletion.
        evaluator_agent_id (UUID | Unset): Narrow to verdicts produced by one evaluator agent.
            Retained same-organization history remains readable after deletion.
        run_session_id (UUID | Unset): Narrow to one root platform-internal evaluation run.
        limit (int | Unset): Maximum verdicts to return. Defaults to 50. Default: 50.
        page_token (str | Unset): Opaque signed continuation from next_page_token. It is bound to
            this organization, filters, and effective limit and expires after one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse
     """


    return sync_detailed(
        client=client,
target_session_id=target_session_id,
target_agent_id=target_agent_id,
evaluator_agent_id=evaluator_agent_id,
run_session_id=run_session_id,
limit=limit,
page_token=page_token,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    target_session_id: UUID | Unset = UNSET,
    target_agent_id: UUID | Unset = UNSET,
    evaluator_agent_id: UUID | Unset = UNSET,
    run_session_id: UUID | Unset = UNSET,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse]:
    """ List immutable evaluation verdicts

     Returns an organization-scoped, newest-first page of immutable evaluator verdicts. Optional filters
    are combined with AND. Retained same-organization evaluation history remains readable after
    referenced sessions or agents are deleted; unknown and cross-organization references are
    indistinguishable 404 responses.

    Args:
        target_session_id (UUID | Unset): Narrow to one target session. Unknown, deleted-without-
            history, and cross-organization ids return 404.
        target_agent_id (UUID | Unset): Narrow to verdicts for one target agent. Retained same-
            organization history remains readable after deletion.
        evaluator_agent_id (UUID | Unset): Narrow to verdicts produced by one evaluator agent.
            Retained same-organization history remains readable after deletion.
        run_session_id (UUID | Unset): Narrow to one root platform-internal evaluation run.
        limit (int | Unset): Maximum verdicts to return. Defaults to 50. Default: 50.
        page_token (str | Unset): Opaque signed continuation from next_page_token. It is bound to
            this organization, filters, and effective limit and expires after one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse]
     """


    kwargs = _get_kwargs(
        target_session_id=target_session_id,
target_agent_id=target_agent_id,
evaluator_agent_id=evaluator_agent_id,
run_session_id=run_session_id,
limit=limit,
page_token=page_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    target_session_id: UUID | Unset = UNSET,
    target_agent_id: UUID | Unset = UNSET,
    evaluator_agent_id: UUID | Unset = UNSET,
    run_session_id: UUID | Unset = UNSET,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse | None:
    """ List immutable evaluation verdicts

     Returns an organization-scoped, newest-first page of immutable evaluator verdicts. Optional filters
    are combined with AND. Retained same-organization evaluation history remains readable after
    referenced sessions or agents are deleted; unknown and cross-organization references are
    indistinguishable 404 responses.

    Args:
        target_session_id (UUID | Unset): Narrow to one target session. Unknown, deleted-without-
            history, and cross-organization ids return 404.
        target_agent_id (UUID | Unset): Narrow to verdicts for one target agent. Retained same-
            organization history remains readable after deletion.
        evaluator_agent_id (UUID | Unset): Narrow to verdicts produced by one evaluator agent.
            Retained same-organization history remains readable after deletion.
        run_session_id (UUID | Unset): Narrow to one root platform-internal evaluation run.
        limit (int | Unset): Maximum verdicts to return. Defaults to 50. Default: 50.
        page_token (str | Unset): Opaque signed continuation from next_page_token. It is bound to
            this organization, filters, and effective limit and expires after one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationListResponse
     """


    return (await asyncio_detailed(
        client=client,
target_session_id=target_session_id,
target_agent_id=target_agent_id,
evaluator_agent_id=evaluator_agent_id,
run_session_id=run_session_id,
limit=limit,
page_token=page_token,

    )).parsed
