import asyncio as _asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
from urllib.parse import quote

import httpx

_logger = logging.getLogger(__name__)

from ...api.workspace_data import delete_entities
from ..ontology import query_ontology
from ...client import Client
from ..exceptions import ApiConnectionError


def _files_delete_url(client: Client, os_workspace: str, os_entity_uid: str) -> str:
    base = client.get_base_url_v1()
    return f"{base}/api/v1/files/delete-file/{quote(os_workspace, safe='')}/{quote(os_entity_uid, safe='')}"


def _query_survivors_sync(os_entity_uids: List[str], client: Client) -> Dict[str, str]:
    """Return {entity_uid: os_workspace} for every UID that still exists."""
    uids_text = ", ".join(f"'{uid}'" for uid in os_entity_uids)
    rows = (
        query_ontology.sync(
            f"SELECT `os_entity_uid`, `os_workspace` FROM `timbr`.`os_workspace_item` WHERE `os_entity_uid` IN ({uids_text})",
            client=client,
        )
        or []
    )
    return {
        row["os_entity_uid"]: row["os_workspace"]
        for row in rows
        if row.get("os_entity_uid") and row.get("os_workspace")
    }


async def _query_survivors_async(
    os_entity_uids: List[str], client: Client
) -> Dict[str, str]:
    """Return {entity_uid: os_workspace} for every UID that still exists."""
    uids_text = ", ".join(f"'{uid}'" for uid in os_entity_uids)
    rows = (
        await query_ontology.asyncio(
            f"SELECT `os_entity_uid`, `os_workspace` FROM `timbr`.`os_workspace_item` WHERE `os_entity_uid` IN ({uids_text})",
            client=client,
        )
        or []
    )
    return {
        row["os_entity_uid"]: row["os_workspace"]
        for row in rows
        if row.get("os_entity_uid") and row.get("os_workspace")
    }


def _files_delete_one_sync(
    os_workspace: str, os_entity_uid: str, client: Client
) -> bool:
    """DELETE /api/v1/files/delete-file/{os_workspace}/{entity_uid}. Returns True on 204, False on 404."""
    url = _files_delete_url(client, os_workspace, os_entity_uid)
    with httpx.Client(verify=client.verify_ssl) as httpx_client:
        resp = httpx_client.delete(
            url,
            headers=client.get_headers(),
            timeout=client.get_timeout(),
            follow_redirects=client.follow_redirects,
        )
    if resp.status_code == 204:
        return True
    if resp.status_code == 404:
        return False
    raise ApiConnectionError("delete_entities (files fallback)", resp, client)


async def _files_delete_one_async(
    os_workspace: str, os_entity_uid: str, client: Client
) -> bool:
    """DELETE /api/v1/files/delete-file/{os_workspace}/{entity_uid}. Returns True on 204, False on 404."""
    url = _files_delete_url(client, os_workspace, os_entity_uid)
    async with httpx.AsyncClient(verify=client.verify_ssl) as httpx_client:
        resp = await httpx_client.delete(
            url,
            headers=client.get_headers(),
            timeout=client.get_timeout(),
            follow_redirects=client.follow_redirects,
        )
    if resp.status_code == 204:
        return True
    if resp.status_code == 404:
        return False
    raise ApiConnectionError("delete_entities (files fallback)", resp, client)


def sync(
    os_entity_uids: List[str],
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete a list of local entities given their IDs

    ## Arguments
    - `os_entity_uids`: The list of IDs
    - `safe`: Whether to raise a ValueError before removal if some entities in the list do not exist
    - `raise_on_missing`: Whether to raise a ConnectionError if some of the entities could not be deleted
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The number of successfully deleted entities

    ## Raises
    - `ValueError`: If the list of IDs contain invalid entries (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If some of the entities could not be removed (and raise_on_missing is enabled)
    """
    assert len(os_entity_uids) > 0
    if safe:
        uids_text = ", ".join(f"'{uid}'" for uid in os_entity_uids)
        uids = query_ontology.sync(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_thing` WHERE `os_entity_uid` IN ({uids_text})",
            client=client,
        )
        if len(uids or []) < len(os_entity_uids):
            raise ValueError("Attempting to remove an entity which does not exist!")

    response = delete_entities.sync_detailed(json_body=os_entity_uids, client=client)
    if response.status_code != 200:
        raise ApiConnectionError("delete_entities", response, client)
    deleted = response.parsed.additional_properties.get("deleted_count", 0)

    if deleted >= len(os_entity_uids):
        return deleted

    # v1/entities/delete silently ignores certain entity types. Query for any survivors and fall back to the
    # v1/files/delete-file endpoint in parallel, which handles the remaining entity types.
    survivors = _query_survivors_sync(os_entity_uids, client)
    if not survivors:
        total = deleted
        if total < len(os_entity_uids):
            _logger.warning("Deleted only %d/%d entities", total, len(os_entity_uids))
            if raise_on_missing:
                raise ConnectionError(
                    "Failed to delete some entities! (likely they did not exist prior to this call)"
                )
        return total

    files_deleted = 0
    max_workers = min(len(survivors), 10)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_files_delete_one_sync, ws, uid, client): uid
            for uid, ws in survivors.items()
        }
        for future in as_completed(futures):
            uid = futures[future]
            try:
                if future.result():
                    files_deleted += 1
            except Exception as e:
                _logger.error("files fallback delete failed for %s: %s", uid, e)

    total = deleted + files_deleted
    if total < len(os_entity_uids):
        _logger.warning("Deleted only %d/%d entities", total, len(os_entity_uids))
        if raise_on_missing:
            raise ConnectionError(
                "Failed to delete some entities! (likely they did not exist prior to this call)"
            )
    return total


async def asyncio(
    os_entity_uids: List[str],
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete asynchronously a list of local entities given their IDs

    ## Arguments
    (Same as sync function)

    ## Returns
    The number of successfully deleted entities

    ## Raises
    - `ValueError`: If the list of IDs contain invalid entries (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If some of the entities could not be removed (and raise_on_missing is enabled)
    """
    assert len(os_entity_uids) > 0
    if safe:
        uids_text = ", ".join(f"'{uid}'" for uid in os_entity_uids)
        uids = await query_ontology.asyncio(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_thing` WHERE `os_entity_uid` IN ({uids_text})",
            client=client,
        )
        if len(uids or []) < len(os_entity_uids):
            raise ValueError("Attempting to remove an entity which does not exist!")

    response = await delete_entities.asyncio_detailed(
        json_body=os_entity_uids, client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("delete_entities", response, client)
    deleted = response.parsed.additional_properties.get("deleted_count", 0)

    if deleted >= len(os_entity_uids):
        return deleted

    # v1/entities/delete silently ignores certain entity types. Query for any survivors and fall back to the
    # v1/files/delete-file endpoint in parallel, which handles the remaining entity types.
    survivors = await _query_survivors_async(os_entity_uids, client)
    if not survivors:
        total = deleted
        if total < len(os_entity_uids):
            _logger.warning("Deleted only %d/%d entities", total, len(os_entity_uids))
            if raise_on_missing:
                raise ConnectionError(
                    "Failed to delete some entities! (likely they did not exist prior to this call)"
                )
        return total

    results = await _asyncio.gather(
        *[_files_delete_one_async(ws, uid, client) for uid, ws in survivors.items()],
        return_exceptions=True,
    )

    files_deleted = 0
    for uid, result in zip(survivors.keys(), results):
        if isinstance(result, Exception):
            _logger.error("files fallback delete failed for %s: %s", uid, result)
        elif result:
            files_deleted += 1

    total = deleted + files_deleted
    if total < len(os_entity_uids):
        _logger.warning("Deleted only %d/%d entities", total, len(os_entity_uids))
        if raise_on_missing:
            raise ConnectionError(
                "Failed to delete some entities! (likely they did not exist prior to this call)"
            )
    return total
