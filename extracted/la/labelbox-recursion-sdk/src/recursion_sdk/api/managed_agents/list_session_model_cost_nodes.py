from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_session_model_cost_nodes_scope import ListSessionModelCostNodesScope
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_session_model_cost_node_list_response import ManagedAgentsSessionModelCostNodeListResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    scope: ListSessionModelCostNodesScope | Unset = ListSessionModelCostNodesScope.SELF,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,
    model_cost_snapshot_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_scope: str | Unset = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    params["limit"] = limit

    params["page_token"] = page_token

    params["model_cost_snapshot_token"] = model_cost_snapshot_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/{session_id}/costs/sessions".format(session_id=quote(str(session_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionModelCostNodeListResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse]:
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
    scope: ListSessionModelCostNodesScope | Unset = ListSessionModelCostNodesScope.SELF,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,
    model_cost_snapshot_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse]:
    """ Page session nodes and scoped model-cost summaries without loading events

    Args:
        session_id (UUID): Session id (UUID) the cost read is scoped to. Any id in the tree; scope
            decides how far the read reaches from it.
        scope (ListSessionModelCostNodesScope | Unset): self selects only this session; subtree
            selects this session and descendants; tree selects the complete root tree. Default:
            ListSessionModelCostNodesScope.SELF.
        limit (int | Unset):  Default: 50.
        page_token (str | Unset): Signed, organization/session/scope/limit/snapshot-bound
            continuation token.
        model_cost_snapshot_token (str | Unset): Signed token returned by a model-cost detail
            page. Pins this companion read to the exact same organization/session/scope snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
scope=scope,
limit=limit,
page_token=page_token,
model_cost_snapshot_token=model_cost_snapshot_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    scope: ListSessionModelCostNodesScope | Unset = ListSessionModelCostNodesScope.SELF,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,
    model_cost_snapshot_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse | None:
    """ Page session nodes and scoped model-cost summaries without loading events

    Args:
        session_id (UUID): Session id (UUID) the cost read is scoped to. Any id in the tree; scope
            decides how far the read reaches from it.
        scope (ListSessionModelCostNodesScope | Unset): self selects only this session; subtree
            selects this session and descendants; tree selects the complete root tree. Default:
            ListSessionModelCostNodesScope.SELF.
        limit (int | Unset):  Default: 50.
        page_token (str | Unset): Signed, organization/session/scope/limit/snapshot-bound
            continuation token.
        model_cost_snapshot_token (str | Unset): Signed token returned by a model-cost detail
            page. Pins this companion read to the exact same organization/session/scope snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse
     """


    return sync_detailed(
        session_id=session_id,
client=client,
scope=scope,
limit=limit,
page_token=page_token,
model_cost_snapshot_token=model_cost_snapshot_token,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    scope: ListSessionModelCostNodesScope | Unset = ListSessionModelCostNodesScope.SELF,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,
    model_cost_snapshot_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse]:
    """ Page session nodes and scoped model-cost summaries without loading events

    Args:
        session_id (UUID): Session id (UUID) the cost read is scoped to. Any id in the tree; scope
            decides how far the read reaches from it.
        scope (ListSessionModelCostNodesScope | Unset): self selects only this session; subtree
            selects this session and descendants; tree selects the complete root tree. Default:
            ListSessionModelCostNodesScope.SELF.
        limit (int | Unset):  Default: 50.
        page_token (str | Unset): Signed, organization/session/scope/limit/snapshot-bound
            continuation token.
        model_cost_snapshot_token (str | Unset): Signed token returned by a model-cost detail
            page. Pins this companion read to the exact same organization/session/scope snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
scope=scope,
limit=limit,
page_token=page_token,
model_cost_snapshot_token=model_cost_snapshot_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    scope: ListSessionModelCostNodesScope | Unset = ListSessionModelCostNodesScope.SELF,
    limit: int | Unset = 50,
    page_token: str | Unset = UNSET,
    model_cost_snapshot_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse | None:
    """ Page session nodes and scoped model-cost summaries without loading events

    Args:
        session_id (UUID): Session id (UUID) the cost read is scoped to. Any id in the tree; scope
            decides how far the read reaches from it.
        scope (ListSessionModelCostNodesScope | Unset): self selects only this session; subtree
            selects this session and descendants; tree selects the complete root tree. Default:
            ListSessionModelCostNodesScope.SELF.
        limit (int | Unset):  Default: 50.
        page_token (str | Unset): Signed, organization/session/scope/limit/snapshot-bound
            continuation token.
        model_cost_snapshot_token (str | Unset): Signed token returned by a model-cost detail
            page. Pins this companion read to the exact same organization/session/scope snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionModelCostNodeListResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
scope=scope,
limit=limit,
page_token=page_token,
model_cost_snapshot_token=model_cost_snapshot_token,

    )).parsed
