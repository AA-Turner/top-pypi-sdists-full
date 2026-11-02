import os
import logging

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from . import get_files_tree


def sync(
    os_workspace: str,
    os_entity_uid: str,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get the full filepath of an Octostar workspace filesystem object (os_wsfs_object) from its ID

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `os_entity_uid`: The object ID
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The full filepath of the object, as a String

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ValueError`: If the object does not exist in the given workspace
    """
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the active ontology!"
        )
    tree = get_files_tree.sync(os_workspace, None, False, True, True, client=client)
    if not tree or len(tree) == 0:
        raise ValueError("Could not fetch workspace items or workspace is empty!")
    res = list(filter(lambda x: x["os_entity_uid"] == os_entity_uid, tree))
    assert len(res) == 1
    return res[0]["#path"]


async def asyncio(
    os_workspace: str,
    os_entity_uid: str,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get asynchronously the full filepath of an Octostar workspace filesystem object (os_wsfs_object) from its ID

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `os_entity_uid`: The object ID
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The full filepath of the object, as a String

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ValueError`: If the object does not exist in the given workspace
    """
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the active ontology!"
        )
    tree = await get_files_tree.asyncio(
        os_workspace, None, False, True, True, client=client
    )
    if not tree or len(tree) == 0:
        raise ValueError("Could not fetch workspace items or workspace is empty!")
    res = list(filter(lambda x: x["os_entity_uid"] == os_entity_uid, tree))
    assert len(res) == 1
    return res[0]["#path"]
