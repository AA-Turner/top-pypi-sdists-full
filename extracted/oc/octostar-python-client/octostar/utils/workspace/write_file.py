from typing import Dict, Optional, Union
from io import BytesIO
import uuid
import logging

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from . import get_item_from_filepath
from . import get_filepath_from_item
from ..ontology import query_ontology
from .write_attachment import _create_entity_sync, _create_entity_async


def sync(
    os_workspace: str,
    filename: str,
    filetype: str,
    file: Union[str, bytes, BytesIO],
    os_entity_uid: Union[str, None] = None,
    os_parent_folder: Union[str, None] = None,
    ontology_name: str = None,
    fields: Optional[Dict] = None,
    entity_type: str = "os_file",
    client: Client = None,
):
    """
    # Write a file to a workspace

    This includes creating a local entity record representing the file as well as writing the file contents to storage so that they can be retrieved with read_file(). Note that using upsert_entity() only allows to save a record about a file, not the file content themselves.

    ## Arguments
    - `os_workspace`: The workspace ID in which to save the file
    - `filename`: The absolute or relative filepath for the file.
        It should generally begin with the workspace name followed by any folders and terminating
        with the filename. Any non-existing folder in-between will be created. It can also be relative to os_parent_folder argument
        if it begins with "./".
    - `filetype`: The MIME type for the file
    - `file`: The file contents, either an UTF-8 string or a bytes-like
    - `os_entity_uid`: The entity ID for the file. Only necessary in case of an update to the file contents
    - `ontology_name`: The name of the ontology
    - `fields`: Optional dict of additional entity fields to include on the entity.
    - `entity_type`: The ontological entity type for the file entity. Defaults to `os_file`.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The record of the written file

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ConnectionError`: If multiple (ambiguous) S3 urls are returned for this file
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    """

    def _write_file_nonrecursive(
        os_workspace,
        os_parent_folder,
        os_entity_uid,
        filename,
        entity_type,
        filetype,
        file,
        client,
        extra_fields=None,
    ):
        entity_fields = {**(extra_fields or {})}
        entity_fields.update(
            {
                "entity_id": os_entity_uid,
                "entity_type": entity_type,
                "entity_label": filename,
                "os_item_name": filename,
                "os_parent_folder": os_parent_folder,
                "os_item_type": entity_type,
            }
        )
        if filetype:
            entity_fields["os_item_content_type"] = filetype

        return _create_entity_sync(
            os_workspace=os_workspace,
            entity_fields=entity_fields,
            file=file,
            content_type=filetype,
            client=client,
        )

    if not client:
        client = get_default_client()
    if not ontology_name:
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    if not os_entity_uid:
        os_entity_uid = str(uuid.uuid4())
    filepath = filename.split("/")[:-1]
    filepath = [elem for elem in filepath if elem]
    workspace_label = query_ontology.sync(
        f"SELECT `entity_label` FROM `timbr`.`os_workspace` WHERE `entity_id`='{os_workspace}'",
        client=client,
    )
    if not workspace_label or not workspace_label[0]:
        raise ValueError("Workspace does not exist!")
    workspace_label = workspace_label[0]["entity_label"]
    if not filepath:
        file_folder = os_workspace
        lookup_base_path = None
    else:
        is_relative = len(filepath) > 0 and filepath[0] == "."
        if is_relative:
            filepath = filepath[1:]
            if os_parent_folder:
                os_parent_workspace = query_ontology.sync(
                    f"SELECT `os_workspace` FROM `timbr`.`os_folder` WHERE `entity_id`='{os_parent_folder}'",
                    client=client,
                )
                if not os_parent_workspace or not os_parent_workspace[0]:
                    raise ValueError("Parent folder does not exist!")
                if os_parent_workspace[0]["os_workspace"] != os_workspace:
                    raise ValueError("Parent folder is not in the same workspace!")
                file_folder = os_parent_folder
                lookup_base_path = get_filepath_from_item.sync(
                    os_workspace, os_parent_folder, ontology_name, client
                )
            else:
                file_folder = os_workspace
                lookup_base_path = workspace_label
        else:
            if filepath[0] != workspace_label:
                filepath.insert(0, workspace_label)
            filepath = filepath[1:]
            file_folder = os_workspace
            lookup_base_path = workspace_label
    folders_to_write = []
    if lookup_base_path:
        for i in range(len(filepath), 0, -1):
            try:
                lookup_path = lookup_base_path + "/" + "/".join(filepath[:i])
                file_entity = get_item_from_filepath.sync(
                    os_workspace, lookup_path, False, ontology_name, client
                )
                if isinstance(file_entity, list):
                    file_entity = file_entity[0]
                file_folder = file_entity["os_entity_uid"]
                break
            except ValueError:
                folders_to_write.insert(0, filepath[i - 1])
    if folders_to_write:
        for folder in folders_to_write:
            file_folder = _write_file_nonrecursive(
                os_workspace,
                file_folder,
                str(uuid.uuid4()),
                folder,
                "os_folder",
                None,
                None,
                client,
            )["os_entity_uid"]
    return _write_file_nonrecursive(
        os_workspace,
        file_folder,
        os_entity_uid,
        filename.rsplit("/", 1)[-1],
        entity_type,
        filetype,
        file,
        client,
        extra_fields=fields,
    )


async def asyncio(
    os_workspace: str,
    filename: str,
    filetype: str,
    file: Union[str, bytes, BytesIO],
    os_entity_uid: Union[str, None] = None,
    os_parent_folder: Union[str, None] = None,
    ontology_name: str = None,
    fields: Optional[Dict] = None,
    entity_type: str = "os_file",
    client: Client = None,
):
    """
    # Write asynchronously file to a workspace

    This includes creating a local entity record representing the file as well as writing the file contents to storage so that they can be retrieved with read_file(). Note that using upsert_entity() only allows to save a record about a file, not the file content themselves.

    ## Arguments
    - `os_workspace`: The workspace ID in which to save the file
    - `filename`: The absolute or relative filepath for the file.
        It should generally begin with the workspace name followed by any folders and terminating
        with the filename. Any non-existing folder in-between will be created. It can also be relative to os_parent_folder argument
        if it begins with "./".
    - `filetype`: The MIME type for the file
    - `file`: The file contents, either an UTF-8 string or a bytes-like
    - `os_entity_uid`: The entity ID for the file. Only necessary in case of an update to the file contents
    - `os_parent_folder`: The parent folder ID if filename is relative
    - `ontology_name`: The name of the ontology
    - `fields`: Optional dict of additional entity fields to include on the entity.
    - `entity_type`: The ontological entity type for the file entity. Defaults to `os_file`.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The record of the written file

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ConnectionError`: If multiple (ambiguous) S3 urls are returned for this file
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    """

    async def _write_file_nonrecursive(
        os_workspace,
        os_parent_folder,
        os_entity_uid,
        filename,
        entity_type,
        filetype,
        file,
        client,
        extra_fields=None,
    ):
        entity_fields = {**(extra_fields or {})}
        entity_fields.update(
            {
                "entity_id": os_entity_uid,
                "entity_type": entity_type,
                "entity_label": filename,
                "os_item_name": filename,
                "os_parent_folder": os_parent_folder,
                "os_item_type": entity_type,
            }
        )
        if filetype:
            entity_fields["os_item_content_type"] = filetype

        return await _create_entity_async(
            os_workspace=os_workspace,
            entity_fields=entity_fields,
            file=file,
            content_type=filetype,
            client=client,
        )

    if not client:
        client = get_default_client()
    if not ontology_name:
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    if not os_entity_uid:
        os_entity_uid = str(uuid.uuid4())
    filepath = filename.split("/")[:-1]
    filepath = [elem for elem in filepath if elem]
    workspace_label = await query_ontology.asyncio(
        f"SELECT `entity_label` FROM `timbr`.`os_workspace` WHERE `entity_id`='{os_workspace}'",
        client=client,
    )
    if not workspace_label or not workspace_label[0]:
        raise ValueError("Workspace does not exist!")
    workspace_label = workspace_label[0]["entity_label"]
    if not filepath:
        file_folder = os_workspace
        lookup_base_path = None
    else:
        is_relative = len(filepath) > 0 and filepath[0] == "."
        if is_relative:
            filepath = filepath[1:]
            if os_parent_folder:
                os_parent_workspace = await query_ontology.asyncio(
                    f"SELECT `os_workspace` FROM `timbr`.`os_folder` WHERE `entity_id`='{os_parent_folder}'",
                    client=client,
                )
                if not os_parent_workspace or not os_parent_workspace[0]:
                    raise ValueError("Parent folder does not exist!")
                if os_parent_workspace[0]["os_workspace"] != os_workspace:
                    raise ValueError("Parent folder is not in the same workspace!")
                file_folder = os_parent_folder
                lookup_base_path = await get_filepath_from_item.asyncio(
                    os_workspace, os_parent_folder, ontology_name, client
                )
            else:
                file_folder = os_workspace
                lookup_base_path = workspace_label
        else:
            if filepath[0] != workspace_label:
                filepath.insert(0, workspace_label)
            filepath = filepath[1:]
            file_folder = os_workspace
            lookup_base_path = workspace_label
    folders_to_write = []
    if lookup_base_path:
        for i in range(len(filepath), 0, -1):
            try:
                lookup_path = lookup_base_path + "/" + "/".join(filepath[:i])
                file_entity = await get_item_from_filepath.asyncio(
                    os_workspace, lookup_path, False, ontology_name, client
                )
                if isinstance(file_entity, list):
                    file_entity = file_entity[0]
                file_folder = file_entity["os_entity_uid"]
                break
            except ValueError:
                folders_to_write.insert(0, filepath[i - 1])
    if folders_to_write:
        for folder in folders_to_write:
            file_folder = (
                await _write_file_nonrecursive(
                    os_workspace,
                    file_folder,
                    str(uuid.uuid4()),
                    folder,
                    "os_folder",
                    None,
                    None,
                    client,
                )
            )["os_entity_uid"]
    return await _write_file_nonrecursive(
        os_workspace,
        file_folder,
        os_entity_uid,
        filename.rsplit("/", 1)[-1],
        entity_type,
        filetype,
        file,
        client,
        extra_fields=fields,
    )
