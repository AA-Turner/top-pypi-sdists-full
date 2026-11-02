import logging

_logger = logging.getLogger(__name__)

from ..ontology import query_ontology
from ...client import Client
from . import delete_entities as _delete_entities


def sync(
    os_relationship_uid: str,
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete a local relationship between two entities given its ID

    ## Arguments
    - `os_relationship_uid`: The ID of the relationship to delete
    - `safe`: Whether to raise a ValueError before removal if the relationship does not exist
    - `raise_on_missing`: Whether to raise a ConnectionError if the relationship could not be deleted
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    True if the relationship was successfully deleted, False if no relationship was deleted

    ## Raises
    - `ValueError`: If the ID is not a valid relationship ID (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If the relationship could not be removed (and raise_on_missing is enabled)
    """
    if safe:
        uids = query_ontology.sync(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_relationship` WHERE `os_entity_uid`='{os_relationship_uid}'",
            client=client,
        )
        if not uids:
            raise ValueError("Attempting to remove an entity which does not exist!")

    deleted = _delete_entities.sync(
        [os_relationship_uid], raise_on_missing=raise_on_missing, client=client
    )
    return deleted >= 1


async def asyncio(
    os_relationship_uid: str,
    safe: bool = False,
    raise_on_missing: bool = False,
    client: Client = None,
):
    """
    # Delete asynchronously a local relationship between two entities given its ID

    ## Arguments
    (Same as sync function)

    ## Returns
    True if the relationship was successfully deleted, False if no relationship was deleted

    ## Raises
    - `ValueError`: If the ID is not a valid relationship ID (and safe is enabled)
    - `ApiConnectionError`: If the request was unsuccessful on the server
    - `ConnectionError`: If the relationship could not be removed (and raise_on_missing is enabled)
    """
    if safe:
        uids = await query_ontology.asyncio(
            f"SELECT `os_entity_uid` FROM `timbr`.`os_relationship` WHERE `os_entity_uid`='{os_relationship_uid}'",
            client=client,
        )
        if not uids:
            raise ValueError("Attempting to remove an entity which does not exist!")

    deleted = await _delete_entities.asyncio(
        [os_relationship_uid], raise_on_missing=raise_on_missing, client=client
    )
    return deleted >= 1
