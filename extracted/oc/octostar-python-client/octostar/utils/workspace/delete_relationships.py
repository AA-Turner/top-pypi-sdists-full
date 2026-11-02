import logging
from typing import List

_logger = logging.getLogger(__name__)

from ..ontology import query_ontology
from ...client import Client
from . import delete_entities as _delete_entities


def sync(
    os_relationship_uids: List[str],
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete a list of local relationships given their IDs

    ## Arguments
    - `os_relationships_uids`: The list of IDs
    - `safe`: Whether to raise a ValueError before removal if some relationships in the list do not exist
    - `raise_on_missing`: Whether to raise a ConnectionError if some of the relationships could not be deleted
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The number of successfully deleted relationships

    ## Raises
    - `ValueError`: If the list of IDs contain invalid entries (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If some of the relationships could not be removed (and raise_on_missing is enabled)
    """
    assert len(os_relationship_uids) > 0
    if safe:
        uids_text = ", ".join(f"'{uid}'" for uid in os_relationship_uids)
        uids = query_ontology.sync(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_relationship` WHERE `os_entity_uid` IN ({uids_text})",
            client=client,
        )
        if len(uids or []) < len(os_relationship_uids):
            raise ValueError(
                "Attempting to remove a relationship which does not exist!"
            )

    return _delete_entities.sync(
        os_relationship_uids, raise_on_missing=raise_on_missing, client=client
    )


async def asyncio(
    os_relationship_uids: List[str],
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete asynchronously a list of local relationships given their IDs

    ## Arguments
    (Same as sync function)

    ## Returns
    The number of successfully deleted relationships

    ## Raises
    - `ValueError`: If the list of IDs contain invalid entries (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If some of the relationships could not be removed (and raise_on_missing is enabled)
    """
    assert len(os_relationship_uids) > 0
    if safe:
        uids_text = ", ".join(f"'{uid}'" for uid in os_relationship_uids)
        uids = await query_ontology.asyncio(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_relationship` WHERE `os_entity_uid` IN ({uids_text})",
            client=client,
        )
        if len(uids or []) < len(os_relationship_uids):
            raise ValueError(
                "Attempting to remove a relationship which does not exist!"
            )

    return await _delete_entities.asyncio(
        os_relationship_uids, raise_on_missing=raise_on_missing, client=client
    )
