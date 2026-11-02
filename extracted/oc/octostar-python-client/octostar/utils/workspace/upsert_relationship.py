from typing import Dict, Union, Any, Optional
import uuid
import os
import logging

_logger = logging.getLogger(__name__)

from ..ontology import query_ontology
from . import upsert_entities
from ...types import Unset, UNSET
from ...client import Client, get_default_client


def sync(
    os_entity_uid_from: str,
    entity_type_from: str,
    os_entity_uid_to: str,
    entity_type_to: str,
    os_relationship_name: str,
    os_relationship_workspace: str,
    relationship_fields: Dict[str, Any] = None,
    os_relationship_uid: Optional[str] = None,
    allow_multi_cardinality: bool = True,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Create or update a local relationship between two entities, a source and a target

    ## Arguments
    - `os_entity_uid_from`: The source entity ID
    - `entity_type_from`: The source entity concept name
    - `os_entity_uid_to`: The target entity ID
    - `entity_type_to`: The target entity concept name
    - `os_relationship_name`: The name of the relationship, from source to target
    - `os_relationship_workspace`: The workspace for the relationship
    - `relationship_fields`: A dictionary of additional properties for the relationship
    - `os_relationship_uid`: The ID for the relationship. Only necessary in case of an update
    - `allow_multi_cardinality`: If True, allows multiple relationships from the same source, target, and relationship name. Otherwise, it updates them.
        Note this uniqueness is only applied per-workspace
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar

    ## Returns
    The created/updated relationship record

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology or for the given data
    - `ApiValidationError`: The server rejected the relationship (the
        underlying ``os_workspace_relationship`` record failed
        validation, the endpoint entity_type is a reserved keyword,
        etc.). The breakdown is exposed as structured attributes (see
        the class docstring for the shape of each):
        - `entity_errors`: ``list[{"entity_id": str, "error": str}]``
        - `invalid_fields`: ``dict[entity_id, list[field_name]]`` —
          drop these fields and re-upsert to recover
        - `reserved_keyword_entity_types`: ``set[str]`` of entity-type
          tokens flagged as reserved keywords
        Subclass of `ApiConnectionError` for backward compatibility.
    - `ApiConnectionError`: If the transport layer failed (network error,
        non-2xx response).
    - `ValueError`: If relationship uniqueness is enforced when the relationship is already not unique
    """
    if relationship_fields is None:
        relationship_fields = {}
    if not os_relationship_uid:
        os_relationship_uid = str(uuid.uuid4())
    if not client:
        client = get_default_client()
    if not ontology_name:
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    if not allow_multi_cardinality:
        check_existence_query = f"""SELECT os_entity_uid FROM dtimbr.os_workspace_relationship
            WHERE os_workspace='{os_relationship_workspace}' AND
                  os_relationship_name='{os_relationship_name}' AND 
                  os_entity_uid_from='{os_entity_uid_from}' AND 
                  os_entity_type_from='{entity_type_from}' AND 
                  os_entity_uid_to='{os_entity_uid_to}' AND
                  os_entity_type_to='{entity_type_to}' """
        result = query_ontology.sync(check_existence_query, client=client)
        if result:
            if len(result) > 1:
                raise ValueError(
                    "Cannot enforce cardinality = 1 when cardinality is already greater than 1!"
                )
            os_relationship_uid = result[0]["os_entity_uid"]
    result = upsert_entities.sync(
        os_relationship_workspace,
        [
            {
                "entity_type": "os_workspace_relationship",
                "os_entity_uid": os_relationship_uid,
                "fields": {
                    **relationship_fields,
                    "os_entity_uid_from": os_entity_uid_from,
                    "os_entity_type_from": entity_type_from,
                    "os_entity_uid_to": os_entity_uid_to,
                    "os_entity_type_to": entity_type_to,
                    "os_relationship_name": os_relationship_name,
                },
            }
        ],
        client=client,
    )
    return result[0]


async def asyncio(
    os_workspace_from: str,
    os_entity_uid_from: str,
    entity_type_from: str,
    os_workspace_to: Union[None, str],
    os_entity_uid_to: str,
    entity_type_to: str,
    os_relationship_name: str,
    relationship_fields: Dict[str, Any] = None,
    os_relationship_uid: Union[str, Unset] = UNSET,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # NOT IMPLEMENTED
    """
    raise NotImplementedError()
