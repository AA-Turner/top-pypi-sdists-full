import logging

_logger = logging.getLogger(__name__)

from ..ontology import query_ontology
from ...client import Client
from . import delete_entities as _delete_entities


def sync(
    os_entity_uid: str,
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete a local entity given its ID

    ## Arguments
    - `os_entity_uid`: The ID of the entity to delete
    - `safe`: Whether to raise a ValueError before removal if the entity does not exist
    - `raise_on_missing`: Whether to raise a ConnectionError if the entity could not be deleted
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    True if the entity was successfully deleted, False if no entity was deleted

    ## Raises
    - `ValueError`: If the ID is not a valid entity ID (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If the entity could not be removed (and raise_on_missing is enabled)
    """
    if safe:
        uids = query_ontology.sync(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_thing` WHERE `os_entity_uid`='{os_entity_uid}'",
            client=client,
        )
        if not uids:
            raise ValueError("Attempting to remove an entity which does not exist!")

    deleted = _delete_entities.sync(
        [os_entity_uid], raise_on_missing=raise_on_missing, client=client
    )
    return deleted >= 1


async def asyncio(
    os_entity_uid: str,
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete asynchronously a local entity given its ID

    ## Arguments
    - `os_entity_uid`: The ID of the entity to delete
    - `safe`: Whether to raise a ValueError before removal if the entity does not exist
    - `raise_on_missing`: Whether to raise a ConnectionError if the entity could not be deleted
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    True if the entity was successfully deleted, False if no entity was deleted

    ## Raises
    - `ValueError`: If the ID is not a valid entity ID (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If the entity could not be removed (and raise_on_missing is enabled)
    """
    if safe:
        uids = await query_ontology.asyncio(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_thing` WHERE `os_entity_uid`='{os_entity_uid}'",
            client=client,
        )
        if not uids:
            raise ValueError("Attempting to remove an entity which does not exist!")

    deleted = await _delete_entities.asyncio(
        [os_entity_uid], raise_on_missing=raise_on_missing, client=client
    )
    return deleted >= 1
