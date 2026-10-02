from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.site_agent_log import SiteAgentLog
from ...models.site_agent_log_create_request import SiteAgentLogCreateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: list["SiteAgentLogCreateRequest"],
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_agent_identity_uuid: Union[Unset, str] = UNSET
    if not isinstance(agent_identity_uuid, Unset):
        json_agent_identity_uuid = str(agent_identity_uuid)
    params["agent_identity_uuid"] = json_agent_identity_uuid

    params["level"] = level

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["timestamp_from"] = timestamp_from

    params["timestamp_to"] = timestamp_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-site-agent-logs/",
        "params": params,
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["SiteAgentLog"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = SiteAgentLog.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["SiteAgentLog"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: list["SiteAgentLogCreateRequest"],
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> Response[list["SiteAgentLog"]]:
    """Push site agent logs

     Receive a batch of log entries from a site agent. Send a list where each entry includes
    agent_identity_uuid.

    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):
        body (list['SiteAgentLogCreateRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SiteAgentLog']]
    """

    kwargs = _get_kwargs(
        body=body,
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: list["SiteAgentLogCreateRequest"],
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> list["SiteAgentLog"]:
    """Push site agent logs

     Receive a batch of log entries from a site agent. Send a list where each entry includes
    agent_identity_uuid.

    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):
        body (list['SiteAgentLogCreateRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SiteAgentLog']
    """

    return sync_detailed(
        client=client,
        body=body,
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: list["SiteAgentLogCreateRequest"],
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> Response[list["SiteAgentLog"]]:
    """Push site agent logs

     Receive a batch of log entries from a site agent. Send a list where each entry includes
    agent_identity_uuid.

    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):
        body (list['SiteAgentLogCreateRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SiteAgentLog']]
    """

    kwargs = _get_kwargs(
        body=body,
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: list["SiteAgentLogCreateRequest"],
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> list["SiteAgentLog"]:
    """Push site agent logs

     Receive a batch of log entries from a site agent. Send a list where each entry includes
    agent_identity_uuid.

    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):
        body (list['SiteAgentLogCreateRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SiteAgentLog']
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            agent_identity_uuid=agent_identity_uuid,
            level=level,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            timestamp_from=timestamp_from,
            timestamp_to=timestamp_to,
        )
    ).parsed
