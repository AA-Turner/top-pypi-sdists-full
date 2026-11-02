"""Scripted bulk update utility -- POST /internal/opensearch/_bulk_update

Send arbitrary Painless scripted updates to OpenSearch documents through
the octostar-api.  When ``do_not_update_before`` is provided, the server
wraps the script with a guard that noops stale updates.
"""

import httpx
from typing import Any, Dict, List, Optional, TypedDict, Union

from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


class ScriptedUpdateDict(TypedDict, total=False):
    entity_id: str  # required
    script_source: str  # required
    script_params: Dict[str, Any]
    do_not_update_before: str


def sync(
    updates: List[Union[ScriptedUpdateDict, Dict[str, Any]]],
    timeout: Optional[float] = 60.0,
    client: Optional[Client] = None,
) -> Dict[str, Any]:
    """Send scripted bulk updates to OpenSearch through octostar-api.

    Args:
        updates: List of update dicts.  Each must contain ``entity_id`` and
            ``script_source``.  Optionally ``script_params`` and
            ``do_not_update_before``.
        timeout: HTTP timeout in seconds.
        client: Octostar client.  Falls back to the default client.

    Returns:
        Dict with ``status``, ``updated``, ``nooped_entity_ids``, ``errors``.

    Raises:
        ApiConnectionError: If the request fails.
    """
    if not updates:
        return {
            "status": "success",
            "updated": 0,
            "nooped_entity_ids": [],
            "errors": [],
        }
    if not client:
        client = get_default_client()

    endpoint_url = f"{client.get_base_url_v1()}/internal/opensearch/_bulk_update"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    json_body = [dict(u) for u in updates]

    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client() as httpx_client:
                    response = httpx_client.post(
                        endpoint_url,
                        json=json_body,
                        headers=headers,
                        timeout=timeout,
                    )
                    if response.status_code != 200:
                        raise ConnectionError(
                            f"bulk_update failed (status {response.status_code}): "
                            + str(response.content)
                        )
                    return response.json()
    except Exception:
        raise ApiConnectionError("bulk_update", response, client)


async def asyncio(
    updates: List[Union[ScriptedUpdateDict, Dict[str, Any]]],
    timeout: Optional[float] = 60.0,
    client: Optional[Client] = None,
) -> Dict[str, Any]:
    """Send scripted bulk updates to OpenSearch through octostar-api (async).

    Args:
        updates: List of update dicts.  Each must contain ``entity_id`` and
            ``script_source``.  Optionally ``script_params`` and
            ``do_not_update_before``.
        timeout: HTTP timeout in seconds.
        client: Octostar client.  Falls back to the default client.

    Returns:
        Dict with ``status``, ``updated``, ``nooped_entity_ids``, ``errors``.

    Raises:
        ApiConnectionError: If the request fails.
    """
    if not updates:
        return {
            "status": "success",
            "updated": 0,
            "nooped_entity_ids": [],
            "errors": [],
        }
    if not client:
        client = get_default_client()

    endpoint_url = f"{client.get_base_url_v1()}/internal/opensearch/_bulk_update"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.token}",
        "x-ontology": client.ontology,
    }
    json_body = [dict(u) for u in updates]

    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient() as httpx_client:
                    response = await httpx_client.post(
                        endpoint_url,
                        json=json_body,
                        headers=headers,
                        timeout=timeout,
                    )
                    if response.status_code != 200:
                        raise ConnectionError(
                            f"bulk_update failed (status {response.status_code}): "
                            + str(response.content)
                        )
                    return response.json()
    except Exception:
        raise ApiConnectionError("bulk_update", response, client)
