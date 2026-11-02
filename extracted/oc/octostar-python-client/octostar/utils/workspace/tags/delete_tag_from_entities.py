from typing import Dict, TypedDict, Union, List, Any, Optional
import os
import uuid
import logging

_logger = logging.getLogger(__name__)

from ....api.workspace_tags import delete_tag_from_entities
from ....models.entity import Entity as TagEntity
from ....client import Client, get_default_client
from ....types import UNSET
from ...exceptions import ApiConnectionError


class Entity(TypedDict):
    os_entity_uid: str
    entity_type: str


def sync(
    os_workspace: str,
    entities: List[Entity],
    tag_uid: str,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Remove a tag from a list of entities

    ## Arguments
    - `os_workspace`: The workspace ID of the tag
    - `entities`: The entities to tag, as a list of dictionaries
        Each dictionary must contain:
        - `os_entity_uid`: The unique ID for the entity
        - `entity_type`: The concept name for the entity
    - `tag_uid`: The unique ID of the tag
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    """
    assert len(entities) > 0
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    entities_to_untag = [
        TagEntity(entity["os_entity_uid"], entity["entity_type"]) for entity in entities
    ]
    response = delete_tag_from_entities.sync_detailed(
        os_workspace, tag_uid, json_body=entities_to_untag, client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("delete_tag_from_entities", response, client)


async def asyncio(
    os_workspace: str,
    entities: List[Entity],
    tag_uid: str,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Remove asynchronously a tag from a list of entities

    ## Arguments
    (Same as sync function)

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    """
    assert len(entities) > 0
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    entities_to_untag = [
        TagEntity(entity["os_entity_uid"], entity["entity_type"]) for entity in entities
    ]
    response = await delete_tag_from_entities.asyncio_detailed(
        os_workspace, tag_uid, json_body=entities_to_untag, client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("delete_tag_from_entities", response, client)
