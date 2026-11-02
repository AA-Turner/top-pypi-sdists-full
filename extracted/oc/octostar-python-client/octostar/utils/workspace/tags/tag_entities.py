from typing import TypedDict, List, Optional

from ...ontology import query_ontology
from ....api.workspace_tags import tag_entities
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
    existing_tag_uid: Optional[str] = None,
    tag_name: Optional[str] = None,
    new_tag_color: Optional[str] = None,
    tag_group: Optional[str] = None,
    new_tag_order: Optional[int] = -1,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Tag a list of entities with a tag

    The tag can be a new tag or an existing one.

    ## Arguments
    - `os_workspace`: The workspace ID in which to write the tag relationships (and the tag itself, if a new one is created)
    - `entities`: The entities to tag, as a list of dictionaries
        Each dictionary must contain:
        - `os_entity_uid`: The unique ID for the entity
        - `entity_type`: The concept name for the entity
    - `existing_tag_uid`: The unique ID of the tag, if an existing tag is used
    - `tag_name`: A label for the tag. If no tag with this name and group pair exists, it is created
    - `new_tag_color`: A color (in hex "#ffffff" format) for the tag, if a new tag is used
    - `tag_group`: A label used to group the tag with other tags. If no tag with this name and group pair exists, it is created
    - `new_tag_order`: The order of the tag within its group, if a new tag is used
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The tag record

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    - `ConnectionError`: If the tag returned from the response is ambiguous
    """
    assert len(entities) > 0
    assert bool(existing_tag_uid) ^ bool(tag_name)  # xor
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    entities_to_tag = [
        TagEntity(entity["os_entity_uid"], entity["entity_type"]) for entity in entities
    ]
    response = tag_entities.sync_detailed(
        os_workspace,
        tag=existing_tag_uid or tag_name,
        json_body=entities_to_tag,
        color=new_tag_color or UNSET,
        group=tag_group or UNSET,
        order=new_tag_order or UNSET,
        client=client,
    )
    if response.status_code != 200 or (
        response.parsed and response.parsed.get("status") != "success"
    ):
        raise ApiConnectionError("tag_entities", response, client)
    assigned_tag = list(
        {entity["os_entity_uid_to"] for entity in (response.parsed.get("data") or [])}
    )
    if not len(assigned_tag) == 1:
        raise ConnectionError(
            f"tag_entities failed, tag upsertion ambiguous or failed! Returned the following tags: "
            + str(assigned_tag)
        )
    assigned_tag = assigned_tag[0]
    full_assigned_tag = query_ontology.sync(
        f"SELECT * FROM dtimbr.os_tag WHERE entity_id='{assigned_tag}'",
        ontology_name=ontology_name,
        client=client,
    )
    return full_assigned_tag[0]


async def asyncio(
    os_workspace: str,
    entities: List[Entity],
    existing_tag_uid: Optional[str] = None,
    tag_name: Optional[str] = None,
    new_tag_color: Optional[str] = None,
    tag_group: Optional[str] = None,
    new_tag_order: Optional[int] = -1,
    ontology_name: str = None,
    client: Client = None,
):
    """
    # Tag asynchronously a list of entities with a tag

    The tag can be a new tag or an existing one.

    ## Arguments
    - `os_workspace`: The workspace ID in which to write the tag relationships (and the tag itself, if a new one is created)
    - `entities`: The entities to tag, as a list of dictionaries
        Each dictionary must contain:
        - `os_entity_uid`: The unique ID for the entity
        - `entity_type`: The concept name for the entity
    - `existing_tag_uid`: The unique ID of the tag, if an existing tag is used
    - `tag_name`: A label for the tag. If no tag with this name and group pair exists, it is created
    - `new_tag_color`: A color (in hex "#ffffff" format) for the tag, if a new tag is used
    - `tag_group`: A label used to group the tag with other tags. If no tag with this name and group pair exists, it is created
    - `new_tag_order`: The order of the tag within its group, if a new tag is used
    - `ontology_name`: The name of the ontology
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    The tag record

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology
    - `ApiConnectionError`: If the operation was unsuccessful on the server
    - `ConnectionError`: If the tag returned from the response is ambiguous
    """
    assert len(entities) > 0
    assert bool(existing_tag_uid) ^ bool(tag_name)  # xor
    if not ontology_name:
        if not client:
            client = get_default_client()
        ontology_name = client.ontology
    if ontology_name != client.ontology:
        raise NotImplementedError(
            "This operation is currently only supported on the current ontology!"
        )
    entities_to_tag = [
        TagEntity(entity["os_entity_uid"], entity["entity_type"]) for entity in entities
    ]
    response = await tag_entities.asyncio_detailed(
        os_workspace,
        tag=existing_tag_uid or tag_name,
        json_body=entities_to_tag,
        color=new_tag_color or UNSET,
        group=tag_group or UNSET,
        order=new_tag_order or UNSET,
        client=client,
    )
    if response.status_code != 200 or (
        response.parsed and response.parsed.get("status") != "success"
    ):
        raise ApiConnectionError("tag_entities", response, client)
    assigned_tag = list(
        {entity["os_entity_uid_to"] for entity in (response.parsed.get("data") or [])}
    )
    if not len(assigned_tag) == 1:
        raise ConnectionError(
            f"tag_entities failed, tag upsertion ambiguous or failed! Returned the following tags: "
            + str(assigned_tag)
        )
    assigned_tag = assigned_tag[0]
    full_assigned_tag = await query_ontology.asyncio(
        f"SELECT * FROM dtimbr.os_tag WHERE entity_id='{assigned_tag}'",
        ontology_name=ontology_name,
        client=client,
    )
    return full_assigned_tag[0]
