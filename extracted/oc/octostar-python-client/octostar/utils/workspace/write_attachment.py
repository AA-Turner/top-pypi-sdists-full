from typing import Dict, Optional, Union
from io import BytesIO
import json
import uuid
import logging
import httpx
import aiofiles
from urllib.parse import quote

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


DEFAULT_TIMEOUT = 120


def _entity_url(client: Client, os_workspace: str) -> str:
    """Build the entity creation endpoint URL."""
    base = client.get_base_url_v1()
    return f"{base}/api/v2/entities/{quote(os_workspace, safe='')}"


def _create_entity_sync(
    os_workspace: str,
    entity_fields: dict,
    file=None,
    content_type: str = None,
    client: "Client" = None,
) -> dict:
    """Create or upsert an entity via the multipart endpoint.

    Sends a multipart/form-data request with an ``entity`` JSON part
    and an optional ``file`` binary part.
    """
    url = _entity_url(client, os_workspace)
    headers = dict(client.get_headers())

    entity_json = json.dumps(entity_fields).encode("utf-8")

    should_close = False
    file_obj = None
    if file is not None:
        if isinstance(file, str):
            file_obj = open(file, "rb")
            should_close = True
        elif isinstance(file, bytes):
            file_obj = BytesIO(file)
        else:
            file_obj = file

    try:
        response = None
        try:
            for attempt in network_retry_strategy():
                with attempt:
                    parts = [("entity", ("entity", entity_json, "application/json"))]
                    if file_obj is not None:
                        if hasattr(file_obj, "seek"):
                            file_obj.seek(0)
                        parts.append(
                            (
                                "file",
                                (
                                    "file",
                                    file_obj,
                                    content_type or "application/octet-stream",
                                ),
                            )
                        )
                    with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                        response = http_client.post(url, files=parts, headers=headers)
                        response.raise_for_status()
        except Exception:
            raise ApiConnectionError("write_attachment", response, client)
    finally:
        if should_close and file_obj:
            file_obj.close()

    return response.json()


async def _create_entity_async(
    os_workspace: str,
    entity_fields: dict,
    file=None,
    content_type: str = None,
    client: "Client" = None,
) -> dict:
    """Create or upsert an entity via the multipart endpoint (async).

    Reads file content into memory for async compatibility, then sends a
    multipart/form-data request with an ``entity`` JSON part and an optional
    ``file`` binary part.
    """
    url = _entity_url(client, os_workspace)
    headers = dict(client.get_headers())

    entity_json = json.dumps(entity_fields).encode("utf-8")

    file_content = None
    if file is not None:
        if isinstance(file, str):
            async with aiofiles.open(file, "rb") as f:
                file_content = await f.read()
        elif isinstance(file, bytes):
            file_content = file
        else:
            file_content = file.read() if hasattr(file, "read") else file

    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                parts = [("entity", ("entity", entity_json, "application/json"))]
                if file_content is not None:
                    parts.append(
                        (
                            "file",
                            (
                                "file",
                                file_content,
                                content_type or "application/octet-stream",
                            ),
                        )
                    )
                async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = await http_client.post(url, files=parts, headers=headers)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("write_attachment", response, client)

    return response.json()


def sync(
    os_workspace: str,
    os_entity_uid: Union[str, None],
    entity_type: str,
    filetype: str,
    file: Union[str, bytes, BytesIO],
    fields: Optional[Dict] = None,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Write an attachment to a workspace for an attachable entity

    This includes creating or updating the local entity record as well as writing
    the attachment contents to storage so that they can be retrieved with
    read_attachment(). Note that using upsert_entity() only allows to save a record
    about an entity, not the attachment of said entity.

    ## Arguments
    - `os_workspace`: The workspace ID the entity should belong to
    - `os_entity_uid`: The entity ID
    - `entity_type`: The ontological entity type. Ensure this inherits from 'os_attachable'
    - `filetype`: The MIME type for the attachment
    - `file`: The attachment, either an UTF-8 string or a bytes-like
    - `fields`: Optional dict of additional entity fields to include on the entity.
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The record of the written entity

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ConnectionError`: If multiple (ambiguous) S3 urls are returned for this file
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    """
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

    entity_fields = {**(fields or {})}
    entity_fields.update(
        {
            "entity_id": os_entity_uid,
            "entity_type": entity_type,
            "os_item_content_type": filetype,
        }
    )
    return _create_entity_sync(
        os_workspace=os_workspace,
        entity_fields=entity_fields,
        file=file,
        content_type=filetype,
        client=client,
    )


async def asyncio(
    os_workspace: str,
    os_entity_uid: Union[str, None],
    entity_type: str,
    filetype: str,
    file: Union[str, bytes, BytesIO],
    fields: Optional[Dict] = None,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Write an attachment to a workspace for an attachable entity (async)

    This includes creating or updating the local entity record as well as writing
    the attachment contents to storage so that they can be retrieved with
    read_attachment(). Note that using upsert_entity() only allows to save a record
    about an entity, not the attachment of said entity.

    ## Arguments
    - `os_workspace`: The workspace ID the entity should belong to
    - `os_entity_uid`: The entity ID
    - `entity_type`: The ontological entity type. Ensure this inherits from 'os_attachable'
    - `filetype`: The MIME type for the attachment
    - `file`: The attachment, either an UTF-8 string or a bytes-like
    - `fields`: Optional dict of additional entity fields to include on the entity.
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The record of the written entity

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ConnectionError`: If multiple (ambiguous) S3 urls are returned for this file
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    """
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

    entity_fields = {**(fields or {})}
    entity_fields.update(
        {
            "entity_id": os_entity_uid,
            "entity_type": entity_type,
            "os_item_content_type": filetype,
        }
    )
    return await _create_entity_async(
        os_workspace=os_workspace,
        entity_fields=entity_fields,
        file=file,
        content_type=filetype,
        client=client,
    )
