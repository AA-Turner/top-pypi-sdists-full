import os
import logging

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from . import get_files_tree


def sync(
    os_workspace: str,
    full_filename: str,
    raise_if_multiple: bool = False,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get the full entry of a workspace filesystem object (os_wsfs_object) given its full filepath

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `full_filename`: The full filepath of the object in the workspace, as a String
    - `raise_if_multiple`: Whether to raise a ValueError if multiple files are found
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A dictionary containing the object data, or a List of such dictionaries if multiple files exist

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ValueError`: If the object does not exist in the given workspace, or if multiple files are found
        when a single one is expected
    """
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the active ontology!"
        )
    tree = get_files_tree.sync(
        os_workspace, recurse=True, flat=True, minimal=True, client=client
    )
    if not tree or len(tree) == 0:
        raise ValueError("Could not fetch workspace items or workspace is empty!")
    res = list(filter(lambda x: x["#path"] == full_filename, tree))
    if not res or len(res) == 0:
        raise ValueError("Could not find item from given filepath!")
    if len(res) == 1:
        res = res[0]
    elif raise_if_multiple:
        raise ValueError("Expected a single file, found " + str(len(res)) + "!")
    return res


async def asyncio(
    os_workspace: str,
    full_filename: str,
    raise_if_multiple: bool = False,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get asynchronously the full entry of a workspace filesystem object (os_wsfs_object) given its full filepath

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `full_filename`: The full filepath of the object in the workspace, as a String
    - `raise_if_multiple`: Whether to raise a ValueError if multiple files are found
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A dictionary containing the object data, or a List of such dictionaries if multiple files exist

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
        os_workspace, recurse=True, flat=True, minimal=True, client=client
    )
    if not tree or len(tree) == 0:
        raise ValueError("Could not fetch workspace items or workspace is empty!")
    res = list(filter(lambda x: x["#path"] == full_filename, tree))
    if not res or len(res) == 0:
        raise ValueError("Could not find item from given filepath!")
    if len(res) == 1:
        res = res[0]
    elif raise_if_multiple:
        raise ValueError("Expected a single file, found " + str(len(res)) + "!")
    return res
