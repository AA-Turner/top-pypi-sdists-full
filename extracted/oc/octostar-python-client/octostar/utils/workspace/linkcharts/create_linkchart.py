import json
import uuid
from typing import List, Optional, TypedDict

from ....client import Client, get_default_client
from ..write_attachment import _create_entity_async, _create_entity_sync

# Linkcharts are stored as os_file entities whose attachment body holds the
# graph settings JSON; this MIME type tells the linkchart how to read it.
LINKCHART_CONTENT_TYPE = "application/octostar-linkchart-settings+json"


def _normalize_nodes(nodes: List["Node"]) -> List[dict]:
    return [
        {
            **{
                k: v
                for k, v in node.items()
                if k not in ["entity_type", "entity_label", "entity_id"]
            },
            "entity_type": node["entity_type"],
            "entity_label": node["entity_label"],
            "entity_id": node["entity_id"],
        }
        for node in nodes
    ]


def _linkchart_v1_content(
    nodes: Optional[List["Node"]], edges: Optional[List["Edge"]]
) -> str:
    """Serialize nodes/edges into the LinkChart V1 saved-state the chart reads natively.

    Nodes become the top-level entity list; each edge resolves its endpoints to those
    entities and carries the label as a relationship. Duplicate nodes and edges are
    collapsed so the graph never receives colliding element ids.
    """
    normalized = _normalize_nodes(nodes) if nodes else []

    v1_nodes: List[dict] = []
    nodes_by_id: dict = {}
    # Key by entity_id alone so dedup matches the edge-endpoint lookup below.
    for node in normalized:
        entity_id = node["entity_id"]
        if entity_id in nodes_by_id:
            continue
        nodes_by_id[entity_id] = node
        v1_nodes.append(node)

    v1_edges: List[dict] = []
    seen_edges = set()
    for edge in edges or []:
        source = nodes_by_id.get(edge["from_node"])
        target = nodes_by_id.get(edge["to_node"])
        if source is None or target is None:
            continue
        relationship_name = edge["label"]
        key = (
            source["entity_type"],
            source["entity_id"],
            relationship_name,
            target["entity_type"],
            target["entity_id"],
        )
        if key in seen_edges:
            continue
        seen_edges.add(key)
        extras = {
            k: v for k, v in edge.items() if k not in ("from_node", "to_node", "label")
        }
        v1_edges.append(
            {
                **extras,
                "from": source,
                "to": target,
                "relationship": {"relationship_name": relationship_name},
            }
        )

    return json.dumps(
        {
            "format": "LinkChart V1",
            "nodes": v1_nodes,
            "edges": v1_edges,
        }
    )


def _linkchart_entity_fields(
    os_workspace: str,
    os_entity_uid: str,
    name: Optional[str],
    path: Optional[str],
    fields: dict,
) -> dict:
    return {
        **fields,
        "entity_id": os_entity_uid,
        "entity_type": "os_file",
        "entity_label": name,
        "os_item_name": name,
        "os_item_type": "os_file",
        "os_item_content_type": LINKCHART_CONTENT_TYPE,
        "os_parent_folder": os_workspace,
        "#os_path": path,
    }


class _NodeRequired(TypedDict):
    entity_type: str
    entity_label: str
    entity_id: str


class Node(_NodeRequired, total=False):
    """
    # Represents an Entity in the Linkchart

    ## Attributes:
        - `entity_type` (str): The type of the entity.
        - `entity_label` (str): The label of the entity.
        - `entity_id` (str): The unique identifier for the entity.
        - `**kwargs`: Any additional fields for the entity. Note that if this entity's ID exists in the data,
          the ontology fields will be fetched by the linkchart regardless of this attribute.
    """

    pass  # this allows further kwargs


class _EdgeRequired(TypedDict):
    from_node: str
    to_node: str
    label: str


class Edge(_EdgeRequired, total=False):
    """
    # Represents a Relationship between Two Entities in the Linkchart

    ## Attributes:
        - `from_node` (str): The unique identifier (entity_id) of the source node.
        - `to_node` (str): The unique identifier (entity_id) of the target node.
        - `label` (str): The label describing the relationship.
        - `**kwargs`: Any additional fields for the relationship. Note that if this relationship's ID exists in the data,
          the ontology fields will be fetched by the linkchart regardless of this attribute.
    """

    pass  # this allows further kwargs


def sync(
    os_workspace: str,
    name: Optional[str] = None,
    nodes: Optional[List[Node]] = None,
    edges: Optional[List[Edge]] = None,
    path: Optional[str] = None,
    os_entity_uid: Optional[str] = None,
    fields: dict = {},
    client: Optional[Client] = None,
):
    """
    # Create or update a local linkchart in a workspace

    ## Arguments
    - `os_workspace`: The workspace ID.
    - `name`: The name for the linkchart.
    - `nodes`: A list of entities to add to the linkchart.
    - `edges`: A list of edges to add to the linkchart.
    - `path`: The path to the linkchart file in the workspace, excluding the linkchart filename.
    - `os_entity_uid`: The entity ID for the linkchart. Only necessary in case of an update to the linkchart.
    - `fields`: Additional fields to include in the entity record.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The created/updated entity record.

    ## Raises
    - `NotImplementedError`: If the operation is not supported for the ontology.
    - `ConnectionError`: If the operation was unsuccessful on the server.
    """
    if not client:
        client = get_default_client()
    if not os_entity_uid:
        os_entity_uid = str(uuid.uuid4())

    content = _linkchart_v1_content(nodes, edges)
    return _create_entity_sync(
        os_workspace=os_workspace,
        entity_fields=_linkchart_entity_fields(
            os_workspace, os_entity_uid, name, path, fields
        ),
        file=content.encode("utf-8"),
        content_type=LINKCHART_CONTENT_TYPE,
        client=client,
    )


async def asyncio(
    os_workspace: str,
    name: Optional[str] = None,
    nodes: Optional[List[Node]] = None,
    edges: Optional[List[Edge]] = None,
    path: Optional[str] = None,
    os_entity_uid: Optional[str] = None,
    fields: dict = {},
    client: Optional[Client] = None,
):
    """
    Create or update asynchronously a local linkchart in a workspace.

    Args:
        os_workspace: The workspace ID.
        name: The name for the linkchart.
        nodes: A list of entities to add to the linkchart.
        edges: A list of edges to add to the linkchart.
        path: The path to the linkchart file in the workspace, excluding the linkchart filename.
        os_entity_uid: The entity ID for the linkchart. Only necessary in case of an update to the linkchart.
        fields: Additional fields to include in the entity record.
        client: The Client with which to connect to Octostar. If None, the default one is used.
    Returns:
        The created/updated entity record.

    Raises:
        NotImplementedError: If the operation is not supported for the ontology.
        ConnectionError: If the operation was unsuccessful on the server.
    """
    if not client:
        client = get_default_client()
    if not os_entity_uid:
        os_entity_uid = str(uuid.uuid4())

    content = _linkchart_v1_content(nodes, edges)
    return await _create_entity_async(
        os_workspace=os_workspace,
        entity_fields=_linkchart_entity_fields(
            os_workspace, os_entity_uid, name, path, fields
        ),
        file=content.encode("utf-8"),
        content_type=LINKCHART_CONTENT_TYPE,
        client=client,
    )
