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
from ...models.managed_agents_tag import ManagedAgentsTag
from ...models.managed_agents_update_tag_request import ManagedAgentsUpdateTagRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    tag_id: UUID,
    *,
    body: ManagedAgentsUpdateTagRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/managed-agents/v1/tags/{tag_id}".format(tag_id=quote(str(tag_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsTag.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tag_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTagRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag]:
    """ Update a tag definition

     Changes a tag's label, color, or description without changing any application. This does not update
    an agent, mint an AgentVersion, or affect a running session.

    Args:
        tag_id (UUID): Tag id (UUID) as returned by createTag or listTags.
        body (ManagedAgentsUpdateTagRequest): Request body for changing a tag definition. Every
            field is optional and tag applications remain unchanged. Example: {'color': '#14b8a6',
            'description': 'example', 'label': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag]
     """


    kwargs = _get_kwargs(
        tag_id=tag_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    tag_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTagRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag | None:
    """ Update a tag definition

     Changes a tag's label, color, or description without changing any application. This does not update
    an agent, mint an AgentVersion, or affect a running session.

    Args:
        tag_id (UUID): Tag id (UUID) as returned by createTag or listTags.
        body (ManagedAgentsUpdateTagRequest): Request body for changing a tag definition. Every
            field is optional and tag applications remain unchanged. Example: {'color': '#14b8a6',
            'description': 'example', 'label': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag
     """


    return sync_detailed(
        tag_id=tag_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    tag_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTagRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag]:
    """ Update a tag definition

     Changes a tag's label, color, or description without changing any application. This does not update
    an agent, mint an AgentVersion, or affect a running session.

    Args:
        tag_id (UUID): Tag id (UUID) as returned by createTag or listTags.
        body (ManagedAgentsUpdateTagRequest): Request body for changing a tag definition. Every
            field is optional and tag applications remain unchanged. Example: {'color': '#14b8a6',
            'description': 'example', 'label': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag]
     """


    kwargs = _get_kwargs(
        tag_id=tag_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    tag_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsUpdateTagRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag | None:
    """ Update a tag definition

     Changes a tag's label, color, or description without changing any application. This does not update
    an agent, mint an AgentVersion, or affect a running session.

    Args:
        tag_id (UUID): Tag id (UUID) as returned by createTag or listTags.
        body (ManagedAgentsUpdateTagRequest): Request body for changing a tag definition. Every
            field is optional and tag applications remain unchanged. Example: {'color': '#14b8a6',
            'description': 'example', 'label': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsTag
     """


    return (await asyncio_detailed(
        tag_id=tag_id,
client=client,
body=body,

    )).parsed
