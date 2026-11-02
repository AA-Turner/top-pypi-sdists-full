import logging
from typing import Union, List
import json

_logger = logging.getLogger(__name__)

from ...api.workspace_data import get_files_tree
from ...client import Client
from ...types import UNSET
from ..exceptions import ApiConnectionError


def sync(
    os_workspace: Union[List[str], str],
    root: Union[None, str] = None,
    exclude_root: bool = False,
    recurse: bool = False,
    flat: bool = False,
    minimal: bool = False,
    client: Client = None,
):
    """
    # Get the tree (or a specific subtree) of a workspace filesystem from its ID

    ## Arguments
    - `os_workspace`: The filesystem ID
    - `root`: An workspace filesystem object ID to use as the tree root (usually a folder)
    - `exclude_root`: Whether to include the root object in the returned tree
    - `recurse`: Whether to recursively get all objects under the root, or only the direct children
    - `flat`: Whether to return the data as a flat list or a nested list structure
    - `minimal`: Whether to return only essential filesystem fields or all fields
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A list where each entry is a dictionary containing the fields of a workspace filesystem object.
    The dictionaries will also contain an entry '#path' containing the full filepath of the
    object as a String. Additionally, if flat is false, each dictionary will contain an entry '#children'
    containing a list of objects.

    ## Raises
    - `ApiConnectionError`: If the data could not be retrieved
    """
    if isinstance(os_workspace, list):
        os_workspace = ",".join(os_workspace)
    response = get_files_tree.sync_detailed(
        os_workspace=os_workspace,
        root=UNSET if not root else root,
        exclude_root=exclude_root,
        recurse=recurse,
        flat=flat,
        minimal=minimal,
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("get_files_tree", response, client)
    return json.loads(response.content)["data"]


async def asyncio(
    os_workspace: Union[List[str], str],
    root: Union[None, str] = None,
    exclude_root: bool = False,
    recurse: bool = False,
    flat: bool = False,
    minimal: bool = False,
    client: Client = None,
):
    """
    # Get asynchronously the tree (or a specific subtree) of a workspace filesystem from its ID

    ## Arguments
    - `os_workspace`: The filesystem ID
    - `root`: An workspace filesystem object ID to use as the tree root (usually a folder)
    - `exclude_root`: Whether to include the root object in the returned tree
    - `recurse`: Whether to recursively get all objects under the root, or only the direct children
    - `flat`: Whether to return the data as a flat list or a nested list structure
    - `minimal`: Whether to return only essential filesystem fields or all fields
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    A list where each entry is a dictionary containing the fields of a workspace filesystem object.
    The dictionaries will also contain an entry '#path' containing the full filepath of the
    object as a String. Additionally, if flat is false, each dictionary will contain an entry '#children'
    containing a list of objects.

    ## Raises
    - `ApiConnectionError`: If the data could not be retrieved
    """
    if isinstance(os_workspace, list):
        os_workspace = ",".join(os_workspace)
    response = await get_files_tree.asyncio_detailed(
        os_workspace=os_workspace,
        root=UNSET if not root else root,
        exclude_root=exclude_root,
        recurse=recurse,
        flat=flat,
        minimal=minimal,
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("get_files_tree", response, client)
    return json.loads(response.content)["data"]
