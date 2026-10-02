from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_sessions_evaluation_result import ListSessionsEvaluationResult
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_session_list_response import ManagedAgentsSessionListResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    status: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    agent_id: str | Unset = UNSET,
    tag_ids: str | Unset = UNSET,
    external_source_type: str | Unset = UNSET,
    external_source_id: str | Unset = UNSET,
    metadata: list[str] | Unset = UNSET,
    metadata_key: list[str] | Unset = UNSET,
    root_only: bool | Unset = UNSET,
    needs_user: bool | Unset = UNSET,
    evaluation_result: ListSessionsEvaluationResult | Unset = UNSET,
    limit: int | Unset = 100,
    page_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["status"] = status

    params["kind"] = kind

    params["agent_id"] = agent_id

    params["tag_ids"] = tag_ids

    params["external_source_type"] = external_source_type

    params["external_source_id"] = external_source_id

    json_metadata: list[str] | Unset = UNSET
    if not isinstance(metadata, Unset):
        json_metadata = metadata


    params["metadata"] = json_metadata

    json_metadata_key: list[str] | Unset = UNSET
    if not isinstance(metadata_key, Unset):
        json_metadata_key = metadata_key


    params["metadata_key"] = json_metadata_key

    params["root_only"] = root_only

    params["needs_user"] = needs_user

    json_evaluation_result: str | Unset = UNSET
    if not isinstance(evaluation_result, Unset):
        json_evaluation_result = evaluation_result.value

    params["evaluation_result"] = json_evaluation_result

    params["limit"] = limit

    params["page_token"] = page_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionListResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    status: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    agent_id: str | Unset = UNSET,
    tag_ids: str | Unset = UNSET,
    external_source_type: str | Unset = UNSET,
    external_source_id: str | Unset = UNSET,
    metadata: list[str] | Unset = UNSET,
    metadata_key: list[str] | Unset = UNSET,
    root_only: bool | Unset = UNSET,
    needs_user: bool | Unset = UNSET,
    evaluation_result: ListSessionsEvaluationResult | Unset = UNSET,
    limit: int | Unset = 100,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse]:
    """ List sessions

     Returns sessions in the calling organization, most recent first, filtered by any combination of
    status, kind, agent_id, current agent tag_ids, and external source. kind accepts a comma-separated
    list, while tag_ids uses AND semantics. Capped by limit (default 100, max 1000) rather than cursor-
    paginated.

    Args:
        status (str | Unset): Filter by session status.
        kind (str | Unset): Filter by session kind. Accepts a comma-separated list
            (kind=chat,api_call) to match any of several kinds, which is how a caller selects agent
            sessions without RL rollouts. Session analyst conversations (kind session_analyst) are
            listed only when this filter names that kind.
        agent_id (str | Unset): Filter by agent id.
        tag_ids (str | Unset): Comma-separated current agent tag ids, with at most 32 distinct
            ids. A session row's agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404. Tags are resolved at read time, not from the session
            snapshot.
        external_source_type (str | Unset):
        external_source_id (str | Unset):
        metadata (list[str] | Unset): Exact-match filter on caller-defined session metadata as
            key:value, split at the first colon. Repeat the parameter to require several pairs; a
            session's root must carry every one (AND semantics). Children of a matching root match
            too, so combine with root_only to list only the roots.
        metadata_key (list[str] | Unset): Require the root session to carry this caller-defined
            metadata key with any value. Repeatable; every listed key must be present.
        root_only (bool | Unset): Return only root sessions. Use this for model-cost list rows so
            children cannot consume the bounded page before their tree root.
        needs_user (bool | Unset): Return only root sessions whose active browser handoff is
            awaiting a person (not already being driven or resolved). Applied before ordering and
            pagination.
        evaluation_result (ListSessionsEvaluationResult | Unset): Filter root sessions by their
            newest immutable evaluation verdict before pagination. evaluated matches any verdict; none
            matches sessions with no evaluation.
        limit (int | Unset): Page size. When more rows match, the response carries
            next_page_token; pass it back as page_token with the same filters and limit to read the
            next page. Default: 100.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization and to the exact filters and limit it was
            issued for; valid for one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse]
     """


    kwargs = _get_kwargs(
        status=status,
kind=kind,
agent_id=agent_id,
tag_ids=tag_ids,
external_source_type=external_source_type,
external_source_id=external_source_id,
metadata=metadata,
metadata_key=metadata_key,
root_only=root_only,
needs_user=needs_user,
evaluation_result=evaluation_result,
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
    status: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    agent_id: str | Unset = UNSET,
    tag_ids: str | Unset = UNSET,
    external_source_type: str | Unset = UNSET,
    external_source_id: str | Unset = UNSET,
    metadata: list[str] | Unset = UNSET,
    metadata_key: list[str] | Unset = UNSET,
    root_only: bool | Unset = UNSET,
    needs_user: bool | Unset = UNSET,
    evaluation_result: ListSessionsEvaluationResult | Unset = UNSET,
    limit: int | Unset = 100,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse | None:
    """ List sessions

     Returns sessions in the calling organization, most recent first, filtered by any combination of
    status, kind, agent_id, current agent tag_ids, and external source. kind accepts a comma-separated
    list, while tag_ids uses AND semantics. Capped by limit (default 100, max 1000) rather than cursor-
    paginated.

    Args:
        status (str | Unset): Filter by session status.
        kind (str | Unset): Filter by session kind. Accepts a comma-separated list
            (kind=chat,api_call) to match any of several kinds, which is how a caller selects agent
            sessions without RL rollouts. Session analyst conversations (kind session_analyst) are
            listed only when this filter names that kind.
        agent_id (str | Unset): Filter by agent id.
        tag_ids (str | Unset): Comma-separated current agent tag ids, with at most 32 distinct
            ids. A session row's agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404. Tags are resolved at read time, not from the session
            snapshot.
        external_source_type (str | Unset):
        external_source_id (str | Unset):
        metadata (list[str] | Unset): Exact-match filter on caller-defined session metadata as
            key:value, split at the first colon. Repeat the parameter to require several pairs; a
            session's root must carry every one (AND semantics). Children of a matching root match
            too, so combine with root_only to list only the roots.
        metadata_key (list[str] | Unset): Require the root session to carry this caller-defined
            metadata key with any value. Repeatable; every listed key must be present.
        root_only (bool | Unset): Return only root sessions. Use this for model-cost list rows so
            children cannot consume the bounded page before their tree root.
        needs_user (bool | Unset): Return only root sessions whose active browser handoff is
            awaiting a person (not already being driven or resolved). Applied before ordering and
            pagination.
        evaluation_result (ListSessionsEvaluationResult | Unset): Filter root sessions by their
            newest immutable evaluation verdict before pagination. evaluated matches any verdict; none
            matches sessions with no evaluation.
        limit (int | Unset): Page size. When more rows match, the response carries
            next_page_token; pass it back as page_token with the same filters and limit to read the
            next page. Default: 100.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization and to the exact filters and limit it was
            issued for; valid for one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse
     """


    return sync_detailed(
        client=client,
status=status,
kind=kind,
agent_id=agent_id,
tag_ids=tag_ids,
external_source_type=external_source_type,
external_source_id=external_source_id,
metadata=metadata,
metadata_key=metadata_key,
root_only=root_only,
needs_user=needs_user,
evaluation_result=evaluation_result,
limit=limit,
page_token=page_token,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    status: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    agent_id: str | Unset = UNSET,
    tag_ids: str | Unset = UNSET,
    external_source_type: str | Unset = UNSET,
    external_source_id: str | Unset = UNSET,
    metadata: list[str] | Unset = UNSET,
    metadata_key: list[str] | Unset = UNSET,
    root_only: bool | Unset = UNSET,
    needs_user: bool | Unset = UNSET,
    evaluation_result: ListSessionsEvaluationResult | Unset = UNSET,
    limit: int | Unset = 100,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse]:
    """ List sessions

     Returns sessions in the calling organization, most recent first, filtered by any combination of
    status, kind, agent_id, current agent tag_ids, and external source. kind accepts a comma-separated
    list, while tag_ids uses AND semantics. Capped by limit (default 100, max 1000) rather than cursor-
    paginated.

    Args:
        status (str | Unset): Filter by session status.
        kind (str | Unset): Filter by session kind. Accepts a comma-separated list
            (kind=chat,api_call) to match any of several kinds, which is how a caller selects agent
            sessions without RL rollouts. Session analyst conversations (kind session_analyst) are
            listed only when this filter names that kind.
        agent_id (str | Unset): Filter by agent id.
        tag_ids (str | Unset): Comma-separated current agent tag ids, with at most 32 distinct
            ids. A session row's agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404. Tags are resolved at read time, not from the session
            snapshot.
        external_source_type (str | Unset):
        external_source_id (str | Unset):
        metadata (list[str] | Unset): Exact-match filter on caller-defined session metadata as
            key:value, split at the first colon. Repeat the parameter to require several pairs; a
            session's root must carry every one (AND semantics). Children of a matching root match
            too, so combine with root_only to list only the roots.
        metadata_key (list[str] | Unset): Require the root session to carry this caller-defined
            metadata key with any value. Repeatable; every listed key must be present.
        root_only (bool | Unset): Return only root sessions. Use this for model-cost list rows so
            children cannot consume the bounded page before their tree root.
        needs_user (bool | Unset): Return only root sessions whose active browser handoff is
            awaiting a person (not already being driven or resolved). Applied before ordering and
            pagination.
        evaluation_result (ListSessionsEvaluationResult | Unset): Filter root sessions by their
            newest immutable evaluation verdict before pagination. evaluated matches any verdict; none
            matches sessions with no evaluation.
        limit (int | Unset): Page size. When more rows match, the response carries
            next_page_token; pass it back as page_token with the same filters and limit to read the
            next page. Default: 100.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization and to the exact filters and limit it was
            issued for; valid for one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse]
     """


    kwargs = _get_kwargs(
        status=status,
kind=kind,
agent_id=agent_id,
tag_ids=tag_ids,
external_source_type=external_source_type,
external_source_id=external_source_id,
metadata=metadata,
metadata_key=metadata_key,
root_only=root_only,
needs_user=needs_user,
evaluation_result=evaluation_result,
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
    status: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    agent_id: str | Unset = UNSET,
    tag_ids: str | Unset = UNSET,
    external_source_type: str | Unset = UNSET,
    external_source_id: str | Unset = UNSET,
    metadata: list[str] | Unset = UNSET,
    metadata_key: list[str] | Unset = UNSET,
    root_only: bool | Unset = UNSET,
    needs_user: bool | Unset = UNSET,
    evaluation_result: ListSessionsEvaluationResult | Unset = UNSET,
    limit: int | Unset = 100,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse | None:
    """ List sessions

     Returns sessions in the calling organization, most recent first, filtered by any combination of
    status, kind, agent_id, current agent tag_ids, and external source. kind accepts a comma-separated
    list, while tag_ids uses AND semantics. Capped by limit (default 100, max 1000) rather than cursor-
    paginated.

    Args:
        status (str | Unset): Filter by session status.
        kind (str | Unset): Filter by session kind. Accepts a comma-separated list
            (kind=chat,api_call) to match any of several kinds, which is how a caller selects agent
            sessions without RL rollouts. Session analyst conversations (kind session_analyst) are
            listed only when this filter names that kind.
        agent_id (str | Unset): Filter by agent id.
        tag_ids (str | Unset): Comma-separated current agent tag ids, with at most 32 distinct
            ids. A session row's agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404. Tags are resolved at read time, not from the session
            snapshot.
        external_source_type (str | Unset):
        external_source_id (str | Unset):
        metadata (list[str] | Unset): Exact-match filter on caller-defined session metadata as
            key:value, split at the first colon. Repeat the parameter to require several pairs; a
            session's root must carry every one (AND semantics). Children of a matching root match
            too, so combine with root_only to list only the roots.
        metadata_key (list[str] | Unset): Require the root session to carry this caller-defined
            metadata key with any value. Repeatable; every listed key must be present.
        root_only (bool | Unset): Return only root sessions. Use this for model-cost list rows so
            children cannot consume the bounded page before their tree root.
        needs_user (bool | Unset): Return only root sessions whose active browser handoff is
            awaiting a person (not already being driven or resolved). Applied before ordering and
            pagination.
        evaluation_result (ListSessionsEvaluationResult | Unset): Filter root sessions by their
            newest immutable evaluation verdict before pagination. evaluated matches any verdict; none
            matches sessions with no evaluation.
        limit (int | Unset): Page size. When more rows match, the response carries
            next_page_token; pass it back as page_token with the same filters and limit to read the
            next page. Default: 100.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization and to the exact filters and limit it was
            issued for; valid for one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionListResponse
     """


    return (await asyncio_detailed(
        client=client,
status=status,
kind=kind,
agent_id=agent_id,
tag_ids=tag_ids,
external_source_type=external_source_type,
external_source_id=external_source_id,
metadata=metadata,
metadata_key=metadata_key,
root_only=root_only,
needs_user=needs_user,
evaluation_result=evaluation_result,
limit=limit,
page_token=page_token,

    )).parsed
