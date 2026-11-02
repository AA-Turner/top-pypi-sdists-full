import os
from typing import List, Union
import logging

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from . import get_files_tree


def sync(
    os_workspace: Union[List[str], str],
    os_entity_uids: List[str],
    raise_on_missing: bool = True,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get the full filepath of an Octostar workspace filesystem object (os_wsfs_object) from its ID

    ## Arguments
    - `os_workspace`: The workspace ID the objects belongs to, or a list of IDs (one per object)
    - `os_entity_uids`: The IDs of the objects
    - `raise_on_missing`: Whether to raise a ValueError if some objects are missing
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A List of paths as Strings (if the object exists) or None, in the same order as the input ids

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ValueError`: If the objects do not exist in the given workspace(s)
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
    res = list(filter(lambda x: x["os_entity_uid"] in os_entity_uids, tree))
    res = {r["os_entity_uid"]: r["#path"] for r in res}
    if raise_on_missing and set(res.keys()) != set(os_entity_uids):
        raise ValueError("Some of the objects do not exist!")
    ordered_res = []
    for id in os_entity_uids:
        ordered_res.append(res.get(id, None))
    return ordered_res


async def asyncio(
    os_workspace: Union[List[str], str],
    os_entity_uids: List[str],
    raise_on_missing: bool = True,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get asynchronously the full filepath of an Octostar workspace filesystem object (os_wsfs_object) from its ID

    ## Arguments
    - `os_workspace`: The workspace ID the objects belongs to, or a list of IDs (one per object)
    - `os_entity_uids`: The IDs of the objects
    - `raise_on_missing`: Whether to raise a ValueError if some objects are missing
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A List of paths as Strings (if the object exists) or None, in the same order as the input ids

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ValueError`: If the objects do not exist in the given workspace(s)
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
    res = list(filter(lambda x: x["os_entity_uid"] in os_entity_uids, tree))
    res = {r["os_entity_uid"]: r["#path"] for r in res}
    if raise_on_missing and set(res.keys()) != set(os_entity_uids):
        raise ValueError("Some of the objects do not exist!")
    ordered_res = []
    for id in os_entity_uids:
        ordered_res.append(res.get(id, None))
    return ordered_res
