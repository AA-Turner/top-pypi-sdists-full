"""Get processing status endpoint - POST /api/v1/pipeline/processing-status/get

Requires x-ontology header to specify which ontology/index to query.
"""

from http import HTTPStatus
from typing import Any, Dict, List, Optional
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response
from ... import errors


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    entity_ids: List[str],
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/pipeline/processing-status/get".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_body: Dict[str, Any] = {
        "entity_ids": entity_ids,
    }

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_body,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    if response.status_code == HTTPStatus.OK:
        return response.json()
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client = None,
    entity_ids: List[str],
) -> Response[Dict[str, Any]]:
    """Get processing status for entities.

    Note: Requires x-ontology header to be set on the client.

    The persisted recursive rollup is always returned in-line as
    ``detailed_status`` per entity (when the debounced rollup job has
    written it). There is no separate "ask for recursive numbers" knob.

    Args:
        client: The client to use for the request (must have x-ontology header set).
        entity_ids: List of entity IDs to retrieve status for.

    Returns:
        Response with status and data dict mapping entity_id -> status or None.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(client=client, entity_ids=entity_ids)
    response = httpx.request(verify=client.verify_ssl, **kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client = None,
    entity_ids: List[str],
) -> Optional[Dict[str, Any]]:
    """Get processing status for entities.

    Note: Requires x-ontology header to be set on the client.

    The persisted recursive rollup is always returned in-line as
    ``detailed_status`` per entity (when the debounced rollup job has
    written it). There is no separate "ask for recursive numbers" knob.

    Args:
        client: The client to use for the request (must have x-ontology header set).
        entity_ids: List of entity IDs to retrieve status for.

    Returns:
        Response dict with status and data.
    """
    return sync_detailed(client=client, entity_ids=entity_ids).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    entity_ids: List[str],
) -> Response[Dict[str, Any]]:
    """Get processing status for entities (async).

    Note: Requires x-ontology header to be set on the client.

    The persisted recursive rollup is always returned in-line as
    ``detailed_status`` per entity (when the debounced rollup job has
    written it). There is no separate "ask for recursive numbers" knob.

    Args:
        client: The client to use for the request (must have x-ontology header set).
        entity_ids: List of entity IDs to retrieve status for.

    Returns:
        Response with status and data dict.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(client=client, entity_ids=entity_ids)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    entity_ids: List[str],
) -> Optional[Dict[str, Any]]:
    """Get processing status for entities (async).

    Note: Requires x-ontology header to be set on the client.

    The persisted recursive rollup is always returned in-line as
    ``detailed_status`` per entity (when the debounced rollup job has
    written it). There is no separate "ask for recursive numbers" knob.

    Args:
        client: The client to use for the request (must have x-ontology header set).
        entity_ids: List of entity IDs to retrieve status for.

    Returns:
        Response dict with status and data.
    """
    return (await asyncio_detailed(client=client, entity_ids=entity_ids)).parsed
