import os
from typing import List
import logging

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from . import get_files_tree


def sync(
    os_workspace: str,
    full_filenames: List[str],
    raise_on_missing: bool = True,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get the full entry of a workspace filesystem object (os_wsfs_object) given its full filepath

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `full_filename`: The full filepath of the object in the workspace, as a String
    - `raise_on_missing`: Whether to raise a ValueError if some objects are missing
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A List of dictionaries, each containing the object data (if the object exists) or None,
    in the order given by the full filename

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
    tree = get_files_tree.sync(
        os_workspace, recurse=True, flat=True, minimal=True, client=client
    )
    if not tree or len(tree) == 0:
        raise ValueError("Could not fetch workspace items or workspace is empty!")
    res = list(filter(lambda x: x["#path"] in full_filenames, tree))
    res = {
        r["#path"]: r for r in res
    }  # this assumes there's only one file per filename
    if raise_on_missing and set(res.keys()) != set(full_filenames):
        raise ValueError("Some of the filenames do not exist!")
    ordered_res = []
    for path in full_filenames:
        ordered_res.append(res.get(path, None))
    return ordered_res


async def asyncio(
    os_workspace: str,
    full_filenames: List[str],
    raise_on_missing: bool = True,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Get asynchronously the full entry of a workspace filesystem object (os_wsfs_object) given its full filepath

    ## Arguments
    - `os_workspace`: The workspace ID the object belongs to
    - `full_filename`: The full filepath of the object in the workspace, as a String
    - `raise_on_missing`: Whether to raise a ValueError if some objects are missing
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A List of dictionaries, each containing the object data (if the object exists) or None,
    in the order given by the full filename

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
    res = list(filter(lambda x: x["#path"] in full_filenames, tree))
    res = {
        r["#path"]: r for r in res
    }  # this assumes there's only one file per filename
    if raise_on_missing and set(res.keys()) != set(full_filenames):
        raise ValueError("Some of the filenames do not exist!")
    ordered_res = []
    for path in full_filenames:
        ordered_res.append(res.get(path, None))
    return ordered_res
