from typing import Dict, Union, Any
import uuid
import os

from ...client import Client
from . import upsert_entities


def sync(
    os_workspace: str,
    os_entity_type: str,
    fields: Dict[str, Any],
    os_entity_uid: Union[str, None] = None,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Create or update a local entity in a workspace

    ## Arguments
    - `os_workspace`: The workspace ID
    - `os_entity_type`: The concept name for the entity
    - `fields`: A dictionary of fields for the entity, according to the concept definition in the ontology
    - `os_entity_uid`: The ID for the entity. Only necessary in case of an update
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The created/updated entity record

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiValidationError`: The server rejected the entity. The
        breakdown is exposed as structured attributes on the exception
        (see the class docstring for the shape of each):
        - `entity_errors`: ``list[{"entity_id": str, "error": str}]``
        - `invalid_fields`: ``dict[entity_id, list[field_name]]`` —
          drop these fields and re-upsert to recover
        - `reserved_keyword_entity_types`: ``set[str]`` of entity-type
          tokens flagged as reserved keywords
        Subclass of `ApiConnectionError` for backward compatibility.
    - `ApiConnectionError`: If the transport layer failed (network error,
        non-2xx response).
    """
    result = upsert_entities.sync(
        os_workspace,
        [
            {
                "os_workspace": os_workspace,
                "entity_type": os_entity_type,
                "os_entity_uid": os_entity_uid,
                "fields": fields,
            }
        ],
        ontology_name=ontology_name,
        client=client,
    )
    return result[0]


async def asyncio(
    os_workspace: str,
    os_entity_type: str,
    fields: Dict[str, Any],
    os_entity_uid: Union[str, None] = None,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Create or update asynchronously a local entity in a workspace

    ## Arguments
    - `os_workspace`: The workspace ID
    - `os_entity_type`: The concept name for the entity
    - `fields`: A dictionary of fields for the entity, according to the concept definition in the ontology
    - `os_entity_uid`: The ID for the entity. Only necessary in case of an update
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The created/updated entity record

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiValidationError`: The server rejected the entity. The
        breakdown is exposed as structured attributes on the exception
        (see the class docstring for the shape of each):
        - `entity_errors`: ``list[{"entity_id": str, "error": str}]``
        - `invalid_fields`: ``dict[entity_id, list[field_name]]`` —
          drop these fields and re-upsert to recover
        - `reserved_keyword_entity_types`: ``set[str]`` of entity-type
          tokens flagged as reserved keywords
        Subclass of `ApiConnectionError` for backward compatibility.
    - `ApiConnectionError`: If the transport layer failed (network error,
        non-2xx response).
    """
    result = await upsert_entities.asyncio(
        os_workspace,
        [
            {
                "os_workspace": os_workspace,
                "entity_type": os_entity_type,
                "os_entity_uid": os_entity_uid,
                "fields": fields,
            }
        ],
        ontology_name=ontology_name,
        client=client,
    )
    return result[0]
